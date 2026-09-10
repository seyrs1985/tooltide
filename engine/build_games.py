# -*- coding: utf-8 -*-
"""Builds the /games/ section: hall page, per-game landing pages (iframe embed,
SEO content, ads slots) and copies playable builds from engine/assets/games.
Also regenerates sitemap.xml to include game URLs. Run AFTER build.py.
"""

import datetime
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import games as games_mod  # noqa: E402
from pages import get_pages  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
ASSETS = os.path.join(ROOT, "engine", "assets", "games")
TODAY = datetime.date.today().isoformat()


def esc(s):
    return html.escape(str(s), quote=True)


def ad_slot(cfg, slot_id):
    client = (cfg.get("adsense_client") or "").strip()
    if not client:
        return ""
    return (f'<div class="ad"><ins class="adsbygoogle" style="display:block" '
            f'data-ad-client="{esc(client)}" data-ad-slot="{esc(slot_id)}" '
            f'data-ad-format="auto" data-full-width-responsive="true"></ins>'
            f"<script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>")


def head(cfg, title, desc, canonical, csspath, extra_ld=()):
    ga = (cfg.get("ga4_id") or "").strip()
    gsc = (cfg.get("gsc_verification") or "").strip()
    ads = (cfg.get("adsense_client") or "").strip()
    ld = json.dumps({"@context": "https://schema.org", "@graph": list(extra_ld)},
                    ensure_ascii=False, separators=(",", ":"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta name="theme-color" content="#0e7490">
{f'<meta name="google-site-verification" content="{esc(gsc)}">' if gsc else ''}
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="{csspath}">
{f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(ads)}" crossorigin="anonymous"></script>' if ads else ''}
{f'<script async src="https://www.googletagmanager.com/gtag/js?id={esc(ga)}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{esc(ga)}");</script>' if ga else ''}
</head>
<body>"""


def nav(base):
    return f"""<header class="site-head"><div class="wrap nav-row">
<a class="logo" href="{base}">🌊 ToolTide</a>
<nav><a href="{base}games/">🎮 Games</a><a href="{base}#calculator">Calculators</a><a href="{base}#converter">Converters</a><a href="{base}#generator">Generators</a></nav>
</div></header>"""


def footer(cfg, base):
    kofi = (cfg.get("kofi_url") or "").strip()
    kofi_link = (f'<a href="{esc(kofi)}" rel="noopener" target="_blank">☕ Support us</a>' if kofi else "")
    return f"""<footer class="site-foot"><div class="wrap">
<nav><a href="{base}about/">About</a><a href="{base}privacy/">Privacy</a><a href="{base}contact/">Contact</a>{kofi_link}</nav>
<p>© {datetime.date.today().year} ToolTide · Free games and tools that run in your browser.</p>
</div></footer>"""


def card(gm, base):
    return (f'<a class="card" href="{base}games/{gm["slug"]}/">'
            f'<span class="card-emoji">{gm["emoji"]}</span>'
            f'<span class="card-title">{esc(gm["h1"])}</span>'
            f'<span class="card-desc">{esc(gm["tagline"][:110])}</span></a>')


def build_hall(cfg, gms):
    base = cfg["base_url"]
    canonical = base + "games/"
    desc = ("Play free browser games on ToolTide: original arcade, puzzle and card games. "
            "No download, no sign-up — instant play on desktop and mobile.")
    cards = "".join(card(gm, base) for gm in gms)
    doc = head(cfg, "Free Online Games — Arcade, Puzzle & Card Games | ToolTide",
               desc, canonical, "../style.css", [{
                   "@type": "CollectionPage", "name": "ToolTide Games", "url": canonical,
                   "description": desc}])
    doc += nav(base)
    doc += f"""<main class="wrap">
<section class="hero"><h1>Free games, zero friction</h1>
<p>Original games that load instantly and run in your browser — no downloads, no accounts, no interruptions. Built with care, played with joy.</p></section>
{ad_slot(cfg, cfg.get('ad_slot_top', '1111111111'))}
<section class="cat"><h2>All games</h2><div class="grid">{cards}</div></section>
<section class="cat" id="about"><h2>Our games are originals</h2>
<p class="cat-blurb">Every game here is either built by us or properly licensed — no scraped clones, no sketchy redirects. They run 100% locally in your browser; nothing you do in a game is tracked or uploaded.</p></section>
</main>"""
    doc += footer(cfg, base) + "</body></html>"
    write("games/index.html", doc)
    print("  game-hall /games/")


def build_landing(cfg, gm, gms):
    base = cfg["base_url"]
    slug = gm["slug"]
    canonical = f"{base}games/{slug}/"
    webapp_ld = {"@type": "VideoGame", "name": gm["h1"], "url": canonical,
                 "description": gm["desc"], "genre": ["Arcade", "Casual"],
                 "gamePlatform": "Web browser", "applicationCategory": "Game",
                 "operatingSystem": "Any", "playMode": "SinglePlayer",
                 "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in gm["faqs"]]}
    howto = "".join(f"<li>{esc(s)}</li>" for s in gm["howto"])
    faqs = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
                   for q, a in gm["faqs"])
    related = "".join(card(x, base) for x in gms if x["slug"] != slug)
    doc = head(cfg, gm["title"], gm["desc"], canonical, "../../style.css",
               [webapp_ld, faq_ld])
    doc += nav(base)
    doc += f"""<main class="wrap">
<article>
<nav class="crumbs" style="margin-top:16px"><a href="{base}">🌊 ToolTide</a> › <a href="{base}games/">Games</a> › <span>{esc(gm['h1'])}</span></nav>
<div class="page-emoji" style="margin-top:14px">{gm['emoji']}</div>
<h1>{esc(gm['h1'])}</h1>
<p class="cat-blurb" style="margin-top:-4px">{esc(gm['tagline'])}</p>
<div class="game-frame">
  <iframe src="{gm.get('play', 'play.html')}" title="{esc(gm['h1'])} — playable" allow="autoplay; fullscreen; gamepad" allowfullscreen></iframe>
  <button id="fs-btn" type="button" title="Fullscreen">⛶</button>
</div>
<p class="controls-line">🎮 {esc(gm['controls'])}</p>
{ad_slot(cfg, cfg.get('ad_slot_mid', '2222222222'))}
<section class="seo-block"><h2>How to play</h2><ol class="howto">{howto}</ol></section>
<section class="seo-block"><h2>Frequently asked questions</h2>{faqs}</section>
<section class="seo-block"><h2>More games</h2><div class="grid">{related}</div></section>
</article>
</main>"""
    doc += footer(cfg, base)
    doc += """<script>(function(){
var f=document.querySelector('.game-frame iframe'),b=document.getElementById('fs-btn');
if(b&&f){b.addEventListener('click',function(){
  if(document.fullscreenElement){document.exitFullscreen();}
  else if(f.requestFullscreen){f.requestFullscreen();}
});}
})();</script></body></html>"""
    write(f"games/{slug}/index.html", doc)
    print(f"  game-page /games/{slug}/")


def write(rel, content):
    full = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def copy_play(gm):
    dst = os.path.join(DOCS, "games", gm["slug"])
    os.makedirs(dst, exist_ok=True)
    play = gm.get("play", "play.html")
    src = os.path.join(ASSETS, gm["slug"], play.rstrip("/"))
    if play.endswith("/"):
        target = os.path.join(dst, "play")
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(src, target)
    else:
        shutil.copy2(src, os.path.join(dst, os.path.basename(play)))


def sitemap(cfg, gms):
    base = cfg["base_url"]
    tool_slugs = [p["slug"] for p in get_pages()[0]]
    urls = ([base] +
            [base + s + "/" for s in tool_slugs] +
            [base + "games/"] +
            [base + "games/" + gm["slug"] + "/" for gm in gms] +
            [base + s for s in ("about/", "privacy/", "contact/")])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{esc(u)}</loc><lastmod>{TODAY}</lastmod>"
                  f"<changefreq>weekly</changefreq><priority>0.8</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    print(f"  sitemap: {len(urls)} urls (tools + games)")


def main():
    cfg_path = os.path.join(ROOT, "config", "site.json")
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    gms = games_mod.GAMES
    for gm in gms:
        copy_play(gm)
    build_hall(cfg, gms)
    for gm in gms:
        build_landing(cfg, gm, gms)
    sitemap(cfg, gms)
    print(f"Games section built: {len(gms)} games")


if __name__ == "__main__":
    main()
