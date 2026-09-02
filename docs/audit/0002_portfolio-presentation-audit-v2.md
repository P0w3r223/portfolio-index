# Portfolio Presentation Audit — Execution Plan (v2)

Date: 2026-08-14
Status: proposed
Author: P0w3r223 + Claude
Related to: supersedes [0001_portfolio-presentation-audit.md](0001_portfolio-presentation-audit.md)

---

## 1. Why there is a v2

Plan 0001 was reviewed before execution. Its measured baseline for the pages (§4.1 two
families, §4.2 titles) was re-derived cell by cell and is exact — it carries forward. But
three premises underneath the plan were wrong, and each of them would have surfaced as
rework mid-execution:

1. **The index repo is private.** `current_projects` returns `"private": true`, and an
   anonymous fetch of `github.com/P0w3r223/current_projects` returns **404**. Plan 0001
   read its About fields through an authenticated API call, so visibility never appeared,
   and then built an entire layer (L1) and a phase (Phase 3) on a page no reader can open.
2. **The public index is the profile README**, which 0001 never inspected. It is public,
   lists every project, links every demo, and does *not* link `current_projects`. It is
   the page the 60-second reader actually reads.
3. **All three Phase 2 pages are generated, and two of them are CI-gated.** 0001 named
   only wroclaw as generated, and described the failure mode as "overwritten by the next
   run". For `it-job-radar` and `car-price-ml` the real failure mode is an immediately red
   PR — see §6.5.

The link-check criterion also passed while broken: run from an authenticated machine it
returns 200 on private-repo URLs that 404 for everyone else.

---

## 2. Corrected map of the presentation chain

There are **two indexes**, not one, and 0001 audited only the private one.

```
L0  Profile README      github.com/P0w3r223 — PUBLIC. The real index.
L1  Working index       current_projects — PRIVATE (404 anonymously). Planning tool.
L2  Repo About          description · website · topics · license
L3  Repo README         first screen: claim, live link, what it proves
L4  Live page           title · meta · structure · visual style   ← source of truth
L5  Repo internals      folder names, docs/ layout, publish path
```

**The `live_site` chain, corrected.** One claim, now **four** renderings: L4 title →
L2 description → L0 profile row → L1 index line. L0 was missing from 0001's chain, and it
is the one that drifted furthest:

> The profile README describes `car-price-ml` as *"The full ML cycle end-to-end: EDA,
> feature engineering, model comparison, SHAP, and a FastAPI + Docker prediction
> service."* — the framing the repo's own README and About abandoned. The page's claim is
> that the model **refuses the cars it cannot price**. The reader meets the discarded
> version first.

Same layer, second defect: the profile's "Start here" table promotes apply-scout,
mlops-car-price, ab-lab and car-price-ml. `wroclaw-air-insights` and `it-job-radar` — A1
and A2, two of the three projects in scope — appear only in the lower "Live demos" table,
as a one-noun label ("Data engineering").

---

## 3. Baseline corrections

Carried forward from 0001 unchanged: **§4.1** (two page families — two repos with full
meta/dark/SVG, six with none, Google Fonts and raster images) and **§4.2** (only
it-job-radar and car-price-ml open with a finding). Both re-verified.

Corrected or newly found:

| # | Fact | Consequence |
|---|------|-------------|
| 3.1 | `current_projects`, `student-wellbeing-pwr`, `infra-docker-workmate` are **private** | Two links in the index README 404 anonymously; A7 is typeset "✅ Live" while invisible |
| 3.2 | Profile README is public and is the real index (§2) | L0 gets criteria and its own phase |
| 3.3 | `it-job-radar` CI job `drift` runs `diff -u docs/index.html build/site/index.html`; `car-price-ml` CI runs `site.build` then `git diff --exit-code` | Hand-editing published HTML turns the PR red immediately |
| 3.4 | `wroclaw` `refresh.yml` triggers only on `schedule: 0 5 * * *` and `workflow_dispatch` — **no `push`** | Merging a generator change does not republish; needs a manual dispatch |
| 3.5 | That dispatch re-pulls GIOŚ data and retrains | Republishing moves the figures — no bare number may be copied into About or the index |
| 3.6 | `docs/` is the Pages root in two repos, so ADRs are already published: `…/it-job-radar/adr/0001_…md` → 200 | Moving `docs/adr` breaks live URLs, which §6.1 forbids |
| 3.7 | `docs/` holds four categories, not two: site, design record, **published dataset** (`docs/data/`), **second site** (`docs/app/`) | A two-way L5 split is wrong by construction |
| 3.8 | Seven submodules show `+`, not eight; five are already on clean `main` | `+` clears only on a superproject bump commit — a step 0001 omitted |
| 3.9 | `it-job-radar`'s `feat/salary-premium` is **already merged** into origin/main | No decision needed; only `pl-jobs-lora` is genuinely unmerged |
| 3.10 | `car-price-ml` page prints "13.9 MB" ×5, never "14 MB"; About and index say "14 MB" | A concrete chain-drift fix for Phase 3 |
| 3.11 | No LICENSE also in `current_projects` and `infra-docker-workmate` | Extends 0001's list |
| 3.12 | Every project is listed **twice** in the index README (Live-now bullets + level table); the bullets run A1,A2,A3,A4,A6,A7,**P2,P1**,P3,P4 | Editing one copy leaves the other free to disagree |
| 3.13 | A6/A7 are "✅ Live" with Site `—` | "Live" means two different things in one column |
| 3.14 | `car-price-ml` and `wroclaw` READMEs open with a CI badge; first live link at line 35 and 51 | Neither is "already compliant" on L3 — real edits, not verification |

---

## 4. Acceptance criteria

0001 called all of these binary. Six were not. They are now split, and the executor may
only tick group A from a script.

### Group A — script-checkable

**A1 · Visibility and links.** Every URL in a public page resolves **anonymously** —
`curl` with no token and no cookie jar. Any repo linked from a public page is public.

**A2 · Page head** (each live page): `meta description`, `og:title`, `og:description`,
`og:url`, `twitter:card`, `rel="icon"` all present; a `prefers-color-scheme` block exists;
zero external-origin resources; `og:url` equals the page's own canonical URL.

**A3 · Palette.** The named CSS variables from the Phase 1 artifact are present, in both
schemes.

**A4 · Charts.** No `<img>` pointing at a raster file inside the report body.

**A5 · About.** Description ≤ 350 chars; `homepageUrl` non-empty and returns 200
anonymously; ≥ 5 topics; LICENSE present.

**A6 · Generated pages.** After running the repo's generator, `git diff --exit-code` over
the published paths is clean. (Already enforced by CI in two of three repos — §3.3.)

**A7 · No bare figures downstream of a scheduled rebuild.** For any repo whose page is
rebuilt on a schedule, the About description and index line contain no digit-bearing
metric. (Wroclaw — §3.5.)

### Group B — reviewer judgement, ticked by a human

**B1** `<title>` states a finding, not the repo name. **B2** The About description says
what the page shows, in the page's own framing. **B3** Topics come from the shared
vocabulary produced in Phase 1. **B4** A folder's name tells the reader whether it holds
source, design record, or published output. **B5** Claim is the first non-heading line of
the README, badges excluded; live link inside the first 15 non-badge lines.

**B6 · Chain read.** The four renderings of a project's claim (L4 / L2 / L0 / L1) are
read side by side and say the same thing. This is the criterion the whole audit exists
for and it cannot be scripted.

---

## 5. Phases

**Phase 0 — Freeze and decide.** Two outputs, both blocking.

*Decision:* publish `current_projects`, or accept that L1 is a private planning tool and
L0 carries the public index alone. Publishing also exposes the submodule layout and the
`archive/legacy-games` branch, so it is a judgement call, not a checkbox. Decide the same
question for `student-wellbeing-pwr`, which the index currently advertises as "✅ Live"
while it 404s (§3.1) — publish it, or stop calling it live.

*Freeze:* bring the in-scope submodules onto clean `main`. `it-job-radar` is a plain
checkout + pull (§3.9). Re-derive the dirty list at execution time rather than trusting
§3.8 — it was already stale once.
*Exit:* `git submodule foreach --quiet 'git status --porcelain'` is silent for in-scope
repos, **and** a superproject commit records the new gitlinks. The `+` markers do not
clear without that commit.

**Phase 1 — Build the standard as an artifact.** Not a document; 0001's prose template
would have been re-implemented three times in three unrelated Python codebases and
re-diverged into exactly the split §4.1 records. Deliverables:

- the head-meta block and `:root` palette, extracted from `it-job-radar`, in a form each
  generator emits verbatim
- a checker script implementing every Group A criterion, exiting non-zero on failure
- the shared topic vocabulary (for B3)
- **the publishing-path decision**, moved here from 0001's Phase 5: it fixes the site URL,
  and therefore `og:url`, the About Website field, and every index link written later. Any
  chosen migration must keep the already-published ADR URLs resolving (§3.6) and must
  account for all four `docs/` categories (§3.7).

*Exit:* the checker runs green against `it-job-radar` — the reference implementation.

**Phase 2 — A1 / A2 / A3, one PR per repo.** Edit the **generator**, never the published
HTML (§6.5). Order within each repo: page → README → About, because the title is what the
other two quote.

- `wroclaw-air-insights` — full redesign to the standard. Largest item: dark mode and
  inline SVG are one change in `charts.py`, not a stylesheet tweak, since a PNG cannot
  follow the theme. Ends with a manual `workflow_dispatch` (§3.4) — the merge alone
  publishes nothing.
- `it-job-radar` — reference implementation; verify against the checker, fix deviations.
- `car-price-ml` — page passes; README does not (§3.14), and its About contradicts its own
  page on the model size (§3.10).

*Exit:* checker green on all three; B1/B2/B5 ticked.

**Phase 3 — The two indexes, in this order.** L0 first, because it is the public one.
Rewrite the profile README's project rows to quote the Phase 2 claims, and reconsider
which six projects sit in "Start here" given that A1 and A2 are currently demoted (§2).
Then L1: legend for the `A`/`B`/`P` codes, unbuilt and private entries marked as such,
the double listing collapsed (§3.12), and "Live" given one meaning (§3.13).
*Exit:* A1 green anonymously; B6 read for all three Phase 2 projects.

**Phase 4 — The remaining five pages** (`mlops-car-price`, `pl-review-sense`, `ab-lab`,
`apply-scout`, `pl-jobs-lora`) to the Phase 1 standard. Outside the current request;
listed so the split stays a decision.

**Phase 5 — Internals.** Execute the L5 migration decided in Phase 1.

---

## 6. Rules of engagement

1. **URLs do not move** — including the ADR URLs that `docs/`-as-Pages-root already
   published (§3.6). If a path changes, the old URL keeps resolving *and* `og:url` is
   updated to the canonical one.
2. **One PR per repository**, titled by layer.
3. **Structure change implies changes to**: that repo's `README.md` and `CLAUDE.md`, any
   path in `.github/workflows/`, config constants (`it_job_radar/config.py` `PUBLISH_DIR`),
   tests that load published paths (`it-job-radar/tests/test_site.py`,
   `car-price-ml/tests/test_browser_parity.py`, `test_frontend.py`), `api/main.py`'s mount
   of `docs/app`, and `.gitignore` — all in the same PR. The **GitHub Pages source
   setting** also changes, and no PR can carry it; it is a manual step.
4. **Nothing downstream asserts what the page does not show.** The live case is §3.10.
5. **No published HTML in this portfolio is hand-edited.** All three generate:
   `wroclaw_air_insights/report.py` + its section modules, `it_job_radar/site/build.py`,
   `car_price_ml/site/{build,stylesheet,form}.py`. Two are CI-gated (§3.3), so a hand-edit
   is a red PR, not a silent overwrite.
6. **No third-party runtime dependency in a page.** Verified viable: it-job-radar's page
   has no external resource of any kind.
7. **Wording is in scope; results are not.** No number changes without the analysis that
   changes it.
8. **Verification is anonymous.** Any check that can see private repos is not the check.

---

## 7. Definition of done

- The checker script exits zero for every repo in the phase's scope.
- The anonymous link sweep over the profile README and all live pages returns no non-200.
- B6 read for each in-scope project across all four layers.
- Each page loaded in both colour schemes and at a narrow viewport.
- Wroclaw's `workflow_dispatch` has run and the published page reflects the redesign.
- Findings deliberately not fixed are listed here with the reason.
