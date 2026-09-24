# -*- coding: utf-8 -*-
"""One-shot: add ue.pct key x9 langs."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
VALS = {
 "zh": "% 序列数",
 "es": "secuencias %",
 "pt": "sequências %",
 "ru": "процентных последовательностей",
 "ja": "%シーケンス",
 "ko": "% 시퀀스",
 "de": "%-Sequenzen",
 "fr": "séquences %",
 "id": "urutan %",
}

p = "_i18n_tables.json"
d = json.load(io.open(p, encoding="utf-8"))
n = 0
for lang, txt in VALS.items():
    entries = [tuple(x) for x in d["chrome"][lang]]
    if any(kk == "ue.pct" for kk, _ in entries):
        continue
    entries.append(("ue.pct", txt))
    d["chrome"][lang] = [list(e) for e in entries]
    n += 1
json.dump(d, io.open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
io.open(p, "a", encoding="utf-8").write("\n")
print("added", n, "zh keys:", len(d["chrome"]["zh"]))
