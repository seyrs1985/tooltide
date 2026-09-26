# -*- coding: utf-8 -*-
"""R139 冬前家居簇:christmas-lights-cost(LEDvs白炽电费账)+furnace-filter(尺寸解码+MERV诚实账)+humidifier-size(房间→加仑/天选型)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: LIGHTCOST ----------
Lc = 'LIGHTCOST = """<div class="tool" id="tt-lc">\n'
Lc += '  <div class="fields">\n'
Lc += '    <div class="field"><label for="lc-n">Strings on display</label><input id="lc-n" type="number" min="1" max="200" value="6"></div>\n'
Lc += '    <div class="field"><label for="lc-t">String type</label><select id="lc-t"><option value="40">Mini incandescent - 40 W</option><option value="5" selected>Mini LED - 5 W</option><option value="175">C9 incandescent - 175 W</option><option value="25">C9 LED - 25 W</option></select></div>\n'
Lc += '    <div class="field"><label for="lc-h">Hours lit per day</label><input id="lc-h" type="number" min="1" max="24" value="6"></div>\n'
Lc += '    <div class="field"><label for="lc-d">Days this season</label><input id="lc-d" type="number" min="1" max="120" value="45"></div>\n'
Lc += '    <div class="field"><label for="lc-r">Electricity per kWh</label><input id="lc-r" type="number" min="0.05" step="0.01" value="0.17"></div>\n'
Lc += '  </div>\n'
Lc += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="lc-out">&#8211;</span><span class="result-unit">electricity for the season</span></div>\n'
Lc += '  <div class="stats">\n'
Lc += '    <div class="stat"><b id="lc-s1">&#8211;</b><span>per day lit</span></div>\n'
Lc += '    <div class="stat"><b id="lc-s2">&#8211;</b><span>LED swap would save</span></div>\n'
Lc += '    <div class="stat"><b id="lc-s3">&#8211;</b><span>watts when all lit</span></div>\n'
Lc += '  </div>\n'
Lc += '  <div class="tool-note" id="lc-note"></div>\n'
Lc += '  <button type="button" class="tool-btn" id="lc-share">Share my light bill</button>\n'
Lc += '</div>\n'
Lc += '<script>(function(){\n'
Lc += "var N=document.getElementById('lc-n'),T=document.getElementById('lc-t'),H=document.getElementById('lc-h'),D=document.getElementById('lc-d'),R=document.getElementById('lc-r');\n"
Lc += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Lc += "function calc(){\n"
Lc += "  var n=Math.max(1,Math.round(num(N))),w=num(T),h=num(H),d=num(D),r=num(R);\n"
Lc += "  var kwh=n*w*h*d/1000, cost=kwh*r;\n"
Lc += "  var ledW=(w>100)?25:5, ledKwh=n*ledW*h*d/1000, save=Math.max(0,(kwh-ledKwh))*r;\n"
Lc += "  var d1=Math.round(cost*100)/100, d2=Math.round(cost/d*100)/100, d3=Math.round(save*100)/100;\n"
Lc += "  document.getElementById('lc-out').textContent='$'+d1;\n"
Lc += "  document.getElementById('lc-s1').textContent='$'+d2;\n"
Lc += "  document.getElementById('lc-s2').textContent='$'+d3;\n"
Lc += "  document.getElementById('lc-s3').textContent=(n*w)+' W';\n"
Lc += "  var msg='That is the whole season of light for the price of one fancy coffee - or not, if you are running old C9 incandescents, which pull as much as a refrigerator per string. The LED swap pays for itself in one to two seasons at six hours a night, and the bulbs stop burning out mid-December. ';\n"
Lc += "  if(w>100){msg+='Two hard rules for the big old bulbs: three strings maximum end-to-end on one plug, and check the fuse in the plug every time a whole string goes dark at once. ';}\n"
Lc += "  else{msg+='LED strings can run longer runs end-to-end because they barely warm up - but read the box, the limit is printed on it. ';}\n"
Lc += "  msg+='The timer plug costs ten dollars and answers the question nobody wants to climb the ladder to ask.';\n"
Lc += "  document.getElementById('lc-note').textContent=msg;\n"
Lc += "  document.title='Holiday lights: $'+d1+' this season - ToolDune';\n"
Lc += "}\n"
Lc += "function save(){try{localStorage.setItem('tt_lightcost',JSON.stringify({n:N.value,t:T.value,h:H.value,d:D.value,r:R.value}));}catch(e){}}\n"
Lc += "[N,T,H,D,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Lc += "var pre=false;\n"
Lc += "var qs=new URLSearchParams(location.search);\n"
Lc += "if(qs.get('n')){N.value=qs.get('n');pre=true;}\n"
Lc += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_lightcost')||'null');if(m){if(m.n){N.value=m.n;}if(m.t){T.value=m.t;}if(m.h){H.value=m.h;}if(m.d){D.value=m.d;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Lc += "calc();\n"
Lc += "document.getElementById('lc-share').addEventListener('click',function(){\n"
Lc += "  var txt='My holiday lights cost $'+document.getElementById('lc-out').textContent+' in electricity this season. Price yours:';\n"
Lc += "  var url=location.origin+location.pathname+'?n='+encodeURIComponent(N.value);\n"
Lc += "  if(navigator.share){navigator.share({title:'Holiday lights cost',text:txt,url:url}).catch(function(){});}\n"
Lc += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my light bill';},1500);}\n"
Lc += "});\n"
Lc += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: FURNFILTER ----------
Ff = 'FURNFILTER = """<div class="tool" id="tt-ff">\n'
Ff += '  <div class="fields">\n'
Ff += '    <div class="field"><label for="ff-s">Filter size on the frame (e.g. 16x25x1)</label><input id="ff-s" type="text" value="16x25x1" autocomplete="off"></div>\n'
Ff += '    <div class="field"><label for="ff-f">Change every</label><select id="ff-f"><option value="30">30 days - peak season</option><option value="60" selected>60 days</option><option value="90">90 days - light use</option></select></div>\n'
Ff += '    <div class="field"><label for="ff-c">Cost per filter</label><input id="ff-c" type="number" min="1" step="0.5" value="12"></div>\n'
Ff += '    <div class="field"><label for="ff-m">MERV rating</label><select id="ff-m"><option value="8" selected>MERV 8 - standard</option><option value="11">MERV 11 - pets, allergies</option><option value="13">MERV 13 - maximum</option></select></div>\n'
Ff += '  </div>\n'
Lc_dummy = None
Ff += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ff-out">&#8211;</span><span class="result-unit">filter cost per year</span></div>\n'
Ff += '  <div class="stats">\n'
Ff += '    <div class="stat"><b id="ff-s1">&#8211;</b><span>filters a year</span></div>\n'
Ff += '    <div class="stat"><b id="ff-s2">&#8211;</b><span>next change</span></div>\n'
Ff += '    <div class="stat"><b id="ff-s3">&#8211;</b><span>airflow honesty</span></div>\n'
Ff += '  </div>\n'
Ff += '  <div class="tool-note" id="ff-note"></div>\n'
Ff += '  <button type="button" class="tool-btn" id="ff-share">Share my filter plan</button>\n'
Ff += '</div>\n'
Ff += '<script>(function(){\n'
Ff += "var S=document.getElementById('ff-s'),FQ=document.getElementById('ff-f'),C=document.getElementById('ff-c'),M=document.getElementById('ff-m');\n"
Ff += "function calc(){\n"
Ff += "  var parts=S.value.toLowerCase().split(/[^0-9.]+/).filter(Boolean);\n"
Ff += "  var dims=parts.length>=3?(parts[0]+' x '+parts[1]+' x '+parts[2]):S.value;\n"
Ff += "  var freq=parseInt(FQ.value,10)||60,cost=parseFloat(C.value)||12,merv=parseInt(M.value,10)||8;\n"
Ff += "  var perYear=365/freq, total=perYear*cost;\n"
Ff += "  var next=new Date(Date.now()+freq*86400000);\n"
Ff += "  var names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];\n"
Lc_dummy = None
Ff += "  var d1=Math.round(total*10)/10, d2=Math.round(perYear*10)/10;\n"
Ff += "  var airflow=merv===13?'drag rises - system pays':(merv===11?'mild drag':'free flowing');\n"
Ff += "  document.getElementById('ff-out').textContent='$'+d1;\n"
Ff += "  document.getElementById('ff-s1').textContent=d2;\n"
Ff += "  document.getElementById('ff-s2').textContent=names[next.getMonth()]+' '+next.getDate();\n"
Ff += "  document.getElementById('ff-s3').textContent=airflow;\n"
Ff += "  document.getElementById('ff-note').textContent='Size '+dims+' is the nominal print - the actual frame runs about a half inch smaller on each side, so buy by the nominal number and let the frame compress its cardboard edge. MERV honesty: 8 handles dust for most homes, 11 earns its price with pets or allergies, but 13 fights the blower unless your system is rated for it - the aisle sells filtration fear, and the bill arrives as longer runtimes. The schedule is a floor, not a law: hold a filter up to a lamp, and if no light comes through, change it today regardless of the calendar.';\n"
Ff += "  document.title='Filters: $'+d1+'/year, next '+names[next.getMonth()]+' '+next.getDate()+' - ToolDune';\n"
Ff += "}\n"
Ff += "function save(){try{localStorage.setItem('tt_furnfilter',JSON.stringify({s:S.value,f:FQ.value,c:C.value,m:M.value}));}catch(e){}}\n"
Ff += "[S,C].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Ff += "[FQ,M].forEach(function(el){el.addEventListener('change',function(){calc();save();});});\n"
Ff += "var pre=false;\n"
Ff += "var qs=new URLSearchParams(location.search);\n"
Ff += "if(qs.get('f')){FQ.value=qs.get('f');pre=true;}\n"
Ff += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_furnfilter')||'null');if(m){if(m.s){S.value=m.s;}if(m.f){FQ.value=m.f;}if(m.c){C.value=m.c;}if(m.m){M.value=m.m;}}}catch(e){}}\n"
Ff += "calc();\n"
Ff += "document.getElementById('ff-share').addEventListener('click',function(){\n"
Ff += "  var txt='My furnace filters run $'+document.getElementById('ff-out').textContent+' a year at MERV '+M.value+'. Plan yours:';\n"
Ff += "  var url=location.origin+location.pathname+'?f='+encodeURIComponent(FQ.value);\n"
Ff += "  if(navigator.share){navigator.share({title:'Furnace filter plan',text:txt,url:url}).catch(function(){});}\n"
Ff += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my filter plan';},1500);}\n"
Ff += "});\n"
Ff += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: HUMIDSIZE ----------
Hm = 'HUMIDSIZE = """<div class="tool" id="tt-hs">\n'
Hm += '  <div class="fields">\n'
Hm += '    <div class="field"><label for="hs-a">Room area (sq ft)</label><input id="hs-a" type="number" min="50" max="5000" value="300"></div>\n'
Hm += '    <div class="field"><label for="hs-h">Ceiling height (ft)</label><input id="hs-h" type="number" min="7" max="14" step="0.5" value="8"></div>\n'
Hm += '    <div class="field"><label for="hs-t">How leaky is the room</label><select id="hs-t"><option value="1.3">Leaky - old windows</option><option value="1" selected>Normal</option><option value="0.75">Tight - newer build</option></select></div>\n'
Hm += '  </div>\n'
Hm += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hs-out">&#8211;</span><span class="result-unit">gallons per day needed</span></div>\n'
Hm += '  <div class="stats">\n'
Hm += '    <div class="stat"><b id="hs-s1">&#8211;</b><span>tank size to shop for</span></div>\n'
Hm += '    <div class="stat"><b id="hs-s2">&#8211;</b><span>electricity per winter</span></div>\n'
Hm += '    <div class="stat"><b id="hs-s3">&#8211;</b><span>refill times per day</span></div>\n'
Hm += '  </div>\n'
Hm += '  <div class="tool-note" id="hs-note"></div>\n'
Hm += '  <button type="button" class="tool-btn" id="hs-share">Share my humidifier size</button>\n'
Hm += '</div>\n'
Hm += '<script>(function(){\n'
Hm += "var A=document.getElementById('hs-a'),H=document.getElementById('hs-h'),T=document.getElementById('hs-t');\n"
Hm += "function calc(){\n"
Hm += "  var a=parseFloat(A.value)||300,h=parseFloat(H.value)||8,tk=parseFloat(T.value)||1;\n"
Hm += "  var gpd=a*0.0033*(h/8)*tk;\n"
Hm += "  var cls=gpd<=1.1?'1 gallon':(gpd<=1.6?'1.5 gallon':(gpd<=2.2?'2 gallon':'3 gallon plus'));\n"
Hm += "  var season=120*0.03*12*0.17;\n"
Hm += "  var refills=gpd/1;\n"
Hm += "  var d1=Math.round(gpd*100)/100, d2=Math.round(season*10)/10, d3=Math.round(refills*10)/10;\n"
Hm += "  document.getElementById('hs-out').textContent=d1;\n"
Hm += "  document.getElementById('hs-s1').textContent=cls;\n"
Hm += "  document.getElementById('hs-s2').textContent='$'+d2;\n"
Hm += "  document.getElementById('hs-s3').textContent='about '+d3;\n"
Hm += "  document.getElementById('hs-note').textContent='The rating on the box assumes a sealed room at 8-foot ceilings for the full rating period - real rooms leak, which is why the multiplier matters more than the marketing. Two honesty notes from the aisle: ultrasonic units spray fine mineral dust on everything unless you run distilled water, and the target in winter is 30-40 percent humidity, because past that the windows sweat and the window frames grow things. A built-in humidistat beats a timer - it stops when the room is done instead of when the clock says so.';\n"
Hm += "  document.title='Humidifier: '+cls+' for '+Math.round(a)+' sq ft - ToolDune';\n"
Hm += "}\n"
Hm += "function save(){try{localStorage.setItem('tt_humidsize',JSON.stringify({a:A.value,h:H.value,t:T.value}));}catch(e){}}\n"
Hm += "[A,H,T].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Hm += "var pre=false;\n"
Hm += "var qs=new URLSearchParams(location.search);\n"
Hm += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Hm += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_humidsize')||'null');if(m){if(m.a){A.value=m.a;}if(m.h){H.value=m.h;}if(m.t){T.value=m.t;}}}catch(e){}}\n"
Hm += "calc();\n"
Hm += "document.getElementById('hs-share').addEventListener('click',function(){\n"
Hm += "  var txt='My room needs a '+document.getElementById('hs-s1').textContent+' humidifier. Size yours:';\n"
Hm += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Hm += "  if(navigator.share){navigator.share({title:'Humidifier sizing',text:txt,url:url}).catch(function(){});}\n"
Hm += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my humidifier size';},1500);}\n"
Hm += "});\n"
Hm += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("LIGHTCOST", "FURNFILTER", "HUMIDSIZE"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Lc + Ff + Hm + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "batterycold": lambda args: BATTERYCOLD,',
    '    "batterycold": lambda args: BATTERYCOLD,\n'
    '    "lightcost": lambda args: LIGHTCOST,\n'
    '    "furnfilter": lambda args: FURNFILTER,\n'
    '    "humidsize": lambda args: HUMIDSIZE,')
sub(BUILD_P, '    "tiretemp": "🚗", "antifreezemix": "⛄", "batterycold": "🚨",',
    '    "tiretemp": "🚗", "antifreezemix": "⛄", "batterycold": "🚨",\n'
    '    "lightcost": "💡", "furnfilter": "🔧", "humidsize": "💧",')

P = []
d = {'slug': 'christmas-lights-cost-calculator',
     'title': 'Christmas Lights Cost Calculator - LED vs Incandescent Season Bill',
     'h1': 'Christmas Lights Cost Calculator',
     'desc': 'Strings, hours and your electric rate become the real season bill - and the exact dollar figure an LED swap saves before you climb the ladder. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'christmas lights electricity cost calculator led vs incandescent',
     'tool': 'lightcost',
     'args': {},
     'intro': ["Count your strings, pick the bulb type - mini incandescent pulls 40 watts a string, mini LED about 5, and the big C9s run 175 versus 25 - then set hours per night and your electric rate. The season bill lands in dollars, with the LED-swap saving right next to it.",
              "Retailer pages sell strings and skip the meter. This one prices the display honestly: LED pays for itself in one to two seasons at six hours a night, three-strings-per-plug is a hard rule for old C9s, and a ten-dollar timer answers the question nobody wants to climb the ladder to ask."],
     'howto': ["Count every string going up, including the ones in the attic you forgot.",
               "Match the type - the wattage per string is printed near the plug.",
               "Set the timer hours honestly; six is the national habit."],
     'faqs': [("How much does it cost to run Christmas lights?",
               "Six mini LED strings at 6 hours a night for 45 days cost well under 2 dollars at typical rates. The same count in old mini incandescents runs about 8 times that, and C9 incandescents make the meter spin like a small space heater."),
              ("Do LED Christmas lights really save money?",
               "Yes - roughly 85-90% less electricity per string, plus they run cool so they last many seasons. The payback on the price difference is typically one to two seasons of evening display use."),
              ("How many Christmas light strings can I connect?",
               "Incandescent: three strings maximum end-to-end on one circuit run - that is the printed safety limit, not a suggestion. LED: read the box, most allow more because the current is tiny and the strings stay cool."),
              ("Why did half my light string go dark?",
               "On incandescent sets, a single dead bulb or the little plug fuse breaks the circuit for everything downstream - check the fuse door in the plug first, then the bulbs nearest the dark section. LEDs fail per-bulb; the rest stay lit.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'furnace-filter-calculator',
     'title': 'Furnace Filter Calculator - Size Decoder, Yearly Cost and MERV Honesty',
     'h1': 'Furnace Filter Calculator',
     'desc': 'Decode the size on the frame, price a year of filters at your change interval, and get the MERV answer without the filtration-fear upsell. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'furnace filter size replacement schedule merv calculator',
     'tool': 'furnfilter',
     'args': {},
     'intro': ["Type the size printed on your current filter frame, pick how often you will actually change it, and set the price per filter. You get the yearly cost, the next change date, and a straight answer on MERV ratings.",
              "The filter aisle sells fear in both directions - premium MERV 13 for everyone, or 1-dollar fiberglass that filters almost nothing. The honest version: MERV 8 for dust, 11 for pets and allergies, 13 only if your system is rated for the airflow drag, which otherwise arrives on your bill as longer runtimes."],
     'howto': ["Read the nominal size off the frame edge - numbers like 16x25x1.",
               "Set the interval honestly; peak heating season is usually 30 days for 1-inch filters.",
               "Check the lamp test monthly: no light through the filter means change it now."],
     'faqs': [("What size furnace filter do I need?",
               "The nominal size printed on your current filter frame - something like 16x25x1. The actual frame is about half an inch smaller on each side; buy by the nominal number and the cardboard edge compresses to seal. If the print is gone, measure the slot and round up to the nearest nominal size."),
              ("How often should I change my furnace filter?",
               "Every 30 days in peak heating or cooling season, 60-90 in shoulder months for 1-inch filters. Pets, wildfire smoke and a dusty renovation shorten it. The calendar is a floor - hold it up to a lamp and let your eyes make the call."),
              ("What MERV rating should I use?",
               "MERV 8 for most homes, MERV 11 with pets or allergies, MERV 13 only if the system manual says it can breathe through one. Higher ratings catch smaller particles but fight the blower, and the cost shows up as longer runtimes, not on the filter price tag."),
              ("What happens if I never change the filter?",
               "Airflow drops, the blower works harder, the heat exchanger runs hotter, and in the worst case the limit switch starts short-cycling the furnace. It is the cheapest maintenance in the house and the most common cause of no-heat calls in January.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'humidifier-size-calculator',
     'title': 'Humidifier Size Calculator - Gallons Per Day for Your Room',
     'h1': 'Humidifier Size Calculator',
     'desc': 'Room area, ceiling height and how leaky the room is give the gallons-per-day rating to shop for - plus winter electricity and honest tank-refill math. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'humidifier size calculator room square feet gallons',
     'tool': 'humidsize',
     'args': {},
     'intro': ["Enter the room area, ceiling height and whether the room leaks air - old windows breathe a lot, new builds barely. The calculator gives the gallons-per-day output to shop for, the tank class on the shelf, and how many refills a day that really means.",
              "Box ratings assume a sealed room with the windows shut. This one prices reality: leaky rooms need a third more capacity, ultrasonic units dust everything with minerals unless you run distilled, and past 40 percent humidity the windows start sweating - the built-in humidistat beats any timer."],
     'howto': ["Measure the room the humidifier will actually live in, not the whole floor.",
               "Be honest about the leakiness - drafty sash windows change the answer.",
               "Shop the tank class, then check the refill width: one gallon a day is a jug a day."],
     'faqs': [("What size humidifier do I need for my room?",
               "Roughly 1 gallon per day for 300 square feet, scaling with ceiling height and air leaks. A leaky 400-square-foot bedroom can need double the rating of a tight one - the calculator prices the leaks instead of ignoring them."),
              ("What humidity should my house be in winter?",
               "30 to 40 percent. Below that, static shocks and dry throats; above it, condensation on the windows and mold risk in the corners. That ceiling is why the humidistat matters more than the run time."),
              ("Why does my ultrasonic humidifier leave white dust?",
               "The mist carries whatever is in the water - hard tap water means fine mineral dust on every surface. Distilled water stops it completely; evaporative wick units do not have this problem because the minerals stay in the wick."),
              ("Do humidifiers use a lot of electricity?",
               "No - even a whole-room unit draws less than a couple of old light bulbs, typically a few dollars over an entire winter. The real cost is the water jugs and the filter wicks, which is where the refill math earns its place.")]}
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
print("R139 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
