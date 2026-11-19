#!/usr/bin/env python3
"""Static check of a built site folder: every <a href> resolves to a real file (and #anchor id),
every img/ asset exists, no duplicate ids, no leftover build tokens.  python3 check_links.py dist/"""
import re, os, sys, glob
D = sys.argv[1] if len(sys.argv) > 1 else 'dist'
files = glob.glob(os.path.join(D, '**', '*.html'), recursive=True)
ids = {os.path.relpath(f, D): set(re.findall(r'\sid="([^"]+)"', open(f, encoding='utf-8').read())) for f in files}
bad = []
for f in files:
    s = open(f, encoding='utf-8').read(); rel = os.path.relpath(f, D); here = os.path.dirname(rel)
    for h in re.findall(r'<a\b[^>]*\shref="([^"]+)"', s):
        if h.startswith(('http:', 'https:', 'tel:', 'mailto:', 'sms:')): continue
        p, _, a = h.partition('#')
        tgt = os.path.normpath(os.path.join(here, p)) if p else rel
        if p.endswith('/') or (p and not os.path.splitext(p)[1]): bad.append((rel, h, 'links to a folder; use the .html file so it works from disk')); continue
        if tgt not in ids: bad.append((rel, h, 'missing page')); continue
        if a and a not in ids[tgt]: bad.append((rel, h, 'missing anchor'))
    for i in set(re.findall(r'''(?:src="|url\(['"]?)((?:\.\./)*img/[^"')\s]+)''', s)):
        if not os.path.exists(os.path.normpath(os.path.join(D, here, i))): bad.append((rel, i, 'missing image'))
    al = re.findall(r'\sid="([^"]+)"', s); d = sorted({x for x in al if al.count(x) > 1})
    if d: bad.append((rel, ', '.join(d), 'duplicate ids'))
    for t in set(re.findall(r'@@\w+@@|%%\w+%%|\{\{\w+\}\}', s)): bad.append((rel, t, 'unresolved build token'))
for b in bad: print('BAD', *b)
print(f'{len(files)} pages checked, {len(bad)} problems'); sys.exit(1 if bad else 0)
