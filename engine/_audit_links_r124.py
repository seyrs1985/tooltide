# -*- coding: utf-8 -*-
"""R124 存量深化:全站内链体检 + 今日新页 sitemap 覆盖检查。只读审计,不改文件。"""
import io, os, re, glob

DOCS = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\docs"

# 1) 收集全部内部链接
href_re = re.compile(r'href="([^"#]+)"')
internal = {}
for path in glob.glob(os.path.join(DOCS, "**", "index.html"), recursive=True):
    with io.open(path, encoding="utf-8") as f:
        html = f.read()
    for m in href_re.finditer(html):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        if href not in internal:
            internal[href] = 0
        internal[href] += 1

# 2) 验证每个内部链接目标存在(docs/ 下文件或目录/index.html)
missing = []
for href, count in sorted(internal.items()):
    rel = href.lstrip("/").split("?")[0].rstrip("/")
    if not rel:
        continue
    as_dir = os.path.join(DOCS, rel, "index.html")
    as_file = os.path.join(DOCS, rel)
    if os.path.exists(as_dir) or os.path.exists(as_file):
        continue
    missing.append((href, count))

# 3) 非规范绝对地址(应为 tooldune.com 或相对路径)
bad_abs = []
abs_re = re.compile(r'(href|content)="https?://(?!tooldune\.com|www\.google\.com|trends\.google|www\.googletagmanager|www\.google-analytics|ssl\.google-analytics|www\.indexnow|api\.indexnow|seyrs1985\.github\.io/neonplay|seyrs1985\.github\.io/tooltide)([^"]{0,60})"')
for path in glob.glob(os.path.join(DOCS, "**", "index.html"), recursive=True):
    with io.open(path, encoding="utf-8") as f:
        html = f.read()
    for m in abs_re.finditer(html):
        bad_abs.append((os.path.relpath(path, DOCS), m.group(0)[:80]))

# 4) sitemap 覆盖:今日 10 新页
sm = io.open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8").read()
new_pages = ["moon-phase-calculator", "full-moon-calendar", "birthday-moon",
             "firewood-calculator", "fire-pit-vs-patio-heater", "firewood-seasoning",
             "pumpkin-pie-calculator", "pumpkin-carving-timing", "pumpkin-seeds-roast-calculator",
             "dst-sleep-shift-planner"]
sm_miss = [p for p in new_pages if ("/" + p + "/") not in sm]

print("internal links total:", len(internal))
print("missing targets:", len(missing))
for h, c in missing[:20]:
    print("  MISS", h, "x", c)
print("non-canonical absolute refs:", len(bad_abs))
for x in bad_abs[:10]:
    print("  ABS", x)
print("new pages missing from sitemap:", sm_miss or "none - all 10 covered")
