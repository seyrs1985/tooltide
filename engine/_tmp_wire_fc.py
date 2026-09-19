# -*- coding: utf-8 -*-
"""One-shot: wire FUELCOST (tt-fc) labels/spans/options in tools.py. Idempotent."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

# (regex, key, text) — group1 must NOT include the closing '>'
PAIRS = [
 (r'(<label for="fc-d")>Trip distance(</label>)', "fc.distance", "Trip distance"),
 (r'(<label for="fc-e")>Consumption(</label>)', "fc.consumption", "Consumption"),
 (r'(<label for="fc-p")>Fuel price(</label>)', "fc.price", "Fuel price"),
 (r'(<option value="us">)Miles / MPG / \$ per gallon(</option>)', "fc.optus", "Miles / MPG / $ per gallon"),
 (r'(<option value="eu">)Kilometers / L per 100 km / \$ per liter(</option>)', "fc.opteu", "Kilometers / L per 100 km / $ per liter"),
 (r'(<span>)fuel needed(</span>)', "fc.fuelneeded", "fuel needed"),
 (r'(<span>)per person, 4 riders(</span>)', "fc.pp4", "per person, 4 riders"),
 (r'(<span>)round trip(</span>)', "fc.roundtrip", "round trip"),
]
for pat, key, text in PAIRS:
    def sub(m, key=key, text=text):
        return m.group(1) + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

# dynamic result-unit
s, n = re.subn(r"document\.getElementById\('fc-unit'\)\.textContent='one-way fuel cost';",
               "document.getElementById('fc-unit').textContent=TT('fc.oneway','one-way fuel cost');", s)
n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("fc_wired", n_total)
