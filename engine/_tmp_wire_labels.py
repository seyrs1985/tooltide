# -*- coding: utf-8 -*-
"""One-shot: wire common field labels (data-i18n) in tools.py. Idempotent."""
import re, io, json

MAP = {
"Units": "lbl.units",
"Height": "lbl.height",
"Weight": "lbl.weight",
"Sex": "lbl.sex",
"Mode": "lbl.mode",
"Length": "lbl.length",
"Width": "lbl.width",
"Age": "lbl.age",
"Distance": "lbl.distance",
"Input": "lbl.input",
"Text": "lbl.text",
"Years": "lbl.years",
"Minutes": "lbl.minutes",
"Seconds": "lbl.seconds",
"Direction": "lbl.direction",
"Method": "lbl.method",
"Term (years)": "lbl.term-years",
"Air temperature": "lbl.airtemp",
"Relative humidity %": "lbl.relhum",
"Body weight (kg)": "lbl.bodyweight",
"Wall height (m)": "lbl.wallheight",
"Your text": "lbl.yourtext",
"Coats": "lbl.coats",
}

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
total = 0
for text, key in MAP.items():
    pat = re.compile(r'(<label for="[^"]{1,60}">)' + re.escape(text) + r'(</label>)')
    def sub(m, key=key):
        return m.group(1) + '<span data-i18n="' + key + '">' + text + '</span>' + m.group(2)
    # label text replaced by an inner span so apply() can translate it safely
    s2, n = pat.subn(lambda m: m.group(1) + '<span data-i18n="' + key + '">' + text + '</span>' + m.group(2), s)
    s = s2
    total += n
io.open(P, "w", encoding="utf-8", newline="").write(s)
json.dump({k: t for t, k in MAP.items()}, io.open("_tmp_label_texts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("labels_wired", total)
