# -*- coding: utf-8 -*-
"""R159 冬日厨房+年假规划双页:slow-cooker-converter(烤箱换炖锅)+pto-optimizer(带薪假串联)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: SLOWCOOK ----------
Sc2 = 'SLOWCOOK = """<div class="tool" id="tt-sc2">\n'
Sc2 += '  <div class="fields">\n'
Sc2 += '    <div class="field"><label for="sc2-m">Oven time in the recipe (minutes)</label><input id="sc2-m" type="number" min="10" max="240" value="60"></div>\n'
Sc2 += '    <div class="field"><label for="sc2-s">Slow cooker setting</label><select id="sc2-s"><option value="low" selected>Low</option><option value="high">High</option></select></div>\n'
Sc2 += '  </div>\n'
Sc2 += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sc2-out">&#8211;</span><span class="result-unit">in the slow cooker</span></div>\n'
Sc2 += '  <div class="stats">\n'
Sc2 += '    <div class="stat"><b id="sc2-s1">&#8211;</b><span>the other setting</span></div>\n'
Sc2 += '    <div class="stat"><b id="sc2-s2">&#8211;</b><span>liquid in the recipe</span></div>\n'
Sc2 += '    <div class="stat"><b id="sc2-s3">&#8211;</b><span>dairy and seafood go in</span></div>\n'
Sc2 += '  </div>\n'
Sc2 += '  <div class="tool-note" id="sc2-note"></div>\n'
Sc2 += '  <button type="button" class="tool-btn" id="sc2-share">Share my conversion</button>\n'
Sc2 += '</div>\n'
Sc2 += '<script>(function(){\n'
Sc2 += "var M=document.getElementById('sc2-m'),S=document.getElementById('sc2-s');\n"
Sc2 += "function calc(){\n"
Sc2 += "  var m=parseFloat(M.value)||60,set=S.value;\n"
Sc2 += "  var low,set2;\n"
Sc2 += "  if(m<=30){low=5;high=1.75;}\n"
Sc2 += "  else if(m<=45){low=7;high=3.5;}\n"
Sc2 += "  else{low=9;high=5;}\n"
Sc2 += "  var hrs=set==='low'?low:high, other=set==='low'?high:low;\n"
Sc2 += "  var d1=Math.round(hrs*10)/10, d2=Math.round(other*10)/10;\n"
Sc2 += "  document.getElementById('sc2-out').textContent=d1+' hours';\n"
Sc2 += "  document.getElementById('sc2-s1').textContent=d2+' hours on '+(set==='low'?'high':'low');\n"
Sc2 += "  document.getElementById('sc2-s2').textContent='cut by half';\n"
Sc2 += "  document.getElementById('sc2-s3').textContent='last hour';\n"
Sc2 += "  document.getElementById('sc2-note').textContent='The conversion is a table, not a formula - these bands are the standard published ranges, quoted as midpoints. Three rules carry the dish: cut liquids by half because the lid seals and nothing evaporates; add dairy, seafood and fresh herbs in the last hour or they curdle and dissolve; and never lift the lid - each peek costs about twenty minutes of cooking. Cheap, tough cuts are the whole point of the machine - collagen needs the hours that expensive steaks would hate. Fill the pot between half and two-thirds; empty pots run hot and full pots run cold.';\n"
Sc2 += "  document.title='Slow cooker: '+d1+' hours on '+set+' - ToolDune';\n"
Sc2 += "}\n"
Sc2 += "function save(){try{localStorage.setItem('tt_slowcook',JSON.stringify({m:M.value,s:S.value}));}catch(e){}}\n"
Sc2 += "[M,S].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Sc2 += "var pre=false;\n"
Sc2 += "var qs=new URLSearchParams(location.search);\n"
Sc2 += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
Sc2 += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_slowcook')||'null');if(m){if(m.m){M.value=m.m;}if(m.s){S.value=m.s;}}}catch(e){}}\n"
Sc2 += "calc();\n"
Sc2 += "document.getElementById('sc2-share').addEventListener('click',function(){\n"
Sc2 += "  var txt='Oven '+M.value+' min converts to '+document.getElementById('sc2-out').textContent+' on '+S.value+' in the slow cooker. Convert yours:';\n"
Sc2 += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value);\n"
Sc2 += "  if(navigator.share){navigator.share({title:'Slow cooker conversion',text:txt,url:url}).catch(function(){});}\n"
Sc2 += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my conversion';},1500);}\n"
Sc2 += "});\n"
Sc2 += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: PTOOPT ----------
Pt = 'PTOOPT = """<div class="tool" id="tt-pt">\n'
Pt += '  <div class="fields">\n'
Pt += '    <div class="field"><label for="pt-d">PTO days per year</label><input id="pt-d" type="number" min="1" max="60" value="15"></div>\n'
Pt += '    <div class="field"><label for="pt-b">Breaks you want</label><select id="pt-b"><option value="2">2 long holidays</option><option value="3" selected>3 breaks</option><option value="4">4 mini-breaks</option></select></div>\n'
Pt += '  </div>\n'
Pt += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pt-out">&#8211;</span><span class="result-unit">calendar days off, chained</span></div>\n'
Pt += '  <div class="stats">\n'
Pt += '    <div class="stat"><b id="pt-s1">&#8211;</b><span>vs one naive block</span></div>\n'
Pt += '    <div class="stat"><b id="pt-s2">&#8211;</b><span>weekends harvested</span></div>\n'
Pt += '    <div class="stat"><b id="pt-s3">&#8211;</b><span>the Wednesday trick</span></div>\n'
Pt += '  </div>\n'
Pt += '  <div class="tool-note" id="pt-note"></div>\n'
Pt += '  <button type="button" class="tool-btn" id="pt-share">Share my PTO math</button>\n'
Pt += '</div>\n'
Pt += '<script>(function(){\n'
Pt += "var D=document.getElementById('pt-d'),B=document.getElementById('pt-b');\n"
Pt += "function calc(){\n"
Pt += "  var d=Math.max(1,parseFloat(D.value)||15),br=parseFloat(B.value)||3;\n"
Pt += "  var per=Math.floor(d/br), use=per*br, weekend=br*2, cal=use+weekend;\n"
Pt += "  var d1=use+2, d2=weekend;\n"
Pt += "  document.getElementById('pt-out').textContent=cal;\n"
Pt += "  document.getElementById('pt-s1').textContent=d1+' in one block';\n"
Pt += "  document.getElementById('pt-s2').textContent=d2;\n"
Pt += "  document.getElementById('pt-s3').textContent='+8 days for 1';\n"
Pt += "  document.getElementById('pt-note').textContent='The chain rule: a PTO day only buys you a workday unless it touches a weekend - so split the allowance into breaks, each starting Monday and ending Friday, and the weekends on both ends ride free. Split fifteen days into three five-day breaks and you travel twenty-one calendar days. The extreme version is the Wednesday trick: a single Wednesday off bridges two weekends into nine days of coverage, which is why booking January flights for July is also on this page - the cheapest seats of the year sell while everyone else is writing resolutions.';\n"
Pt += "  document.title=cal+' days off from '+Math.round(d)+' PTO - ToolDune';\n"
Pt += "}\n"
Pt += "function save(){try{localStorage.setItem('tt_ptoopt',JSON.stringify({d:D.value,b:B.value}));}catch(e){}}\n"
Pt += "[D,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Pt += "var pre=false;\n"
Pt += "var qs=new URLSearchParams(location.search);\n"
Pt += "if(qs.get('d')){D.value=qs.get('d');pre=true;}\n"
Pt += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_ptoopt')||'null');if(m){if(m.d){D.value=m.d;}if(m.b){B.value=m.b;}}}catch(e){}}\n"
Pt += "calc();\n"
Pt += "document.getElementById('pt-share').addEventListener('click',function(){\n"
Pt += "  var txt=document.getElementById('pt-out').textContent+' calendar days off from '+D.value+' PTO - chain yours:';\n"
Pt += "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
Pt += "  if(navigator.share){navigator.share({title:'PTO chaining',text:txt,url:url}).catch(function(){});}\n"
Pt += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my PTO math';},1500);}\n"
Pt += "});\n"
Pt += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("SLOWCOOK", "PTOOPT"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Sc2 + Pt + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "homegym": lambda args: HOMEGYM,',
    '    "homegym": lambda args: HOMEGYM,\n'
    '    "slowcook": lambda args: SLOWCOOK,\n'
    '    "ptoopt": lambda args: PTOOPT,')
sub(BUILD_P, '    "giftreturn": "🔁", "icemelt": "❄", "homegym": "🏠",',
    '    "giftreturn": "🔁", "icemelt": "❄", "homegym": "🏠",\n'
    '    "slowcook": "🍲", "ptoopt": "📅",')

P = []
d = {'slug': 'slow-cooker-converter',
     'title': 'Slow Cooker Converter - Oven Time to Low and High Settings',
     'h1': 'Slow Cooker Converter',
     'desc': 'Convert any oven recipe time to slow cooker hours on low or high - with the liquid, dairy and lid-lid rules that carry the dish. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'slow cooker conversion oven to crockpot time calculator',
     'tool': 'slowcook',
     'args': {},
     'intro': ["Enter the oven time from the recipe and pick a setting. The converter uses the standard published conversion bands - a one-hour oven dish becomes roughly five hours on low - and shows the other setting too, because plans change at noon.",
              "Most conversion charts stop at the hours. This one adds the three rules that actually carry the dish: cut liquids in half because nothing evaporates under the lid, add dairy and seafood in the last hour, and never lift the lid - each peek costs about twenty minutes of cooking."],
     'howto': ["Read the oven time and temperature off the original recipe.",
               "Pick low for all-day cooking or high for the afternoon start.",
               "Halve the liquids and hold the dairy until the end."],
     'faqs': [("How do I convert oven time to slow cooker time?",
               "Use the standard bands: 15-30 oven minutes becomes 4-6 hours on low; 35-45 minutes becomes 6-8 on low; anything from 50 minutes to 3 hours becomes 8-10 on low. High runs about half of low. The calculator quotes the midpoints."),
              ("Does slow cooker liquid need reducing?",
               "Cut it by about half - the sealed lid means nothing evaporates, and recipes written for ovens assume reduction. You can always thicken at the end with the lid off; you cannot un-soup a stew."),
              ("Can I put milk or cream in a slow cooker?",
               "Not at the start - dairy curdles over long hours. Stir milk, cream, yogurt or sour cream in during the last thirty to sixty minutes; the same rule sends seafood and fresh herbs late."),
              ("Does lifting the lid really matter?",
               "Yes - each peek releases heat and costs roughly twenty minutes of cooking time. The slow cooker is designed to be closed; check through the glass if you must, and trust the machine on anything except the last hour.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'pto-optimizer',
     'title': 'PTO Optimizer - Turn Vacation Days into Maximum Days Off',
     'h1': 'PTO Optimizer',
     'desc': 'Split your PTO across chained breaks so weekends ride free - see calendar days off versus one naive block, plus the Wednesday trick. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'pto optimizer how to maximize vacation days 2027',
     'tool': 'ptoopt',
     'args': {},
     'intro': ["Enter your annual PTO and how many breaks you want. The optimizer splits it into Monday-to-Friday chains so the weekends on both ends ride free, and shows the calendar days you get versus one naive block.",
              "The chain rule: a PTO day only buys a workday unless it touches a weekend. Fifteen days split into three five-day breaks is twenty-one calendar days off - and the extreme version, the Wednesday trick, turns a single day into nine days of coverage. Book the July flights in January; the cheapest seats of the year sell while everyone else is writing resolutions."],
     'howto': ["Set your total PTO - the number on your offer letter, not your hopes.",
               "Choose the break count; three five-day chains fit most years.",
               "Anchor each chain to a public holiday for a free extra day."],
     'faqs': [("How do I maximize my PTO days?",
               "Never spend PTO on a weekend side - chain every break from Monday to Friday so four weekend days ride free per break. Split 15 days into three chains and you get 21 calendar days instead of 17 in one block."),
              ("What is the Wednesday trick?",
               "Take only the Wednesday that sits between two weekends: one PTO day buys nine consecutive days away from the desk. It works because the weekends bracket the single day - the cheapest coverage in the PTO playbook."),
              ("When should I book flights for next year?",
               "January, for the summer. Airlines price leisure routes low while demand is seasonal-low and everyone is budgeting rather than booking - the same seats cost noticeably more from spring onward."),
              ("Should I take one long vacation or several breaks?",
               "Research on recovery favors multiple breaks: the refresh from a week away fades within weeks, so three resets beat one long block for year-round wellbeing. The optimizer shows what the chaining costs - usually nothing but planning.")]}
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
print("R159 inject OK: 2 renderers + 2 pages + 2 emoji, ast passed")
