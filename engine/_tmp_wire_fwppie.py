# -*- coding: utf-8 -*-
"""One-shot: wire FIREWOOD (tt-fw) + PUMPKINPIE (tt-ppie) labels/spans/buttons. Idempotent.
NOTE: group(1) must NOT include the closing '>' (v1 lesson)."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 # firewood
 (r'(<label for="fw-a")>Heated area \(sq ft\)(</label>)', "fw.area", "Heated area (sq ft)"),
 (r'(<label for="fw-c")>Climate(</label>)', "fw.climate", "Climate"),
 (r'(<label for="fw-s")>Species(</label>)', "fw.species", "Species"),
 (r'(<label for="fw-p")>Price per cord \(\$\)(</label>)', "fw.price", "Price per cord ($)"),
 (r'(<span class="result-unit")>cords for the winter(</span>)', "fw.cords", "cords for the winter"),
 (r'(<span>)total wood cost(</span>)', "fw.cost", "total wood cost"),
 (r'(<span>)\$ per million Btu(</span>)', "fw.pmbtu", "$ per million Btu"),
 (r'(<span>)same heat, electric(</span>)', "fw.electric", "same heat, electric"),
 (r'(id="fw-share")>Share my winter wood estimate(</button>)', "share.share-my-winterwood", "Share my winter wood estimate"),
 # pumpkin pie
 (r'(<label for="ppie-g")>Guests(</label>)', "ppie.guests", "Guests"),
 (r'(<label for="ppie-s")>Slices per guest(</label>)', "ppie.slices", "Slices per guest"),
 (r'(<span class="result-unit")>9-inch pies(</span>)', "ppie.pies", "9-inch pies"),
 (r'(<span>)cups of puree(</span>)', "ppie.cups", "cups of puree"),
 (r'(<span>)15-oz cans(</span>)', "ppie.cans", "15-oz cans"),
 (r'(<span>)eggs \+ sugar \(cups\)(</span>)', "ppie.eggssugar", "eggs + sugar (cups)"),
 (r'(id="ppie-share")>Share the pie math(</button>)', "share.share-piemath", "Share the pie math"),
]
for pat, key, text in PAIRS:
    def sub(m, key=key, text=text):
        return m.group(1)[:-1] + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("fw_ppie_wired", n_total)
