# -*- coding: utf-8 -*-
"""Analytics → optimization loop.

Reads a Google Search Console performance export (page, impressions, clicks,
position) from data/metrics.csv and emits prioritized optimization actions to
data/insights.json. The daily automation acts on the top actions.

CSV columns (header row required, order-insensitive):
    page, impressions, clicks, position
`page` may be a full URL or a slug like /days-until-christmas/.

Without a metrics file it runs on labeled demo data so the pipeline stays
testable before Search Console is connected.
"""
import csv
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "metrics.csv")
OUT = os.path.join(ROOT, "data", "insights.json")

DEMO = [
    {"page": "/days-until-christmas/", "impressions": 820, "clicks": 31, "position": 18.4},
    {"page": "/percentage-calculator/", "impressions": 540, "clicks": 4, "position": 42.1},
    {"page": "/cm-to-inches/", "impressions": 210, "clicks": 9, "position": 12.7},
    {"page": "/kg-to-lbs/", "impressions": 30, "clicks": 0, "position": 55.0},
    {"page": "/word-counter/", "impressions": 480, "clicks": 12, "position": 9.2},
]


def load_rows(path):
    if not os.path.exists(path):
        return DEMO, True
    with open(path, encoding="utf-8") as f:
        rows = []
        for r in csv.DictReader(f):
            try:
                page = r["page"].strip()
                page = "/" + "/".join(page.split("/")[3:]) if page.startswith("http") else page
                rows.append({
                    "page": page,
                    "impressions": float(r["impressions"] or 0),
                    "clicks": float(r["clicks"] or 0),
                    "position": float(r["position"] or 100),
                })
            except (KeyError, ValueError):
                continue
        return rows, False


def analyze(rows):
    actions = []
    for r in rows:
        imp, clk, pos = r["impressions"], r["clicks"], r["position"]
        ctr = clk / imp * 100 if imp else 0
        if imp >= 100 and ctr < 1.5:
            actions.append({
                "page": r["page"], "priority": 1, "action": "rewrite_title_desc",
                "reason": f"高曝光低点击: {imp:.0f} impressions, CTR {ctr:.1f}%, 平均排名 {pos:.1f} — 标题/描述不够吸引点击",
                "how": "在 engine/pages.py 中改写该页 title 与 desc:加入数字、意图词与差异化卖点,重建部署",
            })
        elif 5 <= pos <= 20 and clk > 0:
            actions.append({
                "page": r["page"], "priority": 2, "action": "expand_content",
                "reason": f"排名 {pos:.1f} 处于第2-3页冲击区 — 扩充内容与内链可推进至首页",
                "how": "为该页追加 2-3 个 FAQ、使用场景段落,并从高分页面增加内链指向",
            })
        elif imp < 10 and pos > 60:
            actions.append({
                "page": r["page"], "priority": 3, "action": "build_internal_links",
                "reason": f"曝光极少({imp:.0f}) — 收录弱或内链不足",
                "how": "确认 sitemap 已提交;从首页与同类页面增加入口链接;等待 1-2 周观察",
            })
        elif ctr >= 8 and pos <= 8:
            actions.append({
                "page": r["page"], "priority": 4, "action": "monetize_check",
                "reason": f"表现优秀: CTR {ctr:.1f}%, 排名 {pos:.1f} — 是变现主力页",
                "how": "确认该页广告位已启用;可增加相关工具推荐提升 session depth",
            })
    actions.sort(key=lambda a: a["priority"])
    return actions


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DATA
    rows, demo = load_rows(path)
    actions = analyze(rows)
    out = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "demo-data" if demo else path,
        "pages_analyzed": len(rows),
        "actions": actions,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"分析 {len(rows)} 个页面 ({'DEMO 数据 — 接入 GSC 后自动切换' if demo else path})")
    print(f"产出 {len(actions)} 条优化动作 → data/insights.json\n")
    for a in actions[:8]:
        print(f"  [P{a['priority']}] {a['action']}: {a['page']}")
        print(f"         {a['reason']}")


if __name__ == "__main__":
    main()
