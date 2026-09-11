# 踩坑与经验（每轮开工前先读）

1. **deploy 凭证**：token 在 `git config tooltide.token`；deploy.sh 已内置原子锁+push前rebase+超时跳过，多流水线并发安全。
2. **IndexNow 403**：密钥必须在域名根（seyrs1985.github.io 用户站仓库承载），子目录无效。
3. **GCM 挂起**：无凭证时 credential manager 会弹 GUI 卡死——deploy.sh 已用 GIT_TERMINAL_PROMPT=0 + token 内联绕开，勿改回。
4. **og-image**：以 build.py 生成版为准（docs/og-image.png）；make_og_image.py 是未接线的历史遗留。
5. **check_site.js 0 failures 是部署红线**；GA4/GSC/adsense 注入字段(ga4_id/gsc_verification/adsense_client)不得破坏。
6. **并发**：与体验 Agent 共仓——开工前 git pull --rebase；部署锁会串行化 push；STATUS.md 里【UX任务】标记的条目优先处理。
7. **体验 Agent 与本流水线分工**：本流水线=扩页(pages.py)+数据+收入；体验=style.css/build.py 模板。勿越界。
