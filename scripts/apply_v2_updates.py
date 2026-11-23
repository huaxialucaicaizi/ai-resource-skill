#!/usr/bin/env python3
"""Apply feedback-round updates on top of the owner skill sources.yaml."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_YAML = ROOT / "skills" / "ai-resource-guide" / "references" / "sources.yaml"
DATA_YAML = ROOT / "data" / "sources.yaml"
DATA_JSON = ROOT / "data" / "sources.json"
QD_NEW = "2026-11-23"


def dump(doc):
    text = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100, default_flow_style=False)
    SKILL_YAML.write_text(text, encoding="utf-8")
    DATA_YAML.write_text(text, encoding="utf-8")
    DATA_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    doc = yaml.safe_load(SKILL_YAML.read_text(encoding="utf-8"))

    # Ensure every scene-tutorial source has tutorials: [] unless already set
    for s in doc["sources"]:
        if s.get("category") == "场景教程" and "tutorials" not in s:
            s["tutorials"] = []

    # --- Route: 写文案 ---
    routes = doc["routes"]
    if not any(r["id"] == "copywriting" for r in routes):
        # insert before systematic
        idx = next(i for i, r in enumerate(routes) if r["id"] == "systematic")
        routes.insert(
            idx,
            {
                "id": "copywriting",
                "name_zh": "想学会写文案",
                "name_en": "Learn AI copywriting",
                "help_zh": "想用 AI 写小红书 / 短视频 / 营销文案，看「场景教程 · 写文案」。",
                "category": "场景教程",
                "scene_filter": "写文案",
            },
        )

    # Ensure new-products keeps x_list_url: null (pending public X list)
    for r in routes:
        if r["id"] == "new-products":
            r["x_list_url"] = None
            r["x_list_note"] = "待填入公开 X 列表链接（一键关注）；未建好前保持 null。"

    # --- 智东西 → 备选 ---
    for s in doc["sources"]:
        if s["id"] == "zhidx":
            s["status"] = "备选"
            data = s.setdefault("数据", {})
            data["须标明"] = "备选。多数字段为未知；测试中 skill 可能主动跳过。字段仅保留可核观测，不估算。"

        if s["id"] == "samuel-douyin":
            # Demote PPT match: keep entry but mark weak match + move sort weight via status note
            s["ppt_match"] = "弱"
            data = s.setdefault("数据", {})
            data["须标明"] = (
                "PPT 对口程度偏弱：主页近期作品偏资讯，PPT 内容占比未知。"
                "用户问「做 PPT」时，优先同场景其他博主；本条仅作补充。"
            )
            # Put samuel after other PPT sources in list order
            pass

    # Reorder PPT scene: non-samuel first, samuel last among PPT
    sources = doc["sources"]
    ppt = [s for s in sources if s.get("scene") == "办公/PPT"]
    others = [s for s in sources if s.get("scene") != "办公/PPT"]
    ppt_sorted = [s for s in ppt if s["id"] != "samuel-douyin"] + [s for s in ppt if s["id"] == "samuel-douyin"]
    # rebuild keeping relative order of non-ppt, replace ppt block position with first ppt occurrence
    first_ppt_idx = next(i for i, s in enumerate(sources) if s.get("scene") == "办公/PPT")
    without_ppt = [s for s in sources if s.get("scene") != "办公/PPT"]
    # insert ppt_sorted at first_ppt_idx among without_ppt... simpler: filter
    new_sources = []
    inserted = False
    for s in sources:
        if s.get("scene") == "办公/PPT":
            if not inserted:
                new_sources.extend(ppt_sorted)
                inserted = True
            continue
        new_sources.append(s)
    sources = new_sources
    doc["sources"] = sources

    # Remove existing copywriting / curator if re-run
    doc["sources"] = [
        s
        for s in doc["sources"]
        if s["id"]
        not in {
            "banpie-xhs",
            "zhangyuncai-douyin",
            "huaxia-lucaicaizi-xhs",
            "huaxia-lucaicaizi-douyin",
        }
    ]

    copywriting_sources = [
        {
            "id": "banpie-xhs",
            "name": "半撇老师",
            "category": "场景教程",
            "语言": "中",
            "国内能否直接访问": "小红书可直接访问",
            "免费/付费": "作品可公开看；简介写「购课合作可私信」，是否另有付费课：未知",
            "适合谁": "想用 AI 写小红书笔记、调文风、做自媒体内容工作流的中文学习者",
            "查询日期": QD_NEW,
            "urls": ["https://www.xiaohongshu.com/user/profile/5d2dd068000000001600f52c"],
            "数据": {
                "场景": "写文案",
                "平台": "小红书",
                "小红书号": "banpie01",
                "简介（公开页可见）": "普通人的AI教练，香港新媒体硕士，半撇私塾创始人&数字游民，助2W+学员开启副业，购课合作可私信。",
                "主题可见帖（公开检索摘要）": "我用AI实现了小红书笔记“一键直出”；零AI味洗稿！Claude Style自定义文风教程；豆包这 7 个隐藏功能；AI生成爆款封面等",
                "粉丝": "未知（2026-11-23 打开主页需登录，未见当前粉丝数）。作者个人站 about 页写「小红书：1万+ 粉丝」，标注截至 2026-03，不是本次主页数字。",
                "近90天篇数": "未知",
                "口径说明": "账号存在性与简介、主题帖标题来自 2026-11-23 公开网页检索到的小红书主页摘要；未登录未能读取主页粉丝与完整笔记列表。",
            },
            "scene": "写文案",
            "platforms": ["小红书"],
            "tutorials": [],
        },
        {
            "id": "zhangyuncai-douyin",
            "name": "张蕴采",
            "category": "场景教程",
            "语言": "中",
            "国内能否直接访问": "抖音可直接访问",
            "免费/付费": "作品可公开看；是否另有付费：未知",
            "适合谁": "想看「用 AI 写有深度的爆款文案」类短视频教程的中文学习者（主页同时有国学/自媒体内容，AI 文案不是唯一主题）",
            "查询日期": QD_NEW,
            "urls": [
                "https://www.douyin.com/user/MS4wLjABAAAAccw_6pHbTgGLOFXtLh2vNTeXPtTS6vGPiTjyDvjJaAv4HAmMkaqvS3k1aZL7ret0"
            ],
            "数据": {
                "场景": "写文案",
                "平台": "抖音",
                "抖音号": "Yuncai_114",
                "简介（公开页可见）": "【华夏文化研习者】 传统文化 · 现代商业践行者 经典解读｜",
                "粉丝": "90.0万（2026-11-23 公开检索到的抖音主页摘要所示）",
                "作品数": "200（同上主页摘要）",
                "最新发布": "2026-05-20（主页摘要「最新作品发布时间」）",
                "IP属地": "重庆（主页摘要）",
                "口径说明": "粉丝、作品数、抖音号、简介来自 2026-11-23 公开网页检索到的抖音主页摘要；机器人打开主页未解析出结构化字段，以检索摘要为准，不估算。",
            },
            "scene": "写文案",
            "platforms": ["抖音"],
            "tutorials": [
                {
                    "title": "教你怎么用AI写出有深度的爆款文案",
                    "link": "https://www.douyin.com/video/7641911668615826734",
                    "date": "2026-05-20",
                    "likes": "442（主页作品列表摘要所示；西瓜视频镜像页亦收录同名内容）",
                    "tools": "未知（标题未点名具体工具）",
                    "free_or_paid": "作品可公开看；是否另有付费资料：未知",
                    "query_date": QD_NEW,
                }
            ],
        },
    ]

    # Insert copywriting sources after data scene block (before 系统学习)
    out = []
    inserted_cw = False
    for s in doc["sources"]:
        if s.get("category") == "系统学习" and not inserted_cw:
            out.extend(copywriting_sources)
            inserted_cw = True
        out.append(s)
    if not inserted_cw:
        out.extend(copywriting_sources)
    doc["sources"] = out

    # --- Curator accounts under systematic, last ---
    curator = [
        {
            "id": "huaxia-lucaicaizi-xhs",
            "name": "华夏路菜菜子",
            "category": "系统学习",
            "语言": "中",
            "国内能否直接访问": "小红书可直接访问",
            "免费/付费": "未知",
            "适合谁": "想关注本名单整理者本人的公开分享（非优先推荐；排序靠后）",
            "查询日期": QD_NEW,
            "urls": [],
            "url_notes": "公开可核对来源：GitHub 主页写明「小红书 / 抖音 / 视频号：@华夏路菜菜子」（https://github.com/huaxialucaicaizi）。本次未解析到可核的小红书 profile URL，链接栏留空。",
            "数据": {
                "平台": "小红书",
                "账号名": "华夏路菜菜子",
                "须标明": "本名单整理者本人的账号",
                "粉丝": "未知",
                "近90天篇数": "未知",
                "口径说明": "存在性依据 GitHub 公开「找到我」字段（2026-11-23 读取）。主页粉丝与更新频率未实测，记为未知。排序不优先。",
            },
            "status": "整理者本人",
            "tutorials": [],
        },
        {
            "id": "huaxia-lucaicaizi-douyin",
            "name": "华夏路菜菜子",
            "category": "系统学习",
            "语言": "中",
            "国内能否直接访问": "抖音可直接访问",
            "免费/付费": "未知",
            "适合谁": "想关注本名单整理者本人的公开分享（非优先推荐；排序靠后）",
            "查询日期": QD_NEW,
            "urls": [],
            "url_notes": "公开可核对来源：GitHub 主页写明「小红书 / 抖音 / 视频号：@华夏路菜菜子」（https://github.com/huaxialucaicaizi）。本次未解析到可核的抖音 profile URL，链接栏留空。",
            "数据": {
                "平台": "抖音",
                "账号名": "华夏路菜菜子",
                "须标明": "本名单整理者本人的账号",
                "粉丝": "未知",
                "近90天篇数": "未知",
                "口径说明": "存在性依据 GitHub 公开「找到我」字段（2026-11-23 读取）。主页粉丝与更新频率未实测，记为未知。排序不优先。",
            },
            "status": "整理者本人",
            "tutorials": [],
        },
    ]
    # Append curator at end of 系统学习 (end of list among that category)
    non_sys = [s for s in doc["sources"] if s.get("category") != "系统学习"]
    sys_sources = [s for s in doc["sources"] if s.get("category") == "系统学习"]
    sys_sources = [s for s in sys_sources if s["id"] not in {"huaxia-lucaicaizi-xhs", "huaxia-lucaicaizi-douyin"}]
    doc["sources"] = non_sys + sys_sources + curator

    # meta note about monthly review
    notes = doc["meta"].setdefault("notes", [])
    review_note = "名单维护：计划每月复查一次（链接、免费/付费政策、账号是否仍可用）；具体字段以各条目查询日期为准。"
    if review_note not in notes:
        notes.append(review_note)
    doc["meta"]["review_cadence"] = "每月复查一次"

    dump(doc)
    from collections import Counter

    c = Counter(s["category"] for s in doc["sources"])
    scenes = Counter(s.get("scene") for s in doc["sources"] if s.get("category") == "场景教程")
    print("total", len(doc["sources"]), dict(c))
    print("scenes", dict(scenes))
    print("routes", [r["id"] for r in doc["routes"]])


if __name__ == "__main__":
    main()
