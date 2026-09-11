# -*- coding: utf-8 -*-
"""One-shot round 22: pages (l/100km-to-mpg, cups-to-grams) + fuel renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("liters-to-quarts-uk", "Liters to Quarts", "liters", "quarts (US)", 1.0566882094, "volume",
                       "Forward direction for the liters-to-quarts family: multiply liters by 1.05669 to get US quarts. Engine capacities, stock pots and paint tins all land on this conversion.",
                       "Handy anchors: 1 L = 1.06 qt, 3 L = 3.17 qt, 5 L = 5.28 qt, 10 L = 10.57 qt."))

    pages.append({
        "slug": "litres-per-100km-to-mpg",
        "title": "L/100km to MPG Converter — Fuel Economy, Both Directions",
        "h1": "L/100km to MPG Calculator",
        "desc": "Convert liters per 100 km to US MPG (and back). The two fuel-economy scales run in opposite directions — this converter handles the inverted math and flags which number is better.",
        "category": "converter",
        "keyword": "litres per 100km to mpg",
        "tool": "fuel",
        "args": {},
        "intro": [
            "Europe measures fuel economy in liters per 100 km; America uses miles per gallon. They are not just different units — they run in opposite directions: lower L/100km is better, higher MPG is better. The conversion is MPG = 235.215 ÷ (L/100km), and this calculator handles the inversion both ways.",
            "So a European-spec car at 6.5 L/100km is a 36 MPG car; an American 30 MPG sedan is a 7.8 L/100km car. Useful when importing, comparing spec sheets, or decoding a rental car dashboard on holiday.",
        ],
        "howto": [
            "Type your figure in liters per 100 km — the MPG equivalent appears instantly.",
            "Or type MPG in the second box to get L/100km in the first.",
            "The better-worse hint updates automatically, so the inverted scales never catch you out.",
        ],
        "faqs": [
            ("How do you convert L/100km to MPG?",
             "Divide 235.215 by the L/100km figure. 8 L/100km = 235.215 ÷ 8 = 29.4 MPG (US). For UK imperial MPG, use 282.481 instead — imperial gallons are 20% bigger."),
            ("Why do the two scales run in opposite directions?",
             "L/100km measures fuel used per distance (lower = efficient); MPG measures distance per fuel (higher = efficient). One is consumption, the other is efficiency — the same idea from opposite ends."),
            ("What is a good L/100km?",
             "For petrol cars: under 6 L/100km is efficient, 6–8 is typical, over 10 is thirsty. Hybrids reach 4–5; large SUVs can exceed 12. Electric cars leave the scale entirely (they use kWh/100km)."),
            ("Is this US MPG or UK MPG?",
             "This converter uses US MPG (the standard in the US). UK MPG uses the larger imperial gallon, so a car rated 40 MPG (UK) is only 33 MPG (US) — check which scale the brochure means."),
        ],
    })

    pages.append({
        "slug": "cups-to-grams",
        "title": "Cups to Grams Converter — By Ingredient (Flour, Sugar, Butter)",
        "h1": "Cups to Grams Converter",
        "desc": "Convert cups to grams by ingredient: flour 125 g/cup, sugar 200 g, butter 227 g and more. The accurate way to translate US recipes onto a kitchen scale.",
        "category": "converter",
        "keyword": "cups to grams",
        "tool": "gramscups",
        "args": {},
        "intro": [
            "Translating an American cup recipe onto a kitchen scale is the single best upgrade a baker can make — and the trick is that the answer depends on the ingredient: a cup of flour is 125 g, a cup of sugar 200 g, a cup of butter 227 g. Choose the ingredient and both directions convert with the correct density.",
            "Cup measurements vary by up to 20% depending on how firmly you scoop; grams never vary. Translate the recipe once with this converter, weigh after that, and your bakes stop varying with them.",
        ],
        "howto": [
            "Choose the ingredient from the dropdown list.",
            "Type the number of cups — the gram weight appears instantly (or go the other way).",
            "Weigh to the gram on your scale; note the translation on the recipe card for next time.",
        ],
        "faqs": [
            ("How many grams is 2 cups of flour?",
             "About 250 g, at the standard 125 g per leveled cup. If the original recipe scooped heavily, the author may have meant closer to 280 g — one more reason weight recipes win."),
            ("How many grams is a cup of butter?",
             "227 g — which is exactly one US stick-based convenience: a 1-pound butter pack is 2 cups. Most butter wrappers print tablespoon and cup markings on the side."),
            ("Is 1 cup always 240 grams?",
             "Only for water and milk. Dense ingredients (sugar 200 g, honey 340 g) and light ones (oats 90 g, powdered sugar 120 g) differ wildly — always convert by ingredient."),
            ("What is 250 grams in cups?",
             "Depends entirely on the ingredient: 2 cups of flour, 1.25 cups of granulated sugar, about 1.1 cups of butter. Pick the ingredient in the converter above."),
        ],
    })

''' + anchor

if '"litres-per-100km-to-mpg"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"litres-per-100km-to-mpg"' in s, '"cups-to-grams"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"fuel"' not in t:
    js = '''
# ---------------------------------------------------------------- fuel economy
FUEL = """
<div class="tool" id="tt-fuel">
  <div class="fields two">
    <div class="field"><label for="fu-l">Liters per 100 km</label><input type="number" id="fu-l" step="any" min="0" placeholder="6.5"></div>
    <div class="field"><label for="fu-m">Miles per gallon (US)</label><input type="number" id="fu-m" step="any" min="0" placeholder="36.2"></div>
  </div>
  <div class="result"><span class="result-num" id="fu-out">–</span><span class="result-unit" id="fu-unit"></span>
    <div class="result-formula" id="fu-note"></div></div>
  <div class="tool-note" id="fu-hint">Lower L/100km is better · higher MPG is better — the scales run in opposite directions.</div>
</div>
<script>(function(){
var L=document.getElementById('fu-l'),M=document.getElementById('fu-m');
var out=document.getElementById('fu-out'),unit=document.getElementById('fu-unit'),hint=document.getElementById('fu-hint');
var lock=false;
function good(l){return l<=6?'efficient':l<=9?'typical':'thirsty';}
function runL(){
  if(lock)return;lock=true;M.value='';
  var v=parseFloat(L.value);
  if(isNaN(v)||v<=0){out.textContent='-';unit.textContent='';hint.textContent='Lower L/100km is better · higher MPG is better.';lock=false;return;}
  var mpg=235.215/v;
  M.value=Math.round(mpg*10)/10;
  out.textContent=Math.round(mpg*10)/10+' mpg';
  unit.textContent='(US)';
  hint.textContent=v+' L/100km = '+Math.round(mpg*10)/10+' US mpg — '+good(v)+' for a petrol car.';
  lock=false;
}
function runM(){
  if(lock)return;lock=true;L.value='';
  var v=parseFloat(M.value);
  if(isNaN(v)||v<=0){out.textContent='-';unit.textContent='';lock=false;return;}
  var l=235.215/v;
  L.value=Math.round(l*100)/100;
  out.textContent=Math.round(l*100)/100+' L/100km';
  unit.textContent='';
  hint.textContent=v+' mpg = '+Math.round(l*100)/100+' L/100km - '+good(l)+' for a petrol car.';
  lock=false;
}
L.addEventListener('input',runL);
M.addEventListener('input',runM);
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"fuel": lambda args: FUEL,' not in t:
    t = t.replace('    "dayofweek": lambda args: DAYOFWEEK,',
                  '    "dayofweek": lambda args: DAYOFWEEK,\n    "fuel": lambda args: FUEL,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("fuel registered:", '"fuel": lambda' in t)
