# -*- coding: utf-8 -*-
"""One-shot: add fw.* + ppie.* + 2 share keys x9 langs (pipe-packed)."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"fw.area": "供暖面积（平方英尺）|Área a calentar (pies cuadrados)|Área aquecida (pés quadrados)|Отапливаемая площадь (кв. футов)|暖房面積（平方フィート）|난방 면적 (제곱피트)|Zu beheizende Fläche (Quadratfuß)|Surface à chauffer (pieds carrés)|Area yang dipanaskan (kaki persegi)",
"fw.climate": "气候|Clima|Clima|Климат|気候|기후|Klima|Climat|Iklim",
"fw.species": "木种|Especie|Espécie|Порода|樹種|나무 종류|Holzart|Essence|Jenis kayu",
"fw.price": "每考得价格（$）|Precio por cuerda ($)|Preço por corda ($)|Цена за корд ($)|1コードの価格（$）|1코르드당 가격 ($)|Preis pro Raummeter ($)|Prix par corde ($)|Harga per kord ($)",
"fw.cords": "越冬所需木材量（考得）|cuerdas para el invierno|cordas para o inverno|кордов на зиму|冬に必要なコード数|겨울용 코드 수|Raummeter für den Winter|cordes pour l hiver|kord untuk musim dingin",
"fw.cost": "木材总费用|coste total de la leña|custo total da lenha|общая стоимость дров|薪の合計コスト|총 장작 비용|Gesamtkosten für Holz|coût total du bois|total biaya kayu",
"fw.pmbtu": "每百万 BTU 成本|$ por millón de Btu|$ por milhão de Btu|$ за миллион БТЕ|100万Btuあたりのコスト|백만 BTU당 비용|Kosten pro Million Btu|coût par million de BTU|biaya per juta Btu",
"fw.electric": "同等热量的电暖费用|mismo calor, eléctrico|mesmo calor, elétrico|то же тепло, электроотопление|同じ熱量の電気|동일 열량의 전기|gleiche Wärme, elektrisch|même chaleur, électrique|panas yang sama, listrik",
"share.share-my-winterwood": "分享我的越冬木材估算|Compartir mi estimación de leña|Compartir minha estimativa de lenha|Поделиться моей оценкой дров|自分の薪の見積りを共有|내 겨울 장작 추정 공유|Meine Brennholzschätzung teilen|Partager mon estimation de bois|Bagikan perkiraan kayu musim dingin saya",
"ppie.guests": "宾客人数|Invitados|Convidados|Гости|ゲスト数|손님 수|Gäste|Invités|Jumlah tamu",
"ppie.slices": "每人块数|Porciones por invitado|Fatias por convidado|кусков на человека|1人あたりの切れ端|1인당 조각 수|Stücke pro Gast|parts par invité|irisan per tamu",
"ppie.pies": "9 英寸派（个）|pies de 9 pulgadas|tortas de 23 cm|пирогов 9 дюймов|9インチパイの数|9인치 파이 수|9-Zoll-Kuchen|tourtes de 9 pouces|pai 9 inci",
"ppie.cups": "南瓜泥（杯）|tazas de puré|xícaras de purê|стаканов пюре|カップのピューレ|퓌레 컵|Tassen Püree|tasses de purée|cangkir pure",
"ppie.cans": "15 盎司罐头|latas de 15 oz|latas de 425 g|банки 425 г|15オンス缶|15온스 캔|425-g-Dosen|boîtes de 425 g|kaleng 15 ons",
"ppie.eggssugar": "蛋 + 糖（杯）|huevos + azúcar (tazas)|ovos + açúcar (xícaras)|яйца + сахар (стаканы)|卵+砂糖（カップ）|계란 + 설탕 (컵)|Eier + Zucker (Tassen)|œufs + sucre (tasses)|telur + gula (cangkir)",
"share.share-piemath": "分享派计算|Compartir el cálculo del pastel|Compartir o cálculo da torta|Поделиться расчётом пирога|パイ計算を共有|파이 계산 공유|Die Kuchenrechnung teilen|Partager le calcul de la tarte|Bagikan hitungan pai",
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
