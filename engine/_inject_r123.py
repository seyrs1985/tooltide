# -*- coding: utf-8 -*-
"""R123 秋令时睡眠规划:dst-sleep-shift-planner(US 11月第一个周日 / EU 10月最后一个周日)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

D = 'DSTPLAN = """<div class="tool" id="tt-dst">\n'
D += '  <div class="fields">\n'
D += '    <div class="field"><label for="dst-r">Region</label><select id="dst-r"><option value="US" selected>US / Canada - Nov 1</option><option value="EU">Europe - Oct 25</option></select></div>\n'
D += '    <div class="field"><label for="dst-p">Shift pace per day</label><select id="dst-p"><option value="10">10 min - gentle</option><option value="15" selected>15 min - standard</option><option value="20">20 min - brisk</option></select></div>\n'
D += '  </div>\n'
D += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dst-out">&#8211;</span><span class="result-unit">clocks fall back</span></div>\n'
D += '  <div class="stats">\n'
D += '    <div class="stat"><b id="dst-s1">&#8211;</b><span>start shifting on</span></div>\n'
D += '    <div class="stat"><b id="dst-s2">&#8211;</b><span>days from today</span></div>\n'
D += '    <div class="stat"><b id="dst-s3">&#8211;</b><span>bedtime shift daily</span></div>\n'
D += '  </div>\n'
D += '  <div class="tool-note" id="dst-note"></div>\n'
D += '  <button type="button" class="tool-btn" id="dst-share">Share my shift plan</button>\n'
D += '</div>\n'
D += '<script>(function(){\n'
D += "var R=document.getElementById('dst-r'),P=document.getElementById('dst-p');\n"
D += "function changeDate(y,region){var d;\n"
D += "  if(region==='US'){d=new Date(Date.UTC(y,10,1));d=new Date(d.getTime()+((7-d.getUTCDay())%7)*86400000);}\n"
D += "  else{d=new Date(Date.UTC(y,9,31));d=new Date(d.getTime()-d.getUTCDay()*86400000);}\n"
D += "  return d;}\n"
D += "function calc(){\n"
D += "  var region=R.value,pace=parseInt(P.value,10),now=new Date(),y=now.getUTCFullYear();\n"
D += "  var cd=changeDate(y,region);\n"
D += "  if(cd.getTime()<now.getTime()){cd=changeDate(y+1,region);}\n"
D += "  var days=Math.ceil((cd.getTime()-new Date(Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate())).getTime())/86400000);\n"
D += "  var shiftDays=Math.ceil(60/pace);\n"
D += "  var st=new Date(cd.getTime()-shiftDays*86400000);\n"
D += "  var names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];\n"
D += "  var cs=names[cd.getUTCMonth()]+' '+cd.getUTCDate()+', '+cd.getUTCFullYear();\n"
D += "  var ss=names[st.getUTCMonth()]+' '+st.getUTCDate();\n"
D += "  document.getElementById('dst-out').textContent=cs;\n"
D += "  document.getElementById('dst-s1').textContent=ss;\n"
D += "  document.getElementById('dst-s2').textContent=days;\n"
D += "  document.getElementById('dst-s3').textContent='+'+pace+' min';\n"
D += "  document.getElementById('dst-note').textContent='Falling back gives the hour back, but bodies still drift: the plan is to move bedtime and wake time '+pace+' minutes later each day for '+shiftDays+' days, so Sunday morning lands on schedule instead of in the dark. Phones update themselves; the microwave, the car clock and the toaster do not. The week hurts most for small kids, pets on a feeding clock and anyone commuting at dawn - start them on the plan, and take the spare hour Sunday morning as a gift, not a mandate.';\n"
D += "  document.title='Fall back '+cs+' - ToolDune';\n"
D += "}\n"
D += "function save(){try{localStorage.setItem('tt_dst',JSON.stringify({r:R.value,p:P.value}));}catch(e){}}\n"
D += "R.addEventListener('change',function(){calc();save();});P.addEventListener('change',function(){calc();save();});\n"
D += "var pre=false;\n"
D += "var qs=new URLSearchParams(location.search);\n"
D += "if(qs.get('r')){R.value=qs.get('r');pre=true;}\n"
D += "if(qs.get('p')){P.value=qs.get('p');pre=true;}\n"
D += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_dst')||'null');if(m){if(m.r){R.value=m.r;}if(m.p){P.value=m.p;}pre=true;}}catch(e){}}\n"
D += "calc();\n"
D += "document.getElementById('dst-share').addEventListener('click',function(){\n"
D += "  var txt='Clocks fall back '+document.getElementById('dst-out').textContent+' - start shifting bedtime '+P.value+' min later on '+document.getElementById('dst-s1').textContent+'. Plan yours:';\n"
D += "  var url=location.origin+location.pathname+'?r='+encodeURIComponent(R.value)+'&p='+encodeURIComponent(P.value);\n"
D += "  if(navigator.share){navigator.share({title:'Daylight saving sleep plan',text:txt,url:url}).catch(function(){});}\n"
D += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my shift plan';},1500);}\n"
D += "});\n"
D += "})();\n</script>\n\"\"\"\n\n"

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

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', D + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "seedroast": lambda args: SEEDSROAST,',
    '    "seedroast": lambda args: SEEDSROAST,\n'
    '    "dstsleep": lambda args: DSTPLAN,')
sub(BUILD_P, '    "pumpkinpie": "🎃", "carvetiming": "🍂", "seedroast": "🌰",',
    '    "pumpkinpie": "🎃", "carvetiming": "🍂", "seedroast": "🌰",\n'
    '    "dstsleep": "⏰",')

P = []
d = {'slug': 'dst-sleep-shift-planner',
     'title': 'Daylight Saving Sleep Planner - When Clocks Fall Back and How to Shift',
     'h1': 'Daylight Saving Sleep Planner',
     'desc': 'Pick your region to see the exact fall-back date, then get a gentle bedtime shift plan - 10 to 20 minutes a day - so the time change lands without wrecking your week.',
     'category': 'calculator',
     'keyword': 'daylight saving time change fall back sleep schedule when do clocks go back',
     'tool': 'dstsleep',
     'args': {},
     'intro': ["Pick your region - the US and Canada fall back on the first Sunday of November, Europe on the last Sunday of October - and this planner shows the exact date, how far out it sits, and a bedtime shift schedule that moves your schedule 10 to 20 minutes a day so Sunday morning lands on purpose instead of in the dark.",
              "The hour itself is not the problem; the drift is. Phones update themselves, the microwave does not, and small kids, pets and dawn commuters feel the change for days. The plan here is the standard pediatric-sleep approach scaled to your pace - and it ends with permission to take the spare hour as a gift."],
     'howto': ["Pick your region so the correct fall-back date is used.",
               "Choose a pace you will actually keep - 15 minutes a day is the standard.",
               "Start bedtime shifts on the date shown, and take Sunday hour as recovery."],
     'faqs': [("When do clocks fall back in 2026?", "The US and Canada fall back on Sunday, November 1, 2026; most of Europe falls back on Sunday, October 25, 2026 - three weeks apart, which is why the region selector matters for travel plans."),
               ("How do I prepare my body for the time change?", "Move bedtime and wake time about 15 minutes later each day for the four nights before the change, keep morning light bright and evenings dim, and let Sunday morning absorb the spare hour."),
               ("Why does falling back feel easier than springing forward?", "You gain an hour instead of losing one, so the main cost is earlier darkness in the evening - but kids and pets still wake on clock time, which is why the gradual shift plan helps both directions."),
               ("Do phones update for daylight saving time automatically?", "Phones, laptops and most smart clocks do; ovens, microwaves, car dashboards and older thermostats do not - the planner note is to check the dumb clocks on the day.")]}
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
print("R123 inject OK: 1 renderer + 1 page + 1 emoji, ast passed")
