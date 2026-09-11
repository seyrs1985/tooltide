# -*- coding: utf-8 -*-
"""One-shot round 23: pages (salary-to-hourly, coin-flip) + renderers. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "salary-to-hourly",
        "title": "Salary to Hourly Calculator — Annual Pay to Hourly Wage",
        "h1": "Salary to Hourly Calculator",
        "desc": "Convert your annual salary to an hourly wage (and back). Uses the standard 2,080-hour work year, with custom hours-per-week support. Know what your time is worth.",
        "category": "calculator",
        "keyword": "salary to hourly",
        "tool": "salary",
        "args": {},
        "intro": [
            "Enter an annual salary and see the equivalent hourly wage — or type an hourly rate and get the yearly figure. The default assumes the American standard of 2,080 work hours per year (40 hours × 52 weeks); adjust hours per week and weeks per year for your reality, including part-time schedules and unpaid leave.",
            "It matters for job comparisons (a $65,000 salary against a $35/hour contract is not obvious until both are on the same scale), for freelancers setting rates, and for anyone working out whether overtime at time-and-a-half actually pays better than the salaried offer.",
        ],
        "howto": [
            "Type your annual salary — the hourly, monthly and weekly equivalents appear instantly.",
            "Adjust hours per week and weeks per year if your schedule differs from 40 × 52.",
            "Or enter an hourly rate to convert upward to yearly pay.",
        ],
        "faqs": [
            ("How do I convert salary to hourly wage?",
             "Divide the annual salary by the hours worked per year. The standard assumption is 2,080 hours (40 hours × 52 weeks), so $52,000 a year is $25 per hour. Adjust the hours if you work part-time or take unpaid leave."),
            ("What is $50,000 a year per hour?",
             "About $24.04 per hour at 2,080 hours a year — roughly $961 a week or $4,167 a month before taxes. Enter it above to see the breakdown at your actual hours."),
            ("Should I compare jobs by hourly or annual pay?",
             "Convert both to the same scale first, then account for benefits: salaried roles often include paid leave and health insurance that hourly rates exclude. A slightly lower salary with paid time off can beat a higher hourly contract."),
            ("How many hours is full-time?",
             "The US standard is 40 hours a week for 52 weeks = 2,080 hours a year. If you take 2 weeks unpaid leave, use 2,000; many contractors bill 1,800–1,900 billable hours a year after non-billable time."),
        ],
    })

    pages.append({
        "slug": "coin-flip",
        "title": "Coin Flip Online — Fair, Cryptographically Random Heads or Tails",
        "h1": "Coin Flip",
        "desc": "Flip a coin online: cryptographically fair heads or tails with a running tally. Can't decide? Let 256 bits of entropy do it. Free, instant, nothing recorded.",
        "category": "generator",
        "keyword": "coin flip",
        "tool": "coinflip",
        "args": {},
        "intro": [
            "Flip a fair coin as many times as you like — each result comes from your browser's cryptographically secure random source, so heads and tails are equally likely every single time, with no hidden patterns. The tally keeps count across flips so you can settle best-of-three, best-of-five, or a best-of-nineteen argument.",
            "The classic use is the decision you already know the answer to: flip the coin and notice which side you were hoping for while it spins. For group decisions, the tally doubles as a neutral referee.",
        ],
        "howto": [
            "Press Flip — the coin lands heads or tails instantly.",
            "Keep flipping for best-of series; the running tally tracks heads, tails and total flips.",
            "Hit Reset to clear the tally for the next decision.",
        ],
        "faqs": [
            ("Is this online coin flip fair?",
             "Yes — each flip uses the browser's WebCrypto secure random source, the same class of generator used for encryption. Every flip is independent and exactly 50/50 in expectation."),
            ("Can I use this for a sports coin toss?",
             "You can, but a physical coin is more ceremonial. This version is handy for remote games, online debates and quick decisions where nobody has a coin."),
            ("What are the odds of flipping 5 heads in a row?",
             "1 in 32 (2 to the power of 5, about 3.1%). The tally makes it easy to spot streaks — which appear more often than intuition expects, a famous quirk of true randomness."),
            ("Does the coin remember previous flips?",
             "No — every flip is independent. The tally is just for record-keeping; past results have zero influence on the next flip."),
        ],
    })

''' + anchor

if '"salary-to-hourly"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"salary-to-hourly"' in s, '"coin-flip"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"salary"' not in t:
    js = '''
# ---------------------------------------------------------------- salary <-> hourly
SALARY = """
<div class="tool" id="tt-sal">
  <div class="fields">
    <div class="field"><label for="sal-yr">Annual salary ($)</label><input type="number" id="sal-yr" step="any" min="0" placeholder="65000"></div>
    <div class="field"><label for="sal-hr">Hourly wage ($)</label><input type="number" id="sal-hr" step="any" min="0" placeholder="31.25"></div>
  </div>
  <div class="fields">
    <div class="field"><label for="sal-hpw">Hours per week</label><input type="number" id="sal-hpw" value="40" step="any" min="1"></div>
    <div class="field"><label for="sal-wpy">Weeks per year</label><input type="number" id="sal-wpy" value="52" step="any" min="1"></div>
  </div>
  <div class="stats">
    <div class="stat"><b id="sal-m">-</b><span>per month</span></div>
    <div class="stat"><b id="sal-w">-</b><span>per week</span></div>
    <div class="stat"><b id="sal-d">-</b><span>per day (5-day week)</span></div>
    <div class="stat"><b id="sal-h">-</b><span>per hour</span></div>
  </div>
</div>
<script>(function(){
var yr=document.getElementById('sal-yr'),hr=document.getElementById('sal-hr');
var hpw=document.getElementById('sal-hpw'),wpy=document.getElementById('sal-wpy');
var lock=false;
function hoursPerYear(){return (parseFloat(hpw.value)||0)*(parseFloat(wpy.value)||0);}
function money(n){return '$'+n.toLocaleString('en-US',{maximumFractionDigits:2});}
function runY(){
  if(lock)return;lock=true;hr.value='';
  var y=parseFloat(yr.value),h=hoursPerYear();
  if(!y||!h){document.getElementById('sal-m').textContent='-';document.getElementById('sal-w').textContent='-';document.getElementById('sal-d').textContent='-';document.getElementById('sal-h').textContent='-';lock=false;return;}
  document.getElementById('sal-m').textContent=money(y/12);
  document.getElementById('sal-w').textContent=money(y/wpy.value);
  document.getElementById('sal-d').textContent=money(y/wpy.value/5);
  document.getElementById('sal-h').textContent=money(y/h);
  lock=false;
}
function runH(){
  if(lock)return;lock=true;yr.value='';
  var r=parseFloat(hr.value),h=hoursPerYear();
  if(!r||!h){lock=false;return;}
  var y=r*h;
  document.getElementById('sal-m').textContent=money(y/12);
  document.getElementById('sal-w').textContent=money(y/wpy.value);
  document.getElementById('sal-d').textContent=money(y/wpy.value/5);
  document.getElementById('sal-h').textContent=money(r);
  lock=false;
}
yr.addEventListener('input',runY);
hr.addEventListener('input',runH);
hpw.addEventListener('input',runY);
wpy.addEventListener('input',runY);
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"salary": lambda args: SALARY,' not in t:
    t = t.replace('    "fuel": lambda args: FUEL,',
                  '    "fuel": lambda args: FUEL,\n    "salary": lambda args: SALARY,', 1)

if '"coinflip"' not in t:
    js2 = '''
# ---------------------------------------------------------------- coin flip
COINFLIP = """
<div class="tool" id="tt-cf">
  <div class="cf-coin" id="cf-face">?</div>
  <button class="btn" id="cf-go" type="button">🪙 Flip</button>
  <button class="btn btn-sm" id="cf-reset" type="button">↻ Reset</button>
  <div class="stats">
    <div class="stat"><b id="cf-h">0</b><span>heads</span></div>
    <div class="stat"><b id="cf-t">0</b><span>tails</span></div>
    <div class="stat"><b id="cf-n">0</b><span>total flips</span></div>
  </div>
</div>
<script>(function(){
var h=0,tt=0;
var face=document.getElementById('cf-face');
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
document.getElementById('cf-go').addEventListener('click',function(){
  var r=secureInt(2);
  if(r){h++;face.textContent='HEADS';}else{tt++;face.textContent='TAILS';}
  document.getElementById('cf-h').textContent=h;
  document.getElementById('cf-t').textContent=tt;
  document.getElementById('cf-n').textContent=h+tt;
});
document.getElementById('cf-reset').addEventListener('click',function(){
  h=0;tt=0;face.textContent='?';
  document.getElementById('cf-h').textContent='0';
  document.getElementById('cf-t').textContent='0';
  document.getElementById('cf-n').textContent='0';
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js2, 1)
if '"coinflip": lambda args: COINFLIP,' not in t:
    t = t.replace('    "salary": lambda args: SALARY,',
                  '    "salary": lambda args: SALARY,\n    "coinflip": lambda args: COINFLIP,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("renderers registered:", '"salary": lambda' in t, '"coinflip": lambda' in t)
