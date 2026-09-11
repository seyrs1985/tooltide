# -*- coding: utf-8 -*-
"""One-shot round 26: ounces-to-ml page + dice-roller renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("ounces-to-ml", "Ounces to ML", "fluid ounces (US)", "milliliters", 29.5735295625, "volume",
                       "US recipes and nutrition labels speak in fluid ounces; the rest of the world pours in milliliters. One US fluid ounce is 29.5735 ml — about 30, which is why the two units feel like near-twins even though they are not twins.",
                       "Handy anchors: 1 fl oz = 29.57 ml, 8 fl oz = 236.6 ml (a cup), 12 fl oz = 354.9 ml (a can), 16 fl oz = 473.2 ml (a pint).", dec=1))

    pages.append({
        "slug": "dice-roller",
        "title": "Online Dice Roller — D6, D20 & Any Dice, Cryptographically Fair",
        "h1": "Dice Roller",
        "desc": "Roll virtual dice online: pick how many dice and how many faces (D6, D20, anything). Cryptographically fair results with per-die outcomes and totals. Perfect for board games and D&D.",
        "category": "generator",
        "keyword": "dice roller",
        "tool": "dice",
        "args": {},
        "intro": [
            "Roll up to 12 dice with any number of faces — the classic D6, the D20 that decides dungeons, or an exotic D7 if your board game demands it. Each die's result is shown individually plus the total, and every roll comes from your browser's cryptographically secure random source.",
            "No physical dice to lose under the sofa, no suspicious thumb techniques, no arguments about whether the roll was fair. The randomness is the same quality used for encryption keys — the fairest dice you will ever throw.",
        ],
        "howto": [
            "Choose the number of dice (1–12) and the number of faces per die (2–100).",
            "Hit Roll — each die shows its result, and the total appears underneath.",
            "Roll again for another set; the table shows the last roll's individual outcomes.",
        ],
        "faqs": [
            ("What is a D20?",
             "A 20-sided die, the signature die of Dungeons & Dragons — a natural 20 (rolling a 20) is the legendary critical success. This roller supports D20 and every other face count from 2 to 100."),
            ("Are online dice rolls actually random?",
             "This one uses the browser's WebCrypto secure random source — cryptographically stronger than most physical dice, which can be slightly unbalanced by weight and shape. Each roll is independent."),
            ("How do I roll 2d6?",
             "Set dice count to 2 and faces to 6 — that is the standard 2d6 notation used in Monopoly, Catan and backgammon. The roller shows each die plus the total."),
            ("Can I use this for a classroom or raffle?",
             "Yes — assign numbers to participants and roll one die with the matching face count. The cryptographic randomness makes it demonstrably fair if anyone questions the result."),
        ],
    })

''' + anchor

if '"ounces-to-ml"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"ounces-to-ml"' in s, '"dice-roller"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"dice"' not in t:
    js = '''
# ---------------------------------------------------------------- dice roller
DICE = """
<div class="tool" id="tt-dice">
  <div class="fields">
    <div class="field"><label for="dc-count">Number of dice</label><input type="number" id="dc-count" min="1" max="12" step="1" value="2"></div>
    <div class="field"><label for="dc-faces">Faces per die</label><input type="number" id="dc-faces" min="2" max="100" step="1" value="6"></div>
  </div>
  <button class="btn" id="dc-go" type="button">🎲 Roll</button>
  <div class="result"><span class="result-num" id="dc-total">-</span><span class="result-unit">total</span>
    <div class="result-formula" id="dc-each"></div></div>
</div>
<script>(function(){
var count=document.getElementById('dc-count'),faces=document.getElementById('dc-faces');
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
document.getElementById('dc-go').addEventListener('click',function(){
  var n=Math.min(12,Math.max(1,parseInt(count.value)||1));
  var f=Math.min(100,Math.max(2,parseInt(faces.value)||6));
  var rolls=[],sum=0;
  for(var i=0;i<n;i++){var r=secureInt(f)+1;rolls.push(r);sum+=r;}
  document.getElementById('dc-total').textContent=sum.toLocaleString('en-US');
  document.getElementById('dc-each').textContent='each die: '+rolls.join(',  ')+'  (D'+f+' x '+n+')';
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"dice": lambda args: DICE,' not in t:
    t = t.replace('    "coinflip": lambda args: COINFLIP,',
                  '    "coinflip": lambda args: COINFLIP,\n    "dice": lambda args: DICE,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("dice registered:", '"dice": lambda' in t)
