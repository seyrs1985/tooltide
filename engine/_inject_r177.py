# -*- coding: utf-8 -*-
"""R177 春季木器与堆肥双页:deck-stain-calculator(露台漆量)+compost-ratio-calculator(堆肥绿棕配比)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: DECKSTAIN ----------
Ds = 'DECKSTAIN = """<div class="tool" id="tt-dst">\n'
Ds += '  <div class="fields">\n'
Ds += '    <div class="field"><label for="dst-a">Deck floor area (sq ft)</label><input id="dst-a" type="number" min="20" max="5000" value="300"></div>\n'
Ds += '    <div class="field"><label for="dst-r">Railing linear feet</label><input id="dst-r" type="number" min="0" max="500" value="40"></div>\n'
Ds += '    <div class="field"><label for="dst-c">Coats</label><select id="dst-c"><option value="1">1 coat - refresh</option><option value="2" selected>2 coats - bare wood</option></select></div>\n'
Ds += '    <div class="field"><label for="dst-p">Price per gallon</label><input id="dst-p" type="number" min="10" value="35"></div>\n'
Ds += '  </div>\n'
Ds += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dst-out">&#8211;</span><span class="result-unit">gallons of stain</span></div>\n'
Ds += '  <div class="stats">\n'
Ds += '    <div class="stat"><b id="dst-s1">&#8211;</b><span>total cost</span></div>\n'
Ds += '    <div class="stat"><b id="dst-s2">&#8211;</b><span>brushing hours</span></div>\n'
Ds += '    <div class="stat"><b id="dst-s3">&#8211;</b><span>redo cycle</span></div>\n'
Ds += '  </div>\n'
Ds += '  <div class="tool-note" id="dst-note"></div>\n'
Ds += '  <button type="button" class="tool-btn" id="dst-share">Share my stain math</button>\n'
Ds += '</div>\n'
Ds += '<script>(function(){\n'
Ds += "var A=document.getElementById('dst-a'),R=document.getElementById('dst-r'),C=document.getElementById('dst-c'),P=document.getElementById('dst-p');\n"
Ds += "function calc(){\n"
Ds += "  var a=parseFloat(A.value)||300,r=parseFloat(R.value)||0,c=parseFloat(C.value)||2,p=parseFloat(P.value)||35;\n"
Ds += "  var area=a+r*2, gal=Math.ceil(area*c/350), cost=gal*p, hrs=Math.round(area*c/120);\n"
Ds += "  var d1=Math.round(cost), d2=hrs;\n"
Ds += "  document.getElementById('dst-out').textContent=gal;\n"
Ds += "  document.getElementById('dst-s1').textContent='$'+d1;\n"
Ds += "  document.getElementById('dst-s2').textContent=d2;\n"
Ds += "  document.getElementById('dst-s3').textContent='2-3 years';\n"
Ds += "  document.getElementById('dst-note').textContent='The rule the aisle forgets: stain covers about 350 square feet per gallon per coat, and rough or thirsty bare wood drinks a first coat faster than the label admits - hence two coats on anything gray. The prep is the part that decides whether the job lasts its 2-3 year cycle: pressure-wash first, because stain over gray dead fibers peels with them, and the forecast needs two dry days either side. Transparent shows grain and fades fastest, solid hides and lasts longest, and the middle semi-transparent is the neighborhood default for a reason.';\n"
Ds += "  document.title='Deck stain: '+gal+' gallons, $'+d1+' - ToolDune';\n"
Ds += "}\n"
Ds += "function save(){try{localStorage.setItem('tt_deckstain',JSON.stringify({a:A.value,r:R.value,c:C.value,p:P.value}));}catch(e){}}\n"
Ds += "[A,R,C,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Ds += "var pre=false;\n"
Ds += "var qs=new URLSearchParams(location.search);\n"
Ds += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Ds += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_deckstain')||'null');if(m){if(m.a){A.value=m.a;}if(m.r){R.value=m.r;}if(m.c){C.value=m.c;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Ds += "calc();\n"
Ds += "document.getElementById('dst-share').addEventListener('click',function(){\n"
Ds += "  var txt='My deck takes '+document.getElementById('dst-out').textContent+' gallons of stain - about '+document.getElementById('dst-s2').textContent+' brushing hours. Run yours:';\n"
Ds += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Ds += "  if(navigator.share){navigator.share({title:'Deck stain math',text:txt,url:url}).catch(function(){});}\n"
Ds += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my stain math';},1500);}\n"
Ds += "});\n"
Ds += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: COMPOSTR ----------
Cp2 = 'COMPOSTR = """<div class="tool" id="tt-cpr">\n'
Cp2 += '  <div class="fields">\n'
Cp2 += '    <div class="field"><label for="cpr-g">Kitchen scraps per week (gallons)</label><input id="cpr-g" type="number" min="0.5" max="20" step="0.5" value="3"></div>\n'
Cp2 += '  </div>\n'
Cp2 += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cpr-out">&#8211;</span><span class="result-unit">gallons of browns weekly</span></div>\n'
Cp2 += '  <div class="stats">\n'
Cp2 += '    <div class="stat"><b id="cpr-s1">&#8211;</b><span>bin size that fits</span></div>\n'
Cp2 += '    <div class="stat"><b id="cpr-s2">&#8211;</b><span>finished compost in</span></div>\n'
Cp2 += '    <div class="stat"><b id="cpr-s3">&#8211;</b><span>browns that are free</span></div>\n'
Cp2 += '  </div>\n'
Cp2 += '  <div class="tool-note" id="cpr-note"></div>\n'
Cp2 += '  <button type="button" class="tool-btn" id="cpr-share">Share my compost ratio</button>\n'
Cp2 += '</div>\n'
Cp2 += '<script>(function(){\n'
Cp2 += "var G=document.getElementById('cpr-g');\n"
Cp2 += "function calc(){\n"
Cp2 += "  var g=parseFloat(G.value)||3, browns=g*2, bin=(g+browns)*3;\n"
Cp2 += "  var d1=Math.round(browns*10)/10, d2=Math.round(bin);\n"
Cp2 += "  document.getElementById('cpr-out').textContent=d1;\n"
Cp2 += "  document.getElementById('cpr-s1').textContent=d2+'+ gallons';\n"
Cp2 += "  document.getElementById('cpr-s2').textContent='2-3 months';\n"
Cp2 += "  document.getElementById('cpr-s3').textContent='dead leaves, cardboard';\n"
Cp2 += "  document.getElementById('cpr-note').textContent='The recipe is two parts brown for every one part green, by volume - kitchen scraps are green, and dry leaves plus shredded cardboard are the browns that keep the pile from becoming a slime event. Smell is the diagnostic: ammonia or sour means add browns and turn; nothing happening means it is too dry, wet it like a wrung sponge. No meat, dairy or cooked food - those invite rats, not microbes. Turn weekly for compost in two to three months, or never turn a static pile and wait a season; both work, one is a hobby and the other is a habit.';\n"
Cp2 += "  document.title='Compost: '+d1+' gal browns per week - ToolDune';\n"
Cp2 += "}\n"
Cp2 += "function save(){try{localStorage.setItem('tt_compostr',JSON.stringify({g:G.value}));}catch(e){}}\n"
Cp2 += "G.addEventListener('input',function(){calc();save();});\n"
Cp2 += "var pre=false;\n"
Cp2 += "var qs=new URLSearchParams(location.search);\n"
Cp2 += "if(qs.get('g')){G.value=qs.get('g');pre=true;}\n"
Cp2 += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_compostr')||'null');if(m&&m.g){G.value=m.g;}}catch(e){}}\n"
Cp2 += "calc();\n"
Cp2 += "document.getElementById('cpr-share').addEventListener('click',function(){\n"
Cp2 += "  var txt='My kitchen bucket needs '+document.getElementById('cpr-out').textContent+' gallons of browns a week. Balance yours:';\n"
Cp2 += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value);\n"
Cp2 += "  if(navigator.share){navigator.share({title:'Compost ratio',text:txt,url:url}).catch(function(){});}\n"
Cp2 += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my compost ratio';},1500);}\n"
Cp2 += "});\n"
Cp2 += "})();\n</script>\n\"\"\"\n\n"

def sub(path, old, new, n=1):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    assert s.count(old) == n, "anchor not %dx: %r" % (n, old[:50])
    s = s.replace(old, new)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)

TOOLS_P = BASE + r"\tools.py"
PAGES_P = BASE + r"\pages.py"
BUILD_P = BASE + r"\build.py"

src = io.open(TOOLS_P, encoding="utf-8").read()
for name in ("DECKSTAIN", "COMPOSTR"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Ds + Cp2 + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "grassseed": lambda args: GRASSSEED,',
    '    "grassseed": lambda args: GRASSSEED,\n'
    '    "deckstain": lambda args: DECKSTAIN,\n'
    '    "compostr": lambda args: COMPOSTR,')
sub(BUILD_P, '    "saliner": "🌊", "rainbarrel": "☔", "grassseed": "🌱",',
    '    "saliner": "🌊", "rainbarrel": "☔", "grassseed": "🌱",\n'
    '    "deckstain": "🎨", "compostr": "♻",')

P = []
d = {'slug': 'deck-stain-calculator',
     'title': 'Deck Stain Calculator - Gallons, Cost and Brushing Hours',
     'h1': 'Deck Stain Calculator',
     'desc': 'Deck area, railing and coats give gallons of stain, the cost and the brushing hours - with the prep rule that decides whether the job lasts. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'deck stain calculator how much stain gallons per square foot',
     'tool': 'deckstain',
     'args': {},
     'intro': ["Enter the deck floor area, the railing run, coats and your stain price. The calculator gives gallons - stain covers about 350 square feet per gallon per coat - plus cost and honest brushing hours.",
              "The prep is what decides whether the job lasts its two-to-three-year cycle: pressure-wash first, because stain over gray dead fibers peels with them, and the forecast needs two dry days either side. Transparent shows grain and fades fastest; solid hides and lasts longest."],
     'howto': ["Measure the floor and add the railing run - it drinks stain too.",
               "Two coats on bare or gray wood, one on a recent refresh.",
               "Pressure-wash first and wait two dry days after."],
     'faqs': [("How much stain do I need for my deck?",
               "About a gallon per 350 square feet per coat, with rough bare wood drinking more. The calculator adds the railing run - rails and balusters can add a third again to the job."),
              ("How often should a deck be stained?",
               "Every two to three years for transparent stains, three to four for solid color - sun and foot traffic decide more than the calendar. When water soaks in instead of beading, the deck is asking."),
              ("Can I stain over old stain?",
               "Only over sound, clean stain of the same opacity family - peeling or gray areas need pressure-washing and stripping first, or the new coat peels with the old within a season."),
              ("Is it better to spray or brush deck stain?",
               "A sprayer is three times faster but pushes stain into back-brushing anyway, so most DIYers brush by pad and win the control. Either way the two-dry-day forecast matters more than the applicator.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'compost-ratio-calculator',
     'title': 'Compost Ratio Calculator - Browns for Your Kitchen Scraps Bucket',
     'h1': 'Compost Ratio Calculator',
     'desc': 'Kitchen scraps per week give the browns volume that keeps the pile composting instead of rotting - bin size, timing and the smell diagnostics. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'compost ratio calculator browns greens kitchen scraps',
     'tool': 'compostr',
     'args': {},
     'intro': ["Enter what your kitchen scrap bucket collects in a week. The calculator gives the browns volume - two parts dry leaves and shredded cardboard per one part scraps - that keeps the pile composting instead of rotting.",
              "Smell is the whole diagnostic: ammonia or sour means add browns and turn, silence means it is too dry. No meat, dairy or cooked food - those invite rats, not microbes - and the finished compost lands in two to three months turned weekly, or a patient season if you never turn it."],
     'howto': ["Weigh or estimate the weekly bucket - most kitchens run 2-4 gallons.",
               "Collect browns: dead leaves, shredded cardboard, sawdust.",
               "Layer as you go; the bin should smell like a forest floor."],
     'faqs': [("What is the right brown to green ratio for compost?",
               "Two parts browns to one part greens by volume - dry leaves, straw and shredded cardboard against kitchen scraps and fresh clippings. The calculator sizes the browns for your bucket."),
              ("Why does my compost smell bad?",
               "Too wet, too green, or meat inside: the anaerobic smell means add browns and turn for air. A working pile smells like a forest floor - if you can smell it from the patio, the ratio needs carbon."),
              ("What should never go in compost?",
               "Meat, dairy, oils and cooked food attract rats; diseased plants and stubborn weeds carry through. Everything else plant-based is fair game, stickers removed."),
              ("How long does compost take?",
               "Two to three months with weekly turning; a static pile takes a season and almost no effort. Both produce the same dark crumbly end - the turning is a speed choice, not a quality one.")]}
P.append("    pages.append(%r)\n" % (d,))

with io.open(PAGES_P, encoding="utf-8") as f:
    s = f.read()
anchor = "    # ---------- Index metadata used by build ----------"
assert s.count(anchor) == 1, "pages anchor"
s = s.replace(anchor, "".join(P) + anchor)
with io.open(PAGES_P, "w", encoding="utf-8", newline="") as f:
    f.write(s)

import ast
for f in (TOOLS_P, PAGES_P, BUILD_P):
    ast.parse(io.open(f, encoding="utf-8").read())
print("R177 inject OK: 2 renderers + 2 pages + 2 emoji, ast passed")
