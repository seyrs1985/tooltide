# -*- coding: utf-8 -*-
"""R162 年初账单三连:credit-min-payment(最低还款陷阱)+meal-prep-batch(备餐经济学)+heating-oil-tank(油罐续航)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: MINPAY ----------
Mp = 'MINPAY = """<div class="tool" id="tt-mp">\n'
Mp += '  <div class="fields">\n'
Mp += '    <div class="field"><label for="mp-b">Card balance</label><input id="mp-b" type="number" min="100" value="3000"></div>\n'
Mp += '    <div class="field"><label for="mp-a">APR (%)</label><input id="mp-a" type="number" min="0" max="40" step="0.5" value="22"></div>\n'
Mp += '    <div class="field"><label for="mp-f">What you pay monthly instead</label><input id="mp-f" type="number" min="10" value="150"></div>\n'
Mp += '  </div>\n'
Mp += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="mp-out">&#8211;</span><span class="result-unit">interest saved by paying more</span></div>\n'
Mp += '  <div class="stats">\n'
Mp += '    <div class="stat"><b id="mp-s1">&#8211;</b><span>years at minimum only</span></div>\n'
Mp += '    <div class="stat"><b id="mp-s2">&#8211;</b><span>interest at minimum only</span></div>\n'
Mp += '    <div class="stat"><b id="mp-s3">&#8211;</b><span>months at your payment</span></div>\n'
Mp += '  </div>\n'
Mp += '  <div class="tool-note" id="mp-note"></div>\n'
Mp += '  <button type="button" class="tool-btn" id="mp-share">Share my payoff math</button>\n'
Mp += '</div>\n'
Mp += '<script>(function(){\n'
Mp += "var B=document.getElementById('mp-b'),A=document.getElementById('mp-a'),F=document.getElementById('mp-f');\n"
Mp += "function calc(){\n"
Mp += "  var bal=parseFloat(B.value)||0,apr=(parseFloat(A.value)||0)/1200,fixed=parseFloat(F.value)||0;\n"
Mp += "  var b1=bal,mi=0,mn=0,guard=0;\n"
Mp += "  while(b1>0.5&&guard<1200){var int1=b1*apr;var pay=Math.max(25,b1*0.02);if(pay<=int1){mi=Infinity;break;}b1=b1+int1-pay;mi+=int1;mn++;guard++;}\n"
Mp += "  var b2=bal,fi=0,fn=0,guard2=0;\n"
Mp += "  while(b2>0.5&&guard2<1200){var int2=b2*apr;b2=b2+int2-fixed;fi+=int2;fn++;guard2++;if(fixed<=int2){fi=Infinity;break;}}\n"
Mp += "  var y1=mn/12, saved=(isFinite(mi)&&isFinite(fi))?(mi-fi):null;\n"
Mp += "  var d1=Math.round(y1*10)/10, d2=Math.round(mi), d3=Math.round(saved);\n"
Mp += "  document.getElementById('mp-out').textContent=(saved!==null&&saved>0)?('$'+d3):'see note';\n"
Mp += "  document.getElementById('mp-s1').textContent=d1;\n"
Mp += "  document.getElementById('mp-s2').textContent='$'+d2;\n"
Mp += "  document.getElementById('mp-s3').textContent=fn;\n"
Mp += "  document.getElementById('mp-note').textContent='The minimum is engineered, not helpful: at a 22 percent APR the interest alone eats most of a 2 percent minimum, so the balance barely moves for years - that is the business model working exactly as designed. The comparison line above is the same card paid at your fixed amount instead. Two moves that beat willpower: anything above the minimum goes entirely to principal, and a 0 percent balance-transfer card moves the balance for a one-time 3 percent fee - cheaper than a year of interest if you actually clear it inside the window.';\n"
Mp += "  document.title='Minimum payment costs $'+d2+' in interest - ToolDune';\n"
Mp += "}\n"
Mp += "function save(){try{localStorage.setItem('tt_minpay',JSON.stringify({b:B.value,a:A.value,f:F.value}));}catch(e){}}\n"
Mp += "[B,A,F].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Mp += "var pre=false;\n"
Mp += "var qs=new URLSearchParams(location.search);\n"
Mp += "if(qs.get('b')){B.value=qs.get('b');pre=true;}\n"
Mp += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_minpay')||'null');if(m){if(m.b){B.value=m.b;}if(m.a){A.value=m.a;}if(m.f){F.value=m.f;}}}catch(e){}}\n"
Mp += "calc();\n"
Mp += "document.getElementById('mp-share').addEventListener('click',function(){\n"
Mp += "  var txt='My card would charge $'+document.getElementById('mp-s2').textContent+' in interest on minimums. The fixed-payment math:';\n"
Mp += "  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value);\n"
Mp += "  if(navigator.share){navigator.share({title:'Minimum payment trap',text:txt,url:url}).catch(function(){});}\n"
Mp += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my payoff math';},1500);}\n"
Mp += "});\n"
Mp += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: MEALPREP ----------
Mpre = 'MEALPREP = """<div class="tool" id="tt-mpp">\n'
Mpre += '  <div class="fields">\n'
Mpre += '    <div class="field"><label for="mpp-w">Meals to cover per week</label><input id="mpp-w" type="number" min="1" max="21" value="5"></div>\n'
Mpre += '    <div class="field"><label for="mpp-p">Portions per batch</label><input id="mpp-p" type="number" min="1" max="20" value="4"></div>\n'
Mpre += '    <div class="field"><label for="mpp-c">Batch ingredient cost</label><input id="mpp-c" type="number" min="2" value="12"></div>\n'
Mpre += '    <div class="field"><label for="mpp-t">Your takeout cost per meal</label><input id="mpp-t" type="number" min="3" value="14"></div>\n'
Mpre += '  </div>\n'
Mpre += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="mpp-out">&#8211;</span><span class="result-unit">per meal, home batch</span></div>\n'
Mpre += '  <div class="stats">\n'
Mpre += '    <div class="stat"><b id="mpp-s1">&#8211;</b><span>saved per week</span></div>\n'
Mpre += '    <div class="stat"><b id="mpp-s2">&#8211;</b><span>batches to cook weekly</span></div>\n'
Mpre += '    <div class="stat"><b id="mpp-s3">&#8211;</b><span>year saving, 48 weeks</span></div>\n'
Mpre += '  </div>\n'
Mpre += '  <div class="tool-note" id="mpp-note"></div>\n'
Mpre += '  <button type="button" class="tool-btn" id="mpp-share">Share my prep math</button>\n'
Mpre += '</div>\n'
Mpre += '<script>(function(){\n'
Mpre += "var W=document.getElementById('mpp-w'),P=document.getElementById('mpp-p'),C=document.getElementById('mpp-c'),T=document.getElementById('mpp-t');\n"
Mpre += "function calc(){\n"
Mpre += "  var w=Math.max(1,Math.round(parseFloat(W.value)||5)),p=Math.max(1,parseFloat(P.value)||4),c=parseFloat(C.value)||12,t=parseFloat(T.value)||14;\n"
Mpre += "  var per=c/p, batches=Math.ceil(w/p), save=(t-per)*w, year=save*48;\n"
Mpre += "  var d1=Math.round(per*100)/100, d2=Math.round(save*10)/10, d3=Math.round(year);\n"
Mpre += "  document.getElementById('mpp-out').textContent='$'+d1;\n"
Mpre += "  document.getElementById('mpp-s1').textContent='$'+d2;\n"
Mpre += "  document.getElementById('mpp-s2').textContent=batches;\n"
Mpre += "  document.getElementById('mpp-s3').textContent='$'+d3;\n"
Mpre += "  document.getElementById('mpp-note').textContent='The takeout number is the honest one: fee, tip and tax add roughly a third on top of the menu price, which is why the comparison looks so lopsided. The honest counterweight is batch fatigue - five identical dinners by Wednesday kills the habit, so freeze half the batch and run two different recipes per week. A 2 hour Sunday cook covers the working week; the containers are a one-time cost and the freezer is the cheat code. January is when this math actually gets done - the same week the card statement from December arrives, which is not a coincidence.';\n"
Mpre += "  document.title='Batch meals: $'+d1+' each vs takeout - ToolDune';\n"
Mpre += "}\n"
Mpre += "function save(){try{localStorage.setItem('tt_mealprep',JSON.stringify({w:W.value,p:P.value,c:C.value,t:T.value}));}catch(e){}}\n"
Mpre += "[W,P,C,T].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Mpre += "var pre=false;\n"
Mpre += "var qs=new URLSearchParams(location.search);\n"
Mpre += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Mpre += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_mealprep')||'null');if(m){if(m.w){W.value=m.w;}if(m.p){P.value=m.p;}if(m.c){C.value=m.c;}if(m.t){T.value=m.t;}}}catch(e){}}\n"
Mpre += "calc();\n"
Mpre += "document.getElementById('mpp-share').addEventListener('click',function(){\n"
Mpre += "  var txt='Batch cooking brings my meals to $'+document.getElementById('mpp-out').textContent+' each - saving $'+document.getElementById('mpp-s1').textContent+' a week. Run yours:';\n"
Mpre += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
Mpre += "  if(navigator.share){navigator.share({title:'Meal prep economics',text:txt,url:url}).catch(function(){});}\n"
Mpre += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my prep math';},1500);}\n"
Mpre += "});\n"
Mpre += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: OILTANK ----------
Ot = 'OILTANK = """<div class="tool" id="tt-ot">\n'
Ot += '  <div class="fields">\n'
Ot += '    <div class="field"><label for="ot-s">Tank size (gallons)</label><select id="ot-s"><option value="275" selected>275 - basement</option><option value="330">330 - underground</option><option value="500">500 - large</option></select></div>\n'
Ot += '    <div class="field"><label for="ot-g">Gauge reading (%)</label><input id="ot-g" type="number" min="0" max="100" value="50"></div>\n'
Ot += '    <div class="field"><label for="ot-b">Winter burn rate (gallons/day)</label><input id="ot-b" type="number" min="0.5" step="0.5" value="5"></div>\n'
Ot += '    <div class="field"><label for="ot-p">Price per gallon</label><input id="ot-p" type="number" min="1" step="0.05" value="3.50"></div>\n'
Ot += '  </div>\n'
Ot += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ot-out">&#8211;</span><span class="result-unit">days of heat left</span></div>\n'
Ot += '  <div class="stats">\n'
Ot += '    <div class="stat"><b id="ot-s1">&#8211;</b><span>usable gallons now</span></div>\n'
Ot += '    <div class="stat"><b id="ot-s2">&#8211;</b><span>refill to full costs</span></div>\n'
Ot += '    <div class="stat"><b id="ot-s3">&#8211;</b><span>order-by gauge</span></div>\n'
Dj_dummy2 = None
Ot += '  </div>\n'
Ot += '  <div class="tool-note" id="ot-note"></div>\n'
Ot += '  <button type="button" class="tool-btn" id="ot-share">Share my tank math</button>\n'
Ot += '</div>\n'
Ot += '<script>(function(){\n'
Ot += "var S=document.getElementById('ot-s'),G=document.getElementById('ot-g'),B=document.getElementById('ot-b'),P=document.getElementById('ot-p');\n"
Ot += "function calc(){\n"
Ot += "  var size=parseFloat(S.value)||275,pct=Math.min(100,Math.max(0,parseFloat(G.value)||0)),burn=Math.max(0.5,parseFloat(B.value)||5),p=parseFloat(P.value)||3.5;\n"
Ot += "  var usable=size*pct/100*0.9, days=burn>0?usable/burn:0, missing=size*0.9-usable, cost=missing*p;\n"
Ot += "  var d1=Math.round(usable), d2=Math.round(cost), d3=Math.round(days);\n"
Ot += "  document.getElementById('ot-out').textContent=d3;\n"
Ot += "  document.getElementById('ot-s1').textContent=d1+' gal';\n"
Ot += "  document.getElementById('ot-s2').textContent='$'+d2;\n"
Ot += "  document.getElementById('ot-s3').textContent='about 33%';\n"
Ot += "  document.getElementById('ot-note').textContent='Two gauge truths: the tank never holds its rated number - a 275 gallon basement tank takes about 240 usable gallons because of the pickup line - and the gauge is a float, not an instrument, so read it as a hint. Order at one third, not on empty: winter delivery queues stretch, emergency fills carry surcharges, and a run-dry line needs a bleed before the burner restarts. Burn rate is the number worth knowing - track it across a cold week and you can predict your own tank better than the delivery company can.';\n"
Ot += "  document.title=days+' days of heating oil left - ToolDune';\n"
Ot += "}\n"
Ot += "function save(){try{localStorage.setItem('tt_oiltank',JSON.stringify({s:S.value,g:G.value,b:B.value,p:P.value}));}catch(e){}}\n"
Ot += "[S,G,B,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Ot += "var pre=false;\n"
Ot += "var qs=new URLSearchParams(location.search);\n"
Ot += "if(qs.get('g')){G.value=qs.get('g');pre=true;}\n"
Ot += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_oiltank')||'null');if(m){if(m.s){S.value=m.s;}if(m.g){G.value=m.g;}if(m.b){B.value=m.b;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Ot += "calc();\n"
Ot += "document.getElementById('ot-share').addEventListener('click',function(){\n"
Ot += "  var txt='My tank has '+document.getElementById('ot-out').textContent+' days of heat left. Run yours:';\n"
Ot += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value);\n"
Ot += "  if(navigator.share){navigator.share({title:'Heating oil tank',text:txt,url:url}).catch(function(){});}\n"
Ot += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my tank math';},1500);}\n"
Ot += "});\n"
Ot += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("MINPAY", "MEALPREP", "OILTANK"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Mp + Mpre + Ot + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "ptoopt": lambda args: PTOOPT,',
    '    "ptoopt": lambda args: PTOOPT,\n'
    '    "minpay": lambda args: MINPAY,\n'
    '    "mealprep": lambda args: MEALPREP,\n'
    '    "oiltank": lambda args: OILTANK,')
sub(BUILD_P, '    "slowcook": "🍲", "ptoopt": "📅",',
    '    "slowcook": "🍲", "ptoopt": "📅",\n'
    '    "minpay": "♾", "mealprep": "🍱", "oiltank": "⛽",')

P = []
d = {'slug': 'credit-card-minimum-payment-calculator',
     'title': 'Credit Card Minimum Payment Calculator - Years and Interest Revealed',
     'h1': 'Credit Card Minimum Payment Calculator',
     'desc': 'Balance and APR versus the minimum-payment math: years to repay, total interest, and what a fixed payment saves - the trap made visible. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'credit card minimum payment calculator how long to pay off',
     'tool': 'minpay',
     'args': {},
     'intro': ["Enter your balance, the APR from your statement, and what you could pay monthly instead. The calculator amortizes both paths: years and interest at minimum-only, versus months and interest at your fixed payment.",
              "The minimum is engineered, not helpful - at a 22 percent APR, interest eats most of a 2 percent minimum, so the balance barely moves for years. That is the business model working as designed, and the comparison line is the same card paid like a normal loan."],
     'howto': ["Balance and APR straight off the statement.",
               "Set the fixed payment you can genuinely sustain monthly.",
               "Compare the interest columns - then point the extra at the highest-APR card."],
     'faqs': [("How long does it take to pay off a credit card with minimum payments?",
               "At 2 percent minimums and a 22 percent APR, a 3,000 dollar balance runs for over a decade and costs thousands in interest - the early payments barely cover the monthly charge. The calculator runs your exact numbers."),
              ("Why is my minimum payment so low?",
               "Because a low minimum maximizes interest: the floor is engineered around the card profit model, not your payoff. Regulators now force issuers to print the warning on statements - the calculator makes it concrete."),
              ("What happens if I pay more than the minimum?",
               "Everything above the minimum hits principal directly, which compounds in your favor: the fixed-payment column shows months and interest collapsing at the same time. Even 20 extra dollars a month changes the curve visibly."),
              ("Is a balance transfer worth it?",
               "Often, yes: a 0 percent transfer with a 3 percent fee beats a year of 22 percent interest if you actually clear the balance inside the window. The fee is the whole cost - the trap is treating the new card as fresh spending room.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'meal-prep-batch-calculator',
     'title': 'Meal Prep Batch Calculator - Cost Per Meal vs Takeout',
     'h1': 'Meal Prep Batch Calculator',
     'desc': 'Batch portions and ingredient cost versus your real takeout price - savings per week, batches to cook, and the year figure. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'meal prep cost calculator batch cooking vs takeout',
     'tool': 'mealprep',
     'args': {},
     'intro': ["Enter meals to cover, portions per batch, what a batch of ingredients costs, and your real takeout price. The calculator gives cost per meal, weekly savings, batches to cook, and the year figure.",
              "The takeout number is the honest one - fee, tip and tax add roughly a third on top of the menu price. The honest counterweight is batch fatigue: freeze half the batch and run two recipes a week, because five identical dinners by Wednesday is how the habit dies."],
     'howto': ["Count the weekday meals you actually buy, not ideal ones.",
               "Price a batch from your last grocery receipt, not an aspirational one.",
               "Freeze half of every batch - variety is what makes prep stick."],
     'faqs': [("How much does meal prep save per week?",
               "At 3 dollars per batch meal against 14 dollar takeout, five weekday meals save about 55 dollars a week - over 2,600 a year on 48 working weeks. The calculator prices your real portions and your real takeout habit."),
              ("Is meal prep actually cheaper than cooking daily?",
               "Marginally cheaper on ingredients - the real win is time and the takeout it replaces. Bulk ingredients, one cook session and zero delivery fees beat both daily cooking and daily ordering."),
              ("How do I avoid getting bored of meal prep?",
               "Two recipes per week with the freezer as the variety engine: cook one batch, freeze half, pull a different cuisine next week. The fatigue is real and the rotation is the standard fix."),
              ("What do delivery fees really add?",
               "App fee, service fee, tip and tax typically add 30 percent or more over the menu price - the number on the checkout screen, not the menu, is the honest takeout figure for this comparison.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'heating-oil-tank-calculator',
     'title': 'Heating Oil Tank Calculator - Days Left, Refill Cost and Order Timing',
     'h1': 'Heating Oil Tank Calculator',
     'desc': 'Tank size, gauge reading and burn rate give usable gallons, days of heat left and the refill cost - with the order-at-one-third rule. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'heating oil tank gauge calculator how many days oil left',
     'tool': 'oiltank',
     'args': {},
     'intro': ["Pick your tank size, read the gauge, set your cold-week burn rate and the local price per gallon. The calculator gives usable gallons, days of heat left, the refill-to-full cost, and the gauge where you should order.",
              "Two gauge truths carry this page: the tank never holds its rated number - a 275 gallon basement tank delivers about 240 usable gallons - and the float gauge is a hint, not an instrument. Order at one third, because winter queues, emergency surcharges and a bleed-the-line restart are all more expensive than planning."],
     'howto': ["Tank size from the label; 275 is the standard basement unit.",
               "Read the gauge and be honest about your cold-week burn rate.",
               "Order at a third of a tank - the calculator shows why."],
     'faqs': [("How long will 100 gallons of heating oil last?",
               "At a typical winter burn of 5 gallons a day, about 20 days. The real rate varies with house size and cold snaps - tracking one cold week gives you a personal number better than any rule of thumb."),
              ("Why does my 275 gallon tank only take 240 gallons?",
               "The pickup line and the internal geometry reserve the bottom of the tank - roughly 90 percent of rated capacity is usable. The calculator applies the same factor to any size."),
              ("When should I order heating oil?",
               "At about one third of a tank. Winter delivery queues stretch to days, emergency or will-call fills carry surcharges, and running dry means a technician visit to bleed the line before the burner restarts."),
              ("Is heating oil cheaper in summer?",
               "Usually - summer and early-fall prices run lower and deliveries are slower-paced, so filling before the first cold snap beats panic-buying in January. The calculator prices the refill so you can time it.")]}
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
print("R162 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
