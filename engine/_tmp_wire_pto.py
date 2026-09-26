# -*- coding: utf-8 -*-
"""One-shot: wire PTOOPT (tt-pt) labels/spans/button + JS restore. Idempotent:
wired forms never match unwired patterns again."""
import io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0
count = {}

def W(before, after, key):
    global s, n_total
    n = s.count(before)
    if n:
        s = s.replace(before, after)
        n_total += n
        count[key] = n

# ---- static ----
W('<label for="pt-d">PTO days per year</label>',
  '<label for="pt-d" data-i18n="pt.daysperyear">PTO days per year</label>', "pt.daysperyear")
W('<label for="pt-b">Breaks you want</label>',
  '<label for="pt-b" data-i18n="pt.breakswant">Breaks you want</label>', "pt.breakswant")
W('<span class="result-unit">calendar days off, chained</span>',
  '<span class="result-unit" data-i18n="pt.chained">calendar days off, chained</span>', "pt.chained")
W('<span>vs one naive block</span>',
  '<span data-i18n="pt.vsnaive">vs one naive block</span>', "pt.vsnaive")
W('<span>weekends harvested</span>',
  '<span data-i18n="pt.weekendsharv">weekends harvested</span>', "pt.weekendsharv")
W('<span>the Wednesday trick</span>',
  '<span data-i18n="pt.wedtrick">the Wednesday trick</span>', "pt.wedtrick")
W('<button type="button" class="tool-btn" id="pt-share">Share my PTO math</button>',
  '<button type="button" class="tool-btn" id="pt-share" data-i18n="share.share-my-ptomath">Share my PTO math</button>',
  "share.share-my-ptomath")
# ---- JS restore ----
W("this.textContent='Share my PTO math';",
  "this.textContent=TT('share.share-my-ptomath','Share my PTO math');", "pt.jsrestore")

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("pto_wired_total", n_total)
print("by_key", json.dumps(count) if (json := __import__("json")) else "")
