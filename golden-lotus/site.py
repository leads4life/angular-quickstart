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
head=head.replace('</style>','</style>\n<style>\n'+rd('pages.css')+rd('legal.css')+rd('seams.css')+'</style>')
WAVE=re.search(r'<!--WAVE-->(.*?)<!--/WAVE-->',T,re.S).group(1)
import json, itertools
LD=json.dumps({'@context':'https://schema.org','@type':'Restaurant','name':'Golden Lotus Chinese Restaurant','servesCuisine':'Chinese','telephone':'+1-561-555-2688','address':{'@type':'PostalAddress','streetAddress':'1236 Wellington Green Dr.','addressLocality':'Wellington','addressRegion':'FL','postalCode':'33414','addressCountry':'US'},'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':d,'opens':o,'closes':c} for d,o,c in ((['Monday','Tuesday','Wednesday','Thursday'],'11:00','21:30'),(['Friday','Saturday'],'11:00','22:00'),(['Sunday'],'12:00','21:00'))]},ensure_ascii=False)
head=head.replace('<!--JSONLD-->','<script type="application/ld+json">'+LD+'</script>')
defs,header,home,footer,script=(block(n) for n in ('DEFS','HEADER','HOME','FOOTER','SCRIPT'))
home=home.replace('<!--WAVE-->','').replace('<!--/WAVE-->','')
ORDER=list(PAGES)
def shapes(html,key):
    cyc=itertools.islice(itertools.cycle('abc'),ORDER.index(key),None)
    return re.sub(r'<figure class="frame">(<img[^>]*>)',lambda m:f'<figure class="frame"><div class="blob" data-shape="{next(cyc)}">{m.group(1)}</div>',html)
def hero_wave(html):
    i=html.find('</section>'); assert 'page-hero' in html[:i]
    return html[:i]+WAVE+'\n'+html[i:]
band=rd('pages/_band.html')
js='<script>\n'+rd('pages.js')+'</script>'
def include(s):
    return re.sub(r'<!--@include (\S+)-->',lambda m: rd(m.group(1)),s)
def esc(s): return s.replace('&','&amp;')
def build(key):
    fn,body,title=PAGES[key]
    main=home if body is None else shapes(hero_wave(include(rd(body))),key)+'\n'+band
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
