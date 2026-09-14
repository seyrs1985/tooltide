# ToolTide i18n BUG 台账

格式:`编号|页面|语言|现象|截图|状态`。状态=待修/已修/范围外。每轮先视觉验证、记录,再修复,部署后线上复验回写。

## 待修

(无)

## 已修
- BUG-001|全站 header|de/ja 等宽语言(桌面1280+)|语言选择器被宽 nav 挤到第二行折行|data/i18n_shots/home-de-top-2.png|已修 2026-09-14 R1(>700px 时 nav 单行+可横向滑、header 容器放宽 1200px,style.css)
- BUG-002|首页|全部 9 译文语言|document.title 不随 tt_lang 切换,tab 始终英文标题|i18n_shots/home-de-top-2.png|已修 2026-09-14 R1(首页 `<title data-i18n-title="meta.title">` + chrome.meta.title 键 ×9 语言 + i18n.js apply() 支持 title 节点;工具页 SEO 标题不动)
- BUG-003|卡片/工具页图标|与语言无关(Win10 Chromium 缺 U13/U14 字形)|emoji 豆腐块:🪞idealweight、🪙coinflip、🪚inchfrac、🛞tire|i18n_shots/home-zh-top-1.png|已修 2026-09-14 R1(TOOL_EMOJI 换 ⚖️/💰/📏/🚗;🪐 为 U12 保留不动)

## 范围外(记录不修)
- 工具页正文(intro/howto/FAQ/卡片英文描述/页脚工具链接名)为英文 SEO 内容,按设计不翻译。

## 覆盖矩阵(页×语言 视觉验证记录)
- 2026-09-14 R1:首页 × zh/de/ja(1280px 桌面视口)——header/hero/搜索/分类芯片/#new/价值卡/页脚矩阵/版权行,除上表 3 项外干净。
- 下轮建议:首页 × ru/fr/id(西里尔长词+变音),再进倒计时族工具页 × de/ja(动态结果文案、document.title 钩子、placeholder)。
