# -*- coding: utf-8 -*-
"""R122 南瓜簇:pumpkin-pie-calculator / pumpkin-carving-timing / pumpkin-seeds-roast-calculator
全程真实 emoji,JS 字符串零撇号,repr 生成 pages 条目。"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

PP = 'PUMPKINPIE = """<div class="tool" id="tt-ppie">\n'
PP += '  <div class="fields">\n'
PP += '    <div class="field"><label for="ppie-g">Guests</label><input type="number" id="ppie-g" min="1" max="200" step="1" placeholder="10"></div>\n'
PP += '    <div class="field"><label for="ppie-s">Slices per guest</label><select id="ppie-s"><option value="1" selected>1 slice (polite)</option><option value="1.5">1.5 slices (holiday)</option><option value="2">2 slices (seconds expected)</option></select></div>\n'
PP += '  </div>\n'
PP += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ppie-out">&#8211;</span><span class="result-unit">9-inch pies</span></div>\n'
PP += '  <div class="stats">\n'
PP += '    <div class="stat"><b id="ppie-s1">&#8211;</b><span>cups of puree</span></div>\n'
PP += '    <div class="stat"><b id="ppie-s2">&#8211;</b><span>15-oz cans</span></div>\n'
PP += '    <div class="stat"><b id="ppie-s3">&#8211;</b><span>eggs + sugar (cups)</span></div>\n'
PP += '  </div>\n'
PP += '  <div class="tool-note" id="ppie-note"></div>\n'
PP += '  <button type="button" class="tool-btn" id="ppie-share">Share the pie math</button>\n'
PP += '</div>\n'
PP += '<script>(function(){\n'
PP += "var G=document.getElementById('ppie-g'),S=document.getElementById('ppie-s');\n"
PP += "function calc(){\n"
PP += "  var g=parseFloat(G.value),sp=parseFloat(S.value);\n"
PP += "  if(!(g>0)){return;}\n"
PP += "  var slices=g*sp, pies=Math.ceil(slices/8), cups=pies*2, cans=Math.ceil(cups/1.75);\n"
PP += "  document.getElementById('ppie-out').textContent=pies;\n"
PP += "  document.getElementById('ppie-s1').textContent=cups;\n"
PP += "  document.getElementById('ppie-s2').textContent=cans;\n"
PP += "  document.getElementById('ppie-s3').textContent=pies*2+' + '+pies*0.75;\n"
PP += "  document.getElementById('ppie-note').textContent='One 9-inch pie feeds 8 polite slices, needs 2 cups of puree, 2 eggs, 3/4 cup sugar and 1 cup evaporated milk. A 15-oz can holds about 1.75 cups, so the can count rounds up - leftover puree freezes fine. Buy baking pumpkins, not carving ones: a 3-4 lb sugar pumpkin roasts down to roughly 2 cups with better flavor, but canned puree has standardized moisture and is the honest choice for first-timers - a watery filling is the number one soggy-crust cause.';\n"
PP += "  document.title=pies+' pies - Pumpkin Pie Calculator - ToolDune';\n"
PP += "}\n"
PP += "function save(){try{localStorage.setItem('tt_ppie',JSON.stringify({g:G.value,s:S.value}));}catch(e){}}\n"
PP += "G.addEventListener('input',function(){calc();save();});S.addEventListener('change',function(){calc();save();});\n"
PP += "var pre=false;\n"
PP += "var q=new URLSearchParams(location.search).get('g');\n"
PP += "if(q){G.value=q;pre=true;}\n"
PP += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_ppie')||'null');if(m&&m.g){G.value=m.g;S.value=m.s||S.value;pre=true;}}catch(e){}}\n"
PP += "calc();\n"
PP += "document.getElementById('ppie-share').addEventListener('click',function(){\n"
PP += "  var txt=G.value+' guests need '+document.getElementById('ppie-out').textContent+' pumpkin pies ('+document.getElementById('ppie-s2').textContent+' cans of puree). Plan yours:';\n"
PP += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value);\n"
PP += "  if(navigator.share){navigator.share({title:'Pumpkin pie math',text:txt,url:url}).catch(function(){});}\n"
PP += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share the pie math';},1500);}\n"
PP += "});\n"
PP += "})();\n</script>\n\"\"\"\n\n"

CV = 'CARVETIMING = """<div class="tool" id="tt-carve">\n'
CV += '  <div class="fields">\n'
CV += '    <div class="field"><label for="carve-m">Preservation method</label><select id="carve-m"><option value="4">None - leave it be</option><option value="6">Petroleum jelly on cuts</option><option value="5">Bleach-water spray</option><option value="7">Fridge nights, porch days</option></select></div>\n'
CV += '  </div>\n'
CV += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="carve-out">&#8211;</span><span class="result-unit">is your carving day</span></div>\n'
CV += '  <div class="stats">\n'
CV += '    <div class="stat"><b id="carve-s1">&#8211;</b><span>days fresh once cut</span></div>\n'
CV += '    <div class="stat"><b id="carve-s2">&#8211;</b><span>days until Halloween</span></div>\n'
CV += '    <div class="stat"><b id="carve-s3">&#8211;</b><span>if carved today</span></div>\n'
PP0 = '  </div>\n'
CV += PP0
CV += '  <div class="tool-note" id="carve-note"></div>\n'
CV += '  <button type="button" class="tool-btn" id="carve-share">Share my carving date</button>\n'
CV += '</div>\n'
CV += '<script>(function(){\n'
CV += "var M=document.getElementById('carve-m');\n"
CV += "function calc(){\n"
CV += "  var fresh=parseFloat(M.value),now=new Date(),y=now.getUTCFullYear();\n"
CV += "  var hall=new Date(Date.UTC(y,9,31));\n"
CV += "  if(now.getTime()>hall.getTime()){hall=new Date(Date.UTC(y+1,9,31));}\n"
CV += "  var days=Math.ceil((hall.getTime()-now.getTime())/86400000);\n"
CV += "  var carve=new Date(hall.getTime()-fresh*86400000);\n"
CV += "  var names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];\n"
CV += "  var cs=names[carve.getUTCMonth()]+' '+carve.getUTCDate();\n"
CV += "  document.getElementById('carve-out').textContent=cs;\n"
CV += "  document.getElementById('carve-s1').textContent='about '+fresh;\n"
CV += "  document.getElementById('carve-s2').textContent=days;\n"
CV += "  document.getElementById('carve-s3').textContent=days>fresh?'too early':'go tonight';\n"
CV += "  document.getElementById('carve-note').textContent='A carved pumpkin is produce, not a prop: cut faces dry, sag and grow fuzz within days, and every method here stretches rather than immortalizes - the fridge-night rhythm is the strongest, petroleum jelly seals moisture into the cuts, bleach spray slows the fuzz but washes off in rain. Whole uncarved pumpkins hold for weeks on a cool porch, so the honest strategy is buy late, carve on the date above, and keep the lid on when the Jack-o-lantern is not on duty.';\n"
CV += "  document.title='Carve on '+cs+' - ToolDune';\n"
CV += "}\n"
CV += "function save(){try{localStorage.setItem('tt_carve',M.value);}catch(e){}}\n"
CV += "M.addEventListener('change',function(){calc();save();});\n"
CV += "var pre=false;\n"
CV += "var q=new URLSearchParams(location.search).get('m');\n"
CV += "if(q){M.value=q;pre=true;}\n"
CV += "if(!pre){try{var m=localStorage.getItem('tt_carve');if(m){M.value=m;pre=true;}}catch(e){}}\n"
CV += "calc();\n"
CV += "document.getElementById('carve-share').addEventListener('click',function(){\n"
CV += "  var txt='Carve the Jack-o-lantern on '+document.getElementById('carve-out').textContent+' so it is fresh for Halloween. Plan yours:';\n"
CV += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value);\n"
CV += "  if(navigator.share){navigator.share({title:'Pumpkin carving timing',text:txt,url:url}).catch(function(){});}\n"
CV += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my carving date';},1500);}\n"
CV += "});\n"
CV += "})();\n</script>\n\"\"\"\n\n"

SD = 'SEEDSROAST = """<div class="tool" id="tt-pseed">\n'
SD += '  <div class="fields">\n'
SD += '    <div class="field"><label for="pseed-w">Pumpkin weight (lbs)</label><input type="number" id="pseed-w" min="1" max="60" step="0.5" placeholder="5"></div>\n'
SD += '    <div class="field"><label for="pseed-r">Electricity... just kidding - oven type</label><select id="pseed-r"><option value="300" selected>300 F - slow and even</option><option value="350">350 F - faster, less even</option></select></div>\n'
SD += '  </div>\n'
SD += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pseed-out">&#8211;</span><span class="result-unit">cups of seeds</span></div>\n'
SD += '  <div class="stats">\n'
SD += '    <div class="stat"><b id="pseed-s1">&#8211;</b><span>snack servings</span></div>\n'
SD += '    <div class="stat"><b id="pseed-s2">&#8211;</b><span>roast minutes</span></div>\n'
SD += '    <div class="stat"><b id="pseed-s3">&#8211;</b><span>oil + salt</span></div>\n'
SD += '  </div>\n'
SD += '  <div class="tool-note" id="pseed-note"></div>\n'
SD += '  <button type="button" class="tool-btn" id="pseed-share">Share the seed math</button>\n'
SD += '</div>\n'
SD += '<script>(function(){\n'
SD += "var W=document.getElementById('pseed-w'),T=document.getElementById('pseed-r');\n"
SD += "function calc(){\n"
SD += "  var w=parseFloat(W.value),t=parseInt(T.value,10);\n"
SD += "  if(!(w>0)){return;}\n"
SD += "  var cups=w*0.15, serv=Math.floor(cups/0.25), mins=t===300?'30-35':'22-28';\n"
SD += "  document.getElementById('pseed-out').textContent=(Math.round(cups*100)/100);\n"
SD += "  document.getElementById('pseed-s1').textContent=serv;\n"
SD += "  document.getElementById('pseed-s2').textContent=mins;\n"
SD += "  document.getElementById('pseed-s3').textContent=Math.ceil(cups)+' tbsp + pinch';\n"
SD += "  document.getElementById('pseed-note').textContent='Yield rule of thumb: about a quarter cup of seeds per pumpkin pound, cleaned and dried. The step most recipes skip and the difference it makes: simmer the clean seeds 10 minutes in salted water, drain and dry overnight if you can - they crisp evenly instead of steaming. Toss with a tablespoon of oil and a pinch of salt per cup, single layer, and stir once mid-roast. Carve-pumpkin seeds and sugar-pumpkin seeds roast the same; the pumpkin does not care about its purpose.';\n"
SD += "  document.title=Math.round(cups*100)/100+' cups - Pumpkin Seeds - ToolDune';\n"
SD += "}\n"
SD += "function save(){try{localStorage.setItem('tt_pseed',JSON.stringify({w:W.value,r:T.value}));}catch(e){}}\n"
SD += "W.addEventListener('input',function(){calc();save();});T.addEventListener('change',function(){calc();save();});\n"
SD += "var pre=false;\n"
SD += "var q=new URLSearchParams(location.search).get('w');\n"
SD += "if(q){W.value=q;pre=true;}\n"
SD += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_pseed')||'null');if(m&&m.w){W.value=m.w;T.value=m.r||T.value;pre=true;}}catch(e){}}\n"
SD += "calc();\n"
SD += "document.getElementById('pseed-share').addEventListener('click',function(){\n"
SD += "  var txt='A '+W.value+'-lb pumpkin yields about '+document.getElementById('pseed-out').textContent+' cups of seeds - roast at '+T.value+' F. Do your own:';\n"
SD += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
SD += "  if(navigator.share){navigator.share({title:'Pumpkin seed math',text:txt,url:url}).catch(function(){});}\n"
SD += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share the seed math';},1500);}\n"
SD += "});\n"
SD += "})();\n</script>\n\"\"\"\n\n"

BLOCK = PP + CV + SD

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

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', BLOCK + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "seasoning": lambda args: SEASONING,',
    '    "seasoning": lambda args: SEASONING,\n'
    '    "pumpkinpie": lambda args: PUMPKINPIE,\n'
    '    "carvetiming": lambda args: CARVETIMING,\n'
    '    "seedroast": lambda args: SEEDSROAST,')
sub(BUILD_P, '    "firewood": "🔥", "firepitvs": "♨️", "seasoning": "🌲",',
    '    "firewood": "🔥", "firepitvs": "♨️", "seasoning": "🌲",\n'
    '    "pumpkinpie": "🎃", "carvetiming": "🍂", "seedroast": "🌰",')

P = []
def page(slug, title, h1, desc, kw, tool, i1, i2, h1s, h2s, h3s, faqs):
    d = {'slug': slug, 'title': title, 'h1': h1, 'desc': desc, 'category': 'calculator',
         'keyword': kw, 'tool': tool, 'args': {}, 'intro': [i1, i2],
         'howto': [h1s, h2s, h3s], 'faqs': faqs}
    P.append("    pages.append(%r)\n" % (d,))

page("pumpkin-pie-calculator",
     "Pumpkin Pie Calculator - How Many Pies for Your Guests",
     "Pumpkin Pie Calculator",
     "Enter guests and appetite to get pies, cups of puree, 15-oz cans, eggs and sugar - the full shopping math for one 9-inch pie feeding eight. Free, instant, no signup.",
     "pumpkin pie calculator how many pies per guest thanksgiving",
     "pumpkinpie",
     "Enter how many guests and how generous your slices are, and this calculator converts it to the shopping list: pies, cups of puree, 15-oz cans, eggs and sugar, all from one standard recipe - a 9-inch pie feeds eight polite slices and drinks 2 cups of puree. The slice slider settles the eternal holiday argument between one polite slice and seconds.",
     "Most pie pages give one recipe and wish you luck scaling it; the classic failure is eleven guests and two pies where one would do, or one can short on the morning of. This page does the arithmetic both directions and says plainly which pumpkin to buy: baking sugar pumpkins roast down to better flavor, but canned puree has standardized moisture and is the reliable pick for a first crust.",
     "Enter your guest count.", "Pick the slice generosity - the slider is the honesty control.", "Read pies, cans and the rest of the shopping list.",
     [("How many people does a pumpkin pie feed?", "One 9-inch pie cuts into 8 polite slices; the slider lets you budget 1.5 or 2 slices per guest for holiday appetites, which is usually the safer plan."),
      ("How much puree is in a 15-oz can?", "About 1.75 cups, and one 9-inch pie needs 2 cups - so one can plus a little fresh roasted, or round up cans; leftover puree freezes well for the next batch."),
      ("Can I use a carving pumpkin for pie?", "Technically yes, but flavor and texture lose: buy small baking (sugar) pumpkins, 3-4 lbs each, which roast down to about 2 cups of denser, sweeter flesh than a stringy jack-o-lantern."),
      ("Why is my pumpkin pie filling soggy or watery?", "Usually moisture: canned puree is standardized, fresh roasted varies a lot - strain fresh puree through a cloth, and pre-bake or blind-bake the crust so the filling does not soak it.")])

page("pumpkin-carving-timing",
     "Pumpkin Carving Timing - The Right Day for a Fresh Jack-o-Lantern",
     "Pumpkin Carving Timing",
     "Carve too early and your Jack-o-lantern sags by Halloween. Pick your preservation method and get the carving date that keeps it fresh for the night that matters.",
     "when to carve pumpkins how early can you carve halloween",
     "carvetiming",
     "A carved pumpkin is produce with a countdown: left alone it holds about four days once cut, petroleum jelly on the cuts stretches it toward six, a bleach-water spray buys five, and the porch-days fridge-nights rhythm is the strongest at about seven. Enter your method and this planner works backward from October 31 to give you the carving date - plus whether carving today is commitment or mistake.",
     "The internet says carve whenever; produce says otherwise, and every year the sad ones prove it. This page treats the Jack-o-lantern as what it is - a cut vegetable on a porch - gives each preservation folk method its honest stretch, and answers the question people actually search the week before Halloween: not how to carve, but when.",
     "Pick your preservation method - be honest about your discipline.", "Read your carving date, worked back from Halloween.", "Carve on the date, keep the lid on between shows.",
     [("When should I carve my pumpkin for Halloween?", "Work backward from your freshness window: with no treatment, carve about 4 days before Halloween; with the fridge-night method, up to a week. The calculator gives your date from the method you will actually keep up."),
      ("How do I make a carved pumpkin last longer?", "The strongest routine is porch days and fridge nights; petroleum jelly seals moisture into cut faces, and a bleach-water spray slows mold but washes off in rain. All methods stretch days, none stop the clock."),
      ("Why did my jack-o-lantern rot in three days?", "Cut faces dry out and mold spores get to work - heat and sun speed it up. Carve later, scoop the walls thinner, and keep the lid on when it is off duty."),
      ("How long do uncarved pumpkins last?", "Weeks on a cool dry porch - which is the real answer: buy late and whole, and carve close to the date instead of preserving a carved one for weeks.")])

page("pumpkin-seeds-roast-calculator",
     "Pumpkin Seeds Roast Calculator - Yield, Servings and Roast Time",
     "Pumpkin Seeds Roast Calculator",
     "Enter your pumpkin weight to get cups of seeds, snack servings, oil and salt, and the roast time at 300 or 350 F - plus the simmer step most recipes skip that makes them crisp.",
     "pumpkin seeds roast time and temperature how many seeds per pumpkin",
     "seedroast",
     "Enter your pumpkin weight and this calculator returns the seed haul - about a quarter cup per pound - the snack servings it makes, the oil and salt to toss with, and roast minutes for 300 or 350 F. The carving leftovers stop being waste and become the actual snack of the evening, with the math to prove it.",
     "Seed recipes assume one mystery pumpkin; this page starts from the weight you actually have and scales everything: yield, servings, seasoning and time. The tip that separates crisp from chewy is in the note - a 10-minute salted simmer before roasting - and the honest closing line is that the pumpkin does not care whether it was bought to carve or to eat.",
     "Weigh your pumpkin and enter it.", "Pick your oven temperament - 300 F for even, 350 F for speed.", "Read cups, servings and the roast timer.",
     [("How many seeds are in a pumpkin?", "Roughly a quarter cup of cleaned seeds per pound of whole pumpkin - a 5-lb carving pumpkin nets about three quarters of a cup, enough for three snack servings."),
      ("What temperature roasts pumpkin seeds best?", "300 F for about 30-35 minutes gives even crisp without scorching; 350 F finishes in 22-28 minutes but watches closer. Stir once mid-roast either way."),
      ("Why simmer pumpkin seeds before roasting?", "A 10-minute simmer in salted water cooks the inside slightly so the oven crisps the shell instead of steaming it - the step most recipes skip and the difference between crisp and chewy."),
      ("Do you eat pumpkin seed shells?", "Yes - roasted shell-on seeds are the classic snack; the shell is where the salt and crunch live. Hulling them is a hobby, not a requirement.")])

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
print("R122 inject OK: 3 renderers + 3 pages + 3 emojis, ast passed")
