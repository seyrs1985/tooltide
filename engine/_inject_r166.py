# -*- coding: utf-8 -*-
"""R166 情人节与早春三连:date-night-cost(约会成本)+seed-starting(育苗日历)+raised-bed-soil(苗床土方)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: DATENIGHT ----------
Dn2 = 'DATENIGHT = """<div class="tool" id="tt-dn">\n'
Dn2 += '  <div class="fields">\n'
Dn2 += '    <div class="field"><label for="dn-d">Dinner for two</label><input id="dn-d" type="number" min="0" value="80"></div>\n'
Dn2 += '    <div class="field"><label for="dn-a">Activity or tickets</label><input id="dn-a" type="number" min="0" value="40"></div>\n'
Dn2 += '    <div class="field"><label for="dn-s">Sitter rate per hour</label><input id="dn-s" type="number" min="0" value="20"></div>\n'
Dn2 += '    <div class="field"><label for="dn-h">Sitter hours</label><input id="dn-h" type="number" min="0" max="12" value="3"></div>\n'
Dn2 += '  </div>\n'
Dn2 += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dn-out">&#8211;</span><span class="result-unit">per date night</span></div>\n'
Dn2 += '  <div class="stats">\n'
Dn2 += '    <div class="stat"><b id="dn-s1">&#8211;</b><span>monthly at twice a month</span></div>\n'
Dn2 += '    <div class="stat"><b id="dn-s2">&#8211;</b><span>the sitter share</span></div>\n'
Dn2 += '    <div class="stat"><b id="dn-s3">&#8211;</b><span>year cost</span></div>\n'
Dn2 += '  </div>\n'
Dn2 += '  <div class="tool-note" id="dn-note"></div>\n'
Dn2 += '  <button type="button" class="tool-btn" id="dn-share">Share my date math</button>\n'
Dn2 += '</div>\n'
Dn2 += '<script>(function(){\n'
Dn2 += "var D=document.getElementById('dn-d'),A=document.getElementById('dn-a'),S=document.getElementById('dn-s'),H=document.getElementById('dn-h');\n"
Dn2 += "function calc(){\n"
Dn2 += "  var d=parseFloat(D.value)||0,a=parseFloat(A.value)||0,s=parseFloat(S.value)||0,h=parseFloat(H.value)||0;\n"
Dn2 += "  var sitter=s*h, total=d+a+sitter, month=total*2, year=total*24;\n"
Dn2 += "  var d1=Math.round(total*100)/100, d2=Math.round(month), d3=Math.round(year);\n"
Dn2 += "  var share=total>0?Math.round(sitter/total*100):0;\n"
Dn2 += "  document.getElementById('dn-out').textContent='$'+d1;\n"
Dn2 += "  document.getElementById('dn-s1').textContent='$'+d2;\n"
Dn2 += "  document.getElementById('dn-s2').textContent=share+'%';\n"
Dn2 += "  document.getElementById('dn-s3').textContent='$'+d3;\n"
Dn2 += "  document.getElementById('dn-note').textContent='The sitter is the hidden headline: for parents the childcare line dwarfs dinner, which is why the swap circle with trusted friends - you take their Tuesday, they take yours - is the single biggest cost fix in this whole budget. The research note worth the money: novelty beats grandeur - a new cuisine on a random Tuesday does more for a relationship than the annual reservation at the famous place. Budget the dates, keep them frequent, and let the big nights be a bonus instead of the whole story.';\n"
Dn2 += "  document.title='Date night: $'+d1+' - ToolDune';\n"
Dn2 += "}\n"
Dn2 += "function save(){try{localStorage.setItem('tt_datenight',JSON.stringify({d:D.value,a:A.value,s:S.value,h:H.value}));}catch(e){}}\n"
Dn2 += "[D,A,S,H].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Dn2 += "var pre=false;\n"
Dn2 += "var qs=new URLSearchParams(location.search);\n"
Dn2 += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
Dn2 += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_datenight')||'null');if(m){if(m.d){D.value=m.d;}if(m.a){A.value=m.a;}if(m.s){S.value=m.s;}if(m.h){H.value=m.h;}}}catch(e){}}\n"
Dn2 += "calc();\n"
Dn2 += "document.getElementById('dn-share').addEventListener('click',function(){\n"
Dn2 += "  var txt='Our date nights run $'+document.getElementById('dn-out').textContent+' - the sitter is '+document.getElementById('dn-s2').textContent+' of it. Price yours:';\n"
Dn2 += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
Dn2 += "  if(navigator.share){navigator.share({title:'Date night cost',text:txt,url:url}).catch(function(){});}\n"
Dn2 += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my date math';},1500);}\n"
Dn2 += "});\n"
Dn2 += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: SEEDSTART ----------
Ss2 = 'SEEDSTART = """<div class="tool" id="tt-ssd">\n'
Ss2 += '  <div class="fields">\n'
Ss2 += '    <div class="field"><label for="ssd-d">Your last frost date</label><input type="date" id="ssd-d"></div>\n'
Ss2 += '    <div class="field"><label for="ssd-v">Crop</label><select id="ssd-v"><option value="9">Peppers - 9 weeks</option><option value="7" selected>Tomatoes - 7 weeks</option><option value="6">Brassicas - 6 weeks</option><option value="5">Zinnias - 5 weeks</option><option value="4">Lettuce - 4 weeks</option><option value="3">Cucumbers - 3 weeks</option></select></div>\n'
Ss2 += '  </div>\n'
Ss2 += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ssd-out">&#8211;</span><span class="result-unit">sow seeds indoors</span></div>\n'
Ss2 += '  <div class="stats">\n'
Ss2 += '    <div class="stat"><b id="ssd-s1">&#8211;</b><span>transplant week</span></div>\n'
Ss2 += '    <div class="stat"><b id="ssd-s2">&#8211;</b><span>days from today</span></div>\n'
Ss2 += '    <div class="stat"><b id="ssd-s3">&#8211;</b><span>the hardening-off week</span></div>\n'
Ss2 += '  </div>\n'
Ss2 += '  <div class="tool-note" id="ssd-note"></div>\n'
Ss2 += '  <button type="button" class="tool-btn" id="ssd-share">Share my sow date</button>\n'
Ss2 += '</div>\n'
Ss2 += '<script>(function(){\n'
Ss2 += "var D=document.getElementById('ssd-d'),V=document.getElementById('ssd-v');\n"
Ss2 += "function calc(){\n"
Ss2 += "  var dv=D.value,wk=parseFloat(V.value)||7;\n"
Ss2 += "  if(!dv){document.getElementById('ssd-out').textContent='\\u2013';return;}\n"
Ss2 += "  var p=dv.split('-');\n"
Ss2 += "  var frost=new Date(parseInt(p[0],10),parseInt(p[1],10)-1,parseInt(p[2],10));\n"
Ss2 += "  var now=new Date();var today=new Date(now.getFullYear(),now.getMonth(),now.getDate());\n"
Ss2 += "  if(frost.getTime()<today.getTime()){frost=new Date(frost.getFullYear()+1,frost.getMonth(),frost.getDate());}\n"
Ss2 += "  var sow=new Date(frost.getTime()-wk*7*86400000);\n"
Ss2 += "  var tp=new Date(frost.getTime()+7*86400000);\n"
Ss2 += "  var left=Math.round((sow-today)/86400000);\n"
Ss2 += "  var names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];\n"
Ss2 += "  document.getElementById('ssd-out').textContent=names[sow.getMonth()]+' '+sow.getDate();\n"
Ss2 += "  document.getElementById('ssd-s1').textContent=names[tp.getMonth()]+' '+tp.getDate();\n"
Ss2 += "  document.getElementById('ssd-s2').textContent=left>0?left:'this week';\n"
Ss2 += "  document.getElementById('ssd-s3').textContent='go gradual';\n"
Ss2 += "  document.getElementById('ssd-note').textContent='The seed packet is the boss - this table is the consensus window, your variety and zone nudge it. Two rules separate thriving starts from leggy disappointments: light beats warmth once sprouted - a sunny window is not enough, a cheap shop light an inch above the seedlings is - and transplant week is earned outdoors, an hour the first day, doubling daily, or the sun burns a month of care in one afternoon. Leggy seedlings are reaching for light you are not giving them, not asking for fertilizer.';\n"
Ss2 += "  document.title='Sow '+names[sow.getMonth()]+' '+sow.getDate()+' indoors - ToolDune';\n"
Ss2 += "}\n"
Ss2 += "function save(){try{localStorage.setItem('tt_seedstart',JSON.stringify({d:D.value,v:V.value}));}catch(e){}}\n"
Ss2 += "[D,V].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Ss2 += "var pre=false;\n"
Ss2 += "var qs=new URLSearchParams(location.search);\n"
Ss2 += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
Ss2 += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_seedstart')||'null');if(m){if(m.d){D.value=m.d;}if(m.v){V.value=m.v;}}}catch(e){}}\n"
Ss2 += "if(!D.value){var td=new Date();D.value=(td.getMonth()>5?td.getFullYear()+1:td.getFullYear())+'-04-15';}\n"
Ss2 += "calc();\n"
Ss2 += "document.getElementById('ssd-share').addEventListener('click',function(){\n"
Ss2 += "  var txt='Sow '+V.value+' seeds indoors on '+document.getElementById('ssd-out').textContent+'. Plan yours:';\n"
Ss2 += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
Ss2 += "  if(navigator.share){navigator.share({title:'Seed starting schedule',text:txt,url:url}).catch(function(){});}\n"
Ss2 += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my sow date';},1500);}\n"
Ss2 += "});\n"
Ss2 += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: BEDSOIL ----------
Bs = 'BEDSOIL = """<div class="tool" id="tt-bs">\n'
Bs += '  <div class="fields">\n'
Bs += '    <div class="field"><label for="bs-l">Bed length (ft)</label><input id="bs-l" type="number" min="1" max="100" step="0.5" value="8"></div>\n'
Bs += '    <div class="field"><label for="bs-w">Bed width (ft)</label><input id="bs-w" type="number" min="0.5" max="50" step="0.5" value="4"></div>\n'
Bs += '    <div class="field"><label for="bs-d">Soil depth (inches)</label><select id="bs-d"><option value="6">6 in - herbs, lettuce</option><option value="12" selected>12 in - tomatoes, roots</option><option value="18">18 in - deep beds</option></select></div>\n'
Bs += '    <div class="field"><label for="bs-p">Price per 1.5 cu ft bag</label><input id="bs-p" type="number" min="1" step="0.5" value="6"></div>\n'
Bs += '  </div>\n'
Bs += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bs-out">&#8211;</span><span class="result-unit">cubic feet of soil</span></div>\n'
Bs += '  <div class="stats">\n'
Bs += '    <div class="stat"><b id="bs-s1">&#8211;</b><span>1.5 cu ft bags</span></div>\n'
Bs += '    <div class="stat"><b id="bs-s2">&#8211;</b><span>soil cost</span></div>\n'
Bs += '    <div class="stat"><b id="bs-s3">&#8211;</b><span>established bed top-up</span></div>\n'
Bs += '  </div>\n'
Bs += '  <div class="tool-note" id="bs-note"></div>\n'
Bs += '  <button type="button" class="tool-btn" id="bs-share">Share my soil order</button>\n'
Bs += '</div>\n'
Bs += '<script>(function(){\n'
Bs += "var L=document.getElementById('bs-l'),W=document.getElementById('bs-w'),D2=document.getElementById('bs-d'),P=document.getElementById('bs-p');\n"
Bs += "function calc(){\n"
Bs += "  var l=parseFloat(L.value)||8,w=parseFloat(W.value)||4,din=parseFloat(D2.value)||12,p=parseFloat(P.value)||6;\n"
Bs += "  var cf=l*w*din/12, bags=Math.ceil(cf/1.5), cost=bags*p, topup=Math.ceil(l*w*2/12/1.5);\n"
Bs += "  var d1=Math.round(cf*10)/10, d2=Math.round(cost);\n"
Bs += "  document.getElementById('bs-out').textContent=d1;\n"
Bs += "  document.getElementById('bs-s1').textContent=bags;\n"
Bs += "  document.getElementById('bs-s2').textContent='$'+d2;\n"
Bs += "  document.getElementById('bs-s3').textContent=topup+' bags';\n"
Bs += "  document.getElementById('bs-note').textContent='Volume math for a new bed is length times width times depth - the soil settles maybe ten percent, so round up the last bag. The honest alternatives at volume: landscape yards sell by the cubic yard at a fraction of bagged pricing, and one yard covers about eighteen of these bags - worth the phone call past six bags. For an established bed, skip the reset entirely: a two-inch compost top-up each spring feeds the soil web better than replacement, and the top-up figure in the stats is that number.';\n"
Bs += "  document.title='Soil: '+d1+' cu ft ('+bags+' bags) - ToolDune';\n"
Bs += "}\n"
Bs += "function save(){try{localStorage.setItem('tt_bedsoil',JSON.stringify({l:L.value,w:W.value,d:D2.value,p:P.value}));}catch(e){}}\n"
Bs += "[L,W,D2,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Bs += "var pre=false;\n"
Bs += "var qs=new URLSearchParams(location.search);\n"
Bs += "if(qs.get('l')){L.value=qs.get('l');pre=true;}\n"
Bs += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_bedsoil')||'null');if(m){if(m.l){L.value=m.l;}if(m.w){W.value=m.w;}if(m.d){D2.value=m.d;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Bs += "calc();\n"
Bs += "document.getElementById('bs-share').addEventListener('click',function(){\n"
Bs += "  var txt='My bed takes '+document.getElementById('bs-out').textContent+' cubic feet of soil - '+document.getElementById('bs-s1').textContent+' bags. Size yours:';\n"
Bs += "  var url=location.origin+location.pathname+'?l='+encodeURIComponent(L.value);\n"
Bs += "  if(navigator.share){navigator.share({title:'Raised bed soil',text:txt,url:url}).catch(function(){});}\n"
Bs += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my soil order';},1500);}\n"
Bs += "});\n"
Bs += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("DATENIGHT", "SEEDSTART", "BEDSOIL"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Dn2 + Ss2 + Bs + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "charmile": lambda args: CHARMILE,',
    '    "charmile": lambda args: CHARMILE,\n'
    '    "datenight": lambda args: DATENIGHT,\n'
    '    "seedstart": lambda args: SEEDSTART,\n'
    '    "bedsoil": lambda args: BEDSOIL,')
sub(BUILD_P, '    "homeded": "📎", "setaside": "💼", "charmile": "🚶",',
    '    "homeded": "📎", "setaside": "💼", "charmile": "🚶",\n'
    '    "datenight": "💘", "seedstart": "🌱", "bedsoil": "🌾",')

P = []
d = {'slug': 'date-night-cost-calculator',
     'title': 'Date Night Cost Calculator - Dinner, Activity and the Sitter Truth',
     'h1': 'Date Night Cost Calculator',
     'desc': 'Dinner, activity and sitter hours give the real per-date cost, the monthly figure and the year - with the swap-circle fix that halves it. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'date night cost calculator with babysitter dinner movie',
     'tool': 'datenight',
     'args': {},
     'intro': ["Enter dinner, the activity, and the sitter rate and hours. The calculator gives the true per-date cost, the monthly figure at twice a month, and the share the sitter quietly takes.",
              "For parents the childcare line dwarfs dinner - which is why the swap circle with trusted friends (you take their Tuesday, they take yours) is the single biggest cost fix in this budget. The research note justifies the spend: novelty beats grandeur, so frequent small new experiences outperform the annual famous reservation."],
     'howto': ["Price dinner and the activity honestly - taxes and tip included.",
               "Set sitter rate and hours; round trips count.",
               "Read the monthly figure - that is the budget line that matters."],
     'faqs': [("What is a reasonable date night budget?",
               "Dinner for two runs 60-120 depending on the city, activities 0-60, and a sitter 60-90 for the evening - so 120-250 total with childcare. The calculator prices your actual pattern, including the monthly figure that belongs in the budget."),
              ("How can we make date nights cheaper?",
               "The sitter swap with another family you trust - alternate Tuesdays, zero cash - halves the total instantly. Lunch dates, museum free days and the walking-and-talking format carry most of the benefit at a fraction of the cost."),
              ("Is an expensive date night worth it?",
               "The research on relationships points at frequency and novelty, not grandeur: new shared experiences - a new cuisine, a class, an unfamiliar neighborhood - outperform repeated luxury. Budget for frequency first; let the grand nights be a bonus."),
              ("How often should couples have a date night?",
               "Weekly is the classic advice; twice a month is where the measurable relationship benefits show up in studies. The calculator prices either cadence so the choice is a budget line, not a guilt spiral.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'seed-starting-calculator',
     'title': 'Seed Starting Calculator - When to Sow Indoors Before Last Frost',
     'h1': 'Seed Starting Calculator',
     'desc': 'Last frost date plus your crop gives the indoor sowing date, the transplant week, and days from today - tomatoes to lettuce on the consensus table. Free.',
     'category': 'calculator',
     'keyword': 'seed starting calculator when to start seeds indoors last frost',
     'tool': 'seedstart',
     'args': {},
     'intro': ["Enter your last frost date and pick the crop. The calculator counts back the consensus weeks - peppers nine, tomatoes seven, cucumbers three - and gives the indoor sowing date, the transplant week, and days from today.",
              "The seed packet is the boss; this table is the consensus window your variety and zone nudge. The two rules that separate thriving starts from leggy disappointment: light beats warmth once sprouted - a shop light an inch above the tray beats any windowsill - and transplant week is earned outdoors gradually, or the sun burns a month of care in one afternoon."],
     'howto': ["Enter your area last frost date - extension tables have it for your town.",
               "Pick each crop; the weeks-before-frost are built in.",
               "Set a shop light an inch above the seedlings; windows stretch them."],
     'faqs': [("When should I start tomato seeds indoors?",
               "Six to eight weeks before your last frost - seven is the sweet spot. Earlier is not better: tomatoes outgrow their trays and get leggy before the garden is ready, and leggy starts fruit less."),
              ("What happens if I start seeds too early?",
               "Root-bound, light-starved transplants that wait weeks for the soil to warm - the head start evaporates. Peppers and tomatoes hold at a smaller size better than they recover from stretched stems."),
              ("Do I need grow lights to start seeds?",
               "For anything beyond lettuce, effectively yes: a cheap shop light an inch above the seedlings for 14-16 hours beats the brightest windowsill, because winter sun is weak and low-angle - the legginess people blame on variety is usually window light."),
              ("What is hardening off?",
               "The transplant-week discipline: an hour of outdoor shade the first day, doubling daily, until the starts survive full sun and breeze. Skipping it burns a month of indoor care in a single afternoon - the calculator schedules the week so it is not skipped.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'raised-bed-soil-calculator',
     'title': 'Raised Bed Soil Calculator - Cubic Feet, Bags and Cost',
     'h1': 'Raised Bed Soil Calculator',
     'desc': 'Bed dimensions times depth give cubic feet of soil, the 1.5 cu ft bag count, the cost, and the two-inch top-up figure for established beds. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'raised bed soil calculator how much soil cubic feet bags',
     'tool': 'bedsoil',
     'args': {},
     'intro': ["Enter the bed length, width and soil depth. The calculator gives cubic feet, the number of 1.5 cubic foot bags, the cost, and the two-inch top-up figure for beds that already exist.",
              "The honest alternatives arrive at volume: landscape yards sell by the cubic yard at a fraction of bagged pricing - one yard covers about eighteen bags - and established beds skip the reset entirely in favor of a two-inch compost top-up that feeds the soil web better than replacement ever does."],
     'howto': ["Measure inside the frame, length by width, and pick the depth.",
               "Twelve inches suits tomatoes and roots; six is fine for lettuce.",
               "Past six bags, call a landscape yard and price a cubic-yard delivery."],
     'faqs': [("How much soil do I need for a 4x8 raised bed?",
               "At 12 inches deep, 32 cubic feet - about 22 of the 1.5 cubic foot bags. Six inches deep halves it to 16 cubic feet. The calculator prices either depth from your dimensions."),
              ("How many bags of soil for a raised bed?",
               "Divide total cubic feet by 1.5 for standard bags and round up for settling. Past about six bags, a landscape yard delivery by the cubic yard costs a fraction of the bagged route."),
              ("What depth does a raised bed need?",
               "Six inches runs lettuce, herbs and greens; twelve covers tomatoes, peppers and root crops; deeper beds mostly buy drainage and root-run for the ambitious. Deeper than your plants need is money spent on soil."),
              ("Do I need to replace raised bed soil every year?",
               "No - top up with two inches of compost each spring instead. Replacement dumps a functioning soil web and costs the most; the calculator shows the top-up figure next to the full reset for the comparison.")]}
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
print("R166 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
