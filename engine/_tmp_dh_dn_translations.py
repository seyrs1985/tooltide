# -*- coding: utf-8 -*-
"""One-shot: add dh.* + dn.* + 2 share keys x9 langs (pipe-packed)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"dh.date": "日期|Fecha|Data|Дата|日付|날짜|Datum|Date|Tanggal",
"dh.lat": "纬度（40 = 美国均值）|Latitud (40 = media de EE. UU.)|Latitude (40 = média dos EUA)|Широта (40 = среднее по США)|緯度（40 = 米平均）|위도 (40 = 미국 평균)|Breitengrad (40 = US-Durchschnitt)|Latitude (40 = moyenne US)|Lintang (40 = rata-rata AS)",
"dh.ofdaylight": "的日照时数|de luz diurna|de luz diurna|часов дневного света|の日照時間|일조 시간|an Tageslicht|de lumière du jour|jam siang",
"dh.longest": "此处最长白昼|día más largo aquí|dia mais longo aqui|самый длинный день здесь|ここで最長の昼|이곳의 최장일|längster Tag hier|jour le plus long ici|hari terpanjang di sini",
"dh.shortest": "此处最短白昼|día más corto aquí|dia mais curto aqui|самый короткий день здесь|ここで最短の昼|이곳의 최단일|kürzester Tag hier|jour le plus court ici|hari terpendek di sini",
"dh.changeperday": "当前每日变化|cambio por día ahora|mudança por dia agora|изменение в день сейчас|現在の1日あたりの変化|현재 일일 변화|Änderung pro Tag jetzt|changement par jour maintenant|perubahan per hari sekarang",
"share.share-my-daylightmath": "分享我的日照计算|Compartir mi cálculo de luz|Compartir meu cálculo de luz|Поделиться моим расчётом света|自分の日照計算を共有|내 일조 계산 공유|Meine Tageslichtrechnung teilen|Partager mon calcul de lumière|Bagikan hitungan siang saya",
"dn.amount": "计划捐赠金额|Monto que planeas donar|Valor que você planeja doar|Сумма пожертвования|寄付予定額|기부할 금액|Geplanter Spendenbetrag|Montant que vous donnez|Jumlah yang akan diberikan",
"dn.rate": "边际税率（%）|Tasa marginal (%)|Alíquota marginal (%)|Предельная ставка (%)|限界税率（%）|한계 세율 (%)|Grenzsteuersatz (%)|Taux marginal (%)|Tarif pajak marginal (%)",
"dn.realcost": "税后实际成本|coste real tras deducción|custo real após dedução|реальная стоимость после вычета|控除後の実質負担|공제 후 실부담|tatsächliche Kosten nach Abzug|coût réel après déduction|biaya nyata setelah potongan pajak",
"dn.taxsaved": "分项扣减时的省税额|ahorro si detalla|economia se detalhar|экономия при детализации|明細採用時の節税額|항목 공제 시 절세액|Ersparnis bei Einzelaufstellung|économie si vous détaillez|penghematan jika merinci",
"dn.daysleft": "距年底天数|días restantes del año|dias restantes do ano|дней до конца года|今年の残り日数|올해 남은 일수|Tage bis Jahresende|jours restants cette année|hari tersisa tahun ini",
"dn.receiptrule": "该金额的收据规则|regla de recibo en tu monto|regra de recibo no seu valor|правило квитанции для вашей суммы|その金額の領収書ルール|금액별 영수증 규칙|Quittungsregel für Ihren Betrag|règle de reçu à votre montant|aturan kwitansi sesuai jumlah Anda",
"share.share-my-givingmath": "分享我的捐赠计算|Compartir mi cálculo de donación|Compartir meu cálculo de doação|Поделиться моим расчётом пожертвования|自分の寄付計算を共有|내 기부 계산 공유|Meine Spendenrechnung teilen|Partager mon calcul de don|Bagikan hitungan donasi saya",
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
