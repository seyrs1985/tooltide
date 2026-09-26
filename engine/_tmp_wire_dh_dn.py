# -*- coding: utf-8 -*-
"""One-shot: wire DAYLIGHT (tt-dh) + DONATE (tt-dn) via full-string replaces. Idempotent:
the wired form never matches the unwired pattern again."""
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

# ---- DAYLIGHT (tt-dh) ----
W('<label for="dh-d">Date</label>',
  '<label for="dh-d" data-i18n="dh.date">Date</label>', "dh.date")
W('<label for="dh-l">Latitude (40 = US average)</label>',
  '<label for="dh-l" data-i18n="dh.lat">Latitude (40 = US average)</label>', "dh.lat")
W('<span class="result-unit">of daylight</span>',
  '<span class="result-unit" data-i18n="dh.ofdaylight">of daylight</span>', "dh.ofdaylight")
W('<span>longest day here</span>',
  '<span data-i18n="dh.longest">longest day here</span>', "dh.longest")
W('<span>shortest day here</span>',
  '<span data-i18n="dh.shortest">shortest day here</span>', "dh.shortest")
W("<span>change per day now</span>",
  '<span data-i18n="dh.changeperday">change per day now</span>', "dh.changeperday")
W('<button type="button" class="tool-btn" id="dh-share">Share my daylight math</button>',
  '<button type="button" class="tool-btn" id="dh-share" data-i18n="share.share-my-daylightmath">Share my daylight math</button>',
  "share.share-my-daylightmath")

# ---- DONATE (tt-dn) ----
W('<label for="dn-a">Amount you plan to give</label>',
  '<label for="dn-a" data-i18n="dn.amount">Amount you plan to give</label>', "dn.amount")
W('<label for="dn-r">Marginal tax rate (%)</label>',
  '<label for="dn-r" data-i18n="dn.rate">Marginal tax rate (%)</label>', "dn.rate")
W('<span class="result-unit">real cost after tax break</span>',
  '<span class="result-unit" data-i18n="dn.realcost">real cost after tax break</span>', "dn.realcost")
W('<span>tax saved if you itemize</span>',
  '<span data-i18n="dn.taxsaved">tax saved if you itemize</span>', "dn.taxsaved")
W('<span>days left this year</span>',
  '<span data-i18n="dn.daysleft">days left this year</span>', "dn.daysleft")
W('<span>receipt rule at your amount</span>',
  '<span data-i18n="dn.receiptrule">receipt rule at your amount</span>', "dn.receiptrule")
W('<button type="button" class="tool-btn" id="dn-share">Share my giving math</button>',
  '<button type="button" class="tool-btn" id="dn-share" data-i18n="share.share-my-givingmath">Share my giving math</button>',
  "share.share-my-givingmath")

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("wired_total", n_total)
json.dump(count, io.open("_tmp_wire_dh_dn_counts.json", "w"), indent=0)
