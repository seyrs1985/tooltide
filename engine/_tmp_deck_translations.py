# -*- coding: utf-8 -*-
"""One-shot: add deck.* + share.share-my-stainmath keys x9 langs (pipe-packed)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"deck.area": "露台地板面积（平方英尺）|Área del piso (pies cuadrados)|Área do piso (pés quadrados)|Площадь пола (кв. футов)|デッキ面積（平方フィート）|데크 바닥 면적 (제곱피트)|Fläche des Bodens (Quadratfuß)|Surface du plancher (pieds carrés)|Area lantai (kaki persegi)",
"deck.railing": "栏杆线性英尺|Pies lineales de barandilla|Metros lineares de corrimão|Погонные футы перил|手すりのフィート数|난간 선형 피트|Laufmeter Geländer|pieds linéaires de rambarde|kaki linear pagar",
"deck.coats": "涂刷层数|Capas|Demãos|Слои|塗り回数|도장 횟수|Anstriche|Couches|Lapisan",
"deck.price": "每加仑价格（$）|Precio por galón ($)|Preço por galão ($)|Цена за галлон ($)|1ガロンの価格（$）|갤런당 가격 ($)|Preis pro Gallone ($)|Prix par gallon ($)|Harga per galon ($)",
"deck.gallons": "所需着色剂加仑数|galones de tinta|galões de mancha|галлонов морилки|必要なステインのガロン数|필요한 스테인 갤런|Gallonen Lasur|gallons de teinture|galon pernis kayu",
"deck.totalcost": "总费用|Coste total|Custo total|Общая стоимость|合計コスト|총 비용|Gesamtkosten|Coût total|Total biaya",
"deck.brushing": "刷涂小时数|Horas de brocha|Horas de pincel|Часов покраски|刷塗時間|브러싱 시간|Streichstunden|heures de brossage|jam mengecat",
"deck.redocycle": "重涂周期|Ciclo de renovación|Ciclo de renovação|Цикл обновления|塗り直しサイクル|재도장 주기|Erneuerungszyklus|Cycle de réfection|Siklus pengecatan ulang",
"share.share-my-stainmath": "分享我的着色计算|Compartir mi cálculo de tinta|Compartir meu cálculo de mancha|Поделиться моим расчётом морилки|自分のステイン計算を共有|내 스테인 계산 공유|Meine Lasur-Rechnung teilen|Partager mon calcul de teinture|Bagikan hitungan pewarna saya",
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
