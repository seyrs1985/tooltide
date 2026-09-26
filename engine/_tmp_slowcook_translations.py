# -*- coding: utf-8 -*-
"""One-shot: add slowcook.* + share.share-my-conversion keys x9 (pipe-packed)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"slowcook.ovenmin": "食谱中的烤箱时间（分钟）|Tiempo de horno en la receta (minutos)|Tempo de forno na receita (minutos)|Время в духовке по рецепту (мин)|レシピのオーブン時間（分）|레시피의 오븐 시간 (분)|Ofenzeit im Rezept (Minuten)|Temps au four dans la recette (minutes)|Waktu oven dalam resep (menit)",
"slowcook.setting": "慢炖锅档位|Ajuste de la olla lenta|Ajuste da panela lenta|Режим мультиварки|スロークッカーの設定|슬로우쿠커 설정|Einstellung des Schongarsers|Réglage de la mijoteuse|Pengaturan slow cooker",
"slowcook.incooker": "慢炖锅烹饪时间|en la olla lenta|na panela lenta|в мультиварке|スロークッカーでの時間|슬로우쿠커에서|im Schongarer|dans la mijoteuse|di slow cooker",
"slowcook.othersetting": "另一档位时间|el otro ajuste|a outra configuração|другой режим|もう一方の設定|다른 설정|die andere Einstellung|l autre réglage|pengaturan lainnya",
"slowcook.liquid": "食谱中的液体量|líquido en la receta|líquido na receita|жидкость в рецепте|レシピの液体|레시피의 액체|Flüssigkeit im Rezept|liquide dans la recette|cairan dalam resep",
"slowcook.dairy": "乳制品与海鲜后放|lácteos y mariscos van al final|laticínios e frutos do mar vão por último|молочное и морепродукты в конце|乳製品と魚介は後から|유제품과 해산물은 마지막에|Milchprodukte und Meeresfrüchte zuletzt|produits laitiers et fruits de mer à la fin|susu dan seafood dimasukkan terakhir",
"share.share-my-conversion": "分享我的换算结果|Compartir mi conversión|Compartir minha conversão|Поделиться моим пересчётом|自分の換算を共有|내 변환 공유|Meine Umrechnung teilen|Partager ma conversion|Bagikan konversi saya",
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
