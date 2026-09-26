# -*- coding: utf-8 -*-
"""R171 婚宴预算单页:wedding-budget-calculator(客数杠杆+10%缓冲+淡季诚实口径)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

Wd = 'WEDDING = """<div class="tool" id="tt-wd">\n'
Wd += '  <div class="fields">\n'
Wd += '    <div class="field"><label for="wd-g">Guests</label><input id="wd-g" type="number" min="10" max="500" value="100"></div>\n'
Wd += '    <div class="field"><label for="wd-c">Catering per head</label><input id="wd-c" type="number" min="20" value="85"></div>\n'
Wd += '    <div class="field"><label for="wd-b">Bar package per head</label><select id="wd-b"><option value="0">Beer and wine only</option><option value="25" selected>Full bar - +25/head</option><option value="45">Premium - +45/head</option></select></div>\n'
Wd += '    <div class="field"><label for="wd-f">Venue, photo, attire, flowers - flat total</label><input id="wd-f" type="number" min="0" value="11500"></div>\n'
Wd += '  </div>\n'
Wd += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wd-out">&#8211;</span><span class="result-unit">total with 10% buffer</span></div>\n'
Wd += '  <div class="stats">\n'
Wd += '    <div class="stat"><b id="wd-s1">&#8211;</b><span>per guest, all in</span></div>\n'
Wd += '    <div class="stat"><b id="wd-s2">&#8211;</b><span>each guest adds</span></div>\n'
Wd += '    <div class="stat"><b id="wd-s3">&#8211;</b><span>cutting 10 guests saves</span></div>\n'
Wd += '  </div>\n'
Wd += '  <div class="tool-note" id="wd-note"></div>\n'
Wd += '  <button type="button" class="tool-btn" id="wd-share">Share my wedding math</button>\n'
Wd += '</div>\n'
Wd += '<script>(function(){\n'
Wd += "var G=document.getElementById('wd-g'),C=document.getElementById('wd-c'),B=document.getElementById('wd-b'),F=document.getElementById('wd-f');\n"
Wd += "function calc(){\n"
Wd += "  var g=Math.max(10,Math.round(parseFloat(G.value)||100)),c=parseFloat(C.value)||85,b=parseFloat(B.value)||0,f=parseFloat(F.value)||0;\n"
Wd += "  var perHead=c+b, base=g*perHead+f, total=base*1.1;\n"
Wd += "  var d1=Math.round(total), d2=Math.round(total/g), d3=Math.round(perHead*1.1*10);\n"
Wd += "  document.getElementById('wd-out').textContent='$'+d1;\n"
Wd += "  document.getElementById('wd-s1').textContent='$'+d2;\n"
Wd += "  document.getElementById('wd-s2').textContent='$'+Math.round(perHead*1.1);\n"
Wd += "  document.getElementById('wd-s3').textContent='$'+d3;\n"
Wd += "  document.getElementById('wd-note').textContent='The lever is the guest list, full stop: every guest costs their plate plus bar plus the share of everything flat, and cutting ten people saves more than any negotiation with a vendor. The buffer line is not padding - it is the day-of costs every wedding forgets: overtime hours, the extra table, the vendor meal count. Two honest levers beyond the list: off-season Saturdays and any Sunday run a discount tier below peak dates, and the bar package is where polite choices cost five figures - beer and wine with a signature cocktail reads generous and prices like a used car less. The national average lands past thirty thousand, which is a fact to see early, not a target to chase.';\n"
Wd += "  document.title='Wedding: $'+d1+' for '+g+' guests - ToolDune';\n"
Wd += "}\n"
Wd += "function save(){try{localStorage.setItem('tt_wedding',JSON.stringify({g:G.value,c:C.value,b:B.value,f:F.value}));}catch(e){}}\n"
Wd += "[G,C,B,F].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Wd += "var pre=false;\n"
Wd += "var qs=new URLSearchParams(location.search);\n"
Wd += "if(qs.get('g')){G.value=qs.get('g');pre=true;}\n"
Wd += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_wedding')||'null');if(m){if(m.g){G.value=m.g;}if(m.c){C.value=m.c;}if(m.b){B.value=m.b;}if(m.f){F.value=m.f;}}}catch(e){}}\n"
Wd += "calc();\n"
Wd += "document.getElementById('wd-share').addEventListener('click',function(){\n"
Wd += "  var txt='Our wedding plan: $'+document.getElementById('wd-out').textContent+' for '+G.value+' guests. Price yours:';\n"
Wd += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value);\n"
Wd += "  if(navigator.share){navigator.share({title:'Wedding budget',text:txt,url:url}).catch(function(){});}\n"
Wd += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my wedding math';},1500);}\n"
Wd += "});\n"
Wd += "})();\n</script>\n\"\"\"\n\n"

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
assert "\nWEDDING = " not in src, "WEDDING already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Wd + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "refundplan": lambda args: REFUNDPLAN,',
    '    "refundplan": lambda args: REFUNDPLAN,\n'
    '    "wedding": lambda args: WEDDING,')
sub(BUILD_P, '    "squares": "🏈", "springbreak": "🌴", "refundplan": "💸",',
    '    "squares": "🏈", "springbreak": "🌴", "refundplan": "💸",\n'
    '    "wedding": "💍",')

P = []
d = {'slug': 'wedding-budget-calculator',
     'title': 'Wedding Budget Calculator - Total, Per Guest and the Guest-Count Lever',
     'h1': 'Wedding Budget Calculator',
     'desc': 'Guests, catering, bar and flat costs give the real total with a 10 percent buffer - and the guest-count math that saves more than any vendor negotiation. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'wedding budget calculator cost per guest average wedding cost',
     'tool': 'wedding',
     'args': {},
     'intro': ["Enter the guest count, catering per head, the bar package and everything flat - venue, photo, attire, flowers. The calculator totals it with the 10 percent buffer every wedding needs, prices each guest all-in, and shows what trimming the list actually saves.",
              "The lever is the guest list, full stop: every guest costs their plate plus bar plus a share of everything flat, so cutting ten people saves more than any negotiation with a vendor. The honest context - the national average lands past thirty thousand - is a fact to see early, not a target to chase."],
     'howto': ["Guest count first - it multiplies everything else on the page.",
               "Price catering and the bar per head from a real quote or two.",
               "Roll venue, photo, attire and flowers into the flat total."],
     'faqs': [("What is the average wedding budget?",
               "The national average lands past thirty thousand dollars for roughly a hundred guests - about 300 per guest all-in. Averages anchor badly though: the venue city and the guest count swing the number more than any other choice, and the calculator prices your plan instead of the average."),
              ("What is the biggest cost lever in a wedding budget?",
               "The guest list. Each guest adds their plate, their bar and their share of the flat costs - commonly 110-150 dollars all-in - so ten fewer guests save more than most vendor haggling ever will."),
              ("How much should the bar cost at a wedding?",
               "Beer and wine with a signature cocktail reads generous and prices a fraction of a full premium bar, which can add 45 dollars per head. Over a hundred guests, the bar choice alone is a five-figure decision."),
              ("Why add 10 percent to the wedding budget?",
               "Day-of costs nobody prices in advance: vendor overtime, the extra table that appeared, the real meal count for the crew. The buffer turns those from crisis line-items into a rounding error - and unspent, it seeds the honeymoon.")]}
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
print("R171 inject OK: 1 renderer + 1 page + 1 emoji, ast passed")
