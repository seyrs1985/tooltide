# -*- coding: utf-8 -*-
"""R168 二月窗三连:super-bowl-squares(奖池分账)+spring-break-budget(春假人均)+tax-refund-planner(退税分派)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: SQUARES ----------
Sq = 'SQUARES = """<div class="tool" id="tt-sq2">\n'
Sq += '  <div class="fields">\n'
Sq += '    <div class="field"><label for="sq2-p">Price per square</label><input id="sq2-p" type="number" min="1" value="25"></div>\n'
Sq += '    <div class="field"><label for="sq2-x">Payout split by quarter (Q1/Q2/Q3/final %)</label><select id="sq2-x"><option value="10,30,40,20" selected>10 / 30 / 40 / 20 - final weighs most</option><option value="25,25,25,25">25 / 25 / 25 / 25 - even</option><option value="20,20,20,40">20 / 20 / 20 / 40 - finale heavy</option></select></div>\n'
Sq += '  </div>\n'
Sq += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sq2-out">&#8211;</span><span class="result-unit">total pool</span></div>\n'
Sq += '  <div class="stats">\n'
Sq += '    <div class="stat"><b id="sq2-s1">&#8211;</b><span>Q1 winner gets</span></div>\n'
Sq += '    <div class="stat"><b id="sq2-s2">&#8211;</b><span>final score winner gets</span></div>\n'
Sq += '    <div class="stat"><b id="sq2-s3">&#8211;</b><span>house keeps (should be 0)</span></div>\n'
Dj_dummy3 = None
Sq += '  </div>\n'
Sq += '  <div class="tool-note" id="sq2-note"></div>\n'
Sq += '  <button type="button" class="tool-btn" id="sq2-share">Share my pool math</button>\n'
Sq += '</div>\n'
Sq += '<script>(function(){\n'
Sq += "var P=document.getElementById('sq2-p'),X=document.getElementById('sq2-x');\n"
Sq += "function calc(){\n"
Sq += "  var p=parseFloat(P.value)||25,parts=X.value.split(','),pool=p*100;\n"
Sq += "  var q1=pool*parseFloat(parts[0])/100,q2=pool*parseFloat(parts[1])/100,q3=pool*parseFloat(parts[2])/100,q4=pool*parseFloat(parts[3])/100;\n"
Sq += "  var d1=Math.round(q1), d4=Math.round(q4);\n"
Sq += "  document.getElementById('sq2-out').textContent='$'+Math.round(pool);\n"
Sq += "  document.getElementById('sq2-s1').textContent='$'+d1;\n"
Sq += "  document.getElementById('sq2-s2').textContent='$'+d4;\n"
Sq += "  document.getElementById('sq2-s3').textContent='$0';\n"
Sq += "  document.getElementById('sq2-note').textContent='The format that keeps friendships: draw the numbers only after every square is sold, and the pool pays out everything - the house cut is what turns a game into a grudge. Your squares inherit two random digits, one per team, and the good ones are the boring endings: 0, 3, 4 and 7 win quarters far more than the lucky 2 or 5, because football scoring does arithmetic in field goals and touchdowns. Payout across the quarters means every score change re-lotteries the room, which is the entire entertainment value for people who do not care about the game.';\n"
Sq += "  document.title='Squares pool: $'+Math.round(pool)+', final pays $'+d4+' - ToolDune';\n"
Sq += "}\n"
Sq += "function save(){try{localStorage.setItem('tt_squares',JSON.stringify({p:P.value,x:X.value}));}catch(e){}}\n"
Sq += "[P,X].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Sq += "var pre=false;\n"
Sq += "var qs=new URLSearchParams(location.search);\n"
Sq += "if(qs.get('p')){P.value=qs.get('p');pre=true;}\n"
Sq += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_squares')||'null');if(m){if(m.p){P.value=m.p;}if(m.x){X.value=m.x;}}}catch(e){}}\n"
Sq += "calc();\n"
Sq += "document.getElementById('sq2-share').addEventListener('click',function(){\n"
Sq += "  var txt='Our squares pool: $'+P.value+' a square, $'+Math.round(pool)+' total, final quarter pays $'+document.getElementById('sq2-s2').textContent+'. Set yours up:';\n"
Sq += "  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value);\n"
Sq += "  if(navigator.share){navigator.share({title:'Squares pool math',text:txt,url:url}).catch(function(){});}\n"
Sq += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my pool math';},1500);}\n"
Sq += "});\n"
Sq += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: SPRINGBREAK ----------
Sb = 'SPRINGBREAK = """<div class="tool" id="tt-sbk">\n'
Sb += '  <div class="fields">\n'
Sb += '    <div class="field"><label for="sbk-n">Travelers</label><input id="sbk-n" type="number" min="1" max="12" value="4"></div>\n'
Sb += '    <div class="field"><label for="sbk-f">Flight per person</label><input id="sbk-f" type="number" min="20" value="350"></div>\n'
Sb += '    <div class="field"><label for="sbk-l">Lodging total for the stay</label><input id="sbk-l" type="number" min="0" value="1200"></div>\n'
Sb += '    <div class="field"><label for="sbk-d">Days on the ground</label><input id="sbk-d" type="number" min="1" max="21" value="5"></div>\n'
Sb += '    <div class="field"><label for="sbk-f2">Food and fun per person per day</label><input id="sbk-f2" type="number" min="10" value="60"></div>\n'
Sb += '  </div>\n'
Sb += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sbk-out">&#8211;</span><span class="result-unit">per person, all in</span></div>\n'
Sb += '  <div class="stats">\n'
Sb += '    <div class="stat"><b id="sbk-s1">&#8211;</b><span>whole group total</span></div>\n'
Sb += '    <div class="stat"><b id="sbk-s2">&#8211;</b><span>daily burn per person</span></div>\n'
Sb += '    <div class="stat"><b id="sbk-s3">&#8211;</b><span>the room-share lever</span></div>\n'
Sb += '  </div>\n'
Sb += '  <div class="tool-note" id="sbk-note"></div>\n'
Sb += '  <button type="button" class="tool-btn" id="sbk-share">Share my break budget</button>\n'
Sb += '</div>\n'
Sb += '<script>(function(){\n'
Sb += "var N=document.getElementById('sbk-n'),F=document.getElementById('sbk-f'),L=document.getElementById('sbk-l'),D=document.getElementById('sbk-d'),F2=document.getElementById('sbk-f2');\n"
Sb += "function calc(){\n"
Sb += "  var n=Math.max(1,Math.round(parseFloat(N.value)||4)),fl=parseFloat(F.value)||0,lo=parseFloat(L.value)||0,d=Math.max(1,parseFloat(D.value)||5),ff=parseFloat(F2.value)||0;\n"
Sb += "  var per=fl+lo/n+ff*d, total=per*n, daily=fl/365+lo/n/d+ff;\n"
Sb += "  var d1=Math.round(total), d2=Math.round(per/d*100)/100;\n"
Sb += "  document.getElementById('sbk-out').textContent='$'+Math.round(per);\n"
Sb += "  document.getElementById('sbk-s1').textContent='$'+d1;\n"
Sb += "  document.getElementById('sbk-s2').textContent='$'+d2;\n"
Sb += "  document.getElementById('sbk-s3').textContent='n splits it';\n"
Sb += "  document.getElementById('sbk-note').textContent='The booking window is the money lever: spring break flights priced in January run visibly cheaper than the February panic, and lodging splits are where the group math lives - the fourth traveler is the one who makes the rental work. Groceries for breakfasts and a cooler for lunches cut the food line roughly in half without touching the fun. And the deposit conversation before booking beats the spreadsheet after: one person floats the rental, everyone transfers their share within the week, and the friendship survives the group chat.';\n"
Sb += "  document.title='Spring break: $'+Math.round(per)+' per person - ToolDune';\n"
Sb += "}\n"
Sb += "function save(){try{localStorage.setItem('tt_springbreak',JSON.stringify({n:N.value,f:F.value,l:L.value,d:D.value,f2:F2.value}));}catch(e){}}\n"
Sb += "[N,F,L,D,F2].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Sb += "var pre=false;\n"
Sb += "var qs=new URLSearchParams(location.search);\n"
Sb += "if(qs.get('n')){N.value=qs.get('n');pre=true;}\n"
Sb += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_springbreak')||'null');if(m){if(m.n){N.value=m.n;}if(m.f){F.value=m.f;}if(m.l){L.value=m.l;}if(m.d){D.value=m.d;}if(m.f2){F2.value=m.f2;}}}catch(e){}}\n"
Sb += "calc();\n"
Sb += "document.getElementById('sbk-share').addEventListener('click',function(){\n"
Sb += "  var txt='Spring break runs $'+document.getElementById('sbk-out').textContent+' per person all in. Budget yours:';\n"
Sb += "  var url=location.origin+location.pathname+'?n='+encodeURIComponent(N.value);\n"
Sb += "  if(navigator.share){navigator.share({title:'Spring break budget',text:txt,url:url}).catch(function(){});}\n"
Sb += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my break budget';},1500);}\n"
Sb += "});\n"
Sb += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: REFUNDPLAN ----------
Rp = 'REFUNDPLAN = """<div class="tool" id="tt-rp">\n'
Rp += '  <div class="fields">\n'
Rp += '    <div class="field"><label for="rp-r">Expected refund</label><input id="rp-r" type="number" min="100" value="3000"></div>\n'
Rp += '    <div class="field"><label for="rp-a">APR on your highest card (%)</label><input id="rp-a" type="number" min="0" max="40" step="0.5" value="22"></div>\n'
Rp += '    <div class="field"><label for="rp-f">Fun share (%)</label><input id="rp-f" type="number" min="0" max="50" value="20"></div>\n'
Rp += '  </div>\n'
Rp += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rp-out">&#8211;</span><span class="result-unit">saved in interest this year</span></div>\n'
Rp += '  <div class="stats">\n'
Rp += '    <div class="stat"><b id="rp-s1">&#8211;</b><span>to the card</span></div>\n'
Rp += '    <div class="stat"><b id="rp-s2">&#8211;</b><span>to the emergency fund</span></div>\n'
Rp += '    <div class="stat"><b id="rp-s3">&#8211;</b><span>guilt-free fun</span></div>\n'
Rp += '  </div>\n'
Rp += '  <div class="tool-note" id="rp-note"></div>\n'
Rp += '  <button type="button" class="tool-btn" id="rp-share">Share my split</button>\n'
Rp += '</div>\n'
Rp += '<script>(function(){\n'
Rp += "var Rr=document.getElementById('rp-r'),A=document.getElementById('rp-a'),F=document.getElementById('rp-f');\n"
Rp += "function calc(){\n"
Rp += "  var ref=parseFloat(Rr.value)||0,apr=(parseFloat(A.value)||0)/100,fun=parseFloat(F.value)||0;\n"
Rp += "  var funAmt=ref*fun/100, rest=ref-funAmt, toCard=rest*0.7, toEm=rest*0.3;\n"
Rp += "  var interest=toCard*apr;\n"
Rp += "  var d1=Math.round(toCard), d2=Math.round(toEm), d3=Math.round(funAmt);\n"
Rp += "  document.getElementById('rp-out').textContent='$'+Math.round(interest);\n"
Rp += "  document.getElementById('rp-s1').textContent='$'+d1;\n"
Rp += "  document.getElementById('rp-s2').textContent='$'+d2;\n"
Rp += "  document.getElementById('rp-s3').textContent='$'+d3;\n"
Rp += "  document.getElementById('rp-note').textContent='The split here is 70/30 between card and emergency fund after the fun share - debt first because the interest saving is a guaranteed return, emergency second because that fund is what keeps the next refund from also going to a card. The pro move nobody loves: a refund is an interest-free loan you gave the government all year, and adjusting your withholding turns next year refund into monthly take-home. And the seasonal warning that saves real money - refund season is phishing season, and the IRS does not call, text or email first, ever.';\n"
Rp += "  document.title='Refund split saves $'+Math.round(interest)+' in interest - ToolDune';\n"
Rp += "}\n"
Rp += "function save(){try{localStorage.setItem('tt_refundplan',JSON.stringify({r:Rr.value,a:A.value,f:F.value}));}catch(e){}}\n"
Rp += "[Rr,A,F].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Rp += "var pre=false;\n"
Rp += "var qs=new URLSearchParams(location.search);\n"
Rp += "if(qs.get('r')){Rr.value=qs.get('r');pre=true;}\n"
Rp += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_refundplan')||'null');if(m){if(m.r){Rr.value=m.r;}if(m.a){A.value=m.a;}if(m.f){F.value=m.f;}}}catch(e){}}\n"
Rp += "calc();\n"
Rp += "document.getElementById('rp-share').addEventListener('click',function(){\n"
Rp += "  var txt='My refund split saves $'+document.getElementById('rp-out').textContent+' in card interest this year. Run yours:';\n"
Rp += "  var url=location.origin+location.pathname+'?r='+encodeURIComponent(Rr.value);\n"
Rp += "  if(navigator.share){navigator.share({title:'Tax refund split',text:txt,url:url}).catch(function(){});}\n"
Rp += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my split';},1500);}\n"
Rp += "});\n"
Rp += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("SQUARES", "SPRINGBREAK", "REFUNDPLAN"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Sq + Sb + Rp + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "bedsoil": lambda args: BEDSOIL,',
    '    "bedsoil": lambda args: BEDSOIL,\n'
    '    "squares": lambda args: SQUARES,\n'
    '    "springbreak": lambda args: SPRINGBREAK,\n'
    '    "refundplan": lambda args: REFUNDPLAN,')
sub(BUILD_P, '    "datenight": "💘", "seedstart": "🌱", "bedsoil": "🌾",',
    '    "datenight": "💘", "seedstart": "🌱", "bedsoil": "🌾",\n'
    '    "squares": "🏈", "springbreak": "🌴", "refundplan": "💸",')

P = []
d = {'slug': 'super-bowl-squares-calculator',
     'title': 'Super Bowl Squares Calculator - Pool, Payouts and the Split',
     'h1': 'Super Bowl Squares Calculator',
     'desc': 'Square price times 100 gives the pool, and the payout split by quarter shows exactly what each winner collects - with the house-cut rule. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'super bowl squares calculator payout split pool',
     'tool': 'squares',
     'args': {},
     'intro': ["Enter the price per square and pick a payout split. The calculator totals the 100-square pool and shows what each quarter winner collects - including the final-score payout under the classic 10/30/40/20 format.",
              "The format that keeps friendships: draw numbers only after every square is sold, pay out everything - the house cut is what turns a game into a grudge - and remember that 0, 3, 4 and 7 win quarters far more than lucky 2 or 5, because football scoring does arithmetic in field goals and touchdowns."],
     'howto': ["Set the square price - 25 dollars makes a 2,500 pool.",
               "Pick the payout split; the final quarter usually weighs most.",
               "Draw numbers after the grid fills, never before."],
     'faqs': [("How do Super Bowl squares payouts work?",
               "The 100-square pool pays four winners - one per quarter under your chosen split. The classic format pays 10/30/40/20, weighting the final score; even 25s across the quarters keeps every score change exciting."),
              ("What are the best numbers in a squares pool?",
               "0, 7, 3 and 4 dominate, in that order - football scores move in sevens and threes, so squares ending in those digits hit quarters far more often. A 2-2 square is a lottery ticket; 0-0 is practically an investment."),
              ("When should numbers be drawn for squares?",
               "After every square is sold. Drawing numbers first lets people buy the good combinations and turns a fun pool into a race - the redraw-after-fill convention is what keeps it fair."),
              ("Should the pool organizer keep a cut?",
               "No - the standard format pays out the entire pool. The organizer keeps their full square like everyone else; a house cut is the fastest way to run the last squares pool your group ever does.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'spring-break-budget-calculator',
     'title': 'Spring Break Budget Calculator - Per Person Cost, All In',
     'h1': 'Spring Break Budget Calculator',
     'desc': 'Flights, shared lodging, days and the daily food-and-fun line give the per-person cost, the group total and the daily burn. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'spring break budget calculator cost per person college',
     'tool': 'springbreak',
     'args': {},
     'intro': ["Enter the traveler count, flights, the lodging total, days on the ground and the daily food-and-fun line. The calculator gives the per-person all-in cost, the whole-group total, and the daily burn rate.",
              "The booking window is the money lever - January prices for March trips run visibly cheaper than the February panic - and the lodging split is where the group math lives: the fourth traveler is the one who makes the rental work. Groceries for breakfasts and a cooler for lunches cut the food line roughly in half without touching the fun."],
     'howto': ["Flights first - they are the line that moves fastest.",
               "Split the lodging by heads, not by rooms.",
               "Set the food line honestly; the cooler is the budget cheat code."],
     'faqs': [("How much does spring break cost per person?",
               "A typical flight-plus-rental trip runs 700-1,200 per person for five days depending on destination and group size - the rental split and the food line are where the range lives. The calculator prices your exact plan."),
              ("When should I book spring break flights?",
               "January. Leisure routes price low while demand is planning-stage and spike through February - the same seat that is 350 in January runs 500 at the panic window."),
              ("How do groups split vacation costs fairly?",
               "Split lodging by heads, track shared groceries in a single pot, and transfer individual shares within a week of booking. One person floats, everyone repays fast - the deposit conversation before booking beats the spreadsheet after."),
              ("How do students save on spring break?",
               "The fourth traveler halves the lodging; groceries for breakfast and lunch cut the food line about in half; and traveling one week off-peak moves every price down a tier without changing the trip.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'tax-refund-planner',
     'title': 'Tax Refund Planner - The 70/30 Split That Saves Real Interest',
     'h1': 'Tax Refund Planner',
     'desc': 'Your refund split between the highest-APR card, the emergency fund and a guilt-free fun share - with the interest saved and the phishing warning. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'what to do with tax refund calculator split savings debt',
     'tool': 'refundplan',
     'args': {},
     'intro': ["Enter your expected refund, the APR on your highest card, and the fun share you can live with. The calculator splits the rest 70/30 between the card and the emergency fund and shows the interest the card payment saves this year.",
              "The order is not moral, it is mathematical: debt first because the interest saving is a guaranteed return, emergency fund second because it is what keeps the next refund from also going to a card. The pro move is withholding tuning - a refund is an interest-free loan you gave the government all year."],
     'howto': ["Refund estimate from your filing software, the day it lands.",
               "Enter the APR on your highest-rate card - the guaranteed-return rate.",
               "Keep a fun share; budgets with zero fun do not survive February."],
     'faqs': [("What should I do with my tax refund?",
               "The standard honest order: high-interest debt first (the interest saved is a guaranteed return), emergency fund second, and a planned fun share so the budget survives February. The calculator prices the split at your numbers."),
              ("Is a tax refund bad for your finances?",
               "A big refund means you lent the government money interest-free all year. It feels like a bonus but it was your take-home; adjusting withholding converts next year refund into monthly cash flow - the refund-happy habit is quietly expensive."),
              ("How much of my refund should go to savings?",
               "Whatever is left after high-APR debt: the emergency fund is the second priority because it prevents the next borrowing. Even 500 dollars in the buffer changes how the next car repair feels."),
              ("Are tax refund scams common?",
               "Refund season is phishing season - fake IRS calls, texts and refund-advance offers spike. The IRS does not call, text or email first, ever, and no legitimate service needs your full return by chat.")]}
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
print("R168 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
