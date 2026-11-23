#!/usr/bin/env python3
"""按路线从 sources.yaml 取出信息源，字段原样输出（不改写任何数字或标签）。

用法：
  python3 pick.py --routes            列出所有路线
  python3 pick.py ppt                 按路线 id 取源（可多个：ppt coding）
  python3 pick.py --all               全部源
  python3 pick.py ppt --full          连「榜单明细」等长字段一起输出
"""
import argparse
import pathlib
import sys

import yaml

DATA = pathlib.Path(__file__).resolve().parent.parent / "references" / "sources.yaml"
LONG_KEYS = {"榜单明细", "补充说明", "累计选课示例", "补充"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("route_ids", nargs="*")
    ap.add_argument("--routes", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--data", default=str(DATA))
    a = ap.parse_args()

    d = yaml.safe_load(open(a.data, encoding="utf-8"))
    routes = {r["id"]: r for r in d["routes"]}
    dump = lambda x: yaml.safe_dump(x, allow_unicode=True, sort_keys=False, width=200)

    if a.routes or not (a.route_ids or a.all):
        print("query_date:", d["meta"]["query_date"])
        for r in d["routes"]:
            print(f'{r["id"]}\t{r["name_zh"]}\t{r["category"]}\t{r["scene_filter"] or "-"}')
        return

    bad = [rid for rid in a.route_ids if rid not in routes]
    if bad:
        sys.exit(f"未知路线 id: {', '.join(bad)}；可选：{', '.join(routes)}")

    print("# meta")
    print(dump({"query_date": d["meta"]["query_date"], "access_rules": d["meta"]["access_rules"]}))

    selected = [(None, d["sources"])] if a.all else []
    for rid in a.route_ids:
        r = routes[rid]
        hits = [s for s in d["sources"] if s["category"] == r["category"]
                and (r["scene_filter"] is None or s.get("scene") == r["scene_filter"])]
        selected.append((r, hits))

    for r, hits in selected:
        print(f'# 路线：{r["name_zh"]}（{r["help_zh"]}）' if r else "# 全部源")
        if r and r.get("x_list_url"):
            print(f'# 一键关注列表：{r["x_list_url"]}')
        for s in hits:
            s = dict(s)
            if not a.full and isinstance(s.get("数据"), dict):
                s["数据"] = {k: v for k, v in s["数据"].items() if k not in LONG_KEYS}
            print(dump([s]))


if __name__ == "__main__":
    main()
