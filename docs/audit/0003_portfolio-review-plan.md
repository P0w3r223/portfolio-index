# Portfolio Review — Multi-Session Plan

Date: 2026-09-02
Status: accepted
Author: P0w3r223
Related to: [0002_portfolio-presentation-audit-v2.md](0002_portfolio-presentation-audit-v2.md), `README.md`, 13 submodules

---

## 1. The commission

Review the whole portfolio — this index repo, all 13 project repos, and every published
live site — and judge it **as a recruiter with many applicants and no time**: someone who
wants to see the result of the work and what it means, immediately, without digging.

Three deliverables were asked for:

1. Are the live sites stylistically consistent with each other?
2. Are the descriptions short — but still specific? (Today several are not.)
3. Which projects are the *limiting* part of the portfolio, and how should they be extended?

## 2. Decisions taken before starting

| Question | Decision |
|----------|----------|
| Order of work | **Triage first**, then extensions, then descriptions, then visual consistency |
| Scope of "descriptions" | All four layers: index README, GitHub About + topics, per-project READMEs, live-site headers |
| Deliverable shape | A document per session for approval; implementation lands separately as PRs |
| Target roles | AI Engineer **and** Data Scientist, weighted equally |
| Time available for building | 1–2 months |
| How far cuts may go | Everything on the table — deleting repos, demoting the flagship, striking the paused A5 |
| **End state for presentation** | **Every project carries its own visual representation.** A project with no page, or a page with nothing to look at, is not finished |
| **Devices** | **Desktop and mobile both count.** A recruiter opens the link from a phone as often as from a laptop, so a page that only holds together at 1440 px has not passed |

### Why the order was inverted

The commission listed sites → descriptions → extensions. That order polishes artifacts
that triage may remove. Curation is the cheapest lever and it constrains everything after
it: there is no point agreeing a one-line description for a project that should drop to
Level B, or unifying the CSS of a page that should stop being linked. Cut first, then
write, then style.

**Exception.** The reconnaissance (§5) found defects that are not curation questions — a
form that crashes for every visitor and a flagship whose only visual is invisible. Those
are fixed on their own track, independent of triage, because no ordering argument makes a
broken page worth leaving broken.

## 3. Session breakdown

Each row is a separate session with its own context. Sessions 5+ are several sessions.

| # | Session | Scope | Output |
|---|---------|-------|--------|
| 0 | Scoping + reconnaissance | Commission, constraints, order; measured survey of every public surface | this document |
| 1 | Recruiter triage | All 13 repos ranked by 60-second recruiter value; keep / demote to Level B / cut; gaps in the stack for AI Engineer + DS | Ranking with reasons |
| 2 | Extensions | For each limiting project: extend / repackage / remove, with cost and payoff, inside the 1–2 month budget | Prioritised proposals |
| 3 | Descriptions | One length standard applied across all four layers; rewritten text ready to paste | Index PR + copy for submodules |
| 4 | Live-site inventory | Divergence table across all 12 pages, **at desktop and at 375 px**; one design spec covering layout, typography, KPI tiles and table overflow | Spec + divergence table |
| 5+ | Spec rollout | One PR per repo, batched 2–3 repos per session | PRs |

## 4. Measured starting facts

Everything in this section was measured on 2026-09-02, not assumed.

- **13 submodules; 12 published pages** — not 10. `mini-traceroute` and `auth-log-scan`
  both shipped sites (`feat(docs): add an interactive live site for the trace`,
  `feat(site): publish a generated demo page on GitHub Pages`) that **neither the index
  nor the profile README links**. `token-budget` returns 404 — it is the one project with
  no visual representation at all.
- All 12 pages return 200 anonymously.
- **The index repo is private.** `current_projects` is not public, so the README this
  review started from is invisible to recruiters. The public index is the profile README,
  which is in noticeably better shape: short, specific rows in a "Start here" table.
- **The pages fall into two families**, and the split is not cosmetic:

  | | Family A (9) | Family B (3) |
  |---|---|---|
  | Theme | dark | light |
  | `h1` | a claim with a number | the repo name |
  | Eyebrow + KPI tiles | present | absent |
  | Evidence | 4–11 inline SVG charts | tables only |
  | Type | system font stack | Inter, from the Google CDN |
  | Who | it-job-radar, car-price-ml, pl-review-sense, ab-lab, doc-extract, auth-log-scan, mini-traceroute, *(wroclaw partially)* | **apply-scout, mlops-car-price, pl-jobs-lora** |

  Family B is P3 (the flagship), P1 and P4 — the three projects the index sells hardest.
  Two Level B side projects present better than the flagship does.
- **Outliers inside family A**: `wroclaw-air-insights` has the eyebrow and the dark theme
  but no KPI tiles and a six-line lead; `mini-traceroute` and `wroclaw` use a descriptive
  `h1` rather than a claim; `auth-log-scan` runs five KPI tiles where the rest run four.
- **Mobile, measured at a 375 px viewport.** Four pages force horizontal scrolling:
  `apply-scout` **+518 px** (an 852 px table), `mlops-car-price` +140 px, `auth-log-scan`
  +119 px, `doc-extract` +93 px. `apply-scout` and `mlops-car-price` carry **zero** media
  queries. The fix already exists in the portfolio — `pl-jobs-lora` has an 826 px table
  and does *not* overflow, because it wraps it in `overflow-x`.
- **About descriptions overflow the pinned card**, which truncates near 150 characters.
  8 of 12 repos exceed it; `ab-lab` (281 chars) is cut at "each m…", `car-price-ml` (279)
  at "Every …". `doc-extract` carries **zero topics**, against the index's own convention.
- **`doc-extract` is described by three different numbers**: the index says `M2 of 7` and
  "milestones 3–7 … are not built", the page eyebrow says "milestones 1–6 of 7, and most
  of the seventh", the KPI tile says "5 / 7". The index understates the project.
- **Index submodule pointers lag origin** by 32 (`doc-extract`), 27 (`apply-scout`), 18,
  14, 14, 12 commits. The live pages are current — the pointers are not. Separately,
  **`pl-jobs-lora` has 7 commits that were never pushed**, plus 1–2 each in `wroclaw`,
  `ab-lab`, `apply-scout`, `pl-review-sense` and `doc-extract`.
- `infra-docker-workmate` is a private submodule with a Polish description, absent from
  the index, 200 commits behind its own origin.

Second pass, over the layers the first pass skipped:

- **CI is green on all 12 repos.** Every link in the profile README resolves (15/15). The
  index's single 404 points into the private repo, so no reader can reach it anyway.
- **Only one page has a JavaScript error** — the valuation form. Verified rather than
  assumed: the console-reading method was first proven against that known exception, then
  applied to the other nine pages, which came back clean.
- **No page links anywhere else in the portfolio.** Zero of eleven link to the profile;
  two link to one sibling project. Every live site is a dead end, so a recruiter who
  arrives at one has no route to the rest.
- **Two repos carry no licence** (`wroclaw-air-insights`, `it-job-radar`); the other ten
  are MIT. Without one, a repo is formally all-rights-reserved.
- **`car-price-ml` reports its main language as Jupyter Notebook** — visible on the pinned
  card. For an ML/AI Engineer reader it says "notebooks" about a project that has a
  FastAPI service and a Docker image.
- **Project READMEs range from 99 to 674 lines** (`doc-extract` 674, `apply-scout` 431,
  `mlops-car-price` 405). Most open with a bold claim, which is the right pattern.
  `auth-log-scan` opens with a demo link instead, and `token-budget` opens with no claim
  at all.

## 5. Defects found during reconnaissance

Fixed on their own track, ahead of triage.

| # | Defect | Location | Effect |
|---|--------|----------|--------|
| 1 | `probeBackend()` returns `"absent"`, but `states` only defines `api` and `browser`; `states["absent"]` is `undefined` and `renderStatus` throws inside `init()` | `car-price-ml/docs/app/app.js:153` | The valuation form — the portfolio's only interactive element — never finishes loading and the submit button stays disabled. **Deterministic: every visitor, every time**, because GitHub Pages has no API to probe |
| 2 | `demo.svg` animates its 55 `<text>` nodes from `opacity: 0` via CSS `@keyframes`, but is embedded with `<img>`; Chrome does not run CSS animations in SVG-as-image | `apply-scout` page | The flagship's only visual is a permanently black rectangle. Opened directly the same file plays correctly and is the strongest artifact in the portfolio |
| 3 | Four pages overflow a 375 px viewport; two carry no media queries at all | see §4 | Tables run off-screen on a phone, worst on the flagship |
| 4 | `autostart()` starts a `requestAnimationFrame` animation as soon as the tab is visible | `mini-traceroute/assets/app.js:544` | Held the render thread busy enough that screenshot injection timed out repeatedly. Not proven to harm a human visitor; the real cost is CPU and battery on a phone. **Needs confirmation on a real device before it is called a defect** |
| 5 | No page links to the profile or to any sibling project | all 11 pages | Every live site is a dead end. The portfolio reads as twelve unrelated artifacts rather than one body of work — which is the opposite of what the "own visual representation" goal is for |

### Fix order

1. **Defect 1** — the form crashes for every visitor; nothing else competes.
2. **Defect 2** — the flagship's only visual.
3. **Defect 3** — `overflow-x` on the four overflowing pages; the pattern already exists in
   `pl-jobs-lora` and only needs copying.
4. **Defect 5** — a shared footer linking back to the profile. Cheap, and it is the piece
   that turns twelve pages into one portfolio.
5. **Defect 4** — measure on a real phone first; do not change code on the strength of a
   screenshot timeout.

### Fix status (2026-09-02)

Committed locally, **nothing pushed**. Each carries a test or a measurement, because a fix
without evidence that it catches the regression is only a hope.

| Defect | Repo / branch | Evidence |
|--------|---------------|----------|
| 1 | `car-price-ml` / `fix/valuation-form-absent-backend` | the guard fails on the unfixed source and names `absent`; 164 tests, ruff clean |
| 2 | `apply-scout` / `fix/page-defects` | animation confirmed playing in Chrome; a test now reads the embed |
| 3 | `apply-scout` / `fix/page-defects` | measured 518 px → 0 px at 375 px |
| 3 | `mlops-car-price` / `fix/table-overflow-on-phones` | measured 140 px → 0 px; 111 tests, ruff clean |

Two corrections worth keeping, both cases of a method lying rather than a page:

- `<object>` first tested black, which nearly discarded the right fix. The test was at
  fault — an `<object>` inserted through `innerHTML` never initialises its nested
  document. Re-run with `createElement`, it plays.
- `nowrap` was **not** carried from `apply-scout` to `mlops-car-price`: measured there it
  widened the tables ~40% for no gain, because one column holds a sentence rather than a
  number. The shape transfers between the sibling pages; the detail does not.

Still open on this track:

- `doc-extract` (+93 px) and `auth-log-scan` (+119 px) both **already have** `overflow-x`,
  so their cause differs from `apply-scout`'s and neither was touched without diagnosing
  it. `auth-log-scan` generates its page from `site/build.py`, so the fix belongs in the
  generator; `doc-extract` sits on a branch with work in progress.
- ~~The flagship's README shows the same black rectangle.~~ **Done** — `apply-scout`
  `feat/demo-gif`, PR #22. The same cast now renders twice: `demo_gif.py` imports the
  layout, timing and palette from `demo_svg` rather than restating them, so the two
  pictures cannot become two accounts of one run. The font is vendored, because left to a
  system font the command would draw a different picture on every machine. Costs ~900 KB
  (564 KB GIF, 340 KB font). The test pins frame count and geometry to the cast, not
  bytes — a rasteriser may differ between CI and a laptop, but a stale picture beside a
  re-recorded run may not. Verified GitHub serves the file byte-identical, 20 frames,
  animated; **not** verified visually in a browser, where screenshots on that page timed
  out repeatedly and canvas reads are blocked cross-origin.
- `apply-scout`'s published table still reads 75% completion; the correction to 62% sits
  in open PR #20, unmerged since 2026-08-21.

## 6. Open items

- Whether `token-budget` gets a page, gets demoted, or gets cut — it is the only project
  with no visual representation.
- Whether the two unlinked Level B pages get promoted into the profile README, and whether
  Level B stays a separate tier at all now that its pages outclass the flagship's.
- Push the six repos holding unpushed commits, `pl-jobs-lora` first.
- Session 4 needs a real device or a proper emulator: `resize_window` is ignored while the
  Chrome window is maximised, so the 375 px measurements came from same-origin iframes.
