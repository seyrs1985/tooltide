# -*- coding: utf-8 -*-
"""R153 新年习惯三连:gym-membership-value(卡值不值)+dry-january-savings(戒酒账)+books-per-year(年阅读量)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: GYMVALUE ----------
Gv = 'GYMVALUE = """<div class="tool" id="tt-gv">\n'
Gv += '  <div class="fields">\n'
Gv += '    <div class="field"><label for="gv-m">Monthly fee</label><input id="gv-m" type="number" min="5" value="45"></div>\n'
Gv += '    <div class="field"><label for="gv-v">Visits per month, honest average</label><input id="gv-v" type="number" min="0" max="60" value="4"></div>\n'
Gv += '    <div class="field"><label for="gv-d">Drop-in price nearby</label><input id="gv-d" type="number" min="1" value="15"></div>\n'
Gv += '  </div>\n'
Gv += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gv-out">&#8211;</span><span class="result-unit">cost per visit</span></div>\n'
Gv += '  <div class="stats">\n'
Gv += '    <div class="stat"><b id="gv-s1">&#8211;</b><span>break-even visits a month</span></div>\n'
Gv += '    <div class="stat"><b id="gv-s2">&#8211;</b><span>year cost at your attendance</span></div>\n'
Gv += '    <div class="stat"><b id="gv-s3">&#8211;</b><span>verdict</span></div>\n'
Gv += '  </div>\n'
Gv += '  <div class="tool-note" id="gv-note"></div>\n'
Gv += '  <button type="button" class="tool-btn" id="gv-share">Share my gym math</button>\n'
Gv += '</div>\n'
Gv += '<script>(function(){\n'
Gv += "var M=document.getElementById('gv-m'),V=document.getElementById('gv-v'),D=document.getElementById('gv-d');\n"
Gv += "function calc(){\n"
Gv += "  var m=parseFloat(M.value)||0,v=Math.max(0,parseFloat(V.value)||0),d=parseFloat(D.value)||15;\n"
Gv += "  var per=v>0?m/v:m, be=d>0?m/d:0, year=m*12;\n"
Gv += "  var d1=Math.round(per*100)/100, d2=Math.round(be*10)/10, d3=Math.round(year);\n"
Gv += "  var verdict=v<=0?'Cancel or pause':(per<=d?'Keep it':(per<=d*2?'Borderline - go more or leave':'The treadmill is winning'));\n"
Gv += "  document.getElementById('gv-out').textContent='$'+d1;\n"
Gv += "  document.getElementById('gv-s1').textContent=d2;\n"
Gv += "  document.getElementById('gv-s2').textContent='$'+d3;\n"
Gv += "  document.getElementById('gv-s3').textContent=verdict;\n"
Gv += "  document.getElementById('gv-note').textContent='Gyms price memberships on no-shows - the business model is selling visits that never happen, which is why January is packed and mid-February is not. The honest numbers: your break-even is the monthly fee over the drop-in price, and anything under three visits a month usually loses to paying per visit. Two outs before cancelling: a cheaper plan tier, or a pause clause - most contracts have one and nobody asks. The calculator prices attendance, not aspirations; the best gym on earth is the one you actually walk into, and the second best is the one you stop paying for when you do not.';\n"
Gv += "  document.title='Gym: $'+d1+' per visit - ToolDune';\n"
Gv += "}\n"
Gv += "function save(){try{localStorage.setItem('tt_gymvalue',JSON.stringify({m:M.value,v:V.value,d:D.value}));}catch(e){}}\n"
Gv += "[M,V,D].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Gv += "var pre=false;\n"
Gv += "var qs=new URLSearchParams(location.search);\n"
Gv += "if(qs.get('v')){V.value=qs.get('v');pre=true;}\n"
Gv += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_gymvalue')||'null');if(m){if(m.m){M.value=m.m;}if(m.v){V.value=m.v;}if(m.d){D.value=m.d;}}}catch(e){}}\n"
Gv += "calc();\n"
Gv += "document.getElementById('gv-share').addEventListener('click',function(){\n"
Gv += "  var txt='My gym visits cost $'+document.getElementById('gv-out').textContent+' each - verdict: '+document.getElementById('gv-s3').textContent+'. Run yours:';\n"
Gv += "  var url=location.origin+location.pathname+'?v='+encodeURIComponent(V.value);\n"
Gv += "  if(navigator.share){navigator.share({title:'Gym membership value',text:txt,url:url}).catch(function(){});}\n"
Gv += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my gym math';},1500);}\n"
Gv += "});\n"
Gv += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: DRYJAN ----------
Dj = 'DRYJAN = """<div class="tool" id="tt-dj">\n'
Dj += '  <div class="fields">\n'
Dj += '    <div class="field"><label for="dj-w">Drinks per week, honest average</label><input id="dj-w" type="number" min="0" max="70" value="6"></div>\n'
Dj += '    <div class="field"><label for="dj-p">Typical price per drink</label><input id="dj-p" type="number" min="0.5" step="0.5" value="7"></div>\n'
Dj += '    <div class="field"><label for="dj-l">Length of the break</label><select id="dj-l"><option value="4" selected>One month - Dry January</option><option value="13">Three months</option><option value="52">A full year</option></select></div>\n'
Dj += '  </div>\n'
Dj += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dj-out">&#8211;</span><span class="result-unit">saved over the break</span></div>\n'
Dj += '  <div class="stats">\n'
Dj += '    <div class="stat"><b id="dj-s1">&#8211;</b><span>per week</span></div>\n'
Dj += '    <div class="stat"><b id="dj-s2">&#8211;</b><span>if kept a full year</span></div>\n'
Dj += '    <div class="stat"><b id="dj-s3">&#8211;</b><span>bar markup honesty</span></div>\n'
Dj += '  </div>\n'
Dj += '  <div class="tool-note" id="dj-note"></div>\n'
Dj += '  <button type="button" class="tool-btn" id="dj-share">Share my dry math</button>\n'
Dj += '</div>\n'
Dj += '<script>(function(){\n'
Dj += "var W=document.getElementById('dj-w'),P=document.getElementById('dj-p'),L=document.getElementById('dj-l');\n"
Dj += "function calc(){\n"
Dj += "  var w=Math.max(0,parseFloat(W.value)||0),p=parseFloat(P.value)||0,l=parseFloat(L.value)||4;\n"
Dj += "  var perWeek=w*p, saved=perWeek*l, year=perWeek*52;\n"
Dj += "  var d1=Math.round(saved*10)/10, d2=Math.round(perWeek*100)/100, d3=Math.round(year);\n"
Dj += "  document.getElementById('dj-out').textContent='$'+d1;\n"
Dj += "  document.getElementById('dj-s1').textContent='$'+d2;\n"
Dj += "  document.getElementById('dj-s2').textContent='$'+d3;\n"
Dj += "  document.getElementById('dj-s3').textContent='3-5x at bars';\n"
Dj += "  document.getElementById('dj-note').textContent='This counts money only - sleep, liver markers and mood are real but unpriced here, and they are the part people report noticing first. The math that motivates: bar drinks carry a three-to-five-times markup over the same bottle at home, so the savings figure assumes your honest average venue. The practical move is visibility - a jar or a labeled account where the not-spent money lands weekly turns an invisible non-purchase into a number that grows, which is the entire psychological trick behind every successful savings habit. February you can spend it on something loud.';\n"
Dj += "  document.title='Dry month saves $'+d1+' - ToolDune';\n"
Dj += "}\n"
Dj += "function save(){try{localStorage.setItem('tt_dryjan',JSON.stringify({w:W.value,p:P.value,l:L.value}));}catch(e){}}\n"
Dj += "[W,P,L].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Dj += "var pre=false;\n"
Dj += "var qs=new URLSearchParams(location.search);\n"
Dj += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Dj += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_dryjan')||'null');if(m){if(m.w){W.value=m.w;}if(m.p){P.value=m.p;}if(m.l){L.value=m.l;}}}catch(e){}}\n"
Dj += "calc();\n"
Dj += "document.getElementById('dj-share').addEventListener('click',function(){\n"
Dj += "  var txt='My dry month saves $'+document.getElementById('dj-out').textContent+' - $'+document.getElementById('dj-s2').textContent+' a week. Run yours:';\n"
Dj += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
Dj += "  if(navigator.share){navigator.share({title:'Dry January savings',text:txt,url:url}).catch(function(){});}\n"
Dj += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my dry math';},1500);}\n"
Dj += "});\n"
Dj += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: BOOKSYEAR ----------
By = 'BOOKSYEAR = """<div class="tool" id="tt-by">\n'
By += '  <div class="fields">\n'
By += '    <div class="field"><label for="by-p">Pages on an average day</label><input id="by-p" type="number" min="1" max="500" value="20"></div>\n'
By += '    <div class="field"><label for="by-l">Average book length (pages)</label><input id="by-l" type="number" min="50" max="1500" value="300"></div>\n'
By += '    <div class="field"><label for="by-s">Reading speed (wpm)</label><select id="by-s"><option value="150">150 - slow</option><option value="225" selected>225 - average</option><option value="300">300 - fast</option></select></div>\n'
By += '  </div>\n'
By += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="by-out">&#8211;</span><span class="result-unit">books a year</span></div>\n'
By += '  <div class="stats">\n'
By += '    <div class="stat"><b id="by-s1">&#8211;</b><span>days per book</span></div>\n'
By += '    <div class="stat"><b id="by-s2">&#8211;</b><span>minutes a day</span></div>\n'
By += '    <div class="stat"><b id="by-s3">&#8211;</b><span>hours a year</span></div>\n'
By += '  </div>\n'
By += '  <div class="tool-note" id="by-note"></div>\n'
By += '  <button type="button" class="tool-btn" id="by-share">Share my reading math</button>\n'
By += '</div>\n'
By += '<script>(function(){\n'
By += "var P=document.getElementById('by-p'),L=document.getElementById('by-l'),S=document.getElementById('by-s');\n"
By += "function calc(){\n"
By += "  var p=Math.max(1,parseFloat(P.value)||20),len=Math.max(50,parseFloat(L.value)||300),wpm=parseFloat(S.value)||225;\n"
By += "  var books=Math.floor(365*p/len), days=len/p, mins=p*300/wpm, hours=mins*365/60;\n"
By += "  var d1=Math.round(days*10)/10, d2=Math.round(mins), d3=Math.round(hours);\n"
By += "  document.getElementById('by-out').textContent=books;\n"
By += "  document.getElementById('by-s1').textContent=d1;\n"
By += "  document.getElementById('by-s2').textContent=d2;\n"
By += "  document.getElementById('by-s3').textContent=d3;\n"
By += "  document.getElementById('by-note').textContent='Twenty pages a day sounds small and lands around thirty books a year - the entire gap between wish-I-read-more and a reading life is a page count, not a resolution. The minutes figure is the reality check: 20 pages at average pace is about half an hour, which is one scrolled-in-bed session redirected. Two honest notes: audiobook minutes count - 225 wpm is also the standard narration pace, and the commute hour converts cleanly; and the book length field is where self-deception lives, because doorstop fantasy and essay collections do not cost the same pages. Set a pages number you can hit on your worst day, not your best.';\n"
By += "  document.title=books+' books a year at '+Math.round(p)+' pages/day - ToolDune';\n"
By += "}\n"
By += "function save(){try{localStorage.setItem('tt_booksyear',JSON.stringify({p:P.value,l:L.value,s:S.value}));}catch(e){}}\n"
By += "[P,L,S].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
By += "var pre=false;\n"
By += "var qs=new URLSearchParams(location.search);\n"
By += "if(qs.get('p')){P.value=qs.get('p');pre=true;}\n"
By += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_booksyear')||'null');if(m){if(m.p){P.value=m.p;}if(m.l){L.value=m.l;}if(m.s){S.value=m.s;}}}catch(e){}}\n"
By += "calc();\n"
By += "document.getElementById('by-share').addEventListener('click',function(){\n"
By += "  var txt='Reading '+P.value+' pages a day is '+document.getElementById('by-out').textContent+' books a year. Run yours:';\n"
By += "  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value);\n"
By += "  if(navigator.share){navigator.share({title:'Books per year',text:txt,url:url}).catch(function(){});}\n"
By += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my reading math';},1500);}\n"
By += "});\n"
By += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("GYMVALUE", "DRYJAN", "BOOKSYEAR"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Gv + Dj + By + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "sourdough": lambda args: SOURDOUGH,',
    '    "sourdough": lambda args: SOURDOUGH,\n'
    '    "gymvalue": lambda args: GYMVALUE,\n'
    '    "dryjan": lambda args: DRYJAN,\n'
    '    "booksyear": lambda args: BOOKSYEAR,')
sub(BUILD_P, '    "blanket": "🌙", "sourdough": "🍞",',
    '    "blanket": "🌙", "sourdough": "🍞",\n'
    '    "gymvalue": "💪", "dryjan": "🎉", "booksyear": "📚",')

P = []
d = {'slug': 'gym-membership-value-calculator',
     'title': 'Gym Membership Value Calculator - Cost Per Visit and Break-Even',
     'h1': 'Gym Membership Value Calculator',
     'desc': 'Monthly fee over your honest visit count gives the true cost per visit, the break-even against drop-in pricing, and a plain verdict. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'gym membership worth it calculator cost per visit',
     'tool': 'gymvalue',
     'args': {},
     'intro': ["Enter your monthly fee, the visits you actually made - last month, not January - and the drop-in price at a nearby gym. The calculator gives your true cost per visit, the monthly break-even, and a verdict from keep to cancel.",
              "Gyms price memberships on no-shows; the business model is selling visits that never happen, which is why January is packed and mid-February is not. This one prices your attendance instead of your aspirations - and points at the pause clause most contracts hide before it points at cancellation."],
     'howto': ["Fee first, then the honest visit count from your check-in history.",
               "Find the drop-in rate of any comparable gym nearby.",
               "Read the verdict as attendance pricing, not a character judgment."],
     'faqs': [("How many gym visits per month make membership worth it?",
               "Divide the fee by the drop-in price: at 45 a month against 15 dollar visits, three visits a month is break-even. Below that, paying per visit wins; above it, the membership earns its keep."),
              ("Why do gyms sell so many memberships?",
               "Because most members stop coming - the model is built on no-shows, with capacity priced for the February crowd, not the January one. Knowing this reframes the contract: you are paying for the option to attend, and options price lower than usage."),
              ("Can I pause my gym membership instead of cancelling?",
               "Most contracts have a pause or freeze clause, often 1-3 months for a small fee - it exists because members who pause return, and cancelled ones rarely do. Ask before cancelling; the calculator verdict borderline usually resolves with a pause."),
              ("What is a fair price per gym visit?",
               "Drop-in rates run 10-25 dollars in most cities. If your membership cost per visit sits under that, you are winning; if it sits over double, the treadmill has been quietly winning for months.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'dry-january-savings-calculator',
     'title': 'Dry January Savings Calculator - What the Break Actually Saves',
     'h1': 'Dry January Savings Calculator',
     'desc': 'Your honest weekly drink count times venue price gives the month, quarter or full-year savings - with the visibility trick that makes it stick. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'dry january savings calculator how much money save not drinking',
     'tool': 'dryjan',
     'args': {},
     'intro': ["Enter the drinks you actually have in a week, what they typically cost, and how long the break runs - one month, a quarter, or a year. The calculator totals the savings and projects what a year of the same habit change is worth.",
              "The math here counts money only; sleep, liver markers and mood are real but unpriced. What the calculator adds is the psychological trick behind every successful savings habit: put the not-spent money somewhere visible weekly, because an invisible non-purchase is a number nobody celebrates."],
     'howto': ["Count an honest average week - holidays and all.",
               "Price it at your real venue, not the bottle shop.",
               "Give the savings a landing place - a jar beats a vague intention."],
     'faqs': [("How much money does Dry January save?",
               "Six drinks a week at bar prices is about 42 dollars a week - 168 over the month, over 2,000 if the habit change holds a year. Home pours save a third of that; the calculator prices your real venue mix."),
              ("Why are bar drinks so expensive?",
               "Markup on alcohol at bars and restaurants runs three to five times retail - you are paying for the seat, the glassware and the evening. The calculator assumes your honest average, which is where most people underestimate."),
              ("Does the savings math include health benefits?",
               "No - this counts cash only. Better sleep and the rest are real but vary person to person; the money is the part that lands weekly and the part a jar makes visible."),
              ("What is the best way to actually keep the savings?",
               "Give them a landing place at the moment of decision: transfer the not-spent amount weekly to a labeled account or a jar. The number that grows in public is the reason Dry January accounts stay open past week two.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'books-per-year-calculator',
     'title': 'Books Per Year Calculator - What Your Daily Pages Add Up To',
     'h1': 'Books Per Year Calculator',
     'desc': 'Daily pages, average book length and reading speed give your books-per-year total, days per book, and the minutes-a-day reality check. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'books per year calculator how many books reading 20 pages a day',
     'tool': 'booksyear',
     'args': {},
     'intro': ["Enter the pages you read on an average day, the length of your typical book, and your pace. The calculator gives books per year, how long one book takes, and the minutes-a-day figure that is the whole habit in miniature.",
              "Twenty pages a day sounds small and lands around thirty books a year - the entire gap between wishing you read more and a reading life is a page count, not a resolution. The calculator also holds the two honest notes: audiobook minutes count at standard narration pace, and the book-length field is where self-deception lives."],
     'howto': ["Set a pages number you can hit on your worst day, not your best.",
               "Use the average length of the books actually on your shelf.",
               "225 wpm is also audiobook narration pace - commutes count."],
     'faqs': [("How many books can I read in a year?",
               "Twenty pages a day compounds to about 24 books of average length - 30 if your books run 250 pages. Ten pages a day still lands around 12, which is more than most people finish. The calculator prices your exact habit."),
              ("How long does it take to read 300 pages?",
               "At 20 pages a day, fifteen days; at 40, a week. In hours: roughly 6-7 at average pace. The days-per-book figure is the one that turns a shelf into a schedule."),
              ("Do audiobooks count as reading?",
               "For the math, yes - 225 wpm is also standard audiobook narration pace, so the minutes convert one to one. The habit argument is yours to have; the calculator counts the time honestly either way."),
              ("How do I read more books without rushing?",
               "Set a pages number sized for your worst day, keep the book visible, and stop counting minutes of scrolling as reading-adjacent. The compounding does the rest - that is literally what this calculator shows.")]}
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
print("R153 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
