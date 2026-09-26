# -*- coding: utf-8 -*-
"""R132 医保开放注册季三页:hdhp-vs-ppo(总成本+盈亏平衡)+fsa-calculator(节税+用完作废)+hsa-contribution-calculator(2026限额+三重免税)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: HDHP ----------
Hd = 'HDHP = """<div class="tool" id="tt-hdhp">\n'
Hd += '  <div class="fields">\n'
Hd += '    <div class="field"><label for="hp-ph">HDHP premium (your share per year)</label><input id="hp-ph" type="number" min="0" value="1800"></div>\n'
Hd += '    <div class="field"><label for="hp-pp">PPO premium (your share per year)</label><input id="hp-pp" type="number" min="0" value="4800"></div>\n'
Hd += '    <div class="field"><label for="hp-dh">HDHP deductible</label><input id="hp-dh" type="number" min="0" value="3200"></div>\n'
Hd += '    <div class="field"><label for="hp-dp">PPO deductible</label><input id="hp-dp" type="number" min="0" value="1500"></div>\n'
Hd += '    <div class="field"><label for="hp-cost">Expected medical costs this year</label><input id="hp-cost" type="number" min="0" value="1200"></div>\n'
Hd += '    <div class="field"><label for="hp-seed">Employer HSA seed</label><input id="hp-seed" type="number" min="0" value="500"></div>\n'
Hd += '  </div>\n'
Hd += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hp-out">&#8211;</span><span class="result-unit">cheaper plan this year</span></div>\n'
Hd += '  <div class="stats">\n'
Hd += '    <div class="stat"><b id="hp-s1">&#8211;</b><span>HDHP all-in</span></div>\n'
Hd += '    <div class="stat"><b id="hp-s2">&#8211;</b><span>PPO all-in</span></div>\n'
Hd += '    <div class="stat"><b id="hp-s3">&#8211;</b><span>PPO wins above</span></div>\n'
Hd += '  </div>\n'
Hd += '  <div class="tool-note" id="hp-note"></div>\n'
Hd += '  <button type="button" class="tool-btn" id="hp-share">Share my plan verdict</button>\n'
Hd += '</div>\n'
Hd += '<script>(function(){\n'
Hd += "var PH=document.getElementById('hp-ph'),PP=document.getElementById('hp-pp'),DH=document.getElementById('hp-dh'),DP=document.getElementById('hp-dp'),C=document.getElementById('hp-cost'),SEED=document.getElementById('hp-seed');\n"
Hd += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Hd += "function calc(){\n"
Hd += "  var ph=num(PH),pp=num(PP),dh=num(DH),dp=num(DP),cost=num(C),seed=num(SEED);\n"
Hd += "  var th=ph+Math.min(cost,dh),tp=pp+Math.min(cost,dp)-seed;\n"
Hd += "  var d1=Math.round(th*10)/10,d2=Math.round(tp*10)/10,diff=Math.round(Math.abs(th-tp)*10)/10;\n"
Hd += "  var x=pp-ph+dh-dp+seed;\n"
Hd += "  var xr=Math.round(x*10)/10;\n"
Hd += "  var inRange=x>Math.max(dh,dp);\n"
Hd += "  if(th<=tp){\n"
Hd += "    document.getElementById('hp-out').textContent='HDHP by $'+diff;\n"
Hd += "  }else{\n"
Hd += "    document.getElementById('hp-out').textContent='PPO by $'+diff;\n"
Hd += "  }\n"
Hd += "  document.getElementById('hp-s1').textContent='$'+d1;\n"
Hd += "  document.getElementById('hp-s2').textContent='$'+d2;\n"
Hd += "  document.getElementById('hp-s3').textContent=inRange?('about $'+xr+' of care'):'no crossover this year';\n"
Hd += "  var msg='The model compares premiums plus costs up to each deductible, minus the employer seed - coinsurance and copays past the deductible are deliberately out, so plug a bigger expected-cost number to feel out a bad year. ';\n"
Hd += "  if(inRange){msg+='Below about $'+xr+' of expected care the HDHP comes out ahead; above it the PPO takes over. Healthy year, the HDHP wins; a surgery or a baby on the calendar tips the math hard.';}\n"
Hd += "  else{msg+='With your premiums and deductibles the same plan wins across the realistic range - the crossover point sits outside it, so the decision rides on the premiums alone.';}\n"
Hd += "  msg+=' The seed is free money either way: whatever the employer contributes, take it.';\n"
Hd += "  document.getElementById('hp-note').textContent=msg;\n"
Hd += "  document.title=(th<=tp?'HDHP':'PPO')+' saves $'+diff+' this year - ToolDune';\n"
Hd += "}\n"
Hd += "function save(){try{localStorage.setItem('tt_hdhp',JSON.stringify({ph:PH.value,pp:PP.value,dh:DH.value,dp:DP.value,c:C.value,s:SEED.value}));}catch(e){}}\n"
Hd += "[PH,PP,DH,DP,C,SEED].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Hd += "var pre=false;\n"
Hd += "var qs=new URLSearchParams(location.search);\n"
Hd += "if(qs.get('c')){C.value=qs.get('c');pre=true;}\n"
Hd += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_hdhp')||'null');if(m){if(m.ph){PH.value=m.ph;}if(m.pp){PP.value=m.pp;}if(m.dh){DH.value=m.dh;}if(m.dp){DP.value=m.dp;}if(m.c){C.value=m.c;}if(m.s){SEED.value=m.s;}}}catch(e){}}\n"
Hd += "calc();\n"
Hd += "document.getElementById('hp-share').addEventListener('click',function(){\n"
Hd += "  var txt='Running my numbers, '+document.getElementById('hp-out').textContent+' this year. Compare your plans:';\n"
Hd += "  var url=location.origin+location.pathname+'?c='+encodeURIComponent(C.value);\n"
Hd += "  if(navigator.share){navigator.share({title:'HDHP vs PPO verdict',text:txt,url:url}).catch(function(){});}\n"
Hd += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my plan verdict';},1500);}\n"
Hd += "});\n"
Hd += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: FSAP ----------
Fs = 'FSAP = """<div class="tool" id="tt-fsa">\n'
Fs += '  <div class="fields">\n'
Fs += '    <div class="field"><label for="fs-c">Annual contribution</label><input id="fs-c" type="number" min="0" max="3400" value="2600"></div>\n'
Fs += '    <div class="field"><label for="fs-r">Marginal tax rate (%)</label><select id="fs-r"><option value="12">12%</option><option value="22" selected>22%</option><option value="24">24%</option><option value="32">32%</option><option value="35">35%</option></select></div>\n'
Fs += '    <div class="field"><label for="fs-n">Paychecks per year</label><select id="fs-n"><option value="12">12 - monthly</option><option value="24" selected>24 - twice a month</option><option value="26">26 - every two weeks</option></select></div>\n'
Fs += '    <div class="field"><label for="fs-e">Planned eligible expenses</label><input id="fs-e" type="number" min="0" value="2400"></div>\n'
Fs += '  </div>\n'
Fs += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fs-out">&#8211;</span><span class="result-unit">real tax saved</span></div>\n'
Fs += '  <div class="stats">\n'
Fs += '    <div class="stat"><b id="fs-s1">&#8211;</b><span>per paycheck</span></div>\n'
Fs += '    <div class="stat"><b id="fs-s2">&#8211;</b><span>use-or-lose risk</span></div>\n'
Fs += '    <div class="stat"><b id="fs-s3">&#8211;</b><span>tax rate that applies</span></div>\n'
Fs += '  </div>\n'
Fs += '  <div class="tool-note" id="fs-note"></div>\n'
Fs += '  <button type="button" class="tool-btn" id="fs-share">Share my FSA math</button>\n'
Fs += '</div>\n'
Fs += '<script>(function(){\n'
Fs += "var CI=document.getElementById('fs-c'),R=document.getElementById('fs-r'),N=document.getElementById('fs-n'),E=document.getElementById('fs-e');\n"
Fs += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Fs += "function calc(){\n"
Fs += "  var c=num(CI),r=num(R)/100,n=parseInt(N.value,10)||24,e=num(E);\n"
Fs += "  var eff=r+0.0765, saved=c*eff, per=c/n, risk=Math.max(0,c-e);\n"
Fs += "  var d1=Math.round(saved*10)/10,d2=Math.round(per*100)/100,d3=Math.round(risk*10)/10;\n"
Fs += "  document.getElementById('fs-out').textContent='$'+d1;\n"
Fs += "  document.getElementById('fs-s1').textContent='$'+d2;\n"
Fs += "  document.getElementById('fs-s2').textContent='$'+d3;\n"
Fs += "  document.getElementById('fs-s3').textContent=Math.round(eff*1000)/10+'%';\n"
Fs += "  var msg='The saving stacks your income-tax bracket with the 7.65% payroll tax, because FSA money never touches either. Use-or-lose is the catch: money left over forfeits at year end, softened by a 2.5 month grace period or a carryover up to about $660 - your plan allows one or the other, rarely both. ';\n"
Fs += "  if(risk>0){msg+='At your numbers about $'+d3+' is at risk. Cover the predictable stuff - glasses, dentist, prescriptions, therapy copays - and hold back the rest; an FSA underfunded by a few hundred is a better deal than one forfeiting a few hundred.';}\n"
Fs += "  else{msg+='You are planning to spend it all - this is the FSA done right. Keep receipts anyway; debit-card audits do happen.';}\n"
Fs += "  msg+=' The 2026 contribution ceiling is $3,400, but your employer may cap lower.';\n"
Fs += "  document.getElementById('fs-note').textContent=msg;\n"
Fs += "  document.title='FSA saves $'+d1+' in taxes - ToolDune';\n"
Fs += "}\n"
Fs += "function save(){try{localStorage.setItem('tt_fsa',JSON.stringify({c:CI.value,r:R.value,n:N.value,e:E.value}));}catch(e){}}\n"
Fs += "[CI,R,N,E].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Fs += "var pre=false;\n"
Fs += "var qs=new URLSearchParams(location.search);\n"
Fs += "if(qs.get('c')){CI.value=qs.get('c');pre=true;}\n"
Fs += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_fsa')||'null');if(m){if(m.c){CI.value=m.c;}if(m.r){R.value=m.r;}if(m.n){N.value=m.n;}if(m.e){E.value=m.e;}}}catch(e){}}\n"
Fs += "calc();\n"
Fs += "document.getElementById('fs-share').addEventListener('click',function(){\n"
Fs += "  var txt='My FSA election saves $'+document.getElementById('fs-out').textContent+' in real taxes. Run yours:';\n"
Fs += "  var url=location.origin+location.pathname+'?c='+encodeURIComponent(CI.value);\n"
Fs += "  if(navigator.share){navigator.share({title:'FSA math',text:txt,url:url}).catch(function(){});}\n"
Fs += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my FSA math';},1500);}\n"
Fs += "});\n"
Fs += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: HSAC ----------
Hs = 'HSAC = """<div class="tool" id="tt-hsa">\n'
Hs += '  <div class="fields">\n'
Hs += '    <div class="field"><label for="hs-cov">Coverage</label><select id="hs-cov"><option value="4400" selected>Self only - $4,400</option><option value="8750">Family - $8,750</option></select></div>\n'
Hs += '    <div class="field"><label for="hs-age">Age</label><input id="hs-age" type="number" min="0" max="100" value="40"></div>\n'
Hs += '    <div class="field"><label for="hs-mine">Your contribution</label><input id="hs-mine" type="number" min="0" value="3000"></div>\n'
Hs += '    <div class="field"><label for="hs-r">Marginal tax rate (%)</label><select id="hs-r"><option value="12">12%</option><option value="22" selected>22%</option><option value="24">24%</option><option value="32">32%</option><option value="35">35%</option></select></div>\n'
Hs += '  </div>\n'
Hs += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hs-out">&#8211;</span><span class="result-unit">tax saved this year</span></div>\n'
Hs += '  <div class="stats">\n'
Hs += '    <div class="stat"><b id="hs-s1">&#8211;</b><span>contribution room</span></div>\n'
Hs += '    <div class="stat"><b id="hs-s2">&#8211;</b><span>over the cap by</span></div>\n'
Hs += '    <div class="stat"><b id="hs-s3">&#8211;</b><span>with payroll tax skipped</span></div>\n'
Hs += '  </div>\n'
Hs += '  <div class="tool-note" id="hs-note"></div>\n'
Hs += '  <button type="button" class="tool-btn" id="hs-share">Share my HSA math</button>\n'
Hs += '</div>\n'
Hs += '<script>(function(){\n'
Hs += "var COV=document.getElementById('hs-cov'),AGE=document.getElementById('hs-age'),MINE=document.getElementById('hs-mine'),R=document.getElementById('hs-r');\n"
Hs += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Hs += "function calc(){\n"
Hs += "  var base=parseFloat(COV.value)||4400,age=num(AGE),mine=num(MINE),r=num(R)/100;\n"
Hs += "  var cap=base+(age>=55?1000:0),over=Math.max(0,mine-cap),saved=mine*r,saved2=mine*(r+0.0765);\n"
Hs += "  var d1=Math.round(saved*10)/10,d2=Math.round(saved2*10)/10,ov=Math.round(over*10)/10;\n"
Hs += "  document.getElementById('hs-out').textContent='$'+d2;\n"
Hs += "  document.getElementById('hs-s1').textContent='$'+cap;\n"
Hs += "  document.getElementById('hs-s2').textContent=over>0?('$'+ov):'$0';\n"
Hs += "  document.getElementById('hs-s3').textContent='$'+d2;\n"
Hs += "  var msg='The HSA is the only triple-tax-free account in the code: money goes in untaxed, grows untaxed, and comes out untaxed for medical care at any age - after 65 it behaves like a traditional IRA for anything else. ';\n"
Hs += "  if(over>0){msg+='You are $'+ov+' over the 2026 cap - over-contributions earn a 6% excise tax every year they sit there; pull the excess or spread it. ';}\n"
Hs += "  else{msg+='You have room left: the cap is $'+cap+' with your age and coverage, and every dollar you do not use rolls over forever - it is yours, not the plans. ';}\n"
Hs += "  msg+='Contribute through payroll if you can: it also skips the 7.65% payroll tax, which is the figure shown. Invest the balance once the cash cushion covers a deductible - that is where the compounding lives.';\n"
Hs += "  document.getElementById('hs-note').textContent=msg;\n"
Hs += "  document.title='HSA: $'+d2+' tax saved this year - ToolDune';\n"
Hs += "}\n"
Hs += "function save(){try{localStorage.setItem('tt_hsa',JSON.stringify({v:COV.value,a:AGE.value,m:MINE.value,r:R.value}));}catch(e){}}\n"
Hs += "[COV,AGE,MINE,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Hs += "var pre=false;\n"
Hs += "var qs=new URLSearchParams(location.search);\n"
Hs += "if(qs.get('m')){MINE.value=qs.get('m');pre=true;}\n"
Hs += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_hsa')||'null');if(m){if(m.v){COV.value=m.v;}if(m.a){AGE.value=m.a;}if(m.m){MINE.value=m.m;}if(m.r){R.value=m.r;}}}catch(e){}}\n"
Hs += "calc();\n"
Hs += "document.getElementById('hs-share').addEventListener('click',function(){\n"
Hs += "  var txt='My HSA contribution saves $'+document.getElementById('hs-out').textContent+' this year. Run yours:';\n"
Fs_dummy = None
Hs += "  var url=location.origin+location.pathname+'?m='+encodeURIComponent(MINE.value);\n"
Hs += "  if(navigator.share){navigator.share({title:'HSA math',text:txt,url:url}).catch(function(){});}\n"
Hs += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my HSA math';},1500);}\n"
Hs += "});\n"
Hs += "})();\n</script>\n\"\"\"\n\n"

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

for tok in ("HDHP ", "FSAP ", "HSAC "):
    src = io.open(TOOLS_P, encoding="utf-8").read()
    name = tok.strip()
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Hd + Fs + Hs + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "heatcmp": lambda args: HEATCMP,',
    '    "heatcmp": lambda args: HEATCMP,\n'
    '    "hdhp": lambda args: HDHP,\n'
    '    "fsa": lambda args: FSAP,\n'
    '    "hsa": lambda args: HSAC,')
sub(BUILD_P, '    "upsruntime": "🔋", "genfuel": "⛽", "heatcmp": "🔥",',
    '    "upsruntime": "🔋", "genfuel": "⛽", "heatcmp": "🔥",\n'
    '    "hdhp": "🏥", "fsa": "💵", "hsa": "💰",')

P = []
d = {'slug': 'hdhp-vs-ppo',
     'title': 'HDHP vs PPO Calculator - Which Health Plan Wins on Total Cost',
     'h1': 'HDHP vs PPO Calculator',
     'desc': 'Premiums, deductibles, expected care and the employer HSA seed become one verdict: which plan wins this year and where the crossover sits. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'hdhp vs ppo which is better calculator',
     'tool': 'hdhp',
     'args': {},
     'intro': ["Pull both plans from your open-enrollment packet - your premium share, each deductible, what the employer seeds into the HSA - and take a straight guess at what this year of care costs you. The calculator totals each plan and shows the crossover point where the PPO takes over.",
              "Plan-comparison charts stop at the premium difference and quietly bury the deductible gap. The honest model here is premiums plus costs up to each deductible minus free employer money - and it says plainly: a healthy year favors the HDHP, a planned surgery or a baby tips it hard, and the seed is yours to claim either way."],
     'howto': ["Copy each plan premium from the enrollment packet - your share, not the employer total.",
               "Enter both deductibles and the employer HSA seed if the HDHP carries one.",
               "Estimate expected care honestly - routine prescriptions and a dental visit, or a known procedure."],
     'faqs': [("When does the HDHP beat the PPO?",
               "When premiums plus your expected costs stay under what the PPO would charge - typically for households with light, predictable care. The crossover in the calculator is the exact care level where the verdict flips at your numbers."),
              ("Do HDHPs cover anything before the deductible?",
               "Yes - since 2020, preventive care including annual physicals, vaccinations and certain screenings is covered before the deductible on HSA-qualified plans. Sick care is what waits behind the deductible."),
              ("Is an HSA-qualified HDHP risky if something big happens?",
               "The out-of-pocket maximum caps the damage, and tax-free HSA money - yours plus the employer seed - pays toward it. The bigger risk is cash flow: you need savings to front the deductible and be reimbursed later."),
              ("Can I switch plans every year?",
               "Yes - open enrollment resets annually, and job changes or qualifying life events allow mid-year switches. Re-running this comparison each fall with fresh premiums is the whole game.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'fsa-calculator',
     'title': 'FSA Calculator - Tax Savings, Per-Paycheck Cost and Use-or-Lose Risk',
     'h1': 'FSA Calculator',
     'desc': 'Your FSA election becomes real tax saved at your bracket plus payroll tax, the per-paycheck dent, and exactly how much sits at use-or-lose risk. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'fsa calculator tax savings use or lose',
     'tool': 'fsa',
     'args': {},
     'intro': ["Set your election, your tax bracket, how many paychecks a year you get, and what you realistically plan to spend on eligible care. The calculator shows the true tax saving - income tax plus the 7.65% payroll tax FSA money skips - and the amount riding on use-or-lose.",
              "Employer flyers sell the FSA as free money and skip the forfeit math entirely. This one prices both sides: the bracket-plus-payroll saving stacking in your favor, and the grace-period or carryover rules deciding what happens to whatever is left on December 31."],
     'howto': ["Election first: the 2026 ceiling is $3,400 unless your employer caps lower.",
               "Pick your marginal bracket from your last pay stub - that is the income tax slice.",
               "Enter planned expenses honestly; the risk figure is what forfeits if plans change."],
     'faqs': [("How much does an FSA actually save in taxes?",
               "Your contribution times your bracket plus 7.65% payroll tax - about 29.6% total at the 22% bracket. On a $2,600 election that is roughly $770 that would otherwise have been taxed away."),
              ("What happens to unused FSA money?",
               "Use-or-lose forfeits it at year end, with two softeners - plans offer either a 2.5-month grace period to spend into March, or a carryover of up to $660 into next year. Check which one yours runs; employers pick one."),
              ("What can I spend FSA money on?",
               "Medical, dental, vision, prescriptions, therapy copays, glasses and contacts, braces, band-aids, sunscreen over SPF 15. Gym memberships and general wellness never qualify - the IRS list is narrower than people hope."),
              ("Is an FSA better than an HSA?",
               "They rarely coexist: the FSA is spend-this-year, the HSA is save-forever, and an FSA generally blocks HSA contributions. If your plan is HSA-qualified, the HSA wins for anyone who can leave money untouched; the FSA suits known, recurring care.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'hsa-contribution-calculator',
     'title': 'HSA Contribution Calculator - 2026 Limits, Tax Savings and the Cap',
     'h1': 'HSA Contribution Calculator',
     'desc': 'The 2026 HSA limits by coverage and age, your real tax saving with payroll tax skipped, and a warning the moment you cross the cap. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'hsa contribution calculator 2026 limits',
     'tool': 'hsa',
     'args': {},
     'intro': ["Pick your coverage, enter your age and what you plan to contribute. The calculator shows the 2026 cap - $4,400 self-only, $8,750 family, plus $1,000 catch-up at 55 or older - the tax saving with payroll tax included, and an over-contribution warning before the IRS charges you for it.",
              "Bank pages quote last year and stop there. This one prices the full stack - bracket plus the 7.65% payroll tax that payroll contributions skip - and nags about the 6% excise tax on the overshoot, the part the enrollment emails never mention."],
     'howto': ["Match coverage to your HDHP - self-only or family - and add the catch-up at 55+.",
               "Enter your planned contribution and bracket from your pay stub.",
               "Contribute through payroll when possible; that is what skips the payroll tax too."],
     'faqs': [("What are the 2026 HSA contribution limits?",
               "$4,400 for self-only coverage, $8,750 for family, plus a $1,000 catch-up for anyone 55 or older - the catch-up counts inside your own contribution. Employer seed money shares the same cap."),
              ("What happens if I over-contribute?",
               "The excess earns a 6% excise tax every year it stays, on top of ordinary tax at withdrawal. Fix it by pulling the excess plus earnings before the filing deadline, or by reducing next year cap-room."),
              ("Why do people call the HSA triple tax free?",
               "Contributions skip income tax, growth is untaxed, and withdrawals for qualified medical care are untaxed at any age - no other account stacks all three. After 65 it behaves like a traditional IRA for non-medical spending."),
              ("Should I spend HSA money now or save receipts?",
               "If cash flow allows, pay care costs out of pocket and bank the receipts - the account grows untaxed and qualified withdrawals can be reimbursed decades later. That is the compounding engine most HSA owners never start.")]}
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
print("R132 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
