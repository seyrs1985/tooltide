# -*- coding: utf-8 -*-
"""R149:.ics 推广收尾第七、八页(shipdead 寄出死线 + cactusbloom 长夜起始)"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

# ---------- CACTUSBLOOM ----------
sub('  <button type="button" class="tool-btn" id="cb-share">Share my bloom plan</button>',
    """  <button type="button" class="tool-btn" id="cb-share">Share my bloom plan</button>
  <button type="button" class="tool-btn" id="cb-ics">Add to calendar (.ics)</button>""")

sub("var D=document.getElementById('cb-d');",
    """var D=document.getElementById('cb-d');
var lastSt=null;""")

sub("""  var v=D.value;if(!v){return;}
  var p=v.split('-');
  var t=new Date(parseInt(p[0],10),parseInt(p[1],10)-1,parseInt(p[2],10));""",
    """  var v=D.value;if(!v){lastSt=null;return;}
  var p=v.split('-');
  var t=new Date(parseInt(p[0],10),parseInt(p[1],10)-1,parseInt(p[2],10));""")

sub("  document.title='Start dark nights on '+sd+' - ToolDune';",
    """  document.title='Start dark nights on '+sd+' - ToolDune';
  lastSt=st;""")

sub("""document.getElementById('cb-share').addEventListener('click',function(){
  var txt='For blooms by '""",
    """function ymdCB(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('cb-ics').addEventListener('click',function(){
  if(!lastSt){return;}
  var end=new Date(lastSt.getTime()+86400000);
  var NL=String.fromCharCode(13,10);
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymdCB(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdCB(lastSt)+NL+'DTEND;VALUE=DATE:'+ymdCB(end)+NL+'SUMMARY:Start long nights for Christmas cactus blooms'+NL+'DESCRIPTION:13 hours of total darkness nightly for 8 weeks. Plan by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='cactus-bloom-schedule.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('cb-share').addEventListener('click',function(){
  var txt='For blooms by '""")

# ---------- SHIPDEAD ----------
sub('  <button type="button" class="tool-btn" id="sh2-share">Share this deadline</button>',
    """  <button type="button" class="tool-btn" id="sh2-share">Share this deadline</button>
  <button type="button" class="tool-btn" id="sh2-ics">Add to calendar (.ics)</button>""")

sub("""var F=['sh2-d','sh2-r'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('sh2-out');""",
    """var F=['sh2-d','sh2-r'].map(function(id){return document.getElementById(id);});
var OUT=document.getElementById('sh2-out');
var lastPost=null;""")

sub("document.title='Holiday Shipping Calculator - ToolDune';return;}",
    "document.title='Holiday Shipping Calculator - ToolDune';lastPost=null;return;}")

sub("  document.title='Post by '+OUT.textContent+' - ToolDune';",
    """  document.title='Post by '+OUT.textContent+' - ToolDune';
  lastPost=post;""")

sub("document.getElementById('sh2-share').addEventListener('click',function(){",
    """function ymdSD(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('sh2-ics').addEventListener('click',function(){
  if(!lastPost){return;}
  var end=new Date(lastPost.getTime()+86400000);
  var NL=String.fromCharCode(13,10);
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymdSD(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdSD(lastPost)+NL+'DTEND;VALUE=DATE:'+ymdSD(end)+NL+'SUMMARY:Last safe day to post the package'+NL+'DESCRIPTION:Includes the peak-season half-transit buffer. Plan by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='shipping-deadline.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('sh2-share').addEventListener('click',function(){""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R149 ics finale OK: shipdead + cactusbloom get .ics export, 8 anchors, ast passed")
