# -*- coding: utf-8 -*-
"""R173 春季家居三连:gutter-cleaning-cost(落水管清理)+air-purifier-size(净化器CADR选型)+lawn-fertilizer(草坪施肥袋数)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: GUTTER ----------
Gu = 'GUTTER = """<div class="tool" id="tt-gu">\n'
Gu += '  <div class="fields">\n'
Gu += '    <div class="field"><label for="gu-f">Gutter linear feet</label><input id="gu-f" type="number" min="40" max="800" value="180"></div>\n'
Gu += '    <div class="field"><label for="gu-s">Stories</label><select id="gu-s"><option value="1" selected>Single story</option><option value="1.3">Two stories</option><option value="1.6">Three stories</option></select></div>\n'
Gu += '    <div class="field"><label for="gu-c">Debris load</label><select id="gu-c"><option value="1">Light - no trees near</option><option value="1.5" selected>Heavy - trees over the roof</option></select></div>\n'
Gu += '    <div class="field"><label for="gu-n">Cleanings per year</label><select id="gu-n"><option value="1">Once a year</option><option value="2" selected>Twice - spring and fall</option></select></div>\n'
Gu += '  </div>\n'
Gu += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gu-out">&#8211;</span><span class="result-unit">per cleaning</span></div>\n'
Gu += '  <div class="stats">\n'
Gu += '    <div class="stat"><b id="gu-s1">&#8211;</b><span>year cost</span></div>\n'
Gu += '    <div class="stat"><b id="gu-s2">&#8211;</b><span>guard install, if you went there</span></div>\n'
Gu += '    <div class="stat"><b id="gu-s3">&#8211;</b><span>years until guards pay off</span></div>\n'
Gu += '  </div>\n'
Gu += '  <div class="tool-note" id="gu-note"></div>\n'
Gu += '  <button type="button" class="tool-btn" id="gu-share">Share my gutter math</button>\n'
Gu += '</div>\n'
Gu += '<script>(function(){\n'
Gu += "var F=document.getElementById('gu-f'),S=document.getElementById('gu-s'),C=document.getElementById('gu-c'),N=document.getElementById('gu-n');\n"
Gu += "function calc(){\n"
Gu += "  var ft=parseFloat(F.value)||180,st=parseFloat(S.value)||1,cd=parseFloat(C.value)||1.5,n=parseFloat(N.value)||2;\n"
Gu += "  var clean=ft*1*st*cd, year=clean*n, guards=Math.round(ft*9), payoff=guards>0?Math.ceil(guards/Math.max(1,year)):0;\n"
Gu += "  var d1=Math.round(clean*10)/10, d2=Math.round(year);\n"
Gu += "  document.getElementById('gu-out').textContent='$'+d1;\n"
Gu += "  document.getElementById('gu-s1').textContent='$'+d2;\n"
Gu += "  document.getElementById('gu-s2').textContent='$'+guards;\n"
Gu += "  document.getElementById('gu-s3').textContent=payoff+'+ years';\n"
Gu += "  document.getElementById('gu-note').textContent='The cleaning is cheap; the skip is what costs - a clogged downspout is the actual villain, dumping water at the foundation and rotting the fascia quietly for a season. Spring and fall are the two fixed appointments, and heavy tree cover is why the second one exists. The guard question answered honestly: guards reduce the cleaning to an inspection rather than eliminating it, they cost 7 to 12 dollars a foot installed, and the payoff line shows how many years of cleanings buy that back - worth it for two-story homes, marginal for single-story. And the ladder rule: most gutter injuries are ladder injuries, which is why two stories is where hiring stops being optional.';\n"
Gu += "  document.title='Gutter cleaning: $'+d1+' per visit - ToolDune';\n"
Gu += "}\n"
Gu += "function save(){try{localStorage.setItem('tt_gutter',JSON.stringify({f:F.value,s:S.value,c:C.value,n:N.value}));}catch(e){}}\n"
Gu += "[F,S,C,N].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Gu += "var pre=false;\n"
Gu += "var qs=new URLSearchParams(location.search);\n"
Gu += "if(qs.get('f')){F.value=qs.get('f');pre=true;}\n"
Gu += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_gutter')||'null');if(m){if(m.f){F.value=m.f;}if(m.s){S.value=m.s;}if(m.c){C.value=m.c;}if(m.n){N.value=m.n;}}}catch(e){}}\n"
Gu += "calc();\n"
Gu += "document.getElementById('gu-share').addEventListener('click',function(){\n"
Gu += "  var txt='My gutters cost $'+document.getElementById('gu-out').textContent+' a cleaning - guards pay off in '+document.getElementById('gu-s3').textContent+'. Run yours:';\n"
Gu += "  var url=location.origin+location.pathname+'?f='+encodeURIComponent(F.value);\n"
Gu += "  if(navigator.share){navigator.share({title:'Gutter cleaning cost',text:txt,url:url}).catch(function(){});}\n"
Gu += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my gutter math';},1500);}\n"
Gu += "});\n"
Gu += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: AIRPUR ----------
Ap = 'AIRPUR = """<div class="tool" id="tt-ap">\n'
Ap += '  <div class="fields">\n'
Ap += '    <div class="field"><label for="ap-a">Room area (sq ft)</label><input id="ap-a" type="number" min="50" max="2000" value="300"></div>\n'
Ap += '    <div class="field"><label for="ap-p">Why you are buying it</label><select id="ap-p"><option value="1">Dust and general air</option><option value="1.5" selected>Allergies - pollen season</option><option value="2">Smoke or wildfire haze</option></select></div>\n'
Ap += '  </div>\n'
Ap += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ap-out">&#8211;</span><span class="result-unit">CADR to look for</span></div>\n'
Ap += '  <div class="stats">\n'
Ap += '    <div class="stat"><b id="ap-s1">&#8211;</b><span>filter budget a year</span></div>\n'
Ap += '    <div class="stat"><b id="ap-s2">&#8211;</b><span>run it in this room first</span></div>\n'
Ap += '    <div class="stat"><b id="ap-s3">&#8211;</b><span>marketing number to ignore</span></div>\n'
Ap += '  </div>\n'
Ap += '  <div class="tool-note" id="ap-note"></div>\n'
Ap += '  <button type="button" class="tool-btn" id="ap-share">Share my CADR math</button>\n'
Ap += '</div>\n'
Ap += '<script>(function(){\n'
Ap += "var A=document.getElementById('ap-a'),P=document.getElementById('ap-p');\n"
Ap += "function calc(){\n"
Ap += "  var a=parseFloat(A.value)||300,f=parseFloat(P.value)||1.5;\n"
Ap += "  var cadr=Math.ceil(a*0.65*f/10)*10, filter=60, market=Math.ceil(a*1.55);\n"
Ap += "  document.getElementById('ap-out').textContent=cadr;\n"
Ap += "  document.getElementById('ap-s1').textContent='$'+filter+'ish';\n"
Ap += "  document.getElementById('ap-s2').textContent='the bedroom';\n"
Ap += "  document.getElementById('ap-s3').textContent=Math.round(a*4)+' sq ft claims';\n"
Ap += "  document.getElementById('ap-note').textContent='CADR is the certified clean-air delivery number on the seal - it is the only spec that survives contact with physics, and the marketing square footage assumes one lazy air change an hour. Allergies want four or five, which is why the allergy multiplier doubles the machine. The room that matters most is the bedroom: eight hours of breathing is the longest exposure anyone gets, door closed so the sizing holds. Run it low at night for noise, high when you come home, and change the filter when it says - a clogged filter moves less air than no purifier at all.';\n"
Ap += "  document.title='Air purifier: CADR '+cadr+' for '+Math.round(a)+' sq ft - ToolDune';\n"
Ap += "}\n"
Ap += "function save(){try{localStorage.setItem('tt_airpur',JSON.stringify({a:A.value,p:P.value}));}catch(e){}}\n"
Ap += "[A,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Ap += "var pre=false;\n"
Ap += "var qs=new URLSearchParams(location.search);\n"
Ap += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Ap += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_airpur')||'null');if(m){if(m.a){A.value=m.a;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Ap += "calc();\n"
Ap += "document.getElementById('ap-share').addEventListener('click',function(){\n"
Ap += "  var txt='My room needs a purifier with CADR '+document.getElementById('ap-out').textContent+'. Size yours:';\n"
Ap += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Ap += "  if(navigator.share){navigator.share({title:'Air purifier sizing',text:txt,url:url}).catch(function(){});}\n"
Ap += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my CADR math';},1500);}\n"
Ap += "});\n"
Ap += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: LAWNFERT ----------
Lf = 'LAWNFERT = """<div class="tool" id="tt-lf">\n'
Lf += '  <div class="fields">\n'
Lf += '    <div class="field"><label for="lf-a">Lawn area (sq ft)</label><input id="lf-a" type="number" min="200" max="50000" value="5000"></div>\n'
Lf += '    <div class="field"><label for="lf-r">Bag label rate (lb per 1000 sq ft)</label><input id="lf-r" type="number" min="1" max="10" step="0.5" value="3.5"></div>\n'
Lf += '    <div class="field"><label for="lf-n">Feedings per year</label><select id="lf-n"><option value="2">2 - minimal</option><option value="4" selected>4 - the holiday rhythm</option><option value="5">5 - irrigation-fed</option></select></div>\n'
Lf += '    <div class="field"><label for="lf-p">Price per bag</label><input id="lf-p" type="number" min="5" value="30"></div>\n'
Lf += '  </div>\n'
Dj_dummy4 = None
Lf += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="lf-out">&#8211;</span><span class="result-unit">pounds per feeding</span></div>\n'
Lf += '  <div class="stats">\n'
Lf += '    <div class="stat"><b id="lf-s1">&#8211;</b><span>bags for the year</span></div>\n'
Lf += '    <div class="stat"><b id="lf-s2">&#8211;</b><span>year cost</span></div>\n'
Lf += '    <div class="stat"><b id="lf-s3">&#8211;</b><span>the holiday rhythm</span></div>\n'
Lf += '  </div>\n'
Lf += '  <div class="tool-note" id="lf-note"></div>\n'
Lf += '  <button type="button" class="tool-btn" id="lf-share">Share my fertilizer math</button>\n'
Lf += '</div>\n'
Lf += '<script>(function(){\n'
Lf += "var A=document.getElementById('lf-a'),R=document.getElementById('lf-r'),N=document.getElementById('lf-n'),P=document.getElementById('lf-p');\n"
Lf += "function calc(){\n"
Lf += "  var a=parseFloat(A.value)||5000,rate=parseFloat(R.value)||3.5,n=parseFloat(N.value)||4,p=parseFloat(P.value)||30;\n"
Lf += "  var perApp=a/1000*rate, year=perApp*n, bags=Math.ceil(year/40), cost=bags*p;\n"
Lf += "  var d1=Math.round(perApp*10)/10, d2=Math.round(cost);\n"
Lf += "  document.getElementById('lf-out').textContent=d1;\n"
Lf += "  document.getElementById('lf-s1').textContent=bags;\n"
Lf += "  document.getElementById('lf-s2').textContent='$'+d2;\n"
Lf += "  document.getElementById('lf-s3').textContent='Memorial, July 4, Labor Day, Halloween';\n"
Lf += "  document.getElementById('lf-note').textContent='The rate comes off the bag label - it is calibrated to the nitrogen number, and nitrogen is the one that burns: more product does not mean greener, it means stripes. The holiday rhythm is the memorization trick for cool-season lawns - Memorial Day, July 4, Labor Day, Halloween - spaced so each feeding lands when the grass is actually growing. The soil test from the county extension costs about fifteen dollars and often deletes a feeding entirely, which pays for itself the first season. And spread on a dry morning before rain - the rain waters it in for free.';\n"
Lf += "  document.title='Fertilizer: '+d1+' lb per feeding - ToolDune';\n"
Lf += "}\n"
Lf += "function save(){try{localStorage.setItem('tt_lawnfert',JSON.stringify({a:A.value,r:R.value,n:N.value,p:P.value}));}catch(e){}}\n"
Lf += "[A,R,N,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Lf += "var pre=false;\n"
Lf += "var qs=new URLSearchParams(location.search);\n"
Lf += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Lf += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_lawnfert')||'null');if(m){if(m.a){A.value=m.a;}if(m.r){R.value=m.r;}if(m.n){N.value=m.n;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Lf += "calc();\n"
Lf += "document.getElementById('lf-share').addEventListener('click',function(){\n"
Lf += "  var txt='My lawn takes '+document.getElementById('lf-out').textContent+' lb of fertilizer per feeding - '+document.getElementById('lf-s1').textContent+' bags a year. Run yours:';\n"
Lf += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Lf += "  if(navigator.share){navigator.share({title:'Lawn fertilizer math',text:txt,url:url}).catch(function(){});}\n"
Lf += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my fertilizer math';},1500);}\n"
Lf += "});\n"
Lf += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("GUTTER", "AIRPUR", "LAWNFERT"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Gu + Ap + Lf + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "wedding": lambda args: WEDDING,',
    '    "wedding": lambda args: WEDDING,\n'
    '    "gutter": lambda args: GUTTER,\n'
    '    "airpur": lambda args: AIRPUR,\n'
    '    "lawnfert": lambda args: LAWNFERT,')
sub(BUILD_P, '    "wedding": "💍",',
    '    "wedding": "💍",\n'
    '    "gutter": "🍂", "airpur": "🍃", "lawnfert": "🌿",')

P = []
d = {'slug': 'gutter-cleaning-cost-calculator',
     'title': 'Gutter Cleaning Cost Calculator - Per Visit, Year and Guards Payoff',
     'h1': 'Gutter Cleaning Cost Calculator',
     'desc': 'Gutter feet, stories and debris load price each cleaning and the year - and answer the guards question with a real payoff math. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'gutter cleaning cost calculator price per linear foot',
     'tool': 'gutter',
     'args': {},
     'intro': ["Enter the gutter run, your story count, the debris load and how many cleanings a year you schedule. The calculator prices each visit, the year, and - the question everyone actually has - how many years until gutter guards pay for themselves.",
              "The cleaning is cheap; the skip is what costs. A clogged downspout is the actual villain, dumping water at the foundation and rotting the fascia quietly for a season. Guards reduce cleaning to inspection rather than eliminating it, and the payoff math says honestly whether they are worth it for your story count."],
     'howto': ["Measure the gutter run along the roofline, corners included.",
               "Two stories and up: the ladder rule makes hiring the sensible default.",
               "Heavy tree cover is why the fall cleaning exists."],
     'faqs': [("How much does gutter cleaning cost?",
               "The national average runs about a dollar per linear foot, scaled up for stories and heavy debris - a typical 180-foot single-story home lands near 180 dollars a visit, twice a year in spring and fall."),
              ("How often should gutters be cleaned?",
               "Twice a year covers most homes - spring and fall. Heavy tree cover pushes it to three; homes with no trees over the roof can stretch to one. The clogged downspout, not the gutter trough, is the failure to prevent."),
              ("Are gutter guards worth the money?",
               "They reduce cleaning to an inspection, not eliminate it - fine debris still gets through. At 7-12 dollars a foot installed, the payoff against yearly cleanings runs years; the calculator prices it for your story count and tree cover."),
              ("Can I clean gutters myself?",
               "Single story with a stable ladder, yes - gloves and a scoop, and never overreach. Two stories and up is where hiring stops being optional: most gutter injuries are ladder injuries, and the cleaning costs less than the emergency room copay.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'air-purifier-size-calculator',
     'title': 'Air Purifier Size Calculator - The CADR Number That Matters',
     'h1': 'Air Purifier Size Calculator',
     'desc': 'Room size and your reason for buying give the CADR to look for on the seal - allergies double it, smoke more - plus the marketing number to ignore. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'air purifier size calculator what size cadr room',
     'tool': 'airpur',
     'args': {},
     'intro': ["Enter the room area and why you are buying - dust, allergies, or smoke. The calculator gives the CADR number to look for on the certification seal, and the marketing square-footage claim to ignore.",
              "CADR is the only spec that survives contact with physics: the marketing room-size numbers assume one lazy air change an hour, while allergies want four or five - which is why the allergy version of this calculator doubles the machine. The room that matters most is the bedroom, because eight hours of breathing is the longest exposure anyone gets."],
     'howto': ["Measure the room the purifier will live in, door closed.",
               "Pick the honest reason - allergies and smoke run bigger machines.",
               "Buy the certified seal, not the square-footage headline."],
     'faqs': [("What size air purifier do I need for my room?",
               "Look for a CADR around two-thirds of your square footage for general air, doubled for allergies, more for smoke. A 300-square-foot bedroom wants roughly CADR 300 for allergy season - the calculator prices your room and reason."),
              ("What does CADR mean on air purifiers?",
               "Clean Air Delivery Rate - the certified cubic-feet-per-minute of filtered air, tested on dust, pollen and smoke. It is the only number verified by an independent standard; everything else on the box is marketing geometry."),
              ("Why does the marketing claim a bigger room than the CADR suggests?",
               "Room-size claims assume one air change per hour; allergy guidance wants four or five. Same machine, different math - the calculator runs the honest version for your reason."),
              ("Where should I run an air purifier?",
               "The bedroom first - eight hours of breathing is the longest exposure of the day - with the door closed so the sizing holds. Run it low at night for noise, high when you return home, and replace filters on schedule.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'lawn-fertilizer-calculator',
     'title': 'Lawn Fertilizer Calculator - Pounds Per Feeding and Bags a Year',
     'h1': 'Lawn Fertilizer Calculator',
     'desc': 'Lawn size, the bag label rate and the holiday rhythm give pounds per feeding, bags a year and the cost - with the soil-test note that saves a feeding. Free.',
     'category': 'calculator',
     'keyword': 'lawn fertilizer calculator how much fertilizer per square foot',
     'tool': 'lawnfert',
     'args': {},
     'intro': ["Enter your lawn size, the application rate printed on the bag, how many feedings a year, and the bag price. The calculator gives pounds per feeding, bags for the year, and the cost.",
              "The rate comes off the bag label because it is calibrated to the nitrogen number - and nitrogen is the one that burns: more product does not mean greener, it means stripes. The holiday rhythm is the memorization trick for cool-season lawns, and the county extension soil test costs about fifteen dollars and often deletes a feeding entirely."],
     'howto': ["Measure the lawn - guess high on the unofficial dirt patches.",
               "The bag label rate is printed with the N-P-K numbers.",
               "Memorial Day, July 4, Labor Day, Halloween - that is the rhythm."],
     'faqs': [("How much fertilizer do I need per square foot?",
               "Bag labels rate applications in pounds per 1000 square feet - commonly 3 to 4 pounds for lawn products. The calculator scales that to your actual lawn and counts the year in bags."),
              ("How often should I fertilize my lawn?",
               "Cool-season lawns do well on four feedings a year, memorized as the holidays: Memorial Day, July 4, Labor Day and Halloween - each landing when the grass is actually growing. Five works with irrigation; two is the honest minimum."),
              ("What happens if I use too much fertilizer?",
               "Nitrogen burns - literal brown stripes where the spreader overlapped - plus runoff that feeds algae downstream. The label rate is a ceiling, not a suggestion; more product means stripes, not green."),
              ("Do I need a soil test before fertilizing?",
               "The county extension soil test costs about fifteen dollars and reports what the lawn actually lacks - it often deletes a feeding entirely or swaps the product, which pays for the test the first season.")]}
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
print("R173 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
