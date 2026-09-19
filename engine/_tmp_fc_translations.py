# -*- coding: utf-8 -*-
"""One-shot: add fc.* fuelcost-page keys x9 langs."""
import json, io

ORDER = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]
T = {
"fc.distance": "行程距离|Distancia del viaje|Distância da viagem|Дистанция поездки|走行距離|주행 거리|Fahrtstrecke|Distance du trajet|Jarak perjalanan",
"fc.consumption": "油耗|Consumo|Consumo|Расход|燃費|연비|Verbrauch|Consommation|Konsumsi",
"fc.price": "油价|Precio del combustible|Preço do combustível|Цена топлива|燃料価格|유류 가격|Kraftstoffpreis|Prix du carburant|Harga bahan bakar",
"fc.optus": "英里 / MPG / 美元每加仑|Millas / MPG / $ por galón|Milhas / MPG / $ por galão|Мили / MPG / $ за галлон|マイル / MPG / 1ガロンあたり$|마일 / MPG / 갤런당 $|Meilen / MPG / $ pro Gallone|Miles / MPG / $ par gallon|Mil / MPG / $ per galon",
"fc.opteu": "公里 / 升每百公里 / 美元每升|Kilómetros / L por 100 km / $ por litro|Quilômetros / L por 100 km / $ por litro|Километры / л на 100 км / $ за литр|キロ / 100kmあたりL / 1リットルあたり$|킬로미터 / 100km당 L / 리터당 $|Kilometer / l auf 100 km / $ pro Liter|Kilomètres / L aux 100 km / $ par litre|Kilometer / L per 100 km / $ per liter",
"fc.fuelneeded": "所需油量|combustible necesario|combustível necessário|необходимо топлива|必要な燃料|필요 연료|benötigter Kraftstoff|carburant nécessaire|bahan bakar yang dibutuhkan",
"fc.pp4": "每人（4 人同行）|por persona, 4 ocupantes|por pessoa, 4 ocupantes|на человека, 4 пассажира|1人あたり（4人乗車）|1인당 (4인 동승)|pro Person, 4 Insassen|par personne, 4 passagers|per orang, 4 penumpang",
"fc.roundtrip": "往返|ida y vuelta|ida e volta|туда и обратно|往復|왕복|Hin- und Rückweg|aller-retour|pulang pergi",
"fc.oneway": "单程油费|coste de combustible (solo ida)|custo de combustível (só ida)|стоимость топлива (в одну сторону)|片道の燃料コスト|편도 유류비|Kraftstoffkosten (einfach)|coût de carburant (aller simple)|biaya bahan bakar (sekali jalan)",
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
