# -*- coding: utf-8 -*-
"""ToolTide static site builder.

Usage:  python engine/build.py
Reads config/site.json + engine/pages.py, writes the full static site to site/.
Only the Python standard library is used.
"""

import datetime
import hashlib
import html
import json
import os
import re
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
 "randomnum": "🎲", "roman": "🏛️", "wordspages": "📄", "grade": "🎓", "dedupe": "🧹", "slug": "🔗", "salestax": "🧾", "average": "🧮", "binary": "💾", "gramscups": "🥤", "fuel": "⛽", "salary": "💼", "sqft": "📐", "pxin": "🖨️", "unitconv": "🔄", "secondsconv": "⏱️", "coinflip": "🪙", "dice": "🎲", "half": "➗", "cubicft": "📦", "unitprice": "🏷️", "degrad": "📐", "romantable": "📜", "hexrgb": "🎨", "numwords": "🔠", "planets": "🪐", "binhex": "🔮", "combiner": "💞", "whitespace": "🧽", "yesno": "🍀", "prime": "🔢", "country": "🌍", "stlb": "⚖️", "ftincm": "📏", "emoji": "🎲", "factorial": "❗", "wordfreq": "📈", "sorter": "🔤", "letter": "🔤", "dayofweek": "📆", "percent": "📊",
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
TOUCH_ICON = "apple-touch-icon.png"
touch_icon_ready = False
MANIFEST = "manifest.webmanifest"
manifest_ready = False

# The stylesheet is inlined into every page's <head>: the site CSS is small
# (~4 KB gzipped), so inlining costs less per page than the render-blocking
# second request it replaces — first paint now needs only the HTML document.
# It also makes Pages' CDN staleness (~10 min after each deploy) harmless:
# HTML and CSS can never desync again. docs/style.css is still written as the
# canonical copy for anyone hot-linking it.
_css_cache = ""


def inline_css():
    """Minified stylesheet for inlining (comments stripped, whitespace folded)."""
    global _css_cache
    if not _css_cache:
        with open(os.path.join(ROOT, "engine", "assets", "style.css"), encoding="utf-8") as f:
            css = f.read()
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css).strip()
        assert "--brand" in css and "@media" in css and ".site-head" in css
        _css_cache = css
    return _css_cache

# Runs before first paint: marks <html class="js"> (reveals the theme toggle)
# and re-applies a visitor's saved light/dark choice ahead of the stylesheet.
PREPAINT_THEME = ('<script>(function(){var d=document.documentElement;d.classList.add("js");'
                  'try{var t=localStorage.getItem("tt-theme");'
                  'if(t==="light"||t==="dark")d.setAttribute("data-theme",t);}catch(e){}})();</script>')


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


def _ocean_icon(size, out):
    """Square ocean gradient + three waves — shared art for the iOS touch
    icon and the PWA manifest icons."""
    from PIL import Image, ImageDraw
    import math
    top, bot = (10, 58, 94), (14, 116, 144)  # same ocean ramp as the OG card
    img = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size, y)],
               fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    for amp, base_y, alpha in [(int(size * .078), int(size * .62), 70),
                               (int(size * .061), int(size * .74), 46),
                               (int(size * .044), int(size * .84), 30)]:
        pts = [(x, base_y + amp * math.sin(x / (size / 6.9))) for x in range(0, size + 1, 4)]
        ov.line(pts, fill=(255, 255, 255, alpha), width=max(4, size // 30))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(out, "PNG", optimize=True)


def ensure_touch_icon():
    """Generate docs/apple-touch-icon.png (180x180 iOS home-screen icon)."""
    global touch_icon_ready
    out = os.path.join(SITE_DIR, TOUCH_ICON)
    if os.path.exists(out):
        touch_icon_ready = True
        return
    try:
        _ocean_icon(180, out)
    except ImportError:
        return
    touch_icon_ready = True
    print(f"  asset /{TOUCH_ICON} (generated)")


def ensure_manifest(cfg):
    """docs/manifest.webmanifest — PWA install metadata. Icon files are shared
    square art at the two sizes Chrome's install prompt wants; without PIL the
    manifest is simply not injected (site works unchanged without it)."""
    global manifest_ready
    icons = []
    for size, name in ((192, "icon-192.png"), (512, "icon-512.png")):
        out = os.path.join(SITE_DIR, name)
        if not os.path.exists(out):
            try:
                _ocean_icon(size, out)
            except ImportError:
                return
            print(f"  asset /{name} (generated)")
        icons.append({"src": cfg["base_url"] + name, "sizes": f"{size}x{size}",
                      "type": "image/png", "purpose": "any"})
    manifest = {
        "name": "ToolTide — Free Online Tools",
        "short_name": "ToolTide",
        "description": "Free online tools: countdown timers, calculators, unit "
                       "converters and generators. Fast, private, no sign-up.",
        "start_url": cfg["base_url"],
        "scope": cfg["base_url"],
        "display": "standalone",
        "background_color": "#f8fafc",
        "theme_color": "#0e7490",
        "icons": icons,
    }
    write(MANIFEST, json.dumps(manifest, indent=2) + "\n")
    manifest_ready = True
    print(f"  asset /{MANIFEST}")


def head_tags(cfg, title, desc, canonical, extra_ld=(), root=False, body_cls=""):
    ga = (cfg.get("ga4_id") or "").strip()
    gsc = (cfg.get("gsc_verification") or "").strip()
    ads = (cfg.get("adsense_client") or "").strip()
    ld = json.dumps({"@context": "https://schema.org", "@graph": list(extra_ld)},
                    ensure_ascii=False, separators=(",", ":"))
    fav = ("data:image/svg+xml," +
           esc('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">🌊</text></svg>'))
    touch = (f'<link rel="apple-touch-icon" href="{esc(cfg["base_url"])}{TOUCH_ICON}">\n'
             if touch_icon_ready else "")
    pwa = (f'<link rel="manifest" href="{esc(cfg["base_url"])}{MANIFEST}">\n'
           if manifest_ready else "")
    og_abs = cfg["base_url"] + OG_IMAGE
    hints = ""
    if ga:
        hints += ('<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>\n'
                  '<link rel="dns-prefetch" href="https://www.googletagmanager.com">\n')
    if ads:
        hints += ('<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>\n'
                  '<link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">\n')
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
{og_img}<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0e7490" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1e293b" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{fav}">
{touch}{pwa}<link rel="search" type="application/opensearchdescription+xml" title="ToolTide" href="{esc(cfg['base_url'])}opensearch.xml">
{hints}{f'<meta name="google-site-verification" content="{esc(gsc)}">' if gsc else ''}
<script type="application/ld+json">{ld}</script>
{PREPAINT_THEME}
<style>{inline_css()}</style>
{f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(ads)}" crossorigin="anonymous"></script>' if ads else ''}
{f'<script async src="https://www.googletagmanager.com/gtag/js?id={esc(ga)}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{esc(ga)}");</script>' if ga else ''}
</head>
<body{f' class="{esc(body_cls)}"' if body_cls else ''}><a class="skip" href="#main">Skip to content</a>"""
    return h


def header_nav(cfg, base):
    links = "".join(
        f'<a href="{base}#{c}">{esc(n)}</a>'
        for c, n in [("calculator", "Calculators"), ("converter", "Converters"),
                     ("countdown", "Countdowns"), ("text", "Text"), ("generator", "Generators")]
    )
    games_url = (cfg.get("sister_site") or {}).get("url", "https://seyrs1985.github.io/neonplay/")
    # GET form into the homepage ?q= contract — search works from every page
    # with zero JS; hidden via CSS where a search box is already on screen.
    return f"""<header class="site-head">
  <div class="wrap nav-row">
    <a class="logo" href="{base}"><span aria-hidden="true">🌊</span> ToolTide</a>
    <form class="head-search" role="search" action="{base}" method="get">
      <input type="search" name="q" placeholder="Search tools…" aria-label="Search tools">
      <button type="submit" aria-label="Search"><span aria-hidden="true">🔍</span></button>
    </form>
    <nav aria-label="Primary"><a href="{esc(games_url)}" title="Our sister site: free online games"><span aria-hidden="true">🎮</span> Games</a>{links}<a href="{base}#all" class="nav-all">All tools</a></nav>
    <button class="theme-toggle" id="theme-toggle" type="button" aria-label="Switch color theme"><span aria-hidden="true">🌙</span></button>
  </div>
</header>"""


# footer tool matrix + hero chips — category keys must match the homepage section ids in pages.py
CAT_EMOJI = {"countdown": "⏳", "calculator": "🧮", "converter": "🔄",
             "text": "🔤", "generator": "🎲"}


def cat_emoji_html(cat):
    """Category emoji as a decorative span — kept out of link accessible names."""
    emo = CAT_EMOJI.get(cat, "")
    return f'<span aria-hidden="true">{emo}</span> ' if emo else ""


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
      <a href="{esc(games_url)}" title="Our sister site: free online games"><span aria-hidden="true">🎮</span> Games on NeonPlay</a>"""
    if kofi:
        site_links += f'\n      <a href="{esc(kofi)}" rel="noopener" target="_blank">☕ Support us</a>'
    cols = ""
    for cat, (label, _blurb) in (cat_info or {}).items():
        cat_pages = spread([x for x in all_pages if x["category"] == cat], 4)
        items = "".join(f'<a href="{base}{x["slug"]}/">{esc(foot_label(x))}</a>' for x in cat_pages)
        cols += (f'<nav class="foot-col" aria-label="{esc(label)}">'
                 f'<h3><a href="{base}#{cat}">{cat_emoji_html(cat)}{esc(label)}</a></h3>'
                 f'{items}</nav>')
    aff = ""
    if affiliate.get("url"):
        aff = f'<p class="aff-note">{esc(affiliate.get("disclosure", ""))} <a href="{esc(affiliate["url"])}" rel="sponsored noopener" target="_blank">{esc(affiliate.get("text", ""))}</a></p>'
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-brand">
      <a class="logo" href="{base}"><span aria-hidden="true">🌊</span> ToolTide</a>
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


# Floating back-to-top button — shared by every page. Hidden until the reader
# scrolls past the fold; smooth-scrolls unless the OS asks for reduced motion.
BACKTOP = """<button class="to-top" id="to-top" type="button" aria-label="Back to top">↑ <span aria-hidden="true">Top</span></button>
<script>(function(){
var b=document.getElementById('to-top');
if(!b)return;
var pending=false;
function update(){
  b.classList.toggle('show',window.scrollY>600);
}
window.addEventListener('scroll',function(){
  if(pending)return;
  pending=true;
  requestAnimationFrame(function(){update();pending=false;});
},{passive:true});
update();
b.addEventListener('click',function(){
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
  var h=document.querySelector('h1');
  if(h){h.setAttribute('tabindex','-1');h.focus({preventScroll:true});}
});
})();</script>"""

# Manual light/dark switch — the single piece of state we keep on a visitor's
# device (localStorage "tt-theme"), disclosed in the privacy policy.
THEME_JS = """<script>(function(){
var b=document.getElementById('theme-toggle');
if(!b)return;
var icon=b.querySelector('span');
function osDark(){return !!(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches);}
function current(){var a=document.documentElement.getAttribute('data-theme');return a==='dark'||a==='light'?a:(osDark()?'dark':'light');}
function syncMeta(t){var m=document.querySelectorAll('meta[name="theme-color"]');for(var i=0;i<m.length;i++){m[i].removeAttribute('media');m[i].setAttribute('content',t==='dark'?'#1e293b':'#0e7490');}}
function paint(t){
  document.documentElement.setAttribute('data-theme',t);
  icon.textContent=t==='dark'?'\\u2600\\uFE0F':'\\uD83C\\uDF19';
  b.setAttribute('aria-label',t==='dark'?'Switch to light theme':'Switch to dark theme');
}
b.addEventListener('click',function(){
  var t=current()==='dark'?'light':'dark';
  paint(t);syncMeta(t);
  try{localStorage.setItem('tt-theme',t);}catch(e){}
});
var saved=null;
try{saved=localStorage.getItem('tt-theme');}catch(e){}
if(saved==='dark'||saved==='light'){paint(saved);syncMeta(saved);}
else{paint(current());}
})();</script>"""

# Cards shown per homepage section before the "Show all" toggle takes over.
SECTION_TOP = 12

# Homepage section collapse: big categories hide cards beyond SECTION_TOP
# behind a "Show all" button. The hiding CSS is gated on html.js (set
# pre-paint by PREPAINT_THEME), so without JS nothing collapses and no card is
# ever lost. Deep links to a section anchor (hero chips, crumbs, footer)
# auto-expand it, and a second click re-collapses.
CATS_JS = """<script>(function(){
function setLabel(b,open){
  b.textContent=open?'Show fewer tools':'Show all '+b.getAttribute('data-count')+' tools';
}
function expand(sec){
  if(sec.classList.contains('open'))return;
  sec.classList.add('open');
  var b=sec.querySelector('.cat-more');
  if(b){b.setAttribute('aria-expanded','true');setLabel(b,true);}
}
// Anchor deep links (#converter from chips/crumbs/footer) must land exactly on
// the section: content-visibility placeholders make the pre-expand offsets
// lie, so re-anchor instantly after expanding instead of trusting the
// browser's fragment scroll.
function reveal(sec){
  expand(sec);
  if(sec.scrollIntoView){
    try{sec.scrollIntoView({behavior:'instant',block:'start'});}
    catch(e){sec.scrollIntoView();}
  }
}
function collapse(sec){
  if(!sec.classList.contains('open'))return;
  sec.classList.remove('open');
  var b=sec.querySelector('.cat-more');
  if(b){b.setAttribute('aria-expanded','false');setLabel(b,false);}
}
var secs=document.querySelectorAll('.cat');
for(var i=0;i<secs.length;i++){(function(sec){
  var b=sec.querySelector('.cat-more');
  if(!b)return;
  b.addEventListener('click',function(){
    if(sec.classList.contains('open'))collapse(sec);else expand(sec);
  });
})(secs[i]);}
function hashExpand(){
  var id=(location.hash||'').slice(1);
  if(!id)return;
  var sec=document.getElementById(id);
  if(sec&&sec.classList.contains('cat'))reveal(sec);
}
if(window.addEventListener)window.addEventListener('hashchange',hashExpand);
// Clicking a section anchor when the hash is already that value never fires
// hashchange — watch anchor clicks directly so a second chip click still
// expands and lands (reveal is idempotent).
if(document.addEventListener)document.addEventListener('click',function(e){
  var t=e.target,a=t&&t.closest?t.closest('a'):null;
  if(!a)return;
  var href=a.getAttribute('href')||'';
  var i=href.lastIndexOf('#');
  if(i<0)return;
  var sec=document.getElementById(href.slice(i+1));
  if(sec&&sec.classList.contains('cat'))reveal(sec);
});
hashExpand();
})();</script>"""


def tool_card(p, base, extra=False, cat_label=""):
    emoji = (p.get("args") or {}).get("emoji") or TOOL_EMOJI.get(p["tool"], "🔧")
    cls = f' class="card extra cat-{p["category"]}"' if extra \
        else f' class="card cat-{p["category"]}"'
    tag = f'<span class="card-tag">{esc(cat_label)}</span>' if cat_label else ""
    return (f'<a{cls} href="{base}{p["slug"]}/">'
            f'<span class="card-emoji" aria-hidden="true">{emoji}</span>'
            f'<span class="card-title">{esc(p["h1"])}</span>'
            f'{tag}'
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
    cat_label = (cat_info or {}).get(p["category"], ("",))[0]
    crumb_items = [("🌊 ToolTide", base)]
    if cat_label:
        crumb_items.append((cat_label, base + "#" + p["category"]))
    crumb_items.append((p["h1"], None))
    crumb_ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name,
         "item": (url or canonical)}
        for i, (name, url) in enumerate(crumb_items)]}

    related = [x for x in all_pages if x["category"] == p["category"] and x["slug"] != p["slug"]]
    related += [x for x in all_pages if x["category"] != p["category"]]
    related_html = "".join(
        tool_card(x, base, cat_label=(cat_info or {}).get(x["category"], ("",))[0])
        for x in related[:6])

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
    doc += crumb(base, crumb_items)
    doc += f"""<main class="wrap" id="main">
<article>
  <div class="page-emoji cat-{p['category']}" aria-hidden="true">{emoji}</div>
  <h1>{esc(p['h1'])}</h1>
  <noscript><p class="noscript-note">This tool runs entirely in your browser and needs JavaScript — please enable it and reload.</p></noscript>
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
    doc += BACKTOP
    doc += THEME_JS
    doc += "</body></html>"
    return doc


# Homepage closing section: the three principles from the About page as
# scannable cards, so the long tool list ends by setting expectations
# (private / fast / free) instead of trailing off into a paragraph.
VALUE_CARDS = [
    ("🔒", "Private by architecture",
     "Every tool runs entirely in your browser. The numbers and text you type "
     "never reach a server — there is simply nothing to send."),
    ("⚡", "Fast on any device",
     "No frameworks, no bloat, no spinner. Pages are tiny and load instantly, "
     "even on a slow mobile connection or an older device."),
    ("💚", "Free, forever",
     "No accounts, no paywalls, no locked features. Supported by unobtrusive "
     "ads — never by selling data or gating the tool you need."),
]


def values_html():
    cards = "".join(
        f'<div class="value-card"><span class="value-emoji" aria-hidden="true">{e}</span>'
        f'<h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for e, t, d in VALUE_CARDS)
    return f'<div class="values">{cards}</div>'


def build_index(cfg, all_pages, cat_info):
    base = cfg["base_url"]
    canonical = base
    desc = "ToolTide — free online tools: countdown timers, calculators, unit converters, word counter, password generator and more. Fast, private, no sign-up."
    sections = []
    search_cards = []
    counts = {c: sum(1 for x in all_pages if x["category"] == c) for c in cat_info}
    for cat, (label, blurb) in cat_info.items():
        cat_pages = [x for x in all_pages if x["category"] == cat]
        # collapse big sections: the rest sit behind a "Show all" toggle
        cards = "".join(tool_card(x, base, extra=i >= SECTION_TOP, cat_label=label)
                        for i, x in enumerate(cat_pages))
        more = ""
        if len(cat_pages) > SECTION_TOP:
            more = (f'<button class="cat-more" type="button" aria-expanded="false" '
                    f'aria-controls="{cat}" data-count="{len(cat_pages)}">'
                    f'Show all {len(cat_pages)} tools</button>')
        sections.append(f'<section class="cat" id="{cat}"><h2>{esc(label)} <span class="cat-count">{counts[cat]}</span></h2><p class="cat-blurb">{esc(blurb)}</p>'
                        f'<div class="grid">{cards}</div>{more}</section>')
        for x in cat_pages:
            search_cards.append((x["h1"], x["desc"], base + x["slug"] + "/",
                                 TOOL_EMOJI.get(x["tool"], "🔧"), label, x["slug"],
                                 x["category"]))
    cards_js = json.dumps([{"t": t, "d": d, "u": u, "e": e, "c": c, "s": s, "k": k}
                           for t, d, u, e, c, s, k in search_cards],
                          ensure_ascii=False)
    chips = "".join(
        f'<a href="#{cat}">{cat_emoji_html(cat)}{esc(label)} <span class="chip-n">{counts[cat]}</span></a>'
        for cat, (label, _blurb) in cat_info.items())
    website_ld = {"@type": "WebSite", "name": "ToolTide", "url": base,
                  "description": desc, "potentialAction": {
                      "@type": "SearchAction",
                      "target": base + "?q={search_term_string}",
                      "query-input": "required name=search_term_string"}}

    doc = head_tags(cfg, "ToolTide — Free Online Tools: Calculators, Converters & Countdowns",
                    desc, canonical, [website_ld], root=True, body_cls="home")
    doc += header_nav(cfg, base)
    doc += f"""<main class="wrap" id="main">
<section class="hero">
  <h1>Free online tools that just work</h1>
  <p>Countdowns, calculators, converters and generators — fast, private, and free. Everything runs in your browser; nothing you type ever leaves your device.</p>
  <input type="search" id="tool-search" placeholder="Search tools… (e.g. percent, kg, christmas)" aria-label="Search tools">
  <p class="search-status" id="search-status" role="status"></p>
  <nav class="hero-chips" aria-label="Browse tools by category">{chips}</nav>
</section>
<div id="search-results" class="grid" style="display:none"></div>
{ad_slot(cfg, cfg.get('ad_slot_top', '1111111111'), 'top')}
{chr(10).join(sections)}
<section class="cat" id="all"><h2>About ToolTide</h2>
<p class="cat-blurb">ToolTide is a collection of small, fast, honest web tools. No accounts, no paywalls, no selling your data — each tool does one job and gets out of your way. Bookmark us and the tide of small annoyances goes out.</p>
{values_html()}</section>
</main>"""
    doc += footer(cfg, base, all_pages, cat_info)
    doc += BACKTOP
    doc += THEME_JS
    doc += CATS_JS
    doc += f"""<script>(function(){{
var CARDS={cards_js};
var inp=document.getElementById('tool-search'),out=document.getElementById('search-results'),live=document.getElementById('search-status');
function esc(s){{return s.replace(/[&<>"']/g,function(m){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[m];}});}}
var ALIAS={{f:'fahrenheit',c:'celsius',k:'kilogram',kg:'kilogram kilograms',lb:'pound pounds',lbs:'pound pounds',km:'kilometer',mi:'mile',cm:'centimeter',mm:'millimeter',ft:'feet',yd:'yard',oz:'ounce',gal:'gallon',pt:'pint',qt:'quart'}};
function hay(c){{return (c.t+' '+c.d+' '+c.c+' '+c.s).toLowerCase();}}
function groups(q){{return q.split(/\\s+/).filter(Boolean).map(function(t){{
  var v=[t];if(ALIAS[t])v=v.concat(ALIAS[t].split(' '));return v;}});}}
function grpLen(t,s,g){{var bt=0,bs=0;g.forEach(function(v){{
  var i=t.indexOf(v);if(i>=0&&v.length>bt)bt=v.length;
  i=s.indexOf(v);if(i>=0&&v.length>bs)bs=v.length;}});return bt*2+bs;}}
function find(q,gs){{
  var ph=CARDS.filter(function(c){{return hay(c).indexOf(q)>=0;}});
  if(ph.length||gs.length<2)return ph.slice(0,12);
  var all=CARDS.filter(function(c){{var h=hay(c);
    return gs.every(function(g){{return g.some(function(v){{return h.indexOf(v)>=0;}});}});}});
  all.sort(function(a,b){{return score(b,gs)-score(a,gs);}});
  return all.slice(0,12);
}}
function score(c,gs){{var t=c.t.toLowerCase(),n=0;gs.forEach(function(g){{n+=grpLen(t,c.s,g);}});return n;}}
function hiTok(s,flat){{var low=s.toLowerCase(),res='',pos=0;
  flat=flat.filter(function(t){{return t.length>=2;}});
  for(;;){{var best=-1,bl=0;
    flat.forEach(function(t){{var i=low.indexOf(t,pos);if(i>=0&&(best<0||i<best)){{best=i;bl=t.length;}}}});
    if(best<0){{res+=esc(s.slice(pos));break;}}
    res+=esc(s.slice(pos,best))+'<mark>'+esc(s.substr(best,bl))+'</mark>';pos=best+bl;}}
  return res;}}
function card(c,flat){{return '<a class="card cat-'+c.k+'" href="'+c.u+'"><span class="card-emoji" aria-hidden="true">'+c.e+'</span><span class="card-title">'+hiTok(c.t,flat)+'</span><span class="card-tag">'+esc(c.c)+'</span><span class="card-desc">'+hiTok(c.d.slice(0,110),flat)+'</span></a>';}}
inp.addEventListener('input',function(){{
  var q=this.value.trim().toLowerCase();
  if(!q){{out.style.display='none';out.innerHTML='';if(live)live.textContent='';document.querySelectorAll('.cat').forEach(function(c){{if(c.id!=='all')c.style.display='';}});return;}}
  document.querySelectorAll('.cat').forEach(function(c){{if(c.id!=='all')c.style.display='none';}});
  var gs=groups(q),flat=[];gs.forEach(function(g){{flat=flat.concat(g);}});
  var hits=find(q,gs);
  if(live)live.textContent=hits.length?hits.length+(hits.length===1?' tool matches':' tools match')+' “'+q+'”':'No tools match “'+q+'”';
  out.innerHTML=hits.map(function(c){{return card(c,flat);}}).join('')
    || '<p class="cat-blurb">No tools match “'+esc(q)+'” — try “calculator”, “convert” or “days”, or <a href="#all">browse all tools</a>.</p>';
  out.style.display='grid';
}});
inp.addEventListener('keydown',function(e){{
  if(e.key==='Enter'){{var first=out.querySelector('a.card');if(first){{e.preventDefault();location.assign(first.href);}}}}
}});
document.addEventListener('keydown',function(e){{
  if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement||{{}}).tagName||'')){{e.preventDefault();inp.focus();}}
}});
var qs=new URLSearchParams(location.search).get('q');
if(qs){{inp.value=qs;inp.dispatchEvent(new Event('input'));}}
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
<p>The only thing we keep in your browser is one preference: your light or dark theme choice, saved via local storage when you use the theme toggle in the header. It never leaves your device and you can clear it anytime from your browser settings. We set no cookies of our own.</p>
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
<p>The page you're looking for doesn't exist (or moved). Search our tools:</p>
<form class="four04-search" action="{base}" method="get">
  <input type="search" name="q" placeholder="Search tools… (e.g. percent, kg, christmas)" aria-label="Search tools">
  <button class="btn" type="submit">Search</button>
</form>
<p>Or <a href="{base}#all">browse all tools</a> instead.</p>"""


def build_static(cfg, path, inner, title, desc, all_pages=(), cat_info=None, body_cls=""):
    base = cfg["base_url"]
    canonical = base + path.strip("/") + ("/" if path.strip("/") and not path.endswith(".html") else "")
    doc = head_tags(cfg, title, desc, canonical, root=True, body_cls=body_cls)
    doc += header_nav(cfg, base)
    doc += crumb(base, [("🌊 ToolTide", base), (title.split("—")[0].strip(), None)])
    inner2 = (inner.replace("{date}", TODAY.isoformat())
                   .replace("{base}", base)
                   .replace("{email}", cfg.get("contact_email", "hello@example.com")))
    doc += f'<main class="wrap"><article class="static-page">{inner2}</article></main>'
    doc += footer(cfg, base, all_pages, cat_info)
    doc += BACKTOP
    doc += THEME_JS
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
    ensure_touch_icon()
    ensure_manifest(cfg)
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
        all_pages, cat_info, body_cls="fourohfour"))

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

    # OpenSearch description — lets browsers register ToolTide as a site search
    # engine; template reuses the homepage ?q= deep-link contract.
    write("opensearch.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>ToolTide</ShortName>
  <Description>Search free online tools on ToolTide</Description>
  <InputEncoding>UTF-8</InputEncoding>
  <Url type="text/html" method="get" template="{cfg['base_url']}?q={{searchTerms}}"/>
</OpenSearchDescription>
""")
    print("  asset /opensearch.xml")

    # IndexNow key file (Bing instant submission) — key persisted in config
    key = cfg.get("indexnow_key") or ""
    if key:
        write(key + ".txt", key)

    print(f"Built {len(all_pages)} tool pages + 5 site pages → docs/  ({cfg['base_url']})")


if __name__ == "__main__":
    main()
