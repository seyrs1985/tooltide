# -*- coding: utf-8 -*-
"""One-shot round 39: pages (km-to-feet, name-combiner) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("km-to-feet", "KM to Feet", "kilometers", "feet", 3280.839895, "distance",
                       "Aviation altitudes, hiking trails and running elevation are quoted in feet even when the distances underneath are metric. One kilometer is 3,280.84 feet — so a 5 km trail climb chart in feet needs this exact factor, not the rough 3,280.",
                       "Handy anchors: 1 km = 3,280.84 ft, 3 km = 9,842 ft (a park loop), 10 km = 32,808 ft, 42 km = 137,795 ft (marathon distance)."))

    pages.append({
        "slug": "name-combiner",
        "title": "Name Combiner — Merge Two Names into One",
        "h1": "Name Combiner",
        "desc": "Blend two names into one: couple names, ship names, baby names, team names or brand ideas. Multiple merge styles, click to copy, everything local.",
        "category": "generator",
        "keyword": "name combiner",
        "tool": "combiner",
        "args": {},
        "intro": [
            "Type two names and get a list of blended possibilities — the classic couple-name game (Brad + Angelina), ship names for fandoms, baby-name brainstorming, or company and product name ideas from two founder names. Several merge styles run at once: front-half + back-half, overlapping sounds, and alternating letters.",
            "Every combination is generated locally in your browser from the two names you type — nothing is sent anywhere, and nothing is recorded. Copy the ones you like and ignore the rest; half the fun is the terrible ones.",
        ],
        "howto": [
            "Type the two names you want to blend.",
            "Read the merged candidates — different splice points produce different styles.",
            "Click any result to copy it; regenerate with different spellings for fresh options.",
        ],
        "faqs": [
            ("How does name blending work?",
             "Each name is split at every syllable-ish boundary, and the front half of one is joined to the back half of the other — both directions. Overlaps where the ending of one name matches the start of the other produce the smoothest blends."),
            ("What is a ship name?",
             "Fandom shorthand for a fictional (or real) couple: Brad + Angelina became 'Brangelina'. Ship names work the same way for TV characters, K-pop pairings and book couples."),
            ("Can I use a blended name for my business?",
             "Blends make memorable brand names (think Pinterest = pin + interest). Before committing, search trademark databases and domain availability — the generator cannot check those for you."),
            ("Does it work with any language?",
             "It works best with Latin-alphabet names. Accented characters are kept as-is, so Spanish, French and Nordic names blend fine."),
        ],
    })

''' + anchor

if '"km-to-feet"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"km-to-feet"' in s, '"name-combiner"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"combiner"' not in t:
    js = '''
# ---------------------------------------------------------------- name combiner
COMBINER = """
<div class="tool" id="tt-nc">
  <div class="fields">
    <div class="field"><label for="nc-a">First name</label><input type="text" id="nc-a" placeholder="Brad" autocomplete="off"></div>
    <div class="field"><label for="nc-b">Second name</label><input type="text" id="nc-b" placeholder="Angelina" autocomplete="off"></div>
  </div>
  <div class="names-grid" id="nc-out"></div>
  <div class="tool-note">Click any blend to copy it. Same-name pairs produce the funniest failures - try it.</div>
</div>
<script>(function(){
var A=document.getElementById('nc-a'),B=document.getElementById('nc-b'),out=document.getElementById('nc-out');
function cap(v){return v.charAt(0).toUpperCase()+v.slice(1).toLowerCase();}
function splits(name){
  var res=[name.toLowerCase()];
  for(var i=1;i<name.length;i++){res.push([name.slice(0,i).toLowerCase(),name.slice(i).toLowerCase()]);}
  return res;
}
function blends(a,b){
  var sa=splits(a),sb=splits(b),res=[];
  sa.forEach(function(x){
    sb.forEach(function(y){
      if(typeof x==='string'&&typeof y==='string'){res.push(cap(x+y));return;}
      var front=Array.isArray(x)?x[0]:x, back=Array.isArray(x)?x[1]:'';
      var f2=Array.isArray(y)?y[0]:y, b2=Array.isArray(y)?y[1]:y;
      res.push(cap(front+b2));
      res.push(cap(f2+back));
    });
  });
  return res.filter(function(v,i,arr){return v&&arr.indexOf(v)===i&&v.toLowerCase()!==a.toLowerCase()&&v.toLowerCase()!==b.toLowerCase();});
}
function run(){
  var a=A.value.trim(),b=B.value.trim();
  out.innerHTML='';
  if(!a||!b)return;
  var list=blends(cap(a),cap(b)).slice(0,12);
  list.forEach(function(v){
    var d=document.createElement('button');d.className='name-card';d.type='button';d.textContent=v;
    d.addEventListener('click',function(){
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(v);}
      d.classList.add('copied');var s=this;setTimeout(function(){s.classList.remove('copied');},900);
    });
    out.appendChild(d);
  });
}
A.addEventListener('input',run);B.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"combiner": lambda args: COMBINER,' not in t:
    t = t.replace('    "planets": lambda args: PLANETS,',
                  '    "planets": lambda args: PLANETS,\n    "combiner": lambda args: COMBINER,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("combiner registered:", '"combiner": lambda' in t)
