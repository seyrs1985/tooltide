# -*- coding: utf-8 -*-
"""One-shot: wire DSTPLAN (tt-dst) labels/spans/button/title in tools.py. Idempotent."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 (r'(<label for="dst-r")>Region(</label>)', "dst.region", "Region"),
 (r'(<label for="dst-p")>Shift pace per day(</label>)', "dst.pace", "Shift pace per day"),
 (r'(<span class="result-unit")>clocks fall back(</span>)', "dst.fallback", "clocks fall back"),
 (r'(<span>)start shifting on(</span>)', "dst.starton", "start shifting on"),
 (r'(<span>)days from today(</span>)', "dst.daysfrom", "days from today"),
 (r'(<span>)bedtime shift daily(</span>)', "dst.bedtime", "bedtime shift daily"),
 (r'(<button type="button" class="tool-btn" id="dst-share")>Share my shift plan(</button>)', "share.share-my-shiftplan", "Share my shift plan"),
]
for pat, key, text in PAIRS:
    def sub(m, key=key, text=text):
        return m.group(1) + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

# title prefix
s, n = re.subn(r"document\.title='Fall back '\+cs\+' - ToolDune';",
               "document.title=TT('dst.fallback','Fall back ')+cs+' - ToolDune';", s)
n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("dst_wired", n_total)
