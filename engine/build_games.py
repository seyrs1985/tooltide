# -*- coding: utf-8 -*-
"""Legacy /games/ path handler — the games section moved to its own site.

NeonPlay (https://seyrs1985.github.io/neonplay/) is now a separate sister site.
This script REMOVES the old docs/games/ build output and leaves permanent-style
redirect stubs behind so any URLs already indexed by Bing keep resolving.
ToolTide sitemap (tools only) is written by build.py and is left untouched.
"""

import os
import shutil
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SISTER_CONFIG = os.path.join(os.path.dirname(ROOT), "game-arcade", "config", "site.json")

REDIRECT_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redirecting…</title>
<link rel="canonical" href="{dest}">
<meta http-equiv="refresh" content="0; url={dest}">
<script>location.replace("{dest_js}");</script>
<style>body{{font-family:system-ui,sans-serif;background:#0b1020;color:#e2e8f0;display:grid;place-items:center;min-height:100vh;margin:0}}a{{color:#7dd3fc}}</style>
</head>
<body>
<main style="text-align:center;padding:2em">
<h1>🎮 The games moved</h1>
<p>Our games now live on their own site: <a href="{dest}">NeonPlay — free online games</a>.</p>
<p style="opacity:.7">ToolTide remains your home for free online tools. Redirecting you…</p>
</main>
</body>
</html>
"""


def write(rel, content):
    full = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  {rel}  ->  redirect")


def main():
    with open(SISTER_CONFIG, encoding="utf-8") as f:
        sCfg = json.load(f)
    dest_base = sCfg["base_url"]
    slugs = ["neon-tide", "snake", "2048", "memory-pairs", "tic-tac-toe"]

    games_dir = os.path.join(DOCS, "games")
    if os.path.isdir(games_dir):
        shutil.rmtree(games_dir)
        print("  removed docs/games/ (moved to NeonPlay)")

    write("games/index.html", REDIRECT_TMPL.format(
        dest=dest_base, dest_js=dest_base.replace('"', '\\"')))
    for s in slugs:
        dest = f"{dest_base}{s}/"
        write(f"games/{s}/index.html", REDIRECT_TMPL.format(
            dest=dest, dest_js=dest.replace('"', '\\"')))

    print(f"Games redirects built: {1 + len(slugs)} stubs -> {dest_base}")


if __name__ == "__main__":
    main()
