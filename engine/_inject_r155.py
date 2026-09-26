# -*- coding: utf-8 -*-
"""R155 冬末节日三连:dehumidifier-size(除湿选型)+secret-santa(礼物交换池)+champagne(气泡酒瓶数)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: DEHUMID ----------
Dh = 'DEHUMID = """<div class="tool" id="tt-dhm">\n'
Dh += '  <div class="fields">\n'
Dh += '    <div class="field"><label for="dh2-a">Room area (sq ft)</label><input id="dh2-a" type="number" min="50" max="3000" value="400"></div>\n'
Dh += '    <div class="field"><label for="dh2-c">How damp is it</label><select id="dh2-c"><option value="8">Slightly damp - musty smell</option><option value="12" selected>Damp - condensation on windows</option><option value="16">Very damp - mold spots</option></select></div>\n'
Dj_dummy = None
Dh += '  </div>\n'
Dh += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dh2-out">&#8211;</span><span class="result-unit">pints per day rating</span></div>\n'
Dh += '  <div class="stats">\n'
Dh += '    <div class="stat"><b id="dh2-s1">&#8211;</b><span>running watts, typical</span></div>\n'
Dh += '    <div class="stat"><b id="dh2-s2">&#8211;</b><span>cost per month at 10 h/day</span></div>\n'
Dh += '    <div class="stat"><b id="dh2-s3">&#8211;</b><span>target humidity</span></div>\n'
Dh += '  </div>\n'
Dh += '  <div class="tool-note" id="dh2-note"></div>\n'
Dh += '  <button type="button" class="tool-btn" id="dh2-share">Share my dehumidifier size</button>\n'
Dh += '</div>\n'
Dh += '<script>(function(){\n'
Dh += "var A=document.getElementById('dh2-a'),C=document.getElementById('dh2-c');\n"
Dh += "function calc(){\n"
Dh += "  var a=parseFloat(A.value)||400,f=parseFloat(C.value)||12;\n"
Dh += "  var pints=Math.ceil(a/500*f), watts=Math.round(pints*10), month=watts*10*30/1000*0.17;\n"
Dh += "  var d1=Math.round(month*100)/100;\n"
Dh += "  document.getElementById('dh2-out').textContent=pints;\n"
Dh += "  document.getElementById('dh2-s1').textContent=watts+' W';\n"
Dh += "  document.getElementById('dh2-s2').textContent='$'+d1;\n"
Dh += "  document.getElementById('dh2-s3').textContent='40-50% RH';\n"
Dh += "  document.getElementById('dh2-note').textContent='Winter condensation on the windows is the classic sign: warm indoor air hits cold glass and dumps its water. The dehumidifier rating on the box assumes a damp 500-square-foot room at 80 F - scale by area and dampness, and buy one size up if the room is a basement, which sits below the water table and fights its own physics. The target is 40 to 50 percent relative humidity: lower dries your sinuses, higher feeds the mold. And place it with airflow around it - a unit pushed into a corner dehumidifies the corner.';\n"
Dh += "  document.title='Dehumidifier: '+pints+' pints/day for '+Math.round(a)+' sq ft - ToolDune';\n"
Dh += "}\n"
Dh += "function save(){try{localStorage.setItem('tt_dehumid',JSON.stringify({a:A.value,c:C.value}));}catch(e){}}\n"
Dh += "[A,C].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Dh += "var pre=false;\n"
Dh += "var qs=new URLSearchParams(location.search);\n"
Dh += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Dh += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_dehumid')||'null');if(m){if(m.a){A.value=m.a;}if(m.c){C.value=m.c;}}}catch(e){}}\n"
Dh += "calc();\n"
Dh += "document.getElementById('dh2-share').addEventListener('click',function(){\n"
Dh += "  var txt='My room needs a '+document.getElementById('dh2-out').textContent+' pint dehumidifier. Size yours:';\n"
Dh += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Dh += "  if(navigator.share){navigator.share({title:'Dehumidifier sizing',text:txt,url:url}).catch(function(){});}\n"
Dh += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my dehumidifier size';},1500);}\n"
Dh += "});\n"
Dh += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: SANTAMATH ----------
Ss = 'SANTAMATH = """<div class="tool" id="tt-ss">\n'
Ss += '  <div class="fields">\n'
Ss += '    <div class="field"><label for="ss2-n">People in the draw</label><input id="ss2-n" type="number" min="3" max="100" value="8"></div>\n'
Ss += '    <div class="field"><label for="ss2-b">Budget cap per gift</label><input id="ss2-b" type="number" min="1" value="25"></div>\n'
Ss += '  </div>\n'
Ss += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ss2-out">&#8211;</span><span class="result-unit">gifts in the exchange</span></div>\n'
Ss += '  <div class="stats">\n'
Ss += '    <div class="stat"><b id="ss2-s1">&#8211;</b><span>total spend, whole group</span></div>\n'
Ss += '    <div class="stat"><b id="ss2-s2">&#8211;</b><span>vs everyone buying for all</span></div>\n'
Ss += '    <div class="stat"><b id="ss2-s3">&#8211;</b><span>saved per person</span></div>\n'
Ss += '  </div>\n'
Ss += '  <div class="tool-note" id="ss2-note"></div>\n'
Ss += '  <button type="button" class="tool-btn" id="ss2-share">Share my draw math</button>\n'
Ss += '</div>\n'
Ss += '<script>(function(){\n'
Ss += "var N=document.getElementById('ss2-n'),B=document.getElementById('ss2-b');\n"
Ss += "function calc(){\n"
Ss += "  var n=Math.max(3,Math.round(parseFloat(N.value)||8)),b=Math.max(1,parseFloat(B.value)||25);\n"
Ss += "  var gifts=n, full=n*(n-1)*b, saved=(n-1-1)*b;\n"
Ss += "  var d1=Math.round(full), d2=Math.round(saved);\n"
Ss += "  document.getElementById('ss2-out').textContent=gifts;\n"
Ss += "  document.getElementById('ss2-s1').textContent='$'+d1;\n"
Ss += "  document.getElementById('ss2-s2').textContent='$'+d1+' vs $'+Math.round(n*(n-1)*b);\n"
Ss += "  document.getElementById('ss2-s3').textContent='$'+d2;\n"
Ss += "  document.getElementById('ss2-note').textContent='The draw has exactly three rules that matter: nobody draws themselves, agreed couples or plus-ones can be excluded as a pair, and the cap is a contract - the person who spends 60 on a 25 gift is not generous, they are breaking the game for whoever receives and cannot match it. Paper names in a hat beats every app for the aunts, and wishlists are the actual luxury: one link per person turns a guessing game into a good gift. The savings line is the honest pitch to the family skeptic - same number of gifts received, a fraction of the shopping, and considerably fewer polite smiles.';\n"
Ss += "  document.title='Secret Santa: '+gifts+' gifts at $'+Math.round(b)+' cap - ToolDune';\n"
Ss += "}\n"
Ss += "function save(){try{localStorage.setItem('tt_santamath',JSON.stringify({n:N.value,b:B.value}));}catch(e){}}\n"
Ss += "[N,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Ss += "var pre=false;\n"
Ss += "var qs=new URLSearchParams(location.search);\n"
Ss += "if(qs.get('n')){N.value=qs.get('n');pre=true;}\n"
Ss += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_santamath')||'null');if(m){if(m.n){N.value=m.n;}if(m.b){B.value=m.b;}}}catch(e){}}\n"
Ss += "calc();\n"
Ss += "document.getElementById('ss2-share').addEventListener('click',function(){\n"
Ss += "  var txt='Our Secret Santa: '+N.value+' people, $'+B.value+' cap, everyone gives and receives exactly once. Plan yours:';\n"
Ss += "  var url=location.origin+location.pathname+'?n='+encodeURIComponent(N.value);\n"
Ss += "  if(navigator.share){navigator.share({title:'Secret Santa math',text:txt,url:url}).catch(function(){});}\n"
Ss += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my draw math';},1500);}\n"
Ss += "});\n"
Ss += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: CHAMP ----------
Cp = 'CHAMP = """<div class="tool" id="tt-cp">\n'
Cp += '  <div class="fields">\n'
Cp += '    <div class="field"><label for="cp-g">Guests</label><input id="cp-g" type="number" min="2" max="200" value="10"></div>\n'
Cp += '    <div class="field"><label for="cp-g2">Glasses each through the evening</label><select id="cp-g2"><option value="1">1 - toast only</option><option value="2">2 - toast and top-up</option><option value="3" selected>3 - a proper evening</option></select></div>\n'
Cp += '    <div class="field"><label for="cp-p">Price per bottle</label><input id="cp-p" type="number" min="5" value="15"></div>\n'
Cp += '  </div>\n'
Cp += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cp-out">&#8211;</span><span class="result-unit">bottles to chill</span></div>\n'
Cp += '  <div class="stats">\n'
Cp += '    <div class="stat"><b id="cp-s1">&#8211;</b><span>total glasses</span></div>\n'
Cp += '    <div class="stat"><b id="cp-s2">&#8211;</b><span>total cost</span></div>\n'
Cp += '    <div class="stat"><b id="cp-s3">&#8211;</b><span>mimosa mix, if brunch</span></div>\n'
Cp += '  </div>\n'
Cp += '  <div class="tool-note" id="cp-note"></div>\n'
Cp += '  <button type="button" class="tool-btn" id="cp-share">Share my bottle math</button>\n'
Cp += '</div>\n'
Cp += '<script>(function(){\n'
Cp += "var G=document.getElementById('cp-g'),G2=document.getElementById('cp-g2'),P=document.getElementById('cp-p');\n"
Cp += "function calc(){\n"
Cp += "  var g=Math.max(2,Math.round(parseFloat(G.value)||10)),ge=parseFloat(G2.value)||3,p=parseFloat(P.value)||15;\n"
Cp += "  var glasses=g*ge, bottles=Math.ceil(glasses/6), cost=bottles*p;\n"
Cp += "  var d1=Math.round(cost*100)/100, oj=Math.round(glasses*125*2/1000*10)/10;\n"
Cp += "  document.getElementById('cp-out').textContent=bottles;\n"
Cp += "  document.getElementById('cp-s1').textContent=glasses;\n"
Cp += "  document.getElementById('cp-s2').textContent='$'+d1;\n"
Cp += "  document.getElementById('cp-s3').textContent=oj+' L of juice';\n"
Cp += "  document.getElementById('cp-note').textContent='A 750 ml bottle pours six honest 125 ml glasses - the math most hosts get wrong by being generous early and empty by ten. The honest label talk: blind tastings keep finding that mid-shelf cava and cremant beat famous-name champagne at three times the price, and for mimosas nobody can tell anything at all - the juice is louder than the bubbles. Chill bottles for at least three hours, open pointing at nobody, and the leftover bottles keep their fizz for a day with a spoon-handle stopper and a prayer.';\n"
Cp += "  document.title='Bubbles: '+bottles+' bottles for '+g+' guests - ToolDune';\n"
Cp += "}\n"
Cp += "function save(){try{localStorage.setItem('tt_champagne',JSON.stringify({g:G.value,g2:G2.value,p:P.value}));}catch(e){}}\n"
Cp += "[G,G2,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Cp += "var pre=false;\n"
Cp += "var qs=new URLSearchParams(location.search);\n"
Cp += "if(qs.get('g')){G.value=qs.get('g');pre=true;}\n"
Cp += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_champagne')||'null');if(m){if(m.g){G.value=m.g;}if(m.g2){G2.value=m.g2;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Cp += "calc();\n"
Cp += "document.getElementById('cp-share').addEventListener('click',function(){\n"
Cp += "  var txt='For '+G.value+' guests I need '+document.getElementById('cp-out').textContent+' bottles of bubbles. Run your party:';\n"
Cp += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value);\n"
Cp += "  if(navigator.share){navigator.share({title:'Bottle math',text:txt,url:url}).catch(function(){});}\n"
Cp += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my bottle math';},1500);}\n"
Cp += "});\n"
Cp += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("DEHUMID", "SANTAMATH", "CHAMP"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Dh + Ss + Cp + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "booksyear": lambda args: BOOKSYEAR,',
    '    "booksyear": lambda args: BOOKSYEAR,\n'
    '    "dehumid": lambda args: DEHUMID,\n'
    '    "santamath": lambda args: SANTAMATH,\n'
    '    "champagne": lambda args: CHAMP,')
sub(BUILD_P, '    "gymvalue": "💪", "dryjan": "🎉", "booksyear": "📚",',
    '    "gymvalue": "💪", "dryjan": "🎉", "booksyear": "📚",\n'
    '    "dehumid": "💨", "santamath": "🎅", "champagne": "🍷",')

P = []
d = {'slug': 'dehumidifier-size-calculator',
     'title': 'Dehumidifier Size Calculator - Pints Per Day for Your Room',
     'h1': 'Dehumidifier Size Calculator',
     'desc': 'Room area and dampness level give the pints-per-day rating to shop for, the running watts and the monthly cost - with the 40-50 percent target. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'dehumidifier size calculator what size dehumidifier for room',
     'tool': 'dehumid',
     'args': {},
     'intro': ["Enter the room area and how damp it honestly is - musty smell, window condensation, or mold spots. The calculator gives the pints-per-day rating to buy, the running watts, and what ten hours a night costs on your bill.",
              "The rating on the box assumes a specific lab room, and basements cheat. This one scales by area and dampness, points at the 40-50 percent humidity target where mold stops and sinuses survive, and explains the window-condensation signal that winter sends every morning."],
     'howto': ["Measure the room, not the floor plan - the machine dehumidifies one space.",
               "Rate the dampness honestly; mold spots mean the top bracket.",
               "Basements and bathrooms take one size up from the number."],
     'faqs': [("What size dehumidifier do I need for my room?",
               "Industry ratings run about 8 pints per day for slightly damp 500 square feet, up to 16 for very damp. The calculator scales to your area and dampness - and basements deserve the next size up."),
              ("What humidity should I set my dehumidifier to?",
               "40 to 50 percent relative humidity. Above 50 the mold and dust mites feed; below 40, wood cracks and throats complain. A unit with a humidistat stops at the target instead of running forever."),
              ("Why is my bedroom window wet in the morning?",
               "Warm indoor air holds moisture that condenses on the cold glass overnight - breathing, drying clothes and cooking all feed it. Ventilation helps at the source; a dehumidifier closes the gap in the dampest room."),
              ("Do dehumidifiers use a lot of electricity?",
               "A typical room unit draws 200-400 watts - about the same as the fridge it sits next to. Run ten hours a night and the calculator prices it; the humidistat keeps the real bill lower by coasting at the target.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'secret-santa-calculator',
     'title': 'Secret Santa Calculator - Gift Pool, Budget Cap and Group Savings',
     'h1': 'Secret Santa Calculator',
     'desc': 'Participants and budget cap give the number of gifts, the whole-group spend, and what everyone saves versus buying for all - plus the three draw rules. Free.',
     'category': 'calculator',
     'keyword': 'secret santa calculator gift exchange budget per person',
     'tool': 'santamath',
     'args': {},
     'intro': ["Enter how many people are in the draw and the budget cap. The calculator shows the gifts in play, the whole-group spend, and what each person saves against buying something for everyone.",
              "The draw has three rules that matter - nobody draws themselves, couples can be excluded as pairs, and the cap is a contract. This page prices the savings for the family skeptic, and makes the case that paper names in a hat beat every app for the aunts."],
     'howto': ["Count the participants, including the ones who claim they want nothing.",
               "Set a cap everyone can afford - the cap is the whole game.",
               "Wishlists are the luxury move: one link per person beats guessing."],
     'faqs': [("How does a Secret Santa draw work?",
               "Everyone draws one name and buys only for that person, within the agreed cap - so everyone gives once and receives once. The calculator shows the group math: eight people at a 25 dollar cap exchange eight gifts instead of fifty-six."),
              ("What is a good Secret Santa budget?",
               "Whatever the poorest member can do without thinking - typically 15-30 dollars. The cap is a contract, not a suggestion: the person who overspends breaks the game for whoever cannot match it."),
              ("How do I make sure nobody draws themselves?",
               "Paper names in a hat, redraw on self-draw, works fine to about twenty people - and beats every app for family groups. For bigger crowds or remote relatives, free online draw tools handle exclusions automatically."),
              ("Can couples be excluded from drawing each other?",
               "Yes - exclude pairs as a block and redraw; the math barely changes and the household harmony doubles. Most families run exactly this rule and consider it obvious.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'champagne-calculator',
     'title': 'Champagne Calculator - Bottles Needed for Your Party',
     'h1': 'Champagne Calculator',
     'desc': 'Guests and glasses per head give the bottles to chill, the total cost, and the mimosa juice ratio - six honest pours per bottle. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'how many bottles of champagne for 10 guests calculator party',
     'tool': 'champagne',
     'args': {},
     'intro': ["Enter the guest count, how many glasses each will actually have through the evening, and your bottle price. The calculator gives bottles to chill, the total cost, and the juice ratio if brunch turns it into mimosas.",
              "The math most hosts get wrong is generosity before ten: a 750 ml bottle pours six honest 125 ml glasses, and running dry at the toast is a bigger social cost than one leftover bottle. The label talk is honest too - blind tastings keep finding mid-shelf cava beats famous champagne at three times the price."],
     'howto': ["Count guests, then choose toast-only versus a proper evening.",
               "Six glasses per bottle is the honest pour, not the optimistic one.",
               "Chill for at least three hours; warm bubbles foam over half the glass."],
     'faqs': [("How many bottles of champagne for 10 guests?",
               "For a proper evening of three glasses each, that is 30 glasses - five bottles at six pours per 750 ml. A toast-only night needs two. The calculator scales to your crowd and your pour honestly."),
              ("How many glasses are in a bottle of champagne?",
               "Six 125 ml pours from a 750 ml bottle - seven if you pour conservatively. Party math that assumes eight is why so many toasts run out before midnight."),
              ("Is expensive champagne worth it for a party?",
               "For toasts and mimosas, no - blind tastings repeatedly rank mid-shelf cava and cremant above big-name bottles at triple the price. Spend on the bottle you hand someone who loves wine; pour the honest stuff for the crowd."),
              ("How much orange juice for mimosas?",
               "The classic mix is two parts juice to one part bubbles, so each bottle of bubbles wants about a liter of juice - the calculator totals it for your glass count. Fresh-squeezed is the only upgrade anyone actually notices.")]}
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
print("R155 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
