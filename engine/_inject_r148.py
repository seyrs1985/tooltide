# -*- coding: utf-8 -*-
"""R148 感恩节旅途双页:road-trip-fuel(自付油账+人均)+flight-vs-drive(全口径对表)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: ROADFUEL ----------
Rf = 'ROADFUEL = """<div class="tool" id="tt-rf">\n'
Rf += '  <div class="fields">\n'
Rf += '    <div class="field"><label for="rf-m">One-way miles</label><input id="rf-m" type="number" min="5" value="250"></div>\n'
Rf += '    <div class="field"><label for="rf-g">Highway mpg</label><input id="rf-g" type="number" min="5" max="120" value="28"></div>\n'
Rf += '    <div class="field"><label for="rf-p">Gas price per gallon</label><input id="rf-p" type="number" min="1" step="0.05" value="3.20"></div>\n'
Rf += '    <div class="field"><label for="rf-n">People in the car</label><select id="rf-n"><option value="1">1 - solo</option><option value="2">2</option><option value="3">3</option><option value="4" selected>4</option><option value="5">5</option><option value="6">6</option></select></div>\n'
Rf += '    <div class="field"><label for="rf-r">Trip type</label><select id="rf-r"><option value="2" selected>Round trip</option><option value="1">One way</option></select></div>\n'
Rf += '  </div>\n'
Rf += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rf-out">&#8211;</span><span class="result-unit">total fuel cost</span></div>\n'
Rf += '  <div class="stats">\n'
Rf += '    <div class="stat"><b id="rf-s1">&#8211;</b><span>gallons burned</span></div>\n'
Rf += '    <div class="stat"><b id="rf-s2">&#8211;</b><span>per person</span></div>\n'
Rf += '    <div class="stat"><b id="rf-s3">&#8211;</b><span>driving hours, no stops</span></div>\n'
Rf += '  </div>\n'
Rf += '  <div class="tool-note" id="rf-note"></div>\n'
Rf += '  <button type="button" class="tool-btn" id="rf-share">Share my fuel math</button>\n'
Rf += '</div>\n'
Rf += '<script>(function(){\n'
Rf += "var M=document.getElementById('rf-m'),G=document.getElementById('rf-g'),P=document.getElementById('rf-p'),N=document.getElementById('rf-n'),Rr=document.getElementById('rf-r');\n"
Rf += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>0?v:0;}\n"
Rf += "function calc(){\n"
Rf += "  var m=num(M),g=num(G),p=num(P),n=parseInt(N.value,10)||1,rt=parseFloat(Rr.value)||2;\n"
Rf += "  var miles=m*rt, gal=miles/g, cost=gal*p, hrs=miles/65;\n"
Rf += "  var d1=Math.round(gal*10)/10, d2=Math.round(cost*100)/100, d3=Math.round(cost/n*100)/100;\n"
Rf += "  var h=Math.floor(hrs), min=Math.round((hrs-h)*60);\n"
Rf += "  document.getElementById('rf-out').textContent='$'+d2;\n"
Rf += "  document.getElementById('rf-s1').textContent=d1;\n"
Rf += "  document.getElementById('rf-s2').textContent='$'+d3;\n"
Rf += "  document.getElementById('rf-s3').textContent=h+' h '+min+' min';\n"
Rf += "  document.getElementById('rf-note').textContent='This is the fuel-only number - the cash that actually leaves your account at the pump. The full cost per mile of driving runs several times higher once tires, oil and depreciation join, which is fine to ignore for a family visit and worth remembering when someone offers to pay half the gas. Holiday traffic adds time, not many gallons, so leave early: the 6 am Thanksgiving-morning road is famously the empty one. And per-person only works if the passengers chip in without being asked twice - set the figure before departure, not at the pump.';\n"
Rf += "  document.title='Drive: $'+d2+' in fuel - ToolDune';\n"
Rf += "}\n"
Rf += "function save(){try{localStorage.setItem('tt_roadfuel',JSON.stringify({m:M.value,g:G.value,p:P.value,n:N.value,r:Rr.value}));}catch(e){}}\n"
Rf += "[M,G,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Rf += "[N,Rr].forEach(function(el){el.addEventListener('change',function(){calc();save();});});\n"
Rf += "var pre=false;\n"
Rf += "var qs=new URLSearchParams(location.search);\n"
Rf += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
Rf += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_roadfuel')||'null');if(m){if(m.m){M.value=m.m;}if(m.g){G.value=m.g;}if(m.p){P.value=m.p;}if(m.n){N.value=m.n;}if(m.r){Rr.value=m.r;}}}catch(e){}}\n"
Rf += "calc();\n"
Rf += "document.getElementById('rf-share').addEventListener('click',function(){\n"
Rf += "  var txt='Our trip burns about '+document.getElementById('rf-out').textContent+' in fuel - '+document.getElementById('rf-s2').textContent+' each. Run yours:';\n"
Rf += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value);\n"
Rf += "  if(navigator.share){navigator.share({title:'Road trip fuel cost',text:txt,url:url}).catch(function(){});}\n"
Rf += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my fuel math';},1500);}\n"
Rf += "});\n"
Rf += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: FLYDRIVE ----------
Fd = 'FLYDRIVE = """<div class="tool" id="tt-fd">\n'
Fd += '  <div class="fields">\n'
Fd += '    <div class="field"><label for="fd-m">Trip miles, door to door</label><input id="fd-m" type="number" min="50" value="500"></div>\n'
Fd += '    <div class="field"><label for="fd-g">Car mpg</label><input id="fd-g" type="number" min="5" max="120" value="28"></div>\n'
Fd += '    <div class="field"><label for="fd-p">Gas price per gallon</label><input id="fd-p" type="number" min="1" step="0.05" value="3.20"></div>\n'
Fd += '    <div class="field"><label for="fd-t">Cheapest round-trip flight</label><input id="fd-t" type="number" min="20" value="180"></div>\n'
Fd += '    <div class="field"><label for="fd-b">Flight bag + ground fees</label><input id="fd-b" type="number" min="0" value="60"></div>\n'
Fd += '  </div>\n'
Fd += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fd-out">&#8211;</span><span class="result-unit">cheaper way</span></div>\n'
Fd += '  <div class="stats">\n'
Fd += '    <div class="stat"><b id="fd-s1">&#8211;</b><span>drive, fuel only</span></div>\n'
Fd += '    <div class="stat"><b id="fd-s2">&#8211;</b><span>fly, all-in</span></div>\n'
Fd += '    <div class="stat"><b id="fd-s3">&#8211;</b><span>gap</span></div>\n'
Fd += '  </div>\n'
Fd += '  <div class="tool-note" id="fd-note"></div>\n'
Fd += '  <button type="button" class="tool-btn" id="fd-share">Share my verdict</button>\n'
Fd += '</div>\n'
Fd += '<script>(function(){\n'
Fd += "var M=document.getElementById('fd-m'),G=document.getElementById('fd-g'),P=document.getElementById('fd-p'),T=document.getElementById('fd-t'),B=document.getElementById('fd-b');\n"
Fd += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Fd += "function calc(){\n"
Fd += "  var m=num(M),g=Math.max(5,num(G)),p=num(P),t=num(T),b=num(B);\n"
Fd += "  var drive=m/g*p, fly=t+b, gap=Math.abs(drive-fly);\n"
Fd += "  var d1=Math.round(drive*100)/100, d2=Math.round(fly*100)/100, d3=Math.round(gap*100)/100;\n"
Fd += "  var win=drive<=fly?'Drive':'Fly';\n"
Fd += "  document.getElementById('fd-out').textContent=win;\n"
Fd += "  document.getElementById('fd-s1').textContent='$'+d1;\n"
Fd += "  document.getElementById('fd-s2').textContent='$'+d2;\n"
Fd += "  document.getElementById('fd-s3').textContent='$'+d3;\n"
Fd += "  document.getElementById('fd-note').textContent='The money verdict is mechanical: fuel against ticket plus bags plus the ride to the airport. The time verdict needs the honest overhead rule - door to door, flying almost never beats driving under 400 miles, because airport buffers, security and boarding eat roughly four hours before the plane even moves. Past 800 miles the plane usually wins outright. The two sides measure different things though: the drive is fuel today and wear later, the flight is cash now and flexibility - and a solo traveler can split nothing, while a car load of four makes the per-seat math brutal for the airline.';\n"
Fd += "  document.title=win+' - saving $'+d3+' - ToolDune';\n"
Fd += "}\n"
Fd += "function save(){try{localStorage.setItem('tt_flydrive',JSON.stringify({m:M.value,g:G.value,p:P.value,t:T.value,b:B.value}));}catch(e){}}\n"
Fd += "[M,G,P,T,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Fd += "var pre=false;\n"
Fd += "var qs=new URLSearchParams(location.search);\n"
Fd += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
Fd += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_flydrive')||'null');if(m){if(m.m){M.value=m.m;}if(m.g){G.value=m.g;}if(m.p){P.value=m.p;}if(m.t){T.value=m.t;}if(m.b){B.value=m.b;}}}catch(e){}}\n"
Fd += "calc();\n"
Fd += "document.getElementById('fd-share').addEventListener('click',function(){\n"
Fd += "  var txt='For this trip, '+document.getElementById('fd-out').textContent+' wins by $'+document.getElementById('fd-s3').textContent+'. Run yours:';\n"
Fd += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value);\n"
Fd += "  if(navigator.share){navigator.share({title:'Fly or drive',text:txt,url:url}).catch(function(){});}\n"
Fd += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my verdict';},1500);}\n"
Fd += "});\n"
Fd += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("ROADFUEL", "FLYDRIVE"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Rf + Fd + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "wrapcalc": lambda args: WRAPCALC,',
    '    "wrapcalc": lambda args: WRAPCALC,\n'
    '    "roadfuel": lambda args: ROADFUEL,\n'
    '    "flydrive": lambda args: FLYDRIVE,')
sub(BUILD_P, '    "treewater": "🌲", "treelights": "✨", "wrapcalc": "✂",',
    '    "treewater": "🌲", "treelights": "✨", "wrapcalc": "✂",\n'
    '    "roadfuel": "🚙", "flydrive": "✈",')

P = []
d = {'slug': 'road-trip-fuel-calculator',
     'title': 'Road Trip Fuel Calculator - Gallons, Cost and Per Person',
     'h1': 'Road Trip Fuel Calculator',
     'desc': 'Miles, mpg and your gas price give the real fuel bill for the trip, split per passenger - plus the honest note on what fuel-only leaves out. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'road trip fuel cost calculator gas money per person',
     'tool': 'roadfuel',
     'args': {},
     'intro': ["Enter the one-way miles, your highway mpg, the gas price where you fill, and how many people are in the car. The calculator gives gallons burned, the total fuel bill, the per-person split, and the driving hours behind it.",
              "Split-the-gas threads argue in circles because nobody states the model. This one states it plainly: fuel-only is the fair number to split, the full cost-per-mile with depreciation is several times higher and belongs to a different conversation, and the per-person figure works only if it is agreed before departure, not negotiated at the pump."],
     'howto': ["Miles one-way from any map app; the round-trip toggle doubles it.",
               "Use real highway mpg from your dashboard trip computer, not the sticker.",
               "Split per person before leaving - it is a bad conversation at the pump."],
     'faqs': [("How much does a 500 mile road trip cost in gas?",
               "At 28 mpg and 3.20 a gallon, about 57 dollars one way - 114 round trip. The calculator prices your car and your pump price exactly, and splits it per passenger."),
              ("Should passengers pay full fuel cost?",
               "The polite convention is to split the fuel-only figure per person, not the true cost of ownership - wear, tires and depreciation ride with the owner. Agreeing on the number before the trip beats a silent grudge at the first fill-up."),
              ("Does holiday traffic burn more gas?",
               "Some - crawling and idling can cost 10-20 percent more fuel than free-flow highway, and it costs far more time. Leaving before dawn on peak travel days is the single cheapest upgrade a holiday road trip can buy."),
              ("What is the true cost per mile of driving?",
               "Fuel is only part of it; with depreciation, tires and maintenance the all-in figure for a typical car runs around 60-70 cents per mile. Use fuel-only for splitting a friendly trip, and the all-in number when deciding whether the trip makes sense at all.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'flight-vs-drive-calculator',
     'title': 'Flight vs Drive Calculator - All-In Cost Comparison for Any Trip',
     'h1': 'Flight vs Drive Calculator',
     'desc': 'Fuel against ticket, bags and airport ground costs - the mechanical money verdict plus the honest door-to-door time rule for choosing plane or car. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'fly vs drive calculator is it cheaper to fly or drive',
     'tool': 'flydrive',
     'args': {},
     'intro': ["Enter the trip miles, your car mpg and gas price, the cheapest round-trip airfare, and the bag and airport-ground fees. The calculator names the cheaper way and the gap - with the time rule that actually settles most debates.",
              "Airline pages compare ticket to ticket and hide the ground costs; car pages forget that flights exist. This one does the mechanical money math both ways, then applies the honest overhead rule: under 400 miles, door to door, flying almost never wins once the airport buffers are counted - and past 800 the plane usually does."],
     'howto': ["Trip miles door to door, from any map app.",
               "Airfare at the cheapest realistic fare, bags and ground rides included.",
               "Let the time rule break ties the money cannot."],
     'faqs': [("Is it cheaper to fly or drive?",
               "For one person under 400-500 miles, driving usually wins on money and often on time once airport overhead counts. Alone on long trips the flight frequently wins; with a full car, the per-seat math almost always favors driving. The calculator prices your exact numbers."),
              ("How much time does airport overhead really add?",
               "Count roughly two hours before departure for parking, security and boarding, plus the ride each way - about four hours that never appear on the ticket. Under that overhead, a 400-mile drive is usually faster door to door."),
              ("What flight costs do people forget?",
               "Checked bags, the seat-selection upsell, airport parking or the ride both ways, and meals at airport prices. Enter them as the bag-and-ground fee and the comparison stops flattering the plane."),
              ("When does flying obviously win?",
               "Roughly past 800 miles, when the drive crosses two full driving days, or when the trip is one-way. Fuel prices move the crossover less than people expect - time and the number of travelers move it far more.")]}
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
print("R148 inject OK: 2 renderers + 2 pages + 2 emoji, ast passed")
