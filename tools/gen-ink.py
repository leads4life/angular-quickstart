#!/usr/bin/env python3
"""Generate the "Ink & Lacquer" textures into src/assets/ink/.

  paper.jpg      seamless rice-paper tile (the ground under the whole site)
  bleed-b.webp   ink edge: opaque at top, bleeding to nothing at the bottom
  bleed-t.webp   the same idea for a top edge (separate seed, then flipped)
  mist.webp      misty ink-wash mountain ranges with a small pagoda
  brush.webp     dry-brush stroke, horizontal (used as a CSS mask)
  brush-v.webp   the same stroke, vertical
  ink-a/b/c.webp ink-bled photo masks (stretched to each photo)

Horizontal tiles (bleed, mist) are periodic in x, so they repeat seamlessly
at their natural size and never stretch. Run: python3 tools/gen-ink.py
"""
import pathlib
import numpy as np
from PIL import Image, ImageDraw

OUT = pathlib.Path(__file__).resolve().parent.parent / "src" / "assets" / "ink"
OUT.mkdir(parents=True, exist_ok=True)


def gblur(a, sx, sy, wrap_x=True, wrap_y=False):
    """Gaussian blur via FFT; periodic on wrapped axes, reflected otherwise."""
    a = np.asarray(a, float)
    for axis, s, wrap in ((1, sx, wrap_x), (0, sy, wrap_y)):
        if s <= 0:
            continue
        pad = 0 if wrap else int(4 * s) + 1
        if pad:
            pw = [(0, 0), (0, 0)]; pw[axis] = (pad, pad); b = np.pad(a, pw, mode="reflect")
        else:
            b = a
        n = b.shape[axis]; f = np.fft.rfftfreq(n); g = np.exp(-2 * (np.pi * f * s) ** 2)
        g = g[None, :] if axis == 1 else g[:, None]
        b = np.fft.irfft(np.fft.rfft(b, axis=axis) * g, n=n, axis=axis)
        a = b if not pad else (b[:, pad:-pad] if axis == 1 else b[pad:-pad])
    return a


def norm(a):
    return (a - a.mean()) / (a.std() + 1e-9)


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def periodic_curve(rng, W, kmax, p=0.9):
    x = np.arange(W)
    s = sum(np.sin(2 * np.pi * k * x / W + rng.uniform(0, 2 * np.pi)) / k ** p for k in range(1, kmax + 1))
    return s / np.abs(s).max()


def save_alpha(alpha, name, rgb=(0, 0, 0), q=82):
    a = (np.clip(alpha, 0, 1) * 255).round().astype(np.uint8)
    img = np.zeros(a.shape + (4,), np.uint8); img[..., :3] = rgb; img[..., 3] = a
    Image.fromarray(img, "RGBA").save(OUT / name, quality=q, method=6)


# ---- ink bleed edge ---------------------------------------------------------
def bleed(seed, W=1800, H=300):
    rng = np.random.default_rng(seed)
    y = np.arange(H)[:, None]
    b = 0.50 * H + 0.12 * H * periodic_curve(rng, W, 12)
    blot = norm(gblur(rng.standard_normal((H, W)), 26, 16))
    bloom = norm(gblur(rng.standard_normal((H, W)), 70, 30))       # large soft ink blooms
    grain = norm(gblur(rng.standard_normal((H, W)), 1.0, 1.0))
    fib = norm(gblur(rng.standard_normal((H, W)), 4, 1.2))          # short paper fibres
    d = (y - b[None, :]) / (0.13 * H) + 0.7 * blot + 0.55 * bloom + 0.07 * grain
    alpha = 1 / (1 + np.exp(1.7 * d))
    edge = np.exp(-((y - b[None, :]) / (0.12 * H)) ** 2)
    alpha += 0.07 * edge * np.clip(fib, 0, None) * (1 - alpha)      # capillary feathering
    # sparse ink specks just past the edge, in small clusters
    yy, xx = np.mgrid[0:H, 0:W]
    for _ in range(int(W * 0.012)):
        cx = rng.integers(0, W); n = rng.integers(1, 4)
        for _ in range(n):
            px = (cx + rng.integers(-14, 15)) % W
            py = min(int(b[px] + rng.uniform(0.1, 0.33) * H), int(0.82 * H))
            r = rng.uniform(0.7, 2.3); a = rng.uniform(0.35, 0.85)
            x0, x1 = px - 4, px + 5
            cols = np.arange(x0, x1) % W
            sub = ((np.arange(x0, x1)[None, :] - px) ** 2 + (np.arange(py - 4, py + 5)[:, None] - py) ** 2) / r ** 2
            dot = a * np.exp(-sub ** 1.5)
            ys = slice(max(py - 4, 0), py + 5)
            alpha[ys, cols] = np.maximum(alpha[ys, cols], dot[: alpha[ys, cols].shape[0]])
    # solid near the top, but the point where fading may begin wanders, so no straight line forms
    g0 = (0.16 * H + 0.05 * H * periodic_curve(rng, W, 9))[None, :]   # never above 11% (CSS overlaps 10%)
    alpha = np.maximum(alpha, 1 - smooth(g0, g0 + 0.14 * H, y))
    alpha *= 1 - smooth(0.86 * H, 0.98 * H, y)                       # nothing at the bottom
    return alpha


save_alpha(bleed(7), "bleed-b.webp")
save_alpha(bleed(21)[::-1], "bleed-t.webp")


# ---- misty ink-wash mountains -------------------------------------------------
def mist(seed=3, W=1800, H=260, ink=(86, 64, 50)):
    rng = np.random.default_rng(seed)
    y = np.arange(H)[:, None]
    grain = norm(gblur(rng.standard_normal((H, W)), 2.5, 2.5))
    A = np.zeros((H, W))
    ridges = []
    for base, amp, op, fade, k in ((0.52, 0.44, .12, 0.30, 12), (0.68, 0.40, .18, 0.24, 18), (0.84, 0.32, .27, 0.19, 24)):
        c = periodic_curve(rng, W, k, 1.05); c = (c - c.min()) / (c.max() - c.min()); c = c ** 2.3
        r = base * H - amp * H * c; ridges.append(r)
        t = (y - r[None, :]) / (fade * H)
        la = op * (1 / (1 + np.exp(-(y - r[None, :]) * 0.55))) * np.exp(-np.clip(t, 0, None) ** 1.3 * 2.4)
        la *= 1 + 0.22 * grain
        A = la + A * (1 - la)
    # a small pagoda on the near ridge
    pg = Image.new("L", (W, H), 0); d = ImageDraw.Draw(pg)
    x0 = int(0.71 * W); yb = int(ridges[2][x0 - 30:x0 + 30].min()) + 4
    w, yy = 30, yb
    for i in range(4):
        d.rectangle([x0 - w * .32, yy - 8, x0 + w * .32, yy], fill=255)
        d.polygon([(x0 - w / 2 - 5, yy - 7), (x0 - w / 2 + 3, yy - 9), (x0, yy - 15), (x0 + w / 2 - 3, yy - 9), (x0 + w / 2 + 5, yy - 7), (x0, yy - 11)], fill=255)
        yy -= 13; w -= 6
    d.line([(x0, yy - 1), (x0, yy - 12)], fill=255, width=2)
    pag = gblur(np.asarray(pg, float) / 255, 0.6, 0.6, wrap_x=False) * 0.3
    A = pag + A * (1 - pag)
    A *= 1 - smooth(0.6 * H, H, y)
    save_alpha(A, "mist.webp", ink, q=80)


mist()


# ---- dry-brush stroke ---------------------------------------------------------
def brush(seed=5, W=900, H=80):
    rng = np.random.default_rng(seed)
    x = np.arange(W)[None, :]; y = np.arange(H)[:, None]
    u = (x - 0.03 * W) / (0.94 * W)
    uc = np.clip(u, 0, 1)
    c = H * 0.5 - 0.07 * H * np.sin(np.pi * uc) + 0.03 * H * np.sin(3 * np.pi * uc)
    T = 0.62 * H * np.sin(np.pi * uc) ** 0.45 * (1 - 0.55 * uc) + 0.12 * H * np.exp(-(uc / 0.05) ** 2)
    T *= 1 + 0.12 * periodic_curve(rng, W, 30)[None, :]
    v = (y - c) / np.maximum(T / 2, 1e-3)
    inside = 1 - smooth(0.82, 1.0, np.abs(v))
    inside *= (u >= 0) & (u <= 1)
    N = 64
    nb = gblur(rng.standard_normal((N, W)), 16, 0, wrap_x=False); nb = nb / nb.std(axis=1, keepdims=True)
    bi = np.clip(((v + 1) / 2 * N).astype(int), 0, N - 1)
    th = -1.3 + 2.1 * uc ** 1.7                                      # drier toward the tail
    ink = 1 / (1 + np.exp(-(nb[bi, np.broadcast_to(np.arange(W)[None, :], bi.shape)] - th) * 4))
    a = gblur(inside * ink, 0.6, 0.6, wrap_x=False)
    save_alpha(a, "brush.webp")
    save_alpha(a.T[::-1], "brush-v.webp")


brush()


# ---- ink-bled photo masks -----------------------------------------------------
def ink_mask(seed, W=1200, H=900):
    rng = np.random.default_rng(seed)
    m = min(W, H); yy, xx = np.mgrid[0:H, 0:W].astype(float)
    inset, r = 0.04 * m, 0.07 * m
    qx = np.abs(xx - W / 2) - (W / 2 - inset - r); qy = np.abs(yy - H / 2) - (H / 2 - inset - r)
    sd = np.hypot(np.clip(qx, 0, None), np.clip(qy, 0, None)) + np.minimum(np.maximum(qx, qy), 0) - r
    blot = norm(gblur(rng.standard_normal((H, W)), 24, 24, wrap_x=False))
    grain = norm(gblur(rng.standard_normal((H, W)), 1.2, 1.2, wrap_x=False))
    fib = norm(gblur(rng.standard_normal((H, W)), 9, 0.8, wrap_x=False))
    bloom = norm(gblur(rng.standard_normal((H, W)), 60, 60, wrap_x=False))
    d = (sd + 0.02 * m * blot + 0.02 * m * bloom + 0.0022 * m * grain) / (0.018 * m)
    a = 1 / (1 + np.exp(d))
    edge = np.exp(-(sd / (0.03 * m)) ** 2)
    a += 0.15 * edge * np.clip(fib, 0, None) * (1 - a)
    return a


for s, n in ((4, "a"), (12, "b"), (27, "c")):
    save_alpha(ink_mask(s), f"ink-{n}.webp")


# ---- rice paper ------------------------------------------------------------------
def paper(seed=9, S=512):
    rng = np.random.default_rng(seed)
    big = norm(gblur(rng.standard_normal((S, S)), 60, 60, True, True))
    mid = norm(gblur(rng.standard_normal((S, S)), 7, 7, True, True))
    grain = norm(gblur(rng.standard_normal((S, S)), .7, .7, True, True))
    f1 = norm(gblur(rng.standard_normal((S, S)), 5, .6, True, True))
    f2 = norm(gblur(rng.standard_normal((S, S)), .6, 5, True, True))
    fib = np.clip(f1 - 2.2, 0, None) + np.clip(f2 - 2.2, 0, None)
    base = np.array([244, 234, 214], float)
    L = 3.2 * big + 1.6 * mid + 2.4 * grain + 3.2 * fib
    img = np.clip(base[None, None, :] + L[..., None] * np.array([1, .96, .9])[None, None, :], 0, 255).astype(np.uint8)
    Image.fromarray(img, "RGB").save(OUT / "paper.jpg", quality=86, optimize=True, progressive=True)


paper()
for p in sorted(OUT.iterdir()):
    print(p.name, Image.open(p).size, f"{p.stat().st_size // 1024} KB")
