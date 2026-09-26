# -*- coding: utf-8 -*-
"""R140 存量质量轮:.ics 日历导出试点(turkey-thaw),LESSONS #9 五选菜单最后一项的落地模式"""
import io

P = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"

def sub(old, new, n=1):
    global SRC
    assert SRC.count(old) == n, "anchor not %dx: %r" % (n, old[:60])
    SRC = SRC.replace(old, new)

with io.open(P, encoding="utf-8") as f:
    SRC = f.read()

# 1) HTML:分享按钮旁加 .ics 按钮
sub('  <button type="button" class="tool-btn" id="tt2-share">Share this schedule</button>',
    """  <button type="button" class="tool-btn" id="tt2-share">Share this schedule</button>
  <button type="button" class="tool-btn" id="tt2-ics">Add to calendar (.ics)</button>""")

# 2) 作用域变量
sub("var F=['tt2-d','tt2-w'].map(function(id){return document.getElementById(id);});",
    """var F=['tt2-d','tt2-w'].map(function(id){return document.getElementById(id);});
var lastThaw=null,lastServe=null;""")

# 3) 失效时清空 lastThaw
sub("document.title='Turkey Thaw Calculator - ToolDune';return;}",
    "document.title='Turkey Thaw Calculator - ToolDune';lastThaw=null;return;}")

# 4) 成功时记录
sub("document.title='Start thawing '+OUT.textContent+' - ToolDune';",
    """document.title='Start thawing '+OUT.textContent+' - ToolDune';
  lastThaw=thaw;lastServe=day;""")

# 5) .ics 下载函数与监听(插在 share 监听前)
sub("document.getElementById('tt2-share').addEventListener('click',function(){",
    """function ymd(dt){return ''+dt.getFullYear()+fmt(dt.getMonth()+1)+fmt(dt.getDate());}
document.getElementById('tt2-ics').addEventListener('click',function(){
  if(!lastThaw){return;}
  var end=new Date(lastThaw.getTime()+86400000);
  var NL=String.fromCharCode(13,10);
  var ics='BEGIN:VCALENDAR'+NL+'VERSION:2.0'+NL+'PRODID:-//ToolDune//EN'+NL+'BEGIN:VEVENT'+NL+'UID:'+Date.now()+'@tooldune.com'+NL+'DTSTAMP:'+ymd(new Date())+'T120000Z'+NL+'DTSTART;VALUE=DATE:'+ymd(lastThaw)+NL+'DTEND;VALUE=DATE:'+ymd(end)+NL+'SUMMARY:Start thawing the turkey'+NL+'DESCRIPTION:Fridge thaw starts - bottom shelf on a tray and breast-side down. Schedule by tooldune.com'+NL+'END:VEVENT'+NL+'END:VCALENDAR';
  var a=document.createElement('a');a.href='data:text/calendar;charset=utf-8,'+encodeURIComponent(ics);a.download='turkey-thaw-schedule.ics';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  this.textContent='Calendar file downloaded';
  var b=this;setTimeout(function(){b.textContent='Add to calendar (.ics)';},1500);
});
document.getElementById('tt2-share').addEventListener('click',function(){""")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(SRC)

import ast
ast.parse(SRC)
print("R140 ics pilot OK: turkey-thaw gets .ics export, 4 anchors, ast passed")
