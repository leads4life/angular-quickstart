# Showcase: studio sales page + live demo

    python3 build.py      # rebuilds everything into dist/

- `dist/index.html`: the sales page (source `sales.html`, facts in `studio.json`: studio name, seal character, tagline, package prices, form endpoint, contact email).
- `dist/demo/golden-lotus/`: the demo restaurant, built from `../golden-lotus` with `restaurant.json` (demo mode on: demo bar, `noindex`, no Google business data).
- `dist/assets/`: screenshots of the demo, retaken on every build by `shoot.js`, so the sales page always shows the current demo.

## Making it live
1. Edit `studio.json`: your studio name, prices (or keep "Quote on request"), `contact_email`, and a `form_endpoint` (e.g. a Formspree form URL) so quote requests are actually delivered. Without an endpoint the form validates and says plainly that nothing was sent.
2. `python3 build.py`, then deploy `dist/` to Netlify/Cloudflare Pages on your domain.

## Using the template for a real client
Copy `golden-lotus/`, edit `restaurant.json` (name, Chinese name, address, phone, hours, ordering link; set `demo.enabled` to false), put their photos in `photo-originals/` under the slot names in PHOTOGRAPHY.md, run `work/grade_photos.py` and `site.py`, then run the website-polish-pro audits.
