# -*- coding: utf-8 -*-
"""R144 黑五结账三连:free-shipping-threshold(凑单裁决)+extended-warranty(延保自保账)+bogo(买赠实折率)"""
import io

BASE = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine"

# ---------- 渲染器 1: SHIPFREE ----------
Sf = 'SHIPFREE = """<div class="tool" id="tt-sf">\n'
Sf += '  <div class="fields">\n'
Sf += '    <div class="field"><label for="sf-c">Your cart total</label><input id="sf-c" type="number" min="0" value="60"></div>\n'
Sf += '    <div class="field"><label for="sf-t">Free shipping threshold</label><input id="sf-t" type="number" min="0" value="75"></div>\n'
Sf += '    <div class="field"><label for="sf-f">Shipping fee if you skip it</label><input id="sf-f" type="number" min="0" step="0.5" value="8.90"></div>\n'
Sf += '  </div>\n'
Sf += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sf-out">&#8211;</span><span class="result-unit">verdict on the filler</span></div>\n'
Sf += '  <div class="stats">\n'
Sf += '    <div class="stat"><b id="sf-s1">&#8211;</b><span>minimum filler to qualify</span></div>\n'
Sf += '    <div class="stat"><b id="sf-s2">&#8211;</b><span>total if you just pay shipping</span></div>\n'
Sf += '    <div class="stat"><b id="sf-s3">&#8211;</b><span>total with the minimum filler</span></div>\n'
Sf += '  </div>\n'
Sf += '  <div class="tool-note" id="sf-note"></div>\n'
Sf += '  <button type="button" class="tool-btn" id="sf-share">Share my checkout math</button>\n'
Sf += '</div>\n'
Sf += '<script>(function(){\n'
Sf += "var C=document.getElementById('sf-c'),T=document.getElementById('sf-t'),F=document.getElementById('sf-f');\n"
Sf += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Sf += "function calc(){\n"
Sf += "  var c=num(C),t=num(T),f=num(F);\n"
Sf += "  var need=Math.max(0,t-c);\n"
Sf += "  var totalShip=c+(c>=t?0:f),totalFill=c+need;\n"
Sf += "  var d1=Math.round(need*100)/100,d2=Math.round(totalShip*100)/100,d3=Math.round(totalFill*100)/100;\n"
Sf += "  var verdict;\n"
Sf += "  if(need<=0){verdict='Already free';}\n"
Sf += "  else if(need<f){verdict='Filler pays';}\n"
Sf += "  else{verdict='Pay shipping';}\n"
Sf += "  document.getElementById('sf-out').textContent=verdict;\n"
Sf += "  document.getElementById('sf-s1').textContent='$'+d1;\n"
Sf += "  document.getElementById('sf-s2').textContent='$'+d2;\n"
Sf += "  document.getElementById('sf-s3').textContent='$'+d3;\n"
Sf += "  document.getElementById('sf-note').textContent='The math is simple and the stores know you skip it: the threshold is usually set just above the average cart. If the minimum filler costs less than the shipping fee, the filler wins - but only if it is something your household genuinely finishes, like batteries or the pantry staple. Grabbing a 25 dollar nobody-item to dodge an 8 dollar fee is the most common way free shipping stops being free. And remember the fee was priced into the product page either way - paying it is not losing, it is declining to buy junk on cue.';\n"
Sf += "  document.title='Filler verdict: '+verdict+' - ToolDune';\n"
Sf += "}\n"
Sf += "function save(){try{localStorage.setItem('tt_shipfree',JSON.stringify({c:C.value,t:T.value,f:F.value}));}catch(e){}}\n"
Sf += "[C,T,F].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Sf += "var pre=false;\n"
Sf += "var qs=new URLSearchParams(location.search);\n"
Sf += "if(qs.get('c')){C.value=qs.get('c');pre=true;}\n"
Sf += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_shipfree')||'null');if(m){if(m.c){C.value=m.c;}if(m.t){T.value=m.t;}if(m.f){F.value=m.f;}}}catch(e){}}\n"
Sf += "calc();\n"
Sf += "document.getElementById('sf-share').addEventListener('click',function(){\n"
Sf += "  var txt='Checkout verdict: '+document.getElementById('sf-out').textContent+' on my '+C.value+' dollar cart. Run yours:';\n"
Sf += "  var url=location.origin+location.pathname+'?c='+encodeURIComponent(C.value);\n"
Sf += "  if(navigator.share){navigator.share({title:'Free shipping threshold',text:txt,url:url}).catch(function(){});}\n"
Sf += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my checkout math';},1500);}\n"
Sf += "});\n"
Sf += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 2: WARRANTY ----------
Wy = 'WARRANTY = """<div class="tool" id="tt-wy">\n'
Wy += '  <div class="fields">\n'
Wy += '    <div class="field"><label for="wy-p">Product price</label><input id="wy-p" type="number" min="10" value="800"></div>\n'
Wy += '    <div class="field"><label for="wy-w">Extended warranty cost</label><input id="wy-w" type="number" min="0" value="120"></div>\n'
Wy += '    <div class="field"><label for="wy-r">Out-of-warranty repair cost</label><input id="wy-r" type="number" min="0" value="300"></div>\n'
Wy += '    <div class="field"><label for="wy-k">Failure odds in years 2-4</label><select id="wy-k"><option value="0.2">Fragile - about 20%</option><option value="0.1" selected>Typical - about 10%</option><option value="0.05">Sturdy - about 5%</option></select></div>\n'
Wy += '  </div>\n'
Wy += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wy-out">&#8211;</span><span class="result-unit">verdict on the warranty</span></div>\n'
Wy += '  <div class="stats">\n'
Wy += '    <div class="stat"><b id="wy-s1">&#8211;</b><span>expected repair cost</span></div>\n'
Wy += '    <div class="stat"><b id="wy-s2">&#8211;</b><span>break-even failure odds</span></div>\n'
Wy += '    <div class="stat"><b id="wy-s3">&#8211;</b><span>warranty as % of price</span></div>\n'
Wy += '  </div>\n'
Wy += '  <div class="tool-note" id="wy-note"></div>\n'
Wy += '  <button type="button" class="tool-btn" id="wy-share">Share my warranty math</button>\n'
Wy += '</div>\n'
Wy += '<script>(function(){\n'
Wy += "var P=document.getElementById('wy-p'),W=document.getElementById('wy-w'),Rr=document.getElementById('wy-r'),K=document.getElementById('wy-k');\n"
Wy += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Wy += "function calc(){\n"
Wy += "  var p=num(P),w=num(W),r=num(Rr),k=parseFloat(K.value)||0.1;\n"
Wy += "  var exp=r*k, be=r>0?Math.round(w/r*100):0, pct=p>0?Math.round(w/p*100):0;\n"
Wy += "  var d1=Math.round(exp*10)/10;\n"
Wy += "  var verdict=w<exp?'Take it - rare':(w>exp*1.5?'Decline':'Coin flip');\n"
Wy += "  document.getElementById('wy-out').textContent=verdict;\n"
Wy += "  document.getElementById('wy-s1').textContent='$'+d1;\n"
Wy += "  document.getElementById('wy-s2').textContent=be+'%';\n"
Wy += "  document.getElementById('wy-s3').textContent=pct+'%';\n"
Wy += "  document.getElementById('wy-note').textContent='The expected-value math: a warranty pays only when failure odds exceed the warranty-to-repair ratio - and most retail plans need failure rates of 30 percent and up, several times reality. Three honest facts before you say yes at the register: many credit cards double the manufacturer warranty for free, which is the first call to make; the margin on the plan is the reason the desk exists; and the self-insurance drawer works - skip the plan, drop its price in a jar, and after a few gadgets the jar pays for the one failure you actually have. A verdict of coin flip means convenience is the only thing left to buy, which is legitimate if you name it honestly.';\n"
Wy += "  document.title='Warranty verdict: '+verdict+' - ToolDune';\n"
Wy += "}\n"
Wy += "function save(){try{localStorage.setItem('tt_warranty',JSON.stringify({p:P.value,w:W.value,r:Rr.value,k:K.value}));}catch(e){}}\n"
Wy += "[P,W,Rr].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Wy += "K.addEventListener('change',function(){calc();save();});\n"
Wy += "var pre=false;\n"
Wy += "var qs=new URLSearchParams(location.search);\n"
Wy += "if(qs.get('w')){W.value=qs.get('w');pre=true;}\n"
Wy += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_warranty')||'null');if(m){if(m.p){P.value=m.p;}if(m.w){W.value=m.w;}if(m.r){Rr.value=m.r;}if(m.k){K.value=m.k;}}}catch(e){}}\n"
Wy += "calc();\n"
Wy += "document.getElementById('wy-share').addEventListener('click',function(){\n"
Wy += "  var txt='Verdict on my extended warranty: '+document.getElementById('wy-out').textContent+'. Run yours:';\n"
Wy += "  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value);\n"
Wy += "  if(navigator.share){navigator.share({title:'Extended warranty math',text:txt,url:url}).catch(function(){});}\n"
Wy += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my warranty math';},1500);}\n"
Wy += "});\n"
Wy += "})();\n</script>\n\"\"\"\n\n"

# ---------- 渲染器 3: BOGO ----------
Bg = 'BOGO = """<div class="tool" id="tt-bg">\n'
Bg += '  <div class="fields">\n'
Bg += '    <div class="field"><label for="bg-a">Item 1 price (cheaper)</label><input id="bg-a" type="number" min="0" value="40"></div>\n'
Bg += '    <div class="field"><label for="bg-b">Item 2 price (pricier)</label><input id="bg-b" type="number" min="0" value="60"></div>\n'
Bg += '    <div class="field"><label for="bg-d">The deal on offer</label><select id="bg-d"><option value="bogo50" selected>Buy one, second 50% off</option><option value="bogofree">Buy one, second free</option><option value="off30">30% off entire purchase</option></select></div>\n'
Bg += '  </div>\n'
Bg += '  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bg-out">&#8211;</span><span class="result-unit">you pay for both</span></div>\n'
Bg += '  <div class="stats">\n'
Bg += '    <div class="stat"><b id="bg-s1">&#8211;</b><span>effective discount</span></div>\n'
Bg += '    <div class="stat"><b id="bg-s2">&#8211;</b><span>basket at full price</span></div>\n'
Bg += '    <div class="stat"><b id="bg-s3">&#8211;</b><span>vs 30% off everything</span></div>\n'
Bg += '  </div>\n'
Bg += '  <div class="tool-note" id="bg-note"></div>\n'
Bg += '  <button type="button" class="tool-btn" id="bg-share">Share my BOGO math</button>\n'
Bg += '</div>\n'
Bg += '<script>(function(){\n'
Bg += "var A=document.getElementById('bg-a'),B2=document.getElementById('bg-b'),D=document.getElementById('bg-d');\n"
Bg += "function num(el){var v=parseFloat(el.value);return isFinite(v)&&v>=0?v:0;}\n"
Bg += "function money(n){return '$'+(Math.round(n*100)/100);}\n"
Bg += "function calc(){\n"
Bg += "  var lo=Math.min(num(A),num(B2)),hi=Math.max(num(A),num(B2));\n"
Bg += "  var deal=D.value,paid,alt;\n"
Bg += "  if(deal==='bogo50'){paid=lo+hi*0.5;alt=(lo+hi)*0.7;}\n"
Bg += "  else if(deal==='bogofree'){paid=hi;alt=(lo+hi)*0.7;}\n"
Bg += "  else{paid=(lo+hi)*0.7;alt=lo+hi*0.5;}\n"
Bg += "  var full=lo+hi,eff=full>0?Math.round((1-paid/full)*100):0;\n"
Bg += "  var d1=money(paid),diff=Math.round((paid-alt)*100)/100;\n"
Bg += "  var cmp=diff<0?money(-diff)+' better than 30% off':(diff>0?money(diff)+' worse than 30% off':'same as 30% off');\n"
Bg += "  document.getElementById('bg-out').textContent=d1;\n"
Bg += "  document.getElementById('bg-s1').textContent=eff+'%';\n"
Bg += "  document.getElementById('bg-s2').textContent=money(full);\n"
Bg += "  document.getElementById('bg-s3').textContent=cmp;\n"
Bg += "  document.getElementById('bg-note').textContent='Buy-one-get-one math quietly assumes the two items cost the same: at equal prices the second-half-off deal is a clean 25 percent off, but drag a cheaper second item in and the discount slides toward 12 percent. The flat-percent comparison in the stats is the honest benchmark stores hope you skip. And the deeper catch: BOGO only saves money if the second item was already on your list - buy two to save is spending 150 percent to feel like you saved.';\n"
Bg += "  document.title='BOGO: pay '+d1+' at '+eff+'% off - ToolDune';\n"
Bg += "}\n"
Bg += "function save(){try{localStorage.setItem('tt_bogo',JSON.stringify({a:A.value,b:B2.value,d:D.value}));}catch(e){}}\n"
Bg += "[A,B2].forEach(function(el){el.addEventListener('input',function(){calc();save();});});\n"
Bg += "D.addEventListener('change',function(){calc();save();});\n"
Bg += "var pre=false;\n"
Bg += "var qs=new URLSearchParams(location.search);\n"
Bg += "if(qs.get('a')){A.value=qs.get('a');pre=true;}\n"
Bg += "if(!pre){try{var m=JSON.parse(localStorage.getItem('tt_bogo')||'null');if(m){if(m.a){A.value=m.a;}if(m.b){B2.value=m.b;}if(m.d){D.value=m.d;}}}catch(e){}}\n"
Bg += "calc();\n"
Bg += "document.getElementById('bg-share').addEventListener('click',function(){\n"
Bg += "  var txt='My BOGO deal works out to '+document.getElementById('bg-out').textContent+' for both - '+document.getElementById('bg-s1').textContent+' off. Run yours:';\n"
Bg += "  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value);\n"
Bg += "  if(navigator.share){navigator.share({title:'BOGO deal math',text:txt,url:url}).catch(function(){});}\n"
Bg += "  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my BOGO math';},1500);}\n"
Bg += "});\n"
Bg += "})();\n</script>\n\"\"\"\n\n"

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
for name in ("SHIPFREE", "WARRANTY", "BOGO"):
    assert ("\n%s = " % name) not in src, name + " already in tools.py"

sub(TOOLS_P, 'STOPDIST = """<div class="tool" id="tt-sd">',
    Sf + Wy + Bg + 'STOPDIST = """<div class="tool" id="tt-sd">')
sub(TOOLS_P, '    "donate": lambda args: DONATE,',
    '    "donate": lambda args: DONATE,\n'
    '    "shipfree": lambda args: SHIPFREE,\n'
    '    "warranty": lambda args: WARRANTY,\n'
    '    "bogo": lambda args: BOGO,')
sub(BUILD_P, '    "daylight": "☀", "holidaytip": "🎁", "donate": "💝",',
    '    "daylight": "☀", "holidaytip": "🎁", "donate": "💝",\n'
    '    "shipfree": "📦", "warranty": "💳", "bogo": "🎯",')

P = []
d = {'slug': 'free-shipping-threshold-calculator',
     'title': 'Free Shipping Threshold Calculator - Is the Filler Item Worth It?',
     'h1': 'Free Shipping Threshold Calculator',
     'desc': 'Cart total, threshold and shipping fee give a straight verdict on the filler item - plus the minimum to add and both checkout totals compared. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'free shipping threshold calculator add to cart for free shipping',
     'tool': 'shipfree',
     'args': {},
     'intro': ["Enter your cart, the free-shipping threshold and the fee. The calculator tells you the minimum filler that qualifies and compares the honest totals: pay shipping, or add exactly the gap and pay nothing.",
              "The trick works because stores set the threshold just above the average cart and count on impulse at the finish line. This one does the math in both directions - and reminds you that paying the fee is not losing; it is declining to buy junk on cue."],
     'howto': ["Cart total first - as it stands, not as you wish.",
               "Set the threshold and the shipping fee from the checkout page.",
               "If the minimum filler is something you genuinely finish, the filler wins."],
     'faqs': [("Should I add an item to get free shipping?",
               "Only when the minimum filler costs less than the shipping fee AND it is something you would buy anyway - batteries, socks, the pantry staple. A nobody-item that costs more than the fee converts free shipping into the most expensive shipping there is."),
              ("Why do stores set free shipping thresholds?",
               "Just above the average cart value - the gap is designed to trigger an add-on. Raising your cart to cross it is a planned behavior stores profit from; the calculator makes the trade explicit instead of emotional."),
              ("Is free shipping really free?",
               "No - the cost is spread into the product prices, which is why flat-fee stores can list lower prices. That is also why paying the fee on a small order is honest economics, not a defeat."),
              ("What is the minimum I should add to qualify?",
               "Exactly the gap between your cart and the threshold - not a dollar more. The calculator shows that figure next to both checkout totals so the decision is one glance, not a debate at the payment screen.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'extended-warranty-calculator',
     'title': 'Extended Warranty Calculator - Expected Value Before You Say Yes',
     'h1': 'Extended Warranty Calculator',
     'desc': 'Product price, plan cost and failure odds become an expected-value verdict at the register - with the credit-card double and the self-insurance drawer. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'extended warranty worth it calculator expected value',
     'tool': 'warranty',
     'args': {},
     'intro': ["Enter the product price, the extended warranty cost, what an out-of-pocket repair would run, and honest failure odds for years 2 to 4. The calculator compares the plan against the expected repair cost and gives a plain verdict.",
              "Warranty desks exist because the plans are profitable, not generous. The math here shows what odds the plan needs to be worth it - usually far above reality - and covers the two outs people forget: free warranty doubling through many credit cards, and the self-insurance drawer that funds the one failure you actually have."],
     'howto': ["Get the real plan price at the register, not the brochure estimate.",
               "Estimate the repair cost honestly - a screen or a logic board, not goodwill.",
               "Pick failure odds; most electronics sit near 10 percent in years 2-4."],
     'faqs': [("Are extended warranties worth the money?",
               "Usually not on the math: plans are priced with fat margins, so the failure odds needed to justify them run several times reality for most electronics. Exceptions exist - fragile screen-first devices, repair costs close to replacement, or a plan that also covers accident damage you genuinely expect."),
              ("Does my credit card cover warranty already?",
               "Many cards extend the manufacturer warranty by up to a year for free - the benefit is printed on the card guide. That alone often covers the most likely early-failure window and makes the retail plan redundant before the pitch starts."),
              ("What is self-insuring against repairs?",
               "Skipping every plan and setting its price aside instead. Across a few gadgets the jar grows faster than the failures arrive, and unspent jar money stays yours - the opposite of a plan, where unused premiums are pure margin."),
              ("What failure rate makes a warranty worth it?",
               "The warranty cost divided by the repair cost - that is the break-even odds figure in the calculator. If a 120 dollar plan covers a 300 dollar repair, it pays at 40 percent failure odds; real-world rates sit far below, which is the whole business model.")]}
P.append("    pages.append(%r)\n" % (d,))

d = {'slug': 'bogo-calculator',
     'title': 'BOGO Calculator - What Buy-One-Get-One Deals Really Discount',
     'h1': 'BOGO Calculator',
     'desc': 'Two prices plus the deal type give what you actually pay, the effective discount, and how it stacks against a plain 30-percent-off sale. Free, no sign-up.',
     'category': 'calculator',
     'keyword': 'bogo calculator buy one get one deal math',
     'tool': 'bogo',
     'args': {},
     'intro': ["Enter both item prices and the deal on offer - second at half off, second free, or a flat 30 percent off everything. The calculator shows what you pay, the true effective discount, and the flat-percent sale that would match it.",
              "BOGO math quietly assumes the two items cost the same: at equal prices, second-half-off is a clean 25 percent off - but drag a cheaper second item in and the discount slides toward 12. The comparison against a flat sale is the honest benchmark stores hope you skip, right next to the deeper catch: the deal only saves money if the second item was already on your list."],
     'howto': ["Enter the cheaper item first - BOGO rules always discount the pricier second.",
               "Pick the deal type from the shelf sign.",
               "Compare against the flat-percent figure before you commit to two."],
     'faqs': [("How much of a discount is buy one get one 50% off?",
               "At equal prices, exactly 25 percent off the pair - half the second item across two items. With unequal prices it shrinks: a 40 dollar item with a 60 dollar partner discounts the pair by only 20 percent, sliding toward 12 percent as the gap widens."),
              ("Is buy one get one free better than 50% off?",
               "BOGO free at equal prices equals 50 percent off the pair - better than half-off-second at 25. But it forces quantity: on a single item, plain 50 percent off wins outright because you buy one, not two."),
              ("Do BOGO deals save money?",
               "Only when the second item was already on your list. The deal engineers a second purchase and calls the bundle a discount - buy two to save is spending 150 percent to feel like you saved. The calculator prices the bundle so the choice is conscious."),
              ("Which is better: BOGO or a flat discount?",
               "Run both through the calculator: flat 30 percent off wins on unequal prices and on single-item purchases; BOGO free wins only when prices are equal and you genuinely need two. The gap between the deal and the flat sale is printed in the stats.")]}
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
print("R144 inject OK: 3 renderers + 3 pages + 3 emoji, ast passed")
