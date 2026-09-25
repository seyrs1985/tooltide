# ToolTide 增长流水线 PLAYBOOK(活方法论,由流水线自我进化)

> 本文件是 40 分钟增长流水线的**可进化层**。宪法(不可削弱红线)在任务 prompt 与 LESSONS.md #5/#8/#9,此处不复述、不冲突。
> 你(流水线本人)有权且有义务按 §9 修订本文件。纪律:每次只改 1-3 条;独立 commit(`playbook: 一句话`);全文 ≤250 行;每条经验一行、尽量带来源轮次;过期内容移 §6 或删除,不许只增不减。

## 0. 目标与现状(每 5 轮刷新数字)
- 终点:稳定 $10,000/月,阶梯 $1/$50/$500/$2000/$10000(config/goals.json);当前=收录爬坡期,收入 $0.00、AdSense 待用户申请,收入数字不作为策略变动依据。
- 运行窗口(2026-09-26 起):仅 23:00-08:00(用户计划免费时段,调度器只在窗口内触发);白天不触发属预期,白天发现"停摆"勿做任何补救动作,等当晚窗口自然恢复。
- 线上 https://tooldune.com/ (2026-09-26 起自定义域名,品牌同步更名 ToolDune;更早的 github.io 与 nuts.fan 均 301;deploy.sh live-check 已跟随)。
- 基线(2026-09-26 R110 后,[PBAudit]):318 工具页;check_site 329 文件 25175 检查 0 失败;i18n 审计 323 页 289 键×9 语言。**规模口径以当轮 check_site 输出为准**(build 输出的页数与 STATUS 口径不同)。

## 1. 选题策略
- 来源:Google Trends RSS(https://trends.google.com/trending/rss?geo=US 与 ?geo=GB,存 data/trends/日期-时段.json 不覆盖)+ 站内品类空白;GSC 真实数据到位后以 data/insights.json P1/P2 为最高优先。
- 节奏:每轮 2-3 页,簇化推进(同主题邻居互链成族);低频期 1-2 页扎实优先于数量;没有好选题宁缺毋滥,转存量深化(扩 FAQ/内链/留存钩子补课)。
- 饱和黑名单(勿加密):倒计时族 40+ 页;通用换算矩阵已双向覆盖;动手前先 grep pages.py 确认簇边界。
- 差异化套路(R96-R103 验证有效):反推销诚实口径+给算式给诊断表不卖货;竞品画像写进 STATUS 一句话。
- 撞名协议:查重必须同时匹配字典形态(`'slug': 'x'`)与工厂调用形态(`_cd(`/`_conv(`),单一正则会全漏检(R96 引号写错漏检教训);发现同名→换角度,不硬塞。

## 2. 扩页套路(每页)
- pages.py 新条目必须在 `def PAGES()` 函数体内(4 空格缩进,列 0 会 IndentationError);新页 **append 到列表尾部**(首页 #new 模块依赖 append 序=上架序,勿插中间)。
- 标准流程:Write 注入脚本 engine/_inject_roundN.py(渲染器块)+_spliceN.py(ast.parse 校验后锚点 replace,repr 生成 dict 防手写括号错;页尾锚点 `# Index metadata used by build`)→build→check_site→i18n_audit。
- 新渲染器必须同步 build.py `TOOL_EMOJI` 映射(check_site 逐页硬闸门,漏了直接拦部署);emoji 选老码位防 Win10 豆腐块。
- 每页标配 4 钩子:document.title 结果钩子 / tt_ 前缀输入记忆 / URL 参数携带状态 / WebShare 分享(降级剪贴板);倒计时页另见 LESSONS #9。
- 一器多页用 `__VAR__` 参数注入(范例 petage 渲染器 __SPECIES__),SEO 分页、逻辑单源。
- 倒计时族已饱和但「date 输入规划器」是新回访钩子形态(R104 movetl 验证):date 输入+天数 title+localStorage,用户每周自动回访,适用搬家/考试/截稿等一切有截止日的事。
- 拼接前自查三件套(分享文案变量/三元括号配平/未定义标识符)——R106(2处)+R107(1处)拼接前拦截;check_site 只拦语法,拦不住未定义变量这类运行时错。
- 渲染器 JS 写完**必跑 check_site**(R93 LOREM `\n` 转义、R99 jetlag 三元优先级、R100 meattime 闭包变量三次实证);build 后 grep 抽查新页文案防草稿残留混入。
- i18n 管线:_i18n_tables.json 补键(9 译文语言 zh/es/pt/ru/ja/ko/de/fr/id 全有;en 基准靠代码 fallback,以 i18n_audit.py 通过为准)→`python engine/_gen_i18n.py`→i18n_audit.py;**i18n.js 是生成物绝不手编**;脚本批量接线后必须 curl 直连抽查渲染结果(i18n R17 教训:属性错位成合法但可见的垃圾串,check_site 与审计都拦不住)。

## 3. 构建、部署与排障
- 全内联 CSS 架构:线上**没有** /assets/style.css(验证 CSS 改动抓页面内联 `<style>`);i18n.js 在站点根 /i18n.js。
- deploy.sh 每次运行会重写 .gitignore——自定义忽略项必须写进 deploy.sh 的 heredoc。
- push 被拒等 30s 重试一次;仍败留本地 commit 下轮捎上(该模式连续多轮零丢失);401/403 记"待凭证"。
- 裸 git 操作需代理 env(HTTP(S)_PROXY=http://127.0.0.1:7890);GitHub 封锁窗判定:站点 200+git 败=等 60s 重试,fetch 128=实锤封锁。
- 部署后复验:curl https://tooldune.com/ 与本轮新页均 200;SW CACHE 名带构建戳,每次部署访客资产自动刷新。

## 4. 数据与收入
- analyze.py:data/metrics.csv 非 DEMO 才有真动作,DEMO 模式跳过;revenue.py 每轮跑,摘要进 STATUS。
- 收入 $0 为当前常态;GSC 出数后,选题优先级=insights.json P1/P2 > Trends。

## 5. 状态与台账格式
- STATUS.md=唯一运营账本,每轮一行,格式:
  `- 日期-时段 · 自动化第N轮【簇名】· 新页列表(一句差异化)· 质量:文件数/检查数/i18n键数 · 部署与线上复验结果 · 收入 · 自评:选题A/B、返工n、闸门拦截n · [PB±n]`
- `[PB+n]`=本轮有 playbook 进化;`[PB-1]`=回滚了某次进化;`[PB+0]`=无进化;`[PBAudit]`=本轮做了方法论审计(每 5 轮强制一次,见 §9)。

## 6. 已证伪/废弃(防重复踩坑;格式:日期+结论+证据)
- (暂空。首次证伪时写入;从 §1/§2 移出的过时规则也放这里,注证据轮次。)

## 7. 待挖掘候选(做完划掉;审计轮负责补充与清理)
- GSC 真实数据接入后的 Search Console 长尾词扩页(等 metrics.csv 出真数)
- 留存 R1 遗留:换算页"最近使用"复用条、manifest.shortcuts 热门深链、倒计时 .ics 导出
- 每日内容钩子("每天答案不同"的日期种子页,按品类逐簇铺)
- 渲染器动态字符串 i18n 长尾(与 i18n 流水线协同,勿改其台账 engine/i18n_bugs.md)

## 8. 边界提醒
- UX/视觉/布局优化归体验线,本流水线不做 style.css 皮肤级改动(结构闸门要求的必要修改除外,STATUS 声明)。
- 游戏/NeonPlay、i18n 巡逻(engine/i18n_bugs.md 台账)归各自流水线;仓库内 `_tmp_*`/`_inject_round*` 脚本是历史工作现场,可复用命名格式但勿当长期资产依赖。

## 9. 自我改进协议(本文件存在的意义)
每轮收尾前 3 分钟复盘三问:
1. 本轮哪里返工/卡壳/被闸门拦?→ 提炼成一条一行规则,写进对应小节,带轮次号。
2. 本轮哪条既有规则被证明多余或错误?→ 移入 §6 注证据,或直接删除。
3. 下次重做同类工作的最小改动路径?→ 更新 §1/§2/§3 套路。
进化纪律:
- 每次进化只改 1-3 条;独立 commit(`playbook: <一句话>`),与页面 commit 分开——git log 即进化史。
- **禁止**:削弱/复制宪法条款(锁/边界/闸门/部署纪律/输出纪律,LESSONS #5 #8 #9);删除或改写本 §9 的三问与纪律;调用任何 cron 管理工具;单次让全文超 250 行。
- 效果回看:凡 `[PB+n]` 的下一轮,开工时先核对上次进化的实效;连续 2 轮负向(该进化直接引起返工/拦截)→ `git revert` 该进化 commit,STATUS 记 `[PB-1]` 与原因。拿不准的进化标 `[PBTrial]`,观察 3 轮再定去留。
- 周期审计(每 5 轮强制,STATUS 记 `[PBAudit]`):通读全文+近 5 轮 STATUS——删过时基线、清 §7 已完成项、合并重复条目、把重复≥2 次的 STATUS 教训升级为正式规则、刷新 §0 数字;审计本身发现的问题按三问流程落地。
