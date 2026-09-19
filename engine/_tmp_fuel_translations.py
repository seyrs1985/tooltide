# -*- coding: utf-8 -*-
"""One-shot: add fu.* fuelcost keys x9 langs."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"fu.l100": "升/百公里|Litros por 100 km|Litros por 100 km|литров на 100 км|リットル/100km|리터/100km|Liter pro 100 km|litres aux 100 km|liter per 100 km",
"fu.mpgus": "英里/加仑（美制）|Millas por galón (EE. UU.)|Milhas por galão (EUA)|миль на галлон (США)|マイル/ガロン(US)|갤런당 마일 (US)|Meilen pro Gallone (US)|miles par gallon (US)|mil per galon (AS)",
"fu.us": "（美制）|(EE. UU.)|(EUA)|(США)|(US)|(US)|(US)|(US)|(AS)",
"fu.efficient": "省油|eficiente|eficiente|экономичный|低燃費|연비 좋음|sparsam|économique|hemat bahan bakar",
"fu.typical": "一般|típico|típico|типичный|標準的|보통|typisch|typique|tipikal",
"fu.thirsty": "费油|consumidor|bebedor|прожорливый|燃費が悪い|연비 나쁨|durstig|gourmand|boros bahan bakar",
"fu.hintbetter": "L/100km 越低越好 · MPG 越高越好。|Menor L/100km es mejor · mayor MPG es mejor.|Menor L/100km é melhor · maior MPG é melhor.|Ниже L/100km лучше · выше MPG лучше.|L/100kmは低いほど・MPGは高いほど良い。|L/100km은 낮을수록 · MPG는 높을수록 좋습니다.|Weniger L/100km ist besser · mehr MPG ist besser.|Moins de L/100km est mieux · plus de MPG est mieux.|L/100km lebih rendah lebih baik · MPG lebih tinggi lebih baik.",
"fu.hintl": "{l} L/100km = {m} 美制 mpg —— 对汽油车来说{v}。|{l} L/100km = {m} mpg (EE. UU.) — {v} para un coche de gasolina.|{l} L/100km = {m} mpg (EUA) — {v} para um carro a gasolina.|{l} л/100км = {m} mpg (США) — {v} для бензиновой машины.|{l} L/100km = {m} 米国mpg — ガソリン車として{v}。|{l} L/100km = {m} 미국 mpg — 휘발유 차로서 {v}.|{l} l/100 km = {m} US-mpg — {v} für einen Benziner.|{l} L/100km = {m} mpg (US) — {v} pour une voiture à essence.|{l} L/100km = {m} mpg AS — {v} untuk mobil bensin.",
"fu.hintm": "{m} mpg = {l} L/100km —— 对汽油车来说{v}。|{m} mpg = {l} L/100km - {v} para un coche de gasolina.|{m} mpg = {l} L/100km - {v} para um carro a gasolina.|{m} mpg = {l} л/100км — {v} для бензиновой машины.|{m} mpg = {l} L/100km — ガソリン車として{v}。|{m} mpg = {l} L/100km — 휘발유 차로서 {v}.|{m} mpg = {l} l/100 km — {v} für einen Benziner.|{m} mpg = {l} L/100km — {v} pour une voiture à essence.|{m} mpg = {l} L/100km — {v} untuk mobil bensin.",
}

p = "_i18n_tables.json"
d = json.load(io.open(p, encoding="utf-8"))
n = 0
for k, line in T.items():
    vals = line.split("|")
    for lang, txt in zip(ORDER, vals):
        entries = [tuple(x) for x in d["chrome"][lang]]
        if any(kk == k for kk, _ in entries):
            continue
        entries.append((k, txt))
        d["chrome"][lang] = [list(e) for e in entries]
        n += 1
json.dump(d, io.open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
io.open(p, "a", encoding="utf-8").write("\n")
print("added", n, "zh keys:", len(d["chrome"]["zh"]))
