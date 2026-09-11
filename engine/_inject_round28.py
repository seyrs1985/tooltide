# -*- coding: utf-8 -*-
"""One-shot round 28: pages (half-calculator, random-letter-generator) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "half-calculator",
        "title": "Half Calculator — Half of Any Number, Fraction or Amount",
        "h1": "Half Calculator",
        "desc": "What is half of 3/4 cup, half of 150, or half of 2-1/2? Split any number, fraction or mixed amount in half — exact fractional answers for recipes and math homework.",
        "category": "calculator",
        "keyword": "half calculator",
        "tool": "half",
        "args": {},
        "intro": [
            "Halving sounds trivial until the number is 3/4 cup of cocoa and you are making a half batch. This calculator halves anything: whole numbers, decimals, fractions (3/4), and mixed amounts (2-1/2) — giving the exact fractional answer (3/8) alongside the decimal, so the reduced recipe stays correct.",
            "It is the quiet hero of batch cooking, scaling down for two, dividing bills between two people, and every math worksheet with the word 'half' in it.",
        ],
        "howto": [
            "Type any amount — whole number, decimal, fraction like 3/4, or mixed like 2-1/2.",
            "Read the exact half as a fraction and as a decimal.",
            "Halve several ingredients in a row while scaling a recipe down.",
        ],
        "faqs": [
            ("What is half of 3/4?",
             "3/8. Dividing a fraction by 2 doubles its bottom number: 3/4 becomes 3/8. In cups, 3/8 cup is 6 tablespoons — a common half-batch conversion."),
            ("What is half of 2/3?",
             "2/3 halved is 1/3 (double the bottom number: 2/3 → 2/6 = 1/3). This trips people up because the decimal form, 0.333, looks nothing like 0.666 halved — but it is exactly half."),
            ("What is half of 1 and 3/4 cups?",
             "7/8 cup. Convert 1-3/4 to 7/4 first, halve it to 7/8 — just under a full cup. Practically: a scant cup."),
            ("How do I halve an odd number?",
             "Odd whole numbers halve to .5 — half of 7 is 3.5. For fractions with odd denominators (like 1/2), double the denominator instead: half of 1/2 is 1/4."),
        ],
    })

    pages.append({
        "slug": "random-letter-generator",
        "title": "Random Letter Generator — Pick Letters A to Z Instantly",
        "h1": "Random Letter Generator",
        "desc": "Generate random letters A–Z for classroom games, giveaways and puzzles. Cryptographically fair, no repeats option, instant results.",
        "category": "generator",
        "keyword": "random letter generator",
        "tool": "letter",
        "args": {},
        "intro": [
            "Generate random letters from A to Z — for classroom activities, drinking-game safe editions, brainstorming ('name a fruit starting with…'), giveaways, or word games. Cryptographically fair, so every letter is equally likely and nobody can predict the pick.",
            "Generate one letter at a time or a batch, with an optional no-repeats mode for letter-bingo style games. Everything runs locally — nothing is recorded anywhere.",
        ],
        "howto": [
            "Set how many letters you need (1–26).",
            "Toggle no-repeats for bingo-style draws, or leave it off for independent picks.",
            "Hit Generate — letters appear instantly; generate again for a fresh set.",
        ],
        "faqs": [
            ("Is the letter pick truly random?",
             "Yes — letters are drawn from your browser's WebCrypto secure random source, the cryptographic-grade generator. Every letter has exactly a 1-in-26 chance."),
            ("Can I generate the whole alphabet in random order?",
             "Set count to 26 with no-repeats on — you get all 26 letters in a random order, ready for letter-bingo or alphabet challenge games."),
            ("What can I use a random letter for?",
             "Classroom games (name a country starting with M), art prompts, assigning fair letter grades to presentations, passwords, brainstorming constraints, and board game substitutes for lost letter tiles."),
            ("Does it work offline?",
             "Yes — generation runs in your browser. Once the page is loaded, no connection is needed."),
        ],
    })

''' + anchor

if '"half-calculator"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"half-calculator"' in s, '"random-letter-generator"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"half"' not in t:
    js = '''
# ---------------------------------------------------------------- half calculator
HALF = """
<div class="tool" id="tt-half">
  <div class="field"><label for="hf-in">Number, fraction or mixed (3/4, 2-1/2, 0.8)</label>
    <input type="text" id="hf-in" placeholder="3/4"></div>
  <div class="result"><span class="result-num" id="hf-out">-</span></div>
  <div class="stats">
    <div class="stat"><b id="hf-frac">-</b><span>exact fraction</span></div>
    <div class="stat"><b id="hf-dec">-</b><span>decimal</span></div>
  </div>
</div>
<script>(function(){
var inp=document.getElementById('hf-in');
var out=document.getElementById('hf-out'),fr=document.getElementById('hf-frac'),dc=document.getElementById('hf-dec');
function gcd(a,b){return b?gcd(b,a%b):a;}
function parse(v){
  v=v.trim().replace(/"/g,'');
  var m=v.match(/^(\\d+)?[- ]?(\\d+)\\/(\\d+)$/);
  if(m){var w=m[1]?+m[1]:0;return {n:w*(+m[3])+(+m[2]),d:+m[3]};}
  var f=parseFloat(v);
  if(isNaN(f))return null;
  if(Number.isInteger(f))return {n:f,d:1};
  var s=f.toFixed(6).replace(/0+$/,'');
  var dec=s.split('.')[1];
  var den=Math.pow(10,dec.length);
  return {n:Math.round(f*den),d:den};
}
function show(v){
  var h=parse(v);
  if(!h||!h.d){out.textContent='-';fr.textContent='-';dc.textContent='-';return;}
  var n=h.n,d=h.d*2,g=gcd(n,d);
  n/=g;d/=g;
  var whole=Math.floor(n/d),rem=n%d;
  var fs=rem?(whole?whole+'-':'')+rem+'/'+d:(whole+'');
  out.textContent=fs;
  fr.textContent=fs;
  dc.textContent=Math.round((h.n/h.d/2)*1e6)/1e6;
}
inp.addEventListener('input',function(){show(this.value);});
show('3/4');
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"half": lambda args: HALF,' not in t:
    t = t.replace('    "dice": lambda args: DICE,',
                  '    "dice": lambda args: DICE,\n    "half": lambda args: HALF,', 1)

if '"letter"' not in t:
    js2 = '''
# ---------------------------------------------------------------- random letter
LETTER = """
<div class="tool" id="tt-rl">
  <div class="chips">
    <button class="chip active" id="rl-uniq" type="button">No repeats</button>
  </div>
  <div class="field"><label for="rl-count">How many letters</label><input type="number" id="rl-count" min="1" max="26" step="1" value="1"></div>
  <button class="btn" id="rl-go" type="button">🔤 Generate</button>
  <div class="result"><span class="result-num" id="rl-out" style="letter-spacing:.2em">-</span></div>
</div>
<script>(function(){
var uniq=false;
document.getElementById('rl-uniq').addEventListener('click',function(){
  uniq=!uniq;this.classList.toggle('active',uniq);
});
document.getElementById('rl-go').addEventListener('click',function(){
  var n=Math.min(26,Math.max(1,parseInt(document.getElementById('rl-count').value)||1));
  var A='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
    do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
  var out=[],seen={};
  if(uniq&&n===26){out=A.split('').sort(function(){return secureInt(3)-1;});}
  else{
    while(out.length<n){
      var ch=A[secureInt(26)];
      if(uniq&&seen[ch])continue;
      seen[ch]=1;out.push(ch);
    }
  }
  document.getElementById('rl-out').textContent=out.join(' ');
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"letter": lambda args: LETTER,' not in t:
    t = t.replace('    "half": lambda args: HALF,',
                  '    "half": lambda args: HALF,\n    "letter": lambda args: LETTER,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"half": lambda' in t, '"letter": lambda' in t)
