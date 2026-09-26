# -*- coding: utf-8 -*-
"""One-shot: wire HOLIDAYTIP (tt-ht) labels/spans/button in tools.py. Idempotent.
NOTE: group(1) must NOT include the closing '>' (v1/v3 lesson)."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 (r'(<label for="ht-b")>Total holiday tipping budget(</label>)', "tip.budget", "Total holiday tipping budget"),
 (r'(<label for="ht-w")>Weekly regulars \(cleaner, dog walker\.\.\.\)(</label>)', "tip.weekly", "Weekly regulars (cleaner, dog walker...)"),
 (r'(<label for="ht-o")>Occasional helpers \(hairdresser, babysitter\.\.\.\)(</label>)', "tip.occasional", "Occasional helpers (hairdresser, babysitter...)"),
 (r'(<span class="result-unit")>per weekly regular(</span>)', "tip.perweekly", "per weekly regular"),
 (r'(<span>)per occasional helper(</span>)', "tip.peroccasional", "per occasional helper"),
 (r'(<span>)to weekly regulars total(</span>)', "tip.weeklytotal", "to weekly regulars total"),
 (r'(<span>)left for the card people(</span>)', "tip.cardleft", "left for the card people"),
 (r'(id="ht-share")>Share my tipping plan(</button>)', "share.share-my-tippingplan", "Share my tipping plan"),
]
for pat, key, text in PAIRS:
    def sub(m, key=key, text=text):
        return m.group(1) + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("tip_wired", n_total)
