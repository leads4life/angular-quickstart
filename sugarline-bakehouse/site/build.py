#!/usr/bin/env python3
"""Sugarline Bakehouse static site builder: stamps the shared head, header, footer and script onto every page."""
import re, shutil, html, pathlib
ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "dist"

PAGES = {  # key: (output file, body file, title, description)
  "home":        ("index.html", "home.html", "Sugarline Bakehouse | Your cake, your story", "Celebration cakes, wedding cakes and cookie boxes, baked by hand in Maple Hollow."),
  "celebration": ("celebration-cakes.html", "celebration.html", "Celebration Cakes | Sugarline Bakehouse", "Birthdays, showers and every reason in between: celebration cakes designed around your story."),
  "weddings":    ("weddings.html", "weddings.html", "Wedding Cakes | Sugarline Bakehouse", "Tiered wedding cakes, designed with you over a tasting."),
  "cookies":     ("cookies.html", "cookies.html", "Cookies & Boxes | Sugarline Bakehouse", "Decorated cookies, boxed to give or to match your cake."),
  "about":       ("about.html", "about.html", "About | Sugarline Bakehouse", "A small bakery in Maple Hollow where every cake starts with a conversation."),
  "order":       ("order.html", "order.html", "Order a Cake | Sugarline Bakehouse", "Tell us your story and we'll reply with a design and a quote."),
  "404":         ("404.html", "404.html", "Page not found | Sugarline Bakehouse", "This page is still in the oven."),
}

T = (SRC / "template.html").read_text()
def part(name): return re.search(rf"<!--{name}-->\n(.*?)<!--/{name}-->", T, re.S).group(1)
HEAD, SPRITE, HEADER, FOOTER, SCRIPT = (part(n) for n in ("HEAD", "SPRITE", "HEADER", "FOOTER", "SCRIPT"))

_n = [0]
def sticker(text, cls=""):
    _n[0] += 1; i = f"stk{_n[0]}"
    return (f'<div class="sticker {cls}" aria-hidden="true"><svg class="spin" viewBox="0 0 132 132"><defs><path id="{i}" d="M66 66m-48 0a48 48 0 1 1 96 0a48 48 0 1 1-96 0"/></defs>'
            f'<text><textPath href="#{i}" textLength="298" lengthAdjust="spacing">{text}</textPath></text></svg><svg class="heart"><use href="#i-heart"/></svg></div>')

def link(key):  # "celebration#design" -> "@@celebration@@#design"
    k, _, a = key.partition("#"); return f"@@{k}@@" + (f"#{a}" if a else "")

def pagehero(m):
    eb, a, b, sub, img, alt, c1, k1, c2, k2, stk = m.group(1).split("|")
    return f'''<section class="sec cream page-hero" aria-labelledby="h-top">
  <div class="sec-in hero-grid">
    <div class="card-paper hero-card">
      <span class="tape" aria-hidden="true"></span>
      <p class="eyebrow">{eb}</p>
      <h1 id="h-top"><span class="a">{a}</span> <span class="b">{b}</span></h1>
      <p class="hero-sub">{sub}</p>
      <div class="btn-row"><a class="btn" href="{link(k1)}">{c1} <svg aria-hidden="true"><use href="#i-arrow"/></svg></a><a class="link" href="{link(k2)}">{c2}</a></div>
    </div>
    <div class="ph-art">
      <div class="arch"><img src="img/{img}" alt="{alt}" width="1800" height="1013"></div>
      {sticker(stk)}
      <svg class="doodle gold d-swirl" aria-hidden="true"><use href="#d-swirl"/></svg>
    </div>
  </div>
</section>'''

def cta(m):
    h, p, lab, k = m.group(1).split("|")
    return f'''<section class="sec cream edge-torn final" data-ghost="celebrate" aria-labelledby="h-cta">
  <div class="sec-in">
    <div class="banner"><h2 id="h-cta">{h}</h2><p class="lead" style="margin:0 auto 24px">{p}</p><a class="btn" href="{link(k)}">{lab} <svg aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
  </div>
</section>'''

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    for d in ("img", "assets", "fonts"): shutil.copytree(SRC / d, OUT / d)
    files = {k: v[0] for k, v in PAGES.items()}
    for key, (fn, body, title, desc) in PAGES.items():
        _n[0] = 0
        b = (SRC / "pages" / body).read_text()
        b = re.sub(r"@@PAGEHERO:(.*?)@@", pagehero, b, flags=re.S)
        b = re.sub(r"@@CTA:(.*?)@@", cta, b, flags=re.S)
        b = re.sub(r"@@STICKER:([^|@]*)\|([^@]*)@@", lambda m: sticker(m.group(1), m.group(2)), b)
        hd, ft = HEADER, FOOTER
        hd = hd.replace(f'href="@@{key}@@"', f'href="@@{key}@@" aria-current="page"')
        ft = ft.replace(f'href="@@{key}@@"', f'href="@@{key}@@" aria-current="page"')
        head = HEAD.replace("@@TITLE@@", html.escape(title)).replace("@@DESC@@", html.escape(desc))
        doc = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n{head}</head>\n<body>\n{SPRITE}{hd}<main id="top">\n{b}\n</main>\n{ft}{SCRIPT}</body>\n</html>\n'
        doc = re.sub(r"@@(\w+)@@", lambda m: files[m.group(1)], doc)
        assert "@@" not in doc, (fn, re.findall(r"@@[^@]{0,30}", doc)[:3])
        (OUT / fn).write_text(doc)
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print("built", len(PAGES), "pages ->", OUT)

if __name__ == "__main__":
    build()
