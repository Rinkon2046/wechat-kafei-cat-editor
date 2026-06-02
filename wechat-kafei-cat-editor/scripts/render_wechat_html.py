#!/usr/bin/env python3
"""Render a Markdown-like Chinese article draft as WeChat-ready inline HTML."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


BODY_STYLE = (
    "margin:0;background:#fff;color:#1a1a1a;"
    "font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',"
    "'Microsoft YaHei',Arial,sans-serif;font-size:16px;line-height:1.7;"
)

SOURCE_KEYS = {
    "source": "source",
    "url": "source",
    "link": "source",
    "author": "author",
    "published": "published",
    "created": "created",
    "title": "title",
}

CHINESE_SOURCE_PATTERNS = [
    ("author", re.compile(r"^\s*作者[：:]\s*(.+?)\s*$")),
    ("source", re.compile(r"^\s*(?:链接|原文|出处|来源|转载自)[：:]\s*(.+?)\s*$")),
    ("reference", re.compile(r"^\s*(?:参考|引用|参考资料)[：:]\s*(.+?)\s*$")),
]

URL_RE = re.compile(r"https?://[^\s)）】>\"']+")


def inline_markup(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r'<strong style="color:#111;">\1</strong>', escaped)
    escaped = re.sub(r"`([^`]+?)`", r'<code style="font-family:Menlo,Consolas,monospace;font-size:0.92em;color:#111;background:#f7f7f7;padding:1px 4px;border-radius:4px;">\1</code>', escaped)
    return escaped


def is_list_item(line: str) -> bool:
    return bool(re.match(r"^\s*(?:[-*+]\s+|\d+[.、]\s+)", line))


def clean_list_item(line: str) -> str:
    return re.sub(r"^\s*(?:[-*+]\s+|\d+[.、]\s+)", "", line).strip()


def split_blocks(text: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    pending: list[str] = []

    def flush_paragraph() -> None:
        nonlocal pending
        if pending:
            blocks.append({"type": "p", "text": " ".join(pending).strip()})
            pending = []

    for raw_line in text.replace("\r\n", "\n").split("\n"):
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue
        image_match = re.match(r"^!\[(.*?)\]\((.*?)\)$", line)
        if image_match:
            flush_paragraph()
            blocks.append({"type": "image", "alt": image_match.group(1).strip(), "src": image_match.group(2).strip(), "caption": ""})
            continue
        if line.startswith("# "):
            flush_paragraph()
            blocks.append({"type": "h1", "text": line[2:].strip()})
        elif line.startswith("## "):
            flush_paragraph()
            blocks.append({"type": "h2", "text": line[3:].strip()})
        elif line.startswith(">"):
            flush_paragraph()
            blocks.append({"type": "quote", "text": line.lstrip(">").strip()})
        elif is_list_item(line):
            flush_paragraph()
            blocks.append({"type": "list", "text": clean_list_item(line)})
        else:
            pending.append(line)
    flush_paragraph()
    return blocks


def extract_article(blocks: list[dict[str, str]]) -> tuple[str, str, list[dict[str, str]]]:
    title = ""
    subtitle = ""
    rest: list[dict[str, str]] = []

    for block in blocks:
        if not title and block["type"] == "h1":
            title = block["text"]
            continue
        if not title and block["type"] == "p":
            title = block["text"]
            continue
        if title and not subtitle and block["type"] == "p":
            subtitle = block["text"]
            continue
        rest.append(block)

    return title or "未命名文章", subtitle, rest


def p(text: str, margin: str = "0 0 14px") -> str:
    return f'  <p style="margin:{margin};color:#444;line-height:1.7;">{inline_markup(text)}</p>'


def quote(text: str, margin: str = "0 0 24px", size: str = "18px") -> str:
    return (
        f'  <p style="margin:{margin};font-size:{size};font-weight:700;color:#111;'
        f'line-height:1.6;padding-left:14px;border-left:3px solid #111;">'
        f"{inline_markup(text)}</p>"
    )


def image_html(src: str, alt: str = "", caption: str = "") -> list[str]:
    escaped_src = html.escape(src.strip(), quote=True)
    escaped_alt = html.escape(alt.strip(), quote=True)
    parts = [
        f'  <p style="margin:24px 0 18px;text-align:center;">'
        f'<img src="{escaped_src}" alt="{escaped_alt}" style="display:block;width:100%;max-width:100%;height:auto;border-radius:8px;"></p>'
    ]
    if caption:
        parts.append(
            f'  <p style="margin:-8px 0 22px;color:#aaa;font-size:12px;text-align:center;line-height:1.6;">'
            f"{inline_markup(caption)}</p>"
        )
    return parts


def render(
    title: str,
    subtitle: str,
    blocks: list[dict[str, str]],
    citations: list[str],
    images: dict[str, list[dict[str, str]]],
    eyebrow: str,
    footer: str,
) -> str:
    parts: list[str] = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{html.escape(title)}</title>",
        "</head>",
        f'<body style="{BODY_STYLE}">',
        '<section style="max-width:660px;margin:0 auto;padding:36px 20px 52px;background:#fff;box-sizing:border-box;">',
        "",
        f'  <p style="margin:0 0 10px;color:#aaa;font-size:12px;letter-spacing:2px;">{html.escape(eyebrow)}</p>',
        f'  <h1 style="margin:0 0 14px;color:#111;font-size:26px;line-height:1.3;font-weight:700;letter-spacing:-0.2px;">{inline_markup(title)}</h1>',
    ]

    if subtitle:
        parts.append(
            f'  <p style="margin:0 0 28px;color:#666;font-size:15px;line-height:1.7;'
            f'padding-bottom:24px;border-bottom:1px solid #eee;">{inline_markup(subtitle)}</p>'
        )
    else:
        parts.append('  <p style="margin:0 0 28px;padding-bottom:8px;border-bottom:1px solid #eee;"></p>')

    for item in images.get("START", []):
        parts.extend(image_html(item["src"], item.get("alt", ""), item.get("caption", "")))

    section_number = 0
    for block in blocks:
        kind = block["type"]
        text = block.get("text", "")
        if kind == "h1":
            continue
        if kind == "h2":
            section_number += 1
            parts.extend(
                [
                    "",
                    f'  <p style="margin:40px 0 4px;color:#aaa;font-size:11px;letter-spacing:2px;">{section_number:02d}</p>',
                    f'  <h2 style="margin:0 0 14px;color:#111;font-size:20px;font-weight:700;line-height:1.4;'
                    f'padding-bottom:12px;border-bottom:1px solid #eee;">{inline_markup(text)}</h2>',
                    "",
                ]
            )
            for item in images.get(text, []):
                parts.extend(image_html(item["src"], item.get("alt", text), item.get("caption", "")))
        elif kind == "quote":
            parts.append(quote(text, margin="0 0 24px" if section_number == 0 else "0 0 14px", size="18px" if section_number == 0 else "17px"))
        elif kind == "image":
            parts.extend(image_html(block["src"], block.get("alt", ""), block.get("caption", "")))
        elif kind == "list":
            parts.append(p(f"**•** {text}", margin="0 0 10px"))
        else:
            parts.append(p(text, margin="0 0 12px"))

    if citations:
        parts.extend(
            [
                "",
                '  <p style="margin:40px 0 4px;color:#aaa;font-size:11px;letter-spacing:2px;">REF</p>',
                '  <h2 style="margin:0 0 14px;color:#111;font-size:20px;font-weight:700;line-height:1.4;padding-bottom:12px;border-bottom:1px solid #eee;">参考与引用</h2>',
            ]
        )
        for item in citations:
            parts.append(p(item, margin="0 0 8px"))

    parts.extend(
        [
            "",
            f'  <p style="margin:40px 0 0;padding-top:20px;border-top:1px solid #eee;color:#ccc;font-size:12px;text-align:center;line-height:1.6;">{html.escape(footer)}</p>',
            "",
            "</section>",
            "</body>",
            "</html>",
        ]
    )
    return "\n".join(parts)


def read_citations(path: str | None) -> list[str]:
    if not path:
        return []
    text = Path(path).read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]


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
        for key, pattern in CHINESE_SOURCE_PATTERNS:
            match = pattern.match(line)
            if match:
                found[key] = strip_quotes(match.group(1))
    return found


def auto_detect_citations(text: str) -> list[str]:
    merged = {**parse_frontmatter(text), **scan_source_lines(text)}
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


def read_images(path: str | None) -> dict[str, list[dict[str, str]]]:
    if not path:
        return {}
    images: dict[str, list[dict[str, str]]] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        columns = line.split("\t")
        if len(columns) < 3:
            raise ValueError("Each image row must be: after<TAB>section-title-or-START<TAB>image-path<TAB>caption")
        mode, target, src = [value.strip() for value in columns[:3]]
        caption = columns[3].strip() if len(columns) > 3 else ""
        if mode != "after":
            raise ValueError('Only "after" image insertion is supported.')
        images.setdefault(target or "START", []).append({"src": src, "caption": caption, "alt": target})
    return images


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a WeChat-ready article HTML file.")
    parser.add_argument("input", help="Markdown or plain-text article draft")
    parser.add_argument("output", help="Output HTML file")
    parser.add_argument("--citations", help="Optional text file, one citation per line")
    parser.add_argument("--auto-citations", action="store_true", help="Automatically detect citation/source lines from the input")
    parser.add_argument("--images", help="Optional TSV: after<TAB>section-title-or-START<TAB>image-path<TAB>caption")
    parser.add_argument("--section-only", action="store_true", help="Write only the <section>...</section> fragment for direct WeChat copy/paste")
    parser.add_argument("--eyebrow", default="公众号一键编辑 · 图文整理")
    parser.add_argument("--footer", default="图文整理版 · 适合公众号发布 / 内部分享 / 社群转发")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    blocks = split_blocks(source)
    title, subtitle, rest = extract_article(blocks)
    citations = read_citations(args.citations) if args.citations else (auto_detect_citations(source) if args.auto_citations else [])
    output = render(title, subtitle, rest, citations, read_images(args.images), args.eyebrow, args.footer)
    if args.section_only:
        match = re.search(r"(<section[\s\S]*?</section>)", output)
        if not match:
            raise RuntimeError("Could not extract section fragment from rendered HTML.")
        output = match.group(1)
    Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
