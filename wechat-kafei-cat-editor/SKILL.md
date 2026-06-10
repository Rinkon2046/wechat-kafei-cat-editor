---
name: wechat-kafei-cat-editor
description: 将中文微信公众号文章初稿整理成可一键复制的精排 HTML，匹配内置黑白灰编辑风格，包含编辑改写、主旨提炼、自动引用识别、必需的 2.35:1 微信封面图，以及内置 Ian 风格咖啡猫手绘解释配图。适用于用户上传或提供公众号草稿、Markdown/纯文本文章、newsletter 初稿，或提到“微信公众号文章”“公众号文章”“微信公众号一键编辑”“公众号排版”“生成公众号 HTML”“公众号封面”“公众号配图”“咖啡猫配图”“猫咪插图”等类似需求。自动从文章内容或元数据中识别引用/参考信息；如果无法识别，直接省略引用部分，不要要求用户补充参考来源。
---

# 微信公众号咖啡猫编辑

设计者：Rinkon

这个技能把原始文章文本处理成一篇完成度较高的微信公众号文章：包括编辑后的正文、提炼后的结构、内联样式 HTML，以及内置 Ian 风格咖啡猫配图。使用本技能时不需要再单独调用其他插图技能。

## 工作流

1. 从用户上传的文件或粘贴的文本中读取草稿。
2. 在改写前先提取并总结原文：识别主题、目标读者、中心论点、支撑论据、可复用案例、薄弱/重复部分，以及需要引用支撑的主张。
3. 在排版前先决定文章形态。对于来源页、案例页、产品页或报告，不要简单保留原结构；先选择微信公众号文章角度，压缩宣传模块，并识别读者自然愿意读完的 3-5 个章节。
4. 从文章内容和元数据中自动识别引用。如果没有明确来源，不要要求用户补充参考资料，直接省略引用部分。
5. 先改文字再排版：压缩重复内容，理顺因果逻辑，优化小标题，提炼主旨，把松散长段落改成适合公众号阅读的节奏。
6. 将文章规范化为：标题、副标题/导语、开篇核心判断、编号章节、结尾总结，以及可选引用。
7. 做编辑完整性检查：最终稿应该像一篇完成的公众号文章，而不是清理过的网页、幻灯片大纲或资料堆。如果仍像来源材料，先继续改写，再进入配图。
8. 基于编辑后的文章制定配图策略，而不是套模板。先识别文章的认知锚点：核心判断、转折点、输入/输出闭环、对比关系、角色交接、瓶颈、清单和实用结论。不要平均每个标题配一张图；只选择手绘图能让读者更快理解的位置。
9. 先规划一张基于全文的必需微信封面图，比例为 `2.35:1`，封面图必须包含文章标题；再规划正文配图组。每张图生成前都要写一个简短 shot plan：插入位置、主题、核心意思、结构类型、原创物理隐喻、咖啡猫正在做什么、建议物件，以及 3-6 个简短中文手写标注。
10. 如果图像生成可用，在生成最终 HTML 之前先生成咖啡猫 PNG。每张图单独生成；不要把多张插图拼成一张拼贴。生成后检查每张图，并根据视觉匹配度分配角色，而不是按生成顺序机械命名：封面、章节流程图、章节概念图、对比图或总结图。不得用 PIL、SVG、HTML canvas、Mermaid、Graphviz 或其他程序化绘图脚本生成的矩形框、箭头流程图、线框图、占位示意图冒充最终咖啡猫插图；程序化脚本只可用于尺寸规范化、拼接质检图或临时草稿，不可进入最终 HTML。
11. 执行下方图片 QA 规则。如果咖啡猫只是装饰、图片像 PPT/流程图、画面太满、中文过多或错误、隐喻不匹配文章、输出复刻了内置示例构图，或视觉上像简陋占位图/低完成度线框图，就重生成或局部编辑。
12. 除非生成图已经满足比例，否则用 `scripts/normalize_cover.py` 将封面图规范化为精确 `2.35:1`。
13. 渲染 HTML 前执行配图密度检查。如果文章读起来配图过少或过密，就增减章节图。
14. 生成一个使用内联样式、兼容微信公众号编辑器的独立 HTML 文件。用户需要直接复制粘贴时，同时生成 section-only HTML 片段，并默认把本地图片转为 `data:image/...;base64` 内嵌图片，避免从本地 HTML 复制到微信公众号编辑窗口时只复制文字、丢失图片。
15. 保持文章版式与 `assets/reference-style.html` 一致：660px 居中的白色内容栏、黑白灰配色、小字号拉开字距的 eyebrow、强标题、克制副标题、编号章节、细分割线、左边框强调块，以及有简单边距的插图。
16. 保存输出包，并告诉用户文件路径：最终 HTML、可选复制版 HTML 片段、封面图、章节配图和图片插入表。

## 内容提取工作流

写最终文章前，先在内部整理一份紧凑的编辑 brief：

- **主题**：这篇文章真正讲什么？
- **目标读者**：谁应该关心？他们已经知道什么？
- **核心论点**：读者最应该记住的一句话是什么？
- **论证链条**：哪 3-7 个点让这个论点可信？
- **保留**：强案例、数字、隐喻、具名工具和具体工作流。
- **裁剪或压缩**：重复解释、松散轶事、宣传式结尾和跑题内容。
- **编辑角度**：让文章值得读的公众号框架，例如案例拆解、方法总结、检查清单、风险提醒或决策指南。
- **识别到的引用**：来源元数据、作者行、来源 URL、转载/翻译/改编说明、明确参考列表或外部链接。

然后把文章改写成下面的结构：

1. 标题
2. 副标题/导语
3. 作为引用块的开篇核心判断
4. 简短开场背景
5. 编号章节
6. 需要时加入实用 takeaway/清单
7. 总结
8. 如有来源则加入引用

## 引用识别

默认不要向用户索要引用信息。应自动识别。

把以下内容视为引用信号：

- Markdown/YAML frontmatter 字段：`source`、`url`、`link`、`author`、`published`、`created`、`title`。
- 常见中文来源行：`作者：`、`链接：`、`来源：`、`原文：`、`出处：`、`转载自：`、`参考：`。
- 文章头部或正文中与来源语境搭配出现的 URL 域名。
- 标题为 `参考`、`引用`、`资料来源`、`参考资料`、`来源` 的已有章节。
- 用户提供的说明，例如“引用了...”“参考了...”“来源是...”。

识别到来源时，将其格式化为 HTML 引用部分中的短行，例如：

```text
原文来源：作者名，发布于 YYYY-MM-DD，链接：https://example.com/...
```

如果只识别到 URL，使用：

```text
参考链接：https://example.com/...
```

如果没有识别到任何引用信号，直接省略引用部分。不要停下来要求用户补充参考来源。

## 编辑改写规则

- 保留用户的核心观点和主张。
- 提升微信公众号可读性：缩短段落、理清转场、强化小标题，减少重复句式。
- 提炼一个开篇核心判断，并渲染为 blockquote（`> ...`），使其成为开头的左边框强调块。
- 优先使用短而好记的标题，把细节放进副标题。除非用户明确要求这种风格，否则不要把所有数字、产品名和结果都塞进 H1。
- 将散乱编号行改成连贯列表。
- 不要编造事实、引用、数据、具名来源或引语。
- 如果某句话依赖未提供的来源，要么作为用户观点保留，要么在引用步骤中请求来源。

### 来源页和案例稿规则

当来源是公司网站、客户案例、产品落地页、新闻稿或活动页时：

- 从编辑视角改写，不要沿用页面所有者的导航结构。
- 删除或压缩重复 CTA、产品菜单、页脚链接、相关案例卡片、口号和模块标签，除非它们直接支撑文章。
- 保留具体证据：数字、具名角色、前后工作流、业务约束和来源中的直接主张。
- 将结构压缩到最小可读形态。典型客户案例应成为 3-5 个编号章节加 takeaway，而不是逐模块复刻来源页。
- 每个章节只承担一个任务：问题、工作流、结果、意义或 takeaway。避免相邻章节重复“AI 提效”这类同一论点。
- 初稿后自检：“如果来源页消失，这篇文章是否仍然成立？”如果不成立，继续改写，直到它能作为独立文章阅读。

## 咖啡猫配图系统

创建 Ian 风格咖啡猫文章配图。目标不是商业插画、PPT 信息图、可爱吉祥物海报或正式系统图，而是把文章里的关键判断、工作流、结构、状态或隐喻，变成一张清爽、怪诞、可读的手绘解释图，像一个敏锐的产品思考者在白纸上随手画出的草图。

### 视觉 DNA

- 使用纯白背景。不要米色纸张、暖灰、纹理、渐变、阴影、噪点、复古纸感或复杂场景。
- 使用极简黑色手绘线稿，线条细、略微抖动。避免精致矢量图、 glossy 效果、3D、照片写实、密集颜色和真实 App 截图。
- 保持大量留白。主体大约占画面的 40%-60%，至少保留 35% 安静空白区域。
- 只在有助于理解时加入少量中文手写批注。优先 3-6 个标注；除非文章确实需要，绝不超过 8 个。每个标注通常为 2-8 个汉字。
- 黑色用于主体线稿和咖啡猫，橙色用于主路径/流向/箭头，红色用于警告/问题/结果，蓝色用于次级说明、AI/系统状态或反馈。蓝色不是必须；颜色必须克制。
- 不要在左上角放类型标签或说明标题，例如“流程图”“系统架构图”“方法论”“路线图”“常见坑”或“Workflow”。
- 一张图只解释一个核心动作、结构、状态或隐喻。如果图片需要大量盒子和箭头才能说清楚，就简化或拆分。

### 咖啡猫 IP

咖啡猫是固定视觉叙述者，必须出现在每张封面和正文配图里。

- 咖啡猫是一只黑色实心手绘小猫，白色圆眼、短爪、短腿、细尾巴、空白但认真的表情、略不规则的身体轮廓，可带轻微马克笔填充纹理。
- 咖啡猫不是吉祥物、贴纸、装饰或可爱卡通。它是画面里正在执行概念工作的冷静操作员。
- 咖啡猫必须承担核心动作：拉、扛、塞、捞、压、称、缝、剪、拧、守、推、接、拆包、贴标签、回收、盖章、打气、开门、修补或连接。
- 如果去掉咖啡猫后，画面隐喻仍然完整成立，这张图就是失败的。要重写提示词，让咖啡猫成为使概念可见的行动主体。
- 不要画成橙色加菲猫式版权形象、商业吉祥物、儿童卡通猫、穿复杂衣服的猫、闪亮大眼猫或过度卖萌的猫。

### 配图策略

文章改写完成后、图像生成前，先制定紧凑的配图计划。

每张候选图都要决定：

- **插入位置**：精确的 `START` 或 `##` 标题目标。
- **主题**：这张图支撑的章节或全文概念。
- **核心意思**：这张图要让读者更容易理解的一句话。
- **结构类型**：从 Workflow、系统局部、前后对比、角色状态、概念隐喻、方法分层、地图路线、2-4 格小漫画中选择一种。
- **原创物理隐喻**：为这篇文章发明的一个具体低科技场景。
- **咖啡猫动作**：咖啡猫正在做什么，如何解释这个概念。
- **建议物件**：来自文章或隐喻的 3-5 个物件。
- **中文标注**：3-6 个简短手写标注。

选择认知锚点，而不是装饰性的阅读间隔。强候选包括：核心判断、两个断点、输入/输出闭环、前后对比、路径或交接、优先级/过滤、“一源多用”、常见坑、角色状态变化和结尾框架。

### 原创隐喻规则

每张封面和正文配图都必须从当前文章的标题、主旨、章节论点、具名实体、工作流和隐喻中重新构图。

使用这个三步方法：

1. 把抽象概念翻译成物理动作：卡住、漏掉、变重、分拣、发酵、打开、折叠、拆包、回流、修补、过滤、盖章或改道。
2. 把系统翻译成一两个低科技物件：纸箱、抽屉、旧机器、漏斗、秤、邮筒、门、井、梯子、水管、线团、闸门、转盘、黑盒、打孔器、压机、晾衣绳、怪工位、瓶子、桥、路标、仓库、桶、阀门或分层罐。
3. 让咖啡猫执行动作：卡在机器里、拉错线、守门、搬材料、称信号、修漏口、剪路径、给判断盖章或打开通路。

除非用户明确要求使用某张参考图，否则不要复制或轻微改名旧示例构图。尤其不要默认复用这些已有场景：信息井、压想法机器、三层信号漏斗、系统承重架、内容坑路线、钩子到知识库到核心课路线、结尾工具箱、一源多用鱼板、流量/信任/转化分叉、发酵瓶、内容机器反馈闭环，或两个断点传送带。

`assets/` 下的内置图片只用于风格校准：线条密度、留白、颜色克制和咖啡猫参与方式。它们不是最终配图，除非用户明确要求占位图或指定复用，否则不要插入新文章。

如果图像生成不可用，说明限制，并提供配图计划和占位文件名。不要把无关的内置参考图作为最终文章图片插入，也不要改用 PIL、SVG、HTML canvas、Mermaid、Graphviz 等脚本绘制低完成度替代图。宁可交付无图 HTML + shot plan，也不要把粗糙占位图插进最终文章。

## 配图规划和密度

根据文章结构规划配图，不要从固定最低数量出发。

默认密度：

- 短文，1-2 个主要章节或约 900 个汉字以内：一张必需封面，加 1 张用于解释概念的正文图。
- 中等案例文章，3-5 个主要章节或约 900-2200 个汉字：一张必需封面，加 2-3 张正文图。
- 长方法论/框架文章，5 个以上主要章节或超过约 2200 个汉字：一张必需封面，加 3 张正文图；如果结尾是清单或框架，可额外加一张总结图。

对于商业案例，优先为每个独立业务场景或工作流簇配一张正文图。如果文章有三个场景章节，例如“前/中/后”“输入/处理/输出”或三个部门工作流，默认应有三张正文图，除非章节非常短或重复。

每张正文图都必须有存在理由：

- 应该解释工作流、对比、决策点、角色交接、信息流或框架。
- 必须内容具体：使用当前章节的具体概念、产品名、角色、屏幕、信号、指标或业务场景，而不是泛泛套用咖啡猫模板。
- 应插入到它解释的章节附近，不要集中堆在开头。
- 应贡献新的视觉想法；避免三张图都在画同一种表格、漏斗、路径、纸箱堆或传送带隐喻。
- 配图说明要短且带解释性，说清楚图片为什么重要，而不是复述章节标题。
- 如果插图像拥挤的产品图、课程页、正式流程图或企业信息图，就简化或替换。咖啡猫图片应该像编辑放在正文旁边的手绘解释。

图片生成后，先检查视觉输出，再命名和插入：

- 选择最强的、基于全文的、可分享的、像标题图的图片作为 `article-slug-cover-235.png`，即使它不是第一张生成的。
- 将工作流重或细节重的图片用作章节插图。
- 拒绝只是在模仿内置示例、却没有反映当前文章内容的图片。
- 拒绝咖啡猫只是站在图旁边的图片。
- 如果生成图文字过多、中文不清晰、裁切差、背景不是白色、太像可爱吉祥物，或隐喻与章节不匹配，就重生成或省略。
- 复制到输出包时保留原始生成文件。

渲染前检查计划中的 `images.tsv`：

- 必须包含一行 `START` 封面。
- 中长案例文章不应只有一张正文图，除非有明确理由。
- 章节图目标必须与真实 `##` 标题完全匹配。
- 最终图片数量应让滚动阅读感觉均衡：避免文章前三分之一之后出现很长的纯文本段落。

## 必需微信封面

总是先生成微信封面，再生成章节配图。

- 比例：`2.35:1`。
- 推荐画布：`1645x700`、`2350x1000` 或任何等效 `2.35:1` PNG。
- 来源：使用优化后的全文，而不只是标题。
- 目的：让文章在微信中更适合分享，并用视觉总结中心论点。
- 内容：包含文章核心张力、关键概念、一组短封面标题/标注，以及正在演绎中心概念的咖啡猫。封面仍应像一个单一手绘场景，而不是塞满文章文案的横幅。
- 标题：封面图必须包含文章标题，通常使用 1-2 行短标题即可。标题应放在纯留白区域，或以极轻量方式融入画面，不能使用大面积白色/彩色底板、卡片、遮罩或不透明背景覆盖原始插图内容；如果需要提升可读性，优先缩小字号、移动位置、换行或使用细下划线，而不是加厚背景块。
- 风格：使用上面的咖啡猫配图系统。
- 文件命名：除非用户要求其他名称，否则保存为 `article-slug-cover-235.png`。
- HTML 插入：用 `--images images.tsv` 的 `START` 目标将封面插入文章开头附近，或在副标题后写入 `![cover](path)`。
- 封面身份规则：微信封面是文章正文中第一张可见的横版咖啡猫插图，通常放在标题/副标题之后、开篇核心判断或第一段正文之前。不要把封面只当成外部分享素材；同一个 `article-slug-cover-235.png` 必须是 `images.tsv` 中的 `START` 图片，也是最终 HTML 正文里的第一张图。
- 比例强制：需要时运行 `scripts/normalize_cover.py input.png article-slug-cover-235.png`，将图片填充/裁切为 `1645x700`。

对于一篇微信公众号文章，默认：

- 每篇文章都有一张必需的 `2.35:1` 微信封面 PNG；
- 短文额外加 1 张章节 PNG；
- 中等案例、多场景文章或框架较重的文章额外加 2-3 张章节 PNG；
- 较长方法论文章额外加 3 张章节 PNG，并可选 1 张总结图；
- 章节图可根据插入位置使用 `16:9`、`4:3` 或竖图，但封面必须保持 `2.35:1`。

生成图里的可见文字要短。长文章内容必须留在 HTML 里，不要写进 PNG。

保存插图资源时，使用稳定命名，例如：

```text
article-slug-cover-235.png
article-slug-section-01.png
article-slug-summary.png
```

## 生成提示词模式

每张正文图使用或改写下面的提示词：

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
Kafei Cat, a small solid-black hand-drawn cat with round white eyes, short paws, tiny legs, a thin tail, blank serious expression, slightly uneven body shape, subtle marker-fill texture. Kafei Cat must perform the core conceptual action, not decorate the scene. Make it serious, deadpan, and slightly bizarre, not cute. Do not draw an orange Garfield-like copyrighted cat; this is an original black coffee cat.

Theme:
[章节配图主题]

Structure type:
[Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 2-4 格小漫画]

Core idea:
[这张图要说明的一句话]

Composition:
[咖啡猫在哪里、正在做什么、主要物件是什么、信息或动作如何流动]

Suggested elements:
[物件 1] / [物件 2] / [物件 3] / [物件 4]

Chinese handwritten labels:
[标注 1] / [标注 2] / [标注 3] / [标注 4] / [可选标注 5]

Color use:
Black for main line art and Kafei Cat. Orange for main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

封面图使用或改写下面的提示词：

```text
Generate one standalone 2.35:1 horizontal WeChat cover illustration, recommended canvas 1645x700 or equivalent.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, shadows, paper texture, complex background, commercial vector style, PPT infographic look, cute mascot poster, children's illustration, photorealism, 3D, or realistic UI.

Kafei Cat required:
A small solid-black original coffee cat with round white eyes, short paws, tiny legs, thin tail, blank serious expression, slightly uneven body shape, and subtle marker-fill texture. It must act out the article's central tension, not pose beside a title.

Article title:
[标题]

Subtitle / thesis:
[副标题或开篇核心判断]

Cover idea:
[全文的核心张力或 takeaway]

Composition:
[一个适合分享的场景：咖啡猫动作 + 中心物件 + 流向或对比]

Short cover labels:
[3-5 个简短中文标注，可包含一个短标题]

Constraints:
Make it a cover, but keep it hand-drawn and editorial. Include the article title in 1-2 short lines, placed in clean blank space. Do not use an opaque title background card, white plate, colored block, or mask that covers the illustration. Do not cram article copy into the image. Do not make a corporate banner, poster, PPT slide, or cute mascot scene. Preserve the 2.35:1 composition with breathing room at both ends. The image should work as the first visible illustration inside the WeChat article.
```

可用修复提示词：

```text
Edit the provided image. Remove only the handwritten title "[要删除的文字]" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

```text
Regenerate this illustration with the same core meaning and simple layout, but make Kafei Cat more central to the conceptual action. Kafei Cat should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, and not cute.
```

```text
Regenerate with fewer boxes, fewer arrows, no title, and more white space. Turn the abstract flow into a physical hand-drawn scene where Kafei Cat performs the key action. Keep only 3-5 short Chinese handwritten labels.
```

## 样式规则

- 所有文章内容只使用内联 CSS。
- 页面背景保持白色，内容宽度约 `660px`。
- 使用系统中文字体：`-apple-system`、`BlinkMacSystemFont`、`PingFang SC`、`Helvetica Neue`、`Microsoft YaHei`、`Arial`、`sans-serif`。
- 使用参考样式中的核心颜色：`#111`、`#1a1a1a`、`#444`、`#666`、`#aaa`、`#ccc`、`#eee`，以及偶尔使用的警示红 `#c0392b`。
- 当草稿有主要章节时，使用 `01`、`02`、`03` 这类章节编号。
- 全文默认左对齐，不要把正文、标题、引用块、列表、图片说明或页尾设置为居中；图片本身可以居中显示。
- 所有普通正文段落使用 `font-size:16px;line-height:1.6;`，并首行缩进两个中文字符，可用内联 CSS 如 `font-size:16px;line-height:1.6;text-indent:2em;text-align:left;`。仅应用于正文段落；不要缩进标题、副标题/导语、引用块、列表行、图片说明、表格、引用区或 UI 式标签。
- 将关键结论渲染为左边框强调块。
- 插入生成插图时使用全宽图片，圆角不超过 8px，需要时加入克制的图片说明。渲染脚本默认会把存在于本地的图片路径转成 `data:image/...;base64`；只有在明确需要保留路径时才使用 `--no-inline-images`。
- 如果有引用，把它放在页脚附近，标题为“参考与引用”。
- 不要添加交互式 JavaScript、外部 CSS、远程资源或装饰 SVG。

## 脚本生成

正文编辑完成且图片列表确定后，使用 `scripts/render_wechat_html.py`：

```bash
python3 scripts/render_wechat_html.py input.md output.html --citations citations.txt --images images.tsv
python3 scripts/render_wechat_html.py input.md output.html --auto-citations --images images.tsv
python3 scripts/render_wechat_html.py input.md copy-section.html --images images.tsv --section-only
python3 scripts/render_wechat_html.py input.md copy-section.html --images images.tsv --section-only --no-inline-images
python3 scripts/extract_citations.py input.md citations.txt
python3 scripts/normalize_cover.py raw-cover.png article-slug-cover-235.png
```

支持的输入约定：

- 第一个 `# Heading` 或第一个非空行会成为标题。
- 标题后的第一个普通段落会成为副标题/导语。
- `>` 引用块会成为左边框强调块。
- `##` 标题会成为编号章节。
- 普通段落会成为 `16px`、`1.6` 行距、左对齐且带两个中文字符首行缩进的微信公众号正文段落，例如 `font-size:16px;line-height:1.6;text-align:left;text-indent:2em;`。
- 以 `- ` 开头的行或 Markdown 编号列表会成为紧凑段落列表行。
- `**bold**` 会渲染为行内加粗。
- `![alt](path)` 会在精确位置嵌入图片。
- `--images images.tsv` 可按章节标题注入生成插图。每行 TSV 为：`after<TAB>section-title-or-START<TAB>image-path<TAB>caption`。
- 默认情况下，本地图片会被转成 base64 data URI，以便从浏览器预览页复制到微信公众号编辑器时尽量连同图片一起带入。若要生成较小的 HTML 或保留相对路径，使用 `--no-inline-images`。
- `--auto-citations` 会从输入中识别来源元数据或来源行；没有来源时自动省略引用。
- `--citations citations.txt` 显式提供引用行，并优先于自动识别。
- `--section-only` 只写出 `<section>...</section>` 片段，适合直接复制到微信公众号编辑器。
- `--eyebrow "TEXT"` 覆盖顶部 eyebrow。
- `--footer "TEXT"` 覆盖末尾 footer 行。

对于 DOCX、PDF 或富文本上传，先用合适的文档技能/工具提取文章文本，再把 Markdown 风格草稿传入脚本。

## 输出包

优先将这些文件保存到一起：

- `article-slug.html`：完整独立预览 HTML。
- `article-slug-copy.html`：section-only 复制粘贴片段。
- `article-slug-cover-235.png`：精确 `2.35:1` 微信封面。
- `article-slug-section-01.png` 等：正文配图。
- `images.tsv`：图片插入映射。

告诉用户：微信正式发布前可能需要单独上传图片。

## 最终质量检查

回复用户前确认：

- 文章有清晰标题、副标题、开篇核心判断和编号章节。
- 标题没有过载；让标题变重的细节已经移到副标题或开篇判断。
- 文章读起来像微信公众号文章，而不是清理过的网页、新闻稿、幻灯片大纲或来源资料摘要。
- 改写后的文本保留了用户立场，没有编造事实。
- 除非用户要求保留，否则重复内容和宣传式结尾已被压缩。
- 案例文章通常已压缩为 3-5 个主章节加 takeaway；来源导航、CTA 文案、页脚链接和相关卡片内容没有被当作正文。
- 封面图片精确为 `2.35:1`。
- 封面图包含文章标题，标题没有使用不透明背景底板、卡片或遮罩覆盖插图；如果标题影响插图主体，已通过缩小、上移、换行或放入留白区解决。
- 正文配图解释概念，而不是随机装饰；它们使用 Ian 风格咖啡猫编辑草图，而不是拥挤的企业信息图。
- 正文配图数量匹配文章结构：中等案例文章通常有 2-3 张正文图，而不是只有一张。
- 除非有明确插入理由，每张正文图都是 16:9；封面保持 `2.35:1`。
- 每张生成图都有干净纯白背景、以黑色手绘线稿为主、克制的红/橙/蓝标注，以及足够留白。
- 咖啡猫在每张图中都是核心动作主体，而不是角落装饰或可爱吉祥物。
- 没有任何生成图像橙色加菲猫式版权形象、商业吉祥物、儿童插画、正式流程图、课程页或 PPT 信息图。
- 没有任何正文插图看起来像简陋占位图、低完成度线框图、几何卡片拼接、程序化矩形框箭头图或临时草稿；如果插图缺少物理隐喻、咖啡猫动作不承担解释功能、留白过大但信息不足，就重生成。
- 没有任何生成图在左上角出现“流程图”“系统架构图”“方法论”“路线图”“常见坑”或“Workflow”等类型标题。
- 中文标注短、少、可读；长解释保留在 HTML 正文中，而不是写进 PNG。
- 每张图的隐喻都是为当前文章重新发明的，没有复刻内置示例场景。
- 已经检查生成图，并按视觉角色分配，而不是按生成顺序机械命名。
- `images.tsv` 包含 `START` 封面行，章节目标与真实 `##` 标题完全匹配。
- `START` 封面行指向的图片，就是最终 HTML 正文第一张可见图片。
- 引用只在从文章/元数据自动识别到或用户明确提供时加入。
- 普通正文段落为 `16px` 字号、`1.6` 行距、左对齐，并首行缩进两个中文字符；标题、副标题、引用块、列表行、图片说明、表格和引用区不缩进。
- 最终 HTML 使用内联样式，不包含 JavaScript 或外部 CSS。
- 当用户需要直接粘贴到微信时，已提供便于复制的 section-only HTML 片段，并确认其中的本地图片已内嵌为 `data:image/...;base64` 或已另行提供可在微信中访问的远程图片地址。

## 手动兜底

如果草稿需要大量编辑重构，使用 `assets/reference-style.html` 作为视觉参考，手写 HTML。保持所有样式内联，并保留相同层级：

1. Eyebrow
2. H1 标题
3. 带底部分割线的副标题/导语
4. 开篇强调
5. 引入段落
6. 开篇/章节咖啡猫插图
7. 编号章节
8. 结尾总结
9. 如有来源则加入引用
10. Footer
