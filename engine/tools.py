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
function candidate(y){
  if(rule){ if(rule.easter)return easterSunday(y); return nthWeekday(y,m-1,rule.week,rule.weekday); }
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
  <div class="result"><span class="result-num" id="dd-days">–</span><span class="result-unit">days</span>
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
})();</script>
"""


# ---------------------------------------------------------------- age
AGE = """
<div class="tool" id="tt-age">
  <div class="fields">
    <div class="field"><label for="age-b">Date of birth</label><input type="date" id="age-b"></div>
    <div class="field"><label for="age-a">Age at date</label><input type="date" id="age-a"></div>
  </div>
  <div class="result"><span class="result-num" id="age-main">–</span>
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
  <div class="result"><span class="result-num" id="dc-final">–</span><span class="result-unit">final price</span>
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
  <div class="result"><span class="result-num" id="ar-out">–</span><span class="result-unit" id="ar-out-unit"></span>
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
  <div class="result"><span class="result-num" id="uc-r">–</span>
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
  <div class="result" id="rng-out" style="display:none"><span class="result-num" id="rng-res"></span></div>
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
  <div class="result"><span class="result-num" id="wp-out">–</span><span class="result-unit">pages</span>
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
  <div class="result"><span class="result-num" id="rn-out">–</span><div class="result-formula" id="rn-note"></div></div>
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
  <div class="result"><span class="result-num" id="gr-pct">–</span><span class="result-unit" id="gr-letter"></span>
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
  <div class="result"><span class="result-num" id="gr-need">–</span><span class="result-unit" id="gr-need-txt">needed on the final</span></div>
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
  <div class="result"><span class="result-num" id="sl-out" style="word-break:break-all">–</span>
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
  <div class="result"><span class="result-num" id="stx-out">–</span><span class="result-unit" id="stx-unit"></span>
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
  <div class="result"><span class="result-num" id="hd-hm">–</span>
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
  <div class="result"><span class="result-num" id="avg-mean">–</span><span class="result-unit">average</span>
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
  <div class="result"><span class="result-num" id="gc-frac">–</span><span class="result-unit" id="gc-fr2"></span>
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
  <div class="result"><span class="result-num" id="dw-out">-</span>
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
  <div class="result"><span class="result-num" id="fu-out">–</span><span class="result-unit" id="fu-unit"></span>
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
    "striphtml": lambda args: STRIPHTML,
    "salestax": lambda args: SALESTAX,
}


def render(tool, args):
    return TOOLS[tool](args)
