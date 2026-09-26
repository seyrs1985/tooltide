# -*- coding: utf-8 -*-
"""R130 断电/取暖簇延伸三页:ups-runtime(电池Wh模型)+generator-fuel(0.18系数)+electric-vs-gas-heating(每百万Btu对比)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: UPSRUN ----------
U = 'UPSRUN = """<div class="tool" id="tt-ups">\n'
U += '  <div class="fields">\n'
U += '    <div class="field"><label for="ups-va">UPS capacity</label><select id="ups-va"><option value="300">300 VA</option><option value="450">450 VA</option><option value="600">600 VA</option><option value="850">850 VA</option><option value="1000" selected>1000 VA</option><option value="1500">1500 VA</option><option value="2200">2200 VA</option></select></div>\n'
U += '    <div class="field"><label for="ups-w">Load on the UPS (watts)</label><input id="ups-w" type="number" min="10" max="3000" value="180"></div>\n'
U += '    <div class="field"><label for="ups-age">Battery age</label><select id="ups-age"><option value="1" selected>Under 1 year</option><option value="0.85">1 to 3 years</option><option value="0.7">Over 3 years</option></select></div>\n'
U += '  </div>\n'
U += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ups-out">&#8211;</span><span class="result-unit">minutes of runtime</span></div>\n'
U += '  <div class="stats">\n'
U += '    <div class="stat"><b id="ups-s1">&#8211;</b><span>power ceiling</span></div>\n'
U += '    <div class="stat"><b id="ups-s2">&#8211;</b><span>load vs ceiling</span></div>\n'
U += '    <div class="stat"><b id="ups-s3">&#8211;</b><span>battery age factor</span></div>\n'
U += '  </div>\n'
U += '  <div class="tool-note" id="ups-note"></div>\n'
U += '  <button type="button" class="tool-btn" id="ups-share">Share my runtime estimate</button>\n'
U += '</div>\n'
U += '<script>(function(){\n'
U += "var VA=document.getElementById('ups-va'),W=document.getElementById('ups-w'),A=document.getElementById('ups-age');\n"
U += "function calc(){\n"
U += "  var va=parseInt(VA.value,10),w=parseFloat(W.value),af=parseFloat(A.value);\n"
U += "  if(!(w>0)){w=10;}\n"
U += "  var wmax=Math.round(va*0.6),pct=Math.round(w/wmax*100);\n"
U += "  document.getElementById('ups-s1').textContent=wmax+' W';\n"
U += "  document.getElementById('ups-s2').textContent=pct+'%';\n"
U += "  document.getElementById('ups-s3').textContent=af;\n"
U += "  if(w>wmax){\n"
U += "    document.getElementById('ups-out').textContent='over cap';\n"
U += "    document.getElementById('ups-note').textContent='This load is '+pct+'% of what the UPS can even power, so it will cut out immediately. Move some devices to a wall socket or step up to a bigger unit - no battery lasts when the inverter is already at its ceiling.';\n"
U += "    document.title='UPS over capacity - ToolDune';\n"
U += "    return;\n"
U += "  }\n"
U += "  var min=Math.round(va*7.65/w*af);\n"
U += "  document.getElementById('ups-out').textContent=min;\n"
U += "  document.getElementById('ups-note').textContent='The model: consumer UPS units carry roughly 0.15 Wh of battery per VA of rating and about 85% of it is deliverable, stretched or shrunk by battery age. Treat the answer as plus or minus a third - runtime is set by the battery, not the VA badge. A 3-year-old battery has already lost a chunk of itself, so run the self-test twice a year. For a work setup the target is not hours - it is 5 to 10 clean minutes to save everything and shut down; the generator or the outage plan covers the rest.';\n"
U += "  document.title='UPS about '+min+' min at '+Math.round(w)+' W - ToolDune';\n"
U += "}\n"
U += "function save(){try{localStorage.setItem('tt_ups',JSON.stringify({v:VA.value,w:W.value,a:A.value}));}catch(e){}}\n"
U += "VA.addEventListener('change',function(){calc();save();});\n"
U += "W.addEventListener('input',function(){calc();save();});\n"
U += "A.addEventListener('change',function(){calc();save();});\n"
U += "var pre=false;\n"
U += "var qs=new URLSearchParams(location.search);\n"
U += "if(qs.get('va')){VA.value=qs.get('va');pre=true;}\n"
U += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
U += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
U += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_ups')||'null');if(m){if(m.v){VA.value=m.v;}if(m.w){W.value=m.w;}if(m.a){A.value=m.a;}pre=true;}}catch(e){}}\n"
U += "calc();\n"
U += "document.getElementById('ups-share').addEventListener('click',function(){\n"
U += "  var txt='My UPS should hold about '+document.getElementById('ups-out').textContent+' minutes at '+W.value+' W. Estimate yours:';\n"
U += "  var url=location.origin+location.pathname+'?va='+encodeURIComponent(VA.value)+'&w='+encodeURIComponent(W.value)+'&a='+encodeURIComponent(A.value);\n"
U += "  if(navigator.share){navigator.share({title:'UPS runtime estimate',text:txt,url:url}).catch(function(){});}\n"
U += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my runtime estimate';},1500);}\n"
U += "});\n"
U += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: GENFUEL ----------
G = 'GENFUEL = """<div class="tool" id="tt-genfuel">\n'
G += '  <div class="fields">\n'
G += '    <div class="field"><label for="gf-kw">Generator size</label><select id="gf-kw"><option value="2">2000 W inverter</option><option value="3.5">3500 W</option><option value="5" selected>5000 W</option><option value="7.5">7500 W</option><option value="10">10000 W</option></select></div>\n'
G += '    <div class="field"><label for="gf-load">Average load</label><select id="gf-load"><option value="0.25">25% - fridge and lights</option><option value="0.5" selected>50% - fridge, lights, TV</option><option value="0.75">75% - plus space heater</option><option value="1">100% - everything it has</option></select></div>\n'
G += '    <div class="field"><label for="gf-h">Outage hours to cover</label><input id="gf-h" type="number" min="1" max="240" value="24"></div>\n'
G += '    <div class="field"><label for="gf-p">Gas price per gallon</label><input id="gf-p" type="number" min="0.5" step="0.05" value="3.20"></div>\n'
G += '  </div>\n'
G += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gf-out">&#8211;</span><span class="result-unit">gallons to have on hand</span></div>\n'
G += '  <div class="stats">\n'
G += '    <div class="stat"><b id="gf-s1">&#8211;</b><span>burn rate per hour</span></div>\n'
G += '    <div class="stat"><b id="gf-s2">&#8211;</b><span>fuel cost for the outage</span></div>\n'
G += '    <div class="stat"><b id="gf-s3">&#8211;</b><span>5-gallon cans to fill</span></div>\n'
G += '  </div>\n'
G += '  <div class="tool-note" id="gf-note"></div>\n'
G += '  <button type="button" class="tool-btn" id="gf-share">Share my fuel plan</button>\n'
G += '</div>\n'
G += '<script>(function(){\n'
G += "var KW=document.getElementById('gf-kw'),LD=document.getElementById('gf-load'),H=document.getElementById('gf-h'),P=document.getElementById('gf-p');\n"
G += "function calc(){\n"
G += "  var kw=parseFloat(KW.value),ld=parseFloat(LD.value),h=parseFloat(H.value),p=parseFloat(P.value);\n"
G += "  if(!(h>0)){h=1;}\n"
G += "  if(!(p>0)){p=0;}\n"
G += "  var gph=kw*ld*0.18,gal=gph*h,cost=gal*p,cans=Math.ceil(gal/5);\n"
G += "  var g1=Math.round(gal*10)/10,g2=Math.round(cost*10)/10;\n"
G += "  document.getElementById('gf-out').textContent=g1;\n"
G += "  document.getElementById('gf-s1').textContent=(Math.round(gph*100)/100)+' gal/h';\n"
G += "  document.getElementById('gf-s2').textContent='$'+g2;\n"
G += "  document.getElementById('gf-s3').textContent=cans;\n"
G += "  document.getElementById('gf-note').textContent='The burn rate is the field rule of thumb - kilowatts times load times 0.18 gallons per hour - and real tanks land within a quarter of it either way. An inverter model in eco mode can halve it at light load; an old contractor unit under the same load drinks more. Store no more than 5 gallons of gasoline and rotate it with stabilizer, never refuel a hot or running generator, keep the unit 20 feet from the house, and never backfeed power into a wall outlet - the line workers downstream are the reason.';\n"
G += "  document.title='Generator fuel: '+g1+' gal over '+h+' h ($'+g2+') - ToolDune';\n"
G += "}\n"
G += "function save(){try{localStorage.setItem('tt_genfuel',JSON.stringify({k:KW.value,l:LD.value,h:H.value,p:P.value}));}catch(e){}}\n"
G += "KW.addEventListener('change',function(){calc();save();});\n"
G += "LD.addEventListener('change',function(){calc();save();});\n"
G += "H.addEventListener('input',function(){calc();save();});\n"
G += "P.addEventListener('input',function(){calc();save();});\n"
G += "var pre=false;\n"
G += "var qs=new URLSearchParams(location.search);\n"
G += "if(qs.get('k')){KW.value=qs.get('k');pre=true;}\n"
G += "if(qs.get('l')){LD.value=qs.get('l');pre=true;}\n"
G += "if(qs.get('h')){H.value=qs.get('h');pre=true;}\n"
G += "if(qs.get('p')){P.value=qs.get('p');pre=true;}\n"
G += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_genfuel')||'null');if(m){if(m.k){KW.value=m.k;}if(m.l){LD.value=m.l;}if(m.h){H.value=m.h;}if(m.p){P.value=m.p;}pre=true;}}catch(e){}}\n"
G += "calc();\n"
G += "document.getElementById('gf-share').addEventListener('click',function(){\n"
G += "  var txt='Covering '+H.value+' hours takes about '+document.getElementById('gf-out').textContent+' gallons of gas for my generator. Plan yours:';\n"
G += "  var url=location.origin+location.pathname+'?k='+encodeURIComponent(KW.value)+'&l='+encodeURIComponent(LD.value)+'&h='+encodeURIComponent(H.value)+'&p='+encodeURIComponent(P.value);\n"
G += "  if(navigator.share){navigator.share({title:'Generator fuel plan',text:txt,url:url}).catch(function(){});}\n"
G += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my fuel plan';},1500);}\n"
G += "});\n"
G += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: HEATCMP ----------
Hc = 'HEATCMP = """<div class="tool" id="tt-hcmp">\n'
Hc += '  <div class="fields">\n'
Hc += '    <div class="field"><label for="hc-e">Electric price per kWh</label><input id="hc-e" type="number" min="0.01" step="0.01" value="0.17"></div>\n'
Hc += '    <div class="field"><label for="hc-g">Gas price per therm</label><input id="hc-g" type="number" min="0.1" step="0.05" value="1.60"></div>\n'
Hc += '    <div class="field"><label for="hc-f">Furnace efficiency</label><select id="hc-f"><option value="0.8">80% - older unit</option><option value="0.9">90% - standard</option><option value="0.95" selected>95% - modern condensing</option></select></div>\n'
Hc += '    <div class="field"><label for="hc-c">Heat pump COP</label><select id="hc-c"><option value="2">2.0 - deep cold</option><option value="2.5">2.5 - cold climate</option><option value="3" selected>3.0 - typical</option><option value="3.5">3.5 - mild climate</option></select></div>\n'
Hc += '  </div>\n'
Hc += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hc-out">&#8211;</span><span class="result-unit">cheapest heat source</span></div>\n'
Hc += '  <div class="stats">\n'
Hc += '    <div class="stat"><b id="hc-s1">&#8211;</b><span>electric resistance</span></div>\n'
Hc += '    <div class="stat"><b id="hc-s2">&#8211;</b><span>gas furnace</span></div>\n'
Hc += '    <div class="stat"><b id="hc-s3">&#8211;</b><span>heat pump</span></div>\n'
Hc += '  </div>\n'
Hc += '  <div class="tool-note" id="hc-note"></div>\n'
Hc += '  <button type="button" class="tool-btn" id="hc-share">Share my heat verdict</button>\n'
Hc += '</div>\n'
Hc += '<script>(function(){\n'
Hc += "var E=document.getElementById('hc-e'),Gp=document.getElementById('hc-g'),F=document.getElementById('hc-f'),C=document.getElementById('hc-c');\n"
Hc += "function calc(){\n"
Hc += "  var e=parseFloat(E.value),g=parseFloat(Gp.value),f=parseFloat(F.value),c=parseFloat(C.value);\n"
Hc += "  if(!(e>0)){e=0.01;}\n"
Hc += "  if(!(g>0)){g=0.01;}\n"
Hc += "  var r1=e*293.07, r2=g*10/f, r3=r1/c;\n"
Hc += "  var d1=Math.round(r1*10)/10, d2=Math.round(r2*10)/10, d3=Math.round(r3*10)/10;\n"
Hc += "  var names=['Electric resistance','Gas furnace','Heat pump'];\n"
Hc += "  var vals=[r1,r2,r3];\n"
Hc += "  var best=vals.indexOf(Math.min(r1,r2,r3));\n"
Hc += "  var worst=Math.max(r1,r2,r3);\n"
Hc += "  var ratio=Math.round(worst/Math.min(r1,r2,r3)*10)/10;\n"
Hc += "  document.getElementById('hc-out').textContent=names[best];\n"
Hc += "  document.getElementById('hc-s1').textContent='$'+d1;\n"
Hc += "  document.getElementById('hc-s2').textContent='$'+d2;\n"
Hc += "  document.getElementById('hc-s3').textContent='$'+d3;\n"
Hc += "  document.getElementById('hc-note').textContent='Each figure is the cost of one million BTU of delivered heat at your rates - the only fair comparison, because electricity is sold in kWh and gas in therms. Resistance electric is 100% efficient but carries the worst fuel price per heat unit; the gas figure divides by furnace efficiency, so an 80% unit pays 25% more than its nameplate suggests; the heat pump divides by its COP, the one lever in home heating that beats fuel physics outright. Use the all-in rate from your bill - delivery charges move the verdict more than the thermostat does. In mild weather the pump also cools, which is the part the gas bill never repays.';\n"
Hc += "  document.title='Heating: '+names[best]+' wins, up to '+ratio+'x cheaper - ToolDune';\n"
Hc += "}\n"
Hc += "function save(){try{localStorage.setItem('tt_hcmp',JSON.stringify({e:E.value,g:Gp.value,f:F.value,c:C.value}));}catch(e){}}\n"
Hc += "E.addEventListener('input',function(){calc();save();});\n"
Hc += "Gp.addEventListener('input',function(){calc();save();});\n"
Hc += "F.addEventListener('change',function(){calc();save();});\n"
Hc += "C.addEventListener('change',function(){calc();save();});\n"
Hc += "var pre=false;\n"
Hc += "var qs=new URLSearchParams(location.search);\n"
Hc += "if(qs.get('e')){E.value=qs.get('e');pre=true;}\n"
Hc += "if(qs.get('g')){Gp.value=qs.get('g');pre=true;}\n"
Hc += "if(qs.get('f')){F.value=qs.get('f');pre=true;}\n"
Hc += "if(qs.get('c')){C.value=qs.get('c');pre=true;}\n"
Hc += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_hcmp')||'null');if(m){if(m.e){E.value=m.e;}if(m.g){Gp.value=m.g;}if(m.f){F.value=m.f;}if(m.c){C.value=m.c;}pre=true;}}catch(e){}}\n"
Hc += "calc();\n"
Hc += "document.getElementById('hc-share').addEventListener('click',function(){\n"
Hc += "  var txt='At my rates, '+document.getElementById('hc-out').textContent+' is the cheapest heat - see all three numbers:';\n"
Hc += "  var url=location.origin+location.pathname+'?e='+encodeURIComponent(E.value)+'&g='+encodeURIComponent(Gp.value)+'&f='+encodeURIComponent(F.value)+'&c='+encodeURIComponent(C.value);\n"
Hc += "  if(navigator.share){navigator.share({title:'Electric vs gas heating',text:txt,url:url}).catch(function(){});}\n"
Hc += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my heat verdict';},1500);}\n"
Hc += "});\n"
Hc += "})();\n</script>\n\"\"\"\n\n"

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

for tok in ("upsruntime", "genfuel", "heatcmp"):
    assert tok not in io.open(TOOLS_P, encoding="utf-8").read(), tok + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    U + G + Hc + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "outagefood": lambda args: OUTAGEFOOD,',
    '    "outagefood": lambda args: OUTAGEFOOD,\n'
    '    "upsruntime": lambda args: UPSRUN,\n'
    '    "genfuel": lambda args: GENFUEL,\n'
    '    "heatcmp": lambda args: HEATCMP,')
sub(BUILD_P, '    "heatcost": "♨", "gensize": "⚡", "outagefood": "🍔",',
    '    "heatcost": "♨", "gensize": "⚡", "outagefood": "🍔",\n'
    '    "upsruntime": "🔋", "genfuel": "⛽", "heatcmp": "🔥",')

P = []
d = {'slug': 'ups-runtime-calculator',
     'title': 'UPS Runtime Calculator - How Long Will a UPS Keep You Powered?',
     'h1': 'UPS Runtime Calculator',
     'desc': 'Enter your UPS size, the load it carries and battery age to estimate real runtime in minutes - and why the VA badge lies while the battery decides. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'ups runtime calculator how long will a ups last',
     'tool': 'upsruntime',
     'args': {},
     'intro': ["Pick your UPS capacity, put in what it actually carries - a router and laptop pull around 80 watts, a desktop with monitors closer to 200 - and set the battery age. The estimate gives minutes of runtime, the power ceiling in watts, and how hard you are loading the unit.",
              "Vendor pages quote half-load runtime on a new battery in lab conditions. This one uses the field model - consumer units carry roughly 0.15 Wh of battery per VA, about 85% deliverable, aging fast after year two - and says plainly that the goal for most setups is 5 to 10 clean minutes to save work and shut down, not to keep computing through the outage."],
     'howto': ["Pick the VA rating printed on the UPS; the watt ceiling is about 60% of it.",
               "Enter the real load - add up the devices plugged in, not what you wish you had.",
               "Set battery age honestly; over three years expect a third gone even with no use."],
     'faqs': [("How long will a 1000VA UPS run a router and laptop?",
               "At about 80 watts combined, expect roughly 90 minutes from a healthy battery. The same unit at a 500 W desktop load drops to about 13 minutes - load, not the VA badge, sets the clock."),
              ("Why does my UPS die in minutes when the box said longer?",
               "The box quotes half-load runtime on a new battery. Batteries lose 20-30% of capacity by year three even unused, and loads creep up as devices accumulate - both shave the same curve."),
              ("Should I buy a UPS sized for hours of runtime?",
               "No - past 10-15 minutes each extra hour buys expensive battery banks and lithium conversions. The standard play is a short-run UPS on anything with unsaved work, and a generator or power station for duration."),
              ("Do UPS batteries need replacing?",
               "Every 3-5 years regardless of use - they age on the shelf. If the self-test beeps or runtime visibly halves, swap in the same spec; a fresh battery makes an old UPS genuinely new again.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'generator-fuel-calculator',
     'title': 'Generator Fuel Calculator - Gallons and Cost for Your Outage',
     'h1': 'Generator Fuel Calculator',
     'desc': 'Generator size, load and outage hours give the burn rate, total gallons, cost and cans to fill - with the refueling and backfeed rules that keep you safe. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'generator fuel consumption calculator gallons per hour',
     'tool': 'genfuel',
     'args': {},
     'intro': ["Size the generator, pick how hard it will actually work - a fridge, lights and router sit near 25-50% on a 5000 W unit - and set the hours you want to cover. You get the burn rate per hour, total gallons, the cost at your pump price, and how many 5-gallon cans that means.",
              "Dealer pages sell capacity and skip the fuel ledger entirely, yet fuel is what decides whether the generator is a tool or a porch ornament. The field rule - 0.18 gallons per hour per kilowatt at full load, scaled by your load - lands within a quarter of real tanks, and the page pairs it with the storage and refueling rules that prevent the classic storm-week mistakes."],
     'howto': ["Pick the generator size you own or are planning to buy or rent.",
               "Be honest about load - most homes never average above 50%.",
               "Set outage hours and your local gas price; the cans figure rounds up."],
     'faqs': [("How much gas does a 5000 watt generator use per day?",
               "At a realistic 50% load, about 0.45 gallons per hour or 11 gallons a day - two and a bit 5-gallon cans. At 25% (fridge, lights, router) it falls to around 5-6 gallons; running everything at once can double it."),
              ("How long can you store gasoline for a generator?",
               "Three to six months untreated, a year or more with fuel stabilizer. Rotate the stock by pouring it into the car and refilling - an outage is the wrong time to discover last season went stale."),
              ("Is a generator cheaper to run than a battery power station?",
               "Per hour of heavy load, gasoline wins on cost. Per outage over years, the battery wins on silence, fumes, maintenance and indoor safety. The honest split: generators for multi-day whole-home events, stations for day-long rides and apartment use."),
              ("Can I refuel a generator while it is running?",
               "Never - a hot engine plus a spilled gallon is the textbook flash fire. Shut down, wait 10-15 minutes, refuel with a funnel, restart. Fifteen minutes of darkness is cheaper than the alternative.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'electric-vs-gas-heating',
     'title': 'Electric vs Gas Heating Cost - Compare per Million BTU at Your Rates',
     'h1': 'Electric vs Gas Heating Cost',
     'desc': 'Your electric and gas prices, furnace efficiency and heat pump COP become one verdict in dollars per million BTU - the honest way to rank heating fuels. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'electric vs gas heating cost per btu comparison',
     'tool': 'heatcmp',
     'args': {},
     'intro': ["Put in what your bill actually charges per kWh and per therm, how efficient the furnace is, and the heat pump COP if you have one. Every option becomes a single number: dollars for one million BTU of delivered heat, the only fair way to compare fuels sold in different units.",
              "Utility blogs compare sticker tariffs and call it done. This page divides by efficiency - an 80% furnace pays 25% more per heat unit than its nameplate, a COP 3 heat pump turns one purchased kWh into three of heat - and says out loud that delivery charges, not the fuel, often decide the verdict."],
     'howto': ["Use all-in rates from your latest bill, not the advertised generation rate.",
               "Set furnace efficiency: 80% for older units, 95% for modern condensing.",
               "Keep the COP at 3 unless you know your unit; deep cold pushes it lower."],
     'faqs': [("What is cheaper per unit of heat, electric or gas?",
               "At US averages - 17 cents per kWh against $1.60 per therm - resistance electric costs about $50 per million BTU and gas about $17, so gas wins by roughly 3x. A heat pump at COP 3 brings electric down near $17 and usually takes the lead."),
              ("Why compare heating in dollars per million BTU?",
               "Electricity is sold in kWh, gas in therms, propane in gallons - raw prices cannot be ranked against each other. One million BTU is the same heat in every fuel, so dividing each price by its efficiency collapses the comparison into one number."),
              ("Does furnace efficiency really change the math?",
               "Yes: every dollar buys only 80-95 cents of heat depending on the unit, so an old furnace on a cheap tariff can cost more per heat than a modern one on a pricier tariff. The calculator prices this instead of trusting the nameplate."),
              ("Is a heat pump worth it over a gas furnace?",
               "On running cost the pump wins whenever its COP beats your normalized electric-to-gas price ratio - with COP 3 and typical US prices that is roughly break-even to cheaper, and it pulls ahead every time gas spikes, while also replacing the AC. Upfront install cost is the honest trade.")]}
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
print("R130 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
