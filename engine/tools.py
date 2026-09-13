# -*- coding: utf-8 -*-
"""Interactive tool renderers for ToolTide.

Each renderer returns HTML + inline vanilla JS. Arguments are injected via the
__ARGS__ placeholder (replaced by build.py with a JSON object), which keeps the
JavaScript free of Python string-formatting braces.
"""

import json


def _args(args):
    return json.dumps(args, ensure_ascii=False)


# ---------------------------------------------------------------- countdown
COUNTDOWN = """
<div class="tool" id="tt-cd">
  <div class="cd-event"><span id="cd-emoji"></span><span id="cd-name"></span></div>
  <div class="cd-big" id="cd-days">–</div>
  <div class="cd-big-label" id="cd-days-label">days to go</div>
  <div class="cd-clock" id="cd-clock">–</div>
  <div class="stats">
    <div class="stat"><b id="cd-weeks">–</b><span>weeks</span></div>
    <div class="stat"><b id="cd-hours">–</b><span>total hours</span></div>
    <div class="stat"><b id="cd-date">–</b><span>the date</span></div>
    <div class="stat" id="cd-today-box" style="display:none"><b>🎉</b><span>It's today!</span></div>
  </div>
</div>
<script>(function(){
var A=__ARGS__;
var m=A.month, d=A.day, rule=A.rule||null;
document.getElementById('cd-emoji').textContent=A.emoji||'📅';
document.getElementById('cd-name').textContent=A.event;
function daysInMonth(y,mo){return new Date(y,mo+1,0).getDate();}
function nthWeekday(y,mo,week,weekday){ // weekday: 0=Sun..6=Sat
  var count=0;
  for(var day=1;day<=daysInMonth(y,mo);day++){
    var dt=new Date(y,mo,day);
    if(dt.getDay()===weekday){count++;if(count===week)return new Date(y,mo,day,0,0,0);}
  }
  return null;
}
function easterSunday(y){ // Anonymous Gregorian computus
  var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,mm=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*mm+114)/31),da=((h+l-7*mm+114)%31)+1;
  return new Date(y,mo-1,da,0,0,0);
}
function nextWeekly(y){
  var now=new Date();
  var t=new Date(now.getFullYear(),now.getMonth(),now.getDate(),0,0,0);
  var delta=(rule.weekday-t.getDay()+7)%7;
  if(delta===0)delta=7;
  t.setDate(t.getDate()+delta);
  return t;
}
function candidate(y){
  if(rule){ if(rule.easter)return easterSunday(y); if(rule.weekly)return nextWeekly(y); return nthWeekday(y,m-1,rule.week,rule.weekday); }
  return new Date(y,m-1,d,0,0,0);
}
function sameDay(a,b){return a.getFullYear()===b.getFullYear()&&a.getMonth()===b.getMonth()&&a.getDate()===b.getDate();}
function target(){
  var now=new Date(),y=now.getFullYear();
  var t=candidate(y);
  if(t===null){t=candidate(y+1);}
  if(sameDay(t,now))return {t:new Date(t.getTime()+86400000),today:true,cand:t};
  if(t<=now){y++;t=candidate(y);if(t===null)t=candidate(y+1);}
  return {t:t,today:false,cand:t};
}
var el=function(id){return document.getElementById(id);};
function pad(n){return (n<10?'0':'')+n;}
function tick(){
  var r=target(),now=new Date(),diff=r.t-now;
  if(diff<0)diff=0;
  var days=Math.floor(diff/86400000);
  var hours=Math.floor(diff/3600000)%24, mins=Math.floor(diff/60000)%60, secs=Math.floor(diff/1000)%60;
  var real=r.today?0:days;
  el('cd-days').textContent=real;
  el('cd-days-label').textContent=r.today?("It's "+A.event+" today! 🎉"):('days to go');
  el('cd-clock').textContent=pad(hours)+':'+pad(mins)+':'+pad(secs)+'  h:m:s remaining today';
  el('cd-clock').style.display=r.today?'none':'block';
  el('cd-weeks').textContent=(diff/604800000).toFixed(1);
  el('cd-hours').textContent=Math.floor(diff/3600000).toLocaleString('en-US');
  el('cd-date').textContent=r.cand.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'});
  el('cd-today-box').style.display=r.today?'block':'none';
  document.title=(real>0?real+'d to '+A.event:A.event)+' - ToolTide';
}
tick();setInterval(tick,1000);
})();</script>
"""


# ---------------------------------------------------------------- date diff
DATEDIFF = """
<div class="tool" id="tt-dd">
  <div class="fields">
    <div class="field"><label for="dd-a">Start date</label><input type="date" id="dd-a"></div>
    <div class="field"><label for="dd-b">End date</label><input type="date" id="dd-b"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dd-days">–</span><span class="result-unit">days</span>
    <div class="result-formula" id="dd-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="dd-weeks">–</b><span>weeks &amp; days</span></div>
    <div class="stat"><b id="dd-wd">–</b><span>weekdays (Mon–Fri)</span></div>
    <div class="stat"><b id="dd-hours">–</b><span>total hours</span></div>
  </div>
</div>
<script>(function(){
var a=document.getElementById('dd-a'),b=document.getElementById('dd-b');
function iso(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
var t=new Date();a.value=iso(t);b.value=iso(new Date(t.getTime()+12096e5));
function run(){
  if(!a.value||!b.value)return;
  var d1=new Date(a.value+'T00:00:00'),d2=new Date(b.value+'T00:00:00');
  var sign=d2<d1?-1:1,lo=sign<0?d2:d1,hi=sign<0?d1:d2;
  var days=Math.round((hi-lo)/864e5);
  document.getElementById('dd-days').textContent=sign*days;
  var w=Math.floor(days/7),rd=days%7;
  document.getElementById('dd-weeks').textContent=w+(rd===1?' week + 1 day':' weeks + '+rd+' days');
  var wd=0,cur=new Date(lo);
  if(days<=500000){for(var i=0;i<days;i++){cur.setDate(cur.getDate()+1);var g=cur.getDay();if(g!==0&&g!==6)wd++;}}
  document.getElementById('dd-wd').textContent=days>500000?'—':wd;
  document.getElementById('dd-hours').textContent=(days*24).toLocaleString('en-US');
  var opts={weekday:'long',year:'numeric',month:'long',day:'numeric'};
  document.getElementById('dd-note').textContent=lo.toLocaleDateString('en-US',opts)+'  →  '+hi.toLocaleDateString('en-US',opts);
}
a.addEventListener('input',run);b.addEventListener('input',run);run();
try{
  var mem=JSON.parse(localStorage.getItem('tt_datediff')||'null');
  if(mem&&mem.a&&mem.b){a.value=mem.a;b.value=mem.b;run();}
  setInterval(function(){try{localStorage.setItem('tt_datediff',JSON.stringify({a:a.value,b:b.value}));}catch(e){}},2000);
}catch(e){}
})();</script>
"""


# ---------------------------------------------------------------- age
AGE = """
<div class="tool" id="tt-age">
  <div class="fields">
    <div class="field"><label for="age-b">Date of birth</label><input type="date" id="age-b"></div>
    <div class="field"><label for="age-a">Age at date</label><input type="date" id="age-a"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="age-main">–</span>
    <div class="result-formula" id="age-total"></div></div>
  <div class="stats">
    <div class="stat"><b id="age-days">–</b><span>days lived</span></div>
    <div class="stat"><b id="age-hours">–</b><span>hours lived</span></div>
    <div class="stat"><b id="age-next">–</b><span>days to next birthday</span></div>
  </div>
</div>
<script>(function(){
var bi=document.getElementById('age-b'),ai=document.getElementById('age-a');
var t=new Date();ai.value=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
function dim(y,mo){return new Date(y,mo+1,0).getDate();}
function run(){
  if(!bi.value||!ai.value)return;
  var b=new Date(bi.value+'T00:00:00'),a=new Date(ai.value+'T00:00:00');
  if(b>a){document.getElementById('age-main').textContent='Birth date must be before the target date';document.getElementById('age-total').textContent='';return;}
  var y=a.getFullYear()-b.getFullYear(),mo=a.getMonth()-b.getMonth(),d=a.getDate()-b.getDate();
  if(d<0){mo--;d+=dim(a.getFullYear(),a.getMonth()-1);}
  if(mo<0){y--;mo+=12;}
  var s=y+(y===1?' year':' years')+', '+mo+(mo===1?' month':' months')+', '+d+(d===1?' day':' days');
  document.getElementById('age-main').textContent=s;
  var totalDays=Math.floor((a-b)/864e5);
  document.getElementById('age-total').textContent=totalDays.toLocaleString('en-US')+' days in total';
  document.getElementById('age-days').textContent=totalDays.toLocaleString('en-US');
  document.getElementById('age-hours').textContent=(totalDays*24).toLocaleString('en-US');
  var nb=new Date(a.getFullYear(),b.getMonth(),b.getDate());
  if(b.getMonth()===1&&b.getDate()===29&&!dim(a.getFullYear(),1)===29){nb=new Date(a.getFullYear(),1,28);}
  var today=new Date(a.getFullYear(),a.getMonth(),a.getDate());
  if(nb<=today)nb=new Date(a.getFullYear()+1,b.getMonth(),b.getDate());
  document.getElementById('age-next').textContent=Math.round((nb-today)/864e5);
}
bi.addEventListener('input',run);ai.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- percentage
PERCENT = """
<div class="tool" id="tt-pc">
  <div class="chips" role="tablist">
    <button class="chip active" data-t="0">X% of Y</button>
    <button class="chip" data-t="1">X is what % of Y</button>
    <button class="chip" data-t="2">% change X → Y</button>
  </div>
  <div class="pane" data-p="0">
    <div class="inline"><input type="number" id="p0-a" step="any" placeholder="20"> <span class="pct">%</span>
      <span class="of">of</span> <input type="number" id="p0-b" step="any" placeholder="150"> <span>=</span>
      <b id="p0-r">–</b></div>
  </div>
  <div class="pane" data-p="1" style="display:none">
    <div class="inline"><input type="number" id="p1-a" step="any" placeholder="15"> <span class="of">is what % of</span>
      <input type="number" id="p1-b" step="any" placeholder="60"> <span>=</span>
      <b id="p1-r">–</b><span class="pct2">%</span></div>
  </div>
  <div class="pane" data-p="2" style="display:none">
    <div class="inline"><input type="number" id="p2-a" step="any" placeholder="80"> <span class="of">→</span>
      <input type="number" id="p2-b" step="any" placeholder="100"> <span>=</span>
      <b id="p2-r">–</b></div>
  </div>
  <div class="tool-note" id="pc-formula"></div>
</div>
<script>(function(){
var A;try{A=JSON.parse('__ARGS__');}catch(e){A={};}
var mode=(A&&A.default)?A.default:0;
var chips=document.querySelectorAll('#tt-pc .chip');
chips.forEach(function(c){c.classList.toggle('active',+c.dataset.t===mode);});
document.querySelectorAll('#tt-pc .pane').forEach(function(p){p.style.display=+p.dataset.p===mode?'block':'none';});
chips.forEach(function(c){c.addEventListener('click',function(){
  mode=+c.dataset.t;
  chips.forEach(function(x){x.classList.toggle('active',x===c);});
  document.querySelectorAll('#tt-pc .pane').forEach(function(p){p.style.display=+p.dataset.p===mode?'block':'none';});
  run();
});});
function num(id){var v=document.getElementById(id).value;return v===''?null:parseFloat(v);}
function fmt(n){return (Math.round(n*1e6)/1e6).toLocaleString('en-US',{maximumFractionDigits:6});}
function run(){
  var f=document.getElementById('pc-formula');
  if(mode===0){var a=num('p0-a'),b=num('p0-b');
    document.getElementById('p0-r').textContent=(a!==null&&b!==null)?fmt(a/100*b):'–';
    f.textContent=(a!==null&&b!==null)?('Formula: '+a+'% × '+b+' = '+a+' ÷ 100 × '+b+' = '+fmt(a/100*b)):'';}
  else if(mode===1){var a=num('p1-a'),b=num('p1-b');
    var r=(a!==null&&b)?a/b*100:null;
    document.getElementById('p1-r').textContent=r===null?'–':fmt(r);
    f.textContent=(r!==null)?('Formula: '+a+' ÷ '+b+' × 100 = '+fmt(r)+'%'):'';}
  else{var a=num('p2-a'),b=num('p2-b');
    var r=(a!==null&&a!==0&&b!==null)?(b-a)/Math.abs(a)*100:null;
    document.getElementById('p2-r').textContent=r===null?'–':(fmt(Math.abs(r))+'% '+(r>=0?'increase':'decrease'));
    f.textContent=(r!==null)?('Formula: ('+b+' − '+a+') ÷ '+Math.abs(a)+' × 100 = '+fmt(r)+'%'):'';}
}
['p0-a','p0-b','p1-a','p1-b','p2-a','p2-b'].forEach(function(id){document.getElementById(id).addEventListener('input',run);});
run();
})();</script>
"""


# ---------------------------------------------------------------- tip
TIP = """
<div class="tool" id="tt-tip">
  <div class="fields">
    <div class="field"><label for="tip-bill">Bill amount ($)</label><input type="number" id="tip-bill" step="0.01" min="0" placeholder="84.50"></div>
    <div class="field"><label for="tip-split">Split between</label><input type="number" id="tip-split" min="1" step="1" value="1"></div>
  </div>
  <div class="chips" id="tip-chips">
    <button class="chip" data-v="10">10%</button>
    <button class="chip" data-v="15">15%</button>
    <button class="chip active" data-v="18">18%</button>
    <button class="chip" data-v="20">20%</button>
    <button class="chip" data-v="25">25%</button>
    <input type="number" id="tip-custom" step="1" min="0" max="100" placeholder="custom %">
  </div>
  <div class="stats">
    <div class="stat"><b id="tip-amt">–</b><span>tip</span></div>
    <div class="stat"><b id="tip-total">–</b><span>total</span></div>
    <div class="stat"><b id="tip-pp">–</b><span>per person</span></div>
    <div class="stat"><b id="tip-tipp">–</b><span>tip / person</span></div>
  </div>
</div>
<script>(function(){
var pct=18;
var bill=document.getElementById('tip-bill'),split=document.getElementById('tip-split'),custom=document.getElementById('tip-custom');
document.querySelectorAll('#tt-tip .chip').forEach(function(c){c.addEventListener('click',function(){
  pct=+c.dataset.v;custom.value='';
  document.querySelectorAll('#tt-tip .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  run();
});});
custom.addEventListener('input',function(){
  if(custom.value==='')return;
  pct=parseFloat(custom.value)||0;
  document.querySelectorAll('#tt-tip .chip').forEach(function(x){x.classList.remove('active');});
  run();
});
function money(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function run(){
  var b=parseFloat(bill.value)||0,n=Math.max(1,parseInt(split.value)||1);
  var tip=b*pct/100,total=b+tip;
  document.getElementById('tip-amt').textContent=money(tip);
  document.getElementById('tip-total').textContent=money(total);
  document.getElementById('tip-pp').textContent=money(total/n);
  document.getElementById('tip-tipp').textContent=money(tip/n);
}
bill.addEventListener('input',run);split.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- discount
DISCOUNT = """
<div class="tool" id="tt-disc">
  <div class="fields">
    <div class="field"><label for="dc-price">Original price ($)</label><input type="number" id="dc-price" step="0.01" min="0" placeholder="120"></div>
    <div class="field"><label for="dc-d1">Discount %</label><input type="number" id="dc-d1" step="any" min="0" max="100" placeholder="30"></div>
    <div class="field"><label for="dc-d2">Extra discount % <small>(optional)</small></label><input type="number" id="dc-d2" step="any" min="0" max="100" placeholder="20"></div>
    <div class="field"><label for="dc-tax">Tax % <small>(optional)</small></label><input type="number" id="dc-tax" step="any" min="0" placeholder="8.5"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dc-final">–</span><span class="result-unit">final price</span>
    <div class="result-formula" id="dc-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="dc-save">–</b><span>you save</span></div>
    <div class="stat"><b id="dc-eff">–</b><span>effective discount</span></div>
    <div class="stat"><b id="dc-taxp">–</b><span>with tax</span></div>
  </div>
</div>
<script>(function(){
['dc-price','dc-d1','dc-d2','dc-tax'].forEach(function(id){document.getElementById(id).addEventListener('input',run);});
function money(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function run(){
  var p=parseFloat(document.getElementById('dc-price').value)||0;
  var d1=parseFloat(document.getElementById('dc-d1').value)||0;
  var d2v=document.getElementById('dc-d2').value,d2=d2v===''?null:(parseFloat(d2v)||0);
  var taxv=document.getElementById('dc-tax').value,tax=taxv===''?null:(parseFloat(taxv)||0);
  var eff=(100-d1)/100, note='';
  if(d2!==null){eff*= (100-d2)/100; note='Stacked: ×'+((100-d1)/100).toFixed(4)+' ×'+((100-d2)/100).toFixed(4)+' = '+eff.toFixed(4)+' of original (NOT '+(d1+d2)+'% off)';}
  else{note='Formula: '+p+' × '+(eff.toFixed(4))+' after '+(100-eff*100)+'% off';}
  var final=p*eff, save=p-final;
  document.getElementById('dc-final').textContent=p?money(final):'–';
  document.getElementById('dc-save').textContent=money(save);
  document.getElementById('dc-eff').textContent=(eff*100).toFixed(2)+'% of original';
  document.getElementById('dc-taxp').textContent=(p&&tax!==null)?money(final*(1+tax/100)):'—';
  document.getElementById('dc-note').textContent=p?note:'';
}
run();
})();</script>
"""


# ---------------------------------------------------------------- reading time
READINGTIME = """
<div class="tool" id="tt-rt">
  <div class="field"><label for="rt-txt">Paste your text</label>
    <textarea id="rt-txt" rows="8" placeholder="Paste an article, script or email here…"></textarea></div>
  <div class="fields">
    <div class="field"><label for="rt-speed">Reading speed</label>
      <select id="rt-speed">
        <option value="150">Slow — 150 wpm</option>
        <option value="225" selected>Average — 225 wpm</option>
        <option value="300">Fast — 300 wpm</option>
      </select></div>
  </div>
  <div class="stats">
    <div class="stat"><b id="rt-read">–</b><span>to read silently</span></div>
    <div class="stat"><b id="rt-speak">–</b><span>to read aloud</span></div>
    <div class="stat"><b id="rt-words">–</b><span>words</span></div>
    <div class="stat"><b id="rt-chars">–</b><span>characters</span></div>
  </div>
</div>
<script>(function(){
function dur(min){if(!isFinite(min)||min<=0)return '–';var s=Math.round(min*60);var m=Math.floor(s/60);s=s%60;return m>0?(m+' min '+(s>0?s+' sec':'')):(s+' sec');}
function run(){
  var t=document.getElementById('rt-txt').value;
  var w=t.trim()?t.trim().split(/\\s+/).length:0;
  var speed=parseFloat(document.getElementById('rt-speed').value)||225;
  document.getElementById('rt-read').textContent=dur(w/speed);
  document.getElementById('rt-speak').textContent=dur(w/140);
  document.getElementById('rt-words').textContent=w.toLocaleString('en-US');
  document.getElementById('rt-chars').textContent=t.length.toLocaleString('en-US');
}
document.getElementById('rt-txt').addEventListener('input',run);
document.getElementById('rt-speed').addEventListener('change',run);run();
})();</script>
"""


# ---------------------------------------------------------------- word counter
WORDCOUNTER = """
<div class="tool" id="tt-wc">
  <div class="field"><label for="wc-txt">Type or paste text</label>
    <textarea id="wc-txt" rows="9" placeholder="Start typing — counts update live. Nothing leaves your browser."></textarea></div>
  <div class="stats">
    <div class="stat"><b id="wc-w">0</b><span>words</span></div>
    <div class="stat"><b id="wc-c">0</b><span>characters</span></div>
    <div class="stat"><b id="wc-cns">0</b><span>chars (no spaces)</span></div>
    <div class="stat"><b id="wc-s">0</b><span>sentences</span></div>
    <div class="stat"><b id="wc-p">0</b><span>paragraphs</span></div>
    <div class="stat"><b id="wc-rt">–</b><span>reading time</span></div>
  </div>
</div>
<script>(function(){
function run(){
  var t=document.getElementById('wc-txt').value;
  var w=t.trim()?t.trim().split(/\\s+/).length:0;
  var sents=(t.match(/[^.!?]+[.!?]+(\\s|$)|[^.!?]+$/g)||[]).filter(function(s){return s.trim();}).length;
  var paras=t.split(/\\n+/).filter(function(p){return p.trim();}).length;
  document.getElementById('wc-w').textContent=w.toLocaleString('en-US');
  document.getElementById('wc-c').textContent=t.length.toLocaleString('en-US');
  document.getElementById('wc-cns').textContent=t.replace(/\\s/g,'').length.toLocaleString('en-US');
  document.getElementById('wc-s').textContent=sents.toLocaleString('en-US');
  document.getElementById('wc-p').textContent=paras.toLocaleString('en-US');
  var m=w/225;
  document.getElementById('wc-rt').textContent=m<1?Math.max(1,Math.round(m*60))+' sec':(Math.round(m*10)/10)+' min';
}
document.getElementById('wc-txt').addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- case converter
CASE = """
<div class="tool" id="tt-case">
  <div class="field"><label for="case-in">Your text</label>
    <textarea id="case-in" rows="6" placeholder="Type or paste text…"></textarea></div>
  <div class="chips">
    <button class="chip" data-c="upper">UPPERCASE</button>
    <button class="chip" data-c="lower">lowercase</button>
    <button class="chip" data-c="title">Title Case</button>
    <button class="chip" data-c="sentence">Sentence case</button>
    <button class="chip" data-c="camel">camelCase</button>
    <button class="chip" data-c="snake">snake_case</button>
    <button class="chip" data-c="kebab">kebab-case</button>
    <button class="chip" data-c="alt">aLtErNaTiNg</button>
  </div>
  <div class="field"><label for="case-out">Result <button class="btn btn-sm" id="case-copy" type="button">Copy</button></label>
    <textarea id="case-out" rows="6" readonly placeholder="Click a case above…"></textarea></div>
</div>
<script>(function(){
var SMALL=['a','an','and','as','at','but','by','for','if','in','nor','of','on','or','per','the','to','v','via','vs'];
function words(t){return t.trim().split(/\\s+/).filter(Boolean);}
function toWords(t){return t.replace(/([a-z0-9])([A-Z])/g,'$1 $2').split(/[^A-Za-z0-9]+/).filter(Boolean);}
var F={
 upper:function(t){return t.toUpperCase();},
 lower:function(t){return t.toLowerCase();},
 title:function(t){return words(t).map(function(w,i){
   var lw=w.toLowerCase();
   if(i>0&&SMALL.indexOf(lw)>=0)return lw;
   return lw.charAt(0).toUpperCase()+lw.slice(1);}).join(' ');},
 sentence:function(t){return t.toLowerCase().replace(/(^\\s*[a-z])|([.!?]\\s+[a-z])/g,function(m){return m.toUpperCase();});},
 camel:function(t){return toWords(t).map(function(w,i){return i===0?w.toLowerCase():w.charAt(0).toUpperCase()+w.slice(1).toLowerCase();}).join('');},
 snake:function(t){return toWords(t).join('_').toLowerCase();},
 kebab:function(t){return toWords(t).join('-').toLowerCase();},
 alt:function(t){var n=0;return t.split('').map(function(ch){return /[a-z]/i.test(ch)?(n++%2?ch.toLowerCase():ch.toUpperCase()):ch;}).join('');}
};
var inp=document.getElementById('case-in'),out=document.getElementById('case-out');
document.querySelectorAll('#tt-case .chip').forEach(function(c){c.addEventListener('click',function(){out.value=F[c.dataset.c](inp.value);});});
document.getElementById('case-copy').addEventListener('click',function(){
  out.select();document.execCommand('copy');
  var b=document.getElementById('case-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
})();</script>
"""


# ---------------------------------------------------------------- aspect ratio
ASPECT = """
<div class="tool" id="tt-ar">
  <div class="chips" id="ar-presets">
    <button class="chip" data-r="16,9">16:9</button>
    <button class="chip" data-r="4,3">4:3</button>
    <button class="chip" data-r="1,1">1:1</button>
    <button class="chip" data-r="9,16">9:16</button>
    <button class="chip" data-r="21,9">21:9</button>
    <button class="chip" data-r="3,2">3:2</button>
  </div>
  <div class="fields">
    <div class="field"><label for="ar-rw">Ratio W</label><input type="number" id="ar-rw" value="16" min="1" step="any"></div>
    <div class="field"><label for="ar-rh">Ratio H</label><input type="number" id="ar-rh" value="9" min="1" step="any"></div>
    <div class="field"><label for="ar-w">Width (px)</label><input type="number" id="ar-w" min="1" step="any" placeholder="1920"></div>
    <div class="field"><label for="ar-h">Height (px)</label><input type="number" id="ar-h" min="1" step="any" placeholder="→ 1080"></div>
  </div>
  <div class="tool-note">Type either width or height — the other dimension fills in to keep the ratio. Or type both to detect the ratio you have.</div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ar-out">–</span><span class="result-unit" id="ar-out-unit"></span>
    <div class="result-formula" id="ar-detect"></div></div>
</div>
<script>(function(){
var rw=document.getElementById('ar-rw'),rh=document.getElementById('ar-rh');
var w=document.getElementById('ar-w'),h=document.getElementById('ar-h');
document.querySelectorAll('#ar-presets .chip').forEach(function(c){c.addEventListener('click',function(){
  var r=c.dataset.r.split(',');rw.value=r[0];rh.value=r[1];
  document.querySelectorAll('#ar-presets .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  run();
});});
function gcd(a,b){return b?gcd(b,a%b):a;}
function run(){
  var R=parseFloat(rw.value),R2=parseFloat(rh.value);
  var W=w.value===''?null:parseFloat(w.value),H=h.value===''?null:parseFloat(h.value);
  var out=document.getElementById('ar-out'),unit=document.getElementById('ar-out-unit'),det=document.getElementById('ar-detect');
  if(R>0&&R2>0&&W&&!H){var hh=W*R2/R;h.placeholder='→ '+Math.round(hh);out.textContent=Math.round(hh);unit.textContent='height for width '+W;}
  else if(R>0&&R2>0&&H&&!W){var ww=H*R/R2;w.placeholder='→ '+Math.round(ww);out.textContent=Math.round(ww);unit.textContent='width for height '+H;}
  else{out.textContent='–';unit.textContent='';}
  if(W&&H&&R&&R2){var g=gcd(Math.round(W),Math.round(H))||1;det.textContent='Your dimensions '+W+'×'+H+' = ratio '+(Math.round(W)/g)+':'+(Math.round(H)/g)+(Math.abs(W/H-R/R2)<0.001?'  ✓ matches '+R+':'+R2:'  (you entered both W and H — clear one to calculate)');}
  else{det.textContent='';}
}
[rw,rh,w,h].forEach(function(el){el.addEventListener('input',run);});run();
})();</script>
"""


# ---------------------------------------------------------------- unit converter
UNITCONV = """
<div class="tool" id="tt-uc">
  <div class="fields two">
    <div class="field"><label for="uc-a" id="uc-la">Value</label><input type="number" id="uc-a" step="any" placeholder="1"></div>
    <div class="field"><label for="uc-b" id="uc-lb">Result</label><input type="number" id="uc-b" step="any" placeholder="" readonly></div>
  </div>
  <div class="chips" id="uc-swap-row"><button class="chip" id="uc-swap">⇄ Swap direction</button></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="uc-r">–</span>
    <div class="result-formula" id="uc-f"></div></div>
  <table class="copytable" id="uc-table"><thead><tr><th id="uc-th1"></th><th id="uc-th2"></th></tr></thead><tbody></tbody></table>
</div>
<script>(function(){
var A=__ARGS__;
var la=document.getElementById('uc-la'),lb=document.getElementById('uc-lb');
var a=document.getElementById('uc-a'),b=document.getElementById('uc-b');
var r=document.getElementById('uc-r'),f=document.getElementById('uc-f');
var swapped=false;
function fmt(n){return n.toLocaleString('en-US',{maximumFractionDigits:A.dec===undefined?4:A.dec});}
function labels(){la.textContent=swapped?A.b:A.a;lb.textContent=swapped?A.a:A.b;}
function conv(v){
  if(isNaN(v))return null;
  if(A.factor===null||A.factor===undefined){
    return swapped?((v-32)*5/9):(v*9/5+32);
  }
  return swapped?v/A.factor:v*A.factor;
}
function run(){
  var v=parseFloat(a.value);
  var out=isNaN(v)?null:conv(v);
  if(out!==null&&out!==undefined){document.title=fmt(v)+' '+A.a+' = '+fmt(out)+' '+(swapped?A.a:A.b)+' - ToolTide';}
  else{document.title='Converter - ToolTide';}
  b.value=out===null?'':out;
  r.textContent=out===null?'–':fmt(out)+' '+(swapped?A.a:A.b);
  f.textContent=isNaN(v)?'':(swapped
    ?(A.factor===null||A.factor===undefined?('Formula: ('+v+' °F − 32) × 5/9 = '+fmt(out)+' °C'):('Formula: '+v+' ÷ '+A.factor+' = '+fmt(out)))
    :(A.factor===null||A.factor===undefined?('Formula: '+v+' × 9/5 + 32 = '+fmt(out)):('Formula: '+v+' × '+A.factor+' = '+fmt(out))));
}
document.getElementById('uc-swap').addEventListener('click',function(){
  swapped=!swapped;
  a.value=b.value;   // the previous result becomes the new input
  b.value='';
  labels();run();
});
a.addEventListener('input',run);
document.getElementById('uc-th1').textContent=A.a;
document.getElementById('uc-th2').textContent=A.b;
var tb=document.querySelector('#uc-table tbody');
var base=A.factor===null||A.factor===undefined?[-40,0,10,20,30,37,50,100]:[1,2,5,10,20,25,50,100,200,500,1000];
base.forEach(function(v){
  var tr=document.createElement('tr');
  var o;
  if(A.factor===null||A.factor===undefined){o=A.a==='Celsius'?v*9/5+32:(v-32)*5/9;}
  else{o=v*A.factor;}
  tr.innerHTML='<td>'+v.toLocaleString('en-US')+'</td><td>'+fmt(o)+'</td>';
  tb.appendChild(tr);
});
labels();a.value='1';run();
})();</script>
"""


# ---------------------------------------------------------------- typing test
TYPING = """
<div class="tool" id="tt-type">
  <div class="chips">
    <button class="chip active" data-s="30">30s</button>
    <button class="chip" data-s="60">60s</button>
    <button class="btn btn-sm" id="type-restart" type="button">↻ Restart</button>
  </div>
  <div class="type-passive" id="type-passage"></div>
  <textarea id="type-in" rows="4" placeholder="Click here and start typing — the timer starts with your first key…"></textarea>
  <div class="cd-clock" id="type-timer">1:00</div>
  <div class="stats">
    <div class="stat"><b id="type-wpm">–</b><span>WPM (net)</span></div>
    <div class="stat"><b id="type-acc">–</b><span>accuracy</span></div>
    <div class="stat"><b id="type-chars">0</b><span>characters typed</span></div>
  </div>
</div>
<script>(function(){
var SENT=['The quick brown fox jumps over the lazy dog while the farmer watches from his porch.','Practice makes perfect when learning to type faster every single day with focus.','A journey of a thousand miles begins with a single step and careful typing.','Typing speed matters less than accuracy because errors cost double the time to fix.','The best time to plant a tree was twenty years ago; the second best time is now.','Simple things should be simple and complex things should be possible for everyone.'];
var PASS=SENT.join(' ');
var dur=30,start=null,timer=null,ended=false;
var inp=document.getElementById('type-in'),pas=document.getElementById('type-passage');
function newPassage(){var i=Math.floor(Math.random()*SENT.length);PASS='';for(var k=0;k<3;k++){PASS+=SENT[(i+k)%SENT.length]+' ';}}
function fmtT(s){return Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0');}
function reset(){
  clearInterval(timer);start=null;ended=false;newPassage();
  pas.textContent=PASS;inp.value='';inp.disabled=false;
  document.getElementById('type-timer').textContent=fmtT(dur);
  document.getElementById('type-wpm').textContent='–';
  document.getElementById('type-acc').textContent='–';
  document.getElementById('type-chars').textContent='0';
  pas.innerHTML=PASS;
}
function finish(){
  ended=true;inp.disabled=true;clearInterval(timer);
  var typed=inp.value,mins=dur/60;
  var correct=0;for(var i=0;i<typed.length;i++){if(typed[i]===PASS[i])correct++;}
  var gross=(typed.length/5)/mins;
  var acc=typed.length?Math.round(correct/typed.length*100):0;
  var net=Math.max(0,Math.round(gross*acc/100));
  document.getElementById('type-wpm').textContent=net;
  document.getElementById('type-acc').textContent=acc+'%';
  highlight(typed.length);
}
function highlight(pos){
  var html='';
  for(var i=0;i<PASS.length;i++){
    var ch=PASS[i]===' '?'&nbsp;':PASS[i];
    if(i<pos)html+='<span class="'+(inp.value[i]===PASS[i]?'tp-ok':'tp-bad')+'">'+ch+'</span>';
    else if(i===pos)html+='<span class="tp-cur">'+ch+'</span>';
    else html+=ch;
  }
  pas.innerHTML=html;
}
inp.addEventListener('input',function(){
  if(ended)return;
  if(!start){start=Date.now();
    timer=setInterval(function(){
      var el=(Date.now()-start)/1000,left=dur-el;
      document.getElementById('type-timer').textContent=left>0?fmtT(left):'0:00';
      if(left<=0)finish();
    },200);}
  highlight(inp.value.length);
  document.getElementById('type-chars').textContent=inp.value.length;
  if(inp.value.length>=PASS.length)finish();
});
document.querySelectorAll('#tt-type .chip[data-s]').forEach(function(c){c.addEventListener('click',function(){
  dur=+c.dataset.s;
  document.querySelectorAll('#tt-type .chip[data-s]').forEach(function(x){x.classList.toggle('active',x===c);});
  reset();
});});
document.getElementById('type-restart').addEventListener('click',reset);
reset();
})();</script>
"""


# ---------------------------------------------------------------- name generator
NAMES = """
<div class="tool" id="tt-names">
  <div class="chips" id="names-styles">
    <button class="chip active" data-s="fantasy">⚔️ Fantasy</button>
    <button class="chip" data-s="team">🏆 Team</button>
    <button class="chip" data-s="character">🎭 Character</button>
  </div>
  <div class="names-grid" id="names-out"></div>
  <div class="tool-note">Click any name to copy it. Every batch is random — millions of combinations.</div>
  <button class="btn" id="names-gen" type="button">🎲 Generate 12 names</button>
</div>
<script>(function(){
var F1=['Ael','Aer','Ari','Bel','Cael','Dael','Eir','Fen','Gal','Hal','Ith','Kael','Lor','Mael','Nym','Ori','Ral','Syl','Thal','Vael','Wyn','Zar'];
var F2=['adric','awyn','ethas','imir','adan','iriel','ogar','othorn','amar','ilin','adriel','ivar','grim','ashel','afall','astorm','abrand','owen'];
var FT=[' the Bold',' the Wise',' of the Vale',' Stormborn',' Ironheart',' Nightwhisper',' Emberfall',' the Untamed',' Dawnstrider',' the Wanderer',' Frostbane',' Silverhand'];
var TA=['Mighty','Savage','Golden','Thunder','Crimson','Iron','Swift','Shadow','Royal','Lucky','Fierce','Silent','Wild','Turbo','Neon','Atomic','Cosmic'];
var TN=['Falcons','Comets','Wolves','Titans','Dragons','Phoenixes','Sharks','Bulls','Raptors','Vipers','Bears','Hawks','Legends','Bandits','Foxes','Kraken','Nomads'];
var C1=['Ava','Liam','Maya','Noah','Zoe','Ethan','Iris','Felix','Nora','Owen','Ruby','Silas','Tessa','Victor','Wren','Xander','Yara','Ezra','Lena','Marcus','June','Hugo'];
var C2=['Hart','Vance','Whitlock','Rivera','Chen','Okafor','Novak','Sato','Meyer','Delgado','Bishop','Kaur','Olsen','Moreau','Tanaka','Reyes','Kovac','Bell','Ashford','Quinn'];
var style='fantasy';
function ri(n){var b=new Uint32Array(1);crypto.getRandomValues(b);return b[0]%n;}
function pick(a){return a[ri(a.length)];}
function one(){
  if(style==='fantasy'){var n=pick(F1)+pick(F2);if(ri(100)<35)n+=pick(FT);return n;}
  if(style==='team'){return ri(100)<30?('The '+pick(TN)):(pick(TA)+' '+pick(TN));}
  return pick(C1)+' '+pick(C2);
}
function gen(){
  var g=document.getElementById('names-out');g.innerHTML='';
  var seen={},count=0;
  while(count<12){var n=one();if(seen[n])continue;seen[n]=1;count++;
    var d=document.createElement('button');d.className='name-card';d.type='button';d.textContent=n;
    d.addEventListener('click',function(){
      var t=this.textContent;
      var done=function(){this.classList.add('copied');var self=this;setTimeout(function(){self.classList.remove('copied');},900);}.bind(this);
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,function(){done();});}else{done();}
    });
    g.appendChild(d);
  }
}
document.querySelectorAll('#names-styles .chip').forEach(function(c){c.addEventListener('click',function(){
  style=c.dataset.s;
  document.querySelectorAll('#names-styles .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  gen();
});});
document.getElementById('names-gen').addEventListener('click',gen);
gen();
})();</script>
"""


# ---------------------------------------------------------------- password generator
PASSWORD = """
<div class="tool" id="tt-pw">
  <div class="pw-out-row"><input type="text" id="pw-out" readonly><button class="btn btn-sm" id="pw-copy" type="button">Copy</button></div>
  <div class="pw-strength"><div class="pw-bar" id="pw-bar"></div><span id="pw-strength"></span></div>
  <div class="fields">
    <div class="field"><label for="pw-len">Length: <b id="pw-lenv">16</b></label><input type="range" id="pw-len" min="8" max="64" value="16"></div>
  </div>
  <div class="chips">
    <button class="chip active" data-s="upper">A-Z</button>
    <button class="chip active" data-s="lower">a-z</button>
    <button class="chip active" data-s="digits">0-9</button>
    <button class="chip active" data-s="symbols">!@#$%</button>
    <button class="chip" data-s="noambig">No look-alikes (0O1lI)</button>
  </div>
  <button class="btn" id="pw-gen" type="button">🔐 Generate password</button>
  <div class="tool-note">Generated with your browser's WebCrypto secure random source. Nothing is sent anywhere — this works even offline.</div>
</div>
<script>(function(){
var SET={upper:'ABCDEFGHIJKLMNOPQRSTUVWXYZ',lower:'abcdefghijklmnopqrstuvwxyz',digits:'0123456789',symbols:'!@#$%^&*()-_=+[]{};:,.<>?'};
var AMB={'0':'O','O':'0','1':'l','l':'1','I':'|','|':'I'};
var on={upper:true,lower:true,digits:true,symbols:true},noambig=false;
var lenIn=document.getElementById('pw-len');
lenIn.addEventListener('input',function(){document.getElementById('pw-lenv').textContent=lenIn.value;gen();});
document.querySelectorAll('#tt-pw .chip[data-s]').forEach(function(c){c.addEventListener('click',function(){
  var s=c.dataset.s;
  if(s==='noambig'){noambig=!noambig;}
  else{on[s]=!on[s];}
  c.classList.toggle('active',(s==='noambig')?noambig:on[s]);
  gen();
});});
function charset(){
  var pool='';
  Object.keys(SET).forEach(function(k){if(on[k])pool+=SET[k];});
  if(noambig){pool=pool.split('').filter(function(ch){return !(ch in AMB);}).join('');}
  return pool;
}
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
function gen(){
  var pool=charset();
  if(!pool){document.getElementById('pw-out').value='Select at least one character set';return;}
  var n=+lenIn.value,out='';
  for(var i=0;i<n;i++)out+=pool[secureInt(pool.length)];
  document.getElementById('pw-out').value=out;
  var bits=n*Math.log2(pool.length);
  var bar=document.getElementById('pw-bar'),lab=document.getElementById('pw-strength');
  var p=Math.min(100,bits),label;
  if(bits<40){label='Weak';}else if(bits<60){label='Fair';}else if(bits<80){label='Strong';}else if(bits<100){label='Very strong';}else{label='Excellent';}
  bar.style.width=p+'%';
  bar.className='pw-bar '+(bits<40?'pw-w':bits<60?'pw-f':bits<80?'pw-s':'pw-x');
  lab.textContent=label+' — about '+Math.round(bits)+' bits of entropy';
}
document.getElementById('pw-gen').addEventListener('click',gen);
document.getElementById('pw-copy').addEventListener('click',function(){
  var o=document.getElementById('pw-out');o.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(o.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('pw-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
gen();
})();</script>
"""


# ---------------------------------------------------------------- random numbers
RANDOMNUM = """
<div class="tool" id="tt-rng">
  <div class="fields">
    <div class="field"><label for="rng-min">Minimum</label><input type="number" id="rng-min" value="1" step="any"></div>
    <div class="field"><label for="rng-max">Maximum</label><input type="number" id="rng-max" value="100" step="any"></div>
    <div class="field"><label for="rng-count">How many numbers</label><input type="number" id="rng-count" value="1" min="1" max="100" step="1"></div>
  </div>
  <div class="chips">
    <button class="chip active" id="rng-int" type="button">Whole numbers only</button>
    <button class="chip" id="rng-unique" type="button">No duplicates</button>
  </div>
  <button class="btn" id="rng-go" type="button">🎲 Generate</button>
  <div class="result" aria-live="polite" aria-atomic="true" id="rng-out" style="display:none"><span class="result-num" id="rng-res"></span></div>
  <div class="tool-note" id="rng-note">Uses your browser's cryptographically secure random source — fair draws, nothing recorded.</div>
</div>
<script>(function(){
var whole=true,unique=false;
var $=function(id){return document.getElementById(id);};
$('rng-int').addEventListener('click',function(){whole=!whole;this.classList.toggle('active',whole);});
$('rng-unique').addEventListener('click',function(){unique=!unique;this.classList.toggle('active',unique);});
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
$('rng-go').addEventListener('click',function(){
  var min=parseFloat($('rng-min').value),max=parseFloat($('rng-max').value);
  var count=parseInt($('rng-count').value)||1;
  var note=$('rng-note');
  if(isNaN(min)||isNaN(max)||max<=min){note.textContent='Maximum must be greater than minimum.';return;}
  if(count<1||count>100){note.textContent='Count must be between 1 and 100.';return;}
  var out=[],seen={};
  if(whole){
    var size=Math.floor(max)-Math.ceil(min)+1;
    if(unique&&count>size){note.textContent='Cannot pick '+count+' unique numbers from a range of '+size+'. Widen the range or allow duplicates.';return;}
    while(out.length<count){
      var v=Math.ceil(min)+secureInt(size);
      if(unique&&seen[v])continue;
      seen[v]=1;out.push(v);
    }
  }else{
    if(unique){note.textContent='No-duplicates applies to whole numbers only.';return;}
    for(var i=0;i<count;i++){out.push((min+(max-min)*secureInt(100000)/100000).toFixed(4));}
  }
  $('rng-res').textContent=out.join(',  ');
  $('rng-out').style.display='block';
  note.textContent='Generated '+out.length+' number'+(out.length>1?'s':'')+' · crypto-secure · nothing recorded.';
});
})();</script>
"""


# ---------------------------------------------------------------- words to pages
WORDSPAGES = """
<div class="tool" id="tt-wp">
  <div class="fields">
    <div class="field"><label for="wp-words">Word count</label><input type="number" id="wp-words" min="0" step="1" placeholder="1000"></div>
    <div class="field"><label for="wp-space">Spacing</label>
      <select id="wp-space">
        <option value="250">Double-spaced (250 words/page)</option>
        <option value="500" selected>Single-spaced (500 words/page)</option>
      </select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wp-out">–</span><span class="result-unit">pages</span>
    <div class="result-formula" id="wp-note"></div></div>
  <div class="tool-note">Assumes 12pt Times New Roman / Arial, 1-inch margins. Handwritten pages hold roughly half as many words.</div>
</div>
<script>(function(){
var w=document.getElementById('wp-words'),s=document.getElementById('wp-space');
function run(){
  var v=parseFloat(w.value)||0,per=parseFloat(s.value);
  var pages=v/per;
  document.getElementById('wp-out').textContent=v?(Math.round(pages*10)/10).toLocaleString('en-US'):'–';
  document.getElementById('wp-note').textContent=v?('≈ '+Math.ceil(pages)+' full page'+(Math.ceil(pages)>1?'s':'')+' · '+v.toLocaleString('en-US')+' words ÷ '+per+' words per page'):'';
}
w.addEventListener('input',run);s.addEventListener('change',run);run();
})();</script>
"""


# ---------------------------------------------------------------- roman numerals
ROMAN = """
<div class="tool" id="tt-roman">
  <div class="fields two">
    <div class="field"><label for="rn-num">Number (1–3999)</label><input type="number" id="rn-num" min="1" max="3999" step="1" placeholder="2026"></div>
    <div class="field"><label for="rn-rom">Roman numeral</label><input type="text" id="rn-rom" placeholder="MMXXVI" autocomplete="off" style="text-transform:uppercase"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rn-out">–</span><div class="result-formula" id="rn-note"></div></div>
  <table class="copytable"><thead><tr><th>Symbol</th><th>Value</th></tr></thead>
  <tbody><tr><td>I · V · X</td><td>1 · 5 · 10</td></tr><tr><td>L · C · D</td><td>50 · 100 · 500</td></tr><tr><td>M</td><td>1000</td></tr><tr><td>IV · IX</td><td>4 · 9 (subtract before)</td></tr><tr><td>XL · XC</td><td>40 · 90</td></tr><tr><td>CD · CM</td><td>400 · 900</td></tr></tbody></table>
</div>
<script>(function(){
var M=[[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']];
var num=document.getElementById('rn-num'),rom=document.getElementById('rn-rom');
var out=document.getElementById('rn-out'),note=document.getElementById('rn-note');
var lock=false;
function toRoman(n){var s='';M.forEach(function(p){while(n>=p[0]){s+=p[1];n-=p[0];}});return s;}
function fromRoman(s){
  s=s.toUpperCase().trim();
  if(!/^[MDCLXVI]+$/.test(s))return null;
  var V={I:1,V:5,X:10,L:50,C:100,D:500,M:1000},t=0;
  for(var i=0;i<s.length;i++){
    var v=V[s.charAt(i)],n2=i+1<s.length?V[s.charAt(i+1)]:0;
    t+=v<n2?-v:v;
  }
  return toRoman(t)===s?t:null;  // reject non-standard forms like IIIV
}
num.addEventListener('input',function(){
  if(lock)return;
  var n=parseInt(num.value);
  if(!n||n<1||n>3999){out.textContent='–';note.textContent=n?'Range is 1–3999.':'';return;}
  var r=toRoman(n);rom.value=r;out.textContent=r;note.textContent=n+' in Roman numerals';
});
rom.addEventListener('input',function(){
  lock=true;num.value='';
  var v=this.value.trim();
  if(!v){out.textContent='–';note.textContent='';lock=false;return;}
  var n=fromRoman(v);
  if(n===null){out.textContent='–';note.textContent='Not a valid standard Roman numeral (1–3999).';}
  else{num.value=n;out.textContent=n.toLocaleString('en-US');note.textContent=v.toUpperCase()+' = '+n.toLocaleString('en-US');}
  lock=false;
});
})();</script>
"""


# ---------------------------------------------------------------- grade calculator
GRADE = """
<div class="tool" id="tt-grade">
  <div class="fields">
    <div class="field"><label for="gr-earned">Points earned</label><input type="number" id="gr-earned" min="0" step="any" placeholder="42"></div>
    <div class="field"><label for="gr-total">Points possible</label><input type="number" id="gr-total" min="0" step="any" placeholder="50"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gr-pct">–</span><span class="result-unit" id="gr-letter"></span>
    <div class="result-formula" id="gr-note"></div></div>
  <div class="chips"><span class="of" style="padding:0 6px">Standard scale:</span>
    <span class="chip" style="pointer-events:none">A ≥ 90</span><span class="chip" style="pointer-events:none">B 80–89</span>
    <span class="chip" style="pointer-events:none">C 70–79</span><span class="chip" style="pointer-events:none">D 60–69</span>
    <span class="chip" style="pointer-events:none">F &lt; 60</span></div>
  <div class="fields" style="margin-top:16px">
    <div class="field"><label for="gr-cur">Current grade % <small>(before final)</small></label><input type="number" id="gr-cur" min="0" max="100" step="any" placeholder="82"></div>
    <div class="field"><label for="gr-weight">Final worth % of grade</label><input type="number" id="gr-weight" min="0" max="100" step="any" placeholder="30"></div>
    <div class="field"><label for="gr-target">Target grade letter</label>
      <select id="gr-target"><option value="90">A (90%)</option><option value="80">B (80%)</option><option value="70">C (70%)</option><option value="60">D (60%)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gr-need">–</span><span class="result-unit" id="gr-need-txt">needed on the final</span></div>
</div>
<script>(function(){
var e=document.getElementById('gr-earned'),t=document.getElementById('gr-total');
function letter(p){return p>=90?'A':p>=80?'B':p>=70?'C':p>=60?'D':'F';}
function pctCol(p){return p>=90?'#16a34a':p>=80?'#0e7490':p>=70?'#d97706':p>=60?'#dc2626':'#b91c1c';}
function run(){
  var a=parseFloat(e.value),b=parseFloat(t.value);
  if(!b||isNaN(a)||a<0){document.getElementById('gr-pct').textContent='–';document.getElementById('gr-letter').textContent='';document.getElementById('gr-note').textContent='';return;}
  var p=a/b*100;
  document.getElementById('gr-pct').textContent=(Math.round(p*10)/10)+'%';
  var L=document.getElementById('gr-letter');L.textContent=letter(p);L.style.color=pctCol(p);
  document.getElementById('gr-note').textContent=a+' ÷ '+b+' × 100 = '+(Math.round(p*100)/100)+'%';
}
e.addEventListener('input',run);t.addEventListener('input',run);run();
var cur=document.getElementById('gr-cur'),wt=document.getElementById('gr-weight'),tg=document.getElementById('gr-target');
function runTarget(){
  var c=parseFloat(cur.value),w=parseFloat(wt.value),target=parseFloat(tg.value);
  var box=document.getElementById('gr-need'),txt=document.getElementById('gr-need-txt');
  if(!w||w<=0||w>100||isNaN(c)){box.textContent='–';txt.textContent='needed on the final';return;}
  var need=(target-c*(1-w/100))/(w/100);
  if(need<0){box.textContent='0%';txt.textContent='— target already secured 🎉';}
  else if(need>100){box.textContent='>100%';txt.textContent='— mathematically out of reach';}
  else{box.textContent=(Math.round(need*10)/10)+'%';txt.textContent='needed on the final';}
}
cur.addEventListener('input',runTarget);wt.addEventListener('input',runTarget);tg.addEventListener('change',runTarget);runTarget();
})();</script>
"""


# ---------------------------------------------------------------- duplicate line remover
DEDUPE = """
<div class="tool" id="tt-dd2">
  <div class="field"><label for="dd2-in">Paste your list or text</label>
    <textarea id="dd2-in" rows="9" placeholder="one item per line…"></textarea></div>
  <div class="stats">
    <div class="stat"><b id="dd2-orig">0</b><span>original lines</span></div>
    <div class="stat"><b id="dd2-uniq">0</b><span>unique lines</span></div>
    <div class="stat"><b id="dd2-rem">0</b><span>duplicates removed</span></div>
  </div>
  <div class="field" style="margin-top:12px"><label for="dd2-out">Cleaned output <button class="btn btn-sm" id="dd2-copy" type="button">Copy</button></label>
    <textarea id="dd2-out" rows="9" readonly placeholder="cleaned list appears here…"></textarea></div>
</div>
<script>(function(){
var inp=document.getElementById('dd2-in'),out=document.getElementById('dd2-out');
function run(){
  var t=inp.value;
  if(!t){document.getElementById('dd2-orig').textContent='0';document.getElementById('dd2-uniq').textContent='0';
    document.getElementById('dd2-rem').textContent='0';out.value='';return;}
  var lines=t.split(/\\n/),seen={},res=[];
  for(var i=0;i<lines.length;i++){
    var L=lines[i];
    if(i===lines.length-1&&L===''){continue;}  // trailing newline
    if(seen.hasOwnProperty(L))continue;
    seen[L]=1;res.push(L);
  }
  document.getElementById('dd2-orig').textContent=lines.length.toLocaleString('en-US');
  document.getElementById('dd2-uniq').textContent=res.length.toLocaleString('en-US');
  document.getElementById('dd2-rem').textContent=(lines.length-res.length).toLocaleString('en-US');
  out.value=res.join('\\n');
}
inp.addEventListener('input',run);
document.getElementById('dd2-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('dd2-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


# ---------------------------------------------------------------- slug generator
SLUG = """
<div class="tool" id="tt-slug">
  <div class="field"><label for="sl-in">Title or text</label>
    <textarea id="sl-in" rows="4" placeholder="My Ultimate Guide to Cold Brew Coffee (2026 Edition)!"></textarea></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sl-out" style="word-break:break-all">–</span>
    <div class="result-formula" id="sl-len"></div></div>
  <div class="tool-note">Lowercase · accents folded · hyphen-separated · trimmed to your spec below.</div>
  <div class="fields"><div class="field"><label for="sl-max">Max length <small>(0 = no limit)</small></label><input type="number" id="sl-max" value="0" min="0" step="1"></div></div>
</div>
<script>(function(){
var inp=document.getElementById('sl-in'),out=document.getElementById('sl-out'),len=document.getElementById('sl-len'),mx=document.getElementById('sl-max');
function slugify(t){
  var from="àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþßłđđšžœ",to="aaaaaaaceeeeiiiionoooooouuuuythsddsoe";
  t=t.toLowerCase().replace(/[-ɏ]/g,function(ch){var i=from.indexOf(ch);return i>=0?to.charAt(i):ch;});
  t=t.replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
  var m=parseInt(mx.value)||0;
  if(m>0&&t.length>m){t=t.slice(0,m);var cut=t.lastIndexOf('-');if(cut>10)t=t.slice(0,cut);}
  return t;
}
function run(){var s=slugify(inp.value);out.textContent=s||'–';len.textContent=s?(s.length+' characters · '+s.split('-').filter(Boolean).length+' words'):'Type a title above…';}
inp.addEventListener('input',run);mx.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- sales tax
SALESTAX = """
<div class="tool" id="tt-stx">
  <div class="chips" role="tablist">
    <button class="chip active" data-m="add">Add tax</button>
    <button class="chip" data-m="rev">Remove tax</button>
  </div>
  <div class="fields">
    <div class="field" id="stx-f1"><label for="stx-price">Pre-tax price ($)</label><input type="number" id="stx-price" step="0.01" min="0" placeholder="100"></div>
    <div class="field" id="stx-f2" style="display:none"><label for="stx-total">Tax-inclusive total ($)</label><input type="number" id="stx-total" step="0.01" min="0" placeholder="110"></div>
    <div class="field"><label for="stx-rate">Tax rate %</label><input type="number" id="stx-rate" step="0.01" min="0" placeholder="10"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="stx-out">–</span><span class="result-unit" id="stx-unit"></span>
    <div class="result-formula" id="stx-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="stx-tax">–</b><span>tax amount</span></div>
    <div class="stat"><b id="stx-base">–</b><span>pre-tax price</span></div>
    <div class="stat"><b id="stx-tot">–</b><span>total</span></div>
  </div>
</div>
<script>(function(){
var mode='add';
var price=document.getElementById('stx-price'),total=document.getElementById('stx-total'),rate=document.getElementById('stx-rate');
document.querySelectorAll('#tt-stx .chip').forEach(function(c){c.addEventListener('click',function(){
  mode=c.dataset.m;
  document.querySelectorAll('#tt-stx .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  document.getElementById('stx-f1').style.display=mode==='add'?'flex':'none';
  document.getElementById('stx-f2').style.display=mode==='rev'?'flex':'none';
  run();
});});
function money(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function run(){
  var r=(parseFloat(rate.value)||0)/100;
  var base,tax,tot;
  if(mode==='add'){
    base=parseFloat(price.value);
    if(isNaN(base)){clear();return;}
    tax=base*r;tot=base+tax;
    document.getElementById('stx-out').textContent=money(tot);
    document.getElementById('stx-unit').textContent='total';
    document.getElementById('stx-note').textContent=base+' × '+(1+r)+' = '+money(tot);
  }else{
    tot=parseFloat(total.value);
    if(isNaN(tot)){clear();return;}
    base=tot/(1+r);tax=tot-base;
    document.getElementById('stx-out').textContent=money(base);
    document.getElementById('stx-unit').textContent='pre-tax';
    document.getElementById('stx-note').textContent=tot+' ÷ '+(1+r)+' = '+money(base)+'  (not '+money(tot*(1-r))+')';
  }
  document.getElementById('stx-tax').textContent=money(tax);
  document.getElementById('stx-base').textContent=money(base);
  document.getElementById('stx-tot').textContent=money(tot);
}
function clear(){document.getElementById('stx-out').textContent='–';document.getElementById('stx-unit').textContent='';
  document.getElementById('stx-note').textContent='';document.getElementById('stx-tax').textContent='–';
  document.getElementById('stx-base').textContent='–';document.getElementById('stx-tot').textContent='–';}
[price,total,rate].forEach(function(el){el.addEventListener('input',run);});run();
})();</script>
"""


# ---------------------------------------------------------------- upside down text
UPSIDE = """
<div class="tool" id="tt-flip">
  <div class="field"><label for="fl-in">Your text</label>
    <textarea id="fl-in" rows="4" placeholder="Type something…"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="fl-out">Flipped upside down <button class="btn btn-sm" id="fl-copy" type="button">Copy</button></label>
    <textarea id="fl-out" rows="4" readonly></textarea></div>
  <div class="tool-note">Uses real Unicode upside-down characters — it survives copy-paste into WhatsApp, Instagram, Twitter/X and bios. Purely local, nothing recorded.</div>
</div>
<script>(function(){
var MAP={'a':'ɐ','b':'q','c':'ɔ','d':'p','e':'ǝ','f':'ɟ','g':'ƃ','h':'ɥ','i':'ᴉ','j':'ɾ','k':'ʞ','l':'l','m':'ɯ','n':'u','o':'o','p':'d','q':'b','r':'ɹ','s':'s','t':'ʇ','u':'n','v':'ʌ','w':'ʍ','x':'x','y':'ʎ','z':'z','A':'∀','B':'𐐒','C':'Ɔ','D':'p','E':'Ǝ','F':'Ⅎ','G':'⅁','H':'H','I':'I','J':'ſ','K':'ʞ','L':'˥','M':'W','N':'N','O':'O','P':'Ԁ','Q':'Ό','R':'ᴚ','S':'S','T':'⊥','U':'∩','V':'Λ','W':'M','X':'X','Y':'⅄','Z':'Z','1':'Ɩ','2':'ᄅ','3':'Ɛ','4':'ㄣ','5':'ϛ','6':'9','7':'ㄥ','8':'8','9':'6','0':'0','.':'˙',',':"'",'?':'¿','!':'¡','"':'„',"'":',','(':')',')':'(','[':']',']':'[','{':'}','}':'{','<':'>','>':'<','&':'⅋','_':'‾'};
var inp=document.getElementById('fl-in'),out=document.getElementById('fl-out');
function flip(t){
  return t.split('').map(function(ch){return MAP[ch]!==undefined?MAP[ch]:ch;}).reverse().join('');
}
inp.addEventListener('input',function(){out.value=flip(inp.value);});
document.getElementById('fl-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('fl-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
})();</script>
"""


# ---------------------------------------------------------------- hours calculator
HOURSDIFF = """
<div class="tool" id="tt-hd">
  <div class="fields">
    <div class="field"><label for="hd-start">Start time</label><input type="time" id="hd-start" value="09:00"></div>
    <div class="field"><label for="hd-end">End time</label><input type="time" id="hd-end" value="17:00"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hd-hm">–</span>
    <div class="result-formula" id="hd-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="hd-dec">–</b><span>decimal hours (for timesheets)</span></div>
    <div class="stat"><b id="hd-mins">–</b><span>total minutes</span></div>
  </div>
</div>
<script>(function(){
var a=document.getElementById('hd-start'),b=document.getElementById('hd-end');
function toMin(v){var p=v.split(':');return (+p[0])*60+(+p[1]);}
function run(){
  if(!a.value||!b.value)return;
  var s=toMin(a.value),e=toMin(b.value),overnight=false;
  if(e<s){e+=1440;overnight=true;}
  var d=e-s,h=Math.floor(d/60),m=d%60;
  document.getElementById('hd-hm').textContent=h+' h '+m+' min';
  var dec=(Math.round(d/6)/100);
  document.getElementById('hd-dec').textContent=dec;
  document.getElementById('hd-mins').textContent=d.toLocaleString('en-US');
  document.getElementById('hd-note').textContent=(overnight?'overnight shift · ':'')+
    a.value+' → '+b.value+'  ·  '+d+' minutes ÷ 60 = '+dec;
}
a.addEventListener('input',run);b.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- strip html
STRIPHTML = """
<div class="tool" id="tt-sh">
  <div class="field"><label for="sh-in">Paste HTML</label>
    <textarea id="sh-in" rows="8" placeholder="<div>Hello <b>world</b></div>"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="sh-out">Plain text <button class="btn btn-sm" id="sh-copy" type="button">Copy</button></label>
    <textarea id="sh-out" rows="8" readonly placeholder="clean text appears here…"></textarea></div>
  <div class="stats"><div class="stat"><b id="sh-tags">0</b><span>tags stripped</span></div></div>
</div>
<script>(function(){
var inp=document.getElementById('sh-in'),out=document.getElementById('sh-out');
var ENT={'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#39;':"'",'&nbsp;':' '};
function run(){
  var t=inp.value;
  var tags=0;
  t=t.replace(/<(script|style)[^>]*>[\s\S]*?<\/>/gi,function(m){tags++;return '';});
  t=t.replace(/<[^>]*>/g,function(m){tags++;return '';});
  t=t.replace(/&amp;|&lt;|&gt;|&quot;|&#39;|&nbsp;/gi,function(m){
    var k=m.toLowerCase();
    return ENT[m.toLowerCase()];
  });
  out.value=t;
  document.getElementById('sh-tags').textContent=tags.toLocaleString('en-US');
}
inp.addEventListener('input',run);
document.getElementById('sh-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('sh-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


# ---------------------------------------------------------------- inch fraction
INCHFRAC = """
<div class="tool" id="tt-if">
  <div class="fields">
    <div class="field"><label for="if-frac">Fractional inches <small>(3/8 or 1-3/4)</small></label><input type="text" id="if-frac" placeholder="1-3/4"></div>
    <div class="field"><label for="if-dec">Decimal inches</label><input type="number" id="if-dec" step="any" min="0" placeholder="1.75"></div>
    <div class="field"><label for="if-mm">Millimeters</label><input type="number" id="if-mm" step="any" min="0" placeholder="44.45"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="if-out">-</span><span class="result-unit" id="if-unit"></span></div>
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
  var m=v.match(/^(\\d+)?[- ]?(\\d+)\\/(\\d+)$/);
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


# ---------------------------------------------------------------- average
AVERAGE = """
<div class="tool" id="tt-avg">
  <div class="field"><label for="avg-in">Numbers <small>(comma, space or line separated)</small></label>
    <textarea id="avg-in" rows="5" placeholder="4, 8, 15, 16, 23, 42"></textarea></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="avg-mean">–</span><span class="result-unit">average</span>
    <div class="result-formula" id="avg-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="avg-sum">–</b><span>sum</span></div>
    <div class="stat"><b id="avg-n">–</b><span>count</span></div>
    <div class="stat"><b id="avg-min">–</b><span>min</span></div>
    <div class="stat"><b id="avg-max">–</b><span>max</span></div>
  </div>
</div>
<script>(function(){
var inp=document.getElementById('avg-in');
function run(){
  var nums=(inp.value.match(/-?\d+(?:\.\d+)?(?:e[+-]?\d+)?/gi)||[]).map(Number);
  if(!nums.length){document.getElementById('avg-mean').textContent='-';
    document.getElementById('avg-sum').textContent='-';document.getElementById('avg-n').textContent='0';
    document.getElementById('avg-min').textContent='-';document.getElementById('avg-max').textContent='-';
    document.getElementById('avg-note').textContent='';return;}
  var sum=nums.reduce(function(a,b){return a+b;},0);
  var mean=sum/nums.length;
  document.getElementById('avg-mean').textContent=(Math.round(mean*1e6)/1e6).toLocaleString('en-US');
  document.getElementById('avg-sum').textContent=(Math.round(sum*1e6)/1e6).toLocaleString('en-US');
  document.getElementById('avg-n').textContent=nums.length.toLocaleString('en-US');
  document.getElementById('avg-min').textContent=Math.min.apply(null,nums).toLocaleString('en-US');
  document.getElementById('avg-max').textContent=Math.max.apply(null,nums).toLocaleString('en-US');
  document.getElementById('avg-note').textContent='Sum '+nums.length+' values ÷ '+nums.length+' = mean';
}
inp.addEventListener('input',run);run();
})();</script>
"""


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
  var parts=v.trim().split(/\s+/).filter(Boolean),bytes=[];
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


# ---------------------------------------------------------------- grams <-> cups (by ingredient)
GRAMSCUPS = """
<div class="tool" id="tt-gc">
  <div class="field"><label for="gc-ing">Ingredient</label>
    <select id="gc-ing">
      <option value="125">All-purpose flour (125 g/cup)</option>
      <option value="200">Granulated sugar (200 g/cup)</option>
      <option value="213">Brown sugar, packed (213 g/cup)</option>
      <option value="120">Powdered sugar (120 g/cup)</option>
      <option value="227">Butter (227 g/cup)</option>
      <option value="240">Water / milk (240 g/cup)</option>
      <option value="340">Honey (340 g/cup)</option>
      <option value="90">Rolled oats (90 g/cup)</option>
      <option value="100">Cocoa powder (100 g/cup)</option>
      <option value="180">Rice, uncooked (180 g/cup)</option>
    </select></div>
  <div class="fields">
    <div class="field"><label for="gc-g">Grams</label><input type="number" id="gc-g" step="any" min="0" placeholder="250"></div>
    <div class="field"><label for="gc-c">Cups</label><input type="number" id="gc-c" step="any" min="0" placeholder=""></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gc-frac">–</span><span class="result-unit" id="gc-fr2"></span>
    <div class="result-formula" id="gc-note"></div></div>
</div>
<script>(function(){
var ing=document.getElementById('gc-ing'),G=document.getElementById('gc-g'),C=document.getElementById('gc-c');
var frac=document.getElementById('gc-frac'),fr2=document.getElementById('gc-fr2'),note=document.getElementById('gc-note');
var lock=false;
function nice(n){
  var common=[0,0.25,0.333,0.5,0.666,0.75,1];
  var best=0,bd=9;
  common.forEach(function(c){var d=Math.abs(n-c);if(d<bd){bd=d;best=c;}});
  var names={0:'',0.25:'1/4',0.333:'1/3',0.5:'1/2',0.666:'2/3',0.75:'3/4',1:'1'};
  var whole=Math.floor(n),rem=n-whole,remR=Math.round(rem*100)/100;
  var base=whole?whole+' ':'';
  var rn=names[best]||null;
  if(remR>0.02&&remR<0.98&&rn&&best!==1)return base+rn;
  if(best===1&&whole)return (whole+1)+'';
  return (Math.round(n*100)/100)+'';
}
function runG(){
  if(lock)return;lock=true;C.value='';
  var g=parseFloat(G.value);
  if(isNaN(g)||!g){frac.textContent='-';fr2.textContent='';note.textContent='';lock=false;return;}
  var c=g/(parseFloat(ing.value));
  var nc=Math.round(c*100)/100;
  C.value=nc;
  frac.textContent=nice(c);fr2.textContent='cup'+(c>1?'s':'');
  note.textContent=g+' g \u00f7 '+ing.value+' g per cup';
  lock=false;
}
function runC(){
  if(lock)return;lock=true;G.value='';
  var c=parseFloat(C.value);
  if(isNaN(c)||!c){frac.textContent='-';fr2.textContent='';note.textContent='';lock=false;return;}
  var g=c*(parseFloat(ing.value));
  var gr=Math.round(g*10)/10;
  G.value=gr;
  frac.textContent=gr+' g';fr2.textContent='';
  note.textContent=c+' cup(s) \u00d7 '+ing.value+' g per cup';
  lock=false;
}
ing.addEventListener('change',runG);
G.addEventListener('input',runG);
C.addEventListener('input',runC);
})();</script>
"""


# ---------------------------------------------------------------- day of week
DAYOFWEEK = """
<div class="tool" id="tt-dw">
  <div class="field"><label for="dw-date">Any date</label><input type="date" id="dw-date"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dw-out">-</span>
    <div class="result-formula" id="dw-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="dw-doy">-</b><span>day of year</span></div>
    <div class="stat"><b id="dw-iso">-</b><span>ISO week</span></div>
  </div>
</div>
<script>(function(){
var d=document.getElementById('dw-date');
var now=new Date();
d.value=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0');
function isoWeek(dt){
  var t=new Date(Date.UTC(dt.getFullYear(),dt.getMonth(),dt.getDate()));
  var day=(t.getUTCDay()+6)%7;
  t.setUTCDate(t.getUTCDate()-day+3);
  var firstThu=new Date(Date.UTC(t.getUTCFullYear(),0,4));
  var fday=(firstThu.getUTCDay()+6)%7;
  firstThu.setUTCDate(firstThu.getUTCDate()-fday+3);
  return 1+Math.round((t-firstThu)/604800000);
}
function run(){
  if(!d.value)return;
  var dt=new Date(d.value+'T00:00:00');
  if(isNaN(dt))return;
  document.getElementById('dw-out').textContent=dt.toLocaleDateString('en-US',{weekday:'long'});
  document.getElementById('dw-note').textContent=dt.toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
  var start=new Date(dt.getFullYear(),0,1);
  document.getElementById('dw-doy').textContent=Math.round((dt-start)/864e5)+1;
  document.getElementById('dw-iso').textContent='W'+isoWeek(dt);
}
d.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- fuel economy
FUEL = """
<div class="tool" id="tt-fuel">
  <div class="fields two">
    <div class="field"><label for="fu-l">Liters per 100 km</label><input type="number" id="fu-l" step="any" min="0" placeholder="6.5"></div>
    <div class="field"><label for="fu-m">Miles per gallon (US)</label><input type="number" id="fu-m" step="any" min="0" placeholder="36.2"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fu-out">–</span><span class="result-unit" id="fu-unit"></span>
    <div class="result-formula" id="fu-note"></div></div>
  <div class="tool-note" id="fu-hint">Lower L/100km is better · higher MPG is better — the scales run in opposite directions.</div>
</div>
<script>(function(){
var L=document.getElementById('fu-l'),M=document.getElementById('fu-m');
var out=document.getElementById('fu-out'),unit=document.getElementById('fu-unit'),hint=document.getElementById('fu-hint');
var lock=false;
function good(l){return l<=6?'efficient':l<=9?'typical':'thirsty';}
function runL(){
  if(lock)return;lock=true;M.value='';
  var v=parseFloat(L.value);
  if(isNaN(v)||v<=0){out.textContent='-';unit.textContent='';hint.textContent='Lower L/100km is better · higher MPG is better.';lock=false;return;}
  var mpg=235.215/v;
  M.value=Math.round(mpg*10)/10;
  out.textContent=Math.round(mpg*10)/10+' mpg';
  unit.textContent='(US)';
  hint.textContent=v+' L/100km = '+Math.round(mpg*10)/10+' US mpg — '+good(v)+' for a petrol car.';
  lock=false;
}
function runM(){
  if(lock)return;lock=true;L.value='';
  var v=parseFloat(M.value);
  if(isNaN(v)||v<=0){out.textContent='-';unit.textContent='';lock=false;return;}
  var l=235.215/v;
  L.value=Math.round(l*100)/100;
  out.textContent=Math.round(l*100)/100+' L/100km';
  unit.textContent='';
  hint.textContent=v+' mpg = '+Math.round(l*100)/100+' L/100km - '+good(l)+' for a petrol car.';
  lock=false;
}
L.addEventListener('input',runL);
M.addEventListener('input',runM);
})();</script>
"""


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


# ---------------------------------------------------------------- square footage
SQFT = """
<div class="tool" id="tt-sq">
  <div class="chips" role="tablist">
    <button class="chip active" data-u="ft">Feet</button>
    <button class="chip" data-u="m">Meters</button>
  </div>
  <div class="fields">
    <div class="field"><label for="sq-l">Length</label><input type="number" id="sq-l" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="sq-w">Width</label><input type="number" id="sq-w" step="any" min="0" placeholder="15"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sq-ft">-</span><span class="result-unit">sq ft</span></div>
  <div class="stats">
    <div class="stat"><b id="sq-sqft">-</b><span>square feet</span></div>
    <div class="stat"><b id="sq-sqm">-</b><span>square meters</span></div>
    <div class="stat"><b id="sq-total">-</b><span>running total</span></div>
  </div>
  <button class="btn btn-sm" id="sq-add" type="button">+ Add to running total</button>
</div>
<script>(function(){
var unit='ft',total=0;
var l=document.getElementById('sq-l'),w=document.getElementById('sq-w');
document.querySelectorAll('#tt-sq .chip').forEach(function(c){c.addEventListener('click',function(){
  unit=c.dataset.u;
  document.querySelectorAll('#tt-sq .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  var labels=document.querySelectorAll('#tt-sq label');
  labels[1].textContent='Length ('+unit+')';labels[2].textContent='Width ('+unit+')';
  run();
});});
function run(){
  var a=parseFloat(l.value),b=parseFloat(w.value);
  var sq=(isNaN(a)||isNaN(b))?null:a*b;
  var sqft=unit==='ft'?sq:sq*10.76391042;
  var sqm=unit==='ft'?sq*0.09290304:sq;
  document.getElementById('sq-ft').textContent=sq===null?'-':(Math.round(sqft*10)/10).toLocaleString('en-US');
  document.getElementById('sq-sqft').textContent=sq===null?'-':(Math.round(sqft*10)/10).toLocaleString('en-US');
  document.getElementById('sq-sqm').textContent=sq===null?'-':(Math.round(sqm*10)/10).toLocaleString('en-US');
}
l.addEventListener('input',run);w.addEventListener('input',run);
document.getElementById('sq-add').addEventListener('click',function(){
  var v=parseFloat(document.getElementById('sq-sqft').textContent.replace(/,/g,''));
  if(!isNaN(v)){total+=v;document.getElementById('sq-total').textContent=Math.round(total*10)/10;}
});
})();</script>
"""


# ---------------------------------------------------------------- seconds converter
SECONDS = """
<div class="tool" id="tt-sec">
  <div class="field"><label for="sec-in">Total seconds</label><input type="number" id="sec-in" step="1" min="0" placeholder="3725"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sec-out">-</span></div>
  <div class="field" style="margin-top:12px"><label for="sec-hms">Duration (h:mm:ss or mm:ss)</label><input type="text" id="sec-hms" placeholder="1:02:05"></div>
</div>
<script>(function(){
var sIn=document.getElementById('sec-in'),hms=document.getElementById('sec-hms');
var out=document.getElementById('sec-out');
var lock=false;
function pad(n){return (n<10?'0':'')+n;}
function fromSeconds(v){
  var h=Math.floor(v/3600),m=Math.floor(v%3600/60),s=v%60;
  return h>0?h+':'+pad(m)+':'+pad(s):m+':'+pad(s);
}
function toSeconds(v){
  var parts=v.trim().split(':').map(Number);
  if(parts.some(isNaN))return null;
  if(parts.length===3)return parts[0]*3600+parts[1]*60+parts[2];
  if(parts.length===2)return parts[0]*60+parts[1];
  if(parts.length===1)return parts[0];
  return null;
}
sIn.addEventListener('input',function(){
  if(lock)return;lock=true;
  var v=parseInt(sIn.value);
  if(isNaN(v)){out.textContent='-';hms.value='';lock=false;return;}
  out.textContent=fromSeconds(v);hms.value=fromSeconds(v);
  lock=false;
});
hms.addEventListener('input',function(){
  if(lock)return;lock=true;
  var v=toSeconds(this.value);
  if(v===null){out.textContent='(use h:mm:ss)';sIn.value='';lock=false;return;}
  out.textContent=v.toLocaleString('en-US')+' seconds';sIn.value=v;
  lock=false;
});
})();</script>
"""


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
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="px-out">-</span><span class="result-unit" id="px-unit"></span>
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


# ---------------------------------------------------------------- dice roller
DICE = """
<div class="tool" id="tt-dice">
  <div class="fields">
    <div class="field"><label for="dc-count">Number of dice</label><input type="number" id="dc-count" min="1" max="12" step="1" value="2"></div>
    <div class="field"><label for="dc-faces">Faces per die</label><input type="number" id="dc-faces" min="2" max="100" step="1" value="6"></div>
  </div>
  <button class="btn" id="dc-go" type="button">🎲 Roll</button>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dc-total">-</span><span class="result-unit">total</span>
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


# ---------------------------------------------------------------- half calculator
HALF = """
<div class="tool" id="tt-half">
  <div class="field"><label for="hf-in">Number, fraction or mixed (3/4, 2-1/2, 0.8)</label>
    <input type="text" id="hf-in" placeholder="3/4"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hf-out">-</span></div>
  <div class="stats">
    <div class="stat"><b id="hf-frac">-</b><span>exact fraction</span></div>
    <div class="stat"><b id="hf-dec">-</b><span>decimal</span></div>
  </div>
</div>
<script>(function(){
var inp=document.getElementById('hf-in');
var out=document.getElementById('hf-out'),fr=document.getElementById('hf-frac'),dc=document.getElementById('hf-dec');
function gcd(a,b){return b?gcd(b,a%b):a;}
function parse(v){
  v=v.trim().replace(/"/g,'');
  var m=v.match(/^(\d+)?[- ]?(\d+)\/(\d+)$/);
  if(m){var w=m[1]?+m[1]:0;return {n:w*(+m[3])+(+m[2]),d:+m[3]};}
  var f=parseFloat(v);
  if(isNaN(f))return null;
  if(Number.isInteger(f))return {n:f,d:1};
  var s=f.toFixed(6).replace(/0+$/,'');
  var dec=s.split('.')[1];
  var den=Math.pow(10,dec.length);
  return {n:Math.round(f*den),d:den};
}
function show(v){
  var h=parse(v);
  if(!h||!h.d){out.textContent='-';fr.textContent='-';dc.textContent='-';return;}
  var n=h.n,d=h.d*2,g=gcd(n,d);
  n/=g;d/=g;
  var whole=Math.floor(n/d),rem=n%d;
  var fs=rem?(whole?whole+'-':'')+rem+'/'+d:(whole+'');
  out.textContent=fs;
  fr.textContent=fs;
  dc.textContent=Math.round((h.n/h.d/2)*1e6)/1e6;
}
inp.addEventListener('input',function(){show(this.value);});
show('3/4');
})();</script>
"""


# ---------------------------------------------------------------- random letter
LETTER = """
<div class="tool" id="tt-rl">
  <div class="chips">
    <button class="chip active" id="rl-uniq" type="button">No repeats</button>
  </div>
  <div class="field"><label for="rl-count">How many letters</label><input type="number" id="rl-count" min="1" max="26" step="1" value="1"></div>
  <button class="btn" id="rl-go" type="button">🔤 Generate</button>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rl-out" style="letter-spacing:.2em">-</span></div>
</div>
<script>(function(){
var uniq=false;
document.getElementById('rl-uniq').addEventListener('click',function(){
  uniq=!uniq;this.classList.toggle('active',uniq);
});
document.getElementById('rl-go').addEventListener('click',function(){
  var n=Math.min(26,Math.max(1,parseInt(document.getElementById('rl-count').value)||1));
  var A='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
    do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
  var out=[],seen={};
  if(uniq&&n===26){out=A.split('').sort(function(){return secureInt(3)-1;});}
  else{
    while(out.length<n){
      var ch=A[secureInt(26)];
      if(uniq&&seen[ch])continue;
      seen[ch]=1;out.push(ch);
    }
  }
  document.getElementById('rl-out').textContent=out.join(' ');
});
})();</script>
"""


# ---------------------------------------------------------------- cubic feet
CUBICFT = """
<div class="tool" id="tt-cf">
  <div class="chips" role="tablist">
    <button class="chip active" data-u="ft">Feet</button>
    <button class="chip" data-u="cm">Centimeters</button>
  </div>
  <div class="fields">
    <div class="field"><label id="cf-l1" for="cf-l">Length (ft)</label><input type="number" id="cf-l" step="any" min="0" placeholder="2"></div>
    <div class="field"><label id="cf-l2" for="cf-w">Width (ft)</label><input type="number" id="cf-w" step="any" min="0" placeholder="2"></div>
    <div class="field"><label id="cf-l3" for="cf-h">Height (ft)</label><input type="number" id="cf-h" step="any" min="0" placeholder="1"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cf-out">-</span><span class="result-unit">cubic feet</span></div>
  <div class="stats">
    <div class="stat"><b id="cf-cuft">-</b><span>cubic feet</span></div>
    <div class="stat"><b id="cf-cum">-</b><span>cubic meters</span></div>
  </div>
</div>
<script>(function(){
var unit='ft';
var l=document.getElementById('cf-l'),w=document.getElementById('cf-w'),h=document.getElementById('cf-h');
document.querySelectorAll('#tt-cf .chip').forEach(function(c){c.addEventListener('click',function(){
  unit=c.dataset.u;
  document.querySelectorAll('#tt-cf .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  document.getElementById('cf-l1').textContent='Length ('+unit+')';
  document.getElementById('cf-l2').textContent='Width ('+unit+')';
  document.getElementById('cf-l3').textContent='Height ('+unit+')';
  run();
});});
function run(){
  var a=parseFloat(l.value),b=parseFloat(w.value),c=parseFloat(h.value);
  if(isNaN(a)||isNaN(b)||isNaN(c)){document.getElementById('cf-cuft').textContent='-';document.getElementById('cf-cum').textContent='-';return;}
  var cuft=unit==='ft'?a*b*c:(a*b*c)/28316.846592;
  document.getElementById('cf-cuft').textContent=(Math.round(cuft*100)/100).toLocaleString('en-US');
  document.getElementById('cf-cum').textContent=(Math.round(cuft*0.0283168466*1000)/1000).toLocaleString('en-US');
  document.getElementById('cf-out').textContent=(Math.round(cuft*100)/100).toLocaleString('en-US');
}
l.addEventListener('input',run);w.addEventListener('input',run);h.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- line sorter
SORTER = """
<div class="tool" id="tt-sort">
  <div class="chips">
    <button class="chip active" data-d="az">A-Z</button>
    <button class="chip" data-d="za">Z-A</button>
    <button class="chip active" id="sort-ci" type="button">Case-insensitive</button>
    <button class="chip" id="sort-blank" type="button">Remove blank lines</button>
    <button class="chip" id="sort-dup" type="button">Remove duplicates</button>
  </div>
  <div class="field"><label for="sort-in">Paste your list</label>
    <textarea id="sort-in" rows="8" placeholder="one item per line…"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="sort-out">Sorted <button class="btn btn-sm" id="sort-copy" type="button">Copy</button></label>
    <textarea id="sort-out" rows="8" readonly placeholder="sorted list appears here…"></textarea></div>
  <div class="stats"><div class="stat"><b id="sort-n">0</b><span>lines out</span></div></div>
</div>
<script>(function(){
var dir='az',ci=true,blank=false,dedupe=false;
var inp=document.getElementById('sort-in'),out=document.getElementById('sort-out');
function bind(id,set){document.getElementById(id).addEventListener('click',function(){set(!set.__v||set.__v===undefined?true:false);});}
var state={ci:true,blank:false,dedupe:false};
['ci','blank','dup'].forEach(function(k){
  var id=k==='ci'?'sort-ci':k==='blank'?'sort-blank':'sort-dup';
  var el=document.getElementById(id);
  el.addEventListener('click',function(){state[k]=!state[k];el.classList.toggle('active',state[k]);run();});
});
document.querySelectorAll('#tt-sort .chip[data-d]').forEach(function(c){c.addEventListener('click',function(){
  dir=c.dataset.d;
  document.querySelectorAll('#tt-sort .chip[data-d]').forEach(function(x){x.classList.toggle('active',x===c);});
  run();
});});
function run(){
  var lines=inp.value.split('\\n');
  if(state.blank)lines=lines.filter(function(L){return L.trim();});
  if(state.dedupe){var seen={};lines=lines.filter(function(L){if(seen.hasOwnProperty(L))return false;seen[L]=1;return true;});}
  lines.sort(function(x,y){
    var a=ci?x.toLowerCase():x,b=ci?y.toLowerCase():y;
    return dir==='az'?a.localeCompare(b):b.localeCompare(a);
  });
  out.value=lines.join('\\n');
  document.getElementById('sort-n').textContent=lines.length;
}
inp.addEventListener('input',run);
document.getElementById('sort-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('sort-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


# ---------------------------------------------------------------- unit price
UNITPRICE = """
<div class="tool" id="tt-up">
  <div class="fields">
    <div class="field"><label for="up-ap">Pack A price ($)</label><input type="number" id="up-ap" step="0.01" min="0" placeholder="3.40"></div>
    <div class="field"><label for="up-aq">Pack A quantity (g/ml/pcs)</label><input type="number" id="up-aq" step="any" min="0" placeholder="900"></div>
  </div>
  <div class="fields">
    <div class="field"><label for="up-bp">Pack B price ($)</label><input type="number" id="up-bp" step="0.01" min="0" placeholder="5.10"></div>
    <div class="field"><label for="up-bq">Pack B quantity</label><input type="number" id="up-bq" step="any" min="0" placeholder="1500"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="up-win">-</span></div>
  <div class="stats">
    <div class="stat"><b id="up-ua">-</b><span>A per unit</span></div>
    <div class="stat"><b id="up-ub">-</b><span>B per unit</span></div>
    <div class="stat"><b id="up-diff">-</b><span>B vs A</span></div>
  </div>
</div>
<script>(function(){
var ids=['up-ap','up-aq','up-bp','up-bq'];
function val(id){return parseFloat(document.getElementById(id).value);}
function money(n){return '$'+n.toLocaleString('en-US',{maximumFractionDigits:4});}
function run(){
  var ap=val('up-ap'),aq=val('up-aq'),bp=val('up-bp'),bq=val('up-bq');
  if(!ap||!aq||!bp||!bq){document.getElementById('up-win').textContent='-';
    document.getElementById('up-ua').textContent='-';document.getElementById('up-ub').textContent='-';
    document.getElementById('up-diff').textContent='-';return;}
  var ua=ap/aq,ub=bp/bq;
  document.getElementById('up-ua').textContent=money(ua);
  document.getElementById('up-ub').textContent=money(ub);
  var pct=Math.round((ub-ua)/ua*100);
  document.getElementById('up-diff').textContent=(pct>=0?'+':'')+pct+'%';
  document.getElementById('up-win').textContent=ua<ub?'Pack A is cheaper':'Pack B is cheaper';
}
ids.forEach(function(id){document.getElementById(id).addEventListener('input',run);});
run();
})();</script>
"""


# ---------------------------------------------------------------- word frequency
WORDFREQ = """
<div class="tool" id="tt-wf">
  <div class="chips"><button class="chip active" id="wf-stop" type="button">Ignore common words</button></div>
  <div class="field"><label for="wf-in">Paste text</label>
    <textarea id="wf-in" rows="7" placeholder="Paste an article, essay or transcript…"></textarea></div>
  <table class="copytable"><thead><tr><th>#</th><th>Word</th><th>Count</th><th>% of text</th></tr></thead><tbody id="wf-tb"></tbody></table>
</div>
<script>(function(){
var STOP={the:1,a:1,an:1,and:1,or:1,but:1,of:1,to:1,in:1,on:1,at:1,for:1,with:1,by:1,from:1,as:1,is:1,are:1,was:1,were:1,be:1,been:1,it:1,its:1,this:1,that:1,these:1,those:1,i:1,you:1,he:1,she:1,we:1,they:1,my:1,your:1,his:1,her:1,their:1,our:1,not:1,no:1,so:1,if:1,then:1,than:1,too:1,very:1,can:1,will:1,just:1};
var inp=document.getElementById('wf-in'),tb=document.getElementById('wf-tb');
var stop=document.getElementById('wf-stop');
var hideStop=true;
stop.addEventListener('click',function(){hideStop=!hideStop;this.classList.toggle('active',hideStop);run();});
function run(){
  var words=(inp.value.toLowerCase().match(/[a-z0-9\u00c0-\u024f']+/gi)||[]);
  var counts={};
  words.forEach(function(w){counts[w]=(counts[w]||0)+1;});
  var rows=Object.keys(counts).map(function(w){return [w,counts[w]];});
  rows.sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0]);});
  var html='',shown=0,total=words.length||1;
  for(var i=0;i<rows.length&&shown<25;i++){
    if(hideStop&&STOP[rows[i][0]])continue;
    shown++;
    html+='<tr><td>'+shown+'</td><td>'+rows[i][0]+'</td><td>'+rows[i][1]+'</td><td>'+Math.round(rows[i][1]/total*1000)/10+'%</td></tr>';
  }
  tb.innerHTML=html||'<tr><td colspan="4" style="color:#94a3b8">Paste text to see word frequencies…</td></tr>';
}
inp.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- degrees <-> radians
DEGRAD = """
<div class="tool" id="tt-dr">
  <div class="fields two">
    <div class="field"><label for="dr-deg">Degrees (°)</label><input type="number" id="dr-deg" step="any" placeholder="90"></div>
    <div class="field"><label for="dr-rad">Radians (number or 3pi/4)</label><input type="text" id="dr-rad" placeholder="1.5708"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dr-out">-</span><div class="result-formula" id="dr-note"></div></div>
  <table class="copytable"><thead><tr><th>Degrees</th><th>Radians (exact)</th><th>Decimal</th></tr></thead><tbody>
  <tr><td>30</td><td>pi/6</td><td>0.5236</td></tr><tr><td>45</td><td>pi/4</td><td>0.7854</td></tr>
  <tr><td>60</td><td>pi/3</td><td>1.0472</td></tr><tr><td>90</td><td>pi/2</td><td>1.5708</td></tr>
  <tr><td>180</td><td>pi</td><td>3.1416</td></tr><tr><td>270</td><td>3pi/2</td><td>4.7124</td></tr>
  <tr><td>360</td><td>2pi</td><td>6.2832</td></tr></tbody></table>
</div>
<script>(function(){
var DEG=document.getElementById('dr-deg'),RAD=document.getElementById('dr-rad');
var out=document.getElementById('dr-out'),note=document.getElementById('dr-note');
var lock=false;
function cleanPi(v){
  v=v.trim().toLowerCase().replace(/\s/g,'');
  var m=v.match(/^(-?)(\d*\.?\d*)\*?pi(?:\/(\d+))?$/);
  if(m){var k=m[2]===''?1:parseFloat(m[2]);var r=m[3]?k/(+m[3]):k;return (m[1]==='-'?-1:1)*r*Math.PI;}
  var f=parseFloat(v);
  return isNaN(f)?null:f;
}
function exactForm(deg){
  var common={30:'pi/6',45:'pi/4',60:'pi/3',90:'pi/2',120:'2pi/3',135:'3pi/4',150:'5pi/6',180:'pi',270:'3pi/2',360:'2pi'};
  return common[deg]||null;
}
DEG.addEventListener('input',function(){
  if(lock)return;lock=true;
  var d=parseFloat(DEG.value);
  if(isNaN(d)){out.textContent='-';note.textContent='';RAD.value='';lock=false;return;}
  var r=d*Math.PI/180,ex=exactForm(Math.abs(d));
  RAD.value=(Math.round(r*10000)/10000)+'';
  out.textContent=(Math.round(r*10000)/10000)+' rad';
  note.textContent=ex?(d+' deg = '+ex+' rad (exact)'):(d+' deg = '+d+' x pi/180 rad');
  lock=false;
});
RAD.addEventListener('input',function(){
  if(lock)return;lock=true;
  var r=cleanPi(this.value);
  if(r===null){out.textContent='-';note.textContent='';DEG.value='';lock=false;return;}
  var d=r*180/Math.PI;
  DEG.value=Math.round(d*100)/100+'';
  out.textContent=(Math.round(d*100)/100)+' deg';
  note.textContent=(Math.round(r*10000)/10000)+' rad = '+Math.round(d*100)/100+' deg';
  lock=false;
});
})();</script>
"""


# ---------------------------------------------------------------- roman table 1-100
def _roman_static(n):
    M = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    out = ""
    for v, sym in M:
        while n >= v:
            out += sym
            n -= v
    return out

ROMANTABLE = """
<table class="copytable" id="tt-rt100">
<thead><tr><th>1-25</th><th>26-50</th><th>51-75</th><th>76-100</th></tr></thead>
<tbody>__ROWS__</tbody>
</table>
<div class="tool-note">Seven symbols, one rule: smaller numeral before a larger one subtracts (IV = 4, XC = 90). Everything else adds.</div>
"""

def _render_romantable(args):
    vals = {n: _roman_static(n) for n in range(1, 101)}
    rows = []
    for r in range(25):
        cells = []
        for off in (0, 25, 50, 75):
            n = r + 1 + off
            cells.append(f"<td>{n} = <b>{vals[n]}</b></td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return ROMANTABLE.replace("__ROWS__", "\n".join(rows))



# ---------------------------------------------------------------- yes or no
YESNO = """
<div class="tool" id="tt-yn" style="text-align:center">
  <div class="result" aria-live="polite" aria-atomic="true" style="border:0;background:transparent"><span class="result-num" id="yn-out" style="font-size:3rem">?</span></div>
  <button class="btn" id="yn-go" type="button" style="font-size:1.1rem;padding:14px 34px">Ask</button>
  <div class="stats" style="max-width:320px;margin:14px auto 0">
    <div class="stat"><b id="yn-y">0</b><span>yes</span></div>
    <div class="stat"><b id="yn-n">0</b><span>no</span></div>
  </div>
</div>
<script>(function(){
var y=0,n=0;
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
document.getElementById("yn-go").addEventListener("click",function(){
  var yes=secureInt(2);
  var o=document.getElementById("yn-out");
  o.textContent=yes?"YES":"NO";
  o.style.color=yes?"#16a34a":"#dc2626";
  if(yes)y++;else n++;
  document.getElementById("yn-y").textContent=y;
  document.getElementById("yn-n").textContent=n;
});
})();</script>
"""


# ---------------------------------------------------------------- prime checker
PRIME = """
<div class="tool" id="tt-pr">
  <div class="field"><label for="pr-in">Whole number (up to 15 digits)</label>
    <input type="number" id="pr-in" step="1" placeholder="1009"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pr-out">-</span>
    <div class="result-formula" id="pr-note"></div></div>
</div>
<script>(function(){
var inp=document.getElementById('pr-in'),out=document.getElementById('pr-out'),note=document.getElementById('pr-note');
function isPrime(n){
  if(n<2)return [false,null];
  for(var p of [2,3,5,7,11,13,17,19,23,29,31,37]){if(n===p)return [true,null];if(n%p===0)return [false,p];}
  var d=n-1,r=0;while(d%2===0){d/=2;r++;}
  var bases=[2,3,5,7,11,13,17,19,23,29,31,37];
  for(var i=0;i<bases.length;i++){
    var x=1,base=bases[i]%n;if(base===0)continue;
    var pow=1,dd=d;
    for(var j=0;j<60&&dd;j++){if(dd&1)pow=pow*base%n;dd>>=1;var tmp=base*base%n;base=tmp?tmp:base;dd=dd;}
    x=pow;
    if(x===1||x===n-1)continue;
    var comp=true;
    for(var k=0;k<r-1;k++){x=x*x%n;if(x===n-1){comp=false;break;}}
    if(comp)return [false,2];
  }
  var lim=Math.sqrt(n);
  for(var f=41;f<=lim;f+=2){if(n%f===0)return [false,f];}
  return [true,null];
}
inp.addEventListener('input',function(){
  var v=this.value.trim();
  if(v===''){out.textContent='-';note.textContent='';return;}
  if(!/^\d+$/.test(v)){out.textContent='-';note.textContent='Whole numbers only.';return;}
  var n=BigInt(v);
  if(n<2n){out.textContent='Not prime';note.textContent='Numbers below 2 are neither prime nor composite.';return;}
  var small=[2n,3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n];
  for(var i=0;i<small.length;i++){
    if(n===small[i]){out.textContent='Prime!';note.textContent=v+' is prime (it is in the base list).';return;}
    if(n%small[i]===0n){out.textContent='Not prime';note.textContent='Divisible by '+small[i]+'.';return;}
  }
  var ok=true,factor=null;
  if(v.length<=15){
    var num=Number(v);
    if(num<=Number.MAX_SAFE_INTEGER){
      var d=num-1n?0:0;
      ok=probablePrime(num);
      if(!ok){for(var f=2n;f*f<=n;f++){if(n%f===0n){factor=f;break;}}}
    }
  }
  out.textContent=ok?'Prime!':'Probably composite';
  note.textContent=ok?(v+' is prime.'):(v+' is composite'+(factor?' - divisible by '+factor.toString():' - no small factor found (use a factoring tool).'));
});
function probablePrime(n){
  var d=n-1n,r=0n;while(d%2n===0n){d/=2n;r++;}
  var bases=[2n,3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n];
  for(var i=0;i<bases.length;i++){
    var a=bases[i]%n;if(a===0n)continue;
    var x=1n,base=a,dd=d;
    while(dd>0n){if(dd&1n)x=x*base%n;base=base*base%n;dd>>=1n;}
    if(x===1n||x===n-1n)continue;
    var composite=true;
    for(var k=1n;k<r;k++){x=x*x%n;if(x===n-1n){composite=false;break;}}
    if(composite)return false;
  }
  return true;
}
})();</script>
"""


# ---------------------------------------------------------------- factorial
FACTORIAL = """
<div class="tool" id="tt-fa">
  <div class="field"><label for="fa-n">n (0 - 1000)</label><input type="number" id="fa-n" min="0" max="1000" step="1" value="5"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fa-out" style="word-break:break-all">-</span></div>
  <div class="stats">
    <div class="stat"><b id="fa-digits">-</b><span>digits</span></div>
    <div class="stat"><b id="fa-chain">-</b><span>multiplication</span></div>
  </div>
</div>
<script>(function(){
function bigFact(n){
  var a=[1n];
  for(var i=2n;i<=n;i++){
    var carry=0n;
    for(var j=0;j<a.length;j++){var p=a[j]*i+carry;a[j]=p%10n;carry=p/10n;}
    while(carry>0n){a.push(carry%10n);carry/=10n;}
  }
  return a.reverse().join('');
}
var inp=document.getElementById('fa-n');
function run(){
  var n=parseInt(inp.value);
  if(isNaN(n)||n<0||n>1000){document.getElementById('fa-out').textContent='0 to 1000 only';document.getElementById('fa-digits').textContent='-';document.getElementById('fa-chain').textContent='-';return;}
  if(n===0){document.getElementById('fa-out').textContent='1';document.getElementById('fa-digits').textContent='1';document.getElementById('fa-chain').textContent='0! = 1 by definition';return;}
  var f=bigFact(n);
  document.getElementById('fa-out').textContent=f;
  document.getElementById('fa-digits').textContent=f.length.toLocaleString('en-US');
  var chain=n<=10?Array.from({length:n},(_,i)=>i+1).join(' x ')+' = '+f:(n+'! = 1 x 2 x ... x '+n);
  document.getElementById('fa-chain').textContent=chain;
}
inp.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- random country
COUNTRY = """
<div class="tool" id="tt-co">
  <div class="field"><label for="co-cont">Continent</label>
    <select id="co-cont">
      <option value="all">Anywhere on Earth</option>
      <option value="Africa">Africa</option>
      <option value="Americas">Americas</option>
      <option value="Asia">Asia</option>
      <option value="Europe">Europe</option>
      <option value="Oceania">Oceania</option>
    </select></div>
  <button class="btn" id="co-go" type="button">🌍 Generate country</button>
  <div class="result" aria-live="polite" aria-atomic="true" style="text-align:center"><span class="result-num" id="co-flag" style="font-size:3.2rem">🌍</span></div>
  <div class="result" aria-live="polite" aria-atomic="true" style="margin-top:-8px"><span class="result-num" id="co-name" style="font-size:1.4rem">?</span>
    <div class="result-formula" id="co-cont2"></div></div>
</div>
<script>(function(){
var C=[
["Afghanistan","Asia","🇦🇫"],["Albania","Europe","🇦🇱"],["Algeria","Africa","🇩🇿"],["Andorra","Europe","🇦🇩"],["Angola","Africa","🇦🇴"],["Argentina","Americas","🇦🇷"],["Armenia","Asia","🇦🇲"],["Australia","Oceania","🇦🇺"],["Austria","Europe","🇦🇹"],["Azerbaijan","Asia","🇦🇿"],
["Bahamas","Americas","🇧🇸"],["Bahrain","Asia","🇧🇭"],["Bangladesh","Asia","🇧🇩"],["Barbados","Americas","🇧🇧"],["Belarus","Europe","🇧🇾"],["Belgium","Europe","🇧🇪"],["Belize","Americas","🇧🇿"],["Benin","Africa","🇧🇯"],["Bhutan","Asia","🇧🇹"],["Bolivia","Americas","🇧🇴"],
["Botswana","Africa","🇧🇼"],["Brazil","Americas","🇧🇷"],["Brunei","Asia","🇧🇳"],["Bulgaria","Europe","🇧🇬"],["Burkina Faso","Africa","🇧🇫"],["Burundi","Africa","🇧🇮"],["Cambodia","Asia","🇰🇭"],["Cameroon","Africa","🇨🇲"],["Canada","Americas","🇨🇦"],["Chad","Africa","🇹🇩"],
["Chile","Americas","🇨🇱"],["China","Asia","🇨🇳"],["Colombia","Americas","🇨🇴"],["Costa Rica","Americas","🇨🇷"],["Croatia","Europe","🇭🇷"],["Cuba","Americas","🇨🇺"],["Cyprus","Europe","🇨🇾"],["Czechia","Europe","🇨🇿"],["Denmark","Europe","🇩🇰"],["Djibouti","Africa","🇩🇯"],
["Dominica","Americas","🇩🇲"],["Ecuador","Americas","🇪🇨"],["Egypt","Africa","🇪🇬"],["El Salvador","Americas","🇸🇻"],["Estonia","Europe","🇪🇪"],["Eswatini","Africa","🇸🇿"],["Ethiopia","Africa","🇪🇹"],["Fiji","Oceania","🇫🇯"],["Finland","Europe","🇫🇮"],["France","Europe","🇫🇷"],
["Gabon","Africa","🇬🇦"],["Gambia","Africa","🇬🇲"],["Georgia","Asia","🇬🇪"],["Germany","Europe","🇩🇪"],["Ghana","Africa","🇬🇭"],["Greece","Europe","🇬🇷"],["Grenada","Americas","🇬🇩"],["Guatemala","Americas","🇬🇹"],["Guinea","Africa","🇬🇳"],["Guyana","Americas","🇬🇾"],
["Haiti","Americas","🇭🇹"],["Honduras","Americas","🇭🇳"],["Hungary","Europe","🇭🇺"],["Iceland","Europe","🇮🇸"],["India","Asia","🇮🇳"],["Indonesia","Asia","🇮🇩"],["Iran","Asia","🇮🇷"],["Iraq","Asia","🇮🇶"],["Ireland","Europe","🇮🇪"],["Israel","Asia","🇮🇱"],
["Italy","Europe","🇮🇹"],["Jamaica","Americas","🇯🇲"],["Japan","Asia","🇯🇵"],["Jordan","Asia","🇯🇴"],["Kazakhstan","Asia","🇰🇿"],["Kenya","Africa","🇰🇪"],["Kiribati","Oceania","🇰🇮"],["Kuwait","Asia","🇰🇼"],["Kyrgyzstan","Asia","🇰🇬"],["Laos","Asia","🇱🇦"],
["Latvia","Europe","🇱🇻"],["Lebanon","Asia","🇱🇧"],["Lesotho","Africa","🇱🇸"],["Liberia","Africa","🇱🇷"],["Liechtenstein","Europe","🇱🇮"],["Lithuania","Europe","🇱🇹"],["Luxembourg","Europe","🇱🇺"],["Madagascar","Africa","🇲🇬"],["Malawi","Africa","🇲🇼"],["Malaysia","Asia","🇲🇾"],
["Maldives","Asia","🇲🇻"],["Mali","Africa","🇲🇱"],["Malta","Europe","🇲🇹"],["Marshall Islands","Oceania","🇲🇭"],["Mauritania","Africa","🇲🇷"],["Mauritius","Africa","🇲🇺"],["Mexico","Americas","🇲🇽"],["Moldova","Europe","🇲🇩"],["Monaco","Europe","🇲🇨"],["Mongolia","Asia","🇲🇳"],
["Montenegro","Europe","🇲🇪"],["Morocco","Africa","🇲🇦"],["Mozambique","Africa","🇲🇿"],["Myanmar","Asia","🇲🇲"],["Namibia","Africa","🇳🇦"],["Nauru","Oceania","🇳🇷"],["Nepal","Asia","🇳🇵"],["Netherlands","Europe","🇳🇱"],["New Zealand","Oceania","🇳🇿"],["Nicaragua","Americas","🇳🇮"],
["Niger","Africa","🇳🇪"],["Nigeria","Africa","🇳🇬"],["North Korea","Asia","🇰🇵"],["North Macedonia","Europe","🇲🇰"],["Norway","Europe","🇳🇴"],["Oman","Asia","🇴🇲"],["Pakistan","Asia","🇵🇰"],["Palau","Oceania","🇵🇼"],["Panama","Americas","🇵🇦"],["Papua New Guinea","Oceania","🇵🇬"],
["Paraguay","Americas","🇵🇾"],["Peru","Americas","🇵🇪"],["Philippines","Asia","🇵🇭"],["Poland","Europe","🇵🇱"],["Portugal","Europe","🇵🇹"],["Qatar","Asia","🇶🇦"],["Romania","Europe","🇷🇴"],["Russia","Europe","🇷🇺"],["Rwanda","Africa","🇷🇼"],["Samoa","Oceania","🇼🇸"],
["San Marino","Europe","🇸🇲"],["Sao Tome and Principe","Africa","🇸🇹"],["Saudi Arabia","Asia","🇸🇦"],["Senegal","Africa","🇸🇳"],["Serbia","Europe","🇷🇸"],["Seychelles","Africa","🇸🇨"],["Sierra Leone","Africa","🇸🇱"],["Singapore","Asia","🇸🇬"],["Slovakia","Europe","🇸🇰"],["Slovenia","Europe","🇸🇮"],
["Solomon Islands","Oceania","🇸🇧"],["Somalia","Africa","🇸🇴"],["South Africa","Africa","🇿🇦"],["South Korea","Asia","🇰🇷"],["South Sudan","Africa","🇸🇸"],["Spain","Europe","🇪🇸"],["Sri Lanka","Asia","🇱🇰"],["Sudan","Africa","🇸🇩"],["Suriname","Americas","🇸🇷"],["Sweden","Europe","🇸🇪"],
["Switzerland","Europe","🇨🇭"],["Syria","Asia","🇸🇾"],["Tajikistan","Asia","🇹🯯"],["Tanzania","Africa","🇹🇿"],["Thailand","Asia","🇹🇭"],["Timor-Leste","Asia","🇹🇱"],["Togo","Africa","🇹🇬"],["Tonga","Oceania","🇹🇴"],["Trinidad and Tobago","Americas","🇹🇹"],["Tunisia","Africa","🇹🇳"],
["Turkey","Asia","🇹🇷"],["Turkmenistan","Asia","🇹🇲"],["Tuvalu","Oceania","🇹🇻"],["Uganda","Africa","🇺🇬"],["Ukraine","Europe","🇺🇦"],["United Arab Emirates","Asia","🇦🇪"],["United Kingdom","Europe","🇬🇧"],["United States","Americas","🇺🇸"],["Uruguay","Americas","🇺🇾"],["Uzbekistan","Asia","🇺🇿"],
["Vanuatu","Oceania","🇻🇺"],["Vatican City","Europe","🇻🇦"],["Venezuela","Americas","🇻🇪"],["Vietnam","Asia","🇻🇳"],["Yemen","Asia","🇾🇪"],["Zambia","Africa","🇿🇲"],["Zimbabwe","Africa","🇿🇼"]
];
var cont=document.getElementById('co-cont');
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
document.getElementById('co-go').addEventListener('click',function(){
  var pool=cont.value==='all'?C:C.filter(function(c){return c[1]===cont.value;});
  if(!pool.length)return;
  var pick=pool[secureInt(pool.length)];
  document.getElementById('co-flag').textContent=pick[2];
  document.getElementById('co-name').textContent=pick[0];
  document.getElementById('co-cont2').textContent=pick[1];
});
})();</script>
"""


# ---------------------------------------------------------------- st+lb <-> kg
STLB = """
<div class="tool" id="tt-sl">
  <div class="fields">
    <div class="field"><label for="sl-st">Stone</label><input type="number" id="sl-st" min="0" step="1" value="11"></div>
    <div class="field"><label for="sl-lb">Pounds</label><input type="number" id="sl-lb" min="0" max="13" step="1" value="7"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sl-kg">-</span><span class="result-unit">kg</span></div>
  <div class="field" style="margin-top:12px"><label for="sl-kg2">Kilograms (reverse)</label><input type="number" id="sl-kg2" step="any" min="0" placeholder="70"></div>
  <div class="stats">
    <div class="stat"><b id="sl-total-lb">-</b><span>pounds only</span></div>
    <div class="stat"><b id="sl-split">-</b><span>st + lb split</span></div>
  </div>
</div>
<script>(function(){
var st=document.getElementById('sl-st'),lb=document.getElementById('sl-lb'),kg2=document.getElementById('sl-kg2');
var lock=false;
function kgFrom(st_,lb_){return st_*6.35029318+lb_*0.45359237;}
function runSTLB(){
  if(lock)return;lock=true;kg2.value='';
  var s=parseFloat(st.value)||0,p=parseFloat(lb.value)||0;
  var kg=kgFrom(s,p);
  document.getElementById('sl-kg').textContent=(Math.round(kg*100)/100).toLocaleString('en-US');
  document.getElementById('sl-total-lb').textContent=Math.round(s*14+p).toLocaleString('en-US');
  document.getElementById('sl-split').textContent='-';
  lock=false;
}
function runKG(){
  if(lock)return;lock=true;st.value='';lb.value='';
  var k=parseFloat(kg2.value);
  if(isNaN(k)||k<0){lock=false;return;}
  var totalLb=k/0.45359237,stones=Math.floor(totalLb/14),lbs=totalLb-stones*14;
  document.getElementById('sl-st').value=stones;
  document.getElementById('sl-lb').value=Math.round(lbs);
  document.getElementById('sl-kg').textContent=(Math.round(k*100)/100).toLocaleString('en-US');
  document.getElementById('sl-total-lb').textContent=Math.round(totalLb).toLocaleString('en-US');
  document.getElementById('sl-split').textContent=stones+' st '+Math.round(lbs)+' lb';
  lock=false;
}
st.addEventListener('input',runSTLB);lb.addEventListener('input',runSTLB);
kg2.addEventListener('input',runKG);
runSTLB();
})();</script>
"""



# ---------------------------------------------------------------- ft+in <-> cm
FTINCM = """
<div class="tool" id="tt-fi">
  <div class="fields">
    <div class="field"><label for="fi-ft">Feet</label><input type="number" id="fi-ft" min="0" step="1" value="5"></div>
    <div class="field"><label for="fi-in">Inches</label><input type="number" id="fi-in" min="0" max="11" step="any" value="7"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fi-cm">-</span><span class="result-unit">cm</span></div>
  <div class="field" style="margin-top:12px"><label for="fi-cm2">Centimeters (reverse)</label><input type="number" id="fi-cm2" step="any" min="0" placeholder="170"></div>
  <div class="stats">
    <div class="stat"><b id="fi-inonly">-</b><span>inches only</span></div>
    <div class="stat"><b id="fi-split">-</b><span>ft + in split</span></div>
  </div>
</div>
<script>(function(){
var ft=document.getElementById('fi-ft'),inch=document.getElementById('fi-in'),cm2=document.getElementById('fi-cm2');
var lock=false;
function cmFrom(f,i){return f*30.48+i*2.54;}
function runFI(){
  if(lock)return;lock=true;cm2.value='';
  var f=parseFloat(ft.value)||0,i=parseFloat(inch.value)||0;
  var cm=cmFrom(f,i);
  document.getElementById('fi-cm').textContent=(Math.round(cm*100)/100).toLocaleString('en-US');
  document.getElementById('fi-inonly').textContent=(Math.round(cm/2.54*10)/10).toLocaleString('en-US');
  document.getElementById('fi-split').textContent='-';
  lock=false;
}
function runCM(){
  if(lock)return;lock=true;ft.value='';inch.value='';
  var c=parseFloat(cm2.value);
  if(isNaN(c)||c<0){lock=false;return;}
  var inOnly=c/2.54,feet=Math.floor(inOnly/12),ins=inOnly-feet*12;
  document.getElementById('fi-ft').value=feet;
  document.getElementById('fi-in').value=Math.round(ins*10)/10;
  document.getElementById('fi-cm').textContent=(Math.round(c*100)/100).toLocaleString('en-US');
  document.getElementById('fi-inonly').textContent=(Math.round(inOnly*10)/10).toLocaleString('en-US');
  document.getElementById('fi-split').textContent=feet+' ft '+Math.round(ins*10)/10+' in';
  lock=false;
}
ft.addEventListener('input',runFI);inch.addEventListener('input',runFI);
cm2.addEventListener('input',runCM);
runFI();
})();</script>
"""



# ---------------------------------------------------------------- random emoji
EMOJI = """
<div class="tool" id="tt-em">
  <div class="chips" id="em-cat">
    <button class="chip active" data-c="all">All</button>
    <button class="chip" data-c="face">Faces</button>
    <button class="chip" data-c="animal">Animals</button>
    <button class="chip" data-c="food">Food</button>
    <button class="chip" data-c="object">Objects</button>
    <button class="chip" data-c="symbol">Symbols</button>
  </div>
  <div class="field"><label for="em-n">How many</label><input type="number" id="em-n" min="1" max="12" step="1" value="3"></div>
  <button class="btn" id="em-go" type="button">Generate</button>
  <div class="result" aria-live="polite" aria-atomic="true" style="text-align:center"><span class="result-num" id="em-out" style="font-size:2.2rem;letter-spacing:.15em">?</span></div>
  <button class="btn btn-sm" id="em-copy" type="button">Copy batch</button>
</div>
<script>(function(){
var E={
face:["😀","😁","😂","🤣","😊","😍","🥰","😎","🤩","🥳","😢","😭","😡","🤯","😱","🤔","😴","🤒","🥶","🥵","😈","🤡","👻","💀","🤖"],
animal:["🐶","🐱","🦊","🐻","🐼","🐨","🦁","🐮","🐷","🐸","🐵","🐔","🐧","🦅","🦉","🦄","🐝","🦋","🐢","🐙","🦈","🐬","🐳","🦕","🦖"],
food:["🍎","🍊","🍋","🍉","🍇","🍓","🫐","🍒","🥑"," broccoli".slice(0,0)+"🥦","🌽","🍕","🍔","🌮","🍣","🍦","🍩","🍪","🎂","☕","🍺","🥑"],
object:["📱","💻","⌚","📷","🎧","🎮","📚","✏️","💡","🔑","🔒","💎","🚗","✈️","🚀","⚽","🏀","🎸","🎨","🧸"],
symbol:["❤️","🧡","💛","💚","💙","💜","🔥","⭐","🌟","✨","⚡","🌈","☀️","🌙","☔","💯","✅","❌","♻️","🔔"]
};
var cat="all";
var out=document.getElementById('em-out');
function pool(){return cat==="all"?Object.values(E).flat():E[cat];}
function secureInt(max){var b=new Uint32Array(1),lim=Math.floor(4294967296/max)*max,x;
  do{crypto.getRandomValues(b);x=b[0];}while(x>=lim);return x%max;}
var last="";
document.getElementById('em-go').addEventListener('click',function(){
  var n=Math.min(12,Math.max(1,parseInt(document.getElementById('em-n').value)||3));
  var p=pool(),res=[];
  for(var i=0;i<n;i++)res.push(p[secureInt(p.length)]);
  last=res.join(" ");
  out.textContent=last;
});
document.getElementById('em-copy').addEventListener('click',function(){
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(last||out.textContent);}
  else{out.select();document.execCommand("copy");}
  var b=document.getElementById("em-copy");b.textContent="Copied!";setTimeout(function(){b.textContent="Copy batch";},1200);
});
document.querySelectorAll('#em-cat .chip').forEach(function(c){c.addEventListener('click',function(){
  cat=c.dataset.c;
  document.querySelectorAll('#em-cat .chip').forEach(function(x){x.classList.toggle('active',x===c);});
});});
})();</script>
"""


# ---------------------------------------------------------------- hex <-> rgb
HEXRGB = """
<div class="tool" id="tt-hr">
  <div class="fields">
    <div class="field"><label for="hr-hex">HEX color</label><input type="text" id="hr-hex" placeholder="#1A73E8" autocomplete="off"></div>
    <div class="field"><label for="hr-r">R (0-255)</label><input type="number" id="hr-r" min="0" max="255" step="1" placeholder="26"></div>
    <div class="field"><label for="hr-g">G (0-255)</label><input type="number" id="hr-g" min="0" max="255" step="1" placeholder="115"></div>
    <div class="field"><label for="hr-b">B (0-255)</label><input type="number" id="hr-b" min="0" max="255" step="1" placeholder="232"></div>
  </div>
  <div class="chips"><button class="chip" id="hr-sh" type="button">Random color</button></div>
  <div class="color-preview" id="hr-preview"></div>
  <div class="stats">
    <div class="stat"><b id="hr-hexout">-</b><span>hex</span></div>
    <div class="stat"><b id="hr-rgbout">-</b><span>rgb()</span></div>
  </div>
</div>
<script>(function(){
var HEX=document.getElementById('hr-hex'),R=document.getElementById('hr-r'),G=document.getElementById('hr-g'),B=document.getElementById('hr-b');
var prev=document.getElementById('hr-preview');
var lock=false;
function clamp(v){return Math.max(0,Math.min(255,Math.round(v)||0));}
function hex2rgb(v){
  v=v.trim().replace('#','');
  if(/^[0-9a-fA-F]{3}$/.test(v))v=v.split('').map(function(c){return c+c;}).join('');
  if(!/^[0-9a-fA-F]{6}$/.test(v))return null;
  return {r:parseInt(v.slice(0,2),16),g:parseInt(v.slice(2,4),16),b:parseInt(v.slice(4,6),16),hex:'#'+v.toUpperCase()};
}
function upd(r,g,b){
  prev.style.background='rgb('+r+','+g+','+b+')';
  var hx='#'+[r,g,b].map(function(x){return x.toString(16).padStart(2,'0').toUpperCase();}).join('');
  document.getElementById('hr-hexout').textContent=hx;
  document.getElementById('hr-rgbout').textContent='rgb('+r+', '+g+', '+b+')';
}
HEX.addEventListener('input',function(){
  if(lock)return;lock=true;
  var c=hex2rgb(this.value);
  if(c){R.value=c.r;G.value=c.g;B.value=c.b;upd(c.r,c.g,c.b);}
  lock=false;
});
[R,G,B].forEach(function(el){el.addEventListener('input',function(){
  if(lock)return;lock=true;
  var r=clamp(parseFloat(R.value)),g=clamp(parseFloat(G.value)),b=clamp(parseFloat(B.value));
  upd(r,g,b);
  lock=false;
});});
document.getElementById('hr-sh').addEventListener('click',function(){
  var r=Math.floor(Math.random()*256),g=Math.floor(Math.random()*256),b=Math.floor(Math.random()*256);
  lock=true;R.value=r;G.value=g;B.value=b;upd(r,g,b);
  HEX.value='#'+[r,g,b].map(function(x){return x.toString(16).padStart(2,'0').toUpperCase();}).join('');
  lock=false;
});
})();</script>
"""


# ---------------------------------------------------------------- age on planets
PLANETS = """
<div class="tool" id="tt-pl">
  <div class="field"><label for="pl-age">Your age in Earth years</label><input type="number" id="pl-age" step="any" min="0" value="30"></div>
  <table class="copytable"><thead><tr><th>Planet</th><th>Your age</th><th>Orbit (Earth years)</th></tr></thead><tbody id="pl-tb"></tbody></table>
</div>
<script>(function(){
var P=[["Mercury",0.2408467,"\u2605"],["Venus",0.61519726,"\u2605"],["Mars",1.8808158,"\u2605"],["Jupiter",11.862615,"\u2605"],["Saturn",29.447498,"\u2605"],["Uranus",84.016846,"\u2605"],["Neptune",164.79132,"\u2605"]];
var inp=document.getElementById('pl-age'),tb=document.getElementById('pl-tb');
function run(){
  var age=parseFloat(inp.value);
  if(isNaN(age)){tb.innerHTML='';return;}
  var html=P.map(function(p){
    var a=Math.round(age/p[1]*100)/100;
    return '<tr><td>'+p[0]+'</td><td><b>'+a+'</b></td><td>'+p[1]+'</td></tr>';
  }).join('');
  tb.innerHTML=html;
}
inp.addEventListener('input',run);run();
})();</script>
"""


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


# ---------------------------------------------------------------- whitespace cleaner
WHITESPACE = """
<div class="tool" id="tt-ws">
  <div class="chips">
    <button class="chip active" id="ws-trim" type="button">Trim line edges</button>
    <button class="chip active" id="ws-collapse" type="button">Collapse space runs</button>
    <button class="chip" id="ws-blank" type="button">Remove blank lines</button>
  </div>
  <div class="field"><label for="ws-in">Messy text</label>
    <textarea id="ws-in" rows="8" placeholder="   paste  text with   stray spaces…  "></textarea></div>
  <div class="stats">
    <div class="stat"><b id="ws-inlines">-</b><span>lines in</span></div>
    <div class="stat"><b id="ws-chars">-</b><span>chars removed</span></div>
  </div>
  <div class="field" style="margin-top:10px"><label for="ws-out">Cleaned <button class="btn btn-sm" id="ws-copy" type="button">Copy</button></label>
    <textarea id="ws-out" rows="8" readonly placeholder="clean text appears here…"></textarea></div>
</div>
<script>(function(){
var inp=document.getElementById('ws-in'),out=document.getElementById('ws-out');
var st={trim:true,collapse:true,blank:false};
['ws-trim','ws-collapse','ws-blank'].forEach(function(id){
  var key=id.replace('ws-','');
  var el=document.getElementById(id);
  el.addEventListener('click',function(){st[key]=!st[key];el.classList.toggle('active',st[key]);run();});
});
function run(){
  var t=inp.value;
  if(!t){out.value='';document.getElementById('ws-inlines').textContent='0';document.getElementById('ws-chars').textContent='0';return;}
  var before=t.length;
  var lines=t.split('\\n');
  lines=lines.map(function(L){
    var x=L;
    if(st.trim)x=x.trim();
    if(st.collapse)x=x.replace(/ {2,}/g,' ');
    return x;
  });
  if(st.blank)lines=lines.filter(function(L){return L.trim();});
  var res=lines.join('\\n');
  out.value=res;
  document.getElementById('ws-inlines').textContent=lines.length.toLocaleString('en-US');
  document.getElementById('ws-chars').textContent=Math.max(0,before-res.length).toLocaleString('en-US');
}
inp.addEventListener('input',run);
['ws-trim','ws-collapse','ws-blank'].forEach(function(id){document.getElementById(id).addEventListener('click',run);});
document.getElementById('ws-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('ws-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


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
  return v.trim().split(/\s+/).filter(Boolean).map(function(g){
    if(!/^[01]{1,8}$/.test(g))throw 'bad';
    return parseInt(g,2).toString(16).toUpperCase().padStart(Math.ceil(g.length/4),'0');
  }).join(' ');
}
function hexToBin(v){
  return v.trim().split(/\s+/).filter(Boolean).map(function(g){
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


# ---------------------------------------------------------------- number to words
NUMWORDS = """
<div class="tool" id="tt-nw">
  <div class="field"><label for="nw-in">Number (0 - 999,999,999,999,999)</label>
    <input type="text" id="nw-in" inputmode="numeric" placeholder="1234"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="nw-out" style="text-transform:capitalize">-</span></div>
  <div class="tool-note">Standard American wording: no "and" before the tens, hyphenated compounds (forty-two), scale words up to trillion.</div>
</div>
<script>(function(){
var ONES=["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"];
var TENS=["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"];
var SCALES=[""," thousand"," million"," billion"," trillion"];
function under1000(n){
  var s="";
  if(n>=100){s+=ONES[Math.floor(n/100)]+" hundred";n%=100;if(n)s+=" ";}
  if(n>=20){s+=TENS[Math.floor(n/10)];if(n%10)s+="-"+ONES[n%10];}
  else if(n>0)s+=ONES[n];
  return s;
}
function toWords(numStr){
  numStr=numStr.replace(/,/g,"").replace(/^0+(?=\d)/,"");
  if(!/^\d{1,15}$/.test(numStr))return null;
  var groups=[];
  var v=numStr;
  while(v.length>0){groups.unshift(v.slice(-3));v=v.slice(0,-3);}
  var parts=[];
  groups.forEach(function(g,i){
    var n=parseInt(g,10);
    if(n)parts.push(under1000(n)+SCALES[groups.length-1-i]);
  });
  if(!parts.length)return "zero";
  return parts.join(" ");
}
var inp=document.getElementById("nw-in"),out=document.getElementById("nw-out");
inp.addEventListener("input",function(){
  var v=this.value.trim();
  if(!v){out.textContent="-";return;}
  var w=toWords(v);
  out.textContent=w||"0 to 999,999,999,999,999 only, digits only";
});
})();</script>
"""


# ---------------------------------------------------------------- cylinder volume
CYLINDER = """
<div class="tool" id="tt-cy">
  <div class="fields">
    <div class="field"><label for="cy-r">Radius</label><input type="number" id="cy-r" step="any" min="0" placeholder="5"></div>
    <div class="field"><label for="cy-h">Height</label><input type="number" id="cy-h" step="any" min="0" placeholder="10"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cy-out">-</span><span class="result-unit" id="cy-unit">cubic units</span></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cy-liters">-</span><span class="result-unit">liters (if cm)</span></div>
  <div class="tool-note">V = πr²h - enter radius (not diameter) and height in the same unit.</div>
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


# ---------------------------------------------------------------- morse code
MORSE = """
<div class="tool" id="tt-mo">
  <div class="field"><label for="mo-txt">Text</label>
    <textarea id="mo-txt" rows="3" placeholder="SOS"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="mo-code">Morse code (dots and dashes, / between words)</label>
    <textarea id="mo-code" rows="3" placeholder="... --- ..."></textarea></div>
  <div class="tool-note">International Morse: letters separated by spaces, words by /.</div>
</div>
<script>(function(){
var T={a:'.-',b:'-...',c:'-.-.',d:'-..',e:'.',f:'..-.',g:'--.',h:'....',i:'..',j:'.---',k:'-.-',l:'.-..',m:'--',n:'-.',o:'---',p:'.--.',q:'--.-',r:'.-.',s:'...',t:'-',u:'..-',v:'...-',w:'.--',x:'-..-',y:'-.--',z:'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--','/':'-..-.','(':'-.--.',')':'-.--.-','&':'.-...',':':'---...','=':'-...-','+':'.-.-.','"':'.-..-.','@':'.--.-.'};
var R={};Object.keys(T).forEach(function(k){R[T[k]]=k;});
var txt=document.getElementById('mo-txt'),code=document.getElementById('mo-code');
var lock=false;
function toMorse(s){
  return s.toLowerCase().split(/\s+/).map(function(word){
    return word.split('').map(function(ch){return T[ch]||null;}).filter(Boolean).join(' ');
  }).filter(Boolean).join(' / ');
}
function fromMorse(m){
  return m.trim().split(/\s*\/\s*/).map(function(word){
    return word.split(/\s+/).filter(Boolean).map(function(sym){return R[sym]||'?';}).join('');
  }).join(' ');
}
txt.addEventListener('input',function(){
  if(lock)return;lock=true;
  code.value=this.value.trim()?toMorse(this.value):'';
  lock=false;
});
code.addEventListener('input',function(){
  if(lock)return;lock=true;
  var v=this.value.trim();
  txt.value=v?fromMorse(v):'';
  lock=false;
});
txt.value='SOS';
txt.dispatchEvent(new Event('input'));
})();</script>
"""


# ---------------------------------------------------------------- epoch timestamp
EPOCH = """
<div class="tool" id="tt-ep">
  <div class="chips"><button class="chip active" id="ep-ms" type="button">Milliseconds (13 digits)</button></div>
  <div class="fields two">
    <div class="field"><label for="ep-ts">Timestamp</label><input type="number" id="ep-ts" step="any" placeholder="1767000000"></div>
    <div class="field"><label for="ep-date">Date & time (local)</label><input type="datetime-local" id="ep-date"></div>
  </div>
  <div class="result"><span class="result-num" id="ep-utc">-</span><span class="result-unit">UTC</span></div>
  <div class="stats">
    <div class="stat"><b id="ep-now">-</b><span>current timestamp</span></div>
    <div class="stat"><b id="ep-local">-</b><span>your local time</span></div>
  </div>
</div>
<script>(function(){
var ts=document.getElementById('ep-ts'),dt=document.getElementById('ep-date');
var ms=document.getElementById('ep-ms').classList.contains('active');
document.getElementById('ep-ms').addEventListener('click',function(){
  this.classList.toggle('active');
  ms=this.classList.contains('active');
  runTs();
});
function factor(){return ms?1000:1;}
function runTs(){
  var v=parseFloat(ts.value);
  if(isNaN(v)){return;}
  var d=new Date(v*factor());
  if(isNaN(d.getTime())){document.getElementById('ep-utc').textContent='out of range';return;}
  document.getElementById('ep-utc').textContent=d.toISOString().slice(0,19).replace('T',' ')+' UTC';
  document.getElementById('ep-local').textContent=d.toLocaleString('en-US');
}
function runDate(){
  if(!dt.value)return;
  var d=new Date(dt.value);
  var secs=Math.floor(d.getTime()/1000);
  ts.value=secs;
  document.getElementById('ep-utc').textContent=d.toISOString().slice(0,19).replace('T',' ')+' UTC';
  document.getElementById('ep-local').textContent=d.toLocaleString('en-US');
}
ts.addEventListener('input',runTs);
dt.addEventListener('input',runDate);
var now=document.getElementById('ep-now');
function tick(){now.textContent=Math.floor(Date.now()/(ms?1:1000)).toLocaleString('en-US');}
setInterval(tick,1000);tick();
})();</script>
"""


# ---------------------------------------------------------------- words to number
WORDSTONUM = """
<div class="tool" id="tt-w2n">
  <div class="field"><label for="w2n-in">Number in words</label>
    <textarea id="w2n-in" rows="3" placeholder="two thousand three hundred forty-two"></textarea></div>
  <div class="result"><span class="result-num" id="w2n-out">-</span></div>
  <div class="tool-note">Handles negatives, hyphens, the British "and", and scales up to trillion.</div>
</div>
<script>(function(){
var SMALL={zero:0,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,eleven:11,twelve:12,thirteen:13,fourteen:14,fifteen:15,sixteen:16,seventeen:17,eighteen:18,nineteen:19};
var TENS={twenty:20,thirty:30,forty:40,fourty:40,fifty:50,sixty:60,seventy:70,eighty:80,ninety:90};
var SCALES={hundred:100,thousand:1000,million:1000000,billion:1000000000,trillion:1000000000000};
var inp=document.getElementById('w2n-in'),out=document.getElementById('w2n-out');
function parse(s){
  s=s.toLowerCase().replace(/-/g,' ').replace(/\band\b/g,' ').replace(/,/g,' ').replace(/\s+/g,' ').trim();
  var neg=false;
  if(/^(minus|negative) /.test(s)){neg=true;s=s.replace(/^(minus|negative) /,'');}
  if(!s)return null;
  var total=0,current=0,ok=true;
  s.split(' ').forEach(function(w){
    if(w in SMALL){current+=SMALL[w];}
    else if(w in TENS){current+=TENS[w];}
    else if(w in SCALES){
      var sc=SCALES[w];
      if(sc===100){current=Math.max(current,1)*100;}
      else{total+=Math.max(current,1)*sc;current=0;}
    }
    else if(/^\d+$/.test(w)){current+=parseInt(w,10);}
    else{ok=false;}
  });
  if(!ok)return null;
  var v=total+current;
  return neg?-v:v;
}
inp.addEventListener('input',function(){
  var v=this.value.trim();
  if(!v){out.textContent='-';return;}
  var n=parse(v);
  out.textContent=(n===null)?'(could not parse - check the spelling)':n.toLocaleString('en-US');
});
})();</script>
"""


# ---------------------------------------------------------------- speed distance time
SDT = """
<div class="tool" id="tt-sdt">
  <div class="fields">
    <div class="field"><label for="sdt-d">Distance</label><input type="number" id="sdt-d" step="any" min="0" placeholder="120"></div>
    <div class="field"><label for="sdt-s">Speed (per hour)</label><input type="number" id="sdt-s" step="any" min="0" placeholder="80"></div>
    <div class="field"><label for="sdt-t">Time (h:mm:ss)</label><input type="text" id="sdt-t" placeholder="1:30:00"></div>
  </div>
  <div class="result"><span class="result-num" id="sdt-out">-</span><span class="result-unit" id="sdt-unit"></span></div>
  <div class="tool-note">Use consistent units - km with km/h, miles with mph. Fill any two fields and the third solves.</div>
</div>
<script>(function(){
var D=document.getElementById('sdt-d'),S=document.getElementById('sdt-s'),T=document.getElementById('sdt-t');
var lock=false;
function toSec(v){var p=v.split(':').map(Number);if(p.some(isNaN))return null;
  if(p.length===3)return p[0]*3600+p[1]*60+p[2];
  if(p.length===2)return p[0]*60+p[1];
  if(p.length===1)return p[0];return null;}
function fmtHMS(sec){var h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),s=Math.round(sec%60);
  return h+' h '+m+' min'+(s?' '+s+' sec':'');}
function hmsStr(sec){var h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),ss=Math.round(sec%60);
  return h+':'+String(m).padStart(2,'0')+':'+String(ss).padStart(2,'0');}
function run(){
  if(lock)return;lock=true;
  var d=parseFloat(D.value),s=parseFloat(S.value),tSec=T.value.trim()?toSec(T.value):null;
  if(d>0&&s>0){var sec=d/s*3600;
    T.value=hmsStr(sec);
    document.getElementById('sdt-out').textContent=fmtHMS(sec);
    document.getElementById('sdt-unit').textContent='total time';
    document.title=fmtHMS(sec)+' - ToolTide';
  } else if(d>0&&tSec>0){var sp=d/(tSec/3600);
    S.value=Math.round(sp*100)/100;
    document.getElementById('sdt-out').textContent=Math.round(sp*100)/100+' /hour';
    document.getElementById('sdt-unit').textContent='average speed';
    document.title=Math.round(sp*100)/100+'/hour - ToolTide';
  } else if(s>0&&tSec>0){var dist=s*(tSec/3600);
    D.value=Math.round(dist*100)/100;
    document.getElementById('sdt-out').textContent=Math.round(dist*100)/100;
    document.getElementById('sdt-unit').textContent='total distance';
    document.title=Math.round(dist*100)/100+' - ToolTide';
  }
  lock=false;
}
[D,S,T].forEach(function(el){el.addEventListener('input',function(){lock=false;run();});});
run();
})();</script>
"""


# ---------------------------------------------------------------- reverse text
REVERSER = """
<div class="tool" id="tt-rv">
  <div class="chips">
    <button class="chip active" data-m="chars">Reverse characters</button>
    <button class="chip" data-m="words">Reverse word order</button>
  </div>
  <div class="field"><label for="rv-in">Your text</label>
    <textarea id="rv-in" rows="4" placeholder="Type something to reverse..."></textarea></div>
  <div class="field" style="margin-top:10px"><label for="rv-out">Reversed <button class="btn btn-sm" id="rv-copy" type="button">Copy</button></label>
    <textarea id="rv-out" rows="4" readonly placeholder="result appears here..."></textarea></div>
</div>
<script>(function(){
var mode="chars";
var inp=document.getElementById('rv-in'),out=document.getElementById('rv-out');
document.querySelectorAll('#tt-rv .chip').forEach(function(c){c.addEventListener('click',function(){
  mode=c.dataset.m;
  document.querySelectorAll('#tt-rv .chip').forEach(function(x){x.classList.toggle('active',x===c);});
  run();
});});
function run(){
  var v=inp.value;
  out.value=mode==='chars'?v.split('').reverse().join(''):v.split(/\s+/).filter(Boolean).reverse().join(' ');
  document.title=(out.value||'Reverse Text')+' - ToolTide';
}
inp.addEventListener('input',run);
document.getElementById('rv-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('rv-copy');b.textContent='Copied!';setTimeout(function(){b.textContent='Copy';},1200);
});
run();
})();</script>
"""


# ---------------------------------------------------------------- weight on moon
MOONWEIGHT = """
<div class="tool" id="tt-mw">
  <div class="field"><label for="mw-in">Your weight on Earth</label>
    <input type="number" id="mw-in" step="any" min="0" value="70"></div>
  <table class="copytable"><thead><tr><th>Location</th><th>Gravity</th><th>You would weigh</th></tr></thead><tbody id="mw-tb"></tbody></table>
</div>
<script>(function(){
var P=[["Moon",0.165],["Mars",0.377],["Venus",0.905],["Earth",1],["Saturn",1.065],["Uranus",0.886],["Jupiter",2.528],["Neptune",1.137]];
var inp=document.getElementById('mw-in'),tb=document.getElementById('mw-tb');
function run(){
  var w=parseFloat(inp.value);
  if(isNaN(w)){tb.innerHTML='';return;}
  tb.innerHTML=P.map(function(p){
    var v=Math.round(w*p[1]*100)/100;
    return '<tr><td>'+p[0]+(p[0]==='Earth'?' (reference)':'')+'</td><td>x'+p[1]+'</td><td><b>'+v+'</b></td></tr>';
  }).join('');
  document.title='Moon weight: '+Math.round(w*0.165*10)/10+' - ToolTide';
}
inp.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- binary <-> decimal
BINDEC = """
<div class="tool" id="tt-bd">
  <div class="fields two">
    <div class="field"><label for="bd-bin">Binary (0s and 1s)</label>
      <input type="text" id="bd-bin" placeholder="1010" autocomplete="off"></div>
    <div class="field"><label for="bd-dec">Decimal</label>
      <input type="number" id="bd-dec" step="1" placeholder="10"></div>
  </div>
  <div class="result"><span class="result-num" id="bd-out">-</span><div class="result-formula" id="bd-note"></div></div>
  <table class="copytable"><thead><tr><th>Bit position</th><th>Value</th></tr></thead><tbody>
  <tr><td>bit 0 (rightmost)</td><td>1</td></tr><tr><td>bit 1</td><td>2</td></tr>
  <tr><td>bit 2</td><td>4</td></tr><tr><td>bit 3</td><td>8</td></tr>
  <tr><td>bit 7 (a byte)</td><td>128</td></tr></tbody></table>
</div>
<script>(function(){
var bin=document.getElementById('bd-bin'),dec=document.getElementById('bd-dec');
var out=document.getElementById('bd-out'),note=document.getElementById('bd-note');
var lock=false;
bin.addEventListener('input',function(){
  if(lock)return;lock=true;dec.value='';
  var v=this.value.trim();
  if(!v){out.textContent='-';note.textContent='';lock=false;return;}
  if(!/^[01]+$/.test(v)){out.textContent='-';note.textContent='Only 0s and 1s are valid in binary.';lock=false;return;}
  var d=BigInt('0b'+v);
  dec.value=d.toString();
  out.textContent=d.toLocaleString('en-US');
  note.textContent=v+' binary = '+d.toLocaleString('en-US')+' decimal';
  lock=false;
});
dec.addEventListener('input',function(){
  if(lock)return;lock=true;bin.value='';
  var v=this.value.trim();
  if(!v||isNaN(Number(v))){out.textContent='-';note.textContent='';lock=false;return;}
  try{
    var b=BigInt(v).toString(2);
    bin.value=b;
    out.textContent=b;
    note.textContent=v+' decimal = '+b+' binary';
  }catch(e){out.textContent='-';note.textContent='Number too large.';}
  lock=false;
});
})();</script>
"""


# ---------------------------------------------------------------- kelvin converter
KELVIN = """
<div class="tool" id="tt-kel">
  <div class="fields">
    <div class="field"><label for="kel-k">Kelvin (K)</label><input type="number" id="kel-k" step="any" placeholder="300"></div>
    <div class="field"><label for="kel-c">Celsius (C)</label><input type="number" id="kel-c" step="any" placeholder="26.85"></div>
    <div class="field"><label for="kel-f">Fahrenheit (F)</label><input type="number" id="kel-f" step="any" placeholder="80.33"></div>
  </div>
  <div class="result"><span class="result-num" id="kel-out">-</span><div class="result-formula" id="kel-note"></div></div>
</div>
<script>(function(){
var K=document.getElementById('kel-k'),C=document.getElementById('kel-c'),F=document.getElementById('kel-f');
var out=document.getElementById('kel-out'),note=document.getElementById('kel-note');
var lock=false;
function r(v){return Math.round(v*100)/100;}
function set(k,c,f,noteTxt){
  K.value=k===null?'':r(k);C.value=c===null?'':r(c);F.value=f===null?'':r(f);
  out.textContent=(k===null?'-':r(k)+' K')+'  =  '+(c===null?'-':r(c)+' C')+'  =  '+(f===null?'-':r(f)+' F');
  note.textContent=noteTxt||'';
  document.title=r(c)+' C - ToolTide';
}
function fromK(k){
  if(isNaN(k)){set(null,null,null,'');return;}
  if(k<0){set(k,k*1-273.15,null,'Below absolute zero - physically impossible.');return;}
  var c=k-273.15,f=c*9/5+32;
  set(k,c,f,'K - 273.15 = C; C x 9/5 + 32 = F');
}
function fromC(c){
  if(isNaN(c)){set(null,null,null,'');return;}
  fromK(c+273.15);
}
function fromF(f){
  if(isNaN(f)){set(null,null,null,'');return;}
  fromK((f-32)*5/9+273.15);
}
K.addEventListener('input',function(){fromK(parseFloat(K.value));});
C.addEventListener('input',function(){fromC(parseFloat(C.value));});
F.addEventListener('input',function(){fromF(parseFloat(F.value));});
fromK(300);
})();</script>
"""

# Double (stacked) discount deal judge: true combined rate vs a flat alternative discount.
# Retention hooks: title result hook, tt_doubledisc input memory, URL state (?p=&d1=&d2=&flat=), Web Share.
DOUBLEDISC = """<div class="tool" id="tt-ddisc">
  <div class="fields">
    <div class="field"><label for="dd-price">Original price ($)</label><input type="number" id="dd-price" step="0.01" min="0" placeholder="200"></div>
    <div class="field"><label for="dd-d1">First discount %</label><input type="number" id="dd-d1" step="any" min="0" max="100" placeholder="30"></div>
    <div class="field"><label for="dd-d2">Second discount %</label><input type="number" id="dd-d2" step="any" min="0" max="100" placeholder="20"></div>
    <div class="field"><label for="dd-flat">Flat alternative % (optional)</label><input type="number" id="dd-flat" step="any" min="0" max="100" placeholder="45"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dd-out">–</span><span class="result-unit" id="dd-unit">stacked final price</span></div>
  <div class="tool-note" id="dd-note"></div>
  <div class="stats">
    <div class="stat"><b id="dd-true">–</b><span>true combined %</span></div>
    <div class="stat"><b id="dd-save">–</b><span>you save</span></div>
    <div class="stat"><b id="dd-verdict">–</b><span>vs flat deal</span></div>
  </div>
  <button type="button" class="tool-btn" id="dd-share">Share this deal math</button>
</div>
<script>(function(){
var E={};['dd-price','dd-d1','dd-d2','dd-flat'].forEach(function(id){E[id]=document.getElementById(id);});
var OUT=document.getElementById('dd-out'),NOTE=document.getElementById('dd-note');
function money(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function num(id){var v=E[id].value;return v===''?null:(parseFloat(v)||0);}
function calc(){
  var p=num('dd-price'),d1=num('dd-d1')||0,d2=num('dd-d2')||0,flat=num('dd-flat');
  if(!p){OUT.textContent='–';NOTE.textContent='';document.getElementById('dd-true').textContent='–';
    document.getElementById('dd-save').textContent='–';document.getElementById('dd-verdict').textContent='–';
    document.title='Double Discount Calculator - ToolTide';return;}
  var eff=(1-d1/100)*(1-d2/100),fin=p*eff,truePct=(1-eff)*100;
  OUT.textContent=money(fin);
  document.getElementById('dd-true').textContent=truePct.toFixed(2)+'%';
  document.getElementById('dd-save').textContent=money(p-fin);
  var note='Applied in order: '+money(p)+' → ×'+(1-d1/100).toFixed(4)+' → '+money(p*(1-d1/100))+' → ×'+(1-d2/100).toFixed(4)+' → '+money(fin)+
    '. Not '+(d1+d2)+'% off — the second discount applies to the already-reduced price.';
  var vd='—';
  if(flat!==null){var ffin=p*(1-flat/100),diff=ffin-fin;
    vd=diff>0.005?('stacked wins by '+money(diff)):diff<-0.005?('flat wins by '+money(-diff)):'identical';
    note+=' Stacked final '+money(fin)+' vs flat '+flat+'% at '+money(ffin)+': '+vd+'.';
  }
  NOTE.textContent=note;
  document.getElementById('dd-verdict').textContent=vd;
  document.title=truePct.toFixed(0)+'% true discount - ToolTide';
}
function save(){try{localStorage.setItem('tt_doubledisc',JSON.stringify({p:E['dd-price'].value,d1:E['dd-d1'].value,d2:E['dd-d2'].value,f:E['dd-flat'].value}));}catch(e){}}
Object.keys(E).forEach(function(k){E[k].addEventListener('input',function(){calc();save();});});
var pre=false;
[['p','dd-price'],['d1','dd-d1'],['d2','dd-d2'],['flat','dd-flat']].forEach(function(a){
  var v=qs(a[0]);if(v!==null){E[a[1]].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_doubledisc')||'null');if(mem){E['dd-price'].value=mem.p||'';E['dd-d1'].value=mem.d1||'';E['dd-d2'].value=mem.d2||'';E['dd-flat'].value=mem.f||'';}}catch(e){}}
calc();
document.getElementById('dd-share').addEventListener('click',function(){
  var txt=E['dd-d1'].value+'% + '+E['dd-d2'].value+'% off is really '+document.getElementById('dd-true').textContent+
    ' off - final '+OUT.textContent+'. Check any deal (no sign-up):';
  var url=location.origin+location.pathname+'?p='+encodeURIComponent(E['dd-price'].value||'')+'&d1='+encodeURIComponent(E['dd-d1'].value||'')+'&d2='+encodeURIComponent(E['dd-d2'].value||'')+'&flat='+encodeURIComponent(E['dd-flat'].value||'');
  if(navigator.share){navigator.share({title:'Stacked discount math',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share this deal math';},1500);}
});
})();
</script>
"""

# Simple interest: SI = P x r x t, with a live "what compound would give" comparison.
# Retention hooks: title result hook, tt_simpleint input memory, URL state (?p=&r=&t=), Web Share.
SIMPLEINT = """<div class="tool" id="tt-si">
  <div class="fields">
    <div class="field"><label for="si-p">Principal ($)</label><input type="number" id="si-p" step="any" min="0" placeholder="5000"></div>
    <div class="field"><label for="si-r">Annual rate %</label><input type="number" id="si-r" step="any" min="0" placeholder="6"></div>
    <div class="field"><label for="si-t">Time (years)</label><input type="number" id="si-t" step="any" min="0" placeholder="3"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="si-out">–</span><span class="result-unit" id="si-unit">total at maturity</span></div>
  <div class="stats">
    <div class="stat"><b id="si-int">–</b><span>interest earned</span></div>
    <div class="stat"><b id="si-permo">–</b><span>per month</span></div>
    <div class="stat"><b id="si-cmp">–</b><span>if compounded monthly</span></div>
  </div>
  <div class="tool-note" id="si-note"></div>
  <button type="button" class="tool-btn" id="si-share">Share this result</button>
</div>
<script>(function(){
var P=document.getElementById('si-p'),R=document.getElementById('si-r'),T=document.getElementById('si-t');
var OUT=document.getElementById('si-out');
function money(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parseFloat(P.value)||0,r=(parseFloat(R.value)||0)/100,t=parseFloat(T.value)||0;
  if(!p||!t){OUT.textContent='–';document.getElementById('si-int').textContent='–';
    document.getElementById('si-permo').textContent='–';document.getElementById('si-cmp').textContent='–';
    document.getElementById('si-note').textContent='';document.title='Simple Interest Calculator - ToolTide';return;}
  var si=p*r*t,total=p+si,rm=r/12,n=Math.round(t*12);
  var cmp=total;
  if(rm>0&&n>0){var bal=p;for(var k=0;k<n;k++){bal=bal*(1+rm);}cmp=bal;}
  OUT.textContent=money(total);
  document.getElementById('si-int').textContent=money(si);
  document.getElementById('si-permo').textContent=money(si/Math.max(t*12,1));
  document.getElementById('si-cmp').textContent=money(cmp);
  document.getElementById('si-note').textContent='SI = P × r × t = '+p.toLocaleString('en-US')+' × '+(r*100).toFixed(2).replace('.00','')+'% × '+t+' = '+money(si)+
    '. Simple interest is flat on the original principal - compounding the same rate would add '+money(cmp-total)+' more over '+t+' years.';
  document.title=money(si)+' interest - ToolTide';
}
function save(){try{localStorage.setItem('tt_simpleint',JSON.stringify({p:P.value,r:R.value,t:T.value}));}catch(e){}}
[P,R,T].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['p',P],['r',R],['t',T]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_simpleint')||'null');if(mem){P.value=mem.p||'';R.value=mem.r||'';T.value=mem.t||'';}}catch(e){}}
calc();
document.getElementById('si-share').addEventListener('click',function(){
  var txt='Simple interest on '+money(parseFloat(P.value)||0)+' at '+(parseFloat(R.value)||0)+'% for '+(parseFloat(T.value)||0)+
    ' years = '+OUT.textContent+'. Run your own (no sign-up):';
  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value||'')+'&r='+encodeURIComponent(R.value||'')+'&t='+encodeURIComponent(T.value||'');
  if(navigator.share){navigator.share({title:'Simple interest result',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share this result';},1500);}
});
})();
</script>
"""

# GPA calculator: credit-weighted 4.0 scale across 7 course rows plus prior cumulative.
# Retention hooks: title result hook, tt_gpa input memory, URL state (?g=&c=&p=&pc=), Web Share.
GPACALC = """<div class="tool" id="tt-gpa">
  <div id="gpa-rows"></div>
  <div class="fields">
    <div class="field"><label for="gpa-pg">Prior cumulative GPA (optional)</label><input type="number" id="gpa-pg" step="any" min="0" max="4" placeholder="3.48"></div>
    <div class="field"><label for="gpa-pc">Prior graded credits (optional)</label><input type="number" id="gpa-pc" step="any" min="0" placeholder="60"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gpa-out">–</span><span class="result-unit" id="gpa-unit">GPA (4.0 scale)</span></div>
  <div class="stats">
    <div class="stat"><b id="gpa-sem">–</b><span>this semester alone</span></div>
    <div class="stat"><b id="gpa-cr">–</b><span>graded credits</span></div>
  </div>
  <div class="tool-note">Weighted by credit hours: A=4.0, A−=3.7, B+=3.3, B=3.0, B−=2.7, C+=2.3, C=2.0, C−=1.7, D+=1.3, D=1.0, F=0. Leave a row blank to exclude it.</div>
  <button type="button" class="tool-btn" id="gpa-share">Share my GPA</button>
</div>
<script>(function(){
var GR=[['A',4],['A-',3.7],['B+',3.3],['B',3],['B-',2.7],['C+',2.3],['C',2],['C-',1.7],['D+',1.3],['D',1],['F',0]];
var ROWS=7,box=document.getElementById('gpa-rows');
for(var i=0;i<ROWS;i++){
  var d=document.createElement('div');d.className='fields';
  d.innerHTML='<div class="field"><label>Course '+(i+1)+' (name optional)</label><input type="text" class="gpa-n" placeholder="Calculus II"></div>'+
    '<div class="field"><label>Credits</label><input type="number" class="gpa-c" step="any" min="0" placeholder="4"></div>'+
    '<div class="field"><label>Grade</label><select class="gpa-g"><option value=""></option>'+
    GR.map(function(g){return '<option value="'+g[1]+'">'+g[0]+'</option>';}).join('')+'</select></div>';
  box.appendChild(d);
}
function parts(){return [box.querySelectorAll('.gpa-n'),box.querySelectorAll('.gpa-c'),box.querySelectorAll('.gpa-g')];}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parts(),pts=0,cr=0;
  for(var i=0;i<ROWS;i++){
    var c=parseFloat(p[1][i].value)||0,g=p[2][i].value===''?null:parseFloat(p[2][i].value);
    if(c>0&&g!==null){pts+=c*g;cr+=c;}
  }
  var sem=cr>0?pts/cr:null,pg=parseFloat(document.getElementById('gpa-pg').value),pc=parseFloat(document.getElementById('gpa-pc').value);
  var out=sem,tot=cr,unit='GPA (4.0 scale)';
  if(sem!==null&&pc>0&&!isNaN(pg)){out=(pts+pg*pc)/(cr+pc);tot=cr+pc;unit='cumulative GPA';}
  document.getElementById('gpa-out').textContent=out===null?'–':out.toFixed(2);
  document.getElementById('gpa-unit').textContent=unit;
  document.getElementById('gpa-sem').textContent=sem===null?'–':sem.toFixed(2);
  document.getElementById('gpa-cr').textContent=tot;
  document.title=(out===null?'GPA Calculator':(unit==='cumulative GPA'?'Cumulative GPA ':'GPA ')+out.toFixed(2))+' - ToolTide';
}
function save(){var p=parts(),o={n:[],c:[],g:[],pg:document.getElementById('gpa-pg').value,pc:document.getElementById('gpa-pc').value};
  for(var i=0;i<ROWS;i++){o.n.push(p[0][i].value);o.c.push(p[1][i].value);o.g.push(p[2][i].value);}
  try{localStorage.setItem('tt_gpa',JSON.stringify(o));}catch(e){}}
function fill(o){var p=parts();
  for(var i=0;i<ROWS;i++){p[0][i].value=(o.n&&o.n[i])||'';p[1][i].value=(o.c&&o.c[i])||'';p[2][i].value=(o.g&&o.g[i])||'';}
  document.getElementById('gpa-pg').value=o.pg||'';document.getElementById('gpa-pc').value=o.pc||'';calc();}
box.addEventListener('input',function(){calc();save();});
box.addEventListener('change',function(){calc();save();});
['gpa-pg','gpa-pc'].forEach(function(id){document.getElementById(id).addEventListener('input',function(){calc();save();});});
var pre=false,gv=qs('g'),cv=qs('c');
if(gv&&cv){var o={g:gv.split(','),c:cv.split(','),pg:qs('p')||'',pc:qs('pc')||'',n:[]};fill(o);pre=true;}
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_gpa')||'null');if(mem){fill(mem);}}catch(e){}}
calc();
document.getElementById('gpa-share').addEventListener('click',function(){
  var v=document.getElementById('gpa-out').textContent;
  var txt='My '+(document.getElementById('gpa-unit').textContent==='cumulative GPA'?'cumulative ':'')+'GPA: '+v+' on the 4.0 scale. Calculate yours (no sign-up):';
  var url=location.origin+location.pathname;
  if(navigator.share){navigator.share({title:'GPA result',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share my GPA';},1500);}
});
})();
</script>
"""

# Sleep cycle planner: 90-minute cycles + 15-min fall-asleep latency, both directions.
# Retention hooks: title result hook, tt_sleep input memory, URL state (?mode=&t=), Web Share.
SLEEP = """<div class="tool" id="tt-sleep">
  <div class="fields">
    <div class="field"><label for="sl-mode">Plan</label>
      <select id="sl-mode"><option value="wake">Wake-up times if I sleep now</option><option value="bed">Bedtime for a target wake-up</option></select></div>
    <div class="field" id="sl-t-wrap" style="display:none"><label for="sl-t">I need to wake up at</label><input type="time" id="sl-t" value="07:00"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sl-out">–</span><span class="result-unit" id="sl-unit"></span></div>
  <div id="sl-list"></div>
  <div class="tool-note">Cycles average 90 minutes and most people take about 15 minutes to fall asleep. Waking between cycles feels far easier than mid-cycle — 5-6 cycles (7.5-9 h in bed) suits most adults, 3 cycles (4.5 h) is the short-night floor.</div>
  <button type="button" class="tool-btn" id="sl-share">Share these times</button>
</div>
<script>(function(){
var MODE=document.getElementById('sl-mode'),T=document.getElementById('sl-t'),TW=document.getElementById('sl-t-wrap');
var OUT=document.getElementById('sl-out'),UNIT=document.getElementById('sl-unit'),LIST=document.getElementById('sl-list');
function fmt(mins){mins=((mins%1440)+1440)%1440;var h=Math.floor(mins/60),m=mins%60,ap=h<12?'AM':'PM',h12=h%12;if(h12===0)h12=12;return h12+':'+(m<10?'0':'')+m+' '+ap;}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var mode=MODE.value,base,rows=[];
  if(mode==='wake'){var n=new Date();base=n.getHours()*60+n.getMinutes()+15;
    for(var k=6;k>=3;k--){rows.push([k,base+90*k]);}
    OUT.textContent=fmt(rows[0][1]);UNIT.textContent='best wake-up (6 cycles ≈ 9 h in bed)';
  }else{
    var v=T.value;if(!v){OUT.textContent='–';UNIT.textContent='';LIST.innerHTML='';document.title='Sleep Cycle Calculator - ToolTide';return;}
    var p=v.split(':');base=parseInt(p[0],10)*60+parseInt(p[1],10)-15;
    for(var j=6;j>=3;j--){rows.push([j,base-90*j]);}
    OUT.textContent=fmt(rows[0][1]);UNIT.textContent='bedtime for a '+v+' wake-up (6 cycles)';
  }
  var h='<div class="stats">';
  rows.forEach(function(r){h+='<div class="stat"><b>'+fmt(r[1])+'</b><span>'+r[0]+' cycles · '+(r[0]*1.5).toFixed(1).replace('.0','')+' h sleep</span></div>';});
  LIST.innerHTML=h+'</div>';
  document.title=(mode==='wake'?'Sleep now, wake ':'Bedtime ')+(mode==='wake'?fmt(rows[0][1]):T.value)+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_sleep',JSON.stringify({m:MODE.value,t:T.value}));}catch(e){}}
MODE.addEventListener('change',function(){TW.style.display=MODE.value==='bed'?'':'none';calc();save();});
T.addEventListener('input',function(){calc();save();});
var mt=qs('mode'),tv=qs('t');
if(mt){MODE.value=(mt==='bed')?'bed':'wake';TW.style.display=MODE.value==='bed'?'':'none';}
if(tv){T.value=tv;}
else{try{var mem=JSON.parse(localStorage.getItem('tt_sleep')||'null');if(mem){MODE.value=mem.m||'wake';TW.style.display=MODE.value==='bed'?'':'none';if(mem.t)T.value=mem.t;}}catch(e){}}
calc();
document.getElementById('sl-share').addEventListener('click',function(){
  var txt=MODE.value==='wake'?('Sleeping now? Best wake-up: '+OUT.textContent+' — plan your night (no sign-up):')
    :('Set bedtime '+OUT.textContent+' to wake at '+T.value+' between cycles. Plan sleep (no sign-up):');
  var url=location.origin+location.pathname+'?mode='+MODE.value+(MODE.value==='bed'?'&t='+encodeURIComponent(T.value):'');
  if(navigator.share){navigator.share({title:'Sleep cycle plan',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share these times';},1500);}
});
})();
</script>
"""
# Retention hooks: title result hook, tt_savings input memory, URL state (?goal=&saved=&dep=&apy=), Web Share.
SAVINGS = """<div class="tool" id="tt-savings">
  <div class="fields">
    <div class="field"><label for="sav-goal">Savings goal ($)</label><input type="number" id="sav-goal" min="1" step="any" placeholder="10000"></div>
    <div class="field"><label for="sav-saved">Already saved ($)</label><input type="number" id="sav-saved" min="0" step="any" placeholder="1200"></div>
    <div class="field"><label for="sav-dep">Monthly deposit ($)</label><input type="number" id="sav-dep" min="0" step="any" placeholder="500"></div>
    <div class="field"><label for="sav-apy">Interest rate APY % (optional)</label><input type="number" id="sav-apy" min="0" step="any" placeholder="4.0"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sav-out">-</span><span class="result-unit" id="sav-unit"></span></div>
  <div class="sav-bar" aria-hidden="true"><div id="sav-fill"></div></div>
  <div class="tool-note" id="sav-detail"></div>
  <button type="button" class="tool-btn" id="sav-share">Share my plan</button>
</div>
<style>.sav-bar{height:10px;border-radius:5px;background:rgba(127,127,127,.18);overflow:hidden;margin:10px 0 4px}.sav-bar>div{height:100%;width:0;border-radius:5px;background:var(--ink,#0891b2);transition:width .3s}</style>
<script>
(function(){
var G=document.getElementById('sav-goal'),S=document.getElementById('sav-saved'),D=document.getElementById('sav-dep'),R=document.getElementById('sav-apy');
var OUT=document.getElementById('sav-out'),UNIT=document.getElementById('sav-unit'),DET=document.getElementById('sav-detail'),FILL=document.getElementById('sav-fill');
var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function money(v){return '$'+Math.round(v).toLocaleString('en-US');}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var g=parseFloat(G.value),s=parseFloat(S.value)||0,d=parseFloat(D.value)||0,apy=parseFloat(R.value)||0;
  if(isNaN(g)||g<=0){OUT.textContent='-';UNIT.textContent='';DET.textContent='';FILL.style.width='0';document.title='Savings Goal Calculator - ToolTide';return;}
  FILL.style.width=Math.min(100,s/g*100)+'%';
  if(s>=g){OUT.textContent='🎉';UNIT.textContent='goal reached';DET.textContent='You are at '+money(s)+' of '+money(g)+' - any deposit now is extra cushion.';document.title='Savings goal reached - ToolTide';return;}
  var bal=s,rm=apy/100/12,m=0,dep=s;
  while(bal<g&&m<1200){bal=bal*(1+rm)+d;dep+=d;m++;}
  if(bal<g){OUT.textContent='100+';UNIT.textContent='years - increase deposit';DET.textContent='At this pace the goal is effectively out of reach. Even a small monthly deposit changes the date dramatically.';document.title='Savings goal - ToolTide';return;}
  var now=new Date(),end=new Date(now.getFullYear(),now.getMonth()+m,now.getDate());
  OUT.textContent=MON[end.getMonth()]+' '+end.getFullYear();UNIT.textContent='goal reached';
  var interest=bal-dep;
  DET.textContent=m+' months · '+money(dep-s)+' deposited'+(interest>=1?' · '+money(interest)+' interest earned':'');
  document.title=m+' months to goal - ToolTide';
}
function save(){try{localStorage.setItem('tt_savings',JSON.stringify({g:G.value,s:S.value,d:D.value,r:R.value}));}catch(e){}}
[G,S,D,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['goal',G],['saved',S],['dep',D],['apy',R]].forEach(function(p){
  var v=qs(p[0]);if(v!==null){p[1].value=v;pre=true;}
});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_savings')||'null');if(mem){G.value=mem.g||'';S.value=mem.s||'';D.value=mem.d||'';R.value=mem.r||'';}}catch(e){}}
calc();
var SB=document.getElementById('sav-share');
SB.addEventListener('click',function(){
  var txt='I plan to hit my '+money(parseFloat(G.value)||0)+' savings goal by '+OUT.textContent+'. Plan yours (no sign-up):';
  var url=location.origin+location.pathname+
    '?goal='+encodeURIComponent(G.value||'')+'&saved='+encodeURIComponent(S.value||'')+'&dep='+encodeURIComponent(D.value||'')+'&apy='+encodeURIComponent(R.value||'');
  if(navigator.share){navigator.share({title:'Savings goal plan',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);SB.textContent='Copied!';setTimeout(function(){SB.textContent='Share my plan';},1500);}
});
})();
</script>
"""

# Compound interest: starting amount + optional monthly contributions -> future value with a yearly table.
# Retention hooks: title result hook, tt_compound input memory, URL state (?p=&m=&r=&y=), Web Share.
COMPOUND = """<div class="tool" id="tt-compound">
  <div class="fields">
    <div class="field"><label for="cp-p">Starting amount ($)</label><input type="number" id="cp-p" min="0" step="any" placeholder="5000"></div>
    <div class="field"><label for="cp-m">Monthly contribution ($, optional)</label><input type="number" id="cp-m" min="0" step="any" placeholder="200"></div>
    <div class="field"><label for="cp-r">Annual rate %</label><input type="number" id="cp-r" min="0" step="any" placeholder="7"></div>
    <div class="field"><label for="cp-y">Years</label><input type="number" id="cp-y" min="1" max="50" step="1" placeholder="10"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cp-out">-</span><span class="result-unit" id="cp-unit"></span></div>
  <div class="tool-note" id="cp-detail"></div>
  <div id="cp-table"></div>
  <button type="button" class="tool-btn" id="cp-share">Share this projection</button>
</div>
<script>
(function(){
var P=document.getElementById('cp-p'),M=document.getElementById('cp-m'),R=document.getElementById('cp-r'),Y=document.getElementById('cp-y');
var OUT=document.getElementById('cp-out'),UNIT=document.getElementById('cp-unit'),DET=document.getElementById('cp-detail'),TB=document.getElementById('cp-table');
function money(v){return '$'+Math.round(v).toLocaleString('en-US');}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parseFloat(P.value)||0,m=parseFloat(M.value)||0,r=(parseFloat(R.value)||0)/100,y=parseFloat(Y.value);
  if(!y||y<1||(p<=0&&m<=0)){OUT.textContent='-';UNIT.textContent='';DET.textContent='';TB.innerHTML='';document.title='Compound Interest Calculator - ToolTide';return;}
  var bal=p,dep=p,rows=[];
  for(var t=1;t<=Math.min(Math.round(y),50);t++){
    for(var k=0;k<12;k++){bal=bal*(1+r/12)+m;dep+=m;}
    rows.push([t,bal,bal-dep]);
  }
  var interest=bal-dep;
  OUT.textContent=money(bal);UNIT.textContent='future value';
  DET.textContent='after '+Math.round(y)+' years · '+money(dep)+' deposited · '+money(interest)+' interest earned · '+
    'rule of 72: at '+(r*100).toFixed(1).replace('.0','')+'% money doubles in about '+Math.round(72/Math.max(r*100,0.1))+' years.';
  var h='<table class="cp-t"><thead><tr><th>Year</th><th>Balance</th><th>Interest so far</th></tr></thead><tbody>';
  rows.forEach(function(row){h+='<tr><td>'+row[0]+'</td><td>'+money(row[1])+'</td><td>'+money(row[2])+'</td></tr>';});
  TB.innerHTML=h+'</tbody></table>';
  document.title=money(bal)+' in '+Math.round(y)+' years - ToolTide';
}
function save(){try{localStorage.setItem('tt_compound',JSON.stringify({p:P.value,m:M.value,r:R.value,y:Y.value}));}catch(e){}}
[P,M,R,Y].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['p',P],['m',M],['r',R],['y',Y]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_compound')||'null');if(mem){P.value=mem.p||'';M.value=mem.m||'';R.value=mem.r||'';Y.value=mem.y||'';}}catch(e){}}
calc();
var SB=document.getElementById('cp-share');
SB.addEventListener('click',function(){
  var txt='Compound interest projection: '+OUT.textContent+' after '+Math.round(parseFloat(Y.value)||0)+' years. Run your own numbers (no sign-up):';
  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value||'')+'&m='+encodeURIComponent(M.value||'')+'&r='+encodeURIComponent(R.value||'')+'&y='+encodeURIComponent(Y.value||'');
  if(navigator.share){navigator.share({title:'Compound interest projection',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);SB.textContent='Copied!';setTimeout(function(){SB.textContent='Share this projection';},1500);}
});
})();
</script>
<style>.cp-t{width:100%;border-collapse:collapse;margin-top:10px;font-size:.92em}.cp-t th,.cp-t td{padding:4px 8px;text-align:right;border-bottom:1px solid rgba(127,127,127,.25)}.cp-t th:first-child,.cp-t td:first-child{text-align:left}</style>
"""


TOOLS = {
    "countdown": lambda args: COUNTDOWN.replace("__ARGS__", _args(args)),
    "datediff": lambda args: DATEDIFF,
    "age": lambda args: AGE,
    "percent": lambda args: PERCENT.replace("__ARGS__", json.dumps(args or {})),
    "tip": lambda args: TIP,
    "discount": lambda args: DISCOUNT,
    "readingtime": lambda args: READINGTIME,
    "wordcounter": lambda args: WORDCOUNTER,
    "case": lambda args: CASE,
    "aspect": lambda args: ASPECT,
    "unitconv": lambda args: UNITCONV.replace("__ARGS__", _args(args)),
    "typing": lambda args: TYPING,
    "names": lambda args: NAMES,
    "password": lambda args: PASSWORD,
    "wordspages": lambda args: WORDSPAGES,
    "randomnum": lambda args: RANDOMNUM,
    "roman": lambda args: ROMAN,
    "grade": lambda args: GRADE,
    "dedupe": lambda args: DEDUPE,
    "slug": lambda args: SLUG,
    "upside": lambda args: UPSIDE,
    "hoursdiff": lambda args: HOURSDIFF,
    "inchfrac": lambda args: INCHFRAC,
    "average": lambda args: AVERAGE,
    "binary": lambda args: BINARY,
    "gramscups": lambda args: GRAMSCUPS,
    "dayofweek": lambda args: DAYOFWEEK,
    "fuel": lambda args: FUEL,
    "salary": lambda args: SALARY,
    "coinflip": lambda args: COINFLIP,
    "dice": lambda args: DICE,
    "half": lambda args: HALF,
    "letter": lambda args: LETTER,
    "cubicft": lambda args: CUBICFT,
    "sorter": lambda args: SORTER,
    "unitprice": lambda args: UNITPRICE,
    "wordfreq": lambda args: WORDFREQ,
    "degrad": lambda args: DEGRAD,
    "romantable": _render_romantable,
    "yesno": lambda args: YESNO,
    "hexrgb": lambda args: HEXRGB,
    "numwords": lambda args: NUMWORDS,
    "wordstonum": lambda args: WORDSTONUM,
    "sdt": lambda args: SDT,
    "reverser": lambda args: REVERSER,
    "moonweight": lambda args: MOONWEIGHT,
    "kelvin": lambda args: KELVIN,
    "bindec": lambda args: BINDEC,
    "cylinder": lambda args: CYLINDER,
    "planets": lambda args: PLANETS,
    "combiner": lambda args: COMBINER,
    "savings": lambda args: SAVINGS,
    "compound": lambda args: COMPOUND,
    "whitespace": lambda args: WHITESPACE,
    "binhex": lambda args: BINHEX,
    "prime": lambda args: PRIME,
    "factorial": lambda args: FACTORIAL,
    "country": lambda args: COUNTRY,
    "stlb": lambda args: STLB,
    "morse": lambda args: MORSE,
    "epoch": lambda args: EPOCH,
    "ftincm": lambda args: FTINCM,
    "emoji": lambda args: EMOJI,
    "sqft": lambda args: SQFT,
    "secondsconv": lambda args: SECONDS,
    "pxin": lambda args: PXIN,
    "striphtml": lambda args: STRIPHTML,
    "salestax": lambda args: SALESTAX,
    "doubledisc": lambda args: DOUBLEDISC,
    "simpleint": lambda args: SIMPLEINT,
    "gpa": lambda args: GPACALC,
    "sleepcycle": lambda args: SLEEP,
}


def render(tool, args):
    return TOOLS[tool](args)
