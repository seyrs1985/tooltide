# -*- coding: utf-8 -*-
"""R143:.ics 推广第二页(dst-sleep-shift-planner),复用 R140 模式"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

sub('  <button type="button" class="tool-btn" id="dst-share" data-i18n="share.share-my-shiftplan">Share my shift plan</button>',
    """  <button type="button" class="tool-btn" id="dst-share" data-i18n="share.share-my-shiftplan">Share my shift plan</button>
  <button type="button" class="tool-btn" id="dst-ics">Add to calendar (.ics)</button>""")

sub("var R=document.getElementById('dst-r'),P=document.getElementById('dst-p');",
    """var R=document.getElementById('dst-r'),P=document.getElementById('dst-p');
var lastSt=null;""")

sub("  document.title=TT('dst.fallback','Fall back ')+cs+' - ToolDune';",
    """  document.title=TT('dst.fallback','Fall back ')+cs+' - ToolDune';
  lastSt=st;""")

sub("document.getElementById('dst-share').addEventListener('click',function(){",
    """function ymd2(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('dst-ics').addEventListener('click',function(){
  if(!lastSt){return;}
  var end=new Date(lastSt.getTime()+86400000);
  var NL=String.fromCharCode(13,10);
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymd2(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymd2(lastSt)+NL+'DTEND;VALUE=DATE:'+ymd2(end)+NL+'SUMMARY:Begin bedtime shift for the clock change'+NL+'DESCRIPTION:Move bedtime '+P.value+' minutes later daily until the fall-back date. Plan by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='clock-change-shift-plan.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('dst-share').addEventListener('click',function(){""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R143 ics promo OK: dst-sleep gets .ics export, 4 anchors, ast passed")
