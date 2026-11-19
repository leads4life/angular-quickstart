#!/usr/bin/env python3
"""Seam and shape generator. Writes a CSS file of custom properties (data-URI SVGs) you then use in the site CSS.
   python3 deco.py --motifs chinese --gold "#d8b468" --out seams.css
Variables written:
  --rule      double gilt rule broken by small industry glyphs (section-to-section seams)   tile W x 18
  --rule-sm   lighter version (header underline, footer dividers)                           tile W x 14
  --shape-a   arched-window mask (feature photos)   --shape-b / --shape-c  soft squircles (cycle a/b/c per page)
  --fret      very quiet repeating background tile for the motif world (key-fret for Chinese, etc.)
Add a motif set by adding glyphs to GLYPHS (10x10 boxes, filled with the gold colour)."""
import re, math, random, argparse, urllib.parse
uri = lambda s: 'url("data:image/svg+xml,' + urllib.parse.quote(re.sub(r"\s+", " ", s).strip(), safe=" =:/,.-") + '")'
GLYPHS = {
 'chinese': {   # lotus, square-holed coin, auspicious cloud, endless knot
   'lotus': '<path d="M5,1.2C6.6,3 6.6,5.6 5,7.6C3.4,5.6 3.4,3 5,1.2Z"/><path d="M5,7.8C3.4,7.2 1.4,5.6 1,3.6C2.8,4 4.2,5.6 5,7.8Z"/><path d="M5,7.8C6.6,7.2 8.6,5.6 9,3.6C7.2,4 5.8,5.6 5,7.8Z"/>',
   'coin': '<path fill-rule="evenodd" d="M5,.6A4.4,4.4 0 1 1 4.99,.6ZM3.7,3.7H6.3V6.3H3.7Z"/>',
   'cloud': '<path d="M1,7.2C.4,5.6 1.6,4.2 3,4.6C3.2,2.6 5.6,1.8 6.8,3.4C8.4,3 9.6,4.6 8.8,6C9.6,6.6 9.2,7.8 8.2,7.8H2C1.6,7.8 1.2,7.6 1,7.2Z"/>',
   'knot': '<path d="M5,.8L9.2,5L5,9.2L.8,5Z" fill="none" stroke="currentColor" stroke-width="1"/><path d="M5,3.2L6.8,5L5,6.8L3.2,5Z"/>'},
 'cards': {     # magician / casino / game night
   'spade': '<path d="M5,0C5,0 .5,3.6 .5,5.6C.5,7.2 1.8,8.1 3,8.1C3.7,8.1 4.3,7.8 4.6,7.3L3.9,9.6H6.1L5.4,7.3C5.7,7.8 6.3,8.1 7,8.1C8.2,8.1 9.5,7.2 9.5,5.6C9.5,3.6 5,0 5,0Z"/>',
   'heart': '<path d="M5,9.2C5,9.2 .5,6 .5,3.1C.5,1.4 1.7,.3 3,.3C4,.3 4.7,.9 5,1.7C5.3,.9 6,.3 7,.3C8.3,.3 9.5,1.4 9.5,3.1C9.5,6 5,9.2 5,9.2Z"/>',
   'club': '<circle cx="5" cy="2.4" r="2.1"/><circle cx="2.7" cy="5.5" r="2.1"/><circle cx="7.3" cy="5.5" r="2.1"/><path d="M4.1,9.6L4.6,5.6H5.4L5.9,9.6Z"/>',
   'diamond': '<path d="M5,0L8.5,4.8L5,9.6L1.5,4.8Z"/>'},
 'botanical': { # florist, bakery (wheat), tea, spa
   'leaf': '<path d="M1,9C1,4 4,1 9,1C9,6 6,9 1,9Z"/>',
   'wheat': '<path d="M5,9.6V3" stroke="currentColor" stroke-width=".8" fill="none"/><ellipse cx="5" cy="2" rx="1" ry="1.8"/><ellipse cx="3.6" cy="4.6" rx=".9" ry="1.6" transform="rotate(-30 3.6 4.6)"/><ellipse cx="6.4" cy="4.6" rx=".9" ry="1.6" transform="rotate(30 6.4 4.6)"/>',
   'dot': '<circle cx="5" cy="5" r="1.6"/>',
   'bud': '<path d="M5,1C7,3 7,6 5,8C3,6 3,3 5,1Z"/>'},
}
TILES = {
 'chinese': '<path d="M2 26V2H26V22H6V6H22V18H10V10H18V14H14" fill="none" stroke="{c}" stroke-width="1.1" stroke-opacity=".07" stroke-linecap="square"/>',   # 回紋 key-fret
 'cards': '<path d="M14 4L18 14L14 24L10 14Z" fill="{c}" fill-opacity=".05"/>',
 'botanical': '<circle cx="14" cy="14" r="1.4" fill="{c}" fill-opacity=".08"/>',
}
def rule(glyphs, order, gold, cell=72, H=18, s=1.15, gap=12, alpha=.6):
    W = cell * len(order); out = []
    for i, k in enumerate(order):
        x0, cx = i * cell, i * cell + cell / 2
        out += [f'<path d="M{x0},{y:.2f} H{cx-gap} M{cx+gap},{y:.2f} H{x0+cell}" stroke="{gold}" stroke-width=".9" opacity="{alpha}"/>' for y in (H/2 - 1.7, H/2 + 1.7)]
        out.append(f'<g transform="translate({cx-5*s:.2f},{H/2-5*s:.2f}) scale({s})" fill="{gold}" color="{gold}" opacity="{min(1, alpha+.3):.2f}">{glyphs[k]}</g>')
    return uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(out)}</svg>'), W, H
def blob(seed, n=12, exp=4.6, wob=.016):
    r = random.Random(seed); pts = []
    for i in range(n):
        t = 2 * math.pi * i / n + r.uniform(-.08, .08); c, s = math.cos(t), math.sin(t)
        x, y = math.copysign(abs(c) ** (2 / exp), c), math.copysign(abs(s) ** (2 / exp), s); k = 1 - wob * r.random()
        pts.append((50 + 49.2 * x * k, 50 + 49.2 * y * k))
    d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f} "
    for i in range(n):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[(i+1) % n], pts[(i+2) % n]
        d += f"C{p1[0]+(p2[0]-p0[0])/6:.2f},{p1[1]+(p2[1]-p0[1])/6:.2f} {p2[0]-(p3[0]-p1[0])/6:.2f},{p2[1]-(p3[1]-p1[1])/6:.2f} {p2[0]:.2f},{p2[1]:.2f} "
    return uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="{d}Z"/></svg>')
def arch():
    d = "M1.2,96C1.2,98.4 2.4,99 4.5,99H95.5C97.6,99 98.8,98.4 98.8,96V30C98.8,12 76,1 50,1C24,1 1.2,12 1.2,30Z"
    return uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="{d}"/></svg>')
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--motifs', default='chinese', choices=GLYPHS); ap.add_argument('--gold', default='#d8b468'); ap.add_argument('--out', default='seams.css')
    a = ap.parse_args(); g = GLYPHS[a.motifs]; keys = list(g)
    r1, W1, H1 = rule(g, [keys[0], keys[1], keys[2], keys[1]], a.gold)
    r2, W2, H2 = rule(g, [keys[3], keys[2], keys[3], keys[0]], a.gold, cell=60, H=14, s=.9, gap=10, alpha=.42)
    fret = uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28">{TILES[a.motifs].format(c=a.gold)}</svg>')
    css = f''':root{{--rule:{r1};--rule-sm:{r2};--shape-a:{arch()};--shape-b:{blob(4)};--shape-c:{blob(27)};--fret:{fret};
  --rule-w:{W1}px;--rule-h:{H1}px;--rule-sm-w:{W2}px;--rule-sm-h:{H2}px}}
/* section-to-section seam */
.sec{{position:relative;overflow-x:clip;overflow-y:visible}}
.sec+.sec::before{{content:"";position:absolute;left:-10px;right:-10px;top:calc(var(--rule-h)/-2);height:var(--rule-h);z-index:3;pointer-events:none;background:var(--rule) 0 0/var(--rule-w) var(--rule-h) round;filter:drop-shadow(0 1px 2px rgba(0,0,0,.6))}}
/* shaped feature photos: <figure class="frame"><div class="blob" data-shape="a|b|c"><img></div></figure> */
.blob{{filter:drop-shadow(0 0 1.2px {a.gold}) drop-shadow(0 18px 26px rgba(0,0,0,.45))}}
.blob img{{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;-webkit-mask:var(--shape-a) center/100% 100% no-repeat;mask:var(--shape-a) center/100% 100% no-repeat}}
.blob[data-shape="b"] img{{-webkit-mask-image:var(--shape-b);mask-image:var(--shape-b)}}
.blob[data-shape="c"] img{{-webkit-mask-image:var(--shape-c);mask-image:var(--shape-c)}}
'''
    open(a.out, 'w').write(css); print('wrote', a.out, len(css), 'bytes')
