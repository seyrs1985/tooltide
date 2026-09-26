# -*- coding: utf-8 -*-
"""R145:.ics 推广第三、四页(carvetiming 雕刻日 + frostplan 冬备启动日),复用 R140/R143 模式"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

# ---------- CARVETIMING ----------
sub('  <button type="button" class="tool-btn" id="carve-share">Share my carving date</button>',
    """  <button type="button" class="tool-btn" id="carve-share">Share my carving date</button>
  <button type="button" class="tool-btn" id="carve-ics">Add to calendar (.ics)</button>""")

sub("var M=document.getElementById('carve-m');",
    """var M=document.getElementById('carve-m');
var lastCarve=null;""")

sub("  document.title='Carve on '+cs+' - ToolDune';",
    """  document.title='Carve on '+cs+' - ToolDune';
  lastCarve=carve;""")

sub("document.getElementById('carve-share').addEventListener('click',function(){",
    """function ymdC(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('carve-ics').addEventListener('click',function(){
  if(!lastCarve){return;}
  var end=new Date(lastCarve.getTime()+86400000);
  var NL=String.fromCharCode(13,10);
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymdC(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdC(lastCarve)+NL+'DTEND;VALUE=DATE:'+ymdC(end)+NL+'SUMMARY:Carve the Jack-o-lantern'+NL+'DESCRIPTION:Carving-day by preservation method so it is fresh for Halloween. Plan by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='pumpkin-carving-day.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('carve-share').addEventListener('click',function(){""")

# ---------- FROSTPLAN ----------
sub('  <button type="button" class="tool-btn" id="ff-share">Share my frost plan</button>',
    """  <button type="button" class="tool-btn" id="ff-share">Share my frost plan</button>
  <button type="button" class="tool-btn" id="ff-ics">Add to calendar (.ics)</button>""")

sub("var D=document.getElementById('ff-d');",
    """var D=document.getElementById('ff-d');
var lastFrost=null;""")

sub("  document.title='First frost in '+days+' days - ToolDune';",
    """  document.title='First frost in '+days+' days - ToolDune';
  lastFrost=f;""")

sub("""document.getElementById('ff-share').addEventListener('click',function(){
  var txt='First frost: '""",
    """function ymdF(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('ff-ics').addEventListener('click',function(){
  if(!lastFrost){return;}
  var prep=new Date(lastFrost.getTime()-42*86400000);
  var end=new Date(prep.getTime()+86400000);
  var NL=String.fromCharCode(13,10);
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymdF(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdF(prep)+NL+'DTEND;VALUE=DATE:'+ymdF(end)+NL+'SUMMARY:Start winterizing before first frost'+NL+'DESCRIPTION:Stop feeding and pest-check the pots coming inside - six weeks before your average first frost. Plan by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='winter-prep-start.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('ff-share').addEventListener('click',function(){
  var txt='First frost: '""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R145 ics promo OK: carvetiming + frostplan get .ics export, 8 anchors, ast passed")
