# -*- coding: utf-8 -*-
"""One-shot: add share.* button translations (75 keys x 9 langs, pipe-packed).
Cross-checks against _tmp_share_texts.json so no slug is missed. Run once."""
import json, io, re

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"share.share-my-bmi": "分享我的 BMI|Compartir mi IMC|Compartir meu IMC|Поделиться моим ИМТ|自分のBMIを共有|내 BMI 공유|Mein BMI teilen|Partager mon IMC|Bagikan BMI saya",
"share.share-my-budget": "分享我的预算|Compartir mi presupuesto|Compartir meu orçamento|Поделиться моим бюджетом|自分の予算を共有|내 예산 공유|Mein Budget teilen|Partager mon budget|Bagikan anggaran saya",
"share.share-my-estimate": "分享我的估算|Compartir mi estimación|Compartir minha estimativa|Поделиться моей оценкой|自分の見積りを共有|내 추정치 공유|Meine Schätzung teilen|Partager mon estimation|Bagikan estimasi saya",
"share.share-my-gpa": "分享我的 GPA|Compartir mi GPA|Compartir meu GPA|Поделиться моим GPA|自分のGPAを共有|내 GPA 공유|Mein GPA teilen|Partager ma moyenne|Bagikan GPA saya",
"share.share-my-macros": "分享我的宏量营养|Compartir mis macros|Compartir meus macros|Поделиться моими БЖУ|自分のマクロを共有|내 매크로 공유|Meine Makros teilen|Partager mes macros|Bagikan makro saya",
"share.share-my-pace": "分享我的配速|Compartir mi ritmo|Compartir meu ritmo|Поделиться моим темпом|自分のペースを共有|내 페이스 공유|Mein Tempo teilen|Partager mon allure|Bagikan pace saya",
"share.share-my-paycheck-math": "分享我的工资计算|Compartir el cálculo de mi sueldo|Compartir o cálculo do meu salário|Поделиться расчётом моей зарплаты|自分の給与計算を共有|내 급여 계산 공유|Meine Gehaltsrechnung teilen|Partager le calcul de mon salaire|Bagikan hitungan gaji saya",
"share.share-my-plan": "分享我的计划|Compartir mi plan|Compartir meu plano|Поделиться моим планом|自分のプランを共有|내 계획 공유|Meinen Plan teilen|Partager mon plan|Bagikan rencana saya",
"share.share-my-sleep-math": "分享我的睡眠计算|Compartir mi cálculo de sueño|Compartir meu cálculo de sono|Поделиться расчётом моего сна|自分の睡眠計算を共有|내 수면 계산 공유|Meine Schlafrechnung teilen|Partager mon calcul de sommeil|Bagikan hitungan tidur saya",
"share.share-my-target": "分享我的目标|Compartir mi objetivo|Compartir minha meta|Поделиться моей целью|自分の目標を共有|내 목표 공유|Mein Ziel teilen|Partager mon objectif|Bagikan target saya",
"share.share-my-tdee": "分享我的 TDEE|Compartir mi TDEE|Compartir mi TDEE|Поделиться моим TDEE|自分のTDEEを共有|내 TDEE 공유|Mein TDEE teilen|Partager mon TDEE|Bagikan TDEE saya",
"share.share-my-total": "分享我的合计|Compartir mi total|Compartir meu total|Поделиться моим итогом|自分の合計を共有|내 합계 공유|Meine Summe teilen|Partager mon total|Bagikan total saya",
"share.share-my-week": "分享我的一周|Compartir mi semana|Compartir minha semana|Поделиться моей неделей|自分の週を共有|내 주간 공유|Meine Woche teilen|Partager ma semaine|Bagikan pekan saya",
"share.share-my-zones": "分享我的心率区间|Compartir mis zonas|Compartir minhas zonas|Поделиться моими зонами|自分のゾーンを共有|내 심박존 공유|Meine Zonen teilen|Partager mes zones|Bagikan zona saya",
"share.share-the-conversion": "分享换算结果|Compartir la conversión|Compartir a conversão|Поделиться конверсией|変換結果を共有|변환 결과 공유|Die Umrechnung teilen|Partager la conversion|Bagikan konversi",
"share.share-the-feels-like": "分享体感温度|Compartir la sensación térmica|Compartir a sensação térmica|Поделиться ощущаемой температурой|体感温度を共有|체감 온도 공유|Die gefühlte Temperatur teilen|Partager la température ressentie|Bagikan suhu terasa",
"share.share-the-result": "分享结果|Compartir el resultado|Compartir o resultado|Поделиться результатом|結果を共有|결과 공유|Das Ergebnis teilen|Partager le résultat|Bagikan hasil",
"share.share-the-score-not-the-password": "分享得分（不含密码）|Compartir la puntuación (no la contraseña)|Compartir a pontuação (não a senha)|Поделиться счётом (не паролем)|スコアを共有（パスワード除く）|점수 공유 (비밀번호 제외)|Den Score teilen (nicht das Passwort)|Partager le score (pas le mot de passe)|Bagikan skor (bukan kata sandi)",
"share.share-the-setting": "分享当前设置|Compartir este ajuste|Compartir este ajuste|Поделиться этой настройкой|この設定を共有|이 설정 공유|Diese Einstellung teilen|Partager ce réglage|Bagikan pengaturan ini",
"share.share-the-split": "分享分摊|Compartir el reparto|Compartir a divisão|Поделиться распределением|割り勘を共有|나눈 금액 공유|Die Aufteilung teilen|Partager le partage|Bagikan pembagian",
"share.share-the-trip-cost": "分享行程费用|Compartir el coste del viaje|Compartir o custo da viagem|Поделиться стоимостью поездки|旅費を共有|여행 비용 공유|Die Reisekosten teilen|Partager le coût du voyage|Bagikan biaya perjalanan",
"share.share-these-delay-times": "分享这些延迟时间|Compartir estos tiempos de espera|Compartir estes tempos de espera|Поделиться этими задержками|これらの遅延時間を共有|이 지연 시간들 공유|Diese Wartezeiten teilen|Partager ces temps d'attente|Bagikan waktu tunggu ini",
"share.share-these-odds": "分享这些赔率|Compartir estas cuotas|Compartir estas odds|Поделиться этими коэффициентами|これらのオッズを共有|이 배당률들 공유|Diese Quoten teilen|Partager ces cotes|Bagikan odds ini",
"share.share-these-times": "分享这些时间|Compartir estos horarios|Compartir estes horários|Поделиться этим расписанием|これらの時間を共有|이 시간들 공유|Diese Zeiten teilen|Partager ces horaires|Bagikan waktu-waktu ini",
"share.share-this-ac-size": "分享空调选型|Compartir este tamaño de AC|Compartir este tamanho de AC|Поделиться мощностью кондиционера|このエアコン容量を共有|이 에어컨 용량 공유|Diese Klimaanlagen-Größe teilen|Partager cette taille de climatisation|Bagikan kapasitas AC ini",
"share.share-this-audit": "分享这份自查清单|Compartir esta auditoría|Compartir esta auditoria|Поделиться этим аудитом|この監査を共有|이 점검 공유|Diese Prüfung teilen|Partager cet audit|Bagikan audit ini",
"share.share-this-break-even": "分享盈亏平衡点|Compartir el punto de equilibrio|Compartir o ponto de equilíbrio|Поделиться точкой безубыточности|損益分岐点を共有|손익분기점 공유|Den Break-Even-Punkt teilen|Partager le seuil de rentabilité|Bagikan titik impas",
"share.share-this-breakdown": "分享这份明细|Compartir este desglose|Compartir este detalhamento|Поделиться этой разбивкой|この内訳を共有|이 내역 공유|Diese Aufschlüsselung teilen|Partager ce détail|Bagikan rinciannya",
"share.share-this-brew": "分享冲煮参数|Compartir esta preparación|Compartir esta extração|Поделиться рецептом заваривания|この抽出を共有|이 브루 공유|Diese Zubereitung teilen|Partager cette préparation|Bagikan seduhan ini",
"share.share-this-burn": "分享消耗率|Compartir la tasa de consumo|Compartir a taxa de queima|Поделиться скоростью расхода|バーンレートを共有|번 레이트 공유|Die Burn-Rate teilen|Partager le burn rate|Bagikan burn rate",
"share.share-this-cagr": "分享这个年化收益率|Compartir esta CAGR|Compartir este CAGR|Поделиться этим CAGR|このCAGRを共有|이 CAGR 공유|Diese CAGR teilen|Partager ce TCAC|Bagikan CAGR ini",
"share.share-this-comparison": "分享这个对比|Compartir esta comparación|Compartir esta comparação|Поделиться этим сравнением|この比較を共有|이 비교 공유|Diesen Vergleich teilen|Partager cette comparaison|Bagikan perbandingan ini",
"share.share-this-converter": "分享这个换算器|Compartir este conversor|Compartir este conversor|Поделиться этим конвертером|このコンバーターを共有|이 변환기 공유|Diesen Konverter teilen|Partager ce convertisseur|Bagikan konverter ini",
"share.share-this-cost": "分享这笔费用|Compartir este coste|Compartir este custo|Поделиться этой стоимостью|このコストを共有|이 비용 공유|Diese Kosten teilen|Partager ce coût|Bagikan biaya ini",
"share.share-this-cost-basis": "分享持仓成本|Compartir el coste base|Compartir o custo base|Поделиться средней ценой покупки|取得単価を共有|평단가 공유|Die Kostenbasis teilen|Partager le prix de revient|Bagikan harga dasar",
"share.share-this-cost-math": "分享费用计算|Compartir el cálculo de costes|Compartir o cálculo de custo|Поделиться расчётом стоимости|コスト計算を共有|비용 계산 공유|Die Kostenrechnung teilen|Partager le calcul des coûts|Bagikan hitungan biaya",
"share.share-this-countdown": "分享这个倒计时|Compartir esta cuenta atrás|Compartir esta contagem regressiva|Поделиться этим обратным отсчётом|このカウントダウンを共有|이 카운트다운 공유|Diesen Countdown teilen|Partager ce compte à rebours|Bagikan hitung mundur ini",
"share.share-this-deal-math": "分享优惠计算|Compartir el cálculo de la oferta|Compartir o cálculo da oferta|Поделиться расчётом скидки|このお得計算を共有|이 혜택 계산 공유|Die Angebotsrechnung teilen|Partager le calcul de l'offre|Bagikan hitungan penawaran",
"share.share-this-dew-point": "分享露点温度|Compartir el punto de rocío|Compartir o ponto de orvalho|Поделиться точкой росы|露点温度を共有|이슬점 공유|Den Taupunkt teilen|Partager le point de rosée|Bagikan titik embun",
"share.share-this-dose": "分享这个剂量|Compartir esta dosis|Compartir esta dose|Поделиться этой дозировкой|この用量を共有|이 용량 공유|Diese Dosis teilen|Partager cette dose|Bagikan dosis ini",
"share.share-this-draw": "分享这次抽选|Compartir este sorteo|Compartir este sorteio|Поделиться этим розыгрышем|この抽選を共有|이 추첨 공유|Diese Ziehung teilen|Partager ce tirage|Bagikan hasil undian ini",
"share.share-this-due-date": "分享预产期|Compartir la fecha probable|Compartir a data provável|Поделиться предполагаемой датой|出産予定日を共有|출산 예정일 공유|Den Geburtstermin teilen|Partager la date prévue|Bagikan tanggal perkiraan",
"share.share-this-estimate": "分享这个估算|Compartir esta estimación|Compartir esta estimativa|Поделиться этой оценкой|この見積りを共有|이 추정치 공유|Diese Schätzung teilen|Partager cette estimation|Bagikan estimasi ini",
"share.share-this-guide": "分享这份指南|Compartir esta guía|Compartir este guia|Поделиться этим руководством|このガイドを共有|이 가이드 공유|Diesen Leitfaden teilen|Partager ce guide|Bagikan panduan ini",
"share.share-this-line": "分享这一行|Compartir esta línea|Compartir esta linha|Поделиться этой строкой|この行を共有|이 줄 공유|Diese Zeile teilen|Partager cette ligne|Bagikan baris ini",
"share.share-this-math": "分享这个计算|Compartir este cálculo|Compartir este cálculo|Поделиться этим расчётом|この計算を共有|이 계산 공유|Diese Rechnung teilen|Partager ce calcul|Bagikan hitungan ini",
"share.share-this-max": "分享这个最大值|Compartir este máximo|Compartir este máximo|Поделиться этим максимумом|この最大値を共有|이 최댓값 공유|Diesen Maximalwert teilen|Partager ce maximum|Bagikan nilai maksimum ini",
"share.share-this-meeting-time": "分享会议时间|Compartir el horario de la reunión|Compartir o horário da reunião|Поделиться временем встречи|会議時間を共有|회의 시간 공유|Die Meetingzeit teilen|Partager l'heure de la réunion|Bagikan waktu rapat",
"share.share-this-number": "分享这个数字|Compartir este número|Compartir este número|Поделиться этим числом|この数字を共有|이 숫자 공유|Diese Zahl teilen|Partager ce nombre|Bagikan angka ini",
"share.share-this-payment": "分享这笔付款|Compartir este pago|Compartir este pagamento|Поделиться этим платежом|この支払いを共有|이 지불 공유|Diese Zahlung teilen|Partager ce paiement|Bagikan pembayaran ini",
"share.share-this-payoff-plan": "分享还债计划|Compartir el plan de pago|Compartir o plano de quitação|Поделиться планом выплат|返済計画を共有|상환 계획 공유|Den Tilgungsplan teilen|Partager le plan de remboursement|Bagikan rencana pelunasan",
"share.share-this-pet-s-age": "分享宠物年龄|Compartir la edad de la mascota|Compartir a idade do pet|Поделиться возрастом питомца|ペットの年齢を共有|반려동물 나이 공유|Das Haustieralter teilen|Partager l'âge de l'animal|Bagikan usia hewan peliharaan",
"share.share-this-plan": "分享这个计划|Compartir este plan|Compartir este plano|Поделиться этим планом|このプランを共有|이 플랜 공유|Diesen Plan teilen|Partager ce plan|Bagikan rencana ini",
"share.share-this-position-size": "分享仓位计算|Compartir el tamaño de la posición|Compartir o tamanho da posição|Поделиться размером позиции|ポジションサイズを共有|포지션 크기 공유|Die Positionsgröße teilen|Partager la taille de position|Bagikan ukuran posisi",
"share.share-this-projection": "分享这个预测|Compartir esta proyección|Compartir esta projeção|Поделиться этим прогнозом|この予測を共有|이 예측 공유|Diese Projektion teilen|Partager cette projection|Bagikan proyeksi ini",
"share.share-this-range": "分享这个区间|Compartir este rango|Compartir esta faixa|Поделиться этим диапазоном|この範囲を共有|이 범위 공유|Diesen Bereich teilen|Partager cette plage|Bagikan rentang ini",
"share.share-this-ratio": "分享这个比例|Compartir esta proporción|Compartir esta proporção|Поделиться этим соотношением|この比率を共有|이 비율 공유|Dieses Verhältnis teilen|Partager ce ratio|Bagikan rasio ini",
"share.share-this-readability-score": "分享可读性得分|Compartir la puntuación de legibilidad|Compartir a pontuação de legibilidade|Поделиться оценкой читаемости|読みやすさスコアを共有|가독성 점수 공유|Den Lesbarkeitsscore teilen|Partager le score de lisibilité|Bagikan skor keterbacaan",
"share.share-this-recipe": "分享这个配方|Compartir esta receta|Compartir esta receita|Поделиться этим рецептом|このレシピを共有|이 레시피 공유|Dieses Rezept teilen|Partager cette recette|Bagikan resep ini",
"share.share-this-result": "分享这个结果|Compartir este resultado|Compartir este resultado|Поделиться этим результатом|この結果を共有|이 결과 공유|Dieses Ergebnis teilen|Partager ce résultat|Bagikan hasil ini",
"share.share-this-roast-plan": "分享烘焙计划|Compartir el plan de tueste|Compartir o plano de torra|Поделиться планом обжарки|ロースト計画を共有|로스팅 계획 공유|Den Röstplan teilen|Partager le plan de torréfaction|Bagikan rencana sangrai",
"share.share-this-round-math": "分享凑整计算|Compartir el redondeo|Compartir o arredondamento|Поделиться этим округлением|丸め計算を共有|반올림 계산 공유|Die Rundungsrechnung teilen|Partager cet arrondi|Bagikan hitungan pembulatan",
"share.share-this-schedule": "分享这个日程|Compartir este horario|Compartir este cronograma|Поделиться этим расписанием|このスケジュールを共有|이 일정 공유|Diesen Zeitplan teilen|Partager ce calendrier|Bagikan jadwal ini",
"share.share-this-stopwatch": "分享这个秒表成绩|Compartir este cronómetro|Compartir este cronômetro|Поделиться результатом секундомера|このストップウォッチを共有|이 스톱워치 공유|Diese Stoppuhr teilen|Partager ce chronomètre|Bagikan stopwatch ini",
"share.share-this-summary": "分享这份摘要|Compartir este resumen|Compartir este resumo|Поделиться этим резюме|このサマリーを共有|이 요약 공유|Diese Zusammenfassung teilen|Partager ce résumé|Bagikan ringkasan ini",
"share.share-this-target": "分享这个目标|Compartir este objetivo|Compartir esta meta|Поделиться этой целью|この目標を共有|이 목표 공유|Dieses Ziel teilen|Partager cet objectif|Bagikan target ini",
"share.share-this-time-card": "分享这份工时卡|Compartir esta ficha de horas|Compartir este cartão de ponto|Поделиться этим табелем|このタイムカードを共有|이 타임카드 공유|Diese Zeiterfassung teilen|Partager cette feuille d'heures|Bagikan kartu waktu ini",
"share.share-this-timer": "分享这个计时器|Compartir este temporizador|Compartir este temporizador|Поделиться этим таймером|このタイマーを共有|이 타이머 공유|Diesen Timer teilen|Partager ce minuteur|Bagikan timer ini",
"share.share-this-tool": "分享这个工具|Compartir esta herramienta|Compartir esta ferramenta|Поделиться этим инструментом|このツールを共有|이 도구 공유|Dieses Tool teilen|Partager cet outil|Bagikan alat ini",
"share.share-this-trade-math": "分享交易计算|Compartir el cálculo de la operación|Compartir o cálculo da operação|Поделиться расчётом сделки|トレード計算を共有|이 거래 계산 공유|Diese Trade-Rechnung teilen|Partager le calcul de trade|Bagikan hitungan trading ini",
"share.share-this-value": "分享这个数值|Compartir este valor|Compartir este valor|Поделиться этим значением|この値を共有|이 값 공유|Diesen Wert teilen|Partager cette valeur|Bagikan nilai ini",
"share.share-this-volume": "分享这个音量|Compartir este volumen|Compartir este volume|Поделиться этим объёмом|この音量を共有|이 볼륨 공유|Dieses Volumen teilen|Partager ce volume|Bagikan volume ini",
"share.share-this-week": "分享这一周|Compartir esta semana|Compartir esta semana|Поделиться этой неделей|この週を共有|이 주 공유|Diese Woche teilen|Partager cette semaine|Bagikan pekan ini",
"share.share-today-s-count": "分享今日计数|Compartir el conteo de hoy|Compartir a contagem de hoje|Поделиться сегодняшним счётом|今日のカウントを共有|오늘의 카운트 공유|Die heutige Zählung teilen|Partager le comptage du jour|Bagikan hitungan hari ini",
"share.share-tonight-s-light": "分享今晚光照|Compartir la luz de esta noche|Compartir a luz de hoje à noite|Поделиться светом этой ночи|今夜の光照を共有|오늘 밤 빛 공유|Das Licht heute Nacht teilen|Partager la lumière de ce soir|Bagikan cahaya malam ini",
}

slugs = json.load(io.open("_tmp_share_texts.json", encoding="utf-8"))
missing = [k for k in slugs if k not in T]
extra = [k for k in T if k not in slugs]
if missing:
    print("MISSING TRANSLATIONS for:", missing)
    raise SystemExit(1)

p = "_i18n_tables.json"
d = json.load(io.open(p, encoding="utf-8"))
n = 0
for slug, text in slugs.items():
    vals = T[slug].split("|")
    for lang, txt in zip(ORDER, vals):
        entries = [tuple(x) for x in d["chrome"][lang]]
        if any(kk == slug for kk, _ in entries):
            continue
        entries.append((slug, txt))
        d["chrome"][lang] = [list(e) for e in entries]
        n += 1
json.dump(d, io.open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
io.open(p, "a", encoding="utf-8").write("\n")
print("added", n, "values; zh keys:", len(d["chrome"]["zh"]))
