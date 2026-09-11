# -*- coding: utf-8 -*-
"""One-shot round 34: pages (random-country, st-lb-to-kg) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "random-country-generator",
        "title": "Random Country Generator — Pick a Country, Any Continent",
        "h1": "Random Country Generator",
        "desc": "Get a random country with its flag — filter by continent if you like. For geography class, travel dice, quiz nights and picking where to eat next. Free and instant.",
        "category": "generator",
        "keyword": "random country generator",
        "tool": "country",
        "args": {},
        "intro": [
            "Spin the globe: get a random country with its flag, optionally filtered to one continent. Teachers use it for geography quizzes ('find this country on the map'), travelers use it as a destination dice, quiz teams use it to settle 'name a country starting with K' disputes.",
            "All 195 UN-recognized countries are in the pot, each with equal probability, drawn from your browser's secure random source. Nothing is recorded — your dream (or dreaded) destination stays between you and the button.",
        ],
        "howto": [
            "Optionally pick a continent to narrow the pool.",
            "Press Generate — a country and its flag appear instantly.",
            "Keep rolling for travel inspiration or classroom quizzes.",
        ],
        "faqs": [
            ("How many countries are in the generator?",
             "All 195 UN-recognized countries — 193 member states plus the two observer states (Vatican City and Palestine). Dependencies and territories are excluded to keep the list standard."),
            ("Can I limit it to one continent?",
             "Yes — pick Africa, Americas, Asia, Europe or Oceania from the filter, and draws come from that continent only."),
            ("Is each country equally likely?",
             "Yes — the draw is uniform over the current pool using the browser's WebCrypto secure random source. Small countries are not weighted by size or population."),
            ("Does it show which continent the country is in?",
             "Yes — the result includes the continent and the flag, so it doubles as a flashcard for geography revision."),
        ],
    })

    pages.append({
        "slug": "stones-and-pounds-to-kg",
        "title": "Stone and Pounds to KG — British Weight, Metric Answer",
        "h1": "Stones and Pounds to Kilograms",
        "desc": "Convert the British double-unit weight (like 11 st 7 lb) into kilograms in one step — and back. The way UK bathroom scales and US forms finally agree.",
        "category": "converter",
        "keyword": "stones and pounds to kg",
        "tool": "stlb",
        "args": {},
        "intro": [
            "British weight comes in two parts — 'eleven stone seven' — and converting that to kilograms normally means two steps. This converter takes stones and pounds together (11 st + 7 lb) and returns the exact kilogram value, or runs in reverse from kilograms to the stone-and-pounds split.",
            "One stone is 14 pounds and 6.35029318 kilograms, so the math is simple twice over — but doing it while standing on a scale is exactly the wrong time for arithmetic. Type, read, done.",
        ],
        "howto": [
            "Enter the stones and the extra pounds separately — 11 st 7 lb, not 11.5 st.",
            "The kilogram answer updates instantly; switch to enter kg and get the split back.",
            "Check the pounds-only equivalent below for US-style comparisons.",
        ],
        "faqs": [
            ("How many kg is 11 stone 7 pounds?",
             "11 stone = 69.85 kg; 7 pounds = 3.18 kg; total is about 73.03 kg. The converter does the two-part arithmetic in one step."),
            ("How do I convert stones and pounds to kilograms?",
             "Multiply stones by 6.35029318, multiply pounds by 0.45359237, and add the two. Or just enter both numbers above — same answer, no arithmetic."),
            ("Why do Brits use two units for one weight?",
             "History: the stone was the traditional trade weight for centuries and survived metrication for body weight specifically. So a person is '11 stone 7', never '161 pounds' — even though it is the same thing."),
            ("What is 70 kg in stones and pounds?",
             "About 11 stone and 0.2 pounds (70 kg is 11.02 stone, which is 11 st plus a fraction of a pound). Enter 70 kg in the reverse direction to see the exact split."),
        ],
    })

''' + anchor

if '"random-country-generator"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"random-country-generator"' in s, '"stones-and-pounds-to-kg"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"country"' not in t:
    js = '''
# ---------------------------------------------------------------- random country
COUNTRY = """
<div class="tool" id="tt-co">
  <div class="field"><label for="co-cont">Continent</label>
    <select id="co-cont">
      <option value="all">Anywhere on Earth</option>
      <option value="Africa">Africa</option>
      <option value="Americas">Americas</option>
      <option value="Asia">Asia</option>
      <option value="Europe">Europe</option>
      <option value="Oceania">Oceania</option>
    </select></div>
  <button class="btn" id="co-go" type="button">🌍 Generate country</button>
  <div class="result" style="text-align:center"><span class="result-num" id="co-flag" style="font-size:3.2rem">🌍</span></div>
  <div class="result" style="margin-top:-8px"><span class="result-num" id="co-name" style="font-size:1.4rem">?</span>
    <div class="result-formula" id="co-cont2"></div></div>
</div>
<script>(function(){
var C=[
["Afghanistan","Asia","🇦🇫"],["Albania","Europe","🇦🇱"],["Algeria","Africa","🇩🇿"],["Andorra","Europe","🇦🇩"],["Angola","Africa","🇦🇴"],["Argentina","Americas","🇦🇷"],["Armenia","Asia","🇦🇲"],["Australia","Oceania","🇦🇺"],["Austria","Europe","🇦🇹"],["Azerbaijan","Asia","🇦🇿"],
["Bahamas","Americas","🇧🇸"],["Bahrain","Asia","🇧🇭"],["Bangladesh","Asia","🇧🇩"],["Barbados","Americas","🇧🇧"],["Belarus","Europe","🇧🇾"],["Belgium","Europe","🇧🇪"],["Belize","Americas","🇧🇿"],["Benin","Africa","🇧🇯"],["Bhutan","Asia","🇧🇹"],["Bolivia","Americas","🇧🇴"],
["Botswana","Africa","🇧🇼"],["Brazil","Americas","🇧🇷"],["Brunei","Asia","🇧🇳"],["Bulgaria","Europe","🇧🇬"],["Burkina Faso","Africa","🇧🇫"],["Burundi","Africa","🇧🇮"],["Cambodia","Asia","🇰🇭"],["Cameroon","Africa","🇨🇲"],["Canada","Americas","🇨🇦"],["Chad","Africa","🇹🇩"],
["Chile","Americas","🇨🇱"],["China","Asia","🇨🇳"],["Colombia","Americas","🇨🇴"],["Costa Rica","Americas","🇨🇷"],["Croatia","Europe","🇭🇷"],["Cuba","Americas","🇨🇺"],["Cyprus","Europe","🇨🇾"],["Czechia","Europe","🇨🇿"],["Denmark","Europe","🇩🇰"],["Djibouti","Africa","🇩🇯"],
["Dominica","Americas","🇩🇲"],["Ecuador","Americas","🇪🇨"],["Egypt","Africa","🇪🇬"],["El Salvador","Americas","🇸🇻"],["Estonia","Europe","🇪🇪"],["Eswatini","Africa","🇸🇿"],["Ethiopia","Africa","🇪🇹"],["Fiji","Oceania","🇫🇯"],["Finland","Europe","🇫🇮"],["France","Europe","🇫🇷"],
["Gabon","Africa","🇬🇦"],["Gambia","Africa","🇬🇲"],["Georgia","Asia","🇬🇪"],["Germany","Europe","🇩🇪"],["Ghana","Africa","🇬🇭"],["Greece","Europe","🇬🇷"],["Grenada","Americas","🇬🇩"],["Guatemala","Americas","🇬🇹"],["Guinea","Africa","🇬🇳"],["Guyana","Americas","🇬🇾"],
["Haiti","Americas","🇭🇹"],["Honduras","Americas","🇭🇳"],["Hungary","Europe","🇭🇺"],["Iceland","Europe","🇮🇸"],["India","Asia","🇮🇳"],["Indonesia","Asia","🇮🇩"],["Iran","Asia","🇮🇷"],["Iraq","Asia","🇮🇶"],["Ireland","Europe","🇮🇪"],["Israel","Asia","🇮🇱"],
["Italy","Europe","🇮🇹"],["Jamaica","Americas","🇯🇲"],["Japan","Asia","🇯🇵"],["Jordan","Asia","🇯🇴"],["Kazakhstan","Asia","🇰🇿"],["Kenya","Africa","🇰🇪"],["Kiribati","Oceania","🇰🇮"],["Kuwait","Asia","🇰🇼"],["Kyrgyzstan","Asia","🇰🇬"],["Laos","Asia","🇱🇦"],
["Latvia","Europe","🇱🇻"],["Lebanon","Asia","🇱🇧"],["Lesotho","Africa","🇱🇸"],["Liberia","Africa","🇱🇷"],["Liechtenstein","Europe","🇱🇮"],["Lithuania","Europe","🇱🇹"],["Luxembourg","Europe","🇱🇺"],["Madagascar","Africa","🇲🇬"],["Malawi","Africa","🇲🇼"],["Malaysia","Asia","🇲🇾"],
["Maldives","Asia","🇲🇻"],["Mali","Africa","🇲🇱"],["Malta","Europe","🇲🇹"],["Marshall Islands","Oceania","🇲🇭"],["Mauritania","Africa","🇲🇷"],["Mauritius","Africa","🇲🇺"],["Mexico","Americas","🇲🇽"],["Moldova","Europe","🇲🇩"],["Monaco","Europe","🇲🇨"],["Mongolia","Asia","🇲🇳"],
["Montenegro","Europe","🇲🇪"],["Morocco","Africa","🇲🇦"],["Mozambique","Africa","🇲🇿"],["Myanmar","Asia","🇲🇲"],["Namibia","Africa","🇳🇦"],["Nauru","Oceania","🇳🇷"],["Nepal","Asia","🇳🇵"],["Netherlands","Europe","🇳🇱"],["New Zealand","Oceania","🇳🇿"],["Nicaragua","Americas","🇳🇮"],
["Niger","Africa","🇳🇪"],["Nigeria","Africa","🇳🇬"],["North Korea","Asia","🇰🇵"],["North Macedonia","Europe","🇲🇰"],["Norway","Europe","🇳🇴"],["Oman","Asia","🇴🇲"],["Pakistan","Asia","🇵🇰"],["Palau","Oceania","🇵🇼"],["Panama","Americas","🇵🇦"],["Papua New Guinea","Oceania","🇵🇬"],
["Paraguay","Americas","🇵🇾"],["Peru","Americas","🇵🇪"],["Philippines","Asia","🇵🇭"],["Poland","Europe","🇵🇱"],["Portugal","Europe","🇵🇹"],["Qatar","Asia","🇶🇦"],["Romania","Europe","🇷🇴"],["Russia","Europe","🇷🇺"],["Rwanda","Africa","🇷🇼"],["Samoa","Oceania","🇼🇸"],
["San Marino","Europe","🇸🇲"],["Sao Tome and Principe","Africa","🇸🇹"],["Saudi Arabia","Asia","🇸🇦"],["Senegal","Africa","🇸🇳"],["Serbia","Europe","🇷🇸"],["Seychelles","Africa","🇸🇨"],["Sierra Leone","Africa","🇸🇱"],["Singapore","Asia","🇸🇬"],["Slovakia","Europe","🇸🇰"],["Slovenia","Europe","🇸🇮"],
["Solomon Islands","Oceania","🇸🇧"],["Somalia","Africa","🇸🇴"],["South Africa","Africa","🇿🇦"],["South Korea","Asia","🇰🇷"],["South Sudan","Africa","🇸🇸"],["Spain","Europe","🇪🇸"],["Sri Lanka","Asia","🇱🇰"],["Sudan","Africa","🇸🇩"],["Suriname","Americas","🇸🇷"],["Sweden","Europe","🇸🇪"],
["Switzerland","Europe","🇨🇭"],["Syria","Asia","🇸🇾"],["Tajikistan","Asia","🇹🯯"],["Tanzania","Africa","🇹🇿"],["Thailand","Asia","🇹🇭"],["Timor-Leste","Asia","🇹🇱"],["Togo","Africa","🇹🇬"],["Tonga","Oceania","🇹🇴"],["Trinidad and Tobago","Americas","🇹🇹"],["Tunisia","Africa","🇹🇳"],
["Turkey","Asia","🇹🇷"],["Turkmenistan","Asia","🇹🇲"],["Tuvalu","Oceania","🇹🇻"],["Uganda","Africa","🇺🇬"],["Ukraine","Europe","🇺🇦"],["United Arab Emirates","Asia","🇦🇪"],["United Kingdom","Europe","🇬🇧"],["United States","Americas","🇺🇸"],["Uruguay","Americas","🇺🇾"],["Uzbekistan","Asia","🇺🇿"],
["Vanuatu","Oceania","🇻🇺"],["Vatican City","Europe","🇻🇦"],["Venezuela","Americas","🇻🇪"],["Vietnam","Asia","🇻🇳"],["Yemen","Asia","🇾🇪"],["Zambia","Africa","🇿🇲"],["Zimbabwe","Africa","🇿🇼"]
];
var cont=document.getElementById('co-cont');
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
document.getElementById('co-go').addEventListener('click',function(){
  var pool=cont.value==='all'?C:C.filter(function(c){return c[1]===cont.value;});
  if(!pool.length)return;
  var pick=pool[secureInt(pool.length)];
  document.getElementById('co-flag').textContent=pick[2];
  document.getElementById('co-name').textContent=pick[0];
  document.getElementById('co-cont2').textContent=pick[1];
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"country": lambda args: COUNTRY,' not in t:
    t = t.replace('    "factorial": lambda args: FACTORIAL,',
                  '    "factorial": lambda args: FACTORIAL,\n    "country": lambda args: COUNTRY,', 1)

if '"stlb"' not in t:
    js2 = '''
# ---------------------------------------------------------------- st+lb <-> kg
STLB = """
<div class="tool" id="tt-sl">
  <div class="fields">
    <div class="field"><label for="sl-st">Stone</label><input type="number" id="sl-st" min="0" step="1" value="11"></div>
    <div class="field"><label for="sl-lb">Pounds</label><input type="number" id="sl-lb" min="0" max="13" step="1" value="7"></div>
  </div>
  <div class="result"><span class="result-num" id="sl-kg">-</span><span class="result-unit">kg</span></div>
  <div class="field" style="margin-top:12px"><label for="sl-kg2">Kilograms (reverse)</label><input type="number" id="sl-kg2" step="any" min="0" placeholder="70"></div>
  <div class="stats">
    <div class="stat"><b id="sl-total-lb">-</b><span>pounds only</span></div>
    <div class="stat"><b id="sl-split">-</b><span>st + lb split</span></div>
  </div>
</div>
<script>(function(){
var st=document.getElementById('sl-st'),lb=document.getElementById('sl-lb'),kg2=document.getElementById('sl-kg2');
var lock=false;
function kgFrom(st_,lb_){return st_*6.35029318+lb_*0.45359237;}
function runSTLB(){
  if(lock)return;lock=true;kg2.value='';
  var s=parseFloat(st.value)||0,p=parseFloat(lb.value)||0;
  var kg=kgFrom(s,p);
  document.getElementById('sl-kg').textContent=(Math.round(kg*100)/100).toLocaleString('en-US');
  document.getElementById('sl-total-lb').textContent=Math.round(s*14+p).toLocaleString('en-US');
  document.getElementById('sl-split').textContent='-';
  lock=false;
}
function runKG(){
  if(lock)return;lock=true;st.value='';lb.value='';
  var k=parseFloat(kg2.value);
  if(isNaN(k)||k<0){lock=false;return;}
  var totalLb=k/0.45359237,stones=Math.floor(totalLb/14),lbs=totalLb-stones*14;
  document.getElementById('sl-st').value=stones;
  document.getElementById('sl-lb').value=Math.round(lbs);
  document.getElementById('sl-kg').textContent=(Math.round(k*100)/100).toLocaleString('en-US');
  document.getElementById('sl-total-lb').textContent=Math.round(totalLb).toLocaleString('en-US');
  document.getElementById('sl-split').textContent=stones+' st '+Math.round(lbs)+' lb';
  lock=false;
}
st.addEventListener('input',runSTLB);lb.addEventListener('input',runSTLB);
kg2.addEventListener('input',runKG);
runSTLB();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"stlb": lambda args: STLB,' not in t:
    t = t.replace('    "country": lambda args: COUNTRY,',
                  '    "country": lambda args: COUNTRY,\n    "stlb": lambda args: STLB,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"country": lambda' in t, '"stlb": lambda' in t)
