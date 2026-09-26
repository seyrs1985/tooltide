# -*- coding: utf-8 -*-
"""R126 首霜/入冬园艺簇:first-frost-planner + bulb-planting-calculator + christmas-cactus-bloom-planner
规则:JS 禁反斜杠u转义(R120)、模板与脚本注释零反斜杠序列(R121/R125)、emoji 老码位(U6.0)
"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"
NAMES = "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']"

F = 'FROSTPLAN = """<div class="tool" id="tt-ff">\n'
F += '  <div class="fields">\n'
F += '    <div class="field"><label for="ff-d">Your average first frost date</label><input type="date" id="ff-d" value="2026-10-15"></div>\n'
F += '  </div>\n'
F += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ff-out">&#8211;</span><span class="result-unit">until first frost</span></div>\n'
F += '  <div class="stats">\n'
F += '    <div class="stat"><b id="ff-s1">&#8211;</b><span>last feeding - 6 wk before</span></div>\n'
F += '    <div class="stat"><b id="ff-s2">&#8211;</b><span>tender pots inside - 4 wk</span></div>\n'
F += '    <div class="stat"><b id="ff-s3">&#8211;</b><span>final harvest - 2 wk</span></div>\n'
F += '  </div>\n'
F += '  <div class="tool-note" id="ff-note"></div>\n'
F += '  <button type="button" class="tool-btn" id="ff-share">Share my frost plan</button>\n'
F += '</div>\n'
F += '<script>(function(){\n'
F += "var D=document.getElementById('ff-d');\n"
F += "function calc(){\n"
F += "  var v=D.value;if(!v){return;}\n"
F += "  var p=v.split('-');\n"
F += "  var f=new Date(parseInt(p[0],10),parseInt(p[1],10)-1,parseInt(p[2],10));\n"
F += "  var now=new Date();var today=new Date(now.getFullYear(),now.getMonth(),now.getDate());\n"
F += "  if(f.getTime()<today.getTime()){f=new Date(f.getFullYear()+1,f.getMonth(),f.getDate());}\n"
F += "  var days=Math.round((f.getTime()-today.getTime())/86400000);\n"
F += "  var names=" + NAMES + ";\n"
F += "  function back(w){var t=new Date(f.getTime()-w*7*86400000);return names[t.getMonth()]+' '+t.getDate();}\n"
F += "  document.getElementById('ff-out').textContent=days+' days';\n"
F += "  document.getElementById('ff-s1').textContent=back(6);\n"
F += "  document.getElementById('ff-s2').textContent=back(4);\n"
F += "  document.getElementById('ff-s3').textContent=back(2);\n"
F += "  document.getElementById('ff-note').textContent='Six weeks out, stop fertilizing so new growth hardens instead of staying soft. Four weeks, bring tender pots inside after a pest check - a firm jet of water knocks aphids off the leaves. Two weeks, harvest the last tender vegetables and the basil. The final week, drain hoses, curl up the drip lines, and keep old sheets ready to throw over tender beds on frost nights. Your average first frost date comes from the weather service or a university extension table for your town; it is an average, so treat it as a drumbeat, not a cliff - the first frost often lands two weeks on either side.';\n"
F += "  document.title='First frost in '+days+' days - ToolDune';\n"
F += "}\n"
F += "function save(){try{localStorage.setItem('tt_frostplan',JSON.stringify({d:D.value}));}catch(e){}}\n"
F += "D.addEventListener('change',function(){calc();save();});\n"
F += "var pre=false;\n"
F += "var qs=new URLSearchParams(location.search);\n"
F += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
F += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_frostplan')||'null');if(m&&m.d){D.value=m.d;pre=true;}}catch(e){}}\n"
F += "calc();\n"
F += "document.getElementById('ff-share').addEventListener('click',function(){\n"
F += "  var txt='First frost: '+D.value+', '+document.getElementById('ff-out').textContent+' out. Pots come in on '+document.getElementById('ff-s2').textContent+'. Plan your winterizing:';\n"
F += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
F += "  if(navigator.share){navigator.share({title:'First frost plan',text:txt,url:url}).catch(function(){});}\n"
F += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my frost plan';},1500);}\n"
F += "});\n"
F += "})();\n</script>\n\"\"\"\n\n"

B = 'BULBSPACE = """<div class="tool" id="tt-bl">\n'
B += '  <div class="fields">\n'
B += '    <div class="field"><label for="bl-l">Bed length (ft)</label><input type="number" id="bl-l" min="1" max="100" step="0.5" placeholder="8"></div>\n'
B += '    <div class="field"><label for="bl-w">Bed width (ft)</label><input type="number" id="bl-w" min="0.5" max="50" step="0.5" placeholder="4"></div>\n'
B += '    <div class="field"><label for="bl-t">Bulb type</label><select id="bl-t"><option value="tulip" selected>Tulip</option><option value="daffodil">Daffodil</option><option value="crocus">Crocus</option><option value="allium">Allium</option><option value="hyacinth">Hyacinth</option></select></div>\n'
B += '  </div>\n'
B += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bl-out">&#8211;</span><span class="result-unit">bulbs to buy</span></div>\n'
B += '  <div class="stats">\n'
B += '    <div class="stat"><b id="bl-s1">&#8211;</b><span>packs of 25</span></div>\n'
B += '    <div class="stat"><b id="bl-s2">&#8211;</b><span>planting depth</span></div>\n'
B += '    <div class="stat"><b id="bl-s3">&#8211;</b><span>spacing apart</span></div>\n'
B += '  </div>\n'
B += '  <div class="tool-note" id="bl-note"></div>\n'
B += '  <button type="button" class="tool-btn" id="bl-share">Share my bulb order</button>\n'
B += '</div>\n'
B += '<script>(function(){\n'
B += "var L=document.getElementById('bl-l'),W=document.getElementById('bl-w'),T=document.getElementById('bl-t');\n"
B += "var SP={tulip:[4,6],daffodil:[4,6],crocus:[3,3],allium:[8,6],hyacinth:[4,6]};\n"
B += "function calc(){\n"
B += "  var l=parseFloat(L.value)||0,w=parseFloat(W.value)||0;\n"
B += "  if(l<1){l=1;}if(w<0.5){w=0.5;}\n"
B += "  var s=SP[T.value];\n"
B += "  var per=144/(s[0]*s[0]);\n"
B += "  var count=Math.ceil(l*w*per);\n"
B += "  document.getElementById('bl-out').textContent=count;\n"
B += "  document.getElementById('bl-s1').textContent=Math.ceil(count/25);\n"
B += "  document.getElementById('bl-s2').textContent=s[1]+' in';\n"
B += "  document.getElementById('bl-s3').textContent=s[0]+' in';\n"
B += "  document.getElementById('bl-note').textContent='The arithmetic: bulbs per square foot from the spacing squared, bed area times that, rounded up because bulbs sell in packs. Plant at the depth shown - the classic rule is two to three times the bulb height - pointy end up. In warm climates tulips need 12 to 16 weeks in the refrigerator before planting; daffodils are the one bulb squirrels leave alone. October is prime time while the soil is still workable - bulbs want about six weeks of root growth before the ground freezes solid.';\n"
B += "  document.title=count+' bulbs for your bed - ToolDune';\n"
B += "}\n"
B += "function save(){try{localStorage.setItem('tt_bulbspace',JSON.stringify({l:L.value,w:W.value,t:T.value}));}catch(e){}}\n"
B += "L.addEventListener('input',function(){calc();save();});W.addEventListener('input',function(){calc();save();});T.addEventListener('change',function(){calc();save();});\n"
B += "var pre=false;\n"
B += "var qs=new URLSearchParams(location.search);\n"
B += "if(qs.get('l')){L.value=qs.get('l');pre=true;}\n"
B += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
B += "if(qs.get('t')){T.value=qs.get('t');pre=true;}\n"
B += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_bulbspace')||'null');if(m){if(m.l){L.value=m.l;}if(m.w){W.value=m.w;}if(m.t){T.value=m.t;}pre=true;}}catch(e){}}\n"
B += "calc();\n"
B += "document.getElementById('bl-share').addEventListener('click',function(){\n"
B += "  var txt='The '+L.value+' by '+W.value+' ft bed takes '+document.getElementById('bl-out').textContent+' '+T.value+' bulbs. Plan yours:';\n"
B += "  var url=location.origin+location.pathname+'?l='+encodeURIComponent(L.value)+'&w='+encodeURIComponent(W.value)+'&t='+encodeURIComponent(T.value);\n"
B += "  if(navigator.share){navigator.share({title:'Bulb planting plan',text:txt,url:url}).catch(function(){});}\n"
B += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my bulb order';},1500);}\n"
B += "});\n"
B += "})();\n</script>\n\"\"\"\n\n"

C = 'CACTUSBLOOM = """<div class="tool" id="tt-cb">\n'
C += '  <div class="fields">\n'
C += '    <div class="field"><label for="cb-d">Want blooms by</label><input type="date" id="cb-d" value="2026-12-25"></div>\n'
C += '  </div>\n'
C += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cb-out">&#8211;</span><span class="result-unit">start long nights</span></div>\n'
C += '  <div class="stats">\n'
C += '    <div class="stat"><b id="cb-s1">&#8211;</b><span>days from today</span></div>\n'
C += '    <div class="stat"><b id="cb-s2">&#8211;</b><span>weeks of the treatment</span></div>\n'
C += '    <div class="stat"><b id="cb-s3">&#8211;</b><span>total darkness per night</span></div>\n'
C += '  </div>\n'
C += '  <div class="tool-note" id="cb-note"></div>\n'
C += '  <button type="button" class="tool-btn" id="cb-share">Share my bloom plan</button>\n'
C += '</div>\n'
C += '<script>(function(){\n'
C += "var D=document.getElementById('cb-d');\n"
C += "function calc(){\n"
C += "  var v=D.value;if(!v){return;}\n"
C += "  var p=v.split('-');\n"
C += "  var t=new Date(parseInt(p[0],10),parseInt(p[1],10)-1,parseInt(p[2],10));\n"
C += "  var now=new Date();var today=new Date(now.getFullYear(),now.getMonth(),now.getDate());\n"
C += "  if(t.getTime()<today.getTime()+56*86400000){t=new Date(t.getFullYear()+1,t.getMonth(),t.getDate());}\n"
C += "  var st=new Date(t.getTime()-56*86400000);\n"
C += "  var days=Math.round((st.getTime()-today.getTime())/86400000);\n"
C += "  var names=" + NAMES + ";\n"
C += "  var sd=names[st.getMonth()]+' '+st.getDate();\n"
C += "  document.getElementById('cb-out').textContent=sd;\n"
C += "  document.getElementById('cb-s1').textContent=days;\n"
C += "  document.getElementById('cb-s2').textContent='8';\n"
C += "  document.getElementById('cb-s3').textContent='13 h';\n"
C += "  document.getElementById('cb-note').textContent='Count back eight weeks from your target and run long nights from that date: 13 hours of total darkness every night - a closet, a spare room, or a cardboard box over the plant - with bright days, cool nights between 13 and 18 C, and water only when the top inch of soil dries. Buds appear around week four, tiny beads at the branch tips. Once buds are pea size, move the plant to a bright window and stop moving it altogether: a turned pot drops buds, and a kitchen with evening lights is the classic bloom killer.';\n"
C += "  document.title='Start dark nights on '+sd+' - ToolDune';\n"
C += "}\n"
C += "function save(){try{localStorage.setItem('tt_cactusbloom',JSON.stringify({d:D.value}));}catch(e){}}\n"
C += "D.addEventListener('change',function(){calc();save();});\n"
C += "var pre=false;\n"
C += "var qs=new URLSearchParams(location.search);\n"
C += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
C += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_cactusbloom')||'null');if(m&&m.d){D.value=m.d;pre=true;}}catch(e){}}\n"
C += "calc();\n"
C += "document.getElementById('cb-share').addEventListener('click',function(){\n"
C += "  var txt='For blooms by '+D.value+', the long-night treatment starts '+document.getElementById('cb-out').textContent+' - 13 h of darkness a night for 8 weeks. Plan yours:';\n"
C += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
C += "  if(navigator.share){navigator.share({title:'Christmas cactus bloom plan',text:txt,url:url}).catch(function(){});}\n"
C += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my bloom plan';},1500);}\n"
C += "});\n"
C += "})();\n</script>\n\"\"\"\n\n"

def sub(path, old, new, n=1):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    assert s.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    s = s.replace(old, new)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)

TOOLS_P = BASE + r"\tools.py"
PAGES_P = BASE + r"\pages.py"
BUILD_P = BASE + r"\build.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', F + B + C + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "tailgatefood": lambda args: TGFOOD,',
    '    "tailgatefood": lambda args: TGFOOD,\n'
    '    "frostplan": lambda args: FROSTPLAN,\n'
    '    "bulbspace": lambda args: BULBSPACE,\n'
    '    "cactusbloom": lambda args: CACTUSBLOOM,')
sub(BUILD_P, '    "coolice": "\U0001F379", "tailgatefood": "\U0001F356",',
    '    "coolice": "\U0001F379", "tailgatefood": "\U0001F356",\n'
    '    "frostplan": "\u2744", "bulbspace": "\U0001F337", "cactusbloom": "\U0001F335",')

P = []
d1 = {'slug': 'first-frost-planner',
      'title': 'First Frost Planner - Winterize Schedule Working Back from Your Date',
      'h1': 'First Frost Planner',
      'desc': 'Enter your average first frost date and get the winterizing schedule working backward: last feeding, tender pots inside, final harvest, hose drain and frost-night covers. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'average first frost date 2026 when to bring plants inside fall',
      'tool': 'frostplan',
      'args': {},
      'intro': ["Enter the average first frost date for your town - the weather service and university extension tables publish one for everywhere - and this planner works backward from it: when to stop feeding, when tender pots come inside, when to make the final harvest, and what to do the last week.",
               "Frost maps stop at the date and leave the work to guesswork. The date is only a drumbeat; the gardening is in the weeks before it, and every chore here has a reason - fertilizer feeds soft growth frost will kill, and the aphids on that pot ride indoors unless evicted first."],
      'howto': ["Look up your average first frost date and enter it - the planner rolls to next year once the date passes.",
                "Put the three dates on your calendar; they are the whole job, weeks ahead of the cold.",
                "Keep old sheets by the door for frost nights - covers buy tender beds two or three degrees."],
      'faqs': [("When should I bring potted plants inside for winter?", "About four weeks before your average first frost - tender houseplants and tropicals stress when nights dip under 10 C. Earlier matters more than the date: a pest inspection and a water blast before the pot crosses the doorstep is what keeps your indoor collection clean."),
               ("What is an average first frost date?", "It is the long-run calendar date where frost has a 50 percent chance of having occurred by then - not a promise. Treat the date as a planning drumbeat; the actual first frost commonly lands within two weeks either side, which is why covers stay by the door."),
               ("When do I stop fertilizing in fall?", "Six weeks before first frost outdoors. Feeding pushes soft new growth that the first frost kills, wasting stored energy - the goal of late season is hardening, not growing. Houseplants coming indoors simply stop being fed until late winter."),
               ("What vegetables survive a light frost?", "Hardy crops - kale, cabbage, carrots, parsnips - improve after a light frost as starches turn to sugar. The tender list is the one the planner harvests two weeks out: basil, beans, cucumbers, peppers, tomatoes. One night at minus 1 C ends all of them.")]}
P.append("    pages.append(%r)\n" % (d1,))

d2 = {'slug': 'bulb-planting-calculator',
      'title': 'Bulb Planting Calculator - How Many Bulbs Fit Your Bed',
      'h1': 'Bulb Planting Calculator',
      'desc': 'How many tulip or daffodil bulbs for your bed? Bed size times spacing gives the count, packs of 25 to buy, planting depth and spacing by bulb type. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'how many tulip bulbs per square foot bulb spacing depth calculator',
      'tool': 'bulbspace',
      'args': {},
      'intro': ["Enter your bed length and width, pick the bulb, and get the count to buy - bulbs per square foot from the spacing chart, packs of 25 rounded up, plus the planting depth and spacing for that bulb.",
               "Planting charts answer per bulb; nobody plants one bulb. The real question at the garden centre till is how many bags a bed actually takes - and the honest answer comes from area arithmetic, not the optimistic picture on the bag."],
      'howto': ["Measure the bed length and width in feet - drifts and borders, not single rows.",
                "Pick the bulb type; the chart carries depth and spacing for the five classics.",
                "Buy the pack count, plant pointy end up at the depth shown, and water once."],
      'faqs': [("How many tulip bulbs per square foot?", "About nine at the standard 4 inch spacing - a 4 by 8 bed takes roughly 290, or 12 packs of 25. Crowd them to 3 inch spacing for a dense display and the same bed wants 12 per square foot, but drainage and bulb food suffer in year two."),
               ("How deep should I plant bulbs?", "Two to three times the bulb height: tulips and daffodils 6 inches, crocus 3, giant alliums 6 with 8 inch spacing. Too shallow and frost heaves them; too deep and the shoot spends its budget getting to daylight."),
               ("Do tulips need chilling before planting?", "In warm climates yes - 12 to 16 weeks in the refrigerator, away from ripening fruit, because a tulip without its winter never forms a proper stem and blooms at knee height on a flop. Daffodils and crocus shrug off the lack."),
               ("When should I plant fall bulbs?", "October into November while soil is still workable - bulbs root best in cool soil and want roughly six weeks before the ground freezes. Planting into warm September soil invites rot; planting after freeze-up buries the season.")]}
P.append("    pages.append(%r)\n" % (d2,))

d3 = {'slug': 'christmas-cactus-bloom-planner',
      'title': 'Christmas Cactus Bloom Planner - Start Long Nights 8 Weeks Before',
      'h1': 'Christmas Cactus Bloom Planner',
      'desc': 'Why is your Christmas cactus not blooming? Pick a target date and get the night to start the 13-hour darkness treatment, cool nights and dry watering that force buds. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'christmas cactus not blooming how to get blooms dark treatment weeks',
      'tool': 'cactusbloom',
      'args': {},
      'intro': ["Pick the date you want flowers - Christmas Day by default - and the planner counts back eight weeks to the night the long-dark treatment starts, with the three rules that actually move buds: 13 hours of total darkness, cool nights, and water only when dry.",
               "The internet blames fertilizer for a budless cactus. Bloom here is triggered by night length and temperature - a photoperiod plant, same machinery as poinsettias - so the fix is a closet schedule, and the date arithmetic is the part everyone misses."],
      'howto': ["Enter your target bloom date; the planner hands the start night, rolling to next year if the window is gone.",
                "From that night: 13 hours of unbroken darkness daily, cool nights, dry-ish watering, for eight weeks.",
                "At pea-size buds, move to a bright window and never move the pot again."],
      'faqs': [("Why is my Christmas cactus not blooming?", "Almost always light at night - a kitchen or living room used after dark gives the plant a summer that never ends. Thirteen hours of true darkness for eight weeks, with nights under 18 C, is the trigger; feed and repotting are side characters."),
               ("How long is the Christmas cactus dark treatment?", "Eight weeks of 13-hour nights, though buds often show by week four. Unbroken matters - even a lamp switched on for a minute resets the clock, which is why a closet or a cardboard box beats a dim corner."),
               ("When do buds appear on a Christmas cactus?", "Around four weeks into the treatment, as beads at the branch tips. From bud set onward the job changes: bright light, steady position, even watering - and no rotating the pot, which is the classic cause of buds dropping before they open."),
               ("What temperature makes a Christmas cactus bloom?", "Cool nights between 13 and 18 C do half the work - a plant on a warm windowsill with a radiator below can get perfect darkness and still stay green. Cool, dark and dry is the whole recipe; the flowers are the plant deciding winter came.")]}
P.append("    pages.append(%r)\n" % (d3,))

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
print("R126 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
