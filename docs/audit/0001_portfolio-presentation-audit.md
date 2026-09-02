# Portfolio Presentation Audit — Process Design

Date: 2026-08-14
Status: superseded by [0002_portfolio-presentation-audit-v2.md](0002_portfolio-presentation-audit-v2.md)
Author: P0w3r223 + Claude
Related to: `README.md` (portfolio index), the 13 project submodules

> **Superseded 2026-08-14.** Code review found three false premises in §4 and five
> execution defects in §5/§6. §4.1 (the two page families) and §4.2 (titles) were
> re-measured and are exact — they carry forward unchanged. Everything else is restated
> in 0002. Kept for the audit trail of what the review caught.

---

## 1. What is audited, and for whom

The audit covers **how the portfolio presents itself**, not whether the code inside it is
correct. Correctness is already covered by each project's CI and by `/code-review`.

Two readers, two budgets:

| Reader | Budget | Enters at | Leaves convinced if |
|--------|--------|-----------|---------------------|
| Recruiter / hiring manager | ~60 s | GitHub profile → index README | They can name what I do and open one working live page |
| Engineer on the panel | ~10 min | A single project repo | They find the decision behind a number without asking me |

Every criterion below exists to serve one of those two. A finding that serves neither is
not a finding.

The audit's core assumption: **inconsistency is only visible across projects**. A reader
who sees one page has no baseline; a reader who opens three notices that one of them
looks like a different person made it. That is why the audit is performed *horizontally*
(one layer across all repos) even though the fixes are shipped *vertically* (one PR per
repo) — see §5.

---

## 2. The presentation chain

Six layers. A reader traverses them in order, and each layer's job is to make the next
one worth opening.

```
L0  Profile          github.com/P0w3r223 — profile README + pinned repos
L1  Index            current_projects — About panel + README
L2  Repo About       description · website · topics · license  (the "live_site" field)
L3  Repo README      first screen: claim, live link, what it proves
L4  Live page        title · meta · structure · visual style
L5  Repo internals   folder names, docs/ layout, notebook names
```

**The `live_site` chain.** The user's term covers L2 → L1 → L4: the repo's *Website*
field, the *live site* link in the index README, and the published page itself. Today
these three carry three differently-worded claims for the same project. The rule adopted
here is **one claim, three renderings**:

- **L4 `<title>`** is the source of truth — the finding, stated as a sentence.
- **L2 description** is that finding plus the evidence that earns it, ≤ 350 chars.
- **L1 index entry** is that finding compressed to one line.

Nothing downstream may assert something the page does not show.

---

## 3. Acceptance criteria

Binary, checkable without judgement calls.

### L0 — Profile
- [ ] Profile README names the target role and links the index repo in the first screen
- [ ] Exactly 6 pinned repos, matching the "Pinned on profile" line in the index README

### L1 — Index
- [ ] About description states what the repository *is* (an index), not what it contains
- [ ] About → Website points at a real destination (currently empty)
- [ ] Topics set (currently none)
- [ ] Every project code (`A1`, `B3`, `P4`) is explained by a legend before first use
- [ ] Entries without a repository are visibly marked as *not yet built*, never styled like a shipped project
- [ ] Every link resolves — verified by script, not by eye

### L2 — Repo About
- [ ] Description follows the L4 title (see §2), ≤ 350 chars, no marketing adjectives
- [ ] Website = the live page, or empty if there is none — never a stale URL
- [ ] ≥ 5 topics, drawn from a shared vocabulary so related projects cluster
- [ ] LICENSE present

### L3 — Repo README
- [ ] The claim is the first non-heading line, in bold
- [ ] Live link within the first screen (~15 lines)
- [ ] Portfolio code and level stated once, in the blockquote
- [ ] Numbers in prose are dated or point at the artifact that carries the current ones

### L4 — Live page
- [ ] `<title>` is the finding, suffixed with ` — <repo>`
- [ ] `meta description`, `og:title`, `og:description`, `og:url`, `twitter:card`, `rel="icon"` present
- [ ] Dark mode via `prefers-color-scheme`, palette expressed as CSS variables
- [ ] No external font/CDN request — the page renders offline and leaks no visitor to a third party
- [ ] Charts are inline SVG inheriting the palette, not raster images
- [ ] Body max-width, card radius, and type scale match the shared template

### L5 — Repo internals
- [ ] A reader can tell from the folder name whether it holds source, docs, or published output
- [ ] The published-site root is the same path in every repo
- [ ] Notebook filenames say what the notebook answers, not just its order

---

## 4. Baseline — what the recon already found

Measured 2026-08-14 against the live pages and the GitHub API.

### 4.1 The pages split into two families

| Repo | description | og: | twitter: | favicon | dark | ext. font | SVG | raster |
|------|-------------|-----|----------|---------|------|-----------|-----|--------|
| it-job-radar | ✅ | ✅ | ✅ | ✅ | ✅ | — | 11 | 0 |
| car-price-ml | ✅ | ✅ | ✅ | ✅ | ✅ | — | 4 | 0 |
| wroclaw-air-insights | — | — | — | — | — | Google Fonts | 0 | 3 |
| mlops-car-price | — | — | — | — | — | Google Fonts | 0 | 0 |
| pl-review-sense | — | — | — | — | — | Google Fonts | 0 | 1 |
| ab-lab | — | — | — | — | — | Google Fonts | 0 | 1 |
| apply-scout | — | — | — | — | — | Google Fonts | 0 | 0 |
| pl-jobs-lora | — | — | — | — | — | Google Fonts | 0 | 0 |

Two pages were built to a standard; six predate it. Shared by a link on a page that
says "portfolio", they read as two authors. This is the single largest presentation
defect, and `wroclaw-air-insights` — the project a reader meets **first**, as A1 —
sits on the wrong side of the split.

### 4.2 Titles

`it-job-radar` and `car-price-ml` open with a finding
("Most junior IT offers in Poland are not development jobs"). The other six open with
their own repo name, which tells the reader nothing they did not already know from the
link they clicked.

### 4.3 Publishing paths disagree

| Repo | Pages source | Site lives in | `docs/` holds |
|------|--------------|---------------|---------------|
| it-job-radar | `main:/docs` | `docs/index.html` | site **and** `adr/`, `research/`, `plan/`, `ideas/` |
| car-price-ml | `main:/docs` | `docs/index.html` | site **and** `adr/`, `research/` |
| wroclaw-air-insights | Actions workflow | `reports/site/index.html` | only `ideas/`, `research/` |

Three repos, three conventions. In two of them `docs/` means both "the published site"
and "the design record", so a reader opening `docs/` to read the reasoning lands in
build output.

### 4.4 Metadata gaps

- `current_projects` (the index — the entry point): description is *"Everything I've
  worked on thus far."*, Website empty, zero topics.
- No LICENSE: `wroclaw-air-insights`, `it-job-radar`, `student-wellbeing-pwr`.
- Zero topics: `student-wellbeing-pwr`.

### 4.5 Index README

- Codes `A1…A7`, `B1…B3`, `P1…P5` are used from the first line with no legend. They also
  encode a second dimension — level *and* order — that is never stated.
- `A5 studia-rag` and `P5 doc-extract` are typeset like shipped projects but have no
  repository.
- The A2 and A3 "what it demonstrates" cells run to ~90 and ~80 words inside a table
  cell. At table width they are a wall, and the reader skips the row entirely.
- `B3` points at a subdirectory of A3, so the same work is counted twice without saying so.

### 4.6 Working-tree state (blocks Phase 2)

Eight submodules are ahead of, or off, the commit the superproject records; `it-job-radar`
is on `feat/salary-premium` and `pl-jobs-lora` on `run/p4-complete`. Editing pages in that
state produces submodule bumps that mix presentation changes with unrelated work.

---

## 5. Execution order

Audit horizontally, ship vertically. Each phase ends in a reviewable state.

**Phase 0 — Freeze.** Bring every submodule that will be touched onto a clean `main`
synced with origin. Record which ones were deliberately left on a feature branch.
*Exit:* `git submodule status` shows no `+` on the repos in scope.

**Phase 1 — Write the standard.** Before any page is edited, extract the shared page
template from `it-job-radar` (palette variables, meta block, type scale, SVG chart
conventions) and record it, plus the About-field template and the code legend. Without
this, six pages get six interpretations of "like it-job-radar".
*Exit:* a template document exists; §3 L4 is checkable against it.

**Phase 2 — A1 / A2 / A3, one PR per repo.** The three projects the reader meets first.
Per repo: L4 page → L3 README → L2 About. In that order, because the page title is the
source of truth the other two quote.
- `wroclaw-air-insights` — full redesign to the standard, the largest item in the audit
- `it-job-radar` — already compliant; verify and fix drift only
- `car-price-ml` — already compliant; verify and fix drift only

*Exit:* three live pages pass L4; three About panels pass L2.

**Phase 3 — Index.** Rewrite `README.md` against L1 once the three claims upstream are
final, so the index quotes rather than invents. Add the legend, mark unbuilt entries, cut
the table cells to one line, set the superproject's About fields.
*Exit:* L1 passes; link check is green.

**Phase 4 — Remaining pages.** `mlops-car-price`, `pl-review-sense`, `ab-lab`,
`apply-scout`, `pl-jobs-lora` to the Phase 1 standard. Out of scope for the current
request; listed so the split is a decision and not an oversight.

**Phase 5 — Internals and verification.** L5 decisions (publishing path, `docs/` split),
then the full checklist re-run.

---

## 6. Rules of engagement

1. **URLs do not move.** Published page URLs are on a CV and in the index. If a
   publishing path changes, the old URL keeps resolving.
2. **One PR per repository**, titled by layer, so a reviewer sees presentation changes
   without unrelated work mixed in.
3. **Structure change implies a documentation change.** Moving or renaming a directory
   means updating that repo's `README.md`, `CLAUDE.md`, and any path referenced in
   `.github/workflows/` — in the same PR.
4. **Nothing is asserted that the page does not show.** A description claiming a number
   the page no longer prints is a defect, not a rounding difference.
5. **Generated pages are edited at the generator.** `wroclaw-air-insights` builds its page
   from `src/wroclaw_air_insights/report.py` and its section modules; editing
   `reports/site/index.html` directly is overwritten by the next refresh run.
6. **No third-party runtime dependency in a page.** Fonts, scripts, and styles are inline
   or same-origin.
7. **The audit does not rewrite claims about results.** Wording is in scope; the numbers
   behind it are not touched without the analysis that changes them.

---

## 7. Definition of done

- Every box in §3 is checked for the repos in the phase's scope.
- A link check over the index README and all live pages returns no non-200.
- The three claims for each project (page title / About / index line) are re-read side by
  side and say the same thing.
- Each live page has been loaded in both colour schemes and at a narrow viewport.
- Findings that were deliberately not fixed are listed here with the reason.
