# -*- coding: utf-8 -*-
"""R128 秋季断电/取暖前哨簇:space-heater-cost-calculator + generator-size-calculator + power-outage-food-calculator
规则:JS 禁反斜杠u转义(R120)、模板与注释零反斜杠序列(R121/R125)、emoji 老码位(U6.0)
"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

H = 'HEATCOST = """<div class="tool" id="tt-sh">\n'
H += '  <div class="fields">\n'
H += '    <div class="field"><label for="sh-w">Heater wattage</label><select id="sh-w"><option value="750">750 W - low</option><option value="1500" selected>1500 W - standard</option><option value="2000">2000 W - large</option></select></div>\n'
H += '    <div class="field"><label for="sh-h">Hours per day</label><input type="number" id="sh-h" min="0.5" max="24" step="0.5" placeholder="8"></div>\n'
H += '    <div class="field"><label for="sh-r">Your price per kWh</label><input type="number" id="sh-r" min="0.03" max="1" step="0.01" placeholder="0.17"></div>\n'
H += '  </div>\n'
H += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sh-out">&#8211;</span><span class="result-unit">per day</span></div>\n'
H += '  <div class="stats">\n'
H += '    <div class="stat"><b id="sh-s1">&#8211;</b><span>per 30-day month</span></div>\n'
H += '    <div class="stat"><b id="sh-s2">&#8211;</b><span>kWh burned per day</span></div>\n'
H += '    <div class="stat"><b id="sh-s3">&#8211;</b><span>per hour of running</span></div>\n'
H += '  </div>\n'
H += '  <div class="tool-note" id="sh-note"></div>\n'
H += '  <button type="button" class="tool-btn" id="sh-share">Share my heater cost</button>\n'
H += '</div>\n'
H += '<script>(function(){\n'
H += "var W=document.getElementById('sh-w'),HR=document.getElementById('sh-h'),R=document.getElementById('sh-r');\n"
H += "function calc(){\n"
H += "  var w=parseFloat(W.value)||1500,h=parseFloat(HR.value)||0,r=parseFloat(R.value)||0.17;\n"
H += "  if(h<0.5){h=0.5;}if(r<0.03){r=0.03;}\n"
H += "  var kwh=w/1000*h;\n"
H += "  var day=kwh*r;\n"
H += "  document.getElementById('sh-out').textContent='$'+day.toFixed(2);\n"
H += "  document.getElementById('sh-s1').textContent='$'+(day*30).toFixed(0);\n"
H += "  document.getElementById('sh-s2').textContent=kwh.toFixed(1);\n"
H += "  document.getElementById('sh-s3').textContent='$'+(w/1000*r).toFixed(2);\n"
H += "  document.getElementById('sh-note').textContent='The arithmetic: watts divided by 1000 times hours is kWh, times your tariff is money - a standard 1500 W heater burns 1.5 kWh every hour it runs. The uncomfortable truth is that electric resistance heat is the most expensive kind, so the trick is heating the person and the room, not the house: close the door, run it where you sit, and let the thermostat keep the rest of the home cooler. Safety is not optional: three feet of clearance, never an extension cord or power strip, and buy one with a tip-over switch - space heaters lead the home-fire list every winter.';\n"
H += "  document.title='$'+day.toFixed(2)+' a day to run - ToolDune';\n"
H += "}\n"
H += "function save(){try{localStorage.setItem('tt_heatcost',JSON.stringify({w:W.value,h:HR.value,r:R.value}));}catch(e){}}\n"
H += "W.addEventListener('change',function(){calc();save();});HR.addEventListener('input',function(){calc();save();});R.addEventListener('input',function(){calc();save();});\n"
H += "var pre=false;\n"
H += "var qs=new URLSearchParams(location.search);\n"
H += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
H += "if(qs.get('h')){HR.value=qs.get('h');pre=true;}\n"
H += "if(qs.get('r')){R.value=qs.get('r');pre=true;}\n"
H += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_heatcost')||'null');if(m){if(m.w){W.value=m.w;}if(m.h){HR.value=m.h;}if(m.r){R.value=m.r;}pre=true;}}catch(e){}}\n"
H += "calc();\n"
H += "document.getElementById('sh-share').addEventListener('click',function(){\n"
H += "  var txt='Running the space heater '+HR.value+' hours a day costs $'+document.getElementById('sh-out').textContent.replace('$','')+'/day - see yours:';\n"
H += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value)+'&h='+encodeURIComponent(HR.value)+'&r='+encodeURIComponent(R.value);\n"
H += "  if(navigator.share){navigator.share({title:'Space heater running cost',text:txt,url:url}).catch(function(){});}\n"
H += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my heater cost';},1500);}\n"
H += "});\n"
H += "})();\n</script>\n\"\"\"\n\n"

G = 'GENSIZE = """<div class="tool" id="tt-gs">\n'
G += '  <div class="fields">\n'
G += '    <div class="field"><label for="gs-r">Running watts you need</label><input type="number" id="gs-r" min="100" max="20000" step="100" placeholder="1200"></div>\n'
G += '    <div class="field"><label for="gs-m">Biggest motor load</label><select id="gs-m"><option value="0">None - lights and electronics only</option><option value="1200" selected>Refrigerator</option><option value="1300">Sump pump</option><option value="1000">Furnace fan</option><option value="2000">Well pump</option><option value="3000">Window AC</option></select></div>\n'
G += '  </div>\n'
G += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gs-out">&#8211;</span><span class="result-unit">generator size</span></div>\n'
G += '  <div class="stats">\n'
G += '    <div class="stat"><b id="gs-s1">&#8211;</b><span>starting surge added</span></div>\n'
G += '    <div class="stat"><b id="gs-s2">&#8211;</b><span>with 25 percent headroom</span></div>\n'
G += '    <div class="stat"><b id="gs-s3">&#8211;</b><span>running watts entered</span></div>\n'
G += '  </div>\n'
G += '  <div class="tool-note" id="gs-note"></div>\n'
G += '  <button type="button" class="tool-btn" id="gs-share">Share my size</button>\n'
G += '</div>\n'
G += '<script>(function(){\n'
G += "var R=document.getElementById('gs-r'),M=document.getElementById('gs-m');\n"
G += "function calc(){\n"
G += "  var r=parseFloat(R.value)||0,m=parseFloat(M.value)||0;\n"
G += "  if(r<100){r=100;}\n"
G += "  var total=r+m;\n"
G += "  var rec=Math.ceil(total/500)*500;\n"
G += "  document.getElementById('gs-out').textContent=rec+' W';\n"
G += "  document.getElementById('gs-s1').textContent=m+' W';\n"
G += "  document.getElementById('gs-s2').textContent=(Math.ceil(rec*1.25/500)*500)+' W';\n"
G += "  document.getElementById('gs-s3').textContent=r+' W';\n"
G += "  document.getElementById('gs-note').textContent='Motors do not start politely: a fridge rated at 200 running watts can ask for three times that for a second, which is why the surge line exists and why undersized generators groan and stall. Size for running watts plus the single biggest motor, then buy the headroom figure if the budget allows - engines last longer at 80 percent load. Two rules outrank every watt: run it outdoors at least 20 feet from windows because the exhaust kills quietly, and connect through a transfer switch or outdoor-rated cords - never backfeed the wall socket, which can injure the line worker restoring your street.';\n"
G += "  document.title='A '+rec+' W generator - ToolDune';\n"
G += "}\n"
G += "function save(){try{localStorage.setItem('tt_gensize',JSON.stringify({r:R.value,m:M.value}));}catch(e){}}\n"
G += "R.addEventListener('input',function(){calc();save();});M.addEventListener('change',function(){calc();save();});\n"
G += "var pre=false;\n"
G += "var qs=new URLSearchParams(location.search);\n"
H2 = "if(qs.get('r')){R.value=qs.get('r');pre=true;}\n"
G += H2
G += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
G += "if(!pre){try{var mm=JSON.parse(localStorage.getItem('tt_gensize')||'null');if(mm){if(mm.r){R.value=mm.r;}if(mm.m){M.value=mm.m;}pre=true;}}catch(e){}}\n"
G += "calc();\n"
G += "document.getElementById('gs-share').addEventListener('click',function(){\n"
G += "  var txt='I need a '+document.getElementById('gs-out').textContent+' generator for the essentials. Size yours:';\n"
G += "  var url=location.origin+location.pathname+'?r='+encodeURIComponent(R.value)+'&m='+encodeURIComponent(M.value);\n"
G += "  if(navigator.share){navigator.share({title:'Generator sizing',text:txt,url:url}).catch(function(){});}\n"
G += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my size';},1500);}\n"
G += "});\n"
G += "})();\n</script>\n\"\"\"\n\n"

O = 'OUTAGEFOOD = """<div class="tool" id="tt-po">\n'
O += '  <div class="fields">\n'
O += '    <div class="field"><label for="po-h">Power out for (hours)</label><input type="number" id="po-h" min="0.5" max="240" step="0.5" placeholder="6"></div>\n'
O += '    <div class="field"><label for="po-f">Freezer was</label><select id="po-f"><option value="full" selected>Full - 48 h keeps</option><option value="half">Half full - 24 h keeps</option></select></div>\n'
O += '    <div class="field"><label for="po-o">Fridge door stayed</label><select id="po-o"><option value="closed" selected>Closed</option><option value="opened">Opened</option></select></div>\n'
O += '  </div>\n'
O += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="po-out">&#8211;</span><span class="result-unit">verdict</span></div>\n'
O += '  <div class="stats">\n'
O += '    <div class="stat"><b id="po-s1">&#8211;</b><span>fridge holds</span></div>\n'
O += '    <div class="stat"><b id="po-s2">&#8211;</b><span>freezer holds</span></div>\n'
O += '    <div class="stat"><b id="po-s3">&#8211;</b><span>margin remaining</span></div>\n'
O += '  </div>\n'
O += '  <div class="tool-note" id="po-note"></div>\n'
O += '  <button type="button" class="tool-btn" id="po-share">Share the verdict</button>\n'
O += '</div>\n'
O += '<script>(function(){\n'
O += "var HR=document.getElementById('po-h'),F=document.getElementById('po-f'),OP=document.getElementById('po-o');\n"
O += "function calc(){\n"
O += "  var h=parseFloat(HR.value)||0,f=F.value,o=OP.value;\n"
O += "  var fl=(f==='full')?48:24;\n"
O += "  var fridgeOk=h<4&&o==='closed';\n"
O += "  var freeOk=h<fl;\n"
O += "  var margin=Math.max(0,Math.round(Math.min(4,fl)-h));\n"
O += "  var v;\n"
O += "  if(fridgeOk&&freeOk){v='Keep it all';}\n"
O += "  else if(freeOk){v='Fridge: toss perishables';}\n"
O += "  else{v='Toss thawed food';}\n"
O += "  document.getElementById('po-out').textContent=v;\n"
O += "  document.getElementById('po-s1').textContent='4 h';\n"
O += "  document.getElementById('po-s2').textContent=fl+' h';\n"
O += "  document.getElementById('po-s3').textContent=margin+' h';\n"
O += "  document.getElementById('po-note').textContent='The federal lines: an unopened fridge keeps food safe about 4 hours, a full freezer 48, a half freezer 24 - a freezer packed with jugs of water is cheap insurance. After the limit, refrigerated perishables - meat, dairy, leftovers, cut fruit - go to the bin, no sniff test, because the bacteria that matter leave no smell. Thawed food still holding ice crystals can be refrozen safely; anything slimy, warm or ballooning the packaging cannot. When in doubt, throw it out - the groceries are cheaper than the hospital.';\n"
O += "  document.title='Power out '+h+' h: '+v+' - ToolDune';\n"
O += "}\n"
O += "function save(){try{localStorage.setItem('tt_outagefood',JSON.stringify({h:HR.value,f:F.value,o:OP.value}));}catch(e){}}\n"
O += "HR.addEventListener('input',function(){calc();save();});F.addEventListener('change',function(){calc();save();});OP.addEventListener('change',function(){calc();save();});\n"
O += "var pre=false;\n"
O += "var qs=new URLSearchParams(location.search);\n"
O += "if(qs.get('h')){HR.value=qs.get('h');pre=true;}\n"
O += "if(qs.get('f')){F.value=qs.get('f');pre=true;}\n"
O += "if(qs.get('o')){OP.value=qs.get('o');pre=true;}\n"
O += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_outagefood')||'null');if(m){if(m.h){HR.value=m.h;}if(m.f){F.value=m.f;}if(m.o){OP.value=m.o;}pre=true;}}catch(e){}}\n"
O += "calc();\n"
O += "document.getElementById('po-share').addEventListener('click',function(){\n"
O += "  var txt='Power was out '+HR.value+' hours - verdict: '+document.getElementById('po-out').textContent+'. Check yours:';\n"
O += "  var url=location.origin+location.pathname+'?h='+encodeURIComponent(HR.value)+'&f='+encodeURIComponent(F.value)+'&o='+encodeURIComponent(OP.value);\n"
O += "  if(navigator.share){navigator.share({title:'Power outage food check',text:txt,url:url}).catch(function(){});}\n"
O += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share the verdict';},1500);}\n"
O += "});\n"
O += "})();\n</script>\n\"\"\"\n\n"

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

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', H + G + O + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "cactusbloom": lambda args: CACTUSBLOOM,',
    '    "cactusbloom": lambda args: CACTUSBLOOM,\n'
    '    "heatcost": lambda args: HEATCOST,\n'
    '    "gensize": lambda args: GENSIZE,\n'
    '    "outagefood": lambda args: OUTAGEFOOD,')
sub(BUILD_P, '    "frostplan": "\u2744", "bulbspace": "\U0001F337", "cactusbloom": "\U0001F335",',
    '    "frostplan": "\u2744", "bulbspace": "\U0001F337", "cactusbloom": "\U0001F335",\n'
    '    "heatcost": "\u2668", "gensize": "\u26a1", "outagefood": "\U0001F354",')

P = []
d1 = {'slug': 'space-heater-cost-calculator',
      'title': 'Space Heater Cost Calculator - Per Hour, Day and Month',
      'h1': 'Space Heater Cost Calculator',
      'desc': 'What does a space heater cost to run? Wattage times hours times your electricity price gives the per-hour, daily and monthly cost - with the safety list. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'space heater cost per hour calculator 1500 watt running cost',
      'tool': 'heatcost',
      'args': {},
      'intro': ["Pick the heater wattage, hours per day and your electricity price. The calculator gives the cost per hour, per day and per 30-day month - a 1500 W heater burns 1.5 kWh every hour it runs, which adds up faster than most bills suggest.",
               "Utility blogs print tables for their own tariffs. This one uses your price and your hours, then says the quiet part: electric resistance heat is the priciest kind, so the strategy is heating the room and the person - not competing with the whole-house thermostat."],
      'howto': ["Read the wattage off the heater label - 1500 W is the standard setting.",
                "Enter honest hours: the evenings you actually sit in that room.",
                "Take your price per kWh from the bill, and read the month figure sitting down."],
      'faqs': [("How much does a 1500 W space heater cost per hour?", "At the typical 17 cents per kWh, about 26 cents an hour - 1.5 kWh times the tariff. Eight evening hours a day lands near 2 dollars, and a cold month of that habit approaches 60 dollars per heater."),
               ("Is it cheaper to run a space heater or the furnace?", "One heater heating one occupied room usually beats the furnace; three heaters running all day do not. The crossover is simple - the heater wins when you would otherwise heat empty rooms, and loses the moment it runs everywhere at once."),
               ("Do space heaters use a lot of electricity?", "Yes - 1500 W is comparable to a microwave that runs for hours. That is why the honest strategy is zone heating: close doors, heat the room you are in, and turn the central thermostat down while you do it."),
               ("What are the space heater safety rules?", "Three feet of clearance from anything flammable, never on an extension cord or power strip, on a hard level floor, switched off when you sleep or leave - and buy a unit with a tip-over switch, because space heaters head the home-fire statistics every single winter.")]}
P.append("    pages.append(%r)\n" % (d1,))

d2 = {'slug': 'generator-size-calculator',
      'title': 'Generator Size Calculator - Running Watts Plus the Biggest Motor',
      'h1': 'Generator Size Calculator',
      'desc': 'What size generator do you need? Your running watts plus the largest motor surge give the right size in watts - with headroom and the two safety rules that outrank watts. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'what size generator do i need calculator running starting watts home',
      'tool': 'gensize',
      'args': {},
      'intro': ["Add up the running watts of what must stay on - fridge, lights, phone chargers, the furnace fan - then pick the biggest motor on the list. The calculator adds the starting surge, rounds to a real generator size, and shows the headroom figure that buys a longer engine life.",
               "Generator dealers size you up to the biggest inverter on the lot. The physics is simpler: motors ask three times their running watts for a second when they start, and everything else is arithmetic. Size for the surge, not for the sales pitch."],
      'howto': ["List what must run in an outage and add the running watts from each label or the manual.",
                "Pick the single biggest motor - fridge, sump pump, well pump or AC.",
                "Buy the size shown, or the headroom figure if the budget allows."],
      'faqs': [("What size generator for a house fridge and lights?", "A fridge (200 W running, 600+ starting) with lights, internet and phone charging lands around 2,000-2,500 W - the calculator adds your exact motor surge to your running total. That is inverter territory: quiet, clean power for electronics, sipping fuel."),
               ("Why do motors need more watts to start?", "An electric motor is briefly a stalled coil at switch-on, drawing two to three times its running current for under a second. A generator that cannot deliver that surge stalls - which is why the size is running watts plus the biggest motor, not just the sum of the labels."),
               ("Should I buy a generator with headroom?", "Yes if the budget allows: engines last longest around 80 percent load, headroom covers the appliance you forgot, and a lightly loaded big generator wastes fuel. The 25 percent figure shown is the sweet spot between those."),
               ("Where should a portable generator run?", "Outdoors only, at least 20 feet from any window or vent, exhaust pointed away - carbon monoxide kills quietly and quickly indoors, garages included. And connect appliances by cord or a transfer switch, never by backfeeding a wall outlet, which can electrocute the utility worker restoring your street.")]}
P.append("    pages.append(%r)\n" % (d2,))

d3 = {'slug': 'power-outage-food-calculator',
      'title': 'Power Outage Food Calculator - Is the Fridge Still Safe?',
      'h1': 'Power Outage Food Calculator',
      'desc': 'How long is food safe when the power is out? Hours out, freezer fullness and the fridge door give the federal 4-hour and 48-hour verdict: keep it, toss the fridge, or bin the thawed. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'how long is food good in fridge without power power outage food safety hours',
      'tool': 'outagefood',
      'args': {},
      'intro': ["Enter how long the power was out, whether the freezer was full, and whether the fridge stayed shut. The calculator applies the federal food-safety lines - 4 hours for an unopened fridge, 48 for a full freezer, 24 for a half one - and returns one plain verdict.",
               "Outage articles bury the numbers in paragraphs while you are standing in front of the fridge with a flashlight. This one is the chart as a decision: keep it all, clear the fridge, or bin everything thawed - with the refreeze rule and the when-in-doubt clause attached."],
      'howto': ["Enter the outage hours - round up, be honest about door openings.",
                "Say how packed the freezer was; a full one simply holds cold longer.",
                "Follow the verdict: ice-crystal food refreezes, warm or slimy never keeps."],
      'faqs': [("How long is food safe in the fridge without power?", "About 4 hours unopened - that is the federal line for a fridge holding 4 C. Every opening trades cold air for room air, so after an hour of peeking treat the clock as done. Past 4 hours, meat, dairy, leftovers and cut fruit go to the bin without a sniff test."),
               ("How long does a freezer keep food frozen without power?", "A full freezer holds 48 hours, a half-full one 24 - a freezer packed with water jugs is the cheapest insurance going. Food that still has ice crystals can be refrozen safely; anything thawed to room temperature and held above 4 C is a toss."),
               ("Can I refreeze food that thawed in an outage?", "If it still has ice crystals and feels refrigerator-cold, yes - quality dips, safety holds. Anything slimy, warm, or ballooning its packaging is gone, and the rule that outranks all of them: when in doubt, throw it out. The groceries are cheaper than the hospital."),
               ("What should I do to prepare the fridge for a storm?", "Freeze water bottles tonight - they extend the hold and become drinking water. Group the freezer into a tight block so it self-insulates, know where the fridge thermometer sits, and skip the grocery run the day the storm lands: a half-empty fridge is a short clock.")]}
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
print("R128 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
