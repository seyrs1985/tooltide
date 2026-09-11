# -*- coding: utf-8 -*-
"""One-shot round 42: page (binary-to-hex) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append({
        "slug": "binary-to-hex",
        "title": "Binary to Hex Converter — Binary ⇄ Hexadecimal, Instant",
        "h1": "Binary to Hex Converter",
        "desc": "Convert binary to hexadecimal and back instantly. Byte-grouped, standard notation, with the 4-bit nibble trick explained. Computer science homework solved.",
        "category": "converter",
        "keyword": "binary to hex",
        "tool": "binhex",
        "args": {},
        "intro": [
            "Paste binary code (space-separated bytes like 01001000 01101001) and get clean hexadecimal — 48 69 — or paste hex and get the binary. The conversion works in groups of four bits: each binary nibble maps to exactly one hex digit, which is why programmers write memory dumps in hex.",
            "Both directions update live and strict validation rejects malformed groups instead of guessing. It pairs with the text-to-binary converter for the full journey from human text to machine notation.",
        ],
        "howto": [
            "Paste binary in the first box — space-separated groups of up to 8 bits.",
            "Read the hexadecimal in the second box, one or two hex digits per group.",
            "Paste hex (like 48 69) in the second box to convert back to binary.",
        ],
        "faqs": [
            ("How do you convert binary to hex?",
             "Group the bits in fours from the right, then convert each group: 0100 = 4, 1001 = 9, so 01001001 = 49 in hex. Four bits (a nibble) cover exactly 0–15, the range of one hex digit."),
            ("Why do programmers use hexadecimal?",
             "It is readable shorthand for binary: every byte is exactly two hex digits instead of eight bits. Memory dumps, color codes and MAC addresses all use hex for this reason."),
            ("What is 11111111 in hex?",
             "FF — the maximum value of one byte, 255 in decimal. Eight 1-bits map to two F digits, one per nibble."),
            ("Does the converter handle values longer than a byte?",
             "Yes — groups are converted independently, so 16-bit, 32-bit and arbitrary-length binary strings all work. Keep the groups separated with spaces for reliable parsing."),
        ],
    })

''' + anchor

if '"binary-to-hex"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"binary-to-hex"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"binhex"' not in t:
    js = '''
# ---------------------------------------------------------------- binary <-> hex
BINHEX = """
<div class="tool" id="tt-bh">
  <div class="field"><label for="bh-bin">Binary (space-separated groups)</label>
    <textarea id="bh-bin" rows="3" placeholder="01001000 01101001"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="bh-hex">Hexadecimal (space-separated)</label>
    <textarea id="bh-hex" rows="3" placeholder="48 69"></textarea></div>
  <div class="tool-note">Each binary group converts to one hex digit pair. Max 8 bits per group; invalid groups are flagged, not guessed.</div>
</div>
<script>(function(){
var bin=document.getElementById('bh-bin'),hex=document.getElementById('bh-hex');
var lock=false;
function binToHex(v){
  return v.trim().split(/\\s+/).filter(Boolean).map(function(g){
    if(!/^[01]{1,8}$/.test(g))throw 'bad';
    return parseInt(g,2).toString(16).toUpperCase().padStart(Math.ceil(g.length/4),'0');
  }).join(' ');
}
function hexToBin(v){
  return v.trim().split(/\\s+/).filter(Boolean).map(function(g){
    if(!/^[0-9a-fA-F]{1,4}$/.test(g))throw 'bad';
    var n=parseInt(g,16);
    var bits=Math.ceil(g.length*4/8)*8;
    return n.toString(2).padStart(bits,'0');
  }).join(' ');
}
bin.addEventListener('input',function(){
  if(lock)return;lock=true;
  try{hex.value=this.value.trim()?binToHex(this.value):'';}
  catch(e){hex.value='(invalid binary groups)';}
  lock=false;
});
hex.addEventListener('input',function(){
  if(lock)return;lock=true;
  try{bin.value=this.value.trim()?hexToBin(this.value):'';}
  catch(e){bin.value='(invalid hex groups)';}
  lock=false;
});
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"binhex": lambda args: BINHEX,' not in t:
    t = t.replace('    "whitespace": lambda args: WHITESPACE,',
                  '    "whitespace": lambda args: WHITESPACE,\n    "binhex": lambda args: BINHEX,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("binhex registered:", '"binhex": lambda' in t)
