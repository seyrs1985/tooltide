# -*- coding: utf-8 -*-
"""One-shot: wire SLOWCOOK (tt-sc2) static labels/spans/button in tools.py. Idempotent.
NOTE: group(1) without closing '>' for attred tags; bare <span> uses full-replace."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 (r'(<label for="sc2-m")>Oven time in the recipe \(minutes\)(</label>)', "slowcook.ovenmin", "Oven time in the recipe (minutes)"),
 (r'(<label for="sc2-s")>Slow cooker setting(</label>)', "slowcook.setting", "Slow cooker setting"),
 (r'(<span class="result-unit")>in the slow cooker(</span>)', "slowcook.incooker", "in the slow cooker"),
 (r'(<span>)the other setting(</span>)', "slowcook.othersetting", "the other setting"),
 (r'(<span>)liquid in the recipe(</span>)', "slowcook.liquid", "liquid in the recipe"),
 (r'(<span>)dairy and seafood go in(</span>)', "slowcook.dairy", "dairy and seafood go in"),
 (r'(id="sc2-share")>Share my conversion(</button>)', "share.share-my-conversion", "Share my conversion"),
]
for pat, key, text in PAIRS:
    def sub(m, key=key, text=text):
        return m.group(1) + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("slowcook_wired", n_total)
