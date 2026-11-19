#!/usr/bin/env python3
"""Build the studio showcase:  python3 build.py
   dist/index.html                 sales page (from sales.html + studio.json)
   dist/demo/golden-lotus/         the demo restaurant (from ../golden-lotus with restaurant.json, demo mode on)
   dist/assets/                    screenshots of the demo taken fresh on every build"""
import json, os, re, subprocess, sys, urllib.parse, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DIST = os.path.join(HERE, 'dist'); DEMO = os.path.join(DIST, 'demo', 'golden-lotus'); ASSETS = os.path.join(DIST, 'assets')
SKILL = os.path.join(ROOT, 'skills', 'website-polish-pro', 'scripts')
S = json.load(open(os.path.join(HERE, 'studio.json'), encoding='utf-8'))
os.makedirs(ASSETS, exist_ok=True)
if os.path.isdir(DEMO): shutil.rmtree(DEMO)
subprocess.run([sys.executable, os.path.join(ROOT, 'golden-lotus', 'site.py'), DEMO], check=True)
subprocess.run(['node', os.path.join(HERE, 'shoot.js'), DEMO, ASSETS], check=True)
# seams: the same gilt rule family as the demo, in a deeper gold for paper
tmp = os.path.join(HERE, '.seams.css')
subprocess.run([sys.executable, os.path.join(SKILL, 'deco.py'), '--motifs', 'chinese', '--gold', '#a8823c', '--out', tmp], check=True, stdout=subprocess.DEVNULL)
seams = open(tmp).read() + ':root{--fret-ink:var(--fret)}'; os.remove(tmp)
src = open(os.path.join(HERE, 'sales.html'), encoding='utf-8').read()
form = f'action="{html.escape(S["form_endpoint"])}" method="POST"' if S.get('form_endpoint') else 'data-demo-form'
contact = f'Contact: <a href="mailto:{html.escape(S["contact_email"])}">{html.escape(S["contact_email"])}</a>' if S.get('contact_email') else ''
T = {'STUDIO': html.escape(S['studio']), 'SEAL': S['seal'], 'TAGLINE': html.escape(S['tagline']), 'PRICE_STARTER': html.escape(S['price_starter']),
     'PRICE_STANDARD': html.escape(S['price_standard']), 'PRICE_PREMIUM': html.escape(S['price_premium']), 'FORM_ATTRS': form, 'CONTACT': contact, 'SEAMS': seams}
doc = re.sub(r'%%(\w+)%%', lambda m: T.get(m.group(1), m.group(0)), src)
cjk = ''.join(sorted({c for c in doc if '⺀' <= c <= '鿿'}))
doc = doc.replace('%%CJK%%', urllib.parse.quote(cjk))
assert '%%' not in doc, re.findall(r'%%\w+%%', doc)
open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(doc)
print('showcase built ->', DIST)
