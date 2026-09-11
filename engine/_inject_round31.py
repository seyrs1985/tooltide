# -*- coding: utf-8 -*-
"""One-shot round 31: pages (mb-to-kb, degrees-to-radians) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("mb-to-kb", "MB to KB", "megabytes", "kilobytes", 1000, "storage",
                       "On the decimal scale storage vendors use, 1 MB = 1,000 KB exactly. (Operating systems sometimes count in binary kibibytes — 1 MiB = 1,024 KiB — which is where the classic 'my file is bigger than it should be' confusion comes from.)",
                       "Handy anchors: 1 MB = 1,000 KB, 5 MB = 5,000 KB (a photo), 25 MB = 25,000 KB (an email attachment limit)."))
    pages.append(_conv("kb-to-mb", "KB to MB", "kilobytes", "megabytes", 1 / 1000, "storage",
                       "Divide kilobytes by 1,000 to get megabytes on the decimal scale — the one storage and telecom pricing actually uses. A 2,000 KB attachment is a 2 MB upload.",
                       "Handy anchors: 500 KB = 0.5 MB (a heavy photo), 1,000 KB = 1 MB, 10,000 KB = 10 MB (a short video clip)."))

    pages.append({
        "slug": "degrees-to-radians",
        "title": "Degrees to Radians Converter — ° to rad and Back",
        "h1": "Degrees to Radians Converter",
        "desc": "Convert degrees to radians and back instantly: 180° = π rad. Exact π forms for common angles plus decimal values. The trigonometry homework companion.",
        "category": "calculator",
        "keyword": "degrees to radians",
        "tool": "degrad",
        "args": {},
        "intro": [
            "Type an angle in degrees and get it in radians instantly — including the exact form in terms of π when one exists (90° is π/2, not 1.5708). Go the other way too: paste a radian value like 3π/4 or a decimal, and the degrees appear.",
            "Trigonometry, physics and every graphing calculator live in radians, while every compass and protractor lives in degrees — this converter is the bridge between the two worlds, with the π-based exact answers math teachers want to see.",
        ],
        "howto": [
            "Type an angle in degrees — the radian value appears instantly, exact π form when available.",
            "Or type radians (decimals like 1.5708, or π-forms like 3pi/4) to get degrees.",
            "Check the common-angle table below for the values worth memorizing.",
        ],
        "faqs": [
            ("How do you convert degrees to radians?",
             "Multiply by π and divide by 180: radians = degrees × π/180. So 90° = 90 × π/180 = π/2 radians. The converter shows both the exact π-form and the decimal."),
            ("Why does math use radians instead of degrees?",
             "Radians make calculus and trig identities clean: sin(x) Derivative works only in radians, and arc length is simply radius × angle. Degrees are human convention; radians are mathematical nature."),
            ("What is 1 radian in degrees?",
             "About 57.2958°. One radian is the angle where the arc length equals the radius — a full circle is 2π radians, which is why π shows up everywhere in circle math."),
            ("How do I type π into the converter?",
             "Just write pi or 3pi/4 — the converter understands pi as π. Decimals like 1.5708 work equally well."),
        ],
    })

''' + anchor

if '"degrees-to-radians"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"mb-to-kb"' in s, '"degrees-to-radians"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"degrad"' not in t:
    js = '''
# ---------------------------------------------------------------- degrees <-> radians
DEGRAD = """
<div class="tool" id="tt-dr">
  <div class="fields two">
    <div class="field"><label for="dr-deg">Degrees (°)</label><input type="number" id="dr-deg" step="any" placeholder="90"></div>
    <div class="field"><label for="dr-rad">Radians (number or 3pi/4)</label><input type="text" id="dr-rad" placeholder="1.5708"></div>
  </div>
  <div class="result"><span class="result-num" id="dr-out">-</span><div class="result-formula" id="dr-note"></div></div>
  <table class="copytable"><thead><tr><th>Degrees</th><th>Radians (exact)</th><th>Decimal</th></tr></thead><tbody>
  <tr><td>30</td><td>pi/6</td><td>0.5236</td></tr><tr><td>45</td><td>pi/4</td><td>0.7854</td></tr>
  <tr><td>60</td><td>pi/3</td><td>1.0472</td></tr><tr><td>90</td><td>pi/2</td><td>1.5708</td></tr>
  <tr><td>180</td><td>pi</td><td>3.1416</td></tr><tr><td>270</td><td>3pi/2</td><td>4.7124</td></tr>
  <tr><td>360</td><td>2pi</td><td>6.2832</td></tr></tbody></table>
</div>
<script>(function(){
var DEG=document.getElementById('dr-deg'),RAD=document.getElementById('dr-rad');
var out=document.getElementById('dr-out'),note=document.getElementById('dr-note');
var lock=false;
function cleanPi(v){
  v=v.trim().toLowerCase().replace(/\\s/g,'');
  var m=v.match(/^(-?)(\\d*\\.?\\d*)\\*?pi(?:\\/(\\d+))?$/);
  if(m){var k=m[2]===''?1:parseFloat(m[2]);var r=m[3]?k/(+m[3]):k;return (m[1]==='-'?-1:1)*r*Math.PI;}
  var f=parseFloat(v);
  return isNaN(f)?null:f;
}
function exactForm(deg){
  var common={30:'pi/6',45:'pi/4',60:'pi/3',90:'pi/2',120:'2pi/3',135:'3pi/4',150:'5pi/6',180:'pi',270:'3pi/2',360:'2pi'};
  return common[deg]||null;
}
DEG.addEventListener('input',function(){
  if(lock)return;lock=true;
  var d=parseFloat(DEG.value);
  if(isNaN(d)){out.textContent='-';note.textContent='';RAD.value='';lock=false;return;}
  var r=d*Math.PI/180,ex=exactForm(Math.abs(d));
  RAD.value=(Math.round(r*10000)/10000)+'';
  out.textContent=(Math.round(r*10000)/10000)+' rad';
  note.textContent=ex?(d+' deg = '+ex+' rad (exact)'):(d+' deg = '+d+' x pi/180 rad');
  lock=false;
});
RAD.addEventListener('input',function(){
  if(lock)return;lock=true;
  var r=cleanPi(this.value);
  if(r===null){out.textContent='-';note.textContent='';DEG.value='';lock=false;return;}
  var d=r*180/Math.PI;
  DEG.value=Math.round(d*100)/100+'';
  out.textContent=(Math.round(d*100)/100)+' deg';
  note.textContent=(Math.round(r*10000)/10000)+' rad = '+Math.round(d*100)/100+' deg';
  lock=false;
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"degrad": lambda args: DEGRAD,' not in t:
    t = t.replace('    "wordfreq": lambda args: WORDFREQ,',
                  '    "wordfreq": lambda args: WORDFREQ,\n    "degrad": lambda args: DEGRAD,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("degrad registered:", '"degrad": lambda' in t)
