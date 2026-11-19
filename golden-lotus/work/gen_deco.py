import re, urllib.parse, math, random
GOLD="#d8b468"; GOLD_DK="#7a5a26"; RED="#b0141c"
uri=lambda s:'url("data:image/svg+xml,'+urllib.parse.quote(re.sub(r"\s+"," ",s).strip(),safe=" =:/,.-")+'")'
G={ # 10x10 boxes, Chinese motifs
 "lotus":'<path d="M5,1.2C6.6,3 6.6,5.6 5,7.6C3.4,5.6 3.4,3 5,1.2Z"/><path d="M5,7.8C3.4,7.2 1.4,5.6 1,3.6C2.8,4 4.2,5.6 5,7.8Z"/><path d="M5,7.8C6.6,7.2 8.6,5.6 9,3.6C7.2,4 5.8,5.6 5,7.8Z"/><path d="M2,8.8H8" stroke="%s" stroke-width=".7" fill="none"/>'%GOLD,
 "coin":'<path fill-rule="evenodd" d="M5,.6A4.4,4.4 0 1 1 4.99,.6ZM3.7,3.7H6.3V6.3H3.7Z"/>',
 "cloud":'<path d="M1,7.2C.4,5.6 1.6,4.2 3,4.6C3.2,2.6 5.6,1.8 6.8,3.4C8.4,3 9.6,4.6 8.8,6C9.6,6.6 9.2,7.8 8.2,7.8H2C1.6,7.8 1.2,7.6 1,7.2Z"/>',
 "knot":'<path d="M5,.8L9.2,5L5,9.2L.8,5Z" fill="none" stroke="%s" stroke-width="1"/><path d="M5,3.2L6.8,5L5,6.8L3.2,5Z"/>'%GOLD,
}
def rule(order=("lotus","coin","cloud","coin"),cell=72,H=18,s=1.15,gap=12,alpha=.6,dbl=True):
    W=cell*len(order); out=[]
    ys=(H/2-1.7,H/2+1.7) if dbl else (H/2,)
    for i,k in enumerate(order):
        x0,cx=i*cell,i*cell+cell/2
        out+=[f'<path d="M{x0},{y:.2f} H{cx-gap} M{cx+gap},{y:.2f} H{x0+cell}" stroke="{GOLD}" stroke-width=".9" opacity="{alpha}"/>' for y in ys]
        out.append(f'<g transform="translate({cx-5*s:.2f},{H/2-5*s:.2f}) scale({s})" fill="{GOLD}" opacity="{min(1,alpha+.3):.2f}">{G[k]}</g>')
    return uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(out)}</svg>'),W,H
def blob(seed,n=12,exp=4.6,wob=.016):
    r=random.Random(seed);pts=[]
    for i in range(n):
        t=2*math.pi*i/n+r.uniform(-.08,.08);c,s=math.cos(t),math.sin(t)
        x,y=math.copysign(abs(c)**(2/exp),c),math.copysign(abs(s)**(2/exp),s);k=1-wob*r.random()
        pts.append((50+49.2*x*k,50+49.2*y*k))
    d=f"M{pts[0][0]:.2f},{pts[0][1]:.2f} "
    for i in range(n):
        p0,p1,p2,p3=pts[i-1],pts[i],pts[(i+1)%n],pts[(i+2)%n]
        d+=f"C{p1[0]+(p2[0]-p0[0])/6:.2f},{p1[1]+(p2[1]-p0[1])/6:.2f} {p2[0]-(p3[0]-p1[0])/6:.2f},{p2[1]-(p3[1]-p1[1])/6:.2f} {p2[0]:.2f},{p2[1]:.2f} "
    return uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="{d}Z"/></svg>')
def arch():
    # moon-gate style window: tall soft arch on top, gently rounded base corners (inside the room's own vocabulary)
    d="M1.2,96 C1.2,98.4 2.4,99 4.5,99 H95.5 C97.6,99 98.8,98.4 98.8,96 V30 C98.8,12 76,1 50,1 C24,1 1.2,12 1.2,30 Z"
    return uri(f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="{d}"/></svg>')
r1,W1,H1=rule()
r2,W2,H2=rule(order=("knot","cloud","knot","lotus"),cell=60,H=14,s=.9,gap=10,alpha=.42)
css=f""":root{{--rule:{r1};--rule-sm:{r2};--shape-a:{arch()};--shape-b:{blob(4)};--shape-c:{blob(27)}}}
"""
css+=f"""
/* ===== seams: three treatments from one world =====
   1. hero exit: the cream & gilt wave (same SVG as the home hero)
   2. section to section: double gilt rule broken by lotus, coin and cloud motifs
   3. arriving at the closing band / footer: gilt wave with the red-lacquer glow  */
.site-head{{border-bottom:0;overflow-x:clip;overflow-y:visible}}
.site-head::after{{content:"";position:absolute;left:-10px;right:-10px;bottom:-7px;height:{H2}px;pointer-events:none;background:var(--rule-sm) 0 0/{W2}px {H2}px round;opacity:.85}}
.sec{{position:relative;overflow-x:clip;overflow-y:visible}}
.sec+.sec::before,.page-hero+.sec.alt::before{{content:"";position:absolute;left:-10px;right:-10px;top:-{H1//2}px;height:{H1}px;z-index:3;pointer-events:none;background:var(--rule) 0 0/{W1}px {H1}px round;filter:drop-shadow(0 1px 2px rgba(0,0,0,.8))}}
.foot-nav{{border-top:0;position:relative}}
.foot-nav::before{{content:"";position:absolute;left:0;right:0;top:-{H2//2}px;height:{H2}px;background:var(--rule-sm) 0 0/{W2}px {H2}px round}}
.foot-glow{{border-top:0;position:relative}}
.foot-glow::before{{content:"";position:absolute;left:-10px;right:-10px;top:-{H2//2}px;height:{H2}px;background:var(--rule-sm) 0 0/{W2}px {H2}px round}}
.site-foot{{overflow-x:clip}}
"""
open('seams.css','w').write(css)
print(len(css))
top='<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="60" viewBox="0 0 1440 60" preserveAspectRatio="none"><path d="M0 34C260 8 520 6 780 30C1040 54 1250 50 1440 22V60H0Z"/></svg>'
stroke='<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="60" viewBox="0 0 1440 60" preserveAspectRatio="none"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#9c7535"/><stop offset=".45" stop-color="#f3d991"/><stop offset="1" stop-color="#b48a41"/></linearGradient></defs><path d="M0 36C260 10 520 8 780 32C1040 56 1250 52 1440 24" fill="none" stroke="url(#g)" stroke-width="3.5" vector-effect="non-scaling-stroke"/></svg>'
open('seams.css','a').write(f":root{{--band-top:{uri(top)};--band-stroke:{uri(stroke)}}}\n")
# 回紋 key-fret field (Chinese meander), very quiet
fret='<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28"><path d="M2 26V2H26V22H6V6H22V18H10V10H18V14H14" fill="none" stroke="#d8b468" stroke-width="1.1" stroke-opacity=".07" stroke-linecap="square"/></svg>'
open('seams.css','a').write(f":root{{--fret:{uri(fret)}}}\n")
