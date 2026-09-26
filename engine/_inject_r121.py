# -*- coding: utf-8 -*-
"""R121 柴火/取暖火簇:firewood-calculator / fire-pit-vs-patio-heater / firewood-seasoning
全程真实 emoji(R120 规则),repr 生成 pages 条目,每条替换断言精确计数。"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

FIREWOOD = (
    'FIREWOOD = """<div class="tool" id="tt-fw">\n'
    '  <div class="fields">\n'
    '    <div class="field"><label for="fw-a">Heated area (sq ft)</label><input type="number" id="fw-a" min="100" max="10000" step="50" placeholder="1000"></div>\n'
    '    <div class="field"><label for="fw-c">Climate</label><select id="fw-c"><option value="2">Mild winters</option><option value="3" selected>Moderate winters</option><option value="4.5">Cold winters</option></select></div>\n'
    '    <div class="field"><label for="fw-s">Species</label><select id="fw-s"><option value="26" selected>Seasoned hardwood (oak, maple)</option><option value="15">Seasoned softwood (pine, fir)</option></select></div>\n'
    '    <div class="field"><label for="fw-p">Price per cord ($)</label><input type="number" id="fw-p" min="50" max="900" step="10" placeholder="280"></div>\n'
    '  </div>\n'
    '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fw-out">&#8211;</span><span class="result-unit">cords for the winter</span></div>\n'
    '  <div class="stats">\n'
    '    <div class="stat"><b id="fw-s1">&#8211;</b><span>total wood cost</span></div>\n'
    '    <div class="stat"><b id="fw-s2">&#8211;</b><span>$ per million Btu</span></div>\n'
    '    <div class="stat"><b id="fw-s3">&#8211;</b><span>same heat, electric</span></div>\n'
    '  </div>\n'
    '  <div class="tool-note" id="fw-note"></div>\n'
    '  <button type="button" class="tool-btn" id="fw-share">Share my winter wood estimate</button>\n'
    '</div>\n'
    '<script>(function(){\n'
    "var F=['fw-a','fw-c','fw-s','fw-p'].map(function(id){return document.getElementById(id);});\n"
    "function calc(){\n"
    "  var a=parseFloat(F[0].value),c=parseFloat(F[1].value),btu=parseFloat(F[2].value),p=parseFloat(F[3].value);\n"
    "  if(!(a>0)||!(p>0)||!(btu>0)){return;}\n"
    "  var cords=a/1000*c, cost=cords*p, mbtu=cords*btu;\n"
    "  var perMbtu=mbtu>0?cost/mbtu:0, elec=293*0.15;\n"
    "  document.getElementById('fw-out').textContent=(Math.round(cords*10)/10);\n"
    "  document.getElementById('fw-s1').textContent='$'+Math.round(cost);\n"
    "  document.getElementById('fw-s2').textContent='$'+(Math.round(perMbtu*10)/10);\n"
    "  document.getElementById('fw-s3').textContent='$'+Math.round(elec);\n"
    "  document.getElementById('fw-note').textContent='Rule of thumb: cords per 1000 sq ft of floor, for wood as a main or heavy supplementary heat in a reasonably tight house. The honest part most firewood pages skip: the sticker price of a cord is not the price of wood heat - your labor is hauling, stacking and a year of seasoning, and electric resistive heat at 15 cents per kWh delivers the same million Btu for about $44 with zero labor. Wood wins on cost per heat unit if your time is cheap to you; gas and oil win on convenience. Split and stack now - seasoned wood is bought a season early.';\n"
    "  document.title=Math.round(cords*10)/10+' cords - Firewood Calculator - ToolDune';\n"
    "}\n"
    "function save(){try{localStorage.setItem('tt_fw',JSON.stringify({a:F[0].value,c:F[1].value,s:F[2].value,p:F[3].value}));}catch(e){}}\n"
    "F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
    "var ks=['a','c','s','p'],pre=false;\n"
    "ks.forEach(function(kk,i){var v=new URLSearchParams(location.search).get(kk);if(v!==null){F[i].value=v;pre=true;}});\n"
    "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_fw')||'null');if(m){ks.forEach(function(kk,i){if(m[kk]!==undefined&&m[kk]!==''){F[i].value=m[kk];}});}}catch(e){}}\n"
    "calc();\n"
    "document.getElementById('fw-share').addEventListener('click',function(){\n"
    "  var txt='Heating '+F[0].value+' sq ft takes about '+document.getElementById('fw-out').textContent+' cords of wood (~$'+document.getElementById('fw-s1').textContent+') this winter. Estimate yours:';\n"
    "  var url=location.origin+location.pathname+'?'+ks.map(function(kk,i){return kk+'='+encodeURIComponent(F[i].value);}).join('&');\n"
    "  if(navigator.share){navigator.share({title:'Firewood estimate',text:txt,url:url}).catch(function(){});}\n"
    "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my winter wood estimate';},1500);}\n"
    "});\n"
    "})();\n</script>\n\"\"\"\n\n"
)

FIREPITVS = (
    'FIREPITVS = """<div class="tool" id="tt-fph">\n'
    '  <div class="fields">\n'
    '    <div class="field"><label for="fph-w">Wood bundle price ($)</label><input type="number" id="fph-w" min="2" max="30" step="0.5" placeholder="8"></div>\n'
    '    <div class="field"><label for="fph-p">Propane tank refill ($)</label><input type="number" id="fph-p" min="5" max="80" step="1" placeholder="25"></div>\n'
    '    <div class="field"><label for="fph-e">Electricity rate ($/kWh)</label><input type="number" id="fph-e" min="0.03" max="0.8" step="0.01" placeholder="0.15"></div>\n'
    '  </div>\n'
    '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fph-out">&#8211;</span><span class="result-unit">cheapest per hour</span></div>\n'
    '  <div class="stats">\n'
    '    <div class="stat"><b id="fph-s1">&#8211;</b><span>wood fire pit / hour</span></div>\n'
    '    <div class="stat"><b id="fph-s2">&#8211;</b><span>propane heater / hour</span></div>\n'
    '    <div class="stat"><b id="fph-s3">&#8211;</b><span>electric infrared / hour</span></div>\n'
    '  </div>\n'
    '  <div class="tool-note" id="fph-note"></div>\n'
    '  <button type="button" class="tool-btn" id="fph-share">Share the per-hour math</button>\n'
    '</div>\n'
    '<script>(function(){\n'
    "var F=['fph-w','fph-p','fph-e'].map(function(id){return document.getElementById(id);});\n"
    "function calc(){\n"
    "  var w=parseFloat(F[0].value),p=parseFloat(F[1].value),e=parseFloat(F[2].value);\n"
    "  if(!(w>0)||!(p>0)||!(e>0)){return;}\n"
    "  var wh=w/1.5, ph=p/10.75, eh=1.5*e;\n"
    "  var r=Math.round, opts=[['wood',r(wh*100)/100],['propane',r(ph*100)/100],['electric',r(eh*100)/100]];\n"
    "  opts.sort(function(a,b){return a[1]-b[1];});\n"
    "  document.getElementById('fph-out').textContent=opts[0][0]+' ($'+opts[0][1]+'/h)';\n"
    "  document.getElementById('fph-s1').textContent='$'+r(wh*100)/100;\n"
    "  document.getElementById('fph-s2').textContent='$'+r(ph*100)/100;\n"
    "  document.getElementById('fph-s3').textContent='$'+r(eh*100)/100;\n"
    "  document.getElementById('fph-note').textContent='The assumptions are on the table: a store bundle (about 0.75 cubic ft) burns roughly 1.5 hours in a fire pit; a 20-lb propane tank holds about 430,000 Btu and a patio heater drinks 40,000 Btu per hour, so one tank is roughly 10.7 hours; electric infrared runs 1500 watts. Electric is always the cheapest heat but it warms a person, not a party - propane warms a 12-ft circle, and wood sells ambience at many times the price of electricity. You are allowed to buy atmosphere; price it honestly.';\n"
    "  document.title='Wood $'+r(wh*100)/100+'/h vs propane $'+r(ph*100)/100+'/h - ToolDune';\n"
    "}\n"
    "function save(){try{localStorage.setItem('tt_fph',JSON.stringify({w:F[0].value,p:F[1].value,e:F[2].value}));}catch(e){}}\n"
    "F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
    "var ks=['w','p','e'],pre=false;\n"
    "ks.forEach(function(kk,i){var v=new URLSearchParams(location.search).get(kk);if(v!==null){F[i].value=v;pre=true;}});\n"
    "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_fph')||'null');if(m){ks.forEach(function(kk,i){if(m[kk]!==undefined&&m[kk]!==''){F[i].value=m[kk];}});}}catch(e){}}\n"
    "calc();\n"
    "document.getElementById('fph-share').addEventListener('click',function(){\n"
    "  var txt='Backyard heat per hour: wood fire pit '+document.getElementById('fph-s1').textContent+', propane patio heater '+document.getElementById('fph-s2').textContent+', electric infrared '+document.getElementById('fph-s3').textContent+'. Do your own math:';\n"
    "  var url=location.origin+location.pathname+'?'+ks.map(function(kk,i){return kk+'='+encodeURIComponent(F[i].value);}).join('&');\n"
    "  if(navigator.share){navigator.share({title:'Fire pit vs patio heater',text:txt,url:url}).catch(function(){});}\n"
    "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share the per-hour math';},1500);}\n"
    "});\n"
    "})();\n</script>\n\"\"\"\n\n"
)

SEASONING = (
    'SEASONING = """<div class="tool" id="tt-fs">\n'
    '  <div class="fields">\n'
    '    <div class="field"><label for="fs-d">Split date</label><input type="date" id="fs-d"></div>\n'
    '    <div class="field"><label for="fs-s">Species</label><select id="fs-s"><option value="12">Oak - 12 months</option><option value="6">Ash - 6 months</option><option value="6.5">Pine/fir - 6-7 months</option><option value="9">Birch - 9 months</option></select></div>\n'
    '    <div class="field"><label for="fs-l">Stack length (ft)</label><input type="number" id="fs-l" min="1" max="60" step="1" placeholder="8"></div>\n'
    '    <div class="field"><label for="fs-h">Stack height (ft)</label><input type="number" id="fs-h" min="1" max="8" step="0.5" placeholder="4"></div>\n'
    '  </div>\n'
    '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fs-out">&#8211;</span><span class="result-unit">ready to burn</span></div>\n'
    '  <div class="stats">\n'
    '    <div class="stat"><b id="fs-s1">&#8211;</b><span>cords in stack</span></div>\n'
    '    <div class="stat"><b id="fs-s2">&#8211;</b><span>months to season</span></div>\n'
    '    <div class="stat"><b id="fs-s3">&#8211;</b><span>hiss test</span></div>\n'
    '  </div>\n'
    '  <div class="tool-note" id="fs-note"></div>\n'
    '  <button type="button" class="tool-btn" id="fs-share">Share my seasoning date</button>\n'
    '</div>\n'
    '<script>(function(){\n'
    "var F=['fs-d','fs-s','fs-l','fs-h'].map(function(id){return document.getElementById(id);});\n"
    "function calc(){\n"
    "  if(!F[0].value){return;}\n"
    "  var d=new Date(F[0].value+'T12:00:00Z'),mo=parseFloat(F[1].value),l=parseFloat(F[2].value),h=parseFloat(F[3].value);\n"
    "  if(isNaN(d.getTime())||!(mo>0)||!(l>0)||!(h>0)){return;}\n"
    "  var ready=new Date(d.getTime());ready.setMonth(ready.getMonth()+Math.ceil(mo));\n"
    "  var cords=l*h*4/128;\n"
    "  var names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];\n"
    "  var rs=names[ready.getMonth()]+' '+ready.getUTCFullYear();\n"
    "  document.getElementById('fs-out').textContent=rs;\n"
    "  document.getElementById('fs-s1').textContent=(Math.round(cords*100)/100);\n"
    "  document.getElementById('fs-s2').textContent=Math.ceil(mo);\n"
    "  document.getElementById('fs-s3').textContent='hiss = still wet';\n"
    "  document.getElementById('fs-note').textContent='Seasoned means under 20 percent moisture, and the signs beat any calendar: split ends turn grey and crack, bark loosens, two logs knocked together clack instead of thud - and a log that hisses while burning is a wet log burning your money. Stack off the ground, cover only the top so wind can pull moisture through the sides, and split early: a whole round seasons far slower than split pieces, which is why oak cut today is next winter\\'s fire.';\n"
    "  document.title='Ready by '+rs+' - ToolDune';\n"
    "}\n"
    "function save(){try{localStorage.setItem('tt_fs',JSON.stringify({d:F[0].value,s:F[1].value,l:F[2].value,h:F[3].value}));}catch(e){}}\n"
    "F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
    "var ks=['d','s','l','h'],pre=false;\n"
    "ks.forEach(function(kk,i){var v=new URLSearchParams(location.search).get(kk);if(v!==null){F[i].value=v;pre=true;}});\n"
    "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_fs')||'null');if(m){ks.forEach(function(kk,i){if(m[kk]!==undefined&&m[kk]!==''){F[i].value=m[kk];}});}}catch(e){}}\n"
    "if(!F[0].value){F[0].value=iso(new Date());}\n"
    "function iso(dt){return dt.toISOString().slice(0,10);}\n"
    "calc();\n"
    "document.getElementById('fs-share').addEventListener('click',function(){\n"
    "  var txt='My wood stack holds '+document.getElementById('fs-s1').textContent+' cords and seasons ready by '+document.getElementById('fs-out').textContent+'. Plan yours:';\n"
    "  var url=location.origin+location.pathname+'?'+ks.map(function(kk,i){return kk+'='+encodeURIComponent(F[i].value);}).join('&');\n"
    "  if(navigator.share){navigator.share({title:'Firewood seasoning',text:txt,url:url}).catch(function(){});}\n"
    "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my seasoning date';},1500);}\n"
    "});\n"
    "})();\n</script>\n\"\"\"\n\n"
)

BLOCK = FIREWOOD + FIREPITVS + SEASONING

def sub(path, old, new, n=1):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    assert s.count(old) == n, "anchor not %dx in %s: %r" % (n, path, old[:60])
    s = s.replace(old, new)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)

TOOLS_P = BASE + r"\tools.py"
PAGES_P = BASE + r"\pages.py"
BUILD_P = BASE + r"\build.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', BLOCK + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "bdaymoon": lambda args: BDAYMOON,',
    '    "bdaymoon": lambda args: BDAYMOON,\n'
    '    "firewood": lambda args: FIREWOOD,\n'
    '    "firepitvs": lambda args: FIREPITVS,\n'
    '    "seasoning": lambda args: SEASONING,')
sub(BUILD_P, '    "moonphase": "🌕", "fullmooncal": "🌖", "bdaymoon": "🌙",',
    '    "moonphase": "🌕", "fullmooncal": "🌖", "bdaymoon": "🌙",\n'
    '    "firewood": "🔥", "firepitvs": "♨️", "seasoning": "🌲",')

P = []
def page(slug, title, h1, desc, kw, tool, i1, i2, h1s, h2s, h3s, faqs):
    d = {'slug': slug, 'title': title, 'h1': h1, 'desc': desc, 'category': 'calculator',
         'keyword': kw, 'tool': tool, 'args': {}, 'intro': [i1, i2],
         'howto': [h1s, h2s, h3s], 'faqs': faqs}
    P.append("    pages.append(%r)\n" % (d,))

page("firewood-calculator",
     "Firewood Calculator - How Many Cords You Need for Winter",
     "Firewood Calculator",
     "Enter heated area, climate and species to get cords for the winter, total cost and dollars per million Btu against electric heat - with the labor cost most firewood pages skip. Free, instant.",
     "firewood calculator how many cords of firewood for winter",
     "firewood",
     "Enter your heated square footage, how cold your winters get, the species and the going price per cord, and this calculator returns cords for the winter, the total damage and the number that actually matters: dollars per million Btu, set against electric resistive heat at the same output. The rule of thumb is on the table - roughly 2, 3 or 4.5 cords per 1000 sq ft by climate - so you can argue with it instead of trusting it.",
     "Firewood sellers quote cords, not heat, and a softwood cord at half the oak price is not half the deal - it carries roughly half the Btu. This page converts everything to dollars per million Btu, and it also prices the part most pages hide: your labor. Wood wins on fuel cost if your time is cheap to you; the calculator leaves that judgment to you on purpose.",
     "Enter heated area and pick your climate.", "Add species and local price per cord.", "Read cords, total cost and the per-Btu verdict.",
     [("How many cords of firewood do I need for winter?", "A common rule is 2 cords per 1000 sq ft in mild climates, 3 in moderate and up to 4.5 in cold ones, assuming wood is a main or heavy supplementary heat in a reasonably tight house. Insulation and how much you burn evenings change it more than any formula."),
      ("Is softwood firewood worth half the price?", "Only if it is actually half the price - seasoned softwood carries roughly 15 million Btu per cord versus about 26 for hardwood, so per unit of heat the discount shrinks. The per-million-Btu line in this calculator settles it with your local prices."),
      ("What does a cord of firewood cost?", "Commonly $200-400 delivered depending on region and species - enter your local number. A cord is a stacked stack 4x4x8 ft, 128 cubic feet, which the seasoning calculator uses directly."),
      ("Should I heat my whole house with wood?", "You can, but the calculator prices only the fuel. Add the labor - hauling, stacking, tending the stove at 5 am - and judge honestly; many households land on wood for the rooms that matter and gas or electric for the rest.")])

page("fire-pit-vs-patio-heater",
     "Fire Pit vs Patio Heater - Real Cost per Hour Compared",
     "Fire Pit vs Patio Heater",
     "Wood fire pit, propane patio heater or electric infrared - enter your local prices and see the honest cost per hour of each, assumptions on the table. The cheapest heat is rarely the one being sold.",
     "fire pit vs patio heater cost per hour propane",
     "firepitvs",
     "Backyard heat has three contenders and sellers quote none of them per hour. This calculator does: a wood bundle burned in a fire pit, a 20-lb propane tank drunk by a 40,000 Btu patio heater, and a 1500-watt electric infrared panel - enter your local prices and read the cost per hour of each, with every assumption written where you can argue with it.",
     "Patio heater listings sell BTUs and fire pit blogs sell vibes; neither says what an evening costs. The answer flips the usual sales pitch: electric infrared is roughly twenty times cheaper per hour than wood - but it warms a person, not a party. Propane buys a 12-ft circle, wood buys the smell and the sparks. This page prices the heat and leaves the atmosphere to you.",
     "Enter wood bundle, propane refill and electricity prices.", "Read the per-hour cost of all three.", "Pick the heat that matches the evening you want.",
     [("How much does a fire pit cost per hour to run?", "A store bundle of wood (about 0.75 cubic feet) burns roughly 1.5 hours in a fire pit, so at $8 a bundle you are paying about $5 per hour - enter your local bundle price for your number."),
      ("How long does a 20-lb propane tank last on a patio heater?", "About 10-11 hours: the tank holds roughly 430,000 Btu and a typical patio heater burns 40,000 Btu per hour. Divide your refill price by that to get the hourly cost."),
      ("Are electric patio heaters cheap to run?", "Per hour, yes - a 1500-watt infrared panel costs about 15-35 cents depending on your rate, far under wood or propane. The catch is coverage: it heats the person in front of it, not the circle."),
      ("Which backyard heater should I buy?", "Match the heater to the evening: cheap reading warmth is electric, a circle of guests is propane, and if you want crackle and smell, wood - now priced honestly per hour.")])

page("firewood-seasoning",
     "Firewood Seasoning Calculator - When Is Your Stack Ready to Burn?",
     "Firewood Seasoning Calculator",
     "Enter your split date and species to get the seasoning-ready month, plus cords in your stack from its footprint - and the tell-tale signs (crack, clack, hiss) that beat any calendar.",
     "firewood seasoning time how long to season firewood",
     "seasoning",
     "Split wood is a promise the calendar has to keep: oak wants about 12 months, ash and pine are usable near 6, birch sits between. Enter your split date and species and this calculator returns the ready month, plus how many cords your stack holds from its length and height (a row 4 ft deep, the standard cord math of 128 cubic feet).",
     "Firewood buying guides pretend seasoning is a detail; it is the whole product - wet wood burns half as hot and coats your stove in creosote. This page gives the species timelines, the stack-to-cord math, and the field tests that beat any date: grey cracked split faces, bark peeling off, a clack instead of a thud when two logs meet, and the hiss that means a wet log is burning your money.",
     "Enter your split date and species.", "Add stack length and height for the cord count.", "Read the ready month and check the signs before burning.",
     [("How long does firewood take to season?", "Split oak wants about 12 months; ash and pine are near 6; birch around 9. Splitting early matters more than species - a whole round seasons far slower than split pieces, so wood cut this spring burns this winter."),
      ("How can I tell if firewood is seasoned?", "Look for grey, cracked split faces and loosening bark; knock two logs together - seasoned wood clacks, wet wood thuds; and if it hisses while burning, it is still wet and paying twice for the heat."),
      ("How many cords are in my stack?", "One row 4 ft deep: multiply length by height by 4 feet and divide by 128 cubic feet - an 8-ft by 4-ft row is a quarter cord. The calculator does it from your stack measurements."),
      ("Should I cover my wood stack?", "Cover the top only, and leave the sides open - wind pulls the moisture out, a full tarp traps it in. Stack off the ground on pallets or rails so the bottom row seasons too.")])

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
print("R121 inject OK: 3 renderers + 3 pages + 3 emojis, ast passed")
