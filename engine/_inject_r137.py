# -*- coding: utf-8 -*-
"""R137 冬前汽车簇:tire-pressure-temperature(胎压温度补偿)+antifreeze-mix(防冻液配比)+car-battery-cold-test(电瓶冷冬风险)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: TIRETEMP ----------
Tt = 'TIRETEMP = """<div class="tool" id="tt-tpc">\n'
Tt += '  <div class="fields">\n'
Tt += '    <div class="field"><label for="tp-pl">Placard pressure (door sticker, PSI)</label><input id="tp-pl" type="number" min="20" max="60" value="33"></div>\n'
Tt += '    <div class="field"><label for="tp-tn">Temperature now (F)</label><input id="tp-tn" type="number" min="-40" max="120" value="60"></div>\n'
Tt += '    <div class="field"><label for="tp-tl">Cold night coming (F)</label><input id="tp-tl" type="number" min="-40" max="100" value="25"></div>\n'
Tt += '  </div>\n'
Tt += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tp-out">&#8211;</span><span class="result-unit">PSI to add today</span></div>\n'
Tt += '  <div class="stats">\n'
Tt += '    <div class="stat"><b id="tp-s1">&#8211;</b><span>loss from the cold snap</span></div>\n'
Tt += '    <div class="stat"><b id="tp-s2">&#8211;</b><span>gauge should read now</span></div>\n'
Tt += '    <div class="stat"><b id="tp-s3">&#8211;</b><span>if you do nothing</span></div>\n'
Tt += '  </div>\n'
Tt += '  <div class="tool-note" id="tp-note"></div>\n'
Tt += '  <button type="button" class="tool-btn" id="tp-share">Share my tire math</button>\n'
Tt += '</div>\n'
Tt += '<script>(function(){\n'
Tt += "var PL=document.getElementById('tp-pl'),TN=document.getElementById('tp-tn'),TL=document.getElementById('tp-tl');\n"
Tt += "function calc(){\n"
Tt += "  var pl=parseFloat(PL.value)||33,tn=parseFloat(TN.value)||60,tl=parseFloat(TL.value)||25;\n"
Tt += "  var ratio=(tn+459.67)/(tl+459.67);\n"
Tt += "  var loss=pl-pl/ratio;\n"
Tt += "  var lowAfter=pl/ratio;\n"
Tt += "  var d1=Math.round(loss*10)/10,d2=Math.round((pl+loss)*10)/10,d3=Math.round(lowAfter*10)/10;\n"
Tt += "  document.getElementById('tp-out').textContent=Math.max(0,Math.round(loss*10)/10);\n"
Tt += "  document.getElementById('tp-s1').textContent=d1+' PSI';\n"
Tt += "  document.getElementById('tp-s2').textContent=d2+' PSI';\n"
Tt += "  document.getElementById('tp-s3').textContent=d3+' PSI';\n"
Tt += "  document.getElementById('tp-note').textContent='The gas law in your tires: pressure falls about 1 PSI per 10 degrees F of temperature drop, which is why the TPMS light loves the first cold morning of the season. The math is exact for the pressure change - what it cannot know is that your gauge or the gas station hose may read half a pound off, so aim near the number, not for it. Check pressure monthly through winter, cold tires in the morning, and never bleed a hot tire down to the placard number - it will be genuinely low when it cools.';\n"
Tt += "  document.title='Add '+Math.max(0,Math.round(loss*10)/10)+' PSI before the cold - ToolDune';\n"
Tt += "}\n"
Tt += "function save(){try{localStorage.setItem('tt_tiretemp',JSON.stringify({p:PL.value,n:TN.value,l:TL.value}));}catch(e){}}\n"
Tt += "[PL,TN,TL].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Tt += "var pre=false;\n"
Tt += "var qs=new URLSearchParams(location.search);\n"
Tt += "if(qs.get('l')){TL.value=qs.get('l');pre=true;}\n"
Tt += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_tiretemp')||'null');if(m){if(m.p){PL.value=m.p;}if(m.n){TN.value=m.n;}if(m.l){TL.value=m.l;}}}catch(e){}}\n"
Tt += "calc();\n"
Tt += "document.getElementById('tp-share').addEventListener('click',function(){\n"
Tt += "  var txt='The cold snap tonight costs my tires '+document.getElementById('tp-s1').textContent+' - adding it now. Check yours:';\n"
Tt += "  var url=location.origin+location.pathname+'?l='+encodeURIComponent(TL.value);\n"
Tt += "  if(navigator.share){navigator.share({title:'Tire pressure vs temperature',text:txt,url:url}).catch(function(){});}\n"
Tt += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my tire math';},1500);}\n"
Tt += "});\n"
Tt += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: ANTIFREEZEMIX ----------
Af = 'ANTIFREEZEMIX = """<div class="tool" id="tt-afm">\n'
Af += '  <div class="fields">\n'
Af += '    <div class="field"><label for="af-c">Cooling system capacity (quarts)</label><input id="af-c" type="number" min="4" max="40" value="12"></div>\n'
Af += '    <div class="field"><label for="af-m">Target mix (ethylene glycol)</label><select id="af-m"><option value="30">30% - protects to +4 F</option><option value="40">40% - protects to -12 F</option><option value="50" selected>50% - protects to -34 F</option><option value="60">60% - protects to -62 F</option></select></div>\n'
Af += '  </div>\n'
Af += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="af-out">&#8211;</span><span class="result-unit">quarts of concentrate</span></div>\n'
Af += '  <div class="stats">\n'
Af += '    <div class="stat"><b id="af-s1">&#8211;</b><span>quarts distilled water</span></div>\n'
Af += '    <div class="stat"><b id="af-s2">&#8211;</b><span>freeze protection</span></div>\n'
Af += '    <div class="stat"><b id="af-s3">&#8211;</b><span>gal of 50/50 pre-mix equivalent</span></div>\n'
Af += '  </div>\n'
Af += '  <div class="tool-note" id="af-note"></div>\n'
Af += '  <button type="button" class="tool-btn" id="af-share">Share my mix math</button>\n'
Af += '</div>\n'
Af += '<script>(function(){\n'
Af += "var C=document.getElementById('af-c'),M=document.getElementById('af-m');\n"
Af += "function calc(){\n"
Af += "  var cap=parseFloat(C.value)||12,pct=parseInt(M.value,10)||50;\n"
Af += "  var conc=cap*pct/100, water=cap-conc, premix=cap/4;\n"
Af += "  var freeze={30:'+4 F',40:'-12 F',50:'-34 F',60:'-62 F'}[pct]||'-34 F';\n"
Af += "  var d1=Math.round(conc*10)/10,d2=Math.round(water*10)/10,d3=Math.round(premix*10)/10;\n"
Af += "  document.getElementById('af-out').textContent=d1;\n"
Af += "  document.getElementById('af-s1').textContent=d2+' qt';\n"
Af += "  document.getElementById('af-s2').textContent=freeze;\n"
Af += "  document.getElementById('af-s3').textContent=d3+' gal';\n"
Af += "  document.getElementById('af-note').textContent='For a fresh fill or a full drain-and-refill: that much concentrate plus distilled water hits your target mix. Never use plain tap water long-term - minerals scale up the passages. Two traps the parts-store shelf will not warn you about: above 70% concentrate the mix actually protects WORSE and moves heat worse, so more is not more; and never mix chemistry families (the old green IAT with orange/pink OAT) - they gel. If the color is unknown, a 5 dollar test strip or a full flush costs less than a cracked block.';\n"
Af += "  document.title='Mix '+pct+'%: '+d1+' qt concentrate - ToolDune';\n"
Af += "}\n"
Af += "function save(){try{localStorage.setItem('tt_afm',JSON.stringify({c:C.value,m:M.value}));}catch(e){}}\n"
Af += "[C,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Af += "var pre=false;\n"
Af += "var qs=new URLSearchParams(location.search);\n"
Af += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
Af += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_afm')||'null');if(m){if(m.c){C.value=m.c;}if(m.m){M.value=m.m;}}}catch(e){}}\n"
Af += "calc();\n"
Af += "document.getElementById('af-share').addEventListener('click',function(){\n"
Af += "  var txt='My cooling system takes '+document.getElementById('af-out').textContent+' quarts of concentrate for winter. Do yours:';\n"
Af += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value);\n"
Af += "  if(navigator.share){navigator.share({title:'Antifreeze mix math',text:txt,url:url}).catch(function(){});}\n"
Af += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my mix math';},1500);}\n"
Af += "});\n"
Af += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: BATTERYCOLD ----------
Bc = 'BATTERYCOLD = """<div class="tool" id="tt-bcw">\n'
Bc += '  <div class="fields">\n'
Bc += '    <div class="field"><label for="bc-a">Battery age (years)</label><input id="bc-a" type="number" min="0" max="12" step="0.5" value="3"></div>\n'
Bc += '    <div class="field"><label for="bc-t">Overnight low coming (F)</label><input id="bc-t" type="number" min="-40" max="60" value="20"></div>\n'
Bc += '    <div class="field"><label for="bc-h">Climate history</label><select id="bc-h"><option value="1">Mostly mild</option><option value="0.9" selected>Mixed seasons</option><option value="0.8">Mostly hot summers</option></select></div>\n'
Bc += '  </div>\n'
Bc += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bc-out">&#8211;</span><span class="result-unit">starting power available</span></div>\n'
Bc += '  <div class="stats">\n'
Bc += '    <div class="stat"><b id="bc-s1">&#8211;</b><span>cold cuts capacity to</span></div>\n'
Bc += '    <div class="stat"><b id="bc-s2">&#8211;</b><span>age and heat have left</span></div>\n'
Bc += '    <div class="stat"><b id="bc-s3">&#8211;</b><span>verdict</span></div>\n'
Bc += '  </div>\n'
Bc += '  <div class="tool-note" id="bc-note"></div>\n'
Bc += '  <button type="button" class="tool-btn" id="bc-share">Share my battery verdict</button>\n'
Bc += '</div>\n'
Bc += '<script>(function(){\n'
Bc += "var A=document.getElementById('bc-a'),T=document.getElementById('bc-t'),H=document.getElementById('bc-h');\n"
Bc += "function capAt(t){\n"
Bc += "  if(t>=80)return 1;\n"
Bc += "  if(t>=32)return 0.65+0.35*(t-32)/48;\n"
Bc += "  if(t>=0)return 0.40+0.25*(t)/32;\n"
Bc += "  return Math.max(0.20,0.40+0.25*(t)/32-(0-t)*0.001);\n"
Bc += "}\n"
Bc += "function calc(){\n"
Bc += "  var age=parseFloat(A.value)||0,low=parseFloat(T.value)||20,heat=parseFloat(H.value)||1;\n"
Bc += "  var cc=capAt(low);\n"
Bc += "  var ageF=Math.max(0.35,1-0.09*age)*heat;\n"
Bc += "  var avail=cc*ageF;\n"
Bc += "  var d1=Math.round(cc*100),d2=Math.round(ageF*100),d3=Math.round(avail*100);\n"
Bc += "  var verdict=avail>=0.55?'Should start':(avail>=0.40?'Marginal - test it':'Get it tested or replaced');\n"
Bc += "  document.getElementById('bc-out').textContent=d3+'%';\n"
Bc += "  document.getElementById('bc-s1').textContent=d1+'%';\n"
Bc += "  document.getElementById('bc-s2').textContent=d2+'%';\n"
Bc += "  document.getElementById('bc-s3').textContent=verdict;\n"
Bc += "  document.getElementById('bc-note').textContent='Batteries die on the first cold snap, not in summer: heat ages the plates all season, then cold exposes what is left - at 0 F a battery holds roughly 40% of its rated cranking power while a cold engine needs twice the torque to spin. The estimate stacks the temperature curve with age wear, and 4 years is the honest decision point in hot climates, 6 in cold ones. Any parts store will load-test it free in five minutes - cheaper than a tow, and the tow is the plan B you get when the verdict was marginal and you drove past the test.';\n"
Bc += "  document.title='Battery: '+d3+'% power at '+Math.round(low)+'F - ToolDune';\n"
Bc += "}\n"
Bc += "function save(){try{localStorage.setItem('tt_bcw',JSON.stringify({a:A.value,t:T.value,h:H.value}));}catch(e){}}\n"
Bc += "[A,T,H].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Bc += "var pre=false;\n"
Bc += "var qs=new URLSearchParams(location.search);\n"
Bc += "if(qs.get('t')){T.value=qs.get('t');pre=true;}\n"
Bc += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_bcw')||'null');if(m){if(m.a){A.value=m.a;}if(m.t){T.value=m.t;}if(m.h){H.value=m.h;}}}catch(e){}}\n"
Bc += "calc();\n"
Bc += "document.getElementById('bc-share').addEventListener('click',function(){\n"
Bc += "  var txt='At '+T.value+' F my battery has '+document.getElementById('bc-out').textContent+' of its power - verdict: '+document.getElementById('bc-s3').textContent+'. Check yours:';\n"
Bc += "  var url=location.origin+location.pathname+'?t='+encodeURIComponent(T.value);\n"
Bc += "  if(navigator.share){navigator.share({title:'Car battery cold check',text:txt,url:url}).catch(function(){});}\n"
Bc += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my battery verdict';},1500);}\n"
Bc += "});\n"
Bc += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("TIRETEMP", "ANTIFREEZEMIX", "BATTERYCOLD"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Tt + Af + Bc + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "rothtra": lambda args: ROTHTRA,',
    '    "rothtra": lambda args: ROTHTRA,\n'
    '    "tiretemp": lambda args: TIRETEMP,\n'
    '    "antifreezemix": lambda args: ANTIFREEZEMIX,\n'
    '    "batterycold": lambda args: BATTERYCOLD,')
sub(BUILD_P, '    "ssclaim": "👴", "thankcost": "🍗", "rothtra": "⚖",',
    '    "ssclaim": "👴", "thankcost": "🍗", "rothtra": "⚖",\n'
    '    "tiretemp": "🚗", "antifreezemix": "⛄", "batterycold": "🚨",')

P = []
d = {'slug': 'tire-pressure-temperature-calculator',
     'title': 'Tire Pressure Temperature Calculator - How Much PSI the Cold Takes',
     'h1': 'Tire Pressure Temperature Calculator',
     'desc': 'The first cold night costs your tires real PSI - see the exact loss, what the gauge should read today, and why the TPMS light loves November mornings. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'tire pressure drop temperature calculator cold weather psi',
     'tool': 'tiretemp',
     'args': {},
     'intro': ["Enter the placard pressure from your door sticker, today temperature, and the cold night in the forecast. The calculator applies the gas law to your tires and gives the PSI you will lose, the gauge reading to set today, and what you would wake up to if you do nothing.",
              "Forum threads argue about the 1-PSI-per-10-degrees rule while the math is sitting right there: pressure scales with absolute temperature. This calculator does the exact version for your numbers - and explains why you should never bleed a warm tire down to the placard figure."],
     'howto': ["Read the placard on the driver door jamb, not the tire sidewall max.",
               "Enter the current temperature and the cold low in the forecast.",
               "Add the shown PSI today so the placard number holds on the cold morning."],
     'faqs': [("How much does tire pressure drop in cold weather?",
               "About 1 PSI for every 10 degrees F drop - roughly 3 PSI for a 30-degree overnight. At typical 33 PSI placards that is close to 10% of your pressure, which is exactly where TPMS warnings begin for marginal tires."),
              ("Why did my TPMS light come on in the morning?",
               "Overnight cold pulled the pressure below the 25%-under-placard trigger. Driving warms the tires and the light often quits - the system is not broken, your tires are genuinely softer on cold mornings. Top up to placard."),
              ("Should I overinflate tires for winter?",
               "No - set placard pressure measured cold. The calculator shows how much to add so the placard number holds in the cold. Overinflating past it shrinks the contact patch and hurts braking on the exact surfaces you are worried about."),
              ("Is the 1 PSI per 10 degrees rule accurate?",
               "It is a good rule of thumb near passenger-car pressures; the calculator runs the exact gas-law ratio for your numbers and temperatures, which drifts from the rule at extreme cold or high pressures like light-truck ratings.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'antifreeze-mix-calculator',
     'title': 'Antifreeze Mix Calculator - Concentrate, Water and Freeze Protection',
     'h1': 'Antifreeze Mix Calculator',
     'desc': 'Cooling system capacity plus target mix gives quarts of concentrate and distilled water - with the freeze chart and the 70% trap the shelf never mentions. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'antifreeze mix ratio calculator coolant water',
     'tool': 'antifreezemix',
     'args': {},
     'intro': ["Enter your cooling system capacity (in the owner manual or a search away) and pick a target mix. The calculator splits it into quarts of glycol concentrate and distilled water, shows the freeze protection, and converts to 50/50 pre-mix gallons if you would rather buy convenience.",
              "Parts-store pages sell concentrate and stop there. This one prices the two honest traps: above 70% concentrate, protection and heat transfer both get worse - more is not more - and mixing chemistry families gels the coolant into a raid-the-hazard situation."],
     'howto': ["Find system capacity in quarts from the manual or filler-neck label.",
               "Pick the target mix for your coldest realistic night, not the record low.",
               "Buy distilled water; never mix coolant colors you cannot identify."],
     'faqs': [("What is the best antifreeze-to-water ratio?",
               "50/50 protects to about -34 F and moves heat well - the universal default. Colder climates run 60% for protection near -62 F; milder ones can run 40%. Above 70% both protection and cooling get worse, which surprises almost everyone."),
              ("Can I use 100% antifreeze in my radiator?",
               "You should not - straight glycol freezes around -37 F, warmer than a 60% mix, and carries heat noticeably worse. The water fraction is not filler; it is half the working fluid."),
              ("Is tap water okay to mix with antifreeze?",
               "Distilled is the standard - tap water brings minerals that scale the passages and shorten water-pump life. In an emergency on the roadside, tap water beats walking; flush it back to spec when you get home."),
              ("How do I know what coolant is already in the car?",
               "Color is a hint, not a promise - green is traditionally IAT, orange/pink/blue are OAT or hybrid families. If the history is unknown, test strips cost a few dollars or do a full flush; never top a system with a different chemistry family.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'car-battery-cold-test',
     'title': 'Car Battery Cold Weather Test - Will It Start Tomorrow Morning?',
     'h1': 'Car Battery Cold Weather Test',
     'desc': 'Battery age, your climate history and the overnight low give the starting power left, the cold-cut capacity curve and a plain verdict: start, test, or replace. Free.',
     'category': 'calculator',
     'keyword': 'car battery cold weather test will my battery start',
     'tool': 'batterycold',
     'args': {},
     'intro': ["Enter the battery age from the label sticker, the overnight low in the forecast, and whether your summers run hot. The estimate stacks the temperature capacity curve with age wear and gives a percentage of rated starting power - plus a plain verdict.",
              "Tow-truck dispatcher pages explain cold after the fact. This one explains the deal in advance: heat all summer quietly ages the plates, cold exposes what is left - at 0 F a battery holds about 40% of rated power while the engine needs twice the torque to spin."],
     'howto': ["Read the age from the date code sticker on the battery case.",
               "Enter the forecast low for the next cold night.",
               "Marginal verdict means get the free parts-store load test this week, not eventually."],
     'faqs': [("Why do car batteries die in cold weather?",
               "They were already dying - summer heat boils off fluid and corrodes the plates, and the first cold morning collects the debt: available cranking power falls to roughly 65% at freezing and 40% at 0 F while cold oil makes the engine harder to crank. The failure looks sudden; the slide was all season."),
              ("How long should a car battery last?",
               "Three to five years in hot climates, five to seven in cold ones - heat is the killer, which is why the calendar depends on where you park. Past four years, a fall load test turns a surprise into a scheduled errand."),
              ("How can I test my battery at home?",
               "Headlights on a cold morning are the folk test - bright that dim when cranking means marginal. The real answer is a load test: every major parts store runs one free in minutes, no purchase required, and it measures what the folk test guesses."),
              ("Can a battery be fine but fail in the cold?",
               "That is the normal pattern - it cranks fine at 60 F with half its capacity gone, because warm engines barely ask anything of it. Capacity is relative; the cold snaps the balance. The calculator shows both sides of that ledger for your numbers.")]}
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
print("R137 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
