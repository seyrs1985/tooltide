# -*- coding: utf-8 -*-
"""One-shot: wire top repeated bare stat spans in tools.py. Idempotent."""
import re, io, json

PAIRS = [
 ("per month", "lbl.permonth"),
 ("total interest", "fin.totalinterest"),
 ("you save", "fin.yousave"),
 ("total paid", "fin.totalpaid"),
 ("per year", "lbl.peryear"),
 ("per day", "lbl.perday"),
 ("paintable area", "paint.paintable"),
 ("full charge cost", "ev.fullcharge"),
 ("day of year", "date.dayofyear"),
 ("cubic meters", "conv.cubicmeters"),
 ("words", "wc.words"),
]

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
total = 0
counts = {}
for text, key in PAIRS:
    pat = re.compile(r"<span>" + re.escape(text) + r"</span>")
    def sub(m, key=key, text=text):
        return '<span data-i18n="' + key + '">' + text + "</span>"
    s, n = pat.subn(sub, s)
    counts[text] = n
    total += n
io.open(P, "w", encoding="utf-8", newline="").write(s)
json.dump(counts, io.open("_tmp_label_counts.json", "w"), indent=0)
print("wired", total)
