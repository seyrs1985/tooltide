# -*- coding: utf-8 -*-
"""R136 存量质量轮:内链体检 v2。修 v1 三缺陷:1)绝对内链接网未验 2)JS拼接href过滤只在STATUS记了没落地 3)sitemap覆盖名单过期。只读审计。"""
import io, os, re, glob
from urllib.parse import urlparse

DOCS = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\docs"
SITE = "https://tooldune.com/"

pages = glob.glob(os.path.join(DOCS, "**", "index.html"), recursive=True)

def is_js_concat(href):
    # R124 记录、v1 未落地的过滤:引号+加号拼接 = 客户端渲染链接(如最近使用条 x.u)
    return ("'+" in href) or ('"+' in href)

# 1) 相对链接(过滤 JS 拼接)
relative = {}
for path in pages:
    html = io.open(path, encoding="utf-8").read()
    for m in re.finditer(r'href="([^"#]+)"', html):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        if is_js_concat(href):
            continue
        relative[href] = relative.get(href, 0) + 1

missing_rel = []
for href in sorted(relative):
    rel = href.lstrip("/").split("?")[0].rstrip("/")
    if not rel:
        continue
    if not (os.path.exists(os.path.join(DOCS, rel, "index.html")) or os.path.exists(os.path.join(DOCS, rel))):
        missing_rel.append((href, relative[href]))

# 2) 绝对内链接网(v1 盲区):tooldune.com 链接逐条验 docs 目标
abs_internal = {}
inbound = {}  # slug -> 入站页数
for path in pages:
    html = io.open(path, encoding="utf-8").read()
    src_slug = os.path.basename(os.path.dirname(path))
    seen = set()
    for m in re.finditer(r'href="(https?://tooldune\.com/[^"#]*)"', html):
        href = m.group(1)
        abs_internal[href] = abs_internal.get(href, 0) + 1
        p = urlparse(href)
        slug = p.path.strip("/")
        if slug and slug not in seen:
            seen.add(slug)
            inbound[slug] = inbound.get(slug, 0) + 1

missing_abs = []
for href in sorted(abs_internal):
    slug = urlparse(href).path.strip("/").split("?")[0].rstrip("/")
    if not slug:
        continue
    if not (os.path.exists(os.path.join(DOCS, slug, "index.html")) or os.path.exists(os.path.join(DOCS, slug))):
        missing_abs.append((href, abs_internal[href]))

# 3) 非规范绝对引用(v1 保留)
bad_abs = []
abs_re = re.compile(r'(href|content)="https?://(?!tooldune\.com|www\.google\.com|trends\.google|www\.googletagmanager|www\.google-analytics|ssl\.google-analytics|www\.indexnow|api\.indexnow|seyrs1985\.github\.io/neonplay|seyrs1985\.github\.io/tooltide)([^"]{0,60})"')
for path in pages:
    html = io.open(path, encoding="utf-8").read()
    for m in abs_re.finditer(html):
        bad_abs.append((os.path.relpath(path, DOCS), m.group(0)[:80]))

# 4) sitemap 覆盖:R130-R135 九新页
sm = io.open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8").read()
new_pages = ["gym-membership-value-calculator", "dry-january-savings-calculator", "books-per-year-calculator",
             "electric-blanket-cost-calculator", "sourdough-starter-calculator"]
sm_miss = [p for p in new_pages if ("/" + p + "/") not in sm]

print("pages scanned:", len(pages))
print("relative links (js-filtered):", len(relative), "missing:", len(missing_rel))
for h, c in missing_rel[:10]:
    print("  MISS-REL", h, "x", c)
print("absolute internal links:", len(abs_internal), "missing:", len(missing_abs))
for h, c in missing_abs[:10]:
    print("  MISS-ABS", h, "x", c)
print("non-canonical absolute refs:", len(bad_abs))
for x in bad_abs[:5]:
    print("  ABS", x)
print("sitemap R130-R135:", sm_miss or "all 9 covered")
print("inbound pages for 9 newest:")
for p in new_pages:
    print("  %-42s %d" % (p, inbound.get(p, 0)))
