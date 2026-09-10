# -*- coding: utf-8 -*-
"""Revenue tracker — progress toward the $1 goal and beyond.

Usage:
    python engine/revenue.py                       # show report
    python engine/revenue.py --add adsense 0.42    # log earnings (today)
    python engine/revenue.py --add affiliate 1.25 --date 2026-09-12 --note "first commission"

Data file: data/revenue.csv  (date,source,amount_usd,note)
Goals:     config/goals.json
"""
import csv
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "revenue.csv")
GOALS = os.path.join(ROOT, "config", "goals.json")


def load_goals():
    try:
        with open(GOALS, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"revenue_goal_usd": 1.0, "stable_monthly_usd": 50.0}


def load_rows():
    if not os.path.exists(DATA):
        return []
    with open(DATA, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def append_row(date, source, amount, note):
    exists = os.path.exists(DATA)
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with open(DATA, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["date", "source", "amount_usd", "note"])
        w.writerow([date, source, f"{float(amount):.2f}", note])


def report():
    rows = load_rows()
    goals = load_goals()
    goal = float(goals.get("revenue_goal_usd", 1.0))
    stable = float(goals.get("stable_monthly_usd", 50.0))
    milestones = goals.get("milestones_usd") or [goal, stable]
    total = sum(float(r["amount_usd"]) for r in rows)
    this_month = datetime.date.today().strftime("%Y-%m")
    month_total = sum(float(r["amount_usd"]) for r in rows if r["date"].startswith(this_month))
    by_src = {}
    for r in rows:
        by_src[r["source"]] = by_src.get(r["source"], 0.0) + float(r["amount_usd"])
    print("=" * 50)
    print(f"  ToolTide 收入看板   ({datetime.date.today().isoformat()})")
    print("=" * 50)
    if not rows:
        print("  尚无收入记录。变现凭证接入后,自动化会自动记录。")
    for src, amt in sorted(by_src.items(), key=lambda x: -x[1]):
        print(f"  {src:<12} ${amt:8.2f}")
    print("-" * 50)
    print(f"  累计收入:     ${total:,.2f}")
    print(f"  本月收入:     ${month_total:,.2f}   (月度稳定目标 ${stable:,.0f})")
    print("  里程碑阶梯:")
    for m in milestones:
        mark = "x" if total >= m else " "
        bar_n = int(min(total / m, 1.0) * 24)
        print(f"   [{mark}] ${m:>6,.0f}  [{'#' * bar_n}{'.' * (24 - bar_n)}] {min(total / m * 100, 100):5.1f}%")
    print(f"  记录笔数:     {len(rows)}")
    return total


def main():
    args = sys.argv[1:]
    if args and args[0] == "--add":
        source = args[1]
        amount = args[2]
        date = datetime.date.today().isoformat()
        note = ""
        if "--date" in args:
            date = args[args.index("--date") + 1]
        if "--note" in args:
            note = args[args.index("--note") + 1]
        append_row(date, source, amount, note)
        print(f"已记录: {date} {source} +${float(amount):.2f} {note}")
    print()
    report()


if __name__ == "__main__":
    main()
