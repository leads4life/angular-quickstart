#!/usr/bin/env python3
"""Build the Golden Lotus site: python3 site.py [outdir]"""
import re, sys, os, shutil
ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'dist')
PAGES={ # key: (filename, body_file, title)
 'home':('index.html',None,'Golden Lotus Chinese Restaurant | Wellington, FL'),
 'menu':('menu.html','pages/menu.html','Menu | Golden Lotus Chinese Restaurant'),
 'takeout':('takeout-delivery.html','pages/takeout.html','Takeout & Delivery | Golden Lotus'),
 'events':('private-events.html','pages/events.html','Private Events | Golden Lotus'),
 'about':('about.html','pages/about.html','About | Golden Lotus'),
 'contact':('contact.html','pages/contact.html','Contact & Hours | Golden Lotus'),
 'privacy':('privacy.html','pages/privacy.html','Privacy Policy | Golden Lotus'),
 'accessibility':('accessibility.html','pages/accessibility.html','Accessibility | Golden Lotus'),
}
rd=lambda p: open(os.path.join(ROOT,p),encoding='utf-8').read()
T=rd('template.html')
def block(name):
    m=re.search(r'<!--%s-->(.*?)<!--/%s-->'%(name,name),T,re.S); assert m,name; return m.group(1).strip()
head=T[:T.index('<!--DEFS-->')]
head=re.sub(r'<title>.*?</title>\s*','',head,flags=re.S)
head=head.replace('</style>','</style>\n<style>\n'+rd('pages.css')+rd('legal.css')+'</style>')
defs,header,home,footer,script=(block(n) for n in ('DEFS','HEADER','HOME','FOOTER','SCRIPT'))
band=rd('pages/_band.html')
js='<script>\n'+rd('pages.js')+'</script>'
def include(s):
    return re.sub(r'<!--@include (\S+)-->',lambda m: rd(m.group(1)),s)
def esc(s): return s.replace('&','&amp;')
def build(key):
    fn,body,title=PAGES[key]
    main=home if body is None else include(rd(body))+'\n'+band
    hdr,ftr=header,footer
    hdr=hdr.replace(f'href="@@{key}@@"',f'href="@@{key}@@" aria-current="page"')
    ftr=ftr.replace(f'href="@@{key}@@"',f'href="@@{key}@@" aria-current="page"')
    doc=f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>{esc(title)}</title>\n{head.strip()}\n</head>\n<body>\n{defs}\n{hdr}\n<main id="top">\n{main}\n</main>\n{ftr}\n{script}\n{js}\n</body>\n</html>\n'
    doc=re.sub(r'@@(\w+)@@',lambda m: PAGES[m.group(1)][0],doc)
    assert '@@' not in doc, key
    return fn,doc
os.makedirs(OUT,exist_ok=True)
for k in PAGES:
    fn,doc=build(k)
    open(os.path.join(OUT,fn),'w',encoding='utf-8').write(doc)
if os.path.isdir(os.path.join(OUT,'img')): shutil.rmtree(os.path.join(OUT,'img'))
shutil.copytree(os.path.join(ROOT,'img'),os.path.join(OUT,'img'))
print('built',len(PAGES),'pages ->',OUT)
