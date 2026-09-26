# -*- coding: utf-8 -*-
"""R134 存量质量轮:补课第二批9渲染器(title+localStorage+URL,ROMANTABLE静态表走事件委托复制+title)"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

# ---------- TYPING (typing-speed-test) ----------
sub("var dur=30,start=null,timer=null,ended=false;",
    """var dur=30,start=null,timer=null,ended=false;
try{var S=JSON.parse(localStorage.getItem('tt_type')||'null');if(S&&S.s){dur=+S.s;}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('s')){dur=parseInt(qs.get('s'),10)||30;}
var chipHit=document.querySelector('#tt-type .chip[data-s="'+dur+'"]');if(chipHit){document.querySelectorAll('#tt-type .chip[data-s]').forEach(function(x){x.classList.toggle('active',x===chipHit);});}""")

sub("  highlight(typed.length);",
    """  highlight(typed.length);
  document.title=net+' WPM, '+acc+'% accuracy - ToolDune';
  try{localStorage.setItem('tt_type',JSON.stringify({s:dur}));}catch(e){}""")

# ---------- BINARY (text-to-binary) ----------
sub("""var txt=document.getElementById('bin-txt'),code=document.getElementById('bin-code');
var lock=false;""",
    """var txt=document.getElementById('bin-txt'),code=document.getElementById('bin-code');
var lock=false;
try{var S=JSON.parse(localStorage.getItem('tt_bin')||'null');if(S&&S.t){txt.value=S.t.length>2000?S.t.slice(0,2000):S.t;code.value=txt.value?toBin(txt.value):'';}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('t')){txt.value=qs.get('t');code.value=txt.value?toBin(txt.value):'';}""")

sub("  code.value=this.value?toBin(this.value):'';",
    """  code.value=this.value?toBin(this.value):'';
  document.title=this.value?('Binary: '+new TextEncoder().encode(this.value).length+' bytes - ToolDune'):'Text to Binary - ToolDune';
  try{localStorage.setItem('tt_bin',JSON.stringify({t:this.value.slice(0,2000)}));}catch(e){}""")

# ---------- COINFLIP (coin-flip) ----------
sub("""var h=0,tt=0;
var face=document.getElementById('cf-face');""",
    """var h=0,tt=0;
var face=document.getElementById('cf-face');
try{var S=JSON.parse(localStorage.getItem('tt_coin')||'null');if(S){h=S.h|0;tt=S.t|0;}}catch(e){}
document.getElementById('cf-h').textContent=h;document.getElementById('cf-t').textContent=tt;document.getElementById('cf-n').textContent=h+tt;""")

sub("  document.getElementById('cf-n').textContent=h+tt;",
    """  document.getElementById('cf-n').textContent=h+tt;
  document.title='Coin: '+(r?'HEADS':'TAILS')+' - '+h+'H '+tt+'T - ToolDune';
  try{localStorage.setItem('tt_coin',JSON.stringify({h:h,t:tt}));}catch(e){}""")

# ---------- WORDFREQ (word-frequency-counter) ----------
sub("var hideStop=true;",
    """var hideStop=true;
try{var S=JSON.parse(localStorage.getItem('tt_wf')||'null');if(S){if(typeof S.h==='boolean'){hideStop=S.h;stop.classList.toggle('active',hideStop);}if(S.t){inp.value=S.t.length>20000?S.t.slice(0,20000):S.t;}}}catch(e){}""")

sub("""  tb.innerHTML=html||'<tr><td colspan="4" style="color:#94a3b8">Paste text to see word frequencies…</td></tr>';
}
inp.addEventListener('input',run);run();""",
    """  tb.innerHTML=html||'<tr><td colspan="4" style="color:#94a3b8">Paste text to see word frequencies…</td></tr>';
}
inp.addEventListener('input',run);run();
inp.addEventListener('input',function(){try{localStorage.setItem('tt_wf',JSON.stringify({t:inp.value.slice(0,20000),h:hideStop}));}catch(e){}var n=(inp.value.match(/[a-z0-9]+/gi)||[]).length;document.title=n?(n+' words analyzed - ToolDune'):'Word Frequency Counter - ToolDune';});
stop.addEventListener('click',function(){try{localStorage.setItem('tt_wf',JSON.stringify({t:inp.value.slice(0,20000),h:hideStop}));}catch(e){}});""")

# ---------- ROMANTABLE (roman-numerals-1-100, 静态表+事件委托复制) ----------
sub('<div class="tool-note">Seven symbols, one rule: smaller numeral before a larger one subtracts (IV = 4, XC = 90). Everything else adds.</div>',
    """  <div class="tool-note">Seven symbols, one rule: smaller numeral before a larger one subtracts (IV = 4, XC = 90). Everything else adds. Click any cell to copy.</div>
<script>(function(){
var tb=document.querySelector('#tt-rt100 tbody');if(!tb)return;
tb.addEventListener('click',function(ev){
  var td=ev.target.closest('td');if(!td)return;
  var parts=td.textContent.split('=');if(parts.length<2)return;
  var s=parts[0].trim()+' = '+parts[1].trim();
  try{navigator.clipboard.writeText(s);}catch(e){}
  var old=document.title;document.title='Copied '+s+' - ToolDune';
  setTimeout(function(){document.title=old;},1200);
});
})();</script>""")

# ---------- HEXRGB (hex-to-rgb) ----------
sub("""var HEX=document.getElementById('hr-hex'),R=document.getElementById('hr-r'),G=document.getElementById('hr-g'),B=document.getElementById('hr-b');
var prev=document.getElementById('hr-preview');
var lock=false;""",
    """var HEX=document.getElementById('hr-hex'),R=document.getElementById('hr-r'),G=document.getElementById('hr-g'),B=document.getElementById('hr-b');
var prev=document.getElementById('hr-preview');
var lock=false;
try{var S=JSON.parse(localStorage.getItem('tt_hexrgb')||'null');if(S&&S.x){HEX.value=S.x;var c0=hex2rgb(S.x);if(c0){R.value=c0.r;G.value=c0.g;B.value=c0.b;upd(c0.r,c0.g,c0.b);}}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('h')){HEX.value=qs.get('h');var c1=hex2rgb(qs.get('h'));if(c1){R.value=c1.r;G.value=c1.g;B.value=c1.b;upd(c1.r,c1.g,c1.b);}}""")

sub("  document.getElementById('hr-rgbout').textContent='rgb('+r+', '+g+', '+b+')';",
    """  document.getElementById('hr-rgbout').textContent='rgb('+r+', '+g+', '+b+')';
  document.title=hx+' = rgb('+r+', '+g+', '+b+') - ToolDune';
  try{localStorage.setItem('tt_hexrgb',JSON.stringify({x:hx}));}catch(e){}""")

# ---------- PLANETS (age-on-other-planets) ----------
sub("""  tb.innerHTML=html;
}
inp.addEventListener('input',run);run();""",
    """  tb.innerHTML=html;
}
function pTitle(){var age=parseFloat(inp.value);if(!isNaN(age)&&age>=0){var m=Math.round(age/0.2408467*100)/100;document.title='Age '+age+': '+m+' Mercury years - ToolDune';}else{document.title='Age on Other Planets - ToolDune';}}
try{var S=JSON.parse(localStorage.getItem('tt_planets')||'null');if(S&&S.a){inp.value=S.a;}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('a')){inp.value=qs.get('a');}
inp.addEventListener('input',function(){run();pTitle();try{localStorage.setItem('tt_planets',JSON.stringify({a:inp.value}));}catch(e){}});
run();pTitle();""")

# ---------- BINHEX (binary-to-hex) ----------
sub("""var bin=document.getElementById('bh-bin'),hex=document.getElementById('bh-hex');
var lock=false;""",
    """var bin=document.getElementById('bh-bin'),hex=document.getElementById('bh-hex');
var lock=false;
try{var S=JSON.parse(localStorage.getItem('tt_binhex')||'null');if(S&&S.b){bin.value=S.b.length>1000?S.b.slice(0,1000):S.b;try{hex.value=binToHex(bin.value);}catch(e){hex.value='';}}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('b')){bin.value=qs.get('b');try{hex.value=binToHex(bin.value);}catch(e){hex.value='';}}""")

sub("  try{hex.value=this.value.trim()?binToHex(this.value):'';}",
    """  try{hex.value=this.value.trim()?binToHex(this.value):'';}
  document.title=this.value.trim()?('Hex: '+hex.value.slice(0,40)+' - ToolDune'):'Binary to Hex - ToolDune';
  try{localStorage.setItem('tt_binhex',JSON.stringify({b:this.value.slice(0,1000)}));}catch(e){}""")

# ---------- MORSE (text-to-morse) ----------
sub("  code.value=this.value.trim()?toMorse(this.value):'';",
    """  code.value=this.value.trim()?toMorse(this.value):'';
  document.title=this.value.trim()?('Morse: '+code.value.slice(0,30)+' - ToolDune'):'Text to Morse - ToolDune';
  if(this.value.trim()&&this.value!=='SOS'){try{localStorage.setItem('tt_morse',JSON.stringify({t:this.value.slice(0,1000)}));}catch(e){}}""")

sub("""txt.value='SOS';
txt.dispatchEvent(new Event('input'));""",
    """var restored=false;
try{var S=JSON.parse(localStorage.getItem('tt_morse')||'null');if(S&&S.t){txt.value=S.t.length>1000?S.t.slice(0,1000):S.t;restored=true;}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('t')){txt.value=qs.get('t').slice(0,1000);restored=true;}
if(!restored){txt.value='SOS';}
txt.dispatchEvent(new Event('input'));""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R134 QA inject OK: 9 renderers, 16 anchors, ast passed")
