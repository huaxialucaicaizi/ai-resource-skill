# [中文](#ai-resource-skill) | [English](#ai-resource-skill-en)

---

# AI Resource Skill

**零基础中文用户的 AI 信息源导航 + 专属清单 Skill。**

作者：[华夏路菜菜子：前大厂 AI 产品增长，现 AI 创业者](https://github.com/huaxialucaicaizi)  
License：MIT

---

## 这是什么

很多人想学 AI，却不知道该看哪些公众号、博主、官方动态和课程，也不知道国内能不能打开、要不要花钱。

这个仓库做两件事：

1. **按「你想做什么」整理好的信息源名单**（行业讯息 / 产品动态 / 场景教程 / 系统学习），每条都标好语言、访问、付费、适合谁和查询日期。  
2. **一个 Agent Skill**：你告诉助手「我是谁、想学什么」，它只根据仓库里的数据，生成一份给你的清单。第一次用**不需要 API key，也不需要联网抓取**。

> v1 已完成：名单 + 标签 + 避坑标准 + Skill + 链接巡检。  
> **周报 / digest 不在 v1**，计划在 v2。

数据查询日期：**2026-11-20**（Asia/Shanghai）。看不到的字段一律写「未知」，不估算。

---

## 一键安装（Skill）

### 方式 A：`npx skills add`（文档约定）

遵循 [vercel-labs/skills](https://github.com/vercel-labs/skills) 文档中的安装约定（`npx skills add owner/repo` 会发现仓库内 `skills/*/SKILL.md`）：

```bash
npx skills add huaxialucaicaizi/ai-resource-skill
```

- **约定来源**：vercel-labs/skills 的 `docs/commands.md` / `docs/creating-skills.md`（本仓库 skill 路径为 `skills/ai-resource-guide/SKILL.md`）。  
- **本环境验证**：已用 `npx skills add <本地仓库路径> --list` 确认能发现 **ai-resource-guide**。针对 GitHub shorthand 的完整安装，请在本机网络下再跑一次上面的命令。

### 方式 B：git clone 到本地 skills 目录（通用）

```bash
# Claude Code 示例
git clone https://github.com/huaxialucaicaizi/ai-resource-skill.git ~/.claude/skills/ai-resource-skill

# Cursor 示例
git clone https://github.com/huaxialucaicaizi/ai-resource-skill.git ~/.cursor/skills/ai-resource-skill
```

克隆后即可离线阅读 `data/sources.yaml` 与 `skills/ai-resource-guide/`。无需 API key。

---

## Skill 与路线

| 名称 | 使用场景 / 对你有什么帮助 |
| --- | --- |
| **AI Resource Guide · AI 信息源导航** | 你说出身份和目标（例如「我是运营，想学做 PPT」），助手从本仓库数据生成带标签的专属信息源清单，并提醒访问限制与付费点。 |

### 你想做什么

| 路线 | 使用场景 / 对你有什么帮助 | 去哪看 |
| --- | --- | --- |
| **想跟上行业新闻** · Follow industry news | 跟中文科技 / AI 媒体 | [行业讯息](sources/industry.md) |
| **想知道新产品新模型** · Track new products and models | 看官方 X 动态（需注意访问限制） | [产品动态](sources/products.md) |
| **想学会做 PPT** · Learn AI for PPT | 短教程、办公场景 | [场景教程](sources/tutorials.md) |
| **想学会写代码 / vibe coding** · Learn vibe coding | 零基础用 AI 做应用 | [场景教程](sources/tutorials.md) |
| **想学会做视频 / 设计** · Learn AI video and design | AIGC 视频与创作流程 | [场景教程](sources/tutorials.md) |
| **想学会数据分析** · Learn AI for data analysis | Excel / 表格 / 数据分析 | [场景教程](sources/tutorials.md) |
| **想系统学 AI** · Learn AI systematically | 官方/公开课程；先读避坑清单 | [系统学习](sources/learning.md) · [课程避坑](sources/course-pitfalls.md) |

入口总表：[sources/routes.md](sources/routes.md)

结构化数据：[data/sources.yaml](data/sources.yaml)（另有 [data/sources.json](data/sources.json)）  
未知项：[data/unknown-items.md](data/unknown-items.md)

---

## 四类信息源（v1）

| 分类 | 条数（含名单中的备选） | 说明 |
| --- | ---: | --- |
| 行业讯息 | 8 | 中文科技 / AI 媒体（公众号等） |
| 产品动态 | 8 | X 官方公司号与对应负责人（正表） |
| 场景教程 | 15 | PPT / vibe coding / 视频设计 / 数据分析（含备选） |
| 系统学习 | 8 | 免费或官方课程入口 |

每条源都包含：语言、国内能否直接访问、免费/付费、适合谁、数据（观测数字与口径）、查询日期。

---

## 课程避坑清单

只写**判断标准**（红旗信号、付钱前要问的问题、如何找免费替代），**不点名**任何机构、课程或个人。  
→ [sources/course-pitfalls.md](sources/course-pitfalls.md)

---

## 和同类项目有什么不同

以下对比只陈述已公开的事实，方便你选型。

### 与 zarazhangrui/follow-builders

| | 本仓库 v1 | follow-builders（据 2026-11-20 调研阅读） |
| --- | --- | --- |
| 入口 | 按「你想做什么」分路线 | 追踪固定英文 builder / 播客 / 博客名单 |
| 信息源类型 | 行业讯息、产品动态、场景教程、系统学习 | 以 X 帖、播客、两家官方博客为主 |
| 标签 | 语言、国内能否访问、免费/付费、适合谁、数据与查询日期 | 无上述统一字段 |
| 主产出 | 根据身份和目标生成**个人源名单** | 每日/每周**简报**（中心抓取 feed，用户侧摘要） |
| 课程避坑 | 有（只讲标准） | 无 |
| 首次用名单 | 读仓库数据即可，无需 API key | 对话出摘要也可不配 key；安装需 clone 等；中心抓取需作者侧密钥 |
| 链接巡检 | CI 检查名单 URL | 侧重中心 feed 生成，而非学习资源链接巡检 |
| 周报 | **计划 v2**，v1 不做 | v1 核心即是日报/周报 |

### 与 AmbroseX/Awesome-AISourceHub

Awesome-AISourceHub 是一份按**平台**分栏的中文 AI 信息源名单（README 表格约 128 条量级，MIT），多数条目有一句话备注；**没有**按「你想做什么」的路线、没有统一的国内访问/适合谁/查询日期标签，也**没有** Agent Skill 或系统化的课程避坑清单。

本仓库 v1 不追求「再列一份更长的平台大全」，而是：路线入口 + 四类结构 + 完整标签 + 可安装 Skill + 链接巡检。

---

## 自动链接检查

`.github/workflows/link-check.yml`：每周定时 + 可手动触发。  
脚本 `scripts/check_links.py` 读取 `data/sources.yaml` 中的 URL，写出 `reports/` 报告，并在 Actions Job Summary 中汇总。  

说明：x.com / 小红书 / 抖音等常拦截机器人；**HTTP 403 / 429 记为「需人工确认」**，不当作死链。无需配置 Secrets。

本地运行：

```bash
pip install pyyaml
python scripts/check_links.py
```

---

## 仓库结构（简）

```text
data/sources.yaml          # 结构化名单（唯一数据源）
data/unknown-items.md      # 未知项清单
sources/                   # 按分类生成的可读 Markdown + 路线 + 避坑
skills/ai-resource-guide/  # Agent Skill（含离线 references/sources.yaml）
scripts/check_links.py     # 链接检查
.github/workflows/         # 每周链接巡检
```

---

## 贡献与原则

- 不新增未经观测的数字、粉丝数、排名或链接。  
- 补数据请写明查询日期与口径；未知就写未知。  
- 不要加入与「花叔」相关的账号或课程。

---

## 安装验证说明

- `npx skills add huaxialucaicaizi/ai-resource-skill`：符合 vercel-labs/skills 已文档化的 GitHub shorthand 约定；本环境已用本地路径 `npx skills add … --list` 核对能发现 `ai-resource-guide`。  
- `git clone … ~/.claude/skills` / `~/.cursor/skills`：通用目录约定，已在文档中写明；不依赖第三方 registry。

---

# AI Resource Skill (EN)

**AI information-source navigation for zero-basis Chinese learners, plus a personal-list Agent Skill.**

Author line (GitHub): 华夏路菜菜子：前大厂 AI 产品增长，现 AI 创业者  
License: MIT

---

## What this is

This repository provides:

1. A curated directory of AI information sources organized by **what you want to do** (industry news / product updates / scenario tutorials / systematic learning), with tags for language, mainland access, free/paid, audience, observed data, and query date.  
2. An **Agent Skill** that turns your identity + goal into a personalized list **drawn only from the repo data**. First run needs **no API key and no network fetch**.

> v1 ships the directory, tags, course-judgment checklist, Skill, and link checker.  
> A **weekly digest is planned for v2** (not in v1).

Observation date: **2026-11-20** (Asia/Shanghai). Unknown fields stay unknown — no estimates.

---

## Install (one-liners)

### A. Documented `npx skills add` convention

```bash
npx skills add huaxialucaicaizi/ai-resource-skill
```

Per [vercel-labs/skills](https://github.com/vercel-labs/skills) docs (`npx skills add owner/repo` discovers `skills/*/SKILL.md`). This repo’s skill lives at `skills/ai-resource-guide/SKILL.md`.

### B. git clone into agent skill folders

```bash
git clone https://github.com/huaxialucaicaizi/ai-resource-skill.git ~/.claude/skills/ai-resource-skill
git clone https://github.com/huaxialucaicaizi/ai-resource-skill.git ~/.cursor/skills/ai-resource-skill
```

Offline-friendly; no API key required to read the bundled list.

---

## Skill & routes

| Name | When it helps / what you get |
| --- | --- |
| **AI Resource Guide · AI 信息源导航** | Tell the agent who you are and what you want (e.g. ops → PPT). It returns a tagged source list from repo data only, with access/paid caveats. |

| Route | When it helps | Open |
| --- | --- | --- |
| **想跟上行业新闻** · Follow industry news | Chinese tech/AI media | [industry](sources/industry.md) |
| **想知道新产品新模型** · Track new products and models | Official X accounts (access limits apply) | [products](sources/products.md) |
| **想学会做 PPT** · Learn AI for PPT | Short tutorials | [tutorials](sources/tutorials.md) |
| **想学会写代码 / vibe coding** · Learn vibe coding | Zero-basis AI coding | [tutorials](sources/tutorials.md) |
| **想学会做视频 / 设计** · Learn AI video and design | AIGC video workflows | [tutorials](sources/tutorials.md) |
| **想学会数据分析** · Learn AI for data analysis | Sheets / Excel / analytics | [tutorials](sources/tutorials.md) |
| **想系统学 AI** · Learn AI systematically | Official/public courses + pitfalls checklist | [learning](sources/learning.md) · [pitfalls](sources/course-pitfalls.md) |

Data: [data/sources.yaml](data/sources.yaml) · Unknowns: [data/unknown-items.md](data/unknown-items.md)

---

## Categories (v1 counts)

| Category | Count | Notes |
| --- | ---: | --- |
| 行业讯息 (Industry) | 8 | Chinese media accounts |
| 产品动态 (Products) | 8 | Official X accounts (primary table) |
| 场景教程 (Tutorials) | 15 | PPT / coding / video / data (incl. alternates) |
| 系统学习 (Learning) | 8 | Official/public course entries |

---

## vs similar projects (factual)

### vs zarazhangrui/follow-builders

Our v1 is a **goal-based, tagged personal source list** (plus course-judgment criteria and URL health checks). follow-builders (as read on 2026-11-20) centers on a **maintainer-generated feed** of English builders/podcasts/blogs and a **daily/weekly digest**. We intentionally **do not** ship digest in v1 (planned for v2).

### vs AmbroseX/Awesome-AISourceHub

Awesome-AISourceHub is a **platform-grouped** Chinese source list (MIT) with short notes; it is not organized by learner goals, does not use our full tag set, and has no Agent Skill / systematic paid-course judgment checklist. We focus on routes + tags + Skill + link checks rather than a longer platform catalog.

---

## Link checking

Weekly GitHub Action + `scripts/check_links.py`. Soft-fail reporting; **403/429** on bot-hostile hosts (e.g. x.com, Xiaohongshu, Douyin) → **manual confirm**, not “dead”. No secrets required.

---

## Principles

- Never invent numbers, ranks, or URLs.  
- Keep 未知 / 待核实 when unverified.  
- No accounts/courses related to 「花叔」.
