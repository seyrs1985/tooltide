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
var mode=0;
var chips=document.querySelectorAll('#tt-pc .chip');
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


TOOLS = {
    "countdown": lambda args: COUNTDOWN.replace("__ARGS__", _args(args)),
    "datediff": lambda args: DATEDIFF,
    "age": lambda args: AGE,
    "percent": lambda args: PERCENT,
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
    "randomnum": lambda args: RANDOMNUM,
}


def render(tool, args):
    return TOOLS[tool](args)
