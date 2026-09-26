# -*- coding: utf-8 -*-
"""R125 尾随派对簇:cooler-ice-calculator(冰量/箱容量) + tailgate-food-calculator(食物量)
规则:JS 禁反斜杠u转义(R120)、三引号模板零撇号零反斜杠(R121)、emoji 老码位(U6.0)
"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

C = 'COOLICE = """<div class="tool" id="tt-ci">\n'
C += '  <div class="fields">\n'
C += '    <div class="field"><label for="ci-g">Guests</label><input type="number" id="ci-g" min="1" max="200" step="1" placeholder="8"></div>\n'
C += '    <div class="field"><label for="ci-h">Hours on ice</label><input type="number" id="ci-h" min="1" max="24" step="0.5" placeholder="4"></div>\n'
C += '    <div class="field"><label for="ci-w">Weather</label><select id="ci-w"><option value="cool" selected>Under 21 C - mild</option><option value="warm">21 to 29 C - warm</option><option value="hot">Over 29 C - hot</option></select></div>\n'
C += '    <div class="field"><label for="ci-f">Packing food too</label><select id="ci-f"><option value="no" selected>Drinks only</option><option value="yes">Drinks plus food</option></select></div>\n'
C += '  </div>\n'
C += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ci-out">&#8211;</span><span class="result-unit">of ice</span></div>\n'
C += '  <div class="stats">\n'
C += '    <div class="stat"><b id="ci-s1">&#8211;</b><span>10 lb bags to buy</span></div>\n'
C += '    <div class="stat"><b id="ci-s2">&#8211;</b><span>cooler size</span></div>\n'
C += '    <div class="stat"><b id="ci-s3">&#8211;</b><span>of it as blocks</span></div>\n'
C += '  </div>\n'
C += '  <div class="tool-note" id="ci-note"></div>\n'
C += '  <button type="button" class="tool-btn" id="ci-share">Share my ice plan</button>\n'
C += '</div>\n'
C += '<script>(function(){\n'
C += "var G=document.getElementById('ci-g'),H=document.getElementById('ci-h'),W=document.getElementById('ci-w'),F=document.getElementById('ci-f');\n"
C += "function calc(){\n"
C += "  var g=parseFloat(G.value)||0,h=parseFloat(H.value)||0;\n"
C += "  if(g<1){g=1;}if(h<1){h=1;}\n"
C += "  var w=W.value,f=F.value==='yes';\n"
C += "  var wm=(w==='hot')?1.3:((w==='warm')?1.15:1);\n"
C += "  var lb=g*(h/4)*wm;\n"
C += "  if(f){lb*=1.5;}\n"
C += "  lb=Math.ceil(lb/5)*5;\n"
C += "  var qt=Math.min(150,Math.max(5,Math.ceil(lb*2/5)*5));\n"
C += "  document.getElementById('ci-out').textContent=lb+' lb';\n"
C += "  document.getElementById('ci-s1').textContent=Math.ceil(lb/10);\n"
C += "  document.getElementById('ci-s2').textContent=qt+' qt';\n"
C += "  document.getElementById('ci-s3').textContent=Math.ceil(lb/2)+' lb';\n"
C += "  document.getElementById('ci-note').textContent='The arithmetic: one pound of ice per guest per four hours keeps drinks cold, and packing food adds half again at a two-to-one ice-to-food ratio. Days over 29 C melt a quarter more. Pre-chill the box with ice water for 30 minutes before packing and the same ice lasts hours longer; blocks melt slower than cubes, so frozen water bottles are free block ice that becomes drinking water. Party-store bags run 7 to 10 pounds - round your buy up, never down, because warm drinks end tailgates early.';\n"
C += "  document.title=lb+' lb of ice - ToolDune';\n"
C += "}\n"
C += "function save(){try{localStorage.setItem('tt_coolice',JSON.stringify({g:G.value,h:H.value,w:W.value,f:F.value}));}catch(e){}}\n"
C += "G.addEventListener('input',function(){calc();save();});H.addEventListener('input',function(){calc();save();});\n"
C += "W.addEventListener('change',function(){calc();save();});F.addEventListener('change',function(){calc();save();});\n"
C += "var pre=false;\n"
C += "var qs=new URLSearchParams(location.search);\n"
C += "if(qs.get('g')){G.value=qs.get('g');pre=true;}\n"
C += "if(qs.get('h')){H.value=qs.get('h');pre=true;}\n"
C += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
C += "if(qs.get('f')){F.value=qs.get('f');pre=true;}\n"
C += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_coolice')||'null');if(m){if(m.g){G.value=m.g;}if(m.h){H.value=m.h;}if(m.w){W.value=m.w;}if(m.f){F.value=m.f;}pre=true;}}catch(e){}}\n"
C += "calc();\n"
C += "document.getElementById('ci-share').addEventListener('click',function(){\n"
C += "  var txt='We need '+document.getElementById('ci-out').textContent+' of ice and a '+document.getElementById('ci-s2').textContent+' cooler for the tailgate. Plan yours:';\n"
C += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value)+'&h='+encodeURIComponent(H.value)+'&w='+encodeURIComponent(W.value)+'&f='+encodeURIComponent(F.value);\n"
C += "  if(navigator.share){navigator.share({title:'Cooler ice plan',text:txt,url:url}).catch(function(){});}\n"
C += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my ice plan';},1500);}\n"
C += "});\n"
C += "})();\n</script>\n\"\"\"\n\n"

T = 'TGFOOD = """<div class="tool" id="tt-tf">\n'
T += '  <div class="fields">\n'
T += '    <div class="field"><label for="tf-a">Adults</label><input type="number" id="tf-a" min="1" max="100" step="1" placeholder="6"></div>\n'
T += '    <div class="field"><label for="tf-k">Kids</label><input type="number" id="tf-k" min="0" max="50" step="1" placeholder="2"></div>\n'
T += '    <div class="field"><label for="tf-m">Meal style</label><select id="tf-m"><option value="snack">Snacks only</option><option value="meal" selected>Full meal</option><option value="seconds">Full meal plus seconds</option></select></div>\n'
T += '    <div class="field"><label for="tf-h">Hours out</label><input type="number" id="tf-h" min="1" max="12" step="1" placeholder="3"></div>\n'
T += '  </div>\n'
T += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tf-out">&#8211;</span><span class="result-unit">of raw meat</span></div>\n'
T += '  <div class="stats">\n'
T += '    <div class="stat"><b id="tf-s1">&#8211;</b><span>cups of sides</span></div>\n'
T += '    <div class="stat"><b id="tf-s2">&#8211;</b><span>cans of drinks</span></div>\n'
T += '    <div class="stat"><b id="tf-s3">&#8211;</b><span>people fed</span></div>\n'
T += '  </div>\n'
T += '  <div class="tool-note" id="tf-note"></div>\n'
T += '  <button type="button" class="tool-btn" id="tf-share">Share my shopping list</button>\n'
T += '</div>\n'
T += '<script>(function(){\n'
T += "var A=document.getElementById('tf-a'),K=document.getElementById('tf-k'),M=document.getElementById('tf-m'),H=document.getElementById('tf-h');\n"
T += "function calc(){\n"
T += "  var a=parseFloat(A.value)||0,k=parseFloat(K.value)||0,h=parseFloat(H.value)||1;\n"
T += "  if(a<1){a=1;}if(k<0){k=0;}if(h<1){h=1;}\n"
T += "  var mf=(M.value==='snack')?0.5:((M.value==='seconds')?1.25:1);\n"
T += "  var meat=(a*0.5+k*0.25)*mf;\n"
T += "  meat=Math.ceil(meat*2)/2;\n"
T += "  var cups=Math.ceil((a+k)*0.5*2);\n"
T += "  var canRaw=a*(h+1)+k*(h+1)*0.5;\n"
T += "  cans=Math.ceil(canRaw/6)*6;\n"
T += "  document.getElementById('tf-out').textContent=meat+' lb';\n"
T += "  document.getElementById('tf-s1').textContent=cups;\n"
T += "  document.getElementById('tf-s2').textContent=cans;\n"
T += "  document.getElementById('tf-s3').textContent=Math.round(a+k);\n"
T += "  document.getElementById('tf-note').textContent='The arithmetic: half a pound of raw meat per adult and a quarter per child, scaled for snack-only or second-helping crowds; bone-in cuts need a third more weight. Sides run half a cup per person each and you want two of them, which is the cups shown. Drinks follow the first-hour rule - two per person in hour one, one each hour after, kids at half rate on juice and water. This list is the food; the cooler calculator sizes the ice and the BBQ charcoal page sizes the fuel.';\n"
T += "  document.title=meat+' lb of meat for '+Math.round(a+k)+' guests - ToolDune';\n"
T += "}\n"
T += "function save(){try{localStorage.setItem('tt_tgfood',JSON.stringify({a:A.value,k:K.value,m:M.value,h:H.value}));}catch(e){}}\n"
T += "A.addEventListener('input',function(){calc();save();});K.addEventListener('input',function(){calc();save();});\n"
T += "M.addEventListener('change',function(){calc();save();});H.addEventListener('input',function(){calc();save();});\n"
T += "var pre=false;\n"
T += "var qs=new URLSearchParams(location.search);\n"
T += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
T += "if(qs.get('k')){K.value=qs.get('k');pre=true;}\n"
T += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
T += "if(qs.get('h')){H.value=qs.get('h');pre=true;}\n"
T += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_tgfood')||'null');if(m){if(m.a){A.value=m.a;}if(m.k){K.value=m.k;}if(m.m){M.value=m.m;}if(m.h){H.value=m.h;}pre=true;}}catch(e){}}\n"
T += "calc();\n"
T += "document.getElementById('tf-share').addEventListener('click',function(){\n"
T += "  var txt='Shopping list for the tailgate: '+document.getElementById('tf-out').textContent+' of meat, '+document.getElementById('tf-s1').textContent+' cups of sides, '+document.getElementById('tf-s2').textContent+' drinks. Build yours:';\n"
T += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value)+'&k='+encodeURIComponent(K.value)+'&m='+encodeURIComponent(M.value)+'&h='+encodeURIComponent(H.value);\n"
T += "  if(navigator.share){navigator.share({title:'Tailgate shopping list',text:txt,url:url}).catch(function(){});}\n"
T += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my shopping list';},1500);}\n"
T += "});\n"
T += "})();\n</script>\n\"\"\"\n\n"

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

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', C + T + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "dstsleep": lambda args: DSTPLAN,',
    '    "dstsleep": lambda args: DSTPLAN,\n'
    '    "coolice": lambda args: COOLICE,\n'
    '    "tailgatefood": lambda args: TGFOOD,')
sub(BUILD_P, '    "dstsleep": "\u23f0",',
    '    "dstsleep": "\u23f0",\n'
    '    "coolice": "\U0001F379", "tailgatefood": "\U0001F356",')

P = []
d1 = {'slug': 'cooler-ice-calculator',
      'title': 'Cooler Ice Calculator - Pounds of Ice by Guests, Hours and Weather',
      'h1': 'Cooler Ice Calculator',
      'desc': 'How much ice for the cooler? Guests times hours plus weather and food give pounds of ice, 10 lb bags to buy and the cooler size in quarts. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'how much ice for cooler calculator pounds per day tailgate',
      'tool': 'coolice',
      'args': {},
      'intro': ["Enter your guest count, how long the cooler holds, the weather, and whether food rides along. The calculator gives pounds of ice, the number of 10 lb bags to buy, and the cooler size in quarts that fits the load.",
               "Cooler reviews argue about rotomolded walls while the actual failure is arithmetic: not enough ice for the hours and the heat. This one prices the real variables - and the free upgrades, pre-chilling and block ice, that outperform any premium shell."],
      'howto': ["Count guests and honest hours from first drink to pack-up.",
               "Pick the weather band and say whether food shares the box.",
               "Buy the bags figure rounded up, pre-chill the box, and pack blocks under cubes."],
      'faqs': [("How much ice do I need for a cooler per day?", "About 6 lb per person per day of drinking covers the standard one-pound-per-four-hours rule - two people on a 12-hour tailgate day want 18-20 lb in warm weather. Food sharing adds half again, and anything over 29 C adds a quarter more."),
               ("What size cooler for a tailgate?", "Quarts roughly double the ice pounds: 20 lb of ice plus food wants a 40-50 qt box. Bigger is not better - an oversized, half-empty cooler melts ice faster because the air space is the enemy."),
               ("Does block ice really last longer?", "Yes - a block melts at roughly half the rate of cubes because less surface touches the air. Frozen water bottles are the cheap version: block ice that becomes cold drinking water instead of a soggy cooler floor."),
               ("Should I pre-chill the cooler?", "A warm cooler eats the first several pounds of ice just cooling its own walls. Thirty minutes of ice water dumped out before packing is the highest-return step in the whole routine - it is free and adds hours.")]}
P.append("    pages.append(%r)\n" % (d1,))

d2 = {'slug': 'tailgate-food-calculator',
      'title': 'Tailgate Food Calculator - Meat, Sides and Drinks per Person',
      'h1': 'Tailgate Food Calculator',
      'desc': 'How much food for a tailgate? Adults, kids and meal style give pounds of raw meat, cups of sides and cans of drinks - a shopping list you can actually buy. Free, no sign-up.',
      'category': 'calculator',
      'keyword': 'tailgate food calculator how much meat per person drinks',
      'tool': 'tailgatefood',
      'args': {},
      'intro': ["Enter adults, kids, the meal style and hours in the lot. The calculator returns pounds of raw meat, cups of sides, and cans of drinks - the three lines of the shopping trip, sized to who is actually coming.",
               "Party food advice speaks in vague handfuls, and tailgates punish vagueness: there is no corner shop at the stadium. The arithmetic here is the deli counter standard - half a pound of raw meat per adult - with honest dials for snack-only mornings and second-helping crowds."],
      'howto': ["Count adults and kids coming to the spread, not the invitation list.",
                "Pick the meal style and hours out; drinks scale with both.",
                "Buy the three numbers as given - and round the ice up on the cooler page."],
      'faqs': [("How much meat do you need per person for a tailgate?", "Half a pound of raw meat per adult and a quarter per child is the standard, before cooking loss - six adults and two kids take 3.5 lb raw, about 2.6 lb cooked. Bone-in cuts like drumsticks need a third more weight for the same eating."),
               ("How many drinks per person for a tailgate?", "Two per person in the first hour and one each hour after - the first-hour rule. Eight adults out for four hours drink about 40 cans, which is why the calculator rounds to six-packs and lets the cooler page size the ice."),
               ("How many sides should a tailgate have?", "Two is the sweet spot: half a cup per person each, so a dozen eaters want 12 cups across both. One side feeds the meal and none feels like a stall - a third side mostly becomes landfill."),
               ("How much food for a 6-hour tailgate?", "Food does not scale much with hours - people eat one meal, maybe seconds. Hours scale the drinks: at six hours, plan four cans per adult. The snack-only morning toggle covers the early kickoff when the meal is the stadium's problem.")]}
P.append("    pages.append(%r)\n" % (d2,))

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
print("R125 inject OK: 2 renderers + 2 pages + 2 emoji, ast passed")
