# ToolTide — AI 全链路增长流水线

免费在线工具站(https://seyrs1985.github.io/tooltide/),由 AI 自动化完成:关键词热点分析 → 程序化建站 → 部署 → 数据分析优化 → 广告/订阅变现。方案详见 [docs/strategy.md](docs/strategy.md)。

## 目录结构

```
ai-growth-engine/
├── engine/
│   ├── pages.py          # 页面库:每个长尾词一页(加新页就在这里)
│   ├── tools.py          # 14 种交互工具渲染器(纯 vanilla JS)
│   ├── build.py          # 构建器 → site/(SEO/sitemap/JSON-LD/隐私页)
│   ├── check_site.js     # 构建后 JS/JSON-LD 语法自检
│   ├── analyze.py        # GSC 数据 → 优化动作清单
│   ├── revenue.py        # 收入台账 + $1 目标看板
│   ├── ping_indexnow.py  # 部署后向 Bing/Yandex 即时提交
│   └── deploy.sh         # 一键:构建→git→建repo→Pages→推送→等上线→IndexNow
├── config/
│   ├── site.json         # 站点配置:URL/GA4/AdSense/联盟/Ko-fi(填了即生效)
│   └── goals.json        # 收入目标:$1 → $50/月
├── data/                 # trends快照 / metrics.csv / insights.json / revenue.csv
├── site/                 # 构建产物(GitHub Pages 从这里发布)
├── docs/strategy.md      # 全链路研究报告与单位经济
└── STATUS.md             # 运营状态(每日自动化追加)
```

## 快速开始(一次性,约 5 分钟)

**1. 提供 GitHub 凭证(唯一缺失的一环):**

打开 https://github.com/settings/tokens/new → 勾选 `repo` → Generate → 复制 token,然后任选其一:

```bash
# 方式A:存入全局 git 配置(永久,推荐)
git config --global tooltide.token ghp_你的token

# 方式B:临时环境变量
GITHUB_TOKEN=ghp_你的token bash engine/deploy.sh
```

**2. 部署上线:**

```bash
bash engine/deploy.sh
```

脚本全自动:构建 → 创建 repo(tooltide)→ 启用 Pages → 推送 → 等待 https://seyrs1985.github.io/tooltide/ 返回 200 → IndexNow 提交收录。以后再跑就是纯增量部署。

**3. 变现接口(拿到账号后填 config/site.json 重建即可):**

| 字段 | 去哪拿 | 效果 |
|---|---|---|
| `adsense_client` | adsense.google.com 申请(需站点已上线) | 广告位自动出现 |
| `ga4_id` | analytics.google.com | 流量统计 |
| `gsc_verification` | search.google.com/search-console | 收录数据(GSC 是 analyze.py 的数据源) |
| `kofi_url` / `affiliate.url` | ko-fi.com / 联盟平台 | 页脚赞助位/推荐位 |

## 日常命令

```bash
python engine/build.py          # 只重建站点
bash engine/deploy.sh           # 构建+部署(日常发布用这个)
python engine/analyze.py        # GSC数据→优化建议(无数据时跑demo)
python engine/revenue.py        # 收入看板
python engine/revenue.py --add adsense 0.37   # 记一笔收入
node engine/check_site.js       # 构建产物自检
```

## 加新工具页(或让自动化加)

在 `engine/pages.py` 的 `PAGES()` 里追加一个条目即可——倒计时用 `_cd(...)`、换算器用 `_conv(...)` 工厂函数一行搞定;复杂工具在 `tools.py` 加渲染器。然后 `bash engine/deploy.sh`。
