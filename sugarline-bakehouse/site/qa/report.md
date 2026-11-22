# Site QA report: `dist`

7 pages · widths 390, 768, 1024, 1440, 1920 · 2026-11-22 23:54

| | Check | Result |
|---|---|---|
| ✅ | Links & files | pass |
| ✅ | Errors & failed requests | pass |
| ✅ | Fonts | pass (loaded: Fraunces, Nunito Sans) |
| ✅ | Sideways scrolling | pass |
| ✅ | Even grid rows | pass |
| ✅ | Decorations clear of text | pass |
| ✅ | First screen | pass |
| ✅ | Menu open/close | pass (works at 3 widths) |
| ✅ | Leftover text | pass |
| ✅ | Text contrast | pass (850 on solid backgrounds, 0 on photos measured from pixels) |
| ✅ | Section seams (style) | pass (160 seams checked) |
| ✅ | Photo shapes (style) | pass (75 photos checked) |
| ℹ️ | Placeholders to fill | 7 findings |
| ℹ️ | Search-engine blocking | 8 findings |

**PASS**: 0 failing findings.

## Placeholders to fill

- **INFO** `404.html`: 5 [bracketed] blanks, 5 <mark> highlights: [Email address], [Opening hours], [Phone number], [Social links], [Street address]
- **INFO** `about.html`: 10 [bracketed] blanks, 10 <mark> highlights: [Baker's name], [Email address], [Founding story, in the baker's own words], [Opening hours], [Phone number], [Social links]
- **INFO** `celebration-cakes.html`: 6 [bracketed] blanks, 12 <mark> highlights: [Allergen policy], [Email address], [Opening hours], [Phone number], [Social links], [Street address]
- **INFO** `cookies.html`: 6 [bracketed] blanks, 7 <mark> highlights: [Box prices], [Email address], [Opening hours], [Phone number], [Social links], [Street address]
- **INFO** `index.html`: 7 [bracketed] blanks, 8 <mark> highlights: [Email address], [Opening hours], [Phone number], [Social links], [Street address]
- **INFO** `order.html`: 10 [bracketed] blanks, 11 <mark> highlights: [Allergen policy], [Email address], [Opening hours], [Phone number], [Social links], [Street address]
- **INFO** `weddings.html`: 8 [bracketed] blanks, 10 <mark> highlights: [$ per serving], [Delivery and set-up details], [Deposit terms], [Email address], [Opening hours], [Phone number]

## Search-engine blocking

- **INFO** `404.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `about.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `celebration-cakes.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `cookies.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `index.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `order.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `weddings.html`: page has noindex (fine for a concept/preview, remove at launch)
- **INFO** `robots.txt`: robots.txt blocks all crawlers (remove at launch)
