TVSIZE = """<div class="tool" id="tt-ts">
  <div class="fields">
    <div class="field"><label for="ts-d">Viewing distance (m)</label><input type="number" id="ts-d" min="0.5" max="10" step="0.1" placeholder="2.5"></div>
    <div class="field"><label for="ts-r">Content resolution</label><select id="ts-r"><option value="1.5" selected>4K UHD</option><option value="2.2">1080p Full HD</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ts-out">–</span><span class="result-unit">inch screen size</span></div>
  <div class="stats">
    <div class="stat"><b id="ts-s1">–</b><span>screen width</span></div>
    <div class="stat"><b id="ts-s2">–</b><span>4K size at same seat</span></div>
    <div class="stat"><b id="ts-s3">–</b><span>too-close limit</span></div>
  </div>
  <div class="tool-note" id="ts-note"></div>
  <button type="button" class="tool-btn" id="ts-share">Share this size</button>
</div>
<script>(function(){
var F=['ts-d','ts-r'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('ts-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var d=parseFloat(F[0].value),r=parseFloat(F[1].value);
  var ok=d>=0.5&&d<=10;
  if(!ok){OUT.textContent='–';['ts-s1','ts-s2','ts-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('ts-note').textContent='';document.title='TV Size Calculator - ToolTide';return;}
  var inch=d*39.37/r;
  var nice=Math.round(inch/2)*2;
  OUT.textContent=nice;
  var wcm=nice*2.54*0.872;
  document.getElementById('ts-s1').textContent=Math.round(wcm)+' cm wide';
  document.getElementById('ts-s2').textContent=r===1.5?'that is the 4K figure':Math.round(d*39.37/1.5/2)*2+' inch';
  document.getElementById('ts-s3').textContent=(nice*2.54/100*0.8).toFixed(1)+' m for this size';
  document.getElementById('ts-note').textContent='Screen size is the upgrade people actually notice - resolution differences at sofa distance are subtle, size is not, which is why showrooms feel bigger than living rooms. The maths: divide seat distance by 1.5 for 4K (close enough that pixels vanish) or 2.2 for 1080p, where closer seating starts resolving individual pixels. Two reality checks: measure the stand or wall width against the screen width shown - a 65-inch panel is about 145 cm wide, stands included; and low-quality upscaling, not the panel, is what makes 1080p broadcast look soft on a big 4K set, so the source matters as much as the diagonal.';
  document.title=nice+' inch TV for your sofa - ToolTide';
}
function save(){try{localStorage.setItem('tt_tvsize',JSON.stringify({d:F[0].value,r:F[1].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var ks=['d','r'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_tvsize')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('ts-share').addEventListener('click',function(){
  var txt='At '+F[0].value+' m, the right TV is about '+OUT.textContent+' inch. Size yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'TV size',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share this size';},1500);}
});
})();
</script>
"""

FISHTANK = """<div class="tool" id="tt-ft">
  <div class="fields">
    <div class="field"><label for="ft-l">Tank volume (litres)</label><input type="number" id="ft-l" min="10" max="2000" step="1" placeholder="100"></div>
    <div class="field"><label for="ft-s">Adult fish size (cm)</label><input type="number" id="ft-s" min="1" max="40" step="0.5" placeholder="4"></div>
    <div class="field"><label for="ft-t">Stock type</label><select id="ft-t"><option value="1.0" selected>Tropical community</option><option value="1.5">Cichlids / territorial</option><option value="2.5">Goldfish (heavy waste)</option></select></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ft-out">–</span><span class="result-unit">fish at adult size</span></div>
  <div class="stats">
    <div class="stat"><b id="ft-s1">–</b><span>total cm of fish</span></div>
    <div class="stat"><b id="ft-s2">–</b><span>litres per fish</span></div>
    <div class="stat"><b id="ft-s3">–</b><span>weekly water change</span></div>
  </div>
  <div class="tool-note" id="ft-note"></div>
  <button type="button" class="tool-btn" id="ft-share">Share this stocking</button>
</div>
<script>(function(){
var F=['ft-l','ft-s','ft-t'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('ft-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var l=parseFloat(F[0].value),s=parseFloat(F[1].value),t=parseFloat(F[2].value);
  var ok=l>=10&&l<=2000&&s>=1&&s<=40;
  if(!ok){OUT.textContent='–';['ft-s1','ft-s2','ft-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('ft-note').textContent='';document.title='Fish Tank Stocking Calculator - ToolTide';return;}
  var cmTotal=l/t;
  var n=Math.floor(cmTotal/s);
  OUT.textContent=n;
  document.getElementById('ft-s1').textContent=cmTotal.toFixed(0)+' cm';
  document.getElementById('ft-s2').textContent=(l/Math.max(n,1)).toFixed(1)+' L';
  document.getElementById('ft-s3').textContent=(l*0.25).toFixed(0)+' L';
  document.getElementById('ft-note').textContent='The one-centimetre-per-litre rule works on ADULT size, and forgetting that is the classic beginner failure: the cute 5 cm juveniles grow into 25 cm adults in a tank that cannot filter their waste. Goldfish need their own multiple because they are ammonia factories, not because of size. Before any fish goes in: the tank must cycle 4-6 weeks (the nitrogen colony grows on the filter, not in the water), and stock in small batches over weeks so the biology keeps pace. The weekly change shown - a quarter of the tank, dechlorinated and temperature-matched - does more for fish health than any gadget; test strips lie less than opinions, so keep nitrates under about 40 and let the water tell you when the plan is wrong.';
  document.title=n+' fish for a '+l+' L tank - ToolTide';
}
function save(){try{localStorage.setItem('tt_fishtank',JSON.stringify({l:F[0].value,s:F[1].value,t:F[2].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var ks=['l','s','t'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_fishtank')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('ft-share').addEventListener('click',function(){
  var txt='A '+F[0].value+' L tank supports about '+OUT.textContent+' fish at adult size. Stock yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'Tank stocking',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share this stocking';},1500);}
});
})();
</script>
"""

LAUNDRY = """<div class="tool" id="tt-ld">
  <div class="fields">
    <div class="field"><label for="ld-k">Drum / load size (kg)</label><input type="number" id="ld-k" min="3" max="12" step="0.5" placeholder="8"></div>
    <div class="field"><label for="ld-s">Soil level</label><select id="ld-s"><option value="0.75">Light (worn once)</option><option value="1" selected>Normal</option><option value="1.3">Heavy (sports, work)</option></select></div>
    <div class="field"><label for="ld-h">Water hardness</label><select id="ld-h"><option value="0.85">Soft</option><option value="1" selected>Medium</option><option value="1.25">Hard</option></select></div>
    <div class="field"><label for="ld-p">Price per litre of liquid (optional)</label><input type="number" id="ld-p" min="0" step="0.1" placeholder="3"></div>
  </div>
  <div class="result" aria-live="polite" aria-atomic="true"><span class="result-num" id="ld-out">–</span><span class="result-unit">ml of liquid detergent</span></div>
  <div class="stats">
    <div class="stat"><b id="ld-s1">–</b><span>powder scoop equivalent</span></div>
    <div class="stat"><b id="ld-s2">–</b><span>per year (~220 washes)</span></div>
    <div class="stat"><b id="ld-s3">–</b><span>yearly cost</span></div>
  </div>
  <div class="tool-note" id="ld-note"></div>
  <button type="button" class="tool-btn" id="ld-share">Share this dose</button>
</div>
<script>(function(){
var F=['ld-k','ld-s','ld-h','ld-p'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('ld-out');
function qs(k){return new URLSearchParams(location.search).get(k);}
function calc(){
  var k=parseFloat(F[0].value),s=parseFloat(F[1].value),h=parseFloat(F[2].value),p=parseFloat(F[3].value);
  var ok=k>=3&&k<=12;
  if(!ok){OUT.textContent='–';['ld-s1','ld-s2','ld-s3'].forEach(function(id){document.getElementById(id).textContent='–';});document.getElementById('ld-note').textContent='';document.title='Laundry Detergent Calculator - ToolTide';return;}
  var ml=50*s*h*Math.sqrt(k/8);
  OUT.textContent=Math.round(ml);
  document.getElementById('ld-s1').textContent=Math.round(ml*0.55)+' g';
  document.getElementById('ld-s2').textContent=(ml*220/1000).toFixed(1)+' L';
  document.getElementById('ld-s3').textContent=(p>0&&!isNaN(p))?(ml*220/1000*p).toFixed(0):'set price';
  document.getElementById('ld-note').textContent='More detergent does not clean more: excess surfactant has nowhere to go, deposits on fibres as the grey stiff film that makes towels crunchy and feeds the mould that smells. The dose scales with soil and hardness, and only weakly with drum size - a bigger drum is mostly air. Brands print generous tables because they sell detergent by the litre; halving a heavy-handed habit is free laundry. Pods are the exception: pre-measured for an average load, they cannot flex down for a half drum, so run them only on full loads. And the biggest lever is not chemistry - a 30 °C wash with a decent dose beats a 40 °C wash you overloaded the machine for.';
  document.title=Math.round(ml)+' ml detergent per wash - ToolTide';
}
function save(){try{localStorage.setItem('tt_laundry',JSON.stringify({k:F[0].value,s:F[1].value,h:F[2].value,p:F[3].value}));}catch(e){}}
F.forEach(function(el){el.addEventListener('input',function(){calc();save();});el.addEventListener('change',function(){calc();save();});});
var ks=['k','s','h','p'],pre=false;
ks.forEach(function(k,i){var v=qs(k);if(v!==null){F[i].value=v;pre=true;}});
if(!pre){try{var mem=JSON.parse(localStorage.getItem('tt_laundry')||'null');if(mem){ks.forEach(function(k,i){if(mem[k]!==undefined&&mem[k]!==''){F[i].value=mem[k];}});}}catch(e){}}
calc();
document.getElementById('ld-share').addEventListener('click',function(){
  var txt='Right detergent dose for my washes: '+OUT.textContent+' ml. Dose yours (free, no sign-up):';
  var url=location.origin+location.pathname+'?'+ks.map(function(k,i){return k+'='+encodeURIComponent(F[i].value);}).join('&');
  if(navigator.share){navigator.share({title:'Laundry dose',text:txt,url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(txt+' '+url);this.textContent='Copied!';var b=this;setTimeout(function(){b.textContent='Share this dose';},1500);}
});
})();
</script>
"""
