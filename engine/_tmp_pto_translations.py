# -*- coding: utf-8 -*-
"""One-shot: add pt.* + share.share-my-ptomath keys x9 langs (pipe-packed)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"pt.daysperyear": "年假天数|Días de PTO al año|Dias de PTO por ano|Дней отпуска в год|年間の有給日数|연간 PTO 일수|PTO-Tage pro Jahr|jours de congés par an|hari cuti PTO per tahun",
"pt.breakswant": "想要的假期段数|Descansos que quieres|Intervalos que deseja|Количество перерывов|欲しい休みの回数|원하는 휴식 횟수|Gewünschte Pausen|pauses souhaitées|jumlah istirahat yang diinginkan",
"pt.chained": "连休日历天数|días naturales consecutivos|dias corridos consecutivos|календарных дней подряд|連続する暦日数|연속 달력 일수|Kalendertage am Stück|jours civils d affilée|hari kalender beruntun",
"pt.vsnaive": "对比单块 naive 方案|vs un bloque ingenuo|vs um bloco ingênuo|vs один наивный блок|単純な1ブロック比較|단순 한 블록 비교|vs ein naiver Block|vs un bloc naïf|vs satu blok naif",
"pt.weekendsharv": "免费收获的周末|fines de semana gratis|fins de semana grátis|бесплатные выходные|ただで手に入る週末|공짜로 얻는 주말|geschenkte Wochenenden|week-ends offerts|akhir pekan gratis",
"pt.wedtrick": "周三技巧|el truco del miércoles|o truque de quarta|трюк со средой|水曜日のテクニック|수요일 트릭|Der Mittwoch-Trick|l astuce du mercredi|trik hari Rabu",
"share.share-my-ptomath": "分享我的假期计算|Compartir mi cálculo de PTO|Compartir meu cálculo de PTO|Поделиться моим расчётом отпуска|自分のPTO計算を共有|내 PTO 계산 공유|Meine PTO-Rechnung teilen|Partager mon calcul de congés|Bagikan hitungan cuti saya",
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
