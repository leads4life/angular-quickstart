# Business intake: Sugarline Bakehouse

| | |
|---|---|
| Project ID | `SLB-2026-11` |
| Business | Sugarline Bakehouse |
| Version | v1.0 |
| Date | 2026-11-22 |
| Status | **DRAFT** (awaiting owner approval) |
| Base branch | `main` → working on `ccr-fbc5b48e-8u9dyt` |

**Legend:** Owner-supplied · Verified (source) · Concept proposal · Unknown · **Fictional** (invented for this test business; never presented as real-world fact).

> Sugarline Bakehouse is a **fictional** business. Every name, place and detail below is invented. The site must not show real phone numbers, real addresses, reviews, star ratings, awards, years in business, health permits or certifications.

---

## 1. Business truth

| Field | Value | Status | Source |
|---|---|---|---|
| Exact name | Sugarline Bakehouse | Owner-supplied (Fictional) | Chat, 2026-11-22 |
| Real or fictional | Fictional test business | Owner-supplied | Chat |
| Location | Main-street shop in **Maple Hollow**, an invented small town | Owner-supplied (Fictional) | Chat |
| Street address | `[Street address], Maple Hollow` | Unknown → placeholder | — |
| Phone | `[Phone number]` | Unknown → placeholder | — |
| Email | `[Email address]` | Unknown → placeholder | — |
| Hours | `[Opening hours]` | Unknown → placeholder | — |
| Business type | Walk-in bakery shop plus made-to-order custom cakes | Owner-supplied | Chat |
| Core offers | Celebration cakes · Wedding cakes · Cookies & cookie boxes | Owner-supplied | Chat |
| Not offered on the site | Daily bread and pastries are not featured | Owner-supplied (not selected) | Chat |
| Signature claim | "Your cake, your story": every design is made for a person and an occasion | Owner-supplied | Chat |
| Brand look | Warm & homemade: cream, butter-yellow and soft brown; flour-dusted wood; natural window light | Owner-supplied | Chat |
| Baker / owner name | `[Baker's name]` | Unknown → placeholder | — |
| Founding year, awards, reviews, press | None. Do not invent any | Prohibited | Rule 1 |
| Differentiator | Personal design conversation for every custom cake; cookie boxes made to match the cake | Concept proposal | Claude |
| Physical setting | Small shop with a glass cake case, cream walls, wood shelves and a big front window; an open work counter behind it where cakes are decorated | Concept proposal (Fictional) | Claude |
| What staff do | Pipe buttercream, stack and smooth tiers, decorate sugar cookies, box orders, run tastings | Concept proposal | Claude |
| What customers do | Browse the case, pick up boxed orders, sit for a wedding tasting, plan a birthday cake | Concept proposal | Claude |

## 2. Commercial model, offers and buyer journey

**How it makes money (Concept proposal):** custom-order cakes are the main revenue (celebration cakes weekly, wedding cakes as the biggest orders), and cookie boxes are add-ons and gifts. Walk-in counter sales support it.

**Offer hierarchy**
1. **Celebration cakes:** birthdays, baby showers, anniversaries, graduations. Size and serving count by request, and the design starts from the customer's story. Price: `[Starting at $]`.
2. **Wedding cakes:** tiered cakes. A tasting and design consultation is booked first. Price: `[Starting at $ per serving]`.
3. **Cookies & cookie boxes:** decorated sugar cookies and gift boxes, including boxes matched to an event's cake. Price: `[Box prices]`.

**Ordering model (Owner-supplied):** a request form, then the bakery replies with a quote. The customer gives the date, servings, occasion, flavour ideas and inspiration. Lead time is shown as `[X] weeks` (Unknown).

**Buyer journey (Concept proposal)**
- *Celebration:* sees a cake for the occasion → checks that the bakery can personalise it → reads how ordering works and the lead time → **Order a cake** → gets a quote → pays and picks up.
- *Wedding:* sees tiered work and the tasting experience → **Book a tasting** → consultation → quote → deposit `[terms]`.
- *Cookies:* browses boxes → adds them to a cake order or orders gift boxes on their own (same request form, Cookies selected).

## 3. Customer, market and research notes

Research not performed: the business is fictional and has no real market. Everything below is a **Concept proposal**.

- **Customers:** parents planning children's birthdays; couples planning a wedding; friends and coworkers buying gifts; local event planners.
- **Motivations:** a cake that feels personal, looks special in photos and tastes homemade.
- **Objections to answer on the site:** "Can you really make my idea?", "How far ahead must I order?", "What does it cost?", "Do you handle allergies?" The allergen wording is `[Allergen policy]` and the site makes no claims about it.
- **Atmosphere to show:** warm, flour-dusted, handmade, generous. Hands at work rather than posed portraits.

## 4. Conversion plan

| CTA label | Where | Goes to | Expected action |
|---|---|---|---|
| **Order a cake** (primary) | Header, hero, end of every product section, footer | `/order` | Send the order request form (date, servings, occasion, flavours, inspiration, contact details) |
| **Book a tasting** (secondary) | Weddings page hero, wedding section on Home | `/weddings#tasting` | Request a wedding tasting slot |
| See celebration cakes | Home offer card | `/celebration-cakes` | Browse |
| See wedding cakes | Home offer card | `/weddings` | Browse |
| See cookie boxes | Home offer card | `/cookies` | Browse |
| Call `[Phone number]` | Footer, Order page | `tel:` placeholder | Call |

## 5. Page inventory

| Slug | Label | Purpose | Sections |
|---|---|---|---|
| `/` | Home | Show the three offers and the "your story" promise; drive orders | Header · Hero · Promise · Three offers · How ordering works · Wedding tasting band · Cookie boxes · Visit the shop · Final CTA · Footer |
| `/celebration-cakes` | Celebration Cakes | Show personalised occasion cakes | Hero · Occasions · How we design your cake · Sizes & servings `[placeholders]` · Flavours · CTA |
| `/weddings` | Wedding Cakes | Tiered work, plus booking a tasting | Hero · Tiered styles · The tasting (`#tasting`) · Planning timeline · Pricing guide `[placeholders]` · CTA |
| `/cookies` | Cookies | Decorated cookies and gift boxes | Hero · Box types · Matching cookie boxes · How to order · CTA |
| `/about` | About | The fictional baker and the shop | Hero · The story (Fictional, placeholder name) · The shop · Values (scratch, personal) · CTA |
| `/order` | Order | Order request form | Intro · Lead time `[X] weeks` · Form · What happens next · Contact |

**Nav:** Celebration Cakes · Wedding Cakes · Cookies · About · **Order a cake** (button). The logo links Home.
**Footer:** logo + one-line promise · page links · `[Street address], Maple Hollow` · `[Phone number]` · `[Email address]` · `[Opening hours]` · `[Social links]` · © 2026 Sugarline Bakehouse.

## 6. Homepage narrative and copy candidates

| Section | Copy candidates |
|---|---|
| Header | Sugarline Bakehouse · Celebration Cakes · Wedding Cakes · Cookies · About · **Order a cake** |
| Hero | **H1:** "Your cake, your story." · Sub: "Celebration cakes, wedding cakes and cookie boxes, baked by hand in Maple Hollow." · CTA: **Order a cake** · link: "See our cakes" |
| Promise | "Every cake starts with a conversation." · "Tell us who it's for and what makes them smile. We'll design and bake something that's only theirs." |
| Three offers | "Celebration Cakes": "Birthdays, showers and every reason in between." · "Wedding Cakes": "Tiered cakes, designed with you over a tasting." · "Cookies & Boxes": "Decorated cookies, boxed to give or to match your cake." |
| How ordering works | "1. Tell us your story · 2. We send your design and quote · 3. Pick up your cake." · Note: "Please order at least [X] weeks ahead." |
| Wedding tasting band | "Taste first, then decide." · "Book a tasting and design your wedding cake with us." · CTA: **Book a tasting** |
| Cookie boxes | "A little box of happy." · "Cookie boxes made to match your cake, your colours or just because." |
| Visit the shop | "Come say hello." · `[Street address], Maple Hollow` · `[Opening hours]` |
| Final CTA | "Have a celebration coming up?" · **Order a cake** |
| Footer | See section 5 |

## 7. Brand, visual DNA and photography

**Palette (Concept proposal, from "warm & homemade")**

| Role | Name | Hex |
|---|---|---|
| Page background | Fresh cream | `#FBF4E6` |
| Alt band | Butter | `#F6E3B4` |
| Accent / highlight | Golden butter | `#E9B949` |
| Primary ink | Cocoa | `#3B2618` |
| Secondary text | Toasted brown | `#7A5236` |
| CTA fill | Cocoa `#3B2618` with cream `#FBF4E6` text (contrast ≈ 14:1) | — |
| Soft accent | Strawberry cream | `#E8A598` (used sparingly) |

**Type character:** a warm, soft-cornered serif for headlines (Fraunces / Recoleta feel), a friendly humanist sans for body text, and an optional hand-script accent used only for short notes.

**Photo look:** natural window light from one side, a warm (not orange) grade, creamy highlights, soft shadows, shallow depth of field, flour-dusted wood and linen, hands at work.

**Industry motifs (use consistently):**
1. **Piped-buttercream scallop edge:** the transition between sections.
2. **Kraft cake-box tag with twine:** labels, step numbers and price notes.
3. **Recipe-card notes:** small hand-written-style asides and the order steps.

**A/B/C systems:** summarised in `VISUAL-DNA.md` and finalised before the mockup round.

**Scene list:** `photo-scenes.json` (written at mise en place).

## 8. Downstream functionality

- Order request form: date, servings, occasion, flavours, inspiration upload, contact. Form backend: **builder intake** (e.g. Netlify Forms, since the repo has `netlify.toml`).
- Tasting request: the same form with type = Wedding tasting, or a booking tool. **Builder intake.**
- Payments and deposits: none on the site. **Builder intake.**
- Social links, map embed: placeholders. **Builder intake.**

## 9. Unknowns, restrictions and prohibited claims

- **Unknown (placeholders):** address, phone, email, hours, baker's name, lead time, prices, allergen policy, deposit terms, social handles.
- **Prohibited:** reviews, testimonials with names, star ratings, "award-winning", "since 19xx", "best in town", "organic", "gluten-free" or other dietary or health claims, permit or licence numbers, real place names.
- **Images:** no text, logos or lettering inside photographs; no real or famous people.

## 10. Locked brief, concept summaries, QA status, revision log

- **Locked brief:** pending owner approval of v1.0.
- **Concept summaries:** pending (mockup round).
- **QA status:** intake complete; photos not started.
- **Standing approval:** granted 2026-11-22 for Muse fix requests and follow-ups within an approved brief. New rounds and fact changes still need a yes.

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-11-22 | First draft from discovery rounds A01–A03 |
