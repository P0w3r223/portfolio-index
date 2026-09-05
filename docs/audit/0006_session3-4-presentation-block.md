# Session 3 + 4 — the presentation block

Date: 2026-09-04
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: [0003_portfolio-review-plan.md](0003_portfolio-review-plan.md) §3 (the session table), §8 and §9 (the
reconciliation rule); [0004_session1-recruiter-triage.md](0004_session1-recruiter-triage.md) §3.2, §6.4, §6.5, §8;
[0005_session2-extensions.md](0005_session2-extensions.md) §7, §9; `apply-scout/docs/decisions/0012_the_page_quotes_the_artifacts.md`

---

## 1. What this document is

`0003` §3 commissions two more sessions before the per-repo rollout: **Session 3** (descriptions, one length
standard across four layers, twelve repositories) and **Session 4** (a divergence table over every published page
at desktop and 375 px, and one design spec). This document designs both as **one block**, because §5 below found
that they overlap on one file each, and it records the decisions taken to start it.

It is the output of an architecture pass. **Every measurement in §2 and §3 was re-taken by hand before this
document was written** — the architecture pass had file access only, no network and no `git`, so its account of
the account-side surfaces and of the working tree could not be checked by it. Two of its statements did not
survive that check and are corrected in §2.4.

## 2. Current state, measured 2026-09-04

### 2.1 The repositories

Twelve public repositories, one private index. **No open pull request anywhere**, every repository on `main`, and
all twelve submodule pointers read `heads/main`. The only working-tree noise is untracked local `.claude/`
directories.

Session 2's technical work is **on `main`, not proposed**: `read_cv.py:55` resolves against a frozen set of
permitted paths, `fetch.py` holds a scheme allowlist, `check_resolved` and a hand-walked redirect chain
(`follow_redirects=False`), and `src/apply_scout/retrieval/` and `src/apply_scout/attack/` both ship with
committed artifacts under `eval/expected/`.

### 2.2 The eleven published pages

*Corrected 2026-09-04 against the live pages; `wroclaw` and `mini-traceroute` were read from a stale local
build and from HTML that skipped an external stylesheet. [`0007`](0007_divergence-and-the-page-spec.md) §3
is the current table and this one is kept for the session it describes.*

| page | `h1` | eyebrow | tiles | tables | card meta | back-link | source |
|---|---|:-:|---|---:|:-:|:-:|---|
| `ab-lab` | claim | yes | `.tile` ×4 | 5 | yes | no | generated |
| `doc-extract` | claim | yes | `.kpi` ×4 | 13 | yes | **yes** | generated |
| `it-job-radar` | claim | yes | `.kpi` ×4 | 1 | yes | no | generated |
| `car-price-ml` | claim | yes | `.kpi` ×4 | 1 | yes | no | generated |
| `auth-log-scan` | claim | yes | `.kpi` ×5 | 2 | yes | no | generated |
| `pl-review-sense` | claim | yes | `.kpi` ×4 | 7 | yes | no | generated |
| `mini-traceroute` | **descriptive** | yes | `.kpi` ×4 | 2 | yes | no | hand-written |
| `apply-scout` | claim | yes | `.kpi` ×4 | 3 | **no** | **yes** | hand-written, test-constrained |
| **`mlops-car-price`** | **repo name** | **no** | **none** | 2 | **no** | no | hand-written |
| **`pl-jobs-lora`** | **repo name** | **no** | **none** | 2 | **no** | no | hand-written |
| `wroclaw-air-insights` | claim | yes | `.stat` ×4 | 4 | yes, bar `og:description` | no | generated daily by CI |

`og:image`: **zero pages out of eleven.** ~~`mini-traceroute` is the one page with no `overflow-x` rule at all,
against two tables.~~ **False, and contradicted by M3 in this same document**: its rules are in an external
stylesheet that every earlier check read past. One of its two tables sits in `.ledger-wrap`; the other is in
a bare `<figure>` with no scroller and passes on margin. See [`0007`](0007_divergence-and-the-page-spec.md)
§8.

`wroclaw-air-insights` is the weakest row here and is marked as such: it publishes from
`reports/site/index.html`, rebuilt daily by `refresh.yml`, and the committed copy is stamped
`Generated 2026-08-11 12:56 CEST`. **Its row must be re-taken from the live URL before the spec quotes it.**

### 2.3 The four description layers

Layer 2 — GitHub About and topics — was read from the API rather than inferred. Six repositories carry a
description that states a measured claim (`ab-lab`, `car-price-ml`, `doc-extract`, `wroclaw-air-insights`,
`it-job-radar`, `apply-scout`). **Four carry an internal portfolio code a recruiter cannot decode:**

| repository | published description |
|---|---|
| `auth-log-scan` | *"… Portfolio proof **B2**."* |
| `mini-traceroute` | *"… Portfolio proof **B1**."* |
| `pl-review-sense` | *"… Portfolio **A4**."* |
| `pl-jobs-lora` | *"**P4:** QLoRA fine-tune …"* |

`pl-review-sense`'s code is also **wrong** against the index, which demoted it to `B4` in `0004` §5.

### 2.4 Three corrections to the architecture pass

Recorded rather than silently fixed, because the mechanism is the one this review keeps naming: a reader of that
pass would carry all three forward.

- **"Five submodules diverged at session start" — false.** `git submodule status` reads `heads/main` on all
  twelve. The five it saw were untracked `.claude/` directories, which is working-tree noise and not a pointer.
  Its "re-point before the divergence table" mitigation is therefore not needed.
- **"The About + topics layer is unmeasured" — no longer true.** It was unmeasurable *by that pass*, which had no
  network. It is measured in §2.3 above, and the finding is sharper than the estimate it replaces: the layer's
  problem is not a missing convention in nine repositories, it is four published internal codes.
- **"`0003` §4's breakpoint line is stale" — false, and this is the important one.** That line says only `ab-lab`
  and `wroclaw-air-insights` carry a width-based breakpoint; the pass reported `wroclaw`'s single `@media` as not
  width-based. Re-measured: `ab-lab` has `@media (max-width: 34rem)`, **`wroclaw` has `@media (max-width: 640px)`**,
  and every other `@media` in the portfolio is `prefers-color-scheme` or `print`. The line is exactly true and is
  **not** struck. A reconciliation that strikes a true statement is worse than one that misses a false one: the
  false statement is still findable, the struck true one is not.

  Found while checking it: **`apply-scout` carries no `@media` rule of any kind** — not width, not
  `prefers-color-scheme`, not `print` — and last session measured that its page still does not scroll sideways at
  375 px. That belongs in B2's divergence table as an observation, not as a defect: a fluid layout that holds is a
  different thing from a fixed one that does not, and the spec has to say which it is asking for.

## 3. What is open, by severity

### High

**H1 — `doc-extract`'s page contradicts itself and understates the flagship.**
`docs/index.html:201-203` prints a KPI tile reading **`5 / 7`**, labelled *Milestones built*, with the note *"the
gate is measured; **injection and the real set are not**"*. The eyebrow twenty-six lines above, on the same page,
reads *"milestones 1–6 of 7, and most of the seventh"*. `CLAUDE.md` carries shipped modules for both: M6 as
`attack/` and `overlay.py`, M7 as `raster.py`, `foreign/`, `degrade/`, `place.py`, `joint.py` and `complete.py`.
The tile's value and label are hardcoded at `docs/build_index.py:1817-1818` and its note at `:1819`; the
eyebrow that contradicts them is at `:1791`.

**This is the sharpest finding in the block.** `0004` §5 promoted `doc-extract` over `apply-scout` to the AI
Engineer flagship position *for its measured injection resistance*, and the flagship's own page denies that
measurement exists — in a KPI tile, which is the part of the page a sixty-second reader actually reads. It is
ADR-0012's defect class on a different repository.

**It is not a new finding, and that is what makes it worth putting first.** `0004` §3.3 counted this tile as one
of three disagreeing figures on 2026-09-02. The index's `M2 of 7` was fixed; the tile was not, and every handoff
since has treated §3.3 as closed. So the defect here is not a missed observation — it is a **partially applied
fix**, which is the same class as `0004` §6.5's checklist, two thirds of which was done within a minute of the
commit that recorded it as open and was never re-read (`0003` §11). One surface of a multi-surface fact was
repaired and the pass was called done.

**H2 — two pages still open with a repository name.** `mlops-car-price/docs/index.html:32` and
`pl-jobs-lora/docs/index.html:35`. Both also have no eyebrow, no tiles and no card metadata — they are the only
two pages with none of the three. `0004` §8 called converting these *"the single highest-value presentation
change identified"*.

**H3 — the index `README.md:44` and the profile README sell `apply-scout` two milestones out of date.** They do
not say it identically, which is itself part of the finding: the profile reads *"with a trajectory-evaluation
harness measuring success rate, citation fidelity, and cost per task"* and `README.md:44` reads *"with a
trajectory-evaluation harness: success rate, citation fidelity, cost per task"*. Neither names
the retrieval evaluation or the attack suite — which are what the repository's own description and page now lead
with. Not false; but it is the source Session 3 rewrites the other layers from, and the profile README is the
most-read surface in the portfolio.

**H4 — nine of eleven pages have no route back to the profile.** Only `doc-extract` and `apply-scout` carry one.
`0003` §7 settled the shape (hub-and-spoke, one link, survives triage) and it is unrolled on nine pages.

### Medium

- **M1 — card metadata.** Absent on `apply-scout`, `mlops-car-price`, `pl-jobs-lora`, `wroclaw`. `og:image`
  absent on all eleven.
- **M2 — three tile conventions and two pages with none.** `.kpi` ×7, `.tile` ×1, `.stat` ×1, none ×2 —
  eleven pages. *An earlier draft said `.kpi` ×6, which sums to ten and contradicts §2.2's own table two
  pages above it. The six was inherited from `0003` §4, measured 2026-09-02, hours before `apply-scout#32`
  gave that page tiles — an inherited figure inside the document whose §2.4 exists to catch inherited
  figures.*
  `apply-scout/docs/index.html:18-20` declares its own choice *provisional pending this spec*, so a shipped
  page's source comment now depends on this block resolving it.
- ~~**M3 — `mini-traceroute`: two tables, no `overflow-x`.**~~ **False, and it had been false for three
  sessions.** That page is the only one in the portfolio whose CSS is not inlined; `docs/assets/styles.css`
  carries `.scroll-x { overflow-x: auto }` and `.ledger-wrap { … overflow: auto }`. Every check, `0004` §6.5's
  and this one's, grepped `index.html`. **What survives is smaller and real:** `.ledger-wrap` wraps one of its
  two tables, and the second sits in a bare `<figure>` with no scrolling ancestor — it passes because it fits
  (+77 px at 375 px), not because it is wrapped. So §6.5's acceptance criterion of *both* tables wrapped is
  still not met, on one table rather than two. See [`0007`](0007_divergence-and-the-page-spec.md) §8.
- **M4 — `pl-review-sense` was repaired in the audit, not on the surfaces.** `CLAUDE.md` still opens *"Portfolio
  project A4"* against the index's `B4`, and the README still leads with the headline `0005` §7 C1 ruled does not
  describe the repository. C1 rewrote the *reason* in `0004` §5; the reader-facing copy is untouched, and C3
  (lead with the 80-sentence Polish adversarial set) is scheduled here.
- ~~**M5 — `wroclaw` diverges on every axis at once**: descriptive `h1`, no eyebrow, a third tile convention, no
  card metadata.~~ **Three of the four were false, and were read from a stale local build** — see
  [`0007`](0007_divergence-and-the-page-spec.md) §4.3 and §8.1. Live, the page's `h1` is a claim, it carries
  an eyebrow, and it carries card metadata bar `og:description`. What survives is the tile convention
  (`.stat`), two token aliases, two absent tokens, a third `--accent-soft` nothing paints, and the missing
  `og:description` — which is why `0007` §9 places it in row 6 and not in row 5.

### Low

- **L1 — the twelve `LICENSE` files.** ~~**Decided, not applied**~~ — **closed 2026-09-04** on twelve
  squash merges and an API read of every default branch afterwards; see §6 decision 2 for the merge SHAs.
  All twelve now read `Copyright (c) 2026 Piotr Cząstkiewicz`, and GitHub still detects MIT on all twelve.
  It is no longer closed on an intention.
- ~~**L2 — the action-pinning question**, reopened on true premises by `0003` §9 decision 2, still
  unanswered.~~ **Answered 2026-09-04: do not pin, and record why.** Measured across all fourteen workflow
  files: **47 `uses:` occurrences, six distinct actions, every one of them first-party `actions/*`, and
  zero SHA pins anywhere.** Three jobs are privileged — `auth-log-scan/ci.yml:58`, `it-job-radar/ci.yml:81`
  (`pages: write` + `id-token: write`) and `wroclaw-air-insights/refresh.yml:12`, the most privileged job in
  the portfolio (`contents: write` **and** `pages: write` **and** `id-token: write`) — so
  the narrowest real question was whether to pin those three and nothing else.

  **The reason is maintenance, not threat modelling.** A compromised `actions/checkout` is a
  GitHub-wide event, not a portfolio one, and the tag a first-party action floats is maintained by the
  same party that hosts the runner. Against that, a SHA pin in a portfolio with no bot to move it decays
  into a stale action — which is precisely the state `0003` §6 had to dig this portfolio out of, eleven
  repositories at once. Pinning buys protection against a scenario the portfolio cannot influence, at the
  cost of re-creating the failure it has already had. **If a third-party action is ever introduced, this
  answer does not cover it and the question reopens on that action alone.**
- **L3 — whether Level B survives as a tier** (`0004` §9). A ranking decision, not a presentation one; excluded
  here, see §7.
- **L4 — `ab-lab`'s `refresh.yml`.** **Closed on a green run**, see §6 decision 3.
- **L5 — the `license` table form is deprecated, in ~~all twelve~~ *eleven of the twelve*.**
  ~~`pyproject.toml` in eleven repositories declares `license = { text = "MIT" }`, and `doc-extract#10`
  adds the twelfth in the same form for consistency.~~ **Corrected 2026-09-05, measured at source:**
  **eleven** `pyproject.toml` files carry the form — `doc-extract` among them — and the twelfth
  repository, **`mini-traceroute`, has no `pyproject.toml` at all**: it is C++/CMake. The exemption is
  structural rather than an oversight, and it is recorded because the wrong count sends the next reader
  looking for a twelfth file that does not exist. See [`0008`](0008_the-rollout-ledger.md) §2.1. Reproduced against setuptools 84.0.0: building the metadata emits
  *"`project.license` as a TOML table is deprecated … By 2027-Feb-18"*, and `requires = ["setuptools>=68"]`
  floats to whatever is current, so every repository inherits that date. The replacement is the SPDX string
  `license = "MIT"` with `requires = ["setuptools>=77"]`, verified to emit `License-Expression: MIT` and no
  warning. **Not applied here**: it is twelve repositories and one form, so it goes the way L1 went — all
  together, on a decision, rather than one repository quietly differing from eleven.

## 4. The decision the block turns on: where the spec lives

A prose spec applied by hand to eleven repositories is **eleven copies of a dozen properties with no source of
truth** — structurally the same defect this review has found in `doc-extract`'s four progress figures,
`apply-scout`'s stale completion rate and the audit documents themselves. So the spec's *carrier* is a design
decision, not a formatting one.

| carrier | cost | drift resistance | verdict |
|---|---|---|---|
| **C-a — prose spec + a per-repo acceptance test** asserting the observable properties (`h1` is not the repository name; every table inside something that scrolls; tiles present; card metadata present; a back-link present) | low | structure high, visual values none | **take** |
| **C-b — one vendored checker**, hash-pinned per repository, the pattern `doc-extract` already uses for XSDs and fonts | low–medium | high, and the checker cannot silently diverge | **take, paired with C-a** |
| **C-c — a vendored shared stylesheet / head partial** | medium–high | high for pixels | **reject** |
| **C-d — convert all four hand-written pages to generators first** | high | none — eleven generators is still eleven places | **reject as a prerequisite** |

**Why C-c is rejected.** The brief's reader is a recruiter with sixty seconds, on desktop and on a phone. That
reader opens *one* link. Divergence *between* pages costs them nothing; divergence *inside* a page — a repository
name where a claim belongs, a table that scrolls off a phone, no route back — costs them everything. C-c buys
the axis nobody measures and is the most expensive option.

**The counter-argument, kept in view rather than dismissed:** a hiring manager who opens three links does form an
impression of coherence, and *twelve pages that look like one body of work* is part of what this portfolio
argues. If that is weighted, C-c returns and the Session 5+ rollout roughly doubles. It is left as a reversible
decision for exactly that reason.

### 4.1 The tile mandate is in tension with ADR-0012

If the spec requires tiles on every page, `mlops-car-price` and `pl-jobs-lora` — the two pages with no tiles, no
generator and no committed table to quote — must either grow a generator or print a figure no artifact produces.
The second violates the portfolio's own standard, which ADR-0012 states as a rule.

Both have a route and neither is free. `mlops-car-price` already has `examples/drift_scenarios.py`,
`examples/detector_evaluation.py` and `examples/artifact_cost.py` that regenerate the README's tables; extending
one is the cheap path. `pl-jobs-lora`'s own status card says *"four of six table rows are real measurements … its
two rows are shown empty rather than estimated"* — so its honest headline is a claim about **baselines measured
before the fine-tune exists**, which is a copy decision that has to be taken before any tile rule can be applied
to it.

**The rule this block adopts:** the spec mandates tiles **where a committed artifact can source them**, and names
the fallback — a lead paragraph carrying the claim — together with the reason, so a later reader does not read
the exemption as sloppiness.

### 4.2 The measurement instrument already exists

`0003` §6 records that Session 4 needs a real device or a proper emulator. That blocker has been closed since
2026-08-14 and no audit document knows it:
`wroclaw-air-insights/.claude/skills/verify-published-page/measure_page.py` drives CDP
`Emulation.setDeviceMetricsOverride`, measures tables at `width: min-content`, reads its marker from the
**fetched** HTML with `--expect` as a gate, and accepts a URL *or a local path* — so a page can be checked before
it ships. `--widths`, `--marker`, `--expect` and `--browser` are all flags.

> ~~the only `wroclaw`-specific thing in it is `--winter`, and that is opt-in.~~ **Wrong, and it mattered.**
> The second was `data-scroll="by-design"`, the attribute the tool read to decide whether a wide table was
> acceptable — and only `wroclaw` sets it. Pointed at the eleven pages it called **seventeen** wide tables
> defects; every one was already inside a box that scrolls. `wroclaw-air-insights#29` generalises it to walk
> the DOM for a scrolling ancestor, after two review passes that found it walking past a clipping box and
> unable to see `wroclaw`'s *own* rule. [`0007`](0007_divergence-and-the-page-spec.md) §2.

Two mismatches to settle before B2 runs it against eleven pages:

- The plan's standard width is **375 px**; the tool defaults to `390,414,768,1200`. Both are real phones
  (iPhone SE / iPhone 12+). **375 is the gate; 390 is measured alongside**, which is one `--widths` argument.
- **The marker check assumes a build stamp**, and gates the whole reading on finding one (`marker_ok` feeds
  `healthy`). `wroclaw` prints `Generated …` because CI rebuilds it daily; the other ten pages do not, so B2 must
  either point `--marker` at something each page actually prints or accept a marker failure on ten of eleven runs
  and read only the geometry. **Decide this before the twenty-two runs, not during them** — otherwise the
  divergence table's health column means one thing on `wroclaw` and another everywhere else.

## 5. The block

Chosen shape: **truth first, then one presentation spec that absorbs the page-header layer.** This splits
`0003` §2's four description layers **3 + 1** — the three text layers stay a descriptions pass, and the live-site
header layer moves into the spec, because on `mlops-car-price` and `pl-jobs-lora` it is the same edit to the same
file. That is a change to the plan's recorded scope, and it is the thing this document needed approval for.

The argument is the plan's own. `0003` §2 inverted the commission's order because *"there is no point … unifying
the CSS of a page that should stop being linked."* One level down, there is no point agreeing a page header in a
descriptions pass and then rewriting that page's whole head in a spec pass.

| | item | cost | what drives it |
|---|---|---|---|
| **B0** | Reconcile `0003`, `0004` and `0005` against the repositories | 0.5 d | eight stale statements across three files; no code |
| **B1** | Fix `doc-extract`'s page (H1) | 0.5 d | deciding what the tile should *say*; the edit is generator + regenerated artifact + the committed-site test |
| ~~**B2**~~ | ~~Divergence table, eleven live pages at 375 and 390 px~~ | ~~0.5–1 d~~ | **Delivered** as [`0007`](0007_divergence-and-the-page-spec.md) §3 |
| ~~**B3**~~ | ~~The spec, including its carrier (§4) and the tile rule (§4.1)~~ | ~~2–3 d~~ | **Delivered** as `0007` §5. It cost less than estimated for a reason worth recording: the spec did not have to be *chosen*. Ten of the eleven pages already implement one design system, seven of them in named tokens with identical values, and the other three as hand-typed literals of the same values — so the document describes what exists before it instructs |
| **B4** | The two family-B conversions, as the spec's first proof (H2) | 1.5–2 d | both hand-written with no generator; `pl-jobs-lora`'s headline must be true of a fine-tune that has not run |
| **B5** | Back-link (H4) + card metadata (M1) + `mini-traceroute` wrappers (M3) | 1–1.5 d | **ten** repositories × one PR — nine need the back-link (**six** generated, three hand-written) and `apply-scout` needs card metadata while already having the link. The six generated ones each need the page regenerated under its byte-diff |
| **B6** | The three text description layers (H3, M4, §2.3's four codes) | 2–3 d | the About convention, and `pl-review-sense`'s C3 repackaging |

**8–11 days.** B0–B4 are one unit; B5 and B6 are schedulable separately, which is why B6 — the one that can slip
without blocking anything — is last.

**Every major stage closes with a `code-reviewer` pass** before it is proposed as merged work.

## 6. Decisions taken 2026-09-04

1. **The block is the shape above**, with the 3 + 1 split of `0003` §2's description layers.
2. **The twelve `LICENSE` files name the person.** `Copyright (c) 2026 Piotr Cząstkiewicz`, all twelve together —
   the file is the only legally operative surface in the portfolio and it was the last one still naming the
   handle while the profile, the profile README and the contact address name the person. One decision, twelve
   one-line commits; deliberately not settled by fixing a subset, which is why it was carried unowned from
   `0003` §9 rather than done piecemeal.

   ~~**The twelve commits have not been made.** L1 is therefore *decided* and not *closed*~~ — **applied
   2026-09-04**, twelve squash merges: `ab-lab` 802dd78, `apply-scout` 1051682, `auth-log-scan` 3ee3105, `car-price-ml` e1112f9, `doc-extract` 9878e0c, `it-job-radar` 4c77007, `mini-traceroute` 9a51d88, `mlops-car-price` ade3a5c, `pl-jobs-lora` 87b5b07, `pl-review-sense` 87f43db, `token-budget` d3e663a, `wroclaw-air-insights` 98b3051. Re-read from the API on the default branches
   afterwards, all twelve carry `Copyright (c) 2026 Piotr Cząstkiewicz` and all twelve still report
   `spdx_id: MIT`. The twelve committed blobs are byte-identical, one object `6a34fcf`.

   The guard this paragraph carried was built against the *premature* strike — the record saying done
   while the files said otherwise, which a first draft of this block did to `0005` §9. Closing it exposes
   the **inverse**: a record that keeps saying not-done after the work lands. Same class, opposite sign,
   and the wording above did not catch it. That is why the closure carries twelve SHAs and an API read
   rather than a sentence.
3. **`ab-lab`'s `refresh.yml` was dispatched by hand** rather than waited on. It last ran 2026-08-31 and
   2026-08-24, both *before* its action-major bump, and its cron (`0 6 * * 1`) would not have fired until
   ~2026-09-07 — so the bump had been carried across two sessions as unexercised. The workflow already declares
   `workflow_dispatch`, so nothing had to change to run it.

   **Result: green** (run `33857055959`). `actions/checkout@v7` and `actions/setup-python@v7` both ran, and
   *Re-measure every recorded finding at full size* — the full `pytest -m slow` pass this job exists for — passed.
   That is the check the bump had never had: the pull-request jobs replay two cells at a tenth of their size, and
   this is the only job that re-measures everything. Closes **L4** on a result rather than on an assumption.

## 7. Deliberate exclusions

| excluded | why |
|---|---|
| **`apply-scout`'s retriever ranking** | separately owned; ranking `find_evidence` changes what the tool returns, which changes every cassette key, which costs a full paid re-record. Nothing here touches it |
| **Theme unification across pages** | §4's argument: a sixty-second reader opens one page. Largest cost, least reader-visible return. Reopen only by overturning C-c |
| **`og:image` assets** | eleven new binary artifacts with no committed source, in a portfolio whose rule is that published artifacts are generated and diffed. Text cards are the honest version until an image can be generated from a record |
| **A project-to-project navigation mesh** | settled by `0003` §7: hub-and-spoke only |
| **`token-budget`'s page** | settled by the demotion, `0005` §6. Not reopened |
| **The Level A/B tier restructure (L3)** | a ranking decision on no new evidence; it would reopen `0004` §5 |
| **Converting all four hand-written pages to generators** | rejected as a prerequisite (§4, C-d); done per repository only where §4.1's tile rule forces it |

## 8. Risks

| risk | severity | mitigation |
|---|---|---|
| **Goodhart on the spec** — eleven pages satisfy a checklist and still read badly | high | ADR-0012 names this blind spot twice, and `verify-published-page`'s own `SKILL.md` says *"whether the page reads well … is a judgement made by looking."* The spec carries an explicit **what this does not check** section |
| **The tile mandate forces an unsourceable figure** (§4.1) | high | mandate tiles *where an artifact can source them*; state the fallback and its reason on the page |
| **`wroclaw`'s committed page is 24 days stale** and rebuilds daily | medium | take its row from the live URL with `--expect`, never from `reports/site/index.html`; any change goes through `report.py` and must survive `refresh.yml` |
| **This document goes stale as the block lands** — §2.4 is that failure caught once already | medium | `0003` §9's rule applied *inside* the block: each item marked against the repository's **default branch**, in the same pass that lands it |
| **B1 edits a generator whose CI byte-diffs the page** | low | two-file change; `doc-extract/tests/test_site_committed.py` catches a half-done one |

## 9. Handoff

~~**B0 is this document plus the reconciliation of the three audit files it names.** Then B1 — the `doc-extract`
tile — because a false statement on a published surface outranks a missing one, and H1 is a false statement on
the flagship about the measurement that made it the flagship.~~

**Both landed 2026-09-04.** B0 is `current_projects` `edcf3d4` plus the review corrections in the commit after
it. B1 is `doc-extract` `fix/the-tile-counts-the-result`: the tile now reads `3 / 6` *attacks the gate never
sees*, computed from `results/attack-gullible` by the same call that renders the grid below it, so it is a
measurement rather than a milestone count and cannot go stale on the next milestone.

**B1 found a second instance of its own defect class while looking for a figure to quote.** The prose under that
grid read *"The **two** payloads the arithmetic never sees are …"* and then interpolated a computed list of
**three**. The names came from the artifact; the number was typed. Both now come from the same list.

~~**Next: B2** — the divergence table, at 375 px as the gate and 390 px alongside, with §4.2's marker question
settled before the twenty-two runs rather than during them.~~ **B2 and B3 both landed 2026-09-04** as
[`0007`](0007_divergence-and-the-page-spec.md), which §5's table above already records — so this
paragraph had been stale against its own document since the day it was written. It is the class §2.4
exists to catch, committed inside the file that names it.

**The plan now lives in [`0008_the-rollout-ledger.md`](0008_the-rollout-ledger.md)**, and the carrier
in [`ADR-0004`](../adr/0004_what-carries-the-page-spec.md).

~~Open and unanswered, carried rather than closed: **L2** (action pinning, on the true premises `0003`
§9 decision 2 established) and **L3** (whether Level B survives as a tier).~~ **Both answered.** L2 by
§3 in this document — do not pin, and why. **L3 by [`0008`](0008_the-rollout-ledger.md) §4**: Level B
survives and one row leaves it, because B3 is a *page* of an A-level project rather than a repository.
