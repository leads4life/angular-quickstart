import re,os,glob
D='dist'; ids={}
for f in glob.glob(D+'/*.html'):
    s=open(f).read(); ids[os.path.basename(f)]=set(re.findall(r'\sid="([^"]+)"',s))
bad=[]
for f in glob.glob(D+'/*.html'):
    s=open(f).read(); b=os.path.basename(f)
    for h in re.findall(r'<a\b[^>]*\shref="([^"]+)"',s):
        if h.startswith(('http','tel:','mailto:')): continue
        p,_,a=h.partition('#'); p=p or b
        if p not in ids: bad.append((b,h)); continue
        if a and a not in ids[p]: bad.append((b,h))
    for i in re.findall(r'img/[\w.-]+',s):
        if not os.path.exists(os.path.join(D,i)): bad.append((b,i))
    # duplicate ids
    al=re.findall(r'\sid="([^"]+)"',s); d={x for x in al if al.count(x)>1}
    if d: bad.append((b,'dup ids',d))
print(bad or 'links ok')
