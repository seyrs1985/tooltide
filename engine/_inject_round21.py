# -*- coding: utf-8 -*-
"""One-shot round 21: pages (grams-to-cups, day-of-week) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "grams-to-cups",
        "title": "Grams to Cups Converter — By Ingredient (Flour, Sugar, Butter)",
        "h1": "Grams to Cups Converter",
        "desc": "Convert grams to cups by ingredient: flour, sugar, butter, oats, cocoa and more. Ingredient density matters — 200 g of flour is not 200 g of sugar in cups.",
        "category": "converter",
        "keyword": "grams to cups",
        "tool": "gramscups",
        "args": {},
        "intro": [
            "Converting grams to cups is the one baking conversion where the ingredient itself matters: a cup of flour weighs 125 g, but a cup of sugar weighs 200 g and a cup of honey nearly 340 g. Pick the ingredient from the list and both directions convert with the right density.",
            "Results include a friendly fraction estimate (like \\u2154 cup) because nobody measures 0.67 cups. For best baking results, grams win — a scale removes the packing-error that makes cup measurements unreliable — but when only cups exist, this converter keeps the recipe honest.",
        ],
        "howto": [
            "Choose the ingredient from the dropdown — density differs for every one.",
            "Type grams to see cups, or type cups to see grams; both directions update live.",
            "Use the fraction shown as the practical measuring-cup answer.",
        ],
        "faqs": [
            ("How many grams is a cup of flour?",
             "About 125 g for all-purpose flour spooned and leveled. Scooping directly from the bag compresses it and can reach 150 g+ — which is why weight recipes beat cup recipes."),
            ("How many grams is a cup of sugar?",
             "Granulated sugar: about 200 g per cup. Brown sugar (packed): about 213 g. Powdered sugar is much lighter: about 120 g per cup."),
            ("Why do grams and cups disagree between websites?",
             "Because cups measure volume, not weight — the answer depends on how densely the ingredient is packed. Reputable sources agree closely on standard weights (flour 120–130 g per cup), and this converter uses the widely accepted values."),
            ("Should I switch my recipes to grams?",
             "If you bake regularly, yes: a scale costs little and removes the single biggest source of baking failure. Use this converter to translate your existing cup recipes once, then weigh forever after."),
        ],
    })

    pages.append({
        "slug": "day-of-week",
        "title": "What Day of the Week Was I Born? — Day of Week Calculator",
        "h1": "Day of the Week Calculator",
        "desc": "Find the day of the week for any date in history — birthdays, historical events, or the date of your next anniversary. Instant, with the day-of-year and week number.",
        "category": "calculator",
        "keyword": "what day of the week was i born",
        "tool": "dayofweek",
        "args": {},
        "intro": [
            "Pick any date and see the day of the week it fell on — or will fall on. It answers the classic 'what day was I born on?' (and whether your birthday lands on a weekend next year), plus historical curiosity: moon landings, royal weddings, and that concert you remember being at.",
            "Alongside the weekday you get the day-of-year number and the ISO week number, which is the detail project plans and European calendars quietly rely on.",
        ],
        "howto": [
            "Pick any date — past or future — from the date picker.",
            "Read the weekday instantly, plus the day-of-year and ISO week number.",
            "Change the year to plan birthdays: see whether yours falls on a weekend next time.",
        ],
        "faqs": [
            ("What day of the week was I born?",
             "Enter your date of birth and the weekday appears instantly. The pattern repeats every 28 years (the solar cycle), so your birth date falls on the same weekday as it did 28 years ago."),
            ("Does the calculator work for any year in history?",
             "It uses your browser's proleptic Gregorian calendar, accurate across a huge historical range. For dates before 1582 (when the Gregorian calendar was introduced) historians use the Julian calendar, so results may differ from historical records."),
            ("Why do dates fall on different weekdays each year?",
             "A year is 365 days — one day longer than 52 weeks — so each year's dates shift one weekday later (two after a leap year). That is why your birthday keeps moving."),
            ("What is the ISO week number?",
             "A standard way of numbering weeks (1–52/53) used in European business calendars: week 1 is the week containing the first Thursday of January."),
        ],
    })

''' + anchor

if '"grams-to-cups"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"grams-to-cups"' in s, '"day-of-week"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"gramscups"' not in t:
    js = '''
# ---------------------------------------------------------------- grams <-> cups (by ingredient)
GRAMSCUPS = """
<div class="tool" id="tt-gc">
  <div class="field"><label for="gc-ing">Ingredient</label>
    <select id="gc-ing">
      <option value="125">All-purpose flour (125 g/cup)</option>
      <option value="200">Granulated sugar (200 g/cup)</option>
      <option value="213">Brown sugar, packed (213 g/cup)</option>
      <option value="120">Powdered sugar (120 g/cup)</option>
      <option value="227">Butter (227 g/cup)</option>
      <option value="240">Water / milk (240 g/cup)</option>
      <option value="340">Honey (340 g/cup)</option>
      <option value="90">Rolled oats (90 g/cup)</option>
      <option value="100">Cocoa powder (100 g/cup)</option>
      <option value="180">Rice, uncooked (180 g/cup)</option>
    </select></div>
  <div class="fields">
    <div class="field"><label for="gc-g">Grams</label><input type="number" id="gc-g" step="any" min="0" placeholder="250"></div>
    <div class="field"><label for="gc-c">Cups</label><input type="number" id="gc-c" step="any" min="0" placeholder=""></div>
  </div>
  <div class="result"><span class="result-num" id="gc-frac">–</span><span class="result-unit" id="gc-fr2"></span>
    <div class="result-formula" id="gc-note"></div></div>
</div>
<script>(function(){
var ing=document.getElementById('gc-ing'),G=document.getElementById('gc-g'),C=document.getElementById('gc-c');
var frac=document.getElementById('gc-frac'),fr2=document.getElementById('gc-fr2'),note=document.getElementById('gc-note');
var lock=false;
function nice(n){
  var common=[0,0.25,0.333,0.5,0.666,0.75,1];
  var best=0,bd=9;
  common.forEach(function(c){var d=Math.abs(n-c);if(d<bd){bd=d;best=c;}});
  var names={0:'',0.25:'1/4',0.333:'1/3',0.5:'1/2',0.666:'2/3',0.75:'3/4',1:'1'};
  var whole=Math.floor(n),rem=n-whole,remR=Math.round(rem*100)/100;
  var base=whole?whole+' ':'';
  var rn=names[best]||null;
  if(remR>0.02&&remR<0.98&&rn&&best!==1)return base+rn;
  if(best===1&&whole)return (whole+1)+'';
  return (Math.round(n*100)/100)+'';
}
function runG(){
  if(lock)return;lock=true;C.value='';
  var g=parseFloat(G.value);
  if(isNaN(g)||!g){frac.textContent='-';fr2.textContent='';note.textContent='';lock=false;return;}
  var c=g/(parseFloat(ing.value));
  var nc=Math.round(c*100)/100;
  C.value=nc;
  frac.textContent=nice(c);fr2.textContent='cup'+(c>1?'s':'');
  note.textContent=g+' g \\u00f7 '+ing.value+' g per cup';
  lock=false;
}
function runC(){
  if(lock)return;lock=true;G.value='';
  var c=parseFloat(C.value);
  if(isNaN(c)||!c){frac.textContent='-';fr2.textContent='';note.textContent='';lock=false;return;}
  var g=c*(parseFloat(ing.value));
  var gr=Math.round(g*10)/10;
  G.value=gr;
  frac.textContent=gr+' g';fr2.textContent='';
  note.textContent=c+' cup(s) \\u00d7 '+ing.value+' g per cup';
  lock=false;
}
ing.addEventListener('change',runG);
G.addEventListener('input',runG);
C.addEventListener('input',runC);
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"gramscups": lambda args: GRAMSCUPS,' not in t:
    t = t.replace('    "binary": lambda args: BINARY,',
                  '    "binary": lambda args: BINARY,\n    "gramscups": lambda args: GRAMSCUPS,', 1)

if '"dayofweek"' not in t:
    js2 = '''
# ---------------------------------------------------------------- day of week
DAYOFWEEK = """
<div class="tool" id="tt-dw">
  <div class="field"><label for="dw-date">Any date</label><input type="date" id="dw-date"></div>
  <div class="result"><span class="result-num" id="dw-out">-</span>
    <div class="result-formula" id="dw-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="dw-doy">-</b><span>day of year</span></div>
    <div class="stat"><b id="dw-iso">-</b><span>ISO week</span></div>
  </div>
</div>
<script>(function(){
var d=document.getElementById('dw-date');
var now=new Date();
d.value=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0');
function isoWeek(dt){
  var t=new Date(Date.UTC(dt.getFullYear(),dt.getMonth(),dt.getDate()));
  var day=(t.getUTCDay()+6)%7;
  t.setUTCDate(t.getUTCDate()-day+3);
  var firstThu=new Date(Date.UTC(t.getUTCFullYear(),0,4));
  var fday=(firstThu.getUTCDay()+6)%7;
  firstThu.setUTCDate(firstThu.getUTCDate()-fday+3);
  return 1+Math.round((t-firstThu)/604800000);
}
function run(){
  if(!d.value)return;
  var dt=new Date(d.value+'T00:00:00');
  if(isNaN(dt))return;
  document.getElementById('dw-out').textContent=dt.toLocaleDateString('en-US',{weekday:'long'});
  document.getElementById('dw-note').textContent=dt.toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
  var start=new Date(dt.getFullYear(),0,1);
  document.getElementById('dw-doy').textContent=Math.round((dt-start)/864e5)+1;
  document.getElementById('dw-iso').textContent='W'+isoWeek(dt);
}
d.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"dayofweek": lambda args: DAYOFWEEK,' not in t:
    t = t.replace('    "gramscups": lambda args: GRAMSCUPS,',
                  '    "gramscups": lambda args: GRAMSCUPS,\n    "dayofweek": lambda args: DAYOFWEEK,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"gramscups": lambda' in t, '"dayofweek": lambda' in t)
