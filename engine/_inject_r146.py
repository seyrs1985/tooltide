# -*- coding: utf-8 -*-
"""R146 圣诞树与包装三连:tree-water(浇水续航)+tree-lights(灯串数)+wrapping-paper(包装纸卷数)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: TREEWATER ----------
Tw = 'TREEWATER = """<div class="tool" id="tt-twt">\n'
Tw += '  <div class="fields">\n'
Tw += '    <div class="field"><label for="tw-d">Trunk diameter (inches)</label><input id="tw-d" type="number" min="1" max="8" step="0.25" value="3"></div>\n'
Tw += '    <div class="field"><label for="tw-c">Stand reservoir (quarts)</label><input id="tw-c" type="number" min="8" max="100" value="24"></div>\n'
Tw += '    <div class="field"><label for="tw-r">Room warmth</label><select id="tw-r"><option value="1">Cool room</option><option value="1.3" selected>Normal heating</option><option value="1.6">Hot - fireplace or sunny window</option></select></div>\n'
Tw += '  </div>\n'
Tw += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tw-out">&#8211;</span><span class="result-unit">quarts per day</span></div>\n'
Tw += '  <div class="stats">\n'
Tw += '    <div class="stat"><b id="tw-s1">&#8211;</b><span>refill every</span></div>\n'
Tw += '    <div class="stat"><b id="tw-s2">&#8211;</b><span>season total, 30 days</span></div>\n'
Tw += '    <div class="stat"><b id="tw-s3">&#8211;</b><span>first-day thirst</span></div>\n'
Tw += '  </div>\n'
Tw += '  <div class="tool-note" id="tw-note"></div>\n'
Tw += '  <button type="button" class="tool-btn" id="tw-share">Share my tree water math</button>\n'
Tw += '</div>\n'
Tw += '<script>(function(){\n'
Tw += "var D=document.getElementById('tw-d'),C=document.getElementById('tw-c'),R=document.getElementById('tw-r');\n"
Tw += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>0?v:0;}\n"
Tw += "function calc(){\n"
Tw += "  var d=num(D),cap=num(C),warm=parseFloat(R.value)||1.3;\n"
Tw += "  var daily=d*warm, refill=cap/daily, season=daily*30, first=d*2;\n"
Tw += "  var d1=Math.round(daily*10)/10, d2=Math.round(refill*10)/10, d3=Math.round(season);\n"
Tw += "  document.getElementById('tw-out').textContent=d1;\n"
Tw += "  document.getElementById('tw-s1').textContent=d2+' days';\n"
Tw += "  document.getElementById('tw-s2').textContent=d3+' qt';\n"
Tw += "  document.getElementById('tw-s3').textContent=Math.round(first*10)/10+' qt';\n"
Tw += "  document.getElementById('tw-note').textContent='The rule is one quart per inch of trunk per day, doubled the first day because the tree is thirsty after the trip. The non-negotiable is under this note: if the cut end goes dry even once, sap seals it and the tree stops drinking forever - so check daily the first week, and make the fresh half-inch cut at planting the moment you get home. Hot rooms drink a third again more. A tree that runs dry is not just sad, it is the fire-hazard version of itself, so lights on only when someone is home until New Year takes the tree out.';\n"
Tw += "  document.title='Tree water: '+d1+' qt a day - ToolDune';\n"
Tw += "}\n"
Tw += "function save(){try{localStorage.setItem('tt_treewater',JSON.stringify({d:D.value,c:C.value,r:R.value}));}catch(e){}}\n"
Tw += "[D,C,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Tw += "var pre=false;\n"
Tw += "var qs=new URLSearchParams(location.search);\n"
Tw += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
Tw += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_treewater')||'null');if(m){if(m.d){D.value=m.d;}if(m.c){C.value=m.c;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Tw += "calc();\n"
Tw += "document.getElementById('tw-share').addEventListener('click',function(){\n"
Tw += "  var txt='My tree drinks '+document.getElementById('tw-out').textContent+' quarts a day - refill every '+document.getElementById('tw-s1').textContent+'. Size yours:';\n"
Tw += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
Tw += "  if(navigator.share){navigator.share({title:'Christmas tree watering',text:txt,url:url}).catch(function(){});}\n"
Tw += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my tree water math';},1500);}\n"
Tw += "});\n"
Tw += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: TREELIGHTS ----------
Tl = 'TREELIGHTS = """<div class="tool" id="tt-tlt">\n'
Tl += '  <div class="fields">\n'
Tl += '    <div class="field"><label for="tl-h">Tree height (feet)</label><input id="tl-h" type="number" min="2" max="15" step="0.5" value="6"></div>\n'
Tl += '    <div class="field"><label for="tl-f">Coverage style</label><select id="tl-f"><option value="50">Sparse - 50 bulbs per foot</option><option value="100" selected>Classic - 100 per foot</option><option value="150">Lush - 150 per foot</option></select></div>\n'
Tl += '    <div class="field"><label for="tl-t">Bulb type</label><select id="tl-t"><option value="0.05" selected>Mini LED</option><option value="0.4">Mini incandescent</option></select></div>\n'
Tw_dummy = None
Tl += '  </div>\n'
Tl += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tl-out">&#8211;</span><span class="result-unit">bulbs on the tree</span></div>\n'
Tl += '  <div class="stats">\n'
Tl += '    <div class="stat"><b id="tl-s1">&#8211;</b><span>100-count strings to buy</span></div>\n'
Tl += '    <div class="stat"><b id="tl-s2">&#8211;</b><span>watts when lit</span></div>\n'
Tl += '    <div class="stat"><b id="tl-s3">&#8211;</b><span>season electricity, 6 h/day</span></div>\n'
Tl += '  </div>\n'
Tl += '  <div class="tool-note" id="tl-note"></div>\n'
Tl += '  <button type="button" class="tool-btn" id="tl-share">Share my light count</button>\n'
Tl += '</div>\n'
Tl += '<script>(function(){\n'
Tl += "var H=document.getElementById('tl-h'),F=document.getElementById('tl-f'),T2=document.getElementById('tl-t');\n"
Tl += "function calc(){\n"
Tl += "  var h=parseFloat(H.value)||6,per=parseFloat(F.value)||100,watt=parseFloat(T2.value)||0.05;\n"
Tl += "  var bulbs=h*per, strings=Math.ceil(bulbs/100), watts=bulbs*watt;\n"
Tl += "  var season=watts*6*45/1000*0.17;\n"
Tl += "  var d1=Math.round(bulbs), d2=Math.round(watts*10)/10, d3=Math.round(season*100)/100;\n"
Tl += "  document.getElementById('tl-out').textContent=d1;\n"
Tl += "  document.getElementById('tl-s1').textContent=strings;\n"
Tl += "  document.getElementById('tl-s2').textContent=d2+' W';\n"
Tl += "  document.getElementById('tl-s3').textContent='$'+d3;\n"
Tl += "  document.getElementById('tl-note').textContent='The classic rule is 100 mini lights per foot of tree; sparse or lush adjusts it. The technique that beats circling: wrap each major branch in a triangle from trunk to tip and back, working in sections - lights end up deep in the tree instead of skimming the surface, and a dropped section does not unwind the whole spiral. Test every string before it goes up, keep the heaviest strands near the bottom where the cord runs, and plug everything into one switched power strip so the whole tree goes dark with a single stomp-worthy dash.';\n"
Tl += "  document.title='Tree lights: '+strings+' strings for '+h+' ft - ToolDune';\n"
Tl += "}\n"
Tl += "function save(){try{localStorage.setItem('tt_treelights',JSON.stringify({h:H.value,f:F.value,t:T2.value}));}catch(e){}}\n"
Tl += "[H,F,T2].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Tl += "var pre=false;\n"
Tl += "var qs=new URLSearchParams(location.search);\n"
Tl += "if(qs.get('h')){H.value=qs.get('h');pre=true;}\n"
Tl += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_treelights')||'null');if(m){if(m.h){H.value=m.h;}if(m.f){F.value=m.f;}if(m.t){T2.value=m.t;}}}catch(e){}}\n"
Tl += "calc();\n"
Tl += "document.getElementById('tl-share').addEventListener('click',function(){\n"
Tl += "  var txt='A '+H.value+' foot tree takes about '+document.getElementById('tl-out').textContent+' lights ('+document.getElementById('tl-s1').textContent+' strings). Size yours:';\n"
Tl += "  var url=location.origin+location.pathname+'?h='+encodeURIComponent(H.value);\n"
Tl += "  if(navigator.share){navigator.share({title:'Christmas tree lights',text:txt,url:url}).catch(function(){});}\n"
Tl += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my light count';},1500);}\n"
Tl += "});\n"
Tl += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: WRAPCALC ----------
Wp = 'WRAPCALC = """<div class="tool" id="tt-wp">\n'
Wp += '  <div class="fields">\n'
Wp += '    <div class="field"><label for="wp-n">Gifts to wrap</label><input id="wp-n" type="number" min="1" max="200" value="12"></div>\n'
Wp += '    <div class="field"><label for="wp-s">Average gift size</label><select id="wp-s"><option value="1">Book-sized - 1 sq ft</option><option value="3" selected>Sweater box - 3 sq ft</option><option value="6">Large toy - 6 sq ft</option><option value="10">Awkward giant - 10 sq ft</option></select></div>\n'
Wp += '    <div class="field"><label for="wp-w">Wrapping style</label><select id="wp-w"><option value="1.2" selected>Neat folds</option><option value="1.5">Enthusiastic tape-and-hope</option></select></div>\n'
Wp += '    <div class="field"><label for="wp-p">Price per 30 sq ft roll</label><input id="wp-p" type="number" min="1" step="0.5" value="4"></div>\n'
Wp += '  </div>\n'
Wp += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wp-out">&#8211;</span><span class="result-unit">sq ft of paper</span></div>\n'
Wp += '  <div class="stats">\n'
Wp += '    <div class="stat"><b id="wp-s1">&#8211;</b><span>rolls to buy</span></div>\n'
Wp += '    <div class="stat"><b id="wp-s2">&#8211;</b><span>paper cost</span></div>\n'
Wp += '    <div class="stat"><b id="wp-s3">&#8211;</b><span>per gift</span></div>\n'
Wp += '  </div>\n'
Wp += '  <div class="tool-note" id="wp-note"></div>\n'
Wp += '  <button type="button" class="tool-btn" id="wp-share">Share my paper math</button>\n'
Wp += '</div>\n'
Wp += '<script>(function(){\n'
Wp += "var N=document.getElementById('wp-n'),S=document.getElementById('wp-s'),W2=document.getElementById('wp-w'),P=document.getElementById('wp-p');\n"
Wp += "function calc(){\n"
Wp += "  var n=Math.max(1,Math.round(parseFloat(N.value)||0)),s=parseFloat(S.value)||3,w=parseFloat(W2.value)||1.2,p=parseFloat(P.value)||4;\n"
Wp += "  var sqft=n*s*w, rolls=Math.ceil(sqft/30), cost=rolls*p, per=cost/n;\n"
Wp += "  var d1=Math.round(sqft), d2=Math.round(cost*100)/100, d3=Math.round(per*100)/100;\n"
Wp += "  document.getElementById('wp-out').textContent=d1;\n"
Wp += "  document.getElementById('wp-s1').textContent=rolls;\n"
Wp += "  document.getElementById('wp-s2').textContent='$'+d2;\n"
Wp += "  document.getElementById('wp-s3').textContent='$'+d3;\n"
Wp += "  document.getElementById('wp-note').textContent='The waste factor is the honest part - real wrapping loses a fifth to a third of the roll to off-cuts and the piece you measured wrong. Two upgrades that actually save: a roll of kraft butcher paper plus a rubber stamp kit beats character paper at triple the price per square foot, and gift bags are the reusable endgame - buy plain ones once, use them for a decade, skip the tape and the folding entirely. Measure the biggest gift first and buy for it, not for the average; one awkward giant always hides in the pile until Christmas Eve.';\n"
Wp += "  document.title='Wrapping: '+rolls+' rolls for '+n+' gifts - ToolDune';\n"
Wp += "}\n"
Wp += "function save(){try{localStorage.setItem('tt_wrapcalc',JSON.stringify({n:N.value,s:S.value,w:W2.value,p:P.value}));}catch(e){}}\n"
Wp += "[N,S,W2,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Wp += "var pre=false;\n"
Wp += "var qs=new URLSearchParams(location.search);\n"
Wp += "if(qs.get('n')){N.value=qs.get('n');pre=true;}\n"
Wp += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_wrapcalc')||'null');if(m){if(m.n){N.value=m.n;}if(m.s){S.value=m.s;}if(m.w){W2.value=m.w;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Wp += "calc();\n"
Wp += "document.getElementById('wp-share').addEventListener('click',function(){\n"
Wp += "  var txt='Wrapping '+N.value+' gifts takes '+document.getElementById('wp-out').textContent+' sq ft of paper - '+document.getElementById('wp-s1').textContent+' rolls. Plan yours:';\n"
Wp += "  var url=location.origin+location.pathname+'?n='+encodeURIComponent(N.value);\n"
Wp += "  if(navigator.share){navigator.share({title:'Wrapping paper math',text:txt,url:url}).catch(function(){});}\n"
Wp += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my paper math';},1500);}\n"
Wp += "});\n"
Wp += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("TREEWATER", "TREELIGHTS", "WRAPCALC"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Tw + Tl + Wp + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "bogo": lambda args: BOGO,',
    '    "bogo": lambda args: BOGO,\n'
    '    "treewater": lambda args: TREEWATER,\n'
    '    "treelights": lambda args: TREELIGHTS,\n'
    '    "wrapcalc": lambda args: WRAPCALC,')
sub(BUILD_P, '    "shipfree": "📦", "warranty": "💳", "bogo": "🎯",',
    '    "shipfree": "📦", "warranty": "💳", "bogo": "🎯",\n'
    '    "treewater": "🌲", "treelights": "✨", "wrapcalc": "✂",')

P = []
d = {'slug': 'christmas-tree-water-calculator',
     'title': 'Christmas Tree Water Calculator - Quarts Per Day and Refill Schedule',
     'h1': 'Christmas Tree Water Calculator',
     'desc': 'Trunk diameter and stand size give the daily quarts your tree drinks, the refill interval, and the one dry-day rule that keeps the needles on. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'christmas tree water calculator how much water per day',
     'tool': 'treewater',
     'args': {},
     'intro': ["Measure the trunk diameter at the base, check how many quarts your stand holds, and rate the room warmth. The calculator gives the daily quarts, how often you will refill, and the season total - with the first-day double everyone learns the hard way.",
              "Care sheets wander; the rule that holds is one quart per inch of trunk per day. This one prices your room into it - hot rooms drink a third again - and repeats the only rule with real consequences: if the cut goes dry once, sap seals it and the tree never drinks again."],
     'howto': ["Measure trunk diameter across the base, not the branch spread.",
               "Find your stand capacity - usually printed on the bottom.",
               "Add the fresh cut at planting and never let the basin run dry."],
     'faqs': [("How much water does a Christmas tree need per day?",
               "About one quart per inch of trunk diameter daily - a 3-inch trunk drinks 3 quarts, doubled the first day. Warm rooms push it a third higher. The stand should never sit below the cut for even a day."),
              ("What happens if my Christmas tree runs dry?",
               "The cut end seals with sap within hours and the tree stops absorbing water permanently - no amount of refilling after that helps, and needle drop follows within days. It also turns the tree into a genuine fire hazard, which is why lights-off-when-out matters."),
              ("Should I cut the trunk before putting the tree in the stand?",
               "Yes - a fresh half-inch cut off the base opens the sap-clogged pores right before the stand. Do it at home the moment the tree arrives, then straight into water; the window matters more than the saw angle."),
              ("Do tree additives or sugar help?",
               "No - controlled tests keep finding plain water equal or better. The money goes on a stand with a real reservoir instead; the calculator sizes how big it needs to be for your trunk and your refill tolerance.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'christmas-tree-lights-calculator',
     'title': 'Christmas Tree Lights Calculator - How Many Strings Your Tree Takes',
     'h1': 'Christmas Tree Lights Calculator',
     'desc': 'Tree height, coverage style and bulb type give the total light count, strings to buy, watts and the season electricity bill. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'how many lights for christmas tree calculator strings per foot',
     'tool': 'treelights',
     'args': {},
     'intro': ["Set the tree height, pick a coverage style - 100 mini lights per foot is the classic, 50 sparse, 150 lush - and choose LED or incandescent. The calculator gives the bulb count, the 100-count strings to buy, the watts when lit, and the season electricity cost.",
              "Most light guides stop at the bulb count. This one finishes the job: watts and season dollars from the lights-cost math, the branch-wrap technique that beats circling the tree, and the one power strip that saves the midnight barefoot dash."],
     'howto': ["Height first - measure, do not guess the ceiling clearance.",
               "Pick coverage honestly; 100 per foot is already generous.",
               "Buy one extra string - dead bulbs are a December tradition."],
     'faqs': [("How many lights for a 6 foot Christmas tree?",
               "About 600 mini bulbs for classic coverage - six 100-count strings. Sparse styling takes 300, a lush showcase takes 900. The calculator scales it to your height and style."),
              ("How many lights per foot of Christmas tree?",
               "The classic rule is 100 mini lights per foot. Thin silhouettes sit at 50; magazine trees push 150-200. Beyond the count, depth matters more - lights woven toward the trunk read twice as bright as surface circles."),
              ("Do LED Christmas tree lights save money?",
               "Yes - mini LEDs draw about a tenth of the watts of incandescent minis, which over a 45-day season is a few dollars per tree. The bigger saving is longevity: LED strings last many seasons without the mid-December dead-string hunt."),
              ("What is the best way to put lights on a tree?",
               "Section by section, wrapping each major branch in a triangle from trunk to tip and back, bottom to top. Lights end up deep where they glow instead of skimming the surface, and one droopy section never unwinds the whole spiral.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'wrapping-paper-calculator',
     'title': 'Wrapping Paper Calculator - Rolls, Square Feet and Cost for Your Gifts',
     'h1': 'Wrapping Paper Calculator',
     'desc': 'Gift count, size and your honest wrapping style give the square feet of paper, rolls to buy and the cost - with the waste factor priced in. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'wrapping paper calculator how many rolls of wrapping paper',
     'tool': 'wrapcalc',
     'args': {},
     'intro': ["Count the gifts, pick the average size from book to awkward-giant, and rate your folding style - neat folds lose about a fifth of the roll, enthusiastic tape-and-hope loses a third. The calculator gives square feet, rolls and cost.",
              "Most roll guides assume perfect cuts and full coverage. This one prices the waste factor honestly - and offers the two real upgrades: kraft butcher paper with a stamp kit at a fraction of character-paper pricing, and gift bags as the buy-once, reuse-for-a-decade endgame."],
     'howto': ["Count every gift on the list, including the office extras.",
               "Size the biggest gift first - one giant always hides in the pile.",
               "Buy for the biggest, not the average; rounds go to the next full roll."],
     'faqs': [("How much wrapping paper do I need per gift?",
               "A book takes about a square foot, a sweater box around 3, a large toy 6 or more - then add the waste factor of your style, 20 to 50 percent. The calculator totals the whole list and rounds up to whole rolls."),
              ("How many gifts does one roll of wrapping paper cover?",
               "A standard 30-square-foot roll covers roughly 8-10 book-sized gifts or 2-3 sweater boxes once the off-cuts are counted. Awkward shapes eat roll fast, which is why the biggest gift sets the purchase."),
              ("Is expensive wrapping paper worth it?",
               "Rarely by the square foot - character and foil runs cost up to triple kraft paper for the same coverage. A kraft roll plus a stamp kit or twine reads intentional at a quarter of the price, and leftovers do not look like leftovers."),
              ("Are gift bags cheaper than wrapping paper?",
               "Per year, no; per decade, yes by a mile. Plain bags survive many seasons of reuse, skip the tape and measuring entirely, and end the folding style debate - the honest endgame for anyone who dreads the paper stage.")]}
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
print("R146 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
