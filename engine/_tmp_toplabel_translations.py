# -*- coding: utf-8 -*-
"""One-shot: add lbl.permonth/peryear/perday + fin/paint/ev/date/conv label keys x9."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"lbl.permonth": "每月|por mes|por mês|в месяц|1か月ごと|월별|pro Monat|par mois|per bulan",
"lbl.peryear": "每年|por año|por ano|в год|1年ごと|연간|pro Jahr|par an|per tahun",
"lbl.perday": "每天|por día|por dia|в день|1日ごと|일별|pro Tag|par jour|per hari",
"fin.totalinterest": "总利息|interés total|juros totais|общие проценты|合計利息|총 이자|Gesamtzinsen|intérêts totaux|total bunga",
"fin.totalpaid": "总还款额|total pagado|total pago|всего выплачено|支払総額|총 지불액|Gesamtzahlung|total payé|total dibayar",
"fin.yousave": "你节省|ahorras|você economiza|вы экономите|節約できる|절약|Du sparst|vous économisez|Anda hemat",
"paint.paintable": "可粉刷面积|área pintable|área pintável|покрываемая площадь|塗装可能面積|도장 가능 면적|streichbare Fläche|surface peignable|area yang bisa dicat",
"ev.fullcharge": "满电充电成本|coste de carga completa|custo de carga completa|стоимость полной зарядки|フル充電コスト|완충 비용|Volladungskosten|coût de charge complète|biaya pengisian penuh",
"date.dayofyear": "年内第几天|día del año|dia do ano|день года|年内の経過日|연중 날짜|Tag des Jahres|jour de l année|hari dalam setahun",
"conv.cubicmeters": "立方米|metros cúbicos|metros cúbicos|кубические метры|立方メートル|입방미터|Kubikmeter|mètres cubes|meter kubik",
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
