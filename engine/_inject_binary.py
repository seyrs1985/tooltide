# -*- coding: utf-8 -*-
"""One-shot: inject BINARY renderer into tools.py. Safe to re-run."""
import io

p = "engine/tools.py"
t = io.open(p, encoding="utf-8").read()

if '"binary": lambda' in t:
    print("binary already present")
    raise SystemExit(0)

js = '''
# ---------------------------------------------------------------- text <-> binary
BINARY = """
<div class="tool" id="tt-bin">
  <div class="field"><label for="bin-txt">Text</label>
    <textarea id="bin-txt" rows="4" placeholder="Hi"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="bin-code">Binary (UTF-8, space-separated bytes)</label>
    <textarea id="bin-code" rows="4" placeholder="01001000 01101001"></textarea></div>
</div>
<script>(function(){
var txt=document.getElementById('bin-txt'),code=document.getElementById('bin-code');
var lock=false;
function toBin(s){
  var bytes=new TextEncoder().encode(s);
  return Array.from(bytes).map(function(b){return b.toString(2).padStart(8,'0');}).join(' ');
}
function fromBin(v){
  var parts=v.trim().split(/\\s+/).filter(Boolean),bytes=[];
  for(var i=0;i<parts.length;i++){
    if(!/^[01]{1,8}$/.test(parts[i]))throw 'bad';
    bytes.push(parseInt(parts[i],2));
  }
  return new TextDecoder().decode(new Uint8Array(bytes));
}
txt.addEventListener('input',function(){
  if(lock)return;lock=true;
  code.value=this.value?toBin(this.value):'';
  lock=false;
});
code.addEventListener('input',function(){
  if(lock)return;lock=true;
  try{txt.value=this.value.trim()?fromBin(this.value):'';}
  catch(e){txt.value='(invalid binary - bytes must be 1-8 bits of 0/1)';}
  lock=false;
});
})();</script>
"""


TOOLS = {'''

t = t.replace("\nTOOLS = {", js, 1)
if '"binary": lambda args: BINARY,' not in t:
    t = t.replace('    "average": lambda args: AVERAGE,',
                  '    "average": lambda args: AVERAGE,\n    "binary": lambda args: BINARY,', 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("binary registered:", '"binary": lambda' in t)
