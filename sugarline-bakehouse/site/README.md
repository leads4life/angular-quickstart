# Sugarline Bakehouse site (fictional concept)

- `src/`: template.html (head, header, footer, sprite, script), pages/*.html (page bodies with @@PAGEHERO@@, @@CTA@@ and @@STICKER@@ macros), assets/styles.css, img/, fonts/ (self-hosted, SIL OFL).
- Build: `python3 build.py` writes full HTML documents to `dist/`.
- QA: `qa/report.md` (site-qa: all checks pass).
- Forms are demos: they validate, then say they aren't connected. Hook them up to Netlify Forms (attributes are already present) or Formspree before launch.
- Placeholders (`<mark>[…]</mark>`) and noindex/robots.txt are intentional until real facts exist.

## Seams and shapes (polish pass)
- Header → page: a piped buttercream bead edge (`.site-head::after`).
- Section → section: torn recipe-card paper (`.edge-torn`), piped scallops (`.edge-scallop`) and a soft buttercream wave (`.edge-wave`), all in the lower section's colour.
- Last section → footer: cocoa scallops. Inside the footer: a dashed rule broken by wheat ears, hearts and stars.
- Photo shapes: hero and feature photos are arches; secondary photos are circles or taped prints; the cookie and matching photos use generated soft squircles (`--blob-a/b/c`, cycled per page) with drop-shadows on the wrapper; cards have alternating asymmetric corners.
- Motion: one hero entrance (card, arch, prints, sticker), off under prefers-reduced-motion.
- JSON-LD on the home page uses only on-page facts. No canonical link until a real domain exists.
