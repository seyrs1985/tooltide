# -*- coding: utf-8 -*-
"""One-shot round 41: pages (inches-to-meters, whitespace-cleaner) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("inches-to-meters", "Inches to Meters", "inches", "meters", 0.0254, "length",
                       "One inch is exactly 0.0254 meters — a small number that trips mental math constantly. The converter keeps all the decimals straight for TV sizes, tool specs and any spec sheet that mixes the two systems.",
                       "Handy anchors: 1 in = 0.0254 m, 10 in = 0.254 m, 39.37 in = 1 m (the memorable reverse), 70 in = 1.778 m (a tall TV diagonal).", dec=4))

    pages.append({
        "slug": "whitespace-cleaner",
        "title": "Whitespace Cleaner — Trim Lines & Collapse Extra Spaces",
        "h1": "Whitespace Cleaner",
        "desc": "Clean messy text instantly: trim leading and trailing spaces on every line, collapse double spaces, and remove blank lines. Live stats and one-click copy.",
        "category": "text",
        "keyword": "remove extra spaces",
        "tool": "whitespace",
        "args": {},
        "intro": [
            "Copied-from-PDF text, CSV exports and pasted emails all carry the same disease: stray leading spaces, doubled spaces and random blank lines. This cleaner trims every line, squeezes space runs down to a single space, and optionally drops blank lines — with a live count of what was removed.",
            "It pairs with the duplicate remover and line sorter as the list-cleaning toolkit: dedupe, sort, strip whitespace, done. All processing is local JavaScript — nothing you paste leaves your browser.",
        ],
        "howto": [
            "Paste the messy text into the input box.",
            "Toggle trims on or off — trim line edges, collapse inner space runs, drop blank lines.",
            "Read the removal stats, then copy the cleaned result.",
        ],
        "faqs": [
            ("What is whitespace?",
             "Any invisible spacing character: regular spaces, tabs, and the line breaks themselves. Cleaner text with tidy whitespace compiles better, sorts better, and pastes into spreadsheets without phantom columns."),
            ("Does it remove spaces inside sentences?",
             "Only the extra ones: 'hello    world' becomes 'hello world' with one space kept, when collapse mode is on. You choose which cleanups run."),
            ("Is my text uploaded anywhere?",
             "No — cleaning is pure JavaScript in your browser. Disconnect from the internet and it still works; nothing is logged anywhere."),
            ("Can it clean tabs too?",
             "Yes — tab characters are treated as whitespace and handled by the trims and collapsing, alongside regular spaces."),
        ],
    })

''' + anchor

if '"inches-to-meters"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"inches-to-meters"' in s, '"whitespace-cleaner"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"whitespace"' not in t:
    js = '''
# ---------------------------------------------------------------- whitespace cleaner
WHITESPACE = """
<div class="tool" id="tt-ws">
  <div class="chips">
    <button class="chip active" id="ws-trim" type="button">Trim line edges</button>
    <button class="chip active" id="ws-collapse" type="button">Collapse space runs</button>
    <button class="chip" id="ws-blank" type="button">Remove blank lines</button>
  </div>
  <div class="field"><label for="ws-in">Messy text</label>
    <textarea id="ws-in" rows="8" placeholder="   paste  text with   stray spaces…  "></textarea></div>
  <div class="stats">
    <div class="stat"><b id="ws-inlines">-</b><span>lines in</span></div>
    <div class="stat"><b id="ws-chars">-</b><span>chars removed</span></div>
  </div>
  <div class="field" style="margin-top:10px"><label for="ws-out">Cleaned <button class="btn btn-sm" id="ws-copy" type="button">Copy</button></label>
    <textarea id="ws-out" rows="8" readonly placeholder="clean text appears here…"></textarea></div>
</div>
<script>(function(){
var inp=document.getElementById('ws-in'),out=document.getElementById('ws-out');
var st={trim:true,collapse:true,blank:false};
['ws-trim','ws-collapse','ws-blank'].forEach(function(id){
  var key=id.replace('ws-','');
  var el=document.getElementById(id);
  el.addEventListener('click',function(){st[key]=!st[key];el.classList.toggle('active',st[key]);run();});
});
function run(){
  var t=inp.value;
  if(!t){out.value='';document.getElementById('ws-inlines').textContent='0';document.getElementById('ws-chars').textContent='0';return;}
  var before=t.length;
  var lines=t.split('\\n');
  lines=lines.map(function(L){
    var x=L;
    if(st.trim)x=x.trim();
    if(st.collapse)x=x.replace(/ {2,}/g,' ');
    return x;
  });
  if(st.blank)lines=lines.filter(function(L){return L.trim();});
  var res=lines.join('\\n');
  out.value=res;
  document.getElementById('ws-inlines').textContent=lines.length.toLocaleString('en-US');
  document.getElementById('ws-chars').textContent=Math.max(0,before-res.length).toLocaleString('en-US');
}
inp.addEventListener('input',run);
['ws-trim','ws-collapse','ws-blank'].forEach(function(id){document.getElementById(id).addEventListener('click',run);});
document.getElementById('ws-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('ws-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"whitespace": lambda args: WHITESPACE,' not in t:
    t = t.replace('    "combiner": lambda args: COMBINER,',
                  '    "combiner": lambda args: COMBINER,\n    "whitespace": lambda args: WHITESPACE,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("whitespace registered:", '"whitespace": lambda' in t)
