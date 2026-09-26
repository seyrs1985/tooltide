# -*- coding: utf-8 -*-
"""One-shot: add tip.* keys x9 langs (pipe-packed)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"tip.budget": "节日小费总预算|Presupuesto total de propinas|Orçamento total de gorjetas|Общий бюджет на чаевые|ホリデーチップ予算の合計|연휴 팁 총예산|Gesamtes Trinkgeldbudget|Budget total de pourboires|Total anggaran tip liburan",
"tip.weekly": "每周固定服务者（保洁、遛狗员等）|Habituales semanales (limpiador, paseador de perros...)|Regulares semanais (diarista, passeador...)|Постоянные еженедельные (уборщик, выгульщик...)|毎週来る人（清掃、ドッグウォーカー等）|주간 정기 서비스 (청소부, 산책도우미 등)|Wöchentliche Stammkräfte (Reinigungskraft, Gassi-Service...)|Habituales semanales (limpiador, paseador...)|Langganan mingguan (cleaning service, dog walker dll.)",
"tip.occasional": "偶发服务者（理发师、临时保姆等）|Ayudantes ocasionales (peluquero, niñera...)|Ajudantes ocasionais (cabeleireiro, babá...)|Разовые помощники (парикмахер, няня...)|たまに来る人（美容師、ベビーシッター等）|가끔 이용하는 서비스 (미용사, 베이비시터 등)|Gelegentliche Helfer (Friseur, Babysitter...)|Aides occasionnels (coiffeur, baby-sitter...)|Pembantu sesekali (penata rambut, babysitter dll.)",
"tip.perweekly": "每位每周固定服务者|por habitual semanal|por regular semanal|каждому постоянному|1人あたり（毎週）|주간 정기 1인당|pro Stammkraft|par habituel|per langganan mingguan",
"tip.peroccasional": "每位偶发服务者|por ayudante ocasional|por ajudante ocasional|каждому разовому помощнику|1人あたり（たまに来る人）|가끔 이용 1인당|pro gelegentlichen Helfer|par aide occasionnel|per pembantu sesekali",
"tip.weeklytotal": "每周固定服务者小计|total a habituales semanales|total para regulares semanais|всего постоянным|毎週来る人への合計|주간 정기 합계|Total an Stammkräfte|total aux habituels|total untuk langganan mingguan",
"tip.cardleft": "剩余给卡片致谢对象|resto para las tarjetas|resta para os cartões|осталось на открытки|カードを贈る人向けに残り|카드 받을 사람 몫|Rest für Karten|reste pour les cartes|sisa untuk penerima kartu",
"share.share-my-tippingplan": "分享我的小费计划|Compartir mi plan de propinas|Compartir meu plano de gorjetas|Поделиться моим планом чаевых|自分のチップ計画を共有|내 팁 계획 공유|Mein Trinkgeldplan teilen|Partager mon plan de pourboires|Bagikan rencana tip saya",
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
