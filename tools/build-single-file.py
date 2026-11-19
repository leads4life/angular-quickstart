#!/usr/bin/env python3
"""Inline the preview build (ng build -c preview) into ONE self-contained HTML file.

Usage: python3 tools/build-single-file.py dist/preview golden-wok-preview.html
Scripts, styles, fonts (woff2) and every image become inline / base64, so the
file opens from disk or as a hosted artifact. Forms can't submit from it.
"""
import base64, mimetypes, pathlib, re, sys

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
html = (src / 'index.html').read_text()

def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or ('font/woff2' if path.suffix == '.woff2' else 'application/octet-stream')
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()

def inline_assets(text: str) -> str:
    # images referenced as assets/... in JS/HTML
    return re.sub(r'assets/img/[\w.-]+\.(?:jpg|png|svg)', lambda m: data_uri(src / m.group(0)), text)

# stylesheet: keep woff2 only, inline fonts
css_name = re.search(r'<link rel="stylesheet" href="([^"]+\.css)"', html).group(1)
css = (src / css_name).read_text()
css = re.sub(r',\s*url\([^)]+\.woff\)\s*format\("woff"\)', '', css)
css = re.sub(r'url\(([^)"\']+\.woff2)\)', lambda m: f'url({data_uri(src / m.group(1))})', css)
html = re.sub(r'<link rel="stylesheet" href="[^"]+\.css"[^>]*>', lambda m: f'<style>{css}</style>', html, count=1)
html = re.sub(r'<noscript><link rel="stylesheet"[^<]*</noscript>', '', html)
html = re.sub(r'<link rel="icon"[^>]*>', '', html)
html = html.replace('<base href="/">', '')

def script(m):
    js = inline_assets((src / m.group(1)).read_text()).replace('</script', '<\\/script')
    return f'<script type="module">{js}</script>'
html = re.sub(r'<script src="([^"]+\.js)" type="module"></script>', script, html)
out.write_text(html)
print(out, f'{out.stat().st_size / 1e6:.2f} MB')
