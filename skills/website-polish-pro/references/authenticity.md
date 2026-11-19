# Authenticity ("DNA") review

A site can use all the right colours and still read as a template. This review asks, section by section, whether each element comes **from this business's own world** or is borrowed decoration. Work through it after the build and before the final polish. Write the findings as a short ranked list for the user, fix what you can without inventing facts, and list what only the owner can supply.

## The questions

**1. Identity in its own language**
- Does the brand appear in the language and script of its culture (a Chinese restaurant's Chinese name, an Italian trattoria's Italian name, a Mexican taquería's Spanish)? A single generic character or word that every business in the category could use (華 "China", "Ristorante", "Taquería") is not identity.
- Translate the name literally and check the connotations before using it. Example: "Golden Lotus" → 金蓮 is also the old euphemism for bound feet and a notorious novel character; 金荷 avoids it. If unsure, propose and flag for the owner.
- Pick one script system and keep it (Traditional vs Simplified Chinese; accents in Spanish/French/Vietnamese). Mixed systems read as machine-made.

**2. Motifs from the right culture**
- Name each decorative motif and its origin. Common slips: seigaiha waves, cherry blossom, torii, kimono patterns are *Japanese*; a Chinese site wants plum blossom (梅), lotus, key-fret (回紋), cloud scrolls (祥雲), lattice (窗花), coins, bamboo, cinnabar seals. Talavera tiles and papel picado are Mexican, not "Latin" generically; zellige is Moroccan.
- Watch alt text and copy for the same slips ("cherry blossom" vs "plum blossom").
- Restraint: lanterns + pagoda + bamboo + dragon + blossom all at once is a theme park. Keep two or three, done well.

**3. Lettering**
- Western wedding/brush scripts (Great Vibes, Pinyon) on a non-Western brand read as borrowed. Use real lettering from the culture (e.g. Kai/brush CJK fonts such as LXGW WenKai TC, Ma Shan Zheng for Simplified) for short accents: a section's name in its language, a vertical label, the seal.
- Never use pastiche "ethnic" display fonts (chop-suey, faux-Arabic, faux-Hebrew Latin). They are the cliché, not the culture.
- Load CJK web fonts as a `&text=` subset of the characters actually used (builder computes it), or pages pull megabytes.
- Vertical CJK: one span per character in a flex column; avoid `writing-mode` quirks.

**4. Customs and terms stated correctly**
- Check every cultural claim. Examples caught in practice: red eggs and ginger belong to a baby's **full-month** party (滿月), not 100 days; longevity noodles are served uncut (長壽麵); whole fish at New Year for 年年有餘; never show chopsticks standing upright in rice (funeral taboo). Fortune cookies are Japanese-American: fine on a Chinese-*American* takeout page, wrong as "authentic".
- Quote real sources when you use one (e.g. Zhou Dunyi 周敦頤, 《愛蓮說》, "出淤泥而不染").

**5. The industry's own document conventions**
- Menus: the way menus in that cuisine/country are actually written. Chinese-American: numbered items (L1 lunch, C1 combination plates, S1 chef's specials, then 1–N), Chinese name + pinyin per dish, lunch specials with fried rice and egg roll/soup, pint/quart soups, pepper icons. Italian: antipasti / primi / secondi / contorni / dolci. Japanese: by preparation (yakimono, agemono). Bakery: by bake time/day. Law firm: practice areas, bar admissions.
- Units, terms of art and section names a person in the trade would use.

**6. Point of view and proof**
- Does the copy say *whose* this is (family, region, chef, year) and back up quality claims? "Authentic", "best", "finest" with no proof is the cliché readers skip. If the owner hasn't supplied the story, write honest copy that doesn't need it, and list the story as a fact to add.
- A kitchen that spans Cantonese, Sichuan and Shanghai with no stated roots has no point of view; ask the owner for the home region.

**7. Trust breakers**
- Buttons that promise something the site can't do ("Order Online" that goes to an explanation). Make the link a single config switch so the real URL drops in later.
- Placeholder phone numbers (555), fake reviews or awards (never invent them), stock-looking or AI photos reused across pages.

## Output format for the user

```
What's not speaking authentic DNA (ranked):
1. <biggest gap>: <one-line why> → <fix I can do now | needs owner>
...
I can fix now: <list>
Only you can supply: <list>
```
