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

## Before going live

- **Placeholder content.** The business name, address, phone, hours and menu are fictional placeholders from the mockups. Edit them all in `src/app/site.data.ts`.
- **Placeholder photos.** The photos in `src/assets/img/` were cropped from the mockup images. They are low resolution, so replace them with real photography under the same file names.
- **Online ordering.** `SITE.orderUrl` currently dials the restaurant. Point it at your ordering provider.
- **Forms** post to [Netlify Forms](https://docs.netlify.com/forms/setup/). The hidden copies in `src/index.html` let Netlify detect them, so keep their field names in sync with `src/app/shared/inquiry-form.component.html`.

## Project layout

```
src/app/site.data.ts      all business info, nav, menu and gallery content
src/app/layout/           header (sticky, mobile menu) and footer
src/app/shared/           icons, logo, wave divider, page hero, inquiry form
src/app/pages/            one component per page
src/styles.css            the whole design system (colors, type, layout)
```

## Commands

```bash
npm install
npm start                       # dev server at http://localhost:4200
npm run build                   # production build to dist/angular-quickstart
npx ng test --browsers=ChromeHeadlessCI --watch=false   # unit tests (headless)
```

Deploys to Netlify using `netlify.toml`. The SPA redirect is already configured.
