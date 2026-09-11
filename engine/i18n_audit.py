# -*- coding: utf-8 -*-
"""i18n audit: every data-i18n key used in docs/ must exist in the language
tables, and every page must load i18n.js. Exit 1 on any gap. Run after
engine/build.py."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
LANGS = ["zh", "es", "pt", "ru", "ja", "ko", "de", "fr", "id"]

import json
with open(os.path.join(HERE, "_i18n_tables.json"), encoding="utf-8") as f:
    tables = json.load(f)

fail = 0


def err(msg):
    global fail
    fail += 1
    print("FAIL:", msg)


# 1. per-language key parity + non-empty values inside the tables
base_keys = set(k for k, _ in tables["chrome"]["zh"])
for l in LANGS:
    keys = set(k for k, _ in tables["chrome"][l])
    if keys != base_keys:
        err("table parity %s: missing %s extra %s" % (l, base_keys - keys, keys - base_keys))
    for k, v in tables["chrome"][l]:
        if not v.strip():
            err("empty value %s.%s" % (l, k))

key_attrs = re.compile(r'data-i18n(?:-html|-placeholder|-aria|-title)?="([^"]+)"')
js_lit = re.compile(r"\b(?:npT|T)\('([a-z0-9._]+)'\)")
used = {}
pages = 0
for dirpath, _dirs, files in os.walk(DOCS):
    for fn in files:
        if fn not in ("index.html", "404.html"):
            continue
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, DOCS).replace("\\", "/")
        if "/play/" in rel:
            continue
        html_txt = open(p, encoding="utf-8").read()
        pages += 1
        if "i18n.js" not in html_txt:
            err("%s: i18n.js not loaded" % rel)
        for m in key_attrs.finditer(html_txt):
            used.setdefault(m.group(1), set()).add(rel)
        for m in js_lit.finditer(html_txt):
            used.setdefault(m.group(1), set()).add(rel)

for k in sorted(used):
    if k in base_keys:
        continue
    if k.startswith("cat."):
        continue
    err("key '%s' used in %d page(s), e.g. %s — not in tables" % (k, len(used[k]), sorted(used[k])[0]))

# 2. every category shipped in pages.py must be fully translated
sys.path.insert(0, HERE)
import pages as pages_mod  # noqa: E402
_pages, cat_info = pages_mod.get_pages()
for cat in cat_info:
    for suffix in ("", ".blurb"):
        if ("cat." + cat + suffix) not in base_keys:
            err("category '%s' missing translation key 'cat.%s%s'" % (cat, cat, suffix))

print("i18n audit: %d pages scanned, %d distinct keys, %d langs" % (pages, len(used), len(LANGS)))
sys.exit(1 if fail else 0)
