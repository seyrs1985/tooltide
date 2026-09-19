# -*- coding: utf-8 -*-
"""One-shot: wire fuelcost renderer strings in tools.py. Idempotent."""
import re, io

P = "tools.py"
s = io.open(P, encoding="utf-8").read()
n_total = 0

PAIRS = [
 (r'(<label for="fu-l">)Liters per 100 km(</label>)', "fu.l100", "Liters per 100 km"),
 (r'(<label for="fu-m">)Miles per gallon \(US\)(</label>)', "fu.mpgus", "Miles per gallon (US)"),
 (r"unit\.textContent='\(US\)'", "fu.us", "(US)"),
 (r"return l<=6\?'efficient':l<=9\?'typical':'thirsty';", "verdicts"),
 (r"hint\.textContent='Lower L/100km is better · higher MPG is better\.'", "fu.hintbetter", "Lower L/100km is better · higher MPG is better."),
 (r"hint\.textContent=v\+' L/100km = '\+Math\.round\(mpg\*10\)/10\+' US mpg — '\+good\(v\)\+' for a petrol car\.'", "fu.hintl"),
 (r"hint\.textContent=v\+' mpg = '\+Math\.round\(l\*100\)/100\+' L/100km - '\+good\(l\)\+' for a petrol car\.'", "fu.hintm"),
]

def wire_verdicts(m):
    return ("function good(l){return l<=6?TT('fu.efficient','efficient'):l<=9?TT('fu.typical','typical'):TT('fu.thirsty','thirsty');}")

# 1. static labels
for pat, key, text in PAIRS[:2]:
    def sub(m, key=key, text=text):
        return m.group(1) + ' data-i18n="' + key + '">' + text + m.group(2)
    s, n = re.subn(pat, sub, s)
    n_total += n

# 2. (US)
s, n = re.subn(PAIRS[2][0], "unit.textContent=TT('fu.us','(US)')", s)
n_total += n

# 3. verdicts
s, n = re.subn(PAIRS[3][0], wire_verdicts, s)
n_total += n

# 4. hint better
s, n = re.subn(PAIRS[4][0], "hint.textContent=TT('fu.hintbetter','Lower L/100km is better · higher MPG is better.')", s)
n_total += n

# 5. hint templates
s, n = re.subn(PAIRS[5][0], "hint.textContent=TT('fu.hintl','{l} L/100km = {m} US mpg — {v} for a petrol car.').replace('{l}',v).replace('{m}',Math.round(mpg*10)/10).replace('{v}',good(v))", s)
n_total += n
s, n = re.subn(PAIRS[6][0], "hint.textContent=TT('fu.hintm','{m} mpg = {l} L/100km - {v} for a petrol car.').replace('{m}',v).replace('{l}',Math.round(l*100)/100).replace('{v}',good(l))", s)
n_total += n

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("fu_wired", n_total)
