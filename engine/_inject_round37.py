# -*- coding: utf-8 -*-
"""One-shot round 37: pages (hex-to-rgb, gallons-to-quarts) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "hex-to-rgb",
        "title": "Hex to RGB Converter — Color Codes Both Ways, Live Preview",
        "h1": "Hex to RGB Converter",
        "desc": "Convert HEX color codes to RGB and back instantly, with a live color preview. For designers, front-end developers and anyone stuck reading #1A73E8 in a spec.",
        "category": "converter",
        "keyword": "hex to rgb",
        "tool": "hexrgb",
        "args": {},
        "intro": [
            "Paste a hex code like #1A73E8 and get its RGB equivalent (26, 115, 232) instantly — or paste RGB values and get the hex. A live swatch shows the actual color, so you can confirm you have the right shade before it goes into CSS, Figma or a brand guide.",
            "Both notations describe the same color: hex is just RGB written in base 16 (1A hex = 26). The converter accepts 3-digit shorthand too (#F00 = #FF0000) and outputs the 6-digit canonical form.",
        ],
        "howto": [
            "Type a hex code (with or without the #) — RGB values and the color swatch appear instantly.",
            "Or type R, G, B numbers (0–255) to get the hex code.",
            "Copy either format straight into CSS, design tools or documentation.",
        ],
        "faqs": [
            ("How do I convert HEX to RGB?",
             "Split the hex code into three pairs and convert each from base 16 to base 10. #1A73E8: 1A = 26, 73 = 115, E8 = 232 — so RGB(26, 115, 232). The converter does both pairs live."),
            ("What is the difference between HEX and RGB?",
             "None in color — they are two notations for the same values. HEX is compact and universal in design handoffs; RGB(A) supports alpha transparency and reads more explicitly in CSS."),
            ("What are 3-digit hex codes?",
             "Shorthand where each digit is doubled: #F00 expands to #FF0000 (red). It exists for brevity; the converter accepts it and outputs the full 6-digit form."),
            ("What is RGBA?",
             "RGB plus an alpha channel for opacity (0–1). This converter handles opaque colors; add the alpha in CSS separately, e.g. rgba(26, 115, 232, 0.5)."),
        ],
    })

    pages.append(_conv("gallons-to-quarts", "Gallons to Quarts", "gallons (US)", "quarts (US)", 4, "volume",
                       "The US volume ladder's final step: 1 gallon is exactly 4 quarts. Milk jugs, engine oil and soup pots all speak this language — multiply gallons by 4 and the recipe or oil change is settled.",
                       "Handy anchors: 1 gal = 4 qt, 2 gal = 8 qt, 0.5 gal = 2 qt (those half-gallon milk cartons)."))

''' + anchor

if '"hex-to-rgb"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"hex-to-rgb"' in s, '"gallons-to-quarts"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"hexrgb"' not in t:
    js = '''
# ---------------------------------------------------------------- hex <-> rgb
HEXRGB = """
<div class="tool" id="tt-hr">
  <div class="fields">
    <div class="field"><label for="hr-hex">HEX color</label><input type="text" id="hr-hex" placeholder="#1A73E8" autocomplete="off"></div>
    <div class="field"><label for="hr-r">R (0-255)</label><input type="number" id="hr-r" min="0" max="255" step="1" placeholder="26"></div>
    <div class="field"><label for="hr-g">G (0-255)</label><input type="number" id="hr-g" min="0" max="255" step="1" placeholder="115"></div>
    <div class="field"><label for="hr-b">B (0-255)</label><input type="number" id="hr-b" min="0" max="255" step="1" placeholder="232"></div>
  </div>
  <div class="chips"><button class="chip" id="hr-sh" type="button">Random color</button></div>
  <div class="color-preview" id="hr-preview"></div>
  <div class="stats">
    <div class="stat"><b id="hr-hexout">-</b><span>hex</span></div>
    <div class="stat"><b id="hr-rgbout">-</b><span>rgb()</span></div>
  </div>
</div>
<script>(function(){
var HEX=document.getElementById('hr-hex'),R=document.getElementById('hr-r'),G=document.getElementById('hr-g'),B=document.getElementById('hr-b');
var prev=document.getElementById('hr-preview');
var lock=false;
function clamp(v){return Math.max(0,Math.min(255,Math.round(v)||0));}
function hex2rgb(v){
  v=v.trim().replace('#','');
  if(/^[0-9a-fA-F]{3}$/.test(v))v=v.split('').map(function(c){return c+c;}).join('');
  if(!/^[0-9a-fA-F]{6}$/.test(v))return null;
  return {r:parseInt(v.slice(0,2),16),g:parseInt(v.slice(2,4),16),b:parseInt(v.slice(4,6),16),hex:'#'+v.toUpperCase()};
}
function upd(r,g,b){
  prev.style.background='rgb('+r+','+g+','+b+')';
  var hx='#'+[r,g,b].map(function(x){return x.toString(16).padStart(2,'0').toUpperCase();}).join('');
  document.getElementById('hr-hexout').textContent=hx;
  document.getElementById('hr-rgbout').textContent='rgb('+r+', '+g+', '+b+')';
}
HEX.addEventListener('input',function(){
  if(lock)return;lock=true;
  var c=hex2rgb(this.value);
  if(c){R.value=c.r;G.value=c.g;B.value=c.b;upd(c.r,c.g,c.b);}
  lock=false;
});
[R,G,B].forEach(function(el){el.addEventListener('input',function(){
  if(lock)return;lock=true;
  var r=clamp(parseFloat(R.value)),g=clamp(parseFloat(G.value)),b=clamp(parseFloat(B.value));
  upd(r,g,b);
  lock=false;
});});
document.getElementById('hr-sh').addEventListener('click',function(){
  var r=Math.floor(Math.random()*256),g=Math.floor(Math.random()*256),b=Math.floor(Math.random()*256);
  lock=true;R.value=r;G.value=g;B.value=b;upd(r,g,b);
  HEX.value='#'+[r,g,b].map(function(x){return x.toString(16).padStart(2,'0').toUpperCase();}).join('');
  lock=false;
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"hexrgb": lambda args: HEXRGB,' not in t:
    t = t.replace('    "yesno": lambda args: YESNO,',
                  '    "yesno": lambda args: YESNO,\n    "hexrgb": lambda args: HEXRGB,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("hexrgb registered:", '"hexrgb": lambda' in t)
