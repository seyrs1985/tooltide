# -*- coding: utf-8 -*-
"""R175 早春庭院与过敏三连:saline-rinse(洗鼻盐水配比)+rain-barrel(屋顶集水)+grass-seed(草籽补播)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: SALINER ----------
Sr = 'SALINER = """<div class="tool" id="tt-srn">\n'
Sr += '  <div class="fields">\n'
Sr += '    <div class="field"><label for="srn-w">Rinse bottle water (ml)</label><select id="srn-w"><option value="240" selected>240 ml - squeeze bottle</option><option value="500">500 ml - neti pot, twice</option><option value="1000">1000 ml - big rinse</option></select></div>\n'
Sr += '  </div>\n'
Sr += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="srn-out">&#8211;</span><span class="result-unit">grams of salt</span></div>\n'
Sr += '  <div class="stats">\n'
Sr += '    <div class="stat"><b id="srn-s1">&#8211;</b><span>baking soda (g)</span></div>\n'
Sr += '    <div class="stat"><b id="srn-s2">&#8211;</b><span>teaspoons of salt</span></div>\n'
Sr += '    <div class="stat"><b id="srn-s3">&#8211;</b><span>water rule</span></div>\n'
Sr += '  </div>\n'
Sr += '  <div class="tool-note" id="srn-note"></div>\n'
Sr += '  <button type="button" class="tool-btn" id="srn-share">Share my rinse recipe</button>\n'
Sr += '</div>\n'
Sr += '<script>(function(){\n'
Sr += "var W=document.getElementById('srn-w');\n"
Sr += "function calc(){\n"
Sr += "  var w=parseFloat(W.value)||240;\n"
Sr += "  var salt=w*0.0094, soda=w*0.0042, tsp=Math.round(salt/5.7*10)/10;\n"
Sr += "  var d1=Math.round(salt*100)/100, d2=Math.round(soda*100)/100;\n"
Sr += "  document.getElementById('srn-out').textContent=d1;\n"
Sr += "  document.getElementById('srn-s1').textContent=d2;\n"
Sr += "  document.getElementById('srn-s2').textContent=tsp;\n"
Sr += "  document.getElementById('srn-s3').textContent='boiled or distilled';\n"
Sr += "  document.getElementById('srn-note').textContent='The safety rule comes first because it is the only fatal one on this page: the water must be boiled for a minute and cooled, or distilled - never straight from the tap, a lake or a shower. The mix is pharmacy-standard: about 9.4 grams of non-iodized salt per liter, plus baking soda to buffer the sting, which is exactly what the commercial packets contain at a heavy markup. Iodized table salt stings and carries anti-caking agents you do not want up there. During allergy season a daily rinse after being outside clears the pollen before it sets up inflammation - it is the cheapest allergy treatment with the best evidence-to-cost ratio on the shelf.';\n"
Sr += "  document.title='Sinus rinse: '+d1+' g salt for '+Math.round(w)+' ml - ToolDune';\n"
Sr += "}\n"
Sr += "function save(){try{localStorage.setItem('tt_saliner',JSON.stringify({w:W.value}));}catch(e){}}\n"
Sr += "W.addEventListener('change',function(){calc();save();});\n"
Sr += "var pre=false;\n"
Sr += "var qs=new URLSearchParams(location.search);\n"
Sr += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Sr += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_saliner')||'null');if(m&&m.w){W.value=m.w;}}catch(e){}}\n"
Sr += "calc();\n"
Sr += "document.getElementById('srn-share').addEventListener('click',function(){\n"
Sr += "  var txt='My sinus rinse: '+document.getElementById('srn-out').textContent+' g salt + '+document.getElementById('srn-s1').textContent+' g baking soda in '+W.value+' ml. Mix yours:';\n"
Sr += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
Sr += "  if(navigator.share){navigator.share({title:'Sinus rinse recipe',text:txt,url:url}).catch(function(){});}\n"
Sr += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my rinse recipe';},1500);}\n"
Sr += "});\n"
Sr += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: RAINBARREL ----------
Rb = 'RAINBARREL = """<div class="tool" id="tt-rb">\n'
Rb += '  <div class="fields">\n'
Rb += '    <div class="field"><label for="rb-r">Roof area feeding the barrel (sq ft)</label><input id="rb-r" type="number" min="100" max="10000" value="1200"></div>\n'
Rb += '    <div class="field"><label for="rb-b">Barrels hooked up (55 gal each)</label><input id="rb-b" type="number" min="1" max="20" value="2"></div>\n'
Dj_dummy5 = None
Rb += '  </div>\n'
Rb += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rb-out">&#8211;</span><span class="result-unit">gallons per inch of rain</span></div>\n'
Rb += '  <div class="stats">\n'
Rb += '    <div class="stat"><b id="rb-s1">&#8211;</b><span>barrels that overflow</span></div>\n'
Rb += '    <div class="stat"><b id="rb-s2">&#8211;</b><span>season harvest, 15 in of rain</span></div>\n'
Rb += '    <div class="stat"><b id="rb-s3">&#8211;</b><span>the mosquito rule</span></div>\n'
Rb += '  </div>\n'
Rb += '  <div class="tool-note" id="rb-note"></div>\n'
Rb += '  <button type="button" class="tool-btn" id="rb-share">Share my harvest math</button>\n'
Rb += '</div>\n'
Rb += '<script>(function(){\n'
Rb += "var Rr=document.getElementById('rb-r'),B=document.getElementById('rb-b');\n"
Rb += "function calc(){\n"
Rb += "  var roof=parseFloat(Rr.value)||1200,bars=Math.max(1,Math.round(parseFloat(B.value)||2));\n"
Rb += "  var gal=roof*0.623*0.85, fills=gal/(bars*55), season=gal*15;\n"
Rb += "  var d1=Math.round(gal), d2=Math.ceil(fills);\n"
Rb += "  document.getElementById('rb-out').textContent=d1;\n"
Rb += "  document.getElementById('rb-s1').textContent=d2+'x over';\n"
Rb += "  document.getElementById('rb-s2').textContent=Math.round(season)+' gal';\n"
Rb += "  document.getElementById('rb-s3').textContent='screened lid';\n"
Rb += "  document.getElementById('rb-note').textContent='The shock of this math is the point: one inch of rain on an ordinary roof harvests hundreds of gallons, which is why the barrel overflows almost immediately and the overflow hose needs a plan - route it back to the garden beds, not the foundation. Two rules keep the barrel a blessing: a screened self-closing lid so mosquitoes cannot breed in it, and the honest note that rainwater is soft and neutral - better for plants than most tap water, which is why the garden notices the switch before you do. Raised on cinder blocks for gravity pressure at the spigot, and check local rules once - most places are fine and a few old statutes are still on the books.';\n"
Rb += "  document.title='Rain harvest: '+d1+' gal per inch of rain - ToolDune';\n"
Rb += "}\n"
Rb += "function save(){try{localStorage.setItem('tt_rainbarrel',JSON.stringify({r:Rr.value,b:B.value}));}catch(e){}}\n"
Rb += "[Rr,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Rb += "var pre=false;\n"
Rb += "var qs=new URLSearchParams(location.search);\n"
Rb += "if(qs.get('r')){Rr.value=qs.get('r');pre=true;}\n"
Rb += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_rainbarrel')||'null');if(m){if(m.r){Rr.value=m.r;}if(m.b){B.value=m.b;}}}catch(e){}}\n"
Rb += "calc();\n"
Rb += "document.getElementById('rb-share').addEventListener('click',function(){\n"
Rb += "  var txt='My roof harvests '+document.getElementById('rb-out').textContent+' gallons per inch of rain. Run yours:';\n"
Rb += "  var url=location.origin+location.pathname+'?r='+encodeURIComponent(Rr.value);\n"
Rb += "  if(navigator.share){navigator.share({title:'Rain barrel harvest',text:txt,url:url}).catch(function(){});}\n"
Rb += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my harvest math';},1500);}\n"
Rb += "});\n"
Rb += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: GRASSSEED ----------
Gs = 'GRASSSEED = """<div class="tool" id="tt-gs">\n'
Gs += '  <div class="fields">\n'
Gs += '    <div class="field"><label for="gs-a">Bare patch area (sq ft)</label><input id="gs-a" type="number" min="10" max="20000" value="200"></div>\n'
Gs += '    <div class="field"><label for="gs-t">Seeding style</label><select id="gs-t"><option value="5" selected>Bare ground - 5 lb/1000</option><option value="2.5">Overseeding thin lawn - 2.5 lb/1000</option></select></div>\n'
Gs += '    <div class="field"><label for="gs-p">Price per lb of seed</label><input id="gs-p" type="number" min="2" value="6"></div>\n'
Gs += '  </div>\n'
Gs += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gs-out">&#8211;</span><span class="result-unit">pounds of seed</span></div>\n'
Gs += '  <div class="stats">\n'
Gs += '    <div class="stat"><b id="gs-s1">&#8211;</b><span>seed cost</span></div>\n'
Gs += '    <div class="stat"><b id="gs-s2">&#8211;</b><span>sprouts in</span></div>\n'
Gs += '    <div class="stat"><b id="gs-s3">&#8211;</b><span>first mow in</span></div>\n'
Gs += '  </div>\n'
Gs += '  <div class="tool-note" id="gs-note"></div>\n'
Gs += '  <button type="button" class="tool-btn" id="gs-share">Share my seed math</button>\n'
Gs += '</div>\n'
Gs += '<script>(function(){\n'
Gs += "var A=document.getElementById('gs-a'),T=document.getElementById('gs-t'),P=document.getElementById('gs-p');\n"
Gs += "function calc(){\n"
Gs += "  var a=parseFloat(A.value)||200,rate=parseFloat(T.value)||5,p=parseFloat(P.value)||6;\n"
Gs += "  var lb=a/1000*rate, cost=lb*p;\n"
Gs += "  var d1=Math.round(lb*10)/10, d2=Math.round(cost*100)/100;\n"
Gs += "  document.getElementById('gs-out').textContent=d1;\n"
Gs += "  document.getElementById('gs-s1').textContent='$'+d2;\n"
Gs += "  document.getElementById('gs-s2').textContent='5-14 days';\n"
Gs += "  document.getElementById('gs-s3').textContent='3-4 weeks';\n"
Gs += "  document.getElementById('gs-note').textContent='The two rules that decide patch success: seed-to-soil contact - rake the seed in lightly so it stops being bird food - and water twice a day, ten minutes, until sprouts show, then taper. The honest calendar note: spring seeding fights crabgrass pre-emergent, which kills grass seed just as enthusiastically as weeds - you cannot have both the barrier and the patch, so pick one. Fall remains the better season for cool-season grass on every measure, and the first mow waits until the new blades reach three inches.';\n"
Gs += "  document.title='Patch: '+d1+' lb of seed - ToolDune';\n"
Gs += "}\n"
Gs += "function save(){try{localStorage.setItem('tt_grassseed',JSON.stringify({a:A.value,t:T.value,p:P.value}));}catch(e){}}\n"
Gs += "[A,T,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});\n"
Gs += "var pre=false;\n"
Gs += "var qs=new URLSearchParams(location.search);\n"
Gs += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Gs += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_grassseed')||'null');if(m){if(m.a){A.value=m.a;}if(m.t){T.value=m.t;}if(m.p){P.value=m.p;}}}catch(e){}}\n"
Gs += "calc();\n"
Gs += "document.getElementById('gs-share').addEventListener('click',function(){\n"
Gs += "  var txt='My bare patch takes '+document.getElementById('gs-out').textContent+' lb of seed. Run yours:';\n"
Gs += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Gs += "  if(navigator.share){navigator.share({title:'Grass seed math',text:txt,url:url}).catch(function(){});}\n"
Gs += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my seed math';},1500);}\n"
Gs += "});\n"
Gs += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("SALINER", "RAINBARREL", "GRASSSEED"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Sr + Rb + Gs + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "lawnfert": lambda args: LAWNFERT,',
    '    "lawnfert": lambda args: LAWNFERT,\n'
    '    "saliner": lambda args: SALINER,\n'
    '    "rainbarrel": lambda args: RAINBARREL,\n'
    '    "grassseed": lambda args: GRASSSEED,')
sub(BUILD_P, '    "gutter": "🍂", "airpur": "🍃", "lawnfert": "🌿",',
    '    "gutter": "🍂", "airpur": "🍃", "lawnfert": "🌿",\n'
    '    "saliner": "🌊", "rainbarrel": "☔", "grassseed": "🌱",')

P = []
d = {'slug': 'saline-rinse-calculator',
     'title': 'Saline Rinse Calculator - Salt and Baking Soda for Any Bottle',
     'h1': 'Saline Rinse Calculator',
     'desc': 'Water volume gives the exact salt and baking soda for a sinus rinse - the pharmacy-packet recipe at pennies, with the boiled-water rule first. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'saline rinse recipe calculator neti pot salt amount',
     'tool': 'saliner',
     'args': {},
     'intro': ["Pick your rinse bottle size and get the exact non-iodized salt and baking soda - the same pharmacy-standard packet recipe at a few cents per rinse instead of a dollar.",
              "The safety rule comes first because it is the only fatal one on the page: the water must be boiled and cooled or distilled, never straight from the tap. During allergy season a daily rinse after being outside clears pollen before it sets up inflammation - the best evidence-to-cost ratio on the allergy shelf."],
     'howto': ["Boil the water a minute and cool it, or use distilled - always.",
               "Weigh the salt and soda; non-iodized salt only.",
               "Rinse daily after outdoor exposure in pollen season."],
     'faqs': [("How much salt do I put in a sinus rinse?",
               "About 9.4 grams of non-iodized salt per liter - 2.25 grams in a 240 ml squeeze bottle - plus baking soda to buffer. The calculator scales it to your bottle exactly, matching the commercial packet."),
              ("Can I use tap water for a nasal rinse?",
               "Never straight - tap, lake and shower water carry a rare but fatal amoeba risk. Boil for a minute and cool, or use distilled. This is the one rule on the page with no exceptions and no home remedies."),
              ("Why does my sinus rinse sting?",
               "Iodized table salt or missing buffer: iodine and anti-caking agents irritate, and the baking soda is what matches your body pH so the rinse feels like nothing. Use pickling or canning salt plus the soda."),
              ("How often can I rinse my sinuses?",
               "Daily during allergy season is standard and safe with clean water - rinse after outdoor exposure to clear pollen before it inflames. Skip when fully blocked; forcing through creates pressure without benefit.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'rain-barrel-calculator',
     'title': 'Rain Barrel Calculator - Gallons Harvested From Your Roof',
     'h1': 'Rain Barrel Calculator',
     'desc': 'Roof area times rainfall gives the gallons one inch of rain harvests, how fast the barrels overflow, and the season total - with the mosquito rule. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'rain barrel calculator how much water from roof rain harvest',
     'tool': 'rainbarrel',
     'args': {},
     'intro': ["Enter the roof area feeding your downspout and how many 55-gallon barrels you run. The calculator shows the gallons one inch of rain harvests - hundreds on an ordinary roof - how fast they overflow, and the season total.",
              "The shock is the point: a modest rain moves hundreds of gallons off your roof. The two rules that keep the barrel a blessing: a screened self-closing lid so mosquitoes cannot breed, and an overflow plan that routes water to garden beds instead of the foundation."],
     'howto': ["Roof area is footprint, not slope - pitch does not change harvest.",
               "One inch of rain yields about 0.62 gallons per square foot.",
               "Raise the barrel on blocks for gravity pressure at the spigot."],
     'faqs': [("How much water comes off a roof in rain?",
               "About 0.62 gallons per square foot per inch of rain - one inch on a 1,200 square foot roof is roughly 750 gallons. Even one 55-gallon barrel fills several times over in a modest shower."),
              ("Is rainwater good for the garden?",
               "Better than most tap water - soft, neutral pH, no chlorine. Plants visibly prefer it, which is why the barrel pays for itself in plant health before the water bill notices."),
              ("Do rain barrels attract mosquitoes?",
               "Only if the water sits open. A screened, self-closing lid makes breeding impossible - the one rule that is non-negotiable, and the overflow hose should leave the barrel area too."),
              ("Are rain barrels legal?",
               "Most places yes; a few states carried historic restrictions that have mostly been repealed with incentives instead. Check your local rules once - the calculator handles the math, the statute needs one search.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'grass-seed-calculator',
     'title': 'Grass Seed Calculator - Pounds for Bare Patches and Overseeding',
     'h1': 'Grass Seed Calculator',
     'desc': 'Patch size times the seeding rate gives pounds of seed, the cost, sprout timing and the first-mow rule - with the crabgrass conflict named honestly. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'grass seed calculator how much seed per square foot bare patch',
     'tool': 'grassseed',
     'args': {},
     'intro': ["Enter the bare patch size, the seeding style - bare ground wants about 5 pounds per 1000 square feet, overseeding half that - and your seed price. The calculator gives pounds, cost, sprout timing and the first-mow rule.",
              "Two rules decide patch success: seed-to-soil contact (rake it in so it stops being bird food) and twice-daily watering until sprouts show. The honest calendar note: spring seeding fights crabgrass pre-emergent, which kills grass seed as enthusiastically as weeds - you cannot have both the barrier and the patch."],
     'howto': ["Measure the bare spots honestly - they always run bigger.",
               "Rake the seed in lightly; contact with soil is everything.",
               "Water twice a day, ten minutes, until the green shows."],
     'faqs': [("How much grass seed do I need per square foot?",
               "Bare ground wants about 5 pounds per 1000 square feet; overseeding a thin lawn takes half that. The calculator scales the rate to your patch and prices it."),
              ("When should I plant grass seed?",
               "Fall is the better season for cool-season grass on every measure - warm soil, cool air, fewer weeds. Spring works but competes with crabgrass pre-emergent, which kills grass seed along with the weeds: pick one."),
              ("How long does grass seed take to sprout?",
               "Five to fourteen days depending on variety and warmth, with the first mow at three inches - about three to four weeks in. Daily watering until sprouts show is the non-negotiable part."),
              ("Why did my grass seed not grow?",
               "Almost always seed-to-soil contact or water: seed sitting on top of old thatch is bird food, and a single missed day of watering at sprout time kills the crop. Rake in, water twice daily, and patience does the rest.")]}
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
print("R175 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
