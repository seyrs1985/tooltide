# -*- coding: utf-8 -*-
"""One-shot round 38: pages (kb-to-gb, age-on-planets) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("kb-to-gb", "KB to GB", "kilobytes", "gigabytes", 1 / 1000000, "storage",
                       "The long jump of the storage ladder: divide kilobytes by 1,000,000 to reach gigabytes (decimal scale). A 500,000 KB photo library is 0.5 GB of cloud space; a 2,000,000 KB video is 2 GB.",
                       "Handy anchors: 100,000 KB = 0.1 GB, 500,000 KB = 0.5 GB, 1,000,000 KB = 1 GB, 10,000,000 KB = 10 GB (a movie download)."))

    pages.append({
        "slug": "age-on-other-planets",
        "title": "Age on Other Planets — Your Age on Mars, Jupiter & More",
        "h1": "Your Age on Other Planets",
        "desc": "Enter your Earth age and see how old you would be on Mercury, Venus, Mars, Jupiter and the rest — each planet's year is a different length. Space science made personal.",
        "category": "calculator",
        "keyword": "age on other planets",
        "tool": "planets",
        "args": {},
        "intro": [
            "A year is one trip around the Sun — but every planet takes a different time to make that trip. Enter your age in Earth years and this calculator shows your age on all eight planets: a 30-year-old is 124 on Mercury (its year is 88 days), just 12 on Uranus, and hasn't even finished one Neptune year.",
            "It is the friendliest possible introduction to orbital periods: the numbers stick because they are about you. Teachers use it for solar system units; everyone else uses it to feel young again (Mercury birthdays come around four times an Earth year).",
        ],
        "howto": [
            "Enter your age in Earth years.",
            "Read your age on all eight planets — each converted by that planet's orbital period.",
            "Note Mercury: you would celebrate a birthday roughly every 88 Earth days.",
        ],
        "faqs": [
            ("How old would I be on Mars?",
             "Divide your Earth age by 1.881 (Mars's year is 1.881 Earth years). A 30-year-old is about 16 on Mars — teenagers on the red planet are in their forties on Earth."),
            ("Why is my age different on other planets?",
             "Age in years counts orbits around the Sun. Mercury orbits in 88 Earth days, Neptune in nearly 165 Earth years — same you, different number of laps completed."),
            ("How old would I be on Mercury?",
             "Multiply your Earth age by about 4.15 — Mercury's year is only 88 days. A 1-year-old baby has already celebrated four Mercury birthdays."),
            ("Which planet makes you oldest?",
             "Mercury, by far — its short orbit means the most birthdays. Neptune is the opposite: no human has completed a single Neptune year since it was discovered in 1846."),
        ],
    })

''' + anchor

if '"kb-to-gb"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"kb-to-gb"' in s, '"age-on-other-planets"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"planets"' not in t:
    js = '''
# ---------------------------------------------------------------- age on planets
PLANETS = """
<div class="tool" id="tt-pl">
  <div class="field"><label for="pl-age">Your age in Earth years</label><input type="number" id="pl-age" step="any" min="0" value="30"></div>
  <table class="copytable"><thead><tr><th>Planet</th><th>Your age</th><th>Orbit (Earth years)</th></tr></thead><tbody id="pl-tb"></tbody></table>
</div>
<script>(function(){
var P=[["Mercury",0.2408467,"\\u2605"],["Venus",0.61519726,"\\u2605"],["Mars",1.8808158,"\\u2605"],["Jupiter",11.862615,"\\u2605"],["Saturn",29.447498,"\\u2605"],["Uranus",84.016846,"\\u2605"],["Neptune",164.79132,"\\u2605"]];
var inp=document.getElementById('pl-age'),tb=document.getElementById('pl-tb');
function run(){
  var age=parseFloat(inp.value);
  if(isNaN(age)){tb.innerHTML='';return;}
  var html=P.map(function(p){
    var a=Math.round(age/p[1]*100)/100;
    return '<tr><td>'+p[0]+'</td><td><b>'+a+'</b></td><td>'+p[1]+'</td></tr>';
  }).join('');
  tb.innerHTML=html;
}
inp.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"planets": lambda args: PLANETS,' not in t:
    t = t.replace('    "hexrgb": lambda args: HEXRGB,',
                  '    "hexrgb": lambda args: HEXRGB,\n    "planets": lambda args: PLANETS,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("planets registered:", '"planets": lambda' in t)
