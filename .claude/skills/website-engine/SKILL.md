---
name: website-engine
description: "One command for the whole website pipeline: concept, intake, build, polish, images, QA and client showcase. Works out where a project stands, starts at the right stage, then runs site-concept, website-polish-intake-v2, mockup-to-website-v2, website-polish-plus-v2, site-images, site-qa and site-showcase in order, carrying everything forward so nothing is asked twice. Use when someone says website engine, wants a site taken end to end, or wants to resume a site project wherever it left off. Accepts an optional starting stage, e.g. '/website-engine from polish'."
---

# Website engine

This skill runs the website pipeline from start to finish. It does not repeat the stage skills' instructions. At each stage it loads that skill with the Skill tool and follows it completely. The engine decides where to start, moves between stages, keeps a status file and enforces the gates below.

## The stages

| # | Stage | Skill to load | Done when |
|---|-------|---------------|-----------|
| 1 | Concept | `site-concept` | `concept/HANDOFF.md` exists and a mockup is chosen |
| 2 | Intake | `website-polish-intake-v2` | The intake summary is agreed: mockup, photos, facts, exact name, viewport, pages, deliverables |
| 3 | Build | `mockup-to-website-v2` | A multi-page site folder exists and is published and zipped |
| 4 | Polish | `website-polish-plus-v2` | The polished build passes its own screenshot checks |
| 5 | Images | `site-images` | Every photo slot is filled with a fitted image or is listed as a placeholder |
| 6 | QA | `site-qa` | The report has no failures (warnings are listed for the user) |
| 7 | Showcase | `site-showcase` | The presentation page is published |

If a stage's skill is not installed, stop and name it. Do not try to do that stage from memory.

## Step 1: Find the starting stage

If the user named a stage (`from polish`, `from qa`, `just images`), start there.

Otherwise, read `ENGINE-STATUS.md` in the project folder. If it exists, tell the user in one line which stage it was on and resume there.

If there is no status file, look at what exists and start at the first stage not yet covered:

- Nothing but a business name or idea → 1 Concept
- `concept/handoff/` exists, or the user has a mockup image → 2 Intake
- The intake is settled but there is no site folder → 3 Build
- A draft or built site folder exists → 4 Polish
- The site is polished but the photos are soft, reused or placeholders → 5 Images
- The site is finished → 6 QA, then 7 Showcase

If it is unclear, ask one question listing the stages, with the one you suggest first.

## Step 2: Run the stages

For each stage, starting from the one found in Step 1:

1. Load the stage's skill with the Skill tool and follow it fully, including its own approval rules. The site-concept rule that emails go out only with the user's yes always applies.
2. Pass on everything settled earlier: project folder, business name, facts and placeholders, mockup, photo source and role map, viewport, pages, deliverables and the latest site folder or zip. Never ask again for something already settled.
3. Ignore the stage's "Next in line" offer. The engine handles moving on.
4. When the stage is done, update `ENGINE-STATUS.md` (see below). Then give a checkpoint of at most three lines: what the stage produced, any open issues, and the next stage. Ask "Continue to <next stage>?"

**Autopilot:** if the user says "run it all", "autopilot" or similar, skip the checkpoints and keep going. Still stop for anything a stage skill says must be asked first (emails, a new Muse round, changes to business facts, money or accounts), for a QA failure that cannot be fixed, and at the end.

## Gates

- **No build without intake.** Stage 3 never starts until the stage 2 summary is agreed, even if the user starts at "build".
- **QA before showcase.** Stage 7 runs only after stage 6 passes with no failures. If QA fails, fix the problems with the polish rules from stage 4 (load `website-polish-plus-v2` again if needed), rebuild and run `site-qa` again. After three rounds that still fail, stop and show the user what remains.
- **QA again after any change.** If anything in the site changes after stage 6, run stage 6 again before stage 7.
- **Honest status.** Never mark a stage done when its output files don't exist. Write PARTIAL and list what is missing.

## ENGINE-STATUS.md

Keep this file in the project folder and rewrite it at the end of each stage:

```markdown
# Website engine status: <Business name>
Updated: <date>
Current stage: <n> <name>, <in progress | done | blocked: reason>
Autopilot: <on | off>

| Stage | Status | Output |
|-------|--------|--------|
| 1 Concept | done | concept/HANDOFF.md, mockup B chosen |
| 2 Intake | done | intake summary below |
| ... | | |

## Settled facts
Exact name, viewport, pages, deliverables, photo source, real facts versus placeholders.

## Open items
What is still needed from the client, and QA warnings.
```

This is what lets `/website-engine` resume in a later session. Remind the user that cloud sessions are temporary, so the project folder (with this file) should be committed, zipped or downloaded at the end of each session.

## Finish

When stage 7 is done, report in a few lines: the published showcase link, the site zip, QA status, and the "what we need from you" items for the client.
