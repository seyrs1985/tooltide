# -*- coding: utf-8 -*-
"""One-shot: inject INCHFRAC renderer into tools.py. Safe to re-run."""
import io

p = "engine/tools.py"
t = io.open(p, encoding="utf-8").read()

if '"inchfrac"' in t:
    print("inchfrac already present")
    raise SystemExit(0)

js = '''
# ---------------------------------------------------------------- inch fraction
INCHFRAC = """
<div class="tool" id="tt-if">
  <div class="fields">
    <div class="field"><label for="if-frac">Fractional inches <small>(3/8 or 1-3/4)</small></label><input type="text" id="if-frac" placeholder="1-3/4"></div>
    <div class="field"><label for="if-dec">Decimal inches</label><input type="number" id="if-dec" step="any" min="0" placeholder="1.75"></div>
    <div class="field"><label for="if-mm">Millimeters</label><input type="number" id="if-mm" step="any" min="0" placeholder="44.45"></div>
  </div>
  <div class="result"><span class="result-num" id="if-out">-</span><span class="result-unit" id="if-unit"></span></div>
  <table class="copytable"><thead><tr><th>Fraction</th><th>Decimal</th><th>MM</th></tr></thead><tbody>
  <tr><td>1/8</td><td>0.125</td><td>3.175</td></tr><tr><td>1/4</td><td>0.25</td><td>6.35</td></tr>
  <tr><td>3/8</td><td>0.375</td><td>9.525</td></tr><tr><td>1/2</td><td>0.5</td><td>12.7</td></tr>
  <tr><td>5/8</td><td>0.625</td><td>15.875</td></tr><tr><td>3/4</td><td>0.75</td><td>19.05</td></tr>
  <tr><td>7/8</td><td>0.875</td><td>22.225</td></tr><tr><td>1</td><td>1.0</td><td>25.4</td></tr></tbody></table>
</div>
<script>(function(){
var F=document.getElementById('if-frac'),D=document.getElementById('if-dec'),M=document.getElementById('if-mm');
var out=document.getElementById('if-out'),unit=document.getElementById('if-unit');
var lock=false;
function parseFrac(v){
  v=v.trim().replace(/"/g,'');
  var m=v.match(/^(\\\\d+)?[- ]?(\\\\d+)\\\\/(\\\\d+)$/);
  if(m){var w=m[1]?+m[1]:0,d=+m[2],n=+m[3];return n?w+d/n:null;}
  var f=parseFloat(v);return isNaN(f)?null:f;
}
function toFrac(dec){
  var sixteenths=Math.round(dec*16),w=Math.floor(sixteenths/16),n=sixteenths%16;
  if(!n)return w+'';
  function gcd(a,b){return b?gcd(b,a%b):a;}
  var g=gcd(n,16);n/=g;var d=16/g;
  var f=n+'/'+d;
  return w?w+'-'+f:f;
}
F.addEventListener('input',function(){
  if(lock)return;lock=true;D.value='';M.value='';
  var v=parseFrac(F.value);
  if(v===null){out.textContent='-';unit.textContent='';lock=false;return;}
  D.value=Math.round(v*10000)/10000;M.value=Math.round(v*25.4*100)/100;
  out.textContent=v+' in = '+Math.round(v*25.4*100)/100+' mm';unit.textContent='';
  lock=false;
});
D.addEventListener('input',function(){
  if(lock)return;lock=true;F.value='';M.value='';
  var v=parseFloat(D.value);
  if(isNaN(v)){out.textContent='-';unit.textContent='';lock=false;return;}
  var f=toFrac(v);F.value=f;
  out.textContent=f+' in';unit.textContent='(nearest 1/16)';
  M.value=Math.round(v*25.4*100)/100;lock=false;
});
M.addEventListener('input',function(){
  if(lock)return;lock=true;F.value='';D.value='';
  var v=parseFloat(M.value);
  if(isNaN(v)){out.textContent='-';unit.textContent='';lock=false;return;}
  var i=v/25.4,f=toFrac(i);F.value=f;
  out.textContent=(Math.round(i*10000)/10000)+' in';unit.textContent='(nearest 1/16)';
  D.value=Math.round(i*10000)/10000;lock=false;
});
})();</script>
"""


TOOLS = {'''

t = t.replace("\nTOOLS = {", js, 1)
if '"inchfrac": lambda args: INCHFRAC,' not in t:
    t = t.replace('    "hoursdiff": lambda args: HOURSDIFF,',
                  '    "hoursdiff": lambda args: HOURSDIFF,\n    "inchfrac": lambda args: INCHFRAC,', 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("inchfrac registered:", '"inchfrac": lambda' in t)
