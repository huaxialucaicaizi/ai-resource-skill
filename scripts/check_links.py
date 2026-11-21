#!/usr/bin/env python3
"""Check every URL in data/sources.yaml.

Exit code:
  0 — finished (even if some links are blocked/dead); soft-fail for CI.
  2 — data file missing or unreadable.

403/429 on known bot-hostile hosts → 「需人工确认」, not dead.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sources.yaml"
REPORT_DIR = ROOT / "reports"
USER_AGENT = (
    "ai-resource-skill-link-check/1.0 (+https://github.com/huaxialucaicaizi/ai-resource-skill; educational)"
)
TIMEOUT = 20

# Platforms that often block bots — treat 403/429 as 需人工确认
BOT_HOST_HINTS = (
    "x.com",
    "twitter.com",
    "xiaohongshu.com",
    "douyin.com",
    "iesdouyin.com",
)


def collect_urls(doc: dict) -> list[tuple[str, str]]:
    """Return list of (source_id, url)."""
    out: list[tuple[str, str]] = []
    for s in doc.get("sources", []):
        sid = s.get("id", "?")
        for u in s.get("urls") or []:
            if isinstance(u, str) and u.startswith(("http://", "https://")):
                out.append((sid, u))
        # Also collect 数据来源 URLs inside 榜单明细
        data = s.get("数据") or {}
        for row in data.get("榜单明细") or []:
            src = row.get("数据来源")
            if isinstance(src, str) and src.startswith(("http://", "https://")):
                out.append((sid, src))
    # de-dupe preserving order
    seen = set()
    uniq = []
    for sid, u in out:
        if u in seen:
            continue
        seen.add(u)
        uniq.append((sid, u))
    return uniq


def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def is_bot_hostile(url: str) -> bool:
    h = host_of(url)
    return any(x in h for x in BOT_HOST_HINTS)


def check_one(url: str) -> dict:
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            # read a tiny bit then discard
            resp.read(1024)
            if 200 <= int(code) < 400:
                return {"url": url, "status": "ok", "http_status": int(code), "detail": ""}
            if int(code) in (403, 429) and is_bot_hostile(url):
                return {
                    "url": url,
                    "status": "需人工确认",
                    "http_status": int(code),
                    "detail": "bot-hostile host returned 403/429",
                }
            return {"url": url, "status": "dead", "http_status": int(code), "detail": f"HTTP {code}"}
    except urllib.error.HTTPError as e:
        code = e.code
        if code in (403, 429) and is_bot_hostile(url):
            return {
                "url": url,
                "status": "需人工确认",
                "http_status": code,
                "detail": "bot-hostile host returned 403/429",
            }
        # Some sites reject GET bots with 403 even if not in list — still mark 需人工确认 for 403/429
        if code in (403, 429):
            return {
                "url": url,
                "status": "需人工确认",
                "http_status": code,
                "detail": "HTTP 403/429 — treat as manual confirm, not dead",
            }
        return {"url": url, "status": "dead", "http_status": code, "detail": str(e.reason)}
    except Exception as e:
        return {"url": url, "status": "dead", "http_status": None, "detail": f"{type(e).__name__}: {e}"}


def write_github_summary(summary: dict, results: list[dict]) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    lines = [
        "# Link check report",
        "",
        f"- Checked at: `{summary['checked_at']}`",
        f"- Total URLs: **{summary['total']}**",
        f"- ok: **{summary['ok']}**",
        f"- 需人工确认 (blocked): **{summary['blocked']}**",
        f"- dead: **{summary['dead']}**",
        "",
        "## Details",
        "",
        "| Status | HTTP | Source | URL | Detail |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for r in results:
        lines.append(
            f"| {r['status']} | {r.get('http_status') if r.get('http_status') is not None else '-'} | `{r['source_id']}` | {r['url']} | {r.get('detail','')} |"
        )
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> int:
    if not DATA.exists():
        print(f"Missing {DATA}", file=sys.stderr)
        return 2
    doc = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    pairs = collect_urls(doc)
    results = []
    for i, (sid, url) in enumerate(pairs):
        r = check_one(url)
        r["source_id"] = sid
        results.append(r)
        print(f"[{r['status']}] {sid} {url} ({r.get('http_status')})")
        # be polite
        if i + 1 < len(pairs):
            time.sleep(0.4)

    buckets = defaultdict(list)
    for r in results:
        buckets[r["status"]].append(r)

    summary = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "ok": len(buckets.get("ok", [])),
        "blocked": len(buckets.get("需人工确认", [])),
        "dead": len(buckets.get("dead", [])),
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = REPORT_DIR / f"link-check-{stamp}.json"
    md_path = REPORT_DIR / "link-check-latest.md"

    payload = {"summary": summary, "results": results}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        f"# Link check — {summary['checked_at']}",
        "",
        f"- Total: {summary['total']}",
        f"- ok: {summary['ok']}",
        f"- 需人工确认: {summary['blocked']}",
        f"- dead: {summary['dead']}",
        "",
    ]
    for status in ("ok", "需人工确认", "dead"):
        md_lines.append(f"## {status}")
        md_lines.append("")
        items = buckets.get(status, [])
        if not items:
            md_lines.append("（无）")
            md_lines.append("")
            continue
        for r in items:
            md_lines.append(
                f"- `{r['source_id']}` — {r['url']} — HTTP {r.get('http_status')} — {r.get('detail','')}"
            )
        md_lines.append("")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    write_github_summary(summary, results)

    print("\nSummary:", json.dumps(summary, ensure_ascii=False))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    # Soft fail: always 0 after a completed run so CI can publish the report.
    # Dead links are visible in the job summary / report file.
    return 0


if __name__ == "__main__":
    sys.exit(main())
