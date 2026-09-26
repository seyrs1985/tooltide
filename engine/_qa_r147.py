# -*- coding: utf-8 -*-
"""R147:.ics 推广第五、六页(movetl 4里程碑多事件 + examplan 双事件),R140 模式升级多 VEVENT"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

# ---------- MOVETL ----------
sub('  <button type="button" class="tool-btn" id="mt-share">Share this plan</button>',
    """  <button type="button" class="tool-btn" id="mt-share">Share this plan</button>
  <button type="button" class="tool-btn" id="mt-ics">Add plan to calendar (.ics)</button>""")

sub("""var D=document.getElementById('mt-d');
var OUT=document.getElementById('mt-out');""",
    """var D=document.getElementById('mt-d');
var OUT=document.getElementById('mt-out');
var lastDay=null;""")

sub("document.title='Moving Timeline Planner - ToolDune';return;}",
    "document.title='Moving Timeline Planner - ToolDune';lastDay=null;return;}")

sub("  document.title=days+' days to moving day - ToolDune';",
    """  document.title=days+' days to moving day - ToolDune';
  lastDay=day;""")

sub("""document.getElementById('mt-share').addEventListener('click',function(){
  var txt=OUT.textContent+' days to my move - plan: '""",
    """function ymdM(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('mt-ics').addEventListener('click',function(){
  if(!lastDay){return;}
  var NL=String.fromCharCode(13,10);
  var EV=[[56,'Book the mover - get three quotes'],[42,'Declutter before any box exists'],[7,'Final week - confirm crew and first-night box'],[0,'Moving day']];
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN';
  for(var i=0;i<EV.length;i++){
    var dt=new Date(lastDay.getTime()-EV[i][0]*86400000);
    ics+=NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'-'+i+'@tooldune.com'+NL+'DTSTAMP:'+ymdM(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdM(dt)+NL+'DTEND;VALUE=DATE:'+ymdM(new Date(dt.getTime()+86400000))+NL+'SUMMARY:'+EV[i][1]+NL+'END:VEVENT';
  }
  ics+=NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='moving-plan.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add plan to calendar (.ics)';},1500);
});
document.getElementById('mt-share').addEventListener('click',function(){
  var txt=OUT.textContent+' days to my move - plan: '""")

# ---------- EXAMPLAN ----------
sub('  <button type="button" class="tool-btn" id="xp-share">Share this plan</button>',
    """  <button type="button" class="tool-btn" id="xp-share">Share this plan</button>
  <button type="button" class="tool-btn" id="xp-ics">Add to calendar (.ics)</button>""")

sub("var F=['xp-d','xp-s'].map(function(id){return document.getElementById(id);});",
    """var F=['xp-d','xp-s'].map(function(id){return document.getElementById(id);});
var lastExam=null;""")

sub("document.title='Exam Study Planner - ToolDune';return;}",
    "document.title='Exam Study Planner - ToolDune';lastExam=null;return;}")

sub("  document.title=days+' days to exam - ToolDune';",
    """  document.title=days+' days to exam - ToolDune';
  lastExam=day;""")

sub("document.getElementById('xp-share').addEventListener('click',function(){",
    """function ymdX(dt){function p(n){return (n<10?'0':'')+n;}return ''+dt.getFullYear()+p(dt.getMonth()+1)+p(dt.getDate());}
document.getElementById('xp-ics').addEventListener('click',function(){
  if(!lastExam){return;}
  var NL=String.fromCharCode(13,10);
  var EV=[[7,'Final week - recall drills only, no new topics'],[0,'Exam day']];
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN';
  for(var i=0;i<EV.length;i++){
    var dt=new Date(lastExam.getTime()-EV[i][0]*86400000);
    ics+=NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'-'+i+'@tooldune.com'+NL+'DTSTAMP:'+ymdX(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymdX(dt)+NL+'DTEND;VALUE=DATE:'+ymdX(new Date(dt.getTime()+86400000))+NL+'SUMMARY:'+EV[i][1]+NL+'END:VEVENT';
  }
  ics+=NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='exam-plan.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('xp-share').addEventListener('click',function(){""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R147 ics promo OK: movetl(4-event) + examplan(2-event), 10 anchors, ast passed")
