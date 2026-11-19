# Seams, shapes and the first screen

## Seams (never a straight line between sections)
Use two or three related treatments from the business's world, all one palette, subtle enough to reward a close look:
1. **Hero exit** (strongest): e.g. a cream & gilt wave with an ink-wash landscape (Chinese), a valance (theatre), a crust edge (pizzeria). Same SVG on every page hero (inject it in the builder; reuse the exact definition).
2. **Section to section** (lighter): a fine double rule broken by small industry glyphs: `scripts/deco.py --motifs chinese|cards|botanical`.
3. **Arrival** at a closing band / footer: a gilt wave, footlights, an awning edge. A curved band top can be done with a mask (`mask: var(--band-top) 0 0/100% 60px no-repeat, linear-gradient(#000,#000) 0 59px/100% calc(100% - 59px) no-repeat`) plus a negative `margin-top` so the section above shows through the curve.
- Remove bare hairlines under navs, around strips and above footers; replace with the small rule.
- Asymmetric motifs (hanging fabric, drips, fringe) get a second, direction-correct asset for the opposite edge, never `scaleY(-1)`.
- Anything that hangs into a section gets matching padding so it never sits on content.
- Inline SVG wave pieces should carry `class="wave"` (or `data-seam`) so the audit counts them.

## Photo shapes (no hard-edged boxes)
- Feature photos: organic mask (`--shape-a` arched window, `--shape-b/c` soft squircles), mask on the `<img>`, shadow as `filter: drop-shadow` on the wrapper so it follows the outline. Cycle shapes per page.
- Cards: soft asymmetric corners alternating along a row (`24px 12px` / `12px 24px`), `overflow:hidden` so images inside are clipped.
- Full-bleed heroes and photo bands are exempt (mark band containers `.photo-band`); their edges are seams.
- Decorative images (`alt=""`/`aria-hidden`) are exempt.

## First screen
- Hero fills the first screen: `min-height:max(FLOOR,calc(100vh - var(--hh)))` then the `100svh` line; `--hh` = sticky header height. Size headings with `clamp()` so the hero never slices at 1366×657 or 390×664.
- Nothing from the next section may peek into the first screen; decorations that poke up (e.g. a bamboo PNG) count too.
- Test at real viewports: a 1920×1080 screenshot at 125% is about 1536×696 CSS px.
