import re, os, html, collections
SITE="docs"; pages=[]
for dp,_,fns in os.walk(SITE):
    for fn in fns:
        if fn.endswith(".html"): pages.append(os.path.join(dp,fn))
print("pages:",len(pages))
issues=collections.Counter(); samples=collections.defaultdict(list)
TAG=re.compile(r'<(h[1-6])\b',re.I)
for p in pages:
    s=open(p,encoding="utf-8").read()
    # heading skips
    hs=[int(m.group(1)) for m in re.finditer(r'<h([1-6])\b',s,re.I)]
    for a,b in zip(hs,hs[1:]):
        if b>a+1:
            issues["heading-skip h%d>h%d"%(a,b)]+=1
            if len(samples["heading-skip"])<5: samples["heading-skip"].append(p)
    # duplicate ids
    ids=re.findall(r'\sid="([^"]+)"',s)
    for k,v in collections.Counter(ids).items():
        if v>1:
            issues["dup-id"]+=1
            if len(samples["dup-id"])<8: samples["dup-id"].append(p+" #"+k)
    # links without text
    for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>',s,re.S|re.I):
        attrs,body=m.group(1),m.group(2)
        if re.search(r'aria-label=',attrs) or re.search(r'title=',attrs): continue
        txt=re.sub(r'<[^>]+>','',body).strip()
        if not txt:
            issues["empty-link"]+=1
            if len(samples["empty-link"])<6: samples["empty-link"].append(p+" "+attrs[:80])
    # inputs without label
    for m in re.finditer(r'<(input|select|textarea)\b([^>]*)>',s,re.I):
        attrs=m.group(2)
        if re.search(r'type\s*=\s*"(hidden|submit|button)"',attrs,re.I): continue
        if 'id=' not in attrs and 'aria-label' not in attrs and 'aria-labelledby' not in attrs:
            # label wrap check: rough
            issues["input-no-id/label"]+=1
            if len(samples["input-no-id/label"])<8: samples["input-no-id/label"].append(p+" "+attrs[:90])
    # iframes without title
    for m in re.finditer(r'<iframe\b([^>]*)>',s,re.I):
        if 'title=' not in m.group(1):
            issues["iframe-no-title"]+=1
            if len(samples["iframe-no-title"])<4: samples["iframe-no-title"].append(p)
    # buttons without text/aria
    for m in re.finditer(r'<button\b([^>]*)>(.*?)</button>',s,re.S|re.I):
        attrs,body=m.group(1),m.group(2)
        if re.search(r'aria-label|>',attrs): continue
        txt=re.sub(r'<[^>]+>','',body).strip()
        if not txt:
            issues["empty-button"]+=1
            if len(samples["empty-button"])<6: samples["empty-button"].append(p+" "+attrs[:80])
for k,v in issues.most_common(): print(k,v)
for k,v in samples.items(): print("SAMPLE",k,v[:5])
