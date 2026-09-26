# -*- coding: utf-8 -*-
"""R164 报税季三连:home-office-deduction(简化法办公室抵扣)+self-employment-set-aside(自雇税预留)+charitable-miles(慈善里程)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: HOMEDED ----------
Hd = 'HOMEDED = """<div class="tool" id="tt-hod">\n'
Hd += '  <div class="fields">\n'
Hd += '    <div class="field"><label for="hod-s">Office area (sq ft)</label><input id="hod-s" type="number" min="5" max="2000" value="120"></div>\n'
Hd += '    <div class="field"><label for="hod-r">Monthly rent or housing cost</label><input id="hod-r" type="number" min="0" value="1800"></div>\n'
Hd += '  </div>\n'
Hd += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hod-out">&#8211;</span><span class="result-unit">simplified deduction</span></div>\n'
Hd += '  <div class="stats">\n'
Hd += '    <div class="stat"><b id="hod-s1">&#8211;</b><span>actual method estimate</span></div>\n'
Hd += '    <div class="stat"><b id="hod-s2">&#8211;</b><span>the better method</span></div>\n'
Hd += '    <div class="stat"><b id="hod-s3">&#8211;</b><span>cap status</span></div>\n'
Hd += '  </div>\n'
Hd += '  <div class="tool-note" id="hod-note"></div>\n'
Hd += '  <button type="button" class="tool-btn" id="hod-share">Share my office math</button>\n'
Hd += '</div>\n'
Hd += '<script>(function(){\n'
Hd += "var S=document.getElementById('hod-s'),R=document.getElementById('hod-r');\n"
Hd += "function calc(){\n"
Hd += "  var s=parseFloat(S.value)||0,rent=parseFloat(R.value)||0;\n"
Hd += "  var simp=Math.min(s,300)*5, pct=s>0?Math.min(100,s/900*100):0, actual=rent*12*(pct/100);\n"
Hd += "  var d1=Math.round(actual);\n"
Hd += "  var better=simp>=actual?'Simplified':'Actual expenses';\n"
Hd += "  var capped=s>300?'capped at 300 sq ft':'under the cap';\n"
Hd += "  document.getElementById('hod-out').textContent='$'+Math.round(simp);\n"
Hd += "  document.getElementById('hod-s1').textContent='$'+d1;\n"
Hd += "  document.getElementById('hod-s2').textContent=better;\n"
Hd += "  document.getElementById('hod-s3').textContent=capped;\n"
Hd += "  document.getElementById('hod-note').textContent='The simplified method is 5 dollars per square foot with a 300 square foot ceiling - no receipts, five minutes on the form. The actual method multiplies your real rent, utilities and insurance by the office share of the home, and wins whenever the space is large or the rent is high; it wants receipts and a year of records. Two gates decide everything before the math: the space must be used regularly AND exclusively for work - a desk in the living room fails the exclusive test - and since 2018, W-2 employees working from home cannot claim it at all. This is a self-employed and freelance deduction only.';\n"
Hd += "  document.title='Home office: $'+Math.round(simp)+' simplified - ToolDune';\n"
Hd += "}\n"
Hd += "function save(){try{localStorage.setItem('tt_homeded',JSON.stringify({s:S.value,r:R.value}));}catch(e){}}\n"
Hd += "[S,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Hd += "var pre=false;\n"
Hd += "var qs=new URLSearchParams(location.search);\n"
Hd += "if(qs.get('s')){S.value=qs.get('s');pre=true;}\n"
Hd += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_homeded')||'null');if(m){if(m.s){S.value=m.s;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Hd += "calc();\n"
Hd += "document.getElementById('hod-share').addEventListener('click',function(){\n"
Hd += "  var txt='My home office deducts $'+document.getElementById('hod-out').textContent+' the simple way. Run yours:';\n"
Hd += "  var url=location.origin+location.pathname+'?s='+encodeURIComponent(S.value);\n"
Hd += "  if(navigator.share){navigator.share({title:'Home office deduction',text:txt,url:url}).catch(function(){});}\n"
Hd += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my office math';},1500);}\n"
Hd += "});\n"
Hd += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: SETASIDE ----------
Sa = 'SETASIDE = """<div class="tool" id="tt-sas">\n'
Sa += '  <div class="fields">\n'
Sa += '    <div class="field"><label for="sas-i">Expected 1099 income this year</label><input id="sas-i" type="number" min="400" value="50000"></div>\n'
Sa += '    <div class="field"><label for="sas-b">Your income tax bracket (%)</label><select id="sas-b"><option value="12">12%</option><option value="22" selected>22%</option><option value="24">24%</option><option value="32">32%</option><option value="35">35%</option></select></div>\n'
Sa += '  </div>\n'
Sa += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sas-out">&#8211;</span><span class="result-unit">of each payment to set aside</span></div>\n'
Sa += '  <div class="stats">\n'
Sa += '    <div class="stat"><b id="sas-s1">&#8211;</b><span>self-employment tax</span></div>\n'
Sa += '    <div class="stat"><b id="sas-s2">&#8211;</b><span>quarterly payment, roughly</span></div>\n'
Sa += '    <div class="stat"><b id="sas-s3">&#8211;</b><span>quarter due dates</span></div>\n'
Sa += '  </div>\n'
Sa += '  <div class="tool-note" id="sas-note"></div>\n'
Sa += '  <button type="button" class="tool-btn" id="sas-share">Share my set-aside rate</button>\n'
Sa += '</div>\n'
Sa += '<script>(function(){\n'
Sa += "var I=document.getElementById('sas-i'),B=document.getElementById('sas-b');\n"
Sa += "function calc(){\n"
Sa += "  var inc=parseFloat(I.value)||0,br=parseFloat(B.value)||22;\n"
Sa += "  var se=inc*0.9235*0.153, incTax=inc*br/100, total=se+incTax, pct=inc>0?total/inc*100:0;\n"
Sa += "  var d1=Math.round(se), d2=Math.round(total/4), d3=Math.round(pct);\n"
Sa += "  document.getElementById('sas-out').textContent=d3+'%';\n"
Sa += "  document.getElementById('sas-s1').textContent='$'+d1;\n"
Sa += "  document.getElementById('sas-s2').textContent='$'+d2;\n"
Sa += "  document.getElementById('sas-s3').textContent='Apr Jun Sep Jan';\n"
Sa += "  document.getElementById('sas-note').textContent='Self-employed income pays both halves of Social Security and Medicare - 15.3 percent on 92.35 percent of net profit, the discount acknowledging the employer half you now pay yourself. Stack your income bracket on top and the set-aside lands near the percentage shown; move that slice to a separate account the day each client payment lands. The quarterly dates are April, June, September and January - and the safe-harbor rule is the amateur-to-pro line: pay 100 percent of last year total tax across the quarters and the underpayment penalty cannot touch you, even if this year doubles.';\n"
Sa += "  document.title='Set aside '+d3+'% of 1099 income - ToolDune';\n"
Sa += "}\n"
Sa += "function save(){try{localStorage.setItem('tt_setaside',JSON.stringify({i:I.value,b:B.value}));}catch(e){}}\n"
Sa += "[I,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Sa += "var pre=false;\n"
Sa += "var qs=new URLSearchParams(location.search);\n"
Sa += "if(qs.get('i')){I.value=qs.get('i');pre=true;}\n"
Sa += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_setaside')||'null');if(m){if(m.i){I.value=m.i;}if(m.b){B.value=m.b;}}}catch(e){}}\n"
Sa += "calc();\n"
Sa += "document.getElementById('sas-share').addEventListener('click',function(){\n"
Sa += "  var txt='Freelancers should set aside about '+document.getElementById('sas-out').textContent+' of each payment. Run yours:';\n"
Sa += "  var url=location.origin+location.pathname+'?i='+encodeURIComponent(I.value);\n"
Sa += "  if(navigator.share){navigator.share({title:'Self-employment tax set-aside',text:txt,url:url}).catch(function(){});}\n"
Sa += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my set-aside rate';},1500);}\n"
Sa += "});\n"
Sa += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: CHARMILE ----------
Cm = 'CHARMILE = """<div class="tool" id="tt-chm">\n'
Cm += '  <div class="fields">\n'
Cm += '    <div class="field"><label for="chm-m">Volunteer miles driven this year</label><input id="chm-m" type="number" min="0" value="200"></div>\n'
Cm += '    <div class="field"><label for="chm-p">Parking and tolls paid</label><input id="chm-p" type="number" min="0" value="15"></div>\n'
Cm += '  </div>\n'
Cm += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="chm-out">&#8211;</span><span class="result-unit">charitable mileage deduction</span></div>\n'
Cm += '  <div class="stats">\n'
Cm += '    <div class="stat"><b id="chm-s1">&#8211;</b><span>the statutory rate</span></div>\n'
Cm += '    <div class="stat"><b id="chm-s2">&#8211;</b><span>what does not count</span></div>\n'
Cm += '    <div class="stat"><b id="chm-s3">&#8211;</b><span>the record that survives audit</span></div>\n'
Cm += '  </div>\n'
Cm += '  <div class="tool-note" id="chm-note"></div>\n'
Cm += '  <button type="button" class="tool-btn" id="chm-share">Share my mileage math</button>\n'
Cm += '</div>\n'
Cm += '<script>(function(){\n'
Cm += "var M=document.getElementById('chm-m'),P2=document.getElementById('chm-p');\n"
Cm += "function calc(){\n"
Cm += "  var mi=parseFloat(M.value)||0,pk=parseFloat(P2.value)||0;\n"
Cm += "  var ded=mi*0.14+pk;\n"
Cm += "  var d1=Math.round(ded*100)/100;\n"
Cm += "  document.getElementById('chm-out').textContent='$'+d1;\n"
Cm += "  document.getElementById('chm-s1').textContent='14 cents a mile';\n"
Cm += "  document.getElementById('chm-s2').textContent='your commute';\n"
Cm += "  document.getElementById('chm-s3').textContent='a dated log';\n"
Cm += "  document.getElementById('chm-note').textContent='Volunteer driving deducts at a statutory 14 cents a mile - a rate the IRS has frozen for years while business rates climbed, which is the honest reason this deduction stays modest. Only miles for a qualified 501(c)(3) count, your commute to regular volunteer duty does not, and parking or tolls add on top. The record that survives an audit is boring and unbeatable: a dated log with destination, purpose and miles - written the same week, not reconstructed in April. And itemizers only: like the giving itself, this rides on Schedule A.';\n"
Cm += "  document.title='Charitable miles: $'+d1+' deduction - ToolDune';\n"
Cm += "}\n"
Cm += "function save(){try{localStorage.setItem('tt_charmile',JSON.stringify({m:M.value,p:P2.value}));}catch(e){}}\n"
Cm += "[M,P2].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Cm += "var pre=false;\n"
Cm += "var qs=new URLSearchParams(location.search);\n"
Cm += "if(qs.get('m')){M.value=qs.get('m');pre=true;}\n"
Cm += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_charmile')||'null');if(m){if(m.m){M.value=m.m;}if(m.p){P2.value=m.p;}}}catch(e){}}\n"
Cm += "calc();\n"
Cm += "document.getElementById('chm-share').addEventListener('click',function(){\n"
Cm += "  var txt='My volunteer miles deduct $'+document.getElementById('chm-out').textContent+'. Log yours:';\n"
Cm += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value);\n"
Cm += "  if(navigator.share){navigator.share({title:'Charitable miles',text:txt,url:url}).catch(function(){});}\n"
Cm += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my mileage math';},1500);}\n"
Cm += "});\n"
Cm += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("HOMEDED", "SETASIDE", "CHARMILE"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Hd + Sa + Cm + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "oiltank": lambda args: OILTANK,',
    '    "oiltank": lambda args: OILTANK,\n'
    '    "homeded": lambda args: HOMEDED,\n'
    '    "setaside": lambda args: SETASIDE,\n'
    '    "charmile": lambda args: CHARMILE,')
sub(BUILD_P, '    "minpay": "♾", "mealprep": "🍱", "oiltank": "⛽",',
    '    "minpay": "♾", "mealprep": "🍱", "oiltank": "⛽",\n'
    '    "homeded": "📎", "setaside": "💼", "charmile": "🚶",')

P = []
d = {'slug': 'home-office-deduction-calculator',
     'title': 'Home Office Deduction Calculator - Simplified vs Actual Method',
     'h1': 'Home Office Deduction Calculator',
     'desc': 'Square feet times 5 dollars under the simplified method, compared against your actual expense share - with the exclusive-use gate that decides everything. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'home office deduction calculator simplified method square feet',
     'tool': 'homeded',
     'args': {},
     'intro': ["Enter the office square footage and your monthly housing cost. The calculator runs the simplified method - 5 dollars per square foot, capped at 300 - and estimates what the actual-expense method would claim from your rent share, naming the better route.",
              "Two gates decide this deduction before any math: the space must be regular AND exclusive work use - a desk in the living room fails - and since 2018, W-2 employees working from home cannot claim it at all. This is a self-employed and freelance deduction, and the calculator says so up front instead of after the audit letter."],
     'howto': ["Measure the dedicated workspace - the part that is truly office.",
               "Enter monthly rent or housing cost for the actual-method estimate.",
               "Compare both methods; keep receipts only if actual wins."],
     'faqs': [("How does the simplified home office deduction work?",
               "Five dollars per square foot of dedicated office space, capped at 300 square feet - up to 1,500 dollars, no receipts required. The calculator runs it against your actual expense share so the choice is a number, not a guess."),
              ("Can I claim a home office as a W-2 employee?",
               "No - the 2017 tax reform suspended unreimbursed employee expenses. The deduction lives on for the self-employed, freelancers and side businesses; employees get nothing even with a perfect home office."),
              ("What does exclusive use actually mean?",
               "The space works only as an office: a spare room with a desk passes, the kitchen table you clear at dinner fails, and a guest room with a treadmill corner fails the strict version. It is the gate audits test first."),
              ("Is the simplified or actual method better?",
               "Simplified wins for small spaces and modest rents; actual wins when the office share of real rent, utilities and insurance exceeds 5 dollars a foot - which happens fast above 200 square feet in high-rent cities. The calculator prices both.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'self-employment-tax-set-aside-calculator',
     'title': 'Self-Employment Tax Calculator - Your 1099 Set-Aside Percentage',
     'h1': 'Self-Employment Tax Set-Aside Calculator',
     'desc': 'Expected 1099 income plus your bracket gives the set-aside percentage, the SE tax, quarterly payments and the safe-harbor rule that ends penalty fear. Free.',
     'category': 'calculator',
     'keyword': 'self employment tax calculator set aside percentage 1099',
     'tool': 'setaside',
     'args': {},
     'intro': ["Enter your expected 1099 income and tax bracket. The calculator stacks self-employment tax - 15.3 percent on 92.35 percent of net profit - with income tax, and hands back the percentage of every payment to set aside.",
              "New freelancers discover the SE tax the expensive way: self-employed income pays both halves of Social Security and Medicare. This calculator prices the full stack into a per-payment percentage, lists the quarterly dates, and explains the safe-harbor rule that makes underpayment penalties structurally impossible."],
     'howto': ["Estimate the year 1099 income from contracts or last year.",
               "Pick your marginal bracket for the income-tax layer.",
               "Move the shown slice to a separate account per client payment."],
     'faqs': [("How much should I set aside for self-employment taxes?",
               "Plan on 25-35 percent of net income: the 15.3 percent SE tax plus your income bracket. The calculator prices your exact stack - the separate-account habit is what makes the number stick."),
              ("What is the self-employment tax rate?",
               "15.3 percent - both halves of Social Security and Medicare - applied to 92.35 percent of net profit. The discount acknowledges that employees split the bill with an employer, and the self-employed pay both halves."),
              ("When are quarterly estimated taxes due?",
               "April 15, June 15, September 15 and January 15 of the following year - the quarters do not match calendar quarters, and June is the one that sneaks up on everyone."),
              ("What is the safe harbor rule for estimated taxes?",
               "Pay 100 percent of last year total tax across the quarters - 110 percent for higher incomes - and no underpayment penalty applies no matter what you owe this year. It converts a volatile income into a predictable payment plan.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'charitable-miles-calculator',
     'title': 'Charitable Miles Calculator - Volunteer Driving Deduction at 14 Cents',
     'h1': 'Charitable Miles Calculator',
     'desc': 'Volunteer miles at the statutory 14 cents plus parking and tolls - with the 501(c)(3) rule, the commute exclusion and the log that survives audit. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'charitable mileage rate calculator volunteer miles deduction',
     'tool': 'charmile',
     'args': {},
     'intro': ["Enter the miles you drove for charity and any parking or tolls. The calculator applies the statutory volunteer rate - 14 cents a mile, a figure the IRS has frozen for years - and adds your out-of-pocket costs.",
              "The honest framing: this deduction is modest, rides on itemizing like all charitable giving, and only counts for qualified 501(c)(3) organizations. Your commute to a regular volunteer shift does not count; the dated log written the same week is what survives an audit."],
     'howto': ["Tally the year volunteer driving from your calendar or log.",
               "Add parking and tolls paid while volunteering.",
               "Keep the log current - reconstructed mileage is the audit classic."],
     'faqs': [("What is the IRS mileage rate for charity work?",
               "14 cents per mile - fixed by statute for years while business rates float upward annually. It is deliberately modest; the deduction also requires itemizing, like the rest of charitable giving."),
              ("Does driving to volunteer count?",
               "Miles driven in service of the charity count - delivering meals, hauling supplies. Your ordinary commute to a regular volunteer location does not, and neither does any route with a personal detour priced in."),
              ("What records do I need for charitable miles?",
               "A dated written log: date, destination, purpose, miles. Reconstructed logs are the classic audit failure; a note on your phone the same week converts to a defensible record at tax time."),
              ("Can I deduct volunteer out-of-pocket costs?",
               "Yes - parking, tolls and unbought supplies for the charity add on top of mileage. Uniform costs count too; the value of your time famously never does.")]}
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
print("R164 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
