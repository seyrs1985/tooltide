# -*- coding: utf-8 -*-
"""One-shot round 60: pages (kelvin-converter, tablespoons-to-ml) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("tablespoons-to-ml", "Tablespoons to ML", "tablespoons", "milliliters", 14.7867648, "volume",
                       "US recipes say tablespoons, metric jugs say milliliters - and one US tablespoon is 14.7868 ml (15 in the rounded convention most kitchens use). The converter shows both the precise and the practical answer, because pancakes forgive rounding but chemistry does not.",
                       "Handy anchors: 1 tbsp = 14.79 ml, 2 tbsp = 29.57 ml (one fluid ounce), 4 tbsp = 59.15 ml (a quarter cup), 16 tbsp = 236.6 ml (a full cup)."))

    pages.append({
        "slug": "kelvin-converter",
        "title": "Kelvin Converter — Kelvin, Celsius & Fahrenheit Together",
        "h1": "Kelvin Converter",
        "desc": "Convert Kelvin to Celsius and Fahrenheit in one view - type in any of the three scales and the others update live. Physics and chemistry homework, solved with the exact offsets shown.",
        "category": "calculator",
        "keyword": "kelvin converter",
        "tool": "kelvin",
        "args": {},
        "intro": [
            "Three temperature scales, one converter: type a value into Kelvin, Celsius or Fahrenheit and the other two update instantly. Kelvin is Celsius shifted by exactly 273.15 - same degree size, different zero - while Fahrenheit needs both an offset and a fraction. The formulas are displayed with your numbers in place.",
            "Kelvin matters because it is absolute: 0 K is the temperature where molecular motion stops, which is why gas laws and thermodynamics refuse to work in degrees. This converter is the bridge between the physics classroom and the weather report.",
        ],
        "howto": [
            "Type a value into any of the three boxes - Kelvin, Celsius or Fahrenheit.",
            "The other two scales update instantly, with the conversion formulas shown below.",
            "Note 0 K (absolute zero) equals -273.15 C: the coldest anything can ever be.",
        ],
        "faqs": [
            ("How do you convert Kelvin to Celsius?",
             "Subtract 273.15. 300 K is 26.85 C. To go back, add 273.15 - the degree sizes are identical, only the zero points differ."),
            ("What is absolute zero in Celsius and Fahrenheit?",
             "0 K = -273.15 C = -459.67 F. It is the theoretical floor of temperature: no colder state exists because molecular motion cannot go below zero."),
            ("Why does science use Kelvin instead of Celsius?",
             "Because formulas need a true zero. Gas laws like PV = nRT only work when temperature is proportional to molecular energy - in Celsius, doubling 10 C to 20 C would absurdly claim double the energy."),
            ("Can temperature be negative in Kelvin?",
             "No - there is no temperature below absolute zero. (Physics classes may mention exotic 'negative temperature' systems, but those are stranger than simple coldness and not what a thermometer measures.)"),
        ],
    })

''' + anchor

if '"kelvin-converter"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"kelvin-converter"' in s, '"tablespoons-to-ml"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"kelvin"' not in t:
    js = '''
# ---------------------------------------------------------------- kelvin converter
KELVIN = """
<div class="tool" id="tt-kel">
  <div class="fields">
    <div class="field"><label for="kel-k">Kelvin (K)</label><input type="number" id="kel-k" step="any" placeholder="300"></div>
    <div class="field"><label for="kel-c">Celsius (C)</label><input type="number" id="kel-c" step="any" placeholder="26.85"></div>
    <div class="field"><label for="kel-f">Fahrenheit (F)</label><input type="number" id="kel-f" step="any" placeholder="80.33"></div>
  </div>
  <div class="result"><span class="result-num" id="kel-out">-</span><div class="result-formula" id="kel-note"></div></div>
</div>
<script>(function(){
var K=document.getElementById('kel-k'),C=document.getElementById('kel-c'),F=document.getElementById('kel-f');
var out=document.getElementById('kel-out'),note=document.getElementById('kel-note');
var lock=false;
function r(v){return Math.round(v*100)/100;}
function set(k,c,f,noteTxt){
  K.value=k===null?'':r(k);C.value=c===null?'':r(c);F.value=f===null?'':r(f);
  out.textContent=(k===null?'-':r(k)+' K')+'  =  '+(c===null?'-':r(c)+' C')+'  =  '+(f===null?'-':r(f)+' F');
  note.textContent=noteTxt||'';
  document.title=r(c)+' C - ToolTide';
}
function fromK(k){
  if(isNaN(k)){set(null,null,null,'');return;}
  if(k<0){set(k,k*1-273.15,null,'Below absolute zero - physically impossible.');return;}
  var c=k-273.15,f=c*9/5+32;
  set(k,c,f,'K - 273.15 = C; C x 9/5 + 32 = F');
}
function fromC(c){
  if(isNaN(c)){set(null,null,null,'');return;}
  fromK(c+273.15);
}
function fromF(f){
  if(isNaN(f)){set(null,null,null,'');return;}
  fromK((f-32)*5/9+273.15);
}
K.addEventListener('input',function(){fromK(parseFloat(K.value));});
C.addEventListener('input',function(){fromC(parseFloat(C.value));});
F.addEventListener('input',function(){fromF(parseFloat(F.value));});
fromK(300);
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"kelvin": lambda args: KELVIN,' not in t:
    t = t.replace('    "moonweight": lambda args: MOONWEIGHT,',
                  '    "moonweight": lambda args: MOONWEIGHT,\n    "kelvin": lambda args: KELVIN,', 1)

if '"tbspml"' not in t:
    pass
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("kelvin registered:", '"kelvin": lambda' in t)
