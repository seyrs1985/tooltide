# -*- coding: utf-8 -*-
"""R150 冬日温暖三连:electric-blanket-cost(被窝电费)+coffee-ratio(粉水比)+sourdough-starter(酵种喂养)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: BLANKET ----------
Bl = 'BLANKET = """<div class="tool" id="tt-blk">\n'
Bl += '  <div class="fields">\n'
Bl += '    <div class="field"><label for="bk-w">Blanket wattage</label><select id="bk-w"><option value="60">60 W - throw</option><option value="100" selected>100 W - double</option><option value="180">180 W - king</option></select></div>\n'
Bl += '    <div class="field"><label for="bk-h">Hours per night</label><input id="bk-h" type="number" min="1" max="12" value="8"></div>\n'
Bl += '    <div class="field"><label for="bk-r">Price per kWh</label><input id="bk-r" type="number" min="0.03" step="0.01" value="0.17"></div>\n'
Bl += '    <div class="field"><label for="bk-n">Nights per season</label><input id="bk-n" type="number" min="10" max="240" value="120"></div>\n'
Bl += '  </div>\n'
Bl += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bk-out">&#8211;</span><span class="result-unit">per night of warmth</span></div>\n'
Bl += '  <div class="stats">\n'
Bl += '    <div class="stat"><b id="bk-s1">&#8211;</b><span>full season cost</span></div>\n'
Bl += '    <div class="stat"><b id="bk-s2">&#8211;</b><span>a 1500 W heater for the same hours</span></div>\n'
Bl += '    <div class="stat"><b id="bk-s3">&#8211;</b><span>ratio vs space heater</span></div>\n'
Bl += '  </div>\n'
Bl += '  <div class="tool-note" id="bk-note"></div>\n'
Bl += '  <button type="button" class="tool-btn" id="bk-share">Share my blanket math</button>\n'
Bl += '</div>\n'
Bl += '<script>(function(){\n'
Bl += "var W=document.getElementById('bk-w'),H=document.getElementById('bk-h'),R=document.getElementById('bk-r'),N=document.getElementById('bk-n');\n"
Bl += "function calc(){\n"
Bl += "  var w=parseFloat(W.value)||100,h=parseFloat(H.value)||8,r=parseFloat(R.value)||0.17,n=parseFloat(N.value)||120;\n"
Bl += "  var night=w*h/1000*r, season=night*n, heater=1500*h/1000*r;\n"
Bl += "  var d1=Math.round(night*100)/100, d2=Math.round(season*100)/100, d3=Math.round(heater*100)/100;\n"
Bl += "  var ratio=night>0?Math.round(heater/night):0;\n"
Bl += "  document.getElementById('bk-out').textContent='$'+d1;\n"
Bl += "  document.getElementById('bk-s1').textContent='$'+d2;\n"
Bl += "  document.getElementById('bk-s2').textContent='$'+d3;\n"
Bl += "  document.getElementById('bk-s3').textContent=ratio+'x cheaper';\n"
Bl += "  document.getElementById('bk-note').textContent='The verdict is not close: warming the bed costs a fraction of warming the room, because the blanket heats about two square metres and the heater fights the whole house. The honest pairing is both on a timer - heater for the evening wind-down in the living room, blanket for sleeping, thermostat down a few degrees overnight where the real savings live. Two safety notes that come free with the math: never leave a very old blanket switched on unattended, and fold it, never crease the wires when storing in spring.';\n"
Bl += "  document.title='Blanket: $'+d1+' per night - ToolDune';\n"
Bl += "}\n"
Bl += "function save(){try{localStorage.setItem('tt_blanket',JSON.stringify({w:W.value,h:H.value,r:R.value,n:N.value}));}catch(e){}}\n"
Bl += "[W,H,R,N].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Bl += "var pre=false;\n"
Bl += "var qs=new URLSearchParams(location.search);\n"
Bl += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Bl += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_blanket')||'null');if(m){if(m.w){W.value=m.w;}if(m.h){H.value=m.h;}if(m.r){R.value=m.r;}if(m.n){N.value=m.n;}}}catch(e){}}\n"
Bl += "calc();\n"
Bl += "document.getElementById('bk-share').addEventListener('click',function(){\n"
Bl += "  var txt='My heated blanket costs $'+document.getElementById('bk-out').textContent+' a night - '+document.getElementById('bk-s3').textContent+' than a space heater. Run yours:';\n"
Bl += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
Bl += "  if(navigator.share){navigator.share({title:'Heated blanket cost',text:txt,url:url}).catch(function(){});}\n"
Bl += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my blanket math';},1500);}\n"
Bl += "});\n"
Bl += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: COFFEERATIO ----------
Cr = 'COFFEERATIO = """<div class="tool" id="tt-cr">\n'
Cr += '  <div class="fields">\n'
Cr += '    <div class="field"><label for="cr-w">Water (ml)</label><input id="cr-w" type="number" min="50" max="5000" value="500"></div>\n'
Cr += '    <div class="field"><label for="cr-r">Brew ratio (coffee : water)</label><select id="cr-r"><option value="12">1:12 - strong / cold brew</option><option value="15">1:15 - bold filter</option><option value="16" selected>1:16 - classic</option><option value="17">1:17 - lighter</option></select></div>\n'
Cr += '  </div>\n'
Cr += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cr-out">&#8211;</span><span class="result-unit">grams of coffee</span></div>\n'
Cr += '  <div class="stats">\n'
Cr += '    <div class="stat"><b id="cr-s1">&#8211;</b><span>tablespoons, roughly</span></div>\n'
Cr += '    <div class="stat"><b id="cr-s2">&#8211;</b><span>cups of 250 ml</span></div>\n'
Cr += '    <div class="stat"><b id="cr-s3">&#8211;</b><span>per cup in the pot</span></div>\n'
Cr += '  </div>\n'
Cr += '  <div class="tool-note" id="cr-note"></div>\n'
Cr += '  <button type="button" class="tool-btn" id="cr-share">Share my brew ratio</button>\n'
Cr += '</div>\n'
Cr += '<script>(function(){\n'
Cr += "var W=document.getElementById('cr-w'),R=document.getElementById('cr-r');\n"
Cr += "function calc(){\n"
Cr += "  var w=parseFloat(W.value)||500,r=parseFloat(R.value)||16;\n"
Cr += "  var g=w/r, tbsp=g/5, cups=w/250, percup=(w/250)>0?g/(w/250):g;\n"
Cr += "  var d1=Math.round(g*10)/10, d2=Math.round(tbsp*10)/10, d3=Math.round(percup*10)/10;\n"
Cr += "  document.getElementById('cr-out').textContent=d1;\n"
Cr += "  document.getElementById('cr-s1').textContent='about '+d2;\n"
Cr += "  document.getElementById('cr-s2').textContent=(Math.round(cups*10)/10);\n"
Cr += "  document.getElementById('cr-s3').textContent=d3+' g';\n"
Cr += "  document.getElementById('cr-note').textContent='The ratio is the whole recipe: grams of coffee times sixteen is grams of water, and every pour-over chart is that line with opinion added. Weigh, do not scoop - a tablespoon of ground coffee can vary by half depending on grind, which is why volume brewing tastes different every morning. Bitter means grind finer or use cooler water, sour means grind coarser or brew longer; the ratio only sets the strength, the grind sets the mood. Change one variable at a time and keep the ratio - it turns guesswork into a dial.';\n"
Cr += "  document.title='Brew: '+d1+' g coffee for '+Math.round(w)+' ml - ToolDune';\n"
Cr += "}\n"
Cr += "function save(){try{localStorage.setItem('tt_coffeeratio',JSON.stringify({w:W.value,r:R.value}));}catch(e){}}\n"
Cr += "[W,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Cr += "var pre=false;\n"
Cr += "var qs=new URLSearchParams(location.search);\n"
Cr += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Cr += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_coffeeratio')||'null');if(m){if(m.w){W.value=m.w;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Cr += "calc();\n"
Cr += "document.getElementById('cr-share').addEventListener('click',function(){\n"
Cr += "  var txt='My brew: '+document.getElementById('cr-out').textContent+' g coffee for '+W.value+' ml at 1:'+R.value+'. Dial yours:';\n"
Cr += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
Cr += "  if(navigator.share){navigator.share({title:'Coffee ratio',text:txt,url:url}).catch(function(){});}\n"
Cr += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my brew ratio';},1500);}\n"
Cr += "});\n"
Cr += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: SOURDOUGH ----------
Sd = 'SOURDOUGH = """<div class="tool" id="tt-sd2">\n'
Sd += '  <div class="fields">\n'
Sd += '    <div class="field"><label for="sd-s">Starter you have (g)</label><input id="sd-s" type="number" min="10" max="1000" value="100"></div>\n'
Sd += '    <div class="field"><label for="sd-r">Feeding ratio (starter : flour : water)</label><select id="sd-r"><option value="1" selected>1:1:1 - daily maintenance</option><option value="2">1:2:2 - building up</option><option value="5">1:5:5 - slow, fridge-friendly</option></select></div>\n'
Sd += '  </div>\n'
Sd += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sd-out">&#8211;</span><span class="result-unit">flour to add (g)</span></div>\n'
Sd += '  <div class="stats">\n'
Sd += '    <div class="stat"><b id="sd-s1">&#8211;</b><span>water to add (g)</span></div>\n'
Sd += '    <div class="stat"><b id="sd-s2">&#8211;</b><span>total after feeding</span></div>\n'
Sd += '    <div class="stat"><b id="sd-s3">&#8211;</b><span>discard it creates</span></div>\n'
Sd += '  </div>\n'
Sd += '  <div class="tool-note" id="sd-note"></div>\n'
Sd += '  <button type="button" class="tool-btn" id="sd-share">Share my feeding math</button>\n'
Sd += '</div>\n'
Sd += '<script>(function(){\n'
Sd += "var S=document.getElementById('sd-s'),R=document.getElementById('sd-r');\n"
Sd += "function calc(){\n"
Sd += "  var st=parseFloat(S.value)||100, f=parseFloat(R.value)||1;\n"
Sd += "  var flour=st*f, water=st*f, total=st+flour+water;\n"
Sd += "  var d1=Math.round(flour), d2=Math.round(water), d3=Math.round(total);\n"
Sd += "  document.getElementById('sd-out').textContent=d1;\n"
Sd += "  document.getElementById('sd-s1').textContent=d2;\n"
Sd += "  document.getElementById('sd-s2').textContent=d3+' g';\n"
Sd += "  document.getElementById('sd-s3').textContent='keep '+Math.round(st)+' g only';\n"
Sd += "  document.getElementById('sd-note').textContent='Equal parts by weight is the whole grammar: keep some starter, feed it its own weight in flour and water, and it doubles in a warm kitchen in four to six hours. The 1:5:5 ratio is the fridge-lovers trick - a small spoon of starter swallows a big feed, buys you two or three quiet days, and keeps the jar from becoming a pumpkin. A starving starter smells of nail polish remover and splits into liquid on top; that is hunger, not death - feed it. And the discard jar is not waste: pancakes, crackers and focaccia all take it happily, which is the difference between a hobby and a flour bill.';\n"
Sd += "  document.title='Feed: '+d1+' g flour + '+d2+' g water - ToolDune';\n"
Sd += "}\n"
Sd += "function save(){try{localStorage.setItem('tt_sourdough',JSON.stringify({s:S.value,r:R.value}));}catch(e){}}\n"
Sd += "[S,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Sd += "var pre=false;\n"
Sd += "var qs=new URLSearchParams(location.search);\n"
Sd += "if(qs.get('s')){S.value=qs.get('s');pre=true;}\n"
Sd += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_sourdough')||'null');if(m){if(m.s){S.value=m.s;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Sd += "calc();\n"
Sd += "document.getElementById('sd-share').addEventListener('click',function(){\n"
Sd += "  var txt='Feeding my starter: '+document.getElementById('sd-out').textContent+' g flour + '+document.getElementById('sd-s1').textContent+' g water. Do yours:';\n"
Sd += "  var url=location.origin+location.pathname+'?s='+encodeURIComponent(S.value);\n"
Sd += "  if(navigator.share){navigator.share({title:'Sourdough feeding',text:txt,url:url}).catch(function(){});}\n"
Bl_dummy = None
Sd += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my feeding math';},1500);}\n"
Sd += "});\n"
Sd += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("BLANKET ", "COFFEERATIO ", "SOURDOUGH "):
    name2 = name.strip()
    src2 = io.open(TOOLS_P, encoding="utf-8").read()
    assert ("\n%s = " % name2) not in src2, name2 + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Bl + Cr + Sd + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "flydrive": lambda args: FLYDRIVE,',
    '    "flydrive": lambda args: FLYDRIVE,\n'
    '    "blanket": lambda args: BLANKET,\n'
    '    "coffeeratio": lambda args: COFFEERATIO,\n'
    '    "sourdough": lambda args: SOURDOUGH,')
sub(BUILD_P, '    "roadfuel": "🚙", "flydrive": "✈",',
    '    "roadfuel": "🚙", "flydrive": "✈",\n'
    '    "blanket": "🌙", "coffeeratio": "☕", "sourdough": "🍞",')

P = []
d = {'slug': 'electric-blanket-cost-calculator',
     'title': 'Electric Blanket Cost Calculator - Per Night and Season Electricity',
     'h1': 'Electric Blanket Cost Calculator',
     'desc': 'Blanket watts, hours and your rate give the per-night cost, the season total, and the ratio against a space heater - warm bed for pocket change. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'electric blanket cost calculator running cost per night',
     'tool': 'blanket',
     'args': {},
     'intro': ["Pick your blanket wattage - a throw runs about 60 W, a king 180 - set the hours and your electricity rate. The calculator gives the per-night cost, the whole winter total, and the ratio against running a 1500 W space heater for the same hours.",
              "The verdict is not close: the blanket heats two square metres of bed while the heater fights the whole room, and it shows in the numbers - roughly fifteen times cheaper per hour. The honest pairing is both on timers: heater for the evening, blanket for sleeping, thermostat down where the real savings live."],
     'howto': ["Find the wattage on the blanket label - controllers quote it too.",
               "Set realistic hours; most people run 8 with an auto-off.",
               "Compare against the space heater figure before touching the thermostat."],
     'faqs': [("How much does it cost to run an electric blanket?",
               "A 100 W double blanket for 8 hours costs about 14 cents at typical rates - roughly 16 dollars across a 120-night winter. The king size doubles it and still beats every other form of electric heat per hour of comfort."),
              ("Is an electric blanket cheaper than a space heater?",
               "By an order of magnitude per hour of personal warmth: the blanket heats the bed, the heater fights the whole room. The smart arrangement uses the heater for evening hours in the living space and the blanket overnight with the thermostat set lower."),
              ("Are old electric blankets safe?",
               "Replace any blanket over ten years old, or one with kinked wiring, scorch marks or a controller that smells warm. Modern units have auto-off timers and sensors; the fold-dont-crease storage rule is what keeps the internal wiring alive."),
              ("Does an electric blanket use a lot of electricity?",
               "Very little - it is a 60-180 W device, closer to a laptop charger than a heater. The season total for most users lands under a takeaway dinner, which is why the per-night figure surprises people in the good way.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'coffee-ratio-calculator',
     'title': 'Coffee Ratio Calculator - Grams of Coffee for Any Water Amount',
     'h1': 'Coffee Ratio Calculator',
     'desc': 'Water amount and brew ratio give exact coffee grams, the tablespoon equivalent and a per-cup breakdown - weigh once, dial forever. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'coffee ratio calculator grams of coffee per cup water',
     'tool': 'coffeeratio',
     'args': {},
     'intro': ["Enter your water in millilitres and pick a ratio - 1:16 is the classic filter strength, 1:15 bolder, 1:12 for cold brew concentration. The calculator gives grams of coffee, the rough tablespoon equivalent, and the per-cup breakdown.",
              "Every pour-over chart is one line with opinion added: grams of coffee times the ratio equals grams of water. This calculator is that line - plus the two honest notes that fix most bad cups: weigh, do not scoop, because a tablespoon varies by half with grind; and bitter versus sour is a grind-and-temperature dial, not a reason to touch the ratio."],
     'howto': ["Measure the water you actually brew, mug by mug.",
               "Pick 1:16 to start, then adjust strength in ratio steps of one.",
               "Change one variable at a time - ratio, grind, or temperature."],
     'faqs': [("What is the best coffee to water ratio?",
               "1:16 by weight is the universal starting point - 31 grams of coffee for 500 ml of water. Go 1:15 or 1:12 for stronger cups and cold brew, 1:17 for a lighter filter style; the best ratio is the one you stopped fiddling with."),
              ("How many tablespoons is 30 grams of coffee?",
               "Roughly six level tablespoons - but that is exactly why weighing wins: a tablespoon of coffee varies by up to half a gram-to-gram depending on grind size, while a 5 dollar scale is exact every morning."),
              ("Why does my coffee taste bitter or sour?",
               "Bitter means over-extraction - grind finer beans ground too fine, water too hot, or brew too long; go coarser or cooler. Sour means under-extraction - go finer or extend the brew. The ratio sets strength; grind sets the flavour faults."),
              ("How much coffee for 2 cups?",
               "Two 250 ml cups is 500 ml of water, which takes about 31 grams of coffee at 1:16 - the calculator splits it per cup so pot brewing and single cups stay consistent.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'sourdough-starter-calculator',
     'title': 'Sourdough Starter Feeding Calculator - Flour, Water and Discard',
     'h1': 'Sourdough Starter Feeding Calculator',
     'desc': 'Starter weight and feeding ratio give the exact flour and water to add, the jar total, and the discard it creates - maintenance, build-up and fridge ratios. Free.',
     'category': 'calculator',
     'keyword': 'sourdough starter feeding ratio calculator flour water',
     'tool': 'sourdough',
     'args': {},
     'intro': ["Weigh your starter and pick a feeding ratio: 1:1:1 for daily maintenance, 1:2:2 to build up for baking, 1:5:5 for the slow fridge rhythm. The calculator gives the flour and water to add, the jar total, and how much discard the feed implies.",
              "Starter guides drown beginners in lore. The grammar is equal parts by weight: feed it its own weight in flour and water and it doubles in four to six hours warm. The calculator also prices the parts nobody explains - the acetone smell is hunger not death, and the discard jar is a feature that pays for the flour."],
     'howto': ["Weigh the starter that stays in the jar - that number drives everything.",
               "Pick the ratio for your rhythm: daily, building, or fridge-slack.",
               "Mark the jar after feeding; the rise line tells you the truth."],
     'faqs': [("What is the best sourdough starter feeding ratio?",
               "1:1:1 (starter, flour, water by weight) for a daily room-temperature rhythm, 1:2:2 when building up for a bake, and 1:5:5 for fridge storage - the small-spoon-big-feed trick that buys two or three quiet days."),
              ("How much flour and water do I feed my starter?",
               "Exactly as much flour as starter, and the same again in water, at 1:1:1 - 100 g of starter takes 100 g of each and lands at 300 g. The calculator scales it to whatever is actually in your jar."),
              ("Why does my starter smell like acetone?",
               "It is starving, not dying: the acetone note and the liquid on top are hunger signals. Feed it promptly and it forgives completely - the starter that is truly beyond saving is the one with fuzzy mould, not the one that smells like a nail salon."),
              ("What do I do with sourdough discard?",
               "Keep a jar in the fridge and spend it: pancakes, crackers, waffles and focaccia all take unfed starter happily. The discard is the difference between feeding a hobby and composting money - the calculator shows exactly how much each feed creates.")]}
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
print("R150 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
