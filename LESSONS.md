# 踩坑与经验（每轮开工前先读）

1. **deploy 凭证**：token 在 `git config tooltide.token`；deploy.sh 已内置原子锁+push前rebase+超时跳过，多流水线并发安全。
2. **IndexNow 403**：密钥必须在域名根（seyrs1985.github.io 用户站仓库承载），子目录无效。
3. **GCM 挂起**：无凭证时 credential manager 会弹 GUI 卡死——deploy.sh 已用 GIT_TERMINAL_PROMPT=0 + token 内联绕开，勿改回。
4. **og-image**：以 build.py 生成版为准（docs/og-image.png）；make_og_image.py 是未接线的历史遗留。
5. **check_site.js 0 failures 是部署红线**；GA4/GSC/adsense 注入字段(ga4_id/gsc_verification/adsense_client)不得破坏。
6. **并发**：与体验 Agent 共仓——开工前 git pull --rebase；部署锁会串行化 push；STATUS.md 里【UX任务】标记的条目优先处理。
7. **体验 Agent 与本流水线分工**：本流水线=扩页(pages.py)+数据+收入；体验=style.css/build.py 模板。勿越界。

8. **差异化红线（每个新页面/新功能必须回答）**：
   - "比 Google 搜索前 3 名多做了什么？"——写不出一句具体答案就不做。
   - 禁止生产纯模板换皮页（同渲染器+同结构仅换关键词不算差异化，除非内容深度明显超越竞品）。
   - 新工具有满足一条：解决 Reddit/Quora 上有人抱怨"找不到好XX工具"的问题 / 比现有头部工具快或简单 10 倍 / 填补站内品类空白且 GSC 显示有搜索量。
   - 扩页 Agent 每轮选题必须附带"为什么这个页面比竞品好"的一句话理由，写进 STATUS.md 日志。
9. **长线留存红线（整洁是前提，每个新页面必须自带至少 2 项）**：
   - 基线五选：A2HS 一次性提示（倒计时页把剩余天数烘进桌面图标=缩略文字）、document.title 实时状态、Web Share 分享（降级剪贴板）、localStorage 记忆复用（tt_ 前缀）、每日内容/自定义倒计时/.ics 日历导出。
   - 留存 UI 文案走 i18n 10 语言（engine/_i18n_tables.json + engine/_gen_i18n.py 重建），i18n_audit.py 必须过；禁止硬编码英文。
   - 留存组件禁止弹窗拦截/伤 LCP，每页新增内联 JS ≤2KB；站点级公共改动（manifest.shortcuts、A2HS 公共模块、SW 离线）最小侵入 build.py 并在 STATUS.md 声明【留存-站点级】，不破坏 GA4/GSC/adsense 注入。
