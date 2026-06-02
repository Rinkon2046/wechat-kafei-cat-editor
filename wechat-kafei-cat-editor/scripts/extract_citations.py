#!/usr/bin/env python3
"""Extract simple citation lines from a Markdown/plain-text article draft."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SOURCE_KEYS = {
    "source": "source",
    "url": "source",
    "link": "source",
    "author": "author",
    "published": "published",
    "created": "created",
    "title": "title",
}

CHINESE_PATTERNS = [
    ("author", re.compile(r"^\s*作者[：:]\s*(.+?)\s*$")),
    ("source", re.compile(r"^\s*(?:链接|原文|出处|来源|转载自)[：:]\s*(.+?)\s*$")),
    ("reference", re.compile(r"^\s*(?:参考|引用|参考资料)[：:]\s*(.+?)\s*$")),
]

URL_RE = re.compile(r"https?://[^\s)）】>\"']+")


def strip_quotes(value: str) -> str:
    value = value.strip().strip(",")
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value.strip()


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    metadata: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        normalized = key.strip().lower()
        if normalized in SOURCE_KEYS:
            metadata[SOURCE_KEYS[normalized]] = strip_quotes(value)
    return metadata


def scan_source_lines(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in text.splitlines()[:80]:
        for key, pattern in CHINESE_PATTERNS:
            match = pattern.match(line)
            if match:
                found[key] = strip_quotes(match.group(1))
    return found


def build_citation(metadata: dict[str, str], source_lines: dict[str, str], text: str) -> list[str]:
    merged = {**metadata, **source_lines}
    author = merged.get("author", "")
    source = merged.get("source") or merged.get("reference", "")
    published = merged.get("published", "")

    if source:
        parts = []
        if author:
            parts.append(author)
        if published:
            parts.append(f"发布于 {published}")
        parts.append(f"链接：{source}" if source.startswith("http") else source)
        return ["原文来源：" + "，".join(parts)]

    urls = URL_RE.findall(text)
    if urls:
        return [f"参考链接：{urls[0]}"]

    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract citation lines from an article draft.")
    parser.add_argument("input", help="Input Markdown/plain-text article")
    parser.add_argument("output", help="Output citations text file")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    citations = build_citation(parse_frontmatter(text), scan_source_lines(text), text)
    Path(args.output).write_text("\n".join(citations) + ("\n" if citations else ""), encoding="utf-8")


if __name__ == "__main__":
    main()
