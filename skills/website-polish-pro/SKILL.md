---
name: website-polish-pro
description: End-to-end website build and polish pipeline that turns a mockup image (or a rough draft site) into a finished, multi-page, screenshot-verified site and proves it with bundled audits. It covers photos cut from the mockup, a template-plus-builder build, industry-themed section seams, soft photo shapes, first-screen fit, column alignment, blank-space and placeholder detection, an authenticity/cultural "DNA" review, one-file-per-slot photography with a PHOTOGRAPHY.md handoff of ChatGPT prompts, and single-switch config for facts like the online ordering link. Use this whenever someone asks to build a site from a mockup, polish or perfect a website, "do another polish", find blank or unfinished areas, make a site feel more authentic to its culture or trade, align sections, or prepare photo replacement instructions, even if they don't name the skill. Prefer it over website-polish, website-polish-plus and mockup-to-website when the user wants the complete process or the audits.
---

# Website Polish Pro

The mockup (or the draft's own art direction) is the spec. The work is a loop: **build → render in a real browser → audit → look → fix**. Nothing is "done" from reading code. The bundled audit runner turns most of the judgement calls into pass/fail lines, so every pass ends with numbers, not impressions.

Bundled resources (paths relative to this skill):
- `scripts/audit.js`: one runner for all page audits (seams, photo shapes, first screen, column alignment, blank space, placeholders, sideways scroll and script errors)
- `scripts/check_links.py`: static links, anchors, images, duplicate ids, leftover build tokens
- `scripts/photo_slots.py`: which image fills which slot; flags shared files; writes the PHOTOGRAPHY.md skeleton
- `scripts/deco.py`: generates seam rules, photo masks and a quiet background tile for a motif world (`chinese`, `cards`, `botanical`; add more)
- `scripts/crop_tools.py`: gridded measuring views, baked-text removal, crops, transparent cut-outs, border trim
- `scripts/shots.js`: full-page screenshots plus 3-up contact sheets
- `references/build.md`: template + builder pattern, config switches, layout rules
- `references/seams-and-shapes.md`: seam treatments, photo shapes, first-screen rules
- `references/authenticity.md`: the DNA review questions and output format
- `references/photography.md`: photo slots and the PHOTOGRAPHY.md handoff

## Ground rules (why they matter)

- **Business facts are copied exactly, never invented.** Name, phone, address, hours, prices, awards and reviews come from the user or the mockup. A made-up fact on a live site is worse than a gap. Sample prices are acceptable only when labelled as samples, and every one is listed for the user to replace.
- **No visible placeholders.** `[brackets]`, `<mark>` highlights and "TBD" read as an unfinished site. Rewrite the sentence so it works without the missing fact ("call us about your guest count" instead of "seats up to [number]"), and list the missing facts in the README. The placeholder audit enforces this.
- **Restraint.** Keep one memorable element per page and make the rest quiet. Decorations must look deliberate at 2× zoom, never like a layout bug.
- **Save before you change.** Copy the site to `before/` (and the mockup to `*_orig.png`) before the first edit. Every audit is run on the before copy too and must fail there, which proves it detects the problem you claim to have fixed.
- **Work in big batches and keep state in files** (template, builder, page bodies, generators), so a reset or a new turn resumes from disk.
- **Report honestly.** If an audit still fails or a step was skipped, say so with the line from the audit output.

## Phase 0 · Intake
1. Collect what exists: the mockup image, any asset zip, an existing draft, real business facts, the user's real viewport (screenshot width ÷ display scaling, minus browser chrome).
2. Start as soon as you have the mockup. Don't stall on missing facts; plan to write around them.
3. Create a task list: photos → build → character → authenticity → verify → deliver.
4. Save `before/` copies.

## Phase 1 · Diagnose
- Screenshot the draft (or the first build) next to the mockup (`scripts/shots.js`).
- List each page's section order. Every adjacent pair is a seam.
- `grep -n 'style="'` for inline styles that will beat later CSS.
- Run `scripts/audit.js` once to get the baseline, and `scripts/photo_slots.py` to see shared or low-res images.
- Decide whether to patch or rebuild. Structural problems mean rebuild, reusing the content.

## Phase 2 · Photography
- **From an asset pack:** trim white borders (`crop_tools.py trim`), crop to each slot's aspect, export about 2× display size as progressive JPEG.
- **From the mockup:** run `crop_tools.py grid` to measure boxes, then `clean` to inpaint baked text (keep icons out of the mask), then `crop` each region a few px inside its edges. Use `cutout` for decorations such as gold bamboo, keyed by hue so the background drops out. Look at the cleaned image once.
- **One file per slot from the start** (`home-hero.jpg`, `hero-menu.jpg`, `about-story.jpg`…), even if two slots temporarily hold the same picture. See `references/photography.md`. This is what makes a later photo swap a pure file drop.

## Phase 3 · Build
Follow `references/build.md`. The essentials:
- One `template.html` plus page bodies plus `site.py`. Tokens for every internal link, `aria-current` on the current page, files rather than folders in links.
- **Single switches** in `site.py` for facts that will change (`ORDER_URL`, booking link). Every dependent button uses the token, so pasting one URL updates the whole site.
- **One content column and one spacing scale.** Sections differ in height, not in edge or rhythm. Card grids use column counts that divide the item count at each breakpoint.
- Tokens on `:root`, explicit single theme (`color-scheme: light` plus explicit colors) unless the mockup has two, sticky header that collapses to a menu button, forms that validate and then say plainly that nothing was sent.
- JSON-LD only from facts on the page.

## Phase 4 · Character
Follow `references/seams-and-shapes.md`.
- Generate the motif kit: `python3 scripts/deco.py --motifs <world> --gold "<accent>" --out seams.css`. Pick or add glyphs a person in the trade would recognize.
- Use three seam treatments (hero exit, section to section, arrival at the footer), with the same wave reused on every page hero.
- Give feature photos organic masks with shadows that follow the outline, and give cards alternating soft corners.
- Make the first screen a composition: the hero fills `100svh` minus the header, and nothing peeks or gets sliced.
- **Fill blanks with substance, not decoration.** When a column or card is short, add what a visitor would actually want there (hours, a call line, a "helpful to include" checklist, a Chinese or local name for the dish) instead of stretching or leaving air.

## Phase 5 · Authenticity review
Read `references/authenticity.md` and work through its seven questions:
1. Identity in its own language
2. Motifs from the right culture
3. Lettering
4. Customs stated correctly
5. The trade's own document conventions (for a restaurant, the menu)
6. Point of view and proof
7. Trust breakers

When the user asks "what isn't authentic", answer with the ranked list format from that file before changing anything. Then fix what needs no new facts and list what only the owner can supply. Translate brand names literally and check their connotations before using them.

## Phase 6 · Verify (one pass, then fix)
Serve both folders over HTTP, start them detached, and run everything:

```bash
(setsid nohup python3 -m http.server 8765 --directory dist >/dev/null 2>&1 </dev/null &)
(setsid nohup python3 -m http.server 8766 --directory before >/dev/null 2>&1 </dev/null &)
python3 <skill>/scripts/check_links.py dist
node <skill>/scripts/audit.js --base http://localhost:8765 --dir dist --label AFTER  > audit-after.txt
node <skill>/scripts/audit.js --base http://localhost:8766 --dir before --label BEFORE > audit-before.txt
python3 <skill>/scripts/photo_slots.py dist
node <skill>/scripts/shots.js --base http://localhost:8765 --dir dist --out shots --widths 1440,390
```

How to read the audit (`tail` shows the summary; `grep ^FAIL` shows the details):

| Check | Fails when | Usual fix |
|---|---|---|
| SEAM | a section boundary is a bare straight line | add the rule/wave; give inline SVG pieces `class="wave"` |
| SHAPE | a framed photo has square corners | wrap in `.blob` with a mask, or radius plus `overflow:hidden` |
| FIRST | later content peeks into the first screen, the fold slices a hero element, or hero content crowds the nav | hero `min-height` calc, clamp heading sizes, move decorations down |
| ALIGN (warn) | a section's content column starts at a different x than most sections | use the shared `--wrap` container; mark split bands `data-align="free"` |
| BLANK | orphan grid slots, hollow cards, an empty vertical run over 280px, lopsided columns (warn) | divisible column counts, stack short cards, fill the short side with useful content |
| PLACE | `[brackets]`, `<mark>`, lorem/TBD/"coming soon"; 555 numbers (warn) | rewrite around the missing fact; list it in the README |
| BASICS | sideways scroll or a script error | `overflow-x:clip` on the overflowing section; fix the error |

The pass bar is **0 FAIL** on AFTER and FAIL on BEFORE for every problem you claim to have fixed. Warnings need a decision. Mention each one in the report as either fixed or intentional.

Then look once at the contact sheets (3 pages per sheet) and once at the homepage at full size. Typical things only eyes catch: a decoration that reads as a glitch, a stray mark baked into a crop, a motif from the wrong culture, an awkward line break. Fix, rebuild, re-run the audit, and don't loop screenshots.

Fonts from Google don't load in an offline sandbox, so the audits block them and screenshots use fallbacks. Say so rather than calling the type broken.

## Phase 7 · Deliver
1. **Publish** the dist folder as one multi-file artifact: every page plus `img/`, published from files on disk. On republish, use `mode: "replace"` (or `remove`) when image files were renamed, so retired files stop being served.
2. **Zip** the folder with `README.md` (pages, how to rebuild, single switches, facts to confirm, missing facts, sample content, seam and shape notes) and `PHOTOGRAPHY.md` (see `references/photography.md`).
3. **Commit and push** the source and generators if working in a repo branch.
4. **Report**: a few sentences on what changed, then the honest caveats (facts that need the owner, sample prices, forms that need a backend such as Formspree, legal pages that need a lawyer's review), then a `✅ Self-reviewed:` line that lists only the checks actually run, with their numbers (for example "audit AFTER 0 FAIL; BEFORE 108 seam / 12 placeholder fails").

## Pitfalls

| Symptom | Fix |
|---|---|
| Audit `evaluate` returns undefined | pass `(${fn})()`, not the function source, to `page.evaluate` |
| Sideways scroll of exactly 10px | a pseudo-element seam with `left/right:-10px` inside a section or header without `overflow-x:clip` |
| Mobile menu disappears after adding `overflow-x:clip` to the header | check the dropdown still shows with `elementFromPoint`; `clip` on x keeps y visible, `hidden` does not |
| A grid looks fine at 1440 but has an orphan card at 1024 | `auto-fit` picked 3 columns for 4 items; use explicit column classes per breakpoint |
| Card grid reports "3 cards in 4 columns" with no visible gap | auto-fit leaves 0px tracks; the audit ignores them, so check your own measurement does too |
| Empty vertical run flagged over an FAQ | closed `<details>` only render `<summary>`; make sure summaries are visible text |
| Photo swap needs HTML edits | slots share files; split them so each slot owns a file name |
| Old images still served after a rename | republish with `mode: "replace"` or `remove` |
| A Chinese site uses a seigaiha (wave-scale) pattern | it's Japanese; use key-fret (回紋) or lattice |
| Literal translation of the brand has a bad connotation | propose an alternative (金荷 for "Golden Lotus") and flag it for the owner |
| CJK text tofu or slow pages | Traditional vs Simplified font mismatch, or no `&text=` subset |
| Stretched hero on wide screens | the photo is a low-res mockup crop; list it in PHOTOGRAPHY.md as a priority replacement |
| Inline `style=""` beats your media query | move it to a class |
