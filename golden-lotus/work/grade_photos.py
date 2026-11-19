#!/usr/bin/env python3
"""Grade the owner's photos toward the site's lacquered night palette. Always runs from photo-originals/ (never stacks on processed copies).
   heroes:  darker + warmer + vignette (text sits on them)       inline: lighter touch       textures: untouched except a slight deepen"""
import numpy as np, os
from PIL import Image, ImageFilter
SRC, OUT = 'photo-originals', 'img'
HEROES = ['home-hero','hero-menu','hero-takeout','hero-events','hero-about','hero-contact']
INLINE = ['home-signature','home-private-dining','events-room','about-story','about-name']
TEXTURE = ['hero-legal','texture-red-floral']
def grade(a, exposure, warm, sat, vig, contrast):
    a = a.astype(np.float32) / 255
    a = a ** (1 / exposure)                                   # exposure < 1 deepens midtones (gamma)
    a = 0.5 + (a - 0.5) * contrast
    lum = (a @ np.array([.2126, .7152, .0722]))[..., None]
    a = lum + (a - lum) * sat                                 # saturation
    a *= np.array([1 + warm, 1 + warm * .35, 1 - warm * .9])  # warm tungsten shift
    h, w = a.shape[:2]; y, x = np.ogrid[-1:1:h*1j, -1:1:w*1j]
    a *= (1 - vig * np.clip((x**2 * .8 + y**2) - .25, 0, 1))[..., None]   # soft vignette
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
for name in HEROES + INLINE + TEXTURE:
    im = np.asarray(Image.open(f'{SRC}/{name}.jpg').convert('RGB'))
    if name in HEROES:   g = grade(im, .80, .045, 1.04, .45, 1.08)
    elif name in INLINE: g = grade(im, .90, .03, 1.03, .30, 1.05)
    else:                g = grade(im, .94, .0, 1.0, .15, 1.0)
    g = g.filter(ImageFilter.UnsharpMask(1.2, 40, 2))
    g.save(f'{OUT}/{name}.jpg', quality=84, optimize=True, progressive=True)
    print(f'{name:22} {os.path.getsize(f"{OUT}/{name}.jpg")//1024} KB')
