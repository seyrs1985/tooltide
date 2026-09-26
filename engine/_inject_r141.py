# -*- coding: utf-8 -*-
"""R141 冬季日光+年终人情簇:daylight-hours(日照时长NOAA近似)+holiday-tipping(年终打点分账)+donation-deadline(捐赠减税与12.31死线)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: DAYLIGHT ----------
Dl = 'DAYLIGHT = """<div class="tool" id="tt-dh">\n'
Dl += '  <div class="fields">\n'
Dl += '    <div class="field"><label for="dh-d">Date</label><input type="date" id="dh-d"></div>\n'
Dl += '    <div class="field"><label for="dh-l">Latitude (40 = US average)</label><input id="dh-l" type="number" min="-66" max="66" step="0.5" value="40"></div>\n'
Dl += '  </div>\n'
Dl += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dh-out">&#8211;</span><span class="result-unit">of daylight</span></div>\n'
Dl += '  <div class="stats">\n'
Dl += '    <div class="stat"><b id="dh-s1">&#8211;</b><span>longest day here</span></div>\n'
Dl += '    <div class="stat"><b id="dh-s2">&#8211;</b><span>shortest day here</span></div>\n'
Dl += '    <div class="stat"><b id="dh-s3">&#8211;</b><span>change per day now</span></div>\n'
Dl += '  </div>\n'
Dl += '  <div class="tool-note" id="dh-note"></div>\n'
Dl += '  <button type="button" class="tool-btn" id="dh-share">Share my daylight math</button>\n'
Dl += '</div>\n'
Dl += '<script>(function(){\n'
Dl += "var DI=document.getElementById('dh-d'),LA=document.getElementById('dh-l');\n"
Dl += "function dayLen(dateObj,lat){\n"
Dl += "  var start=new Date(dateObj.getFullYear(),0,0);\n"
Dl += "  var N=Math.floor((dateObj-start)/86400000);\n"
Dl += "  var dec=-23.44*Math.cos(2*Math.PI/365*(N+10));\n"
Dl += "  var rad=Math.PI/180;\n"
Dl += "  var x=-Math.tan(lat*rad)*Math.tan(dec*rad);\n"
Dl += "  if(x>1)return 0;\n"
Dl += "  if(x<-1)return 24;\n"
Dl += "  var H=Math.acos(x)/rad*2/15;\n"
Dl += "  return H;\n"
Dl += "}\n"
Dl += "function fmtHM(h){var m=Math.round(h*60);return Math.floor(m/60)+' h '+(m%60)+' min';}\n"
Dl += "function calc(){\n"
Dl += "  var dv=DI.value,lat=parseFloat(LA.value);\n"
Dl += "  if(!dv||!isFinite(lat)){document.getElementById('dh-out').textContent='\\u2013';document.title='Daylight Hours Calculator - ToolDune';return;}\n"
Dl += "  var day=new Date(dv+'T12:00:00');\n"
Dl += "  var len=dayLen(day,lat);\n"
Dl += "  var next=dayLen(new Date(day.getTime()+86400000),lat);\n"
Dl += "  var perDay=Math.round((next-len)*60);\n"
Dl += "  var longest=dayLen(new Date(day.getFullYear(),5,21),lat), shortest=dayLen(new Date(day.getFullYear(),11,21),lat);\n"
Dl += "  var txt=len>=1?fmtHM(len):'0 h';\n"
Dl += "  document.getElementById('dh-out').textContent=txt;\n"
Dl += "  document.getElementById('dh-s1').textContent=fmtHM(longest);\n"
Dl += "  document.getElementById('dh-s2').textContent=fmtHM(shortest);\n"
Dl += "  document.getElementById('dh-s3').textContent=(perDay>=0?'+':'')+perDay+' min';\n"
Dl += "  var msg='The clock answer comes from the sun geometry - day length depends only on your latitude and the date, give or take a few minutes for the atmosphere bending light at the horizon. ';\n"
Dl += "  if(len<10&&lat>0){msg+='Under ten hours of daylight is where the winter blues start for most people: the fix with the best evidence is not the sunrise lamp, it is getting outside in the first hour after waking - even overcast sky beats indoor light by a wide margin. The clocks changing barely moves this; the season does (see the sleep-shift planner). ';}\n"
Dl += "  else{msg+='Heading into fall the losses run a few minutes a day - invisible daily, obvious monthly. ';}\n"
Dl += "  msg+='Between the longest and shortest day at your latitude sits '+fmtHM(longest-shortest)+' of light - the whole drama of the season in one number.';\n"
Dl += "  document.getElementById('dh-note').textContent=msg;\n"
Dl += "  document.title=fmtHM(len)+' of daylight - ToolDune';\n"
Dl += "}\n"
Dl += "function save(){try{localStorage.setItem('tt_daylight',JSON.stringify({d:DI.value,l:LA.value}));}catch(e){}}\n"
Dl += "[DI,LA].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Dl += "var pre=false;\n"
Dl += "var qs=new URLSearchParams(location.search);\n"
Dl += "if(qs.get('lat')){LA.value=qs.get('lat');pre=true;}\n"
Dl += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_daylight')||'null');if(m){if(m.d){DI.value=m.d;}if(m.l){LA.value=m.l;}}}catch(e){}}\n"
Dl += "if(!DI.value){var td=new Date();DI.value=td.getFullYear()+'-'+('0'+(td.getMonth()+1)).slice(-2)+'-'+('0'+td.getDate()).slice(-2);}\n"
Dl += "calc();\n"
Dl += "document.getElementById('dh-share').addEventListener('click',function(){\n"
Dl += "  var txt=DI.value+' gets '+document.getElementById('dh-out').textContent+' of daylight at latitude '+LA.value+'. Check yours:';\n"
Dl += "  var url=location.origin+location.pathname+'?lat='+encodeURIComponent(LA.value);\n"
Dl += "  if(navigator.share){navigator.share({title:'Daylight hours',text:txt,url:url}).catch(function(){});}\n"
Dl += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my daylight math';},1500);}\n"
Dl += "});\n"
Dl += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: HOLIDAYTIP ----------
Ht = 'HOLIDAYTIP = """<div class="tool" id="tt-ht">\n'
Ht += '  <div class="fields">\n'
Ht += '    <div class="field"><label for="ht-b">Total holiday tipping budget</label><input id="ht-b" type="number" min="0" value="300"></div>\n'
Ht += '    <div class="field"><label for="ht-w">Weekly regulars (cleaner, dog walker...)</label><input id="ht-w" type="number" min="0" max="20" value="1"></div>\n'
Ht += '    <div class="field"><label for="ht-o">Occasional helpers (hairdresser, babysitter...)</label><input id="ht-o" type="number" min="0" max="20" value="3"></div>\n'
Ht += '  </div>\n'
Ht += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ht-out">&#8211;</span><span class="result-unit">per weekly regular</span></div>\n'
Ht += '  <div class="stats">\n'
Ht += '    <div class="stat"><b id="ht-s1">&#8211;</b><span>per occasional helper</span></div>\n'
Ht += '    <div class="stat"><b id="ht-s2">&#8211;</b><span>to weekly regulars total</span></div>\n'
Dl_dummy = None
Ht += '    <div class="stat"><b id="ht-s3">&#8211;</b><span>left for the card people</span></div>\n'
Ht += '  </div>\n'
Ht += '  <div class="tool-note" id="ht-note"></div>\n'
Ht += '  <button type="button" class="tool-btn" id="ht-share">Share my tipping plan</button>\n'
Ht += '</div>\n'
Ht += '<script>(function(){\n'
Ht += "var B=document.getElementById('ht-b'),W=document.getElementById('ht-w'),O=document.getElementById('ht-o');\n"
Ht += "function calc(){\n"
Ht += "  var b=parseFloat(B.value)||0,nw=Math.max(0,Math.round(parseFloat(W.value)||0)),no=Math.max(0,Math.round(parseFloat(O.value)||0));\n"
Ht += "  var bw=no>=0?b*0.6:b, bo=b-bw;\n"
Ht += "  var perW=nw>0?bw/nw:0, perO=no>0?bo/no:0;\n"
Ht += "  var d1=Math.round(perW), d2=Math.round(perO), d3=Math.round(bw);\n"
Ht += "  document.getElementById('ht-out').textContent=nw>0?('$'+d1):'\\u2013';\n"
Ht += "  document.getElementById('ht-s1').textContent=no>0?('$'+d2):'\\u2013';\n"
Ht += "  document.getElementById('ht-s2').textContent='$'+d3;\n"
Ht += "  document.getElementById('ht-s3').textContent='$'+Math.round(bo);\n"
Ht += "  document.getElementById('ht-note').textContent='The split rule: the people who touch your life weekly get about 60 percent of the budget - one visit fee is the classic for a cleaner or dog walker - and occasional helpers split the rest. Three honest caps the greeting-card industry will not print: USPS carriers may not accept cash beyond 20 dollars (a gift card or consumables work), many school districts bar teachers from cash so aim at classroom supplies or a small gift card, and the super who fixed nothing all year still gets something small if you may need him in January. When the budget is tight, frequency beats warmth: the person who was there every week outranks everyone you met twice.';\n"
Ht += "  document.title='Tipping plan: $'+d1+' per regular - ToolDune';\n"
Ht += "}\n"
Ht += "function save(){try{localStorage.setItem('tt_holidaytip',JSON.stringify({b:B.value,w:W.value,o:O.value}));}catch(e){}}\n"
Ht += "[B,W,O].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Ht += "var pre=false;\n"
Ht += "var qs=new URLSearchParams(location.search);\n"
Ht += "if(qs.get('b')){B.value=qs.get('b');pre=true;}\n"
Ht += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_holidaytip')||'null');if(m){if(m.b){B.value=m.b;}if(m.w){W.value=m.w;}if(m.o){O.value=m.o;}}}catch(e){}}\n"
Ht += "calc();\n"
Ht += "document.getElementById('ht-share').addEventListener('click',function(){\n"
Ht += "  var txt='My holiday tipping plan: '+W.value+' regulars at about $'+document.getElementById('ht-out').textContent+' each. Plan yours:';\n"
Ht += "  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value);\n"
Ht += "  if(navigator.share){navigator.share({title:'Holiday tipping plan',text:txt,url:url}).catch(function(){});}\n"
Ht += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my tipping plan';},1500);}\n"
Ht += "});\n"
Ht += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: DONATE ----------
Dn = 'DONATE = """<div class="tool" id="tt-dn">\n'
Dn += '  <div class="fields">\n'
Dn += '    <div class="field"><label for="dn-a">Amount you plan to give</label><input id="dn-a" type="number" min="0" value="500"></div>\n'
Dn += '    <div class="field"><label for="dn-r">Marginal tax rate (%)</label><select id="dn-r"><option value="12">12%</option><option value="22" selected>22%</option><option value="24">24%</option><option value="32">32%</option><option value="35">35%</option></select></div>\n'
Dn += '  </div>\n'
Dn += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dn-out">&#8211;</span><span class="result-unit">real cost after tax break</span></div>\n'
Dn += '  <div class="stats">\n'
Dn += '    <div class="stat"><b id="dn-s1">&#8211;</b><span>tax saved if you itemize</span></div>\n'
Dn += '    <div class="stat"><b id="dn-s2">&#8211;</b><span>days left this year</span></div>\n'
Dn += '    <div class="stat"><b id="dn-s3">&#8211;</b><span>receipt rule at your amount</span></div>\n'
Dn += '  </div>\n'
Dn += '  <div class="tool-note" id="dn-note"></div>\n'
Dn += '  <button type="button" class="tool-btn" id="dn-share">Share my giving math</button>\n'
Dn += '</div>\n'
Dn += '<script>(function(){\n'
Dn += "var A=document.getElementById('dn-a'),R=document.getElementById('dn-r');\n"
Dn += "function calc(){\n"
Dn += "  var a=parseFloat(A.value)||0,r=parseFloat(R.value)||0;\n"
Dn += "  var saved=a*r/100, cost=a-saved;\n"
Dn += "  var now=new Date();\n"
Dl_dummy2 = None
Dn += "  var eoy=new Date(now.getFullYear(),11,31);\n"
Dn += "  var days=Math.ceil((eoy-now)/86400000);\n"
Dn += "  var d1=Math.round(saved*10)/10, d2=Math.round(cost*10)/10;\n"
Dn += "  document.getElementById('dn-out').textContent='$'+d2;\n"
Dn += "  document.getElementById('dn-s1').textContent='$'+d1;\n"
Dn += "  document.getElementById('dn-s2').textContent=days;\n"
Dn += "  document.getElementById('dn-s3').textContent=a>=250?'acknowledgment letter required':'bank or card record is enough';\n"
Dn += "  document.getElementById('dn-note').textContent='The honest headline first: since the standard deduction roughly doubled, about 90 percent of filers no longer itemize - and if you take the standard deduction, charitable giving saves no tax at all. The workaround is bunching: give two years worth in one December, itemize that year, take the standard deduction the next. Two more levers people miss: an online card gift counts on the day you swipe it, so December 31 at 11 pm is still this year, and donating appreciated stock you have held over a year avoids the capital gains entirely - a move that works at 500 dollars, not just at foundation scale. Give to the charity, not to the deadline panic: a smaller gift you actually planned beats a rushed one you regret.';\n"
Dn += "  document.title='Giving: $'+d2+' real cost, '+days+' days left - ToolDune';\n"
Dn += "}\n"
Dn += "function save(){try{localStorage.setItem('tt_donate',JSON.stringify({a:A.value,r:R.value}));}catch(e){}}\n"
Dn += "[A,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Dn += "var pre=false;\n"
Dn += "var qs=new URLSearchParams(location.search);\n"
Dn += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Dn += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_donate')||'null');if(m){if(m.a){A.value=m.a;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Dn += "calc();\n"
Dn += "document.getElementById('dn-share').addEventListener('click',function(){\n"
Dn += "  var txt='A $'+A.value+' gift really costs $'+document.getElementById('dn-out').textContent+' after the tax break - if you itemize. Run yours:';\n"
Dn += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Dn += "  if(navigator.share){navigator.share({title:'Charitable giving math',text:txt,url:url}).catch(function(){});}\n"
Dn += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my giving math';},1500);}\n"
Dn += "});\n"
Dn += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("DAYLIGHT", "HOLIDAYTIP", "DONATE"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Dl + Ht + Dn + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "humidsize": lambda args: HUMIDSIZE,',
    '    "humidsize": lambda args: HUMIDSIZE,\n'
    '    "daylight": lambda args: DAYLIGHT,\n'
    '    "holidaytip": lambda args: HOLIDAYTIP,\n'
    '    "donate": lambda args: DONATE,')
sub(BUILD_P, '    "lightcost": "💡", "furnfilter": "📏", "humidsize": "💧",',
    '    "lightcost": "💡", "furnfilter": "📏", "humidsize": "💧",\n'
    '    "daylight": "☀", "holidaytip": "🎁", "donate": "💝",')

P = []
d = {'slug': 'daylight-hours-calculator',
     'title': 'Daylight Hours Calculator - Day Length by Date and Latitude',
     'h1': 'Daylight Hours Calculator',
     'desc': 'Any date plus your latitude gives the exact day length, the seasonal longest and shortest, and minutes gained or lost per day - with the winter-light honesty note. Free.',
     'category': 'calculator',
     'keyword': 'daylight hours calculator day length by date',
     'tool': 'daylight',
     'args': {},
     'intro': ["Pick a date and set your latitude - 40 is about the US average. The calculator runs the sun geometry and returns the day length, the longest and shortest days at your latitude, and how many minutes a day you are gaining or losing right now.",
              "Sunrise-sunset tables bury the number people actually want: how much light the day holds, and how fast it is leaving. This one answers that - and says the quiet part about under-ten-hour days: the best-evidenced fix for the winter blues is morning outdoor light, not the desk lamp."],
     'howto': ["Set the date you are curious about - today is preloaded.",
               "Set latitude: about 40 for the US mid-band, 51 for London, 66 is the Arctic Circle.",
               "Watch the per-day change flip sign at the solstices."],
     'faqs': [("How many hours of daylight in winter?",
               "It depends almost entirely on latitude: at 40 degrees north the shortest day runs about 9 hours 20 minutes; at 50 degrees (Frankfurt, Winnipeg edges) it drops under 8; inside the Arctic Circle the sun never rises. The calculator gives your exact figure."),
              ("How fast do we lose daylight in fall?",
               "The steepest losses sit near the equinox - around 3 minutes a day at 40 degrees north, faster the further north you go - slowing to zero at the solstice. Daily it is invisible; over October it adds up to nearly an hour and a half."),
              ("Does daylight saving time change daylight hours?",
               "No - it moves an hour of light from morning to evening (or back). The sun gives the same day length either way; only the clock labels shift. That is why the sleep-shift plan and the daylight math are separate questions."),
              ("Why is my sunrise table a few minutes off this result?",
               "Day length as computed here uses pure geometry; real sunrise tables add atmospheric refraction and the solar disc radius, stretching the day by several minutes at the edges. For planning your daylight, the geometry is the honest middle.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'holiday-tipping-calculator',
     'title': 'Holiday Tipping Calculator - Year-End Budget Split by Recipient',
     'h1': 'Holiday Tipping Calculator',
     'desc': 'Your year-end tipping budget splits across weekly regulars and occasional helpers - with the USPS cap, the teacher rules and the frequency-beats-warmth principle. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'holiday tipping guide calculator how much to give',
     'tool': 'holidaytip',
     'args': {},
     'intro': ["Set your total budget and count who is actually on the list - weekly regulars like a cleaner or dog walker, occasional helpers like a hairdresser or sitter. The calculator splits it on the classic rule: weekly people take about 60 percent, one-visit fee as the benchmark.",
              "Greeting-card tipping guides list everyone equally and leave you guilty. This one prices the real hierarchy - frequency beats warmth: the person who showed up every week outranks everyone you met twice - and prints the three caps the cards never mention: USPS cash limits, school-district teacher rules, and the super who fixed nothing."],
     'howto': ["Set a total you can afford first - guilt is not a budget line.",
               "Count weekly regulars and occasional helpers honestly.",
               "Read the caps note before you hand anyone an envelope."],
     'faqs': [("How much should I tip my house cleaner for the holidays?",
               "The standard is one full visit fee, or a week of service for long-standing weekly arrangements - whichever your budget runs to. If cost splits a year of goodwill, a sincere note plus a smaller envelope beats silence."),
              ("Can I tip my mail carrier?",
               "Not in cash beyond 20 dollars - USPS employees may not accept money gifts, per federal rules. A gift card under the limit, or snacks and a note, are the compliant route. The same cap-and-gift-card logic applies to many public employees."),
              ("Should I give my child's teacher a gift?",
               "Check the district first - many bar cash gifts entirely. The safe play is a small gift card plus a note about something specific they did, or classroom supplies. The handwritten note from your child outperforms every envelope."),
              ("Who do I tip when the budget is tight?",
               "Rank by frequency and dependence: the people who came weekly all year first, then anyone who handled something hard for you, then everyone else gets a card. A smaller gift to the right person beats an even spread that says nothing to anyone.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'donation-deadline-calculator',
     'title': 'Donation Deadline Calculator - Real Cost, Tax Math and December 31',
     'h1': 'Donation Deadline Calculator',
     'desc': 'Your gift amount and bracket give the real after-tax cost, the days left this year, and the receipt rules - plus the bunching move most filers never hear about. Free.',
     'category': 'calculator',
     'keyword': 'charitable donation tax deduction deadline calculator',
     'tool': 'donate',
     'args': {},
     'intro': ["Enter what you plan to give and your tax bracket. The calculator shows the tax saved if you itemize, the real after-tax cost of the gift, the days left before the December 31 deadline, and the receipt rule that applies at your amount.",
              "Year-end giving posts push urgency and skip the fine print. This one leads with the honest headline - since the standard deduction doubled, most filers get no deduction at all - then prices the real levers: bunching two years of giving into one December, swiping the card before midnight, and donating appreciated stock even at modest amounts."],
     'howto': ["Set the amount and your marginal bracket from your last return.",
               "Check whether you itemize - if not, read the bunching note twice.",
               "Give before December 31; the card swipe date is what counts."],
     'faqs': [("How much does a 500 dollar donation save in taxes?",
               "At the 22 percent bracket, 110 dollars - but only if you itemize. Since the standard deduction roughly doubled in 2018, about 90 percent of filers take the standard deduction instead, and charitable gifts then save nothing. The calculator says which world you are in."),
              ("What is the deadline for tax-deductible donations?",
               "December 31 of the tax year. An online card gift counts on the swipe date - December 31 at 11 pm is still this year - and a mailed check counts by postmark. Payroll-deduction gifts count when deducted from pay, even if the charity receives it later."),
              ("What receipt do I need for a donation?",
               "Under 250 dollars, a bank record or receipt is enough. At 250 dollars or more, the charity must send an acknowledgment letter stating whether they gave you anything in return - the IRS rejects the deduction without it. Get it before filing, not before December 31."),
              ("How does donating stock instead of cash help?",
               "If you have held appreciated shares over a year, donating them avoids the capital gains tax entirely and still books the full value as a deduction if you itemize. The move works at 500-dollar scale, not just for foundations - brokers handle the transfer in days, so start before mid-December.")]}
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
print("R141 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
