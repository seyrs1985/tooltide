# -*- coding: utf-8 -*-
"""ToolTide static site builder.

Usage:  python engine/build.py
Reads config/site.json + engine/pages.py, writes the full static site to site/.
Only the Python standard library is used.
"""

import datetime
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pages as pages_mod  # noqa: E402
import tools as tools_mod  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT, "docs")  # GitHub Pages branch-source allows only / or /docs

TODAY = datetime.date.today()
YEAR = TODAY.year

TOOL_EMOJI = {
    "countdown": "⏳", "datediff": "📅", "age": "🎂", "percent": "📊",
    "tip": "💵", "discount": "🏷️", "readingtime": "📖", "wordcounter": "🔤",
    "case": "🔠", "aspect": "🖥️", "unitconv": "🔄", "typing": "⌨️",
    "names": "🎲", "password": "🔐",
 "randomnum": "🎲", "roman": "🏛️", "wordspages": "📄", "grade": "🎓", "dedupe": "🧹", "slug": "🔗", "salestax": "🧾", "average": "🧮", "percent": "📊",
}


def load_config():
    with open(os.path.join(ROOT, "config", "site.json"), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s), quote=True)


def ad_slot(cfg, slot_id, where):
    """AdSense slot markup — invisible (nothing) until adsense_client is configured."""
    client = (cfg.get("adsense_client") or "").strip()
    if not client:
        return ""
    return (
        f'<div class="ad ad-{where}">'
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{esc(client)}" '
        f'data-ad-slot="{esc(slot_id)}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
        f"<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>"
    )


OG_IMAGE = "og-image.png"
og_image_ready = False


def ensure_og_image():
    """Generate docs/og-image.png (1200x630 share card) once; reused on rebuilds."""
    global og_image_ready
    out = os.path.join(SITE_DIR, OG_IMAGE)
    if os.path.exists(out):
        og_image_ready = True
        return
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    bold_candidates = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf",
                       "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    reg_candidates = [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    bold = next((f for f in bold_candidates if os.path.exists(f)), None)
    reg = next((f for f in reg_candidates if os.path.exists(f)), None)
    if not (bold and reg):
        return
    W, H = 1200, 630
    top, bot = (10, 58, 94), (14, 116, 144)  # deep ocean → tooltide teal
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)],
               fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    import math
    for amp, base_y, alpha, phase in [(26, 492, 42, 0.0), (20, 534, 26, 2.1)]:
        pts = [(x, base_y + amp * math.sin(x / 140.0 + phase)) for x in range(0, W + 1, 6)]
        ov.polygon(pts + [(W, H), (0, H)], fill=(255, 255, 255, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((80, 185), "ToolTide", font=ImageFont.truetype(bold, 128), fill=(255, 255, 255))
    d.text((84, 375), "Free online tools — fast, private, no sign-up",
           font=ImageFont.truetype(reg, 44), fill=(165, 243, 252))
    os.makedirs(SITE_DIR, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    og_image_ready = True
    print(f"  asset /{OG_IMAGE} (generated)")


def head_tags(cfg, title, desc, canonical, extra_ld=(), root=False):
    ga = (cfg.get("ga4_id") or "").strip()
    gsc = (cfg.get("gsc_verification") or "").strip()
    ads = (cfg.get("adsense_client") or "").strip()
    ld = json.dumps({"@context": "https://schema.org", "@graph": list(extra_ld)},
                    ensure_ascii=False, separators=(",", ":"))
    fav = ("data:image/svg+xml," +
           esc('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">🌊</text></svg>'))
    css = "style.css" if root else "../style.css"
    og_abs = cfg["base_url"] + OG_IMAGE
    og_img = f'<meta property="og:image" content="{esc(og_abs)}">\n' \
             f'<meta property="og:image:width" content="1200">\n' \
             f'<meta property="og:image:height" content="630">\n' \
             f'<meta property="og:image:alt" content="ToolTide — free online tools">\n' \
             f'<meta name="twitter:card" content="summary_large_image">\n' \
             f'<meta name="twitter:title" content="{esc(title)}">\n' \
             f'<meta name="twitter:description" content="{esc(desc)}">\n' \
             f'<meta name="twitter:image" content="{esc(og_abs)}">\n' \
        if og_image_ready else ""
    h = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:site_name" content="ToolTide">
<meta property="og:locale" content="en_US">
{og_img}<meta name="theme-color" content="#0e7490">
<link rel="icon" href="{fav}">
{f'<meta name="google-site-verification" content="{esc(gsc)}">' if gsc else ''}
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="{css}">
{f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(ads)}" crossorigin="anonymous"></script>' if ads else ''}
{f'<script async src="https://www.googletagmanager.com/gtag/js?id={esc(ga)}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{esc(ga)}");</script>' if ga else ''}
</head>
<body><a class="skip" href="#main">Skip to content</a>"""
    return h


def header_nav(cfg, base):
    links = "".join(
        f'<a href="{base}#{c}">{esc(n)}</a>'
        for c, n in [("calculator", "Calculators"), ("converter", "Converters"),
                     ("countdown", "Countdowns"), ("text", "Text"), ("generator", "Generators")]
    )
    games_url = (cfg.get("sister_site") or {}).get("url", "https://seyrs1985.github.io/neonplay/")
    return f"""<header class="site-head">
  <div class="wrap nav-row">
    <a class="logo" href="{base}">🌊 ToolTide</a>
    <nav aria-label="Primary"><a href="{esc(games_url)}" title="Our sister site: free online games">🎮 Games</a>{links}<a href="{base}#all" class="nav-all">All tools</a></nav>
  </div>
</header>"""


# footer tool matrix + hero chips — category keys must match the homepage section ids in pages.py
CAT_EMOJI = {"countdown": "⏳", "calculator": "🧮", "converter": "🔄",
             "text": "🔤", "generator": "🎲"}


def foot_label(p):
    """Short footer label: 'How Many Days Until Christmas?' -> 'Christmas'."""
    h = p["h1"]
    if h.startswith("How Many Days Until "):
        return h[len("How Many Days Until "):].rstrip("?")
    if h.endswith(" Converter"):
        return h[:-len(" Converter")]
    return h


def spread(pages, n):
    """n evenly spaced picks — keeps reverse-direction converter pairs from crowding out variety."""
    if len(pages) <= n:
        return list(pages)
    step = len(pages) / n
    return [pages[int(i * step)] for i in range(n)]


def footer(cfg, base, all_pages=(), cat_info=None):
    kofi = (cfg.get("kofi_url") or "").strip()
    affiliate = cfg.get("affiliate") or {}
    year = YEAR
    games_url = (cfg.get("sister_site") or {}).get("url", "https://seyrs1985.github.io/neonplay/")
    site_links = f"""<a href="{base}about/">About</a>
      <a href="{base}privacy/">Privacy</a>
      <a href="{base}contact/">Contact</a>
      <a href="{esc(games_url)}" title="Our sister site: free online games">🎮 Games on NeonPlay</a>"""
    if kofi:
        site_links += f'\n      <a href="{esc(kofi)}" rel="noopener" target="_blank">☕ Support us</a>'
    cols = ""
    for cat, (label, _blurb) in (cat_info or {}).items():
        cat_pages = spread([x for x in all_pages if x["category"] == cat], 4)
        items = "".join(f'<a href="{base}{x["slug"]}/">{esc(foot_label(x))}</a>' for x in cat_pages)
        cols += (f'<nav class="foot-col" aria-label="{esc(label)}">'
                 f'<h3><a href="{base}#{cat}">{CAT_EMOJI.get(cat, "")} {esc(label)}</a></h3>'
                 f'{items}</nav>')
    aff = ""
    if affiliate.get("url"):
        aff = f'<p class="aff-note">{esc(affiliate.get("disclosure", ""))} <a href="{esc(affiliate["url"])}" rel="sponsored noopener" target="_blank">{esc(affiliate.get("text", ""))}</a></p>'
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-brand">
      <a class="logo" href="{base}">🌊 ToolTide</a>
      <p>Free online tools that run in your browser. No sign-up, no installs, no tracking of your inputs.</p>
      <nav class="foot-site" aria-label="Site">{site_links}</nav>
    </div>
    <div class="foot-matrix">{cols}</div>
    <div class="foot-legal">
      {aff}
      <p>© {year} ToolTide · Free online tools that run in your browser. No sign-up, no tracking of your inputs.</p>
    </div>
  </div>
</footer>"""


def crumb(base, items):
    inner = "  ›  ".join(f'<a href="{esc(u)}">{esc(t)}</a>' if u else f"<span>{esc(t)}</span>"
                         for t, u in items)
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb">{inner}</nav>'


def tool_card(p, base):
    emoji = (p.get("args") or {}).get("emoji") or TOOL_EMOJI.get(p["tool"], "🔧")
    return (f'<a class="card" href="{base}{p["slug"]}/">'
            f'<span class="card-emoji">{emoji}</span>'
            f'<span class="card-title">{esc(p["h1"])}</span>'
            f'<span class="card-desc">{esc(p["desc"][:110])}…</span></a>')


def build_page(cfg, p, all_pages, cat_info):
    base = cfg["base_url"]
    canonical = base + p["slug"] + "/"
    emoji = TOOL_EMOJI.get(p["tool"], "🔧")

    webapp_ld = {
        "@type": "WebApplication", "name": p["h1"], "url": canonical,
        "applicationCategory": "UtilityApplication", "operatingSystem": "Any",
        "browserRequirements": "Requires JavaScript",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": p["desc"],
    }
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in p["faqs"]]}
    crumb_ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ToolTide", "item": base},
        {"@type": "ListItem", "position": 2, "name": p["h1"], "item": canonical}]}

    related = [x for x in all_pages if x["category"] == p["category"] and x["slug"] != p["slug"]]
    related += [x for x in all_pages if x["category"] != p["category"]]
    related_html = "".join(tool_card(x, base) for x in related[:6])

    tool_html = tools_mod.render(p["tool"], p.get("args", {}))

    facts = p.get("facts") or ""
    tip = p.get("tip") or ""
    info_box = f'<div class="info-box"><strong>Good to know</strong> — {esc(facts)}</div>' if facts else ""
    tip_box = f'<div class="info-box tip"><strong>Quick reference</strong> — {esc(tip)}</div>' if tip else ""

    intro_html = "".join(f"<p>{esc(par)}</p>" for par in p["intro"])
    howto_html = "".join(f"<li>{esc(s)}</li>" for s in p["howto"])
    faq_html = "".join(
        f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for q, a in p["faqs"])

    doc = head_tags(cfg, p["title"], p["desc"], canonical, [webapp_ld, faq_ld, crumb_ld], root=False)
    doc += header_nav(cfg, base)
    doc += crumb(base, [("🌊 ToolTide", base), (p["h1"], None)])
    doc += f"""<main class="wrap" id="main">
<article>
  <div class="page-emoji">{emoji}</div>
  <h1>{esc(p['h1'])}</h1>
  {ad_slot(cfg, cfg.get('ad_slot_top', '1111111111'), 'top')}
  <section class="intro">{intro_html}</section>
  {tool_html}
  <section class="seo-block"><h2>How to use</h2><ol class="howto">{howto_html}</ol></section>
  {info_box}{tip_box}
  {ad_slot(cfg, cfg.get('ad_slot_mid', '2222222222'), 'mid')}
  <section class="seo-block"><h2>Frequently asked questions</h2>{faq_html}</section>
  <section class="seo-block"><h2>Related tools</h2><div class="grid">{related_html}</div></section>
</article>
</main>"""
    doc += footer(cfg, base, all_pages, cat_info)
    doc += "</body></html>"
    return doc


def build_index(cfg, all_pages, cat_info):
    base = cfg["base_url"]
    canonical = base
    desc = "ToolTide — free online tools: countdown timers, calculators, unit converters, word counter, password generator and more. Fast, private, no sign-up."
    sections = []
    search_cards = []
    for cat, (label, blurb) in cat_info.items():
        cat_pages = [x for x in all_pages if x["category"] == cat]
        cards = "".join(tool_card(x, base) for x in cat_pages)
        sections.append(f'<section class="cat" id="{cat}"><h2>{esc(label)}</h2><p class="cat-blurb">{esc(blurb)}</p>'
                        f'<div class="grid">{cards}</div></section>')
        for x in cat_pages:
            search_cards.append((x["h1"], x["desc"], base + x["slug"] + "/",
                                 TOOL_EMOJI.get(x["tool"], "🔧")))
    cards_js = json.dumps([{"t": t, "d": d, "u": u, "e": e} for t, d, u, e in search_cards],
                          ensure_ascii=False)
    chips = "".join(
        f'<a href="#{cat}">{CAT_EMOJI.get(cat, "")} {esc(label)}</a>'
        for cat, (label, _blurb) in cat_info.items())
    website_ld = {"@type": "WebSite", "name": "ToolTide", "url": base,
                  "description": desc, "potentialAction": {
                      "@type": "SearchAction",
                      "target": base + "?q={search_term_string}",
                      "query-input": "required name=search_term_string"}}

    doc = head_tags(cfg, "ToolTide — Free Online Tools: Calculators, Converters & Countdowns",
                    desc, canonical, [website_ld], root=True)
    doc += header_nav(cfg, base)
    doc += f"""<main class="wrap" id="main">
<section class="hero">
  <h1>Free online tools that just work</h1>
  <p>Countdowns, calculators, converters and generators — fast, private, and free. Everything runs in your browser; nothing you type ever leaves your device.</p>
  <input type="search" id="tool-search" placeholder="Search tools… (e.g. percent, kg, christmas)" aria-label="Search tools">
  <nav class="hero-chips" aria-label="Browse tools by category">{chips}</nav>
</section>
<div id="search-results" class="grid" style="display:none"></div>
{ad_slot(cfg, cfg.get('ad_slot_top', '1111111111'), 'top')}
{chr(10).join(sections)}
<section class="cat" id="all"><h2>About ToolTide</h2>
<p class="cat-blurb">ToolTide is a collection of small, fast, honest web tools. No accounts, no paywalls, no selling your data — each tool does one job and gets out of your way. Bookmark us and the tide of small annoyances goes out.</p></section>
</main>"""
    doc += footer(cfg, base, all_pages, cat_info)
    doc += f"""<script>(function(){{
var CARDS={cards_js};
var inp=document.getElementById('tool-search'),out=document.getElementById('search-results');
inp.addEventListener('input',function(){{
  var q=this.value.trim().toLowerCase();
  if(!q){{out.style.display='none';document.querySelectorAll('.cat').forEach(function(c){{if(c.id!=='all')c.style.display='block';}});return;}}
  document.querySelectorAll('.cat').forEach(function(c){{if(c.id!=='all')c.style.display='none';}});
  var hits=CARDS.filter(function(c){{return (c.t+' '+c.d).toLowerCase().indexOf(q)>=0;}}).slice(0,12);
  out.innerHTML=hits.map(function(c){{return '<a class="card" href="'+c.u+'"><span class="card-emoji">'+c.e+'</span><span class="card-title">'+c.t+'</span><span class="card-desc">'+c.d.slice(0,110)+'…</span></a>';}}).join('')
    || '<p class="cat-blurb">No tools match “'+q+'” — try “calculator”, “convert” or “days”.</p>';
  out.style.display='block';
}});
}})();</script></body></html>"""
    return doc


PRIVACY = """<h1>Privacy Policy</h1>
<p><em>Last updated: {date}</em></p>
<p>ToolTide is built to need as little of your data as possible. This policy explains what that means in practice.</p>
<h2>Tool inputs never leave your browser</h2>
<p>Every tool on this site — calculators, converters, counters, generators — runs entirely in your browser with JavaScript. The text, numbers and files you enter into a tool are processed on your device and are <strong>never transmitted to us, logged, or stored</strong>.</p>
<h2>Cookies and advertising</h2>
<p>{ads_line}</p>
<h2>Analytics</h2>
<p>{ga_line}</p>
<h2>Local storage</h2>
<p>We do not use browser local storage or cookies for our own purposes.</p>
<h2>Changes</h2>
<p>If this policy changes, the updated date at the top will change with it.</p>
<h2>Contact</h2>
<p>Questions about privacy? Use the <a href="{base}contact/">contact page</a>.</p>"""

ABOUT = """<h1>About ToolTide</h1>
<p>ToolTide is a collection of small, fast, honest web tools. Each tool does exactly one job — count down to a date, split a dinner bill, convert kilometers to miles — and does it without asking you for an account, a download, or your personal data.</p>
<h2>Our principles</h2>
<ul>
<li><strong>Private by architecture.</strong> Tools run in your browser. We couldn't see your inputs even if we wanted to.</li>
<li><strong>Fast on any device.</strong> No frameworks, no bloat — pages load instantly, even on slow connections.</li>
<li><strong>Free forever.</strong> The site is supported by unobtrusive advertising, never by selling your data or paywalling a tool you need.</li>
</ul>
<p>The site is actively maintained — new tools are added regularly based on what people actually search for.</p>"""

CONTACT = """<h1>Contact</h1>
<p>Found a bug, have an idea for a tool, or a business question? We read everything.</p>
<p><strong>Email:</strong> <a href="mailto:{email}" id="contact-email">{email}</a></p>
<p>We usually reply within a few days. For privacy questions, see the <a href="/privacy/">privacy policy</a>.</p>"""

ERROR404 = """<h1>404 — page drifted out with the tide</h1>
<p>The page you're looking for doesn't exist (or moved). Try one of our tools instead:</p>
<p><a class="btn" href="/">← Back to all tools</a></p>"""


def build_static(cfg, path, inner, title, desc, all_pages=(), cat_info=None):
    base = cfg["base_url"]
    canonical = base + path.strip("/") + ("/" if path.strip("/") and not path.endswith(".html") else "")
    doc = head_tags(cfg, title, desc, canonical, root=True)
    doc += header_nav(cfg, base)
    doc += crumb(base, [("🌊 ToolTide", base), (title.split("—")[0].strip(), None)])
    inner2 = (inner.replace("{date}", TODAY.isoformat())
                   .replace("{base}", base)
                   .replace("{email}", cfg.get("contact_email", "hello@example.com")))
    doc += f'<main class="wrap"><article class="static-page">{inner2}</article></main>'
    doc += footer(cfg, base, all_pages, cat_info)
    doc += "</body></html>"
    return doc


def write(path, content):
    full = os.path.join(SITE_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def main():
    cfg = load_config()
    os.makedirs(SITE_DIR, exist_ok=True)
    ensure_og_image()
    all_pages, cat_info = pages_mod.get_pages()

    # shared stylesheet
    with open(os.path.join(ROOT, "engine", "assets", "style.css"), encoding="utf-8") as f:
        write("style.css", f.read())
        print("  asset /style.css")

    # tool pages
    for p in all_pages:
        write(os.path.join(p["slug"], "index.html"), build_page(cfg, p, all_pages, cat_info))
        print(f"  page  /{p['slug']}/")

    # index
    write("index.html", build_index(cfg, all_pages, cat_info))
    print("  page  /")

    # static pages
    ads_line = ("We use Google AdSense to show ads. AdSense may use cookies (including the Google advertising "
                "cookie) to serve ads based on your prior visits. You can opt out of personalized advertising at "
                "<a href=\"https://adssettings.google.com\" rel=\"noopener\" target=\"_blank\">Google Ads Settings</a>. "
                if (cfg.get("adsense_client") or "").strip() else
                "This site currently runs no third-party advertising. If that changes, this policy will describe exactly what is used before it goes live.")
    ga_line = ("We use Google Analytics 4 with IP anonymization to count page views in aggregate. "
               "We never see individual browsing histories."
               if (cfg.get("ga4_id") or "").strip() else
               "We run no analytics on individual visitors. Aggregate, anonymous page counts may be collected by our host.")
    write("privacy/index.html", build_static(
        cfg, "privacy/", PRIVACY.replace("{ads_line}", ads_line).replace("{ga_line}", ga_line),
        "Privacy Policy — ToolTide", "ToolTide privacy policy: your tool inputs never leave your browser. Details on cookies, ads and analytics.",
        all_pages, cat_info))
    write("about/index.html", build_static(
        cfg, "about/", ABOUT, "About ToolTide — Free Online Tools",
        "About ToolTide: small, fast, honest web tools. Private by architecture, free forever.", all_pages, cat_info))
    write("contact/index.html", build_static(
        cfg, "contact/", CONTACT, "Contact — ToolTide",
        "Contact the ToolTide team: bug reports, tool ideas and business questions.", all_pages, cat_info))
    write("404.html", build_static(
        cfg, "404.html", ERROR404, "Page not found — ToolTide", "Page not found on ToolTide.",
        all_pages, cat_info))

    # ads.txt (AdSense anti-spoofing) — emitted only once adsense_client is set
    ads = (cfg.get("adsense_client") or "").strip()
    if ads:
        pub = ads[3:] if ads.startswith("ca-") else ads
        write("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
        print("  asset /ads.txt")

    # sitemap
    urls = [cfg["base_url"]] + [cfg["base_url"] + p["slug"] + "/" for p in all_pages] + \
           [cfg["base_url"] + s for s in ("about/", "privacy/", "contact/")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{esc(u)}</loc><lastmod>{TODAY.isoformat()}</lastmod>"
                  f"<changefreq>weekly</changefreq><priority>{'1.0' if u == cfg['base_url'] else '0.8'}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")

    # robots
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {cfg['base_url']}sitemap.xml\n")

    # IndexNow key file (Bing instant submission) — key persisted in config
    key = cfg.get("indexnow_key") or ""
    if key:
        write(key + ".txt", key)

    print(f"Built {len(all_pages)} tool pages + 5 site pages → docs/  ({cfg['base_url']})")


if __name__ == "__main__":
    main()
