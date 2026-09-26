# -*- coding: utf-8 -*-
"""R131 存量质量轮:六个文本类老页渲染器级钩子补课(title+localStorage+URL,份额按钮不改HTML故跳过)"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

# ---------- PERCENT(percentage-calculator + percentage-increase 共用) ----------
sub("var mode=(A&&A.default)?A.default:0;",
    """var mode=(A&&A.default)?A.default:0;
try{var S=JSON.parse(localStorage.getItem('tt_percent')||'null');if(S){if(typeof S.m==='number'){mode=S.m;}if(S.v){for(var k in S.v){var el0=document.getElementById(k);if(el0){el0.value=S.v[k];}}}}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('m')){mode=parseInt(qs.get('m'),10)||0;}""")

sub("""['p0-a','p0-b','p1-a','p1-b','p2-a','p2-b'].forEach(function(id){document.getElementById(id).addEventListener('input',run);});
run();""",
    """function save(){try{var v={};['p0-a','p0-b','p1-a','p1-b','p2-a','p2-b'].forEach(function(id){var el=document.getElementById(id);if(el.value){v[id]=el.value;}});localStorage.setItem('tt_percent',JSON.stringify({m:mode,v:v}));}catch(e){}}
['p0-a','p0-b','p1-a','p1-b','p2-a','p2-b'].forEach(function(id){document.getElementById(id).addEventListener('input',function(){run();var f=document.getElementById('pc-formula').textContent;if(f){document.title=f.replace('Formula: ','')+' - ToolDune';}save();});});
run();""")

# ---------- TIP ----------
sub("var bill=document.getElementById('tip-bill'),split=document.getElementById('tip-split'),custom=document.getElementById('tip-custom');",
    """var bill=document.getElementById('tip-bill'),split=document.getElementById('tip-split'),custom=document.getElementById('tip-custom');
try{var S=JSON.parse(localStorage.getItem('tt_tip')||'null');if(S){if(S.b){bill.value=S.b;}if(S.n){split.value=S.n;}if(S.p){pct=S.p;var hit=document.querySelector('#tt-tip .chip[data-v="'+S.p+'"]');if(hit){document.querySelectorAll('#tt-tip .chip').forEach(function(x){x.classList.toggle('active',x===hit);});}else{custom.value=S.p;}}}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('b')){bill.value=qs.get('b');}if(qs.get('p')){pct=parseFloat(qs.get('p'))||18;}""")

sub("document.getElementById('tip-tipp').textContent=money(tip/n);",
    """document.getElementById('tip-tipp').textContent=money(tip/n);
  if(b>0){document.title='Tip '+money(tip)+' on $'+b+' - total '+money(total)+' - ToolDune';}
  try{localStorage.setItem('tt_tip',JSON.stringify({b:bill.value,n:split.value,p:pct}));}catch(e){}""")

# ---------- READINGTIME ----------
sub("""document.getElementById('rt-txt').addEventListener('input',run);
document.getElementById('rt-speed').addEventListener('change',run);run();""",
    """try{var S=JSON.parse(localStorage.getItem('tt_rt')||'null');if(S){if(S.t){document.getElementById('rt-txt').value=S.t.length>20000?S.t.slice(0,20000):S.t;}if(S.s){document.getElementById('rt-speed').value=S.s;}}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('sp')){document.getElementById('rt-speed').value=qs.get('sp');}
document.getElementById('rt-txt').addEventListener('input',run);
document.getElementById('rt-speed').addEventListener('change',run);
function rtMem(){try{localStorage.setItem('tt_rt',JSON.stringify({t:document.getElementById('rt-txt').value.slice(0,20000),s:document.getElementById('rt-speed').value}));}catch(e){}}
document.getElementById('rt-txt').addEventListener('input',function(){rtMem();var w=document.getElementById('rt-words').textContent;document.title=(w&&w!=='0')?(w+' words: '+document.getElementById('rt-read').textContent+' read - ToolDune'):'Reading Time Calculator - ToolDune';});
document.getElementById('rt-speed').addEventListener('change',rtMem);
run();""")

# ---------- WORDCOUNTER ----------
sub("document.getElementById('wc-txt').addEventListener('input',run);run();",
    """try{var S=JSON.parse(localStorage.getItem('tt_wc')||'null');if(S&&S.t){var tv=S.t.length>20000?S.t.slice(0,20000):S.t;document.getElementById('wc-txt').value=tv;}}catch(e){}
document.getElementById('wc-txt').addEventListener('input',run);run();
document.getElementById('wc-txt').addEventListener('input',function(){try{var t=document.getElementById('wc-txt').value;localStorage.setItem('tt_wc',JSON.stringify({t:t.length>20000?t.slice(0,20000):t}));}catch(e){}var w=document.getElementById('wc-w').textContent;document.title=(w&&w!=='0')?(w+' words - ToolDune'):'Word Counter - ToolDune';});""")

# ---------- CASE ----------
sub("document.querySelectorAll('#tt-case .chip').forEach(function(c){c.addEventListener('click',function(){out.value=F[c.dataset.c](inp.value);});});",
    """var LAST='upper';
try{var S=JSON.parse(localStorage.getItem('tt_case')||'null');if(S){if(S.t){inp.value=S.t.length>20000?S.t.slice(0,20000):S.t;}if(S.m&&F[S.m]){LAST=S.m;}}}catch(e){}
document.querySelectorAll('#tt-case .chip').forEach(function(c){c.addEventListener('click',function(){out.value=F[c.dataset.c](inp.value);LAST=c.dataset.c;try{localStorage.setItem('tt_case',JSON.stringify({m:LAST,t:inp.value.slice(0,20000)}));}catch(e){}document.title='Case: '+LAST+' - ToolDune';});});
document.getElementById('case-in').addEventListener('input',function(){out.value=F[LAST](inp.value);try{localStorage.setItem('tt_case',JSON.stringify({m:LAST,t:inp.value.slice(0,20000)}));}catch(e){}});
if(inp.value){out.value=F[LAST](inp.value);document.title='Case: '+LAST+' - ToolDune';}""")

# ---------- SALARY ----------
sub("""var yr=document.getElementById('sal-yr'),hr=document.getElementById('sal-hr');
var hpw=document.getElementById('sal-hpw'),wpy=document.getElementById('sal-wpy');
var lock=false;""",
    """var yr=document.getElementById('sal-yr'),hr=document.getElementById('sal-hr');
var hpw=document.getElementById('sal-hpw'),wpy=document.getElementById('sal-wpy');
var lock=false;
try{var S=JSON.parse(localStorage.getItem('tt_sal')||'null');if(S){if(S.yr){yr.value=S.yr;}if(S.hr){hr.value=S.hr;}if(S.hpw){hpw.value=S.hpw;}if(S.wpy){wpy.value=S.wpy;}}}catch(e){}
var qs=new URLSearchParams(location.search);if(qs.get('y')){yr.value=qs.get('y');runY();}if(qs.get('h')){hr.value=qs.get('h');runH();}
if(yr.value){runY();}else if(hr.value){runH();}""")

sub("""  document.getElementById('sal-h').textContent=money(y/h);
  lock=false;
}""",
    """  document.getElementById('sal-h').textContent=money(y/h);
  document.title='$'+Math.round(y).toLocaleString()+' a year = '+money(y/h)+'/hour - ToolDune';
  try{localStorage.setItem('tt_sal',JSON.stringify({yr:yr.value,hpw:hpw.value,wpy:wpy.value}));}catch(e){}
  lock=false;
}""")

sub("""  document.getElementById('sal-h').textContent=money(r);
  lock=false;
}""",
    """  document.getElementById('sal-h').textContent=money(r);
  document.title=money(r)+'/hour = $'+Math.round(y).toLocaleString()+' a year - ToolDune';
  try{localStorage.setItem('tt_sal',JSON.stringify({hr:hr.value,hpw:hpw.value,wpy:wpy.value}));}catch(e){}
  lock=false;
}""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R131 QA inject OK: 6 renderers, 11 anchors, ast passed")
