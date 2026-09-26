# -*- coding: utf-8 -*-
"""R127 存量质量轮审计器:
1) 留存钩子普查:每页页面级钩子(document.title / tt_ 记忆 / 分享 / date规划器 / URL参数)
2) sitemap 覆盖核对
3) 外链健康抽查(去重后采样,curl 经代理)
"""
import io, os, re, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, os.pardir, "docs")
SITE = "https://tooldune.com/"
OWN = ("tooldune.com", "nuts.fan", "seyrs1985.github.io", "www.w3.org",
       "googletagmanager.com", "google-analytics.com")
CHROME = ("about", "contact", "games", "privacy", "privacy-policy", "terms", "disclaimer", "404")

pages = []
for d in sorted(os.listdir(DOCS)):
    p = os.path.join(DOCS, d, "index.html")
    if os.path.isfile(p) and not d.startswith(("_", ".")) and d not in CHROME:
        pages.append((d, p, io.open(p, encoding="utf-8", errors="ignore").read()))

no_hook, no_title, no_share = [], [], []
for d, p, h in pages:
    h = re.sub(r'<script>\(function\(\)\{\nvar T0=document\.title;.*?</script>', '', h, flags=re.S)  # 剥离站级兜底,只数页面级
    title_js = bool(re.search(r"document\.title\s*=", h))
    tt = bool(re.search(r"localStorage\.(?:set|get)Item\('tt_", h))
    share = bool(re.search(r"navigator\.(?:share|clipboard)", h))
    planner = 'type="date"' in h
    urlp = "URLSearchParams" in h
    page_hooks = sum([title_js, tt, share, planner])
    rn = 'class="result-num"' in h
    page_hooks = sum([title_js, tt, share, planner])
    if page_hooks + (1 if urlp else 0) < 1:  # A2HS 站级恒在,页面级至少 1 项
        no_hook.append(d + ("*兜底覆盖" if rn else ""))
    if not title_js:
        no_title.append(d)
    if not share:
        no_share.append(d)

sm = io.open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8", errors="ignore").read()
missing_sm = [d for d, p, h in pages if d not in CHROME and ("%s%s/" % (SITE, d)) not in sm]

ext = {}
for d, p, h in pages:
    for m in re.findall(r'https?://[^"\'<> )]+', h):
        host = m.split("/")[2] if "://" in m else ""
        if any(o in m for o in OWN) or "example" in m:
            continue
        ext.setdefault(m, d)
sample = sorted(ext) if len(ext) <= 40 else sorted(ext)[:40]
bad, blocked = [], []
for u in sample:
    try:
        r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-m", "8",
                            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                            "-w", "%{http_code}", u], capture_output=True, text=True, timeout=14)
        code = r.stdout.strip()[:3]
    except Exception:
        code = "000"
    if code in ("403", "429"):
        blocked.append((u, code))
    elif code != "200":
        bad.append((u, code))

print("pages=%d" % len(pages))
uncov = [x for x in no_hook if not x.endswith("*兜底覆盖")]
print("retention: no_page_hook=%d (uncovered=%d, site-fallback covered=%d) no_title=%d no_share=%d" %
      (len(no_hook), len(uncov), len(no_hook) - len(uncov), len(no_title), len(no_share)))
if uncov: print("  UNCOVERED:", ", ".join(uncov[:25]))
if no_title: print("  NOTITLE:", ", ".join(no_title[:20]))
print("sitemap: missing=%d %s" % (len(missing_sm), ", ".join(missing_sm[:10])))
print("external: unique=%d sampled=%d ok=%d blocked(403/429)=%d broken=%d" %
      (len(ext), len(sample), len(sample) - len(bad) - len(blocked), len(blocked), len(bad)))
for u, c in bad[:15]:
    print("  BROKEN %s %s (first seen: %s)" % (c, u, ext[u]))
