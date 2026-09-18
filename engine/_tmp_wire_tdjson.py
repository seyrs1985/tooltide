# -*- coding: utf-8 -*-
"""One-shot: wire td/json/jwt static labels in tools.py. Idempotent."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 (r'(<span class="result-unit">)kcal / day to maintain weight \(TDEE\)(</span>)', "td.unit", "kcal / day to maintain weight (TDEE)"),
 (r'(<span>)BMR at rest(</span>)', "td.bmr", "BMR at rest"),
 (r'(<span>)steady loss \(−500\)(</span>)', "td.loss", "steady loss (−500)"),
 (r'(<span>)lean gain \(\+300\)(</span>)', "td.gain", "lean gain (+300)"),
 (r'(<span class="result-unit" id="(?:js|jw)-u")>status(</span>)', "lbl.status", "status"),
 (r'(<button type="button" class="tool-btn" id="js-fmt")>Format(</button>)', "json.fmt", "Format"),
 (r'(<button type="button" class="tool-btn" id="js-min")>Minify(</button>)', "json.minify", "Minify"),
 (r'(<span>)size(</span>)', "json.size", "size"),
 (r'(<span>)keys \+ values(</span>)', "json.kv", "keys + values"),
 (r'(<span>)max depth(</span>)', "json.depth", "max depth"),
 (r'(<span>)algorithm(</span>)', "jwt.alg", "algorithm"),
 (r'(<span>)expiry(</span>)', "jwt.expiry", "expiry"),
 (r'(<span>)claims(</span>)', "jwt.claims", "claims"),
]

for pat, key, text in PAIRS:
    def sub(m, key=key, text=text):
        return m.group(1) + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("wired", n_total)
