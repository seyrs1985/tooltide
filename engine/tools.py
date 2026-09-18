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
  <div class="cd-big-label" id="cd-days-label" data-i18n="cd.days">days to go</div>
  <div class="cd-clock" id="cd-clock">–</div>
  <div class="stats">
    <div class="stat"><b id="cd-weeks">–</b><span data-i18n="cd.weeks">weeks</span></div>
    <div class="stat"><b id="cd-hours">–</b><span data-i18n="cd.hours">total hours</span></div>
    <div class="stat"><b id="cd-date">–</b><span data-i18n="cd.thedate">the date</span></div>
    <div class="stat" id="cd-today-box" style="display:none"><b>🎉</b><span data-i18n="cd.istoday">It's today!</span></div>
  </div>
  <div class="cd-custom" style="display:flex;gap:8px;align-items:center;margin-top:10px;font-size:.9rem">
    <label for="cd-date-in" data-i18n="cd.custom">Custom date</label>
    <input type="date" id="cd-date-in" style="padding:4px 8px;border-radius:8px;border:1px solid rgba(127,127,127,.4);background:transparent;color:inherit;font:inherit">
    <button type="button" class="tool-btn" id="cd-set" data-i18n="cd.set">Set</button>
    <button type="button" class="tool-btn" id="cd-clear" data-i18n="cd.clear" style="display:none">Clear</button>
    <button type="button" class="tool-btn" id="cd-ics" data-i18n="cd.ics">Add to calendar</button>
  </div>
</div>
<script>(function(){
var A=__ARGS__;
var m=A.month, d=A.day, rule=A.rule||null;
var CUST=null;
try{CUST=JSON.parse(localStorage.getItem('tt_customcd')||'null');}catch(e){}
var ICONLINK=null,ICV=null,ILAST=-2;
try{ICONLINK=document.querySelector('link[rel="apple-touch-icon"]');ICV=document.createElement('canvas');ICV.width=180;ICV.height=180;}catch(e){}
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
  if(CUST){
    var cd=new Date(CUST.y,CUST.m,CUST.d,0,0,0),start=new Date(now.getFullYear(),now.getMonth(),now.getDate(),0,0,0);
    if(cd>=start){var today=sameDay(cd,now);return {t:cd,today:today,cand:cd};}
    try{localStorage.removeItem('tt_customcd');}catch(e){}
    CUST=null;el('cd-clear').style.display='none';
  }
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
  var LC=(window.ttLang&&window.ttLang())||'en-US';
  function T(k,f){var v=null;try{v=window.npT?window.npT(k):null;}catch(e){}return v||f;}
  var EV=T('cd.ev.'+A.event.toLowerCase().replace(/[^a-z]+/g,'-').replace(/^-+|-+$/g,''),A.event),daysLbl=T('cd.days','days to go');
  if(CUST){EV=r.cand.toLocaleDateString(LC,{month:'short',day:'numeric',year:'numeric'})+' ★';daysLbl=T('cd.daysyours','days to your date');}
  el('cd-name').textContent=EV;
  if(ICV&&ICONLINK&&real!==ILAST){ILAST=real;try{
    var g=ICV.getContext('2d');
    var grd=g.createLinearGradient(0,0,0,180);grd.addColorStop(0,'#0e7490');grd.addColorStop(1,'#155e75');
    g.fillStyle=grd;g.fillRect(0,0,180,180);g.fillStyle='#fff';g.textAlign='center';
    g.font='40px serif';g.fillText(A.emoji||'📅',90,48);
    g.font='700 74px Arial,sans-serif';g.fillText(String(real),90,128);
    g.font='700 15px Arial,sans-serif';g.fillText('DAYS TO GO',90,154);
    ICONLINK.href=ICV.toDataURL('image/png');
  }catch(e){ILAST=-2;}}
  el('cd-days').textContent=real;
  el('cd-days-label').textContent=r.today?T('cd.today',"It's {ev} today! 🎉").replace('{ev}',EV):daysLbl;
  el('cd-clock').textContent=pad(hours)+':'+pad(mins)+':'+pad(secs)+'  '+T('cd.clock','h:m:s remaining today');
  el('cd-clock').style.display=r.today?'none':'block';
  el('cd-weeks').textContent=(diff/604800000).toFixed(1);
  el('cd-hours').textContent=Math.floor(diff/3600000).toLocaleString(LC);
  el('cd-date').textContent=r.cand.toLocaleDateString(LC,{weekday:'short',month:'short',day:'numeric',year:'numeric'});
  el('cd-today-box').style.display=r.today?'block':'none';
  document.title=(real>0?T('cd.title','{d}d to {ev}').replace('{d}',real).replace('{ev}',EV):EV)+' - ToolTide';
}
tick();setInterval(tick,1000);
var DIN=el('cd-date-in');
function applyCustom(){
  if(DIN.value){var p=DIN.value.split('-');CUST={y:+p[0],m:+p[1]-1,d:+p[2]};try{localStorage.setItem('tt_customcd',JSON.stringify(CUST));}catch(e){}}
  else{CUST=null;try{localStorage.removeItem('tt_customcd');}catch(e){}}
  el('cd-clear').style.display=CUST?'inline-block':'none';tick();
}
el('cd-set').addEventListener('click',applyCustom);
DIN.addEventListener('change',applyCustom);
el('cd-clear').addEventListener('click',function(){DIN.value='';applyCustom();});
if(CUST){var p2=String(CUST.m+1),dd=String(CUST.d);DIN.value=CUST.y+'-'+(p2<10?'0':'')+p2+'-'+(dd<10?'0':'')+dd;el('cd-clear').style.display='inline-block';}
el('cd-ics').addEventListener('click',function(){
  var r=target(),d=r.cand,ev=CUST?'Custom date':A.event;
  function ds(x){var mo=x.getMonth()+1,da=x.getDate();return ''+x.getFullYear()+(mo<10?'0':'')+mo+(da<10?'0':'')+da;}
  var stamp=new Date().toISOString().replace(/[-:]/g,'').split('.')[0]+'Z';
  var CRLF=String.fromCharCode(13,10);
  var ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//ToolTide//EN','BEGIN:VEVENT','UID:tt-'+Date.now()+'@tooltide','DTSTAMP:'+stamp,'DTSTART;VALUE=DATE:'+ds(d),'DTEND;VALUE=DATE:'+ds(new Date(d.getTime()+86400000)),'SUMMARY:'+ev,'DESCRIPTION:Countdown via ToolTide','END:VEVENT','END:VCALENDAR'].join(CRLF);
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);
  a.download=ev.replace(/[^a-z0-9]+/gi,'-').toLowerCase().replace(/^-|-$/g,'')+'.ics';
  document.body.appendChild(a);a.click();a.remove();
});
})();</script>
"""


# ---------------------------------------------------------------- date diff
DATEDIFF = """
<div class="tool" id="tt-dd">
  <div class="fields">
    <div class="field"><label for="dd-a" data-i18n="dd.start">Start date</label><input type="date" id="dd-a"></div>
    <div class="field"><label for="dd-b" data-i18n="dd.end">End date</label><input type="date" id="dd-b"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dd-days">–</span><span class="result-unit" data-i18n="dd.days">days</span>
    <div class="result-formula" id="dd-note"></div></div>
  <div class="stats">
    <div class="stat"><b id="dd-weeks">–</b><span data-i18n="dd.wkslbl">weeks &amp; days</span></div>
    <div class="stat"><b id="dd-wd">–</b><span data-i18n="dd.wdays">weekdays (Mon–Fri)</span></div>
    <div class="stat"><b id="dd-hours">–</b><span data-i18n="dd.hours">total hours</span></div>
  </div>
</div>
<script>(function(){
var a=document.getElementById('dd-a'),b=document.getElementById('dd-b');
function T(k,f){var v=null;try{v=window.npT?window.npT(k):null;}catch(e){}return v||f;}
function iso(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
var LC=(window.ttLang&&window.ttLang())||'en-US';
var t=new Date();a.value=iso(t);b.value=iso(new Date(t.getTime()+12096e5));
function run(){
  LC=(window.ttLang&&window.ttLang())||LC;
  if(!a.value||!b.value)return;
  var d1=new Date(a.value+'T00:00:00'),d2=new Date(b.value+'T00:00:00');
  var sign=d2<d1?-1:1,lo=sign<0?d2:d1,hi=sign<0?d1:d2;
  var days=Math.round((hi-lo)/864e5);
  document.getElementById('dd-days').textContent=sign*days;
  var w=Math.floor(days/7),rd=days%7;
  document.getElementById('dd-weeks').textContent=T('dd.wksfmt','{w} weeks + {d} days').replace('{w}',w).replace('{d}',rd);
  var wd=0,cur=new Date(lo);
  if(days<=500000){for(var i=0;i<days;i++){cur.setDate(cur.getDate()+1);var g=cur.getDay();if(g!==0&&g!==6)wd++;}}
  document.getElementById('dd-wd').textContent=days>500000?'—':wd;
  document.getElementById('dd-hours').textContent=(days*24).toLocaleString(LC);
  var opts={weekday:'long',year:'numeric',month:'long',day:'numeric'};
  document.getElementById('dd-note').textContent=lo.toLocaleDateString(LC,opts)+'  →  '+hi.toLocaleDateString(LC,opts);
}
a.addEventListener('input',run);b.addEventListener('input',run);run();
window.addEventListener('load',run);
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
    <div class="field"><label for="age-b" data-i18n="age.dob">Date of birth</label><input type="date" id="age-b"></div>
    <div class="field"><label for="age-a" data-i18n="age.at">Age at date</label><input type="date" id="age-a"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="age-main">–</span>
    <div class="result-formula" id="age-total"></div></div>
  <div class="stats">
    <div class="stat"><b id="age-days">–</b><span data-i18n="age.lived_d">days lived</span></div>
    <div class="stat"><b id="age-hours">–</b><span data-i18n="age.lived_h">hours lived</span></div>
    <div class="stat"><b id="age-next">–</b><span data-i18n="age.nextbday">days to next birthday</span></div>
  </div>
</div>
<script>(function(){
var bi=document.getElementById('age-b'),ai=document.getElementById('age-a');
function T(k,f){var v=null;try{v=window.npT?window.npT(k):null;}catch(e){}return v||f;}
var t=new Date();ai.value=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
function dim(y,mo){return new Date(y,mo+1,0).getDate();}
function run(){
  if(!bi.value||!ai.value)return;
  var b=new Date(bi.value+'T00:00:00'),a=new Date(ai.value+'T00:00:00');
  if(b>a){document.getElementById('age-main').textContent=T('age.error','Birth date must be before the target date');document.getElementById('age-total').textContent='';return;}
  var y=a.getFullYear()-b.getFullYear(),mo=a.getMonth()-b.getMonth(),d=a.getDate()-b.getDate();
  if(d<0){mo--;d+=dim(a.getFullYear(),a.getMonth()-1);}
  if(mo<0){y--;mo+=12;}
  var s=T('age.ymd','{y} years, {m} months, {d} days').replace('{y}',y).replace('{m}',mo).replace('{d}',d);
  document.getElementById('age-main').textContent=s;
  var totalDays=Math.floor((a-b)/864e5);
  document.getElementById('age-total').textContent=T('age.dtotal','{n} days in total').replace('{n}',totalDays.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US'));
  document.getElementById('age-days').textContent=totalDays.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('age-hours').textContent=(totalDays*24).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
    <div class="inline"><input type="number" id="p0-a" step="any" placeholder="20" aria-label="Percentage"> <span class="pct">%</span>
      <span class="of">of</span> <input type="number" id="p0-b" step="any" placeholder="150" aria-label="Base number"> <span>=</span>
      <b id="p0-r">–</b></div>
  </div>
  <div class="pane" data-p="1" style="display:none">
    <div class="inline"><input type="number" id="p1-a" step="any" placeholder="15" aria-label="Part value"> <span class="of">is what % of</span>
      <input type="number" id="p1-b" step="any" placeholder="60" aria-label="Total"> <span>=</span>
      <b id="p1-r">–</b><span class="pct2">%</span></div>
  </div>
  <div class="pane" data-p="2" style="display:none">
    <div class="inline"><input type="number" id="p2-a" step="any" placeholder="80" aria-label="Old value"> <span class="of">→</span>
      <input type="number" id="p2-b" step="any" placeholder="100" aria-label="New value"> <span>=</span>
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
function fmt(n){return (Math.round(n*1e6)/1e6).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{maximumFractionDigits:6});}
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
    <input type="number" id="tip-custom" step="1" min="0" max="100" placeholder="custom %" aria-label="Custom tip percent">
  </div>
  <div class="stats">
    <div class="stat"><b id="tip-amt">–</b><span data-i18n="tip.tip">tip</span></div>
    <div class="stat"><b id="tip-total">–</b><span data-i18n="tip.total">total</span></div>
    <div class="stat"><b id="tip-pp">–</b><span data-i18n="tip.pp">per person</span></div>
    <div class="stat"><b id="tip-tipp">–</b><span data-i18n="tip.tpp">tip / person</span></div>
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
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
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
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
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
  document.getElementById('rt-words').textContent=w.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('rt-chars').textContent=t.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
    <div class="stat"><b id="wc-w">0</b><span data-i18n="wc.words">words</span></div>
    <div class="stat"><b id="wc-c">0</b><span data-i18n="wc.chars">characters</span></div>
    <div class="stat"><b id="wc-cns">0</b><span data-i18n="wc.cns">chars (no spaces)</span></div>
    <div class="stat"><b id="wc-s">0</b><span data-i18n="wc.sentences">sentences</span></div>
    <div class="stat"><b id="wc-p">0</b><span data-i18n="wc.paras">paragraphs</span></div>
    <div class="stat"><b id="wc-rt">–</b><span data-i18n="wc.rt">reading time</span></div>
  </div>
</div>
<script>(function(){
function T(k,f){var v=null;try{v=window.npT?window.npT(k):null;}catch(e){}return v||f;}
function run(){
  var t=document.getElementById('wc-txt').value;
  var w=t.trim()?t.trim().split(/\\s+/).length:0;
  var sents=(t.match(/[^.!?]+[.!?]+(\\s|$)|[^.!?]+$/g)||[]).filter(function(s){return s.trim();}).length;
  var paras=t.split(/\\n+/).filter(function(p){return p.trim();}).length;
  document.getElementById('wc-w').textContent=w.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('wc-c').textContent=t.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('wc-cns').textContent=t.replace(/\\s/g,'').length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('wc-s').textContent=sents.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('wc-p').textContent=paras.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  var m=w/225;
  document.getElementById('wc-rt').textContent=m<1?Math.max(1,Math.round(m*60))+' '+T('wc.sec','sec'):(Math.round(m*10)/10)+' '+T('wc.min','min');
}
document.getElementById('wc-txt').addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- case converter
CASE = """
<div class="tool" id="tt-case">
  <div class="field"><label for="case-in"><span data-i18n="lbl.yourtext">Your text</span></label>
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
  <div class="field"><label for="case-out">Result <button class="btn btn-sm" id="case-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  var b=document.getElementById('case-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
  <div class="chips" id="uc-swap-row"><button class="chip" id="uc-swap" data-i18n="uc.swap">⇄ Swap direction</button></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="uc-r">–</span>
    <div class="result-formula" id="uc-f"></div></div>
  <table class="copytable" id="uc-table"><thead><tr><th id="uc-th1"></th><th id="uc-th2"></th></tr></thead><tbody></tbody></table>
</div>
<script>(function(){
var A=__ARGS__;
function T(k,f){var v=null;try{v=window.npT?window.npT(k):null;}catch(e){}return v||f;}
var LC=(window.ttLang&&window.ttLang())||'en-US';
var la=document.getElementById('uc-la'),lb=document.getElementById('uc-lb');
var a=document.getElementById('uc-a'),b=document.getElementById('uc-b');
var r=document.getElementById('uc-r'),f=document.getElementById('uc-f');
var swapped=false;
function fmt(n){return n.toLocaleString(LC,{maximumFractionDigits:A.dec===undefined?4:A.dec});}
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
    ?(A.factor===null||A.factor===undefined?(T('uc.formula','Formula: ')+'('+v+' °F − 32) × 5/9 = '+fmt(out)+' °C'):(T('uc.formula','Formula: ')+v+' ÷ '+A.factor+' = '+fmt(out)))
    :(A.factor===null||A.factor===undefined?(T('uc.formula','Formula: ')+v+' × 9/5 + 32 = '+fmt(out)):(T('uc.formula','Formula: ')+v+' × '+A.factor+' = '+fmt(out))));
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
  tr.innerHTML='<td>'+v.toLocaleString(LC)+'</td><td>'+fmt(o)+'</td>';
  tb.appendChild(tr);
});
labels();a.value='1';run();
window.addEventListener('load',run);
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
  <textarea id="type-in" rows="4" placeholder="Click here and start typing — the timer starts with your first key…" aria-label="Typing area"></textarea>
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
  <div class="pw-out-row"><input type="text" id="pw-out" readonly aria-label="Generated password"><button class="btn btn-sm" id="pw-copy" type="button" data-i18n="ui.copy">Copy</button></div>
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
  if(!pool){document.getElementById('pw-out').value=TT('pw.noset','Select at least one character set');return;}
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
  var b=document.getElementById('pw-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
  if(isNaN(min)||isNaN(max)||max<=min){note.textContent=TT('rng.maxmin','Maximum must be greater than minimum.');return;}
  if(count<1||count>100){note.textContent=TT('rng.count','Count must be between 1 and 100.');return;}
  var out=[],seen={};
  if(whole){
    var size=Math.floor(max)-Math.ceil(min)+1;
    if(unique&&count>size){note.textContent=TT('rng.cantpick','Cannot pick {n} unique numbers from a range of {m}. Widen the range or allow duplicates.').replace('{n}',count).replace('{m}',size);return;}
    while(out.length<count){
      var v=Math.ceil(min)+secureInt(size);
      if(unique&&seen[v])continue;
      seen[v]=1;out.push(v);
    }
  }else{
    if(unique){note.textContent=TT('rng.nodup','No-duplicates applies to whole numbers only.');return;}
    for(var i=0;i<count;i++){out.push((min+(max-min)*secureInt(100000)/100000).toFixed(4));}
  }
  $('rng-res').textContent=out.join(',  ');
  $('rng-out').style.display='block';
  note.textContent=TT('rng.gen','Generated: {n} · crypto-secure · nothing recorded.').replace('{n}',out.length);
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
  document.getElementById('wp-out').textContent=v?(Math.round(pages*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US'):'–';
  document.getElementById('wp-note').textContent=v?('≈ '+Math.ceil(pages)+' full page'+(Math.ceil(pages)>1?'s':'')+' · '+v.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' words ÷ '+per+' words per page'):'';
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
  if(n===null){out.textContent='–';note.textContent=TT('roman.invalid','Not a valid standard Roman numeral (1–3999).');}
  else{num.value=n;out.textContent=n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');note.textContent=v.toUpperCase()+' = '+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
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
  if(!w||w<=0||w>100||isNaN(c)){box.textContent='–';txt.textContent=TT('gr.needlbl','needed on the final');return;}
  var need=(target-c*(1-w/100))/(w/100);
  if(need<0){box.textContent='0%';txt.textContent=TT('gr.secured','— target already secured 🎉');}
  else if(need>100){box.textContent='>100%';txt.textContent=TT('gr.outreach','— mathematically out of reach');}
  else{box.textContent=(Math.round(need*10)/10)+'%';txt.textContent=TT('gr.needlbl','needed on the final');}
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
  <div class="field" style="margin-top:12px"><label for="dd2-out">Cleaned output <button class="btn btn-sm" id="dd2-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  document.getElementById('dd2-orig').textContent=lines.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('dd2-uniq').textContent=res.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('dd2-rem').textContent=(lines.length-res.length).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  out.value=res.join('\\n');
}
inp.addEventListener('input',run);
document.getElementById('dd2-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('dd2-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
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
  <div class="field"><label for="fl-in"><span data-i18n="lbl.yourtext">Your text</span></label>
    <textarea id="fl-in" rows="4" placeholder="Type something…"></textarea></div>
  <div class="field" style="margin-top:10px"><label for="fl-out">Flipped upside down <button class="btn btn-sm" id="fl-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  var b=document.getElementById('fl-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
  document.getElementById('hd-mins').textContent=d.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  <div class="field" style="margin-top:10px"><label for="sh-out">Plain text <button class="btn btn-sm" id="sh-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  document.getElementById('sh-tags').textContent=tags.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
}
inp.addEventListener('input',run);
document.getElementById('sh-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('sh-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
  document.getElementById('avg-mean').textContent=(Math.round(mean*1e6)/1e6).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('avg-sum').textContent=(Math.round(sum*1e6)/1e6).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('avg-n').textContent=nums.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('avg-min').textContent=Math.min.apply(null,nums).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('avg-max').textContent=Math.max.apply(null,nums).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('avg-note').textContent='Sum '+nums.length+' values ÷ '+nums.length+' = mean';
}
inp.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- text <-> binary
BINARY = """
<div class="tool" id="tt-bin">
  <div class="field"><label for="bin-txt"><span data-i18n="lbl.text">Text</span></label>
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
  document.getElementById('dw-out').textContent=dt.toLocaleDateString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{weekday:'long'});
  document.getElementById('dw-note').textContent=dt.toLocaleDateString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{year:'numeric',month:'long',day:'numeric'});
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
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{maximumFractionDigits:2});}
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
    <div class="field"><label for="sq-l"><span data-i18n="lbl.length">Length</span></label><input type="number" id="sq-l" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="sq-w"><span data-i18n="lbl.width">Width</span></label><input type="number" id="sq-w" step="any" min="0" placeholder="15"></div>
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
  document.getElementById('sq-ft').textContent=sq===null?'-':(Math.round(sqft*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('sq-sqft').textContent=sq===null?'-':(Math.round(sqft*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('sq-sqm').textContent=sq===null?'-':(Math.round(sqm*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  out.textContent=v.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' seconds';sIn.value=v;
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
  document.getElementById('dc-total').textContent=sum.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  document.getElementById('cf-cuft').textContent=(Math.round(cuft*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('cf-cum').textContent=(Math.round(cuft*0.0283168466*1000)/1000).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('cf-out').textContent=(Math.round(cuft*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  <div class="field" style="margin-top:10px"><label for="sort-out">Sorted <button class="btn btn-sm" id="sort-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  var b=document.getElementById('sort-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{maximumFractionDigits:4});}
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
  if(!/^\d+$/.test(v)){out.textContent='-';note.textContent=TT('num.whole','Whole numbers only.');return;}
  var n=BigInt(v);
  if(n<2n){out.textContent=TT('prime.no','Not prime');note.textContent=TT('prime.lt2','Numbers below 2 are neither prime nor composite.');return;}
  var small=[2n,3n,5n,7n,11n,13n,17n,19n,23n,29n,31n,37n];
  for(var i=0;i<small.length;i++){
    if(n===small[i]){out.textContent=TT('prime.yes','Prime!');note.textContent=TT('prime.list','{v} is prime (it is in the base list).').replace('{v}',v);return;}
    if(n%small[i]===0n){out.textContent=TT('prime.no','Not prime');note.textContent=TT('prime.div','Divisible by {n}.').replace('{n}',small[i].toString());return;}
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
  document.getElementById('fa-digits').textContent=f.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  document.getElementById('sl-kg').textContent=(Math.round(kg*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('sl-total-lb').textContent=Math.round(s*14+p).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  document.getElementById('sl-kg').textContent=(Math.round(k*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('sl-total-lb').textContent=Math.round(totalLb).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  document.getElementById('fi-cm').textContent=(Math.round(cm*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('fi-inonly').textContent=(Math.round(cm/2.54*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  document.getElementById('fi-cm').textContent=(Math.round(c*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('fi-inonly').textContent=(Math.round(inOnly*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
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
  <div class="field" style="margin-top:10px"><label for="ws-out">Cleaned <button class="btn btn-sm" id="ws-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  document.getElementById('ws-inlines').textContent=lines.length.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('ws-chars').textContent=Math.max(0,before-res.length).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
}
inp.addEventListener('input',run);
['ws-trim','ws-collapse','ws-blank'].forEach(function(id){document.getElementById(id).addEventListener('click',run);});
document.getElementById('ws-copy').addEventListener('click',function(){
  out.select();
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(out.value);}
  else{document.execCommand('copy');}
  var b=document.getElementById('ws-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
    <div class="field"><label for="cy-h"><span data-i18n="lbl.height">Height</span></label><input type="number" id="cy-h" step="any" min="0" placeholder="10"></div>
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
  document.getElementById('cy-out').textContent=(Math.round(v*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('cy-unit').textContent='cubic '+('units');
  document.getElementById('cy-liters').textContent=(Math.round(v/1000*1000)/1000).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
}
r.addEventListener('input',run);h.addEventListener('input',run);run();
})();</script>
"""


# ---------------------------------------------------------------- morse code
MORSE = """
<div class="tool" id="tt-mo">
  <div class="field"><label for="mo-txt"><span data-i18n="lbl.text">Text</span></label>
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
  if(isNaN(d.getTime())){document.getElementById('ep-utc').textContent=TT('ep.range','out of range');return;}
  document.getElementById('ep-utc').textContent=d.toISOString().slice(0,19).replace('T',' ')+' UTC';
  document.getElementById('ep-local').textContent=d.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
}
function runDate(){
  if(!dt.value)return;
  var d=new Date(dt.value);
  var secs=Math.floor(d.getTime()/1000);
  ts.value=secs;
  document.getElementById('ep-utc').textContent=d.toISOString().slice(0,19).replace('T',' ')+' UTC';
  document.getElementById('ep-local').textContent=d.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
}
ts.addEventListener('input',runTs);
dt.addEventListener('input',runDate);
var now=document.getElementById('ep-now');
function tick(){now.textContent=Math.floor(Date.now()/(ms?1:1000)).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
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
  out.textContent=(n===null)?'(could not parse - check the spelling)':n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
});
})();</script>
"""


# ---------------------------------------------------------------- speed distance time
SDT = """
<div class="tool" id="tt-sdt">
  <div class="fields">
    <div class="field"><label for="sdt-d"><span data-i18n="lbl.distance">Distance</span></label><input type="number" id="sdt-d" step="any" min="0" placeholder="120"></div>
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
  <div class="field"><label for="rv-in"><span data-i18n="lbl.yourtext">Your text</span></label>
    <textarea id="rv-in" rows="4" placeholder="Type something to reverse..."></textarea></div>
  <div class="field" style="margin-top:10px"><label for="rv-out">Reversed <button class="btn btn-sm" id="rv-copy" type="button" data-i18n="ui.copy">Copy</button></label>
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
  var b=document.getElementById('rv-copy');b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent=TT('ui.copy','Copy');},1200);
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
  out.textContent=d.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  note.textContent=v+' binary = '+d.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' decimal';
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
    note.textContent=TT('bindec.note','{d} decimal = {b} binary').replace('{d}',v).replace('{b}',b);
  }catch(e){out.textContent='-';note.textContent=TT('bindec.big','Number too large.');}
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
  if(k<0){set(k,k*1-273.15,null,TT('temp.belowabs','Below absolute zero - physically impossible.'));return;}
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
  <button type="button" class="tool-btn" id="dd-share" data-i18n="share.share-this-deal-math">Share this deal math</button>
</div>
<script>(function(){
var E={};['dd-price','dd-d1','dd-d2','dd-flat'].forEach(function(id){E[id]=document.getElementById(id);});
var OUT=document.getElementById('dd-out'),NOTE=document.getElementById('dd-note');
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
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
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-deal-math','Share this deal math');},1500);}
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
  <button type="button" class="tool-btn" id="si-share" data-i18n="share.share-this-result">Share this result</button>
</div>
<script>(function(){
var P=document.getElementById('si-p'),R=document.getElementById('si-r'),T=document.getElementById('si-t');
var OUT=document.getElementById('si-out');
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
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
  document.getElementById('si-note').textContent='SI = P × r × t = '+p.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' × '+(r*100).toFixed(2).replace('.00','')+'% × '+t+' = '+money(si)+
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
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-result','Share this result');},1500);}
});
})();
</script>
"""

# GST calculator: price with inclusive/exclusive toggle and India's standard slabs.
# Retention hooks: title result hook, tt_gst input memory, URL state (?p=&r=&mode=), Web Share.
GST = """<div class="tool" id="tt-gst">
  <div class="fields">
    <div class="field"><label for="gs-p">Price (₹)</label><input type="number" id="gs-p" step="any" min="0" placeholder="2499"></div>
    <div class="field"><label for="gs-r">GST rate</label>
      <select id="gs-r"><option value="5">5%</option><option value="12">12%</option><option value="18" selected>18%</option><option value="28">28%</option></select></div>
    <div class="field"><label for="gs-m">Price includes GST?</label>
      <select id="gs-m"><option value="ex">No — add GST</option><option value="in">Yes — extract GST</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gs-out">–</span><span class="result-unit" id="gs-unit"></span></div>
  <div class="stats">
    <div class="stat"><b id="gs-net">–</b><span>net (before GST)</span></div>
    <div class="stat"><b id="gs-tax">–</b><span>GST amount</span></div>
    <div class="stat"><b id="sg-cgst">–</b><span>CGST / SGST each</span></div>
  </div>
  <div class="tool-note" id="gs-note"></div>
  <button type="button" class="tool-btn" id="gs-share" data-i18n="share.share-the-split">Share the split</button>
</div>
<script>(function(){
var P=document.getElementById('gs-p'),R=document.getElementById('gs-r'),M=document.getElementById('gs-m');
var OUT=document.getElementById('gs-out');
function money(n){return '₹'+n.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parseFloat(P.value),r=parseFloat(R.value)||0,incl=M.value==='in';
  if(isNaN(p)||!p){OUT.textContent='–';document.getElementById('gs-net').textContent='–';
    document.getElementById('gs-tax').textContent='–';document.getElementById('sg-cgst').textContent='–';
    document.getElementById('gs-note').textContent='';document.title='GST Calculator - ToolTide';return;}
  var net,tax;
  if(incl){net=p/(1+r/100);tax=p-net;}else{net=p;tax=p*r/100;}
  var gross=net+tax;
  OUT.textContent=incl?money(net):money(gross);
  document.getElementById('gs-unit').textContent=incl?'net price (GST extracted)':'gross price (with GST)';
  document.getElementById('gs-net').textContent=money(net);
  document.getElementById('gs-tax').textContent=money(tax);
  document.getElementById('sg-cgst').textContent=money(tax/2);
  document.getElementById('gs-note').textContent=(incl?'GST extracted from an inclusive price: ':'GST added on an exclusive price: ')+money(tax)+
    ' at '+r+'%. Intra-state sales split it as CGST + SGST of '+money(tax/2)+' each; inter-state is IGST of '+money(tax)+'.';
  document.title='GST '+money(tax)+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_gst',JSON.stringify({p:P.value,r:R.value,m:M.value}));}catch(e){}}
[P,R,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
M.addEventListener('change',function(){calc();save();});
var pre=false;
[['p',P],['r',R],['mode',M]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_gst')||'null');if(mem){P.value=mem.p||'';R.value=mem.r||'18';M.value=mem.m||'ex';}}catch(e){}}
calc();
document.getElementById('gs-share').addEventListener('click',function(){
  var txt='GST on '+money(parseFloat(P.value)||0)+' at '+R.value+'%: '+document.getElementById('gs-tax').textContent+
    '. Split any invoice (no sign-up):';
  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value||'')+'&r='+R.value+'&mode='+M.value;
  if(navigator.share){navigator.share({title:'GST split',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-split','Share the split');},1500);}
});
})();
</script>
"""

# Overtime pay: weekly hours vs threshold x multiplier -> regular, OT and total pay.
# Retention hooks: title result hook, tt_overtime input memory, URL state (?r=&h=&t=&m=), Web Share.
OVERTIME = """<div class="tool" id="tt-ot">
  <div class="fields">
    <div class="field"><label for="ot-r">Hourly rate ($)</label><input type="number" id="ot-r" step="any" min="0" placeholder="25"></div>
    <div class="field"><label for="ot-h">Hours this week</label><input type="number" id="ot-h" step="any" min="0" max="100" placeholder="47"></div>
    <div class="field"><label for="ot-t">OT after (hours)</label><input type="number" id="ot-t" step="1" min="1" max="60" value="40"></div>
    <div class="field"><label for="ot-m">OT multiplier</label><input type="number" id="ot-m" step="any" min="1" max="3" value="1.5"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ot-out">–</span><span class="result-unit">gross pay this week</span></div>
  <div class="stats">
    <div class="stat"><b id="ot-reg">–</b><span>regular pay</span></div>
    <div class="stat"><b id="ot-ot">–</b><span>overtime pay</span></div>
    <div class="stat"><b id="ot-rate">–</b><span>OT hourly rate</span></div>
  </div>
  <div class="tool-note" id="ot-note"></div>
  <button type="button" class="tool-btn" id="ot-share" data-i18n="share.share-my-week">Share my week</button>
</div>
<script>(function(){
var R=document.getElementById('ot-r'),H=document.getElementById('ot-h'),T=document.getElementById('ot-t'),M=document.getElementById('ot-m');
var OUT=document.getElementById('ot-out');
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var r=parseFloat(R.value)||0,h=parseFloat(H.value)||0,t=parseFloat(T.value)||40,m=parseFloat(M.value)||1.5;
  if(!r||!h){OUT.textContent='–';document.getElementById('ot-reg').textContent='–';
    document.getElementById('ot-ot').textContent='–';document.getElementById('ot-rate').textContent='–';
    document.getElementById('ot-note').textContent='';document.title='Overtime Pay Calculator - ToolTide';return;}
  var oth=Math.max(0,h-t),reg=Math.min(h,t)*r,ot=oth*r*m,total=reg+ot;
  OUT.textContent=money(total);
  document.getElementById('ot-reg').textContent=money(reg);
  document.getElementById('ot-ot').textContent=money(ot)+(oth?' ('+oth+' h)':'');
  document.getElementById('ot-rate').textContent=money(r*m);
  document.getElementById('ot-note').textContent='US FLSA baseline: 1.5× past 40 hours in a workweek. '+
    (oth?('This week includes '+oth+' OT hours - worth '+money(oth*r*(m-1))+' extra versus plain time.'):'No overtime hours this week - every hour is plain time.')+
    ' Some states and contracts double time past 12-hour days; adjust the multiplier for those rules.';
  document.title=money(total)+' this week - ToolTide';
}
function save(){try{localStorage.setItem('tt_overtime',JSON.stringify({r:R.value,h:H.value,t:T.value,m:M.value}));}catch(e){}}
[R,H,T,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['r',R],['h',H],['t',T],['m',M]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_overtime')||'null');if(mem){R.value=mem.r||'';H.value=mem.h||'';T.value=mem.t||'40';M.value=mem.m||'1.5';}}catch(e){}}
calc();
document.getElementById('ot-share').addEventListener('click',function(){
  var txt='This week: '+H.value+' hours at '+money(parseFloat(R.value)||0)+'/hr = '+OUT.textContent+
    ' gross'+((parseFloat(H.value)||0)>(parseFloat(T.value)||40)?' (with overtime)':'')+'. Check yours (no sign-up):';
  var url=location.origin+location.pathname+'?r='+encodeURIComponent(R.value||'')+'&h='+encodeURIComponent(H.value||'')+'&t='+encodeURIComponent(T.value||'')+'&m='+encodeURIComponent(M.value||'');
  if(navigator.share){navigator.share({title:'Overtime pay',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-week','Share my week');},1500);}
});
})();
</script>
"""

# Rent affordability: gross income -> max rent by the 30% rule and a 36% DTI check.
# Retention hooks: title result hook, tt_rent input memory, URL state (?inc=&debt=&r=), Web Share.
RENT = """<div class="tool" id="tt-rent">
  <div class="fields">
    <div class="field"><label for="rt-inc">Gross monthly income ($)</label><input type="number" id="rt-inc" step="any" min="0" placeholder="4800"></div>
    <div class="field"><label for="rt-debt">Monthly debt payments ($, optional)</label><input type="number" id="rt-debt" step="any" min="0" placeholder="350"></div>
    <div class="field"><label for="rt-rule">Budget rule</label>
      <select id="rt-rule"><option value="30">30% of income (classic)</option><option value="25">25% — aggressive saving</option><option value="35">35% — high-cost city</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="rt-out">–</span><span class="result-unit">max monthly rent</span></div>
  <div class="stats">
    <div class="stat"><b id="rt-30">–</b><span>by the 30% rule</span></div>
    <div class="stat"><b id="rt-dti">–</b><span>after debts (36% DTI)</span></div>
    <div class="stat"><b id="rt-left">–</b><span>left for everything else</span></div>
  </div>
  <div class="tool-note" id="rt-note"></div>
  <button type="button" class="tool-btn" id="rt-share" data-i18n="share.share-my-budget">Share my budget</button>
</div>
<script>(function(){
var I=document.getElementById('rt-inc'),D=document.getElementById('rt-debt'),RU=document.getElementById('rt-rule');
var OUT=document.getElementById('rt-out');
function money(n){return '$'+Math.round(n).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var inc=parseFloat(I.value)||0,debt=parseFloat(D.value)||0,rule=parseFloat(RU.value)||30;
  if(!inc){OUT.textContent='–';document.getElementById('rt-30').textContent='–';
    document.getElementById('rt-dti').textContent='–';document.getElementById('rt-left').textContent='–';
    document.getElementById('rt-note').textContent='';document.title='Rent Affordability Calculator - ToolTide';return;}
  var cap=inc*rule/100,dti=inc*0.36-debt,left=inc-cap-debt;
  var best=Math.min(cap,dti>0?dti:0);
  OUT.textContent=money(best);
  document.getElementById('rt-30').textContent=money(cap);
  document.getElementById('rt-dti').textContent=money(Math.max(0,dti));
  document.getElementById('rt-left').textContent=money(Math.max(0,left));
  document.getElementById('rt-note').textContent='Landlords typically want rent under 30% of gross income; lenders cap all debt (rent included) near 36%. '+
    (debt>0?('Your '+money(debt)+' in monthly payments is why the DTI line is lower - it is the honest ceiling for this budget.'):'No debts entered - the DTI line matches a 36% total ceiling.')+
    ' Remember utilities, deposits and commuter costs on top of the number.';
  document.title=money(best)+'/mo rent budget - ToolTide';
}
function save(){try{localStorage.setItem('tt_rent',JSON.stringify({i:I.value,d:D.value,r:RU.value}));}catch(e){}}
[I,D,RU].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
RU.addEventListener('change',function(){calc();save();});
var pre=false;
[['inc',I],['debt',D],['r',RU]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_rent')||'null');if(mem){I.value=mem.i||'';D.value=mem.d||'';RU.value=mem.r||'30';}}catch(e){}}
calc();
document.getElementById('rt-share').addEventListener('click',function(){
  var txt='My rent budget: '+OUT.textContent+'/month (30% rule'+(parseFloat(D.value)?' and 36% DTI adjusted':'')+
    '). Find yours (no sign-up):';
  var url=location.origin+location.pathname+'?inc='+encodeURIComponent(I.value||'')+'&debt='+encodeURIComponent(D.value||'')+'&r='+RU.value;
  if(navigator.share){navigator.share({title:'Rent budget',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-budget','Share my budget');},1500);}
});
})();
</script>
"""

# CGPA <-> percentage (Indian 10-point scale, CBSE 9.5 factor), bidirectional with a table.
# Retention hooks: title result hook, tt_cgpa input memory, URL state (?v=&d=), Web Share.
CGPA = """<div class="tool" id="tt-cg">
  <div class="fields">
    <div class="field"><label for="cg-d"><span data-i18n="lbl.direction">Direction</span></label><select id="cg-d"><option value="c2p">CGPA → Percentage</option><option value="p2c">Percentage → CGPA</option></select></div>
    <div class="field"><label for="cg-v">Value (CGPA out of 10, or %)</label><input type="number" id="cg-v" step="any" min="0" max="100" placeholder="8.6"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cg-out">–</span><span class="result-unit" id="cg-unit">percentage</span></div>
  <div class="stats">
    <div class="stat"><b id="cg-class">–</b><span>typical class</span></div>
    <div class="stat"><b id="cg-other">–</b><span>other direction</span></div>
  </div>
  <div class="tool-note" id="cg-note"></div>
  <button type="button" class="tool-btn" id="cg-share" data-i18n="share.share-the-result">Share the result</button>
</div>
<script>(function(){
var D=document.getElementById('cg-d'),V=document.getElementById('cg-v');
var OUT=document.getElementById('cg-out'),UNIT=document.getElementById('cg-unit');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var v=parseFloat(V.value),d=D.value;
  if(isNaN(v)){OUT.textContent='–';UNIT.textContent=d==='c2p'?'percentage':'CGPA (10-point)';document.getElementById('cg-class').textContent='–';document.getElementById('cg-other').textContent='–';document.getElementById('cg-note').textContent='';document.title='CGPA to Percentage - ToolTide';return;}
  var pct,cg;
  if(d==='c2p'){cg=v;pct=v*9.5;}else{pct=v;cg=v/9.5;}
  OUT.textContent=d==='c2p'?Math.round(pct*100)/100+'%':Math.round(cg*100)/100;
  UNIT.textContent=d==='c2p'?'percentage':'CGPA (10-point)';
  var cls='—';
  if(pct>=75)cls='Distinction territory';
  else if(pct>=60)cls='First class';
  else if(pct>=50)cls='Second class';
  document.getElementById('cg-class').textContent=cls;
  document.getElementById('cg-other').textContent=d==='c2p'?Math.round(v/9.5*100)/100:Math.round(v*9.5*100)/100+'%';
  document.getElementById('cg-note').textContent='CBSE formula: percentage = CGPA × 9.5. Some universities use different factors (9.0-10.0) or letter tables - always check your institution\\'s certificate before quoting a converted number on a form.';
  document.title=d==='c2p'?Math.round(pct*100)/100+'% from CGPA - ToolTide':'CGPA '+Math.round(cg*100)/100+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_cgpa',JSON.stringify({d:D.value,v:V.value}));}catch(e){}}
[D,V].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
D.addEventListener('change',function(){V.placeholder=D.value==='c2p'?'8.6':'82';calc();save();});
var pre=false;
[['v',V],['d',D]].forEach(function(a){var x=qs(a[0]);if(x!==null){a[1].value=x;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_cgpa')||'null');if(mem){D.value=mem.d||'c2p';V.value=mem.v||'';}}catch(e){}}
calc();
document.getElementById('cg-share').addEventListener('click',function(){
  var txt='CGPA '+V.value+' converts to '+OUT.textContent+' ('+UNIT.textContent+'). Convert yours (no sign-up):';
  var url=location.origin+location.pathname+'?d='+D.value+'&v='+encodeURIComponent(V.value||'');
  if(navigator.share){navigator.share({title:'CGPA conversion',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-result','Share the result');},1500);}
});
})();
</script>
"""

# Caffeine tracker: common drinks -> daily total vs the 400 mg adult guideline and a cutoff time.
# Retention hooks: title result hook, tt_caffeine input memory, URL state (?drinks=), Web Share.
CAFFEINE = """<div class="tool" id="tt-caf">
  <div id="caf-rows"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="caf-out">–</span><span class="result-unit">mg caffeine today</span></div>
  <div class="stats">
    <div class="stat"><b id="caf-left">–</b><span>of 400 mg guideline</span></div>
    <div class="stat"><b id="caf-cutoff">–</b><span>last safe cup by</span></div>
  </div>
  <div class="tool-note">Half-life is about 5-6 hours: a 4 PM double shot still holds ~100 mg at 10 PM. Sensitive people, pregnancy and some medications lower the safe ceiling - treat 400 mg as the healthy-adult maximum, not a target.</div>
  <button type="button" class="tool-btn" id="caf-share" data-i18n="share.share-my-total">Share my total</button>
</div>
<script>(function(){
var DR=[['Filter coffee',95],['Espresso',63],['Instant coffee',66],['Black tea',47],['Green tea',28],['Cola (330 ml)',34],['Energy drink (250 ml)',80],['Matcha latte',70],['Decaf coffee',7]];
var box=document.getElementById('caf-rows');
DR.forEach(function(d,i){
  var f=document.createElement('div');f.className='fields';
  f.innerHTML='<div class="field"><label for="caf-n'+i+'">'+d[0]+' ('+d[1]+' mg each)</label><select id="caf-n'+i+'" class="caf-n" data-mg="'+d[1]+'">'+
    [0,1,2,3,4,5].map(function(n){return '<option value="'+n+'"'+(n===0?' selected':'')+'>'+n+'</option>';}).join('')+'</select></div>';
  box.appendChild(f);
});
function sel(){return box.querySelectorAll('.caf-n');}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var s=sel(),mg=0;
  for(var i=0;i<s.length;i++){mg+=(parseInt(s[i].value,10)||0)*parseInt(s[i].getAttribute('data-mg'),10);}
  OUT.textContent=mg;
  document.getElementById('caf-left').textContent=Math.max(0,400-mg)+' mg';
  var now=new Date(),cutoff=new Date(now.getTime()+(0));
  var bed=new Date(now.getFullYear(),now.getMonth(),now.getDate(),23,0,0);
  var last=new Date(bed.getTime()-6*3600*1000);
  var hh=last.getHours(),mm=last.getMinutes(),ap=hh<12?'AM':'PM',h12=hh%12;if(h12===0)h12=12;
  document.getElementById('caf-cutoff').textContent=h12+':'+(mm<10?'0':'')+mm+' '+ap+' (for an 11 PM bedtime)';
  document.title=mg+' mg caffeine - ToolTide';
}
function save(){var s=sel(),a=[];for(var i=0;i<s.length;i++)a.push(s[i].value);
  try{localStorage.setItem('tt_caffeine',JSON.stringify(a));}catch(e){}}
function fill(a){var s=sel();for(var i=0;i<s.length;i++)s[i].value=(a&&a[i])||'0';calc();}
box.addEventListener('change',function(){calc();save();});
try{var mem=JSON.parse(localStorage.getItem('tt_caffeine')||'null');if(mem)fill(mem);}catch(e){}
var qsV=qs('drinks');if(qsV)fill(qsV.split(','));
calc();
document.getElementById('caf-share').addEventListener('click',function(){
  var txt='My caffeine today: '+OUT.textContent+' mg. Track yours (no sign-up):';
  var s=sel(),a=[];for(var i=0;i<s.length;i++)a.push(s[i].value);
  var url=location.origin+location.pathname+'?drinks='+a.join(',');
  if(navigator.share){navigator.share({title:'Caffeine total',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-total','Share my total');},1500);}
});
})();
</script>
"""

# Body fat percentage (US Navy circumference method), male and female formulas.
# Retention hooks: title result hook, tt_bodyfat input memory, URL state (?s=&h=&n=&w=&hp=), Web Share.
BODYFAT = """<div class="tool" id="tt-bf">
  <div class="fields">
    <div class="field"><label for="bf-s"><span data-i18n="lbl.sex">Sex</span></label><select id="bf-s"><option value="m">Male</option><option value="f">Female</option></select></div>
    <div class="field"><label for="bf-h">Height (cm)</label><input type="number" id="bf-h" step="any" min="100" max="230" placeholder="175"></div>
    <div class="field"><label for="bf-n">Neck (cm)</label><input type="number" id="bf-n" step="any" min="20" max="60" placeholder="38"></div>
    <div class="field"><label for="bf-w">Waist (cm)</label><input type="number" id="bf-w" step="any" min="40" max="200" placeholder="85"></div>
    <div class="field" id="bf-hip-wrap" style="display:none"><label for="bf-hip">Hip (cm)</label><input type="number" id="bf-hip" step="any" min="50" max="200" placeholder="98"></div>
    <div class="field"><label for="bf-kg">Weight (kg, for mass split)</label><input type="number" id="bf-kg" step="any" min="30" max="300" placeholder="75"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bf-out">–</span><span class="result-unit">estimated body fat</span></div>
  <div class="stats">
    <div class="stat"><b id="bf-cat">–</b><span>category</span></div>
    <div class="stat"><b id="bf-fatkg">–</b><span>fat mass</span></div>
    <div class="stat"><b id="bf-leankg">–</b><span>lean mass</span></div>
  </div>
  <div class="tool-note" id="bf-note"></div>
  <button type="button" class="tool-btn" id="bf-share" data-i18n="share.share-my-estimate">Share my estimate</button>
</div>
<script>(function(){
var S=document.getElementById('bf-s'),H=document.getElementById('bf-h'),N=document.getElementById('bf-n'),W=document.getElementById('bf-w'),HP=document.getElementById('bf-hip'),HW=document.getElementById('bf-hip-wrap');
var OUT=document.getElementById('bf-out');
var CATS={m:[[6,'Essential fat'],[14,'Athletic'],[18,'Fitness'],[25,'Average'],[999,'Above average']],f:[[14,'Essential fat'],[21,'Athletic'],[25,'Fitness'],[32,'Average'],[999,'Above average']]};
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var sex=S.value,h=parseFloat(H.value)||0,n=parseFloat(N.value)||0,w=parseFloat(W.value)||0;
  if(!h||!n||!w||(sex==='f'&&!parseFloat(HP.value))){OUT.textContent='–';document.getElementById('bf-cat').textContent='–';
    document.getElementById('bf-fatkg').textContent='–';document.getElementById('bf-leankg').textContent='–';
    document.getElementById('bf-note').textContent='';document.title='Body Fat Calculator - ToolTide';return;}
  var bf;
  if(sex==='m'){bf=495/(1.0324-0.19077*Math.log10(w-n)+0.15456*Math.log10(h))-450;}
  else{bf=495/(1.29579-0.35004*Math.log10(w+parseFloat(HP.value)-n)+0.221*Math.log10(h))-450;}
  OUT.textContent=Math.round(bf*10)/10+'%';
  var cats=CATS[sex],cat=cats[cats.length-1][1];
  for(var i=0;i<cats.length;i++){if(bf<cats[i][0]){cat=cats[i][1];break;}}
  document.getElementById('bf-cat').textContent=cat;
  var kg=parseFloat(document.getElementById('bf-kg').value)||0;
  document.getElementById('bf-fatkg').textContent=kg?Math.round(kg*bf/100)+' kg':'–';
  document.getElementById('bf-leankg').textContent=kg?Math.round(kg*(1-bf/100))+' kg':'–';
  document.getElementById('bf-note').textContent='US Navy circumference method - accurate to roughly ±3% versus DEXA for most people. Track the trend on the same tape, same time of day, rather than treating one reading as truth.';
  document.title=Math.round(bf*10)/10+'% body fat - ToolTide';
}
function save(){try{localStorage.setItem('tt_bodyfat',JSON.stringify({s:S.value,h:H.value,n:N.value,w:W.value,hp:HP.value,k:document.getElementById('bf-kg').value}));}catch(e){}}
S.addEventListener('change',function(){HW.style.display=S.value==='f'?'':'none';calc();save();});
[H,N,W,HP,document.getElementById('bf-kg')].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['s',S],['h',H],['n',N],['w',W],['hp',HP]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
var kgv=qs('kg');if(kgv!==null){document.getElementById('bf-kg').value=kgv;pre=true;}
if(pre){HW.style.display=S.value==='f'?'':'none';}
else{try{var mem=JSON.parse(localStorage.getItem('tt_bodyfat')||'null');if(mem){S.value=mem.s||'m';H.value=mem.h||'';N.value=mem.n||'';W.value=mem.w||'';HP.value=mem.hp||'';document.getElementById('bf-kg').value=mem.k||'';HW.style.display=S.value==='f'?'':'none';}}catch(e){}}
calc();
document.getElementById('bf-share').addEventListener('click',function(){
  var txt='My estimated body fat: '+OUT.textContent+' (US Navy method). Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?s='+S.value+'&h='+encodeURIComponent(H.value||'')+'&n='+encodeURIComponent(N.value||'')+'&w='+encodeURIComponent(W.value||'')+(S.value==='f'?'&hp='+encodeURIComponent(HP.value||''):'')+'&kg='+encodeURIComponent(document.getElementById('bf-kg').value||'');
  if(navigator.share){navigator.share({title:'Body fat estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-estimate','Share my estimate');},1500);}
});
})();
</script>
"""

# Oven temperature converter: F, C and UK gas mark, with a full reference table.
# Retention hooks: title result hook, tt_oven input memory, URL state (?v=&u=), Web Share.
OVEN = """<div class="tool" id="tt-oven">
  <div class="fields">
    <div class="field"><label for="ov-u">Input unit</label><select id="ov-u"><option value="f">°Fahrenheit</option><option value="c">°Celsius</option><option value="g">Gas mark</option></select></div>
    <div class="field"><label for="ov-v">Oven temperature</label><input type="number" id="ov-v" step="any" placeholder="350"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ov-out">–</span><span class="result-unit" id="ov-unit"></span></div>
  <div id="ov-table"></div>
  <div class="tool-note">Recipes from the US use °F, Europe uses °C, and UK ovens use gas marks. Fan ovens run about 20°C hotter than the numbers here - subtract 20°C (or one gas mark equivalent) for fan-assisted settings.</div>
  <button type="button" class="tool-btn" id="ov-share" data-i18n="share.share-the-conversion">Share the conversion</button>
</div>
<script>(function(){
var U=document.getElementById('ov-u'),V=document.getElementById('ov-v');
var OUT=document.getElementById('ov-out'),UNIT=document.getElementById('ov-unit'),TB=document.getElementById('ov-table');
function qs(k){return new URLSearchParams(location.search).get(k);}
function toGas(c){var marks=[[125,1],[140,2],[150,2],[160,3],[170,3],[180,4],[190,5],[200,6],[210,6],[220,7],[230,8],[240,9],[250,10]];
  var best=marks[0][1],d=1e9;marks.forEach(function(m){var dd=Math.abs(m[0]-c);if(dd<d){d=dd;best=m[1];}});return best;}
function calc(){
  var v=parseFloat(V.value),u=U.value;
  if(isNaN(v)){OUT.textContent='–';UNIT.textContent='';TB.innerHTML='';document.title='Oven Temperature Converter - ToolTide';return;}
  var f=u==='f'?v:(u==='c'?v*9/5+32:0);
  if(u==='g'){f=250+25*v;}
  var c=(f-32)*5/9,g=Math.max(1,Math.min(10,toGas(c)));
  OUT.textContent=Math.round(c)+'°C / '+Math.round(f)+'°F';
  UNIT.textContent='gas mark '+g+' equivalent';
  var rows=[[275,135,1],[300,150,2],[325,165,3],[350,175,4],[375,190,5],[400,200,6],[425,220,7],[450,230,8],[475,245,9],[500,260,10]];
  var h='<table class="cp-t"><thead><tr><th>°F</th><th>°C</th><th>Gas</th><th>Typical use</th></tr></thead><tbody>';
  var uses=['Very low - meringues','Low - slow roasting','Low - drying','Moderate - casseroles','Moderate - cakes & cookies','Moderate hot - roasting veg','Hot - bread & scones','Hot - roasting meat','Very hot - pizza & pastry','Very hot - fast browning'];
  rows.forEach(function(r){h+='<tr><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+r[2]+'</td><td>'+uses[r[2]-1]+'</td></tr>';});
  TB.innerHTML=h+'</tbody></table>';
  document.title=Math.round(c)+'C oven - ToolTide';
}
function save(){try{localStorage.setItem('tt_oven',JSON.stringify({u:U.value,v:V.value}));}catch(e){}}
[U,V].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){V.placeholder=U.value==='f'?'350':(U.value==='c'?'175':'4');calc();save();});
var pre=false;
[['v',V],['u',U]].forEach(function(a){var x=qs(a[0]);if(x!==null){a[1].value=x;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_oven')||'null');if(mem){U.value=mem.u||'f';V.value=mem.v||'';}}catch(e){}}
calc();
document.getElementById('ov-share').addEventListener('click',function(){
  var txt='Oven setting: '+OUT.textContent+' ('+UNIT.textContent+'). Convert any recipe (no sign-up):';
  var url=location.origin+location.pathname+'?u='+U.value+'&v='+encodeURIComponent(V.value||'');
  if(navigator.share){navigator.share({title:'Oven temperature',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-conversion','Share the conversion');},1500);}
});
})();
</script>
"""

# Commission pay: base + rate x revenue, with quota-attainment context.
# Retention hooks: title result hook, tt_commission input memory, URL state (?b=&r=&rev=), Web Share.
COMMISSION = """<div class="tool" id="tt-cm">
  <div class="fields">
    <div class="field"><label for="cm-b">Base pay per period ($)</label><input type="number" id="cm-b" step="any" min="0" placeholder="2000"></div>
    <div class="field"><label for="cm-r">Commission rate %</label><input type="number" id="cm-r" step="any" min="0" max="100" placeholder="8"></div>
    <div class="field"><label for="cm-v">Revenue this period ($)</label><input type="number" id="cm-v" step="any" min="0" placeholder="45000"></div>
    <div class="field"><label for="cm-q">Quota ($, optional)</label><input type="number" id="cm-q" step="any" min="0" placeholder="40000"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cm-out">–</span><span class="result-unit">total pay this period</span></div>
  <div class="stats">
    <div class="stat"><b id="cm-comm">–</b><span>commission earned</span></div>
    <div class="stat"><b id="cm-att">–</b><span>quota attainment</span></div>
    <div class="stat"><b id="cm-mix">–</b><span>commission share of pay</span></div>
  </div>
  <div class="tool-note" id="cm-note"></div>
  <button type="button" class="tool-btn" id="cm-share" data-i18n="share.share-my-paycheck-math">Share my paycheck math</button>
</div>
<script>(function(){
var B=document.getElementById('cm-b'),R=document.getElementById('cm-r'),V=document.getElementById('cm-v'),Q=document.getElementById('cm-q');
var OUT=document.getElementById('cm-out');
function money(n){return '$'+Math.round(n).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var b=parseFloat(B.value)||0,r=(parseFloat(R.value)||0)/100,v=parseFloat(V.value)||0;
  if(!b&&!v){OUT.textContent='–';document.getElementById('cm-comm').textContent='–';
    document.getElementById('cm-att').textContent='–';document.getElementById('cm-mix').textContent='–';
    document.getElementById('cm-note').textContent='';document.title='Commission Calculator - ToolTide';return;}
  var comm=v*r,total=b+comm;
  OUT.textContent=money(total);
  document.getElementById('cm-comm').textContent=money(comm);
  var q=parseFloat(Q.value);
  document.getElementById('cm-att').textContent=(q>0)?Math.round(v/q*100)+'%':'—';
  document.getElementById('cm-mix').textContent=total>0?Math.round(comm/total*100)+'%':'—';
  var note='Base '+money(b)+' + '+Math.round(r*100)+'% of '+money(v)+' = '+money(total)+'.';
  if(q>0){
    if(v>=q){note+=' Quota cleared with '+money(v-q)+' to spare - accelerators past quota may lift the rate further.';}
    else{note+=' '+money(q-v)+' short of quota - each extra 10% of revenue adds '+money(q*0.1*r)+' at this rate.';}
  }
  document.getElementById('cm-note').textContent=note;
  document.title=money(total)+' paycheck - ToolTide';
}
function save(){try{localStorage.setItem('tt_commission',JSON.stringify({b:B.value,r:R.value,v:V.value,q:Q.value}));}catch(e){}}
[B,R,V,Q].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['b',B],['r',R],['rev',V],['q',Q]].forEach(function(a){var x=qs(a[0]);if(x!==null){a[1].value=x;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_commission')||'null');if(mem){B.value=mem.b||'';R.value=mem.r||'';V.value=mem.v||'';Q.value=mem.q||'';}}catch(e){}}
calc();
document.getElementById('cm-share').addEventListener('click',function(){
  var txt='My period pay: '+OUT.textContent+' ('+money(parseFloat(B.value)||0)+' base + '+money(parseFloat(V.value)||0)*(parseFloat(R.value)||0)/100+' commission). Run your numbers (no sign-up):';
  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value||'')+'&r='+encodeURIComponent(R.value||'')+'&rev='+encodeURIComponent(V.value||'')+'&q='+encodeURIComponent(Q.value||'');
  if(navigator.share){navigator.share({title:'Commission pay',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-paycheck-math','Share my paycheck math');},1500);}
});
})();
</script>
"""

# Air fryer conversion: conventional oven recipe -> fryer temp & time with a reference table.
# Retention hooks: title result hook, tt_airfryer input memory, URL state (?t=&m=&min=), Web Share.
AIRFRYER = """<div class="tool" id="tt-af">
  <div class="fields">
    <div class="field"><label for="af-u">Recipe units</label><select id="af-u"><option value="f">°F + minutes</option><option value="c">°C + minutes</option></select></div>
    <div class="field"><label for="af-t">Recipe oven temperature</label><input type="number" id="af-t" step="any" placeholder="400"></div>
    <div class="field"><label for="af-min">Recipe time (minutes)</label><input type="number" id="af-min" step="1" min="1" max="600" placeholder="25"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="af-out">–</span><span class="result-unit" id="af-unit"></span></div>
  <div class="stats">
    <div class="stat"><b id="af-tset">–</b><span>fryer temperature</span></div>
    <div class="stat"><b id="af-time">–</b><span>fryer time</span></div>
    <div class="stat"><b id="af-save">–</b><span>time saved</span></div>
  </div>
  <div class="tool-note">Air fryers are small convection ovens: drop the temperature by about 25°F (15°C), cut the time to roughly 80%, and check food early - the fan crisps fast in the last minutes. Shake or flip halfway for even browning, and don't crowd the basket.</div>
  <button type="button" class="tool-btn" id="af-share" data-i18n="share.share-the-setting">Share the setting</button>
</div>
<script>(function(){
var U=document.getElementById('af-u'),T=document.getElementById('af-t'),MI=document.getElementById('af-min');
var OUT=document.getElementById('af-out'),UNIT=document.getElementById('af-unit');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var t=parseFloat(T.value),m=parseFloat(MI.value),f=U.value==='f';
  if(isNaN(t)||!m||m<1){OUT.textContent='–';UNIT.textContent='';
    document.getElementById('af-tset').textContent='–';document.getElementById('af-time').textContent='–';
    document.getElementById('af-save').textContent='–';document.title='Air Fryer Converter - ToolTide';return;}
  var ft=f?t-25:(t-15),fm=Math.max(1,Math.round(m*0.8));
  OUT.textContent=Math.round(ft)+'°'+(f?'F':'C')+' · '+fm+' min';
  UNIT.textContent='air fryer setting';
  document.getElementById('af-tset').textContent=Math.round(ft)+'°'+(f?'F':'C');
  document.getElementById('af-time').textContent=fm+' min';
  document.getElementById('af-save').textContent=(m-fm)+' min';
  document.title='Air fryer '+Math.round(ft)+'°'+(f?'F':'C')+' '+fm+' min - ToolTide';
}
function save(){try{localStorage.setItem('tt_airfryer',JSON.stringify({u:U.value,t:T.value,m:MI.value}));}catch(e){}}
[U,T,MI].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){T.placeholder=U.value==='f'?'400':'200';calc();save();});
var pre=false;
[['t',T],['min',MI],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_airfryer')||'null');if(mem){U.value=mem.u||'f';T.value=mem.t||'';MI.value=mem.m||'';}}catch(e){}}
calc();
document.getElementById('af-share').addEventListener('click',function(){
  var txt='Air fryer version: '+OUT.textContent+' (recipe said '+T.value+'° for '+MI.value+' min). Convert yours (no sign-up):';
  var url=location.origin+location.pathname+'?t='+encodeURIComponent(T.value||'')+'&min='+encodeURIComponent(MI.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Air fryer setting',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-setting','Share the setting');},1500);}
});
})();
</script>
"""

# Fuel cost for a trip: distance + efficiency + price -> gallons/liters and cost.
# Retention hooks: title result hook, tt_fuelcost input memory, URL state (?d=&e=&p=&u=), Web Share.
FUELCOST = """<div class="tool" id="tt-fc">
  <div class="fields">
    <div class="field"><label for="fc-u"><span data-i18n="lbl.units">Units</span></label><select id="fc-u"><option value="us">Miles / MPG / $ per gallon</option><option value="eu">Kilometers / L per 100 km / $ per liter</option></select></div>
    <div class="field"><label for="fc-d">Trip distance</label><input type="number" id="fc-d" step="any" min="0" placeholder="480"></div>
    <div class="field"><label for="fc-e">Consumption</label><input type="number" id="fc-e" step="any" min="0" placeholder="30"></div>
    <div class="field"><label for="fc-p">Fuel price</label><input type="number" id="fc-p" step="any" min="0" placeholder="3.45"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fc-out">–</span><span class="result-unit" id="fc-unit"></span></div>
  <div class="stats">
    <div class="stat"><b id="fc-fuel">–</b><span>fuel needed</span></div>
    <div class="stat"><b id="fc-pp">–</b><span>per person, 4 riders</span></div>
    <div class="stat"><b id="fc-rt">–</b><span>round trip</span></div>
  </div>
  <div class="tool-note" id="fc-note"></div>
  <button type="button" class="tool-btn" id="fc-share" data-i18n="share.share-the-trip-cost">Share the trip cost</button>
</div>
<script>(function(){
var U=document.getElementById('fc-u'),D=document.getElementById('fc-d'),E=document.getElementById('fc-e'),P=document.getElementById('fc-p');
var OUT=document.getElementById('fc-out');
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var d=parseFloat(D.value)||0,e=parseFloat(E.value)||0,p=parseFloat(P.value)||0,us=U.value==='us';
  if(!d||!e||!p){OUT.textContent='–';document.getElementById('fc-fuel').textContent='–';
    document.getElementById('fc-pp').textContent='–';document.getElementById('fc-rt').textContent='–';
    document.getElementById('fc-note').textContent='';document.title='Fuel Cost Calculator - ToolTide';return;}
  var fuel,cost,unit;
  if(us){fuel=d/e;unit='gallons';}else{fuel=d*e/100;unit='liters';}
  cost=fuel*p;
  OUT.textContent=money(cost);
  document.getElementById('fc-unit').textContent='one-way fuel cost';
  document.getElementById('fc-fuel').textContent=(Math.round(fuel*100)/100)+' '+unit;
  document.getElementById('fc-pp').textContent=money(cost/4);
  document.getElementById('fc-rt').textContent=money(cost*2);
  document.getElementById('fc-note').textContent='Math: '+d+' '+(us?'miles ÷ ':'km ÷ ')+(us?e+' MPG':e+' L/100km')+' = '+
    (Math.round(fuel*100)/100)+' '+unit+' × '+money(p)+' = '+money(cost).slice(1)+
    '. Real-world driving (AC, hills, luggage) can add 10-15% - the round-trip line already doubles it for planning.';
  document.title=money(cost)+' fuel - ToolTide';
}
function save(){try{localStorage.setItem('tt_fuelcost',JSON.stringify({u:U.value,d:D.value,e:E.value,p:P.value}));}catch(e){}}
[U,D,E,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){E.placeholder=U.value==='us'?'30':'7.8';P.placeholder=U.value==='us'?'3.45':'1.65';calc();save();});
var pre=false;
[['d',D],['e',E],['p',P],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_fuelcost')||'null');if(mem){U.value=mem.u||'us';D.value=mem.d||'';E.value=mem.e||'';P.value=mem.p||'';}}catch(e){}}
calc();
document.getElementById('fc-share').addEventListener('click',function(){
  var txt='Trip fuel cost: '+D.value+' '+(U.value==='us'?'miles':'km')+' = '+OUT.textContent+
    ' one-way ('+document.getElementById('fc-fuel').textContent+'). Split yours (no sign-up):';
  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value||'')+'&e='+encodeURIComponent(E.value||'')+'&p='+encodeURIComponent(P.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Fuel cost',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-trip-cost','Share the trip cost');},1500);}
});
})();
</script>
"""

# Macro calculator: calories + split % -> grams of protein, carbs and fat.
# Retention hooks: title result hook, tt_macros input memory, URL state (?cal=&p=&c=&f=), Web Share.
MACROS = """<div class="tool" id="tt-mac">
  <div class="fields">
    <div class="field"><label for="mc-cal">Daily calories (kcal)</label><input type="number" id="mc-cal" step="any" min="0" placeholder="2400"></div>
    <div class="field"><label for="mc-goal">Goal preset</label>
      <select id="mc-goal">
        <option value="30,40,30">Balanced — 30p/40c/30f</option>
        <option value="40,35,25">High protein — 40p/35c/25f</option>
        <option value="25,45,30">Endurance — 25p/45c/30f</option>
        <option value="35,25,40">Low carb — 35p/25c/40f</option>
        <option value="custom">Custom…</option>
      </select></div>
  </div>
  <div class="fields">
    <div class="field"><label for="mc-p">Protein %</label><input type="number" id="mc-p" step="1" min="0" max="100" placeholder="30"></div>
    <div class="field"><label for="mc-c">Carbs %</label><input type="number" id="mc-c" step="1" min="0" max="100" placeholder="40"></div>
    <div class="field"><label for="mc-f">Fat %</label><input type="number" id="mc-f" step="1" min="0" max="100" placeholder="30"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="mc-out">–</span><span class="result-unit">g protein / carbs / fat per day</span></div>
  <div class="stats">
    <div class="stat"><b id="mc-pg">–</b><span>protein g</span></div>
    <div class="stat"><b id="mc-cg">–</b><span>carbs g</span></div>
    <div class="stat"><b id="mc-fg">–</b><span>fat g</span></div>
  </div>
  <div class="tool-note" id="mc-note"></div>
  <button type="button" class="tool-btn" id="mc-share" data-i18n="share.share-my-macros">Share my macros</button>
</div>
<script>(function(){
var CAL=document.getElementById('mc-cal'),GOAL=document.getElementById('mc-goal'),P=document.getElementById('mc-p'),C=document.getElementById('mc-c'),F=document.getElementById('mc-f');
var PGOAL=document.getElementById('mc-pg'),CGOAL=document.getElementById('mc-cg'),FGOAL=document.getElementById('mc-fg'),OUT=document.getElementById('mc-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var cal=parseFloat(CAL.value)||0;
  if(!cal){OUT.textContent='–';PGOAL.textContent=CGOAL.textContent=FGOAL.textContent='–';document.getElementById('mc-note').textContent='';document.title='Macro Calculator - ToolTide';return;}
  var pp=parseFloat(P.value)||0,cp=parseFloat(C.value)||0,fp=parseFloat(F.value)||0,sum=pp+cp+fp;
  document.getElementById('mc-note').textContent=sum===100?'Splits to 100% - good.':'Splits total '+sum+'% (should be 100%) - grams shown are still proportional.';
  var pg=cal*(pp/100)/4,cg=cal*(cp/100)/4,fg=cal*(fp/100)/9;
  OUT.textContent=Math.round(pg)+' / '+Math.round(cg)+' / '+Math.round(fg);
  PGOAL.textContent=Math.round(pg)+' g';CGOAL.textContent=Math.round(cg)+' g';FGOAL.textContent=Math.round(fg)+' g';
  document.title=Math.round(pg)+'P/'+Math.round(cg)+'C/'+Math.round(fg)+'F - ToolTide';
}
function save(){try{localStorage.setItem('tt_macros',JSON.stringify({c:CAL.value,g:GOAL.value,p:P.value,ca:C.value,f:F.value}));}catch(e){}}
GOAL.addEventListener('change',function(){
  if(GOAL.value!=='custom'){var v=GOAL.value.split(',');P.value=v[0];C.value=v[1];F.value=v[2];}
  calc();save();
});
[CAL,P,C,F].forEach(function(el){el.addEventListener('input',function(){
  var s=GOAL.value.split(',');if(P.value!==s[0]||C.value!==s[1]||F.value!==s[2])GOAL.value='custom';
  calc();save();
});});
var pre=false;
[['cal',CAL],['p',P],['c',C],['f',F]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(pre){GOAL.value='custom';}
else{try{var mem=JSON.parse(localStorage.getItem('tt_macros')||'null');if(mem){CAL.value=mem.c||'';GOAL.value=mem.g||'30,40,30';P.value=mem.p||'30';C.value=mem.ca||'40';F.value=mem.f||'30';}}catch(e){}}
calc();
document.getElementById('mc-share').addEventListener('click',function(){
  var txt='My macros at '+(parseFloat(CAL.value)||0)+' kcal: '+OUT.textContent+' g (P/C/F). Plan yours (no sign-up):';
  var url=location.origin+location.pathname+'?cal='+encodeURIComponent(CAL.value||'')+'&p='+encodeURIComponent(P.value||'')+'&c='+encodeURIComponent(C.value||'')+'&f='+encodeURIComponent(F.value||'');
  if(navigator.share){navigator.share({title:'Macro targets',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-macros','Share my macros');},1500);}
});
})();
</script>
"""

# Electricity cost: watts x hours x rate -> daily / monthly / yearly running cost.
# Retention hooks: title result hook, tt_electricity input memory, URL state (?w=&h=&r=), Web Share.
ELECTRIC = """<div class="tool" id="tt-el">
  <div class="fields">
    <div class="field"><label for="el-w">Power rating (watts)</label><input type="number" id="el-w" step="any" min="0" placeholder="1500"></div>
    <div class="field"><label for="el-h">Hours used per day</label><input type="number" id="el-h" step="any" min="0" max="24" placeholder="3"></div>
    <div class="field"><label for="el-r">Electricity rate ($/kWh)</label><input type="number" id="el-r" step="any" min="0" placeholder="0.17"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="el-out">–</span><span class="result-unit">per month</span></div>
  <div class="stats">
    <div class="stat"><b id="el-day">–</b><span>per day</span></div>
    <div class="stat"><b id="el-year">–</b><span>per year</span></div>
    <div class="stat"><b id="el-kwh">–</b><span>kWh per month</span></div>
  </div>
  <div class="tool-note" id="el-note"></div>
  <button type="button" class="tool-btn" id="el-share" data-i18n="share.share-this-cost">Share this cost</button>
</div>
<script>(function(){
var W=document.getElementById('el-w'),H=document.getElementById('el-h'),R=document.getElementById('el-r');
var OUT=document.getElementById('el-out');
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(W.value)||0,h=parseFloat(H.value)||0,r=parseFloat(R.value)||0;
  if(!w||!h||!r){OUT.textContent='–';document.getElementById('el-day').textContent='–';
    document.getElementById('el-year').textContent='–';document.getElementById('el-kwh').textContent='–';
    document.getElementById('el-note').textContent='';document.title='Electricity Cost Calculator - ToolTide';return;}
  var kwhDay=w*h/1000,day=kwhDay*r,mon=day*30.4,year=day*365;
  OUT.textContent=money(mon);
  document.getElementById('el-day').textContent=money(day);
  document.getElementById('el-year').textContent=money(year);
  document.getElementById('el-kwh').textContent=Math.round(kwhDay*30.4).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('el-note').textContent='Math: '+w+' W × '+h+' h = '+(Math.round(kwhDay*100)/100)+' kWh/day, × your $'+r.toFixed(2)+'/kWh. Standby power typically adds 1-2 W around the clock - devices left plugged in cost a few dollars a year each.';
  document.title=money(mon)+'/mo to run - ToolTide';
}
function save(){try{localStorage.setItem('tt_electricity',JSON.stringify({w:W.value,h:H.value,r:R.value}));}catch(e){}}
[W,H,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['w',W],['h',H],['r',R]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_electricity')||'null');if(mem){W.value=mem.w||'';H.value=mem.h||'';R.value=mem.r||'';}}catch(e){}}
calc();
document.getElementById('el-share').addEventListener('click',function(){
  var txt='Running my '+W.value+' W device '+H.value+' h/day costs '+OUT.textContent+'/month ('+document.getElementById('el-year').textContent+'/year). Check yours (no sign-up):';
  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value||'')+'&h='+encodeURIComponent(H.value||'')+'&r='+encodeURIComponent(R.value||'');
  if(navigator.share){navigator.share({title:'Electricity cost',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-cost','Share this cost');},1500);}
});
})();
</script>
"""

# Wind chill (NOAA): how cold it feels on exposed skin, with frostbite time estimates.
# Retention hooks: title result hook, tt_windchill input memory, URL state (?t=&v=&u=), Web Share.
WINDCHILL = """<div class="tool" id="tt-wc">
  <div class="fields">
    <div class="field"><label for="wc-u"><span data-i18n="lbl.units">Units</span></label><select id="wc-u"><option value="f">°F, mph</option><option value="c">°C, km/h</option></select></div>
    <div class="field"><label for="wc-t"><span data-i18n="lbl.airtemp">Air temperature</span></label><input type="number" id="wc-t" step="any" placeholder="20"></div>
    <div class="field"><label for="wc-v">Wind speed</label><input type="number" id="wc-v" step="any" min="0" placeholder="20"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wc-out">–</span><span class="result-unit" id="wc-unit">feels like on exposed skin</span></div>
  <div class="stats">
    <div class="stat"><b id="wc-frost">–</b><span>frostbite time</span></div>
    <div class="stat"><b id="wc-delta">–</b><span>added by wind</span></div>
  </div>
  <div class="tool-note" id="wc-note"></div>
  <button type="button" class="tool-btn" id="wc-share" data-i18n="share.share-the-feels-like">Share the feels-like</button>
</div>
<script>(function(){
var U=document.getElementById('wc-u'),T=document.getElementById('wc-t'),V=document.getElementById('wc-v');
var OUT=document.getElementById('wc-out'),UNIT=document.getElementById('wc-unit');
function qs(k){return new URLSearchParams(location.search).get(k);}
function fc(c){return Math.round(c*9/5+32);}
function calc(){
  var tv=parseFloat(T.value),v=parseFloat(V.value)||0,imp=U.value==='f';
  if(isNaN(tv)){OUT.textContent='–';document.getElementById('wc-frost').textContent='–';
    document.getElementById('wc-delta').textContent='–';document.getElementById('wc-note').textContent='';
    document.title='Wind Chill Calculator - ToolTide';return;}
  var tf=imp?tv:fc(tv),vmp=imp?v:v*0.621371;
  var wc,note='';
  if(tf>50||vmp<3){wc=tf;
    note='The wind chill formula is defined for 50°F (10°C) and below with wind above 3 mph - outside that range, the air temperature itself is the standard figure.';
    document.getElementById('wc-frost').textContent='—';
    document.getElementById('wc-delta').textContent='—';
  }else{
    var vp=Math.pow(vmp,0.16);
    wc=35.74+0.6215*tf-35.75*vp+0.4275*tf*vp;
    var frost='—';
    if(wc<=-19)frost='30 minutes';
    if(wc<=-32)frost='10 minutes';
    if(wc<=-48)frost='5 minutes';
    document.getElementById('wc-frost').textContent=frost;
    document.getElementById('wc-delta').textContent='-'+Math.round(Math.abs(wc-tf))+'°';
    note='Exposed skin freezes faster as wind strips away the warm air layer: watch for numbness or white patches at this level. The figure assumes shade at night, per NOAA.';
  }
  var out=imp?Math.round(wc):Math.round((wc-32)*5/9*10)/10;
  OUT.textContent=out+'°'+(imp?'F':'C');
  document.getElementById('wc-note').textContent=note;
  UNIT.textContent='feels like on exposed skin';
  document.title='Feels like '+out+'°'+(imp?'F':'C')+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_windchill',JSON.stringify({t:T.value,v:V.value,u:U.value}));}catch(e){}}
[U,T,V].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){calc();save();});
var pre=false;
[['t',T],['v',V],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_windchill')||'null');if(mem){T.value=mem.t||'';V.value=mem.v||'';U.value=mem.u||'f';}}catch(e){}}
calc();
document.getElementById('wc-share').addEventListener('click',function(){
  var txt='It is '+T.value+'°'+(U.value==='f'?'F':'C')+' with '+V.value+' '+(U.value==='f'?'mph':'km/h')+' wind - feels like '+OUT.textContent+'. Check yours (no sign-up):';
  var url=location.origin+location.pathname+'?t='+encodeURIComponent(T.value||'')+'&v='+encodeURIComponent(V.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Wind chill',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-feels-like','Share the feels-like');},1500);}
});
})();
</script>
"""

# Running pace: distance + time -> pace per km and per mile, with same-pace race predictions.
# Retention hooks: title result hook, tt_pace input memory, URL state (?d=&h=&m=&s=&u=), Web Share.
PACE = """<div class="tool" id="tt-pace">
  <div class="fields">
    <div class="field"><label for="pa-u">Distance unit</label><select id="pa-u"><option value="km">Kilometers</option><option value="mi">Miles</option></select></div>
    <div class="field"><label for="pa-d"><span data-i18n="lbl.distance">Distance</span></label><input type="number" id="pa-d" step="any" min="0" placeholder="10"></div>
  </div>
  <div class="fields">
    <div class="field"><label for="pa-h">Hours</label><input type="number" id="pa-h" step="1" min="0" max="30" placeholder="0"></div>
    <div class="field"><label for="pa-m"><span data-i18n="lbl.minutes">Minutes</span></label><input type="number" id="pa-m" step="1" min="0" max="59" placeholder="52"></div>
    <div class="field"><label for="pa-s"><span data-i18n="lbl.seconds">Seconds</span></label><input type="number" id="pa-s" step="1" min="0" max="59" placeholder="30"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pa-out">–</span><span class="result-unit" id="pa-unit">/km</span></div>
  <div class="stats">
    <div class="stat"><b id="pa-mpm">–</b><span>per mile</span></div>
    <div class="stat"><b id="pa-kmh">–</b><span>speed km/h</span></div>
    <div class="stat"><b id="pa-mph">–</b><span>speed mph</span></div>
  </div>
  <div class="tool-note" id="pa-note"></div>
  <button type="button" class="tool-btn" id="pa-share" data-i18n="share.share-my-pace">Share my pace</button>
</div>
<script>(function(){
var U=document.getElementById('pa-u'),D=document.getElementById('pa-d'),H=document.getElementById('pa-h'),M=document.getElementById('pa-m'),S=document.getElementById('pa-s');
var OUT=document.getElementById('pa-out'),UNIT=document.getElementById('pa-unit');
function qs(k){return new URLSearchParams(location.search).get(k);}
function pfmt(secPerUnit){if(!isFinite(secPerUnit)||secPerUnit<=0)return '–';var m=Math.floor(secPerUnit/60),s=Math.round(secPerUnit%60);if(s===60){m++;s=0;}return m+':'+(s<10?'0':'')+s;}
function calc(){
  var d=parseFloat(D.value)||0,sec=(parseFloat(H.value)||0)*3600+(parseFloat(M.value)||0)*60+(parseFloat(S.value)||0);
  if(!d||!sec){OUT.textContent='–';document.getElementById('pa-mpm').textContent='–';
    document.getElementById('pa-kmh').textContent='–';document.getElementById('pa-mph').textContent='–';
    document.getElementById('pa-note').textContent='';document.title='Running Pace Calculator - ToolTide';return;}
  var dkm=U.value==='km'?d:d*1.609344;
  var perKm=sec/dkm,perMi=perKm*1.609344;
  OUT.textContent=pfmt(U.value==='km'?perKm:perMi);
  UNIT.textContent=U.value==='km'?'/km':'/mile';
  document.getElementById('pa-mpm').textContent=pfmt(perMi);
  document.getElementById('pa-kmh').textContent=(3600/perKm).toFixed(2);
  document.getElementById('pa-mph').textContent=(3600/perMi).toFixed(2);
  var races=[['5K',5],['10K',10],['Half',21.0975],['Marathon',42.195]],h='<div class="stats">';
  races.forEach(function(r){h+='<div class="stat"><b>'+pfmt(perKm*r[1])+'</b><span>'+r[0]+' at this pace</span></div>';});
  document.getElementById('pa-note').innerHTML=h+'</div>';
  document.title='Pace '+pfmt(U.value==='km'?perKm:perMi)+' '+UNIT.textContent+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_pace',JSON.stringify({u:U.value,d:D.value,h:H.value,m:M.value,s:S.value}));}catch(e){}}
[U,D,H,M,S].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){calc();save();});
var pre=false;
[['d',D],['h',H],['m',M],['s',S],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_pace')||'null');if(mem){U.value=mem.u||'km';D.value=mem.d||'';H.value=mem.h||'';M.value=mem.m||'';S.value=mem.s||'';}}catch(e){}}
calc();
document.getElementById('pa-share').addEventListener('click',function(){
  var txt='Ran '+D.value+' '+U.value+' in '+(parseFloat(H.value)||0)+'h '+(parseFloat(M.value)||0)+'m '+(parseFloat(S.value)||0)+
    's - that is '+OUT.textContent+UNIT.textContent+'. Calculate your pace (no sign-up):';
  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value||'')+'&h='+encodeURIComponent(H.value||'')+'&m='+encodeURIComponent(M.value||'')+'&s='+encodeURIComponent(S.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Running pace',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-pace','Share my pace');},1500);}
});
})();
</script>
"""

# Heat index (NOAA Rothfusz): "feels like" in shade with official risk bands.
# Retention hooks: title result hook, tt_heatindex input memory, URL state (?t=&rh=&u=), Web Share.
HEATINDEX = """<div class="tool" id="tt-hi">
  <div class="fields">
    <div class="field"><label for="hi-u"><span data-i18n="lbl.units">Units</span></label><select id="hi-u"><option value="f">°F</option><option value="c">°C</option></select></div>
    <div class="field"><label for="hi-t"><span data-i18n="lbl.airtemp">Air temperature</span></label><input type="number" id="hi-t" step="any" placeholder="95"></div>
    <div class="field"><label for="hi-rh"><span data-i18n="lbl.relhum">Relative humidity %</span></label><input type="number" id="hi-rh" step="any" min="0" max="100" placeholder="60"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hi-out">–</span><span class="result-unit" id="hi-unit">feels like (in shade)</span></div>
  <div class="stats">
    <div class="stat"><b id="hi-band">–</b><span>risk band</span></div>
    <div class="stat"><b id="hi-delta">–</b><span>added by humidity</span></div>
  </div>
  <div class="tool-note" id="hi-note"></div>
  <button type="button" class="tool-btn" id="hi-share" data-i18n="share.share-the-feels-like">Share the feels-like</button>
</div>
<script>(function(){
var U=document.getElementById('hi-u'),T=document.getElementById('hi-t'),RH=document.getElementById('hi-rh');
var OUT=document.getElementById('hi-out'),UNIT=document.getElementById('hi-unit');
function qs(k){return new URLSearchParams(location.search).get(k);}
function cf(f){return Math.round((f-32)*5/9*10)/10;}
function calc(){
  var tv=parseFloat(T.value),rh=parseFloat(RH.value)||0,f=U.value==='f';
  if(isNaN(tv)){OUT.textContent='–';document.getElementById('hi-band').textContent='–';
    document.getElementById('hi-delta').textContent='–';document.getElementById('hi-note').textContent='';
    document.title='Heat Index Calculator - ToolTide';return;}
  var tf=f?tv:tv*9/5+32;
  if(tf<80){var d=0;OUT.textContent=(f?tv:tv)+'°'+U.value.toUpperCase();
    UNIT.textContent='feels like (humidity effect negligible below 80°F)';document.getElementById('hi-band').textContent='—';
    document.getElementById('hi-delta').textContent='+0°';document.getElementById('hi-note').textContent='The heat index is defined for 80°F (27°C) and above — below that, air temperature alone is the standard "feels like" figure.';return;}
  var T2=tf*tf,R2=rh*rh,TR=tf*rh;
  var hi=-42.379+2.04901523*tf+10.14333127*rh-0.22475541*TR-0.00683783*T2*rh-0.05481717*R2+0.00122874*T2*R2+0.00085282*tf*R2-0.00000199*T2*R2;
  if(rh<13&&tf>=80&&tf<=112)hi-=((13-rh)/4)*Math.sqrt(Math.abs(17-Math.abs(tf-95))/17);
  if(rh>85&&tf>=80&&tf<=87)hi+=((rh-85)/10)*((87-tf)/5);
  var band='Caution (80-90°F): fatigue possible with prolonged exposure',cls='#f59e0b';
  if(hi>=125){band='Extreme danger (125°F+): heat stroke imminent';cls='#dc2626';}
  else if(hi>=103){band='Danger (103-124°F): heat cramps or heat stroke likely';cls='#dc2626';}
  else if(hi>=90){band='Extreme caution (90-102°F): heat stroke possible';cls='#ea580c';}
  OUT.textContent=(f?Math.round(hi*10)/10:cf(hi))+'°'+U.value.toUpperCase();
  document.getElementById('hi-band').textContent=band;
  document.getElementById('hi-delta').textContent='+'+(f?Math.round((hi-tf)*10)/10:cf(hi-tf))+'°';
  document.getElementById('hi-note').textContent='NOAA Rothfusz regression in shade with light wind. Direct sun can add up to 15°F (8°C) - and the band guidance means hydration, shade and midday effort cuts.';
  UNIT.textContent='feels like (in shade)';
  document.title='Feels like '+(f?Math.round(hi):cf(hi))+'°'+U.value.toUpperCase()+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_heatindex',JSON.stringify({t:T.value,r:RH.value,u:U.value}));}catch(e){}}
[U,T,RH].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){calc();save();});
var pre=false;
[['t',T],['rh',RH],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_heatindex')||'null');if(mem){T.value=mem.t||'';RH.value=mem.r||'';U.value=mem.u||'f';}}catch(e){}}
calc();
document.getElementById('hi-share').addEventListener('click',function(){
  var txt='It is '+T.value+'°'+U.value.toUpperCase()+' at '+RH.value+'% humidity - feels like '+OUT.textContent+' ('+document.getElementById('hi-band').textContent.split(':')[0].toLowerCase()+'). Check yours (no sign-up):';
  var url=location.origin+location.pathname+'?t='+encodeURIComponent(T.value||'')+'&rh='+encodeURIComponent(RH.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Heat index',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-feels-like','Share the feels-like');},1500);}
});
})();
</script>
"""

# BMI: metric & imperial, WHO categories and the healthy weight window for your height.
# Retention hooks: title result hook, tt_bmi input memory, URL state (?u=&h=&w=), Web Share.
BMI = """<div class="tool" id="tt-bmi">
  <div class="fields">
    <div class="field"><label for="bmi-u"><span data-i18n="lbl.units">Units</span></label><select id="bmi-u"><option value="m">Metric (cm, kg)</option><option value="i">Imperial (in, lb)</option></select></div>
    <div class="field"><label for="bmi-h"><span data-i18n="lbl.height">Height</span></label><input type="number" id="bmi-h" step="any" min="50" placeholder="175"></div>
    <div class="field"><label for="bmi-w"><span data-i18n="lbl.weight">Weight</span></label><input type="number" id="bmi-w" step="any" min="10" placeholder="70"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bmi-out">–</span><span class="result-unit" id="bmi-unit">BMI</span></div>
  <div class="stats">
    <div class="stat"><b id="bmi-cat">–</b><span data-i18n="bmi.cat">WHO category</span></div>
    <div class="stat"><b id="bmi-lo">–</b><span data-i18n="bmi.lo">healthy low</span></div>
    <div class="stat"><b id="bmi-hi">–</b><span data-i18n="bmi.hi">healthy high</span></div>
  </div>
  <div class="tool-note">BMI = weight ÷ height². It is a population screening tool, not a diagnosis - muscle, age and frame all shift what a healthy number looks like for you individually.</div>
  <button type="button" class="tool-btn" id="bmi-share" data-i18n="share.share-my-bmi">Share my BMI</button>
</div>
<script>(function(){
var U=document.getElementById('bmi-u'),H=document.getElementById('bmi-h'),W=document.getElementById('bmi-w');
var OUT=document.getElementById('bmi-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var h=parseFloat(H.value),w=parseFloat(W.value),imp=U.value==='i';
  if(!h||!w){OUT.textContent='–';document.getElementById('bmi-cat').textContent='–';
    document.getElementById('bmi-lo').textContent='–';document.getElementById('bmi-hi').textContent='–';
    document.title='BMI Calculator - ToolTide';return;}
  var bmi=imp?703*w/(h*h):w/((h/100)*(h/100)),u2=imp?'lb':'kg';
  var cat=TT('bmi.v.o1','Obese (Class I) - BMI 30-34.9');
  if(bmi<18.5)cat=TT('bmi.v.uw','Underweight - BMI below 18.5');
  else if(bmi<25)cat=TT('bmi.v.hw','Healthy weight - BMI 18.5-24.9');
  else if(bmi<30)cat=TT('bmi.v.ow','Overweight - BMI 25-29.9');
  else if(bmi<35)cat=TT('bmi.v.o1','Obese (Class I) - BMI 30-34.9');
  else if(bmi<40)cat=TT('bmi.v.o2','Obese (Class II) - BMI 35-39.9');
  else cat=TT('bmi.v.o3','Obese (Class III) - BMI 40+');
  document.getElementById('bmi-cat').textContent=cat;
  OUT.textContent=Math.round(bmi*10)/10;
  document.getElementById('bmi-lo').textContent=Math.round(18.5*(imp?(h/39.37)*(h/39.37):(h/100)*(h/100)))+' '+u2;
  document.getElementById('bmi-hi').textContent=Math.round(24.9*(imp?(h/39.37)*(h/39.37):(h/100)*(h/100)))+' '+u2;
  document.title='BMI '+Math.round(bmi*10)/10+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_bmi',JSON.stringify({u:U.value,h:H.value,w:W.value}));}catch(e){}}
[U,H,W].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){H.placeholder=U.value==='i'?'69':'175';W.placeholder=U.value==='i'?'160':'70';calc();save();});
var pre=false;
[['u',U],['h',H],['w',W]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_bmi')||'null');if(mem){U.value=mem.u||'m';H.value=mem.h||'';W.value=mem.w||'';}}catch(e){}}
calc();
window.addEventListener('load',calc);
document.getElementById('bmi-share').addEventListener('click',function(){
  var txt='My BMI: '+OUT.textContent+' ('+document.getElementById('bmi-cat').textContent.split(' - ')[0].toLowerCase()+'). Check yours (no sign-up):';
  var url=location.origin+location.pathname+'?u='+U.value+'&h='+encodeURIComponent(H.value||'')+'&w='+encodeURIComponent(W.value||'');
  if(navigator.share){navigator.share({title:'BMI result',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-bmi','Share my BMI');},1500);}
});
})();
</script>
"""

# TDEE calculator: Mifflin-St Jeor BMR x activity multiplier, with cut/bulk reference lines.
# Retention hooks: title result hook, tt_tdee input memory, URL state (?s=&a=&h=&w=&act=), Web Share.
TDEE = """<div class="tool" id="tt-tdee">
  <div class="fields">
    <div class="field"><label for="td-sex"><span data-i18n="lbl.sex">Sex</span></label><select id="td-sex"><option value="m">Male</option><option value="f">Female</option></select></div>
    <div class="field"><label for="td-age"><span data-i18n="lbl.age">Age</span></label><input type="number" id="td-age" min="10" max="100" step="1" placeholder="30"></div>
  </div>
  <div class="fields">
    <div class="field"><label for="td-h">Height (cm)</label><input type="number" id="td-h" min="100" max="230" step="any" placeholder="175"></div>
    <div class="field"><label for="td-w">Weight (kg)</label><input type="number" id="td-w" min="30" max="300" step="any" placeholder="75"></div>
  </div>
  <div class="field"><label for="td-act">Activity level</label>
    <select id="td-act">
      <option value="1.2">Sedentary — desk job, little exercise</option>
      <option value="1.375">Light — 1-3 workouts a week</option>
      <option value="1.55" selected>Moderate — 3-5 workouts a week</option>
      <option value="1.725">Very active — 6-7 workouts a week</option>
      <option value="1.9">Athlete — twice-daily training or physical job</option>
    </select></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="td-out">–</span><span class="result-unit">kcal / day to maintain weight (TDEE)</span></div>
  <div class="stats">
    <div class="stat"><b id="td-bmr">–</b><span>BMR at rest</span></div>
    <div class="stat"><b id="td-loss">–</b><span>steady loss (−500)</span></div>
    <div class="stat"><b id="td-gain">–</b><span>lean gain (+300)</span></div>
  </div>
  <div class="tool-note">Mifflin-St Jeor equation × activity multiplier — the same method most dietitians start from. Treat every figure as a starting estimate: track real weight change for two weeks and adjust by 100-200 kcal rather than trusting any formula blindly.</div>
  <button type="button" class="tool-btn" id="td-share" data-i18n="share.share-my-tdee">Share my TDEE</button>
</div>
<script>(function(){
var S=document.getElementById('td-sex'),A=document.getElementById('td-age'),H=document.getElementById('td-h'),W=document.getElementById('td-w'),ACT=document.getElementById('td-act');
var OUT=document.getElementById('td-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),h=parseFloat(H.value),w=parseFloat(W.value),m=parseFloat(ACT.value);
  if(!a||!h||!w){OUT.textContent='–';document.getElementById('td-bmr').textContent='–';
    document.getElementById('td-loss').textContent='–';document.getElementById('td-gain').textContent='–';
    document.title='TDEE Calculator - ToolTide';return;}
  var bmr=10*w+6.25*h-5*a+(S.value==='m'?5:-161),tdee=bmr*m;
  OUT.textContent=Math.round(tdee).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('td-bmr').textContent=Math.round(bmr).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('td-loss').textContent=Math.round(tdee-500).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('td-gain').textContent=Math.round(tdee+300).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.title=Math.round(tdee).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' kcal TDEE - ToolTide';
}
function save(){try{localStorage.setItem('tt_tdee',JSON.stringify({s:S.value,a:A.value,h:H.value,w:W.value,act:ACT.value}));}catch(e){}}
[S,A,H,W,ACT].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['s',S],['a',A],['h',H],['w',W],['act',ACT]].forEach(function(p){var v=qs(p[0]);if(v!==null){p[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_tdee')||'null');if(mem){S.value=mem.s||'m';A.value=mem.a||'';H.value=mem.h||'';W.value=mem.w||'';ACT.value=mem.act||'1.55';}}catch(e){}}
calc();
document.getElementById('td-share').addEventListener('click',function(){
  var txt='My maintenance calories (TDEE): '+OUT.textContent+' kcal/day. Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?s='+S.value+'&a='+encodeURIComponent(A.value||'')+'&h='+encodeURIComponent(H.value||'')+'&w='+encodeURIComponent(W.value||'')+'&act='+ACT.value;
  if(navigator.share){navigator.share({title:'TDEE estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-tdee','Share my TDEE');},1500);}
});
})();
</script>
"""

# Tip split: bill + tip % + people -> fair per-person share with a round-up option.
# Retention hooks: title result hook, tt_tipsplit input memory, URL state (?b=&p=&n=&r=), Web Share.
TIPSPLIT = """<div class="tool" id="tt-ts">
  <div class="fields">
    <div class="field"><label for="ts-bill">Bill total ($)</label><input type="number" id="ts-bill" step="0.01" min="0" placeholder="184.50"></div>
    <div class="field"><label for="ts-tip">Tip %</label><input type="number" id="ts-tip" step="any" min="0" max="100" placeholder="18"></div>
    <div class="field"><label for="ts-people">People</label><input type="number" id="ts-people" step="1" min="1" placeholder="4"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ts-out">–</span><span class="result-unit">per person (with tip)</span></div>
  <div class="stats">
    <div class="stat"><b id="ts-tipamt">–</b><span>tip total</span></div>
    <div class="stat"><b id="ts-grand">–</b><span>grand total</span></div>
    <div class="stat"><b id="ts-round">–</b><span>if each rounds up</span></div>
  </div>
  <div class="tool-note" id="ts-note"></div>
  <button type="button" class="tool-btn" id="ts-share" data-i18n="share.share-the-split">Share the split</button>
</div>
<script>(function(){
var B=document.getElementById('ts-bill'),P=document.getElementById('ts-tip'),N=document.getElementById('ts-people');
var OUT=document.getElementById('ts-out');
function money(n){return '$'+n.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var b=parseFloat(B.value)||0,p=parseFloat(P.value)||0,n=Math.max(1,Math.round(parseFloat(N.value)||1));
  if(!b){OUT.textContent='–';document.getElementById('ts-tipamt').textContent='–';
    document.getElementById('ts-grand').textContent='–';document.getElementById('ts-round').textContent='–';
    document.getElementById('ts-note').textContent='';document.title='Tip Split Calculator - ToolTide';return;}
  var tip=b*p/100,grand=b+tip,per=grand/n;
  OUT.textContent=money(per);
  document.getElementById('ts-tipamt').textContent=money(tip);
  document.getElementById('ts-grand').textContent=money(grand);
  var ru=Math.ceil(per);
  document.getElementById('ts-round').textContent=money(ru);
  document.getElementById('ts-note').textContent=n+' people × '+money(ru)+' = '+money(ru*n)+' collected - the extra '+(ru*n>=grand?money(ru*n-grand):'$0.00')+' becomes a fatter tip. One person paying? The grand total is '+money(grand)+'.';
  document.title=money(per)+' each - ToolTide';
}
function save(){try{localStorage.setItem('tt_tipsplit',JSON.stringify({b:B.value,p:P.value,n:N.value}));}catch(e){}}
[B,P,N].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['b',B],['p',P],['n',N]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_tipsplit')||'null');if(mem){B.value=mem.b||'';P.value=mem.p||'';N.value=mem.n||'';}}catch(e){}}
calc();
document.getElementById('ts-share').addEventListener('click',function(){
  var txt='Dinner split: '+money(parseFloat(B.value)||0)+' + '+(parseFloat(P.value)||0)+'% tip across '+(Math.round(parseFloat(N.value)||1))+
    ' people = '+OUT.textContent+' each. Split yours (no sign-up):';
  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value||'')+'&p='+encodeURIComponent(P.value||'')+'&n='+encodeURIComponent(N.value||'');
  if(navigator.share){navigator.share({title:'Tip split',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-split','Share the split');},1500);}
});
})();
</script>
"""

# Final grade calculator: what score the final requires, with 100/80/60 scenario previews.
# Retention hooks: title result hook, tt_finalgrade input memory, URL state (?cur=&w=&tgt=), Web Share.
FINALGRADE = """<div class="tool" id="tt-fg">
  <div class="fields">
    <div class="field"><label for="fg-cur">Current grade %</label><input type="number" id="fg-cur" step="any" min="0" max="100" placeholder="78"></div>
    <div class="field"><label for="fg-w">Final exam worth %</label><input type="number" id="fg-w" step="any" min="0" max="100" placeholder="30"></div>
    <div class="field"><label for="fg-tgt">Target course grade %</label><input type="number" id="fg-tgt" step="any" min="0" max="100" placeholder="80"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fg-out">–</span><span class="result-unit" id="fg-unit">needed on the final</span></div>
  <div class="tool-note" id="fg-note"></div>
  <div class="stats">
    <div class="stat"><b id="fg-s100">–</b><span>if you score 100%</span></div>
    <div class="stat"><b id="fg-s80">–</b><span>if you score 80%</span></div>
    <div class="stat"><b id="fg-s60">–</b><span>if you score 60%</span></div>
  </div>
  <button type="button" class="tool-btn" id="fg-share" data-i18n="share.share-my-plan">Share my plan</button>
</div>
<script>(function(){
var C=document.getElementById('fg-cur'),W=document.getElementById('fg-w'),G=document.getElementById('fg-tgt');
var OUT=document.getElementById('fg-out'),UNIT=document.getElementById('fg-unit'),NOTE=document.getElementById('fg-note');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var c=parseFloat(C.value),w=(parseFloat(W.value)||0)/100,t=parseFloat(G.value);
  var s100=document.getElementById('fg-s100'),s80=document.getElementById('fg-s80'),s60=document.getElementById('fg-s60');
  if(isNaN(c)||isNaN(t)||w<=0||w>1){OUT.textContent='–';UNIT.textContent='needed on the final';NOTE.textContent='';s100.textContent=s80.textContent=s60.textContent='–';document.title='Final Grade Calculator - ToolTide';return;}
  var need=(t-c*(1-w))/w,fin=function(x){return (c*(1-w)+x*w).toFixed(1)+'%';};
  OUT.textContent=Math.ceil(need*10)/10+'%';
  NOTE.textContent='Formula: need = (target − current × (1 − '+Math.round(w*100)+'%)) ÷ '+Math.round(w*100)+'% = ( '+t+' − '+c+' × '+(1-w).toFixed(2)+' ) ÷ '+w.toFixed(2)+'.';
  if(need>100){UNIT.textContent='not reachable - max course grade:';OUT.textContent=fin(100);}
  else if(need<=0){UNIT.textContent='already secured even at 0% on the final:';OUT.textContent=fin(0);}
  else{UNIT.textContent='needed on the final';}
  s100.textContent=fin(100);s80.textContent=fin(80);s60.textContent=fin(60);
  document.title='Need '+OUT.textContent+' on final - ToolTide';
}
function save(){try{localStorage.setItem('tt_finalgrade',JSON.stringify({c:C.value,w:W.value,t:G.value}));}catch(e){}}
[C,W,G].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['cur',C],['w',W],['tgt',G]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_finalgrade')||'null');if(mem){C.value=mem.c||'';W.value=mem.w||'';G.value=mem.t||'';}}catch(e){}}
calc();
document.getElementById('fg-share').addEventListener('click',function(){
  var txt='To end '+document.getElementById('fg-tgt').value+'% in the course I need '+OUT.textContent+' on the final. Plan yours (no sign-up):';
  var url=location.origin+location.pathname+'?cur='+encodeURIComponent(C.value||'')+'&w='+encodeURIComponent(W.value||'')+'&tgt='+encodeURIComponent(G.value||'');
  if(navigator.share){navigator.share({title:'Final grade plan',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-plan','Share my plan');},1500);}
});
})();
</script>
"""

# Daily water intake: weight-based baseline + exercise and heat adjustments, in bottles and cups.
# Retention hooks: title result hook, tt_water input memory, URL state (?kg=&ex=&hot=), Web Share.
WATER = """<div class="tool" id="tt-water">
  <div class="fields">
    <div class="field"><label for="wt-kg"><span data-i18n="lbl.bodyweight">Body weight (kg)</span></label><input type="number" id="wt-kg" step="any" min="20" max="300" placeholder="70"></div>
    <div class="field"><label for="wt-ex">Exercise today (minutes)</label><input type="number" id="wt-ex" step="any" min="0" placeholder="45"></div>
    <div class="field"><label for="wt-hot">Hot weather (over 30°C / 86°F)</label>
      <select id="wt-hot"><option value="0">No</option><option value="1">Yes</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wt-out">–</span><span class="result-unit">liters per day</span></div>
  <div class="stats">
    <div class="stat"><b id="wt-base">–</b><span>baseline from weight</span></div>
    <div class="stat"><b id="wt-exadd">–</b><span>exercise bonus</span></div>
    <div class="stat"><b id="wt-bottles">–</b><span>500 ml bottles</span></div>
    <div class="stat"><b id="wt-cups">–</b><span>8 oz cups</span></div>
  </div>
  <div class="tool-note" id="wt-note"></div>
  <button type="button" class="tool-btn" id="wt-share" data-i18n="share.share-my-target">Share my target</button>
</div>
<script>(function(){
var KG=document.getElementById('wt-kg'),EX=document.getElementById('wt-ex'),HOT=document.getElementById('wt-hot');
var OUT=document.getElementById('wt-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var kg=parseFloat(KG.value)||0,ex=parseFloat(EX.value)||0,hot=HOT.value==='1';
  if(kg<=0){OUT.textContent='–';document.getElementById('wt-base').textContent='–';
    document.getElementById('wt-exadd').textContent='–';document.getElementById('wt-bottles').textContent='–';
    document.getElementById('wt-cups').textContent='–';document.getElementById('wt-note').textContent='';
    document.title='Water Intake Calculator - ToolTide';return;}
  var base=kg*33/1000,exadd=Math.round(ex/30*400)/1000,hotadd=hot?0.5:0,total=base+exadd+hotadd;
  OUT.textContent=(Math.round(total*10)/10).toFixed(1);
  document.getElementById('wt-base').textContent=(Math.round(base*10)/10).toFixed(1)+' L';
  document.getElementById('wt-exadd').textContent='+'+(Math.round((exadd+hotadd)*100)/100).toFixed(2)+' L';
  document.getElementById('wt-bottles').textContent='~'+Math.ceil(total/0.5);
  document.getElementById('wt-cups').textContent='~'+Math.ceil(total/0.237);
  document.getElementById('wt-note').textContent='Baseline ≈ 33 ml per kg. Exercise adds ~400 ml per 30 minutes; heat adds 0.5 L. Spread it across the day - a glass when you wake, one with each meal, and sip around workouts beats drinking it all at once. All food and drink counts toward the total.';
  document.title=(Math.round(total*10)/10).toFixed(1)+' L water a day - ToolTide';
}
function save(){try{localStorage.setItem('tt_water',JSON.stringify({k:KG.value,e:EX.value,h:HOT.value}));}catch(e){}}
[KG,EX,HOT].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
HOT.addEventListener('change',function(){calc();save();});
var pre=false;
[['kg',KG],['ex',EX],['hot',HOT]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_water')||'null');if(mem){KG.value=mem.k||'';EX.value=mem.e||'';HOT.value=mem.h||'0';}}catch(e){}}
calc();
document.getElementById('wt-share').addEventListener('click',function(){
  var txt='My daily water target: '+OUT.textContent+' L ('+document.getElementById('wt-bottles').textContent+' bottles). Find yours (no sign-up):';
  var url=location.origin+location.pathname+'?kg='+encodeURIComponent(KG.value||'')+'&ex='+encodeURIComponent(EX.value||'')+'&hot='+encodeURIComponent(HOT.value||'0');
  if(navigator.share){navigator.share({title:'Daily water target',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-target','Share my target');},1500);}
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
  <button type="button" class="tool-btn" id="gpa-share" data-i18n="share.share-my-gpa">Share my GPA</button>
</div>
<script>(function(){
var GR=[['A',4],['A-',3.7],['B+',3.3],['B',3],['B-',2.7],['C+',2.3],['C',2],['C-',1.7],['D+',1.3],['D',1],['F',0]];
var ROWS=7,box=document.getElementById('gpa-rows');
for(var i=0;i<ROWS;i++){
  var d=document.createElement('div');d.className='fields';
  d.innerHTML='<div class="field"><label for="gpa-n'+i+'">Course '+(i+1)+' (name optional)</label><input type="text" id="gpa-n'+i+'" class="gpa-n" placeholder="Calculus II"></div>'+
    '<div class="field"><label for="gpa-c'+i+'">Credits</label><input type="number" id="gpa-c'+i+'" class="gpa-c" step="any" min="0" placeholder="4"></div>'+
    '<div class="field"><label for="gpa-g'+i+'">Grade</label><select id="gpa-g'+i+'" class="gpa-g"><option value=""></option>'+
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
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-gpa','Share my GPA');},1500);}
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
  <button type="button" class="tool-btn" id="sl-share" data-i18n="share.share-these-times">Share these times</button>
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
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-these-times','Share these times');},1500);}
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
  <button type="button" class="tool-btn" id="sav-share" data-i18n="share.share-my-plan">Share my plan</button>
</div>
<style>.sav-bar{height:10px;border-radius:5px;background:rgba(127,127,127,.18);overflow:hidden;margin:10px 0 4px}.sav-bar>div{height:100%;width:0;border-radius:5px;background:var(--ink,#0891b2);transition:width .3s}</style>
<script>
(function(){
var G=document.getElementById('sav-goal'),S=document.getElementById('sav-saved'),D=document.getElementById('sav-dep'),R=document.getElementById('sav-apy');
var OUT=document.getElementById('sav-out'),UNIT=document.getElementById('sav-unit'),DET=document.getElementById('sav-detail'),FILL=document.getElementById('sav-fill');
var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function money(v){return '$'+Math.round(v).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
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
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);SB.textContent=TT('ui.copied','Copied!');setTimeout(function(){SB.textContent=TT('share.share-my-plan','Share my plan');},1500);}
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
    <div class="field"><label for="cp-y"><span data-i18n="lbl.years">Years</span></label><input type="number" id="cp-y" min="1" max="50" step="1" placeholder="10"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cp-out">-</span><span class="result-unit" id="cp-unit"></span></div>
  <div class="tool-note" id="cp-detail"></div>
  <div id="cp-table"></div>
  <button type="button" class="tool-btn" id="cp-share" data-i18n="share.share-this-projection">Share this projection</button>
</div>
<script>
(function(){
var P=document.getElementById('cp-p'),M=document.getElementById('cp-m'),R=document.getElementById('cp-r'),Y=document.getElementById('cp-y');
var OUT=document.getElementById('cp-out'),UNIT=document.getElementById('cp-unit'),DET=document.getElementById('cp-detail'),TB=document.getElementById('cp-table');
function money(v){return '$'+Math.round(v).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
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
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);SB.textContent=TT('ui.copied','Copied!');setTimeout(function(){SB.textContent=TT('share.share-this-projection','Share this projection');},1500);}
});
})();
</script>
<style>.cp-t{width:100%;border-collapse:collapse;margin-top:10px;font-size:.92em}.cp-t th,.cp-t td{padding:4px 8px;text-align:right;border-bottom:1px solid rgba(127,127,127,.25)}.cp-t th:first-child,.cp-t td:first-child{text-align:left}</style>
"""


# Loan payment: amortized monthly payment + total interest + interest share of total.
# Retention hooks: title result hook, tt_loan input memory, URL state (?p=&r=&y=), Web Share.
LOANPAY = """<div class="tool" id="tt-ln">
  <div class="fields">
    <div class="field"><label for="ln-p">Loan amount ($)</label><input type="number" id="ln-p" step="any" min="0" placeholder="25000"></div>
    <div class="field"><label for="ln-r">Annual interest rate %</label><input type="number" id="ln-r" step="any" min="0" max="40" placeholder="7.5"></div>
    <div class="field"><label for="ln-y"><span data-i18n="lbl.term-years">Term (years)</span></label><input type="number" id="ln-y" step="any" min="0.5" max="40" placeholder="5"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ln-out">–</span><span class="result-unit">per month</span></div>
  <div class="stats">
    <div class="stat"><b id="ln-int">–</b><span>total interest</span></div>
    <div class="stat"><b id="ln-tot">–</b><span>total paid</span></div>
    <div class="stat"><b id="ln-sharepct">–</b><span>interest share of payments</span></div>
  </div>
  <div class="tool-note" id="ln-note"></div>
  <button type="button" class="tool-btn" id="ln-share" data-i18n="share.share-this-payment">Share this payment</button>
</div>
<script>(function(){
var P=document.getElementById('ln-p'),R=document.getElementById('ln-r'),Y=document.getElementById('ln-y');
var OUT=document.getElementById('ln-out');
function money(n){return '$'+Math.round(n).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parseFloat(P.value),ar=parseFloat(R.value),y=parseFloat(Y.value);
  if(!(p>0)||!(y>0)||isNaN(ar)||ar<0){OUT.textContent='–';
    document.getElementById('ln-int').textContent='–';document.getElementById('ln-tot').textContent='–';
    document.getElementById('ln-sharepct').textContent='–';document.getElementById('ln-note').textContent='';
    document.title='Loan Payment Calculator - ToolTide';return;}
  var r=ar/100/12,n=Math.round(y*12),m;
  if(r===0){m=p/n;}
  else{var f=Math.pow(1+r,n);m=p*r*f/(f-1);}
  var tot=m*n,int=tot-p;
  OUT.textContent=money(m);
  document.getElementById('ln-int').textContent=money(int);
  document.getElementById('ln-tot').textContent=money(tot);
  document.getElementById('ln-sharepct').textContent=Math.round(int/tot*100)+'%';
  document.getElementById('ln-note').textContent=money(p)+' at '+ar+'% for '+y+' years costs '+money(int)+' in interest - '+Math.round(int/tot*100)+' cents of every payment. Extra principal each month shortens the term and skips the interest those months would have carried.';
  document.title=money(m)+'/mo loan payment - ToolTide';
}
function save(){try{localStorage.setItem('tt_loan',JSON.stringify({p:P.value,r:R.value,y:Y.value}));}catch(e){}}
[P,R,Y].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['p',P],['r',R],['y',Y]].forEach(function(a){var x=qs(a[0]);if(x!==null){a[1].value=x;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_loan')||'null');if(mem){P.value=mem.p||'';R.value=mem.r||'';Y.value=mem.y||'';}}catch(e){}}
calc();
document.getElementById('ln-share').addEventListener('click',function(){
  var txt='Loan payment: '+OUT.textContent+'/mo ('+document.getElementById('ln-int').textContent+' total interest). Run your numbers (no sign-up):';
  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value||'')+'&r='+encodeURIComponent(R.value||'')+'&y='+encodeURIComponent(Y.value||'');
  if(navigator.share){navigator.share({title:'Loan payment',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-payment','Share this payment');},1500);}
});
})();
</script>
"""

# VAT add/remove with quick country rates. The "divide, not subtract" teaching note is the differentiator.
# Retention hooks: title result hook, tt_vat input memory, URL state (?m=&a=&r=), Web Share.
VATCALC = """<div class="tool" id="tt-vat">
  <div class="fields">
    <div class="field"><label for="vat-m"><span data-i18n="lbl.mode">Mode</span></label><select id="vat-m"><option value="add">Add VAT (net to gross)</option><option value="rem">Remove VAT (gross to net)</option></select></div>
    <div class="field"><label for="vat-a">Amount</label><input type="number" id="vat-a" step="any" min="0" placeholder="100"></div>
    <div class="field"><label for="vat-r">VAT rate %</label><input type="number" id="vat-r" step="any" min="0" max="40" placeholder="20"></div>
    <div class="field"><label for="vat-p">Quick rates</label><select id="vat-p"><option value="">Choose a rate…</option><option value="20">UK standard 20%</option><option value="5">UK reduced 5%</option><option value="19">Germany 19%</option><option value="21">Netherlands / Spain 21%</option><option value="22">Italy 22%</option><option value="23">Ireland 23%</option><option value="10">Common reduced 10%</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="vat-out">–</span><span class="result-unit" id="vat-u">incl. VAT</span></div>
  <div class="stats">
    <div class="stat"><b id="vat-net">–</b><span>net (ex VAT)</span></div>
    <div class="stat"><b id="vat-amt">–</b><span>VAT amount</span></div>
    <div class="stat"><b id="vat-gr">–</b><span>gross (incl VAT)</span></div>
  </div>
  <div class="tool-note" id="vat-note"></div>
  <button type="button" class="tool-btn" id="vat-share" data-i18n="share.share-this-breakdown">Share this breakdown</button>
</div>
<script>(function(){
var M=document.getElementById('vat-m'),A=document.getElementById('vat-a'),R=document.getElementById('vat-r'),PR=document.getElementById('vat-p');
var OUT=document.getElementById('vat-out'),U=document.getElementById('vat-u');
function money(n){return '$'+(Math.round(n*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),r=(parseFloat(R.value)||0)/100;
  if(!(a>0)||r<0){OUT.textContent='–';U.textContent='';
    document.getElementById('vat-net').textContent='–';document.getElementById('vat-amt').textContent='–';
    document.getElementById('vat-gr').textContent='–';document.getElementById('vat-note').textContent='';
    document.title='VAT Calculator - ToolTide';return;}
  var net,gross;
  if(M.value==='add'){net=a;gross=a*(1+r);}else{gross=a;net=a/(1+r);}
  var amt=gross-net;
  OUT.textContent=money(M.value==='add'?gross:net);
  U.textContent=M.value==='add'?'incl. VAT':'net of VAT';
  document.getElementById('vat-net').textContent=money(net);
  document.getElementById('vat-amt').textContent=money(amt);
  document.getElementById('vat-gr').textContent=money(gross);
  var rt=Math.round(r*100);
  document.getElementById('vat-note').textContent=M.value==='add'
    ?'Adding '+rt+'% VAT: '+money(net)+' x '+(1+r).toFixed(r>0?4:0)+' = '+money(gross)+'.'
    :'Removing '+rt+'% VAT: '+money(gross)+' / '+(1+r).toFixed(r>0?4:0)+' = '+money(net)+'. Divide - never subtract '+rt+'%, because the gross already carries the tax.';
  document.title=money(M.value==='add'?gross:net)+(M.value==='add'?' incl. VAT':' ex VAT')+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_vat',JSON.stringify({m:M.value,a:A.value,r:R.value}));}catch(e){}}
[M,A,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
PR.addEventListener('change',function(){if(PR.value!==''){R.value=PR.value;calc();save();}});
var pre=false;
[['m',M],['a',A],['r',R]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_vat')||'null');if(mem){M.value=mem.m||'add';A.value=mem.a||'';R.value=mem.r||'';}}catch(e){}}
calc();
document.getElementById('vat-share').addEventListener('click',function(){
  var txt='VAT breakdown: net '+document.getElementById('vat-net').textContent+' + VAT '+document.getElementById('vat-amt').textContent+' = gross '+document.getElementById('vat-gr').textContent+'. Run yours (no sign-up):';
  var url=location.origin+location.pathname+'?m='+M.value+'&a='+encodeURIComponent(A.value||'')+'&r='+encodeURIComponent(R.value||'');
  if(navigator.share){navigator.share({title:'VAT breakdown',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-breakdown','Share this breakdown');},1500);}
});
})();
</script>
"""

# Fraction arithmetic with exact simplified, mixed and decimal outputs plus a worked LCD line.
# Retention hooks: title result hook, tt_frac input memory, URL state (?a=&b=&c=&d=&op=), Web Share.
FRACTION = """<div class="tool" id="tt-fr">
  <div class="fields">
    <div class="field"><label for="fr-a">Numerator 1</label><input type="number" id="fr-a" step="1" placeholder="3"></div>
    <div class="field"><label for="fr-b">Denominator 1</label><input type="number" id="fr-b" step="1" placeholder="4"></div>
    <div class="field"><label for="fr-op">Operation</label><select id="fr-op"><option value="+">+ add</option><option value="-">− subtract</option><option value="*">× multiply</option><option value="/">÷ divide</option></select></div>
    <div class="field"><label for="fr-c">Numerator 2</label><input type="number" id="fr-c" step="1" placeholder="5"></div>
    <div class="field"><label for="fr-d">Denominator 2</label><input type="number" id="fr-d" step="1" placeholder="6"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fr-out">–</span><span class="result-unit">exact answer</span></div>
  <div class="stats">
    <div class="stat"><b id="fr-mix">–</b><span>as a mixed number</span></div>
    <div class="stat"><b id="fr-dec">–</b><span>as a decimal</span></div>
    <div class="stat"><b id="fr-lcd">–</b><span>common denominator used</span></div>
  </div>
  <div class="tool-note" id="fr-note"></div>
  <button type="button" class="tool-btn" id="fr-share" data-i18n="share.share-this-result">Share this result</button>
</div>
<script>(function(){
var A=document.getElementById('fr-a'),B=document.getElementById('fr-b'),C=document.getElementById('fr-c'),D=document.getElementById('fr-d'),OP=document.getElementById('fr-op');
var OUT=document.getElementById('fr-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function gcd(x,y){x=Math.abs(x);y=Math.abs(y);while(y){var t=x%y;x=y;y=t;}return x||1;}
function mixed(n,d){
  var s=n<0?'−':'',an=Math.abs(n),w=Math.floor(an/d),r2=an%d;
  if(r2===0)return s+w;
  if(w===0)return s+r2+'/'+d;
  return s+w+' '+r2+'/'+d;
}
function calc(){
  var a=parseInt(A.value,10),b=parseInt(B.value,10),c=parseInt(C.value,10),d=parseInt(D.value,10),op=OP.value;
  if([a,b,c,d].some(isNaN)||!b||!d||(op==='/'&&!c)){OUT.textContent='–';
    document.getElementById('fr-mix').textContent='–';document.getElementById('fr-dec').textContent='–';
    document.getElementById('fr-lcd').textContent='–';document.getElementById('fr-note').textContent='Enter whole numbers - a denominator (or the fraction you divide by) cannot be zero.';
    document.title='Fraction Calculator - ToolTide';return;}
  var n,dd,lcdUsed=null;
  if(op==='+'||op==='-'){
    var l=b*d/gcd(b,d);
    var x=a*(l/b),y=c*(l/d);
    n=op==='+'?x+y:x-y;dd=l;
    lcdUsed=l;
  }else if(op==='*'){n=a*c;dd=b*d;}
  else{n=a*d;dd=b*c;}
  var g=gcd(n,dd);n/=g;dd/=g;
  if(dd<0){n=-n;dd=-dd;}
  OUT.textContent=n+'/'+dd;
  document.getElementById('fr-mix').textContent=mixed(n,dd);
  document.getElementById('fr-dec').textContent=(Math.round(n/dd*1e6)/1e6).toString();
  document.getElementById('fr-lcd').textContent=lcdUsed===null?'—':lcdUsed;
  var sym=op==='+'?'+':(op==='-'?'−':(op==='*'?'×':'÷'));
  var note=a+'/'+b+' '+sym+' '+c+'/'+d+' = ';
  if(lcdUsed){note+=a*(lcdUsed/b)+'/'+lcdUsed+' '+sym+' '+c*(lcdUsed/d)+'/'+lcdUsed+' = ';}
  if(op==='/'){note+='flip and multiply: '+a+'/'+b+' × '+d+'/'+c+' = ';}
  note+=OUT.textContent+(g>1?' (divided by '+g+')':'');
  document.getElementById('fr-note').textContent=note;
  document.title=OUT.textContent+' = '+document.getElementById('fr-dec').textContent+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_frac',JSON.stringify({a:A.value,b:B.value,c:C.value,d:D.value,op:OP.value}));}catch(e){}}
[A,B,C,D].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
OP.addEventListener('change',function(){calc();save();});
var pre=false;
[['a',A],['b',B],['c',C],['d',D],['op',OP]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_frac')||'null');if(mem){A.value=mem.a||'';B.value=mem.b||'';C.value=mem.c||'';D.value=mem.d||'';OP.value=mem.op||'+';}}catch(e){}}
calc();
document.getElementById('fr-share').addEventListener('click',function(){
  var txt=document.getElementById('fr-note').textContent+'. Solve yours step by step (no sign-up):';
  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value||'')+'&b='+encodeURIComponent(B.value||'')+'&c='+encodeURIComponent(C.value||'')+'&d='+encodeURIComponent(D.value||'')+'&op='+encodeURIComponent(OP.value);
  if(navigator.share){navigator.share({title:'Fraction result',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b2=this;setTimeout(function(){b2.textContent=TT('share.share-this-result','Share this result');},1500);}
});
})();
</script>
"""

# Pregnancy due date: Naegele +280d from LMP, +266d from conception, or back from ultrasound GA.
# Retention hooks: title result hook (gestational age), tt_preg memory, URL state (?m=&d=&w=&g=), Web Share.
PREGNANCY = """<div class="tool" id="tt-pg">
  <div class="fields">
    <div class="field"><label for="pg-m"><span data-i18n="lbl.method">Method</span></label><select id="pg-m"><option value="lmp">Last period (LMP)</option><option value="con">Conception date</option><option value="us">Ultrasound (date + GA)</option></select></div>
    <div class="field"><label for="pg-d">Reference date</label><input type="date" id="pg-d"></div>
    <div class="field"><label for="pg-w">GA weeks (ultrasound only)</label><input type="number" id="pg-w" step="1" min="0" max="42" placeholder="8"></div>
    <div class="field"><label for="pg-g">GA days</label><input type="number" id="pg-g" step="1" min="0" max="6" placeholder="3"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pg-out">–</span><span class="result-unit" id="pg-u">estimated due date</span></div>
  <div class="stats">
    <div class="stat"><b id="pg-ga">–</b><span>gestational age now</span></div>
    <div class="stat"><b id="pg-left">–</b><span>days to go</span></div>
    <div class="stat"><b id="pg-tri">–</b><span>trimester</span></div>
  </div>
  <div class="tool-note" id="pg-note"></div>
  <button type="button" class="tool-btn" id="pg-share" data-i18n="share.share-this-due-date">Share this due date</button>
</div>
<script>(function(){
var M=document.getElementById('pg-m'),D=document.getElementById('pg-d'),W=document.getElementById('pg-w'),G=document.getElementById('pg-g');
var OUT=document.getElementById('pg-out'),U=document.getElementById('pg-u');
var MS=86400000;
function qs(k){return new URLSearchParams(location.search).get(k);}
function fmt(t){
  var d=new Date(t),mo=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var wd=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][d.getUTCDay()];
  return wd+', '+d.getUTCDate()+' '+mo[d.getUTCMonth()]+' '+d.getUTCFullYear();
}
function calc(){
  var dv=D.value;
  if(!dv){OUT.textContent='–';U.textContent='estimated due date';
    document.getElementById('pg-ga').textContent='–';document.getElementById('pg-left').textContent='–';
    document.getElementById('pg-tri').textContent='–';document.getElementById('pg-note').textContent='';
    document.title='Pregnancy Due Date Calculator - ToolTide';return;}
  var dt=new Date(dv+'T00:00:00Z').getTime();
  if(isNaN(dt)){OUT.textContent='–';return;}
  var edd;
  if(M.value==='lmp'){edd=dt+280*MS;}
  else if(M.value==='con'){edd=dt+266*MS;}
  else{
    var w=parseInt(W.value,10),g=parseInt(G.value,10);
    if(isNaN(w)){OUT.textContent='–';U.textContent='enter GA weeks';return;}
    if(isNaN(g))g=0;
    edd=dt+(280-(w*7+g))*MS;
  }
  var now=new Date();var today=Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate());
  var carried=dt;
  if(M.value==='us'){var w2=parseInt(W.value,10)||0,g2=parseInt(G.value,10)||0;carried=dt-(w2*7+g2)*MS;}
  var days=Math.floor((today-carried)/MS),w3=Math.floor(days/7),d3=days%7;
  OUT.textContent=fmt(edd);
  U.textContent='estimated due date';
  var left=Math.round((edd-today)/MS);
  document.getElementById('pg-ga').textContent=w3+'w '+d3+'d';
  document.getElementById('pg-left').textContent=left>=0?left+' days':'born!';
  var pct=Math.max(0,Math.min(100,Math.round(days/280*100)));
  document.getElementById('pg-tri').textContent=days<98?'1st':(days<196?'2nd':'3rd');
  document.getElementById('pg-note').textContent=pct+'% of the way (day '+days+' of 280) - only 5% of babies arrive exactly on the due date, most land within two weeks of it.';
  document.title=w3+'w'+d3+'d · due '+OUT.textContent.slice(0,-6)+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_preg',JSON.stringify({m:M.value,d:D.value,w:W.value,g:G.value}));}catch(e){}}
[M,D,W,G].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
M.addEventListener('change',function(){W.disabled=M.value!=='us';G.disabled=M.value!=='us';calc();save();});
W.disabled=true;G.disabled=true;
var pre=false;
[['m',M],['d',D],['w',W],['g',G]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_preg')||'null');if(mem){M.value=mem.m||'lmp';D.value=mem.d||'';W.value=mem.w||'';G.value=mem.g||'';}}catch(e){}}
W.disabled=M.value!=='us';G.disabled=M.value!=='us';
calc();
document.getElementById('pg-share').addEventListener('click',function(){
  var txt='Due date: '+OUT.textContent+' - '+document.getElementById('pg-ga').textContent+' along today. Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?m='+M.value+'&d='+encodeURIComponent(D.value||'')+'&w='+encodeURIComponent(W.value||'')+'&g='+encodeURIComponent(G.value||'');
  if(navigator.share){navigator.share({title:'Due date',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-due-date','Share this due date');},1500);}
});
})();
</script>
"""

# Time zone converter via Intl (DST-aware, no library): wall-time guess + offset iteration.
# Retention hooks: title result hook, tt_tz memory, URL state (?f=&t=&dt=), Web Share.
TZCONVERT = """<div class="tool" id="tt-tz">
  <div class="fields">
    <div class="field"><label for="tz-f">From zone</label><select id="tz-f"></select></div>
    <div class="field"><label for="tz-dt">Date &amp; time there</label><input type="datetime-local" id="tz-dt"></div>
    <div class="field"><label for="tz-t">To zone</label><select id="tz-t"></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tz-out">–</span><span class="result-unit" id="tz-u">local time there</span></div>
  <div class="stats">
    <div class="stat"><b id="tz-diff">–</b><span>time difference</span></div>
    <div class="stat"><b id="tz-fd">–</b><span>date shift</span></div>
    <div class="stat"><b id="tz-day">–</b><span>your device now</span></div>
  </div>
  <div class="tool-note" id="tz-note"></div>
  <button type="button" class="tool-btn" id="tz-share" data-i18n="share.share-this-meeting-time">Share this meeting time</button>
</div>
<script>(function(){
var F=document.getElementById('tz-f'),T=document.getElementById('tz-t'),DT=document.getElementById('tz-dt');
var OUT=document.getElementById('tz-out'),U=document.getElementById('tz-u');
var ZONES=[['New York','America/New_York'],['Los Angeles','America/Los_Angeles'],['Chicago','America/Chicago'],['Denver','America/Denver'],['Mexico City','America/Mexico_City'],['Sao Paulo','America/Sao_Paulo'],['London','Europe/London'],['Paris / Berlin / Madrid','Europe/Paris'],['Lagos','Africa/Lagos'],['Cairo','Africa/Cairo'],['Moscow','Europe/Moscow'],['Dubai','Asia/Dubai'],['Karachi','Asia/Karachi'],['Mumbai','Asia/Kolkata'],['Dhaka','Asia/Dhaka'],['Bangkok / Jakarta','Asia/Bangkok'],['Singapore / Hong Kong','Asia/Singapore'],['Tokyo','Asia/Tokyo'],['Seoul','Asia/Seoul'],['Sydney','Australia/Sydney'],['Auckland','Pacific/Auckland']];
var myTZ='';
try{myTZ=Intl.DateTimeFormat().resolvedOptions().timeZone||'';}catch(e){}
if(!myTZ)myTZ='Europe/London';
function fill(sel,def){
  var html='';
  if(myTZ){html+='<option value="'+myTZ+'"'+(def===myTZ?' selected':'')+'>My device ('+myTZ+')</option>';}
  ZONES.forEach(function(z){html+='<option value="'+z[1]+'"'+(def===z[1]?' selected':'')+'>'+z[0]+'</option>';});
  sel.innerHTML=html;
}
var defTo=ZONES.some(function(z){return z[1]===myTZ;})?'Europe/London':myTZ;
fill(F,myTZ);fill(T,defTo);
function qs(k){return new URLSearchParams(location.search).get(k);}
function partsIn(tz,t){
  var dtf;
  try{dtf=new Intl.DateTimeFormat('en-GB',{timeZone:tz,hour12:false,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'});}catch(e){return null;}
  var p={};dtf.formatToParts(new Date(t)).forEach(function(x){p[x.type]=x.value;});
  return {y:+p.year,mo:+p.month,d:+p.day,h:+p.hour%24,mi:+p.minute};
}
function wallToUTC(tz,y,mo,d,h,mi){
  var wall=Date.UTC(y,mo-1,d,h,mi),guess=wall;
  for(var i=0;i<2;i++){
    var p=partsIn(tz,guess);
    if(!p)return null;
    var asUTC=Date.UTC(p.y,p.mo-1,p.d,p.h,p.mi);
    guess+=wall-asUTC;
  }
  return guess;
}
function offsetH(tz,t){var p=partsIn(tz,t);if(!p)return 0;return (Date.UTC(p.y,p.mo-1,p.d,p.h,p.mi)-t)/3600000;}
function calc(){
  var v=DT.value;
  if(!v){OUT.textContent='–';U.textContent='local time there';
    document.getElementById('tz-diff').textContent='–';document.getElementById('tz-fd').textContent='–';
    document.getElementById('tz-day').textContent='–';document.getElementById('tz-note').textContent='';
    document.title='Time Zone Converter - ToolTide';return;}
  var m=v.match(/^(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2})/);
  if(!m){OUT.textContent='–';return;}
  var utc=wallToUTC(F.value,+m[1],+m[2],+m[3],+m[4],+m[5]);
  if(utc===null){OUT.textContent='–';return;}
  var p=partsIn(T.value,utc);
  var pf=partsIn(F.value,utc);
  if(!p||!pf){OUT.textContent='–';return;}
  var h12=((p.h+11)%12)+1,ap=p.h<12?'am':'pm';
  var wd=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][(new Date(Date.UTC(p.y,p.mo-1,p.d))).getUTCDay()];
  OUT.textContent=wd+' '+p.d+', '+String(p.y).slice(2)+' · '+h12+':'+String(p.mi).padStart(2,'0')+' '+ap;
  U.textContent='in '+T.options[T.selectedIndex].text;
  var df=offsetH(T.value,utc)-offsetH(F.value,utc);
  var dh=Math.abs(df),sign=df>=0?'+':'−';
  document.getElementById('tz-diff').textContent=sign+Math.floor(dh)+'h'+(Math.round(dh%1*60)?Math.round(dh%1*60)+'m':'');
  document.getElementById('tz-fd').textContent=p.d!==pf.d?(df>=0?'next day':'prev day'):'same day';
  var now=new Date(),np=partsIn(myTZ,now.getTime());
  var nh=((np.h+11)%12)+1;
  document.getElementById('tz-day').textContent=nh+':'+String(np.mi).padStart(2,'0')+' '+(np.h<12?'am':'pm');
  document.getElementById('tz-note').textContent='DST handled automatically - zones shift with their own daylight rules, so the same meeting in July and January can differ by an hour.';
  document.title=OUT.textContent+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_tz',JSON.stringify({f:F.value,t:T.value,dt:DT.value}));}catch(e){}}
[F,T].forEach(function(el){el.addEventListener('change',function(){calc();save();});});
DT.addEventListener('input',function(){calc();save();});
function setSel(sel,val){for(var i=0;i<sel.options.length;i++){if(sel.options[i].value===val){sel.selectedIndex=i;return true;}}return false;}
var pre=false;
var qf=qs('f'),qt=qs('t'),qd=qs('dt');
if(qf!==null){if(setSel(F,qf))pre=true;}
if(qt!==null){if(setSel(T,qt))pre=true;}
if(qd!==null){DT.value=qd;pre=true;}
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_tz')||'null');if(mem&&mem.dt){DT.value=mem.dt;setSel(F,mem.f||myTZ);setSel(T,mem.t||defTo);}}catch(e){}}
if(!DT.value){var n=new Date();DT.value=n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0')+'T'+String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');}
calc();
document.getElementById('tz-share').addEventListener('click',function(){
  var txt=F.options[F.selectedIndex].text+' '+DT.value.replace('T',' at ')+' = '+OUT.textContent+'. Line up yours (no sign-up):';
  var url=location.origin+location.pathname+'?f='+encodeURIComponent(F.value)+'&t='+encodeURIComponent(T.value)+'&dt='+encodeURIComponent(DT.value);
  if(navigator.share){navigator.share({title:'Meeting time',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-meeting-time','Share this meeting time');},1500);}
});
})();
</script>
"""

# ISO week number with week boundaries, quarter and day-of-year.
# Retention hooks: title result hook, tt_week memory, URL state (?d=), Web Share.
WEEKNUM = """<div class="tool" id="tt-wk">
  <div class="fields">
    <div class="field"><label for="wk-d">Any date in the week</label><input type="date" id="wk-d"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wk-out">–</span><span class="result-unit">ISO week</span></div>
  <div class="stats">
    <div class="stat"><b id="wk-span">–</b><span>Mon – Sun of that week</span></div>
    <div class="stat"><b id="wk-q">–</b><span>quarter</span></div>
    <div class="stat"><b id="wk-doy">–</b><span>day of year</span></div>
  </div>
  <div class="tool-note" id="wk-note"></div>
  <button type="button" class="tool-btn" id="wk-share" data-i18n="share.share-this-week">Share this week</button>
</div>
<script>(function(){
var D=document.getElementById('wk-d');
var OUT=document.getElementById('wk-out');
var MS=86400000;
var MO=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function qs(k){return new URLSearchParams(location.search).get(k);}
function isoCal(t){
  var d=new Date(t);d.setUTCHours(0,0,0,0);
  d.setUTCDate(d.getUTCDate()+4-(d.getUTCDay()||7));
  var yearStart=Date.UTC(d.getUTCFullYear(),0,1);
  var week=Math.ceil(((d.getTime()-yearStart)/MS+1)/7);
  return {week:week,isoYear:d.getUTCFullYear()};
}
function fmt(t){var d=new Date(t);return d.getUTCDate()+' '+MO[d.getUTCMonth()];}
function calc(){
  var v=D.value;
  if(!v){OUT.textContent='–';
    document.getElementById('wk-span').textContent='–';document.getElementById('wk-q').textContent='–';
    document.getElementById('wk-doy').textContent='–';document.getElementById('wk-note').textContent='';
    document.title='Week Number Calculator - ToolTide';return;}
  var t=new Date(v+'T00:00:00Z').getTime();
  if(isNaN(t)){OUT.textContent='–';return;}
  var c=isoCal(t);
  OUT.textContent='Week '+c.week;
  var dow=(new Date(t)).getUTCDay()||7;
  var mon=t-(dow-1)*MS,sun=t+(7-dow)*MS;
  document.getElementById('wk-span').textContent=fmt(mon)+' – '+fmt(sun);
  var mo=new Date(t).getUTCMonth();
  document.getElementById('wk-q').textContent='Q'+(Math.floor(mo/3)+1);
  var y=new Date(t).getUTCFullYear();
  var leap=(y%4===0&&y%100!==0)||y%400===0;
  var jan1=Date.UTC(y,0,1);
  document.getElementById('wk-doy').textContent=(Math.floor((t-jan1)/MS)+1)+' / '+(leap?366:365);
  document.getElementById('wk-note').textContent='ISO-8601 weeks run Monday to Sunday, and week 1 always holds the first Thursday - which is why early-January dates can still belong to week 52 or 53 of the year before.';
  document.title='Week '+c.week+' ('+fmt(mon)+'-'+fmt(sun)+') - ToolTide';
}
function save(){try{localStorage.setItem('tt_week',JSON.stringify({d:D.value}));}catch(e){}}
D.addEventListener('input',function(){calc();save();});
var pre=false;
var q=qs('d');if(q!==null){D.value=q;pre=true;}
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_week')||'null');if(mem&&mem.d)D.value=mem.d;}catch(e){}}
if(!D.value){var n=new Date();D.value=n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0');}
calc();
document.getElementById('wk-share').addEventListener('click',function(){
  var txt=OUT.textContent+' of '+isoCal(new Date(D.value+'T00:00:00Z').getTime()).isoYear+' ('+document.getElementById('wk-span').textContent+'). Check any week (no sign-up):';
  var url=location.origin+location.pathname+'?d='+encodeURIComponent(D.value);
  if(navigator.share){navigator.share({title:'Week number',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-week','Share this week');},1500);}
});
})();
</script>
"""

# Weekly time card: in/out per day, shared lunch deduction, overnight shifts, OT over 40h.
# Retention hooks: title result hook, tt_timecard memory, packed URL state (?l=&s=), Web Share.
TIMECARD = """<div class="tool" id="tt-tc">
  <div class="fields" id="tc-rows">
    <div class="field"><label for="tc-l">Unpaid lunch (min/day)</label><input type="number" id="tc-l" step="5" min="0" max="180" placeholder="30"></div>
  </div>
  <div id="tc-days"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tc-out">–</span><span class="result-unit">total hours this week</span></div>
  <div class="stats">
    <div class="stat"><b id="tc-dec">–</b><span>decimal hours</span></div>
    <div class="stat"><b id="tc-ot">–</b><span>overtime over 40h</span></div>
    <div class="stat"><b id="tc-days-w">–</b><span>days worked</span></div>
  </div>
  <div class="tool-note" id="tc-note"></div>
  <button type="button" class="tool-btn" id="tc-share" data-i18n="share.share-this-time-card">Share this time card</button>
</div>
<script>(function(){
var DAYS=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
var box=document.getElementById('tc-days');
var html='';
DAYS.forEach(function(d,i){
  html+='<div class="fields"><div class="field"><label>In '+d+'</label><input type="time" id="tc-i'+i+'"></div><div class="field"><label>Out '+d+'</label><input type="time" id="tc-o'+i+'"></div></div>';
});
box.innerHTML=html;
var L=document.getElementById('tc-l');
var OUT=document.getElementById('tc-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function mins(v){if(!v)return null;var m=v.match(/^(\\d{1,2}):(\\d{2})$/);return m?(+m[1])*60+(+m[2]):null;}
function fmtHM(min){var h=Math.floor(min/60),m=min%60;return h+'h'+(m?' '+m+'m':'');}
function calc(){
  var lunch=Math.max(0,parseInt(L.value,10)||0),total=0,dw=0,rows=[];
  for(var i=0;i<7;i++){
    var a=mins(document.getElementById('tc-i'+i).value),b=mins(document.getElementById('tc-o'+i).value);
    if(a===null||b===null){rows.push(null);continue;}
    if(b<=a)b+=1440;
    var d=Math.max(0,b-a-lunch);
    total+=d;dw++;rows.push(d);
  }
  if(!dw){OUT.textContent='–';
    document.getElementById('tc-dec').textContent='–';document.getElementById('tc-ot').textContent='–';
    document.getElementById('tc-days-w').textContent='–';document.getElementById('tc-note').textContent='';
    document.title='Time Card Calculator - ToolTide';return;}
  OUT.textContent=fmtHM(total);
  document.getElementById('tc-dec').textContent=(Math.round(total/60*100)/100).toString();
  var ot=Math.max(0,total-2400);
  document.getElementById('tc-ot').textContent=ot>0?fmtHM(ot):'—';
  document.getElementById('tc-days-w').textContent=dw;
  var av=total/dw;
  document.getElementById('tc-note').textContent='Average '+fmtHM(Math.round(av))+' per worked day, lunch of '+lunch+' min already deducted. Overnight shifts (out before in) roll to the next day automatically.';
  document.title=fmtHM(total)+' this week - ToolTide';
}
function pack(){
  var s=[];
  for(var i=0;i<7;i++){s.push(document.getElementById('tc-i'+i).value+'-'+document.getElementById('tc-o'+i).value);}
  return s.join(',');
}
function save(){try{localStorage.setItem('tt_timecard',JSON.stringify({l:L.value,s:pack()}));}catch(e){}}
L.addEventListener('input',function(){calc();save();});
for(var j=0;j<7;j++){
  document.getElementById('tc-i'+j).addEventListener('input',function(){calc();save();});
  document.getElementById('tc-o'+j).addEventListener('input',function(){calc();save();});
}
var pre=false;
var ql=qs('l'),qsv=qs('s');
if(ql!==null){L.value=ql;pre=true;}
if(qsv!==null){
  var parts=qsv.split(',');
  if(parts.length===7){
    pre=true;
    for(var k=0;k<7;k++){var pr=parts[k].split('-');
      if(pr.length===2){document.getElementById('tc-i'+k).value=pr[0];document.getElementById('tc-o'+k).value=pr[1];}}
  }
}
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_timecard')||'null');
  if(mem){L.value=mem.l||'';
    if(mem.s){var ps=mem.s.split(',');
      for(var q=0;q<7&&q<ps.length;q++){var pr2=ps[q].split('-');
        if(pr2.length===2){document.getElementById('tc-i'+q).value=pr2[0];document.getElementById('tc-o'+q).value=pr2[1];}}}}}catch(e){}}
calc();
document.getElementById('tc-share').addEventListener('click',function(){
  var txt='Time card this week: '+OUT.textContent+' ('+document.getElementById('tc-dec').textContent+'h decimal, '+document.getElementById('tc-days-w').textContent+' days). Tally yours (no sign-up):';
  var url=location.origin+location.pathname+'?l='+encodeURIComponent(L.value||'')+'&s='+encodeURIComponent(pack());
  if(navigator.share){navigator.share({title:'Weekly hours',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-time-card','Share this time card');},1500);}
});
})();
</script>
"""

# One-rep max: Epley / Brzycki / Lander consensus + percentage working weights.
# Retention hooks: title result hook, tt_orm memory, URL state (?w=&r=&u=), Web Share.
ONEREPMAX = """<div class="tool" id="tt-orm">
  <div class="fields">
    <div class="field"><label for="orm-w">Weight lifted</label><input type="number" id="orm-w" step="any" min="0" placeholder="100"></div>
    <div class="field"><label for="orm-r">Reps completed</label><input type="number" id="orm-r" step="1" min="1" max="12" placeholder="5"></div>
    <div class="field"><label for="orm-u"><span data-i18n="lbl.units">Units</span></label><select id="orm-u"><option value="lb">lb</option><option value="kg">kg</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="orm-out">–</span><span class="result-unit" id="orm-u2">estimated 1RM</span></div>
  <div class="stats">
    <div class="stat"><b id="orm-e">–</b><span>Epley</span></div>
    <div class="stat"><b id="orm-b">–</b><span>Brzycki</span></div>
    <div class="stat"><b id="orm-w5">–</b><span>5x5 working weight</span></div>
  </div>
  <div class="tool-note" id="orm-note"></div>
  <button type="button" class="tool-btn" id="orm-share" data-i18n="share.share-this-max">Share this max</button>
</div>
<script>(function(){
var W=document.getElementById('orm-w'),R=document.getElementById('orm-r'),U=document.getElementById('orm-u');
var OUT=document.getElementById('orm-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function rnd(n){return Math.round(n);}
function calc(){
  var w=parseFloat(W.value),r=parseInt(R.value,10),u=U.value;
  if(!(w>0)||!(r>=1)){OUT.textContent='–';
    document.getElementById('orm-e').textContent='–';document.getElementById('orm-b').textContent='–';
    document.getElementById('orm-w5').textContent='–';document.getElementById('orm-note').textContent='';
    document.title='One Rep Max Calculator - ToolTide';return;}
  var ep=w*(1+r/30),br=r<37?w*36/(37-r):0,ld=w*100/(101.3-2.67123*r);
  var avg=(ep+br+ld)/3;
  OUT.textContent=rnd(avg)+' '+u;
  document.getElementById('orm-u2').textContent='estimated 1RM';
  document.getElementById('orm-e').textContent=rnd(ep)+' '+u;
  document.getElementById('orm-b').textContent=rnd(br)+' '+u;
  document.getElementById('orm-w5').textContent=rnd(avg*0.8)+' '+u;
  document.getElementById('orm-note').textContent='Three formulas, one answer: '+rnd(avg)+' '+u+' average. Programs speak percentages of 1RM - 80% for 5x5 strength blocks, 70% for volume work, 90%+ only for singles. Estimates tighten under 10 reps; beyond that they drift.';
  document.title=rnd(avg)+' '+u+' one rep max - ToolTide';
}
function save(){try{localStorage.setItem('tt_orm',JSON.stringify({w:W.value,r:R.value,u:U.value}));}catch(e){}}
[W,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){calc();save();});
var pre=false;
[['w',W],['r',R],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_orm')||'null');if(mem){W.value=mem.w||'';R.value=mem.r||'';U.value=mem.u||'lb';}}catch(e){}}
calc();
document.getElementById('orm-share').addEventListener('click',function(){
  var txt='Estimated 1RM: '+OUT.textContent+' from '+W.value+U.value+' x '+R.value+' reps. Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?w='+encodeURIComponent(W.value||'')+'&r='+encodeURIComponent(R.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'One rep max',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-max','Share this max');},1500);}
});
})();
</script>
"""

# Standard deviation: paste-in dataset -> n, mean, sample & population SD, variance, range.
# Retention hooks: title result hook, tt_sd memory, URL state (?d=), Web Share.
STDDEV = """<div class="tool" id="tt-sd">
  <div class="fields">
    <div class="field"><label for="sd-in">Data (separated by spaces, commas or new lines)</label><textarea id="sd-in" rows="4" placeholder="2 4 4 4 5 5 7 9"></textarea></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sd-out">–</span><span class="result-unit">sample standard deviation</span></div>
  <div class="stats">
    <div class="stat"><b id="sd-pop">–</b><span>population SD</span></div>
    <div class="stat"><b id="sd-mean">–</b><span>mean</span></div>
    <div class="stat"><b id="sd-n">–</b><span>n · min-max</span></div>
  </div>
  <div class="tool-note" id="sd-note"></div>
  <button type="button" class="tool-btn" id="sd-share" data-i18n="share.share-this-summary">Share this summary</button>
</div>
<script>(function(){
var IN=document.getElementById('sd-in');
var OUT=document.getElementById('sd-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var raw=IN.value.split(/[\\s,;]+/).filter(function(x){return x.length>0;});
  var nums=raw.map(parseFloat).filter(function(x){return isFinite(x);});
  if(nums.length<2){OUT.textContent='–';
    document.getElementById('sd-pop').textContent='–';document.getElementById('sd-mean').textContent='–';
    document.getElementById('sd-n').textContent='–';document.getElementById('sd-note').textContent='Paste at least two numbers.';
    document.title='Standard Deviation Calculator - ToolTide';return;}
  var n=nums.length,sum=0,i;
  for(i=0;i<n;i++)sum+=nums[i];
  var mean=sum/n,ss=0;
  for(i=0;i<n;i++)ss+=(nums[i]-mean)*(nums[i]-mean);
  var sv=ss/(n-1),pv=ss/n,sd=Math.sqrt(sv),pd=Math.sqrt(pv);
  var mn=Math.min.apply(null,nums),mx=Math.max.apply(null,nums);
  var fx=function(x){return Math.round(x*1e6)/1e6;};
  OUT.textContent=fx(sd);
  document.getElementById('sd-pop').textContent=fx(pd);
  document.getElementById('sd-mean').textContent=fx(mean);
  document.getElementById('sd-n').textContent=n+' · '+fx(mn)+'-'+fx(mx);
  document.getElementById('sd-note').textContent='Sample SD divides by n-1 ('+fx(sv)+' variance) and estimates from a sample; population SD divides by n ('+fx(pv)+' variance) when the data IS the whole population. When in doubt with a sample, report the n-1 number.';
  document.title='SD '+fx(sd)+' (n='+n+') - ToolTide';
}
function save(){try{localStorage.setItem('tt_sd',IN.value);}catch(e){}}
IN.addEventListener('input',function(){calc();save();});
var q=qs('d');
if(q!==null){IN.value=q;}
else{try{var mem=localStorage.getItem('tt_sd');if(mem)IN.value=mem;}catch(e){}}
calc();
document.getElementById('sd-share').addEventListener('click',function(){
  var txt='Data summary: mean '+document.getElementById('sd-mean').textContent+', sample SD '+OUT.textContent+', population SD '+document.getElementById('sd-pop').textContent+' (n='+document.getElementById('sd-n').textContent+'). Summarize yours (no sign-up):';
  var url=location.origin+location.pathname+'?d='+encodeURIComponent(IN.value);
  if(navigator.share){navigator.share({title:'Data summary',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-summary','Share this summary');},1500);}
});
})();
</script>
"""

# Concrete: slab dimensions -> cubic yards + ready-mix + bag counts (80/60/40 lb yields).
# Retention hooks: title result hook, tt_conc memory, URL state (?l=&w=&t=&u=), Web Share.
CONCRETE = """<div class="tool" id="tt-cc">
  <div class="fields">
    <div class="field"><label for="cc-l"><span data-i18n="lbl.length">Length</span></label><input type="number" id="cc-l" step="any" min="0" placeholder="10"></div>
    <div class="field"><label for="cc-w"><span data-i18n="lbl.width">Width</span></label><input type="number" id="cc-w" step="any" min="0" placeholder="10"></div>
    <div class="field"><label for="cc-t">Thickness</label><select id="cc-t"><option value="4">4 in - patio/walkway</option><option value="5">5 in</option><option value="6">6 in - driveway</option><option value="8">8 in</option><option value="12">12 in (1 ft)</option></select></div>
    <div class="field"><label for="cc-u"><span data-i18n="lbl.units">Units</span></label><select id="cc-u"><option value="ft">feet</option><option value="m">meters</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cc-out">–</span><span class="result-unit">cubic yards to order</span></div>
  <div class="stats">
    <div class="stat"><b id="cc-ft3">–</b><span>cubic feet / m³</span></div>
    <div class="stat"><b id="cc-b80">–</b><span>80 lb bags</span></div>
    <div class="stat"><b id="cc-b60">–</b><span>60 lb bags</span></div>
  </div>
  <div class="tool-note" id="cc-note"></div>
  <button type="button" class="tool-btn" id="cc-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var L=document.getElementById('cc-l'),W=document.getElementById('cc-w'),T=document.getElementById('cc-t'),U=document.getElementById('cc-u');
var OUT=document.getElementById('cc-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var l=parseFloat(L.value),w=parseFloat(W.value),th=parseFloat(T.value)/12;
  var metric=U.value==='m';
  if(metric){th=parseFloat(T.value)*0.0254;}
  if(!(l>0)||!(w>0)||!(th>0)){OUT.textContent='–';
    document.getElementById('cc-ft3').textContent='–';document.getElementById('cc-b80').textContent='–';
    document.getElementById('cc-b60').textContent='–';document.getElementById('cc-note').textContent='';
    document.title='Concrete Calculator - ToolTide';return;}
  var vol=metric?l*w*th:l*w*th;
  var yd3,volLabel;
  if(metric){yd3=vol*1.30795;volLabel=vol.toFixed(2)+' m³';}
  else{yd3=vol/27;volLabel=Math.round(vol*100)/100+' ft³';}
  var y=Math.ceil(yd3*10)/10;
  OUT.textContent=y.toString();
  document.getElementById('cc-ft3').textContent=volLabel;
  document.getElementById('cc-b80').textContent=metric?'—':(Math.ceil(vol/0.60)).toString();
  document.getElementById('cc-b60').textContent=metric?'—':(Math.ceil(vol/0.45)).toString();
  document.getElementById('cc-note').textContent=metric
    ?(vol.toFixed(2)+' m³ = '+y+' yd³ for the pour. Order 5-10% extra for spillage and uneven subgrade; ready-mix suppliers sell by the partial truck, bags only make sense below ~0.5 m³.')
    :(Math.round(vol*100)/100+' ft³ = '+y+' yd³ ('+volLabel.split(' ')[0]+' / 27). Bag counts assume 0.60 ft³ yield per 80 lb and 0.45 ft³ per 60 lb bag, no waste - add 10% for real jobs. Below about 1 yd³, bags beat ready-mix; above it, order the truck.');
  document.title=y+' yd³ concrete - ToolTide';
}
function save(){try{localStorage.setItem('tt_conc',JSON.stringify({l:L.value,w:W.value,t:T.value,u:U.value}));}catch(e){}}
[L,W].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
[T,U].forEach(function(el){el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['l',L],['w',W],['t',T],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_conc')||'null');if(mem){L.value=mem.l||'';W.value=mem.w||'';T.value=mem.t||'4';U.value=mem.u||'ft';}}catch(e){}}
calc();
document.getElementById('cc-share').addEventListener('click',function(){
  var txt='Concrete estimate: '+OUT.textContent+' yd³ ('+L.value+'x'+W.value+', '+T.value+' in thick). Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?l='+encodeURIComponent(L.value||'')+'&w='+encodeURIComponent(W.value||'')+'&t='+T.value+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Concrete estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

# Slope from two points: decimal + exact fraction, angle, intercept, perpendicular.
# Retention hooks: title result hook, tt_slope memory, URL state (?x1=&y1=&x2=&y2=), Web Share.
SLOPECALC = """<div class="tool" id="tt-sl">
  <div class="fields">
    <div class="field"><label for="sl-x1">x₁</label><input type="number" id="sl-x1" step="any" placeholder="2"></div>
    <div class="field"><label for="sl-y1">y₁</label><input type="number" id="sl-y1" step="any" placeholder="3"></div>
    <div class="field"><label for="sl-x2">x₂</label><input type="number" id="sl-x2" step="any" placeholder="7"></div>
    <div class="field"><label for="sl-y2">y₂</label><input type="number" id="sl-y2" step="any" placeholder="8"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sl-out">–</span><span class="result-unit">slope m</span></div>
  <div class="stats">
    <div class="stat"><b id="sl-frac">–</b><span>as a fraction</span></div>
    <div class="stat"><b id="sl-ang">–</b><span>inclination angle</span></div>
    <div class="stat"><b id="sl-b">–</b><span>y-intercept b</span></div>
  </div>
  <div class="tool-note" id="sl-note"></div>
  <button type="button" class="tool-btn" id="sl-share" data-i18n="share.share-this-line">Share this line</button>
</div>
<script>(function(){
var X1=document.getElementById('sl-x1'),Y1=document.getElementById('sl-y1'),X2=document.getElementById('sl-x2'),Y2=document.getElementById('sl-y2');
var OUT=document.getElementById('sl-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function gcd(x,y){x=Math.abs(Math.round(x*1e6));y=Math.abs(Math.round(y*1e6));while(y){var t=x%y;x=y;y=t;}return x||1;}
function calc(){
  var x1=parseFloat(X1.value),y1=parseFloat(Y1.value),x2=parseFloat(X2.value),y2=parseFloat(Y2.value);
  if([x1,y1,x2,y2].some(isNaN)){OUT.textContent='–';
    document.getElementById('sl-frac').textContent='–';document.getElementById('sl-ang').textContent='–';
    document.getElementById('sl-b').textContent='–';document.getElementById('sl-note').textContent='';
    document.title='Slope Calculator - ToolTide';return;}
  var dx=x2-x1,dy=y2-y1;
  if(dx===0){OUT.textContent='undefined';
    document.getElementById('sl-frac').textContent='vertical';
    document.getElementById('sl-ang').textContent='90°';
    document.getElementById('sl-b').textContent='x = '+x1;
    document.getElementById('sl-note').textContent='Both points share x = '+x1+', so the line is vertical: slope is division by zero, the angle is 90°, and there is no y-intercept (unless the line IS the y-axis).';
    document.title='Vertical line x='+x1+' - ToolTide';return;}
  var m=dy/dx;
  var g=gcd(dy,dx),fn=dy/g,fd=dx/g;
  if(fd<0){fn=-fn;fd=-fd;}
  var frac=(fd===1)?String(fn):(fn+'/'+fd);
  var b=y1-m*x1;
  var ang=Math.atan(m)*180/Math.PI;
  var fx=function(x){return Math.round(x*1e4)/1e4;};
  OUT.textContent=fx(m);
  document.getElementById('sl-frac').textContent=frac;
  document.getElementById('sl-ang').textContent=(Math.round(ang*100)/100)+'°';
  document.getElementById('sl-b').textContent=fx(b);
  var dir=dy===0?'horizontal':(m>0?'rising left to right':'falling left to right');
  document.getElementById('sl-note').textContent='m = ('+fx(dy)+') / ('+fx(dx)+') = '+fx(m)+' ('+frac+'), a '+dir+' line at '+(Math.round(ang*100)/100)+'° from the horizontal. y = '+fx(m)+'x + '+fx(b)+' is the full equation; any perpendicular line has slope '+(m===0?'undefined':fx(-1/m))+'.';
  document.title='Slope '+fx(m)+' ('+frac+') - ToolTide';
}
function save(){try{localStorage.setItem('tt_slope',JSON.stringify({x1:X1.value,y1:Y1.value,x2:X2.value,y2:Y2.value}));}catch(e){}}
[X1,Y1,X2,Y2].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['x1',X1],['y1',Y1],['x2',X2],['y2',Y2]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_slope')||'null');if(mem){X1.value=mem.x1||'';Y1.value=mem.y1||'';X2.value=mem.x2||'';Y2.value=mem.y2||'';}}catch(e){}}
calc();
document.getElementById('sl-share').addEventListener('click',function(){
  var txt='Line through ('+X1.value+', '+Y1.value+') and ('+X2.value+', '+Y2.value+'): slope '+OUT.textContent+', y-intercept '+document.getElementById('sl-b').textContent+'. Find yours (no sign-up):';
  var url=location.origin+location.pathname+'?x1='+encodeURIComponent(X1.value||'')+'&y1='+encodeURIComponent(Y1.value||'')+'&x2='+encodeURIComponent(X2.value||'')+'&y2='+encodeURIComponent(Y2.value||'');
  if(navigator.share){navigator.share({title:'Slope result',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-line','Share this line');},1500);}
});
})();
</script>
"""

# Random team generator: paste names, split into N teams with crypto shuffle, re-shuffle button.
# Retention hooks: title result hook, tt_team memory, URL state (?n=&s=), Web Share.
TEAMGEN = """<div class="tool" id="tt-tg">
  <div class="fields">
    <div class="field"><label for="tg-in">Names (one per line)</label><textarea id="tg-in" rows="5" placeholder="Alice&#10;Bob&#10;Carol&#10;Dave&#10;Eve&#10;Frank"></textarea></div>
    <div class="field"><label for="tg-n">Number of teams</label><input type="number" id="tg-n" step="1" min="2" max="20" placeholder="2"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tg-out">–</span><span class="result-unit" id="tg-u">people per team</span></div>
  <div class="stats">
    <div class="stat"><b id="tg-p">–</b><span>people</span></div>
    <div class="stat"><b id="tg-t">–</b><span>teams</span></div>
    <div class="stat"><b id="tg-bal">–</b><span>balance</span></div>
  </div>
  <div class="tool-note" id="tg-note">Press Shuffle to draw teams.</div>
  <div style="margin-top:10px"><button type="button" class="tool-btn" id="tg-run">Shuffle teams</button></div>
  <div class="tool-note" id="tg-list" style="margin-top:10px"></div>
  <button type="button" class="tool-btn" id="tg-share" data-i18n="share.share-this-draw">Share this draw</button>
</div>
<script>(function(){
var IN=document.getElementById('tg-in'),N=document.getElementById('tg-n');
var OUT=document.getElementById('tg-out');
var lastDraw=null;
function qs(k){return new URLSearchParams(location.search).get(k);}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function names(){
  return IN.value.split(/[\\n\\r]+/).map(function(x){return x.trim();}).filter(function(x){return x.length>0;});
}
function shuffle(a){
  for(var i=a.length-1;i>0;i--){
    var j;
    if(window.crypto&&crypto.getRandomValues){var u=new Uint32Array(1);crypto.getRandomValues(u);j=u[0]%(i+1);}
    else{j=Math.floor(Math.random()*(i+1));}
    var t=a[i];a[i]=a[j];a[j]=t;
  }
  return a;
}
function calc(){
  var ns=names(),n=parseInt(N.value,10);
  var cnt=ns.length;
  if(!cnt||!(n>=2)){OUT.textContent='–';document.getElementById('tg-u').textContent='people per team';
    document.getElementById('tg-p').textContent='–';document.getElementById('tg-t').textContent='–';
    document.getElementById('tg-bal').textContent='–';document.title='Random Team Generator - ToolTide';return;}
  var base=Math.floor(cnt/n),rem=cnt%n;
  document.getElementById('tg-p').textContent=cnt;
  document.getElementById('tg-t').textContent=n;
  document.getElementById('tg-bal').textContent=rem===0?base+' each':rem+' of '+(base+1)+' + '+(n-rem)+' of '+base;
  OUT.textContent=base+(rem?'-'+(base+1):'');
  document.getElementById('tg-u').textContent='people per team';
  document.title=cnt+' people into '+n+' teams - ToolTide';
}
function run(){
  var ns=names(),n=parseInt(N.value,10);
  if(!ns.length||!(n>=2)||n>ns.length){document.getElementById('tg-list').textContent='Enter at least as many names as teams.';return;}
  var pool=shuffle(ns.slice());
  var teams=[],i;
  for(i=0;i<n;i++)teams.push([]);
  var k=0;
  for(i=0;i<pool.length;i++){teams[k%n].push(pool[i]);k++;}
  var html='';
  for(i=0;i<n;i++){
    html+='<div><b>Team '+(i+1)+' ('+teams[i].length+'):</b> '+teams[i].map(esc).join(', ')+'</div>';
  }
  document.getElementById('tg-list').innerHTML=html;
  lastDraw=teams;
  document.getElementById('tg-note').textContent='Drawn with cryptographically secure randomness - every arrangement equally likely, no seeding, no favorites.';
}
function save(){try{localStorage.setItem('tt_team',JSON.stringify({i:IN.value,n:N.value}));}catch(e){}}
IN.addEventListener('input',function(){calc();save();});
N.addEventListener('input',function(){calc();save();});
document.getElementById('tg-run').addEventListener('click',function(){run();save();});
var qn=qs('n'),qs2=qs('s');
if(qn!==null){N.value=qn;}
if(qs2!==null){IN.value=qs2.replace(/\\|/g,String.fromCharCode(10));}
else{try{var mem=JSON.parse(localStorage.getItem('tt_team')||'null');if(mem){IN.value=mem.i||'';N.value=mem.n||'2';}}catch(e){}}
calc();
if(names().length&&parseInt(N.value,10)>=2){run();}
document.getElementById('tg-share').addEventListener('click',function(){
  if(!lastDraw){this.textContent='Shuffle first';var b0=this;setTimeout(function(){b0.textContent=TT('share.share-this-draw','Share this draw');},1500);return;}
  var txt=lastDraw.map(function(t,i){return 'Team '+(i+1)+': '+t.join(', ');}).join(' | ');
  txt+='. Draw yours (no sign-up):';
  var url=location.origin+location.pathname+'?n='+encodeURIComponent(N.value||'')+'&s='+encodeURIComponent(IN.value.split(/[\\n\\r]+/).filter(function(x){return x.trim();}).join('|'));
  if(navigator.share){navigator.share({title:'Team draw',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-draw','Share this draw');},1500);}
});
})();
</script>
"""

# Paint: room geometry minus doors/windows, coats multiplier, coverage-based gallons/liters.
# Retention hooks: title result hook, tt_paint memory, URL state (?l=&w=&h=&d=&n=&c=&u=), Web Share.
PAINTCALC = """<div class="tool" id="tt-pt">
  <div class="fields">
    <div class="field"><label for="pt-l">Room length</label><input type="number" id="pt-l" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="pt-w">Room width</label><input type="number" id="pt-w" step="any" min="0" placeholder="10"></div>
    <div class="field"><label for="pt-h">Wall height</label><input type="number" id="pt-h" step="any" min="0" placeholder="8"></div>
    <div class="field"><label for="pt-d">Doors (21 sq each)</label><input type="number" id="pt-d" step="1" min="0" max="20" placeholder="2"></div>
    <div class="field"><label for="pt-n">Windows (12 sq each)</label><input type="number" id="pt-n" step="1" min="0" max="20" placeholder="2"></div>
    <div class="field"><label for="pt-c"><span data-i18n="lbl.coats">Coats</span></label><select id="pt-c"><option value="1">1</option><option value="2" selected>2</option><option value="3">3</option></select></div>
    <div class="field"><label for="pt-u"><span data-i18n="lbl.units">Units</span></label><select id="pt-u"><option value="ft">feet / gallons</option><option value="m">meters / liters</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pt-out">–</span><span class="result-unit" id="pt-u2">to buy</span></div>
  <div class="stats">
    <div class="stat"><b id="pt-area">–</b><span>paintable area</span></div>
    <div class="stat"><b id="pt-cov">–</b><span>coverage used</span></div>
    <div class="stat"><b id="pt-waste">–</b><span>with 10% rounding</span></div>
  </div>
  <div class="tool-note" id="pt-note"></div>
  <button type="button" class="tool-btn" id="pt-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var L=document.getElementById('pt-l'),W=document.getElementById('pt-w'),H=document.getElementById('pt-h'),DD=document.getElementById('pt-d'),NN=document.getElementById('pt-n'),C=document.getElementById('pt-c'),U=document.getElementById('pt-u');
var OUT=document.getElementById('pt-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var l=parseFloat(L.value),w=parseFloat(W.value),h=parseFloat(H.value);
  var d=Math.max(0,parseInt(DD.value,10)||0),n=Math.max(0,parseInt(NN.value,10)||0),co=parseInt(C.value,10)||1;
  var m=U.value==='m';
  if(!(l>0)||!(w>0)||!(h>0)){OUT.textContent='–';
    document.getElementById('pt-area').textContent='–';document.getElementById('pt-cov').textContent='–';
    document.getElementById('pt-waste').textContent='–';document.getElementById('pt-note').textContent='';
    document.title='Paint Calculator - ToolTide';return;}
  var per,door,win,covTxt,area,paint,unit;
  if(m){
    per=2*(l+w);door=1.9;win=1.1;
    area=Math.max(0,per*h-d*door-n*win)*co;
    paint=area/10;
    covTxt='10 m²/L';unit='L';
    document.getElementById('pt-area').textContent=Math.round(area*100)/100+' m²';
    OUT.textContent=Math.ceil(paint)+' L';
  }else{
    per=2*(l+w);door=21;win=12;
    area=Math.max(0,per*h-d*door-n*win)*co;
    paint=area/350;
    covTxt='350 sq ft/gal';unit='gal';
    document.getElementById('pt-area').textContent=Math.round(area)+' sq ft';
    OUT.textContent=Math.ceil(paint)+' gal';
  }
  document.getElementById('pt-cov').textContent=covTxt;
  var up=Math.ceil(paint*1.1);
  document.getElementById('pt-waste').textContent=(m?up+' L':up+' gal');
  document.getElementById('pt-u2').textContent='to buy ('+(m?'liters':'gallons')+')';
  document.getElementById('pt-note').textContent='Wall area '+document.getElementById('pt-area').textContent+' after '+d+' door(s) and '+n+' window(s), '+co+' coat'+(co>1?'s':'')+' - about '+Math.round(paint*10)/10+' '+unit+' of paint. Buy the rounded-up figure (or +10%) for cut-ins and touch-ups: paint is batch-matched, so running out mid-wall is the expensive mistake.';
  document.title=OUT.textContent+' paint needed - ToolTide';
}
function save(){try{localStorage.setItem('tt_paint',JSON.stringify({l:L.value,w:W.value,h:H.value,d:DD.value,n:NN.value,c:C.value,u:U.value}));}catch(e){}}
[L,W,H,DD,NN].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
[C,U].forEach(function(el){el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['l',L],['w',W],['h',H],['d',DD],['n',NN],['c',C],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_paint')||'null');if(mem){L.value=mem.l||'';W.value=mem.w||'';H.value=mem.h||'';DD.value=mem.d||'';NN.value=mem.n||'';C.value=mem.c||'2';U.value=mem.u||'ft';}}catch(e){}}
calc();
document.getElementById('pt-share').addEventListener('click',function(){
  var txt='Paint estimate for a '+L.value+'x'+W.value+' room: '+OUT.textContent+' ('+document.getElementById('pt-area').textContent+' paintable). Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?l='+encodeURIComponent(L.value||'')+'&w='+encodeURIComponent(W.value||'')+'&h='+encodeURIComponent(H.value||'')+'&d='+encodeURIComponent(DD.value||'')+'&n='+encodeURIComponent(NN.value||'')+'&c='+C.value+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Paint estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

# Tile: area + tile size + waste -> tile count, boxes and coverage check.
# Retention hooks: title result hook, tt_tile memory, URL state (?l=&w=&tw=&th=&b=&u=), Web Share.
TILECALC = """<div class="tool" id="tt-ti">
  <div class="fields">
    <div class="field"><label for="ti-l">Area length</label><input type="number" id="ti-l" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="ti-w">Area width</label><input type="number" id="ti-w" step="any" min="0" placeholder="10"></div>
    <div class="field"><label for="ti-tw">Tile length</label><input type="number" id="ti-tw" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="ti-th">Tile width</label><input type="number" id="ti-th" step="any" min="0" placeholder="12"></div>
    <div class="field"><label for="ti-b">Tiles per box</label><input type="number" id="ti-b" step="1" min="1" placeholder="12"></div>
    <div class="field"><label for="ti-u"><span data-i18n="lbl.units">Units</span></label><select id="ti-u"><option value="in">inches / feet</option><option value="cm">cm / meters</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ti-out">–</span><span class="result-unit">tiles to buy</span></div>
  <div class="stats">
    <div class="stat"><b id="ti-area">–</b><span>area to cover</span></div>
    <div class="stat"><b id="ti-box">–</b><span>boxes</span></div>
    <div class="stat"><b id="ti-wst">–</b><span>includes 10% waste</span></div>
  </div>
  <div class="tool-note" id="ti-note"></div>
  <button type="button" class="tool-btn" id="ti-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var L=document.getElementById('ti-l'),W=document.getElementById('ti-w'),TW=document.getElementById('ti-tw'),TH=document.getElementById('ti-th'),B=document.getElementById('ti-b'),U=document.getElementById('ti-u');
var OUT=document.getElementById('ti-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var l=parseFloat(L.value),w=parseFloat(W.value),tw=parseFloat(TW.value),th=parseFloat(TH.value),bx=Math.max(1,parseInt(B.value,10)||1);
  var metric=U.value==='cm';
  if(!(l>0)||!(w>0)||!(tw>0)||!(th>0)){OUT.textContent='–';
    document.getElementById('ti-area').textContent='–';document.getElementById('ti-box').textContent='–';
    document.getElementById('ti-wst').textContent='–';document.getElementById('ti-note').textContent='';
    document.title='Tile Calculator - ToolTide';return;}
  var area,perTile,areaTxt;
  if(metric){
    area=(l*w);
    perTile=(tw*th)/10000;
    areaTxt=Math.round(area*100)/100+' m²';
  }else{
    area=(l*w);
    perTile=(tw*th)/144;
    areaTxt=Math.round(area*100)/100+' sq ft';
  }
  var need=Math.ceil(area/perTile*1.1);
  var boxes=Math.ceil(need/bx);
  OUT.textContent=need.toString();
  document.getElementById('ti-area').textContent=areaTxt;
  document.getElementById('ti-box').textContent=boxes+' boxes';
  document.getElementById('ti-wst').textContent='+'+(need-Math.ceil(area/perTile))+' spare';
  document.getElementById('ti-note').textContent='A '+areaTxt+' floor at '+tw+'x'+th+' '+(metric?'cm':'in')+' tiles takes '+Math.ceil(area/perTile)+' tiles; with the standard 10% cutting and breakage allowance that is '+need+' - buy '+boxes+' box'+(boxes>1?'es':'')+' of '+bx+'. Keep spare boxes for future repairs: dye lots change.';
  document.title=need+' tiles ('+boxes+' boxes) - ToolTide';
}
function save(){try{localStorage.setItem('tt_tile',JSON.stringify({l:L.value,w:W.value,tw:TW.value,th:TH.value,b:B.value,u:U.value}));}catch(e){}}
[L,W,TW,TH,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
U.addEventListener('change',function(){calc();save();});
var pre=false;
[['l',L],['w',W],['tw',TW],['th',TH],['b',B],['u',U]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_tile')||'null');if(mem){L.value=mem.l||'';W.value=mem.w||'';TW.value=mem.tw||'';TH.value=mem.th||'';B.value=mem.b||'12';U.value=mem.u||'in';}}catch(e){}}
calc();
document.getElementById('ti-share').addEventListener('click',function(){
  var txt='Tile estimate: '+OUT.textContent+' tiles ('+document.getElementById('ti-box').textContent+') for a '+document.getElementById('ti-area').textContent+' area. Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?l='+encodeURIComponent(L.value||'')+'&w='+encodeURIComponent(W.value||'')+'&tw='+encodeURIComponent(TW.value||'')+'&th='+encodeURIComponent(TH.value||'')+'&b='+encodeURIComponent(B.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Tile estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b2=this;setTimeout(function(){b2.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

# Half birthday: birthdate -> next half birthday, days until, exact current age.
# Retention hooks: title result hook (days until), tt_half memory, URL state (?b=), Web Share.
HALFBDAY = """<div class="tool" id="tt-hb">
  <div class="fields">
    <div class="field"><label for="hb-b">Your birthday</label><input type="date" id="hb-b"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hb-out">–</span><span class="result-unit">until your half birthday</span></div>
  <div class="stats">
    <div class="stat"><b id="hb-date">–</b><span>half birthday</span></div>
    <div class="stat"><b id="hb-age">–</b><span>your age now</span></div>
    <div class="stat"><b id="hb-next">–</b><span>next birthday</span></div>
  </div>
  <div class="tool-note" id="hb-note"></div>
  <button type="button" class="tool-btn" id="hb-share" data-i18n="share.share-this-countdown">Share this countdown</button>
</div>
<script>(function(){
var B=document.getElementById('hb-b');
var OUT=document.getElementById('hb-out');
var MO=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
var WD=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var MS=86400000;
function qs(k){return new URLSearchParams(location.search).get(k);}
function halfOf(y,mo,d){
  var ny=mo>=6?y+1:y,nm=(mo+6)%12;
  var dim=new Date(ny,nm+1,0).getDate();
  var nd=Math.min(d,dim);
  return new Date(ny,nm,nd);
}
function ageAt(bd,today){
  var y=today.getFullYear()-bd.getFullYear();
  var m=today.getMonth()-bd.getMonth();
  var d=today.getDate()-bd.getDate();
  if(d<0){m--;d+=new Date(today.getFullYear(),today.getMonth(),0).getDate();}
  if(m<0){y--;m+=12;}
  return {y:y,m:m,d:d};
}
function calc(){
  var v=B.value;
  if(!v){OUT.textContent='–';
    document.getElementById('hb-date').textContent='–';document.getElementById('hb-age').textContent='–';
    document.getElementById('hb-next').textContent='–';document.getElementById('hb-note').textContent='';
    document.title='Half Birthday Calculator - ToolTide';return;}
  var m2=v.match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
  if(!m2){OUT.textContent='–';return;}
  var by=+m2[1],bmo=+m2[2]-1,bd=+m2[3];
  var bd=new Date(by,bmo,bd);
  var today=new Date();today.setHours(0,0,0,0);
  var hb=halfOf(today.getFullYear(),bd.getMonth(),bd.getDate());
  if(hb<today){hb=halfOf(today.getFullYear()+1,bd.getMonth(),bd.getDate());}
  var days=Math.round((hb-today)/MS);
  var isToday=days===0;
  var a=ageAt(bd,today);
  var turning=a.y+0.5;
  OUT.textContent=isToday?'Today!':days+' days';
  document.getElementById('hb-date').textContent=WD[hb.getDay()]+', '+MO[hb.getMonth()]+' '+hb.getDate()+', '+hb.getFullYear();
  document.getElementById('hb-age').textContent=a.y+'y '+a.m+'m '+a.d+'d';
  var nb=new Date(today.getFullYear(),bd.getMonth(),bd.getDate());
  if(nb<today){nb=new Date(today.getFullYear()+1,bd.getMonth(),bd.getDate());}
  document.getElementById('hb-next').textContent=Math.round((nb-today)/MS)+' days';
  document.getElementById('hb-note').textContent=isToday
    ?('Happy half birthday! You are exactly '+a.y+' and a half years old today - the 6-month mirror of '+MO[bd.getMonth()]+' '+bd.getDate()+'.')
    :('Six months after '+MO[bd.getMonth()]+' '+bd.getDate()+' is '+MO[hb.getMonth()]+' '+hb.getDate()+' - when you turn '+Math.floor(turning)+' and a half. End-of-month birthdays clamp to the last day of the shorter month.');
  document.title=(isToday?'Half birthday today!':days+' days to half birthday')+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_half',B.value);}catch(e){}}
B.addEventListener('input',function(){calc();save();});
var q=qs('b');
if(q!==null){B.value=q;}
else{try{var mem=localStorage.getItem('tt_half');if(mem)B.value=mem;}catch(e){}}
calc();
document.getElementById('hb-share').addEventListener('click',function(){
  var txt='My half birthday is '+document.getElementById('hb-date').textContent+' - '+OUT.textContent+'! Find yours (no sign-up):';
  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value||'');
  if(navigator.share){navigator.share({title:'Half birthday',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b2=this;setTimeout(function(){b2.textContent=TT('share.share-this-countdown','Share this countdown');},1500);}
});
})();
</script>
"""

# Ratio solver: A:B = C:x with simplified ratio and percent views.
# Retention hooks: title result hook, tt_ratio memory, URL state (?a=&b=&c=), Web Share.
RATIOCALC = """<div class="tool" id="tt-ra">
  <div class="fields">
    <div class="field"><label for="ra-a">A</label><input type="number" id="ra-a" step="any" placeholder="3"></div>
    <div class="field"><label for="ra-b">B</label><input type="number" id="ra-b" step="any" placeholder="4"></div>
    <div class="field"><label for="ra-c">C</label><input type="number" id="ra-c" step="any" placeholder="x-input like 15"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ra-out">–</span><span class="result-unit" id="ra-u">the missing value</span></div>
  <div class="stats">
    <div class="stat"><b id="ra-simp">–</b><span>A:B simplified</span></div>
    <div class="stat"><b id="ra-dec">–</b><span>A ÷ B</span></div>
    <div class="stat"><b id="ra-pct">–</b><span>A as % of B</span></div>
  </div>
  <div class="tool-note" id="ra-note"></div>
  <button type="button" class="tool-btn" id="ra-share" data-i18n="share.share-this-ratio">Share this ratio</button>
</div>
<script>(function(){
var A=document.getElementById('ra-a'),B=document.getElementById('ra-b'),C=document.getElementById('ra-c');
var OUT=document.getElementById('ra-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function gcd(x,y){x=Math.abs(Math.round(x*1000));y=Math.abs(Math.round(y*1000));while(y){var t=x%y;x=y;y=t;}return x||1;}
function calc(){
  var a=parseFloat(A.value),b=parseFloat(B.value),c=parseFloat(C.value);
  if(!isFinite(a)||!isFinite(b)||a===0||b===0){OUT.textContent='–';
    document.getElementById('ra-simp').textContent='–';document.getElementById('ra-dec').textContent='–';
    document.getElementById('ra-pct').textContent='–';document.getElementById('ra-note').textContent='';
    document.title='Ratio Calculator - ToolTide';return;}
  var dec=a/b;
  document.getElementById('ra-dec').textContent=Math.round(dec*10000)/10000;
  document.getElementById('ra-pct').textContent=Math.round(dec*10000)/100+'%';
  var g=gcd(a,b),sa=a/g,sb=b/g;
  if(sb<0){sa=-sa;sb=-sb;}
  document.getElementById('ra-simp').textContent=sa+':'+sb;
  if(!isFinite(c)){OUT.textContent='–';document.getElementById('ra-note').textContent='';
    document.title='Ratio Calculator - ToolTide';return;}
  var x=c*b/a;
  OUT.textContent=Math.round(x*1e6)/1e6;
  document.getElementById('ra-u').textContent='= C-companion (A:B = C:x)';
  document.getElementById('ra-note').textContent='A:B = C:x means x = C x B / A: '+a+':'+b+' = '+c+':'+Math.round(x*1e6)/1e6+'. Cross-multiply to check: '+a+' x '+Math.round(x*1e6)/1e6+' = '+Math.round(a*x*1000)/1000+' and '+b+' x '+c+' = '+Math.round(b*c*1000)/1000+'.';
  document.title=a+':'+b+' = '+c+':'+Math.round(x*100)/100+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_ratio',JSON.stringify({a:A.value,b:B.value,c:C.value}));}catch(e){}}
[A,B,C].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['a',A],['b',B],['c',C]].forEach(function(z){var v=qs(z[0]);if(v!==null){z[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_ratio')||'null');if(mem){A.value=mem.a||'';B.value=mem.b||'';C.value=mem.c||'';}}catch(e){}}
calc();
document.getElementById('ra-share').addEventListener('click',function(){
  var txt='Ratio solved: '+A.value+':'+B.value+' = '+C.value+':'+OUT.textContent+'. Solve yours (no sign-up):';
  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value||'')+'&b='+encodeURIComponent(B.value||'')+'&c='+encodeURIComponent(C.value||'');
  if(navigator.share){navigator.share({title:'Ratio result',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b2=this;setTimeout(function(){b2.textContent=TT('share.share-this-ratio','Share this ratio');},1500);}
});
})();
</script>
"""

# Calories burned via MET values: activity presets + custom MET, weight, duration.
# Retention hooks: title result hook, tt_cal memory, URL state (?m=&w=&min=&u=), Web Share.
CALBURN = """<div class="tool" id="tt-cb">
  <div class="fields">
    <div class="field"><label for="cb-act">Activity</label><select id="cb-act">
      <option value="3.5">Walking (3 mph)</option>
      <option value="5.0">Brisk walking (4 mph)</option>
      <option value="6.0">Hiking</option>
      <option value="7.0">Jogging</option>
      <option value="9.8">Running (8 mph)</option>
      <option value="7.5">Cycling (12-14 mph)</option>
      <option value="8.0">Swimming laps</option>
      <option value="5.0">Weight training</option>
      <option value="3.0">Yoga</option>
      <option value="10.0">HIIT</option>
      <option value="5.5">Dancing</option>
      <option value="3.0">Housework</option>
      <option value="custom">Custom MET…</option>
    </select></div>
    <div class="field"><label for="cb-m">Custom MET</label><input type="number" id="cb-m" step="0.1" min="0" max="25" placeholder="optional"></div>
    <div class="field"><label for="cb-w">Body weight</label><input type="number" id="cb-w" step="any" min="0" placeholder="70"></div>
    <div class="field"><label for="cb-u"><span data-i18n="lbl.units">Units</span></label><select id="cb-u"><option value="kg">kg</option><option value="lb">lb</option></select></div>
    <div class="field"><label for="cb-min">Duration (minutes)</label><input type="number" id="cb-min" step="1" min="1" max="600" placeholder="30"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cb-out">–</span><span class="result-unit">calories burned</span></div>
  <div class="stats">
    <div class="stat"><b id="cb-rate">–</b><span>kcal per 10 min</span></div>
    <div class="stat"><b id="cb-met">–</b><span>MET used</span></div>
    <div class="stat"><b id="cb-equiv">–</b><span>≈ in food</span></div>
  </div>
  <div class="tool-note" id="cb-note"></div>
  <button type="button" class="tool-btn" id="cb-share" data-i18n="share.share-this-burn">Share this burn</button>
</div>
<script>(function(){
var ACT=document.getElementById('cb-act'),M=document.getElementById('cb-m'),W=document.getElementById('cb-w'),U=document.getElementById('cb-u'),MI=document.getElementById('cb-min');
var OUT=document.getElementById('cb-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var met=ACT.value==='custom'?parseFloat(M.value):parseFloat(ACT.value);
  var w=parseFloat(W.value),min=parseFloat(MI.value);
  if(!(met>0)||!(w>0)||!(min>0)){OUT.textContent='–';
    document.getElementById('cb-rate').textContent='–';document.getElementById('cb-met').textContent='–';
    document.getElementById('cb-equiv').textContent='–';document.getElementById('cb-note').textContent='';
    document.title='Calories Burned Calculator - ToolTide';return;}
  var kg=U.value==='lb'?w/2.2046:w;
  var kcal=met*kg*(min/60);
  OUT.textContent=Math.round(kcal);
  document.getElementById('cb-rate').textContent=Math.round(met*kg/6);
  document.getElementById('cb-met').textContent=Math.round(met*10)/10;
  var eq=Math.round(kcal/95);
  document.getElementById('cb-equiv').textContent=kcal<95?'—':eq+' banana'+(eq>1?'s':'');
  document.getElementById('cb-note').textContent='MET x kg x hours: '+Math.round(met*10)/10+' x '+Math.round(kg*10)/10+'kg x '+(Math.round(min/60*100)/100)+'h = '+Math.round(kcal)+' kcal. MET figures are population averages - intensity, fitness and terrain move your real number by 10-20%.';
  document.title=Math.round(kcal)+' kcal burned - ToolTide';
}
function save(){try{localStorage.setItem('tt_cal',JSON.stringify({a:ACT.value,m:M.value,w:W.value,u:U.value,min:MI.value}));}catch(e){}}
[W,M,MI].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
[ACT,U].forEach(function(el){el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['a',ACT],['m',M],['w',W],['u',U],['min',MI]].forEach(function(z){var v=qs(z[0]);if(v!==null){
  if(z[0]==='a'){for(var i=0;i<ACT.options.length;i++){if(ACT.options[i].value===v){ACT.selectedIndex=i;break;}}}
  else{z[1].value=v;}
  pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_cal')||'null');if(mem){ACT.value=mem.a||'3.5';M.value=mem.m||'';W.value=mem.w||'';U.value=mem.u||'kg';MI.value=mem.min||'';}}catch(e){}}
M.disabled=ACT.value!=='custom';
calc();
document.getElementById('cb-share').addEventListener('click',function(){
  var txt=ACT.options[ACT.selectedIndex].text+' for '+MI.value+' min: '+OUT.textContent+' kcal. Estimate yours (no sign-up):';
  var url=location.origin+location.pathname+'?a='+ACT.value+'&w='+encodeURIComponent(W.value||'')+'&min='+encodeURIComponent(MI.value||'')+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Calories burned',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-burn','Share this burn');},1500);}
});
})();
</script>
"""

# Debt payoff: month-by-month simulation, interest trap detection, total cost.
# Retention hooks: title result hook, tt_debt memory, URL state (?b=&r=&m=), Web Share.
DEBTPAYOFF = """<div class="tool" id="tt-dp">
  <div class="fields">
    <div class="field"><label for="dp-b">Balance ($)</label><input type="number" id="dp-b" step="any" min="0" placeholder="5000"></div>
    <div class="field"><label for="dp-r">APR %</label><input type="number" id="dp-r" step="any" min="0" max="45" placeholder="18"></div>
    <div class="field"><label for="dp-m">Monthly payment ($)</label><input type="number" id="dp-m" step="any" min="0" placeholder="200"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dp-out">–</span><span class="result-unit">until debt-free</span></div>
  <div class="stats">
    <div class="stat"><b id="dp-int">–</b><span>total interest</span></div>
    <div class="stat"><b id="dp-tot">–</b><span>total paid</span></div>
    <div class="stat"><b id="dp-yr">–</b><span>debt-free in</span></div>
  </div>
  <div class="tool-note" id="dp-note"></div>
  <button type="button" class="tool-btn" id="dp-share" data-i18n="share.share-this-payoff-plan">Share this payoff plan</button>
</div>
<script>(function(){
var B=document.getElementById('dp-b'),R=document.getElementById('dp-r'),M=document.getElementById('dp-m');
var OUT=document.getElementById('dp-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function money(n){return '$'+Math.round(n).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
function calc(){
  var b=parseFloat(B.value),apr=parseFloat(R.value),pay=parseFloat(M.value);
  if(!(b>0)||isNaN(apr)||apr<0||!(pay>0)){OUT.textContent='–';
    document.getElementById('dp-int').textContent='–';document.getElementById('dp-tot').textContent='–';
    document.getElementById('dp-yr').textContent='–';document.getElementById('dp-note').textContent='';
    document.title='Debt Payoff Calculator - ToolTide';return;}
  var r=apr/100/12,interest=0,months=0;
  while(b>0&&months<600){
    var add=b*r;
    if(pay<=add&&months>0){
      OUT.textContent='never';
      document.getElementById('dp-int').textContent='grows forever';
      document.getElementById('dp-tot').textContent='—';
      document.getElementById('dp-yr').textContent='—';
      document.getElementById('dp-note').textContent='At '+money(pay)+'/mo the payment does not cover the '+money(add)+' of interest accruing each month - the balance grows. Minimum payments are engineered exactly this way. You need at least '+money(Math.ceil(add*1.05))+'/mo to make progress, and realistically more.';
      document.title='Payment below interest - ToolTide';return;}
    interest+=add;b=b+add-pay;
    if(b<0){interest+=b;b=0;}
    months++;
  }
  if(months>=600){OUT.textContent='600+ mo';document.title='Debt Payoff Calculator - ToolTide';return;}
  var yrs=Math.floor(months/12),mos=months%12;
  OUT.textContent=months+' mo';
  document.getElementById('dp-int').textContent=money(interest);
  document.getElementById('dp-tot').textContent=money(interest+b);
  document.getElementById('dp-yr').textContent=yrs?(yrs+'y '+(mos?mos+'m':'')):mos+' mo';
  var start=parseFloat(B.value)||0;
  var extra=pay*1.1,ei=0,eb=start,em=0;
  while(eb>0&&em<600){var a2=eb*r;ei+=a2;eb=eb+a2-extra;if(eb<0){ei+=eb;eb=0;}em++;}
  var saved=Math.round(interest-ei);
  document.getElementById('dp-note').textContent=money(start)+' at '+apr+'% APR with '+money(pay)+'/mo: '+months+' payments, '+money(interest)+' of interest ('+Math.round(interest/(interest+start)*100)+'% on top of the balance).'+(saved>0?' Paying just '+money(Math.round(pay*0.1))+' more per month clears it '+(months-em)+' months sooner and saves '+money(saved)+'.':' Snowball (smallest balance first) or avalanche (highest APR first) both work - consistency is the variable that pays.');
  document.title='Debt-free in '+months+' months - ToolTide';
}
function save(){try{localStorage.setItem('tt_debt',JSON.stringify({b:B.value,r:R.value,m:M.value}));}catch(e){}}
[B,R,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['b',B],['r',R],['m',M]].forEach(function(z){var v=qs(z[0]);if(v!==null){z[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_debt')||'null');if(mem){B.value=mem.b||'';R.value=mem.r||'';M.value=mem.m||'';}}catch(e){}}
calc();
document.getElementById('dp-share').addEventListener('click',function(){
  var txt='Debt payoff: '+OUT.textContent+' to clear '+B.value+' at '+R.value+'% APR paying '+M.value+'/mo ('+document.getElementById('dp-int').textContent+' interest). Model yours (no sign-up):';
  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value||'')+'&r='+encodeURIComponent(R.value||'')+'&m='+encodeURIComponent(M.value||'');
  if(navigator.share){navigator.share({title:'Debt payoff plan',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b2=this;setTimeout(function(){b2.textContent=TT('share.share-this-payoff-plan','Share this payoff plan');},1500);}
});
})();
</script>
"""

# JSON formatter + validator: pretty print, minify, byte size, node count, error position.
# Retention hooks: title result hook, tt_json memory, URL state for short payloads (?d=), Web Share.
JSONTOOL = """<div class="tool" id="tt-js">
  <div class="fields">
    <div class="field"><label for="js-in">JSON input</label><textarea id="js-in" rows="7" placeholder='{"name":"ToolTide","tools":237,"free":true}'></textarea></div>
    <div class="field"><label for="js-ind">Indent</label><select id="js-ind"><option value="2" selected>2 spaces</option><option value="4">4 spaces</option><option value="tab">Tabs</option></select></div>
  </div>
  <div style="display:flex;gap:8px;margin:8px 0"><button type="button" class="tool-btn" id="js-fmt">Format</button><button type="button" class="tool-btn" id="js-min">Minify</button></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="js-out">–</span><span class="result-unit" id="js-u">status</span></div>
  <div class="stats">
    <div class="stat"><b id="js-size">–</b><span>size</span></div>
    <div class="stat"><b id="js-nodes">–</b><span>keys + values</span></div>
    <div class="stat"><b id="js-depth">–</b><span>max depth</span></div>
  </div>
  <pre id="js-pre" style="white-space:pre-wrap;word-break:break-all;background:rgba(14,116,144,.06);border:1px solid rgba(14,116,144,.2);border-radius:10px;padding:12px;font-size:.85rem;max-height:340px;overflow:auto;margin:10px 0"></pre>
  <div class="tool-note" id="js-note">Everything runs locally in your browser - API keys and payloads never leave this page.</div>
  <button type="button" class="tool-btn" id="js-share" data-i18n="share.share-this-tool">Share this tool</button>
</div>
<script>(function(){
var IN=document.getElementById('js-in'),IND=document.getElementById('js-ind'),PRE=document.getElementById('js-pre');
var OUT=document.getElementById('js-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function count(x,d){
  var n=0,md=d;
  if(x&&typeof x==='object'){
    for(var k in x){n++;var r=count(x[k],d+1);n+=r.n;if(r.d>md)md=r.d;}
  }else{n=1;}
  return {n:n,d:md};
}
function fmt(bytes){return bytes<1024?bytes+' B':(bytes<1048576?(Math.round(bytes/102.4)/10)+' KB':(Math.round(bytes/104857.6)/10)+' MB');}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function render(minify){
  var v=IN.value;
  if(!v.trim()){OUT.textContent='–';document.getElementById('js-u').textContent='status';
    document.getElementById('js-size').textContent='–';document.getElementById('js-nodes').textContent='–';
    document.getElementById('js-depth').textContent='–';PRE.textContent='';
    document.title='JSON Formatter - ToolTide';return;}
  try{
    var o=JSON.parse(v);
    var ind=IND.value==='tab'?'\\t':parseInt(IND.value,10);
    var out=minify?JSON.stringify(o):JSON.stringify(o,null,ind);
    OUT.textContent='Valid JSON';
    document.getElementById('js-u').textContent=minify?'minified':'pretty-printed';
    var bytes=new Blob([v]).size;
    document.getElementById('js-size').textContent=fmt(bytes);
    var c=count(o,0);
    document.getElementById('js-nodes').textContent=c.n;
    document.getElementById('js-depth').textContent=c.d;
    PRE.innerHTML=esc(out);
    document.title='Valid JSON · '+fmt(bytes)+' - ToolTide';
  }catch(e){
    OUT.textContent='Invalid';
    document.getElementById('js-u').textContent='parse error';
    var msg=String(e.message||e);
    var pm=msg.match(/position (\\d+)/);
    var line='';
    if(pm){
      var pos=+pm[1],upto=v.slice(0,pos),ln=upto.split(String.fromCharCode(10)).length;
      line=' near line '+ln+' (char '+pos+')';
    }
    document.getElementById('js-note').textContent='Parse error'+line+': '+msg+' - check trailing commas, single quotes and unquoted keys, the three most common offenders.';
    OUT.textContent='Invalid JSON';
  }
}
function save(){try{localStorage.setItem('tt_json',IN.value.slice(0,20000));}catch(e){}}
IN.addEventListener('input',function(){render(false);save();});
IND.addEventListener('change',function(){render(false);save();});
document.getElementById('js-fmt').addEventListener('click',function(){render(false);save();});
document.getElementById('js-min').addEventListener('click',function(){render(true);save();});
var q=qs('d');
if(q!==null&&q.length<4000){IN.value=q;}
else{try{var mem=localStorage.getItem('tt_json');if(mem)IN.value=mem;}catch(e){}}
render(false);
document.getElementById('js-share').addEventListener('click',function(){
  var txt='Format and validate JSON locally in the browser - nothing uploaded: ';
  var url=location.origin+location.pathname+(IN.value.length<800?'?d='+encodeURIComponent(IN.value):'');
  if(navigator.share){navigator.share({title:'JSON formatter',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-tool','Share this tool');},1500);}
});
})();
</script>
"""

# Base64 encode/decode, UTF-8 safe both directions.
# Retention hooks: title result hook, tt_b64 memory, URL state for short payloads (?d=&m=), Web Share.
BASE64 = """<div class="tool" id="tt-b6">
  <div class="fields">
    <div class="field"><label for="b6-m"><span data-i18n="lbl.mode">Mode</span></label><select id="b6-m"><option value="enc">Encode text → Base64</option><option value="dec">Decode Base64 → text</option></select></div>
    <div class="field"><label for="b6-in"><span data-i18n="lbl.input">Input</span></label><textarea id="b6-in" rows="5" placeholder="Hello, ToolTide!"></textarea></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="b6-out" style="font-size:.95rem;word-break:break-all">–</span><span class="result-unit" id="b6-u">output</span></div>
  <div class="stats">
    <div class="stat"><b id="b6-in-len">–</b><span>input chars</span></div>
    <div class="stat"><b id="b6-out-len">–</b><span>output chars</span></div>
    <div class="stat"><b id="b6-bytes">–</b><span>UTF-8 bytes in</span></div>
  </div>
  <div class="tool-note" id="b6-note">UTF-8 safe: emoji and non-Latin text round-trip correctly in both directions. All local, nothing uploaded.</div>
  <button type="button" class="tool-btn" id="b6-copy">Copy output</button>
</div>
<script>(function(){
var M=document.getElementById('b6-m'),IN=document.getElementById('b6-in');
var OUT=document.getElementById('b6-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function utf8ToB64(s){return btoa(unescape(encodeURIComponent(s)));}
function b64ToUtf8(s){return decodeURIComponent(escape(atob(s)));}
function calc(){
  var v=IN.value;
  if(!v){OUT.textContent='–';document.getElementById('b6-u').textContent='output';
    document.getElementById('b6-in-len').textContent='–';document.getElementById('b6-out-len').textContent='–';
    document.getElementById('b6-bytes').textContent='–';
    document.title='Base64 Encode & Decode - ToolTide';return;}
  var enc=M.value==='enc';
  try{
    var out=enc?utf8ToB64(v):b64ToUtf8(v);
    OUT.textContent=out;
    document.getElementById('b6-u').textContent=enc?'Base64 output':'decoded text';
    document.getElementById('b6-in-len').textContent=v.length;
    document.getElementById('b6-out-len').textContent=out.length;
    var bytes=new Blob([v]).size;
    document.getElementById('b6-bytes').textContent=bytes;
    document.getElementById('b6-note').textContent=enc
      ?(v.length+' chars = '+bytes+' UTF-8 bytes → '+out.length+' Base64 chars (every 3 bytes become 4). Padding = signs make the length a multiple of 4.')
      :('Decoded '+v.length+' Base64 chars back to '+out.length+' chars ('+bytes+'→'+new Blob([out]).size+' bytes). Invalid characters or wrong length would have thrown here.');
    document.title=(enc?'Encoded ':'Decoded ')+out.length+' chars - ToolTide';
  }catch(e){
    OUT.textContent='Invalid Base64';
    document.getElementById('b6-u').textContent='cannot decode';
    document.getElementById('b6-note').textContent='Not valid Base64: the alphabet is A-Z a-z 0-9 + / with = padding, and length must be a multiple of 4. Whitespace is usually the culprit - paste the bare string.';
    document.title='Invalid Base64 - ToolTide';
  }
}
function save(){try{localStorage.setItem('tt_b64',JSON.stringify({m:M.value,i:IN.value.slice(0,10000)}));}catch(e){}}
[M].forEach(function(el){el.addEventListener('change',function(){calc();save();});});
IN.addEventListener('input',function(){calc();save();});
var qm=qs('m'),qd=qs('d');
if(qm!==null){M.value=qm==='dec'?'dec':'enc';}
if(qd!==null&&qd.length<4000){IN.value=qd;}
else{try{var mem=JSON.parse(localStorage.getItem('tt_b64')||'null');if(mem){M.value=mem.m||'enc';IN.value=mem.i||'';}}catch(e){}}
calc();
document.getElementById('b6-copy').addEventListener('click',function(){
  var t=OUT.textContent;
  if(t==='–'||t==='Invalid Base64'){this.textContent='Nothing to copy';var b0=this;setTimeout(function(){b0.textContent='Copy output';},1500);return;}
  var b=this;
  if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent='Copy output';},1500);}).catch(function(){});}
});
})();
</script>
"""

# URL encode/decode with the component-vs-full-URI distinction.
# Retention hooks: title result hook, tt_url memory, URL state for short payloads (?d=&m=), Web Share.
URLCOD = """<div class="tool" id="tt-ue">
  <div class="fields">
    <div class="field"><label for="ue-m"><span data-i18n="lbl.mode">Mode</span></label><select id="ue-m"><option value="enc">Encode</option><option value="dec">Decode</option></select></div>
    <div class="field"><label for="ue-k">Scope</label><select id="ue-k"><option value="component">Component (?q= value style)</option><option value="full">Full URL (keep ://?&)</option></select></div>
    <div class="field"><label for="ue-in"><span data-i18n="lbl.input">Input</span></label><textarea id="ue-in" rows="4" placeholder="café & croissants / menu"></textarea></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ue-out" style="font-size:.95rem;word-break:break-all">–</span><span class="result-unit" id="ue-u">output</span></div>
  <div class="stats">
    <div class="stat"><b id="ue-in-len">–</b><span>input chars</span></div>
    <div class="stat"><b id="ue-out-len">–</b><span>output chars</span></div>
    <div class="stat"><b id="ue-pct">–</b><span>% sequences</span></div>
  </div>
  <div class="tool-note" id="ue-note">Component mode encodes everything a query-string value must have encoded (& = ? / and spaces as %20); full-URL mode keeps the structure characters a URL needs. Runs locally.</div>
  <button type="button" class="tool-btn" id="ue-copy">Copy output</button>
</div>
<script>(function(){
var M=document.getElementById('ue-m'),K=document.getElementById('ue-k'),IN=document.getElementById('ue-in');
var OUT=document.getElementById('ue-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var v=IN.value;
  if(!v){OUT.textContent='–';document.getElementById('ue-u').textContent='output';
    document.getElementById('ue-in-len').textContent='–';document.getElementById('ue-out-len').textContent='–';
    document.getElementById('ue-pct').textContent='–';
    document.title='URL Encoder & Decoder - ToolTide';return;}
  var enc=M.value==='enc',comp=K.value==='component';
  try{
    var out=enc?(comp?encodeURIComponent(v):encodeURI(v)):(comp?decodeURIComponent(v):decodeURI(v));
    OUT.textContent=out;
    document.getElementById('ue-u').textContent=enc?'encoded':'decoded';
    document.getElementById('ue-in-len').textContent=v.length;
    document.getElementById('ue-out-len').textContent=out.length;
    document.getElementById('ue-pct').textContent=(out.match(/%[0-9A-Fa-f]{2}/g)||[]).length;
    document.getElementById('ue-note').textContent=enc
      ?('Encoded '+v.length+' → '+out.length+' chars. Component mode is the right choice for query values (spaces become %20, & and = get escaped so they cannot be read as separators); spaces never become + here - that is the legacy form-encoding style.')
      :('Decoded '+v.length+' → '+out.length+' chars. Malformed sequences like a lone % or a truncated %E2 would throw - the error note explains when that happens.');
    document.title=(enc?'Encoded ':'Decoded ')+out.length+' chars - ToolTide';
  }catch(e){
    OUT.textContent='Malformed input';
    document.getElementById('ue-u').textContent='cannot decode';
    document.getElementById('ue-note').textContent='A % sequence is incomplete or not followed by two hex digits - every % must introduce exactly two hex characters (like %20). Fix or remove the stray percent sign and decode again.';
    document.title='URL Decoder error - ToolTide';
  }
}
function save(){try{localStorage.setItem('tt_url',JSON.stringify({m:M.value,k:K.value,i:IN.value.slice(0,10000)}));}catch(e){}}
[M,K].forEach(function(el){el.addEventListener('change',function(){calc();save();});});
IN.addEventListener('input',function(){calc();save();});
var qm=qs('m'),qk=qs('k'),qd=qs('d');
if(qm!==null){M.value=qm==='dec'?'dec':'enc';}
if(qk!==null){K.value=qk==='full'?'full':'component';}
if(qd!==null&&qd.length<4000){IN.value=qd;}
else{try{var mem=JSON.parse(localStorage.getItem('tt_url')||'null');if(mem){M.value=mem.m||'enc';K.value=mem.k||'component';IN.value=mem.i||'';}}catch(e){}}
calc();
document.getElementById('ue-copy').addEventListener('click',function(){
  var t=OUT.textContent;
  if(t==='–'||t==='Malformed input'){this.textContent='Nothing to copy';var b0=this;setTimeout(function(){b0.textContent='Copy output';},1500);return;}
  var b=this;
  if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){b.textContent=TT('ui.copied','Copied!');setTimeout(function(){b.textContent='Copy output';},1500);}).catch(function(){});}
});
})();
</script>
"""

# JWT decoder: base64url-decode header+payload, humanize exp/iat/nbf timing.
# Retention hooks: title result hook, tt_jwt memory (device-local only; no URL
# param by design - tokens must not travel in links), Web Share of tool link.
JWTDECODE = """<div class="tool" id="tt-jw">
  <div class="fields">
    <div class="field"><label for="jw-in">JWT token (paste the whole thing)</label><textarea id="jw-in" rows="4" placeholder="eyJhbGciOi..."></textarea></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="jw-out">–</span><span class="result-unit" id="jw-u">status</span></div>
  <div class="stats">
    <div class="stat"><b id="jw-alg">–</b><span>algorithm</span></div>
    <div class="stat"><b id="jw-exp">–</b><span>expiry</span></div>
    <div class="stat"><b id="jw-claims">–</b><span>claims</span></div>
  </div>
  <h2 style="margin:12px 0 4px;font-size:1.17rem">Header</h2>
  <pre id="jw-h" style="white-space:pre-wrap;word-break:break-all;background:rgba(14,116,144,.06);border:1px solid rgba(14,116,144,.2);border-radius:10px;padding:12px;font-size:.85rem;max-height:180px;overflow:auto"></pre>
  <h2 style="margin:12px 0 4px;font-size:1.17rem">Payload</h2>
  <pre id="jw-p" style="white-space:pre-wrap;word-break:break-all;background:rgba(14,116,144,.06);border:1px solid rgba(14,116,144,.2);border-radius:10px;padding:12px;font-size:.85rem;max-height:280px;overflow:auto"></pre>
  <div class="tool-note" id="jw-note">Decode only - signatures are never verified here. Tokens stay in your browser: no URL state by design, so a token cannot leak into a shared link.</div>
  <button type="button" class="tool-btn" id="jw-share" data-i18n="share.share-this-tool">Share this tool</button>
</div>
<script>(function(){
var IN=document.getElementById('jw-in');
var OUT=document.getElementById('jw-out');
function b64u(s){
  var t=s.replace(/-/g,'+').replace(/_/g,'/');
  while(t.length%4)t+='=';
  return decodeURIComponent(escape(atob(t)));
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function when(ts){
  var d=new Date(ts*1000);
  var diff=(Date.now()-ts*1000)/1000;
  var abs=Math.abs(diff),f;
  if(abs<60)f=Math.round(abs)+'s';
  else if(abs<3600)f=Math.round(abs/60)+'min';
  else if(abs<86400)f=Math.round(abs/3600)+'h';
  else f=Math.round(abs/86400)+'d';
  return (diff>=0?f+' ago':'in '+f)+' ('+d.toISOString().slice(0,16).replace('T',' ')+')';
}
function calc(){
  var v=IN.value.trim();
  if(!v){OUT.textContent='–';document.getElementById('jw-u').textContent='status';
    document.getElementById('jw-alg').textContent='–';document.getElementById('jw-exp').textContent='–';
    document.getElementById('jw-claims').textContent='–';
    document.getElementById('jw-h').textContent='';document.getElementById('jw-p').textContent='';
    document.title='JWT Decoder - ToolTide';return;}
  var parts=v.split('.');
  if(parts.length<2||!parts[0]||!parts[1]){OUT.textContent='Invalid';document.getElementById('jw-u').textContent='needs 2+ dot-separated parts';
    document.getElementById('jw-note').textContent='A JWT looks like header.payload.signature - three base64url parts separated by dots. Check you pasted the whole token.';
    document.title='JWT Decoder - ToolTide';return;}
  try{
    var h=JSON.parse(b64u(parts[0])),p=JSON.parse(b64u(parts[1]));
    document.getElementById('jw-h').textContent=JSON.stringify(h,null,2);
    document.getElementById('jw-p').textContent=JSON.stringify(p,null,2);
    var alg=h.alg||'?';
    document.getElementById('jw-alg').textContent=alg;
    var keys=Object.keys(p).length;
    document.getElementById('jw-claims').textContent=keys;
    var status;
    if(p.exp){
      var expTxt=when(p.exp);
      document.getElementById('jw-exp').textContent=expTxt;
      var expired=p.exp*1000<Date.now();
      status=expired?'Expired':'Active';
      if(p.nbf&&p.nbf*1000>Date.now())status='Not yet valid';
      document.getElementById('jw-note').textContent='exp '+expTxt+(expired?' - this token no longer authenticates; refresh to get a new one.':' - inside its validity window.')+(p.iat?' Issued '+when(p.iat)+'.':'')+' Signature is NOT checked - decoding proves readability, not authenticity.';
    }else{
      document.getElementById('jw-exp').textContent='none set';
      status='No expiry';
      document.getElementById('jw-note').textContent='No exp claim - some tokens never expire by design (refresh tokens often rotate instead). Signature is NOT checked.';
    }
    OUT.textContent=status;
    document.getElementById('jw-u').textContent=alg+' · '+keys+' claims';
    document.title='JWT '+alg+' · '+status+' - ToolTide';
  }catch(e){
    OUT.textContent='Invalid';document.getElementById('jw-u').textContent='decode failed';
    document.getElementById('jw-note').textContent='The parts are not valid base64url JSON - check for truncated paste or surrounding quotes.';
    document.title='JWT Decoder - ToolTide';
  }
}
function save(){try{localStorage.setItem('tt_jwt',IN.value.slice(0,20000));}catch(e){}}
IN.addEventListener('input',function(){calc();save();});
try{var mem=localStorage.getItem('tt_jwt');if(mem)IN.value=mem;}catch(e){}
calc();
document.getElementById('jw-share').addEventListener('click',function(){
  var txt='Decode JWTs locally - header, payload and expiry timing, nothing uploaded: ';
  var url=location.origin+location.pathname;
  if(navigator.share){navigator.share({title:'JWT decoder',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-tool','Share this tool');},1500);}
});
})();
</script>
"""

# Amortization schedule: payment table with interest/principal split and balance.
# Retention hooks: title result hook, tt_amort memory, URL state (?p=&r=&y=&x=), Web Share.
AMORTIZE = """<div class="tool" id="tt-am">
  <div class="fields">
    <div class="field"><label for="am-p">Loan amount ($)</label><input type="number" id="am-p" step="any" min="0" placeholder="25000"></div>
    <div class="field"><label for="am-r">Annual rate %</label><input type="number" id="am-r" step="any" min="0" max="40" placeholder="7.5"></div>
    <div class="field"><label for="am-y"><span data-i18n="lbl.term-years">Term (years)</span></label><input type="number" id="am-y" step="any" min="0.5" max="40" placeholder="5"></div>
    <div class="field"><label for="am-x">Extra monthly ($)</label><input type="number" id="am-x" step="any" min="0" placeholder="0"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="am-out">–</span><span class="result-unit">monthly payment</span></div>
  <div class="stats">
    <div class="stat"><b id="am-int">–</b><span>total interest</span></div>
    <div class="stat"><b id="am-mo">–</b><span>months to payoff</span></div>
    <div class="stat"><b id="am-sv">–</b><span>saved by extra</span></div>
  </div>
  <div class="tool-note" id="am-note"></div>
  <table id="am-t" style="width:100%;border-collapse:collapse;margin-top:10px;font-size:.88em"></table>
  <button type="button" class="tool-btn" id="am-share" data-i18n="share.share-this-schedule">Share this schedule</button>
</div>
<script>(function(){
var P=document.getElementById('am-p'),R=document.getElementById('am-r'),Y=document.getElementById('am-y'),X=document.getElementById('am-x');
var OUT=document.getElementById('am-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function money(n){return '$'+(Math.round(n*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{minimumFractionDigits:0,maximumFractionDigits:2});}
function calc(){
  var p=parseFloat(P.value),ar=parseFloat(R.value),y=parseFloat(Y.value),x=Math.max(0,parseFloat(X.value)||0);
  if(!(p>0)||!(y>0)||isNaN(ar)||ar<0){OUT.textContent='–';
    document.getElementById('am-int').textContent='–';document.getElementById('am-mo').textContent='–';
    document.getElementById('am-sv').textContent='–';document.getElementById('am-t').innerHTML='';
    document.getElementById('am-note').textContent='';document.title='Amortization Schedule - ToolTide';return;}
  var r=ar/100/12,n0=Math.round(y*12),f=Math.pow(1+r,n0);
  var m=r===0?p/n0:p*r*f/(f-1);
  function run(extra){
    var b=p,int=0,rows=[],mo=0;
    while(b>0&&mo<600){
      var add=b*r,pr=m+extra-add;
      if(pr<=0)return null;
      if(pr>b)pr=b;
      mo++;int+=add;b-=pr;
      if(mo<=12||mo%12===0||b===0)rows.push([mo,m+extra,add,pr,b]);
    }
    return {rows:rows,int:int,mo:mo};
  }
  var base=run(0),alt=run(x);
  OUT.textContent=money(m);
  document.getElementById('am-int').textContent=money(base.int);
  document.getElementById('am-mo').textContent=base.mo;
  if(alt&&x>0){
    document.getElementById('am-sv').textContent=money(base.int-alt.int)+' + '+(base.mo-alt.mo)+'mo';
  }else{document.getElementById('am-sv').textContent='—';}
  document.getElementById('am-note').textContent='First year shown month by month, then each anniversary. Extra principal goes straight to balance - '+(alt&&x>0?(base.mo-alt.mo)+' months and '+money(base.int-alt.int)+' interest shaved.':'enter an extra amount to see the savings.');
  var html='<tr style="text-align:left;border-bottom:2px solid rgba(14,116,144,.4)"><th>#</th><th>Payment</th><th>Interest</th><th>Principal</th><th>Balance</th></tr>';
  base.rows.forEach(function(rw){
    html+='<tr style="border-bottom:1px solid rgba(127,127,127,.2)"><td>'+rw[0]+'</td><td>'+money(rw[1])+'</td><td>'+money(rw[2])+'</td><td>'+money(rw[3])+'</td><td>'+money(rw[4])+'</td></tr>';
  });
  document.getElementById('am-t').innerHTML=html;
  document.title=money(m)+'/mo · '+base.mo+' months - ToolTide';
}
function save(){try{localStorage.setItem('tt_amort',JSON.stringify({p:P.value,r:R.value,y:Y.value,x:X.value}));}catch(e){}}
[P,R,Y,X].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['p',P],['r',R],['y',Y],['x',X]].forEach(function(a){var v=qs(a[0]);if(v!==null){a[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_amort')||'null');if(mem){P.value=mem.p||'';R.value=mem.r||'';Y.value=mem.y||'';X.value=mem.x||'';}}catch(e){}}
calc();
document.getElementById('am-share').addEventListener('click',function(){
  var txt='Loan schedule: '+OUT.textContent+'/mo, '+document.getElementById('am-mo').textContent+' months, '+document.getElementById('am-int').textContent+' interest. Build yours (no sign-up):';
  var url=location.origin+location.pathname+'?p='+encodeURIComponent(P.value||'')+'&r='+encodeURIComponent(R.value||'')+'&y='+encodeURIComponent(Y.value||'')+'&x='+encodeURIComponent(X.value||'');
  if(navigator.share){navigator.share({title:'Amortization schedule',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-schedule','Share this schedule');},1500);}
});
})();
</script>
"""

# CSV to JSON: header row -> object keys, quoted-value aware, delimiter sniffing.
# Retention hooks: title result hook, tt_csv memory (short payloads via ?d=), Web Share.
CSV2JSON = """<div class="tool" id="tt-cj">
  <div class="fields">
    <div class="field"><label for="cj-in">CSV (first row = headers)</label><textarea id="cj-in" rows="7" placeholder="name,role&#10;Ada,engineer&#10;Grace,admiral"></textarea></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cj-out">–</span><span class="result-unit" id="cj-u">records</span></div>
  <div class="stats">
    <div class="stat"><b id="cj-cols">–</b><span>columns</span></div>
    <div class="stat"><b id="cj-delim">–</b><span>delimiter</span></div>
    <div class="stat"><b id="cj-num">–</b><span>numeric cells</span></div>
  </div>
  <pre id="cj-pre" style="white-space:pre-wrap;word-break:break-all;background:rgba(14,116,144,.06);border:1px solid rgba(14,116,144,.2);border-radius:10px;padding:12px;font-size:.85rem;max-height:340px;overflow:auto;margin:10px 0"></pre>
  <div class="tool-note" id="cj-note">Quotes handled: commas inside quoted cells stay put. Numeric cells become JSON numbers. Runs locally.</div>
  <button type="button" class="tool-btn" id="cj-share" data-i18n="share.share-this-converter">Share this converter</button>
</div>
<script>(function(){
var IN=document.getElementById('cj-in');
var OUT=document.getElementById('cj-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function sniff(line){
  var c=(line.match(/,/g)||[]).length,s=(line.match(/;/g)||[]).length,t=(line.match(/\\t/g)||[]).length;
  return t>c&&t>s?'\\t':(s>c?';':',');
}
function splitLine(line,d){
  var out=[],cur='',q=false;
  for(var i=0;i<line.length;i++){
    var ch=line[i];
    if(ch==='\"'){
      if(q&&line[i+1]==='\"'){cur+='\"';i++;}
      else{q=!q;}
    }else if(ch===d&&!q){out.push(cur);cur='';}
    else{cur+=ch;}
  }
  out.push(cur);
  return out.map(function(x){return x.trim();});
}
function calc(){
  var v=IN.value;
  if(!v.trim()){OUT.textContent='–';document.getElementById('cj-u').textContent='records';
    document.getElementById('cj-cols').textContent='–';document.getElementById('cj-delim').textContent='–';
    document.getElementById('cj-num').textContent='–';document.getElementById('cj-pre').textContent='';
    document.title='CSV to JSON - ToolTide';return;}
  var lines=v.split(/[\\r\\n]+/).filter(function(x){return x.trim().length;});
  if(lines.length<2){OUT.textContent='–';document.getElementById('cj-u').textContent='need a header row plus data';
    document.getElementById('cj-pre').textContent='';document.title='CSV to JSON - ToolTide';return;}
  var d=sniff(lines[0]);
  var head=splitLine(lines[0],d);
  var recs=[],nums=0;
  for(var i=1;i<lines.length;i++){
    var cells=splitLine(lines[i],d),o={};
    for(var j=0;j<head.length;j++){
      var c=cells[j]!==undefined?cells[j]:'';
      var num=c!==''&&isFinite(c)&&/^[-+]?\\d*\\.?\\d+(e[-+]?\\d+)?$/i.test(c);
      if(num){o[head[j]]=parseFloat(c);nums++;}else{o[head[j]]=c;}
    }
    recs.push(o);
  }
  OUT.textContent=recs.length;
  document.getElementById('cj-u').textContent='records';
  document.getElementById('cj-cols').textContent=head.length;
  document.getElementById('cj-delim').textContent=d==='\\t'?'tab':d;
  document.getElementById('cj-num').textContent=nums;
  document.getElementById('cj-pre').innerHTML=esc(JSON.stringify(recs,null,2));
  document.getElementById('cj-note').textContent=head.length+' columns × '+recs.length+' rows converted'+(d!==','?' (delimiter '+d+' auto-detected)':'')+'. Header row became object keys; '+nums+' numeric cells were typed as JSON numbers - quote them in the CSV to force strings.';
  document.title=recs.length+' records → JSON - ToolTide';
}
function save(){try{localStorage.setItem('tt_csv',IN.value.slice(0,20000));}catch(e){}}
IN.addEventListener('input',function(){calc();save();});
var q=qs('d');
if(q!==null&&q.length<4000){IN.value=q;}
else{try{var mem=localStorage.getItem('tt_csv');if(mem)IN.value=mem;}catch(e){}}
calc();
document.getElementById('cj-share').addEventListener('click',function(){
  var txt='Convert CSV to JSON locally in the browser: ';
  var url=location.origin+location.pathname+(IN.value.length<800?'?d='+encodeURIComponent(IN.value):'');
  if(navigator.share){navigator.share({title:'CSV to JSON',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-converter','Share this converter');},1500);}
});
})();
</script>
"""

# Online timer: minutes:seconds countdown, wall-clock accurate, title-tab live
# countdown, WebAudio beep at zero. Retention: tab-title countdown + tt_timer.
ONLINETIMER = """<div class="tool" id="tt-tm">
  <div class="fields">
    <div class="field"><label for="tm-m"><span data-i18n="lbl.minutes">Minutes</span></label><input type="number" id="tm-m" step="1" min="0" max="600" placeholder="10"></div>
    <div class="field"><label for="tm-s"><span data-i18n="lbl.seconds">Seconds</span></label><input type="number" id="tm-s" step="1" min="0" max="59" placeholder="0"></div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0" id="tm-presets"></div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="tm-out" style="font-variant-numeric:tabular-nums">10:00</span><span class="result-unit" id="tm-u">ready</span></div>
  <div style="display:flex;gap:8px;margin:8px 0"><button type="button" class="tool-btn" id="tm-go">Start</button><button type="button" class="tool-btn" id="tm-rst">Reset</button></div>
  <div class="tool-note" id="tm-note">The countdown keeps perfect time even if the tab throttles - it measures wall-clock, not ticks. Three beeps sound at zero and the tab title shows the time remaining.</div>
  <button type="button" class="tool-btn" id="tm-share" data-i18n="share.share-this-timer">Share this timer</button>
</div>
<script>(function(){
var M=document.getElementById('tm-m'),S=document.getElementById('tm-s');
var OUT=document.getElementById('tm-out'),U=document.getElementById('tm-u');
var GO=document.getElementById('tm-go');
var endAt=null,iv=null;
function qs(k){return new URLSearchParams(location.search).get(k);}
function pad(n){return String(n).padStart(2,'0');}
function fmt(ms){var t=Math.max(0,Math.ceil(ms/1000));return Math.floor(t/60)+':'+pad(t%60);}
function beep(at,when){setTimeout(function(){try{var c=new (window.AudioContext||window.webkitAudioContext)();var o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);o.frequency.value=880;g.gain.value=.25;o.start();setTimeout(function(){try{o.stop();c.close();}catch(e){}},180);}catch(e){}},when);}
function stop(){if(iv){clearInterval(iv);iv=null;}}
function tick(){
  var left=endAt-Date.now();
  if(left<=0){
    OUT.textContent='0:00';U.textContent='done';
    document.title='⏰ Time is up! - ToolTide';
    beep(0,0);beep(0,350);beep(0,700);
    stop();endAt=null;GO.textContent='Start';
    return;
  }
  OUT.textContent=fmt(left);U.textContent='running';
  document.title=fmt(left)+' - Online Timer - ToolTide';
}
function total(){return (Math.max(0,parseInt(M.value,10)||0))*60+(Math.max(0,parseInt(S.value,10)||0));}
GO.addEventListener('click',function(){
  if(endAt){stop();endAt=null;GO.textContent='Start';U.textContent='paused';return;}
  var t=total()*1000;
  if(t<=0)return;
  endAt=Date.now()+t;
  GO.textContent='Pause';
  tick();stop();iv=setInterval(tick,250);
  try{localStorage.setItem('tt_timer',JSON.stringify({m:M.value,s:S.value}));}catch(e){}
});
document.getElementById('tm-rst').addEventListener('click',function(){
  stop();endAt=null;GO.textContent='Start';
  var t=total();
  OUT.textContent=t?fmt(t*1000):'0:00';U.textContent='ready';
  document.title='Online Timer - ToolTide';
});
[M,S].forEach(function(el){el.addEventListener('input',function(){
  if(!endAt){var t=total();OUT.textContent=t?fmt(t*1000):'0:00';}
  try{localStorage.setItem('tt_timer',JSON.stringify({m:M.value,s:S.value}));}catch(e){}
});});
var presets=[1,3,5,10,15,25,45,60];
var ph='';
presets.forEach(function(p){ph+='<button type="button" class="tool-btn" data-p="'+p+'" style="padding:4px 10px">'+p+' min</button>';});
document.getElementById('tm-presets').innerHTML=ph;
Array.prototype.forEach.call(document.querySelectorAll('#tm-presets button'),function(b){
  b.addEventListener('click',function(){stop();endAt=null;GO.textContent='Start';
    M.value=b.getAttribute('data-p');S.value=0;
    OUT.textContent=fmt(parseInt(b.getAttribute('data-p'),10)*60000);U.textContent='ready';
  });
});
var qm=qs('m'),qs2=qs('s');
if(qm!==null)M.value=qm;
if(qs2!==null)S.value=qs2;
if(qm===null&&qs2===null){try{var mem=JSON.parse(localStorage.getItem('tt_timer')||'null');if(mem){M.value=mem.m||'';S.value=mem.s||'';}}catch(e){}}
var t0=total();
OUT.textContent=t0?fmt(t0*1000):'10:00';
document.getElementById('tm-share').addEventListener('click',function(){
  var txt='Set a timer for '+(total()||600)+' seconds and let the tab title count it down: ';
  var url=location.origin+location.pathname+'?m='+encodeURIComponent(M.value||'')+'&s='+encodeURIComponent(S.value||'');
  if(navigator.share){navigator.share({title:'Online timer',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+url);this.textContent=TT('ui.copied','Copied!');var b2=this;setTimeout(function(){b2.textContent=TT('share.share-this-timer','Share this timer');},1500);}
});
})();
</script>
"""

# Stopwatch: 10ms precision, laps, survives reload via timestamped state.
STOPWATCH = """<div class="tool" id="tt-sw">
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sw-out" style="font-variant-numeric:tabular-nums">0:00.00</span><span class="result-unit" id="sw-u">stopped</span></div>
  <div style="display:flex;gap:8px;margin:8px 0"><button type="button" class="tool-btn" id="sw-go">Start</button><button type="button" class="tool-btn" id="sw-lap">Lap</button><button type="button" class="tool-btn" id="sw-rst">Reset</button></div>
  <div id="sw-laps" style="font-variant-numeric:tabular-nums;font-size:.95rem;margin-top:10px"></div>
  <div class="tool-note" id="sw-note">Measures real elapsed time from timestamps, so it stays accurate through tab throttling and even survives a page reload while running. Laps record splits.</div>
  <button type="button" class="tool-btn" id="sw-share" data-i18n="share.share-this-stopwatch">Share this stopwatch</button>
</div>
<script>(function(){
var OUT=document.getElementById('sw-out'),U=document.getElementById('sw-u'),GO=document.getElementById('sw-go');
var state={acc:0,start:null,laps:[]};
var iv=null;
function pad(n,w){return String(n).padStart(w||2,'0');}
function fmt(ms){var m=Math.floor(ms/60000),s=Math.floor(ms/1000)%60,c=Math.floor(ms/10)%100;return m+':'+pad(s)+'.'+pad(c);}
function render(){
  var t=state.acc+(state.start?Date.now()-state.start:0);
  OUT.textContent=fmt(t);
  U.textContent=state.start?'running':(state.acc?'stopped':'stopped');
  if(state.start)document.title=fmt(t)+' - Stopwatch - ToolTide';
  else document.title='Stopwatch - ToolTide';
}
function save(){try{localStorage.setItem('tt_stopwatch',JSON.stringify(state));}catch(e){}}
function renderLaps(){
  var h='';
  state.laps.forEach(function(l,i){h+='<div>#'+(i+1)+' — '+fmt(l.split)+' <span style="opacity:.6">(total '+fmt(l.total)+')</span></div>';});
  document.getElementById('sw-laps').innerHTML=h;
}
GO.addEventListener('click',function(){
  if(state.start){state.acc+=Date.now()-state.start;state.start=null;GO.textContent='Start';stop();}
  else{state.start=Date.now();GO.textContent='Stop';if(!iv)iv=setInterval(render,43);}
  save();render();
});
document.getElementById('sw-lap').addEventListener('click',function(){
  if(!state.start&&!state.acc)return;
  var t=state.acc+(state.start?Date.now()-state.start:0);
  var prev=state.laps.length?state.laps[state.laps.length-1].total:0;
  state.laps.push({split:t-prev,total:t});
  save();renderLaps();
});
document.getElementById('sw-rst').addEventListener('click',function(){
  stop();state={acc:0,start:null,laps:[]};
  GO.textContent='Start';renderLaps();save();render();
});
function stop(){if(iv){clearInterval(iv);iv=null;}}
try{var m=JSON.parse(localStorage.getItem('tt_stopwatch')||'null');
  if(m&&typeof m==='object'){state={acc:m.acc||0,start:m.start||null,laps:m.laps||[]};
    if(state.start){GO.textContent='Stop';iv=setInterval(render,43);}}}catch(e){}
renderLaps();render();
document.getElementById('sw-share').addEventListener('click',function(){
  var txt='Stopwatch at '+OUT.textContent+' with '+state.laps.length+' laps. Try it (no sign-up): ';
  var url=location.origin+location.pathname;
  if(navigator.share){navigator.share({title:'Stopwatch',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-stopwatch','Share this stopwatch');},1500);}
});
})();
</script>
"""

# Stock average down: blended cost basis after adding shares at a new price.
# Retention hooks: title result hook, tt_stockavg input memory, URL state (?e=&ep=&n=&np=), Web Share.
STOCKAVG = """<div class="tool" id="tt-sa">
  <div class="fields">
    <div class="field"><label for="sa-e">Shares you already own</label><input type="number" id="sa-e" step="any" min="0" placeholder="100"></div>
    <div class="field"><label for="sa-ep">Your average buy price ($)</label><input type="number" id="sa-ep" step="any" min="0" placeholder="50"></div>
    <div class="field"><label for="sa-n">New shares to buy</label><input type="number" id="sa-n" step="any" min="0" placeholder="100"></div>
    <div class="field"><label for="sa-np">New buy price ($)</label><input type="number" id="sa-np" step="any" min="0" placeholder="35"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sa-out">–</span><span class="result-unit" data-i18n="sa.avgcost">new average cost</span></div>
  <div class="stats">
    <div class="stat"><b id="sa-sh">–</b><span data-i18n="sa.shares">total shares</span></div>
    <div class="stat"><b id="sa-inv">–</b><span data-i18n="sa.invested">total invested</span></div>
    <div class="stat"><b id="sa-dr">–</b><span data-i18n="sa.lowered">average lowered by</span></div>
  </div>
  <div class="tool-note" id="sa-note"></div>
  <button type="button" class="tool-btn" id="sa-share" data-i18n="share.share-this-cost-basis">Share this cost basis</button>
</div>
<script>(function(){
var E=document.getElementById('sa-e'),EP=document.getElementById('sa-ep'),N=document.getElementById('sa-n'),NP=document.getElementById('sa-np');
var OUT=document.getElementById('sa-out');
function money(n){return '$'+(Math.round(n*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var e=parseFloat(E.value),ep=parseFloat(EP.value),n=parseFloat(N.value),np=parseFloat(NP.value);
  if(!(e>0)||!(ep>0)||!(n>0)||!(np>0)){OUT.textContent='–';
    ['sa-sh','sa-inv','sa-dr'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('sa-note').textContent='';document.title='Stock Average Calculator - ToolTide';return;}
  var tc=e+n,inv=e*ep+n*np,avg=inv/tc;
  OUT.textContent=money(avg);
  document.getElementById('sa-sh').textContent=tc.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('sa-inv').textContent=money(inv);
  document.getElementById('sa-dr').textContent=ep>avg?((ep-avg)/ep*100).toFixed(1)+'%':'0%';
  var br=ep>avg?'Break-even is now '+money(avg)+' - the stock no longer has to recover to '+money(ep)+' for you to be whole.':
    'The new buy is above your existing average, so the blend moved up to '+money(avg)+'.';
  document.getElementById('sa-note').textContent=tc.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' shares at '+money(avg)+' average = '+money(inv)+' invested. '+br+' Averaging down only pays if the thesis holds - it lowers the bar, it does not remove it.';
  document.title=money(avg)+' avg cost - ToolTide';
}
function save(){try{localStorage.setItem('tt_stockavg',JSON.stringify({e:E.value,ep:EP.value,n:N.value,np:NP.value}));}catch(e){}}
[E,EP,N,NP].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['e',E],['ep',EP],['n',N],['np',NP]].forEach(function(a){var x=qs(a[0]);if(x!==null){a[1].value=x;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_stockavg')||'null');if(mem){E.value=mem.e||'';EP.value=mem.ep||'';N.value=mem.n||'';NP.value=mem.np||'';}}catch(e){}}
calc();
document.getElementById('sa-share').addEventListener('click',function(){
  var txt='Averaging '+E.value+'@'+money(parseFloat(EP.value))+' with '+N.value+'@'+money(parseFloat(NP.value))+' gives '+OUT.textContent+' average. Run your numbers (no sign-up):';
  var url=location.origin+location.pathname+'?e='+encodeURIComponent(E.value||'')+'&ep='+encodeURIComponent(EP.value||'')+'&n='+encodeURIComponent(N.value||'')+'&np='+encodeURIComponent(NP.value||'');
  if(navigator.share){navigator.share({title:'Stock average',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-cost-basis','Share this cost basis');},1500);}
});
})();
</script>
"""

# Position size: % risk per trade -> shares/units, with stop distance and optional R:R.
# Retention hooks: title result hook, tt_possize input memory, URL state (?a=&r=&en=&sl=&tg=), Web Share.
POSSIZE = """<div class="tool" id="tt-ps">
  <div class="fields">
    <div class="field"><label for="ps-a">Account size ($)</label><input type="number" id="ps-a" step="any" min="0" placeholder="10000"></div>
    <div class="field"><label for="ps-r">Risk per trade (%)</label><input type="number" id="ps-r" step="any" min="0" max="100" placeholder="1"></div>
    <div class="field"><label for="ps-en">Entry price ($)</label><input type="number" id="ps-en" step="any" min="0" placeholder="50"></div>
    <div class="field"><label for="ps-sl">Stop loss ($)</label><input type="number" id="ps-sl" step="any" min="0" placeholder="47.5"></div>
    <div class="field"><label for="ps-tg">Target price ($) - optional</label><input type="number" id="ps-tg" step="any" min="0" placeholder="57.5"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ps-out">–</span><span class="result-unit">shares / units</span></div>
  <div class="stats">
    <div class="stat"><b id="ps-risk">–</b><span>risk amount</span></div>
    <div class="stat"><b id="ps-dist">–</b><span>stop distance</span></div>
    <div class="stat"><b id="ps-val">–</b><span>position value</span></div>
    <div class="stat"><b id="ps-rr">–</b><span>reward:risk</span></div>
  </div>
  <div class="tool-note" id="ps-note"></div>
  <button type="button" class="tool-btn" id="ps-share" data-i18n="share.share-this-position-size">Share this position size</button>
</div>
<script>(function(){
var A=document.getElementById('ps-a'),R=document.getElementById('ps-r'),EN=document.getElementById('ps-en'),SL=document.getElementById('ps-sl'),TG=document.getElementById('ps-tg');
var OUT=document.getElementById('ps-out');
function money(n){return '$'+(Math.round(n*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US',{maximumFractionDigits:2});}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),r=parseFloat(R.value),en=parseFloat(EN.value),sl=parseFloat(SL.value),tg=parseFloat(TG.value);
  if(!(a>0)||!(r>0)||!(en>0)||!(sl>0)||sl===en){OUT.textContent='–';
    ['ps-risk','ps-dist','ps-val','ps-rr'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('ps-note').textContent='';document.title='Position Size Calculator - ToolTide';return;}
  var risk=a*r/100,d=Math.abs(en-sl),units=Math.floor(risk/d),val=units*en;
  OUT.textContent=units.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('ps-risk').textContent=money(risk);
  document.getElementById('ps-dist').textContent=(d/en*100).toFixed(2)+'%';
  document.getElementById('ps-val').textContent=money(val);
  var rr='–';
  if(tg>0){var rw=Math.abs(tg-en);rr=(rw/d).toFixed(2)+':1';}
  document.getElementById('ps-rr').textContent=rr;
  document.getElementById('ps-note').textContent='Risking '+money(risk)+' ('+r+'% of '+money(a)+') with a '+(d/en*100).toFixed(2)+'% stop allows '+units.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' shares ('+money(val)+'). Shares are rounded down so real risk stays at or under '+r+'%. '+(tg>0?'At target '+money(tg)+' that is '+rr+' reward vs risk.':'Add a target price to see reward:risk.');
  document.title=units.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' shares - ToolTide';
}
function save(){try{localStorage.setItem('tt_possize',JSON.stringify({a:A.value,r:R.value,en:EN.value,sl:SL.value,tg:TG.value}));}catch(e){}}
[A,R,EN,SL,TG].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['a',A],['r',R],['en',EN],['sl',SL],['tg',TG]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_possize')||'null');if(mem){A.value=mem.a||'';R.value=mem.r||'';EN.value=mem.en||'';SL.value=mem.sl||'';TG.value=mem.tg||'';}}catch(e){}}
calc();
document.getElementById('ps-share').addEventListener('click',function(){
  var txt='Position size: '+OUT.textContent+' shares for '+document.getElementById('ps-risk').textContent+' risk. Plan your trades (no sign-up):';
  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value||'')+'&r='+encodeURIComponent(R.value||'')+'&en='+encodeURIComponent(EN.value||'')+'&sl='+encodeURIComponent(SL.value||'')+'&tg='+encodeURIComponent(TG.value||'');
  if(navigator.share){navigator.share({title:'Position size',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-position-size','Share this position size');},1500);}
});
})();
</script>
"""

# Lottery odds: exact jackpot combinatorics, per-ticket EV and the break-even jackpot.
# Retention hooks: title result hook, tt_lotto input memory, URL state (?g=&j=), Web Share.
LOTTO = """<div class="tool" id="tt-lo">
  <div class="fields">
    <div class="field"><label for="lo-g">Game</label><select id="lo-g">
      <option value="pb">Powerball (5/69 + 1/26)</option>
      <option value="mm">Mega Millions (5/70 + 1/24)</option>
      <option value="em">EuroMillions (5/50 + 2/12)</option>
      <option value="cu">Custom pick numbers</option>
    </select></div>
    <div class="field cu-hide"><label for="lo-p">Ticket price ($)</label><input type="number" id="lo-p" step="any" min="0" placeholder="2"></div>
    <div class="field cu-hide"><label for="lo-j">Jackpot ($)</label><input type="number" id="lo-j" step="any" min="0" placeholder="100000000"></div>
    <div class="field cu-hide" id="lo-c1"><label for="lo-a">Main numbers picked from</label><input type="number" id="lo-a" step="1" min="5" placeholder="49"></div>
    <div class="field cu-hide" id="lo-c2"><label for="lo-b">Bonus balls drawn from (2 = xCHOOSE2)</label><input type="number" id="lo-b" step="1" min="1" placeholder="1"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="lo-out">–</span><span class="result-unit">jackpot odds (1 in …)</span></div>
  <div class="stats">
    <div class="stat"><b id="lo-ev">–</b><span>jackpot EV per ticket</span></div>
    <div class="stat"><b id="lo-be">–</b><span>break-even jackpot</span></div>
    <div class="stat"><b id="lo-any">–</b><span>odds of any prize</span></div>
  </div>
  <div class="tool-note" id="lo-note"></div>
  <button type="button" class="tool-btn" id="lo-share" data-i18n="share.share-these-odds">Share these odds</button>
</div>
<script>(function(){
var G=document.getElementById('lo-g'),P=document.getElementById('lo-p'),J=document.getElementById('lo-j'),A=document.getElementById('lo-a'),B=document.getElementById('lo-b');
var OUT=document.getElementById('lo-out');
function C(n,k){var r=1;for(var i=1;i<=k;i++){r=r*(n-k+i)/i;}return r;}
function money(n){if(n>=1e9)return '$'+(n/1e9).toFixed(2)+'B';if(n>=1e6)return '$'+(n/1e6).toFixed(1)+'M';return '$'+Math.round(n).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');}
function cfg(){var g=G.value;
  if(g==='pb')return{a:69,b:26,bd:1,any:'1 in 24.9'};
  if(g==='mm')return{a:70,b:24,bd:1,any:'1 in 24'};
  if(g==='em')return{a:50,b:12,bd:2,any:'1 in 13'};
  return{a:parseFloat(A.value),b:parseFloat(B.value),bd:parseFloat(B.value)>2?2:1,any:'–'};}
function price(){return G.value==='cu'?parseFloat(P.value):(G.value==='em'?2.5:2);}
function calc(){
  var c=cfg(),pr=price(),j=parseFloat(J.value);
  if(!(c.a>=5)||!(c.b>=1)||!(pr>0)){OUT.textContent='–';
    ['lo-ev','lo-be','lo-any'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('lo-note').textContent='';document.title='Lottery Odds Calculator - ToolTide';return;}
  var bonus=c.bd===2?C(c.b,2):c.b;
  var odds=C(c.a,5)*bonus;
  OUT.textContent=Math.round(odds).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  var ev=j>0?j/odds:0;
  document.getElementById('lo-ev').textContent=j>0?money(ev):'–';
  document.getElementById('lo-be').textContent=money(pr*odds);
  document.getElementById('lo-any').textContent=c.any;
  document.getElementById('lo-note').textContent='Jackpot-only expected value is '+money(ev)+' on a '+money(pr)+' ticket - the jackpot would need to hit '+money(pr*odds)+' just to break even on that line. Lower prize tiers add roughly $0.20-0.35 of EV, but taxes (lump sum is about half the headline) and split jackpots cut the rest. Every combination is equally likely - the machine has no memory of your lucky numbers.';
  document.title='1 in '+Math.round(odds).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' - ToolTide';
}
function cuMode(){var cu=G.value==='cu';
  document.querySelectorAll('.cu-hide').forEach(function(el){el.style.display=cu?'':'none';});}
function save(){try{localStorage.setItem('tt_lotto',JSON.stringify({g:G.value,p:P.value,j:J.value,a:A.value,b:B.value}));}catch(e){}}
[G,P,J,A,B].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
G.addEventListener('change',function(){cuMode();calc();save();});
cuMode();
var pre=false;
[['g',G],['p',P],['j',J],['a',A],['b',B]].forEach(function(x){var v=new URLSearchParams(location.search).get(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(pre){cuMode();}
else{try{var mem=JSON.parse(localStorage.getItem('tt_lotto')||'null');if(mem){G.value=mem.g||'pb';P.value=mem.p||'';J.value=mem.j||'';A.value=mem.a||'';B.value=mem.b||'';cuMode();}}catch(e){}}
calc();
document.getElementById('lo-share').addEventListener('click',function(){
  var txt='Jackpot odds: 1 in '+OUT.textContent+'. Check what a jackpot is really worth (no sign-up):';
  var url=location.origin+location.pathname+'?g='+encodeURIComponent(G.value)+'&j='+encodeURIComponent(J.value||'');
  if(navigator.share){navigator.share({title:'Lottery odds',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-these-odds','Share these odds');},1500);}
});
})();
</script>
"""


# Pomodoro timer: wall-clock phase cycling, daily session count, tab-title countdown.
# Retention hooks: title countdown, tt_pomodoro daily counter + settings memory, WebAudio beep, Web Share.
POMODORO = """<div class="tool" id="tt-po">
  <div class="fields">
    <div class="field"><label for="po-w" data-i18n="pomo.focusmin">Focus minutes</label><input type="number" id="po-w" min="1" max="120" value="25"></div>
    <div class="field"><label for="po-b" data-i18n="pomo.shortbreak">Short break</label><input type="number" id="po-b" min="1" max="60" value="5"></div>
    <div class="field"><label for="po-l" data-i18n="pomo.longbreak">Long break (every 4)</label><input type="number" id="po-l" min="1" max="90" value="15"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="po-out">25:00</span><span class="result-unit" id="po-phase">focus - ready</span></div>
  <div class="stats">
    <div class="stat"><b id="po-today">0</b><span data-i18n="pomo.blocks">focus blocks today</span></div>
    <div class="stat"><b id="po-cycle">1/4</b><span data-i18n="pomo.cycle">cycle position</span></div>
    <div class="stat"><b id="po-total">0</b><span data-i18n="pomo.mins">focus minutes today</span></div>
  </div>
  <div class="tool-note" id="po-note">Auto-runs focus → break cycles. The tab title counts down, so the timer survives tab-switching; progress is saved per day and comes back after a reload.</div>
  <button type="button" class="tool-btn" id="po-go" data-i18n="pomo.start">Start</button>
  <button type="button" class="tool-btn" id="po-reset" data-i18n="pomo.reset">Reset</button>
  <button type="button" class="tool-btn" id="po-share" data-i18n="share.share-today-s-count">Share today's count</button>
</div>
<script>(function(){
var W=document.getElementById('po-w'),B=document.getElementById('po-b'),L=document.getElementById('po-l');
var OUT=document.getElementById('po-out'),PH=document.getElementById('po-phase'),GO=document.getElementById('po-go');
var st={run:false,mode:'work',end:0,left:0,cyc:0};var iv=null;
function today(){var d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();}
function load(){try{var m=JSON.parse(localStorage.getItem('tt_pomodoro')||'null');
  if(m){if(m.d===today()){st.done=m.n||0;st.mins=m.tm||0;}else{st.done=0;st.mins=0;}
    if(m.w)W.value=m.w;if(m.b)B.value=m.b;if(m.l)L.value=m.l;}}catch(e){}st.done=st.done||0;st.mins=st.mins||0;}
function save(){try{localStorage.setItem('tt_pomodoro',JSON.stringify({d:today(),n:st.done,tm:st.mins,w:W.value,b:B.value,l:L.value}));}catch(e){}}
function mm(n){return Math.max(0,Math.round(n));}
function fmt(s){var m=Math.floor(s/60),x=Math.floor(s%60);return m+':'+(x<10?'0':'')+x;}
function beep(){try{var c=new (window.AudioContext||window.webkitAudioContext)();
  [0,350,700].forEach(function(t){var o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);
  o.frequency.value=880;o.type='sine';g.gain.value=.12;o.start(c.currentTime+t/1000);o.stop(c.currentTime+t/1000+.22);});}catch(e){}}
function render(){var s=st.run?(st.end-Date.now())/1000:st.left;
  OUT.textContent=fmt(s);
  var label=(st.mode==='work'?TT('pomo.focus','focus'):TT('pomo.break','break'))+(st.run?'':' '+TT('pomo.paused','- paused'));
  PH.textContent=label;
  document.title=(st.run?'🍅 ':'⏸ ')+fmt(s)+' '+(st.mode==='work'?TT('pomo.titlefocus','Focus'):TT('pomo.titlebreak','Break'))+' - ToolTide';
  document.getElementById('po-today').textContent=st.done;
  document.getElementById('po-cycle').textContent=(st.cyc%4+1)+'/4';
  document.getElementById('po-total').textContent=st.mins;}
function next(){if(st.mode==='work'){st.done++;st.mins+=parseInt(W.value)||25;}
  st.cyc=st.mode==='work'?st.cyc+1:st.cyc;
  var wasWork=st.mode==='work';
  st.mode=wasWork?(st.cyc%4===0?'long':'break'):'work';
  var mins=st.mode==='work'?parseInt(W.value):(st.mode==='long'?parseInt(L.value):parseInt(B.value));
  st.left=(mins||25)*60;st.end=Date.now()+st.left*1000;
  beep();save();render();arm();}
function arm(){if(iv)clearInterval(iv);iv=null;
  if(!st.run)return;iv=setInterval(function(){
    var s=(st.end-Date.now())/1000;
    if(s<=0){next();}else{OUT.textContent=fmt(s);
      document.title='🍅 '+fmt(s)+' '+(st.mode==='work'?TT('pomo.titlefocus','Focus'):TT('pomo.titlebreak','Break'))+' - ToolTide';}},250);}
window.addEventListener('load',render);
GO.addEventListener('click',function(){
  if(st.run){st.run=false;st.left=(st.end-Date.now())/1000;GO.textContent=TT('pomo.start','Start');}
  else{if(!st.left||st.left<=0){var mins=(st.mode==='work'?parseInt(W.value):parseInt(B.value))||25;st.left=mins*60;}
    st.end=Date.now()+st.left*1000;st.run=true;GO.textContent=TT('pomo.pause','Pause');arm();}
  render();});
document.getElementById('po-reset').addEventListener('click',function(){
  if(iv)clearInterval(iv);iv=null;st.run=false;st.mode='work';st.cyc=0;
  st.left=(parseInt(W.value)||25)*60;GO.textContent=TT('pomo.start','Start');save();render();});
document.getElementById('po-share').addEventListener('click',function(){
  var txt=st.done+' pomodoros ('+st.mins+' focus minutes) today. Start your own timer (no sign-up):';
  var url=location.origin+location.pathname;
  if(navigator.share){navigator.share({title:'Pomodoro',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent="Share today's count";},1500);}});
[W,B,L].forEach(function(el){el.addEventListener('input',function(){if(!st.run){st.mode='work';st.left=(parseInt(W.value)||25)*60;render();}save();});});
load();st.left=(parseInt(W.value)||25)*60;render();
})();
</script>
"""

# Password strength: entropy math + pattern penalties + honest crack-time table.
# Deliberately no password memory/URL state (a password must never persist or travel).
# Retention hooks: title score hook, Web Share (score only, never the password).
PASSSTRENGTH = """<div class="tool" id="tt-pw">
  <div class="fields">
    <div class="field"><label for="pw-in">Type a password to test</label><input type="password" id="pw-in" autocomplete="off" spellcheck="false" placeholder="try something…"></div>
    <div class="field"><label for="pw-show">Show it</label><input type="checkbox" id="pw-show"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pw-out">–</span><span class="result-unit">bits of entropy</span></div>
  <div class="stats">
    <div class="stat"><b id="pw-verdict">–</b><span>verdict</span></div>
    <div class="stat"><b id="pw-on">–</b><span>vs online attack (100/s)</span></div>
    <div class="stat"><b id="pw-gpu">–</b><span>vs offline GPU (10^10/s)</span></div>
  </div>
  <div class="tool-note" id="pw-note"></div>
  <button type="button" class="tool-btn" id="pw-share" data-i18n="share.share-the-score-not-the-password">Share the score (not the password)</button>
</div>
<script>(function(){
var IN=document.getElementById('pw-in'),OUT=document.getElementById('pw-out');
var COMMON=['password','passw0rd','qwerty','letmein','welcome','admin','login','dragon','monkey','iloveyou','football','baseball','abc123','123456','12345678','1234567890','sunshine','princess','master','shadow','superman','trustno1','starwars','whatever','password1','azerty','zxcvbn','asdfgh','qazwsx','michael','jennifer','jordan','harley','ranger','hunter','summer','ashley'];
function bits2(b){if(b<=0)return 'instantly';
  var units=[[1,'second'],[60,'minute'],[3600,'hour'],[86400,'day'],[2592000,'month'],[31536000,'year']];
  if(b<20)return 'seconds';
  var secs=Math.pow(2,b-1);
  if(secs/31536000>1e9)return 'billions of years';
  if(secs/31536000>1000)return 'thousands of years';
  for(var i=units.length-1;i>=0;i--){if(secs>=units[i][0]){var v=secs/units[i][0];
    return (v>=10?Math.round(v):v.toFixed(1))+' '+units[i][1]+(v>=2?'s':'');}}
  return 'instantly';}
function calc(){
  var pw=IN.value||'';
  if(!pw){OUT.textContent='–';document.getElementById('pw-verdict').textContent='–';
    document.getElementById('pw-on').textContent='–';document.getElementById('pw-gpu').textContent='–';
    document.getElementById('pw-note').textContent='';document.title='Password Strength Checker - ToolTide';return;}
  var cs=0;if(/[a-z]/.test(pw))cs+=26;if(/[A-Z]/.test(pw))cs+=26;if(/[0-9]/.test(pw))cs+=10;
  if(/[^a-zA-Z0-9 ]/.test(pw))cs+=33;if(/ /.test(pw))cs+=1;
  var bits=pw.length*(cs>1?Math.log2(cs):0);
  var notes=[],norm=pw.toLowerCase().replace(/[@4]/g,'a').replace(/0/g,'o').replace(/1/g,'l').replace(/3/g,'e').replace(/5/g,'s');
  var hits=COMMON.filter(function(w){return norm.indexOf(w)>=0;});
  if(hits.length){bits=Math.min(bits,14);notes.push('contains the dictionary word "'+hits[0]+'" - crackers try these first');}
  if(/(.)\\1{2,}/.test(pw)){bits-=8;notes.push('repeated characters add almost nothing');}
  if(/(0123|1234|2345|3456|4567|5678|6789|abcd|bcde|cdef|qwer|asdf|zxcv)/i.test(pw)){bits-=8;notes.push('keyboard or number sequences are guessed early');}
  if(/^\\d{4,8}$/.test(pw)&&/^(19|20)\\d\\d/.test(pw)){bits-=8;notes.push('looks like a year/date - dates are brute-forced first');}
  bits=Math.max(4,bits);
  OUT.textContent=Math.round(bits);
  var verdict=bits<28?'Very weak':bits<36?'Weak':bits<60?'Fair':bits<80?'Strong':'Excellent';
  document.getElementById('pw-verdict').textContent=verdict;
  document.getElementById('pw-on').textContent=bits2(bits/2);
  document.getElementById('pw-gpu').textContent=bits2(bits-33.2>0?bits-33.2:1);
  document.getElementById('pw-note').textContent=(notes.length?'Deductions: '+notes.join('; ')+'. ':'')+
    'Entropy is length × log2(character pool) - length beats complexity: "correct-horse-battery" style passphrases outrun symbol soup. The real killer is reuse: one breached site hands attackers every account that shares the password. Nothing you type here is stored, sent or remembered - check and close.';
  document.title=Math.round(bits)+' bits - '+verdict+' - ToolTide';
}
IN.addEventListener('input',calc);
document.getElementById('pw-show').addEventListener('change',function(){IN.type=this.checked?'text':'password';});
document.getElementById('pw-show').addEventListener('change',calc);
calc();
document.getElementById('pw-share').addEventListener('click',function(){
  if(!IN.value)return;
  var txt='My test password scores '+OUT.textContent+' bits ('+document.getElementById('pw-verdict').textContent+') - it would survive an offline GPU attack for '+document.getElementById('pw-gpu')+'. Check yours (nothing is stored):';
  var url=location.origin+location.pathname;
  if(navigator.share){navigator.share({title:'Password strength',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-the-score-not-the-password','Share the score (not the password)');},1500);}
});
})();
</script>
"""

# Crypto profit: fee-aware P/L, ROI and the exact break-even sell price.
# Retention hooks: title result hook, tt_cryptoprofit input memory, URL state (?b=&s=&q=&f=), Web Share.
CRYPTOPROFIT = """<div class="tool" id="tt-cp">
  <div class="fields">
    <div class="field"><label for="cp-b">Buy price ($ per coin)</label><input type="number" id="cp-b" step="any" min="0" placeholder="60000"></div>
    <div class="field"><label for="cp-s">Sell price ($ per coin)</label><input type="number" id="cp-s" step="any" min="0" placeholder="65000"></div>
    <div class="field"><label for="cp-q">Quantity (coins)</label><input type="number" id="cp-q" step="any" min="0" placeholder="0.5"></div>
    <div class="field"><label for="cp-f">Fee per side (%)</label><input type="number" id="cp-f" step="any" min="0" max="10" placeholder="0.1"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cp-out">–</span><span class="result-unit">net profit / loss</span></div>
  <div class="stats">
    <div class="stat"><b id="cp-inv">–</b><span>invested (incl. buy fee)</span></div>
    <div class="stat"><b id="cp-ret">–</b><span>returned (after sell fee)</span></div>
    <div class="stat"><b id="cp-roi">–</b><span>ROI</span></div>
    <div class="stat"><b id="cp-be">–</b><span>break-even sell price</span></div>
  </div>
  <div class="tool-note" id="cp-note"></div>
  <button type="button" class="tool-btn" id="cp-share" data-i18n="share.share-this-trade-math">Share this trade math</button>
</div>
<script>(function(){
var B=document.getElementById('cp-b'),S=document.getElementById('cp-s'),Q=document.getElementById('cp-q'),F=document.getElementById('cp-f');
var OUT=document.getElementById('cp-out');
function money(n){return '$'+(Math.abs(n)>=100?Math.round(n).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US'):(Math.round(n*100)/100).toString());}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var b=parseFloat(B.value),s=parseFloat(S.value),q=parseFloat(Q.value),f=parseFloat(F.value);
  if(isNaN(f)||f<0)f=0;
  if(!(b>0)||!(q>0)){OUT.textContent='–';
    ['cp-inv','cp-ret','cp-roi','cp-be'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('cp-note').textContent='';document.title='Crypto Profit Calculator - ToolTide';return;}
  var inv=b*q*(1+f/100),ret=(s>0?s*q*(1-f/100):0),pl=ret-inv;
  var roi=pl/inv*100,be=b*(1+f/100)/(1-f/100);
  OUT.textContent=(pl>=0?'+':'−')+money(Math.abs(pl)).replace('$','$');
  document.getElementById('cp-inv').textContent=money(inv);
  document.getElementById('cp-ret').textContent=s>0?money(ret):'–';
  document.getElementById('cp-roi').textContent=(pl>=0?'+':'')+roi.toFixed(2)+'%';
  document.getElementById('cp-be').textContent='$'+(Math.round(be*100)/100);
  document.getElementById('cp-note').textContent='Fees hit both sides: '+money(b*q)+' in at '+f+'% costs '+money(inv)+' all-in, so break-even is not your buy price - it is $'+(Math.round(be*100)/100)+', '+(f>0?((be/b-1)*100).toFixed(2)+'% above it. ':'')+ 'Round-trip fees on frequent trades are the silent position-sizer: 0.1% twice on 50 trades a year is ~10% gone.';
  document.title=(pl>=0?'+':'')+roi.toFixed(1)+'% ROI - ToolTide';
}
function save(){try{localStorage.setItem('tt_cryptoprofit',JSON.stringify({b:B.value,s:S.value,q:Q.value,f:F.value}));}catch(e){}}
[B,S,Q,F].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['b',B],['s',S],['q',Q],['f',F]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_cryptoprofit')||'null');if(mem){B.value=mem.b||'';S.value=mem.s||'';Q.value=mem.q||'';F.value=mem.f||'';}}catch(e){}}
calc();
document.getElementById('cp-share').addEventListener('click',function(){
  var txt='Trade math: '+OUT.textContent+' ('+document.getElementById('cp-roi').textContent+' ROI) after fees, break-even at '+document.getElementById('cp-be').textContent+'. Run yours (no sign-up):';
  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value||'')+'&s='+encodeURIComponent(S.value||'')+'&q='+encodeURIComponent(Q.value||'')+'&f='+encodeURIComponent(F.value||'');
  if(navigator.share){navigator.share({title:'Crypto profit',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-trade-math','Share this trade math');},1500);}
});
})();
</script>
"""

# Pet age: dog/cat calendar age -> human-equivalent years (vet growth tables, size-aware for dogs).
# Retention hooks: title result hook, tt_petage memory, URL state (?y=&m=&z=), Web Share.
PETAGE = """<div class="tool" id="tt-pa">
  <div class="fields">
    <div class="field"><label for="pa-y">Age - years</label><input type="number" id="pa-y" step="1" min="0" max="35" placeholder="4"></div>
    <div class="field"><label for="pa-m">+ months</label><input type="number" id="pa-m" step="1" min="0" max="11" placeholder="6"></div>
    <div class="field" id="pa-zw"><label for="pa-z">Size (dogs only)</label><select id="pa-z"><option value="s">Small (under 9 kg / 20 lb)</option><option value="m" selected>Medium (9-22 kg / 20-50 lb)</option><option value="l">Large (over 22 kg / 50 lb)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pa-out">–</span><span class="result-unit">in human years</span></div>
  <div class="stats">
    <div class="stat"><b id="pa-stage">–</b><span>life stage</span></div>
    <div class="stat"><b id="pa-lifes">–</b><span>typical lifespan</span></div>
    <div class="stat"><b id="pa-pct">–</b><span>of life lived (est.)</span></div>
  </div>
  <div class="tool-note" id="pa-note"></div>
  <button type="button" class="tool-btn" id="pa-share" data-i18n="share.share-this-pet-s-age">Share this pet's age</button>
</div>
<script>(function(){
var Y=document.getElementById('pa-y'),M=document.getElementById('pa-m'),Z=document.getElementById('pa-z');
var OUT=document.getElementById('pa-out');
var SP='__SPECIES__';
var TABLE_DOG={s:[[1,15],[2,24],[3,28],[4,32],[5,36],[6,40],[7,44],[8,48],[9,52],[10,56],[11,60],[12,64],[13,68],[14,72],[15,76],[16,80]],
  m:[[1,15],[2,24],[3,28],[4,32],[5,36],[6,42],[7,47],[8,51],[9,56],[10,60],[11,65],[12,69],[13,74],[14,78],[15,83],[16,87]],
  l:[[1,15],[2,24],[3,29],[4,34],[5,39],[6,45],[7,50],[8,55],[9,61],[10,66],[11,72],[12,77],[13,82],[14,88],[15,93],[16,99]]};
var TABLE_CAT=[[1,15],[2,24],[3,28],[4,32],[5,36],[6,40],[7,44],[8,48],[9,52],[10,56],[11,60],[12,64],[13,68],[14,72],[15,76],[16,80],[18,88],[20,96]];
function qs(k){return new URLSearchParams(location.search).get(k);}
function stage(h){return h<13?'baby/child':h<20?'teen':h<35?'young adult':h<56?'adult':h<75?'senior':'geriatric';}
function calc(){
  var y=parseFloat(Y.value),m=parseFloat(M.value)||0;
  if(SP==='cat'){document.getElementById('pa-zw').style.display='none';}
  if(isNaN(y)||y<0||y>35){OUT.textContent='–';
    ['pa-stage','pa-lifes','pa-pct'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('pa-note').textContent='';document.title=(SP==='dog'?'Dog':'Cat')+' Age Calculator - ToolTide';return;}
  var a=y+m/12,h=0;
  if(SP==='dog'){var t=TABLE_DOG[Z.value]||TABLE_DOG.m;
    if(a<=0.5)h=Math.max(1,Math.round(a*30));
    else if(a<1)h=15;
    else if(a>=16)h=t[15][1]+Math.round((a-16)*(Z.value==='l'?7:5));
    else{for(var i=0;i<t.length-1;i++){if(a>=t[i][0]&&a<t[i+1][0]){h=Math.round(t[i][1]+(t[i+1][1]-t[i][1])*(a-t[i][0]));break;}}}
    var lifes=Z.value==='s'?14:Z.value==='m'?13:11;
    document.getElementById('pa-lifes').textContent=lifes+' yrs';
    document.getElementById('pa-pct').textContent=Math.min(100,Math.round(a/lifes*100))+'%';
    var seven=Math.round(a*7);
    document.getElementById('pa-note').textContent='Human-equivalent age: '+h+' years (veterinary growth table, size-adjusted). The old "multiply by 7" rule would say '+seven+' - it fails because '+ (SP==='dog'?'dogs mature ~15 human years in year one, then slow down, and large breeds age faster than small ones.':'pets mature ~15 human years in year one, then slow down.')+' Senior screening checkups are recommended from about age 7 (human mid-40s).';}
  else{if(a<=0.5)h=Math.max(1,Math.round(a*30));
    else if(a<1)h=15;
    else if(a>=20)h=96+Math.round((a-20)*4);
    else{for(var j=0;j<TABLE_CAT.length-1;j++){if(a>=TABLE_CAT[j][0]&&a<TABLE_CAT[j+1][0]){h=Math.round(TABLE_CAT[j][1]+(TABLE_CAT[j+1][1]-TABLE_CAT[j][1])*(a-TABLE_CAT[j][0]));break;}}}
    document.getElementById('pa-lifes').textContent='12-18 yrs';
    document.getElementById('pa-pct').textContent=Math.min(100,Math.round(a/15*100))+'%';
    document.getElementById('pa-note').textContent='Human-equivalent age: '+h+' years (veterinary association table). Cats race through year one (~15 human years), hit their mid-twenties by age two, then age ~4 human years per calendar year. Indoor cats typically outlive outdoor cats by years - and from about age 10 (human late-50s), twice-yearly vet visits pay for themselves.';}
  OUT.textContent=h;
  document.getElementById('pa-stage').textContent=stage(h);
  document.title=OUT.textContent+' human yrs - ToolTide';
}
function save(){try{localStorage.setItem('tt_petage',JSON.stringify({sp:SP,y:Y.value,m:M.value,z:Z.value}));}catch(e){}}
[Y,M,Z].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['y',Y],['m',M],['z',Z]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_petage')||'null');if(mem&&mem.sp===SP){Y.value=mem.y||'';M.value=mem.m||'';if(mem.z)Z.value=mem.z;}}catch(e){}}
calc();
document.getElementById('pa-share').addEventListener('click',function(){
  var txt='A '+Y.value+'-year-old '+(SP==='dog'?'dog':'cat')+' is about '+OUT.textContent+' in human years. Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?y='+encodeURIComponent(Y.value||'')+'&m='+encodeURIComponent(M.value||'');
  if(navigator.share){navigator.share({title:'Pet age',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent="Share this pet's age";},1500);}
});
})();
</script>
"""

# Flesch reading ease + grade level: syllable-aware scoring for writers and students.
# Retention hooks: title score hook, tt_flesch text memory (capped), Web Share.
FLESCH = """<div class="tool" id="tt-fl">
  <div class="fields">
    <div class="field" style="flex:1 1 100%"><label for="fl-in">Paste text to score</label><textarea id="fl-in" rows="7" style="width:100%;box-sizing:border-box" placeholder="Paste a paragraph, an article intro or your essay here…"></textarea></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fl-out">–</span><span class="result-unit">reading ease</span></div>
  <div class="stats">
    <div class="stat"><b id="fl-grade">–</b><span>grade level</span></div>
    <div class="stat"><b id="fl-words">–</b><span>words</span></div>
    <div class="stat"><b id="fl-sents">–</b><span>sentences</span></div>
    <div class="stat"><b id="fl-wps">–</b><span>words / sentence</span></div>
  </div>
  <div class="tool-note" id="fl-note"></div>
  <button type="button" class="tool-btn" id="fl-share" data-i18n="share.share-this-readability-score">Share this readability score</button>
</div>
<script>(function(){
var IN=document.getElementById('fl-in'),OUT=document.getElementById('fl-out');
function syl(w){w=w.toLowerCase().replace(/[^a-z]/g,'');if(!w)return 0;
  if(w.length<=3)return 1;
  w=w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'');
  var m=w.match(/[aeiouy]{1,2}/g);return m?m.length:1;}
function calc(){
  var t=IN.value||'';
  if(!t.trim()){OUT.textContent='–';
    ['fl-grade','fl-words','fl-sents','fl-wps'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('fl-note').textContent='';document.title='Flesch Reading Ease Calculator - ToolTide';return;}
  var words=t.trim().split(/\\s+/).filter(function(w){return /[a-z0-9]/i.test(w);});
  var sents=t.split(/[.!?]+(?:\\s|$)/).filter(function(s){return s.trim().length>0;});
  var W=words.length,S=Math.max(1,sents.length),SY=0;
  words.forEach(function(w){SY+=syl(w);});
  var re=206.835-1.015*(W/S)-84.6*(SY/W);
  var gl=0.39*(W/S)+11.8*(SY/W)-15.59;
  OUT.textContent=Math.max(0,Math.round(re));
  document.getElementById('fl-grade').textContent=Math.max(1,Math.round(gl*10)/10);
  document.getElementById('fl-words').textContent=W.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('fl-sents').textContent=S;
  document.getElementById('fl-wps').textContent=Math.round(W/S*10)/10;
  var band=re>=90?'very easy (5th grade)':re>=80?'easy (6th grade)':re>=70?'fairly easy (7th grade)':re>=60?'plain English (8-9th grade)':re>=50?'fairly difficult (10-12th)':re>=30?'difficult (college)':'very difficult (graduate)';
  document.getElementById('fl-note').textContent='Reading ease '+Math.round(re)+'/100 = '+band+'. Most web content aims for 60-70: shorter sentences move the score more than shorter words, because 1.015×(words per sentence) outweighs the syllable term. The score is a compass, not a rule - legal text and children\\'s books rightly live at opposite ends.';
  document.title='Reading ease '+Math.round(re)+'/100 - ToolTide';
  try{if(t.length<20000)localStorage.setItem('tt_flesch',t);}catch(e){}
}
IN.addEventListener('input',calc);
try{var mem=localStorage.getItem('tt_flesch');if(mem)IN.value=mem;}catch(e){}
calc();
document.getElementById('fl-share').addEventListener('click',function(){
  var txt='My text scores '+OUT.textContent+'/100 reading ease ('+document.getElementById('fl-grade').textContent+'th grade level). Score yours (free, local):';
  var url=location.origin+location.pathname;
  if(navigator.share){navigator.share({title:'Flesch reading ease',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-readability-score','Share this readability score');},1500);}
});
})();
</script>
"""

# Dew point: Magnus formula, comfort bands. Neighbors: heatindex, windchill.
# Retention hooks: title result hook, tt_dewpoint memory, URL state (?t=&h=&u=), Web Share.
DEWPOINT = """<div class="tool" id="tt-dp">
  <div class="fields">
    <div class="field"><label for="dp-u"><span data-i18n="lbl.units">Units</span></label><select id="dp-u"><option value="c">°C</option><option value="f">°F</option></select></div>
    <div class="field"><label for="dp-t"><span data-i18n="lbl.airtemp">Air temperature</span></label><input type="number" id="dp-t" step="any" placeholder="30"></div>
    <div class="field"><label for="dp-h"><span data-i18n="lbl.relhum">Relative humidity %</span></label><input type="number" id="dp-h" step="any" min="1" max="100" placeholder="70"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dp-out">–</span><span class="result-unit" id="dp-u2">°C dew point</span></div>
  <div class="stats">
    <div class="stat"><b id="dp-band">–</b><span>comfort verdict</span></div>
    <div class="stat"><b id="dp-ah">–</b><span>water vapor in air</span></div>
    <div class="stat"><b id="dp-gap">–</b><span>temp − dew point</span></div>
  </div>
  <div class="tool-note" id="dp-note"></div>
  <button type="button" class="tool-btn" id="dp-share" data-i18n="share.share-this-dew-point">Share this dew point</button>
</div>
<script>(function(){
var U=document.getElementById('dp-u'),T=document.getElementById('dp-t'),H=document.getElementById('dp-h');
var OUT=document.getElementById('dp-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function cv(v,u){return u==='f'?(v-32)*5/9:v;}
function back(v,u){return u==='f'?v*9/5+32:v;}
function calc(){
  var u=U.value,t=parseFloat(T.value),h=parseFloat(H.value);
  document.getElementById('dp-u2').textContent='°'+u+' dew point';
  if(isNaN(t)||!(h>0)){OUT.textContent='–';
    ['dp-band','dp-ah','dp-gap'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('dp-note').textContent='';document.title='Dew Point Calculator - ToolTide';return;}
  var tc=cv(t,u);
  var g=Math.log(h/100)+17.62*tc/(243.12+tc);
  var td=243.12*g/(17.62-g),tv=back(td,u);
  OUT.textContent=Math.round(tv*10)/10;
  var c=td;
  var band=c<10?'dry':c<16?'comfortable':c<21?'noticeable humidity':c<24?'muggy':'oppressive';
  document.getElementById('dp-band').textContent=band;
  document.getElementById('dp-ah').textContent=(2.1674*Math.pow(6.112,1)*Math.exp(17.62*td/(243.12+td))*100/(273.15+td)).toFixed(1)+' g/m³';
  document.getElementById('dp-gap').textContent=Math.round((t-tv)*10)/10+'°';
  document.getElementById('dp-note').textContent='Dew point '+Math.round(tv*10)/10+'°'+u+' = '+band+'. The dew point - not relative humidity - is the honest mugginess meter: 70% RH at 15°C feels fine, 70% RH at 30°C is a swamp, because dew point states the actual water in the air. Sweat stops evaporating once dew point nears skin temperature (about 33°C), which is why the mid-20s feels like a wall. Fog or dew forms overnight once air cools to this number.';
  document.title=Math.round(tv*10)/10+'°'+u+' dew point - ToolTide';
}
function save(){try{localStorage.setItem('tt_dewpoint',JSON.stringify({u:U.value,t:T.value,h:H.value}));}catch(e){}}
[U,T,H].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['u',U],['t',T],['h',H]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_dewpoint')||'null');if(mem){U.value=mem.u||'c';T.value=mem.t||'';H.value=mem.h||'';}}catch(e){}}
calc();
document.getElementById('dp-share').addEventListener('click',function(){
  var txt='Dew point '+OUT.textContent+'°'+U.value+' ('+document.getElementById('dp-band').textContent+'). Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?u='+encodeURIComponent(U.value)+'&t='+encodeURIComponent(T.value||'')+'&h='+encodeURIComponent(H.value||'');
  if(navigator.share){navigator.share({title:'Dew point',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-dew-point','Share this dew point');},1500);}
});
})();
</script>
"""

# AC sizing: area x height -> base BTU, with insulation/sun/occupancy/kitchen adjustments.
# Retention hooks: title result hook, tt_btu memory, URL state (?a=&h=&i=&s=&p=&k=), Web Share.
BTUCALC = """<div class="tool" id="tt-bt">
  <div class="fields">
    <div class="field"><label for="bt-a">Room area (m²)</label><input type="number" id="bt-a" step="any" min="1" placeholder="20"></div>
    <div class="field"><label for="bt-h">Ceiling height (m)</label><input type="number" id="bt-h" step="any" min="2" placeholder="2.7"></div>
    <div class="field"><label for="bt-i">Insulation</label><select id="bt-i"><option value="g">Good (modern)</option><option value="m" selected>Average</option><option value="p">Poor (old windows)</option></select></div>
    <div class="field"><label for="bt-s">Sun exposure</label><select id="bt-s"><option value="sh">Shaded</option><option value="av" selected>Average</option><option value="su">Very sunny</option></select></div>
    <div class="field"><label for="bt-p">People usually inside</label><input type="number" id="bt-p" step="1" min="1" max="12" placeholder="2"></div>
    <div class="field"><label for="bt-k">Kitchen? </label><select id="bt-k"><option value="n">No</option><option value="y">Yes (appliances add heat)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bt-out">–</span><span class="result-unit">BTU needed</span></div>
  <div class="stats">
    <div class="stat"><b id="bt-kw">–</b><span>kW cooling</span></div>
    <div class="stat"><b id="bt-ton">–</b><span>tons of cooling</span></div>
    <div class="stat"><b id="bt-base">–</b><span>base before adjustments</span></div>
  </div>
  <div class="tool-note" id="bt-note"></div>
  <button type="button" class="tool-btn" id="bt-share" data-i18n="share.share-this-ac-size">Share this AC size</button>
</div>
<script>(function(){
var A=document.getElementById('bt-a'),H=document.getElementById('bt-h'),I=document.getElementById('bt-i'),S=document.getElementById('bt-s'),P=document.getElementById('bt-p'),K=document.getElementById('bt-k');
var OUT=document.getElementById('bt-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),h=parseFloat(H.value)||2.7,p=parseInt(P.value)||2;
  if(!(a>0)){OUT.textContent='–';
    ['bt-kw','bt-ton','bt-base'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('bt-note').textContent='';document.title='BTU Calculator - ToolTide';return;}
  var sqft=a*10.7639,base=sqft*20*(h/2.7);
  var f=1;
  if(I.value==='g')f-=0.05;if(I.value==='p')f+=0.15;
  if(S.value==='su')f+=0.10;if(S.value==='sh')f-=0.10;
  var btu=base*f;if(p>2)btu+=600*(p-2);if(K.value==='y')btu+=4000;
  btu=Math.round(btu/500)*500;
  OUT.textContent=btu.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('bt-kw').textContent=(btu*0.000293).toFixed(1)+' kW';
  document.getElementById('bt-ton').textContent=(btu/12000).toFixed(1);
  document.getElementById('bt-base').textContent=Math.round(base/500)*500>=1000?((Math.round(base/500)*500).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')):Math.round(base);
  document.getElementById('bt-note').textContent='Roughly a '+(Math.round(btu/9000*10)/10)+' kW split unit. Undersized units run forever and never dehumidify; oversized ones short-cycle - cold but clammy, and they wear out faster. The 20 BTU/sqft rule of thumb is temperate-climate: in Phoenix or Dubai add 10-20%, and ducted losses can eat another 10%. Heat pumps list cooling and heating BTU separately - size for the dominant season.';
  document.title=btu.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' BTU - ToolTide';
}
function save(){try{localStorage.setItem('tt_btu',JSON.stringify({a:A.value,h:H.value,i:I.value,s:S.value,p:P.value,k:K.value}));}catch(e){}}
[A,H,I,S,P,K].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['a',A],['h',H],['i',I],['s',S],['p',P],['k',K]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_btu')||'null');if(mem){A.value=mem.a||'';H.value=mem.h||'';I.value=mem.i||'m';S.value=mem.s||'av';P.value=mem.p||'';K.value=mem.k||'n';}}catch(e){}}
calc();
document.getElementById('bt-share').addEventListener('click',function(){
  var txt='My '+A.value+' m² room needs about '+OUT.textContent+' BTU of cooling. Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value||'')+'&h='+encodeURIComponent(H.value||'')+'&i='+I.value+'&s='+S.value;
  if(navigator.share){navigator.share({title:'BTU sizing',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-ac-size','Share this AC size');},1500);}
});
})();
</script>
"""

# Tire size comparison: diameter math -> speedometer error, clearance, revs per mile.
# Retention hooks: title result hook, tt_tire memory, URL state (?w=&a=&r=&w2=&a2=&r2=), Web Share.
TIRE = """<div class="tool" id="tt-ts">
  <div class="fields">
    <div class="field"><label for="ts-w">Current width (mm)</label><input type="number" id="ts-w" step="1" placeholder="225"></div>
    <div class="field"><label for="ts-a">Current aspect (%)</label><input type="number" id="ts-a" step="1" placeholder="45"></div>
    <div class="field"><label for="ts-r">Current rim (in)</label><input type="number" id="ts-r" step="any" min="10" placeholder="17"></div>
    <div class="field"><label for="ts-w2">New width (mm)</label><input type="number" id="ts-w2" step="1" placeholder="245"></div>
    <div class="field"><label for="ts-a2">New aspect (%)</label><input type="number" id="ts-a2" step="1" placeholder="40"></div>
    <div class="field"><label for="ts-r2">New rim (in)</label><input type="number" id="ts-r2" step="any" min="10" placeholder="18"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ts-out">–</span><span class="result-unit">% diameter change</span></div>
  <div class="stats">
    <div class="stat"><b id="ts-dia">–</b><span>new vs old diameter</span></div>
    <div class="stat"><b id="ts-speed">–</b><span>speedo at 100 km/h</span></div>
    <div class="stat"><b id="ts-rev">–</b><span>revs / mile change</span></div>
    <div class="stat"><b id="ts-fit">–</b><span>fitment verdict</span></div>
  </div>
  <div class="tool-note" id="ts-note"></div>
  <button type="button" class="tool-btn" id="ts-share" data-i18n="share.share-this-comparison">Share this comparison</button>
</div>
<script>(function(){
var W=document.getElementById('ts-w'),A=document.getElementById('ts-a'),R=document.getElementById('ts-r'),
    W2=document.getElementById('ts-w2'),A2=document.getElementById('ts-a2'),R2=document.getElementById('ts-r2');
var OUT=document.getElementById('ts-out');
function dia(w,a,r){return r*25.4+2*w*a/100;}
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(W.value),a=parseFloat(A.value),r=parseFloat(R.value),
      w2=parseFloat(W2.value),a2=parseFloat(A2.value),r2=parseFloat(R2.value);
  if(!(w>0)||!(a>0)||!(r>0)||!(w2>0)||!(a2>0)||!(r2>0)){OUT.textContent='–';
    ['ts-dia','ts-speed','ts-rev','ts-fit'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('ts-note').textContent='';document.title='Tire Size Comparison - ToolTide';return;}
  var d1=dia(w,a,r),d2=dia(w2,a2,r2),pct=(d2/d1-1)*100;
  OUT.textContent=(pct>=0?'+':'')+pct.toFixed(1);
  document.getElementById('ts-dia').textContent=Math.round(d1)+' → '+Math.round(d2)+' mm';
  var sp=100/d2*d1;
  document.getElementById('ts-speed').textContent='reads '+Math.round(sp)+' km/h';
  var rev1=1609344/d1,rev2=1609344/d2;
  document.getElementById('ts-rev').textContent=((rev2/rev1-1)*100).toFixed(1)+'%';
  var ok=Math.abs(pct)<=3;
  document.getElementById('ts-fit').textContent=ok?'within ±3% - generally safe':'outside ±3% - rub risk';
  document.getElementById('ts-note').textContent='Diameter = rim + 2 × sidewall (width × aspect). Your speedometer and odometer are calibrated to the original rolling diameter, so '+pct.toFixed(1)+'% means the speedo reads '+Math.round(sp)+' when the truth is 100 - and the odometer drifts the same way. Stay within ±3% to avoid rubbing, gearing and ABS/ESP complaints. The sidewall math is exactly why plus-sizing goes: bigger rim, smaller aspect, similar total height.';
  document.title=(pct>=0?'+':'')+pct.toFixed(1)+'% tire size - ToolTide';
}
function save(){try{localStorage.setItem('tt_tire',JSON.stringify({w:W.value,a:A.value,r:R.value,w2:W2.value,a2:A2.value,r2:R2.value}));}catch(e){}}
[W,A,R,W2,A2,R2].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['w',W],['a',A],['r',R],['w2',W2],['a2',A2],['r2',R2]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_tire')||'null');if(mem){W.value=mem.w||'';A.value=mem.a||'';R.value=mem.r||'';W2.value=mem.w2||'';A2.value=mem.a2||'';R2.value=mem.r2||'';}}catch(e){}}
calc();
document.getElementById('ts-share').addEventListener('click',function(){
  var txt='Tire swap 225/45-17 → '+W2.value+'/'+A2.value+'-'+R2.value+' = '+OUT.textContent+'% diameter (speedo at '+document.getElementById('ts-speed').textContent+'). Compare yours (free):';
  var url=location.origin+location.pathname+'?w='+W.value+'&a='+A.value+'&r='+R.value+'&w2='+W2.value+'&a2='+A2.value+'&r2='+R2.value;
  if(navigator.share){navigator.share({title:'Tire size comparison',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-comparison','Share this comparison');},1500);}
});
})();
</script>
"""

# Heart rate zones: Karvonen (%HRR) vs %MHR, five training bands.
# Retention hooks: title result hook, tt_hrzone memory, URL state (?a=&r=&m=), Web Share.
HRZONE = """<div class="tool" id="tt-hz">
  <div class="fields">
    <div class="field"><label for="hz-a"><span data-i18n="lbl.age">Age</span></label><input type="number" id="hz-a" min="10" max="100" placeholder="35"></div>
    <div class="field"><label for="hz-r">Resting heart rate</label><input type="number" id="hz-r" min="30" max="120" placeholder="60"></div>
    <div class="field"><label for="hz-m"><span data-i18n="lbl.method">Method</span></label><select id="hz-m"><option value="k">Karvonen (% of reserve)</option><option value="m">% of max HR</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="hz-out">–</span><span class="result-unit">max heart rate</span></div>
  <div class="stats" id="hz-rows"></div>
  <div class="tool-note" id="hz-note"></div>
  <button type="button" class="tool-btn" id="hz-share" data-i18n="share.share-my-zones">Share my zones</button>
</div>
<script>(function(){
var A=document.getElementById('hz-a'),R=document.getElementById('hz-r'),M=document.getElementById('hz-m');
var OUT=document.getElementById('hz-out'),ROWS=document.getElementById('hz-rows');
var Z=[['Z1 recovery',.5,.6],['Z2 aerobic base',.6,.7],['Z3 tempo',.7,.8],['Z4 threshold',.8,.9],['Z5 VO2max',.9,1]];
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),r=parseFloat(R.value)||60,m=M.value;
  if(!(a>=10&&a<=100)){OUT.textContent='–';ROWS.innerHTML='';document.getElementById('hz-note').textContent='';
    document.title='Heart Rate Zones Calculator - ToolTide';return;}
  var max=220-a;
  OUT.textContent=max;
  var html='';
  Z.forEach(function(z){
    var lo,hi;
    if(m==='k'){if(!(r>=30&&r<=120)){lo=hi=null;}else{lo=Math.round(r+z[1]*(max-r));hi=Math.round(r+z[2]*(max-r));}}
    else{lo=Math.round(max*z[1]);hi=Math.round(max*z[2]);}
    html+='<div class="stat"><b>'+(lo?lo+'–'+hi:'set resting HR')+'</b><span>'+z[0]+' ('+Math.round(z[1]*100)+'-'+Math.round(z[2]*100)+'%)</span></div>';});
  ROWS.innerHTML=html;
  document.getElementById('hz-note').textContent=(m==='k'?'Karvonen scales intensity by your heart rate reserve (max − resting), so zones shift up for trained hearts with low resting rates - it is the fairer map if you know your resting HR. ':'The % of max method is the classic wall-chart formula - simpler, but it ignores fitness: a rested athlete and a beginner get identical zones. Switch to Karvonen for reserve-based bands. ')+'220 − age is a population average with ±10+ bpm of scatter; if you have a measured lactate-threshold or lab number, trust it over any formula.';
  document.title=max+' bpm max - ToolTide';
}
function save(){try{localStorage.setItem('tt_hrzone',JSON.stringify({a:A.value,r:R.value,m:M.value}));}catch(e){}}
[A,R,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['a',A],['r',R],['m',M]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_hrzone')||'null');if(mem){A.value=mem.a||'';R.value=mem.r||'';M.value=mem.m||'k';}}catch(e){}}
calc();
document.getElementById('hz-share').addEventListener('click',function(){
  var txt='My max HR is '+OUT.textContent+' bpm - Z2 aerobic base runs '+(ROWS.textContent.split('Z2')[0]||'').trim()+' . Find your training zones (free):';
  var url=location.origin+location.pathname+'?a='+encodeURIComponent(A.value||'')+'&r='+encodeURIComponent(R.value||'')+'&m='+M.value;
  if(navigator.share){navigator.share({title:'HR zones',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-zones','Share my zones');},1500);}
});
})();
</script>
"""

# Golf handicap: WHS differential from a round, course handicap for the next tee.
# Retention hooks: title result hook, tt_golf memory, URL state (?s=&c=&sl=&h=), Web Share.
GOLF = """<div class="tool" id="tt-gf">
  <div class="fields">
    <div class="field"><label for="gf-s">Adjusted gross score</label><input type="number" id="gf-s" min="18" max="200" placeholder="95"></div>
    <div class="field"><label for="gf-c">Course rating</label><input type="number" id="gf-c" step="any" min="55" max="85" placeholder="72.4"></div>
    <div class="field"><label for="gf-sl">Slope</label><input type="number" id="gf-sl" min="55" max="155" placeholder="128"></div>
    <div class="field"><label for="gf-h">Your handicap index (opt.)</label><input type="number" id="gf-h" step="any" min="-10" max="54" placeholder="15.2"></div>
    <div class="field"><label for="gf-p">Par of that course</label><input type="number" id="gf-p" min="54" max="80" placeholder="72"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gf-out">–</span><span class="result-unit">round differential</span></div>
  <div class="stats">
    <div class="stat"><b id="gf-ch">–</b><span>course handicap here</span></div>
    <div class="stat"><b id="gf-target">–</b><span>\"net even\" target score</span></div>
    <div class="stat"><b id="gf-vs">–</b><span>vs your index</span></div>
  </div>
  <div class="tool-note" id="gf-note"></div>
  <button type="button" class="tool-btn" id="gf-share" data-i18n="share.share-this-round-math">Share this round math</button>
</div>
<script>(function(){
var S=document.getElementById('gf-s'),C=document.getElementById('gf-c'),SL=document.getElementById('gf-sl'),HI=document.getElementById('gf-h'),P=document.getElementById('gf-p');
var OUT=document.getElementById('gf-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var s=parseFloat(S.value),c=parseFloat(C.value),sl=parseFloat(SL.value),hi=parseFloat(HI.value),par=parseFloat(P.value);
  if(!(s>0)||!(c>0)||!(sl>0)){OUT.textContent='–';
    ['gf-ch','gf-target','gf-vs'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('gf-note').textContent='';document.title='Golf Handicap Calculator - ToolTide';return;}
  var d=(113/sl)*(s-c);
  OUT.textContent=Math.round(d*10)/10;
  var ch=(hi>0||hi===0)?Math.round(hi*(sl/113)+(c-(par||72))):-1;
  document.getElementById('gf-ch').textContent=ch>=0?ch:'–';
  document.getElementById('gf-target').textContent=(ch>=0&&par)?(s-ch<par?par:par+ch):'–';
  document.getElementById('gf-vs').textContent=(ch>=0)?((d<hi?'✓ better than':'worse than')+' your '+hi+' index'):'–';
  document.getElementById('gf-note').textContent='Differential = (113 ÷ slope) × (score − course rating) = '+OUT.textContent+' - the one number the World Handicap System compares across courses. Your index is the average of your best 8 differentials from the last 20 rounds, so one blow-up hole (capped by net double bogey) cannot wreck it. Course handicap '+ (ch>=0?'means you get '+ch+' strokes here - play to par + '+ch+' for a \"handicap round\".':'needs your index above.') ;
  document.title='Differential '+OUT.textContent+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_golf',JSON.stringify({s:S.value,c:C.value,sl:SL.value,h:HI.value,p:P.value}));}catch(e){}}
[S,C,SL,HI,P].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['s',S],['c',C],['sl',SL],['h',HI],['p',P]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_golf')||'null');if(mem){S.value=mem.s||'';C.value=mem.c||'';SL.value=mem.sl||'';HI.value=mem.h||'';P.value=mem.p||'';}}catch(e){}}
calc();
document.getElementById('gf-share').addEventListener('click',function(){
  var txt='Shot '+S.value+' on a '+C.value+'/'+SL.value+' course = '+OUT.textContent+' differential. Do your round math (free, no sign-up):';
  var url=location.origin+location.pathname+'?s='+S.value+'&c='+C.value+'&sl='+SL.value;
  if(navigator.share){navigator.share({title:'Golf differential',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-round-math','Share this round math');},1500);}
});
})();
</script>
"""

# BPM tools: delay times per note division + LFO/Hz sync for producers.
# Retention hooks: title result hook, tt_bpm memory, URL state (?b=), Web Share.
BPMDelay = """<div class="tool" id="tt-bpm">
  <div class="fields">
    <div class="field"><label for="bp-b">Track BPM</label><input type="number" id="bp-b" min="20" max="400" placeholder="120"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="bp-out">–</span><span class="result-unit">ms 1/4 note delay</span></div>
  <div class="stats">
    <div class="stat"><b id="bp-d8">–</b><span>1/8 dotted (ping-pong classic)</span></div>
    <div class="stat"><b id="bp-8t">–</b><span>1/8 triplet</span></div>
    <div class="stat"><b id="bp-hz">–</b><span>LFO 1 cycle / bar</span></div>
    <div class="stat"><b id="bp-bar">–</b><span>one 4/4 bar</span></div>
  </div>
  <div class="tool-note" id="bp-note"></div>
  <button type="button" class="tool-btn" id="bp-share" data-i18n="share.share-these-delay-times">Share these delay times</button>
</div>
<script>(function(){
var B=document.getElementById('bp-b');
var OUT=document.getElementById('bp-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var b=parseFloat(B.value);
  if(!(b>=20&&b<=400)){OUT.textContent='–';
    ['bp-d8','bp-8t','bp-hz','bp-bar'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('bp-note').textContent='';document.title='BPM Delay Calculator - ToolTide';return;}
  var q=60000/b;
  OUT.textContent=Math.round(q);
  document.getElementById('bp-d8').textContent=Math.round(q*1.5)+' ms';
  document.getElementById('bp-8t').textContent=Math.round(q*2/3)+' ms';
  document.getElementById('bp-hz').textContent=(b/60/4).toFixed(3)+' Hz';
  document.getElementById('bp-bar').textContent=Math.round(q*4).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' ms';
  document.getElementById('bp-note').textContent='Set a delay\\'s time in ms (not tap-tempo) to these values and echoes land exactly between the notes: dotted 1/8 is the classic ambient/edge-of-chaos choice, 1/4 keeps echoes on the beat, triplets swing. For reverb predelay, 10-30 ms keeps vocals in front of the wash. Many plugins accept Hz for modulation instead - one LFO cycle per bar is '+ (b/60/4).toFixed(3)+' Hz here.';
  document.title=Math.round(q)+' ms 1/4 delay - ToolTide';
}
function save(){try{localStorage.setItem('tt_bpm',B.value);}catch(e){}}
B.addEventListener('input',function(){calc();save();});
var v=qs('b');if(v!==null)B.value=v;
else{try{var mem=localStorage.getItem('tt_bpm');if(mem)B.value=mem;}catch(e){}}
calc();
document.getElementById('bp-share').addEventListener('click',function(){
  var txt='At '+B.value+' BPM: 1/4 delay = '+OUT.textContent+' ms, dotted 1/8 = '+document.getElementById('bp-d8').textContent+'. Sync your delays (free):';
  var url=location.origin+location.pathname+'?b='+encodeURIComponent(B.value||'');
  if(navigator.share){navigator.share({title:'BPM delay times',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-these-delay-times','Share these delay times');},1500);}
});
})();
</script>
"""

# EV charging cost: per-mile vs gas comparison, charging-loss aware.
# Retention hooks: title result hook, tt_evcharge memory, URL state (?k=&e=&u=&r=&g=&m=), Web Share.
EVCHARGE = """<div class="tool" id="tt-ev">
  <div class="fields">
    <div class="field"><label for="ev-u"><span data-i18n="lbl.units">Units</span></label><select id="ev-u"><option value="mi">miles / mpg</option><option value="km">km / L100</option></select></div>
    <div class="field"><label for="ev-k">Usable battery (kWh)</label><input type="number" id="ev-k" step="any" min="1" placeholder="60"></div>
    <div class="field"><label for="ev-e">Efficiency (mi/kWh)</label><input type="number" id="ev-e" step="any" min="1" max="10" placeholder="4"></div>
    <div class="field"><label for="ev-r">Electricity rate ($/kWh)</label><input type="number" id="ev-r" step="any" min="0" placeholder="0.15"></div>
    <div class="field"><label for="ev-g">Gas price ($/unit, opt.)</label><input type="number" id="ev-g" step="any" min="0" placeholder="3.50"></div>
    <div class="field"><label for="ev-m">Gas car (mpg or L/100km)</label><input type="number" id="ev-m" step="any" min="1" placeholder="30"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ev-out">–</span><span class="result-unit" id="ev-unit2">per mile</span></div>
  <div class="stats">
    <div class="stat"><b id="ev-full">–</b><span>full charge cost</span></div>
    <div class="stat"><b id="ev-100">–</b><span>cost per 100 (mi/km)</span></div>
    <div class="stat"><b id="ev-gasc">–</b><span>gas car same distance</span></div>
    <div class="stat"><b id="ev-save">–</b><span>saved vs gas</span></div>
  </div>
  <div class="tool-note" id="ev-note"></div>
  <button type="button" class="tool-btn" id="ev-share" data-i18n="share.share-this-cost-math">Share this cost math</button>
</div>
<script>(function(){
var U=document.getElementById('ev-u'),K=document.getElementById('ev-k'),E=document.getElementById('ev-e'),R=document.getElementById('ev-r'),G=document.getElementById('ev-g'),M=document.getElementById('ev-m');
var OUT=document.getElementById('ev-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function money(n){return '$'+(Math.abs(n)>=1?n.toFixed(2):(n.toFixed(3)));}
function calc(){
  var u=U.value,k=parseFloat(K.value),e=parseFloat(E.value),r=parseFloat(R.value),g=parseFloat(G.value),m=parseFloat(M.value);
  document.getElementById('ev-unit2').textContent=u==='mi'?'per mile':'per km';
  document.getElementById('ev-e').previousElementSibling.textContent=u==='mi'?'Efficiency (mi/kWh)':'Efficiency (kWh/100km)';
  if(!(k>0)||!(e>0)||!(r>0)){OUT.textContent='–';
    ['ev-full','ev-100','ev-gasc','ev-save'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('ev-note').textContent='';document.title='EV Charging Cost Calculator - ToolTide';return;}
  var cpm=u==='mi'?r/e:r*e/100;
  OUT.textContent=money(cpm);
  document.getElementById('ev-full').textContent=money(k*r);
  document.getElementById('ev-100').textContent=money(cpm*100);
  var gc=null;
  if(g>0&&m>0){gc=u==='mi'?g/m:g*m/100;}
  document.getElementById('ev-gasc').textContent=gc!==null?money(gc):'–';
  document.getElementById('ev-save').textContent=gc!==null?money(gc-cpm)+' ('+Math.max(0,Math.round((1-cpm/gc)*100))+'%)':'–';
  document.getElementById('ev-note').textContent='Full charge = battery × your rate, but real wall-to-battery losses add ~10% on Level 2 (more on fast chargers) - mentally add a tenth. Off-peak tariffs often cut the rate by half, which is the difference between charging for pocket change and a utility bill surprise. '+(gc!==null?'At these prices the EV runs for '+money(cpm)+' where the gas car burns '+money(gc)+' - over 12,000 '+(u==='mi'?'miles':'km')+' that is '+money(Math.abs(gc-cpm)*12000)+' a year.':'Add a gas price and consumption to see the comparison.');
  document.title=money(cpm)+' '+(u==='mi'?'per mile':'per km')+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_evcharge',JSON.stringify({u:U.value,k:K.value,e:E.value,r:R.value,g:G.value,m:M.value}));}catch(e){}}
[U,K,E,R,G,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['u',U],['k',K],['e',E],['r',R],['g',G],['m',M]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_evcharge')||'null');if(mem){U.value=mem.u||'mi';K.value=mem.k||'';E.value=mem.e||'';R.value=mem.r||'';G.value=mem.g||'';M.value=mem.m||'';}}catch(e){}}
calc();
document.getElementById('ev-share').addEventListener('click',function(){
  var txt='My EV costs '+OUT.textContent+' '+(U.value==='mi'?'per mile':'per km')+' to charge'+(parseFloat(G.value)>0?' vs '+document.getElementById('ev-gasc').textContent+' for gas':'')+'. Run your numbers (free):';
  var url=location.origin+location.pathname+'?k='+K.value+'&e='+E.value+'&r='+R.value+'&u='+U.value;
  if(navigator.share){navigator.share({title:'EV charging cost',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-cost-math','Share this cost math');},1500);}
});
})();
</script>
"""

# Golden hour: NOAA solar position -> sunrise/sunset + morning/evening golden windows.
# Retention hooks: title result hook, tt_golden memory, URL state (?d=&la=&lo=), Web Share.
GOLDEN = """<div class="tool" id="tt-gh">
  <div class="fields">
    <div class="field"><label for="gh-d">Date</label><input type="date" id="gh-d"></div>
    <div class="field"><label for="gh-la">Latitude (+N)</label><input type="number" id="gh-la" step="any" min="-66" max="66" placeholder="40.7"></div>
    <div class="field"><label for="gh-lo">Longitude (−W)</label><input type="number" id="gh-lo" step="any" min="-180" max="180" placeholder="-74.0"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="gh-out">–</span><span class="result-unit">evening golden hour</span></div>
  <div class="stats">
    <div class="stat"><b id="gh-sr">–</b><span>sunrise</span></div>
    <div class="stat"><b id="gh-am">–</b><span>morning golden hour</span></div>
    <div class="stat"><b id="gh-ss">–</b><span>sunset</span></div>
    <div class="stat"><b id="gh-len">–</b><span>window length</span></div>
  </div>
  <div class="tool-note" id="gh-note"></div>
  <button type="button" class="tool-btn" id="gh-share" data-i18n="share.share-tonight-s-light">Share tonight's light</button>
</div>
<script>(function(){
var D=document.getElementById('gh-d'),LA=document.getElementById('gh-la'),LO=document.getElementById('gh-lo');
var OUT=document.getElementById('gh-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function rad(x){return x*Math.PI/180;}
function hrsToStr(h){
  if(isNaN(h))return '–';
  var off=-new Date().getTimezoneOffset()/60;
  var t=h+off,total=Math.round(t*60)+1440*7;
  var hh=Math.floor(total/60)%24,mm=total%60;
  return (hh<10?'0':'')+hh+':'+(mm<10?'0':'')+mm;}
function solar(date,lat,lon,h0){
  var start=Date.UTC(date.getFullYear(),date.getMonth(),date.getDate())/86400000+2440587.5;
  var n=start-2451545.0+0.0008;
  var Jstar=n-lon/360;
  var M=(357.5291+0.98560028*Jstar)%360;
  var C=1.9148*Math.sin(rad(M))+0.02*Math.sin(rad(2*M))+0.0003*Math.sin(rad(3*M));
  var lam=(M+C+282.6341+360)%360;
  var Jt=Jstar+0.0053*Math.sin(rad(M))-0.0069*Math.sin(rad(2*lam));
  var d=rad(Math.asin(Math.sin(rad(lam))*Math.sin(rad(23.4397))));
  var cosH=(Math.sin(rad(h0))-Math.sin(rad(lat))*Math.sin(d))/(Math.cos(rad(lat))*Math.cos(d));
  if(cosH>1)return{polar:'night'};
  if(cosH<-1)return{polar:'day'};
  var H=rad(Math.acos(cosH))*180/Math.PI;
  var solarNoon=Jt+H/360,solarMid=Jt-H/360;
  return{rise:solarMid%1,noon:(solarNoon)%1,set:solarNoon%1};
}
function calc(){
  var dv=D.value?new Date(D.value+'T12:00:00'):null,la=parseFloat(LA.value),lo=parseFloat(LO.value);
  if(!dv||isNaN(la)||isNaN(lo)){OUT.textContent='–';
    ['gh-sr','gh-am','gh-ss','gh-len'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('gh-note').textContent='';document.title='Golden Hour Calculator - ToolTide';return;}
  var sr=solar(dv,la,lo,-0.833),am6=solar(dv,la,lo,6),pm4=solar(dv,la,lo,-4);
  if(sr.polar||am6.polar){OUT.textContent=am6.polar==='day'?'all day':'–';
    document.getElementById('gh-note').textContent=am6.polar==='day'?'Sun never sets here on this date - golden light lasts for hours near the horizon at high latitudes in summer.':'Sun never rises here on this date.';
    ['gh-sr','gh-am','gh-ss','gh-len'].forEach(function(id){document.getElementById(id).textContent='–';});
    return;}
  var srT=hrsToStr(sr.rise),ssT=hrsToStr(sr.set),amEnd=hrsToStr(am6.rise),pmStart=hrsToStr(pm4.set);
  var ghpmMins=Math.max(10,Math.round((sr.set-pm4.set)*60));
  OUT.textContent=pmStart+' – '+ssT;
  document.getElementById('gh-sr').textContent=srT;
  document.getElementById('gh-am').textContent=srT+' – '+amEnd;
  document.getElementById('gh-ss').textContent=ssT;
  document.getElementById('gh-len').textContent=ghpmMins+' min';
  document.getElementById('gh-note').textContent='Golden hour = sun within roughly 6° above the horizon; here that is about '+ghpmMins+' minutes. The light is warm and directional because the sun\\'s path through the atmosphere is long - UV is filtered out, shadows stretch, and contrast drops. Arrive 20 minutes early: the best light is often the first half. Times are in your device\\'s timezone; blue hour follows right after sunset for cityscapes.';
  document.title='Golden hour '+pmStart+'–'+ssT+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_golden',JSON.stringify({d:D.value,la:LA.value,lo:LO.value}));}catch(e){}}
[D,LA,LO].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['d',D],['la',LA],['lo',LO]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_golden')||'null');if(mem){D.value=mem.d||'';LA.value=mem.la||'';LO.value=mem.lo||'';}}catch(e){}}
if(!D.value)D.value=new Date().toISOString().slice(0,10);
calc();
document.getElementById('gh-share').addEventListener('click',function(){
  var txt='Golden hour on '+D.value+' at '+LA.value+','+LO.value+': '+OUT.textContent+'. Plan your shoot (free, no sign-up):';
  var url=location.origin+location.pathname+'?d='+D.value+'&la='+LA.value+'&lo='+LO.value;
  if(navigator.share){navigator.share({title:'Golden hour',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent="Share tonight's light";},1500);}
});
})();
</script>
"""

# Pizza dough: baker's percentages -> exact grams for N balls.
# Retention hooks: title result hook, tt_pizza memory, URL state (?n=&w=&h=&s=), Web Share.
PIZZA = """<div class="tool" id="tt-pz">
  <div class="fields">
    <div class="field"><label for="pz-n">How many pizzas</label><input type="number" id="pz-n" min="1" max="40" placeholder="4"></div>
    <div class="field"><label for="pz-w">Ball weight (g)</label><input type="number" id="pz-w" min="80" max="500" placeholder="250"></div>
    <div class="field"><label for="pz-h">Hydration %</label><input type="number" id="pz-h" min="50" max="90" placeholder="65"></div>
    <div class="field"><label for="pz-y">Yeast type</label><select id="pz-y"><option value="i">Instant (room-temp day)</option><option value="f">Fresh (room-temp day)</option><option value="c">Instant (24h cold ferment)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pz-out">–</span><span class="result-unit">g flour</span></div>
  <div class="stats">
    <div class="stat"><b id="pz-wat">–</b><span>g water</span></div>
    <div class="stat"><b id="pz-salt">–</b><span>g salt</span></div>
    <div class="stat"><b id="pz-yeast">–</b><span>g yeast</span></div>
    <div class="stat"><b id="pz-tot">–</b><span>g total dough</span></div>
  </div>
  <div class="tool-note" id="pz-note"></div>
  <button type="button" class="tool-btn" id="pz-share" data-i18n="share.share-this-recipe">Share this recipe</button>
</div>
<script>(function(){
var N=document.getElementById('pz-n'),W=document.getElementById('pz-w'),H=document.getElementById('pz-h'),Y=document.getElementById('pz-y');
var OUT=document.getElementById('pz-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var n=parseFloat(N.value),w=parseFloat(W.value),h=parseFloat(H.value);
  var y=Y.value==='f'?1.0:Y.value==='c'?0.25:0.4, s=2.8;
  if(!(n>0)||!(w>0)||!(h>0)){OUT.textContent='–';
    ['pz-wat','pz-salt','pz-yeast','pz-tot'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('pz-note').textContent='';document.title='Pizza Dough Calculator - ToolTide';return;}
  var factor=1+h/100+s/100+y/100;
  var flour=n*w/factor;
  function g(x){return Math.round(x);}
  OUT.textContent=g(flour);
  document.getElementById('pz-wat').textContent=g(flour*h/100);
  document.getElementById('pz-salt').textContent=g(flour*s/100);
  document.getElementById('pz-yeast').textContent=g(flour*y/100*10)/10;
  document.getElementById('pz-tot').textContent=g(n*w);
  document.getElementById('pz-note').textContent='Baker\\'s percentages keep the recipe scale-proof: water at '+h+'% of flour weight ('+(h<60?'a stiff, NY-style dough - easier for beginners':h<70?'the Neapolitan sweet spot':'a wet, airy dough - needs well-floured hands')+'), salt ~3% for flavor without slowing yeast, and just enough yeast for the time you give it. Cold fermentation (24-48h in the fridge) trades a pinch of yeast for noticeably better flavor and easier stretching - the single biggest upgrade in home pizza.';
  document.title=g(flour)+'g flour - ToolTide';
}
function save(){try{localStorage.setItem('tt_pizza',JSON.stringify({n:N.value,w:W.value,h:H.value,y:Y.value}));}catch(e){}}
[N,W,H,Y].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['n',N],['w',W],['h',H],['y',Y]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_pizza')||'null');if(mem){N.value=mem.n||'';W.value=mem.w||'';H.value=mem.h||'';Y.value=mem.y||'i';}}catch(e){}}
calc();
document.getElementById('pz-share').addEventListener('click',function(){
  var txt=N.value+' pizzas: '+OUT.textContent+'g flour, '+document.getElementById('pz-wat').textContent+'g water, '+document.getElementById('pz-salt').textContent+'g salt. Scale your dough (free):';
  var url=location.origin+location.pathname+'?n='+N.value+'&w='+W.value+'&h='+H.value+'&y='+Y.value;
  if(navigator.share){navigator.share({title:'Pizza dough',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-recipe','Share this recipe');},1500);}
});
})();
</script>
"""

# Inflation: US CPI-U annual averages -> purchasing power of a dollar across years.
# Retention hooks: title result hook, tt_inflation memory, URL state (?a=&f=&t=), Web Share.
INFLATION = """<div class="tool" id="tt-inf">
  <div class="fields">
    <div class="field"><label for="inf-a">Amount ($)</label><input type="number" id="inf-a" step="any" min="0" placeholder="100"></div>
    <div class="field"><label for="inf-f">From year</label><input type="number" id="inf-f" min="1913" max="2025" step="1" placeholder="1990"></div>
    <div class="field"><label for="inf-t">To year</label><input type="number" id="inf-t" min="1913" max="2025" step="1" placeholder="2025"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="inf-out">–</span><span class="result-unit">today's buying power</span></div>
  <div class="stats">
    <div class="stat"><b id="inf-cum">–</b><span>cumulative inflation</span></div>
    <div class="stat"><b id="inf-avg">–</b><span>avg per year</span></div>
    <div class="stat"><b id="inf-half">–</b><span>years to halve value</span></div>
  </div>
  <div class="tool-note" id="inf-note"></div>
  <button type="button" class="tool-btn" id="inf-share" data-i18n="share.share-this-math">Share this math</button>
</div>
<script>(function(){
var A=document.getElementById('inf-a'),F=document.getElementById('inf-f'),T=document.getElementById('inf-t');
var OUT=document.getElementById('inf-out');
var CPI=[9.9,10,10.1,10.9,12.8,15.1,17.3,20,17.9,16.8,17.1,17.1,17.5,17.7,17.4,17.1,17.1,16.7,15.2,13.7,13,13.4,13.7,13.9,14.4,14.1,13.9,14,14.7,16.3,17.3,17.6,18,19.5,22.3,24.1,23.8,24.1,26,26.5,26.7,26.9,26.8,27.2,28.1,28.9,29.1,29.6,29.9,30.2,30.6,31,31.5,32.4,33.4,34.8,36.7,38.8,40.5,41.8,44.4,49.3,53.8,56.9,60.6,65.2,72.6,82.4,90.9,96.5,99.6,103.9,107.6,109.6,113.6,118.3,124,130.7,136.2,140.3,144.5,148.2,152.4,156.9,160.5,163,166.6,172.2,177.1,179.9,184,188.9,195.3,201.6,207.3,215.3,214.5,218.1,224.9,229.6,233,236.7,237,240,245.1,251.1,255.7,258.8,271,292.7,304.7,313.7,322];
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),f=parseInt(F.value),t=parseInt(T.value);
  if(!(a>0)||!(f>=1913&&f<=2025)||!(t>=1913&&t<=2025)){OUT.textContent='–';
    ['inf-cum','inf-avg','inf-half'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('inf-note').textContent='';document.title='Inflation Calculator - ToolTide';return;}
  var ci=CPI[f-1913],ct=CPI[t-1913];
  var adj=a*ct/ci;
  OUT.textContent='$'+(Math.round(adj*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  var cum=(ct/ci-1)*100, yrs=t-f;
  document.getElementById('inf-cum').textContent=(cum>=0?'+':'')+cum.toFixed(1)+'%';
  var avgPct=yrs>0?((Math.pow(ct/ci,1/yrs)-1)*100):null;
  document.getElementById('inf-avg').textContent=avgPct!==null?avgPct.toFixed(2)+'%/yr':'–';
  var halve=yrs>0&&ct>ci?Math.log(.5)/Math.log(ci/ct):0;
  document.getElementById('inf-half').textContent=halve>0?Math.round(halve)+' yrs':'–';
  document.getElementById('inf-note').textContent=a.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' dollars from '+f+' bought what $'+(Math.round(adj*100)/100).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' buys in '+t+' - prices '+(cum>=0?'rose ':'fell ')+Math.abs(cum).toFixed(1)+'% over '+yrs+' years. Based on BLS CPI-U annual averages (1982-84=100; latest year approximate). CPI measures an average basket, not your basket: housing, health and education have outrun it while electronics defied it - treat the number as the honest map of the dollar, not of your receipt.';
  document.title='$'+(Math.round(adj*100)/100)+' in '+t+' money - ToolTide';
}
function save(){try{localStorage.setItem('tt_inflation',JSON.stringify({a:A.value,f:F.value,t:T.value}));}catch(e){}}
[A,F,T].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['a',A],['f',F],['t',T]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_inflation')||'null');if(mem){A.value=mem.a||'';F.value=mem.f||'';T.value=mem.t||'';}}catch(e){}}
calc();
document.getElementById('inf-share').addEventListener('click',function(){
  var txt=A.value+' dollars in '+F.value+' = '+OUT.textContent+' in '+T.value+' money. Check any year (free, no sign-up):';
  var url=location.origin+location.pathname+'?a='+A.value+'&f='+F.value+'&t='+T.value;
  if(navigator.share){navigator.share({title:'Inflation calculator',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-math','Share this math');},1500);}
});
})();
</script>
"""

# Sleep debt: weekly shortfall vs personal target, with honest recovery notes.
# Retention hooks: title result hook, tt_sleepdebt memory, URL state (?a=&t=&n=), Web Share.
SLEEPDEBT = """<div class="tool" id="tt-sd">
  <div class="fields">
    <div class="field"><label for="sd-a">Avg hours slept / night</label><input type="number" id="sd-a" step="any" min="0" max="14" placeholder="6.5"></div>
    <div class="field"><label for="sd-t">Your target hours</label><input type="number" id="sd-t" step="any" min="5" max="12" placeholder="8"></div>
    <div class="field"><label for="sd-n">Nights at this pace</label><input type="number" id="sd-n" min="1" max="365" placeholder="7"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sd-out">–</span><span class="result-unit">hours of sleep debt</span></div>
  <div class="stats">
    <div class="stat"><b id="sd-wk">–</b><span>shortfall per week</span></div>
    <div class="stat"><b id="sd-cat">–</b><span>debt level</span></div>
    <div class="stat"><b id="sd-pay">–</b><span>nights to clear (at target+1h)</span></div>
  </div>
  <div class="tool-note" id="sd-note"></div>
  <button type="button" class="tool-btn" id="sd-share" data-i18n="share.share-my-sleep-math">Share my sleep math</button>
</div>
<script>(function(){
var A=document.getElementById('sd-a'),T=document.getElementById('sd-t'),N=document.getElementById('sd-n');
var OUT=document.getElementById('sd-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var a=parseFloat(A.value),t=parseFloat(T.value),n=parseInt(N.value);
  if(!(a>=0)||!(t>0)||!(n>0)){OUT.textContent='–';
    ['sd-wk','sd-cat','sd-pay'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('sd-note').textContent='';document.title='Sleep Debt Calculator - ToolTide';return;}
  var debt=Math.max(0,(t-a)*n);
  OUT.textContent=Math.round(debt*10)/10;
  document.getElementById('sd-wk').textContent=Math.max(0,Math.round((t-a)*7*10)/10)+' h';
  var lvl=debt<=0?'none':debt<7?'mild':debt<21?'moderate':'chronic';
  document.getElementById('sd-cat').textContent=lvl;
  var surplus=1;
  document.getElementById('sd-pay').textContent=debt>0?Math.ceil(debt/surplus):'0';
  document.getElementById('sd-note').textContent='Sleeping '+(t-a>=0?(t-a):0)+' hours short of your target each night adds up to '+OUT.textContent+' hours of debt - at the '+lvl+' level. The honest science: weekend catch-up restores alertness but not the metabolic and memory costs, and \u201crepayment\u201d works best as extra hours nightly plus an early night or two, not one 14-hour coma. If debt is chronic, the fix is the target itself: shift bedtime 15 minutes earlier each week rather than trying to win it back on Sunday.';
  document.title=Math.round(debt*10)/10+' h sleep debt - ToolTide';
}
function save(){try{localStorage.setItem('tt_sleepdebt',JSON.stringify({a:A.value,t:T.value,n:N.value}));}catch(e){}}
[A,T,N].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['a',A],['t',T],['n',N]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_sleepdebt')||'null');if(mem){A.value=mem.a||'';T.value=mem.t||'';N.value=mem.n||'';}}catch(e){}}
calc();
document.getElementById('sd-share').addEventListener('click',function(){
  var txt='My sleep math: '+A.value+'h vs a '+T.value+'h target = '+OUT.textContent+' hours of debt. Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?a='+A.value+'&t='+T.value+'&n='+N.value;
  if(navigator.share){navigator.share({title:'Sleep debt',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-my-sleep-math','Share my sleep math');},1500);}
});
})();
</script>
"""

# Coffee ratio: two-way beans <-> water at your chosen brew strength.
# Retention hooks: title result hook, tt_coffee memory, URL state (?w=&r=&d=), Web Share.
COFFEE = """<div class="tool" id="tt-cf">
  <div class="fields">
    <div class="field"><label for="cf-d"><span data-i18n="lbl.direction">Direction</span></label><select id="cf-d"><option value="w2b">I know my water → beans</option><option value="b2w">I have beans → water</option></select></div>
    <div class="field"><label for="cf-w">Water (ml)</label><input type="number" id="cf-w" step="any" min="0" placeholder="500"></div>
    <div class="field" id="cf-bw"><label for="cf-b">Coffee (g)</label><input type="number" id="cf-b" step="any" min="0" placeholder="30"></div>
    <div class="field"><label for="cf-r">Ratio (1 : X)</label><input type="number" id="cf-r" step="any" min="10" max="25" placeholder="16"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cf-out">–</span><span class="result-unit" id="cf-unit">g coffee</span></div>
  <div class="stats">
    <div class="stat"><b id="cf-strength">–</b><span>strength verdict</span></div>
    <div class="stat"><b id="cf-cups">–</b><span>approx cups (250ml)</span></div>
    <div class="stat"><b id="cf-scoop">–</b><span>tablespoons (whole beans)</span></div>
  </div>
  <div class="tool-note" id="cf-note"></div>
  <button type="button" class="tool-btn" id="cf-share" data-i18n="share.share-this-brew">Share this brew</button>
</div>
<script>(function(){
var D=document.getElementById('cf-d'),W=document.getElementById('cf-w'),B=document.getElementById('cf-b'),R=document.getElementById('cf-r');
var OUT=document.getElementById('cf-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var d=D.value,r=parseFloat(R.value),w=parseFloat(W.value),b=parseFloat(B.value);
  document.getElementById('cf-w').parentElement.style.display=d==='w2b'?'':'none';
  document.getElementById('cf-bw').style.display=d==='b2w'?'':'none';
  document.getElementById('cf-unit').textContent=d==='w2b'?'g coffee':'ml water';
  var x=d==='w2b'?w:b;
  if(!(r>0)||!(x>0)){OUT.textContent='–';
    ['cf-strength','cf-cups','cf-scoop'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('cf-note').textContent='';document.title='Coffee Ratio Calculator - ToolTide';return;}
  var grams=d==='w2b'?x/r:x*r;
  OUT.textContent=Math.round(grams*10)/10;
  var water=d==='w2b'?x:grams;
  document.getElementById('cf-strength').textContent=r<=15?'strong & bold':r<=17?'balanced (specialty sweet spot)':'light & tea-like';
  document.getElementById('cf-cups').textContent=Math.round(water/250*10)/10;
  document.getElementById('cf-scoop').textContent=Math.round((d==='w2b'?grams:x)/5*10)/10+' tbsp';
  document.getElementById('cf-note').textContent='The golden ratio: grams of coffee × '+r+' = grams (≈ml) of water - weigh both once and your coffee stops being a lottery. Grind matters as much as ratio: too bitter, grind coarser or use less coffee; too sour and weak, grind finer or use more. Start at 1:16 for pour-over, 1:15 for French press, and adjust by taste one notch at a time - a 5% change is noticeable, a 20% change is a different cup.';
  document.title=Math.round(grams*10)/10+'g coffee - ToolTide';
}
function save(){try{localStorage.setItem('tt_coffee',JSON.stringify({d:D.value,w:W.value,b:B.value,r:R.value}));}catch(e){}}
[D,W,B,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['d',D],['w',W],['b',B],['r',R]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_coffee')||'null');if(mem){D.value=mem.d||'w2b';W.value=mem.w||'';B.value=mem.b||'';R.value=mem.r||'';}}catch(e){}}
calc();
document.getElementById('cf-share').addEventListener('click',function(){
  var txt='My brew: '+OUT.textContent+'g coffee at 1:'+R.value+' ('+document.getElementById('cf-strength').textContent+'). Dial in yours (free):';
  var url=location.origin+location.pathname+'?d='+D.value+'&w='+W.value+'&r='+R.value;
  if(navigator.share){navigator.share({title:'Coffee ratio',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-brew','Share this brew');},1500);}
});
})();
</script>
"""

# Break-even: fixed costs, price, variable cost -> units & revenue to break even.
# Retention hooks: title result hook, tt_breakeven memory, URL state (?f=&p=&v=), Web Share.
BREAKEVEN = """<div class="tool" id="tt-be">
  <div class="fields">
    <div class="field"><label for="be-f">Fixed costs (per month, $)</label><input type="number" id="be-f" step="any" min="0" placeholder="3000"></div>
    <div class="field"><label for="be-p">Price per unit ($)</label><input type="number" id="be-p" step="any" min="0" placeholder="49"></div>
    <div class="field"><label for="be-v">Variable cost per unit ($)</label><input type="number" id="be-v" step="any" min="0" placeholder="17"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="be-out">–</span><span class="result-unit">units / month to break even</span></div>
  <div class="stats">
    <div class="stat"><b id="be-rev">–</b><span>revenue at break-even</span></div>
    <div class="stat"><b id="be-margin">–</b><span>margin per unit</span></div>
    <div class="stat"><b id="be-cm">–</b><span>contribution margin</span></div>
  </div>
  <div class="tool-note" id="be-note"></div>
  <button type="button" class="tool-btn" id="be-share" data-i18n="share.share-this-break-even">Share this break-even</button>
</div>
<script>(function(){
var F=document.getElementById('be-f'),P=document.getElementById('be-p'),V=document.getElementById('be-v');
var OUT=document.getElementById('be-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var f=parseFloat(F.value),p=parseFloat(P.value),v=parseFloat(V.value);
  if(!(f>=0)||!(p>0)||!(v>=0)){OUT.textContent='–';
    ['be-rev','be-margin','be-cm'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('be-note').textContent='';document.title='Break-Even Calculator - ToolTide';return;}
  if(p<=v){OUT.textContent='–';
    document.getElementById('be-note').textContent='Price is at or below variable cost - every sale loses money, so no volume can break even. Fix the price, the cost, or the business.';
    ['be-rev','be-margin','be-cm'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.title='Break-Even Calculator - ToolTide';return;}
  var units=Math.ceil(f/(p-v));
  OUT.textContent=units.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('be-rev').textContent='$'+Math.round(units*p).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('be-margin').textContent='$'+(Math.round((p-v)*100)/100);
  document.getElementById('be-cm').textContent=Math.round((p-v)/p*100)+'%';
  document.getElementById('be-note').textContent='Each sale contributes '+(Math.round((p-v)*100)/100)+' ('+Math.round((p-v)/p*100)+'% of price) toward the $'+f.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' of monthly fixed costs - unit #'+units.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' is the one that clears the rent. Two levers move this number faster than hustle: a +$5 price usually beats a +5% volume push, and trimming variable cost compounds across every future unit. Anything above break-even drops to profit at nearly 100% margin - that is why startups celebrate it.';
  document.title=units.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' units to break even - ToolTide';
}
function save(){try{localStorage.setItem('tt_breakeven',JSON.stringify({f:F.value,p:P.value,v:V.value}));}catch(e){}}
[F,P,V].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['f',F],['p',P],['v',V]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_breakeven')||'null');if(mem){F.value=mem.f||'';P.value=mem.p||'';V.value=mem.v||'';}}catch(e){}}
calc();
document.getElementById('be-share').addEventListener('click',function(){
  var txt='Break-even: '+OUT.textContent+' units/month ($'+P.value+' price, $'+V.value+' cost). Run your numbers (free, no sign-up):';
  var url=location.origin+location.pathname+'?f='+F.value+'&p='+P.value+'&v='+V.value;
  if(navigator.share){navigator.share({title:'Break-even',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-break-even','Share this break-even');},1500);}
});
})();
</script>
"""

# Ideal weight: Devine formula + healthy BMI band, sex-aware, honest framing.
# Retention hooks: title result hook, tt_idealweight memory, URL state (?h=&u=&s=), Web Share.
IDEALW = """<div class="tool" id="tt-iw">
  <div class="fields">
    <div class="field"><label for="iw-u"><span data-i18n="lbl.units">Units</span></label><select id="iw-u"><option value="m">cm / kg</option><option value="i">ft-in / lb</option></select></div>
    <div class="field"><label for="iw-s"><span data-i18n="lbl.sex">Sex</span></label><select id="iw-s"><option value="m">Male</option><option value="f">Female</option></select></div>
    <div class="field"><label for="iw-h" id="iw-hl">Height (cm)</label><input type="number" id="iw-h" step="any" min="120" max="230" placeholder="175"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="iw-out">–</span><span class="result-unit" id="iw-un">kg</span></div>
  <div class="stats">
    <div class="stat"><b id="iw-bmi">–</b><span>healthy BMI range</span></div>
    <div class="stat"><b id="iw-dev">–</b><span>Devine formula</span></div>
    <div class="stat"><b id="iw-lo">–</b><span>lower / upper of band</span></div>
  </div>
  <div class="tool-note" id="iw-note"></div>
  <button type="button" class="tool-btn" id="iw-share" data-i18n="share.share-this-range">Share this range</button>
</div>
<script>(function(){
var U=document.getElementById('iw-u'),S=document.getElementById('iw-s'),H=document.getElementById('iw-h');
var OUT=document.getElementById('iw-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var u=U.value,s=S.value,h=parseFloat(H.value);
  document.getElementById('iw-hl').textContent=u==='m'?'Height (cm)':'Height (inches, total)';
  document.getElementById('iw-un').textContent=u==='m'?'kg':'lb';
  if(!(h>0)){OUT.textContent='–';
    ['iw-bmi','iw-dev','iw-lo'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('iw-note').textContent='';document.title='Ideal Weight Calculator - ToolTide';return;}
  var cm=u==='m'?h:h*2.54,m=cm/100,kgPerIn=u==='m'?null:2.54;
  var inches=u==='m'?cm/2.54:h;
  var dev=(s==='m'?50:45.5)+2.3*Math.max(0,inches-60);
  if(u==='i')dev=dev/2.54*1;
  var loB=18.5*m*m,hiB=24.9*m*m;
  var fmt=function(kg){return u==='m'?Math.round(kg):Math.round(kg*2.20462);};
  OUT.textContent=fmt(dev)+' '+document.getElementById('iw-un').textContent;
  document.getElementById('iw-bmi').textContent=fmt(loB)+'–'+fmt(hiB)+' '+document.getElementById('iw-un').textContent;
  document.getElementById('iw-dev').textContent=fmt(dev)+' '+document.getElementById('iw-un').textContent;
  document.getElementById('iw-lo').textContent=fmt(loB)+' / '+fmt(hiB);
  document.getElementById('iw-note').textContent='Two honest answers: the Devine formula ('+fmt(dev)+' - a 1974 drug-dosing rule, still the classic \u201cideal weight\u201d) and the healthy-BMI band ('+fmt(loB)+'-'+fmt(hiB)+'), which is wider because bodies are. Neither knows your frame, muscle or history - an athletic '+fmt(hiB+5)+' can be healthier than a sedentary '+fmt(loB)+'. Use the band as a range, judge by trend and how you move, and let a clinician argue with the scale.';
  document.title=fmt(dev)+' '+document.getElementById('iw-un').textContent+' ideal - ToolTide';
}
function save(){try{localStorage.setItem('tt_idealweight',JSON.stringify({u:U.value,s:S.value,h:H.value}));}catch(e){}}
[U,S,H].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['u',U],['s',S],['h',H]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_idealweight')||'null');if(mem){U.value=mem.u||'m';S.value=mem.s||'m';H.value=mem.h||'';}}catch(e){}}
calc();
document.getElementById('iw-share').addEventListener('click',function(){
  var txt='Healthy weight band at my height: '+document.getElementById('iw-bmi').textContent+'. Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?h='+H.value+'&u='+U.value+'&s='+S.value;
  if(navigator.share){navigator.share({title:'Ideal weight',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-range','Share this range');},1500);}
});
})();
</script>
"""

# Lorem ipsum: count-exact paragraph generator with copy.
# Retention hooks: tt_lorem settings memory, copy button, live word count.
LOREM = """<div class="tool" id="tt-lr">
  <div class="fields">
    <div class="field"><label for="lr-p">Paragraphs</label><input type="number" id="lr-p" min="1" max="20" value="3"></div>
    <div class="field"><label for="lr-w">Words per paragraph</label><input type="number" id="lr-w" min="20" max="200" value="60"></div>
    <div class="field"><label for="lr-s">Start with \u201cLorem ipsum\u2026\u201d</label><input type="checkbox" id="lr-s" checked></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="lr-out">–</span><span class="result-unit">words generated</span></div>
  <textarea id="lr-tx" rows="9" style="width:100%;box-sizing:border-box;margin-top:10px;font-size:.95em" readonly aria-label="Generated lorem ipsum text"></textarea>
  <div class="tool-note" id="lr-note"></div>
  <button type="button" class="tool-btn" id="lr-copy">Copy to clipboard</button>
  <button type="button" class="tool-btn" id="lr-new">Regenerate</button>
</div>
<script>(function(){
var P=document.getElementById('lr-p'),W=document.getElementById('lr-w'),S=document.getElementById('lr-s');
var TX=document.getElementById('lr-tx'),OUT=document.getElementById('lr-out');
var POOL='lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum perspiciatis unde omnis iste natus error voluptatem accusantium doloremque laudantium totam rem aperiam eaque ipsa quae ab illo inventore veritatis quasi architecto beatae vitae dicta explicabo nemo ipsam quia voluptas aspernatur aut odit fugit consequuntur magni dolores eos ratione sequi nesciunt neque porro quisquam dolorem adipisci numquam eius modi tempora incidunt magnam quaerat etiam'.split(' ');
function qs(k){return new URLSearchParams(location.search).get(k);}
function gen(){
  var p=Math.max(1,Math.min(20,parseInt(P.value)||3)),w=Math.max(20,Math.min(200,parseInt(W.value)||60));
  var out=[],total=0;
  for(var i=0;i<p;i++){
    var words=[];
    for(var j=0;j<w;j++){words.push(POOL[Math.floor(Math.random()*POOL.length)]);}
    if(i===0&&S.checked){words[0]='lorem';words[1]='ipsum';words[2]='dolor';words[3]='sit';words[4]='amet';}
    words[0]=words[0].charAt(0).toUpperCase()+words[0].slice(1);
    var para=words.join(' ');
    total+=w;
    out.push(para+'.');}
  TX.value=out.join('\\n\\n');
  OUT.textContent=total;
  document.getElementById('lr-note').textContent='Count-exact: '+p+' paragraphs × '+w+' words. Every regenerate draws fresh random sentences - paste straight into your mockup, CSS or CMS.';
  document.title=total+' placeholder words - ToolTide';
}
function save(){try{localStorage.setItem('tt_lorem',JSON.stringify({p:P.value,w:W.value,s:S.checked}));}catch(e){}}
[P,W].forEach(function(el){el.addEventListener('input',function(){gen();save();});});
S.addEventListener('change',function(){gen();save();});
document.getElementById('lr-new').addEventListener('click',function(){gen();});
var pre=qs('p');
if(pre){P.value=pre;gen();}
else{try{var mem=JSON.parse(localStorage.getItem('tt_lorem')||'null');if(mem){P.value=mem.p||3;W.value=mem.w||60;S.checked=mem.s!==false;}}catch(e){}}
gen();
document.getElementById('lr-copy').addEventListener('click',function(){
  TX.select();
  if(navigator.clipboard){navigator.clipboard.writeText(TX.value);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent='Copy to clipboard';},1500);}
  else{document.execCommand('copy');this.textContent=TT('ui.copied','Copied!');var c=this;setTimeout(function(){c.textContent='Copy to clipboard';},1500);}
});
})();
</script>
"""

# CAGR: compound annual growth rate between two values over N years.
# Retention hooks: title result hook, tt_cagr memory, URL state (?b=&e=&y=), Web Share.
CAGR = """<div class="tool" id="tt-cg">
  <div class="fields">
    <div class="field"><label for="cg-b">Beginning value ($)</label><input type="number" id="cg-b" step="any" min="0" placeholder="10000"></div>
    <div class="field"><label for="cg-e">Ending value ($)</label><input type="number" id="cg-e" step="any" min="0" placeholder="26000"></div>
    <div class="field"><label for="cg-y"><span data-i18n="lbl.years">Years</span></label><input type="number" id="cg-y" step="any" min="0.1" max="200" placeholder="6"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cg-out">–</span><span class="result-unit" data-i18n="cg.peryear">CAGR per year</span></div>
  <div class="stats">
    <div class="stat"><b id="cg-tot">–</b><span data-i18n="cg.totgrowth">total growth</span></div>
    <div class="stat"><b id="cg-mul">–</b><span data-i18n="cg.multiple">multiple of start</span></div>
    <div class="stat"><b id="cg-dbl">–</b><span data-i18n="cg.yrsdouble">years to double at this rate</span></div>
  </div>
  <div class="tool-note" id="cg-note"></div>
  <button type="button" class="tool-btn" id="cg-share" data-i18n="share.share-this-cagr">Share this CAGR</button>
</div>
<script>(function(){
var B=document.getElementById('cg-b'),E=document.getElementById('cg-e'),Y=document.getElementById('cg-y');
var OUT=document.getElementById('cg-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var b=parseFloat(B.value),e=parseFloat(E.value),y=parseFloat(Y.value);
  if(!(b>0)||!(e>0)||!(y>0)){OUT.textContent='–';
    ['cg-tot','cg-mul','cg-dbl'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('cg-note').textContent='';document.title='CAGR Calculator - ToolTide';return;}
  var c=Math.pow(e/b,1/y)-1;
  OUT.textContent=(c*100>=0?'+':'')+(c*100).toFixed(2)+'%';
  document.getElementById('cg-tot').textContent=((e/b-1)*100>=0?'+':'')+((e/b-1)*100).toFixed(1)+'%';
  document.getElementById('cg-mul').textContent=(e/b).toFixed(2)+'×';
  document.getElementById('cg-dbl').textContent=c>0?Math.round(Math.log(2)/Math.log(1+c)*10)/10+' yrs':'–';
  document.getElementById('cg-note').textContent='CAGR smooths a jagged journey into one honest number: +26% a year for '+(Math.round(y*10)/10)+' years turns '+(b.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US'))+' into '+(e.toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US'))+' - even if year two was -40% and year three +80%, the compound rate is what compounds. Rule of 72 for sanity: at this rate money doubles every '+(c>0?Math.round(72/(c*100)):'–')+' years. Watch the trap: a big loss needs a bigger gain to recover - -50% needs +100% just to get back to zero, which is why steady beats spectacular.';
  document.title=(c*100>=0?'+':'')+(c*100).toFixed(1)+'% CAGR - ToolTide';
}
function save(){try{localStorage.setItem('tt_cagr',JSON.stringify({b:B.value,e:E.value,y:Y.value}));}catch(e){}}
[B,E,Y].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['b',B],['e',E],['y',Y]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_cagr')||'null');if(mem){B.value=mem.b||'';E.value=mem.e||'';Y.value=mem.y||'';}}catch(e){}}
calc();
document.getElementById('cg-share').addEventListener('click',function(){
  var txt=B.value+' grew to '+E.value+' in '+Y.value+' years = '+OUT.textContent+' CAGR. Check your growth rate (free, no sign-up):';
  var url=location.origin+location.pathname+'?b='+B.value+'&e='+E.value+'&y='+Y.value;
  if(navigator.share){navigator.share({title:'CAGR',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-cagr','Share this CAGR');},1500);}
});
})();
</script>
"""

# Pool volume: rectangular/circular/oval -> liters, gallons, water weight.
# Retention hooks: title result hook, tt_pool memory, URL state (?s=&a=&b=&c=&u=), Web Share.
POOL = """<div class="tool" id="tt-pl">
  <div class="fields">
    <div class="field"><label for="pl-s">Shape</label><select id="pl-s"><option value="r">Rectangular</option><option value="c">Circular</option><option value="o">Oval</option></select></div>
    <div class="field"><label for="pl-a" id="pl-aa">Length (m)</label><input type="number" id="pl-a" step="any" min="0" placeholder="8"></div>
    <div class="field" id="pl-bw"><label for="pl-b" id="pl-bb">Width (m)</label><input type="number" id="pl-b" step="any" min="0" placeholder="4"></div>
    <div class="field"><label for="pl-c">Average depth (m)</label><input type="number" id="pl-c" step="any" min="0" placeholder="1.4"></div>
    <div class="field"><label for="pl-u"><span data-i18n="lbl.units">Units</span></label><select id="pl-u"><option value="m">meters / liters</option><option value="f">feet / gallons</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pl-out">–</span><span class="result-unit" id="pl-u2">liters</span></div>
  <div class="stats">
    <div class="stat"><b id="pl-gal">–</b><span>US gallons</span></div>
    <div class="stat"><b id="pl-m3">–</b><span>cubic meters</span></div>
    <div class="stat"><b id="pl-ton">–</b><span>tonnes of water</span></div>
  </div>
  <div class="tool-note" id="pl-note"></div>
  <button type="button" class="tool-btn" id="pl-share" data-i18n="share.share-this-volume">Share this volume</button>
</div>
<script>(function(){
var S=document.getElementById('pl-s'),A=document.getElementById('pl-a'),B=document.getElementById('pl-b'),C=document.getElementById('pl-c'),U=document.getElementById('pl-u');
var OUT=document.getElementById('pl-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var s=S.value,a=parseFloat(A.value),b=parseFloat(B.value),c=parseFloat(C.value),u=U.value;
  var circ=s==='c';
  document.getElementById('pl-bw').style.display=circ?'none':'';
  document.getElementById('pl-aa').textContent=circ?(u==='m'?'Diameter (m)':'Diameter (ft)'):(u==='m'?'Length (m)':'Length (ft)');
  document.getElementById('pl-bb').textContent=u==='m'?'Width (m)':'Width (ft)';
  document.getElementById('pl-u2').textContent=u==='m'?'liters':'US gallons';
  if(!(a>0)||!(c>0)||(!circ&&!(b>0))){OUT.textContent='–';
    ['pl-gal','pl-m3','pl-ton'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('pl-note').textContent='';document.title='Pool Volume Calculator - ToolTide';return;}
  var m3;
  if(circ){m3=Math.PI*(a/2)*(a/2)*c;}
  else if(s==='o'){m3=Math.PI*(a/2)*(b/2)*c;}
  else{m3=a*b*c;}
  if(u==='f')m3*=0.0283168;
  var lit=m3*1000,gal=m3*264.172;
  OUT.textContent=Math.round(lit).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('pl-gal').textContent=Math.round(gal).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('pl-m3').textContent=(Math.round(m3*10)/10).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('pl-ton').textContent=(Math.round(m3*10)/10)+' t';
  var deep=c*1.4>2.2;
  document.getElementById('pl-note').textContent='Average depth is the honest input: (shallow end + deep end) ÷ 2 - most owners overestimate, and every chemical dose, pump runtime and heating bill scales with this number. Fill to about 90% of the coping, so subtract ~10% for the actual refill. '+(deep?'Deep enough for a diving-type slide check with local rules.':'This is a pool for swimming, not for diving - the deep end is shallower than diving guidelines.')+' Refilling '+(Math.round(lit/100)/10)+'k liters costs real money; a cover pays for itself in evaporation alone.';
  document.title=Math.round(lit).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' L pool - ToolTide';
}
function save(){try{localStorage.setItem('tt_pool',JSON.stringify({s:S.value,a:A.value,b:B.value,c:C.value,u:U.value}));}catch(e){}}
[S,A,B,C,U].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['s',S],['a',A],['b',B],['c',C],['u',U]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_pool')||'null');if(mem){S.value=mem.s||'r';A.value=mem.a||'';B.value=mem.b||'';C.value=mem.c||'';U.value=mem.u||'m';}}catch(e){}}
calc();
document.getElementById('pl-share').addEventListener('click',function(){
  var txt='My pool holds '+OUT.textContent+' '+(U.value==='m'?'liters':'gallons')+'. Calculate yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?s='+S.value+'&a='+A.value+(S.value!=='c'?'&b='+B.value:'')+'&c='+C.value+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Pool volume',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-volume','Share this volume');},1500);}
});
})();
</script>
"""

# Time spent: daily hours -> years of a lifetime, waking-life share.
# Retention hooks: title result hook, tt_timespent memory, URL state (?h=&d=&a=&t=), Web Share.
TIMESPENT = """<div class="tool" id="tt-tsp">
  <div class="fields">
    <div class="field"><label for="ts2-h">Hours per day</label><input type="number" id="ts2-h" step="any" min="0" max="24" placeholder="3"></div>
    <div class="field"><label for="ts2-d">Days per week</label><input type="number" id="ts2-d" step="any" min="0.5" max="7" placeholder="7"></div>
    <div class="field"><label for="ts2-a">From age</label><input type="number" id="ts2-a" min="1" max="100" placeholder="15"></div>
    <div class="field"><label for="ts2-t">To age</label><input type="number" id="ts2-t" min="2" max="100" placeholder="80"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ts2-out">–</span><span class="result-unit">years of your life</span></div>
  <div class="stats">
    <div class="stat"><b id="ts2-months">–</b><span>in months</span></div>
    <div class="stat"><b id="ts2-wake">–</b><span>% of waking hours</span></div>
    <div class="stat"><b id="ts2-work">–</b><span>40-hour work-weeks</span></div>
  </div>
  <div class="tool-note" id="ts2-note"></div>
  <button type="button" class="tool-btn" id="ts2-share" data-i18n="share.share-this-math">Share this math</button>
</div>
<script>(function(){
var H=document.getElementById('ts2-h'),D=document.getElementById('ts2-d'),A=document.getElementById('ts2-a'),T=document.getElementById('ts2-t');
var OUT=document.getElementById('ts2-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var h=parseFloat(H.value),d=parseFloat(D.value)||7,a=parseFloat(A.value),t=parseFloat(T.value);
  if(!(h>0)||!(a>0)||!(t>a)){OUT.textContent='–';
    ['ts2-months','ts2-wake','ts2-work'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('ts2-note').textContent='';document.title='Time Spent Calculator - ToolTide';return;}
  var years=h*(d*52.14)*(t-a)/24/365.25;
  OUT.textContent=Math.round(years*10)/10;
  document.getElementById('ts2-months').textContent=Math.round(years*12);
  var wakePct=h*d*52.14/(16*365.25)*100;
  document.getElementById('ts2-wake').textContent=Math.round(wakePct)+'%';
  document.getElementById('ts2-work').textContent=Math.round(years*365.25*h/40).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('ts2-note').textContent=years+' years of '+(t-a)+' is '+Math.round(years/(t-a)*100)+'% of that whole stretch - spent at '+h+' hours a day. Read it however you need: if this is the habit you love, that is a life well invested; if it is the app you open without noticing, the same math says what an hour back a day is worth over a decade. The calculator does not judge - it just refuses to let the number stay invisible.';
  document.title=Math.round(years*10)/10+' years - ToolTide';
}
function save(){try{localStorage.setItem('tt_timespent',JSON.stringify({h:H.value,d:D.value,a:A.value,t:T.value}));}catch(e){}}
[H,D,A,T].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['h',H],['d',D],['a',A],['t',T]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_timespent')||'null');if(mem){H.value=mem.h||'';D.value=mem.d||'';A.value=mem.a||'';T.value=mem.t||'';}}catch(e){}}
calc();
document.getElementById('ts2-share').addEventListener('click',function(){
  var txt=H.value+' hours a day from age '+A.value+' to '+T.value+' = '+OUT.textContent+' years of my life. Run your own math (free):';
  var url=location.origin+location.pathname+'?h='+H.value+'&d='+D.value+'&a='+A.value+'&t='+T.value;
  if(navigator.share){navigator.share({title:'Time spent',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-math','Share this math');},1500);}
});
})();
</script>
"""

# Meat cooking time: per-kg table by cut at 180C/350F, rest time and core temp.
# Retention hooks: title result hook, tt_meat memory, URL state (?m=&w=&u=), Web Share.
MEATTIME = """<div class="tool" id="tt-mt">
  <div class="fields">
    <div class="field"><label for="mt-m">Cut</label><select id="mt-m">
      <option value="cw">Whole chicken</option>
      <option value="cb">Chicken breast</option>
      <option value="tw">Whole turkey</option>
      <option value="pl">Pork loin</option>
      <option value="br">Beef ribs / pot roast</option>
      <option value="ll">Lamb leg</option>
    </select></div>
    <div class="field"><label for="mt-w"><span data-i18n="lbl.weight">Weight</span></label><input type="number" id="mt-w" step="any" min="0.1" placeholder="1.5"></div>
    <div class="field"><label for="mt-u"><span data-i18n="lbl.units">Units</span></label><select id="mt-u"><option value="k">kg</option><option value="p">lb</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="mt-out">–</span><span class="result-unit">in the oven (180°C / 350°F)</span></div>
  <div class="stats">
    <div class="stat"><b id="mt-core">–</b><span>safe / target core temp</span></div>
    <div class="stat"><b id="mt-rest">–</b><span>rest before carving</span></div>
    <div class="stat"><b id="mt-total">–</b><span>total including rest</span></div>
  </div>
  <div class="tool-note" id="mt-note"></div>
  <button type="button" class="tool-btn" id="mt-share" data-i18n="share.share-this-roast-plan">Share this roast plan</button>
</div>
<script>(function(){
var M=document.getElementById('mt-m'),W=document.getElementById('mt-w'),U=document.getElementById('mt-u');
var OUT=document.getElementById('mt-out');
var T={cw:[42,48,15,74],cb:[25,30,5,74],tw:[35,40,30,74],pl:[40,45,10,63],br:[35,45,15,95],ll:[40,50,15,63]};
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var t=T[M.value],w=parseFloat(W.value),u=U.value;
  if(!(w>0)){OUT.textContent='–';
    ['mt-core','mt-rest','mt-total'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('mt-note').textContent='';document.title='Meat Cooking Time Calculator - ToolTide';return;}
  var kg=u==='k'?w:w*0.4536;
  var lo=Math.round(kg*t[0]/5)*5,hi=Math.round(kg*t[1]/5)*5;
  OUT.textContent=lo+'–'+hi+' min';
  var core=u==='k'?t[3]+'°C':Math.round(t[3]*9/5+32)+'°F';
  document.getElementById('mt-core').textContent=core;
  document.getElementById('mt-rest').textContent=t[2]+' min';
  document.getElementById('mt-total').textContent=lo+t[2]+'–'+(hi+t[2])+' min';
  document.getElementById('mt-note').textContent='Times are for '+(kg.toFixed(1))+' kg at 180°C (350°F) conventional - remove the meat when a probe reads a few degrees BELOW the target core and let the resting finish the job (carryover heat adds 3-5°C while juices redistribute; carving early floods the board). The thermometer is the boss and the minutes are just the plan: ovens lie by ±15°C, and core temperature is the only thing that is both safe and juicy. Chicken and turkey: no pink, 74°C core, always. Pork loin is done at 63°C + rest - dry gray pork is a choice, not a rule.';
  document.title=lo+'–'+hi+' min roast - ToolTide';
}
function save(){try{localStorage.setItem('tt_meat',JSON.stringify({m:M.value,w:W.value,u:U.value}));}catch(e){}}
[M,W,U].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['m',M],['w',W],['u',U]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_meat')||'null');if(mem){M.value=mem.m||'cw';W.value=mem.w||'';U.value=mem.u||'k';}}catch(e){}}
calc();
document.getElementById('mt-share').addEventListener('click',function(){
  var t=T[M.value];
  var txt=M.options[M.selectedIndex].text+' ('+W.value+(U.value==='k'?'kg':'lb')+'): '+OUT.textContent+' at 180°C, rest '+t[2]+' min. Plan your roast (free):';
  var url=location.origin+location.pathname+'?m='+M.value+'&w='+W.value+'&u='+U.value;
  if(navigator.share){navigator.share({title:'Roast timing',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-roast-plan','Share this roast plan');},1500);}
});
})();
</script>
"""

# Car depreciation: value after N years at an annual rate, with the 3-year truth.
# Retention hooks: title result hook, tt_cardep memory, URL state (?p=&y=&r=), Web Share.
CARDEP = """<div class="tool" id="tt-cd">
  <div class="fields">
    <div class="field"><label for="cd-p">Purchase price ($)</label><input type="number" id="cd-p" step="any" min="0" placeholder="30000"></div>
    <div class="field"><label for="cd-y">Years owned</label><input type="number" id="cd-y" step="1" min="0" max="30" placeholder="3"></div>
    <div class="field"><label for="cd-r">Annual depreciation %</label><input type="number" id="cd-r" step="any" min="1" max="40" placeholder="15"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cd-out">–</span><span class="result-unit">current value</span></div>
  <div class="stats">
    <div class="stat"><b id="cd-lost">–</b><span>value lost</span></div>
    <div class="stat"><b id="cd-pct">–</b><span>% of purchase price gone</span></div>
    <div class="stat"><b id="cd-yr">–</b><span>avg cost per year owned</span></div>
  </div>
  <div class="tool-note" id="cd-note"></div>
  <button type="button" class="tool-btn" id="cd-share" data-i18n="share.share-this-math">Share this math</button>
</div>
<script>(function(){
var P=document.getElementById('cd-p'),Y=document.getElementById('cd-y'),R=document.getElementById('cd-r');
var OUT=document.getElementById('cd-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parseFloat(P.value),y=parseInt(Y.value),r=parseFloat(R.value);
  if(!(p>0)||y===undefined||isNaN(y)||!(r>0)){OUT.textContent='–';
    ['cd-lost','cd-pct','cd-yr'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('cd-note').textContent='';document.title='Car Depreciation Calculator - ToolTide';return;}
  var v=p*Math.pow(1-r/100,y);
  OUT.textContent='$'+Math.round(v).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('cd-lost').textContent='$'+Math.round(p-v).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('cd-pct').textContent=Math.round((1-v/p)*100)+'%';
  document.getElementById('cd-yr').textContent='$'+Math.round((p-v)/Math.max(1,y)).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US');
  document.getElementById('cd-note').textContent='Depreciation is front-loaded: a typical car sheds 40-50% of its value in the first three years, then the curve flattens - which is why a 3-year-old car is the classic value pick: the steepest part of the curve is someone else\u2019s receipt. Run the rate at 15-18% for average sedans, more for luxury marques, less for rare hold-the-value models. The per-year figure is the honest cost of ownership that fuel calculators forget - often bigger than the fuel bill itself.';
  document.title='$'+Math.round(v).toLocaleString((typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US')+' car value - ToolTide';
}
function save(){try{localStorage.setItem('tt_cardep',JSON.stringify({p:P.value,y:Y.value,r:R.value}));}catch(e){}}
[P,Y,R].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['p',P],['y',Y],['r',R]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_cardep')||'null');if(mem){P.value=mem.p||'';Y.value=mem.y||'';R.value=mem.r||'';}}catch(e){}}
calc();
document.getElementById('cd-share').addEventListener('click',function(){
  var txt='A $'+P.value+' car after '+Y.value+' years at '+R.value+'%/yr: '+OUT.textContent+'. Depreciation is the real cost - check yours (free):';
  var url=location.origin+location.pathname+'?p='+P.value+'&y='+Y.value+'&r='+R.value;
  if(navigator.share){navigator.share({title:'Car depreciation',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-math','Share this math');},1500);}
});
})();
</script>
"""

# Jet lag: adaptation days by zones crossed and direction, with light strategy.
# Retention hooks: title result hook, tt_jetlag memory, URL state (?z=&d=), Web Share.
JETLAG = """<div class="tool" id="tt-jl">
  <div class="fields">
    <div class="field"><label for="jl-z">Time zones crossed</label><input type="number" id="jl-z" min="1" max="12" placeholder="7"></div>
    <div class="field"><label for="jl-d"><span data-i18n="lbl.direction">Direction</span></label><select id="jl-d"><option value="e">Eastward (losing hours)</option><option value="w">Westward (gaining hours)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="jl-out">–</span><span class="result-unit">days to feel normal</span></div>
  <div class="stats">
    <div class="stat"><b id="jl-shift">–</b><span>pre-shift before flying</span></div>
    <div class="stat"><b id="jl-light">–</b><span>light strategy</span></div>
    <div class="stat"><b id="jl-back">–</b><span>days to readjust home</span></div>
  </div>
  <div class="tool-note" id="jl-note"></div>
  <button type="button" class="tool-btn" id="jl-share" data-i18n="share.share-this-plan">Share this plan</button>
</div>
<script>(function(){
var Z=document.getElementById('jl-z'),D=document.getElementById('jl-d');
var OUT=document.getElementById('jl-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var z=parseInt(Z.value),d=D.value;
  if(!(z>=1&&z<=12)){OUT.textContent='–';
    ['jl-shift','jl-light','jl-back'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('jl-note').textContent='';document.title='Jet Lag Calculator - ToolTide';return;}
  var days=d==='e'?z*1.0:z*0.6;
  days=Math.max(1,Math.round(days));
  OUT.textContent=days;
  document.getElementById('jl-shift').textContent=Math.min(z,days)+' days (1h/day)';
  document.getElementById('jl-light').textContent=d==='e'?'morning light, avoid evening':'evening light, avoid dawn';
  document.getElementById('jl-back').textContent=d==='e'?Math.max(1,Math.round(z*0.6)):Math.max(1,z);
  document.getElementById('jl-note').textContent='Eastward is harder: your clock must advance, and the body resists sleeping early more than staying up late - hence roughly a day per zone east versus about half a day per zone west. The pre-shift is the pro move: move bedtime and meals 1 hour per day toward destination time before you fly, and most of the work is done on the ground. On arrival, light is the drug - '+ (d==='e'?'get bright morning light locally and wear sunglasses in the evening to hold the advance.':'seek evening light and stay up to local evening, letting dawn come late.')+' Caffeine before local noon; no alcohol on the plane - it costs more sleep than it buys.';
  document.title=days+' days to adapt - ToolTide';
}
function save(){try{localStorage.setItem('tt_jetlag',JSON.stringify({z:Z.value,d:D.value}));}catch(e){}}
[Z,D].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['z',Z],['d',D]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_jetlag')||'null');if(mem){Z.value=mem.z||'';D.value=mem.d||'e';}}catch(e){}}
calc();
document.getElementById('jl-share').addEventListener('click',function(){
  var txt=Z.value+' time zones '+(D.value==='e'?'east':'west')+'ward = about '+OUT.textContent+' days of jet lag. Plan yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?z='+Z.value+'&d='+D.value;
  if(navigator.share){navigator.share({title:'Jet lag plan',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-plan','Share this plan');},1500);}
});
})();
</script>
"""

PAINT = """<div class="tool" id="tt-pa">
  <div class="fields">
    <div class="field"><label for="pa-w">Wall width (m)</label><input type="number" id="pa-w" min="0.1" step="0.1" placeholder="4"></div>
    <div class="field"><label for="pa-h"><span data-i18n="lbl.wallheight">Wall height (m)</span></label><input type="number" id="pa-h" min="0.1" step="0.1" placeholder="2.5"></div>
    <div class="field"><label for="pa-n">Walls</label><input type="number" id="pa-n" min="1" step="1" placeholder="4"></div>
    <div class="field"><label for="pa-c"><span data-i18n="lbl.coats">Coats</span></label><input type="number" id="pa-c" min="1" max="4" step="1" placeholder="2"></div>
    <div class="field"><label for="pa-x">Doors + windows (m²)</label><input type="number" id="pa-x" min="0" step="0.1" placeholder="3"></div>
    <div class="field"><label for="pa-cv">Coverage (m² per litre, per coat)</label><input type="number" id="pa-cv" min="1" step="0.5" placeholder="10"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pa-out">–</span><span class="result-unit">litres of paint</span></div>
  <div class="stats">
    <div class="stat"><b id="pa-s1">–</b><span>paintable area</span></div>
    <div class="stat"><b id="pa-s2">–</b><span>litres per coat</span></div>
    <div class="stat"><b id="pa-s3">–</b><span>buy (10% spare)</span></div>
  </div>
  <div class="tool-note" id="pa-note"></div>
  <button type="button" class="tool-btn" id="pa-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['pa-w','pa-h','pa-n','pa-c','pa-x','pa-cv'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('pa-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(F[0].value),h=parseFloat(F[1].value),n=parseInt(F[2].value),c=parseInt(F[3].value),x=parseFloat(F[4].value),cv=parseFloat(F[5].value);
  var ok=w>0&&h>0&&n>=1&&c>=1&&cv>0;
  if(!ok){OUT.textContent='–';['pa-s1','pa-s2','pa-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('pa-note').textContent='';document.title='Paint Calculator - ToolTide';return;}
  var area=Math.max(w*h*n-(isNaN(x)?0:x),0);
  var litres=area*c/cv;
  var buy=litres*1.1;
  OUT.textContent=litres.toFixed(2);
  document.getElementById('pa-s1').textContent=area.toFixed(1)+' m²';
  document.getElementById('pa-s2').textContent=(area/cv).toFixed(2)+' L';
  document.getElementById('pa-s3').textContent=buy.toFixed(2)+' L';
  document.getElementById('pa-note').textContent='The tin wins over any calculator: check its stated coverage, because matte and deep-base paints spread differently. Two coats is the honest default - one-coat claims usually assume a flat colour over a primed surface. Painting dark over light (or the reverse)? Budget for a primer coat or a third coat, because pigment hiding is the real constraint, not wall area. The 10% spare absorbs roller waste, edges, and the patch-up you will want in six months.';
  document.title=litres.toFixed(1)+' L of paint needed - ToolTide';
}
function save(){try{localStorage.setItem('tt_paint',JSON.stringify({w:F[0].value,h:F[1].value,n:F[2].value,c:F[3].value,x:F[4].value,cv:F[5].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['w',F[0]],['h',F[1]],['n',F[2]],['c',F[3]],['x',F[4]],['cv',F[5]]].forEach(function(p){var v=qs(p[0]);if(v!==null){p[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_paint')||'null');if(mem){F[0].value=mem.w||'';F[1].value=mem.h||'';F[2].value=mem.n||'';F[3].value=mem.c||'';F[4].value=mem.x||'';F[5].value=mem.cv||'';}}catch(e){}}
calc();
document.getElementById('pa-share').addEventListener('click',function(){
  var txt='Painting '+document.getElementById('pa-s1').textContent+' needs about '+OUT.textContent+' L ('+document.getElementById('pa-s3').textContent+' with spare). Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?w='+F[0].value+'&h='+F[1].value+'&n='+F[2].value+'&c='+F[3].value+'&x='+F[4].value+'&cv='+F[5].value;
  if(navigator.share){navigator.share({title:'Paint estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

MULCH = """<div class="tool" id="tt-mu">
  <div class="fields">
    <div class="field"><label for="mu-l">Bed length (m)</label><input type="number" id="mu-l" min="0.1" step="0.1" placeholder="6"></div>
    <div class="field"><label for="mu-w">Bed width (m)</label><input type="number" id="mu-w" min="0.1" step="0.1" placeholder="2"></div>
    <div class="field"><label for="mu-d">Depth (cm)</label><input type="number" id="mu-d" min="1" max="30" step="0.5" placeholder="5"></div>
    <div class="field"><label for="mu-b">Bag size (litres)</label><input type="number" id="mu-b" min="1" step="1" placeholder="50"></div>
    <div class="field"><label for="mu-p">Price per bag (optional)</label><input type="number" id="mu-p" min="0" step="0.1" placeholder="0"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="mu-out">–</span><span class="result-unit">bags of mulch</span></div>
  <div class="stats">
    <div class="stat"><b id="mu-s1">–</b><span>bed area</span></div>
    <div class="stat"><b id="mu-s2">–</b><span>volume</span></div>
    <div class="stat"><b id="mu-s3">–</b><span>total cost</span></div>
  </div>
  <div class="tool-note" id="mu-note"></div>
  <button type="button" class="tool-btn" id="mu-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['mu-l','mu-w','mu-d','mu-b','mu-p'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('mu-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var l=parseFloat(F[0].value),w=parseFloat(F[1].value),d=parseFloat(F[2].value),b=parseInt(F[3].value),p=parseFloat(F[4].value);
  var ok=l>0&&w>0&&d>0&&b>0;
  if(!ok){OUT.textContent='–';['mu-s1','mu-s2','mu-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('mu-note').textContent='';document.title='Mulch Calculator - ToolTide';return;}
  var area=l*w;
  var vol=area*d/100;
  var bags=Math.ceil(vol*1000/b);
  OUT.textContent=bags;
  document.getElementById('mu-s1').textContent=area.toFixed(1)+' m²';
  document.getElementById('mu-s2').textContent=vol.toFixed(2)+' m³';
  document.getElementById('mu-s3').textContent=(p>0&&!isNaN(p))?(bags*p).toFixed(2):'set price';
  document.getElementById('mu-note').textContent='5 cm is the weed-suppressing sweet spot; 7-8 cm for bare soil or a refresh on old mulch. Past 10 cm you start starving tree and shrub roots of air, and mulch volcanoes piled against trunks invite rot - keep a hand-width clear. Bulk tip: 1 m³ of bulk mulch replaces about '+Math.ceil(1000/b)+' bags, so past a few cubic metres the delivered skip is usually cheaper and lighter on plastic.';
  document.title=bags+' bags of mulch - ToolTide';
}
function save(){try{localStorage.setItem('tt_mulch',JSON.stringify({l:F[0].value,w:F[1].value,d:F[2].value,b:F[3].value,p:F[4].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['l',F[0]],['w',F[1]],['d',F[2]],['b',F[3]],['p',F[4]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_mulch')||'null');if(mem){F[0].value=mem.l||'';F[1].value=mem.w||'';F[2].value=mem.d||'';F[3].value=mem.b||'';F[4].value=mem.p||'';}}catch(e){}}
calc();
document.getElementById('mu-share').addEventListener('click',function(){
  var txt=document.getElementById('mu-s1').textContent+' of beds at '+F[2].value+' cm deep = '+OUT.textContent+' bags of mulch. Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?l='+F[0].value+'&w='+F[1].value+'&d='+F[2].value+'&b='+F[3].value+'&p='+F[4].value;
  if(navigator.share){navigator.share({title:'Mulch estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

LAMINATE = """<div class="tool" id="tt-lm">
  <div class="fields">
    <div class="field"><label for="lm-l">Room length (m)</label><input type="number" id="lm-l" min="0.1" step="0.1" placeholder="4"></div>
    <div class="field"><label for="lm-w">Room width (m)</label><input type="number" id="lm-w" min="0.1" step="0.1" placeholder="3.5"></div>
    <div class="field"><label for="lm-p">Pack coverage (m²)</label><input type="number" id="lm-p" min="0.1" step="0.01" placeholder="2.1"></div>
    <div class="field"><label for="lm-s">Waste allowance (%)</label><input type="number" id="lm-s" min="0" max="25" step="1" placeholder="8"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="lm-out">–</span><span class="result-unit">packs of laminate</span></div>
  <div class="stats">
    <div class="stat"><b id="lm-s1">–</b><span>room area</span></div>
    <div class="stat"><b id="lm-s2">–</b><span>area with waste</span></div>
    <div class="stat"><b id="lm-s3">–</b><span>extra you buy</span></div>
  </div>
  <div class="tool-note" id="lm-note"></div>
  <button type="button" class="tool-btn" id="lm-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['lm-l','lm-w','lm-p','lm-s'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('lm-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var l=parseFloat(F[0].value),w=parseFloat(F[1].value),p=parseFloat(F[2].value),s=parseFloat(F[3].value);
  var ok=l>0&&w>0&&p>0&&!isNaN(s)&&s>=0;
  if(!ok){OUT.textContent='–';['lm-s1','lm-s2','lm-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('lm-note').textContent='';document.title='Laminate Flooring Calculator - ToolTide';return;}
  var area=l*w;
  var need=area*(1+s/100);
  var packs=Math.ceil(need/p);
  OUT.textContent=packs;
  document.getElementById('lm-s1').textContent=area.toFixed(2)+' m²';
  document.getElementById('lm-s2').textContent=need.toFixed(2)+' m²';
  document.getElementById('lm-s3').textContent=(packs*p-area).toFixed(2)+' m²';
  document.getElementById('lm-note').textContent='8% waste covers a straight-lay rectangular room; use 10-12% for L-shaped rooms, lots of doorways, or herringbone, and 15%+ for a 45° diagonal lay. The real pro habit: buy the full packs now and keep receipts - unopened packs usually go back, but a half-pack shortfall mid-job means hunting a matching batch number, because shade lots differ between production runs. Let the boxes sit in the room 48h before fitting so the boards acclimatise.';
  document.title=packs+' packs of laminate - ToolTide';
}
function save(){try{localStorage.setItem('tt_laminate',JSON.stringify({l:F[0].value,w:F[1].value,p:F[2].value,s:F[3].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['l',F[0]],['w',F[1]],['p',F[2]],['s',F[3]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_laminate')||'null');if(mem){F[0].value=mem.l||'';F[1].value=mem.w||'';F[2].value=mem.p||'';F[3].value=mem.s||'';}}catch(e){}}
calc();
document.getElementById('lm-share').addEventListener('click',function(){
  var txt=document.getElementById('lm-s1').textContent+' room = '+OUT.textContent+' packs of laminate (with '+F[3].value+'% waste). Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?l='+F[0].value+'&w='+F[1].value+'&p='+F[2].value+'&s='+F[3].value;
  if(navigator.share){navigator.share({title:'Laminate estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

WALLP = """<div class="tool" id="tt-wp">
  <div class="fields">
    <div class="field"><label for="wp-p">Perimeter of walls (m)</label><input type="number" id="wp-p" min="0.1" step="0.1" placeholder="14"></div>
    <div class="field"><label for="wp-h"><span data-i18n="lbl.wallheight">Wall height (m)</span></label><input type="number" id="wp-h" min="0.5" step="0.05" placeholder="2.5"></div>
    <div class="field"><label for="wp-rw">Roll width (m)</label><input type="number" id="wp-rw" min="0.1" step="0.01" placeholder="0.53"></div>
    <div class="field"><label for="wp-rl">Roll length (m)</label><input type="number" id="wp-rl" min="0.5" step="0.05" placeholder="10.05"></div>
    <div class="field"><label for="wp-r">Pattern repeat (cm, 0 if plain)</label><input type="number" id="wp-r" min="0" max="200" step="0.5" placeholder="0"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="wp-out">–</span><span class="result-unit">rolls of wallpaper</span></div>
  <div class="stats">
    <div class="stat"><b id="wp-s1">–</b><span>strips needed</span></div>
    <div class="stat"><b id="wp-s2">–</b><span>strips per roll</span></div>
    <div class="stat"><b id="wp-s3">–</b><span>cut length</span></div>
  </div>
  <div class="tool-note" id="wp-note"></div>
  <button type="button" class="tool-btn" id="wp-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['wp-p','wp-h','wp-rw','wp-rl','wp-r'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('wp-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var p=parseFloat(F[0].value),h=parseFloat(F[1].value),rw=parseFloat(F[2].value),rl=parseFloat(F[3].value),r=parseFloat(F[4].value);
  var ok=p>0&&h>0&&rw>0&&rl>0&&!isNaN(r)&&r>=0;
  if(!ok){OUT.textContent='–';['wp-s1','wp-s2','wp-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('wp-note').textContent='';document.title='Wallpaper Calculator - ToolTide';return;}
  var cut=h+0.1;
  if(r>0){var rm=r/100;cut=Math.ceil((h+0.1)/rm)*rm;}
  var spr=Math.floor(rl/cut);
  if(spr<1){OUT.textContent='0';
    ['wp-s1','wp-s2','wp-s3'].forEach(function(id){document.getElementById(id).textContent='–';});
    document.getElementById('wp-note').textContent='This roll is shorter than one cut length - check the roll dimensions, because no strip can be cut from it.';
    document.title='Roll too short - ToolTide';return;}
  var sn=Math.ceil(p/rw);
  var rolls=Math.ceil(sn/spr);
  OUT.textContent=rolls;
  document.getElementById('wp-s1').textContent=sn;
  document.getElementById('wp-s2').textContent=spr;
  document.getElementById('wp-s3').textContent=cut.toFixed(2)+' m';
  document.getElementById('wp-note').textContent=(r>0?'A '+r+' cm pattern repeat is the silent budget killer: every strip must start on the same point of the pattern, so the cut length rounds up to the next multiple of the repeat and the offcuts are not reusable. ':'Plain paper uses nearly the whole roll, which is why offcuts still cover above doors and windows. ')+'The 10 cm trim allowance per strip absorbs ceiling and skirting unevenness - walls are rarely square. Buy every roll from the same batch number (shade lots differ), and order one spare roll beyond this figure if the pattern is bold: future repairs need the same dye lot, and discontinued lines never come back.';
  document.title=rolls+' rolls of wallpaper - ToolTide';
}
function save(){try{localStorage.setItem('tt_wallpaper',JSON.stringify({p:F[0].value,h:F[1].value,rw:F[2].value,rl:F[3].value,r:F[4].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['p',F[0]],['h',F[1]],['rw',F[2]],['rl',F[3]],['r',F[4]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_wallpaper')||'null');if(mem){F[0].value=mem.p||'';F[1].value=mem.h||'';F[2].value=mem.rw||'';F[3].value=mem.rl||'';F[4].value=mem.r||'';}}catch(e){}}
calc();
document.getElementById('wp-share').addEventListener('click',function(){
  var txt=OUT.textContent+' rolls of wallpaper for '+F[0].value+' m of walls'+(parseFloat(F[4].value)>0?' with a '+F[4].value+' cm pattern repeat':'')+'. Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?p='+F[0].value+'&h='+F[1].value+'&rw='+F[2].value+'&rl='+F[3].value+'&r='+F[4].value;
  if(navigator.share){navigator.share({title:'Wallpaper estimate',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

DIAPERS = """<div class="tool" id="tt-dp">
  <div class="fields">
    <div class="field"><label for="dp-n">Diapers per day</label><input type="number" id="dp-n" min="1" max="20" step="1" placeholder="8"></div>
    <div class="field"><label for="dp-p">Price per diaper</label><input type="number" id="dp-p" min="0.01" step="0.01" placeholder="0.25"></div>
    <div class="field"><label for="dp-m">Months of diapering</label><input type="number" id="dp-m" min="1" max="48" step="1" placeholder="24"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="dp-out">–</span><span class="result-unit">total diaper cost</span></div>
  <div class="stats">
    <div class="stat"><b id="dp-s1">–</b><span>per day</span></div>
    <div class="stat"><b id="dp-s2">–</b><span>per month</span></div>
    <div class="stat"><b id="dp-s3">–</b><span>per year</span></div>
  </div>
  <div class="tool-note" id="dp-note"></div>
  <button type="button" class="tool-btn" id="dp-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['dp-n','dp-p','dp-m'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('dp-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function fmt(v){return v.toFixed(2);}
function calc(){
  var n=parseInt(F[0].value),p=parseFloat(F[1].value),m=parseInt(F[2].value);
  var ok=n>=1&&p>0&&m>=1;
  if(!ok){OUT.textContent='–';['dp-s1','dp-s2','dp-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('dp-note').textContent='';document.title='Diaper Cost Calculator - ToolTide';return;}
  var day=n*p,mon=day*30.44,tot=mon*m;
  OUT.textContent=fmt(tot);
  document.getElementById('dp-s1').textContent=fmt(day);
  document.getElementById('dp-s2').textContent=fmt(mon);
  document.getElementById('dp-s3').textContent=fmt(mon*12);
  document.getElementById('dp-note').textContent='Count drift is the line nobody prices in: newborns burn 10-12 a day, toddlers are down to 4-6, so a flat per-day figure overstates the later months. Wipes, cream and bags typically add 15-20% on top. Cloth crossover: a full cloth stash costs roughly one to three months of disposables, so past month two or three it is paid off - if you actually run the washes at 60°C.';
  document.title=fmt(tot)+' total diaper cost - ToolTide';
}
function save(){try{localStorage.setItem('tt_diaper',JSON.stringify({n:F[0].value,p:F[1].value,m:F[2].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['n',F[0]],['p',F[1]],['m',F[2]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_diaper')||'null');if(mem){F[0].value=mem.n||'';F[1].value=mem.p||'';F[2].value=mem.m||'';}}catch(e){}}
calc();
document.getElementById('dp-share').addEventListener('click',function(){
  var txt=OUT.textContent+' of diapers over '+F[2].value+' months (about '+document.getElementById('dp-s2').textContent+'/month). Price yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?n='+F[0].value+'&p='+F[1].value+'&m='+F[2].value;
  if(navigator.share){navigator.share({title:'Diaper cost',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

WAKE = """<div class="tool" id="tt-ww">
  <div class="fields">
    <div class="field"><label for="ww-a">Baby age (months)</label><input type="number" id="ww-a" min="0" max="24" step="1" placeholder="6"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ww-out">–</span><span class="result-unit">min wake window</span></div>
  <div class="stats">
    <div class="stat"><b id="ww-s1">–</b><span>wake window range</span></div>
    <div class="stat"><b id="ww-s2">–</b><span>naps per day</span></div>
    <div class="stat"><b id="ww-s3">–</b><span>total sleep / day</span></div>
  </div>
  <div class="tool-note" id="ww-note"></div>
  <button type="button" class="tool-btn" id="ww-share" data-i18n="share.share-this-guide">Share this guide</button>
</div>
<script>(function(){
var A=document.getElementById('ww-a');
var OUT=document.getElementById('ww-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
var RANGES=[[0,45,60,'4-5','15-17 h'],[1,60,90,'4-5','14-16 h'],[3,75,105,'3-4','14-16 h'],[4,90,120,'3-4','12-15 h'],[5,120,150,'2-3','12-15 h'],[6,150,180,'2-3','12-14 h'],[9,150,210,'2','12-14 h'],[12,180,240,'1-2','11-14 h'],[18,240,360,'1','11-12 h']];
function calc(){
  var a=parseInt(A.value);
  if(!(a>=0&&a<=24)){OUT.textContent='–';['ww-s1','ww-s2','ww-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('ww-note').textContent='';document.title='Wake Window Calculator - ToolTide';return;}
  var r=RANGES[0];
  for(var i=0;i<RANGES.length;i++){if(a>=RANGES[i][0]){r=RANGES[i];}}
  OUT.textContent=r[1]+'-'+r[2];
  document.getElementById('ww-s1').textContent=(r[1]/60).toFixed(1)+'-'+(r[2]/60).toFixed(1)+' h';
  document.getElementById('ww-s2').textContent=r[3];
  document.getElementById('ww-s3').textContent=r[4];
  document.getElementById('ww-note').textContent='A wake window is how long a baby can comfortably stay up before sleep pressure wins - stretch it and you get cortisol instead of a longer nap, which is why overtired babies fight sleep hardest. Read the ranges as centre of gravity, not law: eye-rubbing, staring and fussing outrank the clock. The classic rhythm around 4-6 months is wake-feed-play, down at the first yawn, and the 2-3-4 pattern (2 h before nap one, 3 before nap two, 4 before bed) once naps consolidate to two.';
  document.title='Wake window '+r[1]+'-'+r[2]+' min at '+a+' months - ToolTide';
}
function save(){try{localStorage.setItem('tt_wake',JSON.stringify({a:A.value}));}catch(e){}}
A.addEventListener('input',function(){calc();save();});
var v=qs('a');
if(v!==null){A.value=v;}
else{try{var mem=JSON.parse(localStorage.getItem('tt_wake')||'null');if(mem){A.value=mem.a||'';}}catch(e){}}
calc();
document.getElementById('ww-share').addEventListener('click',function(){
  var txt='At '+A.value+' months, typical wake windows are '+OUT.textContent+' min. Check your baby (free, no sign-up):';
  var url=location.origin+location.pathname+'?a='+A.value;
  if(navigator.share){navigator.share({title:'Wake windows',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-guide','Share this guide');},1500);}
});
})();
</script>
"""

FORMULA = """<div class="tool" id="tt-ff">
  <div class="fields">
    <div class="field"><label for="ff-w">Baby weight (kg)</label><input type="number" id="ff-w" min="2" max="15" step="0.1" placeholder="5"></div>
    <div class="field"><label for="ff-f">Feeds per day</label><input type="number" id="ff-f" min="4" max="12" step="1" placeholder="7"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ff-out">–</span><span class="result-unit">ml per feed (typical)</span></div>
  <div class="stats">
    <div class="stat"><b id="ff-s1">–</b><span>range per feed</span></div>
    <div class="stat"><b id="ff-s2">–</b><span>total per day</span></div>
    <div class="stat"><b id="ff-s3">–</b><span>fl oz per feed</span></div>
  </div>
  <div class="tool-note" id="ff-note"></div>
  <button type="button" class="tool-btn" id="ff-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['ff-w','ff-f'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('ff-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(F[0].value),f=parseInt(F[1].value);
  var ok=w>=2&&w<=15&&f>=4&&f<=12;
  if(!ok){OUT.textContent='–';['ff-s1','ff-s2','ff-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('ff-note').textContent='';document.title='Formula Feeding Calculator - ToolTide';return;}
  var per=w*150/f;
  OUT.textContent=Math.round(per);
  document.getElementById('ff-s1').textContent=Math.round(w*120/f)+'-'+Math.round(w*200/f)+' ml';
  document.getElementById('ff-s2').textContent=Math.round(w*150)+' ml';
  document.getElementById('ff-s3').textContent=(per/29.574).toFixed(1)+' oz';
  document.getElementById('ff-note').textContent='The 150 ml per kg per day rule is the standard mid-point; normal runs 120-200 ml/kg/day depending on age, growth spurts and prematurity. Feed the baby, not the spreadsheet: finishing the bottle is not a goal, and hungry cues before the next feed matter more than the arithmetic. Never dilute or concentrate formula to stretch it, and check any feeding concern with your pediatrician first.';
  document.title=Math.round(per)+' ml per formula feed - ToolTide';
}
function save(){try{localStorage.setItem('tt_formula',JSON.stringify({w:F[0].value,f:F[1].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['w',F[0]],['f',F[1]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_formula')||'null');if(mem){F[0].value=mem.w||'';F[1].value=mem.f||'';}}catch(e){}}
calc();
document.getElementById('ff-share').addEventListener('click',function(){
  var txt='At '+F[0].value+' kg and '+F[1].value+' feeds/day: about '+OUT.textContent+' ml per feed. Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?w='+F[0].value+'&f='+F[1].value;
  if(navigator.share){navigator.share({title:'Formula feeding',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

PROTEIN = """<div class="tool" id="tt-pr">
  <div class="fields">
    <div class="field"><label for="pr-w"><span data-i18n="lbl.bodyweight">Body weight (kg)</span></label><input type="number" id="pr-w" min="30" max="200" step="0.5" placeholder="75"></div>
    <div class="field"><label for="pr-g">Goal</label><select id="pr-g"><option value="sed">General health (sedentary)</option><option value="act" selected>Active / training</option><option value="bld">Building muscle</option><option value="cut">Cutting (fat loss)</option><option value="old">Older adult (60+)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="pr-out">–</span><span class="result-unit">g protein per day</span></div>
  <div class="stats">
    <div class="stat"><b id="pr-s1">–</b><span>range</span></div>
    <div class="stat"><b id="pr-s2">–</b><span>per meal (×4)</span></div>
    <div class="stat"><b id="pr-s3">–</b><span>chicken breast equiv.</span></div>
  </div>
  <div class="tool-note" id="pr-note"></div>
  <button type="button" class="tool-btn" id="pr-share" data-i18n="share.share-this-target">Share this target</button>
</div>
<script>(function(){
var W=document.getElementById('pr-w'),G=document.getElementById('pr-g');
var OUT=document.getElementById('pr-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
var RG={sed:[0.8,1.0],act:[1.2,1.6],bld:[1.6,2.2],cut:[1.8,2.4],old:[1.2,1.5]};
function calc(){
  var w=parseFloat(W.value),g=G.value;
  if(!(w>=30&&w<=200)){OUT.textContent='–';['pr-s1','pr-s2','pr-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('pr-note').textContent='';document.title='Protein Intake Calculator - ToolTide';return;}
  var r=RG[g],lo=w*r[0],hi=w*r[1],mid=(lo+hi)/2;
  OUT.textContent=Math.round(mid);
  document.getElementById('pr-s1').textContent=Math.round(lo)+'-'+Math.round(hi)+' g';
  document.getElementById('pr-s2').textContent=Math.round(mid/4)+' g';
  document.getElementById('pr-s3').textContent=Math.round(mid/31*100)+' g';
  document.getElementById('pr-note').textContent='Ranges per kg of bodyweight, not per kg of magic: sedentary adults hold at 0.8, training pushes needs to 1.2-1.6, muscle building tops out near 2.2 - beyond that extra protein is just expensive energy. Cutting raises the target because protein protects muscle in a deficit. The chicken figure uses 31 g per 100 g cooked breast; eggs run about 6.5 g each, greek yogurt 10 g per 100 g, lentils 9 g per 100 g cooked. Spread it over 3-4 meals: muscle protein synthesis responds to per-meal doses near 0.4 g/kg, not one giant dinner.';
  document.title=Math.round(mid)+' g protein per day - ToolTide';
}
function save(){try{localStorage.setItem('tt_protein',JSON.stringify({w:W.value,g:G.value}));}catch(e){}}
[W,G].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['w',W],['g',G]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_protein')||'null');if(mem){W.value=mem.w||'';G.value=mem.g||'act';}}catch(e){}}
calc();
document.getElementById('pr-share').addEventListener('click',function(){
  var txt=Math.round(parseFloat(W.value)*(RG[G.value][0]+RG[G.value][1])/2)+' g protein a day for '+W.value+' kg. Get yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?w='+W.value+'&g='+G.value;
  if(navigator.share){navigator.share({title:'Protein target',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-target','Share this target');},1500);}
});
})();
</script>
"""

CREATINE = """<div class="tool" id="tt-cr">
  <div class="fields">
    <div class="field"><label for="cr-w"><span data-i18n="lbl.bodyweight">Body weight (kg)</span></label><input type="number" id="cr-w" min="30" max="200" step="0.5" placeholder="75"></div>
    <div class="field"><label for="cr-m">Protocol</label><select id="cr-m"><option value="load" selected>With loading week</option><option value="maint">Maintenance only</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cr-out">–</span><span class="result-unit">g per day (maintenance)</span></div>
  <div class="stats">
    <div class="stat"><b id="cr-s1">–</b><span>maintenance range</span></div>
    <div class="stat"><b id="cr-s2">–</b><span>loading dose</span></div>
    <div class="stat"><b id="cr-s3">–</b><span>days of 500 g tub</span></div>
  </div>
  <div class="tool-note" id="cr-note"></div>
  <button type="button" class="tool-btn" id="cr-share" data-i18n="share.share-this-dose">Share this dose</button>
</div>
<script>(function(){
var W=document.getElementById('cr-w'),M=document.getElementById('cr-m');
var OUT=document.getElementById('cr-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(W.value),m=M.value;
  if(!(w>=30&&w<=200)){OUT.textContent='–';['cr-s1','cr-s2','cr-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('cr-note').textContent='';document.title='Creatine Calculator - ToolTide';return;}
  var lo=w*0.03,hi=w*0.05,mid=Math.max(3,(lo+hi)/2);
  OUT.textContent=mid.toFixed(1);
  document.getElementById('cr-s1').textContent=Math.max(3,lo).toFixed(1)+'-'+Math.min(5,hi).toFixed(1)+' g';
  document.getElementById('cr-s2').textContent=m==='load'?(w*0.3).toFixed(0)+' g/day × 5-7 days':'skipped';
  document.getElementById('cr-s3').textContent=Math.round(500/mid);
  document.getElementById('cr-note').textContent=(m==='load'?'Loading saturates muscles in about a week: '+(w*0.3).toFixed(0)+' g/day split into 4 doses, then drop to maintenance. ':'Skipping loading is fine - 3-5 g a day reaches the same saturation in 3-4 weeks. ')+'Do not cycle creatine: it is not a stimulant, and stopping just drains the stores you paid to fill. Expect 1-2 kg of water weight in the first weeks - that is the mechanism, not fat. Monohydrate is the cheapest and most-studied form; fancy versions buy marketing, not results. Healthy kidneys handle it fine; anyone with kidney disease should ask a doctor first.';
  document.title=mid.toFixed(1)+' g creatine a day - ToolTide';
}
function save(){try{localStorage.setItem('tt_creatine',JSON.stringify({w:W.value,m:M.value}));}catch(e){}}
[W,M].forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['w',W],['m',M]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_creatine')||'null');if(mem){W.value=mem.w||'';M.value=mem.m||'load';}}catch(e){}}
calc();
document.getElementById('cr-share').addEventListener('click',function(){
  var txt=OUT.textContent+' g creatine a day for '+W.value+' kg'+(M.value==='load'?' after a loading week':'')+'. Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?w='+W.value+'&m='+M.value;
  if(navigator.share){navigator.share({title:'Creatine dose',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-dose','Share this dose');},1500);}
});
})();
</script>
"""

DATAUSAGE = """<div class="tool" id="tt-du">
  <div class="fields">
    <div class="field"><label for="du-s">Streaming quality</label><select id="du-s"><option value="0.7">SD (0.7 GB/h)</option><option value="3" selected>HD (3 GB/h)</option><option value="7">4K (7 GB/h)</option></select></div>
    <div class="field"><label for="du-sh">Streaming hours/day</label><input type="number" id="du-sh" min="0" max="16" step="0.5" placeholder="2"></div>
    <div class="field"><label for="du-mu">Music hours/day</label><input type="number" id="du-mu" min="0" max="16" step="0.5" placeholder="1"></div>
    <div class="field"><label for="du-vc">Video calls hours/day</label><input type="number" id="du-vc" min="0" max="12" step="0.5" placeholder="0.5"></div>
    <div class="field"><label for="du-we">Web + social hours/day</label><input type="number" id="du-we" min="0" max="16" step="0.5" placeholder="2"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="du-out">–</span><span class="result-unit">GB per month</span></div>
  <div class="stats">
    <div class="stat"><b id="du-s1">–</b><span>GB per day</span></div>
    <div class="stat"><b id="du-s2">–</b><span>streaming share</span></div>
    <div class="stat"><b id="du-s3">–</b><span>unlimited-plan cut</span></div>
  </div>
  <div class="tool-note" id="du-note"></div>
  <button type="button" class="tool-btn" id="du-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['du-s','du-sh','du-mu','du-vc','du-we'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('du-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var st=parseFloat(F[0].value),sh=parseFloat(F[1].value),mu=parseFloat(F[2].value),vc=parseFloat(F[3].value),we=parseFloat(F[4].value);
  var ok=st>0&&sh>=0&&mu>=0&&vc>=0&&we>=0;
  if(!ok){OUT.textContent='–';['du-s1','du-s2','du-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('du-note').textContent='';document.title='Data Usage Calculator - ToolTide';return;}
  var streamGB=st*sh,day=streamGB+mu*0.1+vc*1.2+we*0.35;
  var mon=day*30.44;
  OUT.textContent=Math.round(mon);
  document.getElementById('du-s1').textContent=day.toFixed(1)+' GB';
  document.getElementById('du-s2').textContent=day>0?Math.round(streamGB/day*100)+'%':'0%';
  document.getElementById('du-s3').textContent=Math.round(mon)+' GB';
  document.getElementById('du-note').textContent='Quality is the lever that moves everything: one hour of 4K eats as much as 10 hours of SD, so dropping one notch on a capped plan saves more than any other tweak. Music at high streaming quality runs about 0.1 GB/h, HD video calls 1.2 GB/h, social feeds with autoplay video 0.3-0.5 GB/h. Downloads and OS updates arrive in spikes - add about 5-10 GB a month of background noise before comparing against a mobile plan cap. Home broadband caps are usually 1 TB+: if this figure clears 800 GB, check for stray cloud backups, not Netflix.';
  document.title=Math.round(mon)+' GB per month - ToolTide';
}
function save(){try{localStorage.setItem('tt_data',JSON.stringify({s:F[0].value,sh:F[1].value,mu:F[2].value,vc:F[3].value,we:F[4].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['s',F[0]],['sh',F[1]],['mu',F[2]],['vc',F[3]],['we',F[4]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_data')||'null');if(mem){F[0].value=mem.s||'3';F[1].value=mem.sh||'';F[2].value=mem.mu||'';F[3].value=mem.vc||'';F[4].value=mem.we||'';}}catch(e){}}
calc();
document.getElementById('du-share').addEventListener('click',function(){
  var txt='My household burns about '+OUT.textContent+' GB a month. Measure yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?s='+F[0].value+'&sh='+F[1].value+'&mu='+F[2].value+'&vc='+F[3].value+'&we='+F[4].value;
  if(navigator.share){navigator.share({title:'Data usage',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

FLIGHTDELAY = """<div class="tool" id="tt-fd">
  <div class="fields">
    <div class="field"><label for="fd-k">Flight distance (km)</label><input type="number" id="fd-k" min="0" max="20000" step="50" placeholder="1800"></div>
    <div class="field"><label for="fd-h">Arrival delay (hours)</label><input type="number" id="fd-h" min="0" max="72" step="0.5" placeholder="5"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="fd-out">–</span><span class="result-unit">fixed compensation</span></div>
  <div class="stats">
    <div class="stat"><b id="fd-s1">–</b><span>distance band</span></div>
    <div class="stat"><b id="fd-s2">–</b><span>threshold</span></div>
    <div class="stat"><b id="fd-s3">–</b><span>also claimable</span></div>
  </div>
  <div class="tool-note" id="fd-note"></div>
  <button type="button" class="tool-btn" id="fd-share" data-i18n="share.share-this-result">Share this result</button>
</div>
<script>(function(){
var K=document.getElementById('fd-k'),H=document.getElementById('fd-h');
var OUT=document.getElementById('fd-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var k=parseFloat(K.value),h=parseFloat(H.value);
  if(!(k>=0&&k<=20000&&h>=0&&h<=72)){OUT.textContent='–';['fd-s1','fd-s2','fd-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('fd-note').textContent='';document.title='Flight Delay Compensation Calculator - ToolTide';return;}
  var band=k<=1500?'short':(k<=3500?'medium':'long');
  var amt=0,why='';
  if(h<3){amt=0;why='Under 3 hours of arrival delay there is no fixed compensation - but the airline still owes care: meals, and a hotel if the delay runs overnight.';}
  else if(band==='short'){amt=250;why='Flights up to 1,500 km pay a flat 250 for a 3-hour-plus arrival delay.';}
  else if(band==='medium'){amt=400;why='EU-internal flights over 1,500 km and other 1,500-3,500 km flights pay 400.';}
  else {amt=(h<4)?300:600;why='Long-haul over 3,500 km pays 600 - halved to 300 when the arrival delay stays under 4 hours.';}
  OUT.textContent=amt>0?amt:0;
  document.getElementById('fd-s1').textContent=band==='short'?'up to 1,500 km':(band==='medium'?'1,500-3,500 km':'over 3,500 km');
  document.getElementById('fd-s2').textContent=h<3?'no fixed claim':(h<4?'3-4 h band':'4 h+ band');
  document.getElementById('fd-s3').textContent='receipts + reroute';
  document.getElementById('fd-note').textContent=why+' Two fine points: the clock is arrival delay at the final destination, not departure - a 2-hour late takeoff that lands 3:15 late still qualifies. And extraordinary circumstances (severe weather, air-traffic control strikes) can excuse the airline from the fixed sum, but never from the duty of care. Keep boarding passes and receipts: meals, hotels, taxis and rebooking costs are claimable on top regardless. Claims stay open for years - six in England and Wales - and no-woo legal firms typically take a cut you can keep by claiming direct with the airline first.';
  document.title=(amt>0?amt+' fixed compensation':'No fixed claim')+' - ToolTide';
}
function save(){try{localStorage.setItem('tt_flightdelay',JSON.stringify({k:K.value,h:H.value}));}catch(e){}}
[K,H].forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var pre=false;
[['k',K],['h',H]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_flightdelay')||'null');if(mem){K.value=mem.k||'';H.value=mem.h||'';}}catch(e){}}
calc();
document.getElementById('fd-share').addEventListener('click',function(){
  var txt='Delay of '+H.value+' h on a '+K.value+' km flight = fixed compensation '+OUT.textContent+'. Check yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?k='+K.value+'&h='+H.value;
  if(navigator.share){navigator.share({title:'Flight delay compensation',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-result','Share this result');},1500);}
});
})();
</script>
"""

SUBS = """<div class="tool" id="tt-sub">
  <div class="fields">
    <div class="field"><label for="su-p1">Subscription 1: price</label><input type="number" id="su-p1" min="0" step="0.01" placeholder="12.99"></div>
    <div class="field"><label for="su-f1">billed</label><select id="su-f1"><option value="m" selected>monthly</option><option value="q">quarterly</option><option value="y">yearly</option></select></div>
    <div class="field"><label for="su-p2">Subscription 2: price</label><input type="number" id="su-p2" min="0" step="0.01" placeholder="8.99"></div>
    <div class="field"><label for="su-f2">billed</label><select id="su-f2"><option value="m" selected>monthly</option><option value="q">quarterly</option><option value="y">yearly</option></select></div>
    <div class="field"><label for="su-p3">Subscription 3: price</label><input type="number" id="su-p3" min="0" step="0.01" placeholder="5.99"></div>
    <div class="field"><label for="su-f3">billed</label><select id="su-f3"><option value="m" selected>monthly</option><option value="q">quarterly</option><option value="y">yearly</option></select></div>
    <div class="field"><label for="su-p4">Subscription 4: price</label><input type="number" id="su-p4" min="0" step="0.01" placeholder="59.99"></div>
    <div class="field"><label for="su-f4">billed</label><select id="su-f4"><option value="m">monthly</option><option value="q">quarterly</option><option value="y" selected>yearly</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="su-out">–</span><span class="result-unit">per year, all subscriptions</span></div>
  <div class="stats">
    <div class="stat"><b id="su-s1">–</b><span>per month</span></div>
    <div class="stat"><b id="su-s2">–</b><span>biggest cost</span></div>
    <div class="stat"><b id="su-s3">–</b><span>cut biggest, save</span></div>
  </div>
  <div class="tool-note" id="su-note"></div>
  <button type="button" class="tool-btn" id="su-share" data-i18n="share.share-this-audit">Share this audit</button>
</div>
<script>(function(){
var F=['su-p1','su-f1','su-p2','su-f2','su-p3','su-f3','su-p4','su-f4'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('su-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function mon(p,f){return f==='m'?p:(f==='q'?p/3:p/12);}
function calc(){
  var t=0,big=0,bigIdx=-1;
  for(var i=0;i<4;i++){var p=parseFloat(F[i*2].value)||0;var m=mon(p,F[i*2+1].value);t+=m;if(m>big){big=m;bigIdx=i;}}
  OUT.textContent=(t*12).toFixed(0);
  document.getElementById('su-s1').textContent=t.toFixed(2);
  document.getElementById('su-s2').textContent=big>0?big.toFixed(2)+'/mo':(bigIdx+1);
  document.getElementById('su-s3').textContent=(big*12).toFixed(0)+'/yr';
  document.getElementById('su-note').textContent='The yearly figure is the honest one: monthly pricing hides that 12.99 a month is 155.88 a year. Annual billing on anything you kept all last year typically cuts 15-20%, and pausing beats cancelling for seasonal services - many streaming plans now hold your list for 1-3 months. The audit rule: if you cannot remember opening it last month, that line is the cut.';
  document.title=(t*12).toFixed(0)+' a year on subscriptions - ToolTide';
}
function save(){try{localStorage.setItem('tt_subs',JSON.stringify({p1:F[0].value,f1:F[1].value,p2:F[2].value,f2:F[3].value,p3:F[4].value,f3:F[5].value,p4:F[6].value,f4:F[7].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var ks=['p1','f1','p2','f2','p3','f3','p4','f4'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_subs')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('su-share').addEventListener('click',function(){
  var txt=OUT.textContent+' a year on subscriptions. Audit yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'Subscription audit',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-audit','Share this audit');},1500);}
});
})();
</script>
"""

SILVERVAL = """<div class="tool" id="tt-sv">
  <div class="fields">
    <div class="field"><label for="sv-w">Silver weight (g)</label><input type="number" id="sv-w" min="0.1" step="0.1" placeholder="100"></div>
    <div class="field"><label for="sv-p">Purity</label><select id="sv-p"><option value="0.999" selected>Fine silver 999</option><option value="0.925">Sterling 925</option><option value="0.800">Continental 800</option></select></div>
    <div class="field"><label for="sv-s">Spot price ($ per troy oz)</label><input type="number" id="sv-s" min="1" step="0.01" placeholder="30"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="sv-out">–</span><span class="result-unit">melt value</span></div>
  <div class="stats">
    <div class="stat"><b id="sv-s1">–</b><span>fine silver content</span></div>
    <div class="stat"><b id="sv-s2">–</b><span>per gram</span></div>
    <div class="stat"><b id="sv-s3">–</b><span>typical dealer offer</span></div>
  </div>
  <div class="tool-note" id="sv-note"></div>
  <button type="button" class="tool-btn" id="sv-share" data-i18n="share.share-this-value">Share this value</button>
</div>
<script>(function(){
var F=['sv-w','sv-p','sv-s'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('sv-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(F[0].value),p=parseFloat(F[1].value),s=parseFloat(F[2].value);
  var ok=w>0&&p>0&&s>0;
  if(!ok){OUT.textContent='–';['sv-s1','sv-s2','sv-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('sv-note').textContent='';document.title='Silver Value Calculator - ToolTide';return;}
  var fine=w*p;
  var val=fine*s/31.1035;
  OUT.textContent=val.toFixed(2);
  document.getElementById('sv-s1').textContent=fine.toFixed(1)+' g';
  document.getElementById('sv-s2').textContent=(p*s/31.1035).toFixed(2);
  document.getElementById('sv-s3').textContent=(val*0.88).toFixed(2);
  document.getElementById('sv-note').textContent='Melt value is the floor, not the quote: dealers pay 85-95% of spot for scrap, so weigh offers against the 88% mid-figure shown. hallmarks first - 925 stamped sterling and 999 bullion price cleanly, while unmarked plate and silver-plated ware are worth roughly nothing by weight. A troy ounce is 31.1035 g, the unit every spot price quotes. Coins and antique pieces can carry collector value above melt: check sold listings on two marketplaces before melting anything with a date, portrait or maker mark.';
  document.title=val.toFixed(0)+' silver melt value - ToolTide';
}
function save(){try{localStorage.setItem('tt_silver',JSON.stringify({w:F[0].value,p:F[1].value,s:F[2].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var pre=false;
[['w',F[0]],['p',F[1]],['s',F[2]]].forEach(function(x){var v=qs(x[0]);if(v!==null){x[1].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_silver')||'null');if(mem){F[0].value=mem.w||'';F[1].value=mem.p||'0.999';F[2].value=mem.s||'';}}catch(e){}}
calc();
document.getElementById('sv-share').addEventListener('click',function(){
  var txt=F[0].value+' g of silver = '+OUT.textContent+' melt value. Value yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?w='+F[0].value+'&p='+F[1].value+'&s='+F[2].value;
  if(navigator.share){navigator.share({title:'Silver value',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-value','Share this value');},1500);}
});
})();
</script>
"""

YARN = """<div class="tool" id="tt-yn">
  <div class="fields">
    <div class="field"><label for="yn-sw">Swatch width (cm)</label><input type="number" id="yn-sw" min="1" step="0.5" placeholder="10"></div>
    <div class="field"><label for="yn-sh">Swatch height (cm)</label><input type="number" id="yn-sh" min="1" step="0.5" placeholder="10"></div>
    <div class="field"><label for="yn-sy">Yarn used in swatch (m)</label><input type="number" id="yn-sy" min="0.1" step="0.1" placeholder="25"></div>
    <div class="field"><label for="yn-pw">Project width (cm)</label><input type="number" id="yn-pw" min="1" step="1" placeholder="100"></div>
    <div class="field"><label for="yn-ph">Project height (cm)</label><input type="number" id="yn-ph" min="1" step="1" placeholder="100"></div>
    <div class="field"><label for="yn-sk">Skein size (m)</label><input type="number" id="yn-sk" min="1" step="1" placeholder="200"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="yn-out">–</span><span class="result-unit">metres of yarn needed</span></div>
  <div class="stats">
    <div class="stat"><b id="yn-s1">–</b><span>with 15% buffer</span></div>
    <div class="stat"><b id="yn-s2">–</b><span>skeins to buy</span></div>
    <div class="stat"><b id="yn-s3">–</b><span>project ÷ swatch area</span></div>
  </div>
  <div class="tool-note" id="yn-note"></div>
  <button type="button" class="tool-btn" id="yn-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['yn-sw','yn-sh','yn-sy','yn-pw','yn-ph','yn-sk'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('yn-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var sw=parseFloat(F[0].value),sh=parseFloat(F[1].value),sy=parseFloat(F[2].value),pw=parseFloat(F[3].value),ph=parseFloat(F[4].value),sk=parseFloat(F[5].value);
  var ok=sw>0&&sh>0&&sy>0&&pw>0&&ph>0&&sk>0;
  if(!ok){OUT.textContent='–';['yn-s1','yn-s2','yn-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('yn-note').textContent='';document.title='Yarn Yardage Calculator - ToolTide';return;}
  var ratio=(pw*ph)/(sw*sh);
  var need=sy*ratio;
  OUT.textContent=Math.round(need);
  document.getElementById('yn-s1').textContent=Math.round(need*1.15)+' m';
  document.getElementById('yn-s2').textContent=Math.ceil(need*1.15/sk);
  document.getElementById('yn-s3').textContent=ratio.toFixed(1)+'×';
  document.getElementById('yn-note').textContent='The swatch is the only honest yardstick: knit it in the project stitch, measure it relaxed after blocking, and weigh or measure the yarn it ate (a kitchen scale and grams-per-metre from the ball band works if unravelling is not). The 15% buffer covers tension drift, sampling and the sleeves you reknit. Dye lots are the trap the maths cannot fix: however many skeins you buy, buy them from one lot number, because replacement skeins a month later rarely match. Leftover yarn is not waste - it is the repair stash for the decade after.';
  document.title=Math.round(need)+' m of yarn needed - ToolTide';
}
function save(){try{localStorage.setItem('tt_yarn',JSON.stringify({sw:F[0].value,sh:F[1].value,sy:F[2].value,pw:F[3].value,ph:F[4].value,sk:F[5].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});});
var ks=['sw','sh','sy','pw','ph','sk'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_yarn')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('yn-share').addEventListener('click',function(){
  var txt='That project needs about '+OUT.textContent+' m of yarn ('+document.getElementById('yn-s2').textContent+' skeins). Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'Yarn yardage',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
"""

CASTON = """<div class="tool" id="tt-co">
  <div class="fields">
    <div class="field"><label for="co-h">Head circumference (cm)</label><input type="number" id="co-h" min="30" max="70" step="0.5" placeholder="56"></div>
    <div class="field"><label for="co-g">Gauge (stitches per 10 cm)</label><input type="number" id="co-g" min="8" max="40" step="0.5" placeholder="20"></div>
    <div class="field"><label for="co-n">Negative ease (cm)</label><input type="number" id="co-n" min="0" max="6" step="0.5" placeholder="2.5"></div>
    <div class="field"><label for="co-m">Pattern multiple</label><select id="co-m"><option value="1" selected>Any (stockinette)</option><option value="2">×2 (2×2 rib needs 4)</option><option value="4">×4 (2×2 rib)</option><option value="6">×6 (cable panels)</option><option value="8">×8 (lace repeats)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="co-out">–</span><span class="result-unit">stitches to cast on</span></div>
  <div class="stats">
    <div class="stat"><b id="co-s1">–</b><span>raw stitches</span></div>
    <div class="stat"><b id="co-s2">–</b><span>adjusted to multiple</span></div>
    <div class="stat"><b id="co-s3">–</b><span>finished stretch</span></div>
  </div>
  <div class="tool-note" id="co-note"></div>
  <button type="button" class="tool-btn" id="co-share" data-i18n="share.share-this-number">Share this number</button>
</div>
<script>(function(){
var F=['co-h','co-g','co-n','co-m'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('co-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var h=parseFloat(F[0].value),g=parseFloat(F[1].value),n=parseFloat(F[2].value),m=parseInt(F[3].value);
  var ok=h>=30&&h<=70&&g>=8&&g<=40&&n>=0&&n<=6&&m>=1;
  if(!ok){OUT.textContent='–';['co-s1','co-s2','co-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('co-note').textContent='';document.title='Knitting Cast-On Calculator - ToolTide';return;}
  var raw=(h-n)*g/10;
  var adj=m>1?Math.round(raw/m)*m:Math.round(raw);
  OUT.textContent=adj;
  document.getElementById('co-s1').textContent=Math.round(raw);
  document.getElementById('co-s2').textContent=m>1?('nearest multiple of '+m):'no multiple needed';
  document.getElementById('co-s3').textContent=(adj/(g/10)).toFixed(1)+' cm';
  document.getElementById('co-note').textContent='Negative ease is the reason knitted hats stay on: 2-3 cm smaller than the head, because ribbing and stockinette stretch to fit and relax back. The gauge must come from your own blocked swatch in the project stitch - not the ball band, which quotes a generic figure. If the pattern multiple knocks you more than 2-3 stitches off raw, go one needle size up or down rather than stretching the multiple, or the brim puckers or bags. Cast on, knit the brim, try it on: the number is a starting point, the head is the boss.';
  document.title='Cast on '+adj+' stitches - ToolTide';
}
function save(){try{localStorage.setItem('tt_caston',JSON.stringify({h:F[0].value,g:F[1].value,n:F[2].value,m:F[3].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var ks=['h','g','n','m'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_caston')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('co-share').addEventListener('click',function(){
  var txt='Cast on '+OUT.textContent+' stitches for a '+F[0].value+' cm head. Get yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'Cast-on count',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-number','Share this number');},1500);}
});
})();
</script>
"""

CURTAIN = """<div class="tool" id="tt-cu">
  <div class="fields">
    <div class="field"><label for="cu-w">Track or pole width (cm)</label><input type="number" id="cu-w" min="40" max="600" step="1" placeholder="150"></div>
    <div class="field"><label for="cu-d">Finished drop (cm)</label><input type="number" id="cu-d" min="30" max="350" step="1" placeholder="137"></div>
    <div class="field"><label for="cu-f">Fullness</label><select id="cu-f"><option value="1.5">1.5× (flat/eyelet)</option><option value="2" selected>2× (pencil pleat)</option><option value="2.5">2.5× (pinch pleat)</option></select></div>
    <div class="field"><label for="cu-r">Fabric roll width (cm)</label><input type="number" id="cu-r" min="90" max="300" step="1" placeholder="137"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="cu-out">–</span><span class="result-unit">metres of fabric</span></div>
  <div class="stats">
    <div class="stat"><b id="cu-s1">–</b><span>panels / widths</span></div>
    <div class="stat"><b id="cu-s2">–</b><span>cut length each</span></div>
    <div class="stat"><b id="cu-s3">–</b><span>gathering width</span></div>
  </div>
  <div class="tool-note" id="cu-note"></div>
  <button type="button" class="tool-btn" id="cu-share" data-i18n="share.share-this-estimate">Share this estimate</button>
</div>
<script>(function(){
var F=['cu-w','cu-d','cu-f','cu-r'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('cu-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var w=parseFloat(F[0].value),d=parseFloat(F[1].value),f=parseFloat(F[2].value),r=parseFloat(F[3].value);
  var ok=w>=40&&w<=600&&d>=30&&d<=350&&r>=90&&r<=300;
  if(!ok){OUT.textContent='–';['cu-s1','cu-s2','cu-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('cu-note').textContent='';document.title='Curtain Fabric Calculator - ToolTide';return;}
  var gather=w*f;
  var panels=Math.ceil(gather/r);
  var cut=d+30;
  var meters=panels*cut/100;
  OUT.textContent=meters.toFixed(1);
  document.getElementById('cu-s1').textContent=panels;
  document.getElementById('cu-s2').textContent=cut.toFixed(0)+' cm';
  document.getElementById('cu-s3').textContent=gather.toFixed(0)+' cm';
  document.getElementById('cu-note').textContent='The 30 cm added per panel covers a double-turned 15 cm hem plus heading allowance - the difference between curtains that hang and curtains that flap. Fullness is the look: pencil pleat wants double the track width, pinch pleat two and a half, eyelet rings manage with less. Fabric with a visible pattern repeat needs extra per drop so the design matches across panels - add one repeat per panel beyond the first, and buy it all from one dye lot. Always buy a spare 10% over the figure: curtain fabric goes out of print faster than any yarn.';
  document.title=meters.toFixed(1)+' m of curtain fabric - ToolTide';
}
function save(){try{localStorage.setItem('tt_curtain',JSON.stringify({w:F[0].value,d:F[1].value,f:F[2].value,r:F[3].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var ks=['w','d','f','r'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_curtain')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('cu-share').addEventListener('click',function(){
  var txt='Those curtains need about '+OUT.textContent+' m of fabric ('+document.getElementById('cu-s1').textContent+' panels). Measure yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'Curtain fabric',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent=TT('ui.copied','Copied!');var b=this;setTimeout(function(){b.textContent=TT('share.share-this-estimate','Share this estimate');},1500);}
});
})();
</script>
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
    "finalgrade": lambda args: FINALGRADE,
    "water": lambda args: WATER,
    "tdee": lambda args: TDEE,
    "tipsplit": lambda args: TIPSPLIT,
    "heatindex": lambda args: HEATINDEX,
    "bmi": lambda args: BMI,
    "windchill": lambda args: WINDCHILL,
    "pace": lambda args: PACE,
    "macros": lambda args: MACROS,
    "electricity": lambda args: ELECTRIC,
    "bodyfat": lambda args: BODYFAT,
    "oven": lambda args: OVEN,
    "cgpa": lambda args: CGPA,
    "caffeine": lambda args: CAFFEINE,
    "gst": lambda args: GST,
    "overtime": lambda args: OVERTIME,
    "rent": lambda args: RENT,
    "fuelcost": lambda args: FUELCOST,
    "commission": lambda args: COMMISSION,
    "airfryer": lambda args: AIRFRYER,
    "loanpay": lambda args: LOANPAY,
    "vatcalc": lambda args: VATCALC,
    "fraction": lambda args: FRACTION,
    "pregnancy": lambda args: PREGNANCY,
    "tzconvert": lambda args: TZCONVERT,
    "weeknum": lambda args: WEEKNUM,
    "timecard": lambda args: TIMECARD,
    "onerepmax": lambda args: ONEREPMAX,
    "stddev": lambda args: STDDEV,
    "concrete": lambda args: CONCRETE,
    "slopecalc": lambda args: SLOPECALC,
    "teamgen": lambda args: TEAMGEN,
    "paintcalc": lambda args: PAINTCALC,
    "tilecalc": lambda args: TILECALC,
    "halfbday": lambda args: HALFBDAY,
    "ratiocalc": lambda args: RATIOCALC,
    "calburn": lambda args: CALBURN,
    "debtpayoff": lambda args: DEBTPAYOFF,
    "jsontool": lambda args: JSONTOOL,
    "base64": lambda args: BASE64,
    "urlcod": lambda args: URLCOD,
    "jwtdecode": lambda args: JWTDECODE,
    "amortize": lambda args: AMORTIZE,
    "csv2json": lambda args: CSV2JSON,
    "onlinetimer": lambda args: ONLINETIMER,
    "stopwatch": lambda args: STOPWATCH,
    "stockavg": lambda args: STOCKAVG,
    "possize": lambda args: POSSIZE,
    "lotto": lambda args: LOTTO,
    "pomodoro": lambda args: POMODORO,
    "passstrength": lambda args: PASSSTRENGTH,
    "cryptoprofit": lambda args: CRYPTOPROFIT,
    "petagedog": lambda args: PETAGE.replace("__SPECIES__", "dog"),
    "petagecat": lambda args: PETAGE.replace("__SPECIES__", "cat"),
    "flesch": lambda args: FLESCH,
    "dewpoint": lambda args: DEWPOINT,
    "btucalc": lambda args: BTUCALC,
    "tire": lambda args: TIRE,
    "hrzone": lambda args: HRZONE,
    "golf": lambda args: GOLF,
    "bpmdelay": lambda args: BPMDelay,
    "evcharge": lambda args: EVCHARGE,
    "goldenhour": lambda args: GOLDEN,
    "pizza": lambda args: PIZZA,
    "inflation": lambda args: INFLATION,
    "sleepdebt": lambda args: SLEEPDEBT,
    "coffee": lambda args: COFFEE,
    "breakeven": lambda args: BREAKEVEN,
    "idealweight": lambda args: IDEALW,
    "lorem": lambda args: LOREM,
    "cagr": lambda args: CAGR,
    "pool": lambda args: POOL,
    "timespent": lambda args: TIMESPENT,
    "meattime": lambda args: MEATTIME,
    "cardep": lambda args: CARDEP,
    "jetlag": lambda args: JETLAG,
    "paint": lambda args: PAINT,
    "mulch": lambda args: MULCH,
    "laminate": lambda args: LAMINATE,
    "wallp": lambda args: WALLP,
    "diapers": lambda args: DIAPERS,
    "wake": lambda args: WAKE,
    "formula": lambda args: FORMULA,
    "protein": lambda args: PROTEIN,
    "creatine": lambda args: CREATINE,
    "datausage": lambda args: DATAUSAGE,
    "flightdelay": lambda args: FLIGHTDELAY,
    "subs": lambda args: SUBS,
    "silverval": lambda args: SILVERVAL,
    "yarn": lambda args: YARN,
    "caston": lambda args: CASTON,
    "curtain": lambda args: CURTAIN,
}


TT_SNIPPET = ('<script>window.TT=function(k,f){try{var v=window.npT?window.npT(k):null;'
               '}catch(e){}return v||f};'
               # a focused number input silently mutates on wheel while the user
               # scrolls the page — block that; typing and arrow keys still work
               'document.addEventListener("wheel",function(e){var t=e.target;'
               'if(t&&t.type==="number"&&document.activeElement===t)e.preventDefault();},'
               '{passive:false});</script>')


def render(tool, args):
    return TT_SNIPPET + TOOLS[tool](args)
