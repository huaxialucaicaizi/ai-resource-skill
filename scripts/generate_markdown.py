#!/usr/bin/env python3
"""Generate human-readable markdown from data/sources.yaml."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sources.yaml"
OUT = ROOT / "sources"


def load():
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


def fmt_data(data: dict) -> str:
    lines = []
    for k, v in data.items():
        if k == "榜单明细" and isinstance(v, list):
            if not v:
                lines.append(f"- **{k}**：无")
                continue
            lines.append(f"- **{k}**：")
            for row in v:
                parts = [f"{kk}={vv}" for kk, vv in row.items()]
                lines.append(f"  - {'; '.join(parts)}")
        elif isinstance(v, list):
            lines.append(f"- **{k}**：")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"- **{k}**：{v}")
    return "\n".join(lines)


def write_category(doc, category: str, filename: str, intro: str):
    items = [s for s in doc["sources"] if s["category"] == category]
    lines = [
        f"# {category}",
        "",
        f"> 查询日期：{doc['meta']['query_date']}（{doc['meta']['timezone']}）。数字与字段均来自观测记录，未知项保持「未知」。",
        "",
        intro,
        "",
        f"本类共 **{len(items)}** 条。",
        "",
    ]
    for s in items:
        status = s.get("status")
        title = s["name"] + (f"（{status}）" if status else "")
        lines.append(f"## {title}")
        lines.append("")
        if s.get("account_id"):
            lines.append(f"- **账号 / ID**：{s['account_id']}")
        if s.get("handle"):
            lines.append(f"- **Handle**：{s['handle']}")
        if s.get("scene"):
            lines.append(f"- **场景**：{s['scene']}")
        if s.get("platforms"):
            lines.append(f"- **平台**：{'、'.join(s['platforms'])}")
        lines.append(f"- **语言**：{s['语言']}")
        lines.append(f"- **国内能否直接访问**：{s['国内能否直接访问']}")
        lines.append(f"- **免费/付费**：{s['免费/付费']}")
        lines.append(f"- **适合谁**：{s['适合谁']}")
        lines.append(f"- **查询日期**：{s['查询日期']}")
        if s.get("urls"):
            lines.append("- **链接**：")
            for u in s["urls"]:
                lines.append(f"  - {u}")
        elif s.get("url_notes"):
            lines.append(f"- **链接**：无（{s['url_notes']}）")
        if s.get("url_notes") and s.get("urls"):
            lines.append(f"- **链接说明**：{s['url_notes']}")
        lines.append("- **数据**：")
        for dl in fmt_data(s["数据"]).splitlines():
            lines.append("  " + dl if dl.startswith("-") else dl)
        # fix nesting — rewrite data block simply
        lines = lines  # placeholder
        lines.append("")
    # Regenerate cleanly without the nesting bug
    lines = [
        f"# {category}",
        "",
        f"> 查询日期：{doc['meta']['query_date']}（{doc['meta']['timezone']}）。数字与字段均来自观测记录，未知项保持「未知」。",
        "",
        intro,
        "",
        f"本类共 **{len(items)}** 条。",
        "",
    ]
    for s in items:
        status = s.get("status")
        title = s["name"] + (f"（{status}）" if status else "")
        lines.append(f"## {title}")
        lines.append("")
        if s.get("account_id"):
            lines.append(f"- **账号 / ID**：{s['account_id']}")
        if s.get("handle"):
            lines.append(f"- **Handle**：{s['handle']}")
        if s.get("scene"):
            lines.append(f"- **场景**：{s['scene']}")
        if s.get("platforms"):
            lines.append(f"- **平台**：{'、'.join(s['platforms'])}")
        lines.append(f"- **语言**：{s['语言']}")
        lines.append(f"- **国内能否直接访问**：{s['国内能否直接访问']}")
        lines.append(f"- **免费/付费**：{s['免费/付费']}")
        lines.append(f"- **适合谁**：{s['适合谁']}")
        lines.append(f"- **查询日期**：{s['查询日期']}")
        if s.get("urls"):
            lines.append("- **链接**：")
            for u in s["urls"]:
                lines.append(f"  - {u}")
        if s.get("url_notes"):
            lines.append(f"- **链接说明**：{s['url_notes']}")
        if s.get("ppt_match"):
            lines.append(f"- **PPT 对口程度**：{s['ppt_match']}")
        if s.get("copywriting_match"):
            lines.append(f"- **写文案对口程度**：{s['copywriting_match']}")
        tuts = s.get("tutorials") or []
        if tuts:
            lines.append("- **保姆教程**：")
            for t in tuts:
                lines.append(
                    f"  - {t.get('title')}｜{t.get('link')}｜日期 {t.get('date')}｜赞 {t.get('likes')}｜工具 {t.get('tools')}｜{t.get('free_or_paid')}｜查询 {t.get('query_date', '')}"
                )
        elif s.get("category") == "场景教程":
            lines.append("- **保姆教程**：暂无已核实条目")
        lines.append("- **数据**：")
        lines.append("")
        lines.append(fmt_data(s["数据"]))
        lines.append("")
    path = OUT / filename
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print("wrote", path)


def write_routes(doc):
    lines = [
        "# 你想做什么？",
        "",
        "先选一条路线，再打开对应分类里的信息源。每条源都标了语言、国内能否直接访问、免费/付费、适合谁、数据和查询日期。",
        "",
        "| 路线 | 使用场景 / 对你有什么帮助 | 对应分类 | 可读名单 |",
        "| --- | --- | --- | --- |",
    ]
    file_map = {
        "行业讯息": "industry.md",
        "产品动态": "products.md",
        "场景教程": "tutorials.md",
        "系统学习": "learning.md",
    }
    for r in doc["routes"]:
        fname = file_map[r["category"]]
        scene = r.get("scene_filter")
        extra = f"（场景：{scene}）" if scene else ""
        lines.append(
            f"| **{r['name_zh']}** · {r['name_en']} | {r['help_zh']} | {r['category']}{extra} | [{fname}](./{fname}) |"
        )
    lines += [
        "",
        "## 怎么用",
        "",
        "1. 想清楚你现在最想解决的一件事（例如：学会做 PPT）。",
        "2. 打开上表对应的名单，先看「适合谁」「国内能否直接访问」「免费/付费」。",
        "3. 若要系统上课，先读 [课程避坑清单](./course-pitfalls.md)。",
        "4. 也可以把身份和目标告诉 AI 助手，用本仓库的 Skill 生成专属清单（见 README）。",
        "",
        "## 四类信息源一览",
        "",
        "| 分类 | 条数 | 文件 |",
        "| --- | ---: | --- |",
    ]
    counts = {}
    for s in doc["sources"]:
        counts[s["category"]] = counts.get(s["category"], 0) + 1
    for cat, fname in file_map.items():
        lines.append(f"| {cat} | {counts.get(cat, 0)} | [{fname}](./{fname}) |")
    path = OUT / "routes.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", path)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = load()
    write_routes(doc)
    write_category(
        doc,
        "行业讯息",
        "industry.md",
        "中文科技 / AI 媒体。西瓜数据等第三方估计值不是后台粉丝数；新榜名次本次全部为未知。",
    )
    write_category(
        doc,
        "产品动态",
        "products.md",
        "X 上的官方公司号与对应负责人（正表 8 个）。x.com 不能直接访问，需要特殊网络环境。附注中未列入正表的账号不在此列出。",
    )
    write_category(
        doc,
        "场景教程",
        "tutorials.md",
        "按场景：办公/PPT、vibe coding、视频/设计、数据分析。小红书、抖音可直接访问。标「备选」的条目按原名单保留，使用时请阅读其须标明字段。",
    )
    write_category(
        doc,
        "系统学习",
        "learning.md",
        "免费 / 官方课程（正表 8 个）。许多海外平台国内访问为「未知（未实测）」。选课前请先读课程避坑清单。",
    )


if __name__ == "__main__":
    main()
