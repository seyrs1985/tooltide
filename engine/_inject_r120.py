# -*- coding: utf-8 -*-
"""R120 月相簇注入:moon-phase-calculator / full-moon-calendar / birthday-moon
每条替换断言精确计数,防半改。"""
import io, sys

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 共享天文算法 JS(均值朔望月,诚实±1天口径) ----------
MATH = (
    "var SYN=29.530588853,EPO=2451550.1;\n"
    "function jd(d){return d.getTime()/86400000+2440587.5;}\n"
    "function mage(dt){var a=(jd(dt)-EPO)%SYN;if(a<0)a+=SYN;return a;}\n"
    "function mill(a){return Math.round((1-Math.cos(2*Math.PI*a/SYN))/2*1000)/10;}\n"
    "function memoji(a){var i=Math.floor(a/SYN*8+0.5)%8;return ['\\uD83C\\uDF11','\\uD83C\\uDF12','\\uD83C\\uDF13','\\uD83C\\uDF14','\\uD83C\\uDF15','\\uD83C\\uDF16','\\uD83C\\uDF17','\\uD83C\\uDF18'][i];}\n"
    "function mname(a){var i=Math.floor(a/SYN*8+0.5)%8;return ['New Moon','Waxing Crescent','First Quarter','Waxing Gibbous','Full Moon','Waning Gibbous','Last Quarter','Waning Crescent'][i];}\n"
    "function nfull(dt){var a=mage(dt),d=(14.7654-a+SYN)%SYN;if(d<0.3)d+=SYN;return new Date(dt.getTime()+d*86400000);}\n"
    "function nnew(dt){var a=mage(dt),d=(SYN-a)%SYN;if(d<0.3)d+=SYN;return new Date(dt.getTime()+d*86400000);}\n"
    "function pdate(dt){return dt.toUTCString().slice(5,11)+' '+dt.getUTCFullYear();}\n"
    "function iso(dt){return dt.toISOString().slice(0,10);}\n"
)

MOONPHASE = (
    'MOONPHASE = """<div class="tool" id="tt-moon">\n'
    '  <div class="fields">\n'
    '    <div class="field"><label for="moon-d">Date</label><input type="date" id="moon-d"></div>\n'
    '  </div>\n'
    '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="moon-emo">&#x1F311;</span><span class="result-unit" id="moon-name">&#8211;</span></div>\n'
    '  <div class="stats">\n'
    '    <div class="stat"><b id="moon-s1">&#8211;</b><span>illuminated</span></div>\n'
    '    <div class="stat"><b id="moon-s2">&#8211;</b><span>moon age (days)</span></div>\n'
    '    <div class="stat"><b id="moon-s3">&#8211;</b><span>next full moon</span></div>\n'
    '  </div>\n'
    '  <div class="tool-note" id="moon-note"></div>\n'
    '  <button type="button" class="tool-btn" id="moon-share">Share tonight&#8217;s moon</button>\n'
    '</div>\n'
    '<script>(function(){\n'
    + MATH +
    "var D=document.getElementById('moon-d');\n"
    "function calc(){\n"
    "  if(!D.value){return;}\n"
    "  var dt=new Date(D.value+'T12:00:00Z');\n"
    "  if(isNaN(dt.getTime())){return;}\n"
    "  var a=mage(dt),il=mill(a),em=memoji(a),nm=mname(a);\n"
    "  document.getElementById('moon-emo').textContent=em;\n"
    "  document.getElementById('moon-name').textContent=nm;\n"
    "  document.getElementById('moon-s1').textContent=il+'%';\n"
    "  document.getElementById('moon-s2').textContent=Math.round(a*10)/10;\n"
    "  document.getElementById('moon-s3').textContent=pdate(nfull(dt));\n"
    "  document.getElementById('moon-note').textContent='A mean-synodic estimate computed live from a fixed epoch: the 29.5306-day cycle counted from the reference new moon of 6 Jan 2000. It can drift up to about a day from official almanac times because the orbit is elliptical and the Moon speeds up and slows down. Almanac and observatory tables win for minute-precise times; this page wins for any date, instantly, with the math on the table instead of a frozen table of someone else\\u2019s year.';\n"
    "  document.title=em+' '+nm+' ('+il+'% lit) - ToolDune';\n"
    "}\n"
    "function save(){try{localStorage.setItem('tt_moon',D.value);}catch(e){}}\n"
    "D.addEventListener('input',function(){calc();save();});\n"
    "var pre=false;\n"
    "var q=new URLSearchParams(location.search).get('d');\n"
    "if(q){D.value=q;pre=true;}\n"
    "if(!pre){try{var m=localStorage.getItem('tt_moon');if(m){D.value=m;pre=true;}}catch(e){}}\n"
    "if(!pre){D.value=iso(new Date());}\n"
    "calc();\n"
    "document.getElementById('moon-share').addEventListener('click',function(){\n"
    "  var em=document.getElementById('moon-emo').textContent;\n"
    "  var txt='The moon on '+D.value+': '+em+' '+document.getElementById('moon-name').textContent+' ('+document.getElementById('moon-s1').textContent+' lit). Check any date:';\n"
    "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
    "  if(navigator.share){navigator.share({title:'Moon phase',text:txt,url:url}).catch(function(){});}\n"
    "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share tonight\\u2019s moon';},1500);}\n"
    "});\n"
    "})();\n</script>\n\"\"\"\n\n"
)

FULLMOONCAL = (
    'FULLMOONCAL = """<div class="tool" id="tt-fmc">\n'
    '  <div class="fields">\n'
    '    <div class="field"><label for="fmc-y">Year</label><input type="number" id="fmc-y" min="1900" max="2100" step="1"></div>\n'
    '  </div>\n'
    '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fmc-out">&#8211;</span><span class="result-unit">full moons that year</span></div>\n'
    '  <div class="stats">\n'
    '    <div class="stat"><b id="fmc-s1">&#8211;</b><span>first</span></div>\n'
    '    <div class="stat"><b id="fmc-s2">&#8211;</b><span>last</span></div>\n'
    '    <div class="stat"><b id="fmc-s3">&#8211;</b><span>extra moon?</span></div>\n'
    '  </div>\n'
    '  <ol id="fmc-list"></ol>\n'
    '  <div class="tool-note" id="fmc-note"></div>\n'
    '  <button type="button" class="tool-btn" id="fmc-share">Share this year&#8217;s full moons</button>\n'
    '</div>\n'
    '<script>(function(){\n'
    + MATH +
    "var Y=document.getElementById('fmc-y');\n"
    "function calc(){\n"
    "  var y=parseInt(Y.value,10);\n"
    "  if(!(y>=1900&&y<=2100)){return;}\n"
    "  var d0=new Date(Date.UTC(y,0,1)),a=mage(d0),d=(14.7654-a+SYN)%SYN;\n"
    "  if(d<0.3){d+=SYN;}\n"
    "  var t=d0.getTime()+d*86400000,out=[],n=0;\n"
    "  while(new Date(t).getUTCFullYear()===y&&n<14){out.push(new Date(t));t+=SYN*86400000;n++;}\n"
    "  document.getElementById('fmc-out').textContent=out.length;\n"
    "  document.getElementById('fmc-s1').textContent=pdate(out[0]);\n"
    "  document.getElementById('fmc-s2').textContent=pdate(out[out.length-1]);\n"
    "  document.getElementById('fmc-s3').textContent=out.length>12?'yes - blue moon year':'no';\n"
    "  var L=document.getElementById('fmc-list');L.innerHTML='';\n"
    "  out.forEach(function(dt){var li=document.createElement('li');li.textContent=pdate(dt);L.appendChild(li);});\n"
    "  document.getElementById('fmc-note').textContent='Printed almanac tables freeze the year they were printed; this list is computed for any year you type from the same 29.5306-day cycle, so it carries the same about-a-day tolerance - an observatory table wins for minute-precise or eclipse-adjacent dates. Most years get twelve full moons; thirteen when a cycle lands in the first days of January, which is where blue moon years come from.';\n"
    "  document.title='Full Moons '+y+' ('+out.length+') - ToolDune';\n"
    "}\n"
    "function save(){try{localStorage.setItem('tt_fmcy',Y.value);}catch(e){}}\n"
    "Y.addEventListener('input',function(){calc();save();});\n"
    "var pre=false;\n"
    "var q=new URLSearchParams(location.search).get('y');\n"
    "if(q){Y.value=q;pre=true;}\n"
    "if(!pre){try{var m=localStorage.getItem('tt_fmcy');if(m){Y.value=m;pre=true;}}catch(e){}}\n"
    "if(!pre){Y.value=String(new Date().getUTCFullYear());}\n"
    "calc();\n"
    "document.getElementById('fmc-share').addEventListener('click',function(){\n"
    "  var txt='There are '+document.getElementById('fmc-out').textContent+' full moons in '+Y.value+' - first on '+document.getElementById('fmc-s1').textContent+'. Every full moon, any year:';\n"
    "  var url=location.origin+location.pathname+'?y='+encodeURIComponent(Y.value);\n"
    "  if(navigator.share){navigator.share({title:'Full moon calendar',text:txt,url:url}).catch(function(){});}\n"
    "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share this year\\u2019s full moons';},1500);}\n"
    "});\n"
    "})();\n</script>\n\"\"\"\n\n"
)

BDAYMOON = (
    'BDAYMOON = """<div class="tool" id="tt-bm">\n'
    '  <div class="fields">\n'
    '    <div class="field"><label for="bmoon-d">Your birth date</label><input type="date" id="bmoon-d"></div>\n'
    '  </div>\n'
    '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bmoon-emo">&#x1F311;</span><span class="result-unit" id="bmoon-name">&#8211;</span></div>\n'
    '  <div class="stats">\n'
    '    <div class="stat"><b id="bmoon-s1">&#8211;</b><span>illuminated that day</span></div>\n'
    '    <div class="stat"><b id="bmoon-s2">&#8211;</b><span>moon age (days)</span></div>\n'
    '    <div class="stat"><b id="bmoon-s3">&#8211;</b><span>next full moon after</span></div>\n'
    '  </div>\n'
    '  <div class="tool-note" id="bmoon-note"></div>\n'
    '  <button type="button" class="tool-btn" id="bmoon-share">Share my birthday moon</button>\n'
    '</div>\n'
    '<script>(function(){\n'
    + MATH +
    "var D=document.getElementById('bmoon-d');\n"
    "function calc(){\n"
    "  if(!D.value){return;}\n"
    "  var dt=new Date(D.value+'T12:00:00Z');\n"
    "  if(isNaN(dt.getTime())){return;}\n"
    "  var a=mage(dt),il=mill(a),em=memoji(a),nm=mname(a);\n"
    "  document.getElementById('bmoon-emo').textContent=em;\n"
    "  document.getElementById('bmoon-name').textContent='Born under a '+nm+' moon';\n"
    "  document.getElementById('bmoon-s1').textContent=il+'%';\n"
    "  document.getElementById('bmoon-s2').textContent=Math.round(a*10)/10;\n"
    "  document.getElementById('bmoon-s3').textContent=pdate(nfull(dt));\n"
    "  document.getElementById('bmoon-note').textContent='The moon you were born under depends only on the date, not your birth time or location - everyone born that day shares the phase, within about a day of tolerance from the mean-synodic estimate (same 29.5306-day cycle counted from the reference new moon of 6 Jan 2000). Roughly one person in eight shares your lunar emoji, which is exactly the group-chat fact the share button is for.';\n"
    "  document.title='Born under '+em+' - ToolDune';\n"
    "}\n"
    "function save(){try{localStorage.setItem('tt_bday',D.value);}catch(e){}}\n"
    "D.addEventListener('input',function(){calc();save();});\n"
    "var pre=false;\n"
    "var q=new URLSearchParams(location.search).get('d');\n"
    "if(q){D.value=q;pre=true;}\n"
    "if(!pre){try{var m=localStorage.getItem('tt_bday');if(m){D.value=m;pre=true;}}catch(e){}}\n"
    "calc();\n"
    "document.getElementById('bmoon-share').addEventListener('click',function(){\n"
    "  if(!D.value){return;}\n"
    "  var em=document.getElementById('bmoon-emo').textContent;\n"
    "  var txt='I was born under '+em+' '+document.getElementById('bmoon-name').textContent.replace('Born under a ','').replace(' moon','')+' ('+document.getElementById('bmoon-s1').textContent+' lit). Find yours:';\n"
    "  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);\n"
    "  if(navigator.share){navigator.share({title:'Birthday moon',text:txt,url:url}).catch(function(){});}\n"
    "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my birthday moon';},1500);}\n"
    "});\n"
    "})();\n</script>\n\"\"\"\n\n"
)

BLOCK = MOONPHASE + FULLMOONCAL + BDAYMOON

def sub(path, old, new, n=1):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    assert s.count(old) == n, "anchor not %dx in %s: %r" % (n, path, old[:60])
    s = s.replace(old, new)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)

TOOLS_P = BASE + r"\tools.py"
PAGES_P = BASE + r"\pages.py"
BUILD_P = BASE + r"\build.py"

# 1) 三个渲染器常量插到 STOPDIST 前
sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">', BLOCK + 'STOPDIST = """<div class="tool" id="tt-sd">')
# 2) TOOLS 注册
sub(TOOLS_P, '    "carryon": lambda args: CARRYON,',
    '    "carryon": lambda args: CARRYON,\n'
    '    "moonphase": lambda args: MOONPHASE,\n'
    '    "fullmooncal": lambda args: FULLMOONCAL,\n'
    '    "bdaymoon": lambda args: BDAYMOON,')
# 3) TOOL_EMOJI(锚点用真实 emoji 字符)
sub(BUILD_P, '    "countdown": "⏳", "datediff": "📅", "age": "🎂", "percent": "📊",',
    '    "countdown": "⏳", "datediff": "📅", "age": "🎂", "percent": "📊",\n'
    '    "moonphase": "🌕", "fullmooncal": "🌖", "bdaymoon": "🌙",')

P = []
def page(slug, title, h1, desc, kw, tool, i1, i2, h1s, h2s, h3s, faqs):
    d = {'slug': slug, 'title': title, 'h1': h1, 'desc': desc, 'category': 'calculator',
         'keyword': kw, 'tool': tool, 'args': {}, 'intro': [i1, i2],
         'howto': [h1s, h2s, h3s], 'faqs': faqs}
    P.append("    pages.append(%r)\n" % (d,))

page("moon-phase-calculator",
     "Moon Phase Calculator - Tonight's Moon for Any Date",
     "Moon Phase Calculator",
     "Pick any date and get the moon phase, illuminated fraction and moon age, computed live from the 29.53-day synodic cycle - plus the next full moon. Honest about the one-day tolerance, instant, free.",
     "moon phase calculator what is the moon phase tonight",
     "moonphase",
     "Type any date - tonight, a wedding, a camping trip, a historical morning - and this calculator returns the moon's phase name, its emoji, the illuminated fraction and its age in days, plus the next full moon after that date. Everything is computed live in your browser from the 29.5306-day synodic cycle, so the answer arrives before a moon-phase site finishes loading its ads.",
     "Moon almanac sites freeze one year per page and bury the phase behind article text. This one answers any date at once and tells you the size of its own error - about a day - instead of pretending almanac precision. The result lands in your tab title, so the moon follows you while you open other tabs.",
     "Pick a date (today is pre-filled).", "Read the phase name, emoji and illuminated percentage.", "Check the next full moon date - or share the result link.",
     [("How accurate is this moon phase calculator?", "It uses the mean synodic cycle of 29.5306 days counted from a reference new moon, which can drift up to about a day from official almanac times. For minute-precise times an observatory table wins; for any-date answers this is faster than looking one up."),
      ("What is the moon phase tonight?", "Today's date is pre-filled, so the big emoji shows tonight's phase the moment the page opens, with the illuminated fraction and the next full moon date beside it."),
      ("Why does the moon age matter?", "Moon age is how many days past new moon the date sits - day 0 is new, about 14.77 is full, and the count explains why full moons shift about 11 days earlier each calendar year."),
      ("Does my location change the moon phase?", "No - the phase depends only on the date. Where you are changes when the moon rises, not how lit it is.")])

page("full-moon-calendar",
     "Full Moon Calendar - Every Full Moon in Any Year",
     "Full Moon Calendar",
     "Type any year and get every full moon date in it, computed live from the synodic cycle - twelve or thirteen, first to last, with the blue-moon years flagged. No frozen tables, no ads between dates.",
     "full moon calendar full moons this year dates",
     "fullmooncal",
     "Enter a year and the calendar lists every full moon in it with dates, counts them, and flags the years that get thirteen - the blue moon years. Because the list is computed from the 29.5306-day cycle rather than copied from a printed table, any year from 1900 to 2100 answers instantly, including years no almanac ever bothered to print.",
     "Most full moon pages are one frozen year per page, tuned for ads. This one answers the question people actually have - when are the full moons - for any year at once, and says plainly that the simple cycle carries about a day of tolerance, so you know when to trust it for a moonlit walk and when to check an observatory for an eclipse.",
     "Type a year (this year is pre-filled).", "Read the dated list and the count.", "Watch for the extra-moon flag - that year has a blue moon.",
     [("How many full moons are in a year?", "Usually twelve - one synodic month is 29.53 days versus about 30.4 days per calendar month, so a full moon lands roughly every month. Thirteen arrive when one falls in the first days of January, and those years are marked here."),
      ("What is a blue moon?", "The common modern meaning is the second full moon in one calendar month, which happens in the same years that fit thirteen full moons. The calendar flags those years so you know where to look."),
      ("How precise are these full moon dates?", "Within about a day of official almanac times, because the simple synodic cycle ignores the orbit's elliptical speed-ups. For eclipse nights or minute-precise timing, an observatory table is the better tool."),
      ("Can I see full moons for a past year?", "Yes - any year from 1900 to 2100 works, which printed calendars never bother covering.")])

page("birthday-moon",
     "Birthday Moon - What Was the Moon Phase When You Were Born?",
     "Birthday Moon",
     "Enter your birth date and meet the moon you were born under - phase, emoji, illuminated fraction - computed live for any birthday since 1900. One-tap share settles the group chat.",
     "birthday moon phase what moon was i born under",
     "bdaymoon",
     "Type your birth date and the page shows the moon that hung over it: the phase name, its emoji, how lit it was and how old the moon was that night, plus the first full moon that followed you into the world. The answer is computed live for any date in seconds - no paging through archived almanacs.",
     "Birthday-moon sites wrap a one-line answer in horoscope copy and signup walls. This one gives the astronomy straight, says plainly that everyone born on your date shares the phase, and hands you the share link - roughly one person in eight carries your lunar emoji, which is the part of astrology that is actually true.",
     "Enter your birth date.", "Read your moon's phase, emoji and illumination.", "Share the result - one in eight friends will match your emoji.",
     [("What was the moon phase when I was born?", "Type your birth date and the phase appears instantly - name, emoji and illuminated fraction, computed from the synodic cycle with about a day of tolerance."),
      ("Does my birth time or place change my birthday moon?", "No - the phase depends only on the date. Your location changes moonrise times, not the fraction lit; everyone born on your date shares the same phase."),
      ("Why do people care about birth moons?", "Mostly for the fun of a concrete, checkable fact - the emoji doubles as a badge, and about one in eight people share yours, which makes it a better icebreaker than a star sign."),
      ("How far back does it work?", "Any date from 1900 onward - grandparents' birthdays included.")])

with io.open(PAGES_P, encoding="utf-8") as f:
    s = f.read()
anchor = "    # ---------- Index metadata used by build ----------"
assert s.count(anchor) == 1, "pages anchor"
block = "".join(P)
s = s.replace(anchor, block + anchor)
with io.open(PAGES_P, "w", encoding="utf-8", newline="") as f:
    f.write(s)

# ast 校验两个 py 文件
import ast
for f in (TOOLS_P, PAGES_P, BUILD_P):
    ast.parse(io.open(f, encoding="utf-8").read())
print("R120 inject OK: 3 renderers + 3 pages + 3 emojis, ast passed")
