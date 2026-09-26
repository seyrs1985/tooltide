# -*- coding: utf-8 -*-
"""R157 节后与冬储三连:gift-return(退货死线+.ics)+ice-melt(融冰盐袋数)+home-gym-payback(器械回本)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: GIFTRETURN ----------
Gr = 'GIFTRETURN = """<div class="tool" id="tt-gr">\n'
Gr += '  <div class="fields">\n'
Gr += '    <div class="field"><label for="gr-d">Purchase (or gift) date</label><input type="date" id="gr-d"></div>\n'
Gr += '    <div class="field"><label for="gr-w">Return window</label><select id="gr-w"><option value="14">14 days</option><option value="30" selected>30 days - most stores</option><option value="60">60 days</option><option value="90">90 days - generous</option></select></div>\n'
Gr += '  </div>\n'
Gr += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gr-out">&#8211;</span><span class="result-unit">last day to return</span></div>\n'
Gr += '  <div class="stats">\n'
Gr += '    <div class="stat"><b id="gr-s1">&#8211;</b><span>days from today</span></div>\n'
Gr += '    <div class="stat"><b id="gr-s2">&#8211;</b><span>receipt rule of thumb</span></div>\n'
Gr += '    <div class="stat"><b id="gr-s3">&#8211;</b><span>holiday extension</span></div>\n'
Gr += '  </div>\n'
Gr += '  <div class="tool-note" id="gr-note"></div>\n'
Gr += '  <button type="button" class="tool-btn" id="gr-share">Share my return window</button>\n'
Gr += '  <button type="button" class="tool-btn" id="gr-ics">Add to calendar (.ics)</button>\n'
Gr += '</div>\n'
Gr += '<script>(function(){\n'
Gr += "var D=document.getElementById('gr-d'),W=document.getElementById('gr-w');\n"
Gr += "var lastRet=null;\n"
Gr += "function calc(){\n"
Gr += "  var dv=D.value,win=parseFloat(W.value)||30;\n"
Gr += "  if(!dv){document.getElementById('gr-out').textContent='\\u2013';lastRet=null;return;}\n"
Gr += "  var day=new Date(dv+'T12:00:00');\n"
Gr += "  var ret=new Date(day.getTime()+win*86400000);\n"
Gr += "  var now=new Date();var today=new Date(now.getFullYear(),now.getMonth(),now.getDate());\n"
Gr += "  var left=Math.round((ret-today)/86400000);\n"
Gr += "  var names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];\n"
Gr += "  var rs=names[ret.getMonth()]+' '+ret.getDate();\n"
Gr += "  document.getElementById('gr-out').textContent=rs;\n"
Gr += "  document.getElementById('gr-s1').textContent=left;\n"
Gr += "  document.getElementById('gr-s2').textContent='no receipt = store credit';\n"
Gr += "  document.getElementById('gr-s3').textContent='Dec gifts often run to Jan 31';\n"
Gr += "  document.getElementById('gr-note').textContent='Two things trip people up every year. First, the clock starts on the purchase date, not the gift date - a present bought in November on a 30-day window is already expired by Boxing Day, which is why stores quietly extend holiday purchases to the end of January; check the receipt page for the words extended holiday returns. Second, no receipt usually means store credit at the current lower price, not refund. Keep the gift receipt with the box, do not open packaging you might return, and start the return the week after the holiday when the queue is shortest.';\n"
Gr += "  document.title='Return by '+rs+' - ToolDune';\n"
Gr += "  lastRet=ret;\n"
Gr += "}\n"
Gr += "function save(){try{localStorage.setItem('tt_giftreturn',JSON.stringify({d:D.value,w:W.value}));}catch(e){}}\n"
Gr += "[D,W].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Gr += "var pre=false;\n"
Gr += "var qs=new URLSearchParams(location.search);\n"
Gr += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
Gr += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Gr += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_giftreturn')||'null');if(m){if(m.d){D.value=m.d;}if(m.w){W.value=m.w;}}}catch(e){}}\n"
Gr += "if(!D.value){var td=new Date();D.value=td.getFullYear()+'-'+('0'+(td.getMonth()+1)).slice(-2)+'-'+('0'+td.getDate()).slice(-2);}\n"
Gr += "calc();\n"
Gr += "function ymdGR(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}\n"
Gr += "document.getElementById('gr-ics').addEventListener('click',function(){\n"
Gr += "  if(!lastRet){return;}\n"
Gr += "  var end=new Date(lastRet.getTime()+86400000);\n"
Gr += "  var NL=String.fromCharCode(13,10);\n"
Gr += "  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymdGR(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdGR(lastRet)+NL+'DTEND;VALUE=DATE:'+ymdGR(end)+NL+'SUMMARY:Last day to return'+NL+'DESCRIPTION:Bring the receipt and the box. Window by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';\n"
Gr += "  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='return-deadline.ics';\n"
Gr += "  document.body.appendChild(a);a.click();document.body.removeChild(a);\n"
Gr += "  this.textContent='Calendar file downloaded';\n"
Gr += "  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);\n"
Gr += "});\n"
Gr += "document.getElementById('gr-share').addEventListener('click',function(){\n"
Gr += "  var txt='Return by '+document.getElementById('gr-out').textContent+' - set the date free:';\n"
Gr += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value)+'&w='+encodeURIComponent(W.value);\n"
Gr += "  if(navigator.share){navigator.share({title:'Return deadline',text:txt,url:url}).catch(function(){});}\n"
Gr += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my return window';},1500);}\n"
Gr += "});\n"
Gr += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: ICEMELT ----------
Im = 'ICEMELT = """<div class="tool" id="tt-im">\n'
Im += '  <div class="fields">\n'
Im += '    <div class="field"><label for="im-a">Driveway and walkway area (sq ft)</label><input id="im-a" type="number" min="100" max="10000" value="600"></div>\n'
Im += '    <div class="field"><label for="im-t">Product</label><select id="im-t"><option value="4">Rock salt - 4 lb/1000 sq ft</option><option value="6" selected>Ice melt blend - 6 lb/1000</option><option value="3">Calcium chloride - 3 lb/1000</option></select></div>\n'
Im += '    <div class="field"><label for="im-n">Applications per winter</label><input id="im-n" type="number" min="1" max="40" value="8"></div>\n'
Im += '    <div class="field"><label for="im-p">Price per 50 lb bag</label><input id="im-p" type="number" min="5" value="25"></div>\n'
Im += '  </div>\n'
Im += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="im-out">&#8211;</span><span class="result-unit">pounds per application</span></div>\n'
Im += '  <div class="stats">\n'
Im += '    <div class="stat"><b id="im-s1">&#8211;</b><span>50 lb bags for the winter</span></div>\n'
Im += '    <div class="stat"><b id="im-s2">&#8211;</b><span>season cost</span></div>\n'
Im += '    <div class="stat"><b id="im-s3">&#8211;</b><span>lowest working temp</span></div>\n'
Im += '  </div>\n'
Im += '  <div class="tool-note" id="im-note"></div>\n'
Im += '  <button type="button" class="tool-btn" id="im-share">Share my salt math</button>\n'
Im += '</div>\n'
Im += '<script>(function(){\n'
Im += "var A=document.getElementById('im-a'),T=document.getElementById('im-t'),N=document.getElementById('im-n'),P=document.getElementById('im-p');\n"
Im += "function calc(){\n"
Im += "  var a=parseFloat(A.value)||600,rate=parseFloat(T.value)||6,n=Math.max(1,parseFloat(N.value)||8),p=parseFloat(P.value)||25;\n"
Im += "  var perApp=a/1000*rate, winter=perApp*n, bags=Math.ceil(winter/50), cost=bags*p;\n"
Im += "  var temps={4:'+5 F',6:'-10 F',3:'-25 F'};\n"
Im += "  var temp=temps[rate]||'-10 F';\n"
Im += "  var d1=Math.round(perApp*10)/10, d2=Math.round(cost*100)/100;\n"
Im += "  document.getElementById('im-out').textContent=d1;\n"
Im += "  document.getElementById('im-s1').textContent=bags;\n"
Im += "  document.getElementById('im-s2').textContent='$'+d2;\n"
Im += "  document.getElementById('im-s3').textContent=temp;\n"
Im += "  document.getElementById('im-note').textContent='More salt does not melt faster - the right dose melts once and the rest just wrecks concrete and paws. Rock salt stops working near 5 F, blends reach about -10, calcium chloride keeps going to -25 and is the one for the deep-cold week. Two honest warnings the bag prints too small: salt damages new concrete for its first winter and burns pet paws - pet-safe blends cost more and earn it. Spread before the snow sticks if you can; pre-treating is the difference between a shovel job and an ice pick job.';\n"
Im += "  document.title='Ice melt: '+d1+' lb per storm - ToolDune';\n"
Im += "}\n"
Im += "function save(){try{localStorage.setItem('tt_icemelt',JSON.stringify({a:A.value,t:T.value,n:N.value,p:P.value}));}catch(e){}}\n"
Im += "[A,T,N,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Im += "var pre=false;\n"
Im += "var qs=new URLSearchParams(location.search);\n"
Im += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Im += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_icemelt')||'null');if(m){if(m.a){A.value=m.a;}if(m.t){T.value=m.t;}if(m.n){N.value=m.n;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Im += "calc();\n"
Im += "document.getElementById('im-share').addEventListener('click',function(){\n"
Im += "  var txt='My driveway takes '+document.getElementById('im-out').textContent+' lb of ice melt per storm - '+document.getElementById('im-s1').textContent+' bags a winter. Run yours:';\n"
Im += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Im += "  if(navigator.share){navigator.share({title:'Ice melt math',text:txt,url:url}).catch(function(){});}\n"
Im += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my salt math';},1500);}\n"
Im += "});\n"
Im += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: HOMEGYM ----------
Hg = 'HOMEGYM = """<div class="tool" id="tt-hg">\n'
Hg += '  <div class="fields">\n'
Hg += '    <div class="field"><label for="hg-c">Equipment cost</label><input id="hg-c" type="number" min="50" value="600"></div>\n'
Hg += '    <div class="field"><label for="hg-m">Gym fee it replaces (monthly)</label><input id="hg-m" type="number" min="5" value="45"></div>\n'
Hg += '    <div class="field"><label for="hg-r">Resale value if you quit (%)</label><select id="hg-r"><option value="30">30% - dusty gear</option><option value="50" selected>50% - cared for</option><option value="70">70% - barely used, hot market</option></select></div>\n'
Hg += '  </div>\n'
Hg += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hg-out">&#8211;</span><span class="result-unit">months to pay back</span></div>\n'
Gr_dummy = None
Hg += '  <div class="stats">\n'
Hg += '    <div class="stat"><b id="hg-s1">&#8211;</b><span>gym cost in that time</span></div>\n'
Hg += '    <div class="stat"><b id="hg-s2">&#8211;</b><span>net if you quit after a year</span></div>\n'
Hg += '    <div class="stat"><b id="hg-s3">&#8211;</b><span>the starter kit costs</span></div>\n'
Hg += '  </div>\n'
Hg += '  <div class="tool-note" id="hg-note"></div>\n'
Hg += '  <button type="button" class="tool-btn" id="hg-share">Share my payback math</button>\n'
Hg += '</div>\n'
Hg += '<script>(function(){\n'
Hg += "var C=document.getElementById('hg-c'),M=document.getElementById('hg-m'),Rr=document.getElementById('hg-r');\n"
Hg += "function calc(){\n"
Hg += "  var c=parseFloat(C.value)||0,m=Math.max(1,parseFloat(M.value)||45),r=parseFloat(Rr.value)||0.5;\n"
Hg += "  var months=Math.ceil(c/m), gymYear=m*12, quitNet=c*(1-r)-m*12, starter=300;\n"
Hg += "  var d1=Math.round(gymYear), d2=Math.round(quitNet);\n"
Hg += "  document.getElementById('hg-out').textContent=months;\n"
Hg += "  document.getElementById('hg-s1').textContent='$'+d1;\n"
Hg += "  document.getElementById('hg-s2').textContent=(quitNet>=0?'+':'')+'$'+Math.abs(d2);\n"
Hg += "  document.getElementById('hg-s3').textContent='$'+starter;\n"
Hg += "  document.getElementById('hg-note').textContent='The payback math is simple division; the honesty lives in the quit case. Home gear pays back only while you train, and the resale column is what separates a reasonable experiment from a regret - adjustable dumbbells and a bench, about 300 dollars of starter kit, cover most routines and resell near half price. The mirror-class machines cost a gym decade and resell for transport money. Two more truths: the membership you replace includes showers and a change of scene, which is worth real money to some people, and home training trades variety for zero commute - the workout you actually do is the cheap one.';\n"
Hg += "  document.title='Home gym pays back in '+months+' months - ToolDune';\n"
Hg += "}\n"
Hg += "function save(){try{localStorage.setItem('tt_homegym',JSON.stringify({c:C.value,m:M.value,r:Rr.value}));}catch(e){}}\n"
Hg += "[C,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Hg += "Rr.addEventListener('change',function(){calc();save();});\n"
Hg += "var pre=false;\n"
Hg += "var qs=new URLSearchParams(location.search);\n"
Hg += "if(qs.get('c')){C.value=qs.get('c');pre=true;}\n"
Hg += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_homegym')||'null');if(m){if(m.c){C.value=m.c;}if(m.m){M.value=m.m;}if(m.r){Rr.value=m.r;}}}catch(e){}}\n"
Hg += "calc();\n"
Hg += "document.getElementById('hg-share').addEventListener('click',function(){\n"
Hg += "  var txt='A home gym pays back in '+document.getElementById('hg-out').textContent+' months at my gym fee. Run yours:';\n"
Hg += "  var url=location.origin+location.pathname+'?c='+encodeURIComponent(C.value);\n"
Hg += "  if(navigator.share){navigator.share({title:'Home gym payback',text:txt,url:url}).catch(function(){});}\n"
Hg += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my payback math';},1500);}\n"
Hg += "});\n"
Hg += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("GIFTRETURN", "ICEMELT", "HOMEGYM"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Gr + Im + Hg + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "champagne": lambda args: CHAMP,',
    '    "champagne": lambda args: CHAMP,\n'
    '    "giftreturn": lambda args: GIFTRETURN,\n'
    '    "icemelt": lambda args: ICEMELT,\n'
    '    "homegym": lambda args: HOMEGYM,')
sub(BUILD_P, '    "dehumid": "💨", "santamath": "🎅", "champagne": "🍷",',
    '    "dehumid": "💨", "santamath": "🎅", "champagne": "🍷",\n'
    '    "giftreturn": "🔁", "icemelt": "❄", "homegym": "🏠",')

P = []
d = {'slug': 'gift-return-deadline-calculator',
     'title': 'Gift Return Deadline Calculator - Last Day to Return Anything',
     'h1': 'Gift Return Deadline Calculator',
     'desc': 'Purchase date plus the store window gives the exact last return day, days remaining, and the holiday-extension fine print - with a calendar download. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'gift return deadline calculator how many days to return',
     'tool': 'giftreturn',
     'args': {},
     'intro': ["Enter the purchase date and the store return window. The calculator gives the exact last day, how much time is left, and a calendar download so the deadline stops living in your head.",
              "The annual trap is built in: return clocks run on the purchase date, not the gift date, so November presents expire by Boxing Day - which is exactly why stores extend holiday purchases to late January. This calculator catches the trap and explains the no-receipt reality: store credit at the current price, not a refund."],
     'howto': ["Set the real purchase date - check the receipt, not your memory.",
               "Pick the window printed on the receipt or policy page.",
               "Download the reminder; the week after the holiday has the shortest queue."],
     'faqs': [("How many days do I have to return a gift?",
               "Most stores run 30 days from purchase; some run 14 for electronics and 60-90 for generous retailers. Gifts bought in November on a 30-day window are technically expired by late December - always check for the holiday extension."),
              ("Can I return a gift without a receipt?",
               "Usually yes, but as store credit at the current selling price - not a refund to the buyer. The gift receipt exists precisely for this: it proves the purchase without revealing the price."),
              ("Do stores extend return windows for Christmas?",
               "Many do - purchases from November onward often run to January 31. It is printed on the receipt or the policy page, and it is the single most useful line to read before standing in the post-Christmas queue."),
              ("What cannot be returned after opening?",
               "Electronics activated with accounts, sealed health and personal items, custom or personalized goods, and anything digital. Keep packaging intact on anything with return potential - opened-box restocking fees start at 15 percent.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'ice-melt-calculator',
     'title': 'Ice Melt Calculator - Bags of Salt for Your Driveway This Winter',
     'h1': 'Ice Melt Calculator',
     'desc': 'Driveway area, product type and storm count give pounds per application, bags for the winter and the cost - with the pet-paw and concrete warnings. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'ice melt calculator how much salt per driveway bags',
     'tool': 'icemelt',
     'args': {},
     'intro': ["Enter your driveway and walkway area, the product you use, how many storms you realistically fight each winter, and the bag price. The calculator gives pounds per application, bags for the season, and the cost.",
              "More salt does not melt faster - the right dose works once and the surplus wrecks concrete and paws. This calculator prices the product honestly by type: rock salt quits near 5 F, blends reach -10, calcium chloride keeps working to -25, and the pet-safe blends cost more for reasons the paws will explain."],
     'howto': ["Measure the paved area you actually clear, including the walkway.",
               "Pick the product for your coldest realistic storm, not the record.",
               "Buy at season start; the first storm empties the aisle."],
     'faqs': [("How much ice melt do I need per 1000 square feet?",
               "About 4 pounds of rock salt, 6 of a blended melt, or 3 of calcium chloride per application. Spreading double does not double the speed - it doubles the runoff, the concrete damage and the cost."),
              ("Which ice melt is safe for pets and concrete?",
               "Pet-safe blends use gentler salts and cost more per bag; on paws, any product should be wiped off after walks. On concrete under one year old, avoid rock salt entirely - use calcium-based products sparingly, or sand for traction."),
              ("At what temperature does rock salt stop working?",
               "Around 5 F (-15 C). Blends reach roughly -10 F and calcium chloride keeps melting near -25 F. Below a product limit, adding more does nothing - that is what the calculator's temperature column is for."),
              ("Should I salt before or after snow?",
               "Before, if you can - a pre-treat layer stops the bond forming and turns the shovel job into a sweep. After, it still works but slower. The calculator sizes the per-storm dose either way.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'home-gym-payback-calculator',
     'title': 'Home Gym Payback Calculator - Months to Beat the Membership',
     'h1': 'Home Gym Payback Calculator',
     'desc': 'Equipment cost over your gym fee gives the payback months, the quit-case net with resale, and the 300-dollar starter kit reality. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'home gym worth it calculator payback vs gym membership',
     'tool': 'homegym',
     'args': {},
     'intro': ["Enter the equipment cost and the monthly fee it replaces. The calculator gives the payback in months, what the gym would have cost in that time, and - the honest part - your net if you quit after a year, resale value included.",
              "The payback math is simple division; the quit case is where calculators usually stop. This one prices resale, names the 300-dollar starter kit that covers most routines, and admits what the membership includes: showers, a change of scene, and nobody re-racking your weights."],
     'howto': ["Price the gear you would actually buy, not the showroom dream.",
               "Set the fee honestly - the one you would really cancel.",
               "Read the quit-case line before, not after, the credit card swipe."],
     'faqs': [("Is a home gym cheaper than a gym membership?",
               "Past the payback months - equipment cost divided by the fee - yes, and the gap widens every month after. At 45 a month, 600 dollars of gear pays back in 14 months; everything beyond is profit measured in not-going."),
              ("What home gym equipment is worth buying first?",
               "Adjustable dumbbells and an adjustable bench, about 300 dollars together - they cover most strength routines, store in a corner and resell near half price. The expensive machines are the ones that become clothes racks."),
              ("What is the real cost of quitting a home gym?",
               "The resale haircut: gear resells around 30-70 percent depending on care and market. The calculator nets that against the membership fees you skipped, which is why quitting in month two is expensive and quitting in year three is a refund."),
              ("Does a home gym replace everything a commercial gym offers?",
               "No - showers, machines for isolation work, and the change of scene are real value for some people. The honest comparison is the workout you actually do, in the place you actually do it, at the price that keeps you doing it.")]}
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
print("R157 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
