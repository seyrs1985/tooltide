# -*- coding: utf-8 -*-
"""One-shot round 30: pages (unit-price, word-frequency) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "unit-price-calculator",
        "title": "Unit Price Calculator — Which Pack Is Actually Cheaper?",
        "h1": "Unit Price Calculator",
        "desc": "Compare two packs by unit price: price ÷ quantity for A and B, winner highlighted. Works with any unit — per 100g, per liter, per sheet. Stop falling for bulk illusions.",
        "category": "calculator",
        "keyword": "unit price calculator",
        "tool": "unitprice",
        "args": {},
        "intro": [
            "The shelf price lies by omission: the 900 ml bottle at $3.40 versus the 1.5 L jug at $5.10 — which is cheaper per drink? Enter price and quantity for each pack, and the calculator computes the unit price of both and names the winner instantly.",
            "Bulk is usually cheaper per unit — but not always, and supermarkets know shoppers assume it is. Ten seconds with this calculator pays for itself the first time it catches a 'family size' that costs more per gram than the regular box.",
        ],
        "howto": [
            "Enter pack A's price and quantity, then pack B's.",
            "Read both unit prices — the cheaper one is highlighted automatically.",
            "Use any quantity unit you like (grams, ml, sheets, tablets); just use the same unit for both packs.",
        ],
        "faqs": [
            ("How do I calculate unit price?",
             "Divide the price by the quantity: $3.40 for 900 ml is 3.40 ÷ 900 = $0.00378 per ml (or 37.8 cents per 100 ml). Do the same for the other pack and compare — the calculator does both divisions at once."),
            ("Is bigger always cheaper per unit?",
             "Usually, but not always. Discount lines sometimes cost more per gram than the standard size, and sale prices can invert the rule. That is exactly why shelf tags saying 'value size' deserve a quick unit-price check."),
            ("What unit should I compare in?",
             "Any unit, as long as both packs use the same one. Per 100 g or per liter reads most naturally; for paper goods, per sheet or per 100 sheets is the honest comparison."),
            ("Does it work for three or more packs?",
             "Compare in pairs — A against B, then the winner against C. Two rounds settle a three-way comparison."),
        ],
    })

    pages.append({
        "slug": "word-frequency-counter",
        "title": "Word Frequency Counter — Top Words in Any Text",
        "h1": "Word Frequency Counter",
        "desc": "Paste text and see which words appear most often, ranked by count with percentages. Live TOP table, stopwords toggle, 100% in-browser.",
        "category": "text",
        "keyword": "word frequency counter",
        "tool": "wordfreq",
        "args": {},
        "intro": [
            "Paste an article, essay or transcript and instantly see which words you use most: a ranked table of every word with its count and percentage of the text. Toggle small function words (the, a, of…) off to reveal the words that actually carry your meaning — writers use this to catch overused words; SEO folks, to check keyword balance.",
            "The analysis runs entirely in your browser: nothing you paste is uploaded anywhere. Case is folded (The and the count together), punctuation is ignored, and the table re-ranks live as you edit.",
        ],
        "howto": [
            "Paste your text into the box — the frequency table builds instantly.",
            "Toggle 'ignore common words' to hide the/a/of-style fillers and see content words.",
            "Scan the top of the table for accidental repetition, then copy or re-edit your text.",
        ],
        "faqs": [
            ("What is word frequency analysis used for?",
             "Writers catch overused words; students check vocabulary variety in essays; SEO writers verify keyword balance; linguists and teachers study text style. It is the fastest way to see what a text is really made of."),
            ("How are words counted?",
             "Text is split on anything that is not a letter or number, and case is folded — 'Dog', 'dog' and 'DOG!' all count as the same word. Numbers count as words too."),
            ("What are stopwords?",
             "High-frequency function words (the, and, of, to…) that carry grammar but little meaning. Hiding them lets the content words rise to the top of the table — usually where the insight is."),
            ("Is my text private?",
             "Completely — counting happens in your browser's JavaScript. Nothing is transmitted, stored or logged, so confidential drafts are safe here."),
        ],
    })

''' + anchor

if '"unit-price-calculator"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"unit-price-calculator"' in s, '"word-frequency-counter"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"unitprice"' not in t:
    js = '''
# ---------------------------------------------------------------- unit price
UNITPRICE = """
<div class="tool" id="tt-up">
  <div class="fields">
    <div class="field"><label for="up-ap">Pack A price ($)</label><input type="number" id="up-ap" step="0.01" min="0" placeholder="3.40"></div>
    <div class="field"><label for="up-aq">Pack A quantity (g/ml/pcs)</label><input type="number" id="up-aq" step="any" min="0" placeholder="900"></div>
  </div>
  <div class="fields">
    <div class="field"><label for="up-bp">Pack B price ($)</label><input type="number" id="up-bp" step="0.01" min="0" placeholder="5.10"></div>
    <div class="field"><label for="up-bq">Pack B quantity</label><input type="number" id="up-bq" step="any" min="0" placeholder="1500"></div>
  </div>
  <div class="result"><span class="result-num" id="up-win">-</span></div>
  <div class="stats">
    <div class="stat"><b id="up-ua">-</b><span>A per unit</span></div>
    <div class="stat"><b id="up-ub">-</b><span>B per unit</span></div>
    <div class="stat"><b id="up-diff">-</b><span>B vs A</span></div>
  </div>
</div>
<script>(function(){
var ids=['up-ap','up-aq','up-bp','up-bq'];
function val(id){return parseFloat(document.getElementById(id).value);}
function money(n){return '$'+n.toLocaleString('en-US',{maximumFractionDigits:4});}
function run(){
  var ap=val('up-ap'),aq=val('up-aq'),bp=val('up-bp'),bq=val('up-bq');
  if(!ap||!aq||!bp||!bq){document.getElementById('up-win').textContent='-';
    document.getElementById('up-ua').textContent='-';document.getElementById('up-ub').textContent='-';
    document.getElementById('up-diff').textContent='-';return;}
  var ua=ap/aq,ub=bp/bq;
  document.getElementById('up-ua').textContent=money(ua);
  document.getElementById('up-ub').textContent=money(ub);
  var pct=Math.round((ub-ua)/ua*100);
  document.getElementById('up-diff').textContent=(pct>=0?'+':'')+pct+'%';
  document.getElementById('up-win').textContent=ua<ub?'Pack A is cheaper':'Pack B is cheaper';
}
ids.forEach(function(id){document.getElementById(id).addEventListener('input',run);});
run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"unitprice": lambda args: UNITPRICE,' not in t:
    t = t.replace('    "sorter": lambda args: SORTER,',
                  '    "sorter": lambda args: SORTER,\n    "unitprice": lambda args: UNITPRICE,', 1)

if '"wordfreq"' not in t:
    js2 = '''
# ---------------------------------------------------------------- word frequency
WORDFREQ = """
<div class="tool" id="tt-wf">
  <div class="chips"><button class="chip active" id="wf-stop" type="button">Ignore common words</button></div>
  <div class="field"><label for="wf-in">Paste text</label>
    <textarea id="wf-in" rows="7" placeholder="Paste an article, essay or transcript…"></textarea></div>
  <table class="copytable"><thead><tr><th>#</th><th>Word</th><th>Count</th><th>% of text</th></tr></thead><tbody id="wf-tb"></tbody></table>
</div>
<script>(function(){
var STOP={the:1,a:1,an:1,and:1,or:1,but:1,of:1,to:1,in:1,on:1,at:1,for:1,with:1,by:1,from:1,as:1,is:1,are:1,was:1,were:1,be:1,been:1,it:1,its:1,this:1,that:1,these:1,those:1,i:1,you:1,he:1,she:1,we:1,they:1,my:1,your:1,his:1,her:1,their:1,our:1,not:1,no:1,so:1,if:1,then:1,than:1,too:1,very:1,can:1,will:1,just:1};
var inp=document.getElementById('wf-in'),tb=document.getElementById('wf-tb');
var stop=document.getElementById('wf-stop');
var hideStop=true;
stop.addEventListener('click',function(){hideStop=!hideStop;this.classList.toggle('active',hideStop);run();});
function run(){
  var words=(inp.value.toLowerCase().match(/[a-z0-9\\u00c0-\\u024f']+/gi)||[]);
  var counts={};
  words.forEach(function(w){counts[w]=(counts[w]||0)+1;});
  var rows=Object.keys(counts).map(function(w){return [w,counts[w]];});
  rows.sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0]);});
  var html='',shown=0,total=words.length||1;
  for(var i=0;i<rows.length&&shown<25;i++){
    if(hideStop&&STOP[rows[i][0]])continue;
    shown++;
    html+='<tr><td>'+shown+'</td><td>'+rows[i][0]+'</td><td>'+rows[i][1]+'</td><td>'+Math.round(rows[i][1]/total*1000)/10+'%</td></tr>';
  }
  tb.innerHTML=html||'<tr><td colspan="4" style="color:#94a3b8">Paste text to see word frequencies…</td></tr>';
}
inp.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"wordfreq": lambda args: WORDFREQ,' not in t:
    t = t.replace('    "unitprice": lambda args: UNITPRICE,',
                  '    "unitprice": lambda args: UNITPRICE,\n    "wordfreq": lambda args: WORDFREQ,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"unitprice": lambda' in t, '"wordfreq": lambda' in t)
