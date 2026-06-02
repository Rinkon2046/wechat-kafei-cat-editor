# WeChat Kafei Cat Editor

把中文微信公众号初稿整理成可直接复制进微信编辑器的精排 HTML，并生成 2.35:1 微信封面和 Ian 风格咖啡猫正文配图。

设计者：Rinkon

## What It Does

- 将 Markdown、纯文本、newsletter 初稿或来源页改写成完整公众号文章。
- 自动提炼标题、导语、核心判断、编号章节、总结和可选引用。
- 生成兼容微信公众号编辑器的内联样式 HTML。
- 为每篇文章规划并生成一张必需的 2.35:1 微信封面。
- 内置 Ian 风格咖啡猫手绘解释图系统，用于正文关键概念配图。
- 自动识别来源、作者、链接、参考资料等引用信号；没有来源时直接省略引用部分。

## Install

Clone this repository, then copy the skill folder into your Codex skills directory:

```bash
git clone https://github.com/YOUR_USERNAME/wechat-kafei-cat-editor.git
mkdir -p ~/.codex/skills
cp -R wechat-kafei-cat-editor/wechat-kafei-cat-editor ~/.codex/skills/
```

Restart Codex after installation.

## Usage

In Codex, ask:

```text
Use $wechat-kafei-cat-editor to turn this draft into a polished WeChat article with a cover, Kafei Cat illustrations, and copy-ready HTML.
```

Or in Chinese:

```text
用 $wechat-kafei-cat-editor 把这篇初稿整理成微信公众号文章，生成 2.35:1 封面、正文咖啡猫配图和可复制 HTML。
```

## Repository Layout

```text
.
├── README.md
├── examples/
│   ├── prompts.md
│   └── images/
├── wechat-kafei-cat-editor/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   └── scripts/
├── NOTICE.md
└── LICENSE
```

The installable skill is the nested `wechat-kafei-cat-editor/` directory.

## Output Files

The skill typically produces:

- Final WeChat-ready HTML
- Section-only HTML snippet for one-click copying
- 2.35:1 cover PNG
- Body illustration PNGs
- Image insertion table

## Notes

The bundled images in `wechat-kafei-cat-editor/assets/` are style references and examples. For real article work, the skill should create fresh metaphors and new image prompts based on the current article rather than reuse the examples as final illustrations.
