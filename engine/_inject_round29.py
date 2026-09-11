# -*- coding: utf-8 -*-
"""One-shot round 29: pages (cubic-feet, line-sorter) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "cubic-feet-calculator",
        "title": "Cubic Feet Calculator — Volume from Length, Width & Height",
        "h1": "Cubic Feet Calculator",
        "desc": "Calculate cubic feet from length, width and height — for moving trucks, storage units, fridges and shipping. Works in feet or cm and converts to cubic meters.",
        "category": "calculator",
        "keyword": "cubic feet calculator",
        "tool": "cubicft",
        "args": {},
        "intro": [
            "Enter length, width and height to get the volume in cubic feet — the number that decides which moving truck to book, whether the fridge fits the alcove, and what the shipping company will charge. It works in feet or centimeters and shows cubic meters alongside, because the rest of the world quotes volumes that way.",
            "Everything updates as you type, and the cm mode means European appliance specs and American shelf measurements can finally be compared on one screen.",
        ],
        "howto": [
            "Choose feet or centimeters, then enter length, width and height.",
            "Read the volume in cubic feet and cubic meters side by side.",
            "Add a margin for packing — moving boxes never pack at 100% density.",
        ],
        "faqs": [
            ("How do I calculate cubic feet?",
             "Multiply length × width × height, all in feet. A box measuring 2 ft × 2 ft × 1 ft is 4 cubic feet. Measure the largest points (including handles and feet on appliances) to be safe."),
            ("How many cubic feet is a standard fridge?",
             "A typical fridge-freezer holds 18–25 cubic feet; a compact dorm fridge around 3–4. Check the interior capacity spec, not the exterior size — walls and compressors eat space."),
            ("What size moving truck do I need?",
             "A studio flat fits in a 10–12 ft truck (about 350–450 cu ft), a one-bedroom in a 15–16 ft truck, and a 3-bedroom house usually needs a 20–26 ft truck (1,400+ cu ft). Measure your largest furniture first."),
            ("How do I convert cubic feet to cubic meters?",
             "Multiply by 0.0283. A 40 cu ft storage crate is about 1.13 cubic meters. The calculator shows both units automatically."),
        ],
    })

    pages.append({
        "slug": "line-sorter",
        "title": "Line Sorter — Alphabetize Text Lists Online (A-Z or Z-A)",
        "h1": "Line Sorter",
        "desc": "Sort text lines alphabetically A-Z or Z-A instantly. Case-insensitive option, duplicate and blank line cleanup, live line counts. 100% in your browser.",
        "category": "text",
        "keyword": "alphabetize lines",
        "tool": "sorter",
        "args": {},
        "intro": [
            "Paste any list — names, keywords, URLs, tasks — and sort the lines alphabetically in one pass. A-Z or Z-A, with case-insensitive comparison so 'apple' and 'Apple' sort together instead of by capital letter. Blank lines can be dropped, duplicates collapsed, and the line count updates live.",
            "It pairs naturally with the duplicate remover for list cleaning: dedupe first, sort second, copy the result. Like every ToolTide text tool, it runs entirely in your browser — private by architecture.",
        ],
        "howto": [
            "Paste your list into the input box.",
            "Choose A-Z or Z-A; toggle case-insensitive, remove blanks or dedupe as needed.",
            "The sorted list and line count update live — copy when it looks right.",
        ],
        "faqs": [
            ("How do I alphabetize a list of names?",
             "Paste the names one per line and click A-Z. Case-insensitive sorting keeps 'smith' and 'Smith' together instead of putting all lowercase names after all uppercase ones."),
            ("Does sorting change my original text?",
             "No — the sorted output appears in its own box. Your input stays untouched until you clear or edit it."),
            ("What does case-insensitive mean here?",
             "The sort compares letters without caring about capitalization, which is what humans expect: 'banana' sorts between 'Apple' and 'Cherry' rather than at the end."),
            ("Is there a line limit?",
             "The practical limit is browser memory — tens of thousands of lines sort instantly. Nothing is uploaded; sorting is local JavaScript."),
        ],
    })

''' + anchor

if '"cubic-feet-calculator"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"cubic-feet-calculator"' in s, '"line-sorter"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"cubicft"' not in t:
    js = '''
# ---------------------------------------------------------------- cubic feet
CUBICFT = """
<div class="tool" id="tt-cf">
  <div class="chips" role="tablist">
    <button class="chip active" data-u="ft">Feet</button>
    <button class="chip" data-u="cm">Centimeters</button>
  </div>
  <div class="fields">
    <div class="field"><label id="cf-l1" for="cf-l">Length (ft)</label><input type="number" id="cf-l" step="any" min="0" placeholder="2"></div>
    <div class="field"><label id="cf-l2" for="cf-w">Width (ft)</label><input type="number" id="cf-w" step="any" min="0" placeholder="2"></div>
    <div class="field"><label id="cf-l3" for="cf-h">Height (ft)</label><input type="number" id="cf-h" step="any" min="0" placeholder="1"></div>
  </div>
  <div class="result"><span class="result-num" id="cf-out">-</span><span class="result-unit">cubic feet</span></div>
  <div class="stats">
    <div class="stat"><b id="cf-cuft">-</b><span>cubic feet</span></div>
    <div class="stat"><b id="cf-cum">-</b><span>cubic meters</span></div>
  </div>
</div>
<script>(function(){
var unit='ft';
var l=document.getElementById('cf-l'),w=document.getElementById('cf-w'),h=document.getElementById('cf-h');
document.querySelectorAll('#tt-cf .chip').forEach(function(c){c.addEventListener('click',function(){
  unit=c.dataset.u;
  document.querySelectorAll('#tt-cf .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  document.getElementById('cf-l1').textContent='Length ('+unit+')';
  document.getElementById('cf-l2').textContent='Width ('+unit+')';
  document.getElementById('cf-l3').textContent='Height ('+unit+')';
  run();
});});
function run(){
  var a=parseFloat(l.value),b=parseFloat(w.value),c=parseFloat(h.value);
  if(isNaN(a)||isNaN(b)||isNaN(c)){document.getElementById('cf-cuft').textContent='-';document.getElementById('cf-cum').textContent='-';return;}
  var cuft=unit==='ft'?a*b*c:(a*b*c)/28316.846592;
  document.getElementById('cf-cuft').textContent=(Math.round(cuft*100)/100).toLocaleString('en-US');
  document.getElementById('cf-cum').textContent=(Math.round(cuft*0.0283168466*1000)/1000).toLocaleString('en-US');
  document.getElementById('cf-out').textContent=(Math.round(cuft*100)/100).toLocaleString('en-US');
}
l.addEventListener('input',run);w.addEventListener('input',run);h.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"cubicft": lambda args: CUBICFT,' not in t:
    t = t.replace('    "letter": lambda args: LETTER,',
                  '    "letter": lambda args: LETTER,\n    "cubicft": lambda args: CUBICFT,', 1)

if '"sorter"' not in t:
    js2 = '''
# ---------------------------------------------------------------- line sorter
SORTER = """
<div class="tool" id="tt-sort">
  <div class="chips">
    <button class="chip active" data-d="az">A-Z</button>
    <button class="chip" data-d="za">Z-A</button>
    <button class="chip active" id="sort-ci" type="button">Case-insensitive</button>
    <button class="chip" id="sort-blank" type="button">Remove blank lines</button>
    <button class="chip" id="sort-dup" type="button">Remove duplicates</button>
  </div>
  <div class="field"><label for="sort-in">Paste your list</label>
    <textarea id="sort-in" rows="8" placeholder="one item per line…"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="sort-out">Sorted <button class="btn btn-sm" id="sort-copy" type="button">Copy</button></label>
    <textarea id="sort-out" rows="8" readonly placeholder="sorted list appears here…"></textarea></div>
  <div class="stats"><div class="stat"><b id="sort-n">0</b><span>lines out</span></div></div>
</div>
<script>(function(){
var dir='az',ci=true,blank=false,dedupe=false;
var inp=document.getElementById('sort-in'),out=document.getElementById('sort-out');
function bind(id,set){document.getElementById(id).addEventListener('click',function(){set(!set.__v||set.__v===undefined?true:false);});}
var state={ci:true,blank:false,dedupe:false};
['ci','blank','dup'].forEach(function(k){
  var id=k==='ci'?'sort-ci':k==='blank'?'sort-blank':'sort-dup';
  var el=document.getElementById(id);
  el.addEventListener('click',function(){state[k]=!state[k];el.classList.toggle('active',state[k]);run();});
});
document.querySelectorAll('#tt-sort .chip[data-d]').forEach(function(c){c.addEventListener('click',function(){
  dir=c.dataset.d;
  document.querySelectorAll('#tt-sort .chip[data-d]').forEach(function(x){x.classList.toggle('active',x===c);});
  run();
});});
function run(){
  var lines=inp.value.split('\\n');
  if(state.blank)lines=lines.filter(function(L){return L.trim();});
  if(state.dedupe){var seen={};lines=lines.filter(function(L){if(seen.hasOwnProperty(L))return false;seen[L]=1;return true;});}
  lines.sort(function(x,y){
    var a=ci?x.toLowerCase():x,b=ci?y.toLowerCase():y;
    return dir==='az'?a.localeCompare(b):b.localeCompare(a);
  });
  out.value=lines.join('\\n');
  document.getElementById('sort-n').textContent=lines.length;
}
inp.addEventListener('input',run);
document.getElementById('sort-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('sort-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"sorter": lambda args: SORTER,' not in t:
    t = t.replace('    "cubicft": lambda args: CUBICFT,',
                  '    "cubicft": lambda args: CUBICFT,\n    "sorter": lambda args: SORTER,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"cubicft": lambda' in t, '"sorter": lambda' in t)
