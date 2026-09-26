# -*- coding: utf-8 -*-
"""R135 年终钱袋簇:social-security-break-even(领钱年龄账)+thanksgiving-dinner-cost(每客菜单账)+roth-vs-traditional-401k(税点裁决)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: SSCLAIM ----------
Sc = 'SSCLAIM = """<div class="tool" id="tt-ssc">\n'
Sc += '  <div class="fields">\n'
Sc += '    <div class="field"><label for="ss-b">Birth year</label><input id="ss-b" type="number" min="1930" max="2010" value="1965"></div>\n'
Sc += '    <div class="field"><label for="ss-p">Monthly benefit at full retirement age</label><input id="ss-p" type="number" min="100" step="10" value="2000"></div>\n'
Sc += '    <div class="field"><label for="ss-a">Claiming age</label><select id="ss-a"><option value="62">62 - earliest</option><option value="65">65</option><option value="67" selected>67</option><option value="70">70 - max delay</option></select></div>\n'
Sc += '  </div>\n'
Sc += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ss-out">&#8211;</span><span class="result-unit">monthly at your claiming age</span></div>\n'
Sc += '  <div class="stats">\n'
Sc += '    <div class="stat"><b id="ss-s1">&#8211;</b><span>vs full retirement age</span></div>\n'
Sc += '    <div class="stat"><b id="ss-s2">&#8211;</b><span>annual at claim age</span></div>\n'
Sc += '    <div class="stat"><b id="ss-s3">&#8211;</b><span>62 vs 70 break-even</span></div>\n'
Sc += '  </div>\n'
Sc += '  <div class="tool-note" id="ss-note"></div>\n'
Sc += '  <button type="button" class="tool-btn" id="ss-share">Share my claiming math</button>\n'
Sc += '</div>\n'
Sc += '<script>(function(){\n'
Sc += "var BY=document.getElementById('ss-b'),PIA=document.getElementById('ss-p'),AG=document.getElementById('ss-a');\n"
Sc += "function fraMonths(y){\n"
Sc += "  if(y<=1937)return 65*12;\n"
Sc += "  if(y<=1942)return (65*12)+(y-1937)*2;\n"
Sc += "  if(y<=1954)return 66*12;\n"
Sc += "  if(y<=1959)return (66*12)+(y-1954)*2;\n"
Sc += "  return 67*12;\n"
Sc += "}\n"
Sc += "function calc(){\n"
Sc += "  var y=parseInt(BY.value,10)||1965,p=parseFloat(PIA.value)||0,a=parseInt(AG.value,10)||67;\n"
Sc += "  var fm=fraMonths(y),am=a*12,d=Math.round(am-fm);\n"
Sc += "  var f=1;\n"
Sc += "  if(d<0){var e=Math.min(36,-d),e2=Math.max(0,(-d)-36);f=1-(e*5/9+e2*5/12)/100;}\n"
Sc += "  else if(d>0){f=1+(d*2/3)/100;}\n"
Sc += "  var f62=1,m62=62*12,d62=Math.round(m62-fm),e1=Math.min(36,d62),e2=Math.max(0,d62-36);\n"
Sc += "  f62=1-(e1*5/9+e2*5/12)/100;\n"
Sc += "  var f70=1+(8*12*2/3)/100;\n"
Sc += "  var m=p*f,ann=m*12,base=p*f62,mx=p*f70;\n"
Sc += "  var be=62+(mx*8)/(mx-base);\n"
Sc += "  var d1=Math.round(m),d2=Math.round((m-p)*10)/10,d3=Math.round(ann);\n"
Sc += "  document.getElementById('ss-out').textContent='$'+d1.toLocaleString();\n"
Sc += "  document.getElementById('ss-s1').textContent=(d2>=0?'+':'-')+'$'+Math.abs(d2);\n"
Sc += "  document.getElementById('ss-s2').textContent='$'+d3.toLocaleString();\n"
Sc += "  document.getElementById('ss-s3').textContent='about '+Math.floor(be);\n"
Sc += "  var msg='Claiming at '+a+' locks a monthly check of $'+d1.toLocaleString();\n"
Sc += "  if(d<0){msg+=' - a cut of about '+Math.round((1-f)*100)+'% for starting early, and the smaller base also means every future cost-of-living raise is smaller.';}\n"
Sc += "  else if(d>0){msg+=' - delayed credits add about '+Math.round((f-1)*100)+'% for life, and the bigger base compounds every COLA after it.';}\n"
Sc += "  else{msg+=' - your full retirement age, no cut and no credit.';}\n"
Sc += "  msg+=' The break-even for 62-versus-70 sits near age '+Math.floor(be)+': live past it and waiting wins on raw totals. The honest tiebreakers are health, cash need, and the earnings test that claws back $1 per $2 earned above the limit before full retirement age - optimization macho is not on the list.';\n"
Sc += "  document.getElementById('ss-note').textContent=msg;\n"
Sc += "  document.title='Claim at '+a+': $'+d1.toLocaleString()+'/mo - ToolDune';\n"
Sc += "}\n"
Sc += "function save(){try{localStorage.setItem('tt_ssclaim',JSON.stringify({b:BY.value,p:PIA.value,a:AG.value}));}catch(e){}}\n"
Sc += "[BY,PIA,AG].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Sc += "var pre=false;\n"
Sc += "var qs=new URLSearchParams(location.search);\n"
Sc += "if(qs.get('p')){PIA.value=qs.get('p');pre=true;}\n"
Sc += "if(qs.get('a')){AG.value=qs.get('a');pre=true;}\n"
Sc += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_ssclaim')||'null');if(m){if(m.b){BY.value=m.b;}if(m.p){PIA.value=m.p;}if(m.a){AG.value=m.a;}}}catch(e){}}\n"
Sc += "calc();\n"
Sc += "document.getElementById('ss-share').addEventListener('click',function(){\n"
Sc += "  var txt='Claiming at '+AG.value+' pays $'+document.getElementById('ss-out').textContent+' a month. Run your own numbers:';\n"
Sc += "  var url=location.origin+location.pathname+'?p='+encodeURIComponent(PIA.value)+'&a='+encodeURIComponent(AG.value);\n"
Sc += "  if(navigator.share){navigator.share({title:'Social Security claiming math',text:txt,url:url}).catch(function(){});}\n"
Sc += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my claiming math';},1500);}\n"
Sc += "});\n"
Sc += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: THANKCOST ----------
Tk = 'THANKCOST = """<div class="tool" id="tt-tkc">\n'
Tk += '  <div class="fields">\n'
Tk += '    <div class="field"><label for="tk-g">Guests</label><input id="tk-g" type="number" min="1" max="60" value="10"></div>\n'
Tk += '    <div class="field"><label for="tk-p">Turkey price per pound</label><input id="tk-p" type="number" min="0.5" step="0.05" value="1.90"></div>\n'
Tk += '    <div class="field"><label for="tk-s">Sides style</label><select id="tk-s"><option value="4">Simple - $4/guest</option><option value="7" selected>Classic - $7/guest</option><option value="10">Full spread - $10/guest</option></select></div>\n'
Tk += '    <div class="field"><label for="tk-d">Drinks and extras per guest</label><input id="tk-d" type="number" min="0" step="0.5" value="3"></div>\n'
Tk += '  </div>\n'
Tk += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tk-out">&#8211;</span><span class="result-unit">total dinner bill</span></div>\n'
Tk += '  <div class="stats">\n'
Tk += '    <div class="stat"><b id="tk-s1">&#8211;</b><span>per guest</span></div>\n'
Tk += '    <div class="stat"><b id="tk-s2">&#8211;</b><span>turkey pounds to buy</span></div>\n'
Tk += '    <div class="stat"><b id="tk-s3">&#8211;</b><span>turkey share of bill</span></div>\n'
Tk += '  </div>\n'
Tk += '  <div class="tool-note" id="tk-note"></div>\n'
Tk += '  <button type="button" class="tool-btn" id="tk-share">Share my dinner budget</button>\n'
Tk += '</div>\n'
Tk += '<script>(function(){\n'
Tk += "var G=document.getElementById('tk-g'),PR=document.getElementById('tk-p'),S=document.getElementById('tk-s'),DR=document.getElementById('tk-d');\n"
Tk += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Tk += "function calc(){\n"
Tk += "  var g=Math.max(1,Math.round(num(G))),pr=num(PR),side=num(S),dr=num(DR);\n"
Tk += "  var lbs=g*1.5, bird=lbs*pr, sides=g*side, drinks=g*dr, total=bird+sides+drinks;\n"
Tk += "  var d1=Math.round(total*10)/10, d2=Math.round(total/g*100)/100, d3=Math.round(bird*10)/10;\n"
Tk += "  var share=total?Math.round(bird/total*100):0;\n"
Tk += "  document.getElementById('tk-out').textContent='$'+d1;\n"
Tk += "  document.getElementById('tk-s1').textContent='$'+d2;\n"
Tk += "  document.getElementById('tk-s2').textContent=Math.round(lbs)+' lb';\n"
Tk += "  document.getElementById('tk-s3').textContent=share+'%';\n"
Tk += "  document.getElementById('tk-note').textContent='The 1.5 pounds per guest rule is what guarantees leftovers - a 15-pound bird for 10 people means sandwiches all weekend, and the thaw math starts days earlier (see the turkey thaw planner). The bird looks like the headline, but sides quietly match it and drinks pad the tail. Two honest moves: frozen turkeys drop in price the week after the holiday panic, and the potluck move - assigning two sides to guests - cuts the bill by a fifth without anyone noticing.';\n"
Tk += "  document.title='Thanksgiving for '+g+': $'+d1+' - ToolDune';\n"
Tk += "}\n"
Tk += "function save(){try{localStorage.setItem('tt_tkcost',JSON.stringify({g:G.value,p:PR.value,s:S.value,d:DR.value}));}catch(e){}}\n"
Tk += "[G,PR,S,DR].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Tk += "var pre=false;\n"
Tk += "var qs=new URLSearchParams(location.search);\n"
Tk += "if(qs.get('g')){G.value=qs.get('g');pre=true;}\n"
Tk += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_tkcost')||'null');if(m){if(m.g){G.value=m.g;}if(m.p){PR.value=m.p;}if(m.s){S.value=m.s;}if(m.d){DR.value=m.d;}}}catch(e){}}\n"
Tk += "calc();\n"
Tk += "document.getElementById('tk-share').addEventListener('click',function(){\n"
Tk += "  var txt='Thanksgiving for '+G.value+' comes to about $'+document.getElementById('tk-out').textContent+'. Budget yours:';\n"
Tk += "  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value);\n"
Tk += "  if(navigator.share){navigator.share({title:'Thanksgiving dinner budget',text:txt,url:url}).catch(function(){});}\n"
Tk += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my dinner budget';},1500);}\n"
Tk += "});\n"
Tk += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: ROTHTRA ----------
Rt = 'ROTHTRA = """<div class="tool" id="tt-rvt">\n'
Rt += '  <div class="fields">\n'
Rt += '    <div class="field"><label for="rv-c">Annual contribution</label><input id="rv-c" type="number" min="100" step="100" value="6000"></div>\n'
Rt += '    <div class="field"><label for="rv-n">Your tax rate now (%)</label><select id="rv-n"><option value="12">12%</option><option value="22" selected>22%</option><option value="24">24%</option><option value="32">32%</option><option value="35">35%</option></select></div>\n'
Rt += '    <div class="field"><label for="rv-r">Expected rate in retirement (%)</label><select id="rv-r"><option value="12" selected>12% - lower</option><option value="22">22% - same</option><option value="24">24% - higher</option><option value="32">32% - much higher</option></select></div>\n'
Rt += '    <div class="field"><label for="rv-y">Years to grow</label><input id="rv-y" type="number" min="1" max="45" value="25"></div>\n'
Rt += '  </div>\n'
Rt += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rv-out">&#8211;</span><span class="result-unit">wins after all taxes</span></div>\n'
Rt += '  <div class="stats">\n'
Rt += '    <div class="stat"><b id="rv-s1">&#8211;</b><span>Roth final, tax free</span></div>\n'
Rt += '    <div class="stat"><b id="rv-s2">&#8211;</b><span>Traditional final, after tax</span></div>\n'
Rt += '    <div class="stat"><b id="rv-s3">&#8211;</b><span>gap over the years</span></div>\n'
Rt += '  </div>\n'
Rt += '  <div class="tool-note" id="rv-note"></div>\n'
Rt += '  <button type="button" class="tool-btn" id="rv-share">Share my verdict</button>\n'
Rt += '</div>\n'
Rt += '<script>(function(){\n'
Rt += "var C=document.getElementById('rv-c'),TN=document.getElementById('rv-n'),TR=document.getElementById('rv-r'),Y=document.getElementById('rv-y');\n"
Rt += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Rt += "function calc(){\n"
Rt += "  var c=num(C),tn=num(TN)/100,tr=num(TR)/100,y=Math.min(45,Math.max(1,num(Y))),r=0.07;\n"
Rt += "  var fv=c*((Math.pow(1+r,y)-1)/r);\n"
Rt += "  var roth=fv*(1-tn),trad=fv*(1-tr);\n"
Rt += "  var gap=Math.abs(roth-trad);\n"
Rt += "  var d1=Math.round(roth).toLocaleString(),d2=Math.round(trad).toLocaleString(),d3=Math.round(gap).toLocaleString();\n"
Rt += "  var winner=roth>=trad?'Roth':'Traditional';\n"
Rt += "  document.getElementById('rv-out').textContent=winner;\n"
Rt += "  document.getElementById('rv-s1').textContent='$'+d1;\n"
Rt += "  document.getElementById('rv-s2').textContent='$'+d2;\n"
Rt += "  document.getElementById('rv-s3').textContent='$'+d3;\n"
Rt += "  var msg='Same growth, same market - the only question is which year the government takes its cut. If your rate in retirement is lower than today, the traditional deduction wins; if it is higher, the Roth lock-in wins; if identical, they tie exactly. ';\n"
Rt += "  msg+='Nobody actually knows their retirement rate, which is why the honest default is split contributions - Roth while your bracket is low, traditional in peak earning years. Employer match rides on top of either choice and is always worth taking first.';\n"
Rt += "  document.getElementById('rv-note').textContent=msg;\n"
Rt += "  document.title=winner+' wins by $'+d3+' - ToolDune';\n"
Rt += "}\n"
Rt += "function save(){try{localStorage.setItem('tt_rothtra',JSON.stringify({c:C.value,n:TN.value,r:TR.value,y:Y.value}));}catch(e){}}\n"
Rt += "[C,TN,TR,Y].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Rt += "var pre=false;\n"
Rt += "var qs=new URLSearchParams(location.search);\n"
Rt += "if(qs.get('c')){C.value=qs.get('c');pre=true;}\n"
Rt += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_rothtra')||'null');if(m){if(m.c){C.value=m.c;}if(m.n){TN.value=m.n;}if(m.r){TR.value=m.r;}if(m.y){Y.value=m.y;}}}catch(e){}}\n"
Rt += "calc();\n"
Rt += "document.getElementById('rv-share').addEventListener('click',function(){\n"
Rt += "  var txt='My verdict: '+document.getElementById('rv-out').textContent+' wins by $'+document.getElementById('rv-s3').textContent+'. Run yours:';\n"
Rt += "  var url=location.origin+location.pathname+'?c='+encodeURIComponent(C.value);\n"
Rt += "  if(navigator.share){navigator.share({title:'Roth vs Traditional',text:txt,url:url}).catch(function(){});}\n"
Rt += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my verdict';},1500);}\n"
Rt += "});\n"
Rt += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("SSCLAIM", "THANKCOST", "ROTHTRA"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Sc + Tk + Rt + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "hsa": lambda args: HSAC,',
    '    "hsa": lambda args: HSAC,\n'
    '    "ssclaim": lambda args: SSCLAIM,\n'
    '    "thankcost": lambda args: THANKCOST,\n'
    '    "rothtra": lambda args: ROTHTRA,')
sub(BUILD_P, '    "hdhp": "🏥", "fsa": "💵", "hsa": "💰",',
    '    "hdhp": "🏥", "fsa": "💵", "hsa": "💰",\n'
    '    "ssclaim": "👴", "thankcost": "🍗", "rothtra": "⚖",')

P = []
d = {'slug': 'social-security-break-even-calculator',
     'title': 'Social Security Break Even Calculator - Claim at 62, 67 or 70?',
     'h1': 'Social Security Break Even Calculator',
     'desc': 'Your birth year and benefit estimate become the real monthly check at each claiming age - with the 62-vs-70 break-even age and the earnings-test warning. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'social security break even calculator claim at 62 or 70',
     'tool': 'ssclaim',
     'args': {},
     'intro': ["Enter your birth year and the benefit estimate from your SSA statement, then pick a claiming age. The calculator applies the actual reduction and credit formulas - 5/9 and 5/12 of a percent per early month, 2/3 of a percent per delayed month - and shows your real monthly check.",
              "Most claiming articles stop at wait-as-long-as-you-can. This one shows the break-even age where waiting wins on raw totals - around 80 for the 62-versus-70 question - and then says the quiet part: health, cash need and the earnings test decide more than the spreadsheet does."],
     'howto': ["Birth year sets your full retirement age - 67 for anyone born 1960 or later.",
               "Use the monthly estimate from your ssa.gov statement, not a guess.",
               "Slide the claiming age and watch the note flip between cut, par and credit."],
     'faqs': [("What is the Social Security break even age?",
               "For claiming at 62 versus 70, monthly checks cross in the early 80s: the smaller early check accumulates until the larger late check catches up. Live past it, waiting paid more; die before it, claiming early did. That is why health is the first input, not the last."),
              ("How much do I lose if I claim at 62?",
               "With a full retirement age of 67, claiming at 62 cuts the check by 30% - permanently. The base never recovers, and every future cost-of-living adjustment applies to the smaller figure, so the gap widens in dollar terms over time."),
              ("How much do delayed retirement credits add?",
               "Two-thirds of a percent per month past full retirement age, up to age 70 - 8% per year, or 24% more per month for waiting from 67 to 70. Credits stop at 70; claiming later never helps."),
              ("Can I work while collecting early?",
               "Yes, but the earnings test withholds $1 for every $2 earned above the annual limit before full retirement age. The money is not lost - it is credited back at full retirement age - but the cash flow surprises people every year.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'thanksgiving-dinner-cost-calculator',
     'title': 'Thanksgiving Dinner Cost Calculator - Total and Per Guest',
     'h1': 'Thanksgiving Dinner Cost Calculator',
     'desc': 'Guests, turkey price and sides style become a total dinner bill, a per-guest figure and the exact turkey weight to buy. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'thanksgiving dinner cost per person calculator',
     'tool': 'thankcost',
     'args': {},
     'intro': ["Set your guest count, the turkey price at your store, a sides style and the drinks budget. The calculator totals the bill, splits it per guest, and tells you the turkey weight to actually buy at 1.5 pounds per person.",
              "Supermarket flyers quote a per-guest average that fits nobody. This one prices your table - and points out that sides quietly match the bird, frozen turkeys get cheap after the panic week, and assigning two sides to guests cuts a fifth off the bill invisibly."],
     'howto': ["Count everyone at the table, including the cousin who only eats rolls.",
               "Check your store's price per pound - frozen birds run cheaper than fresh.",
               "Pick the sides style honestly; the potluck move is always available."],
     'faqs': [("How much turkey do I need per person?",
               "1.5 pounds uncooked per guest - it sounds huge, but bones, shrinkage and the strategic leftovers requirement eat most of it. A 15-pound bird comfortably feeds 10 with sandwich stock for the weekend."),
              ("What is the average cost of Thanksgiving dinner?",
               "National surveys land around $60-90 for a 10-person table, but the honest range is huge: geography, sides style and whether dessert is homemade swing it double. The calculator prices your actual cart instead of a national average."),
              ("How do I cut Thanksgiving costs without anyone noticing?",
               "Three moves: buy frozen early (prices drop after the panic week), run the potluck play with two sides assigned to guests, and make the drinks section self-serve. Nobody remembers the cranberry sauce brand."),
              ("When should I start thawing the turkey?",
               "Fridge thawing takes about 24 hours per 4-5 pounds, so a 15-pound bird starts five days out. The turkey thaw planner on this site builds the exact schedule from your dinner time.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'roth-vs-traditional-401k',
     'title': 'Roth vs Traditional 401k Calculator - Which Wins After All Taxes',
     'h1': 'Roth vs Traditional 401k Calculator',
     'desc': 'Same growth, different tax year: see the final after-tax value of Roth versus Traditional at your rates, and why the verdict reduces to one question. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'roth vs traditional 401k calculator which is better',
     'tool': 'rothtra',
     'args': {},
     'intro': ["Enter your annual contribution, your tax bracket now, your expected bracket in retirement and the years to grow. The calculator compounds both paths at 7% and shows the final after-tax value of each - Roth grows tax-free, Traditional deducts now and taxes at the end.",
              "Most comparison pages bury the punchline: with identical growth, the entire verdict collapses to whether your tax rate is higher today or in retirement. This one shows the math collapsing to exactly that - and then says honestly that nobody knows their retirement rate, which is why split contributions are the rational default."],
     'howto': ["Set the contribution you can actually sustain every year.",
               "Pick your bracket from your pay stub; pick the retirement bracket honestly.",
               "Watch the gap change as the retirement-rate guess moves - that is the real lesson."],
     'faqs': [("Which is better, Roth or Traditional 401k?",
               "Whichever comes with the lower tax rate: contribute and deduct at a high rate now (Traditional) or pay tax now and withdraw tax-free later (Roth). If the rates were identical they would tie exactly - every dollar of difference in the calculator comes from the rate gap."),
              ("Should young investors choose Roth?",
               "Usually yes - early-career brackets are the lowest of a working life, so buying tax-free growth at a 12% rate and withdrawing at 22%+ is a good trade. The calculator shows the same logic quantified: low rate now, Roth wins."),
              ("Does the employer match count for Roth?",
               "By default employer match lands pre-tax (Traditional side) regardless of your election, though plans increasingly allow Roth match. Either way the match itself is a 50-100% instant return - never leave it, whatever the flavor."),
              ("Can I split between Roth and Traditional?",
               "Yes, in the same plan, in the same year - and it is the honest strategy when the future rate is unknown. Splitting builds tax diversification: withdrawals can be balanced across taxable, Traditional and Roth buckets in retirement.")]}
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
print("R135 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
