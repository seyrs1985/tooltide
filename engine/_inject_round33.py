# -*- coding: utf-8 -*-
"""One-shot round 33: pages (prime-checker, factorial-calculator) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "prime-checker",
        "title": "Prime Number Checker — Is It Prime? Instant Test",
        "h1": "Prime Number Checker",
        "desc": "Check if any number is prime instantly, with the first factor shown when it is not. Handles numbers up to 15 digits using fast trial division and Miller-Rabin.",
        "category": "calculator",
        "keyword": "prime number checker",
        "tool": "prime",
        "args": {},
        "intro": [
            "Type any whole number and find out whether it is prime — and if it is not, one of its factors is shown, so you can see exactly why. Numbers up to 15 digits are checked with deterministic Miller-Rabin plus trial division, which is instant for homework numbers and fast well beyond them.",
            "Prime numbers are the atoms of arithmetic: divisible only by 1 and themselves. They drive cryptography, appear in nature (cicada life cycles), and are the endless fascination of number theory — this checker settles any 'is 1,009 prime?' argument in a keystroke.",
        ],
        "howto": [
            "Type any whole number (2 or greater).",
            "Read the verdict instantly — prime, or composite with a factor shown.",
            "Try famous cases: Mersenne suspects like 2,147,483,647, or your phone number.",
        ],
        "faqs": [
            ("What is a prime number?",
             "A whole number greater than 1 whose only divisors are 1 and itself: 2, 3, 5, 7, 11, 13… Every other number (composites) breaks into prime factors, which is why primes are called the atoms of arithmetic."),
            ("Is 1 a prime number?",
             "No — by definition primes need exactly two distinct divisors, and 1 has only one (itself). Mathematicians agreed on this convention precisely so that unique factorization works."),
            ("What is the largest known prime number?",
             "The largest known primes are Mersenne primes of the form 2^p − 1 — the record has millions of digits and is found by distributed GIMPS projects. This checker handles everyday numbers up to 15 digits instantly."),
            ("Why do primes matter outside math class?",
             "Internet encryption (RSA, Diffie-Hellman) is built on the difficulty of factoring huge composite numbers made of two large primes. Every HTTPS connection starts with prime number mathematics."),
        ],
    })

    pages.append({
        "slug": "factorial-calculator",
        "title": "Factorial Calculator — n! up to 1000, Exact Digits",
        "h1": "Factorial Calculator",
        "desc": "Calculate n! for any n up to 1,000 with full precision — every digit, not scientific notation. Shows the multiplication chain and digit count.",
        "category": "calculator",
        "keyword": "factorial calculator",
        "tool": "factorial",
        "args": {},
        "intro": [
            "Enter n and get n! — the product of every whole number from 1 to n — computed exactly, with all digits shown. Factorials explode fast (10! already has 7 digits, 100! has 158), and most calculators quietly switch to scientific notation and lose the digits. This one keeps every single one.",
            "Factorials count arrangements: 5! is the number of ways to order five things (120), which makes it the backbone of probability, combinatorics, and the permutation formulas behind shuffles, rankings and lottery odds.",
        ],
        "howto": [
            "Type a whole number n between 0 and 1,000.",
            "Read n! with every digit displayed — 0! is defined as 1.",
            "Check the digit count to appreciate how fast factorials grow.",
        ],
        "faqs": [
            ("What is 5 factorial?",
             "5! = 5 × 4 × 3 × 2 × 1 = 120. It counts the ways to arrange 5 items in order — five books on a shelf have 120 possible orders."),
            ("Why is 0 factorial equal to 1?",
             "By definition: there is exactly one way to arrange zero items (do nothing). The convention also makes formulas like n! = n × (n−1)! work for n = 1."),
            ("How big is 100 factorial?",
             "158 digits long — roughly 9.33 × 10^157. It exceeds the number of atoms in the observable universe by a wide margin, which is why exact-digit display matters."),
            ("Where are factorials used?",
             "Counting permutations and combinations, probability (card shuffles, lottery odds), Taylor series in calculus, and algorithm analysis. Anywhere 'how many orderings' appears, factorials are hiding."),
        ],
    })

''' + anchor

if '"prime-checker"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"prime-checker"' in s, '"factorial-calculator"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"prime"' not in t:
    js = '''
# ---------------------------------------------------------------- prime checker
PRIME = """
<div class="tool" id="tt-pr">
  <div class="field"><label for="pr-in">Whole number (up to 15 digits)</label>
    <input type="number" id="pr-in" step="1" placeholder="1009"></div>
  <div class="result"><span class="result-num" id="pr-out">-</span>
    <div class="result-formula" id="pr-note"></div></div>
</div>
<script>(function(){
var inp=document.getElementById('pr-in'),out=document.getElementById('pr-out'),note=document.getElementById('pr-note');
function isPrime(n){
  if(n<2)return [false,null];
  for(var p of [2,3,5,7,11,13,17,19,23,29,31,37]){if(n===p)return [true,null];if(n%p===0)return [false,p];}
  var d=n-1,r=0;while(d%2===0){d/=2;r++;}
  var bases=[2,3,5,7,11,13,17,19,23,29,31,37];
  for(var i=0;i<bases.length;i++){
    var x=1,base=bases[i]%n;if(base===0)continue;
    var pow=1,dd=d;
    for(var j=0;j<60&&dd;j++){if(dd&1)pow=pow*base%n;dd>>=1;var tmp=base*base%n;base=tmp?tmp:base;dd=dd;}
    x=pow;
    if(x===1||x===n-1)continue;
    var comp=true;
    for(var k=0;k<r-1;k++){x=x*x%n;if(x===n-1){comp=false;break;}}
    if(comp)return [false,2];
  }
  var lim=Math.sqrt(n);
  for(var f=41;f<=lim;f+=2){if(n%f===0)return [false,f];}
  return [true,null];
}
inp.addEventListener('input',function(){
  var v=this.value.trim();
  if(v===''){out.textContent='-';note.textContent='';return;}
  if(!/^\\d+$/.test(v)){out.textContent='-';note.textContent='Whole numbers only.';return;}
  var n=BigInt(v);
  if(n<2n){out.textContent='Not prime';note.textContent='Numbers below 2 are neither prime nor composite.';return;}
  var small=[2n,3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n];
  for(var i=0;i<small.length;i++){
    if(n===small[i]){out.textContent='Prime!';note.textContent=v+' is prime (it is in the base list).';return;}
    if(n%small[i]===0n){out.textContent='Not prime';note.textContent='Divisible by '+small[i]+'.';return;}
  }
  var ok=true,factor=null;
  if(v.length<=15){
    var num=Number(v);
    if(num<=Number.MAX_SAFE_INTEGER){
      var d=num-1n?0:0;
      ok=probablePrime(num);
      if(!ok){for(var f=2n;f*f<=n;f++){if(n%f===0n){factor=f;break;}}}
    }
  }
  out.textContent=ok?'Prime!':'Probably composite';
  note.textContent=ok?(v+' is prime.'):(v+' is composite'+(factor?' - divisible by '+factor.toString():' - no small factor found (use a factoring tool).'));
});
function probablePrime(n){
  var d=n-1n,r=0n;while(d%2n===0n){d/=2n;r++;}
  var bases=[2n,3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n];
  for(var i=0;i<bases.length;i++){
    var a=bases[i]%n;if(a===0n)continue;
    var x=1n,base=a,dd=d;
    while(dd>0n){if(dd&1n)x=x*base%n;base=base*base%n;dd>>=1n;}
    if(x===1n||x===n-1n)continue;
    var composite=true;
    for(var k=1n;k<r;k++){x=x*x%n;if(x===n-1n){composite=false;break;}}
    if(composite)return false;
  }
  return true;
}
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"prime": lambda args: PRIME,' not in t:
    t = t.replace('    "yesno": lambda args: YESNO,',
                  '    "yesno": lambda args: YESNO,\n    "prime": lambda args: PRIME,', 1)

if '"factorial"' not in t:
    js2 = '''
# ---------------------------------------------------------------- factorial
FACTORIAL = """
<div class="tool" id="tt-fa">
  <div class="field"><label for="fa-n">n (0 - 1000)</label><input type="number" id="fa-n" min="0" max="1000" step="1" value="5"></div>
  <div class="result"><span class="result-num" id="fa-out" style="word-break:break-all">-</span></div>
  <div class="stats">
    <div class="stat"><b id="fa-digits">-</b><span>digits</span></div>
    <div class="stat"><b id="fa-chain">-</b><span>multiplication</span></div>
  </div>
</div>
<script>(function(){
function bigFact(n){
  var a=[1n];
  for(var i=2n;i<=n;i++){
    var carry=0n;
    for(var j=0;j<a.length;j++){var p=a[j]*i+carry;a[j]=p%10n;carry=p/10n;}
    while(carry>0n){a.push(carry%10n);carry/=10n;}
  }
  return a.reverse().join('');
}
var inp=document.getElementById('fa-n');
function run(){
  var n=parseInt(inp.value);
  if(isNaN(n)||n<0||n>1000){document.getElementById('fa-out').textContent='0 to 1000 only';document.getElementById('fa-digits').textContent='-';document.getElementById('fa-chain').textContent='-';return;}
  if(n===0){document.getElementById('fa-out').textContent='1';document.getElementById('fa-digits').textContent='1';document.getElementById('fa-chain').textContent='0! = 1 by definition';return;}
  var f=bigFact(n);
  document.getElementById('fa-out').textContent=f;
  document.getElementById('fa-digits').textContent=f.length.toLocaleString('en-US');
  var chain=n<=10?Array.from({length:n},(_,i)=>i+1).join(' x ')+' = '+f:(n+'! = 1 x 2 x ... x '+n);
  document.getElementById('fa-chain').textContent=chain;
}
inp.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"factorial": lambda args: FACTORIAL,' not in t:
    t = t.replace('    "prime": lambda args: PRIME,',
                  '    "prime": lambda args: PRIME,\n    "factorial": lambda args: FACTORIAL,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"prime": lambda' in t, '"factorial": lambda' in t)
