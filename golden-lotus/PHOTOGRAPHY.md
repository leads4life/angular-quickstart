# Golden Lotus · Photography Replacement Guide

Every photo position on the site has its **own file name**. To replace a photo:

1. Make the image (ChatGPT prompts below, or better, a real photo of the restaurant).
2. Save it with the **exact file name** from the table. Lowercase, `.jpg`, no spaces.
3. Send the files back to Claude (or drop them into `golden-lotus/img/` and run `python3 site.py`).

Nothing else needs to change. The site picks a file up by its name.

## Status (November 2026)
All 13 slots now hold the owner-supplied images (AI-generated, fictional). Untouched originals are kept in `photo-originals/`; the site uses graded copies made by `work/grade_photos.py` (warmer, deeper, soft vignette to match the dark lacquer palette). To replace a photo later, drop the new file into `photo-originals/` with the same name, run `python3 work/grade_photos.py` then `python3 site.py`.
Still worth replacing with real photos when available: `hero-contact.jpg` (your real entrance) and `about-story.jpg` (your own kitchen).

---

## The slot map

| # | File name | Where it appears | Shape on screen | Ask ChatGPT for | Keep clear |
|---|-----------|------------------|-----------------|-----------------|------------|
| 1 | `home-hero.jpg` | Home, first screen | Full screen, wide (≈16:9; phones show the right half) | Landscape 1536×1024 | Left 40% dark and empty (headline sits there). Hero dish at about 65% from the left |
| 2 | `home-signature.jpg` | Home, left of "Signature Dishes" | Edges fade into black | Landscape 1536×1024 | Dark background all round, plate centred |
| 3 | `home-private-dining.jpg` | Home, "Private Events" band (left side) | Wide band, about 2:1 | Landscape 1536×1024 | Main subject centred, nothing important near top/bottom edges |
| 4 | `hero-menu.jpg` | Menu page, first screen | Full screen, wide | Landscape 1536×1024 | Left 40% dark |
| 5 | `hero-takeout.jpg` | Takeout & Delivery, first screen | Full screen, wide | Landscape 1536×1024 | Left 40% dark |
| 6 | `hero-events.jpg` | Private Events, first screen | Full screen, wide | Landscape 1536×1024 | Left 40% darker |
| 7 | `hero-about.jpg` | About, first screen | Full screen, wide | Landscape 1536×1024 | Left 40% dark |
| 8 | `hero-contact.jpg` | Contact, first screen | Full screen, wide | Landscape 1536×1024 | Left 40% dark |
| 9 | `hero-legal.jpg` | Privacy + Accessibility, first screen | Full screen, wide | Landscape 1536×1024 | A texture, no subject |
| 10 | `events-room.jpg` | Private Events, "A Round Table Under the Moon Window" | Moon-gate arch (top corners curve away) | Landscape 1536×1024 | Subject centred, keep top corners unimportant |
| 11 | `about-story.jpg` | About, "A Neighborhood Kitchen" | Soft rounded square | Landscape 1536×1024 | Subject centred |
| 12 | `about-name.jpg` | About, "Why the Lotus" | Soft rounded square | Landscape 1536×1024 | Subject centred |
| 13 | `texture-red-floral.jpg` | Behind "Private Events" text and the red "Hungry?" band on every page | Background texture | Landscape 1536×1024 | Even, low-contrast pattern, no subject |
| — | `bamboo.png` | Gold bamboo decoration, home | Transparent cut-out | Leave as is | — |

> Real photos beat AI every time, and two slots really need them: **`hero-contact.jpg`** (your actual entrance, so guests recognise it) and **`about-story.jpg`** (your own kitchen and cooks). Shoot landscape, at least 2400 px wide.

---

## Step 1 · Paste this into ChatGPT first (sets the style for the whole session)

```
You are the food and interior photographer for Golden Lotus (金荷), a family Chinese
restaurant in Wellington, Florida, that serves Cantonese and Sichuan classics and
Chinese-American favourites. I will ask for one photo at a time for the restaurant's
website. Rules for every image:

- Photorealistic editorial restaurant photography, not illustration.
- Dark, moody, warm tungsten light; deep near-black backgrounds; accents of
  cinnabar red and antique gold; shallow depth of field.
- Landscape 1536x1024 unless I say otherwise.
- Chinese, not generic "Asian": Chinese porcelain and stoneware, rosewood,
  lattice screens, red paper lanterns, plum blossom (梅花, NOT cherry blossom),
  lotus, bamboo. No Japanese elements: no sushi, no torii, no kimono, no
  cherry blossom, no bonsai, no Japanese lettering.
- Never show chopsticks standing upright in a bowl of rice (a funeral taboo).
- No text, no signs, no menus with writing, no logos, no watermarks.
- Real-looking portions and real Chinese dishes; no fantasy garnishes.
- Leave the requested empty dark area for website text.

Reply only with the image.
```

## Step 2 · One prompt per slot (send one at a time)

**1 · `home-hero.jpg`**
```
General Tso's chicken with broccoli and red pepper in a dark hand-thrown stoneware bowl,
one glossy sesame-coated piece lifted by dark wooden chopsticks, steam rising, a red
paper lantern glowing softly out of focus behind. A branch of pink plum blossom enters
the top-left corner. The bowl sits at the right, about 65% across the frame; the left
40% is dark, empty, out-of-focus restaurant interior.
```

**2 · `home-signature.jpg`**
```
Close-up three-quarter view of General Tso's chicken on a dark speckled stoneware plate,
sesame seeds and thin curled scallions on top, a carved carrot flower garnish at the
left, red brocade cloth just visible under the plate. Black background fading to darkness
on every side so the photo can blend into a black web page.
```

**3 · `home-private-dining.jpg`**
```
A private Chinese banquet room: round table with white cloth, red folded napkins, wine
glasses, a lazy Susan, pink orchids in the centre; behind it a circular moon-gate window
painted with plum blossoms, dark rosewood lattice screens and glowing wall lanterns.
Eye-level, table centred, warm and inviting, no people.
```

**4 · `hero-menu.jpg`**
```
Overhead family-style spread on a dark rosewood table: a bamboo steamer of xiao long bao,
a plate of beef chow fun, mapo tofu in a clay pot, garlic bok choy, steamed rice in
porcelain bowls, a small dish of chili oil. Dishes fill the right 60% of the frame; the
left 40% is dark empty table.
```

**5 · `hero-takeout.jpg`**
```
Chinese takeout at a dark wood counter: white folded paper pails of lo mein and fried
rice, a container of General Tso's chicken, a red paper carry bag, wrapped chopsticks and
small sauce cups. Warm counter light from above; items on the right; left 40% dark.
```

**6 · `hero-events.jpg`**
```
A Lunar New Year banquet seen from a low angle: round table set for ten with a whole
steamed fish topped with ginger and scallion at the centre, red lanterns overhead, gold
accents, glasses raised just out of focus at the edge. Main subject right of centre; left
40% darker.
```

**7 · `hero-about.jpg`**
```
A chef's hands tossing beef chow fun in a flaming black carbon-steel wok, flames licking
the rim, motion in the noodles, a steel commercial kitchen in deep shadow. Wok at the
right; left 40% dark. Show hands and forearms only, no face.
```

**8 · `hero-contact.jpg`** (ideally replace with a real photo of your entrance)
```
Entrance of a Chinese restaurant in a Florida shopping plaza at dusk: glass door, two red
lanterns, potted bamboo, warm light spilling onto the pavement, palm silhouette against a
deep blue sky. No readable signs or text. Door at the right; left 40% darker sky and wall.
```

**9 · `hero-legal.jpg`**
```
Close-up texture of deep cinnabar-red lacquer with a faint gold key-fret (回紋) border
pattern and soft gold peony motifs, slightly worn, evenly lit, no objects. Seamless and
calm, suitable as a website background.
```

**10 · `events-room.jpg`**
```
The same private banquet room from a slightly different angle: round table centred,
moon-gate window with plum blossom painting behind, orchids on the table, red napkins.
Keep the top corners simple (dark lattice) because they will be curved away by an arch frame.
```

**11 · `about-story.jpg`** (ideally replace with a real photo of your kitchen)
```
Close-up of a cook's hands pleating xiao long bao on a floured wooden board, a bamboo
steamer of finished dumplings beside, warm side light, dark background. Hands only, no face.
```

**12 · `about-name.jpg`**
```
Pink lotus flowers (荷花) and broad lotus leaves on a still summer pond at golden hour,
one flower in full bloom in sharp focus, a lotus seed pod beside it, dark water, soft
gold light. Calm and elegant.
```

**13 · `texture-red-floral.jpg`**
```
Deep red silk brocade with a tone-on-tone peony and cloud pattern, soft directional light,
low contrast, even across the whole frame, no objects. Website background texture.
```

## Step 3 · Before sending them back
- Rename each file exactly as in the table (e.g. `hero-menu.jpg`).
- If ChatGPT gives you a `.png` or `.webp`, that's fine. Send it as is and Claude will convert it.
- Send them all in one message: "Here are the replacement photos." Claude will place, crop, compress, check every page and republish.
