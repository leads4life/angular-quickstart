#!/usr/bin/env python3
"""Photo tools for rebuilding photography from a mockup image (no asset pack).
  python3 crop_tools.py grid mockup.png outdir/            -> gridded views in 3 bands (25px lines, labels every 50px) to measure boxes
  python3 crop_tools.py clean mockup.png clean.png '[[x0,y0,x1,y1],...]' '[[fill boxes]]'
        -> removes baked-in text: light/gold text masked by HSV inside text boxes, fill boxes (buttons/pills) fully masked,
           dilate 7px, cv2.inpaint TELEA, then a blurred blend so smears read as bokeh
  python3 crop_tools.py crop clean.png img/name.jpg x0 y0 x1 y1   -> crop, 2x Lanczos + unsharp, progressive JPEG q86
  python3 crop_tools.py cutout mockup.png img/name.png x0 y0 x1 y1 hue_lo hue_hi
        -> transparent PNG of a decoration (e.g. gold bamboo) keyed by hue + saturation
  python3 crop_tools.py trim in.jpg out.jpg                       -> trims white export borders from asset-pack images
Always run from the untouched original (save mockup_orig.png first); never stack fixes on a processed copy."""
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
def grid(src, out):
    im = Image.open(src).convert('RGB'); W, H = im.size; step = H // 3 + 20
    for i, a in enumerate(range(0, H, step - 20)):
        c = im.crop((0, a, W, min(H, a + step))).copy(); d = ImageDraw.Draw(c)
        for x in range(0, W, 25): d.line([(x, 0), (x, c.height)], fill=(0, 255, 255) if x % 50 == 0 else (0, 110, 110))
        for y in range(a - a % 25, a + c.height, 25):
            if y >= a: d.line([(0, y - a), (W, y - a)], fill=(0, 255, 255) if y % 50 == 0 else (0, 110, 110)); y % 50 == 0 and d.text((2, y - a + 1), str(y), fill=(255, 255, 0))
        for x in range(0, W, 50): d.text((x + 2, 2), str(x), fill=(255, 255, 0))
        c.save(f'{out}/grid{i}.png')
def clean(src, dst, boxes, fills):
    img = cv2.imread(src); hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); mask = np.zeros(img.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes: sub = hsv[y0:y1, x0:x1]; mask[y0:y1, x0:x1] |= (((sub[..., 2] > 150) & (sub[..., 1] < 170)) * 255).astype(np.uint8)
    for x0, y0, x1, y1 in fills: mask[y0:y1, x0:x1] = 255
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8)); out = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
    blur = cv2.GaussianBlur(out, (0, 0), 14); bm = np.clip(cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 10)[..., None] * 1.4, 0, 1)
    cv2.imwrite(dst, (out * (1 - bm) + blur * bm).astype(np.uint8))
def crop(src, dst, x0, y0, x1, y1):
    c = Image.open(src).convert('RGB').crop((x0, y0, x1, y1)); c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 3))
    c.save(dst, quality=86, optimize=True, progressive=True)
def cutout(src, dst, x0, y0, x1, y1, hlo=8, hhi=32):
    im = cv2.imread(src)[y0:y1, x0:x1]; hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(float)
    a = np.clip((hsv[..., 2] - 55) / 90, 0, 1) * ((hsv[..., 0] > hlo) & (hsv[..., 0] < hhi) & (hsv[..., 1] > 70))
    a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), .6); rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    I = Image.fromarray(np.dstack([rgb, (a * 255).astype(np.uint8)]), 'RGBA'); I.resize((I.width * 2, I.height * 2), Image.LANCZOS).save(dst, optimize=True)
def trim(src, dst):
    im = Image.open(src).convert('RGB'); a = np.asarray(im.convert('L')).astype(float); bad = lambda v: v.mean() > 232 and v.std() < 14
    t, b, l, r = 0, a.shape[0], 0, a.shape[1]
    while t < b - 10 and bad(a[t, l:r]): t += 1
    while b > t + 10 and bad(a[b - 1, l:r]): b -= 1
    while l < r - 10 and bad(a[t:b, l]): l += 1
    while r > l + 10 and bad(a[t:b, r - 1]): r -= 1
    im.crop((l + 2, t + 2, r - 2, b - 2)).save(dst, quality=86, optimize=True, progressive=True)
if __name__ == '__main__':
    cmd, *a = sys.argv[1:]
    if cmd == 'grid': grid(*a)
    elif cmd == 'clean': clean(a[0], a[1], json.loads(a[2]), json.loads(a[3]) if len(a) > 3 else [])
    elif cmd == 'crop': crop(a[0], a[1], *map(int, a[2:6]))
    elif cmd == 'cutout': cutout(a[0], a[1], *map(int, a[2:8]))
    elif cmd == 'trim': trim(*a)
