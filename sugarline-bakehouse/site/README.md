# Sugarline Bakehouse site (fictional concept)

- `src/`: template.html (head, header, footer, sprite, script), pages/*.html (page bodies with @@PAGEHERO@@, @@CTA@@ and @@STICKER@@ macros), assets/styles.css, img/, fonts/ (self-hosted, SIL OFL).
- Build: `python3 build.py` writes full HTML documents to `dist/`.
- QA: `qa/report.md` (site-qa: all checks pass).
- Forms are demos: they validate, then say they aren't connected. Hook them up to Netlify Forms (attributes are already present) or Formspree before launch.
- Placeholders (`<mark>[…]</mark>`) and noindex/robots.txt are intentional until real facts exist.
