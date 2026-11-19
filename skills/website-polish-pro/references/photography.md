# Photo slots and the PHOTOGRAPHY.md handoff

## One file per slot
Every place a photo appears gets its own file named by role + location, even if it temporarily holds a copy of another photo:
`home-hero.jpg`, `home-signature.jpg`, `home-private-dining.jpg`, `hero-<page>.jpg`, `<page>-<section>.jpg`, `texture-<name>.jpg`, decorations as `.png`.
Then replacing a photo = saving a file under its name and rebuilding. No HTML edits, no "which photo was that?" later.
- Run `scripts/photo_slots.py dist/` to see every file, where it's used and which are SHARED. Shared is fine only when deliberate (the same hero at two breakpoints, one legal-page hero, a texture). Split everything else into its own file and update the references.
- When replacing old files, publish the artifact with `mode: "replace"` (or `remove`) so retired files stop being served.

## PHOTOGRAPHY.md (deliver it with the zip)
Generate the skeleton with `scripts/photo_slots.py dist/ --md PHOTOGRAPHY.md`, then write:
1. **How it works** (3 lines): make image → save with exact name → send back.
2. **Slot map table**: file name · where it appears · shape on screen (full-screen hero / faded edges / arch / band) · what to ask for (ChatGPT image sizes: landscape 1536×1024, portrait 1024×1536, square 1024×1024) · what to keep clear (e.g. "left 40% dark for the headline").
3. **Which slots need real photos** (storefront/entrance, own kitchen and team). AI can't show the real place.
4. **Style brief to paste into ChatGPT first**: brand + what the business is, photographic style (light, palette, depth of field), cultural do's and don'ts from the authenticity review (e.g. plum blossom not cherry; no Japanese elements on a Chinese site; never chopsticks upright in rice), "no text, signs, logos or watermarks", "leave the requested empty area for website text", "reply only with the image".
5. **One prompt per file**: subject, composition (where the subject sits, which side stays empty), props from the real culture/trade, no people's faces unless wanted.
6. **Before sending back**: exact names; png/webp are fine (convert on arrival: crop to the slot's shape, resize ~2× display size, progressive JPEG q80–86); send all in one message.

When files come back: put them in `img/` under their names, re-run `photo_slots.py`, build, run the audits, look once, republish.
