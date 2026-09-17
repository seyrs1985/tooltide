# -*- coding: utf-8 -*-
"""One-shot: wire ALL Share buttons in tools.py.
- static: <button ...>Share X</button>  -> insert data-i18n="share.<slug>"
- JS:     .textContent='Share X'        -> .textContent=TT('share.<slug>','Share X')
Also emits _tmp_share_texts.json mapping slug -> english text.
Idempotent: already-wired occurrences are skipped."""
import re, json, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()

def slug(t):
    return "share." + re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

texts = {}

# --- JS restores (do BEFORE static so inserted attrs don't confuse) ---
def js_sub(m):
    text = m.group(2)
    k = slug(text)
    texts[k] = text
    return "textContent=TT('" + k + "','" + text.replace("'", "\\'") + "')"

s2, n_js = re.subn(r"textContent=('|\")(Share[^'\"]*)\1", js_sub, s)

# --- static buttons ---
def st_sub(m):
    text = m.group(2)
    k = slug(text)
    texts[k] = text
    return m.group(1) + ' data-i18n="' + k + '">' + text + m.group(3)

s3, n_st = re.subn(r"(<button\b[^>]*?)>((?:Share |&#x27;)[^<]*)(</button>)", st_sub, s2)

io.open(P, "w", encoding="utf-8", newline="").write(s3)
json.dump(texts, io.open("_tmp_share_texts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
print("js_wired", n_js, "| static_wired", n_st, "| distinct_texts", len(texts))
missing = [t for k, t in texts.items() if "'" in t and "\\'" not in t]
print("texts_with_apostrophe:", len([t for t in texts.values() if "'" in t]))
