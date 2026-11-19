# Golden Wok Chinese Restaurant

An Angular 13 website built from the Golden Wok page-concept mockups: eight routed pages that share a header, a footer and one visual system (charcoal-brown photography, parchment cream, burgundy, brushed gold, flowing wave dividers, serif display type, and a red Order Online button on every page).

| Route | Page |
| --- | --- |
| `/` | Home |
| `/menu` | Menu, with category anchors (`/menu#noodles`) |
| `/about` | About |
| `/private-events` | Private Events, with inquiry form |
| `/order-online` | Order Online |
| `/catering` | Catering, with request form |
| `/gallery` | Gallery, with keyboard-friendly lightbox |
| `/contact` | Contact, with form, hours and directions |
| any other path | 404 page (`noindex`) |

## Before going live

- **Placeholder content.** The business name, address, phone, hours and menu are fictional placeholders from the mockups. Edit them all in `src/app/site.data.ts`.
- **Placeholder photos.** The photos in `src/assets/img/` are rebuilt from the mockup images (2×/4× AI super-resolution, baked-in nav text painted out). They are still soft at large sizes, so replace them with real photography under the same file names and aspect ratios.
- **Online ordering.** `SITE.orderUrl` currently dials the restaurant. Point it at your ordering provider.
- **Forms** post to [Netlify Forms](https://docs.netlify.com/forms/setup/). The hidden copies in `src/index.html` let Netlify detect them, so keep their field names in sync with `src/app/shared/inquiry-form.component.html`.

## Design system notes

**Every page opens on a full first screen.** The hero is `max(560px, 100svh)` tall and ends on its wave, so nothing from the next section shows before scrolling.

**Seams.** No boundary is a straight line:

| Seam | Motif |
| --- | --- |
| Hero → first section | Cream wave with a brushed-gold edge (`app-wave`) |
| Section → section, section → photo band | Fine gold double rule broken by small cloud, coin and lantern glyphs (`.seam`, `.seam--dark` over photos) |
| Between menu categories, stacked panels on phones, inside the footer | The same rule, smaller (`--rule-sm`, `--rule-ft`) |
| Last section → footer | Burgundy wave with a gold edge, arriving on a faint gold seigaiha (wave-scale) pattern |

**Photo shapes.** No framed photo has hard square corners:

| Role | Shape |
| --- | --- |
| Feature photos (About, Private Events, Menu sections) | Soft organic squircle with a gold rim and soft shadow; three variants a/b/c, cycled so neighbours differ |
| Gallery cards | Asymmetric soft corners (30px/20px), alternating |
| Popular-dish plates | Feathered oval fade into the cream |
| Photo bands, heroes | Full-bleed; their edges are seams |

The ornaments are generated SVG held in CSS variables. To change them, edit `tools/gen-ornaments.py` and run `python3 tools/gen-ornaments.py`, which rewrites `src/ornaments.css`.

Fonts (Playfair Display and Jost, latin, only the weights used) are self-hosted from `@fontsource`, so no Google Fonts request is made.

## Single-file preview

```bash
npx ng build -c preview                    # hash URLs (/#/menu), output in dist/preview
python3 tools/build-single-file.py dist/preview golden-wok-preview.html
```

The result is one HTML file with everything inlined. It opens from disk with no server, which is handy for sharing a review copy. Its forms can't submit; use the Netlify deploy for that.

## Project layout

```
src/app/site.data.ts      all business info, nav, menu and gallery content
src/app/layout/           header (sticky, mobile menu) and footer
src/app/shared/           icons, logo, wave divider, page hero, inquiry form
src/app/pages/            one component per page
src/styles.css            the whole design system (colors, type, layout, seams, shapes)
src/ornaments.css         generated seam rules, footer pattern, photo masks
tools/                    ornament generator, single-file preview builder
```

## Commands

```bash
npm install
npm start                       # dev server at http://localhost:4200
npm run build                   # production build to dist/angular-quickstart
npx ng test --browsers=ChromeHeadlessCI --watch=false   # unit tests (headless)
```

Deploys to Netlify using `netlify.toml`. The SPA redirect is already configured.
