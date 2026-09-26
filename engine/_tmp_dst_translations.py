# -*- coding: utf-8 -*-
"""One-shot: add dst.* + share.share-my-shiftplan keys x9 langs."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"dst.region": "地区|Región|Região|Регион|地域|지역|Region|Région|Wilayah",
"dst.pace": "每日调整幅度|Ajuste por día|Ajuste por dia|Сдвиг в день|1日のずらし幅|하루 조정 폭|Anpassung pro Tag|Décalage par jour|Pergeseran per hari",
"dst.fallback": "时钟回拨|Atraso horario|Atraso horário|Перевод часов|時計が戻る|시계 백워드|Uhren zurückstellen|Recul des horloges|Jam dimundurkan",
"dst.starton": "开始调整日|empezar a ajustar desde|começar a ajustar em|начать сдвигать с|調整開始日|조정 시작일|Beginn der Umstellung|commencer le décalage le|mulai geser pada",
"dst.daysfrom": "距今天数|días desde hoy|dias a partir de hoje|дней с сегодняшнего дня|今日からの日数|오늘부터 일수|Tage ab heute|jours à partir d aujourd hui|hari dari hari ini",
"dst.bedtime": "每日就寝调整|cambio de hora de acostarse|ajuste diário de horário|сдвиг отхода ко сну daily|就寝時刻の毎日のずらし|매일 취침 조정|tägliche Bettzeit-Verschiebung|décalage du coucher daily|pergeseran jam tidur harian",
"share.share-my-shiftplan": "分享我的调整计划|Compartir mi plan de ajuste|Compartir meu plano de ajuste|Поделиться планом перестройки|自分の調整プランを共有|내 조정 계획 공유|Meinen Umstellungsplan teilen|Partager mon plan de décalage|Bagikan rencana pergeseran saya",
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
