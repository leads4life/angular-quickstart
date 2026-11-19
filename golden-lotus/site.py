#!/usr/bin/env python3
"""Restaurant site builder. All business facts come from restaurant.json (or the file given as 2nd arg).
   python3 site.py [outdir] [restaurant.json]"""
import re, sys, os, shutil, json, html as H
ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'dist')
CFG=json.load(open(sys.argv[2] if len(sys.argv)>2 else os.path.join(ROOT,'restaurant.json'),encoding='utf-8'))
ORDER_URL=CFG.get('order_url','')   # empty = "Order Online" buttons go to Takeout > How to order
DEMO=CFG.get('demo',{}).get('enabled',False)
DAYN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
def t12(hm):
    h,m=map(int,hm.split(':')); return f"{(h-1)%12+1}:{m:02d} {'AM' if h<12 else 'PM'}"
def row(days,label,o,c): return f'<tr data-days="{" ".join(map(str,days))}" data-open="{o}" data-close="{c}"><th scope="row">{label}</th><td>{t12(o)} – {t12(c)}</td></tr>'
HRS=CFG['hours']
byday={d:h for h in HRS for d in h['days']}
FACTS={
 'NAME':CFG['name'],'NAME_UPPER':CFG['name_upper'],'NAME_ZH':CFG['name_zh'],'NAME_PY':CFG['name_pinyin'],
 'SEAL':''.join(f'<span>{c}</span>' for c in CFG['name_zh']),
 'STREET':CFG['street'],'CITY':CFG['city'],'CITYLINE':f"{CFG['city']}, {CFG['region']} {CFG['postal']}",
 'PHONE':CFG['phone'],'TEL':CFG['tel'],'TZ':CFG['timezone'],
 'MAPS_URL':'https://www.google.com/maps/search/?api=1&amp;query='+'+'.join((CFG['street']+' '+CFG['city']+' '+CFG['region']+' '+CFG['postal']).replace('.','').split()),
 'HOURS_MINI':''.join(row(h['days'],h['label'],h['open'],h['close']) for h in HRS),
 'HOURS_FULL':''.join(row([d],DAYN[d],byday[d]['open'],byday[d]['close']) if d in byday else f'<tr><th scope="row">{DAYN[d]}</th><td>Closed</td></tr>' for d in [1,2,3,4,5,6,0]),
 'HOURS_LINES':'<br>'.join(f"{h['label']} {t12(h['open'])} – {t12(h['close'])}" for h in HRS),
}
def fill(s):
    s=re.sub(r'%%(\w+)%%',lambda m: FACTS.get(m.group(1),m.group(0)),s)
    return s
ZH_EYEBROW={'menu':'菜單','takeout':'外賣','events':'宴會','about':'關於我們','contact':'聯絡我們','privacy':'隱私政策','accessibility':'無障礙'}
PAGES={ # key: (filename, body_file, title)
 'home':('index.html',None,'%%NAME%% Chinese Restaurant | %%CITYLINE%%'),
 'menu':('menu.html','pages/menu.html','Menu | %%NAME%% Chinese Restaurant'),
 'takeout':('takeout-delivery.html','pages/takeout.html','Takeout & Delivery | %%NAME%%'),
 'events':('private-events.html','pages/events.html','Private Events | %%NAME%%'),
 'about':('about.html','pages/about.html','About | %%NAME%%'),
 'contact':('contact.html','pages/contact.html','Contact & Hours | %%NAME%%'),
 'privacy':('privacy.html','pages/privacy.html','Privacy Policy | %%NAME%%'),
 'accessibility':('accessibility.html','pages/accessibility.html','Accessibility | %%NAME%%'),
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
LD=json.dumps({'@context':'https://schema.org','@type':'Restaurant','name':CFG['name']+' '+CFG['cuisine_label'],'servesCuisine':'Chinese','telephone':CFG['tel'],'address':{'@type':'PostalAddress','streetAddress':CFG['street'],'addressLocality':CFG['city'],'addressRegion':CFG['region'],'postalCode':CFG['postal'],'addressCountry':'US'},'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':[DAYN[d] for d in h['days']],'opens':h['open'],'closes':h['close']} for h in HRS]},ensure_ascii=False)
if DEMO:   # a fictional demo must not look like a real business to search engines
    head=head.replace('<!--JSONLD-->','<meta name="robots" content="noindex, nofollow">')
    D=CFG['demo']
    DEMOBAR=f'''<div class="demo-bar" role="note"><span class="db-seal" aria-hidden="true">印</span><span class="db-txt"><b>Demo restaurant</b><span class="db-long"> by {H.escape(D['studio'])} · {H.escape(D['note'])}</span></span><a class="db-cta" href="{D['studio_url']}">Want a site like this? <svg class="ico" aria-hidden="true"><use href="#i-chev"/></svg></a></div>'''
    head=head.replace('</style>','''</style>
<style>
body.demo{--hh:65px}
.demo-bar{position:relative;z-index:60;display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;padding:7px 16px;background:linear-gradient(90deg,#f3e6c8,#fbf3e2 50%,#f3e6c8);color:#2a1a14;font:500 14px/1.3 var(--f-body);text-align:center;border-bottom:1px solid #c9a65e}
.db-seal{display:inline-grid;place-items:center;width:22px;height:22px;background:#b0141c;color:#fbeedd;font:700 13px/1 var(--f-cjk);border-radius:2px}
.db-cta{font-weight:600;color:#8c0e14;text-decoration:none;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
.db-cta:hover{text-decoration:underline}
.db-cta .ico{font-size:12px}
@media (max-width:700px){.db-long{display:none}.demo-bar{font-size:13px;gap:10px}}
</style>''',1)
else:
    DEMOBAR=''
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
    if key in ZH_EYEBROW: main=main.replace('<p class="eyebrow">',f'<p class="eyebrow"><span class="zh-e" lang="zh-Hant">{ZH_EYEBROW[key]}</span>',1)
    hdr,ftr=header,footer
    hdr=hdr.replace(f'href="@@{key}@@"',f'href="@@{key}@@" aria-current="page"')
    ftr=ftr.replace(f'href="@@{key}@@"',f'href="@@{key}@@" aria-current="page"')
    doc=f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>{esc(fill(title))}</title>\n{head.strip()}\n</head>\n<body{' class="demo"' if DEMO else ''}>\n{defs}\n{DEMOBAR}\n{hdr}\n<main id="top">\n{main}\n</main>\n{ftr}\n{script}\n{js}\n</body>\n</html>\n'
    doc=doc.replace('@@order@@',ORDER_URL or '@@takeout@@#order')
    doc=re.sub(r'@@(\w+)@@',lambda m: PAGES[m.group(1)][0],doc)
    assert '@@' not in doc, key
    doc=fill(doc)
    left=set(re.findall(r'%%(?!CJK)\w+%%',doc)); assert not left, (key,left)
    return fn,doc
os.makedirs(OUT,exist_ok=True)
import urllib.parse
docs=[build(k) for k in PAGES]
cjk=''.join(sorted({c for _,d in docs for c in d if '\u2e80'<=c<='\u9fff' or '\uf900'<=c<='\ufaff' or c in '・《》（）'}))
for fn,doc in docs:
    open(os.path.join(OUT,fn),'w',encoding='utf-8').write(doc.replace('%%CJK%%',urllib.parse.quote(cjk)))
print('CJK subset:',len(cjk),'characters')
if os.path.isdir(os.path.join(OUT,'img')): shutil.rmtree(os.path.join(OUT,'img'))
shutil.copytree(os.path.join(ROOT,'img'),os.path.join(OUT,'img'))
print('built',len(PAGES),'pages ->',OUT)
