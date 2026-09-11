# -*- coding: utf-8 -*-
"""One-shot round 25: pages (gb-to-mb, pixels-to-inches) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("gb-to-mb", "GB to MB", "gigabytes", "megabytes", 1000, "storage",
                       "Storage makers use decimal gigabytes: 1 GB = 1,000 MB. Your operating system may display binary gibibytes (1 GiB = 1,024 MiB), which is why a '256 GB' drive shows as about 238 GiB in Windows — the drive is not lying, the units are different.",
                       "Handy anchors: 1 GB = 1,000 MB, 5 GB = 5,000 MB (a phone plan), 64 GB = 64,000 MB (a flash drive), 500 GB = 500,000 MB (a laptop SSD)."))
    pages.append(_conv("mb-to-gb", "MB to GB", "megabytes", "gigabytes", 1 / 1000, "storage",
                       "Convert megabytes to gigabytes by dividing by 1,000 — the decimal definition storage and telecom companies use. A 5,000 MB photo collection is 5 GB of cloud storage you did not know you needed.",
                       "Handy anchors: 100 MB = 0.1 GB (an app), 700 MB = 0.7 GB (a CD), 4,700 MB = 4.7 GB (a DVD), 50,000 MB = 50 GB (a video game)."))

    pages.append({
        "slug": "pixels-to-inches",
        "title": "Pixels to Inches Calculator — Print Size at Any DPI",
        "h1": "Pixels to Inches Calculator",
        "desc": "Convert pixels to inches for print or screen: enter pixel dimensions and DPI/PPI to get exact physical size. Includes print-quality DPI guidance.",
        "category": "calculator",
        "keyword": "pixels to inches",
        "tool": "pxin",
        "args": {},
        "intro": [
            "Pixels have no physical size until you give them a density: the same 3,000-pixel image is 10 inches wide at 300 DPI (print quality) or 31 inches at 96 DPI (a screen). Enter pixel dimensions and the DPI, and this calculator gives the exact physical width and height in inches and centimeters.",
            "The print rule of thumb: 300 DPI for photos in the hand, 150 DPI acceptable for posters viewed at arm's length, 96–72 DPI is screen territory. Work backwards from a target print size and the calculator tells you the pixel dimensions your camera or export needs.",
        ],
        "howto": [
            "Enter the pixel width and height of your image.",
            "Enter the DPI/PPI — 300 for photo prints, 150 for posters, 96 for screens.",
            "Read the physical size in inches and centimeters; adjust DPI to fit a target print size.",
        ],
        "faqs": [
            ("How do I convert pixels to inches?",
             "Divide the pixel count by the DPI (dots per inch). A 1,200-pixel-wide image at 300 DPI prints 4 inches wide: 1,200 ÷ 300 = 4. The calculator does this for width and height together."),
            ("What DPI should I use for printing photos?",
             "300 DPI is the photo-lab standard viewed at reading distance. 150 DPI works for posters and wall art viewed from a meter or more; large-format banners can go as low as 100 DPI."),
            ("How many pixels is an 8x10 print at 300 DPI?",
             "2,400 × 3,000 pixels — 7.2 megapixels. Any modern phone camera exceeds this, which is why phone photos generally print beautifully at ordinary sizes."),
            ("Why does my 4000-pixel image look blurry when printed?",
             "Because it was stretched beyond its pixel budget: at 4,000 pixels and 300 DPI the sharp size is 13.3 inches. Printing it at 20 inches means 200 DPI, and the softness you see is interpolation filling in pixels that were never captured."),
        ],
    })

''' + anchor

if '"gb-to-mb"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"gb-to-mb"' in s, '"pixels-to-inches"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"pxin"' not in t:
    js = '''
# ---------------------------------------------------------------- pixels <-> inches
PXIN = """
<div class="tool" id="tt-px">
  <div class="fields">
    <div class="field"><label for="px-w">Width (px)</label><input type="number" id="px-w" step="any" min="0" placeholder="3000"></div>
    <div class="field"><label for="px-h">Height (px)</label><input type="number" id="px-h" step="any" min="0" placeholder="2000"></div>
    <div class="field"><label for="px-dpi">DPI / PPI</label><input type="number" id="px-dpi" step="any" min="1" value="300"></div>
  </div>
  <div class="chips">
    <button class="chip" data-d="300">Print 300 DPI</button>
    <button class="chip" data-d="150">Poster 150</button>
    <button class="chip active" data-d="96">Screen 96</button>
  </div>
  <div class="result"><span class="result-num" id="px-out">-</span><span class="result-unit" id="px-unit"></span>
    <div class="result-formula" id="px-note"></div></div>
</div>
<script>(function(){
var w=document.getElementById('px-w'),h=document.getElementById('px-h'),dpi=document.getElementById('px-dpi');
function run(){
  var W=parseFloat(w.value),H=parseFloat(h.value),D=parseFloat(dpi.value);
  var o=document.getElementById('px-out'),u=document.getElementById('px-unit'),n=document.getElementById('px-note');
  if(!D||D<=0||isNaN(W)||isNaN(H)||!W||!H){o.textContent='-';u.textContent='';n.textContent='';return;}
  var wi=W/D,hi=H/D;
  o.textContent=Math.round(wi*100)/100+' x '+Math.round(hi*100)/100;
  u.textContent='inches';
  n.textContent=Math.round(wi*2.54*100)/100+' x '+Math.round(hi*2.54*100)/100+' cm  ('+W+'px / '+D+'dpi)';
}
[w,h,dpi].forEach(function(el){el.addEventListener('input',run);});
document.querySelectorAll('#tt-px .chip').forEach(function(c){c.addEventListener('click',function(){
  dpi.value=c.dataset.d;
  document.querySelectorAll('#tt-px .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  run();
});});
run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"pxin": lambda args: PXIN,' not in t:
    t = t.replace('    "secondsconv": lambda args: SECONDS,',
                  '    "secondsconv": lambda args: SECONDS,\n    "pxin": lambda args: PXIN,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("pxin registered:", '"pxin": lambda' in t)
