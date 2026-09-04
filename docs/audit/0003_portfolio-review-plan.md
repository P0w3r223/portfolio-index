# Portfolio Review — Multi-Session Plan

Date: 2026-09-02 (updated twice the same day — fix track closed, then corrected against a
verification pass: see the boxes in §4 and §5, and `0004` §6). **Reconciled 2026-09-03** against
the repositories: four statements below had gone stale because the work landed and the document
did not follow — see §8. **Reconciled again later the same day** — see §9, which is what §8 asked
for and did not itself achieve.
Status: accepted
Author: P0w3r223
Related to: [0002_portfolio-presentation-audit-v2.md](0002_portfolio-presentation-audit-v2.md), `README.md`, ~~13~~ **12** submodules (`infra-docker-workmate` unpinned 2026-09-03, §8 decision 4)

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

- **~~13~~ 12 submodules; 12 published pages** — not 10. *(13 when measured; `infra-docker-workmate`
  was unpinned 2026-09-03, §8 decision 4. It was the one with no page, so the page count stands.)*
  `mini-traceroute` and `auth-log-scan`
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
  rewritten to unify the commit identity, so every
  pre-rewrite hash in this portfolio resolves to nothing. Tree contents are unchanged.)*
- `infra-docker-workmate` is a private submodule with a Polish description, absent from
  the index, 200 commits behind its own origin.

Second pass, over the layers the first pass skipped:

- ~~**CI is green on all 12 repos.**~~ ~~**Corrected 2026-09-02: `doc-extract` has no CI at
  all**~~ — no `.github/workflows/` existed, so its 803 tests ran on no push and the only
  Actions runs were the automatic `pages-build-deployment`. Green was read off a repo list
  without checking whether a workflow was there to be green. The other eleven stood.
  **Closed 2026-09-03** by `doc-extract#6` (`ae0353d`), so the original statement is true again
  — and now verified rather than inferred: all twelve public repositories run a `test` job on
  both `push` and `pull_request`, checked by reading every workflow file rather than a repo list.
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
  *Sharpened 2026-09-03: both **declare MIT in `pyproject.toml`**, and `wroclaw`'s README has a
  `## License` section saying MIT outright. ~~Neither ships a `LICENSE` file~~ — **both do since
  2026-09-03** (`it-job-radar#28`, `wroclaw-air-insights#28`); all twelve now report `spdx_id: MIT`.
  The `LICENSE` file is the only
  surface GitHub reads and the only one that is legally operative. So this is not an omission —
  it is one fact on three surfaces where the silent one is the one that counts, which is this
  review's recurring shape with a legal consequence instead of a presentational one.*
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
| 3 | `auth-log-scan` | #1 ✅ merged | measured 119 px → 0 px; 40 tests, CI green |
| 3 | `doc-extract` | #3 ✅ merged | measured 93 px → 0 px; 806 tests, ruff clean |
| 5 | `doc-extract` | #3 ✅ merged | the footer's 404 replaced by the profile; partial — see below |
| — | `apply-scout` | #23 ✅ merged | the caption reopened below; 62 % on the page, verified live |

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
  ~~**Reopened 2026-09-02.**~~ PR #20 corrected the *table* — all three rows read 62 %. It did not
  correct the **prose beneath it**, which still read *"Completion is 75% rather than 100% because
  **two** of the eight advertisements were taken down"*, against the README's corrected "Three of
  the eight postings produce no deliverable". Verified on the live page. **The flagship's page
  contradicted itself in public**, and marking this done was checking the artifact that was named
  rather than the page.

  **Closed 2026-09-02** by `apply-scout#23`, *"the page explained a completion rate its own table
  stopped reporting"*. Re-verified on the live site 2026-09-03: `docs/index.html` reads
  *"Completion is 62% rather than 100% because three of the eight postings produce no
  deliverable"*, and `curl` against `p0w3r223.github.io/apply-scout/` returns the same. The
  remaining `75%` occurrences in that repository are all historical — decision records and the
  README's own account of the re-record that moved the number — which is what they should be.

## 6. Open items

- ~~Whether `token-budget` gets a page, gets demoted, or gets cut — it is the only project
  with no visual representation.~~ **Settled: demoted, and no page.** `0004` § 5 rejected building
  one — *"a stdlib CLI that proves nothing the other twelve do not"* — and `0005` § 6 declined to
  reopen it, recording instead that its measured finding about cache-read economics is a
  *description* problem for `0006` B6, not an extension one.
- ~~Whether the two unlinked Level B pages get promoted into the profile README~~ — **both are
  linked**, `mini-traceroute` and `auth-log-scan`, in the profile's *Live demos* table. ~~and whether
  Level B stays a separate tier at all now that its pages outclass the flagship's.~~ **This half is
  still open** and is carried as `0006` L3: it is a ranking decision on no new evidence, so `0006`
  § 7 excludes it from the block rather than settling it in a presentation pass.
- ~~Push the six repos holding unpushed commits.~~ **Pushed, not merged** — see §4. Three repos
  hold work on origin branches with no pull request, `pl-jobs-lora`'s seven commits included.
- ~~**`doc-extract` has no CI.**~~ **Closed 2026-09-03**, `doc-extract#6` — 806 passed, 22
  skipped, `ruff` clean. It did not go the siblings' "rebuild the page and fail on any diff"
  route: that check already existed here as `tests/test_site_committed.py`, and a blunt diff
  would have been worse, because the page has two parts that legitimately differ from a rebuild
  — the footer's commit stamp, and the blocks that need a corpus on disk. Simulating a runner
  found the staleness check passes on **no** checkout without `data/`, which is every CI
  checkout; the suite had simply never run where the corpus was absent, because there was no CI.
- ~~Session 4 needs a real device or a proper emulator: `resize_window` is ignored while the
  Chrome window is maximised, so the 375 px measurements came from same-origin iframes.~~
  **Closed, and it had been closed since before this line was written** — found 2026-09-04,
  see [`0006`](0006_session3-4-presentation-block.md) §4.2.
  `wroclaw-air-insights/.claude/skills/verify-published-page/measure_page.py` (committed
  2026-08-14) drives CDP `Emulation.setDeviceMetricsOverride`, takes a URL *or a local path*,
  and its own docstring names the exact trap this line describes. `--widths`, `--marker` and
  `--expect` are all flags; only `--winter` is `wroclaw`-specific and it is opt-in. **Nothing in
  this review knew the instrument existed**, which is the §9 failure running in the unrecorded-
  progress direction rather than the stale-debt one.
- ~~**Action versions lag in eleven repositories**~~ — `checkout@v4` and `setup-python@v5` ran on
  Node 20 and annotated every run with a deprecation warning. `wroclaw-air-insights` was already
  on the current majors, so the portfolio contradicted itself here too. **Decided 2026-09-03:**
  bump all eleven to match it, unpinned, because the tokens are read-only and no secret is
  exposed — pinning here alone would diverge from the sibling that has already migrated.
  **Closed the same day:** all eleven bumped and merged, `it-job-radar` last (`#24`) because
  `#23` already touched its workflow. Twelve of twelve green on `main`. The unpinned half of that
  rationale turned out to be wrong about the one job it applies to most — see §9.

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

The fix track is closed. ~~Two PRs await review (`auth-log-scan#1`, `doc-extract#3`)~~ — both
merged 2026-09-02, and nothing blocked the triage. **Session 1 has since been delivered as
`0004` and executed on both public surfaces** (`#38`, `P0w3r223#1`); this section is kept for
the record rather than as a live handoff. The current handoff is §8.

With one piece of context the plan did not start with — the flagship carries a security
debt. A review of `apply-scout` at HEAD found the evaluation harness genuinely holds up
(both published tables replay byte-identical offline, 188 tests, rate card correct), but
the loop has four real holes, the worst being that it ingests untrusted web content,
reads a model-chosen path with no confinement, and can fetch an arbitrary URL — with the
README's fifteen-item limitations list not naming it. That belongs in the triage's reading
of P3, and in Session 2's extension proposals.

---

## 8. Reconciliation, 2026-09-03

This document was read back against the repositories before any new work began, on the
principle that a plan nobody can trust is worse than no plan. **Four of its statements were
stale, all in the same direction: the work had landed and the document had not followed.**

| Statement | Was | Is |
|---|---|---|
| `apply-scout`'s 75 % caption (§5) | "Reopened 2026-09-02" | closed by `#23`, verified live |
| `auth-log-scan#1`, `doc-extract#3` (§5 table, §7) | "open", "await review" | merged 2026-09-02 |
| "`doc-extract` has no CI" (§4, §6) | open item for Session 2 | closed by `#6`, `ae0353d` |
| Session 1 (§7) | "this is where the next session starts" | delivered as `0004`, executed |

**The mechanism is worth naming, because it is the same one this review keeps finding in the
portfolio itself.** Every one of these was fixed by a pull request whose description said so,
and none of the fixes updated the document that tracked it. That is exactly the failure behind
`doc-extract`'s four conflicting progress figures and `apply-scout`'s twelve-day-stale
completion rate — one fact, several surfaces, and no rule about which one leads. A plan
document is a surface like any other. **Reconcile it before starting a session, not after.**

Nothing found here was wrong when written; §4's measurements and §5's diagnoses all stand.

### Decisions taken 2026-09-03

Four, each with the reasoning that decided it.

1. **`it-job-radar`'s parquet gets the full remap.** The `git_sha` column carries 15 distinct
   hashes across 25 rows and every one dangles after the rewrite, while `manifest.json` names
   snapshot 25 as `de4d944` and the parquet still calls the same event `ea6c199` — so the
   published dataset disagrees with itself about one build. The alternative on the table was
   dropping the column, since the manifest carries the file's contract. Rejected: a portfolio
   whose argument is provenance does not answer a provenance defect by deleting the provenance.
   All 15 were confirmed resolvable in the pre-rewrite mirror before this was agreed, so the
   mapping is recoverable rather than hoped for, and the method is the one already used for the
   four page stamps — pair by tree plus both dates.
2. **Action versions bump in all eleven lagging repositories**, to what `wroclaw-air-insights`
   already runs. Not pinned to SHAs: the tokens are read-only and hold no secret, so pinning
   buys little, and doing it in eleven repos while the twelfth stays unpinned would replace one
   inconsistency with another.
3. **§6.5's table wrapping stays with Session 4** — `pl-review-sense` 7 tables and 0 wrappers,
   `it-job-radar` 1 and 0, `mini-traceroute` 2 and 0. Session 4 owns the family-wide rule and
   Session 5+ touches every repository anyway, so acting now costs three PRs and then three
   more. **Condition attached:** it is carried as a bound checklist item of the Session 4 spec,
   not as prose. The generalisation was written down once and not applied, and deferring it a
   second time without a binding is how it would be lost for good.
4. **`infra-docker-workmate` is unpinned from the portfolio, and its repository is kept.**
   The proposal was to move its contents somewhere safe; the survey found there is nowhere to
   move them *to*, because they already live in their own private repository —
   `P0w3r223/infra-docker-workmate`, 1.17 MB, last pushed 2026-08-21, **200 commits ahead** of
   the pointer this index holds. The portfolio references it in `.gitmodules` and nowhere else;
   `README.md` has never mentioned it. So the submodule is the only thing removed, the
   repository is untouched, and the drift §4 recorded stops being the portfolio's problem.

### The handoff — **spent**

~~In order, and the first is a precondition rather than a step: **this section.** Then the
`doc-extract` submodule pointer, which still names the merged PR's branch; then decisions 4, 1
and 2 above; then **Session 2 proper** — the RAG gap, `doc-extract`'s zero topics,
`car-price-ml`'s reported language, and `apply-scout`'s security debt.~~

All four landed the same day: the pointer in `#41`, decision 4 in `#42`, decision 1 in
`it-job-radar#23`, decision 2 in eleven repositories, and every pointer re-checked in `#43`.
~~Two items are the author's and are not blocked by any of it: the contact details (`0004` §6.1)
and the profile pin.~~ **Both done by the author** — see §9. Session 2 has not started; the
live handoff is §9.

---

## 9. Second reconciliation, 2026-09-03

**§8 has a worked example against itself.** It said reconcile the plan before starting a session,
and the same four-commit series that wrote it reconciled *this* document and left `0004`
asserting two things the repositories contradict. So the rule needs its second half stated:
**reconciling one document is not reconciling the record.** A fact lives on every surface that
names it, and the pass is finished when all of them agree — not when the file you had open does.

### What was stale on the second pass

| Statement | Was | Is |
|---|---|---|
| `0004` §5 — `infra-docker-workmate` "stays a submodule … declined" | unmarked, while §9 of the same file records the reversal | unpinned by `#42` |
| `0004` §4 l. 125 — `apply-scout` "the page still contradicts itself in public … 75 %" | present tense | closed by `#23`, re-verified live |
| `0004` §9 — the parquet's fifteen dangling hashes | present tense | remapped by `it-job-radar#23` |
| §6 above — "Action versions lag in eleven repositories" | present tense | all eleven bumped, twelve green |
| §8's handoff | four next steps | all four landed in `#41`–`#43` |
| Header — "13 submodules" | 13 | 12 |
| `README.md` — "Pinned on profile" | the old six, and "`doc-extract` is not among them" | the pins moved; `car-price-ml` was swapped out |

**The last row is a different failure from the other six and worth separating.** The others went
stale because a pull request landed and the document did not follow. That one went stale because
the *account* changed: the pins are a GitHub setting with no public API, the author set them, and
no commit anywhere records it. A surface that tracks state it cannot see has no mechanism to stay
true — so it should say where the truth lives rather than restate it. `README.md` now names the
set and says it is read from the account, not maintained here.

### What the author closed, and what is left of §6.1

`0004` §6.1 called the contact route the cheapest high-value item in the review, and this document
carried it as blocked on the author. Re-read from the API on 2026-09-03: `email`
(`p0w3r2243@gmail.com`), `bio`, the URL field (the `doc-extract` live site) and *Available for
hire* are **set**, and the pins are the agreed set — `doc-extract, ab-lab, apply-scout,
mlops-car-price, wroclaw-air-insights, it-job-radar`.

~~Three pieces of it are still open, and none is blocked on the author's account alone:~~
**All three settled the same day.**

- ~~**`name` is still null**, so the profile renders as the bare handle `P0w3r223`.~~ **Set** to
  *Piotr Cząstkiewicz*. The profile no longer renders as a bare handle, which was the last part of
  §6.1's original finding still true of the account.
- ~~**The published bio reads *"Open to AI/ ML engineer"***~~ — the wording is the author's and the
  topic is **closed by their decision**. Recorded here only so a later reader does not reopen it as
  a defect: the field is filled and reads as intended.
- ~~**The profile README still carries no contact line.**~~ **`P0w3r223#2`, merged** — and
  verified on `main`, not on the pull request, which is the distinction §8 exists to enforce and
  the one this line got wrong once already. The live file now opens
  `# Piotr Cząstkiewicz — AI Engineer / Data Scientist` with the address two lines under it.
  Placed under the opening paragraph rather than in a `Contact` section at
  the foot: the argument is about a reader with sixty seconds, and at the bottom of the file it is
  found only by someone who already scrolled to the end, which is someone who would have gone
  looking anyway. One line, because there is no LinkedIn and no published CV, and it does not
  restate the roles named directly above it. The heading takes the surname for the same reason the
  `name` field now carries it.

**So §6.1 is closed on every surface** — the account (`name`, `bio`, `email`, the URL field,
*Available for hire*), the pins, and the index a reader actually reads. Zero social accounts
remains true and is not a gap; there are no accounts to link.

*This paragraph has now been written three times: as open, as closed on the strength of a pull
request that had not merged, and as closed against `main`. The middle one is why §9 says what it
says, and it is left visible in the history rather than tidied away.*

### Decisions taken on the second pass

Three, each on a finding the day's green checks did not cover.

1. **`.nojekyll` is restored to the Pages artifact** in `auth-log-scan` and `it-job-radar`, by
   `include-hidden-files: true` on `upload-pages-artifact`. `v4` stopped including hidden files, so
   the bump silently dropped both — the artifact shrank by exactly their 61 bytes. It is inert
   today, because Pages serving an artifact never runs Jekyll at all; the fix is chosen anyway
   because it restores the artifact byte-for-byte and needs no argument about whether the file is
   necessary, whereas deleting it needs that argument to stay true if the source is ever flipped
   back to the legacy branch. Seven siblings serve Pages that way, where the file does matter.
   **The reference repo documents this exact check in a comment** and the check was not repeated
   per repo, which is the reuse error the bump's own rationale invited.
2. **The unpinned rationale in §8 decision 2 is corrected rather than the workflows.** It reads
   "the tokens are read-only and hold no secret". Job-level `permissions:` *replaces* the
   workflow-level set, so the two `deploy` jobs run with `pages: write` + `id-token: write` and
   three unpinned actions inside — the recorded reasoning is wrong about the one job it most
   applies to, and the live site is the asset. This is **not** a regression: `v3`/`v4`/`v5` floated
   too, and pinning two repos while ten stay unpinned trades one inconsistency for another. So the
   record is fixed and the pinning question is reopened on true premises rather than answered on
   false ones. Recorded with it: that job is skipped on pull requests, so `configure-pages@v6` and
   `setup-node@v7` first ran on `main` with no in-portfolio precedent — they were guesses the
   stated rationale did not cover, and they went green.
3. **The published parquet is rewritten by the pinned toolchain, and CI is taught to notice.**
   `created_by` reads `parquet-cpp-arrow 25.0.1`; the project declares `pyarrow>=17,<21` and pins
   `20.0.0`. Benign — same schema, SNAPPY, format 2.6, and the pinned readers parse it — but the
   fixing PR's own premise is that defects enter artifacts *after* they are written, and it was
   itself applied by a writer outside the supported range with nothing able to see it. Widening
   the declared range was the cheaper option and was rejected: it makes the document chase the
   accident. A test asserting `created_by` falls inside the declared range is the same shape as
   `tests/test_committed_dataset.py` and closes the class, not the instance.

### The handoff — **spent, and this line is the point of §9**

~~In order:~~ **All five landed on 2026-09-03.** The list is struck rather than deleted, because
§9 exists to say that a handoff which quietly becomes a record of finished work is how the other
six statements in this document went stale. Reconciled in the same pass that re-pointed the
submodules, rather than in the session after.

*Each line below is marked against the repository's **default branch**, not against a merged-looking
pull request. That distinction is not pedantry here: item 4 was first written up as landed on the
strength of its PR existing, and `main` said otherwise — which is the same error, one document
later, that this section was created to name.*

1. ~~**This section**, and `0004`'s matching corrections.~~ `#44`.
2. ~~**`it-job-radar`** — the three gaps in the new tests (a missing `git` binary raises
   `FileNotFoundError` where the guard exists to skip; the skip and `fetch-depth: 0` are coupled
   only by a YAML comment, so dropping the block leaves a green skip; the manifest is asserted to
   agree with the row it names but not to name the *newest* row), then decision 3 above~~ — `#25`,
   each gap proven red first, 229 passed and the page byte-identical. ~~then its
   two hygiene gaps: `build/` is not gitignored though `drift` writes there, and there is no ruff
   configuration, unlike its siblings.~~ `build/` in `#25`, ruff in `#26` — the portfolio set
   (`E,F,I,UP,B,SIM,RUF` at 100), 24 lines rewrapped by hand and six ambiguous-unicode findings
   ignored per file with the reason, because `×` and `–` are the glyphs the page prints.
3. ~~**Decision 1** — one PR per repo, `auth-log-scan` and `it-job-radar`.~~ `auth-log-scan#3`,
   `it-job-radar#27`. **Verified live rather than reasoned about**: both `.nojekyll` answered 404
   before and answer 200 after, and both pages still serve.
4. ~~**The profile README's contact line**~~ — `P0w3r223#2`, **merged and verified on `main`.**
   The only item in this review that changes what a convinced reader can *do*.
5. ~~Then **Session 2 proper** — the RAG gap, `doc-extract`'s zero topics, `car-price-ml`'s reported
   language, and `apply-scout`'s security debt. **This is where the next session starts.**~~
   **Held 2026-09-03 as [`0005_session2-extensions.md`](0005_session2-extensions.md)**, and marked
   here in the same pass that produced it rather than in the session after — which is the whole
   content of §9. Two of the four are closed: the topics are set (0 → 13) and the language is
   `car-price-ml#21`. The other two are **proposals**, not merged work, which is what §3 commissions
   Session 2 to produce; §10 below records what the survey found on the way and what is still a
   decision.
   The licence is off that list: `it-job-radar#28` and `wroclaw-air-insights#28` shipped the file
   each README and `pyproject.toml` already claimed, and all twelve now report `spdx_id: MIT`.
   What that leaves unowned is the *copyright holder* — ~~every `LICENSE` here names the handle
   `P0w3r223` while the profile now carries a legal name~~. **Closed 2026-09-04**: all twelve name the
   person, applied together rather than by fixing a subset, and read back from the API afterwards. See
   [`0006`](0006_session3-4-presentation-block.md) § 6 decision 2.

~~Two account fields are the author's and block nothing: `name`, and the bio's stray space.~~
Both settled by the author; see above.

### One finding carried into Session 2, sharpened

`wroclaw-air-insights` and `it-job-radar` carry **no licence on GitHub** — `spdx_id` is null on
both, so each is formally all-rights-reserved. That much the earlier note had. What it missed is
that **both declare MIT in `pyproject.toml`, and `wroclaw`'s README has a `## License` section
saying MIT outright.** ~~Neither ships a `LICENSE` file~~ — **shipped the same day**, eleven lines
above this one, in `it-job-radar#28` and `wroclaw-air-insights#28`. *This document therefore
recorded a fix and left its own statement of the defect in the present tense in the same section:
the §11 pattern, inside the section that names it.* The `LICENSE` file is the only surface that is
legally operative. One fact, three surfaces, and the silent one is the one that counts — the same shape
this review has been finding everywhere else, and here it has a legal consequence rather than a
presentational one. The fix is one file per repository.

~~Known and deliberately not acted on: `ab-lab`'s `refresh.yml` was bumped but runs weekly on a
schedule — last run 2026-08-31, before the bump — so no check has exercised it yet.~~ **Exercised
2026-09-04** by `workflow_dispatch` and green — run `33857055959`, `checkout@v7`, `setup-python@v7`
and the full-size re-measure. *This sentence and its twin in `0005` § 9 are one fact on two
surfaces; a first draft of § 11 struck the twin and left this one standing, which is the shape § 11
is written to prevent.*

## 10. Session 2, 2026-09-03

Delivered as [`0005_session2-extensions.md`](0005_session2-extensions.md). §3's contract for this
row — *extend / repackage / remove, with cost and payoff, inside the 1–2 month budget* — is met with
six prioritised items totalling **12–18 days** against that ceiling, plus two variants deliberately
left costed-but-unrecommended rather than dropped, because either would consume most of the budget
alone.

**Reconciliation before it started, per §9.** Every open item this document and `0004` carried was
re-read against the repositories, not against the documents. Nothing was stale this time — the first
pass since §8 was written where that is true — and the one thing the record did not know was that
`current_projects#46` had merged. The merged branch is deleted, and its content was verified present
on `main` by tree equality (`298c13a`) before deleting, because a squash-merge makes `git branch -d`
warn in exactly the way a genuinely unmerged branch does.

### Two findings that came out of reading source the earlier sessions described from outside

- **`apply-scout` already contains three quarters of a retrieval evaluation, and it cannot see its
  own retriever.** Corpus, retriever, generator, grounding metrics and an offline replay harness are
  all present. What is missing is that `evidence_grounding` scores citations *against what the
  retriever returned* — so **the retrieval is the ground truth**, and a miss by `find_evidence` is
  invisible to every metric in the project. The retriever is also the weakest component in it: it
  matches the whole requirement as one literal substring, it does not rank, and the portfolio's
  better matcher (`matching.tokens`, fixed in milestone 17) is wired to the guardrail and the
  harness but **not** to the retriever. This reframes the RAG gap from *build something new* to
  *finish something three quarters built*, and it is why `0005` § 4 recommends the cheap variant.
- **`pl-review-sense` was demoted on its headline.** `0004` § 5 records "TF-IDF against HerBERT on
  PolEmo 2.0 is a textbook exercise". The repository holds 5 607 lines of Python, a paired McNemar
  test, bootstrap intervals, an 80-sentence hand-written Polish adversarial set with its own ADR,
  a cascade cost model and a learning curve — and its page opens with a **claim as the title**,
  the family A pattern, while three Level A projects still open with a repository name. Session 1
  flagged its own uncertainty here in the next paragraph; this makes it concrete. The ranking is
  still defensible; **the recorded reason is not**, and `0005` § 7 puts the options.

### Three items closed ahead of the document

`doc-extract` 0 → 13 topics (it was the only repository with none, and the one the portfolio most
wants found); `auth-log-scan`'s empty `homepage` set, which makes all twelve consistent —
`token-budget` is the one exception and correctly so; and `car-price-ml#21` for the reported
language, green and awaiting merge.

### What is now a decision rather than a finding

Three, all in `0005` § 9: which RAG variant, which security level for `apply-scout`, and what
happens to `pl-review-sense`. ~~**This is where the next session starts**~~ — but unlike every
previous handoff in this document, it starts from a decision the author has to make and not from work
waiting to be done. **All three were decided 2026-09-03 and all three landed by 2026-09-04:** variant
B, B3 staged, and C1 now with C3 into Session 3. See § 11.

---

## 11. Third reconciliation, 2026-09-04 — and it runs in the other direction

Sessions 3 and 4 are designed as one block in
[`0006_session3-4-presentation-block.md`](0006_session3-4-presentation-block.md). This section is
the reconciliation § 9's rule requires before it starts.

**Nine statements across this document, `0004` and `0005` were re-read against the repositories.
Eight were stale; one was not, and the one that was not is the point of this section.**

§ 8 and § 9 both diagnosed the same direction: *work lands, the document does not follow*. This pass
found the mirror image and it is more dangerous, because nothing prompts a check for it:

- **§ 6's "Session 4 needs a real device"** was written while the instrument to close it had been
  committed in `wroclaw-air-insights` for three weeks. Nobody was tracking it, because a *capability*
  arriving is not an item on anyone's debt list.
- **`0004` § 6.5's table-wrapping checklist**, deliberately *bound* to the Session 4 spec by § 8
  decision 3 so it could not be lost, was **two thirds done 43 seconds after the commit that
  recorded it as three open pages** (`pl-review-sense#8` and `it-job-radar#21`, both written for
  this checklist, merged 13:08:00Z and 13:08:20Z on 2026-09-02 against 13:07:17Z) and nothing
  re-read it in the two days since —
  `pl-review-sense` 7/7 and `it-job-radar` 1/1 are wrapped; only `mini-traceroute` 0/2 is open.

**So a handoff that tracks only debt over-scopes the next block, and this one would have by about a
third.** § 9's rule gets its third clause: reconcile in both directions — what went stale *and* what
quietly got done.

### The one statement that survived, and why it is recorded

§ 4's breakpoint line — *"nine of eleven pages carry no width-based breakpoint at all; only `ab-lab`
and `wroclaw-air-insights` have any"* — **is exactly true**, re-measured 2026-09-04: `ab-lab` has
`@media (max-width: 34rem)`, `wroclaw` has `@media (max-width: 640px)`, every other `@media` in the
portfolio is `prefers-color-scheme` or `print`. The architecture pass that produced `0006` reported
this line as stale on the grounds that `wroclaw`'s query is not width-based. **It is.** The
correction is recorded rather than absorbed, because a reconciliation that strikes a true line is
worse than one that misses a false one — the false line is still findable, the struck true one is not.

Also re-measured and standing: `apply-scout` carries **no `@media` rule of any kind** — not
width, not `prefers-color-scheme`, not `print` — and last session measured that its page still does
not scroll sideways at 375 px. Recorded for the § 4.2 divergence table rather than as a defect: a
fluid layout that holds is not the same defect as a fixed one that does not, and the spec should say
which it is asking for.

### The scope of this pass, stated so the next reader knows what was not checked

**Nine named statements were re-read, listed below.** The three documents' *other* open-item and
still-open lists were then swept once for contradictions and four more were found; they are closed
in this same pass and listed after the table. **Anything outside those two passes is unchecked** —
notably the body prose of `0004` §§ 1–5 and of `0005` §§ 1–7, which were read for the statements
named here and not audited line by line.

### What was stale

| statement | was | is |
|---|---|---|
| § 6 — "Session 4 needs a real device or a proper emulator" | open blocker | `measure_page.py`, committed 2026-08-14; see above |
| § 10 / § 9 — "this is where the next session starts", three decisions pending | pending | all three decided 2026-09-03, all three landed by 2026-09-04 |
| `0004` § 3.2 — "family B is exactly the three headline projects" | three | **two**: `apply-scout`'s `h1` has been a claim since `#32` |
| `0004` § 6.4 — "the three most-promoted pages have no social metadata" | three | **four**: `wroclaw-air-insights` carries none either. The `<title>` half of that finding stands on all three named |
| `0004` § 6.5 — the bound wrapping checklist | three open | **one open** (`mini-traceroute` 0/2) |
| `0005` § 8 — priority items 3, 4 and 5 marked "next" / "after B2" | queued | all three on `main` |
| `0005` § 9 — "B2 — confine the loop. **Not started**" | not started | B2 **and** B3 landed; ADR-0012 was written after them |
| `0005` § 9 — `apply-scout` "still opens *Portfolio project P3 (the flagship)*" | open | closed; neither its README nor its `CLAUDE.md` says it |

### One figure that is still wrong, and it is the flagship's

`0004` § 3.3 found three figures for `doc-extract`'s progress: the index's `M2 of 7`, the
README / `CLAUDE.md` / page-eyebrow *"milestones 1–6 of 7"*, and the page's KPI tile `5 / 7`. **Only
the index's was fixed.** Re-measured 2026-09-04: the index now reads `M6 of 7`, and the tile still
reads `5 / 7` — twenty-six lines below an eyebrow on the same page saying *"milestones 1–6 of 7, and
most of the seventh"*. One page, two numbers for one fact.

*The tile was in § 3.3's count from the start; an earlier draft of this section claimed it was a
fourth surface nobody had counted. It was not, and the claim is corrected rather than removed — the
finding does not need inflating, because what makes it `0006`'s H1 is not that it went unnoticed but
that **it is a false statement on the flagship's page about the measurement that made it the
flagship**: the tile's note reads "the gate is measured; injection and the real set are not", and
`CLAUDE.md` carries M6's `attack/` and M7's `raster.py`, `foreign/`, `degrade/`, `place.py`,
`joint.py` and `complete.py` as shipped.*
