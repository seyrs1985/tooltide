# -*- coding: utf-8 -*-
"""One-shot R9 (BUG-013 continuation): localize the feedback + validation
string family. 19 new keys x9 languages into _i18n_tables.json, plus tools.py
wiring: render() gets a shared window.TT() helper, all 106 'Copied!' feedbacks,
8 plain copy buttons (label via data-i18n="ui.copy" + localized restore), and
16 per-renderer validation/status strings. Safe to re-run."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]

# ---------------- 1) tools.py wiring ----------------
p = os.path.join(HERE, "engine", "tools.py")
s = io.open(p, encoding="utf-8").read()

# 1a. shared TT helper prepended once per tool page via render()
old_render = "def render(tool, args):\n    return TOOLS[tool](args)"
new_render = (
    "TT_SNIPPET = ('<script>window.TT=function(k,f){try{var v=window.npT?window.npT(k):null;'"
    "\n               '}catch(e){}return v||f};</script>')\n\n\n"
    "def render(tool, args):\n    return TT_SNIPPET + TOOLS[tool](args)"
)
assert s.count(old_render) == 1, "render() anchor not found"
s = s.replace(old_render, new_render)

# 1b. exact-match replacements: (old, new, expected_count)
REPL = [
    # copy feedback, all renderers
    ("textContent='Copied!'",
     "textContent=TT('ui.copied','Copied!')", 106),
    # plain copy buttons: localized restore
    ("textContent='Copy';",
     "textContent=TT('ui.copy','Copy');", 8),
    # plain copy buttons: static label wired to existing ui.copy key
    (">Copy</button>",
     " data-i18n=\"ui.copy\">Copy</button>", 8),
    # password generator
    ("value='Select at least one character set'",
     "value=TT('pw.noset','Select at least one character set')", 1),
    # random number generator
    ("note.textContent='Maximum must be greater than minimum.'",
     "note.textContent=TT('rng.maxmin','Maximum must be greater than minimum.')", 1),
    ("note.textContent='Count must be between 1 and 100.'",
     "note.textContent=TT('rng.count','Count must be between 1 and 100.')", 1),
    ("note.textContent='Cannot pick '+count+' unique numbers from a range of '+size+'. Widen the range or allow duplicates.'",
     "note.textContent=TT('rng.cantpick','Cannot pick {n} unique numbers from a range of {m}. Widen the range or allow duplicates.').replace('{n}',count).replace('{m}',size)", 1),
    ("note.textContent='No-duplicates applies to whole numbers only.'",
     "note.textContent=TT('rng.nodup','No-duplicates applies to whole numbers only.')", 1),
    ("note.textContent='Generated '+out.length+' number'+(out.length>1?'s':'')+' · crypto-secure · nothing recorded.'",
     "note.textContent=TT('rng.gen','Generated: {n} · crypto-secure · nothing recorded.').replace('{n}',out.length)", 1),
    # roman numerals
    ("note.textContent='Not a valid standard Roman numeral (1–3999).'",
     "note.textContent=TT('roman.invalid','Not a valid standard Roman numeral (1–3999).')", 1),
    # grade calculator
    ("txt.textContent='needed on the final'",
     "txt.textContent=TT('gr.needlbl','needed on the final')", 2),
    ("txt.textContent='— target already secured 🎉'",
     "txt.textContent=TT('gr.secured','— target already secured 🎉')", 1),
    ("txt.textContent='— mathematically out of reach'",
     "txt.textContent=TT('gr.outreach','— mathematically out of reach')", 1),
    # big number / primality
    ("note.textContent='Whole numbers only.'",
     "note.textContent=TT('num.whole','Whole numbers only.')", 1),
    ("out.textContent='Not prime'",
     "out.textContent=TT('prime.no','Not prime')", 2),
    ("out.textContent='Prime!'",
     "out.textContent=TT('prime.yes','Prime!')", 1),
    ("note.textContent='Numbers below 2 are neither prime nor composite.'",
     "note.textContent=TT('prime.lt2','Numbers below 2 are neither prime nor composite.')", 1),
    ("note.textContent=v+' is prime (it is in the base list).'",
     "note.textContent=TT('prime.list','{v} is prime (it is in the base list).').replace('{v}',v)", 1),
    ("note.textContent='Divisible by '+small[i]+'.'",
     "note.textContent=TT('prime.div','Divisible by {n}.').replace('{n}',small[i].toString())", 1),
    # epoch converter
    ("textContent='out of range'",
     "textContent=TT('ep.range','out of range')", 1),
    # binary ↔ decimal
    ("note.textContent='Number too large.'",
     "note.textContent=TT('bindec.big','Number too large.')", 1),
    ("note.textContent=v+' decimal = '+b+' binary'",
     "note.textContent=TT('bindec.note','{d} decimal = {b} binary').replace('{d}',v).replace('{b}',b)", 1),
    # temperature
    ("'Below absolute zero - physically impossible.'",
     "TT('temp.belowabs','Below absolute zero - physically impossible.')", 1),
]
for old, new, want in REPL:
    got = s.count(old)
    assert got == want, "count %d != %d for: %s" % (got, want, old[:60])
    s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("tools.py: %d replacement groups wired" % len(REPL))

# ---------------- 2) i18n tables: 19 keys x9 ----------------
KEYS = {
    "ui.copied": {
        "zh": "已复制!", "es": "¡Copiado!", "pt": "Copiado!",
        "ru": "Скопировано!", "ja": "コピーしました", "ko": "복사됨!",
        "de": "Kopiert!", "fr": "Copié !", "id": "Tersalin!"},
    "pw.noset": {
        "zh": "请至少选择一种字符集",
        "es": "Selecciona al menos un conjunto de caracteres",
        "pt": "Selecione pelo menos um conjunto de caracteres",
        "ru": "Выберите хотя бы один набор символов",
        "ja": "文字種を1つ以上選択してください",
        "ko": "문자 집합을 하나 이상 선택하세요",
        "de": "Bitte mindestens einen Zeichensatz wählen",
        "fr": "Sélectionnez au moins un jeu de caractères",
        "id": "Pilih setidaknya satu kumpulan karakter"},
    "rng.maxmin": {
        "zh": "最大值必须大于最小值。",
        "es": "El máximo debe ser mayor que el mínimo.",
        "pt": "O máximo deve ser maior que o mínimo.",
        "ru": "Максимум должен быть больше минимума.",
        "ja": "最大値は最小値より大きくしてください。",
        "ko": "최댓값은 최솟값보다 커야 합니다.",
        "de": "Das Maximum muss größer als das Minimum sein.",
        "fr": "Le maximum doit être supérieur au minimum.",
        "id": "Maksimum harus lebih besar dari minimum."},
    "rng.count": {
        "zh": "数量必须在 1 到 100 之间。",
        "es": "La cantidad debe estar entre 1 y 100.",
        "pt": "A quantidade deve estar entre 1 e 100.",
        "ru": "Количество должно быть от 1 до 100.",
        "ja": "個数は1〜100の間にしてください。",
        "ko": "개수는 1~100 사이여야 합니다.",
        "de": "Die Anzahl muss zwischen 1 und 100 liegen.",
        "fr": "Le nombre doit être compris entre 1 et 100.",
        "id": "Jumlah harus antara 1 dan 100."},
    "rng.cantpick": {
        "zh": "范围只有 {m} 个数，无法取 {n} 个不重复的数。请扩大范围或允许重复。",
        "es": "No se pueden elegir {n} números únicos de un rango de {m}. Amplía el rango o permite duplicados.",
        "pt": "Não é possível escolher {n} números únicos de um intervalo de {m}. Amplie o intervalo ou permita duplicados.",
        "ru": "Нельзя выбрать {n} уникальных чисел из диапазона из {m}. Расширьте диапазон или разрешите повторы.",
        "ja": "{m} 個の範囲から重複のない {n} 個は選べません。範囲を広げるか重複を許可してください。",
        "ko": "{m}개 범위에서 고유한 {n}개를 뽑을 수 없습니다. 범위를 넓히거나 중복을 허용하세요.",
        "de": "{n} eindeutige Zahlen aus einem Bereich von {m} nicht möglich. Bereich erweitern oder Duplikate erlauben.",
        "fr": "Impossible de choisir {n} nombres uniques dans une plage de {m}. Élargissez la plage ou autorisez les doublons.",
        "id": "Tidak bisa mengambil {n} angka unik dari rentang {m}. Perluas rentang atau izinkan duplikat."},
    "rng.nodup": {
        "zh": "“不重复”仅适用于整数。",
        "es": "«Sin duplicados» solo se aplica a números enteros.",
        "pt": "«Sem duplicados» aplica-se apenas a números inteiros.",
        "ru": "«Без повторов» применяется только к целым числам.",
        "ja": "「重複なし」は整数のみに適用されます。",
        "ko": "'중복 없음'은 정수에만 적용됩니다.",
        "de": "„Ohne Duplikate“ gilt nur für ganze Zahlen.",
        "fr": "« Sans doublons » s'applique uniquement aux nombres entiers.",
        "id": "'Tanpa duplikat' hanya berlaku untuk bilangan bulat."},
    "rng.gen": {
        "zh": "已生成：{n} 个 · 加密安全 · 不记录。",
        "es": "Generados: {n} · criptoseguro · no se registra nada.",
        "pt": "Gerados: {n} · criptograficamente seguro · nada é registrado.",
        "ru": "Сгенерировано: {n} · криптостойко · ничего не сохраняется.",
        "ja": "生成：{n} 個 · 暗号学的に安全 · 記録なし。",
        "ko": "생성됨: {n}개 · 암호학적 난수 · 기록 없음.",
        "de": "Generiert: {n} · kryptografisch sicher · nichts gespeichert.",
        "fr": "Générés : {n} · crypto-sûr · rien n'est enregistré.",
        "id": "Dibuat: {n} · aman-kripto · tidak ada yang dicatat."},
    "roman.invalid": {
        "zh": "不是有效的标准罗马数字（1–3999）。",
        "es": "No es un numeral romano estándar válido (1–3999).",
        "pt": "Não é um numeral romano padrão válido (1–3999).",
        "ru": "Это не корректное стандартное римское число (1–3999).",
        "ja": "有効な標準ローマ数字ではありません（1〜3999）。",
        "ko": "유효한 표준 로마 숫자가 아닙니다(1–3999).",
        "de": "Keine gültige römische Standardzahl (1–3999).",
        "fr": "Ce n'est pas un chiffre romain standard valide (1–3999).",
        "id": "Bukan angka Romawi standar yang valid (1–3999)."},
    "gr.needlbl": {
        "zh": "期末考所需的分数",
        "es": "necesario en el examen final",
        "pt": "necessário na prova final",
        "ru": "необходимо на финальном экзамене",
        "ja": "期末試験で必要な点数",
        "ko": "기말고사에서 필요한 점수",
        "de": "in der Abschlussprüfung nötig",
        "fr": "nécessaire à l'examen final",
        "id": "yang dibutuhkan di ujian akhir"},
    "gr.secured": {
        "zh": "— 目标已稳拿 🎉",
        "es": "— objetivo ya asegurado 🎉",
        "pt": "— meta já garantida 🎉",
        "ru": "— цель уже достигнута 🎉",
        "ja": "— 目標はすでに確定 🎉",
        "ko": "— 목표 이미 달성 🎉",
        "de": "— Ziel bereits erreicht 🎉",
        "fr": "— objectif déjà atteint 🎉",
        "id": "— target sudah tercapai 🎉"},
    "gr.outreach": {
        "zh": "— 数学上已无可能",
        "es": "— matemáticamente fuera de alcance",
        "pt": "— matematicamente fora de alcance",
        "ru": "— математически недостижимо",
        "ja": "— 数学的に届きません",
        "ko": "— 수학적으로 불가능",
        "de": "— mathematisch nicht mehr erreichbar",
        "fr": "— mathématiquement hors d'atteinte",
        "id": "— secara matematis tidak mungkin"},
    "num.whole": {
        "zh": "只能输入整数。",
        "es": "Solo números enteros.",
        "pt": "Apenas números inteiros.",
        "ru": "Только целые числа.",
        "ja": "整数のみ入力できます。",
        "ko": "정수만 입력할 수 있습니다.",
        "de": "Nur ganze Zahlen.",
        "fr": "Nombres entiers uniquement.",
        "id": "Hanya bilangan bulat."},
    "prime.lt2": {
        "zh": "小于 2 的数既不是质数也不是合数。",
        "es": "Los números menores que 2 no son primos ni compuestos.",
        "pt": "Números menores que 2 não são primos nem compostos.",
        "ru": "Числа меньше 2 не являются ни простыми, ни составными.",
        "ja": "2 未満の数は素数でも合成数でもありません。",
        "ko": "2 미만의 수는 소수도 합성수도 아닙니다.",
        "de": "Zahlen unter 2 sind weder prim noch zusammengesetzt.",
        "fr": "Les nombres inférieurs à 2 ne sont ni premiers ni composés.",
        "id": "Angka di bawah 2 bukan prima maupun komposit."},
    "prime.yes": {
        "zh": "是质数！", "es": "¡Es primo!", "pt": "É primo!",
        "ru": "Простое число!", "ja": "素数です！", "ko": "소수입니다!",
        "de": "Primzahl!", "fr": "Nombre premier !", "id": "Prima!"},
    "prime.no": {
        "zh": "不是质数", "es": "No es primo", "pt": "Não é primo",
        "ru": "Не простое", "ja": "素数ではありません", "ko": "소수가 아님",
        "de": "Keine Primzahl", "fr": "Pas premier", "id": "Bukan prima"},
    "prime.list": {
        "zh": "{v} 是质数（它在基础列表中）。",
        "es": "{v} es primo (está en la lista base).",
        "pt": "{v} é primo (está na lista base).",
        "ru": "{v} — простое (есть в базовом списке).",
        "ja": "{v} は素数です（基本リスト内）。",
        "ko": "{v}은(는) 소수입니다(기본 목록에 있음).",
        "de": "{v} ist eine Primzahl (in der Basisliste).",
        "fr": "{v} est premier (il est dans la liste de base).",
        "id": "{v} adalah prima (ada di daftar dasar)."},
    "prime.div": {
        "zh": "可被 {n} 整除。",
        "es": "Divisible por {n}.",
        "pt": "Divisível por {n}.",
        "ru": "Делится на {n}.",
        "ja": "{n} で割り切れます。",
        "ko": "{n}으로 나누어 떨어짐.",
        "de": "Durch {n} teilbar.",
        "fr": "Divisible par {n}.",
        "id": "Dapat dibagi {n}."},
    "ep.range": {
        "zh": "超出范围", "es": "fuera de rango", "pt": "fora do intervalo",
        "ru": "вне диапазона", "ja": "範囲外", "ko": "범위를 벗어남",
        "de": "außerhalb des Bereichs", "fr": "hors plage", "id": "di luar rentang"},
    "bindec.big": {
        "zh": "数字太大。",
        "es": "El número es demasiado grande.",
        "pt": "O número é grande demais.",
        "ru": "Слишком большое число.",
        "ja": "数値が大きすぎます。",
        "ko": "숫자가 너무 큽니다.",
        "de": "Zahl zu groß.",
        "fr": "Nombre trop grand.",
        "id": "Angka terlalu besar."},
    "bindec.note": {
        "zh": "十进制 {d} = 二进制 {b}",
        "es": "{d} decimal = {b} binario",
        "pt": "{d} decimal = {b} binário",
        "ru": "{d} в десятичной = {b} в двоичной",
        "ja": "10 進数 {d} = 2 進数 {b}",
        "ko": "10진수 {d} = 2진수 {b}",
        "de": "{d} dezimal = {b} binär",
        "fr": "{d} décimal = {b} binaire",
        "id": "{d} desimal = {b} biner"},
    "temp.belowabs": {
        "zh": "低于绝对零度——物理上不可能。",
        "es": "Por debajo del cero absoluto: físicamente imposible.",
        "pt": "Abaixo do zero absoluto — fisicamente impossível.",
        "ru": "Ниже абсолютного нуля — физически невозможно.",
        "ja": "絶対零度未満 — 物理的に不可能です。",
        "ko": "절대영도 이하 — 물리적으로 불가능합니다.",
        "de": "Unter dem absoluten Nullpunkt — physikalisch unmöglich.",
        "fr": "En dessous du zéro absolu — physiquement impossible.",
        "id": "Di bawah nol mutlak — secara fisika tidak mungkin."},
}

tp = os.path.join(HERE, "engine", "_i18n_tables.json")
with io.open(tp, encoding="utf-8") as f:
    tabs = json.load(f)
added = 0
for lang in LANGS:
    existing = set(k for k, _ in tabs["chrome"][lang])
    for key, tr in KEYS.items():
        if key in existing:
            continue
        tabs["chrome"][lang].append([key, tr[lang]])
        added += 1
with io.open(tp, "w", encoding="utf-8", newline="") as f:
    json.dump(tabs, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("tables: %d key/lang pairs added" % added)
