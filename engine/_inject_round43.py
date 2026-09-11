# -*- coding: utf-8 -*-
"""One-shot round 43: pages (mm-to-feet, volume-of-cylinder) + renderer. Safe to re-run."""
import io

# ---------- 1) pages.py ----------
p = "engine/pages.py"
s = io.open(p, encoding="utf-8").read()
anchor = "    # ---------- Index metadata used by build ----------"
assert anchor in s and s.count(anchor) == 1

new = '''    pages.append(_conv("mm-to-feet", "MM to Feet", "millimeters", "feet", 0.003280839895, "length",
                       "Metric engineering drawings meet American construction: convert millimeters to feet by dividing by 304.8. A 1,000 mm meter stick is 3.28 feet; a 2,438 mm sheet of plywood is exactly 8 feet.",
                       "Handy anchors: 300 mm = 0.98 ft (about a foot), 1,000 mm = 3.28 ft, 2,438 mm = 8 ft (a plywood sheet), 5,000 mm = 16.4 ft (a parking space)."))

    pages.append({
        "slug": "volume-of-cylinder",
        "title": "Volume of a Cylinder Calculator — pi x r2 x Height",
        "h1": "Volume of a Cylinder Calculator",
        "desc": "Calculate cylinder volume from radius and height: V = pi x r2 x h. Results in cubic units and liters/gallons for tanks, pipes and cans. Instant, with formula shown.",
        "category": "calculator",
        "keyword": "volume of a cylinder",
        "tool": "cylinder",
        "args": {},
        "intro": [
            "Enter the radius and height of a cylinder and get its volume instantly — in cubic units plus liters and US gallons, which is what water tanks, propane cylinders and rain barrels are actually sold in. The formula V = \\u03c0r\\u00b2h is shown with your numbers in place, so the homework answer and the intuition both arrive together.",
            "Cylinders are everywhere once you look: cans, pipes, wells, engines, candles. One formula covers them all.",
        ],
        "howto": [
            "Enter the radius of the circular base and the height of the cylinder.",
            "Read the volume in cubic units, then in liters and US gallons for real-world capacity.",
            "Use diameter instead of radius by halving it first — the calculator works in radius.",
        ],
        "faqs": [
            ("What is the formula for the volume of a cylinder?",
             "V = \\u03c0r\\u00b2h: pi times the radius squared, times the height. A cylinder with a 5 cm radius and 10 cm height holds about 785 cubic centimeters (0.785 liters)."),
            ("How many gallons is a 24-inch by 48-inch tank?",
             "Radius 12 in, height 48 in: V = \\u03c0 \\u00d7 144 \\u00d7 48 \\u2248 21,715 cubic inches \\u2248 94 gallons. The calculator handles the cubic-inch-to-gallon hop when you work in inches."),
            ("Does diameter work instead of radius?",
             "Yes, if you halve it first: a 20 cm diameter cylinder has a 10 cm radius. Entering the diameter as the radius overstates the volume by 4x - the most common mistake with this formula."),
            ("What is the volume of a cylinder in liters per cm of height?",
             "That is the cross-sectional area: \\u03c0r\\u00b2 cubic centimeters per centimeter of height. A 5 cm radius cylinder holds \\u03c0 \\u00d7 25 \\u2248 78.5 ml per centimeter - handy for rain gauges and graduations."),
        ],
    })

''' + anchor

if '"mm-to-feet"' not in s:
    s = s.replace(anchor, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("pages ok:", '"mm-to-feet"' in s, '"volume-of-cylinder"' in s)

# ---------- 2) tools.py ----------
p2 = "engine/tools.py"
t = io.open(p2, encoding="utf-8").read()

if '"cylinder"' not in t:
    js = '''
# ---------------------------------------------------------------- cylinder volume
CYLINDER = """
<div class="tool" id="tt-cy">
  <div class="fields">
    <div class="field"><label for="cy-r">Radius</label><input type="number" id="cy-r" step="any" min="0" placeholder="5"></div>
    <div class="field"><label for="cy-h">Height</label><input type="number" id="cy-h" step="any" min="0" placeholder="10"></div>
  </div>
  <div class="result"><span class="result-num" id="cy-out">-</span><span class="result-unit" id="cy-unit">cubic units</span></div>
  <div class="result"><span class="result-num" id="cy-liters">-</span><span class="result-unit">liters (if cm)</span></div>
  <div class="tool-note">V = \\u03c0r\\u00b2h - enter radius (not diameter) and height in the same unit.</div>
</div>
<script>(function(){
var r=document.getElementById('cy-r'),h=document.getElementById('cy-h');
function run(){
  var rr=parseFloat(r.value),hh=parseFloat(h.value);
  if(isNaN(rr)||isNaN(hh)){document.getElementById('cy-out').textContent='-';document.getElementById('cy-liters').textContent='-';return;}
  var v=Math.PI*rr*rr*hh;
  document.getElementById('cy-out').textContent=(Math.round(v*100)/100).toLocaleString('en-US');
  document.getElementById('cy-unit').textContent='cubic '+('units');
  document.getElementById('cy-liters').textContent=(Math.round(v/1000*1000)/1000).toLocaleString('en-US');
}
r.addEventListener('input',run);h.addEventListener('input',run);run();
})();</script>
"""


TOOLS = {'''
    t = t.replace("\nTOOLS = {", js, 1)
if '"cylinder": lambda args: CYLINDER,' not in t:
    t = t.replace('    "numwords": lambda args: NUMWORDS,',
                  '    "numwords": lambda args: NUMWORDS,\n    "cylinder": lambda args: CYLINDER,', 1)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("cylinder registered:", '"cylinder": lambda' in t)
