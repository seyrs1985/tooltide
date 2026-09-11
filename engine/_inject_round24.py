# -*- coding: utf-8 -*-
"""One-shot round 24: pages (square-footage, seconds-converter) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "square-footage-calculator",
        "title": "Square Footage Calculator — Length × Width in Feet or Meters",
        "h1": "Square Footage Calculator",
        "desc": "Calculate square footage (or square meters) from length and width. Works in feet or meters, converts between them, and totals multiple rooms. For flooring, paint and real estate.",
        "category": "calculator",
        "keyword": "square footage calculator",
        "tool": "sqft",
        "args": {},
        "intro": [
            "Enter the length and width of a room, house or garden and get the area in square feet or square meters — the number behind flooring orders, paint estimates, rent-per-square-foot comparisons and 'is this apartment actually big?' checks. It works in either unit and converts automatically.",
            "For irregular spaces, measure section by section and add the areas together — the running total box keeps the math honest. An L-shaped living room is just two rectangles that happen to share a wall.",
        ],
        "howto": [
            "Choose feet or meters, then enter the length and width.",
            "Read the area in square feet and square meters side by side.",
            "For multi-room projects, add each room's area to the running total.",
        ],
        "faqs": [
            ("How do I calculate square footage of a room?",
             "Measure the length and width in feet and multiply them: a 12 ft × 15 ft room is 180 square feet. For closets and alcoves, measure separately and add the areas."),
            ("How many square feet is 12x12?",
             "12 ft × 12 ft = 144 square feet — a standard bedroom size, and conveniently exactly the amount of flooring in one box quote territory (most boxes cover 18–25 sq ft, so order 6–8 boxes plus 10% waste)."),
            ("How do I convert square feet to square meters?",
             "Multiply by 0.0929. A 1,000 sq ft apartment is about 92.9 square meters. The calculator shows both units side by side automatically."),
            ("How much extra flooring should I buy?",
             "Add 10% for straight layouts and 15% for diagonal patterns or lots of cuts — waste is real, and dye lots mean buying more later may not match. Use the running total to plan the order."),
        ],
    })

    pages.append({
        "slug": "seconds-converter",
        "title": "Seconds to Hours, Minutes & Seconds Converter — h:m:s",
        "h1": "Seconds Converter",
        "desc": "Convert a raw number of seconds into hours, minutes and seconds (h:m:s) — perfect for video lengths, run times and logs. Two-way: type a duration too.",
        "category": "converter",
        "keyword": "seconds to hours",
        "tool": "secondsconv",
        "args": {},
        "intro": [
            "Type a raw number of seconds — 3725, 86,400, whatever a log file, API response or stopwatch hands you — and see it as readable hours, minutes and seconds. Go the other way too: type 1:02:05 and get the total seconds, which is what video timestamps and countdowns actually expect.",
            "It is a small tool with an outsized number of uses: run splits (a marathon in seconds), podcast chapters, benchmark timings, game speedruns, and every timestamp that was clearly never meant for human eyes.",
        ],
        "howto": [
            "Type a number of seconds — the h:m:s breakdown appears instantly.",
            "Or type a duration like 1:02:05 in the second box to get total seconds.",
            "Both boxes stay in sync — edit either side at any time.",
        ],
        "faqs": [
            ("How many seconds are in an hour?",
             "3,600 — 60 seconds × 60 minutes. A day is 86,400 seconds, which is the number behind most computer clock internals."),
            ("How do I convert seconds to h:mm:ss?",
             "Divide by 3,600 for hours, take the remainder and divide by 60 for minutes, and what is left is seconds. 7,325 seconds = 2:02:05. The converter does this and shows the padding."),
            ("How many seconds is a 4 minute mile?",
             "A 4-minute mile is 240 seconds — or 0.066 hours. Elite marathoners cover the same distance in under 4:35 per mile for two hours straight."),
            ("Why do APIs return seconds instead of hh:mm:ss?",
             "Because plain integer seconds are unambiguous, sortable and easy to add — no 60-based carrying. Humans get readability; machines get seconds, and this converter translates between them."),
        ],
    })

''' + anchor

if '"square-footage-calculator"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"square-footage-calculator"' in s, '"seconds-converter"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"sqft"' not in t:
    js = '''
# ---------------------------------------------------------------- square footage
SQFT = """
<div class="tool" id="tt-sq">
  <div class="chips" role="tablist">
    <button class="chip active" data-u="ft">Feet</button>
    <button class="chip" data-u="m">Meters</button>
  </div>
  <div class="fields">
    <div class="field"><label for="sq-l">Length</label><input type="number" id="sq-l" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="sq-w">Width</label><input type="number" id="sq-w" step="any" min="0" placeholder="15"></div>
  </div>
  <div class="result"><span class="result-num" id="sq-ft">-</span><span class="result-unit">sq ft</span></div>
  <div class="stats">
    <div class="stat"><b id="sq-sqft">-</b><span>square feet</span></div>
    <div class="stat"><b id="sq-sqm">-</b><span>square meters</span></div>
    <div class="stat"><b id="sq-total">-</b><span>running total</span></div>
  </div>
  <button class="btn btn-sm" id="sq-add" type="button">+ Add to running total</button>
</div>
<script>(function(){
var unit='ft',total=0;
var l=document.getElementById('sq-l'),w=document.getElementById('sq-w');
document.querySelectorAll('#tt-sq .chip').forEach(function(c){c.addEventListener('click',function(){
  unit=c.dataset.u;
  document.querySelectorAll('#tt-sq .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  var labels=document.querySelectorAll('#tt-sq label');
  labels[1].textContent='Length ('+unit+')';labels[2].textContent='Width ('+unit+')';
  run();
});});
function run(){
  var a=parseFloat(l.value),b=parseFloat(w.value);
  var sq=(isNaN(a)||isNaN(b))?null:a*b;
  var sqft=unit==='ft'?sq:sq*10.76391042;
  var sqm=unit==='ft'?sq*0.09290304:sq;
  document.getElementById('sq-ft').textContent=sq===null?'-':(Math.round(sqft*10)/10).toLocaleString('en-US');
  document.getElementById('sq-sqft').textContent=sq===null?'-':(Math.round(sqft*10)/10).toLocaleString('en-US');
  document.getElementById('sq-sqm').textContent=sq===null?'-':(Math.round(sqm*10)/10).toLocaleString('en-US');
}
l.addEventListener('input',run);w.addEventListener('input',run);
document.getElementById('sq-add').addEventListener('click',function(){
  var v=parseFloat(document.getElementById('sq-sqft').textContent.replace(/,/g,''));
  if(!isNaN(v)){total+=v;document.getElementById('sq-total').textContent=Math.round(total*10)/10;}
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"sqft": lambda args: SQFT,' not in t:
    t = t.replace('    "coinflip": lambda args: COINFLIP,',
                  '    "coinflip": lambda args: COINFLIP,\n    "sqft": lambda args: SQFT,', 1)

if '"secondsconv"' not in t:
    js2 = '''
# ---------------------------------------------------------------- seconds converter
SECONDS = """
<div class="tool" id="tt-sec">
  <div class="field"><label for="sec-in">Total seconds</label><input type="number" id="sec-in" step="1" min="0" placeholder="3725"></div>
  <div class="result"><span class="result-num" id="sec-out">-</span></div>
  <div class="field" style="margin-top:12px"><label for="sec-hms">Duration (h:mm:ss or mm:ss)</label><input type="text" id="sec-hms" placeholder="1:02:05"></div>
</div>
<script>(function(){
var sIn=document.getElementById('sec-in'),hms=document.getElementById('sec-hms');
var out=document.getElementById('sec-out');
var lock=false;
function pad(n){return (n<10?'0':'')+n;}
function fromSeconds(v){
  var h=Math.floor(v/3600),m=Math.floor(v%3600/60),s=v%60;
  return h>0?h+':'+pad(m)+':'+pad(s):m+':'+pad(s);
}
function toSeconds(v){
  var parts=v.trim().split(':').map(Number);
  if(parts.some(isNaN))return null;
  if(parts.length===3)return parts[0]*3600+parts[1]*60+parts[2];
  if(parts.length===2)return parts[0]*60+parts[1];
  if(parts.length===1)return parts[0];
  return null;
}
sIn.addEventListener('input',function(){
  if(lock)return;lock=true;
  var v=parseInt(sIn.value);
  if(isNaN(v)){out.textContent='-';hms.value='';lock=false;return;}
  out.textContent=fromSeconds(v);hms.value=fromSeconds(v);
  lock=false;
});
hms.addEventListener('input',function(){
  if(lock)return;lock=true;
  var v=toSeconds(this.value);
  if(v===null){out.textContent='(use h:mm:ss)';sIn.value='';lock=false;return;}
  out.textContent=v.toLocaleString('en-US')+' seconds';sIn.value=v;
  lock=false;
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"secondsconv": lambda args: SECONDS,' not in t:
    t = t.replace('    "sqft": lambda args: SQFT,',
                  '    "sqft": lambda args: SQFT,\n    "secondsconv": lambda args: SECONDS,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"sqft": lambda' in t, '"secondsconv": lambda' in t)
