#!/usr/bin/env python3
"""Photo slot report for a built site.
   python3 photo_slots.py dist/ [--md PHOTOGRAPHY.md]
Lists every image file, where it is used (page + nearest heading + whether it is a CSS background or an <img>),
its pixel size, and flags files that fill more than one slot. Each slot should own its own file
(e.g. hero-menu.jpg, about-story.jpg) so a replacement photo only has to be saved under the right name.
With --md it writes a PHOTOGRAPHY.md skeleton (slot map); add the prompts yourself."""
import re, os, sys, glob, html
from collections import defaultdict
from PIL import Image
D = sys.argv[1]; MD = sys.argv[sys.argv.index('--md') + 1] if '--md' in sys.argv else None
uses = defaultdict(list)
for f in sorted(glob.glob(os.path.join(D, '**', '*.html'), recursive=True)):
    s = open(f, encoding='utf-8').read(); page = os.path.relpath(f, D)
    styles = [(m.start(), m.end()) for m in re.finditer(r'<style[^>]*>.*?</style>', s, re.S)]
    for m in re.finditer(r'''(?:src="|url\(['"]?)((?:\.\./)*img/([^"')\s]+))''', s):
        if any(a <= m.start() < b for a, b in styles):          # stylesheet rule: report its selector once, not per page
            sel = s[:m.start()].rsplit('}', 1)[-1].split('{')[0].strip()[:60]
            uses[m.group(2)].append(('stylesheet', 'css', sel)); continue
        kind = 'img' if m.group(0).startswith('src=') else 'inline-bg'
        before = s[:m.start()]
        if kind == 'inline-bg':                                  # inline hero background: name it by the next heading
            nxt = re.search(r'<h[1-3][^>]*>(.*?)</h[1-3]>', s[m.end():], re.S)
            heading = 'hero: ' + ' '.join(html.unescape(re.sub('<[^>]+>', ' ', nxt.group(1))).split()[:6]) if nxt else '(hero)'
        else:
            hs = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', before + s[m.end():m.end() + 3000], re.S)
            near = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', s[m.end():m.end() + 3000], re.S)
            pick = near[0] if near else (hs[-1] if hs else '(top of page)')
            heading = ' '.join(html.unescape(re.sub('<[^>]+>', ' ', pick)).split()[:7])
        uses[m.group(2)].append((page, kind, heading))
rows = []
for name in sorted(os.listdir(os.path.join(D, 'img'))):
    p = os.path.join(D, 'img', name)
    try: w, h = Image.open(p).size
    except Exception: w = h = 0
    u = sorted(set(uses.get(name, [])))
    slots = sorted({(pg, hd) for pg, k, hd in u})
    flag = 'SHARED by %d slots' % len(slots) if len(slots) > 1 else ('UNUSED' if not u else 'ok')
    rows.append((name, w, h, flag, u))
    print(f'{name:32} {w}x{h:<6} {flag}', flush=True)
    for pg, k, hd in u: print(f'    {pg:28} {k:10} {hd}')
if MD:
    out = ['# Photography Replacement Guide', '', 'Each photo position has its own file. Save the replacement with the exact file name and send it back; nothing else changes.', '',
           '| File name | Where it appears | Current size | Ask for | Keep clear |', '|---|---|---|---|---|']
    for name, w, h, flag, u in rows:
        where = '; '.join(sorted({f'{pg} – {hd}' for pg, k, hd in u})) or '(unused)'
        out.append(f'| `{name}` | {where} | {w}×{h} | TODO | TODO |')
    out += ['', '## Style brief to paste into ChatGPT first', '', '```', 'TODO: brand, cuisine/trade, light, palette, cultural do/don\'t list, no text/logos/watermarks', '```', '', '## One prompt per file', '', 'TODO']
    open(MD, 'w').write('\n'.join(out) + '\n'); print('wrote', MD)
