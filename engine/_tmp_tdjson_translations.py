# -*- coding: utf-8 -*-
"""One-shot: add td/json/jwt/lbl.status translations (13 keys x 9 langs)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"td.unit": "维持体重的每日千卡（TDEE）|kcal/día para mantener el peso (TDEE)|kcal/dia para manter o peso (TDEE)|ккал/день для поддержания веса (TDEE)|体重維持の1日kcal（TDEE）|체중 유지 하루 kcal (TDEE)|kcal/Tag zur Gewichtshaltung (TDEE)|kcal/jour pour maintenir le poids (TDEE)|kcal/hari untuk menjaga berat (TDEE)",
"td.bmr": "静息基础代谢（BMR）|Metabolismo basal (BMR)|Metabolismo basal (BMR)|Базовый метаболизм (BMR)|安静時の基礎代謝（BMR）|휴식 시 기초대사량 (BMR)|Grundumsatz (BMR)|Métabolisme de base (BMR)|Metabolisme dasar (BMR)",
"td.loss": "稳定减重（−500）|Pérdida constante (−500)|Perda constante (−500)|Стабильное похудение (−500)|着実な減量(−500)|꾸준한 감량 (−500)|Stetige Abnahme (−500)|Perte stable (−500)|Penurunan stabil (−500)",
"td.gain": "精瘦增重（+300）|Ganancia magra (+300)|Ganho magro (+300)|Чистый набор (+300)|精益な増量(+300)|린 게인 (+300)|Magerer Aufbau (+300)|Prise maigre (+300)|Penambahan lean (+300)",
"lbl.status": "状态|Estado|Estado|Статус|ステータス|상태|Status|Statut|Status",
"json.fmt": "格式化|Formatear|Formatar|Форматировать|整形|포맷|Formatieren|Formater|Format",
"json.minify": "压缩|Minificar|Minificar|Минифицировать|圧縮|압축|Minifizieren|Minifier|Perkecil",
"json.size": "大小|tamaño|tamanho|размер|サイズ|크기|Größe|taille|ukuran",
"json.kv": "键 + 值|claves + valores|chaves + valores|ключи + значения|キーと値|키 + 값|Schlüssel + Werte|clés + valeurs|kunci + nilai",
"json.depth": "最大深度|profundidad máx.|profundidade máx.|макс. глубина|最大の深さ|최대 깊이|max. Tiefe|profondeur max|kedalaman maks.",
"jwt.alg": "算法|Algoritmo|Algoritmo|Алгоритм|アルゴリズム|알고리즘|Algorithmus|Algorithme|Algoritma",
"jwt.expiry": "过期时间|Caducidad|Expiração|Срок действия|有効期限|만료|Ablauf|Expiration|Kedaluwarsa",
"jwt.claims": "声明|Claims|Claims|Клеймы|クレーム|클레임|Claims|Claims|Klaim",
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
