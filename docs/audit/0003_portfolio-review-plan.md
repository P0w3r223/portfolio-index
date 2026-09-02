# Portfolio Review — Multi-Session Plan

Date: 2026-09-02 (updated twice the same day — fix track closed, then corrected against a
verification pass: see the boxes in §4 and §5, and `0004` §6)
Status: accepted
Author: P0w3r223 + Claude
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
  ~~but no KPI tiles~~ — **corrected: it has four**, under a third class name (`.stat`, against
  `.kpi` on six pages and `li.tile` on `ab-lab`). It was recorded as lacking tiles because the
  survey looked for one convention. Three naming conventions is itself the finding, and it is
  what the Session 4 spec has to unify — and a six-line lead;
  `mini-traceroute` and `wroclaw` use a descriptive
  `h1` rather than a claim; `auth-log-scan` runs five KPI tiles where the rest run four.
- **Mobile, measured at a 375 px viewport.** Four pages force horizontal scrolling:
  `apply-scout` **+518 px** (an 852 px table), `mlops-car-price` +140 px, `auth-log-scan`
  +119 px, `doc-extract` +93 px. ~~`apply-scout` and `mlops-car-price` carry **zero** media
  queries.~~ **Corrected: nine of eleven pages carry no width-based breakpoint at all** — only
  `ab-lab` and `wroclaw-air-insights` have any; every other `@media` in the portfolio is
  `prefers-color-scheme`, `print` or `prefers-reduced-motion`. Naming two pages made this look
  like an outlier when it is the norm, which would have mis-scoped the Session 4 spec.
  The fix already exists in the portfolio — `pl-jobs-lora` has an 826 px table
  and does *not* overflow, because it wraps it in `overflow-x`.
- **About descriptions overflow the pinned card.** ~~which truncates near 150 characters.
  8 of 12 repos exceed it~~ **Corrected: the truncation point is 191 characters**, which is
  where both worked examples actually cut — `ab-lab` (281 chars) at "each m…" and
  `car-price-ml` (279) at "Every …". At 191 the count is **4 of 12**, not 8. The document's own
  two examples contradicted its stated threshold.
  `doc-extract` carries **zero topics**, against the index's own convention.
- **`doc-extract` is described by three different numbers**: the index says `M2 of 7` and
  "milestones 3–7 … are not built", the page eyebrow says "milestones 1–6 of 7, and most
  of the seventh", the KPI tile says "5 / 7". The index understates the project.
- **Index submodule pointers lag origin.** ~~by 32 (`doc-extract`), 27 (`apply-scout`), 18,
  14, 14, 12 commits~~ — **corrected: twelve of thirteen lag**, not six. Only `token-budget` is
  current. Measured 2026-09-02: `doc-extract` 38, `apply-scout` 34, `pl-review-sense` 18,
  `it-job-radar` 12, `ab-lab` 7, `pl-jobs-lora` 5, `car-price-ml` 4, `mlops-car-price` 4,
  `auth-log-scan` 3, `mini-traceroute` 2, `wroclaw` 1, `infra-docker-workmate` 200.
  The live pages are current — the pointers are not. Separately,
  **`pl-jobs-lora` has 7 commits that were never pushed**, plus 1–2 each in `wroclaw`,
  `ab-lab`, `apply-scout`, `pl-review-sense` and `doc-extract`.
  **Pushed is not merged.** Those commits are all on origin now, but `pl-jobs-lora`'s seven sit
  on `feat/raise-decoding-cap` with **no pull request**, and its `main` has not moved since the
  metric-corrections merge; `pl-review-sense` and `wroclaw` are the same shape. §6 recorded this
  as done, which was true of the push and false of the visibility. *(That commit was named here
  by hash. The hash is not repeated: on 2026-09-02 the history of all thirteen repositories was
  rewritten to drop the Claude co-author trailer and unify the commit identity, so every
  pre-rewrite hash in this portfolio resolves to nothing. Tree contents are unchanged.)*
- `infra-docker-workmate` is a private submodule with a Polish description, absent from
  the index, 200 commits behind its own origin.

Second pass, over the layers the first pass skipped:

- ~~**CI is green on all 12 repos.**~~ **Corrected 2026-09-02: `doc-extract` has no CI at
  all** — no `.github/workflows/` exists, so its 803 tests run on no push and the only
  Actions runs are the automatic `pages-build-deployment`. Green was read off a repo list
  without checking whether a workflow was there to be green. The other eleven stand.
  Every link in the profile README resolves (15/15). The
  index's single 404 points into the private repo, so no reader can reach it anyway.
- **Only one page has a JavaScript error** — the valuation form. Verified rather than
  assumed: the console-reading method was first proven against that known exception, then
  applied to the other nine pages, which came back clean.
- **No page links anywhere else in the portfolio.** Zero of eleven link to the profile;
  two link to one sibling project. Every live site is a dead end, so a recruiter who
  arrives at one has no route to the rest.

  Re-measured 2026-09-02 over the published pages only — a survey of the whole `docs/`
  tree produces false hits, because `apply-scout`'s ADRs discuss a *hallucinated* profile
  URL its guardrail caught. Confirmed: `doc-extract` → `current_projects` and
  `pl-jobs-lora` → `it-job-radar`, and nothing else. **`doc-extract`'s link was a 404** —
  it pointed at the index repository, which is private, so the one route off that page
  answered every visitor with an error. A dead way back is worse than none; it reads as a
  portfolio that has been taken down. Fixed to the profile in `doc-extract#3`.
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
   that turns twelve pages into one portfolio. *(Note the fix named here is the profile
   link only; sibling-project navigation is diagnosed above but never specified. See §7 —
   "Back-navigation: what was planned, and what was not".)*
5. **Defect 4** — measure on a real phone first; do not change code on the strength of a
   screenshot timeout.

### Fix status — **the track was closed too early** (2026-09-02)

> **Correction, same day.** A verification pass found this track was closed on four pages while its
> own diagnosis predicted more. Measured live: `pl-review-sense` has **7 tables and 0 wrappers**,
> `it-job-radar` 1 and 0, `mini-traceroute` 2 and 0. They do not overflow *today* only because they
> happen to be narrow — the exact condition this document warns about two paragraphs below. The
> generalisation was written down and then not applied. Also reopened: `apply-scout`'s 75 % caption,
> at the end of this section.
>
> Four numbers in §4 are wrong and are corrected there. The measurements in the table below were
> re-checked and stand.

Every fix carries a test or a before/after measurement, because a fix without evidence that
it catches the regression is only a hope.

| Defect | Repo | PR | Evidence |
|--------|------|----|----------|
| 1 | `car-price-ml` | #18 ✅ merged | the guard fails on the unfixed source and names `absent`; 164 tests, ruff clean |
| 2 | `apply-scout` | #21 ✅ merged | animation confirmed playing in Chrome; a test now reads the embed |
| 2 | `apply-scout` | #22 ✅ merged | the README's GIF, rendered from the same cast as the SVG |
| 3 | `apply-scout` | #21 ✅ merged | measured 518 px → 0 px at 375 px |
| 3 | `mlops-car-price` | #15 ✅ merged | measured 140 px → 0 px; 111 tests, ruff clean |
| 3 | `auth-log-scan` | #1 — open | measured 119 px → 0 px; 40 tests, CI green |
| 3 | `doc-extract` | #3 — open | measured 93 px → 0 px; 806 tests, ruff clean |
| 5 | `doc-extract` | #3 — open | the footer's 404 replaced by the profile; partial — see below |

**One diagnosis, three repos.** `auth-log-scan` and `doc-extract` were scoped below as
having a cause *different* from `apply-scout`'s, on the grounds that both "already have
`overflow-x`". They do not differ — the cause is identical. In all three the two existing
`overflow-x` are `.chart-wrap` and `pre`, and **no table was ever wrapped**. This is one gap
in the pattern family A's pages are generated from, not three independent bugs, and it
belongs in the Session 4 spec rather than being re-derived per repo. Family B pages will
have it too wherever their tables happen to be narrow enough not to show it yet.

`doc-extract` applies the wrapper to the *assembled page* in `build()` rather than at each of
thirteen call sites, and asserts the two premises that makes safe (bare `<table>`, no
nesting) — the tables are literal strings scattered through a 2000-line generator, and the
fourteenth would otherwise be written unwrapped.

Two corrections worth keeping, both cases of a method lying rather than a page:

- `<object>` first tested black, which nearly discarded the right fix. The test was at
  fault — an `<object>` inserted through `innerHTML` never initialises its nested
  document. Re-run with `createElement`, it plays.
- `nowrap` was **not** carried from `apply-scout` to `mlops-car-price`: measured there it
  widened the tables ~40% for no gain, because one column holds a sentence rather than a
  number. The shape transfers between the sibling pages; the detail does not.

Two measurement defects found while closing this track, both worth keeping because both
would have sent the next person the wrong way:

- **The 384 px reading for `doc-extract` was a probe defect, not a mystery.** The note below
  was right that 384 px cannot account for a 468 px scroll width. The reason is that 384 px
  is the *fifth* table; the probe stopped at the first one over the threshold and never
  reached the 448 px one below it. `20 px` of body padding plus 448 is 468 exactly, with
  nothing left to explain. Filtering on `getBoundingClientRect().right` rather than on
  element width is necessary but was not sufficient — the probe also has to keep looking.
- **A survey of `docs/` is not a survey of the page.** See §4.

~~Still open on this track:~~ **resolved.**

- ~~`doc-extract` (+93 px) and `auth-log-scan` (+119 px) both **already have** `overflow-x`,
  so their cause differs from `apply-scout`'s.~~ They do not — see above. `auth-log-scan`'s
  fix went into `site/build.py` as expected; `doc-extract`'s branch was settled first
  (`doc-extract#2`, merged: M7k plus the generalisation of `tier`/`template` into
  corpus-declared `facets`, which is groundwork M7's real held-out set needs).
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
- ~~~~`apply-scout`'s published table still reads 75% completion.~~ **Done** — PR #20 merged.~~
  **Reopened 2026-09-02.** PR #20 corrected the *table* — all three rows read 62 %. It did not
  correct the **prose beneath it**, which still reads *"Completion is 75% rather than 100% because
  **two** of the eight advertisements were taken down"*, against the README's corrected "Three of
  the eight postings produce no deliverable". Verified on the live page. **The flagship's page
  contradicts itself in public**, and marking this done was checking the artifact that was named
  rather than the page.

## 6. Open items

- Whether `token-budget` gets a page, gets demoted, or gets cut — it is the only project
  with no visual representation.
- Whether the two unlinked Level B pages get promoted into the profile README, and whether
  Level B stays a separate tier at all now that its pages outclass the flagship's.
- ~~Push the six repos holding unpushed commits.~~ **Pushed, not merged** — see §4. Three repos
  hold work on origin branches with no pull request, `pl-jobs-lora`'s seven commits included.
- **`doc-extract` has no CI.** A public repo with 803 tests that run on no push, and the
  one repo where a reader who looks would find no green check at all. Cheap to add; belongs
  in Session 2's proposals rather than in the closed fix track, because the same question —
  *what does each repo prove to someone who opens it* — is what that session is for.
- Session 4 needs a real device or a proper emulator: `resize_window` is ignored while the
  Chrome window is maximised, so the 375 px measurements came from same-origin iframes.

## 7. Next session

Start here. The reconnaissance does not need repeating — everything below is measured.

### Before anything else — **done**

~~Five PRs are open and none is merged.~~ All merged 2026-09-02, including
**`apply-scout#20`**, which had been open since 2026-08-21 and left the published table
overstating completion at 75% instead of 62%.

### The three remaining fixes — **two done, one deliberately split**

1. ~~**`auth-log-scan` — +119 px.**~~ **Done**, PR #1. The premise was wrong: it does have
   `overflow-x` twice, but on `.chart-wrap` and `pre` — *no* table was wrapped, so there was
   no table that had "fallen out of a rule". Both tables wrapped, not only the overflowing
   one; the second fits in exactly 335 px, which is a property of the demo log rather than
   of the layout. 119 → 0 px. The five-KPI-tile divergence was left alone: that is a
   Session 4 question, not a defect.

2. ~~**`doc-extract` — +93 px.**~~ **Done**, PR #3. Same cause, same fix. See §5 for the
   probe defect behind the 384 px reading.

3. **Back-navigation — split, and only the broken half is done.** See below.

Deferred on purpose: `mini-traceroute`'s `requestAnimationFrame` autostart. It repeatedly
froze screenshot injection, but that is a tooling symptom. Measure it on a real phone
before touching the code.

### Back-navigation: what was planned, and what was not

Worth stating plainly, because the plan was vaguer here than it looks. Project-to-project
navigation — *from `it-job-radar`'s page to another project's page* — appears in this
document exactly twice, and is **specified in neither**:

- §5 names it in the *diagnosis*: "No page links to the profile **or to any sibling
  project**."
- §5's fix order then drops it: "a shared footer linking back to **the profile**."
- §7 restored it only as a wish: "linking to the profile, **and ideally** to the sibling
  projects."

No target list, no pattern, no answer to what happens when triage cuts a project. So: it is
**recorded as a goal and never designed**. That gap is what the rest of this section closes.

**What is done.** Only the defect: `doc-extract`'s footer pointed at the *private* index
repo, so its one outbound link was a 404 for every reader. Now the profile. Nothing else
was touched.

**Why the rest waits for the spec.** Three reasons, in order of weight:

1. **The content depends on triage.** A sibling link written now names a project Session 1
   may demote or cut, and the page carrying it is not the page that changes — eleven others
   are.
2. **A mesh is shared state across twelve independent repositories.** Twelve pages each
   naming eleven siblings is 132 links with no single source of truth, in a portfolio whose
   documented failure mode is exactly this: stale submodule pointers, three different
   numbers for `doc-extract`'s progress, a completion figure that stayed wrong for twelve
   days. Hand-maintained cross-links would drift the same way, and a cut project would
   leave eleven 404s.
3. **Session 5+ touches every repo anyway.** Doing it now means eleven PRs, then eleven more
   when the spec lands.

**The shape recommended for the spec — hub and spoke, not mesh.** Every page carries one
link back to the **profile**, whose README is the index. One target, one string per repo,
nothing to drift, and it survives triage untouched: cutting a project changes the profile
README and no page. That is the cheap piece the plan always meant, and it is what turns
twelve artifacts into one body of work.

Project-to-project links stay **editorial, not navigational** — used only where two projects
genuinely bear on each other and the link says why. That pattern already exists and reads
well: `pl-jobs-lora` → `it-job-radar` (the job data it fine-tunes on), `mlops-car-price` ↔
`car-price-ml`, `mlops-car-price` → `ab-lab`'s paired-bootstrap decision record. Those are
arguments, not a menu, and they do not rot when a *different* project is cut.

If Session 4 wants a genuine "next project" control anyway, the open question it must answer
first is **where the list lives** — a hand-written strip in twelve repos will drift, so it
needs generating from one declaration, and the repos have no shared build step. That is a
real design problem and it should not be solved by pasting a list eleven times.

### How the mobile numbers were taken

`resize_window` reports success and does nothing while the Chrome window is maximised —
`window.innerWidth` stays put, so anything measured that way is worthless. What worked was
a same-origin iframe at 390 px, comparing `documentElement.scrollWidth` against
`clientWidth`. The same harness applied the fix live and re-measured, which is where the
518 px → 0 and 140 px → 0 figures come from.

### Then: Session 1, the triage — **this is where the next session starts**

The fix track is closed. Two PRs await review (`auth-log-scan#1`, `doc-extract#3`) and
nothing blocks the triage.

With one piece of context the plan did not start with — the flagship carries a security
debt. A review of `apply-scout` at HEAD found the evaluation harness genuinely holds up
(both published tables replay byte-identical offline, 188 tests, rate card correct), but
the loop has four real holes, the worst being that it ingests untrusted web content,
reads a model-chosen path with no confinement, and can fetch an arbitrary URL — with the
README's fifteen-item limitations list not naming it. That belongs in the triage's reading
of P3, and in Session 2's extension proposals.
