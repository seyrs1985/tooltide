# -*- coding: utf-8 -*-
"""One-shot: wire developer-family shared strings in tools.py (idempotent).
Covers: result-unit 'output', 'input chars', 'output chars', 'UTF-8 bytes in',
'Copy output' buttons + restore assignments, 'Nothing to copy',
'Invalid Base64', 'Malformed input'."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

def sub(pat, repl_factory, s):
    global n_total
    s2, n = re.subn(pat, repl_factory, s)
    n_total += n
    return s2

# result-unit 'output' (exact)
s = sub(r'(<span class="result-unit"[^>]*>)output(</span>)',
        lambda m: m.group(1) + '<span data-i18n="dev.output">output</span>' + m.group(2), s)
# stat labels
s = sub(r'(<span>)input chars(</span>)',
        lambda m: m.group(1) + '<span data-i18n="dev.inchars">input chars</span>' + m.group(2), s)
s = sub(r'(<span>)output chars(</span>)',
        lambda m: m.group(1) + '<span data-i18n="dev.outchars">output chars</span>' + m.group(2), s)
s = sub(r'(<span>)UTF-8 bytes in(</span>)',
        lambda m: m.group(1) + '<span data-i18n="dev.utf8">UTF-8 bytes in</span>' + m.group(2), s)
# Copy output buttons (static)
s = sub(r'(<button type="button" class="tool-btn"[^>]*?)>Copy output(</button>)',
        lambda m: m.group(1) + ' data-i18n="dev.copyout">Copy output' + m.group(2), s)
# Nothing to copy (dynamic)
s = sub(r"textContent='Nothing to copy'",
        lambda m: "textContent=TT('dev.nothing','Nothing to copy')", s)
# Copy output restore (dynamic, single-quoted)
s = sub(r"textContent='Copy output'",
        lambda m: "textContent=TT('dev.copyout','Copy output')", s)
# per-tool errors
s = sub(r"'Invalid Base64'",
        lambda m: "TT('dev.invalidb64','Invalid Base64')", s)
s = sub(r"'Malformed input'",
        lambda m: "TT('dev.malformed','Malformed input')", s)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("dev_family_wired", n_total)
