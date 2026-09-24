# ToolTide i18n BUG 台账

格式:`编号|页面|语言|现象|截图|状态`。状态=待修/已修/范围外。每轮先视觉验证、记录,再修复,部署后线上复验回写。

## 待修
- 字段标签长尾(367种去重)|所有译文语言|模板静态label未接线(通用词+一次性技术标签)|rg清单|已修R13高频23种×9语言(64处实例:Units×14/Height/Weight/Sex/Mode等);余量为一次性技术标签长尾,随逐家族轮次接入
- Share按钮家族(92处)|所有译文语言|共享/复制链未本地化:静态标签与1.5s恢复标签共74种Share文案(Share this estimate×12等)+92处恢复赋值;反馈Copied!已R9本地化,仅剩按钮标签本身(内容性文案,量大可逐簇)|rg清单(uniq -c)|待修(下轮或分簇)
- BUG-013余量|其余渲染器家族|所有译文语言|动态字符串后缀类剩余量:校验/状态/复制反馈已R9清空,仍散见科普长注记(FLSA/折扣顺序等运行时note长句)与零星标签,随逐轮家族巡查接续(参照TT()键模式)|IAB DOM探针|待修(逐轮蚕食)
- BUG-013续6|pomodoro-timer|ko全部|计时器14处未接线:3字段标签+3stat+Start/Pause/Reset按钮+focus/break相位与document.title|IAB DOM探针|已修R14+线上复验(pomo.*14键×9语言;复验ko:시작/초기화/집중 시간(분)/오늘의 집중 블록/phase=집중 - 일시정지全韩;并补window load重跑render修解析期竞态第四例)
- BUG-013续7|stock-average-calculator+cagr-calculator|es/id各4处|stat标签与result单位未接线(new average cost/total shares/total invested/average lowered by;CAGR per year/total growth/multiple of start/years to double)|IAB DOM探针|已修R15+线上复验(sa.avgcost/shares/invested/lowered+cg.peryear/totgrowth/multiple/yrsdouble×8键×9语言;复验es/id:total saham/rata-rata turun sebesar/pertumbuhan total全对;savings-goal×ru全净)
- BUG-013续8|开发者族base64/urlencode等+heart-rate-zones|ja/ru|开发者族共享串19处未接线(output/input chars/output chars/UTF-8 bytes in/Copy output按钮+Nothing to copy/Invalid Base64/Malformed input)+hz静息心率/最大心率2处|IAB DOM探针|已修R16+线上复验(dev.output/inchars/outchars/utf8/copyout/nothing/invalidb64/malformed×8键×19处脚本化接线+hz.rest/maxhr×2键×9语言;curl直连实证服务HTML全接线;复验ru:Пульс в покое/максимальный пульс/Копировать вывод;注意b6-u为嵌套span结构属正常)
- BUG-013续9|tdee/json-formatter/jwt-decoder|全部译文语言|14处标签接线脚本属性插错位(生成<span> data-i18n=...>text</span>可见垃圾文本,审计曾放行因属合法HTML)|用户可见+curl实证|已修R17+线上复验(三页garbage=0;i18n_audit新增永久防错门:> data-i18n=出现即FAIL;教训=脚本接线后必须curl直连抽查渲染结果,审计/check_site都验不出文本级错位)
- BUG-013续10|seconds-converter|pt|①可见标签Total seconds/Duration (h:mm:ss or mm:ss)未接线;②发现out元素指向不存在元素(历史死代码,seconds后缀实际不可见,secconv.seconds/usehms键已备但为无操作)|IAB DOM探针(box全文无结果元素)|已修R19+线上复验(secconv.totalseconds/duration×2键×9语言;curl实证data-i18n在服务HTML;死代码留档不动)
- BUG-013续11|case-converter|ru/ja|8个大小写模式chip未接线(UPPERCASE/lowercase/Title Case/Sentence case/camelCase/snake_case/kebab-case/aLtErNaTiNg)+输入框placeholder|IAB DOM探针|已修R26+线上复验(case.upper/lower/title/sentence+case.ph×5键×9语言接线;camelCase/snake_case/kebab-case/aLtErNaTiNg为命名规范专名保留英文属范围外;curl实证case.upper/case.ph上线)
- BUG-013续11|全站高频裸span|所有译文语言|高频重复stat标签未接线TOP11(per month×4/total interest×3/you save×2/total paid×2/per year×2/per day×2/paintable area×2/full charge cost×2/day of year×2/cubic meters×2/words×2)|rg存量盘点|已修R20+部署(脚本化25处实例接lbl.permonth/peryear/perday+fin.totalinterest/totalpaid/yousave+paint.paintable+ev.fullcharge+date.dayofyear+conv.cubicmeters×10键×9语言,words复用既有wc.words;并行工作者卷带提交部署;长尾×1约300种留逐家族)
- BUG-013续12|fuel-cost-calculator(tt-fc)|de抽查|真页FUELCOST模板9处未接线(Trip distance/Consumption/Fuel price标签+2个单位select选项+fuel needed/per person 4 riders/round trip stat+动态one-way fuel cost);另发现此前R20排查目标fu-out属于另一模板tt-fuel(当前无页面消费,FUEL渲染器孤儿, fu.*9键备而不用)|curl实证+rg映射溯源|已修R22+线上复验(fc.*9键×9语言;部署前grep自检再次逮住脚本错位(option/span组含右括号,5处),同款修复正则已固化;教训强化=接线脚本分组一律不含闭括号;curl实证fc接线7处+garbage=0)
- BUG-013续13|url-encoder-decoder|ja|ue-pct动态stat标签(percent sequences)未接线(嵌套span假阳性掩盖)|IAB DOM探针|已修R26+线上复验(ue.pct×9语言;复验ja:%シーケンス等全日文,unwired空;同轮巡逻heart-rate×ko与RW×es全净)
- 范围外低优|unitconv|全部|公式行 factor 未格式化(×0.39370078740157477 长小数)与结果行英文单位词("0.39 inches")——前者渲染器打磨归UX轮,后者单位名=内容按设计不翻

## 已修
- BUG-013续2|word-counter|de|阅读时长值串 "sec"/"min" 英文后缀|IAB DOM探针|已修R9b(wc.sec/wc.min×2键×9语言,T()已入脚本;复验de:2.4 Min.)
- BUG-013续|全站渲染器(tools.py)|所有译文语言|反馈与校验提示家族未本地化:106处Copied!、8个纯Copy按钮链、21条校验/状态串(pw/rng/roman/gr/prime/epoch/bindec/temp)硬编码英文|rg清单+构建grep|已修R9(render()注入window.TT()辅助+21键×9语言经_i18n_tables.json重生成;298文件4741检查0失败+审计过;de文案人工撰写,线上复验待push恢复后补)
- BUG-005|全站chrome(用户报告)|英文态|截图=切English后仍见中文(头部搜索占位符/面包屑计算器);线上HTML验证干净英文,IAB复现zh→en切换正常→定性=用户端reload未完成或bfcache恢复旧zh DOM|用户截图|已修R3(i18n.js pageshow persisted时原地重apply+选择器同步;ttSetLang加reload兜底重试)
- BUG-006|倒计时族(days-until-*×7页,渲染器tools.py CD)|de/ja全部|动态结果文案零i18n接线:时钟行"h:m:s remaining today"、大数字标签"days to go"、标题钩子"100d to Christmas"、日期/千分位硬编码en-US|data/i18n_shots/(DOM探针证据:xmas页 de clock/title/lbl)|已修R4+线上复验通过(tools.py加T()辅助+LC=ttLang(),接cd.days/cd.daysyours/cd.today/cd.clock/cd.title×5键×9语言;复验de:clock=h:m:s heute verbleibend,title=Noch 100 Tage bis Christmas,lbl=Tage verbleibend,date=Fr., 25. Dez. 2026;ja日期2026年12月25日(金),overflowX=false;事件名Christmas英译键留下轮)
- BUG-007|全站SW缓存|所有语言|sw.js字节永不变→CACHE"tooltide-v1"永不重装→PRECACHE里的i18n.js被钉死在访客安装SW当天(旧键缺失/旧文案顽固不更新,用户端旧缓存根因之一)|线上sw.js+IAB复现(二次reload仍旧i18n.js)|已修R4+线上复验通过(CACHE烙构建时间戳tooltide-v1-YYYYMMDDHHMM,每次部署字节变化→浏览器重装SW→预缓存重取最新资产;复验:新SW controlled后de全链德语生效)
- BUG-008|倒计时族35事件页|de/ja全部|事件名不走i18n:cd-name与标题钩子恒英文(Christmas/Thanksgiving等)|IAB DOM探针|已修R5+线上复验通过(cd.ev.*35键×9语言(12月份+4季节+19节日);注意args无slug,改用事件名派生键cd.ev.+event小写连字符化;复验de:cd-name=Weihnachten,title=Noch 100 Tage bis Weihnachten)
- BUG-009|days-between-dates+business-days-calculator|de全部|DATEDIFF渲染器静态标签(Start date/End date/days/weeks&days/weekdays/total hours)+动态周数串"2 weeks + 0 days"+日期区间/千分位硬编码en-US|IAB DOM探针|已修R5+线上复验通过(dd.start/end/days/wkslbl/wdays/hours/wksfmt×7键×9语言+LC;复验de:Startdatum/Enddatum/Tage/2 Wochen + 0 Tage/note=Dienstag, 15. September 2026;修解析期竞态=window load重跑run())
- BUG-010|全站SW|所有语言|SWR实测不自愈:旧SW cache-first命中毒化预缓存,新SW install取数又经旧SW handler→i18n.js跨部署顽固陈旧(连续4次部署后tab仍无cd.ev键,缓存诊断fresh:false实证)|IAB caches诊断(唯一cache 69845字节旧版)|已修R5+线上复验通过(①install改new Request(u,{cache:'reload'})绕过HTTP缓存直取源站②fetch handler对i18n.js改network-first(离线回缓存)③注册加updateViaCache:'none'消除sw.js的10分钟HTTP缓存滞后;重置SW后de全链验证通过)
- BUG-011|换算族UNITCONV(约101页)|de全部|⇄Swap direction按钮、Formula:公式前缀×4分支硬编码英文;fmt()与换算表列 toLocaleString('en-US')千分位不随语言|IAB DOM探针 cm-to-inches|已修R6+线上复验通过(uc.swap/uc.formula×2键×9语言+T()/LC辅助;复验de:⇄Richtung wechseln,Formel: 1 × 0.39…;补window load重跑run()修解析期竞态)
- BUG-012|全站渲染器(tools.py 111处)|所有译文语言|数字格式系统性硬编码 toLocaleString/DateString('en-US'),千分位与区域习惯不随界面语言|rg清单+IAB DOM探针|已修R7+线上复验通过(正则清扫115处为 (typeof window!=='undefined'&&window.ttLang)?window.ttLang():'en-US' 带守卫表达式;复验de age页:13.241 days/317.784 德语千分位端到端生效)
- BUG-013|age-calculator+wordcounter|de全部|动态字符串后缀与静态标签:age的YMD拼串/"days in total"/错误提示与5个静态标签,wc的6个stat标签均未接线|IAB DOM探针|已修R8+线上复验通过(age.dob/at/lived_d/lived_h/nextbday/error/ymd/dtotal+wc.words/chars/cns/sentences/paras/rt共14键×9语言;复验de:36 Jahre, 3 Monate, 0 Tage/insgesamt 13.241 Tage/Geburtsdatum/Stichtag全对)
- BUG-004|全站 header|ru(桌面1280)|R1单行方案回归:logo被挤到内部折行(🌊与ToolTide两行,header高90px),nav末项"Все инст…"截断|data/i18n_shots/home-ru-top-7.png|已修R2+线上复验通过(logo nowrap+nav gap10/字号.9rem+行距8px+select收窄,navClip=0/headH68)
- BUG-001|全站 header|de/ja 等宽语言(桌面1280+)|语言选择器被宽 nav 挤到第二行折行|data/i18n_shots/home-de-top-2.png|已修+线上复验通过 2026-09-14 R1(>700px 时 nav 单行+可横向滑、header 容器放宽 1200px,style.css)
- BUG-002|首页|全部 9 译文语言|document.title 不随 tt_lang 切换,tab 始终英文标题|i18n_shots/home-de-top-2.png|已修+线上复验通过 2026-09-14 R1(首页 `<title data-i18n-title="meta.title">` + chrome.meta.title 键 ×9 语言 + i18n.js apply() 支持 title 节点;工具页 SEO 标题不动)
- BUG-003|卡片/工具页图标|与语言无关(Win10 Chromium 缺 U13/U14 字形)|emoji 豆腐块:🪞idealweight、🪙coinflip、🪚inchfrac、🛞tire|i18n_shots/home-zh-top-1.png|已修+线上复验通过 2026-09-14 R1(TOOL_EMOJI 换 ⚖️/💰/📏/🚗;🪐 为 U12 保留不动)

## 范围外(记录不修)
- BUG-013续5|bmi-calculator|ru全部|①bmi-cat动态分类值6变体英文硬编码;②逻辑缺陷:BMI≥35误标Class I - BMI 30-34.9(缺Class II/III分支,数值误导)|IAB URL参数实证(?h=170&w=110)|已修R12+线上复验(calc()补Class II(35-39.9)/III(40+)分支+TT()接bmi.v.uw/hw/ow/o1/o2/o3×6键×9语言+window load重跑修解析期竞态;复验ru:BMI38.1→Ожирение (II ст.) - ИМТ 35-39.9/健康档24.2→Здоровый вес,标签категория ВОЗ等全俄)
- 工具页正文(intro/howto/FAQ/卡片英文描述/页脚工具链接名)为英文 SEO 内容,按设计不翻译。

## 覆盖矩阵(页×语言 视觉验证记录)
- 2026-09-14 R1:首页 × zh/de/ja(1280px 桌面视口)——header/hero/搜索/分类芯片/#new/价值卡/页脚矩阵/版权行,除上表 3 项外干净。
- 下轮建议:首页 × ru/fr/id(西里尔长词+变音),再进倒计时族工具页 × de/ja(动态结果文案、document.title 钩子、placeholder)。
- 2026-09-15 R10:首页 × ko 全对(title/占位符韩语,零裸键)——**首页×9译文语言全覆盖达成**(zh/de/ja/ru/fr/id/es/pt/ko);巡逻抽查 tip-calculator fr 发现4个stat标签未接线,当轮即修(见BUG-013续3)。
- 2026-09-19 R18:TDEE×de 复验通过(R17修复后接线端到端渲染,garbage=false,unit=kcal/Tag zur Gewichtshaltung);loan×ko与xmas×ru巡逻全净(倒计时族回归无恙)。本轮零新BUG(计数1)。
- 2026-09-22 R23:about×id与privacy×ko站点页全净(garbage=false);基线审计276键×9过+check_site 23607检查0失败。本轮零新BUG(计数1,零BUG轮1)。
- 2026-09-24 R24:fuel-cost×de(R22 fc.*新接线渲染验证通过)/loan×ru/random-number×ko巡逻三页全净(garbage=false);审计276键×9过。本轮零新BUG(计数2)——**稳定巡逻模式正式生效**:每轮3页×3语言+审计,发现即修。
- 2026-09-24 R25(06:01档):tdee×de/fuel-cost×ja/json-formatter×ru巡逻三页全净(garbage=false;R17/R22家族成果线上站得住)。本轮零新BUG。
- 2026-09-24 R28(10:01档):heart-rate×pt/word-counter×fr/seconds×ko巡逻三页全净(garbage=false)。零新BUG。
