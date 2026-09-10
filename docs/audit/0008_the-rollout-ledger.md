# The rollout ledger

Date: 2026-09-05
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`0007_divergence-and-the-page-spec.md`](0007_divergence-and-the-page-spec.md) §5 (the clauses this
rolls out) and §9 (the rollout this supersedes),
[`0006_session3-4-presentation-block.md`](0006_session3-4-presentation-block.md) §5 (B4–B6),
[`0004_session1-recruiter-triage.md`](0004_session1-recruiter-triage.md) §9 (L3),
[`../adr/0004_what-carries-the-page-spec.md`](../adr/0004_what-carries-the-page-spec.md) (the carrier)

---

## 1. What this is, and the gap it closes

A previous session designed this block as ten stages and roughly forty-one pull requests. **None of it was ever
written to a document.** It lived in that session's context and was lost with it; the handoff that survived says
only *"the design is in the block plan"*, and there is no such file. This is that file, and the reason it exists
at all is worth stating: a plan that is not a document is not a plan.

It is a **ledger**, not a table of measurements. `0007` §3 was corrected five times across two sessions because
a measurement inside a normative document cannot be accepted without being frozen. So the split of
[`ADR-0004`](../adr/0004_what-carries-the-page-spec.md) §5 applies here too: `0007` §5 keeps the rules, the
checker will own the conformance table from S2 onward, and **this file owns the plan and its status**.

Each stage is marked against the repository's **default branch** in the pass that lands it — `0003` §9's rule,
applied inside the block.

## 2. Entry state, measured 2026-09-05

No open pull request in the index or in any of the twelve submodules. All twelve pointers equal *and* are
reachable from their `origin/main`. Index `main` at `3feba2a`. The only working-tree noise is untracked local
`.claude/` directories.

### 2.1 Three recorded figures corrected against the repositories

Derived from the repositories at entry rather than from the documents, which is the rule the previous session
earned the hard way. Recorded here rather than silently fixed, because a reader carrying the old figure forward
is exactly how `0006` §2.4 happened.

| the record says | the repositories say |
|---|---|
| L5: the deprecated `license` TOML table form is present *"in all twelve"* (`0006` §3 L5) | **eleven of twelve.** `mini-traceroute` is C++/CMake and has **no `pyproject.toml` at all**. The exemption is structural, not an oversight, and must be recorded — otherwise the next reader finds eleven and goes looking for a twelfth |
| *"62 `Author: P0w3r223` fields across nine repositories"* | **70 fields across ten.** The count omitted the index itself, which holds 8 — and the index is where `0003`–`0005` live. Both self-disagreeing repositories are already half-migrated: `apply-scout` 10 handle / 2 name, the index 8 handle / 4 name at the time of writing |
| `0007` §9 row 5 scopes the contrast repair **by page** | **by token source: three repositories, four surfaces.** Row 5 already named the right three repositories, so this is a re-scoping rather than a refutation — what it missed is that `car-price-ml` has *one* token source feeding *two* published surfaces (`src/car_price_ml/site/assets/tokens.css` is inlined into `docs/index.html`, and `chart.css` is shared with the form by `build.py` and `form.py`), so one hex edit moves both |

### 2.2 What the contrast repair actually is, read from the usage sites

The threshold is decided by how a value is *painted*, not by how it is declared — the step that found the
`--positive` failure at all. Re-derived at entry, and every ratio below recomputed rather than cited:

**Light scheme**, against the light grounds:

| token | value | on `--bg` `#ffffff` | on `--surface` `#f6f8fa` |
|---|---|---|---|
| `--accent-soft` majority | `#93c5fd` | **1.80:1** ✗ | 1.69:1 ✗ |
| `--accent-soft` measured | `#5b93e4` | **3.12:1** ✓ | 2.93:1 ✗ |
| `--positive` majority | `#059669` | **3.77:1** | 3.54:1 |
| `--positive` measured | `#047857` | **5.48:1** ✓ | 5.15:1 ✓ |

**Dark scheme**, against the *dark* grounds — a separate table, and the separation is not cosmetic:

| token | value | on dark `--bg` `#0f1319` | on dark `--surface` `#161c25` |
|---|---|---|---|
| `--accent-soft` majority | `#2c4a7c` | 2.11:1 ✗ | 1.94:1 ✗ |
| `--accent-soft` measured | `#4167a6` | 3.30:1 ✓ | 3.03:1 ✓ |
| `--positive` (uniform) | `#34d399` | 9.69:1 ✓ | 8.90:1 ✓ |

> **The first draft of this file put all six rows in one table headed by the two *light* grounds**, so the two
> dark rows were computed against `#0f1319` / `#161c25` while the header said `#ffffff` / `#f6f8fa`. A reader
> re-deriving `#2c4a7c` from the stated header gets **8.83:1** — a comfortable pass — and drops the ✗. Caught by
> review, and recorded rather than quietly fixed because it is this record's signature defect committed three
> lines above the sentence that names it.

**The ground matters and no document had recorded it.** Parsed from the committed pages, the charts that paint
`--accent-soft` sit at `html > body > figure > div.chart-wrap > svg.chart` — **outside every card** — and
`body { background: var(--bg) }`. So the ground is `#ffffff` and the pinned `#5b93e4` clears the 3:1 non-text
minimum at 3.12:1. On `--surface` it would measure **2.93:1 and fail**. Clause 1's pin is correct; the reason it
is correct was never written down, and a later reader moving a chart inside a card would break it without
noticing.

`mini-traceroute` is the one live AA **text** failure (SC 1.4.3), and it is confirmed independently: `.ledger` parses to
`html > body > div.ledger-wrap > table.ledger`, outside every card, so `.ledger td.probe-ok`
(`docs/assets/styles.css:251`, 0.86 rem / weight 600) and `.verdict .ok` (`:295`, 0.85 rem / weight 700) paint
`#059669` as normal-sized body text on `#ffffff` at **3.77:1** against AA's 4.5:1.

**It is not the only live AA failure, and the distinction is the threshold rather than the severity.**
SC 1.4.11 Non-text Contrast is also Level AA, at 3:1, and the light `--accent-soft` majority `#93c5fd`
measures **1.80:1** wherever it is painted — `car-price-ml/src/car_price_ml/site/assets/chart.css:14` and
`auth-log-scan/src/auth_log_scan/site/assets/styles.css:128, :143`, both `fill:` on chart marks. So S1's
three repositories each carry a live AA failure; `mini-traceroute` is simply the one failing the *text*
criterion, which is why it is the one a reader meets as unreadable prose rather than as a faint mark.

**Two couplings the stage must measure rather than assume, because in both the painted result is not the raw
hex.** `mini-traceroute` paints `--accent-soft` as a *row background* through `color-mix` (`:254`,
`tr.matched`), so changing the token changes the ground under every cell in those rows. And
`auth-log-scan/src/auth_log_scan/site/assets/styles.css:143` paints `.chart .window-band` with
`opacity: 0.45`, so the composited mark is not the declared value either. **Neither is a pure token swap**,
which is what S1's "hex values only" means as an *edit* and does not mean as a *verification*.
*The second of these is what removed `auth-log-scan` from S1 altogether — §3.2.*

## 3. The stages

Every stage closes with a `code-reviewer` pass before it is proposed as merged work. Scope is stated from the
repositories at entry; a stage that finds its scope has moved re-derives it and says so here.

| # | stage | scope, measured at entry | est. | status |
|---|---|---|---|---|
| **S0** | Split `0007`; accept §5 / §5.1 / clause 9 as normative; freeze §3; move §9 here; record §2.1's refuted figures; take the carrier decision (`ADR-0004`) | index only, no code | 0.5 d | **closed** — `current_projects` `89a9cc2` on `main` |
| **S1** | **The contrast repair** — `car-price-ml` (one source, two surfaces), `mini-traceroute` (both tokens). **`auth-log-scan` attempted and reverted, §3.2** | 2 repos, 3 surfaces, hex values only | 0.5–1 d | **closed** — `car-price-ml` `0abbfe3`, `mini-traceroute` `19cda5f`, both on `main` with CI green **on `main`**, not on the PR |
| **S2** | **The checker**, report mode, over all twelve. Static core composed from the two halves of `ADR-0004` §2.1 | `tools/pagespec/`, 253 tests, CI in two jobs | 1.5–2 d | **closed** — `current_projects` `ef3d8c0` on `main`, CI green **on `main`**. §3.5 |
| **S3** | **`apply-scout`** (`0007` row 1) — tokens, dark override, card metadata, `.table-wrap`, drop Inter | 1 hand-written page + its acceptance test | 1 d | **closed** — `apply-scout` `33a8559`, `current_projects` `6b7d3b8`, both on `main` with CI green **on `main`**, not on the PR. Both carriers read a usage site; three review passes were needed to guard all four of the role rule's exception shapes, and §3.10 records why the corpus sweep could not find the last one |
| **S4** | **`mlops-car-price` + `pl-jobs-lora`** (`0007` row 2 = `0006` B4), with clause 9's `mlops` half in the same pass, both pages' card tags (§4.3), **eight tiles now that §5.1's exemption is struck**, and every rounded figure re-quoted | 2 hand-written pages · 14 card tags · **22 literal declaration sites** with one two-role trap on each · 8 tiles · 2 new page tests | ~2 d | **closed** — `mlops-car-price` `e1d797e`, `pl-jobs-lora` `9be52a2`, `current_projects` `d2e96b8`, all on `main` with CI green **on `main`**. The review's four HIGH are fixed and merged too — `mlops-car-price` `9641f07`, `pl-jobs-lora` `879b5df`, both on `main`; the first version of this row said "fixed in #21 / #14" while both were still open, which read as merged and was the same defect §1 forbids. Both pages read `clear`; §4.7 re-derived the scope before the stage, §4.8 records what the quotation rule caught once it was executable, §4.9 what the review found once the guards were mutated |
| **S5** | **Clause 9 on `car-price-ml`** (`0007` row 3, other half) | 1 generated page + regeneration | 0.5 d | **closed** — `car-price-ml` `f1e61a1` on `main`, taken inside the S9b pass exactly as this cell predicted. The bridge names this page's measurement and points at `mlops-car-price` **without quoting its figures**, which §5.0 would forbid; `7140e46` then gave it the guard its twin has had since S4, because the page change alone left it carried by CI's byte-diff — an instrument that would go on passing with the bridge deleted from both sides. §4.17 |
| **S6** | **Back-link + card metadata** (`0007` row 4 = `0006` B5) | 9 repositories, 10 surfaces, measured at entry and reproducing the recorded scope exactly. Card metadata only where a surface had none — §4.3 | 1.5 d | **closed** — nine repositories on `main`, CI green **on `main`**. Clause 6 passes on all eleven committed surfaces; §4.3 says what was deliberately left |
| **S7** | **Naming, the pinned values where nothing paints them, and two live SC 1.4.11 repairs** (`0007` row 6, plus §3.2's two carried items) | **Nine repositories** — the row named four items and one set; the stage re-derived it to nine, §4.6 | 1.5 d | **closed** — nine repositories on `main`, CI green **on `main`**. Clauses 2 and 3 now pass on every committed surface |
| **S-gate** | **Make the checker able to fail**, by clause. A ratchet: gate on the set reporting zero `FAIL` across every surface read, and extend it by one clause as each stage closes | `tools/pagespec/__main__.py`, `.github/workflows/pagespec.yml`, the two tests that pin the exit code, **and `ADR-0004` §6** — the normative home, which still read *"report-only first"*. **No page changes** — §4.11 | 0.5 d | **closed** — `current_projects` `297e3c5` on `main` with CI green **on `main`**. *The first version of this cell cited `043bf72` + `38f26a9`, which are branch commits: this repository squash-merges, so neither is reachable from `main` and neither ever will be — §4.12's last paragraph.* **Fifteen** mutations — twelve red on the guard that names them, one red on nothing in this repository by design (row 8), and **two that reddened nothing at all** until a later pass found the guard absent or out of reach (rows 9 and 15). **Four review passes**, the last three finding fixes that displaced a defect rather than removing it; §4.12 |
| **S9** | **The separator** (clause 8), scoped by formatter rather than by page. **S9a** four repositories, **not build-only in two of them** · **S9b** `car-price-ml`, both surfaces · **S9c** `doc-extract`, a spec amendment and not an edit | **20 non-conforming write sites in 14 files across five repositories and six surfaces**; 7 failing surfaces. *The count is not re-typed again — §4.13 routes the census into the checker's output, and that is S9's first commit* | **2–2.5 d** | **closed** — `ab-lab` `5f3a802`, `it-job-radar` `7e64bd8`, `pl-review-sense` `6f908ec`, `wroclaw-air-insights` `bb881da`, `car-price-ml` `f1e61a1`, all on `main`; the gate widened in `current_projects`. Clause 8 reads `clear` on all **twelve**, and the twelfth was confirmed from the wire before the pointers moved. **S9a was not build-only in any of the four**, not two — §4.17's first finding. *What follows is the state before that closure.* **first commit and S9c closed** — the census prints on every run (§4.15) and clause 8's two amendments plus one recorded refusal have landed (§4.16); `doc-extract` reads clear and no page was edited. **S9a and S9b remain.** Then S9a's four repositories, each its own commit carrying its own test change — the commit that changes `wroclaw`'s separator widens `test_report.py:1524` **and** re-pins `:377` in the same change (§4.13). The `GATED` widening is a separate index commit, after `wroclaw` rebuilds; §4.15's last paragraph is why |
| **S10** | **Clause 4's `<title>` half** — `auth-log-scan` mechanical; `mini-traceroute`, `car-price-ml/app` and `wroclaw` copy decisions. Folds in the guard defect §4.11 records, **which is what makes it four rather than three** | **4 surfaces** · 1 guard | 0.5 d + copy | **closed** — `auth-log-scan` `ddfac46`, `mini-traceroute` `b875b28`, `car-price-ml` `f1e61a1` (the app title, riding with S9b's `:7` and `:27` as §4.13 required), `wroclaw-air-insights` `bb881da`, all on `main`. **The copy cost nothing**: all four are the same words in the other order, and `wroclaw`'s is not a copy decision at all once the comment beside its tags is read — *"figure-free, like every standing sentence on this page"* rules out the alternatives. `og:title` moved with each `<title>`, which the row did not enumerate. §4.17 |
| **S8a** | **The text layers, public half** — the four About codes, their README twins, **six published-page sites, ten cross-references and two package docstrings**, L3, H3. ~~`pl-review-sense` C3~~ leaves for S8c | **26 committed sites across all twelve repositories, plus 4 About descriptions**, re-derived 2026-09-09 — **not the 8 READMEs this row implied.** `0003` §2's scope table (line 31) scoped four layers and the live-site one was lost between `0006` §2.3 and §4.11; §4.20 and `ADR-0007` | 1.5–2 d | **closed 2026-09-09 — §4.21.** *What follows is the state at W2.* **W1 and W2 closed 2026-09-09; W3 and W4 remain.** Twelve sibling pull requests merged and the four About descriptions rewritten, so **no public surface in the portfolio publishes a portfolio code**: the census over READMEs, pages and package docstrings reads zero, and the four account descriptions read back clean. What is left is the index's own half — L3's renumber and H3, which are W3 — and the profile README, W4. *Designed and its copy decisions taken, `ADR-0007`, 2026-09-09.* L3 accepted 2026-09-08 §4, so the renumber rides with the deletion. **W0 is discharged**: the four About descriptions are frozen in `ADR-0007` §2, the baseline table reads zero `FAIL`, and no pull request is open anywhere in the portfolio. *The first census was phrase-based and reported 13 sites in 11 repositories; §4.20's erratum is why the figure moved* |
| **S8b** | **The text layers, contributor half** — the portfolio code in `CLAUDE.md` | **26 sites in 16 files across 10 repositories**, re-derived 2026-09-09 — **not the 12 files this row said**, and the two that are clean are clean because S8a took them (`ADR-0007` D2). Twelve own codes, fourteen cross-references, and **17 decoy hits** in `doc-extract` alone — its own `B0`–`B3` evaluation baselines, in `CLAUDE.md` and in `src/doc_extract/eval/`, where an edit changes behaviour rather than copy | 0.5 d | **closed 2026-09-09 — §4.22.** The row's *"different audience, different argument"* resolved **both ways**, because it is two questions: the fourteen cross-references went and the twelve own codes stayed |
| **S8c** | **`pl-review-sense`'s adversarial set, made visible** — `0005` §7 C3's intent, taken as a question about the page rather than about its `<h1>` | 1 generated page. **`_headline` is not touched** | S | open — split out of S8a by `ADR-0007` D3. **C3 as written cannot be published and inverting the rule was refused on measurement**: `analysis.probe()` scores one model, so *"both models"* is a figure no artifact prints (`0007` §5.0, S4's trap); and state 1 leads because HerBERT **won** — 0.986 against 0.944, McNemar p = 3.1e-06 — so inverting precedence would lead with the baseline's failure and move the conformance table, since clause 4 prints the `h1`. Scoring HerBERT on the challenge set stays available, unscheduled, and costed as the project it is |
| **Sx** | **L5 + the `Author:` finish**, as one sweep on the L1 pattern | 11 `pyproject.toml`; 70 fields / 10 repos. **Both reproduce to the field, 2026-09-07** | 0.5 d | **closed** — eleven sibling pull requests merged, plus `current_projects` `b416c83` (the index's own eight fields) and `d550066` (the eleven pointers), both on `main`. `d550066` is CI green **on `main`**; `b416c83` touches only `docs/**`, which the workflow's paths filter excludes, so it has **no run at all** — the absence is the filter working and not a check that went missing. Header-form author fields carrying the GitHub handle: **0** portfolio-wide, from 70. The deprecated licence table form: **0**, from eleven. *Neither figure is written here as the string it counts — §12.1.2 of `0009` is what that costs.* No page moved and the conformance table is unchanged. §4.14 |
| **S11** | **The gate registry, and the twelfth surface** — `0009` §7 row 13b. `GATED` becomes `GATE`, a registry of `(prefix, state, reason)` with a third state; the ratchet's two guards take their corpus from the mode the run is in; `live` gains the guards it never had | `tools/pagespec/__main__.py`, three test files, `pagespec.yml`, **`ADR-0006`**. **No page changes**, and the conformance table is byte-identical | 0.5 d | **closed** — §4.18 |
| **S12** | **The contrast finding, and the clause that could not see it** — `0009` §7 row 12, opened by measurement. **S12a** `pl-review-sense`'s heatmap share label, a live SC 1.4.3 failure in both schemes · **S12b** `clause_1_composited` learns to read paint alpha in the markup | 1 sibling page + its palette guard · `render.py`, `clauses.py`, one fixture of record | 0.5 d | **closed** — §4.19. **S13 is the rest of row 12** and is scheduled below rather than folded in |
| **S13** | **The contrast census** — an element stream, a selector matcher with specificity, grounds by static-attribute containment, and three keys `UNDECIDED` **by construction**. Row 12's instrument, without its verdicts | `render.py` (the element stream, **landed**), a new `tools/pagespec/contrast.py`, `clauses.check`, `NOT_A_CLAUSE` **and** `spec.NOT_A_SENTENCE` with both their pins, `tests/test_spec.py`'s static source read, a census | **M, 2–3 d** | **closed** — `current_projects` `6bba74f` on `main` (`#107`, nine commits) with CI green **on `main`**. `ADR-0008` is the decision, §4.23 what the first commit measured and **§4.24 what closing it measured** — including four readings the census refuted before a verdict could ship on any of them, which is D2's argument turning out to be worth more than the section that made it. *This cell read `in progress` for a day after the stage merged, and the row above it is the reason that matters: a reader deciding what to take next reads §3, and §3 said the largest open instrument was still being built.* §3.11 stands except its verdict table: D1 replaces *"every preceding painted sibling"* with containment, because **§3.11's worked example does not survive its own rule** on 133 of 139 sites. No `GATE` row and no `report_only()` edit — a census cannot gate |
| **S14** | **The verdicts**, and since §4.25 it is two halves on S12's precedent. **S14a — the control boundaries**, **nine** form controls on two surfaces against SC 1.4.11's 3:1 — 1.17:1 light and 1.29:1 dark, so it is a two-scheme repair — given a token of their own. **Not a sibling stage**: clause 1's role rule admits only `--border` on a border and none of its four exceptions reaches a control, so the index is amended first — a fourth role, its registry pin and its guards — then the siblings, then the pointer bump. *The ninth, `mini-traceroute`'s `#base-port`, is styled by a refused selector and is invisible to the census that found the other eight, so the scope comes from the stylesheets and not from the instrument.* **S14b — the verdicts themselves**: `PASS`/`FAIL` over what the census already resolves, D6's own-background ground, and the cascade an element's single painted colour needs and that no clause-1 check has ever needed, since every one of them is per declaration | `contrast.py`, `GATE`, `tools/spec.py` `c1.s6` and the new `c1.s6b`, `0007` §5 clause 1, `_EVERY_KEY_HTML` — **plus, since §4.25, `ADR-0008` D5 and D6, and whatever the nine control boundaries need, in both schemes**. Re-derived 2026-09-09 from the census: text goes to **zero failures** on the self-as-ground correction alone, the cascade is **542 sites and 525 of them `fill`**, and verdicts over marks without D5 fail **1 195 of 1 785** | **M** for S14b; S14a is S. *The row carried M before §4.25 and the estimate did not move when the scope did — two sibling pull requests, a pointer bump, D5 and D6 to implement, and a 153-site population D5 leaves open* | **closed 2026-09-10**, both halves — §4.26 and §4.27. *This cell opened `open` and stayed `open` after both halves landed, while saying "**S14 is closed.**" far into its own text. §3's status column is what a reader scanning for the next stage reads, and §3.11's erratum records this same table doing this same thing one stage earlier — that cell read `in progress` for a day after S13 merged. Found 2026-09-10 by a grep for open rows, run to check a sentence in `CLAUDE.md` claiming this file has no open stage: the work had none and the column said otherwise, so the sentence was true and uncheckable at once.* **S14a's index half is done, §4.26**: `0007` §5 clause 1 carries a fourth house role, `c1.s4b` is requoted because a fourth role falsified its count, `c1.s4c` records the half `1 usage roles` does not enforce, and `--border-control` is pinned in both schemes. `ADR-0008` D7. No page moved and the conformance table is byte-identical, so five mutations are what prove it. **S14a is closed, 2026-09-10**, in the order the row required: the amendment as `1ba8975`, then the two siblings — `car-price-ml` `a0d19cb` (#32) and `mini-traceroute` `d440ab0` (#10) — then the pointer bump. All three affected surfaces read `clear` with `--border-control` pinned in both schemes, gate 0, suite 610. `car-price-ml` declares the token in the shared `tokens.css` because `test_both_pages_are_built_from_the_same_palette` makes one palette serve both its pages, so its report surface carries the declaration and paints nothing with it — the alternative was a second palette, which that test exists to prevent. The review that closed the amendment found the plan table still carrying the retired count and `ADR-0008` §8 inverting the reason the binding ground binds; both were repaired before the merge. **S14b is closed the same day, §4.27**: `contrast text` and `contrast marks` take verdicts, `0007` §5 clause 1 gains D4's obligation sentence as `c1.s6b`, and both keys leave `NOT_A_CLAUSE` and `NOT_A_SENTENCE`. **Neither key entered the state this row predicted, and the closing review is what found both.** `contrast text` went straight to `GATED_STATE`, not `pending`: a `--fetch` run reads it clean on all twelve, which is the refutation `ADR-0006` §3 says *demands* promotion — and the scheduled `live` job went red against a `pending` row before the merge rather than the morning after, which is §4.15's trap caught by the instrument for the first time. `contrast marks` entered `REPORT_ONLY_STATE` rather than no state at all: the argument below is about `pending` and does not reach report-only, and a key that prints `FAIL` while the run exits 0 with nothing said about it is the exact shape `gate policy` exists to refuse. **S14 is closed.** *What follows is the state before that half.* `ADR-0008` D2, D3 and D4, and **§4.25 is the scope re-derivation, which found the row's central assumption false**: this is not a regression guard over a clean corpus, because nine form-control boundaries on two surfaces read 1.17:1 light and 1.29:1 dark against SC 1.4.11's 3:1. **One key enters as `Ratchet(prefix, PENDING_STATE, reason)`, not two** — the text key, which D6 takes to zero failures. The marks key does not enter `GATE` in any state at S14: 153 SVG sites still measure below 3.0:1 after S14a lands, and `ADR-0006` §3's pending state is refutable in both directions, so a key that can never read clean cannot hold it. `ADR-0008` §7. Not before the census prints: D4's sentence is pinned by a guard the moment it is written. **And the census printed two things the design could not have known, which block the stage rather than sizing it — §4.24 measures both.** *First*, **a site's own painted background is not among its candidate grounds.** `_grounds` walks ancestors from `element.parent` and the preceding siblings that contain it, so a `<button>` painting `background: var(--accent)` on itself has its white label measured against `<body>` — `<button> color` at **1.00:1** on `mini-traceroute` and **1.06:1** on `car-price-ml/app`, the two worst text readings in the portfolio, both against a ground the button covers. Neither is a page defect: the real value is 5.17:1, and `car-price-ml/docs/app/styles.css:225` says so in the page's own comment. **S14 cannot read its own census until a site can be its own ground**, and that is not the cascade. *Second*, the marks question is not the one a design would guess: the worst mark is `<rect class="cell"> fill` at **1.00:1** — `pl-review-sense`'s heatmap cells, whose `fill-opacity` *is* the datum — and the 1.17:1 band holds eight `<input>`/`<select>` borders, which are user-interface component boundaries and the first half of SC 1.4.11's own wording. So **S14 cannot fail anything until it has a rule for which marks a reader must perceive**, and the corpus makes that concrete rather than hypothetical. Both are taken at S14's **scope re-derivation from the census's own output** — §4.7's precedent for the fifth time, and `ADR-0008` §4's own reason 2, *"a census decides with an instrument rather than with this document"* — the marks rule entering as `ADR-0008` D5. *The first version of this cell blamed the absent cascade for the two `<button>` readings and told S14 to cascade first; §4.24's erratum is why that would have moved neither number* |

Roughly **13–14 days** as first written; **+3–3.5 days** for S-gate (0.5) + S9 (**2–2.5**) + S10 (0.5), plus
S10's
copy time, which is not estimated because three of its four surfaces need a claim written rather than a line
moved. §4.11 shows all three were never scheduled rather than newly discovered. S0–S2 are one unit; everything after S3 is schedulable separately.

*S9's figure was 1.5–2 until §4.13. It grew because the stage's S9a half was costed as "four repositories,
build-only" and two of those four are not: one needs a simulation re-recorded and a byte-guarded README
region rebuilt, the other needs a test's number pattern widened in the same commit as the edit. **The
re-derivation happened before the stage rather than during it**, which is §4.7's precedent and the only
reason the figure moved on paper instead of on the day.*

**S8 is no longer last, and it is no longer one stage.** The row placed it last *"because it is the one that
can slip without blocking anything"* — true of the work, and it is now the stage most blocked *itself*: L3's
cost case is refuted (§4.1) and its scope is two to three times its row (§4.11). **S-gate moves to first**, on
§3.1's own reasoning one step further: that section promoted S1 because a row which *stops harm* does not owe
the ordering rule *"prove the spec before applying it widely."* A gate proves nothing and prevents recurrence,
and unlike S1 it costs no page change at all — the clauses it starts with already pass on all twelve
surfaces.

### 3.1 Why S1 moves from fifth to first

`0007` §9 places the contrast repair **fifth**, behind three rows of naming and metadata, while its own row-5
text calls it *"the one item here a reader can be **harmed** by."*

Its stated ordering principle is *"so the spec is proved before it is applied widely."* That principle does not
reach row 5, because **row 5 proves nothing** — it stops harm, and WCAG is a measurement rather than a house
style, so it does not depend on the spec being accepted at all. `0007`'s own row-3 argument, *"a published
contradiction outranks a missing convention"*, is the same reasoning one step further; applied consistently it
promotes row 5 rather than row 3.

And §2.1 shows it is also among the cheapest items in the block: three repositories, four surfaces, hex values
only. **Row 5 gave no reason for its position** — its "why here" column argues harm, which is an argument for
moving it *up*. The position looks like the residue of ordering the rollout by how much of the spec each row
proves, applied to a row that proves none of it.

### 3.2 `auth-log-scan` was in S1, was applied, and was reverted — the token fix makes that page worse

Recorded at length because the reasoning is the stage's own rule turned against the stage, and because a later
reader will otherwise re-derive the change and re-apply it.

The edit was made, the page regenerated byte-identically, forty tests passed, and **it was still wrong**. Two
things the entry scope had not measured:

**Its only passing paint site does not exist.** The commit justified itself on `.chart .bar.muted` and
`.chart .window-band`. `charts.Bar` carries `muted: bool = False` and **nothing in the package ever sets it** —
the published page holds 16 `class="bar"` and **zero** `class="bar muted"`. That rule is inherited from the
shared design language; `pl-review-sense` emits it, this repository does not. So the only live paint site is
the band.

**And the band is painted on `.lane`, not on the page.** `.chart .lane { fill: var(--surface) }`, and the band
rect is emitted immediately after the lane at the same `y` and `height` — verified in the shipped artifact,
row `192.0.2.11`: lane `x=132 y=200 w=466 h=22`, band `x=132.0 y=200.0 w=466.0 h=22`, the full width of the
lane. The marks are emitted **after** the band and sit on it. So the band composites over `--surface`, and the
marks composite over the band:

| mark | before | after |
|---|---|---|
| `.ev-failed` (`--accent` @ .85) | 3.12:1 ✓ | **2.61:1 ✗** |
| `.ev-invalid` (`--warn` @ .90) | 3.31:1 ✓ | **2.75:1 ✗** |
| `.ev-accepted` (`--positive` stroke) | 2.81:1 ✗ | 2.27:1 ✗ |

**Two marks cross from passing SC 1.4.11 to failing it, inside the commit that exists to satisfy SC 1.4.11**,
and the band itself stays under 3:1 either way (1.26:1 → 1.56:1 against the lane). The change fixed nothing
live and degraded two things, so it was reverted rather than shipped with a caveat.

**Two items this leaves, both new:**

- `auth-log-scan` **cannot take the pinned token value without a usage-site change** — the band needs its own
  value or a lower opacity, chosen against `--surface` with the marks composited on top. That is outside S1's
  agreed boundary and belongs with the naming and usage work in **S7**.
- `.ev-accepted` measures **2.81:1 on the band today**, before any change. A pre-existing SC 1.4.11 failure
  that no sweep had found, because every previous pass measured tokens against page grounds rather than marks
  against what they are painted on.

*The general lesson, and it is sharper than "measure the ground": a token's ground can be **another element the
same token paints**. The stage rule — read the threshold per usage site — was right and was applied one layer
too shallow.*

**This is a third constraint on S2's checker**, alongside the two in [`ADR-0004`](../adr/0004_what-carries-the-page-spec.md)
§4.1: it must resolve a mark's ground by **paint order within the SVG**, not by the nearest card or the page.
A checker that walked to the nearest ancestor with a background would have cleared this change, because the
band and the marks share an ancestor and the band is a sibling drawn before them.

### 3.5 What S2 settled, and the one thing it deliberately refuses to say

**The checker reproduces `0007` §3 on every comparable cell** — tokens, dark, tiles, eyebrow,
scroller, card meta, back-link, webfont, `<title>`, and the separator inventory that took four hand
attempts to get right. §5's aggregates fall out of it too: 61 plain-space figures of 85. That is the
freeze decision of [`ADR-0004`](../adr/0004_what-carries-the-page-spec.md) §5 vindicated — the table was
correct as of 2026-09-04 and is now computed rather than maintained.

**Two cells do not match, and both are the checker being more precise than the table.** §3 gives
`wroclaw`'s scroller as `.chart-wrap` + the table itself; `.chart-wrap` wraps a chart, not a table, so
only the second half is true of any table on that page. And §3 calls that page's `<title>` the
repository name, where mechanically *"Wrocław Air Insights"* does not lead with the directory
`wroclaw-air-insights`. Neither is a defect on either side; both are recorded so the next reader does
not treat the difference as drift.

> **Erratum — §4.11.** The second half is reversed. *"Neither is a defect on either side"* was measured
> against the **guard** (`clauses.py:568`, `startswith`), not against the **clause**: §3 was right and the
> checker is wrong, because `ł` and the space-for-hyphen are what the comparison fails on, not the naming.
> Normalised, the title reduces to exactly the repository's three tokens. **S10 repairs the guard, and
> `wroclaw` becomes its fourth surface.**

**What it refuses to say is the part worth keeping.** Every `color-mix` or `opacity` usage is reported
`undecided`, never as a verdict, because resolving one needs the ground the mark is *drawn over* and
paint order inside an SVG is not recoverable from a stylesheet. That is §3.2's lesson encoded rather
than restated. Clause 3 answers `undecided` for the same reason when a page's only scroller is the
table itself: the rule sits inside `@media (max-width: 640px)` and the reader does not carry media
conditions, so it cannot tell a scroller that always engages from one that engages on a phone.

**Three clauses remain outside it**, and §7 rather than silence is where they belong: whether an `h1`
states a claim, whether a scroller is *at or below the card* and *has somewhere to scroll* (both need
geometry), and whether two pages agree on a shared fact (§6 clause 9).

### 3.3 What `car-price-ml` traded, recorded rather than fixed

`.chart .bar` is `--accent-soft` and `.chart .bar.served` is `--accent`, so raising `--accent-soft` toward
`--accent` narrows the served/rejected pair from 2.87:1 to 1.66:1 light (3.66:1 to 2.34:1 dark). **SC 1.4.11's
adjacency requirement does not reach it** — the bars are at `y` 17, 47 and 77 at height 16, so 14 px of page
ground separates them, and the criterion each bar owes is against that ground, which the change moves from
**1.80:1 (failing) to 3.12:1 (passing)**. The distinction it weakens is carried by the prose under the figure,
which names the served model; colour is a second reading, the same defence `mini-traceroute`'s stylesheet
states for its swatches. Taken deliberately, not overlooked.

### 3.4 `mini-traceroute` is one repository with six items, not six rows that mention it

It carries both live contrast failures, the unwrapped `<figure>` table, a descriptive `h1`, a repo-name
`<title>`, the `.ledger-wrap` name and the B1 About code — and it has no `pyproject.toml`, so it can host no
per-repo Python test and is covered by the index checker alone (`ADR-0004` §4). S1 pulls its worst item forward;
the rest stay in S7 and S8, but it should be *planned* as one repository rather than discovered six times.

> **Erratum — §4.11.** *"The rest stay in S7 and S8"* did not hold for the `<title>`: **S7 closed without it
> and S8's scope list never contained it.** §4.11 calls this the sharper instance of the whole finding — an
> item routed to two stages, neither of which was going to carry it. It is **S10** now.

### 3.11 S13's design, taken before the stage rather than during it

§4.7's precedent, applied to the largest open row. Every figure below is measured against the
pinned gitlinks; §4.19 is where the measurements are.

**What a usage site is: an element, not a selector.** `auth-log-scan` settles this on its own.
`.ev-failed { fill: var(--accent); opacity: 0.85 }` matches elements in three places on that
page — a legend swatch on `--bg`, chart 1 on `--bg`, and chart 2 inside
`<g class="row">` → `<rect class="lane">` → `<rect class="window-band">`. A rule-keyed clause has
to pick one ground for that selector and is wrong twice. `0008` §3.2 is the record of a checker
resolving against the nearest card and clearing the change that had to be reverted.

**Grounds by paint order, and the verdict is asymmetric.** This is what lets the clause ship
without a geometry engine, which is the part that would make it L:

| verdict | against what | why it is earned |
|---|---|---|
| `PASS` | **every** candidate ground — the ancestor chain and every preceding painted sibling in the enclosing `<svg>` | a universal over a superset of the true ground |
| `FAIL` | the **ancestor chain only** | containment is structural; a sibling's coverage is geometric and unknown |
| `UNDECIDED` | a site clearing its guaranteed ground and failing a candidate | names the candidate and the ratio, and hands it to that repository's own page test |

Worked against the corpus, measured: `auth-log-scan`'s `.ev-failed` marks clear `--bg`
(**3.98:1**), the lane (**3.79:1**) and the band (**3.09:1**, which is the figure that page's own CSS comment carries), so they `PASS` **without the
clause ever knowing which marks touch the band** — that band is 13.2 units wide on a 466-unit
lane in one row and 358.5 in another, which is exactly the geometry this avoids needing.

**Three keys, and not one of them may start with `1 `.** `_gated` tests
`clause.startswith(prefix)` and `GATED` already holds `"1 "`, so `1 contrast text` would gate
from its first commit — the opposite of shipping report-only. `contrast text` (SC 1.4.3),
`contrast marks` (SC 1.4.11) and `contrast ground` (the ground could not be resolved;
`UNDECIDED` by construction, the twin of `1 composited`).

**Where each key goes, and this is what S11 built.** `contrast ground` is `NOT_A_CLAUSE` — it
can never be `PASS` or `FAIL`, which is that set's entry condition and its own pin. The other
two are `Ratchet(prefix, REPORT_ONLY_STATE, reason)` in `GATE`, and adding them means editing
the `report_only()` pin, which is the second deliberate edit S11's review insisted on. *Row 12
said `NOT_A_CLAUSE` for all of it; that route is refused by the guard beside it, since a
contrast clause passes on a conforming page.* And `_CSS_DERIVED` gains `"contrast "`, or an
unread stylesheet produces contrast failures on a sheet the run never opened.

**What must be `UNDECIDED` rather than guessed**, each with the corpus reason it is on the list:
an unresolvable value (`resolve()` returns `None`); a 4- or 8-digit hex, which `colour.rgb`
already refuses; an ancestor chain reaching no painted background — **do not assume white**; an
ancestor carrying `opacity`, which flattens its whole subtree; a rule inside a non-`prefers-`
`@media` block, because `css.rules()` drops the condition by design and such a rule currently
reads as unconditional; font size or weight unresolvable, since the 4.5/3.0 split turns on it;
and **a selector matching no element in the static document** — `mini-traceroute` builds its
entire diagram in `app.js`, so sixteen paint rules there match nothing, and that is
`contrast ground`, never `n/a` and never a pass.

**One departure from row 12's wording, stated rather than taken quietly.** The row says
`UNDECIDED` for `color-mix()`. Over a *known* ground it is decidable with `resolve()` +
`composite()`, which is what those two functions were built for and why they have shipped
unused since S2. Decide it.

**A fourth verdict row, and the review of S12b is what found it missing.** An element that a
later sibling in the same `<svg>` may be drawn over is `UNDECIDED` **as a mark**, with its ratio
printed. Not because its ratio is unknown — it is not — but because *whether it is a mark at
all* is unknown: a region another element is painted onto is a ground in every page in this
corpus, and no structural signal separates a highlight band from a data mark. This is the same
asymmetry as the rows above, one notch further out: the clause refuses to `FAIL` where the
answer is not guaranteed, and a **role** it cannot establish is such a case.

*Note what this costs and what it does not.* Every mark that has something drawn over it drops
to `UNDECIDED`, which on this corpus is chart furniture and highlight regions. Every leaf mark
— the ones a reader is meant to read a value from — keeps its verdict.

**And that is why the governing-rule escape stays deferred.** `auth-log-scan`'s window band
measures 1.27:1 against its lane and **1.29:1 against `--bg`**, and the page measured that and
wrote the reason in a CSS comment — which `0007` §5.0 says wins and no checker can read. It
looked like this forced a `data-contrast="by-design"` amendment to §5, on clause 3's
`data-scroll` precedent. Under the row above it does not: the band is a candidate ground for
the marks that follow it, so it reports `UNDECIDED` with 1.29:1 printed, and a reader sees the
number without the gate claiming anything.

*The first version of this paragraph deferred the amendment on a rule that does not exclude the
band — "the band has marks drawn over it, so it is a ground and not a site, and v1 scopes marks
to elements with no painted descendants." The marks are the band's **siblings**, as this section
says three paragraphs above, so the band has no descendants at all and neither clause reaches
it; under the `FAIL` row it would have measured against its ancestor chain and reported 1.29:1
as a failure on a page that recorded its reason. A design deferring an amendment on a rule that
does not do the work is the confident-wrong-verdict shape this whole package refuses, written
into the design for it.*

**Sequencing.** The element stream and the matcher land first with their own guards, then the
clause; `spec.py` `c1.s6`, `GATE`, `NOT_A_CLAUSE`, `_CSS_DERIVED`, `test_published_surfaces`'s
`CLAUSES` tuple and the census go in **the same commit as the clause**, because each of them
fails silently on its own. `clauses.py` is 1 225 lines against this project's own 800 ceiling,
so the clause is a new module and not another function there.

### 3.6 S3 was written and was not done — the defect it fixes was unguarded by both carriers

**Recorded as a blocker rather than as progress**, because the page and the checker both report it clean.

S3's substantive fix was a token migrated **by value instead of by role**: `#eef1f6` carried two roles on that
page, and the table separator was mapped to `--surface` where six sibling pages use `--border`. That is fixed.
What is not fixed is that **nothing detects it coming back**. Reintroducing exactly that line leaves
`apply-scout`'s 300 tests green and the checker reporting the page `clear`.

Both carriers read the **`:root` block** and nothing reads a **usage site**, so the whole class is invisible to
them: a role swapped for another declared role, `code { background: var(--border) }`, or `--radius` deleted
while `.card` and `.kpi` still paint it.

**And the commit message over-claims.** It lists the mutations that prove the new tests, and the one it names
for this defect is *a literal creeping back into `th, td`* — a different and easier mutation than the wrong
*token* the commit actually repaired. The easy one turns the suite red; the real one does not. *This is the
record's own signature failure committed in the sentence asserting the opposite, and it was caught by review
rather than by me.*

**What the next session had to close, all measured — and all closed 2026-09-05:**

| | | closed by |
|---|---|---|
| **HIGH** | Assert the token **at the usage site**, in the shape the existing wrapper test uses — behaviour, not names. That also makes the page's own CSS comment about the two roles enforceable instead of advisory | Both carriers. `1 usage refs` / `1 usage roles` in the checker, over all twelve surfaces; `tests/expected/docs_page_tokens.md` in `apply-scout`, thirteen rows approved cell by cell. §3.7 |
| **MEDIUM** | `_resolve_chain` treats *"the chain ends at a non-hex value"* as *"the chain goes nowhere"*, so an alias ending in a length or a font stack reports `FAIL — resolves to nothing`. No page triggers it today, and **S7 is scoped to exactly the two shapes that will** — `mini-traceroute`'s extensions and `wroclaw`'s absent `--radius` | Repaired **before** S7 rather than inside it. The resolver returns the terminal value whatever its type, and carries *why* a chain failed. **Removed from S7's dependency list** |
| **MEDIUM** | The two carriers disagree on four inputs. Sharpest: `HOUSE_PALETTE` in the per-repo test omits `--radius`, which is the one token this session singled out as accident-prone, so that test covers nine of clause 1's ten | **It was five, not four** — §3.7. `HOUSE_PALETTE` gains `--radius`; `HOUSE_TOKENS` gains `--accent-soft` and `--positive`; the checker gains the literals clause it never had; the title check is rewritten; the usage-site walk is new in both |
| **MEDIUM** | The title test's second half passes on any title sharing one word with the `h1` | It passed on the *first* word, which on this page is *"This"*. Now: the two surfaces state the same claim, so one contains the other once whitespace is normalised |
| **LOW** | A literal inside the dark block but outside its `:root` survives; a mutual cycle is caught with the wrong message; clause 7 passes a third-party stylesheet whose host has no *"font"* in it | First two closed. **Clause 7's stands, and is carried rather than fixed**: `sources._with_styles` already files a third-party sheet under `unreadable`, which surfaces as an `undecided` *"stylesheets"* finding, so it is quiet rather than silent |

### 3.7 What closing S3 found, which is more than S3 was about

**Every guard on both branches was proved red by the mutation it names**, by running each. That
instruction came from §3.6's own HIGH — a commit message that asserted an equivalence between
two mutations that does not hold — and it earned its keep three times.

*Read on its own this section says the work was finished here. It was not: two further review
passes each found a shape of the role rule with no guard on it at all — §3.9 and §3.10 — and a
guard that does not exist cannot be green under its mutation, which is the gap this sentence
does not cover. **Moving a fact into one cell does not sweep the prose that argues from it**,
which `0007` §8.5 named and this paragraph then demonstrated.*

- **Two of the twelve new guards were green under the mutation they name, and both were mine,
  written in the commit immediately before.** The mutual-cycle test asserted `"cycle" in
  detail`, and the direct-self-reference sentence also ends in the word *cycle*; and the
  cycle-detection `seen` set was never exercised at all, because the fixture's second hop
  lands back on the name the walk started from. *The guard was written for a defect and proved
  by an easier mutation than the one it claims to stop — §3.6's finding, one layer in, in work
  written to close §3.6.*
- **The carriers disagreed on five inputs, not four.** The fifth is the sharpest and was in
  neither the ledger nor the review: **the index checker implemented no literals-outside-`:root`
  clause at all.** `0007` §5 clause 1's third sentence was enforced on **one surface of twelve,
  in one scheme of two**. The cause is structural rather than an oversight — §3.5 records that
  the checker reproduces `0007` §3 on every comparable cell, and §3 has no literals column,
  because it encodes literals-versus-tokens as a page-level binary. **The checker was composed
  from the frozen table's columns rather than from the normative clauses' sentences**, and that
  is a thing to check for the whole of S6 and S7, not a one-off.
- **It found a live defect on its first run**: `car-price-ml/docs/app` publishes
  `button { color: #ffffff }` — a literal outside the token block, on a published surface, that
  nothing in this portfolio could see. Taken in **S6**, which visits that surface anyway.
- **`HOUSE_TOKENS` held eight of clause 1's ten**, so `--accent-soft` and `--positive` — the two
  the clause argues hardest about — were the two whose *absence* it could not report; `PINNED`
  answers `n/a — not declared`, which is not a miss. Every surface with a `:root` already
  declares all ten, so the correction moves no cell.
- **A published figure in `apply-scout/docs/index.html` was wrong**: *"Six sibling pages"* write
  `border-bottom: 1px solid var(--border)`. The trees hold **seven**.

**And a figure in this session's own work, corrected one commit later — not before it was
committed.** The census behind `0007` §5 clause 1's new sentence was first written as *124
declarations, 108 naming the house role* — 124 minus the sixteen exceptions, without excluding
the eleven `color-mix()` declarations the clause does not reach. Measured: **124 total, 11
`color-mix`, 113 remaining, 97 conforming, 16 exceptions** in four shapes. The subtraction was
the whole error, and it is the class `0007` §8.4 names: a number nobody re-derived because it
looked derived.

*A first draft of this paragraph said "corrected before it was committed", which the branch's
own history refutes: `d2d1af8` carries 108 in the docstring **and in its commit message**, and
only the docstring was corrected. **A commit message is a published artifact in this record** —
§3.6 blocks S3 partly over a claim in one — so the correction note was itself a claim the
repository refutes, inside the paragraph written about that exact failure. Caught by review.*

### 3.9 The review blocked, its HIGH was real, and its fix reached one of the two holes

The guard `1 usage roles` shipped with was **proved on the one page where its weakness does not
open.** Two of the four exception shapes were keyed on conditions that conforming rules already
satisfy, so the exemption fired on the mutation rather than on the exception:

| shape | the condition | what satisfies it after a swap |
|---|---|---|
| *its own fill* | the border names the role its own background names | `.card { background: var(--surface); border: 1px solid var(--surface) }` — the S3 defect itself |
| *filled control* | the rule also declares `color` | `body { background: var(--bg); color: var(--text) }` — on every page |

**Measured by sweeping every conforming declaration on disk, one at a time, each swapped to
the other family's house role: the guard takes the checker from 55 of 97 caught to 97 of 97.**
Unguarded it misses **42** — 31 of 56 in the border family, 11 of 41 in the ground family. The
exemption census reads **16 either way**, because those sixteen name a non-house role today and
`_role_exception` is never consulted for the other 97; *the census cannot show the hole and the
sweep can*, which is worth carrying into S6 and S7.

Per surface, unguarded: the border swap was silent on **eight** of the nine tokenised surfaces —
`apply-scout` the only escape, because its `.card`, `.kpi` and `th, td` declare no background in
the same rule — and the ground swap on **all nine**, `apply-scout` included, through its own
`body { background: var(--bg); color: var(--text) }`. *That is §3.6's HIGH one repository over,
in the branch written to close it, and it matters most on the four surfaces with no page test —
`mini-traceroute`, `mlops-car-price`, `pl-jobs-lora` and `wroclaw` — where this checker is the
only carrier there is.*

*A first draft of this paragraph said **"silent on seven of the nine"** and that `apply-scout`
was "the one page where the weakness does not open". Both are wrong, and both were **taken from
the review rather than measured** — the figure is eight in one family and nine in the other, and
`apply-scout`'s weakness does open, just not for the border mutation that repository ran. A
number inherited from a reviewer is exactly as unverified as a number inherited from a document,
and this paragraph is about publishing figures the repositories refute.*

**The review's diagnosis was exact and its proposed fix reached one hole of the two.** It
suggested `role not in _GROUND_ROLES`; `--border` is not a ground role, so
`body { background: var(--border) }` stays exempt under it. The condition has to deny **every**
house role, which is also the more honest statement of what the shapes describe — a surface
painted deliberately outside the house scheme.

**And the first fix put that condition on three shapes of four.** A second review pass found the
rail unguarded: keyed on thickness alone, `.result.pending { border-left: 3px solid var(--border) }`
in `car-price-ml/docs/app` — a thick one-sided border that *is* the box's edge — stayed exempt
when its role was swapped. One live declaration, on the surface CI does not byte-diff, and the
sweep stood at **96 of 97** while this document claimed all nine surfaces were covered. *A guard
put on three shapes of four is the same defect as no guard, one instance wide, and it is the
third appearance of this class on this branch.*

Applied to all four, the corpus census is **unchanged to the cell** (124 / 11 / 113 / 97, and
11 rail + 3 filled control + 1 own fill + 1 focus ring) and the sweep is **97 of 97**.

Three smaller findings closed with it, and one carried:

- **The code's focus-ring exemption was wider than the sentence licensing it** — all six border
  properties where §5 says `border-color`, and `":focus" in selector` matched inside a quoted
  attribute value. §3.8's argument for amending the spec was that a rule in code with no
  normative statement is this record's failure inverted; a normative statement *narrower* than
  the code is the same gap facing the other way. Narrowed to the spec.
- **`_census` was 45 lines of new reporting with no test**, while §3.8 leans on it as S6's
  report-only observation. Three tests now.
- **Reference integrity read the light palette alone**, so a rule inside the dark block painting
  a dark-only token would report `undeclared`. The first repair admitted such a token
  *everywhere*, which is a rule wider than the comment licensing it — the focus-ring finding
  facing the other way, in the commit that closed the focus-ring finding. `cssmod.split_schemes`
  now carries which half a site is in, so the dark-only token is admitted inside the dark block
  and still refused outside it. Latent either way — no surface holds one — and S7 rewrites nine
  palettes, which is when it would have appeared.
- **The `--only` census test asserted nothing in the job that runs it.** It called `main` against
  the real working tree with no `submodules` marker, so in `core` — the job that must never go
  red, checked out with no submodule — there was no page on disk and the census was empty
  whether or not the suppression existed. Moved onto the fixture, *and the fixture turned out to
  paint no token either*, so the same vacuum would have survived the move: it now paints two, and
  a sibling test asserts the census **is** printed without `--only`, which a suppression that
  suppressed always would fail.
- **Carried:** the census prints 113 where the spec headline is 124, because it excludes
  `color-mix()`. Labelled rather than reconciled; they are two different quantities and the
  label now says which.

**The pattern the passes are really about, and it is about this file.** Three of the second
pass's four findings are *the same defect as the finding they were written to close, displaced
by one step*: a guard on three shapes of four; a repair wider than its own comment, in the commit
that closed a repair wider than its own comment; a test moved onto a fixture that turned out to
be as empty as the tree it came from. **The fixes were not careless — each was verified against
the case it names.** Verifying *the case it names* is exactly what §3.6 blocked S3 for.

### 3.10 The third pass, the fourth appearance, and the limit of the sweep

**A third review pass found the guard on three shapes of four again — the focus ring this
time** — in the paragraph above, which had just declared the third instance closed. The
condition went on the rail, the filled control and its own fill; the focus-ring branch kept a
test on the property and the state alone, so `input:focus-visible { border-color: var(--surface) }`
was exempt while the identical declaration without the pseudo-class failed. Both the docstring
and `0007` §5 clause 1 stated it was on all four. *Two published statements, one of them
normative, refuted by six lines of code beneath them.*

**And this one the sweep could not have found.** No page writes a `:focus` `border-color` in a
house role, so 97 of 97 was true and the guard was still incomplete. That is the honest limit of
the instrument §3.9 recommends: **a corpus sweep proves the rule against the corpus, and the
corpus is not the rule.** What found it was reading the four branches against each other — which
is the argument for keeping them in one function rather than one per shape, and for the test that
now walks all four together and fails when the next one is omitted.

Two more from the same pass:

- **`split_schemes` is not a partition when a dark query nests inside a dark query.** `finditer`
  resumes just past the opening brace rather than past the block, so the inner match is taken
  twice and the excision index is rewound behind itself: the inner rules are emitted twice, the
  outer block's remaining rules land in *both* halves, and the rewound tail welds the outer `}`
  onto the next selector. The code is byte-identical to what `palettes()` held before the
  extraction, so the diff introduced no regression — it introduced a **second consumer whose
  correctness depends on the split being a partition**, and clause 1's verdicts, the reported
  site strings and the census counts all now ride on it. **It fails silently green.** Fixed, and
  `tests/test_css.py` asserts the partition directly rather than through `palettes()`.
- **The refuted "seven of the nine" was corrected in two documents and left standing in a third
  place** — a test docstring. The erratum and the figure it corrects were three files apart.

*The extraction was checked the way §3.5 of this ledger checked the whole checker: `palettes()` after the
refactor agrees with the pre-refactor implementation on every one of the eleven surfaces, to the
key and the value. That is what said the refactor was safe; it is also what could not say the
partition was, because no surface on disk nests a dark query.*

**S6 and S7 should sweep, not spot-check** — and where a rule has branches, read the branches
against each other as well, because a sweep only ever proves what the corpus happens to contain.

### 3.8 `0007` §5 clause 1 gained a fourth sentence, and why that was the decision rather than the work

The HIGH could not be closed by a test alone. **Nothing in the normative spec said which role
belongs where** — clause 1 had three sentences and none of them is the rule §3.6 asks to
enforce — so a test asserting it would have encoded a rule with no normative home, which is
this record's signature failure inverted: not a document contradicted by the repositories, but
a rule in code that no document states.

The user took the decision to amend. `ADR-0004` §5 permits it: a document stating *measurements*
must be frozen, a document stating *rules* can be accepted and therefore amended, and §5 is the
normative half of `0007` rather than the frozen half. The sentence is written as a **description
with its exceptions counted**, in §5's own stated method, so a reader can re-derive it from the
repositories rather than believe it.

**Three options were measured and two rejected on evidence rather than taste.** A contrast band
at the usage site was refuted by measurement: the separator swap moves the row rule from
**1.24:1 to 1.06:1** light and **1.40:1 to 1.09:1** dark, both far below any WCAG threshold —
a table separator is decorative and SC 1.4.11 does not reach it — so any bound between 1.06 and
1.24 is a house number with a 0.18 margin. Worse, the mirror mutation
`code { background: var(--border) }` *raises* contrast, 1.06 → 1.24, so a lower bound misses it
entirely. A per-repository snapshot alone was rejected as *sufficient* for the same reason
`ADR-0004` §6 gives: its ceiling was the seven repositories with a page test, and the four that
could not see the rule were `mini-traceroute`, `mlops-car-price`, `pl-jobs-lora` and `wroclaw`.
**That is no longer the count.** `ADR-0004` was amended twice on 2026-09-06: `wroclaw` gained page
assertions in S6 and S7, S4 gave them to the other two, and the uncovered set is now
`mini-traceroute` alone — where the exemption is structural. It is kept as the second carrier,
not as the only one.

## 4. L3 — the recommendation

`0004` §9 left this open as *"whether Level B survives as a tier at all once `token-budget` and `pl-review-sense`
join it — it will then hold five items of three quite different kinds."* `0006` §7 then excluded it for having
*"no new evidence"*. **That ground is gone**: the evidence is in the index's own `README.md`, and it is sharper
than the question anticipated — the tier holds **four** kinds, not three.

| row | what it is | kind |
|---|---|---|
| B1 `mini-traceroute` | repository, has a page | breadth proof outside the target roles |
| B2 `auth-log-scan` | repository, has a page | breadth proof outside the target roles |
| **B3 `car-price-ml frontend`** | **a page of an A-level project — not a repository** | **category error** |
| B4 `pl-review-sense` | repository, has a page | a full project demoted on its *headline* |
| B5 `token-budget` | repository, **Site column `—`** | deliberately page-less, pre-authorised by `0004` |

**Recommendation: Level B survives, and exactly one row leaves it.**

> **Accepted 2026-09-08.** The recommendation below is the decision: B3 dissolves into A3, Level B keeps four rows, and `B4` → `B3`, `B5` → `B4`. Taken by the portfolio's owner, which is what this row always needed — §4.1 settles the *cost* and could never settle the *ranking*, and `0004` §9 left it open across two audits for that reason.
>
> **S8a is unblocked.** §4.1's ordering constraint stands and is now live: the renumber touches `pl-review-sense/README.md:8` and `token-budget/README.md:6`, and S8a deletes both lines — so the two are **one change**, and taking them separately edits the same two lines twice.

**Dissolve B3 into A3.** It is a surface, not a project: `car-price-ml/docs/app/index.html`, already linked from
A3's own row (`🌐 · 🧮`). Listing it as a ranked portfolio entry is what created `0007` §7's *"twelfth
surface"* — a published page no clause could confidently bind because nobody agreed what it was. Its JavaScript
claim is real and must not vanish; it folds into A3's description, where the reader already is.

B5's empty Site column is **not** a second category error. `0004` demoted `token-budget` deliberately and
redefined the tier so it *"no longer promises an exhibit"*. That reasoning stands and is not reopened here. It
is worth stating that the tier still *reads* as an exhibit tier to anyone scanning the Site column, and that is
the price of the choice, not a defect in it.

### 4.1 The consequence that was argued to make S8 cheaper — and the argument the trees refuted

Removing B3 renumbers the tier: B4 → B3, B5 → B4. Those codes are published — in four GitHub About descriptions
*and* in the committed READMEs behind them (`auth-log-scan/README.md:11`, `mini-traceroute/README.md:13`,
`pl-review-sense/README.md:8`, `pl-jobs-lora/README.md:6`). Renumbering them across two surfaces each would be
work created by the fix.

**Measured, the renumbering costs nothing — and that is not the reason to remove the codes.** The two rows that
move are `pl-review-sense` (B4→B3) and `token-budget` (B5→B4), and **neither publishes its current B-code**:
`pl-review-sense/README.md:8` publishes `A4` and `token-budget/README.md:6` publishes `A6` — both stale codes
from before their demotion. `mini-traceroute` (B1) and `auth-log-scan` (B2) sit *above* the removed row and do
not move at all. So renumbering touches zero published surfaces.

> **Refuted by the trees, 2026-09-07 — and by this record's own repair.** Both stale codes were corrected in
> §4.10's documentation round the day after this paragraph was written: `token-budget` `6605324` (*"A6 was
> renamed B5 two audits ago"*) and `pl-review-sense` in the same round. `pl-review-sense/README.md:8` now reads
> **B4** and `token-budget/README.md:6` reads **B5** — their *current* codes. **So the renumbering now touches
> two committed README lines**, and the measured-cost case above is false as written.
>
> *The conclusion survives and the reasoning changes.* If S8a deletes the codes from those READMEs, the
> renumbering is free **because the lines are deleted**, not because they are stale — which makes L3's renumber
> and S8a's removal **one change rather than two**, and taking them separately edits the same two lines twice.
> That is an ordering constraint the paragraph above cannot state, because it was written when the lines were
> already wrong for a different reason.
>
> **And a fix in one place invalidated an argument three files away.** The four precise README references are
> what made this cost case read as measured — §4.1's own erratum says exactly that of its predecessor, one
> paragraph down. It was refuted not by drift but by this record repairing the very lines it was citing, which
> is a failure mode neither §8.4 of `0007` nor §3.7 of this file had named: **a citation can be invalidated by
> your own correctness.**
>
> One consequence is live and unscheduled: `pl-review-sense`'s GitHub About still reads *"Portfolio A4."* while
> its own README now reads `B4`. **Two surfaces of one repository contradict each other today**, which is what
> H3 and M4 are about, and the README half was fixed without the account half.

*A first draft of this section argued the opposite — that keeping the codes would force a renumber across two
surfaces each, and so that L3 decided the other way would double S8. It cited four README lines that each
refute it. Corrected by review; the four precise references were what made an unmeasured cost case read as a
measured one.*

**The codes still come off the public surfaces, on the argument that was always sufficient:** `0006` §2.3's
finding that a recruiter cannot decode them, and that two repositories publish a code the index contradicts.
What L3 settles is narrower than a cost — it is *which* ranking the index holds once B3 is no longer a row,
and **S8a** cannot rewrite an opening line without knowing that. *§4.11 splits the stage; this constraint
follows the public half, because §2.3's recruiter argument is what reaches a published surface. `CLAUDE.md`
(S8b) needs its own reason and is not blocked on L3.*

### 4.2 S4's copy decision was taken, and it grew the stage

`0007` §5.1 records that `pl-jobs-lora` has **no tiles, no generator and no committed table to quote**, so a
tile mandate would make it print a figure no artifact produces — which this portfolio's own standard forbids.
Three ways out were put to the user: an honest headline about the baselines measured before the fine-tune
exists; dropping `pl-jobs-lora` from S4 and taking `mlops-car-price` alone; or **building the artifact first**.

**The user chose to build the artifact — and the repository had already built it.** `pl-jobs-lora` commits
`results/eval/report.md` and `report.json`, generated by `src/pl_jobs_lora/eval/report.py`, covered by
`tests/test_eval_report.py`, and **quoted by its own page since 2026-08-21**. `mlops-car-price` commits three
such tables. `0007` §5.1's premise was false when it was written, and is now struck there.

**So the item that grew this stage does not exist as work, and the estimate returns to ~2 days.** The scope
that remains is larger than the row in a different direction — §4.7.

*The decision is not thereby wasted: it was the only one of the three options that removed the exception
instead of recording it, and the measurement shows the exception never held. What the choice was really
protecting — **which claim each page opens with** — was untouched by it and is settled in §4.7.*

*The re-read §5.1 asked for has a stronger answer than anticipated: not "after S4 only one page cannot source
a figure" but **neither ever could not**. An exemption granted from a document rather than from the
repositories is the failure this record's §2 method exists to prevent, and it stood for two weeks.*

### 4.3 What S6 covered, what it left, and the defect it turned up

**Scope derived from the repositories, not from the row.** The S6 row reads *"back-link + card metadata"*
in its title and *"the back-link is what they need"* in its body, and the body is the one that matches the
measurement: nine repositories lack clause 6, three surfaces lack clause 5, and `apply-scout`'s card metadata
— the item the title is about — was supplied by S3. So S6 rolled out **the back-link on ten surfaces**, plus
card metadata only where a surface had none of it.

| | |
|---|---|
| **Back-link, all ten** | `ab-lab` `f8e8bb0`, `auth-log-scan` `a783180`, `car-price-ml` `30c6a04` (both surfaces), `it-job-radar` `e21a3ad`, `mini-traceroute` `dbf04a5`, `mlops-car-price` `5d2b072`, `pl-jobs-lora` `e0ed459`, `pl-review-sense` `5039299`, `wroclaw-air-insights` `d8d41b6`. Two follow-ups from the review then landed on top: `auth-log-scan` `4f16990` and `wroclaw-air-insights` `88c580f` — §4.4 |
| **Card metadata** | `car-price-ml/docs/app` gains all seven; `wroclaw` gains the one it lacked, `og:description` |
| **Deliberately left** | `mlops-car-price` and `pl-jobs-lora` keep no card metadata. Both are **S4** targets and S4 rewrites those pages — tokens, eyebrow, `h1`, `<title>`. Seven `og:*` tags written now are seven rewritten then |

**Where the edit goes is not the same question as which page is wrong.** Six of the nine pages are
generated and three are hand-written. Of the six, **five are byte-diffed by their own CI** — `ab-lab`,
`auth-log-scan`, `it-job-radar`, `pl-review-sense`, `car-price-ml` — so the back-link went into a template,
a theme module or a generator; the sixth is `wroclaw`, which is generated and byte-diffed by nothing,
because it commits no HTML at all. `car-price-ml` is both kinds at once, and its second surface is the only
HTML there that CI does *not* diff. *A first draft wrote "five … three", which reads as a partition of nine
and covers eight.* Each generated page was rebuilt with its own command, its hash checked before
and after, and the diff read before publishing — `ab-lab`'s first rebuild ran without the package importable
and **silently changed nothing**, which is the trap §3 of this ledger already records.

**And the literals clause earned its keep on its first stage.** `car-price-ml`'s valuation form painted its
submit button `color: #ffffff` on `background: var(--accent)`. White in both schemes, so in dark it put 16px
600-weight text on `#6ea8fe` at **2.42:1** against Level AA's 4.5:1 — on the only control that page has.
`var(--bg)` follows the scheme: **5.17:1 light, 7.71:1 dark**. It was reported as one hex outside the token
block, on the surface CI does not byte-diff, and *nothing in this portfolio could see it before S3*.

**One figure this stage refuted, and it has the cause §3.7 already named.** `0007` §9 row 4 scopes card
metadata to *"Nine and **three** repositories"*. Three is what §3's card-meta column says, because that
column is a page-level yes/no — and **§5 clause 5, in the same document, refutes it**: *"`wroclaw`'s `yes` is
the one that is not whole … missing `og:description`."* The real scope is **four surfaces**. §9 is superseded
and its rows are not restated here, but the *cause* is worth carrying, because this is its second instance:
**§3.7 recorded the checker being composed from §3's frozen columns rather than from §5's sentences, and this
is the same substitution made by a person rather than by a program.** A column that answers *whether* a page
has something cannot answer *what it is missing*, and every scope derived from one inherits that.

**`wroclaw` is the one whose result this branch cannot confirm.** It commits no HTML; the page is built by
the daily refresh, and `reports/site/` is a gitignored local build that has produced a wrong answer
surviving a session. Its three new assertions run on every push there, which is why they were added rather
than left to the index checker — §6's first row still applies, and confirming the live page means
dispatching `refresh.yml` and reading the URL.

### 4.4 The S6 review, and the fifth appearance of one class

The review confirmed every claim in the nine commits — the nine/ten scope, the six-generated /
three-hand-written split verified by running each repository's own build command, the three contrast
ratios, the four live URLs, the two test counts — and found nothing wrong with the code in any
repository. What it found was in the record and in one guard.

**The guard is the one worth carrying.** `wroclaw`'s new card-metadata check decided *"whether a cached
description quotes a number this run produced"*, and compared against `f"{value:g}"` alone — while every
metric on that page renders through `formatting.fmt`. The MAE reads `3.00`, not `3`. **So the single
likeliest way a figure reaches that description — somebody lifting the page's own sentence — was the one
shape that passed.** Fixing it exposed a second miss in the same line: the right-hand bound `(?![\d.])`
rejects a continuing number *and* the full stop ending a sentence, so `its error of 3.00.` still slipped
through. It is `(?!\d)(?!\.\d)` now, proved on four shapes plus a control — a value the run did **not**
measure, because a guard reddening on any decimal would pass the other four and mean nothing.

*That is a claim wider than its code, and it is the fifth appearance of that class across S3 and S6.* The
four before it were guards on n−1 shapes of n; this one is a guard on one rendering of two. **The
instrument that finds it is the same every time — enumerate what the thing can actually receive, and check
the guard against all of it — and the instrument that misses it is the same too: proving it on the shape
the author had in mind.**

Two smaller items landed with it. `auth-log-scan`'s back-link was a literal in a template where every
other URL is substituted from a constant — one string in one place, but the wrong place for that
repository's pattern; the published page is byte-identical, which is how that is known to be a move rather
than a change. And `_PROFILE_URL`'s comment in `wroclaw` claimed it was named *"for the same reason
`_REPO_URL` is"*, whose stated reason is drift between two use sites; `_PROFILE_URL` has one. A stated
reason that does not hold is the defect this record names, and it was written into the fix for it.

One item is **carried, not fixed**: `car-price-ml`'s new `description` writes `1 200 trees` with a plain
space. Clause 8 scores rendered text, so meta content is outside every carrier there is — the checker reads
`space 1` on that surface while the file holds two grouped figures. No *new* violation is introduced — but that surface already
fails clause 8 today (`FAIL 8 separator space 1`) on the body occurrence at `docs/app/index.html:27`, and
both separators are the same U+0020. The point stands and is sharper for it: the checker reads `space 1`
where the file holds **two** grouped figures, so a later separator migration must find the second one with
nothing pointing at it. S7 and S8 should know meta content is a blind spot rather than discover it.

> **Erratum — §4.11.** The migration is **S9**, not S7 or S8, and this paragraph's warning was
> *nearly* wasted: §4.11's first census listed only `docs/app/index.html:27` and missed `:7`
> — `the same 1 200 trees` — which is the exact second figure named here. **The blind spot was
> rediscovered by falling into it**, one section after it was written down, and the review caught
> it rather than the pointer. §4.11's table now carries `:7`.

### 4.5 The page did self-update; what did not was the code that renders it

S6 closed with the live `wroclaw` page contradicting the merged tree, and the question worth answering was
not *"did the deploy fail"* but *"what exactly is automatic here"*. Measured:

- **The data refresh works.** The last **22** scheduled runs — 2026-08-16 to 09-06 — are every one
  `success`, rebuilding and republishing the page daily. Over the full record there are **51** scheduled
  runs since 2026-07-18 and **four** failures, all of them in July. Nothing was broken in September.
- **The stale page was five hours of ordinary timing.** The day's run started 09:16Z from `98b3051`; the S6
  commits merged at 14:31Z and 14:46Z. The page was one run behind, not wrong.
- **But `refresh.yml` was the only workflow that deploys Pages, and it had no push trigger.** `ci.yml` runs
  on every push and only tests. So a change to the *rendering code* had no publish path of its own and
  waited for the next data run — up to a day, and here rather more than that. Fixed: it now also triggers
  on a push touching `src/**` or the workflow. The merge that added the trigger was published **by the
  trigger it added**.
- **And the schedule itself is not the schedule.** Measured over all 51 scheduled runs, as minutes after
  the 05:00Z the cron asks for:

  | period | runs | delay |
  |---|---|---|
  | 2026-07-18 → 08-06 | 20 | 123–218 min |
  | 2026-08-07 → 08-14 | 8 | 47–81 min |
  | 2026-08-15 → 08-26 | 12 | **31–43 min** |
  | 2026-08-27 → 09-06 | 11 | 235–737 min |

  **The delay has never been under half an hour**, and it has swung by a factor of twenty across four bands
  rather than stepping once. *A cron expression is a request, and this record should not read one as a
  time.*

  *A first draft of this section said the runs kept 05:33–05:43Z "until 2026-08-26" and then stepped once.
  That range is the **twelve days** of 08-15 to 08-26 — the best spell in the record — and I read the most
  recent thirty runs and stated what they showed of the whole. It also called `ab-lab`'s Monday cron
  corroboration; that workflow has **two** scheduled runs in its entire history, which is a coincidence
  worth noting and not evidence of anything. The conclusion survives and is stronger on 51 runs than on the
  window that happened to be in front of me — but the evidence under it was the shape `0007` §8.4 names:
  an observation true of one window, stated of the class.*

*The general lesson is §3.5's, one layer out: the instrument said the page was wrong, and the instrument was
right — but the reason it gave (`FAIL`) and the reason it had (one run behind) are different sentences, and
only the second one leads to a fix.*

### 4.6 S7's scope, re-derived — the row named four items and the stage touched nine repositories

§3's own rule is that a stage finding its scope has moved re-derives it and says so here, and S6 set the
precedent in §4.3. S7's row names `.tile`/`.stat`, `.scroll`/`.ledger-wrap`/`.tablewrap`, `--ink`/`--line`
and `wroclaw`'s two absent tokens. What the repositories held at entry was more, and less, than that.

| | |
|---|---|
| **Named and done** | `ab-lab` `.tile`+`.scroll` `fa58484`; `wroclaw` `.stat`+`--ink`/`--line`+`--radius`/`--positive` `c06d5fa`; `mini-traceroute` `.ledger-wrap` `7458aaf`; `mlops-car-price` `47f7cc0` and `pl-jobs-lora` `0b1c21e` `.tablewrap` |
| **Named by `0007` §9 row 6, dropped by the S7 row** | `wroclaw`'s third `--accent-soft`, and `mini-traceroute`'s unwrapped `<figure>` table — the stage's one real clause-3 failure |
| **Carried into S7 by §3.2** | `auth-log-scan` could not take the pinned `--accent-soft` without a usage-site change, and `.ev-accepted` was a live SC 1.4.11 failure. `83a22b5` |
| **Not named anywhere, and taken on §9 row 5's reasoning** | the pinned values on `ab-lab` (dark), `doc-extract` `2a1be1d`, `it-job-radar` `c740900`, `pl-review-sense` `6ac7d66`. Row 5 set these aside as *"conformance, not harm"* and moved them to row 6, which is this stage; the S7 row simply did not carry that forward |

**The one that was bigger than recorded.** §3.2 left `auth-log-scan` with one known failure. Sweeping every
mark against every band found **four**: `ev-accepted` on the window band at 2.81:1, and all three of the
other marks on the *flagged* band — a second band §3.2 never measured, because its reasoning was about
`--accent-soft` and that band paints `--danger`. Solved by measurement rather than choice: 0.25 and 0.15 are
the highest 0.05 steps at which every mark clears 3:1 with the pinned tokens. All sixteen pairs pass now.

**And the rename made a clause able to answer.** `wroclaw`'s palette had no `--border`, so `1 usage roles`
reported `undecided` — the treatment S3 built precisely so a planned stage's starting state is not called a
defect before the stage runs. The moment `--line` became `--border`, the clause could decide, and the first
thing it decided was a real question: `nav.toc a:hover` paints `border-color: var(--accent)`. That is an
interaction state, not a wrong role; `0007` §5 clause 1 now says so, and `:focus` turned out to have been
one instance of a shape rather than the shape.

*Four review passes ran over this stage. Three blocked, and between them they found nine figures or guards
that were right about the case in front of their author and silent about the rest of the set — including
one where the fix for the eighth introduced the ninth, defeating a guard that had worked before it. The
count is in §3.9, §3.10 and here; the instrument that finds them has not changed once.*

### 4.7 S4's scope, re-derived before the stage rather than during it

The row grew twice on premises that measurement removes, and grew once on something nobody had counted.

| the row said | the repositories say |
|---|---|
| *"plus one generator or table that does not exist yet"* (§4.2) | **it exists**, generated and tested, and the page has quoted it since 2026-08-21. Not work. `0007` §5.1 struck |
| §5.1: clause 2 does not bind on either page | **it binds on both.** Eight tiles are sourceable from committed cells today |
| *"2 hand-written pages, 14 card tags"* | plus **12 literal migrations**, plus **8 tiles**, plus **every rounded figure re-quoted** |
| implied: the index checker carries the result | it carries neither the quotation rule nor clause 2's binding. Two new page tests, `ADR-0004` §4 amended |
| 2–3 days | **~2 days** |

**Both pages already fail the constraint they are being brought under**, which is the finding that shapes the
stage. `mlops-car-price` prints `728k`, `119k`, `148k` where its artifacts print `727,554`, `118,993`,
`148,049`, and writes `−0.9%` with U+2212 where the artifact writes a hyphen. `pl-jobs-lora` prints `2.3`,
`2.5`, `21.4` where its report prints `2.25`, `2.47`, `21.43`. Under §5.0 the separators and the minus are the
page's typography and are fine; **the rounding is not**, so those six figures either come from a regenerated
artifact or leave the page.

**And the S3 defect is loaded on both pages, identically.** `#eef1f6` serves two roles on each:
`th, td { border-bottom }` — which is `--border` — and `code { background }` — which is `--surface`. A
migration done by value maps both to one token and ships a page every carrier reports clean; the checker's
`1 usage roles` catches the border half and **nothing catches the `code` half**, because a ground role in a
ground property is conforming whichever ground it names. Read the two rules against each other before writing,
and pin the mapping in each repository's own test with the mutation run.

**The claims, settled with the user before any page is touched.** `mlops-car-price` opens on *the most
accurate model is the one this system refuses to deploy* — 8,908 PLN at 338.5 MB against 9,278 PLN at 3.3 MB,
against a declared 50 MB budget; a claim about the layer rather than the model, which is the only thing that
distinguishes it from `car-price-ml` in a recruiter's thirty seconds, and it discharges clause 9 by
construction. `pl-jobs-lora` opens on *94% of what the input makes recoverable* — a sentence its own artifact
prints verbatim at `results/eval/report.md:36`, model-free, and finished rather than pending, so S5 makes it
context instead of making it false.

### 4.8 What closing S4 measured — including a scope figure neither page produces

Both pages read `clear`. `mlops-car-price` reported seven clause failures at entry and `pl-jobs-lora` six; the
single `undecided` left on each is clause 4's `h1`, which the checker declines to judge rather than fails.
**Three of the eleven committed surfaces are now clear** — `apply-scout`, and these two. Live bytes were
compared against the git blob, not against the working tree: both identical, so this is a statement about the
published page and not about a local checkout (§6's third assumption, discharged for the two surfaces
this stage touched). 116 tests on `mlops-car-price`, 231 on `pl-jobs-lora`.

**§4.7's "12 literal migrations" is a figure no page produces.** It is the same failure §2.1 records three of
at entry — a count written into a plan and then carried, never read back off a repository. Read from the two
stylesheets at entry: **22 declaration sites**, 7 on `mlops-car-price` and 15 on `pl-jobs-lora`, carrying 11
distinct values between them and 16 counted per page. And **two of the 22 were deleted rather than migrated**:
`#fffaf0` and `#fffbfa`, the tints on `pl-jobs-lora`'s `.status` and `.correction` cards, which no house role
names and which the rail replaces. So the row is 22 sites, 20 migrations, 2 deletions. The two-role trap was
on each page as §4.7 said it would be, and it was `#eef1f6` on both.

**What the rule caught once it was executable, and what it does not catch.** Running each new test's quotation
check against the page as it stood at entry rejects **four figures on `mlops-car-price`** — `728`, `119`,
`148` where the reports print `727,554`, `118,993`, `148,049`, and `338` where the page's own next sentence
wrote `338.5` — and **six on `pl-jobs-lora`**: `2.3`, `21.4`, `67.9`, `4.9`, `568` and `11`. Ten figures
that had been published, none of them a quotation of anything.

Two more were also wrong and the guard is **silent** on them: `36 %` and `23 %` on `pl-jobs-lora`, found by
reading the report rather than by running the check. `results/eval/report.md` writes `36` and `ADR-0001`
writes `n=23`, both for unrelated reasons, and a bare two-digit integer is very likely to be a whole token
somewhere in four artifacts two of which are prose. The guard is strong for a decimal and for three digits or
more, weak for a two-digit integer; **the limit is written into the test**, because a guard whose boundary is
not recorded gets read as covering everything. Versioning `results/probe/` would take the first ADR off the
artifact set and tighten it.

**The tokeniser welded two cells and the defect was mine.** Admitting the ordinary space into the number class
— it is a legitimate group separator under clause 8 — joins adjacent table cells into one token:
`0.05 0.04` reads as `0.050.04` and matches nothing, so a whole table silently stops being checked. Caught on
`pl-jobs-lora`, latent on `mlops-car-price`, and it is the same welding §8.5 of `0007` already records
against every earlier separator tally in this portfolio.

**One exemption is about a figure rather than about a not-a-figure.** `pl-jobs-lora`'s correction section
quotes what the page *used to* publish, and no generator prints a number that was withdrawn. The shape is
`<s class="withdrawn">`, struck in the markup so a reader sees it is not a claim, and exempt in the test —
because the alternative forbids the one section on that page whose whole subject is a figure that should not
have been published.

### 4.9 The S4 review, and the sixth and seventh appearance of one class

The review blocked: **four HIGH, six MEDIUM, two LOW, every one proved by a mutation that shipped green**
rather than by reading. Two of the four are the class §3.9 and §3.10 record — *a guard that is green under
the very mutation its own docstring names* — and both were in the tests S4 had just written to close it.

| the guard's own sentence | what passed it |
|---|---|
| *"asserted per tile against the cell, not in aggregate"* | four tiles printing one number, and a tile printing its neighbour's cell. It compared each tile against every figure in the file, one tile at a time — which is the aggregate comparison |
| *"nothing catches the `code` half"* | a later `@media (prefers-color-scheme: dark) { code { … } }`. CSS resolves by the **last** declaration and `re.search` returns the **first**, and the page test and `pagespec` were both clean |
| *"a dead exemption is worse than none"* | every exemption on both pages, always. It searched the raw HTML, where an exempted shape is still present long after the pass that consumed it |
| — | every figure in `og:description`. Attribute content is stripped along with its tag, so the social card was outside the provenance rule entirely |

**Asking the liveness question correctly killed an exemption on sight.** `mlops-car-price` carried a `years`
shape that consumed nothing a reader sees — the page's only year is inside the build date, which the shape
above it already removes — while accepting a four-digit corruption of any cell: `15 422` retyped as `2019`
passed. It was pure widening, and it is gone.

**Two things in the review did not survive being checked, and checking them was the point.**

* Its proposed fix for the liveness guard — *"count hits per pattern inside `_rendered_text()` and assert each
  `> 0`"* — is wrong, and measurably so: run against the finished text, **every** exemption reads dead, because
  removing them is what that function does. The question only has an answer at the point each pattern is
  applied, so the pipeline now tallies as it strips.
* Its census, *"7 of 22 printed figures have an accepted corruption"*, did not reproduce. Substituting one
  digit at a time gives **10 of 22** on `mlops-car-price` and **56 of 59** on `pl-jobs-lora`; the review's own
  cited example, `12.9 ms` retyped as `13.0 ms`, is a two-digit corruption its family excluded. Both censuses
  are now in the test files **with the corruption family stated**, because a census whose definition is
  unstated is a number nobody can reproduce — which is how it came to be quoted at a figure it never measured.

**16 mutations across the two repositories, all red.** The first `pl-jobs-lora` run was thrown away: the
mutation harness restores each file with `git checkout --`, and an uncommitted caption edit went with it, so
two verdicts were measured against a test that was already red for an unrelated reason. Re-run against a
committed tree. That is the second time in one day that a restore-from-HEAD took work nobody had looked at,
and the rule it earns is narrow: **commit before the harness runs, not before the harness finishes.**

### 4.10 The documentation round — and the surface the rule was never applied to

Three reviews, split by **question** rather than by file, because 102 documents read for "anything wrong"
gets read thinly: are the twelve `CLAUDE.md` correct as instructions someone follows *before* reading the
code; do the thirteen READMEs state things their own repositories contradict; is this record internally
consistent and still true of the trees. All three blocked.

**The finding that matters most is structural.** S4 spent a stage establishing that a published surface
quotes and never retypes, and applied it to `docs/index.html`. **Nobody applied it to `README.md`** — which
GitHub renders first and the page is a click away from. Ten of the twelve READMEs carried at least one
figure no artifact prints, including in `apply-scout`, which §4.8 records as `clear`: that repository's
`tests/test_docs_page.py` pins `48978+10983 | cost: $0.4368` so the *page* cannot round it, and the README
beside it printed `49.0k+11.0k` and `$0.44`. "Three of eleven surfaces are clear" was a statement about one
file per repository.

The sharpest single figure was not a rounding at all. `pl-jobs-lora/README.md` opened its motivation
sentence with *"0.23 field F1 few-shot"* where the report and the README's own table forty lines above both
print `0.30`. It reconstructs exactly as the **pre-redefinition** four-field mean — `(0.25 + 0.12 + 0.54 +
0.01) / 4` — from before `field F1` was redefined to drop `tech_optional`. That is §4.8's own named blind
spot, *a figure moved to the wrong place*, and it survived because `0.23` does appear in the artifacts, as a
different metric on a different row.

**What the reviews corrected in this record, rather than in the repositories.**

| what it said | what the trees say |
|---|---|
| §4.8: the ten figures S4 removed are still in the READMEs | **eight.** `67.90` quoted as `67.9` is legal — §5.0 names a trailing zero as the page's typography — and `568` is printed by `configs/config.yaml` and `ADR-0006`, which the page's own artifact set excludes |
| §4.8: *"Three more were also wrong"* | **two** are named on the line. Written in the paragraph arguing that an unstated census is a number nobody can reproduce |
| §4.7: *"those seven figures"* | **six** are enumerated |
| The S4 row: *"closed … the review's four HIGH fixed in #21 and #14"* | both were **open** when that was written. It read as merged, which §1 forbids in as many words. Now merged, and the row says what the first version got wrong |
| §3.8 and §3.9: **four** repositories cannot see the rule | **one.** `ADR-0004` was amended twice the same day and this ledger contradicted it two sections apart |
| §3.7 and `clauses.py`: `apply-scout`'s **298** tests | **300**, at the S3 closing commit and today. 298 is no revision of that repository — and it sat inside the paragraph blocking S3 for over-claiming |

**And one rule was stricter than the spec it cites.** `0007` §5.0 names *the separator, the minus sign and
the presence or absence of a trailing zero* as the page's typography; the page tests compared digit strings,
so `67.90` and `67.9` read as different figures. The sentence is now implemented in `_canonical()` and
pinned by a test, in both repositories. A guard that disagrees with its own normative source is worse than a
missing one, because it produces confident false findings — this one produced two.

**The census is dated rather than re-derived**, in `0007` §5 clause 1 and in `clauses.py`. It was measured at
S3 close; S4 added conforming sites to two pages and two rails to `pl-jobs-lora`, so it is stale. Three
attempts at a replacement — the review's, and two of mine over different populations — produced three
different numbers, which is the argument for not typing a fourth. `ef3d8c0` already moved one table in that
document from typed to computed; the report prints a role census on every run, and clause 8's `61 of 85`
went the same way for the same reason.

**The `CLAUDE.md` round found one instruction actively pointing the wrong way** in nine of twelve files: a
block telling the reader to prefer an MCP server *over* Grep and to fall back only when the graph does not
cover the question. That server is declared in each submodule's own `.mcp.json`, so it is simply absent
whenever a session starts in this index one directory up — as every session of this block has. Neither index
has a hook, and both were weeks behind the trees they describe. `car-price-ml`'s version was the one that
said all of this already; the other nine were rewritten to match it. The page contract itself — the thing
eleven of these repositories are held to — appeared in none of the twelve, and now appears in ten, naming
each repository's own local carrier or, for `mini-traceroute`, the absence of one.

### 4.11 The two clauses no stage owned, and the instrument that cannot fail

Measured at entry 2026-09-07: no open pull request in any of the thirteen repositories, all twelve pointers
equal *and* on `main`, working tree clean apart from untracked `.claude/`. Index `main` at `2d1cf41`.

**Three of twelve surfaces read `clear`, and the nine that do not fail exactly two clauses between them.**
Tallied over every verdict the checker emits, with `--fetch`:

| clause | FAIL | ok | n/a or undecided |
|---|---|---|---|
| **8 separator** | **7** | **1** | 4 print no grouped figure |
| **4 title** | **3** | 9 | measured **against the current guard**, not against the clause — the repair below takes `wroclaw` from `ok` to `FAIL` and makes it 4 / 8 |
| 1 (tokens, dark, light, literals, usage) | 0 | 12 each | — |
| 1 composited | 0 | 5 | **7 undecided** — the second-largest undecided population in the portfolio, and §3.2 and §3.5 argue hardest for keeping it that way |
| 2 tiles · 3 tables · 4 eyebrow · 5 card meta · 6 back-link · 7 webfont | **0** | 11 · 10 · 12 · 12 · 12 · 12 | 1 · 2 |

**Every `FAIL` in this portfolio is one of two clauses.** Nothing else fails anywhere, on any surface. And
clause 8's single `ok` is `mlops-car-price` — the page S4 rewrote — so **one published surface prints a
grouped figure and prints it correctly**, against seven that print one wrongly.

#### Why no stage owns them

`0007` §9's rollout is scoped **by repository row**, and this ledger inherited that scoping without
re-deriving it. Clauses 8 and 4-title cut *across* rows: they are properties of every page, not of the three
or four a row names. So they were only ever repaired **incidentally**, on the pages a stage happened to
rewrite for another reason — which is exactly the three surfaces that read `clear` today.

**This is §3.7's finding one layer out.** §3.7 records the checker being *"composed from the frozen table's
columns rather than from the normative clauses' sentences."* Here the same substitution was made by the
**plan** rather than by the program: the stages were composed from §9's rows rather than from §5's clauses,
and two clauses have no row. §3.7 said this *"is a thing to check for the whole of S6 and S7, not a one-off"*
— it was checked for the checker and not for the ledger that sentence is written in.

The sharper instance is already in this file. §3.4 assigned `mini-traceroute`'s repo-name `<title>` to
*"S7 and S8"*. **S7 closed without it and S8's scope list does not contain it** — an item routed to two
stages, one of which has closed, and neither of which was ever going to carry it.

#### The mechanism, which is not the scoping

`tools/pagespec/__main__.py` ends `return 0`, unconditionally, on any finding. `.github/workflows/pagespec.yml`
runs it with the comment *"Read from the log rather than gated on, until `0008` schedules the gate."*
**This ledger scheduled no gate before this section** — not in S0–S8, not in Sx, not in §5's carried list.
Two published artifacts, one of them a workflow, pointed at a stage that did not exist; a third is the
checker's own module docstring, which says *"`0008` S2 schedules the gate after the rollout"* — and S2 is the
stage that built the checker and is **closed**. §3's table now holds S-gate, so this paragraph is the
diagnosis of the state this commit ends rather than a claim about the document it now lives in. *Written in
the present tense first, inside the section whose next sentence calls that this record's signature defect.* *That is this record's signature
defect committed in the file whose §1 exists to prevent it.*

Then, per repository: **no submodule test asserts which separator a page writes** — swept over all twelve.
**Refuted 2026-09-07; two do, and both assert a comma — §4.13.** The sentence is left standing because the
conclusion it supports survives and the correction changes a *stage's* cost rather than this section's
argument. And the two that name `U+202F` are the two that most deliberately cannot see it. `mlops-car-price/tests/test_docs_page.py:41`
and its twin in `pl-jobs-lora` build

```python
_SEP_CHARS  = "    "
_SEPARATORS = str.maketrans(dict.fromkeys("," + _SEP_CHARS, ""))
```

— a table that **deletes** every separator, U+202F included, before comparing, because `0007` §5.0 makes the
separator the page's typography rather than part of a quotation. `car-price-ml/tests/test_site.py:184` strips
both space characters for the same reason, and `doc-extract/tests/test_ground.py:359` normalises U+00A0 and
U+0020 to one value before asserting.

*So the tests written closest to clause 8 are blind to it **correctly**, and the blindness is not an oversight
any of them should fix: a per-repository test cannot both honour §5.0's quotation rule and enforce clause 8's
glyph, because §5.0 exists to say the glyph is not part of the claim. **Clause 8 can only ever be carried by
the index checker** — which is the gate argument arriving from the opposite direction, and it is stronger than
the one this section opened with.* So clause 8 and clause 4-title are carried by an instrument that **cannot return non-zero**,
and by nothing else.

**The counterfactual is in the trees rather than in the argument.** Every clause-8-failing repository was
edited by S6, S7 or both: S6 put a back-link into `ab-lab`, `car-price-ml` (both surfaces), `it-job-radar`,
`pl-review-sense` and `wroclaw` (`d8d41b6`); S7 rewrote palettes on `doc-extract`, `it-job-radar`,
`pl-review-sense` and `wroclaw` (`c06d5fa`). **Two stages** rebuilt those pages — and of the seven failing
surfaces, **five carry a rebuild-and-compare guard** that ran on every one of those merges: `ab-lab`
(`tests/test_site_committed.py:61`), `it-job-radar` (`tests/test_site.py:258`, byte-exact), `car-price-ml`
and `pl-review-sense` (CI `diff`), and `doc-extract` — whose comparison is **normalised rather than
byte-exact**, and still would have caught a separator. `wroclaw` and `car-price-ml/app` are guarded by
nothing (§4.3). **Not one separator moved.**

*So this is not a story about weak guards.* Five instruments compared a regenerated page against its
committed bytes, twice each, and every one of them passed — because a guard that asks *"does the page still
match its inputs"* cannot ask *"are the inputs right"*. That is the whole argument for the index gate, and
it is also why the gate does not make those five redundant. Repairing seven surfaces
while leaving the gate unbuilt reproduces that condition exactly.

#### What clause 8's subject actually is

Not seven pages. **Eighteen non-conforming write sites, in thirteen files, across five repositories and six
surfaces** — counted by file and line, because `regime_section.py:25` and `:46` are two edits and the stage is
scoped by formatter rather than by page.

> **Corrected 2026-09-07, and the number is deliberately not re-typed here — §4.13.** The table below lists
> **nineteen**, not eighteen; the trees hold **twenty**. Both figures in the sentence above are wrong, in the
> way the italics two paragraphs down already describe about *fifteen*. **A fourth hand-count would be a
> fourth number**, so the census moves into the checker's output rather than being patched again, and §4.13
> says what it must print.

*A first version of this sentence said **fifteen** sites across **six repositories**, and both are wrong in
the way this section is about. Fifteen was taken from a design pass and never counted back off the table
printed directly beneath it — §2.1's and §4.8's defect, committed in the paragraph naming it. Six counted
`car-price-ml/app` as a repository, which is a **surface** of `car-price-ml` — and §4 of this same file rules
that exact substitution a category error, in the row that dissolves B3. Caught by review.*

| repository | site | writes |
|---|---|---|
| `ab-lab` | `sitegen/numbers.py:46` `integer()` · `sitegen/page.py:219` literal · **`examples/validation_table.py:130`** — added 2026-09-07, §4.13 | comma · space · **comma** |
| `car-price-ml` | `site/charts.py:76` | **U+202F** ✓ |
| `car-price-ml` | `site/build.py:76` `_thousands` · `site/export.py:179` `_pln` · `templates/index.html.j2:83, 114, 160` | space |
| `car-price-ml/app` | `docs/app/index.html:27` literal · **`:7` `<meta name="description">` literal** | space |
| `it-job-radar` | `site/charts.py:93` · `site/build.py:355, 386` | space |
| `pl-review-sense` | `site/charts.py:89` · `site/build.py:290` | space |
| `wroclaw` | `accuracy_section.py:25` · `regime_section.py:25, 46` · `report.py:248, 307` | comma |
| `doc-extract` | `docs/build_index.py:1590` | **U+202F** ✓ |

*Two conforming **write sites**. Counting conforming **figures** instead gives more — `mlops-car-price`'s
hand-written page holds eight U+202F literals, which is the `ok 8 separator U+202F 8` in the table above and
the reason that page is the portfolio's one correct grouped-figure surface. Both quantities are real and the
table counts sites, because a site is what S9 edits.*

**`car-price-ml` holds two byte-identical copies of one function and a third implementation that drifted
with them:**

```
charts.py:76    return f"{value:,.0f}".replace(",", " ")            ->  U+202F
build.py:76     return f"{value:,.0f}".replace(",", " ")            ->  U+0020
export.py:179   return f"{value:,.0f}".replace(",", " ") + " PLN"   ->  U+0020
```

`charts.py:76` and `build.py:76` are `_thousands` and are byte-identical **apart from one invisible
codepoint**: a reader comparing them in a terminal, a diff or a `grep` sees the same line twice.
`export.py:179` is `_pln`, a different function — and it is the stronger evidence rather than the weaker,
because its own docstring asserts the convention the repository does not keep: *"Thousands separated by a
space, as everywhere else on the page and in Polish usage."* **Everywhere else on the page is U+202F.**

*A first version of this block trimmed `+ " PLN"` so all three lines would read identically, and called them
three copies of one function. The trees refute it, and the trimmed quote made a true point with a doctored
exhibit — which is worse than the untrimmed one, because the untrimmed one carries the docstring.* So `0007` §5 clause 8's *"`car-price-ml` is mid-migration in public — 16 figures with a plain
space against 12 with `U+202F`"* is accurate as a page count and **wrong about what it is**: it is not a
migration, it is one repository's helper duplicated three times and drifted. The page count is a symptom, and
scoping the repair by page would have repaired the symptom.

*The general form, and it is the reason this belongs in the ledger rather than in a stage: **a clause whose
subject is a formatter cannot be scoped by the pages that print it.** §3.2 earned the sibling lesson for
contrast — read the threshold per usage site — and this is the same shape for provenance.*

#### Three things a page-scoped repair would have got wrong

- **`doc-extract` is a false positive, and "fixing" it publishes a false statement.** Its one clause-8 hit is
  `docs/index.html:438`, `<code>3&nbsp;466,62</code>`, inside the sentence *"reads as `3 466,62` in a flat text
  dump, **because a space is also Poland's thousands separator**."* The subject of the sentence is the glyph,
  and `synth/render.py:531` really does print an ordinary space into the corpus. Migrating the specimen would
  make the page claim something its own generator does not do. **This needs a spec amendment, not an edit** —
  S9c — written in §5's own method, as a description with its census: swept over the eleven committed
  surfaces, **exactly one site** qualifies as a displayed specimen, and every other grouped figure sits in
  `<p>`, `<td>` or SVG `<text>`. State the census in the clause and print it from the checker, so the
  exemption cannot silently widen — §3.9's own instrument.
- ***Closed 2026-09-07 by `#86`, and the citation below is to code that no longer exists.*** The comparison is `_leads_with_the_projects_identity` now: positional, over the project's identity in both its directory spelling and its prose spelling. Left standing rather than rewritten because the diagnosis is what the stage was built from.
- **Clause 4's guard is weaker than clause 4.** `clauses.py:568` is
  `page.title.strip().lower().startswith(repo.lower())`. `wroclaw`'s title *"Wrocław Air Insights"* **is** the
  repository's name in prose and **passes**, because `ł` and the space-for-hyphen defeat the comparison.
  §3.5 records this cell as *"the checker being more precise than the table"*; measured against the **clause**
  it is the opposite. Sixth appearance of §3.9's class — a guard proved on the shape its author had in mind.
  **And the repair changes the stage's scope rather than only the checker's honesty**: normalised, `wroclaw`'s
  title reduces to exactly the repository's three tokens, so it moves from `ok` to `FAIL` and **S10 is four
  surfaces, not three**. The other eleven titles were checked and none moves, so the consequence is bounded
  and re-derivable. *A guard too weak to fail is also a guard too weak to scope a stage — which is why this
  was found by review of a scope figure and not by the checker.*
- **A B-code sweep would corrupt a table about something else.** `doc-extract/README.md:507-529` uses
  **B1 / B2 / B3** as the names of its `constant` / `pattern` / `noisy` baselines, and `:211`, `:520` and
  `:523` argue from them. Nine lines that a grep-driven renumber would hit and that have nothing to do with
  the portfolio tiers. Separately, `mlops-car-price/README.md` uses `A3` six times as a live cross-reference.

#### S8's scope, re-derived before the stage rather than during it

§3's rule, and §4.3 and §4.7 set the precedent. The S8 row reads *"4 About + ≥6 READMEs + 5 `CLAUDE.md`"*.
Measured:

| the row said | the trees say |
|---|---|
| ≥6 READMEs | **8** publish a portfolio code: `wroclaw:15` A1, `it-job-radar:14` A2, `car-price-ml:8` A3, `mini-traceroute:13` B1, `auth-log-scan:11` B2, `pl-review-sense:8` B4, `token-budget:6` B5, `pl-jobs-lora:6` P4 |
| 5 `CLAUDE.md` | **all twelve** |

**And the stage was doing two jobs for two audiences.** `0006` §2.3's removal argument is that *a recruiter
cannot decode the codes*. That reaches a published `README.md`; it does **not** reach `CLAUDE.md`, which no
recruiter opens and whose reader is a contributor for whom the code is a useful pointer into `0004`. One
argument cannot decide both surfaces, so the stage splits: **S8a** is the public half and carries L3 with it;
**S8b** is the contributor half and needs its own reason. *A row that names two populations and one estimate
is a scope that has never been taken.*

#### The gate, and the three policy decisions it needs

The deferral's stated reason — *a gate written before any page is green has no reference to gate against* —
was true at S2, when the unit was a whole page. **Per clause it is false today**, and the table at the head of
this section is why: clauses 1, 2, 3, 5, 6 and 7 report **zero `FAIL` across all twelve surfaces**, so they
can be gated now with no page changing at all.

So: a **ratchet**. Gate the clauses that are already clean, and extend the set by one as each stage closes.
Three decisions the implementation must state rather than imply:

1. **Fail on `FAIL` only** — with one exception, found by review and recorded at the end of §4.12. Clause 4's
   `h1` is undecided on every surface today because *"states a claim"* is a judgement no checker can make
   (`0007` §7) — **not undecided *by design*, which is what a first draft of this line said**: it still
   `FAIL`s on a missing `h1` or one equal to the repository's name, and that sentence became load-bearing the
   moment `4 h1` entered `GATED`. Clause 3 answers `undecided` where a media condition is not read, clause 2
   is `n/a` on a page with no tiles, and **clause 1's `composited` is undecided on seven of twelve surfaces**
   — the largest such population, and the one §3.2 and §3.5 argue hardest to keep, because resolving a
   `color-mix` or an `opacity` needs the ground the mark is *drawn over*. A gate that reddens on those would
   be a gate on the checker's honesty.
2. **An unread surface that should have been readable is a failure.** Otherwise a renamed path degrades to a
   green skip — which is the shape of every silent-green defect in §3.7, §3.9 and §4.9.
3. **`--fetch` moves to a scheduled job, not the push job.** The push job gates eleven committed surfaces; a
   daily job gates twelve. That keeps a network failure from reading as a page regression — the reason
   `--fetch` was excluded in the first place, and the comment states it — while ending the state where
   `wroclaw` is gated by nothing at all.

   *S-gate shipped this against the cron already in the file, which is **Monday**, so for one commit the
   policy said daily and the workflow ran weekly — a regression on the one surface that exists nowhere but
   the wire could have stood for six days. Caught by review; the cron is `0 7 * * *` now. The schedule was
   inherited from when this workflow only printed, and inheriting it unread is how a policy and its
   implementation came to disagree inside one change.*

**The mutation that proves it, and the second one is the interesting half.** Revert `charts.py:76` to a comma,
rebuild, run the checker: today it prints `FAIL` and exits 0. Then make the same source edit **without**
rebuilding: the gate stays green and `car-price-ml`'s own byte-diff reddens instead. **The two guards are
complementary rather than redundant** — one sees a page that no longer matches its inputs, the other sees a
page that matches inputs which are themselves wrong — and that is worth recording so a later reader does not
delete one as duplicate coverage.

### 4.12 What S-gate closed, and the two guards that turned out not to be redundant

`current_projects` `297e3c5`, on `main`. **No page changed**, which was the argument for taking it first: the ratchet
starts on the clauses that already report zero `FAIL` on all twelve surfaces, so the gate went from
"impossible" to "green" without a single byte of any page moving.

**The unit is the finding key, not the clause number**, and clause 4 is why. `4 h1` and `4 eyebrow` are clean
everywhere while `4 title` fails on three surfaces; gating by the number would either pull `4 title` in before
S10 or hold the other two out. `GATED` is `("1 ", "2 ", "3 ", "4 eyebrow", "4 h1", "5 ", "6 ", "7 ")`.

**Gating is the default, with `--report-only` to opt out — not a `--gate` flag.** A gate reached only by
remembering a flag is one a later workflow edit drops without anyone noticing, which is the shape §3.7, §3.9,
§4.4 and §4.9 record five times between them. It costs nothing to default: the set is clean today.

#### The fifteen mutations

Every guard was proved red by the mutation its own docstring names, by running each — §3.7's instruction, and
the one §3.6 blocked S3 for asserting without doing.

| # | mutation | what reddened |
|---|---|---|
| 1 | add `"8 "` to `GATED` before S9 lands | the corpus ratchet test — *the guard against widening the ratchet past its measurement* |
| 2 | `return 0` unconditionally again | the gated-clause test, and the empty-root test |
| 3 | let `UNDECIDED` gate too | the ungated-clause test **and** the whole-index green test |
| 4 | never gate on an unread surface | the deleted-surface test |
| 5 | gate on `needs --fetch` too | the `needs --fetch` test |
| 6 | gate every `FAIL`, ignoring `GATED` | the ungated-clause test |
| 7 | ignore `--report-only` | the report-only test |
| 8 | revert `charts.py:76` to a comma, **without rebuilding** | **nothing in the index** — and `car-price-ml`'s own `tests/test_site.py` |
| **9** | `missing = missing or reason == "not found"` — drop the **fetch-failure** branch | **nothing, before the fix — the whole suite stayed green.** `test_a_failed_fetch_is_not_reported_as_a_flag_the_reader_forgot` now |
| **10** | stop gating an unread same-origin stylesheet | the same-origin test |
| **11** | gate a **third-party** sheet too | the third-party test — *the other half, and it has to be asserted separately* |
| **12** | reinstate the prose parse **behind an `if not loaded.unreadable: return []` guard**, which is the shipped bug's actual reach: `detail.removeprefix("unread: ").split(", ")` | **2** — the third-party test and the same-origin test |
| **13** | `raise` on `main`'s first line — the checker never runs | 20 tests, **and the determinism test is the one that counts**: before the fix it was the single test that ran the module as a process, and it *passed* — two empty outputs comparing equal |
| **14** | print the stylesheet gate under the `GATED` header | the same-origin test — *the header is part of the finding, not decoration* |
| **15** | `raise` inside `clauses.check` — the checker dies **after** printing its header | **nothing, before the fourth pass.** The determinism test's `startswith("pagespec")` reaches only a failure *earlier* than the first print, and the header is emitted above the surface loop: both seeds emit the header and nothing else, and the two compare equal. Red now, on the exit code |

*Row 12 was first written as **three** tests, and the number is worth the paragraph it costs.* Three
reconstructions of the same one-line bug give **three different counts**: parsing inside the function that
runs for *every* surface reddens 3, because an empty `unreadable` list yields `[""]` and gates the whole
portfolio — a larger bug than the one that shipped; the same parse behind a non-empty guard, which is the
shipped bug's real reach, reddens 2; and the review's own reconstruction reddened 1. **None of them is wrong;
they are three different mutations wearing one description.** The row now quotes the text it was measured
against, because §4.9 already records what an unstated census costs and this is the same thing one layer
down: *a mutation named in prose is not a mutation, and its count is not reproducible until the code is on
the page.*

*Rows 9, 10, 13 and 15 were not in the first version of this table, and rows 9 and 15 are the ones that
matter. Row 9: `missing` has
**three** reasons and only two were asserted, so the branch behind the `live` job's entire stated purpose
could be deleted with nothing going red. Row 15 is the same lesson about a **guard that exists but stops
short** — the determinism test's compensating assertion could only ever fire before the checker's first
print, so a crash one line later was invisible to it. The sentence above this table — "every guard was proved red by the
mutation its own docstring names" — was true, and silent about the path that had no docstring because it had
no guard, and later silent again about the guard that had a docstring and less reach than it read. **A mutation table proves the guards you wrote, not the branches you have**, which is §3.10's
"a corpus sweep proves the rule against the corpus" applied to a conditional instead of a page.*

**Mutation 6 is the one that proves the ratchet is a ratchet.** Without a test that fails when the gate stops
consulting `GATED`, every other guard here would pass on a gate that simply gates everything — which would go
red on S9's own first commit and on every surface S9 had not reached yet. A gate that cannot be partial is not
a rollout instrument.

**And mutation 8 is the one worth keeping.** Reverting `car-price-ml`'s conforming formatter — one of the
portfolio's **two**, alongside `doc-extract/docs/build_index.py:1590`, as §4.11's own table says — left the index
gate **green** — correctly, because clause 8 is outside `GATED` until S9 and because the page bytes had not
moved — while `car-price-ml`'s own byte-diff went red. Run the other way (rebuild, then check) the index would
see it and the byte-diff would not.

> **The two guards are complementary rather than redundant.** One asks *does the page still match its inputs*;
> the other asks *are the inputs right*. §4.11's counterfactual is exactly the gap between those two questions
> — five rebuild-and-compare guards passed twice each while seven surfaces drifted — and it is recorded here
> so that a later reader tidying up does not delete one as duplicate coverage of the other.

#### Five things the stage found that were not in its scope

*The heading said **three** and the list below it has always had five — written at three, grown by the second
and third passes, and never recounted. Found on the fourth pass, in the section whose subject is exactly
this, two headings below a table corrected for the same thing on the same day.*

- **`ADR-0004` §6 still read *"report-only first"*.** Turning the gate on while the ADR licensing the
  instrument says otherwise is §3.8's finding facing the other way: not a document the repositories refute,
  but **a rule in code that no document states**. Amended in the same commit, and the amendment says what
  expired rather than deleting the bullet — the deferral's reason was *per page*, and it still holds per page;
  the gate simply does not have to be per page.
- **The `core` job's contract nearly took a submodule-dependent test.** The ratchet's corpus check was written
  into `tests/test_report.py`, which is the file the `core` job runs **with no submodule on disk** — the job
  the workflow header calls *"the one that must never be allowed to go red."* Moved to
  `test_published_surfaces.py`. *A test that asserts a claim about the trees cannot live in the file whose
  contract is that there are no trees.*
- **The determinism test could no longer fail for one reason.** `test_the_computed_table_does_not_depend_on_set_iteration_order` shells out with `check=True`, so turning on the gate coupled hash-seed determinism to the exit status: it reddened under four of the mutations above, none of which is about set iteration order, and raised `CalledProcessError` instead of showing the two tables that differ. **I saw it redden during the mutation run and wrote it off as a bystander.** It runs `--report-only` now. *The third bullet of this list states the principle, and I broke it two files away while writing the list.*
- **The ratchet's corpus test would have reddened on the rollout's success.** It guarded vacuity with `assert failing` — so once S9 and S10 close and nothing fails, the guard fails. It also failed rather than skipped in a fresh clone, against this file's own docstring. Vacuity is guarded on what was **read** now. *A guard that goes red when the work it guards finishes is worse than no guard, and it would have arrived as a mystery at exactly the wrong moment.*
- **A guard of mine proved nothing until `--only` was added to it.** The `needs --fetch` test first ran over
  the whole fixture tree, where nine committed surfaces are also absent — so it gated on *those* and would
  have passed whatever the `needs --fetch` branch did. Caught by running it. **A test has to be able to fail
  for one reason**, and this is §4.4's *"enumerate what the thing can actually receive"* met from the other
  side: the guard received more than the shape it was written for.

#### The fourth pass, and a citation the merge strategy cannot preserve

**Both code findings are the shape the third pass is named for**: a fix applied where the defect was found
and not where it also lived, five lines away in one case.

- **The determinism test still passed on a checker that crashed** — mutation 15. The third pass correctly
  identified `check=False` as having removed the last assertion that the subprocess did anything, and added
  `startswith("pagespec")` in its place. That assertion reaches a failure *before* the first print and no
  other, because the header is emitted above the surface loop. It now asserts the exit code as well: under
  `--report-only` `main` returns 0 whatever it finds, so a non-zero code means the process died rather than
  that the gate refused — the coupling `--report-only` exists to break stays broken, and the assertion is
  back at full strength. Not `check=True`, which raises `CalledProcessError` and hides the two tables.
- **`test_the_report_runs_over_the_whole_index_and_the_gate_is_green` ran behind one
  `require_submodule("ab-lab")`** — the exact guard the ratchet test five lines below had been corrected for,
  in the commit whose message spells out why one call is not a guard. Before the gate a missing sibling was a
  `not read:` line and this test passed; **since S-gate an unread committed surface gates**, so on a checkout
  that is *partial* rather than *empty* `main` returns 1 and this file's docstring — *"every test skips when
  its submodule is not checked out"* — is false. Reproduced on a root holding only `ab-lab/docs`: exit 1,
  `gate — a surface that should have been readable was not read`, and nothing in the message about
  submodules. *Turning on a gate changes what every skip-guard in the suite is guarding, and the pass that
  turned it on re-derived that for one test of two.*

**And the status cell cited two commits that cannot be on `main`.** It read `closed — current_projects
043bf72 + 38f26a9`. This repository **squash-merges**: every commit on `main` has a single parent, so no
branch SHA survives. Checked — `89a9cc2` (S0), `ef3d8c0` (S2), `6b7d3b8` (S3) and `d2e96b8` (S4) are all
reachable from `main`; `043bf72`, `38f26a9` and `3163908` are not and never will be. The stage *was* merged,
as `#77` → **`297e3c5`**, with CI green on `main` — so this is not the S4 defect the row above it records, a
row saying closed while the work is unmerged. It is a narrower one underneath: **the row was written in a
citation form this repository's merge strategy discards**, so it named the work correctly and pointed at
nothing. §1's rule is *marked against the default branch in the pass that lands it*; a SHA that will not
exist on that branch cannot discharge it, however true the sentence around it is.

> **Read from a stale `origin/main`, that same cell says the stage was never merged at all.** Both this pass
> and an architecture pass run beside it reached exactly that conclusion, independently, within an hour of
> `#77` merging — because both read `.git/refs/remotes/origin/*`, which is a local file that a session
> inherits and no command refreshes on its own. Three unreachable SHAs and a `gh pr list` returning empty
> read as *"the work is on a branch and nobody opened a pull request."* **The record was right and the
> instrument was stale**, which is the inverse of every other correction in this file and the reason §6's
> last row now says *after a fresh fetch* rather than naming two commands. *A citation form that cannot be
> resolved on `main` and a ref that has not been updated produce the same sentence, and only one of them is
> about the document.*

#### What the gate deliberately does not do

It never gates on a clause's `UNDECIDED` or `n/a`, and the list that protects is longer than it looks: clause
4's `h1` (undecided on all twelve today, because *"states a claim"* is a judgement no checker can make,
`0007` §7 — it still **fails** on a missing `h1` or one naming the repository), clause 3 where a media
condition is unread, clause 2 on a page with no tiles, and **clause 1's `composited` on seven of twelve
surfaces** — the largest such population, kept undecided because resolving a `color-mix()` needs the ground
the mark is drawn over (§3.2). *A gate that reddened on those would be a gate on the checker's own honesty,
and the fix for it would be to make the checker claim verdicts it cannot reach.*

**And there is exactly one `UNDECIDED` that does gate, which the review found and this section had described
as a four-member set that is five.** `sources._with_styles` files a stylesheet it could not open under
`unreadable`, surfacing as an undecided `stylesheets` finding — and every clause reading `loaded.css` then
answers from a stylesheet it knows is incomplete. Measured: renaming a same-origin sheet carrying a webfont
`@import` takes a surface from `FAIL 7 webfont` to **`clear`**, exit 1 to exit 0. That is policy 2's own
argument one level down — a renamed *stylesheet* degrading to a green pass where a renamed *page* is already
refused — so it gates for the same reason. A **third-party** sheet stays exempt: it is unread by design, and
fetching one would put a page's verdict on somebody else's CDN.

*Not live on any surface today — every page is all-inline or all-external, and losing an all-external sheet
trips `1 tokens` instead. It is scheduled work that makes it reachable: S9 edits generators in five
repositories and `car-price-ml/app` is hand-written.*

> **The first fix for it shipped with the defect this record is named after.** It parsed the `stylesheets`
> message with `split(", ")` — and the third-party marker is `" (third party, not read)"`, which **contains
> that separator**, so every exempt sheet split into two fragments and the second one gated. The structured
> list was on `loaded.unreadable` the whole time and reconstructing it from prose was the whole error. It is
> §3.5's welded-token defect — *"`str.split()` destroying the two codepoints clause 8 counts"* — in a third
> place, and it was caught by running all four cases rather than the one the fix was written for.

### 4.13 The errata S9 inherits — four corrections taken before the stage rather than during it

§3's rule, and §4.3, §4.7 and §4.11 set the precedent. **All four were verified against the trees before
being written here**, and three of them change S9's cost. Taken as one round because §4.10 records what
happens otherwise: *the first commit refuted three sections and marked only one.*

#### 1. Two submodule tests do assert a separator, and both assert a comma

§4.11 says, as a sweep over all twelve, *"no submodule test asserts which separator a page writes."* Two do:

| test | assertion |
|---|---|
| `wroclaw-air-insights/tests/test_report.py:377` | `assert "1,280 hours" in html` — on the render of `regime_section`, **the exact module S9a edits at `:25`** |
| `ab-lab/tests/test_record.py:86` | `assert any(f"n = {solved.per_group:,}/arm" in scenario …)` |

**The conclusion survives and the cost does not.** Those two pin the *wrong* separator rather than enforcing
clause 8, so §4.11's *"clause 8 can only ever be carried by the index checker"* still holds — the four tests
it names really are blind to the glyph, correctly, under `0007` §5.0. But the sweep was used to say the
per-repository tests are *uniformly* blind, and two of them are not blind at all: they are pointed the other
way, and they **go red on S9a's own edit**. The false half is the half that costs work.

*A sweep that finds nothing is the hardest kind to audit, because it leaves no exhibit to re-read. This one
was searched for tests that assert `U+202F`; a test that asserts a comma answers a different query, and those
are the ones the stage collides with.*

#### 2. The census is eighteen in prose, nineteen in its own table, twenty in the trees

Counting the table's non-conforming entries: `ab-lab` 2 + `car-price-ml` 5 + `car-price-ml/app` 2 +
`it-job-radar` 3 + `pl-review-sense` 2 + `wroclaw` 5 = **19**. §4.4's erratum added `docs/app/index.html:7`
to the table and the headline was never re-derived — **the same failure the paragraph directly beneath that
headline already records about *fifteen***, committed in the act of correcting it.

**And a twentieth site was missing from the table entirely:** `ab-lab/examples/validation_table.py:130`,

```python
f"Sample size solved for 80% power (n = {design.per_group:,}/arm)",
```

reaching `ab-lab/docs/data/findings.json`, `docs/index.html` and `README.md` verbatim as `n = 14,745/arm`.
It is a *second formatter inside one repository* — the page's other comma figure, `10,000`, is
`numbers.integer()` — and the checker corroborates the split independently: `ab-lab` reports
`FAIL 8 separator comma 2`, two comma figures from two different write sites, where the census named one.

*This is the sharpest of the four, because the repository already documents the site by name.*
`ab-lab/sitegen/numbers.py:1-11` — *"no renderer is allowed a format string of its own"* — cites this exact
figure as the drift that motivated the module, and `ab-lab/docs/decisions/0007-the-page-is-generated.md:19-22`
tabulates `examples/validation_table.py` with its format string as the divergence the whole package argues
against. **The one site the sweep missed is the one site a decision record names.** A census read off
generators and templates does not look in `examples/`, and that repository's own ADR is the artifact that
would have said so.

**The number is not patched here, and the refusal is the finding rather than an omission.** Three hand-counts
have now produced fifteen, eighteen and nineteen. **The census belongs in the checker's output**, the way
clause 1's census and the role census went — printed on every run, reproducible by a reader, and unable to go
stale between a design pass and the stage that spends it. That is `ADR-0004` §5's rule and this file's own
precedent, and it is S9's **first commit** rather than a follow-up: *a stage scoped by a figure no instrument
prints is scoped by whoever counted last.*

#### 3. S9 will blind the provenance guard §4.4 was written to repair — in the act of doing its own work

`wroclaw-air-insights/tests/test_report.py:1524` matches comma grouping and nothing else, and `_numbers_in`
strips `","` alone. Measured:

```
"1,752 hours"  ->  [1752.0]        today
"1 752 hours"  ->  [1.0, 752.0]    after S9a rewrites report.py:307
```

So the card-description provenance guard — the one §4.4 records fixing **twice**, for the `3.00` miss and
then for its numeric bound — **stops seeing grouped figures at all, and passes.** It goes green on exactly
the shape it exists to catch.

**This is the only item in this ledger that cannot be found after the fact.** Every other silent-green in
§3.7, §3.9, §4.4, §4.9 and §4.12 was found by looking at a guard that had already failed to fire, with the
evidence still on disk. This one is *created by scheduled work*: the guard is correct today, the stage is
correct today, and only the composition is wrong. **The pattern widens in the same commit that changes the
separator** — not in a follow-up, because a follow-up is a window in which the page is unguarded and nothing
anywhere says so.

*Swept: `wroclaw` is the only submodule test that parses comma-grouped numbers.
`car-price-ml/tests/test_site.py:184`, the `_SEP_CHARS` tables in `mlops-car-price` and `pl-jobs-lora`, and
`doc-extract/tests/test_ground.py:359` all delete separators before comparing and are unaffected — §4.11 is
right about those four.*

#### 4. S5, S9b and S10 land on three adjacent lines of one file

`car-price-ml/docs/app/index.html` is hand-written and is the one surface CI does not byte-diff (§4.3):

| line | content | stage |
|---|---|---|
| `:6` | `<title>car-price-ml — valuation form</title>` | **S10** |
| `:7` | `<meta name="description" content="… the same 1 200 trees …">` | **S9b** |
| `:27` | `the same 1 200 trees the API serves` | **S9b** |

And S5 regenerates `docs/index.html`, which S9b also regenerates after editing `build.py:76`,
`export.py:179` and the template. §3's table schedules S5, S9 and S10 as independently schedulable; §4.1's
erratum already established the governing rule for this shape — *taking them separately edits the same lines
twice*, here on the one surface with no byte-diff to catch a bad second edit.

**This does not re-scope clause 8 by page.** §4.11 is right that a formatter's clause cannot be found that
way, and the census stays formatter-scoped. What changes is only what one commit carries.

#### What this costs, and the one thing it does not

| stage | before | after |
|---|---|---|
| **S9** | 18 sites · 13 files · *"S9a four repositories, build-only"* · 1.5–2 d | **20 sites · 14 files**, census printed by the checker · S9a is **not build-only in two of the four**: `ab-lab` needs a simulation re-record and a generated README region, `wroclaw` needs its number pattern widened and `test_report.py:377` re-pinned · **2–2.5 d** |
| **S10** | 4 surfaces · 1 guard | unchanged, but its `car-price-ml/app` line rides with S9b |
| **S5** | independently schedulable | folds into the `car-price-ml` pass |
| **Sx** | *"open, schedulable anywhere"* | **the only open item with no dependency on the gate, on a clause, or on another stage** — and both figures reproduced again 2026-09-07 |

**None of it touches the gate.** `GATED` is unchanged, clause 8 is still outside it until S9 closes, and the
ratchet test still holds. *The errata move a stage's cost and not the instrument's contract, which is the
separation `ADR-0004` §5 exists to keep.*

### 4.14 What closing Sx measured — three things the record did not have, and two mistakes in the doing

Taken 2026-09-07. Every figure below comes from a shell or a build, not from a reading of this
file — §3's rule, applied to the stage that discharges §5's carried list.

#### 1. L5 is a deprecation with a date, and the date is not far

§5 calls L5 *"the deprecated `license` table form"* and attaches no urgency. Built against
setuptools 84.0.0:

```
SetuptoolsDeprecationWarning: `project.license` as a TOML table is deprecated
    By 2027-Feb-18, you need to update your project and remove deprecated calls
```

After the change the wheel carries `Metadata-Version: 2.4`, `License-Expression: MIT` and
`License-File: LICENSE`, and the licence is packaged into `dist-info/licenses/` — which the table
form never did. **Every one of the eleven runs an editable install in CI** — seven with the `[dev]` extra,
the others with `[site]`, `[tools]` or none, and three of the eleven on a two-version
matrix — so the warning was firing on a live build path on every run in the portfolio
rather than being cosmetic. *A first version of this sentence said all eleven used `[dev]`
on two versions, which is one repository's workflow read as the portfolio's.* `requires` moved to `setuptools>=77`, the release that understands the
expression.

*This is the opposite shape from the errata above: those corrected a figure the record had. This
one is a fact the record never held, and it changes L5 from tidying into scheduled work.*

#### 2. `mini-traceroute`'s exemption reaches both halves, not one

§5 predicts a structural exemption for the licence half — it is C++, holds no `pyproject.toml`.
It also carried **no `Author:` field at all**, so it is the one repository Sx did not touch in any
way. The row said to *"record `mini-traceroute`'s structural exemption"*, singular; it is two.

#### 3. §6 row 3 is discharged by an instrument for the first time, and it says eleven

The row reads *"Ten of eleven pages are still served byte-identical to their committed file."*
Fetched and hashed, 2026-09-07: **eleven of eleven**. Five differ bytewise and every one of the
five differs *only* in line endings — `core.autocrlf = true`, and the byte delta equals the file's
CRLF count exactly, in all five.

**That is a constraint on `0009` §7 row 8 and not only a discharge.** A byte-for-byte hash run
from a Windows working tree would report five false regressions; the comparison has to normalise
line endings, compare the git blob, or state that it is CI-only.

#### 4. Two mistakes in the execution, recorded because neither was caught by a guard

- **`git add -A` was too broad.** Four sibling commits picked up untracked
  `.claude/sessions/*.md`. Removed before any pull request opened — but the cause stands: **eight of the
  twelve submodules do not gitignore `.claude/`**, so in those eight the files are untracked rather
  than ignored and any `-A` reaches them. `apply-scout`, `doc-extract`, `pl-jobs-lora` and
  `wroclaw-air-insights` already ignore it, and all four commits that picked a file up were in the
  exposed eight. *A first version said none of the twelve — measured only on the four repositories
  that had the problem, which is a sample chosen by the conclusion.*
- **A background script produced ten empty summaries that looked like results.** It resolved a
  relative interpreter path after `cd`, so every suite reported `<no summary>` — output shaped
  like a measurement with no measurement in it. Sx's evidence is what actually ran: `doc-extract`'s
  full suite (817), the one test in the portfolio that parses `pyproject.toml`, the byte guard over
  generated README regions, a sweep showing **no test anywhere reads an `Author:` field**, and then
  CI on each of the eleven pull requests.

### 4.15 What S9's first commit measured, and the two guards that shipped green

Taken 2026-09-08. Index only: no page moved, `GATED` is untouched, and the conformance table
is byte-identical on all eleven committed surfaces before and after — checked at three points
during the stage, because the change reaches `render.py`, which every clause reads.

**The design decision, taken against an architecture pass that recommended the other way.**
The pass proposed a `WRITE_SITES` registry in `sources.py`, probed at the pinned gitlink, with
the arithmetic between registered sites and rendered figures printed as a reconciliation.
`0009` §7 row 6 recommends the opposite — *no permanent source census* — closing W4, whose
argument is that `sources.py:1` defines the module as *"the I/O boundary, and nothing else"*.
**Row 6 was taken**, and the pass's own measurement is the strongest argument for it: grepping
`car-price-ml` for `:,` returns eighteen hits of which three are write sites, so a discovery
sweep is roughly 80 % false positive — and a *declared* registry is hand-authored, so it
records the hand count rather than replacing it. It would have inherited the blind spot and
added an I/O axis and an `ADR-0004` capability amendment to carry it.

What the checker can count honestly is the other side of the same migration: **the figures
those sites reach**, which are bytes it already holds. That is what ships.

#### Three things the record did not have, and a fourth the reconciliation found

| | measured |
|---|---|
| **88 figures, 88 separators over the eleven; 91 and 91 over the twelve** | `clause_8_separator`'s docstring states the two are equal *"because none prints a figure at or above a million"* — an assumption about the corpus, asserted in a comment. It is now printed on every run in both units, so the first seven-digit figure makes them disagree **in the report** rather than silently inside a tally. *Both scopes are given because the first draft of this row gave only `88` and did not say of what: the `surfaces` job reads eleven and the scheduled `live` job reads twelve, and a figure that does not name its corpus is the defect this stage was reviewed twice for.* |
| **The portfolio's only U+00A0 is `in code 1`** | `doc-extract`'s `3<U+00A0>466,62` is a displayed specimen of the Polish invoice format its extractor reads. §4.11 requires S9c's exemption censused *"so it cannot silently widen"*, and until this commit `Page` kept a flat list of strings in which that figure and an ordinary one were the same kind of thing. The exemption now has an **element** as its discriminator instead of a literal string |
| **`car-price-ml` prints `8<U+202F>612` and `8<space>612` on one page** | The first in `<svg text>` from `charts.py:76`, the second in `<p>` from the template — one figure, two formatters, and the element is what tells them apart. §4.13 did this reconciliation by hand once and it is how the twentieth write site was found; it is now a printed line |

Also printed and not previously stated anywhere: **four of the eleven committed surfaces group
no thousands at all**, listed as rows rather than omitted, because an absent row and a row
reading zero are different claims and only one of them is checkable.

#### And a fourth, which is a finding about this plan rather than about the checker

**S9's twenty-site scope and the clause it closes measure different populations, and nothing
said so.** Reconciling the census against §4.11's write-site table on its first use:
`car-price-ml/app` is credited with **two** write sites — `docs/app/index.html:27` and `:7`,
the `<meta name="description">` — and the census scores **one figure** there. The meta content
is an attribute; it is not in `rendered_text`; clause 8 cannot see it.

Swept over the twelve: **six grouped figures live in `<meta>` content and clause 8 reads none
of them** — `car-price-ml` `8<space>612` and `8<space>798` in both `description` and
`og:description`, `car-price-ml/app` `1<space>200`, `doc-extract` `183<U+202F>798`. **Five of
the six are non-conforming.**

*This is the checker obeying the spec, not missing it.* `c8.s2` reads *"scored over whole
grouped figures in each page's **rendered text**"*, and `tools/spec.py` carries that sentence
verbatim. The consequence is the plan's:

- **Fixing all twenty sites and turning clause 8 green are different achievements.**
  `car-price-ml/app` goes green on `:27` alone, while `:7` keeps publishing a plain space into
  the description a search result and a social card render.
- It is a second instance of the escape clause 8's docstring already names for another shape —
  *deleting the grouping is a cheaper route to green than migrating* — and the remedy is the
  same kind: **an amendment to `0007` §5, not a change to the checker.** S9c already carries
  one amendment; whether the two travel together is that stage's call.
- §4.9 records `og:description` having been *"outside the provenance rule entirely"* on this
  same surface. The blind spot has a history and this is its second appearance.

**Not fixed here, and deliberately.** Widening clause 8 to read attributes would move the
conformance table, and this commit's contract is that it does not. Recorded so S9 cannot spend
its scope figure without knowing the two halves are not the same set.

#### The twelfth surface's clause-8 figures, counted for the first time

The `live` job dispatched on this branch reads all twelve from the wire, and it is the first
count of `wroclaw-air-insights` this clause has ever had: **3 figures, `comma` 3** — in `b` 1,
`p` 1 and `span` 1. §4.11's write-site table credits that repository with **five** sites
(`accuracy_section.py:25`, `regime_section.py:25, 46`, `report.py:248, 307`); the page renders
three figures. Neither number is wrong — a formatter can render none or many depending on the
data of the day, and `wroclaw` rebuilds daily — but the two are now both printed, which is what
lets S9a check its `wroclaw` edit against something rather than against a memory.

Portfolio-wide over the twelve: `comma` **5**, not 2 — `ab-lab` 2 plus `wroclaw` 3.

> **Corrected 2026-09-08, and the correction is about the process rather than the number.**
> This paragraph first said the three sit *"in `p` 2 and `b` 1"*. They sit in `b` 1, `p` 1 and
> `span` 1. The wrong version was obtained by **subtracting `ab-lab`'s two from the portfolio
> `comma` row** — `p` 2, `b` 1, `span` 1, `td` 1 — instead of reading the surface, which is a
> hand derivation off a printed total and lands the total right and the parts wrong.
>
> **It is the one commit of this stage that no `code-reviewer` pass saw.** Two passes ran and
> both blocked on figures; this paragraph was written after the second and merged without a
> third, on the argument that it was documentation. The stage's own subject is that a figure
> nobody measured is a figure nobody should quote, and `0008` §3's rule — *figures come from an
> instrument, not from a hand count* — does not have a docs exemption. `0009` §13.6's shape
> once more: the fix inherits the blast radius of the thing it fixes, and this paragraph was
> itself a fix for an unscoped figure.

#### Two mistakes in the doing, and both are the class this file exists to record

1. **The census printed the page's own bytes, and killed the mode CI runs.** `--detail` died
   with `UnicodeEncodeError: 'charmap' codec can't encode character ' '` on a cp1250
   console, taking the whole report with it — on the census's first run. Every other line in
   this checker names codepoints instead of emitting them, and that convention turns out to be
   load-bearing rather than tidy. The second reason survives any encoding: a space, a thin
   space, a no-break space and a narrow no-break space are **one string** in a terminal, a diff
   and a grep, so a census whose rows a reader cannot tell apart is the hand count with an
   instrument's authority.

2. **Two guards shipped green over the mutation they were written for**, both found by
   mutating and neither by re-reading:

   - the ancestry guard was built from `<br/>` and `<img>`, which are **void** and so never
     enter the branch that pops the tag stack. It took a non-void self-closed tag — `<span/>`,
     or the `<h1/>` the neighbouring comment already records from an earlier repair — to reach
     the code the test names;
   - the `--only` guard asserted the census stays silent for a single surface, on a fixture
     whose pages **group no thousands**. It was silent either way, and passed with the
     suppression removed.

   *The shape is one shape: a guard whose fixture cannot reach the branch it names.*

3. **The review found two more of the same, and repairing one of those exposed a third.**
   Recorded as an erratum to the two rows above rather than rewritten over them, because the
   count is the finding:

   - `test_a_figure_is_never_read_across_two_text_nodes` used `<span>5</span><span>315</span>`
     — **no whitespace between the elements** — so a welded read yields `5315`, which matches
     `_GROUPED` under no reading at all. The guard for the mechanism behind *every wrong
     separator tally in the record* was green over that exact weld. The docstring cites
     `auth-log-scan`'s stat tiles, which are separated by markup whitespace; the fixture was
     not a reduction of them.
   - `test_the_census_prints_every_grouped_figure_and_asserts_nothing` ran with
     `--report-only`, and `main` returns 0 at that branch **before** any gate section prints —
     so both assertions carrying *"asserts nothing"* held whether the census gated or not. A
     census appending to `blocked` left it green and reddened **one** test in the suite, in a
     module marked `submodules`. *A pull request green on `core` alone proved nothing about
     it*, which is the hazard `CLAUDE.md` states about `GATED`, reappearing on a different
     constant.
   - Repairing that one left it green again: the seeded figure was **conforming**, so a
     gating census had nothing to object to and behaved exactly like a printing one. Found by
     re-running the mutation rather than by trusting the repair — §13.6's rule that a fix
     inherits the blast radius of the thing it fixes.

   **Four guards, five occurrences.** With the two above that is the ninth through thirteenth
   appearance of §3.9's class, and the row that said *ninth and tenth* was written while three
   of them were still green. Three further census properties had **no** effective guard at
   all: the verdict column (`assert "clause 8" in out`, which `not clause 8` satisfies — the
   substring shape §12.1.2 records, here costing a verdict rather than a figure), the
   both-units branch that fires only above a million, and the `in <element>` column. Each was
   proved by a mutation that left the **whole suite** green.

4. **A sentence this commit's own instrument refutes, in the docstring arguing for the
   instrument.** `render.py` said the specimen aside, *"every other grouped figure on the
   twelve sits in `<p>`, `<td>` or SVG `<text>`"*. The census refutes it: **fourteen
   counterexamples** — fifteen figures sit outside those three elements, one of which is the
   specimen the sentence had already excluded. A reader scoping S9 off the enumeration would
   have missed **nine** of `car-price-ml`'s sixteen non-conforming figures.

   *Both of those numbers were wrong when this erratum was first written* — "fifteen
   counterexamples", which counts the specimen the sentence excludes, and "five figures",
   which is the number of distinct **elements** `car-price-ml`'s sixteen span rather than the
   number of figures outside the enumeration. Found by the second review pass: a figure right
   about one quantity and written about another, **inside the erratum whose subject is that
   failure**, understating the reader's exposure by four.

   **The repair was not a better enumeration.** The docstring now states only that `<code>`
   is unique, which is the single fact the exemption needs; the distribution is what the
   census prints on every run. Spelling it out was a hand-typed census — `0009` §8 row 1 is
   this record refusing to type one for exactly that reason — so the first fix reproduced the
   defect it was fixing, at a smaller radius. `0009` §13.6, met by the stage that cites it.

5. **A second review pass, and it found the census has two `in` columns where the record
   assumed one.** Item 3 lists the `in <element>` column among the properties that had no
   guard, and the guard written for it covered the **per-figure row `--detail` prints**. The
   *summary* row — `in code 1, p 1`, printed on every run under the portfolio totals — was
   still unguarded, and deleting it left the whole suite green. It is also the row the
   deleted docstring enumeration was a hand sum over, so the one line that could have kept
   that figure honest was the line nothing checked.

   And `_group`, the test helper, appended with `str.replace("</body>", …)`, which returns
   the string unchanged when it matches nothing. Removing `</body>` from a fixture reddened
   four tests loudly and left **the `--only` guard green** — the same guard item 2 already
   records passing for the wrong reason. It now refuses rather than doing nothing.

**Nineteen mutations, each red on the guard that names it** once every repair above was in.
Suite **460 → 479**, `core` **419**, `submodules` 60. `python -m tools.pagespec` and
`--detail` both exit 0, and the conformance table is byte-identical to `main`'s at every one
of the six points it was checked — including once against `main`'s own checker run over the
same live trees, which is the comparison rather than the assumption.

*The stage's own numbers moved under **both** review passes — the second correcting two
figures inside the erratum written to correct the first. That is the argument for the census
in miniature, and the reason the enumeration was deleted rather than re-typed: every figure
left here is one an instrument prints or a mutation demonstrated.*

#### What rides with it, and what it unblocks

`0009` §7 row 13's other two items were taken in the same pass: **N1's remaining half** — the
workflow's two `paths:` filters are now tied to `sources.SURFACES` by a `core` test, closing
the one registry drift the row correctly calls *the silent failure* — and **N3**, resolved as
deferred and unowned in `ADR-0004` §4 and in `tools/spec.py`'s `c3.s2`. N3's evidence did not
reproduce and its conclusion sharpened; `0009` §8 row 7 records what a sweep asking the wrong
question cost.

**S9c is now buildable and it goes second, not last** — it changes no page, its whole scope is
a `0007` §5 amendment plus the exemption, and `8 separator` cannot enter `GATED` before it
lands, because `doc-extract`'s page will otherwise keep failing on a figure that is correct by
design. *The ledger did not carry that dependency.*

**And the `GATED` widening is its own commit, after the sibling pull requests and after
`wroclaw` rebuilds.** `wroclaw` commits no HTML and republishes from a Pages artifact rebuilt
daily, so its published page does not move when its pull request merges — while
`test_the_ratchet_cannot_be_narrowed_either_every_clean_clause_is_gated` reads the eleven at
the superproject's gitlinks and *demands* the widening the moment those eleven go clean. A
pointer bump that cleans the eleven arms the floor guard while the twelfth still fails. The
guard's own failure message is the procedure: land the siblings, **do not bump the pointers**,
confirm the twelfth with `--fetch` or a `live` dispatch, then bump and widen in one commit.
The same trap applies to `4 title` after S10, where `wroclaw` is one of the four surfaces.

### 4.16 What S9c closed, and the sentence the corpus refused

Taken 2026-09-08, straight after S9's first commit and before any sibling edit — which is the
order S9-0 made possible, because the exemption's discriminator is a thing the census prints.
**No page was edited in any repository.** `doc-extract`'s `build_index.py:1590` already writes
`U+202F`; the stage was always *"a spec amendment and not an edit"*, and it stayed one.

`0007` §5 clause 8 gains two sentences and records one refusal. Each was measured over all
twelve surfaces **before** being written.

#### 8a — the specimen, and why it is an element

A figure the page displays as a specimen of another system's format is quoted, not written.
`doc-extract` prints `3<U+00A0>466,62` to say *this is the shape the extractor reads*, and
requiring `U+202F` there would require the page to misquote the format it documents.

**Scoped to `<code>` rather than to a value, a surface or a separator**, because §4.11 admits
the exemption only on the condition that it is censused *"so it cannot silently widen"*. Two
things follow, and both are guarded: the clause reports the exempt figure in its own detail
**even where the page would otherwise read `n/a`** — a page displaying a specimen and a page
grouping nothing are different states — and the census prints it with its element on every run.
Measured: **one** such figure on the twelve, and it is the portfolio's only `U+00A0`.

#### 8b — the metadata, and the write site the old rule could not see

Scoring widened from *the page's rendered text* to that **and the metadata it publishes**,
scoped to clause 5's six keys. §4.15's fourth finding is what forced it: `car-price-ml/app`
writes `1<space>200` from **two** sites, `docs/app/index.html:7` and `:27`, and the old rule
reached only the second — so a stage fixing the body alone would have turned the surface green
while the description a search result renders kept a plain space.

Measured before amending: six grouped figures in metadata across three surfaces, five
non-conforming, and **widening moves no surface's verdict**. It moves three counts:
`car-price-ml` `space 16 → 20`, `car-price-ml/app` `space 1 → 2`, and `doc-extract`
`U+202F 3 → 4`. *This paragraph said two and omitted the third, contradicting §4.15's own list
of the six metadata figures by an enumeration that read as complete — the exemption cannot add
a `U+202F`, so `doc-extract`'s fourth is 8b's doing and nothing else's.* A write site the stage
must fix became a figure the stage's own instrument can see.

#### 8c — the escape stays open, and why no number is written down for it

*"A figure of four or more digits is grouped"* is the closure named in `clause_8_separator`'s
docstring and in `tools/spec.py`'s `c8.s1` — **those two and no others.** It is not taken.

**The first version of this section said the corpus refutes it, and gave a count and a
characterisation. Both were wrong, and the review caught them.** The claim was *27 ungrouped
four-digit tokens, and they are years, dates, the traceroute base port and identifiers —
figures that are not quantities at all.* The corpus says otherwise:

| named token | surface | what it is |
|---|---|---|
| `9894` in *"every one of the 9894 values"* | `doc-extract` | **a quantity**, ungrouped, on the page that groups `183<U+202F>798` — the exact inconsistency the sentence exists to catch |
| `3989` in *"every one of those 3989 values"* | `doc-extract` | a quantity |
| `6570` in *"6570 of 6571 listed today"* | `it-job-radar` | a count of job offers — **this section called it an identifier** |
| `2026-03-14` | `auth-log-scan` | a date, which the sentence would catch wrongly |
| `33434` | `mini-traceroute` | the traceroute base port, likewise |

So the sentence is **not refuted — it is undecidable by a static read.** It would catch real
violations and real false positives together, and the page that S9c turns green is itself one
of the pages it would rightly catch. Separating the two needs a page to declare which of its
numbers are quantities, and that is a larger amendment than this one. *That conclusion is
stronger than the one it replaces and it costs the same nothing to act on, which is worth
noticing: the wrong evidence was not supporting a wrong decision, it was supporting the right
decision badly.*

**And no total for that population is written anywhere — which is not the same as "no figure
is."** `0007` §5 states 8a's *one* and 8b's *six*, both frozen and both reproducible, and the
erratum above quotes the withdrawn `27` in order to withdraw it. `ADR-0004` §5 admits a
measurement into a normative document **once it is frozen**; the omission here is that this
one could not be. *The first version of this paragraph claimed no figure was written at all,
twenty lines below one and in a document carrying two more — the same absolute-claim shape the
section is about, committed while writing it.* Four attempts to measure the
population produced **four different answers** — the first matched inside hex strings because
it did not exclude letter adjacency; the second and third disagreed with each other because
the character class turned on a codepoint that is **invisible in a terminal**, and the shell
rendered it one way in one run and another way in the next. That is precisely the failure this
stage's own census was built to end, reproduced by the person building it, four times, inside
the amendment that ends it.

*`0007` §5 carries the rule and names the counterexamples; it carries no count. `ADR-0004` §5
is the reason — a document that states measurements cannot be accepted without freezing them,
and this one could not be frozen because it could not be measured twice the same way.*

#### What the review found, and it blocked on the normative half

**A measurement written into `0007` §5 that did not reproduce, and a characterisation the
corpus refuted.** That is the worst place in this repository for a wrong figure: `ADR-0004` §5
accepts §5 as normative precisely on the condition that it states rules and not measurements,
and this one carried both a count and a claim about what the counted things *are*. The claim
was refuted by `doc-extract` — **the surface this very stage turns green** — which prints
`9894 values` ungrouped on a page where it groups `183<U+202F>798`. The section above is the
rewrite; the count is gone from every document and the demonstration is named tokens.

**Two guards green over the mutation their name claims, and three properties with no guard.**

- The metadata-scope guard was named for clause 5's **six** keys and exercised **one**.
  Narrowing the production filter to two keys left the whole suite green — it caught widening
  past clause 5 and nothing on the narrowing side, which is the direction a later stage takes
  to make a surface pass. Now parametrised over `CARD_META` itself.
- **Clause 8a shipped with two incompatible readings and nothing pinned either.** The code
  exempts on the whole ancestry; the docstring said the innermost tag. Both were green. Under
  the flat reading a figure in `<code><td>` keeps its exemption while the census prints
  `in td` — *spared by an element the census does not name*, which breaks the condition §4.11
  grants the exemption under. Settled as ancestry-wide, and `_where` now prints `code td` the
  way it already printed `svg text`.
- Unguarded entirely: metadata read raw where body text is flattened (so a `content` holding
  a doubled space hid the figure the same bytes show in a `<p>`); the exemption unmarked on
  the **per-surface** census row, which is the row a stage reads first; and — found by
  mutating my own repair of that row — the row marked `exempt` whenever *any* figure was
  spared rather than all of them.

*Four counts, one nesting reading, and three unguarded properties, in a stage whose subject is
that a figure nobody measured is a figure nobody should quote.* The stage did the thing it was
built to prevent, in the amendment that prevents it, and it took a review pass to see it.

Six further mutations after the repairs, each red on the guard that names it. Suite **488 →
497**, `core` **437**.

#### The second review pass, and the two it blocked on

**A sentence in `0007` §5 that §5 itself refutes.** The withdrawal was justified with *"this
document states rules; `ADR-0004` §5 is why a measurement cannot be accepted into it."* The ADR
says the opposite of that flat reading — *"cannot be accepted **without freezing them**"* — and
§5 carries three frozen measurements, two of them in the same amendment and one of them four
lines above the sentence. The justification for omitting an unfreezable figure declared the
frozen ones inadmissible. *Right conclusion, wrong reason, in a normative document* — the same
pairing as 8c itself, one review round later.

**And the repaired scope guard leaned on an unpinned constant, so the hole moved up rather than
closed.** Parametrising over `CARD_META` catches a narrowing of the *filter*; it cannot catch a
narrowing of `CARD_META`. Measured: dropping `og:type` from the tuple left the **whole suite
green** — the parametrised guard loses one case and says nothing. And the constant feeds
**clause 5, which is in `GATED`**, so one edit silently narrows a gated clause and clause 8b's
scope together. `tools/spec.py` quotes the six from `0007` §5 and the registry is held to the
document, so the registry could not drift; the constant could drift out from under it. Now
pinned literally, because a guard that reads the constant it guards asserts nothing — which is
how the hole survived a round of being repaired.

The pass also replaced 8c's two named false positives with a stronger witness it found in the
corpus: `doc-extract` prints *"mandatory since 2026 — is `183<U+202F>798`"* in **one sentence**,
and `9894 values` on the same page. The originals, `2026-03-14` and `33434+`, both carry
adjacent punctuation a digit rule could key on, so a reader testing the claim against exactly
the evidence given could defeat it. One page, both kinds, nothing lexical between them.

*Counting this stage honestly: **six** guards or claims of the green-over-its-own-defect and
wider-than-its-measurement families, across two review passes and one self-audit, in the
amendment whose whole subject is that a figure nobody measured is a figure nobody should quote.*

#### One trade this stage takes, recorded because it comes due later

`og:url` is one of clause 5's six keys, so 8b puts it in clause 8's scoring scope, and the
parametrised guard pins it there. **Nothing on the twelve matches** — the census finds metadata
figures only under `description` and `og:description`. But once S9 brings clause 8 into `GATED`,
a canonical URL carrying a `_GROUPED` match, say `?n=1,234`, would **refuse the build** on a
string no reader reads as a quantity.

Taken deliberately, and the alternative was worse: excluding `og:url` means clause 8b's scope
stops being *"the six keys of clause 5"* and becomes a second, hand-maintained list of what
counts as published metadata — which is the drift `CARD_META` exists to prevent, and which the
review of this same stage found unpinned. Recorded here so the day it fires it reads as a known
trade rather than as a defect, and so the amendment that would undo it has its reason written
down: **a URL is machine-facing text inside a human-facing set, and the set is the thing worth
keeping whole.**

#### What moved

| | before | after |
|---|---|---|
| clause 8 failing, committed surfaces | 6 | **5** — `doc-extract` reads `ok 8 separator U+202F 4; U+00A0 1 specimen, exempt` |
| grouped figures censused, eleven surfaces | 88 | **94** — six in metadata |
| normative sentences in the registry | 31 | **33**, uncarried still 4 |

`GATED` is untouched and clause 8 stays outside it: five committed surfaces and `wroclaw` still
fail. The conformance table **moved on purpose**, which is what separates this stage from S9-0 —
and the two counts that moved are the metadata write sites becoming visible, not a page changing.

Six mutations, each red on the guard that names it. The one pre-existing test that had to move
is `test_the_recorded_narrow_spaced_page_reproduces_its_inventory`: **its fixture did not
change, the clause did**, and the reduction was re-checked against the live `doc-extract` page
before the expectation was rewritten — a fixture of record that had drifted from its origin
would have made that a rewrite of the evidence rather than of the verdict.

### 4.17 What closing S9, S10 and S5 measured — and the sweep that was wrong a third time

Taken 2026-09-08, in **one** ratchet cycle rather than the two §3 schedules. The fallback was
already written into the architecture pass that designed this closure: take one cycle if S10's
copy is approved before S9a's pull requests are ready, because the only argument for two was
that a bounded correctness fix should not wait on unbounded writing. The copy was approved in
the first minutes and turned out not to be copy at all — see below — so the cycle collapsed to
one, and `wroclaw`'s eleven-minute rebuild and the twelfth-surface confirmation were each paid
once instead of twice.

Eight sibling pull requests, then one index commit bumping seven pointers and admitting both
keys. **Every figure below comes from `python -m tools.pagespec`, `--fetch` or a mutation.**

#### 1. S9a was not build-only in *any* of the four, and the sweep that said so was wrong a third time

§4.13's first erratum corrected §4.11's sweep — *"no submodule test asserts which separator a
page writes"* — by finding **two** that do, both asserting a comma. Its own italic names the
mechanism: *"this one was searched for tests that assert `U+202F`; a test that asserts a comma
answers a different query."*

**A test that asserts a plain space answers a third, and five exist.** Swept with a pattern for
a digit, a separator character and three digits, across the tests of all five repositories:

| test | assertion | reached by |
|---|---|---|
| `it-job-radar/tests/test_coverage_series.py:110` | `assert "of 6 603 listed" in svg` | `site/build.py:355` |
| `pl-review-sense/tests/test_site.py:655` | `assert "0.944 at n=5 264" in markup` | `site/charts.py:294` |
| `pl-review-sense/tests/test_site.py:667` | `">4 800</text>" in markup` | `site/charts.py:284` |
| `pl-review-sense/tests/test_site.py:669` | `'…middle">5 264</text>' **not** in markup` | `site/charts.py:284` |
| `pl-review-sense/tests/test_site.py:671` | `assert "at n=5 264" in markup` | `site/charts.py:294` |

So the cost cell's *"**not** build-only in two of the four"* understates it: the stage edits a
test in every one of the four. **Three sweeps of the same question have now produced three
answers** — none, two, seven — and all three were wrong in the same direction, because each
searched for a spelling rather than for the property. `0009` §8's closing note is the diagnosis
and this is its fourth instance: *a sweep is worth what its query is worth, and the query is the
part that does not appear in the finding.*

*The instrument that would have answered it in one line did not exist until S9's own first
commit: the census prints every grouped figure with its element, and a sweep for **assertions
containing a grouped figure** is the same shape one layer out. That is worth noticing rather
than acting on — a test-corpus census is `0009` §7 row 6's refused shape, and refusing it was
right.*

#### 2. One of those five is negative, and it goes green over its own subject

```python
# pl-review-sense/tests/test_site.py:669
assert (
    'text-anchor="middle">5 264</text>' not in markup
), "on a log axis the last two sizes sit a few pixels apart; two numbers there read as neither"
```

Once the formatter emits `5<U+202F>264`, the forbidden string can never appear again. The
assertion becomes vacuously true and the tick-collision rule it guards becomes unguarded,
silently, with the suite green.

**Demonstrated rather than argued**, which is the only form this record accepts. Disabling the
collision rule (`if position - drawn_at < 44` → `if False`):

| assertion spelling | rule disabled | result |
|---|---|---|
| re-pinned to U+202F | yes | **FAILED** |
| plain space, i.e. before the stage | yes | **passed** — the guard is vacuous |

This is §4.13 item 3's shape — *the guard is correct today, the stage is correct today, only the
composition is wrong* — in a repository that section did not name, and it is the second of two,
not the only one. Item 3 called itself *"the only item in this ledger that cannot be found after
the fact."* That was true of the item and not of the class.

#### 3. `wroclaw`'s provenance guard needed two lines, and a fixture that reaches them

§4.13 item 3 names `tests/test_report.py:1524`, the `_NUMBER` pattern. The strip at `:1530` is
equally load-bearing and the section does not name it: widening the pattern alone makes
`float("1<U+202F>752")` raise, so the two must move together. Both did.

**And neither would have been noticed by the guard's own fixture.** `_fresh_metadata()` carries
`n_train = 800` and `n_test = 200`, so **no four-digit figure has ever entered its `measured`
set** and `_NUMBER`'s grouping branch has never run under it. Widening a pattern no fixture
reaches is not a repair. `test_the_card_description_check_can_read_a_grouped_figure_at_all`
lands with it and reddens on each half separately — `AssertionError` when the pattern is
narrowed, `ValueError` when the strip is.

*Three of this stage's findings are the same sentence at three depths: a query narrower than the
claim (1), a guard narrower than its name (2), a fixture narrower than its guard (3).*

#### 4. A sixth `car-price-ml` write site, reached by no rebuild

§4.11's table credits `car-price-ml` with `charts.py:76`, `build.py:76`, `export.py:179` and
three template literals. After all six were corrected and the page rebuilt, the checker still
read `FAIL 8 separator U+202F 28, space 5`.

The five are the refusals table's `34 093`, `33 576`, `38 399` and `37 248`, in `<span>`. They
are written by `export.py` into `docs/data/refusals.json` and reach the page **from the JSON**,
and `site.build` does not run the exporter — CI diffs `docs/index.html`, `docs/app/styles.css`
and `docs/app/config.json`, and re-runs neither `export` nor anything that would notice. So a
formatter change lands, the page rebuilds, and five figures keep the old glyph with every local
guard green.

`site.export` was re-run rather than the JSON hand-edited. Every measured value came back
byte-identical and the browser-parity check reported `worst 3.97e-06 PLN over 200 adverts`; only
`commit` moved, which is the field recording the HEAD the export was taken at.

**The general form, and it is the one worth carrying forward:** a page's figures do not all come
from the page's build. Where a committed *data* artifact holds pre-formatted text, the formatter
and the artifact are two hops apart and only the index checker spans them.

#### 5. `ab-lab`'s recorded evidence named a version two releases old

Re-running `examples/validation_table.py --record` moved three fields, not one. The scenario
string was the intended one; `recorded_on` was `2026-08-21`; and **`ab_lab_version` was
`0.3.0.dev0` against a package at `0.4.1`** — the published provenance naming a version that no
longer exists.

**Every one of the five measured rates reproduced to the digit** — 0.0538, 0.0497, 0.8077,
0.7929, 0.0110 — so the seed is honest and two minor releases moved no result. That is the check
worth having, and it is why the re-record is reported here rather than assumed. *§4.13's cost
table called this half "a simulation re-record" and priced it as work; it was work, and it also
turned out to be a measurement nobody had taken.*

#### 6. What `tests/test_record.py:86` actually guards, which is not what its name suggests

The obvious mutation — `examples/validation_table.py:130` back to its own `{:,}` — left it
**green**. The guard reads `docs/data/findings.json`, a committed artifact, and an un-recorded
script edit does not touch it. Mutating the recorded string reddens it; mutating the script *and*
re-recording reddens it.

So the guard is live over the evidence and over the script *through* a re-record, and
deliberately blind to a script edit alone. That is correct — `findings.json` is the artifact —
but it is not what *"still names the size the design solves for"* suggests to a reader deciding
whether the write site is covered. Written down because the first reading was mine.

#### 7. The escape, and the one literal left standing

The portfolio's two already-conforming write sites — `car-price-ml/site/charts.py:76` and
`doc-extract/docs/build_index.py:1590` — both wrote U+202F as **the character**. Every site this
stage touched writes it as `"\u202f"` instead, and the argument is this stage's own subject: in a
diff, a terminal and a `grep`, U+0020 and U+202F are the same string, so a reviewer asked to
approve twenty write sites could not verify one of them by eye. Markdown and HTML templates keep
the character, having no escape.

*The convention broke on the author before it was written down.* Three separate attempts to type
the escape into a commit message and a patch spec emitted the character instead, each time
silently. The patcher that applied this stage builds both spellings with `chr()` and refuses an
edit whose search string is not present at the expected multiplicity — which is what caught it,
twice, without a single wrong byte reaching a repository. §4.15's second mistake, met from the
other side: there it was a terminal that could not show the difference, here an author who could
not type it.

**`doc-extract/docs/build_index.py:1590` is left as a literal**, and that is a decision rather
than an oversight: it is outside S9's scope, its page has read `clear` since S9c, and changing it
costs a pull request and a pointer bump for zero behaviour change. It is the one site where the
portfolio's convention is now split, and §5 carries it.

#### 8. What moved

| | before | after |
|---|---|---|
| clause 8 failing, twelve surfaces | 6 | **0** |
| clause 4 `<title>` failing, twelve surfaces | 4 | **0** |
| grouped figures, eleven surfaces | 94 — `U+202F` 24, space 67, comma 2, `U+00A0` 1 | **95** — `U+202F` 94, `U+00A0` 1 exempt |
| grouped figures, twelve surfaces | 97 — plus `wroclaw`'s comma 3 | **98** — `U+202F` 97, `U+00A0` 1 exempt |
| `GATED` | 8 prefixes | **10** — every clause key |
| suite | 498 / core 438 | 498 / core 438 |

The ninety-fifth figure is new rather than converted: clause 9's bridge prints
`{{ thousands(metrics.n_train) }}`, so S5 added a grouped figure to the page S9b was clearing.
*The total moving by one while the stage converted every one of the eleven surfaces' sixty-nine
non-conforming figures is exactly the kind of delta a hand count absorbs without noticing, and
the census made it a sentence.*

`served` reads `ok` on eleven of eleven: every published page is byte-identical to its committed
file, digests equal, after seven merges in one afternoon.

#### 9. The eleven/twelve trap, watched rather than avoided

It fired exactly where `CLAUDE.md` says. With the eleven working trees updated and the pointers
untouched, `pytest -m submodules` reported:

```
4 title reports no failure on any committed surface and is not in GATED:
the ratchet was narrowed, so a clause that passes everywhere has stopped gating.
```

That is the floor guard **demanding** a widening that would have reddened the next morning's
`live` run, because `wroclaw` had not rebuilt yet. The procedure held: siblings landed, pointers
stayed, `refresh.yml` was watched to completion — eleven minutes, triggered by the push to
`src/**` exactly as §4.5 records — `--fetch` reported all twelve `clear`, and only then did the
pointers and `GATED` move in one commit.

**It is spent, not gone.** The next key admitted to `GATED` meets it again, and `0009` §7 row 12's
contrast clause is the one on the table. The architecture pass that designed this closure proposed
closing the asymmetry in the instrument — parametrise the sweep's fetch mode and give the `live`
job a `pytest` step — and it was **deliberately not taken**: its feasibility was reasoned rather
than run, and §13.6's rule is that a fix inherits the blast radius of the thing it fixes. Changing
the two ratchet guards in the window those guards were carrying the stage is the wrong week for it.
§5 carries it.

#### 10. The gate, and the test that was written for this moment

`GATED` now holds every finding key a clause can fail on, so `_gated` and `status == FAIL`
coincide for everything except `served`. Three mutations:

| mutation | result |
|---|---|
| one U+202F on `pl-review-sense`'s page back to a plain space | checker **exits 1** |
| `mini-traceroute`'s title back to leading with the name | checker **exits 1** |
| both new prefixes removed from `GATED` | floor guard **reds** in `surfaces` |

The first two are the point of the whole stage: **the gate now refuses a build on a wrong
separator and on a title that leads with the project's name**, which it has never been able to do.

And `test_a_page_failing_only_an_ungated_clause_still_passes` survives, as its own docstring
predicted one stage early: it constructs its ungated set by *removing* these two prefixes rather
than borrowing whatever `GATED` holds. *"Removing the two prefixes here is a no-op today and is
the whole test afterwards."* Today is afterwards.


#### 11. What the review found, and it blocked on a guard this stage wrote

**The stage's own subject, committed inside the guard against it, and green over the half it
could not see.**

`car-price-ml/tests/test_site.py`'s clause-9 guard shipped its `<style>`/`<script>` strip as

```
re.sub(r"<(style|script)\x08.*?</\x01>", ...)
```

— `\b` and `\1` written as the **bytes** U+0008 and U+0001, inside a raw string, so `re` looked
for a backspace and an SOH and matched nothing. Cause: that one edit was authored through a
shell heredoc rather than through the patcher item 7 describes, and the heredoc consumed the
backslashes. In a diff, `git show`, a terminal and a `grep` the line renders as
`<(style|script).*?</>` — **indistinguishable from the correct one**, which is this stage's
entire subject arriving in a form the stage had not anticipated: not an invisible *separator*
but an invisible *escape*.

The consequence was a live hole. With the bridge paragraph moved from the page body into a
`<style>` element, the guard **passed** — clause 9's bridge invisible to every reader, the suite
green, and CI's byte-diff content because template and page still agreed.

**And the mutation that "proved" the repair could not have caught it.** Item 7 of the previous
commit reports three mutations, one of which found the comment hole and reddened after the fix.
That mutation exercises `r"<!--.*?-->"`, which carries **no backslash to lose**. The half that
was broken was never mutated, because the repair and its proof were written in the same breath
and the proof was aimed at the defect already known. *A mutation confirms the branch it enters.
Repairing two branches and mutating one is the same arithmetic as a sweep whose query is
narrower than its claim — findings 1, 2 and 3 of this section, at a fourth depth, inside the
commit that names the first three.*

**Two more the review measured that this section had stated otherwise:**

- **Item 4's "sixth write site" is a seventh.** `car-price-ml/site/build.py`'s `_megabytes` kept
  `f"{size / 1e6:,.0f} MB"` three lines from the helper this stage extracted, and it feeds the
  `<h1>` claim. It is dormant rather than live — no artifact in the portfolio reaches four
  digits of megabytes — but the rival is already 590 MB, and now that clause 8 gates, the first
  bake-off winner over a gigabyte refuses the build during an unrelated retrain. Routed through
  `thousands()`; the page does not move.
- **Item 7's "one site where the convention is now split" was two.** `car-price-ml/tests/test_site.py:194`
  held a literal U+202F beside a literal U+0020, so `.replace(…).replace(…)` read as a duplicated
  call. It predates the stage and the sentence claiming a single split site does not — measured
  after writing it would have found both. Written as an escape now; `doc-extract` remains the one
  deliberate literal, and §5 carries it.

**One the review found that the guard's twin already had.** The clause-9 guard does not read
`<meta>` content, and `mlops-car-price`'s does, with its reason written down: those tags carry
figures, and stripping tags alone drops them. This page publishes **six** grouped figures inside
`<meta>`, so a sibling's cell pasted into the description would have passed while reaching every
search result and shared link — the second of the two readers clause 4 names. The commit
introducing the guard said it was *"built deliberately like its twin, including the two details
that twin's docstring records paying for."* There were three.

**And `ab-lab`'s README came out of this stage carrying both spellings** where it had been
consistent in one: `:317` moved because the page carries the same sentence, and three hand-typed
figures did not. `:178` and `:325` follow; `:189` deliberately does not, because it is inside a
fenced code block a reader copies and the README is not a surface `0007` §5 governs.

*Counting this stage honestly, and the count is the finding: **five** of the green-over-its-own-
subject family — the negative assertion at `pl-review-sense:669`, `wroclaw`'s unreachable
fixture, the inert `<style>` strip, its unmutated half, and a guard narrower than the twin it
cites. The first two this stage found and fixed; the last three it committed, and a review found
them.* `0009` §13.6 once more: a fix inherits the blast radius of the thing it fixes, and every
one of these is inside the repair for the one before it.

**What the review confirmed rather than found**, which is worth as much: the eleven/twelve
procedure reproduces step by step from the record alone; `wroclaw`'s two-line widening reddens
on each half separately; `pl-review-sense:669` reds on the collision rule; every figure in item 8
reproduces from the checker; and across every source this stage touched there are **zero**
literal U+202F in Python outside the two now named.

### 4.18 What closing S11 measured — and the row that could not be done as written

`0009` §7 row 13b, taken 2026-09-08 straight after S9/S10 and the landing-surface measurement,
because §7 row 12's own state cell says this is the procedure that admission needs.

**The row does not land as written, and the reason is the finding.** Row 13b asks for one
change — parametrise the sweep's fetch mode and let the expected count follow it. Applied
literally, the fetching floor emits `served`, sees it `PASS` on eleven of eleven, and under its
own rule *demands* that it be gated. `test_report.py` refuses `served` in `GATED`. `test_spec.py`
refuses it in `NOT_A_CLAUSE`, and is right to: that set's pin demands a proof the key can never
be `FAIL`, and `served` fails whenever a sibling publishes ahead of a pointer bump. **Three
guards, each correct, and no arrangement satisfying all three.** `0009` §7 row 8 had already
written down the shape of what was missing and left it; `ADR-0006` is the decision that supplies
it.

**Four ways a fetching corpus is incomplete, where the row implies one.** The twelfth not
answering is the one a count catches. The other three are silent, and the third is the dangerous
one:

| # | how | what the floor would then do |
|---|---|---|
| 1 | the twelfth did not answer | `read` is eleven against an expectation of twelve — caught |
| 2 | one of the eleven fell back to its committed file | certify a key clean on *the twelve published surfaces* from a file nobody served |
| 3 | a same-origin **stylesheet** the wire dropped | `_undecided_where_the_stylesheet_is_incomplete` rewrites every clause-1 and clause-3 `FAIL` to `UNDECIDED`, so a **failing** clause reads clean and its admission is *demanded* on a sheet the run never opened |
| 4 | the mode never reaching `sources.load` | the wire is taken from all twelve, the corpus is incomplete, and the guard **skips** — green, with the row's whole subject unmeasured |

All four skip rather than fail, because none is a statement about a page. Number 4 needed its own
assertion for the reason that makes it worth recording: **a skip is a pass.** With `_fetch`
stubbed to answer from disk no fetch can fail, so an incomplete corpus there has exactly one
cause and the guard fails instead of skipping.

#### The twenty mutations

Stated as *break this, watch that go red*, in §4.12's form, because that section's own erratum
rules that **a mutation named in prose is not a mutation** and its count is not reproducible
until the list is written down. Thirteen were run before the `code-reviewer` pass; the pass
found **seven** more that shipped **green across all 510 tests**, and those are rows 14-20.

| # | mutation | what reddened |
|---|---|---|
| 1 | `_sweep` ignores its mode argument | `…reads_the_twelfth_surface_the_fetchless_one_cannot` — **green on the first attempt**, see below |
| 2a | `_expected` pinned at `len(COMMITTED)` | the same test, fetching case |
| 2b | `_expected` pinned at `len(SURFACES)` | the same test, fetchless case |
| 3 | the incomplete-corpus skip removed | the three wire-failure guards |
| 4 | the unreachable-stylesheet branch removed | `…stylesheet_the_wire_dropped_skips_the_fetching_sweep` |
| 5 | a prefix declared in two rows | `…one_row_per_prefix_and_every_state_is_a_known_one` |
| 6 | a state nobody derives from (`"gatd"`) | the same |
| 7 | a non-gated row with an empty reason | `…every_row_the_gate_does_not_refuse_on_carries_a_reason` |
| 8 | `_policy` returns nothing | `…prints_every_key_the_gate_does_not_refuse_on` |
| 9 | a clean key dropped from the registry | the floor, `…cannot_be_narrowed_either…` |
| 10 | `explained` matches exactly instead of by prefix | the floor, and the `core` arithmetic test |
| 11 | `served` renamed out of the registry | `…served_is_deliberately_outside_the_gate…` |
| 12 | the `--fetch` pytest step moved into `surfaces` | `test_the_wire_never_reaches_the_push_path` |
| 13 | `pending_refuted`'s fetching branch disabled | `…pending_row_clean_on_the_twelve_demands_its_promotion` |
| **14** | **a gated row demoted to `report-only`** | **nothing — see below.** Now `…report_only_set_is_pinned…` |
| **15** | **`main` stops printing the policy block** | **nothing.** Now `…prints_every_key…`, asserted through `main` |
| **16** | **a `--fetch` step in `surfaces` behind a step-level `if:`** | **nothing.** Now `test_the_wire_never_reaches_the_push_path` |
| **17** | **`--fetch` dropped from `live`'s pytest step** | **nothing.** Now the same guard's positive half |
| **18** | **`_policy` lists the gated rows too** | **nothing.** Now `…prints_every_key…` |
| **19** | **a nested prefix (`"4 "`) above `4 eyebrow`** | **nothing.** Now `…one_row_per_prefix…` |
| **20** | **a prefix duplicated across two states** | **nothing** — the disjointness assertion chained three sets with `&`, which is empty whenever any one is, and `pending()` is empty by design. Now `…gated_is_derived_from_the_registry…`, pairwise |

**Rows 14-20 are the finding, and the first four are one shape between them.** Each is a claim this
stage made in prose that no test held: *the registry cannot be narrowed* (14), *the policy is
printed* (15), *the wire never reaches a push* (16), *the ratchet reads twelve in `live`* (17).
Rows 14 and 15 are the two the brief warned about — a guard green over the defect it names,
and a fix that displaces one. **Row 16 is the sharpest**: `live`'s new `if: always()` is the
first step-level `if:` this workflow has ever carried, so the change that needed the guard
widened is the change that demonstrated the shape inside the file the guard reads.

**Two things about the doing.** Both are method rather than subject:

- **Row 1 was GREEN on the first attempt**, because the guard degraded to a skip rather than
  to a failure. That is incompleteness #4 above, found by the battery and not by reasoning.
  `pytest.fail` inside the skip handler is the repair, and *a skip is a pass* is the sentence
  worth carrying.
- **The battery's own first run was invalid.** Each detector was invoked as
  `pytest <path> -k a or b or c` with the expression split on whitespace into separate argv
  items, so pytest read `or` as a file path and exited non-zero — and *every* mutation reported
  RED, including two that were not caught at all. A mutation battery whose failure mode is
  indistinguishable from success proves nothing. Fixed by passing each `-k` expression as one
  argument **and by running every detector green against unmutated code first**, which is the
  baseline the first battery had no reason to skip and did.

**What did not move.** The conformance table is byte-identical on the eleven; `--fetch` reports
all twelve `clear`; `GATED` derives to the same ten prefixes it held before. Suite 498 → **511**;
`core` 438 → **447**, the thirteen new guards split nine to `core` and four to `surfaces`.

**And one correction to `CLAUDE.md`, found by a reader who came for a different paragraph.** Its
gate section said *"two clauses print and do not gate — clause 8 and clause 4's `<title>` half
— and they are the open work"*. S9 and S10 closed both on 2026-09-08, the morning before. The
sentence describing the partiality outlived the partiality it described by one day, in the file a
session loads first. **That is the argument for `gate policy` being printed by the run**: a
policy written in prose ages against an instrument that does not.

### 4.19 What S12 measured — and the three claims about row 12 that did not survive it

`0009` §7 row 12 is *contrast at the usage site*, and it was taken as an architecture pass plus
a measurement before any of it was built. The measurement refuted the pass's headline, found a
different failure that is real, and re-scoped the row. All three are the reason the stage
splits.

**1. The pass's "single most likely surprise" is not live.** The claim: `--accent-soft` measures
**2.93:1** on `--surface` (reproduced exactly), so any chart inside a
`.card { background: var(--surface) }` crosses SC 1.4.11's 3:1 floor in light mode. The pass
spot-checked two surfaces and cleared them. **Measured across all eleven: 35 `<svg>` elements,
zero of them inside an element carrying `card`.** Seven surfaces declare that rule and none puts
a chart in one, so the marks sit on `--bg` at **3.12:1** and pass — by 0.12, which is worth
knowing and is not a finding.

**2. A rule-keyed clause would be almost entirely false positives.** The cheap design — every
paint declaration against the page's two grounds — was run over the eleven: **500 sites, 59
under 4.5:1, 48 under 3:1**. Every text hit is `color: var(--bg)` on a *filled control* whose
ground is its own background; **24 of the 32** graphic hits under 1.3:1 are chart furniture
(`.axis`, `.grid`, `.lane-line`, `.track`) painted `--border` on purpose, and the other eight
are shapes filled with a page ground itself — `.chart .lane` on `--surface`, `.diagram .node`
and `.series-dot.observed` on `--bg`. None is a real finding; the first version of this
sentence put all 32 in the named list, which is a characterisation wider than the sweep. That is the measured argument
for the element-keyed, paint-order design and against the shortcut, and it is why **S13 is
sized from the walk rather than from the arithmetic**.

**3. The one live failure is in the place neither carrier was looking.**
`pl-review-sense`'s confusion matrix draws two text labels on each cell, and the cell's alpha is
a **presentation attribute** computed per cell from the data:

| label | token | densest committed cell | at the ramp's cap |
|---|---|---|---|
| `.cell-text`, the count | `--text` | 7.01:1 light · 5.21:1 dark | 6.70 · 4.91 |
| `.cell-share`, "95% of row" | `--muted` | **2.69:1 · 2.47:1** | **2.57 · 2.33** |

**Three of the nine cells failed, not one** — the whole diagonal, at 2.69/2.71/2.77:1 light and 2.47/2.47/2.59:1 dark. Counted by the `code-reviewer` pass on the sibling half, which is the second figure this stage got from a review rather than from its own sweep. With both labels on `--text` the worst cell is **7.01:1 light and 5.21:1 dark**.

**And the reasoning that should have caught it was already written down.**
`_CELL_MAX_OPACITY = 0.55` caps the shading ramp under a comment recording *why* — switching ink
by density puts the chart's worst contrast at the switch, 2.5:1, measured — and concluding that
capping *"keeps a single label colour above 4.5:1 everywhere, in both colour schemes."* True of
the count. The cell carries two labels. The repository's guard,
`test_every_confusion_cell_keeps_its_count_readable`, is correct and covers the same one; its
docstring carries the same singular.

*This is `0007` §5.0's governing rule from the inside: a page measured a reason and recorded it,
and the measurement reached one of the two things it licensed. The record's own class — a claim
wider than the measurement under it — arriving in a comment written to prevent it.*

**Why the index could not see it either.** `clause_1_composited` read CSS `opacity` and
`color-mix()`. Alpha reaches a pixel from **three** places and a data-driven one has nowhere to
live but the markup, because a stylesheet cannot hold a value per cell. So the clause whose
whole subject is *this page paints a value that is not the declared one* reported **1 usage** on
the one surface in the portfolio that composites per element; it now reports **9**, and no other
surface moved. S12b is that repair, with `data_driven_alpha.html` as the fixture of record cut
from the page at `6f908ec`, before it was fixed.

**What the S12b review found, and none of it was in the code.** Five claims wider than the
measurement under them, in a stage whose subject is a measurement nobody had taken:
`fill-opacity="0.000"` appears **once**, on the one empty cell of nine, and *nine* was the cell
count written as the zero count — beside a report that prints `9 usage(s)` for the same
surface, so there were two different nines to confuse. `.cell-text`'s dark figure read 5.24
where this document's own next paragraph says **5.21**. *Every* graphic hit under 1.3:1 was
called `--border` chart furniture; **24 of 32** are, and the other eight are shapes filled with
a page ground. The clause was said to read *one* of alpha's three routes where two other files
edited in the same commit say **two**. And a guard docstring named a mutation — *"zero times if
it were added only to the branch that pushes"* — that **does not redden it**: `<rect>` is not
void, so both spellings take the push branch and moving the collector inside it left all 502
tests green. A void-tag case now makes the claim true, and reddens.

*The pattern is one thing: a stage that reproduced every figure it took from an architecture
pass wrote five of its own that it had not. The measurements were checked; the sentences around
them were not.*

**Both halves were mutation-proven.** In the sibling: reverting the share to `--muted` reddens
the widened guard at 40% of the ramp with the ratio in the message — *and with the token
hardcoded back to `text` the same revert passes*, which is what makes reading it out of
`styles.css` the load-bearing half rather than a tidiness. In the index: five mutations, each
red on the guard that names it, including `check()` no longer passing the page — the wiring a
unit test on the clause cannot reach.

### 4.22 What closing S8b measured — one row, two questions, two answers

Three pull requests: `doc-extract` #15, `mlops-car-price` #25, `pl-jobs-lora` #18. Re-derived
from the trees before the stage, which is now this block's habit and twice its saving.

**The row said "all 12" and the measurement says 10** — and the two files that are clean are
clean because **S8a took them**, per `ADR-0007` D2. S8a's own row had been wrong upward, from 8
to 26; this one was wrong downward. The lesson is not the direction, it is that a scope figure
written before a stage and not re-derived at it has been wrong every time it has been checked.

| class | sites | what it is |
|---|---|---|
| own code | 12 | mostly `CLAUDE.md`'s opening line — `Portfolio project **P2**. A Python package for…` |
| cross-reference | 14 | `A3` meaning `car-price-ml` (7), `P2` meaning `ab-lab`, `P1` meaning `mlops-car-price` (2), `P3`/`P4` in `doc-extract` |
| **decoy** | **17** | `doc-extract`'s own `B0`–`B3` evaluation baselines, in `CLAUDE.md` and `src/doc_extract/eval/` |

**The row's framing — "a different audience and a different argument" — resolved both ways,
because it was two questions wearing one row.**

A cross-reference does not depend on who is reading. `A3` is a worse name for `car-price-ml`
than `car-price-ml` is, for a recruiter and a contributor alike, and five of the fourteen sites
already wrote the name *beside* the code — `` `car_price_ml` (project A3, pinned to…) ``,
`P1 mlops-car-price`, ``P3 `apply-scout` `` — so the code was carrying nothing the line did not
already have. Those went, on `ADR-0007` D5's argument applied one layer down.

An own code does. `CLAUDE.md`'s audience is whoever maintains twelve repositories, and the tier
in its opening line is what orients them; that is the file's whole purpose. Those stayed.

*One argument against keeping them was raised and not taken, and it is worth recording because
it is the sharper one: **the key to the codes lives in a private repository.** The tier tables
are in this index's `README.md`, so a contributor who is not the owner cannot decode `P2` any
more than a recruiter could — the same diagnosis as `0006` §2.3, put to a different reader. It
loses to the fact that `CLAUDE.md`'s actual audience today is the owner and the sessions working
for them, both of which have the key. If that stops being true, this is the row to reopen.*

**Untouched by construction**: `doc-extract`'s seventeen decoys, and `pl-jobs-lora`'s own `P4` in
`normalize.py` and `vocab.py`, where the code names this project inside its own source.

### 4.21 What closing S8a measured — zero, on a surface nobody can gate

Fourteen pull requests: twelve siblings (W1), one on the index (W3, `#104`) and one on the
profile repository (W4, `P0w3r223/P0w3r223` `#3`), plus two index commits for the design and the
W1/W2 record. Four GitHub About descriptions rewritten (W2), which no pull request can carry.

**The closing census, over every public layer at once, reads zero.** READMEs, published pages,
package docstrings, all twelve account descriptions, and the profile README — the last two being
surfaces no clause, test or `SURFACES` row reaches. All twelve surfaces read `clear` **from the
wire** after the pages deployed, and the conformance table never moved: the stage changed no
verdict, which is what a text stage should do.

**Three things the doing found that the design had not.**

1. **Two sibling guards go red on a correct edit, and that is the guard working.**
   `mlops-car-price` and `pl-jobs-lora` each exempted `\b[AP]\d\b` from their provenance check
   *and* asserted the exemption still fired. Deleting the codes kills the exemption, so each
   pull request deleted it in the same commit. `mlops`'s case was unambiguous **only because
   the cross-references were in scope**: its page held three such sites and all three went. Had
   `ADR-0007` D5 left them out, that guard would have stayed green over two surviving codes and
   the stage would have read as complete.
2. **A figure can be on a page and invisible to a grep of it.** `pl-review-sense`'s lead prints
   `p < 0.0001` as `p &lt; 0.0001`, so checking the About copy against the raw markup reported a
   figure as unsourced that the page prints. The check was made against parsed text instead.
   `0007` §5.0 has **no carrier on the account layer**, so that check was the only thing between
   it and a figure no artifact prints — and the near-miss is the argument for `0009` §7 row 11's
   provenance reader, not against it.
3. **L3's renumber cost nothing, for the reason §4.1's erratum predicted and not the one it
   first gave.** `pl-review-sense` `B4`→`B3` and `token-budget` `B5`→`B4` touched no published
   line, because W1 had already deleted the two lines that published those codes. The two rode
   in one change; taken separately they would have edited the same two lines twice.

**What the stage did not touch, and why.** The index keeps its codes: this repository is private
and its README is the taxonomy's home. `0003` §2's fourth layer — the index README — is handled
by L3 and H3 as *content*, not as a code sweep. And eight module-docstring sites stay with S8b
under `ADR-0007` D1's boundary, named there so nobody sweeps for them a third time.

*The stage's own instrument had to be corrected twice before it was right — once for counting a
phrase over a population defined by a code set, once for leaving one layer on the old instrument
while fixing the others. Both were caught by review, before any of the fourteen pull requests
existed. §4.20 is the record of that, and it is the more useful half of this stage.*

### 4.20 S8a's scope, re-derived before the stage rather than during it — and it grew by a layer

§4.7's precedent, applied a second time. The design is `ADR-0007`; what belongs here is the
measurement and what it corrects.

**The row's own figure holds exactly where it was measured, and the row's scope does not.** §4.11
re-derived the README half to eight and it reproduces to the line, 2026-09-09 — same eight files,
same eight line numbers. What §4.11 never asked is the other two layers, and `0003` §2's scope
table (line 31) had scoped **four**: *index README, GitHub About + topics, per-project READMEs,
live-site headers*.

Counted with `rg -noE '\b(A[1-3]|B[1-5]|P[1-5])\b'` over `*/README.md` and `*/docs/**/index.html`:

| layer | own code | cross-reference | sites | repositories |
|---|---|---|---|---|
| README | 8 | 6 | **14** | 9 |
| **published page** | 6 | 2 | **8** | 5 |
| **package docstring** | 2 | 2 | **4** | 3 |
| **committed** | **16** | **10** | **26** | **12** |
| GitHub About | 4 | — | **4** | 4 |

**Twenty-six committed sites, and every one of the twelve repositories publishes a code
somewhere.** The layer that was lost is the one §2.3's own argument reaches hardest: **three of the
six own-code page sites are in the `.eyebrow`, the page's first line** — `mini-traceroute:19`
(`Portfolio proof B1`), `ab-lab:146` (`Portfolio P2`) and `doc-extract:175` (`P5`) — and three more
sit in footers beside the gated clause-6 back-link. A stage that had taken the eight READMEs would
have left every one of them.

**Two About descriptions are worse than stale.** `pl-review-sense` publishes **`A4`** — and `A4` is
not a code in this portfolio at all, because Level A ends at `A3` (`README.md:25-27`) — while its
own README reads `B4`. §4.1's last paragraph predicted the contradiction and called it *live and
unscheduled*; what it did not have is that the published half names a tier position that does not
exist. And `pl-jobs-lora` opens its description with `P4:`, so the code is the **first two
characters** a reader meets on the repository card.

**Two corrections to the record, taken here rather than applied silently.** `0006` §3 H3 cites
index `README.md:44`, which is now the Level P table header — the `apply-scout` row is `:48` and
the claim repeats compressed at `:56`, so H3 is two sites. And `0003` §11 closed `0005` §9's
`apply-scout` row on the grounds that *"neither its README nor its `CLAUDE.md` says it"*, while the
package docstring still does, with the `(the flagship)` claim `0004` §5 withdrew — a row closed
against two layers of three, which is `0006` §3 H1's class.

**Erratum, in two rounds, both found by review before this stage's design was merged.** The first
draft of this section counted the page layer with the phrase `Portfolio (project|proof)` and
reported **four page sites in three repositories**, a union of thirteen, and `doc-extract` as
publishing no code publicly. The measured figures are eight, five, twenty-six and
`doc-extract/docs/index.html:175`. **Two** pages write the bare code with no word between —
`ab-lab:146` and `doc-extract:175` — and `ab-lab:146` is an **eyebrow**, the exact site-shape this
section uses to argue the page layer belongs in the stage. An edit taking only `ab-lab`'s footer
would have left the code in the page's first line with the repository's byte-diff guard green,
because that guard compares the page to a generator the same edit would have corrected.

*The second round corrected this erratum itself.* It first said **three** pages were bare and named
`ab-lab:439` among them; `:439` reads `Portfolio project P2` and the phrase census had found it.
And it left the **package layer** on the original instrument — a literal lookup for one string in
one known file — through the same commit that replaced the phrase census everywhere else, which
hid `doc-extract/src/doc_extract/__init__.py:1` and moved the union from 23 to 26. *A repair
applied to the layers that had already failed, and not to the layer nobody had checked.*

*A phrase census over a population defined by a code set. It is the same class as the defect the
stage exists to fix — a sweep that reads as complete because everything it found was real — and it
fails in the same direction as §4.13's three tallies of clause 8's write sites: too few, never too
many, because a wrong instrument omits silently and over-reports loudly.*

**A third correction the same error produced.** That version also asserted §4.11's false-positive
warning names `doc-extract/README.md:507-529` *"only"*. It does not: §4.11 also names `:211`,
`:520` and `:523`, and ends with *"Separately, `mlops-car-price/README.md` uses `A3` six times as a
live cross-reference"* — the class the census had dropped, already on the record. `ADR-0007` D5
now owns it, and it grew the stage by eight sites. What §4.11 does **not** name, and what belongs
to **S8b**, is that `doc-extract/CLAUDE.md` carries the same `B0`–`B3` baseline decoys its README
does.

*The pattern §4.7 and §4.13 both record repeats: the re-derivation cost one afternoon and moved the
figure on paper. Taking S8a as written would have moved it on the day, mid-stage, with eight pull
requests already open — and the erratum above is what a re-derivation costs when it is done with
the wrong instrument, which is one review rather than one stage.*

### 4.23 What S13's first commit measured — and three figures the design carried that did not survive it

§4.7's precedent applied a third time, to the one stage that was already designed. §3.11 took
S13's design before the stage; this is the re-derivation taken before the *work*, and it moved
the stage's shape before a line was written. `ADR-0008` is the decision; what belongs here is
what was measured and what the record had wrong.

**The instrument first, because two of the three findings below could not be had without it.**
S13's first commit adds an element stream to `render.py` — every element in document order with
its classes, its attributes and a pointer to its parent, plus an ancestor walk and the preceding
siblings under one parent. `paint_alphas` reads the same markup for one attribute and flattens
it, so it can say *this page composites somewhere* and cannot say *this cell is painted on that
rect*. That gap is the whole reason a rule-keyed contrast clause is wrong twice on one selector.

**Two standing figures became reproducible by an instrument on the day it landed.**

| figure | where it stood | measured |
|---|---|---|
| `0009` §4.19's scoping claim — 35 `<svg>`, **none inside an element carrying `card`** | a hand count no committed instrument could take; §4.19 says as much | **35 `<svg>`, 0 inside a `card`**, across six surfaces. Reproduces exactly |
| the population of `.ev-failed` sites on `auth-log-scan` | §3.11 works three of them and asserts a verdict for all | **139 marks, 133 of them with a preceding sibling of their own class**, in runs of 40, 16 and 12 |

**Finding 1 — `0009` §7 row 12's promotion argument has expired, and the row does not say so.**
It promotes itself as *"the only open row where a published page can harm a reader"*, and the
harm it names is §4.19's `pl-review-sense` `.cell-share` at 2.69:1. **S12 fixed it**:
`pl-review-sense/docs/index.html:189` reads `fill: var(--text)` and has since 2026-09-08. So S13
is a regression guard over a clean corpus. Worth building, and §3.1's promotion rule no longer
reaches it — which reopens its order against row 9, and row 9 is the one that grows while it
waits. *The row was promoted on a fact that its own neighbouring stage then closed, and the two
sections never met.*

**Finding 2 — §3.11's worked example does not survive §3.11's verdict rule.** The rule says a
site `PASS`es only by clearing **every** candidate ground, *"the ancestor chain and every
preceding painted sibling in the enclosing `<svg>`"*. Two marks of one class are the same
declared colour, so the candidate ratio between them is **1.00:1**, and 133 of the 139 marks
have such a sibling. Under the rule as written they are all `UNDECIDED`; §3.11 says they
`PASS` at 3.98:1, 3.79:1 and 3.09:1. **The figures are right** — all four reproduce from
`colour.py` as shipped, and the 1.27:1 one matches the comment `auth-log-scan`'s own stylesheet
carries — so the rule is what is wrong, and it is wrong in the direction this checker exists to
refuse: a confident `UNDECIDED` over 96 % of a conforming page. `ADR-0008` D1 takes containment
instead. **133 is a lower bound**; it counts only the siblings where the collapse is certain.

**Finding 3 — the obligation S13 would enforce is not in the normative slice.** `c1.s6` chooses
*which* threshold — 4.5 for a token painted as text, 3.0 for a mark. The sentence requiring a
usage site to **meet** it is not in `0007` §5; it is in §7, *What this spec does not check*,
which `tools.spec.NORMATIVE_TO` deliberately excludes from the range guard 1 searches. Building
S13 without amending §5 would put the checker ahead of its spec — the `data-scroll` shape from
the other side, and that one has been open since 2026-09-07. `ADR-0008` D4 is the amendment,
and its wording is deliberately deferred until the census prints, because the registry pins the
quote for as long as the sentence exists.

**Three errata, and one of them is this document's own.**

1. **`0008` §3.11 says `clauses.py` is `1 225` lines. It is 1 235** — S12's `paint_alphas` work,
   landed after the design was written. The sentence's point stands and is strengthened: the
   file is further over the 800 ceiling than the argument for a new module claimed. *This is the
   failure §4.13 and `0009` §8 row 1 both name — a figure typed into prose goes stale in
   silence — occurring in the section that was written to avoid it.*
2. **The re-derivation pass reported 1 236 for the same file**, having correctly found the
   record's figure stale. Neither number came from an instrument; `wc -l` says 1 235. Recorded
   because a pass that catches a hand count with a hand count has not caught it.
3. **§3.11's cost note is wrong in its own terms.** It says *"every leaf mark keeps its
   verdict"* under the sibling rule. On this corpus a leaf mark *is* a preceding sibling of the
   next leaf mark, so the note describes the case the corpus does not contain.

**What the mutation battery found, which is more than the guards it was written for.** Eight
mutations over the element stream, and the first run returned **7 of 8** plus one hang.

- **`handle_endtag` could stop popping the element stack with all six new guards green.** Every
  case they cover opens its elements before any of them closes, so the stack is never read
  after a pop and the mutation has nowhere to show. A closed element followed by a sibling is
  the commonest shape on every page in the corpus and had no test. `0008` records at least
  seven guards that shipped green over the defect they existed to catch; this is the eighth,
  and the first caught before shipping rather than after.
- **`ancestors()` hung rather than failing.** An element parenting itself — the first mutation
  the walk is written against — looped forever appending, to 9.7 GB before the process was
  killed. The walk is bounded by the element count now: a chain cannot be longer than the page,
  so the bound is a fact about the data and not a defensive check. **A guard that cannot be run
  is not a guard**, and a battery that its own subject can stop proves nothing.
- **The battery's `restore()` discarded an uncommitted fix mid-run.** `git checkout --` is how a
  mutation is undone and it does not distinguish the mutation from the work beside it. Already
  on the record; recorded again because knowing it did not prevent it.

*The measurement that says the stage moved no page: 526 tests green against 519 at entry, the
conformance table byte-identical, and `python -m tools.pagespec` still exits 0 on eleven
surfaces. No clause reads the stream yet, which is what the first commit of an instrument stage
should be able to say.*

### 4.24 What closing S13 measured — and the two sentences the stage falsified about its own checker

§4.23 recorded the first commit. This records the close, and it is written a day late: the row
in §3 read `in progress` from the merge of `#107` until this section was written, while the
stage's code sat on `main` and green. *A reader deciding what to take next reads §3.*

**What shipped.** Five modules rather than the one the row named — `render.Element` plus
`selector.py`, `geometry.py`, `paint.py` and `contrast.py` — with three keys `UNDECIDED`
**by construction**: `contrast.py` has no `PASS` and no `FAIL` branch at all, which is a
stronger claim than a policy and is guarded as one, by a test that reads the module's source
statically so S14 cannot add a verdict without going red. Both pins were edited
(`conftest.NOT_A_CLAUSE`, `spec.NOT_A_SENTENCE`), which `ADR-0008` §5 warned would ship green
if forgotten.

**The population it prints, over the eleven committed surfaces**, computed by the run and not
typed here from a hand count: **2 347 mark sites** (1 785 measured), **565 text sites** (552
measured), and **575 sites with no resolved ground**. That last figure is the census being
honest rather than the census failing: it is what the `contrast ground` key exists to say.

**Four readings the census refuted before a verdict could ship on any of them**, which is the
whole of `ADR-0008` §4's reason 2 and the best argument this record has for taking an
instrument before a rule. Each was a plausible reading held by the pass that wrote it, and
each was wrong on the corpus: `color` inherited to every element, which put **589** text sites
on `auth-log-scan` where the shipped census reads 43; a background counted as a mark, which
led six surfaces with a `<code>` background at 1.06:1; a ground's own alpha ignored, so
`pl-review-sense`'s cells read as full `--accent` and every label on one measured 1.00:1 — *on
the page that carried the real SC 1.4.3 failure S12 had just fixed*; and a sibling of a mark's
own colour scored at 1.00:1, which is §3.11's collapse, 133 of 139. **These four are a
development record and are not reproducible from the shipped code**, which is stated because
every other figure in this section is, and the difference matters to anyone auditing them.

**Three decisions taken by measurement rather than preference.** `_resolve_chain` stays in
`clauses.py` — all 238 palette tokens resolve in one hop, which `ADR-0008` §5 left open; two
rules declaring one alpha is `None` and not a product, on four elements of `auth-log-scan`;
and `#id` and `*` are refused by the matcher because no paint-carrying selector in the corpus
uses either. *These three figures, like the four above, were measured during the stage and no
run prints them; the 519 and the 576 below are the ones a reader can reproduce.*

**Two orphans closed, and the registry now reads two uncarried from four.** `c7.s1` — clause 7
reads `font-family` through the palette — and `c3.s3`, clause 3 honouring the `data-scroll`
escape it had been overruling. Of the two that remain, `c3.s2` is a recorded decision
(`ADR-0004` §4), so **the single genuinely open normative sentence is `c1.s6`, which is S14's**.

**And the stage falsified two sentences about the checker's own reach, in two documents, and
neither moved for a day.** `colour.resolve()` and `colour.composite()` had shipped unused
since S2; S13 calls both — `paint.py` resolves a declared value against the palette,
`contrast.py` composites a mark over its ground. Until this commit, `tools/spec.py`'s `c1.s6`
`why` said they *"ship unused; only `contrast()` is called"* — **printed by
`python -m tools.spec` on every run**, in the one field the registry prints so that an open
row cannot go stale unseen — and `CLAUDE.md`'s architecture block said the same thing one line
down while listing **six** modules against the ten on disk, omitting all four this stage added.
*This is the class `0009` §7 row 13b already named and this file already carries twice: a
sentence describing a partiality outliving the partiality it describes.* The registry field is
the sharper of the two, because it is the instrument reporting on itself.

**What the census then printed that blocks S14**, both measured and both recorded in the S14
row.

*A site's own painted background is not among its candidate grounds.* `_grounds` walks
`page.ancestors(element)`, which starts at `element.parent`, and then the preceding siblings
that contain the element — so an element that paints its **own** background is measured
against whatever is behind it instead. The two worst text readings in the portfolio are both
this shape:

| site | declared | ground the census used | ratio | what the button actually paints on |
|---|---|---|---|---|
| `mini-traceroute` `<button id="play">` | `color: var(--bg)` → `#ffffff` | `<body>` `#ffffff` | **1.00:1** | its own `background: var(--accent)` |
| `car-price-ml/app` `<button id="submit">` | `color: var(--bg)` → `#ffffff` | `<form>` `#f6f8fa` | **1.06:1** | its own `background: var(--accent)` |

**Neither is a page defect.** `#ffffff` on `--accent` `#2563eb` is **5.169:1**, and
`car-price-ml/docs/app/styles.css:225` carries the measurement in the page's own comment —
*"the same rule measures 5.17:1 light and 7.71:1 dark"* — written when a literal white was
replaced by the token for exactly this reason. The page measured its control and recorded why;
the census cannot see the ground because the ground is the element itself.

*The marks question, measured rather than guessed.* Every mark reading at or below 1.24:1 —
**153 readings across 152 sites**, the two figures differing because one site has two grounds
in that band:

| ratio | readings | site |
|---|---|---|
| **1.00:1** | 6 | `pl-review-sense` `<rect class="cell">` fill — heatmap cells whose `fill-opacity` *is* the datum |
| 1.04:1 | 9 | `auth-log-scan` `<line class="lane-line">` stroke |
| 1.06:1 | 8 | `auth-log-scan` `<rect class="lane">` fill |
| 1.16:1 | 4 | `car-price-ml` `<line class="grid">` stroke |
| 1.17:1 | 126 | `ab-lab`'s table borders (93), grid and axis strokes (21), `<code>` borders (3); **eight `<input>`/`<select>` borders** on `car-price-ml/app` and `mini-traceroute`; one `card caution` border |

So the D5 question is **not** about chart furniture. The worst readings are cells encoding a
value, and the 1.17:1 band contains user-interface component boundaries — which is the first
half of SC 1.4.11's own wording, not the second.

***Erratum, and it is this section's own.*** The paragraph above said, in its first version,
that both `<button>` readings *"are the absent cascade"* and that **S14 must cascade before it
can read its own census**. Both are false. Each of those two sites has `competing=1` — one rule
reaches it — so no cascade can move either number by a thousandth. The cascade is the right
diagnosis for `mini-traceroute`'s `#step` and `#reset`, which carry `.secondary`, report
`competing=2`, and are already reported `unresolved` with the census's own words — *"2 rules
reach it and the census has no cascade"* — which means **they never enter a `worst` figure at
all** and were never the sites being explained. The consequence is what makes this expensive
rather than untidy: the sentence pointed the next stage at a change that would have left both
numbers exactly where they are. *And the same paragraph called the worst remaining marks
"separators and gridlines" at `<li> border` 1.24:1 and `<line> stroke` 1.04:1 — a figure that
travelled out of `#107`'s commit message, through the stage's closing note, into two places
here, while the run printed `pl-review-sense … worst 1.00:1 at <rect> fill` on its own line the
whole time and this section's author had already read it.* Both were caught by the stage's
`code-reviewer` pass, which is what that pass is in the working rules for.

*The measurement that says the stage moved no page: **576 tests** collected at the merge
against 519 at the stage's own entry, `python -m tools.pagespec` exiting 0 on eleven surfaces
and on twelve with `--fetch`, all twelve reading `clear`, and the conformance table
byte-identical across the pointer bump that followed — captured by writing the table to a file
before and after and diffing it, rather than by reading it twice.*

### 4.25 S14's scope, re-derived from the census — and the row is not the stage it describes

§4.7's precedent, fifth application, and the first one where the instrument the previous stage
shipped is what does the deriving. `ADR-0008` §4's reason 2 said a census would decide these
questions *"with an instrument rather than with this document"*. It did, and it moved three of
them.

*Every figure in this section is the **eleven committed surfaces in the light palette**. `wroclaw` commits no HTML and is read only with `--fetch`; `contrast.py:89` takes `palettes(css).get("light", {})`. `GATE` covers twelve, so a marks or text key admitted on these figures is a light-scheme gate over eleven until something says otherwise.*

**Q1 — self-as-ground closes the two worst text readings and opens nothing.** 35 text sites
paint their own background; correcting the ground moves **17** ratios that already had one and
produces **zero** failures. *The definition matters and the first version did not give it:
counting every reading that changes gives **28**, because 11 `<body> color` sites have no
painted ancestor today and gain a first ground at 15.62:1, taking the measured text population
from 552 to 563. An implementer checking against 17 alone will see 28 and think they are
wrong.* The two the S14 row names go the right way and land exactly where the pages say they
should:

| site | census today | with the site's own ground |
|---|---|---|
| `mini-traceroute` `<button id="play">` | 1.00:1 | **5.17:1** |
| `car-price-ml/app` `<button id="submit">` | 1.06:1 | **5.17:1** |
| `car-price-ml` `<a>` ×6 | 5.17:1 | 4.85:1 — still clear of 4.5 |

`car-price-ml/docs/app/styles.css:225` predicted the 5.17 in prose two stages ago. **Text is
then clean across the eleven**: 2 of 552 measured sites read below 4.5:1 today and both are these
buttons, so the correction takes the text half to zero without touching a page.

***The trap this measurement walked into first, recorded because it produced a confident wrong
answer for one run.*** Reading a site's own ground through `_GROUND_PROPERTIES` as the module
holds it — `("background", "background-color", "fill")` — makes **every `<text>` element its
own ground**, because in SVG one property is a shape's paint *and* a text's foreground. That
version reported 704 moved ratios and **684 failures**, all of them `1.00:1`, and every one was
an artifact of asking whether a thing contrasts with itself. Two corrections fall out and both
are D6's substance: self-as-ground is a question about `color` over `background` and never
about `fill`; and **a border is a boundary, so its visibility comes from the colour on the
other side** — correcting `mini-traceroute`'s `<button> border` to its own background gives
1.00:1, which is the wrong comparison confidently computed.

**Q2 — the cascade population is 542 sites, and it is not where the row implies.** Sites
reporting `competing ≥ 2` with no ratio, by surface: `it-job-radar` 226, `pl-review-sense` 134,
`auth-log-scan` 70, `car-price-ml` 59, `doc-extract` 49, `car-price-ml/app` 2,
`mini-traceroute` 2. **525 of the 542 are `fill`** — chart marks reached by two rules — and 2
are `color`. So the cascade is a *marks* problem with a two-site text tail, where the row
describes it as the general prerequisite.

**Q3 — and this is what resizes the stage. Verdicts over marks, with no rule about which marks
are owed one, fail 1 195 of 1 785 measured sites**, across all eleven:

| class | sites | measured | below 3.0:1 | |
|---|---|---|---|---|
| CSS `border`/`outline` | 1 054 | 1 051 | **1 042** | 99 % of what is measured — table rules, card edges, `<h2>` top rules, `<pre>` borders. Three declare `border: none` and are not measured |
| `accent-color` | 3 | 3 | **0** | two range sliders and a checkbox, all 4.85:1 |
| SVG `fill`/`stroke` | 1 290 | 731 | **153** | 21 % of what is measured — the actual chart marks. The unmeasured 559 are `contrast ground`'s population |

*The first version of this table headed one column `measured` and printed 1 054 and 731 under
it — a site count beside a measured count — and reached 1 785 only by folding the three
`accent-color` sites into the border row, which is the wrong side of D5. Both are corrected
above.*

The arithmetic is right and the obligation is not: a light rule under a table row is
`--border` on white at 1.17:1, and SC 1.4.11 asks for 3:1 from *user-interface components* and
from *graphical objects required to understand the content* — a horizontal rule between two
rows of a table whose data is entirely text is neither. **So `ADR-0008` D5 is not a refinement
of the marks key; it is the question of whether that key can exist at all.** A `pending` row
admitted before D5 would demand its own promotion the first time a `live` run read it clean,
and it would never read clean.

**And inside that border population there is one the criterion does reach.** Twenty-three sites
sit on a control tag, and they are three different things: **17 `border`, of which 14 measure
below 3.0:1**; 3 `accent-color`, which are not a boundary and pass at 4.85:1; and 3 declaring
`border: none`, which are not measured at all. The fourteen divide:

- **Six `<a>` borders on `car-price-ml` at 1.24:1** — links rendered as cards. The link is
  identified by its text, so the border carries no information the criterion requires. *This is
  a judgement, and it is the one D5 claims not to need — `ADR-0008` §7 states it rather than
  leaving it here.*
- **Eight form controls at 1.17:1**, every one `1px solid var(--border)` → `#e3e7ee`:
  `car-price-ml/app`'s `#mark`, `#model`, `#year`, `#mileage`, `#vol_engine`, `#fuel` and
  `#province`, and `mini-traceroute`'s `#scenario`. **This is the boundary that says where the
  field is**, which is SC 1.4.11's own worked example.

***The eight is nine, and the ninth is why a scope taken from the census would have been
wrong.*** `mini-traceroute/docs/assets/styles.css:177` writes
`.field select, .field input[type="number"]` over one `border: 1px solid var(--border)`.
`paint.read_rules` splits the list and parses each half: `.field select` yields `#scenario`,
and **`.field input[type="number"]` comes back a `Refusal`** — an attribute selector this
matcher does not read. So `#base-port` (`mini-traceroute/docs/index.html:103`) carries the same
border at the same ratio and **is invisible to the census that found the other eight**. A
repair scoped to what the instrument printed would leave it failing *and the control population
reading clean* — the shape `CLAUDE.md` names, a guard green over the defect it exists to catch.
**The refused-selector list bounds the control count from below**, and that bound is recorded
beside D5.

***And every figure in this section is the light palette only.*** `contrast.py:89` reads
`palettes(css).get("light", {})`, so the census has one scheme, and neither this section's
first version nor `ADR-0008` §7's said so. The same controls measure **1.29:1 in dark** —
`--border` `#263041` on `--surface` `#161c25` — so they fail in both, and a repair sized from
1.17:1 alone would fix one scheme and leave the other. `car-price-ml/docs/app/styles.css`'s own
button comment records both schemes for exactly this reason, and the S12 row above says *"a
live SC 1.4.3 failure in both schemes"*. **The repair is a two-scheme repair.**

*One correction to the sentence this paragraph replaces: it called these "the same class of
live failure S12 found and fixed on `pl-review-sense`". The **procedural** precedent holds — a
sibling page repair scheduled from the index — but S12a was SC **1.4.3**, text contrast, and
these are SC **1.4.11**, non-text. This record is precise about criteria everywhere else.*

*That last group is the finding of this re-derivation.* It means S14 is not the regression
guard over a clean corpus that §4.23 and `ADR-0008` §4's reason 1 both assumed: **the corpus is
clean for text and is not clean for controls.**

**Both decisions were taken by the owner the same day, and they are `ADR-0008` §7.** D5 scopes
the marks obligation to user-interface component boundaries and SVG graphical objects, leaving
structural CSS borders outside it — the reading that makes the key a clause rather than a
portfolio-wide red. D6 makes a site's own opaque background **occlude** what is behind it, with
`fill` excluded and a border kept facing outward. **The nine controls are repaired** in both
schemes: a token for the control boundary, `--border` untouched elsewhere. That is two sibling
pull requests and a pointer bump, which this repository schedules and does not author — it
re-points submodules and does not edit them.

***And the repair does not land as a sibling stage, because this specification forbids it.***
Attempted on `mini-traceroute` — a `--border-control` token at 3.21:1 light and 3.19:1 dark,
applied to the one rule that styles `#scenario` and `#base-port` — the run came back
`FAIL 1 usage roles`, on a **gated** key:

```
1: .field select, .field input[type="number"] {border: var(--border-control)} — expected --border
```

`0007` §5 clause 1's fourth sentence gives a border exactly one house role, and
`_role_exception`'s four measured shapes are each a case where a border **stops being an
edge**: a rail thicker than a hairline, a filled control's *ground*, a border naming the role
its own background names, and an interaction state. **A control boundary is still the box's
edge** — that is what makes it the thing SC 1.4.11 asks about — so it takes none of the four,
and the only value clause 1 admits is `--border`, which measures 1.17:1.

**So two clauses of one specification now disagree.** Clause 1 says a border paints `--border`;
D5 says a control boundary must clear 3:1, and `--border` does not. The repair is not
unrepresentable in CSS, it is unrepresentable *in this spec* — which means **S14a is not a
sibling stage at all**. The order is: amend the index first (a fourth house role, `_BORDER_ROLES`,
`0007` §5 clause 1's fourth sentence and its registry pin, with guards and a mutation), then
the two sibling pull requests, then the pointer bump. Taken the other way round, a correct
page change reddens a gated clause and the bump goes red — `CLAUDE.md`'s trap arriving from the
side it does not describe.

*Two alternatives were measured and refused.* Changing `--border`'s own value portfolio-wide to
clear 3:1 repaints table rules and card edges on eleven surfaces to fix nine controls, and D5
had just decided those rules are owed nothing. Overriding `--border` inside the control rule
satisfies the role check by making one token mean two things, which is the opposite of what a
named role is for.

**What the repair does not do is make the marks key gateable, and the first version of this
section implied it would.** After the nine land, **153 SVG sites still measure below 3.0:1** —
`auth-log-scan` 101, `ab-lab` 23, `pl-review-sense` 19, `car-price-ml` 7, `it-job-radar` 3 —
and D5 puts SVG graphical objects *inside* the obligation. So §7's own argument against the
pre-D5 key, that it *"could never read clean"*, still reaches the post-D5 key. **The marks key
does not enter `GATE` at S14 in any state**, and what would change that is a further rule about
which of those 153 are required to understand the content — the escape D5 leaves available. The
text key is the one S14b can gate, and after D6 it is clean.

### 4.26 What S14a's index half amended — and the guard whose premise was wrong

§4.25 established that two clauses of one specification disagree, and that the index must
therefore be amended before either sibling moves. This is that amendment. **No page changed,
and the conformance table is byte-identical** — no surface declares `--border-control` yet, so
the eleven print `1 light --border-control n/a — not declared` twenty-two times and decide
nothing. `ADR-0008` §8 is the decision; this is what doing it measured.

**Three things the re-derivation carried that the row did not, all found before code was
written and all reproducing.**

1. **`c1.s4b`'s pinned quote is *falsified* by the amendment, and no guard could have caught
   it.** It read *"All four hold only where the role in question is not one of the **three**
   named above"*. A fourth house role makes that sentence false. Guard 1
   (`test_every_quote_is_still_the_document_s_own_words`) compares the registry's quote against
   `0007` and would catch the two files **disagreeing**; it cannot catch them **agreeing on a
   wrong count**. The replacement carries no count — *"not a house role named above"* — which
   is this repository's own lesson about typed figures applied prospectively for once, and it
   survives a sixth role.
2. **There is a third site saying "three", and it is the one nothing pins at all.**
   `clauses.py`'s comment over `_HOUSE_ROLES` read *"The three roles the fourth sentence
   assigns"*. The re-derivation named the registry quote and the document; the comment was
   found by reading the code the edit lands in. It now carries no count either, and says why.
3. **The census cannot see the dark half of the repair.** `contrast.py:89` takes
   `palettes(css).get("light", {})`, and `clause_1_tokens`'s `PINNED` loop is the **only**
   per-scheme value check in the instrument. A sibling declaring the token in its light
   `:root` and forgetting the dark override would ship a one-scheme repair with every guard
   green — on a stage whose own re-derivation closes by insisting *"the repair is a two-scheme
   repair"*. The token is pinned in both schemes for that reason and no other.

**The values, and the ground they are measured on.** `#808a9c` light and `#596a89` dark —
3.27:1 and 3.14:1 against `--surface`, 3.48:1 and 3.41:1 against `--bg`. `--surface` is the
binding side in both schemes and is the ground §4.25's 1.17:1 and 1.29:1 were read on. Both
surfaces that carry a control declare `--bg`, `--surface` and `--border` identically to the
byte, so one pinned pair serves both siblings. The margin is close to 3:1 on `--accent-soft`'s
precedent (3.12:1 and 3.30:1): a boundary is a boundary and not an emphasis.

**The finding of the doing, and it is about a guard rather than about the page.** The stage's
design specified sweeping all four `_role_exception` shapes with `--border-control` as a second
wrong role. **Three of the four then assert that a conforming declaration fails.**
`--border-control` on a `border-left` is admitted by `role in allowed` and never reaches
`_role_exception` at all, so the rail case demanded a `FAIL` the specification forbids. The
sweep's own comment already records that mistake being made once, one *shape* to the left —
*"using one role for both would have made half of this test assert that a conforming
declaration fails — it did, on the first run"* — and this was the same mistake one *role* to
the left. **Two of the four discriminate** — the shapes whose template declares a `background`:
the *filled control*, and *its own fill*, whose template writes a ground and a border together.
Both fire on `role not in _HOUSE_ROLES`, which is where widening `clause_1_usage`'s local
`allowed` instead of `_BORDER_ROLES` becomes observable. A border-only shape cannot tell the
difference at all. *This paragraph said "only the ground shape" and the sweep shipped one case
short of the corpus; the review measured all four and found it.* *A guard
whose premise is wrong fails on correct code, which is the cheap direction. The expensive
direction is a guard that passes over the defect it names, and running the mutation is what
tells them apart — reading the design did not.*

**Five mutations, five red, over a baseline.** M1 revert `_BORDER_ROLES`; M2 put the role in
`_GROUND_ROLES` instead; M3 widen the local `allowed` and leave `_BORDER_ROLES` at three; M4
drop the dark pin; M5 drift the `c1.s4c` quote from the document. The baseline pass — every
selector run unmutated, asserted green over a non-zero collection — is not ceremony: **M4's
first form reported `2 errors`, not a red guard**, because deleting the pin entry without its
comment line left `},` inside a comment. The battery called that UNCAUGHT rather than RED.
Checking the exit code alone would have scored a syntax error as a caught mutation, which is
the *"a guard that degrades to skip reads as caught"* trap arriving through a different door.

**What the stage did not do.** It repaired no page: the two sibling pull requests and the
pointer bump follow, and taken in the other order a correct page change reddens a gated key.
It did not touch `GATE` — `"1 "` is already `GATED_STATE`, `1 usage roles` stays clean
throughout, and both ratchet guards keep answering as they did. *That is worth stating because
`CLAUDE.md`'s eleven/twelve trap trains the reflex to add a `pending` row at every clause
change, and here there is nothing to add.*

**And one bound recorded rather than re-derived later.** §4.25 names `#base-port` as invisible
to the census because `.field input[type="number"]` is a refused selector. Reading the page for
this stage found a **second mechanism** with the same effect: `#speed` (`mini-traceroute`
`docs/index.html:120`, a `<select>` in `.transport`, not `.field`) and `#numeric` (`:107`, a
checkbox) carry **no author boundary at all** — no rule reaches them, so there is nothing for a
selector to refuse. After the repair, two controls on that page keep the user agent's boundary
while the other two carry the house token. Not a defect and not this repository's to fix, but
it belongs beside `ADR-0008` D5's bound instead of being found again by whoever reads the page
next.

**What the review found, and one of the six is why this stage existed at all.**

*The gate was refusing on an authority the document did not carry.* `1 light --border-control`
and `1 dark --border-control` are gated through `Ratchet("1 ", GATED_STATE)` and their detail
line reads `spec pins #808a9c` — but the values appeared in `ADR-0008` and in this section and
**nowhere in `0007`**, while `--accent-soft` and `--positive` have had their values, their
ratios and their rejected alternatives stated normatively since the clause was written. The
finest-matching carrier was therefore `c1.s5`, whose cite is *the two split values* and whose
subject is two other tokens, so a reader auditing the refusal was sent to the wrong sentence.
`0007` §5 clause 1 now states the pair, and `c1.s5b` carries it. **The gap was invisible from
the code and from the guards** — `tools/spec`'s ownership test passes either way, because the
prefix genuinely matched — and it becomes load-bearing at S14b rather than here: §5.0 lets a
page that measures and records its own reason win, and the two siblings are the first pages
this key can refuse.

*Two edits in the diff that no mutation reddened.* Drifting `PINNED["light"]["border-control"]`
left the whole suite green, and so did deleting the role from `COLOUR_ROLES`. The light pin is
the sharper of the two: the argument that earned the dark pin its guard — that no surface
declares this token, so unlike `--accent-soft` the corpus cannot stand in — reaches the light
value identically, and the light value is the one S14b's repairs meet first. Both now have an
assertion and both reddened on the drift.

*A count contradicted by the instrument, in the decision table later stages cite.* D7 and §8
said **fifth** house role. `_HOUSE_ROLES` has four members and `_BORDER_ROLES` gains its
second. The number came from the parallel construction one paragraph above it — *"a fifth
`_role_exception` shape"*, which is correct, there being four — and §4.25 had already carried
it here before the stage started. Corrected in all four places rather than in the two written
this session, because the origin is the one a reader reaches first. *In four of five: the S14
row of the plan table said it twice more and was missed — and that row is the origin this
sentence names. Found by the `code-reviewer` pass that closed the stage; corrected
2026-09-10.*

*And a repair that broke something, caught by a guard that was already there.* Printing the
pin's failure detail against both grounds — §4.25's figures bind on `--surface`, and the detail
named only `--bg`, so a value refused at 2.97:1 on the binding ground could print `3.16:1` in
its own refusal — was written to compute the ratios before checking that the declared value is
an opaque hex. `test_an_alpha_hex_token_is_reported_without_a_ratio_rather_than_crashing`
turned it from a crash into a failed assertion in one run. *The stage's own argument is that
only mutations can prove a guard here; this is the other half of it — the suite proving a
change, which is what a suite is for and what this section had no example of.*

*And the battery's `git checkout --` discarded uncommitted work for the second time in
two stages.* S13 recorded it; this stage re-ran the battery with the review's repairs still
uncommitted in the two files `restore()` reverts, and lost both — the `c1.s5b` row and the
two-ground detail. They were rewritten from the documents, which still referenced them, and
the tell was an anchor assertion failing in the battery rather than anything the suite said.
**A recorded trap is not a guard.** The battery would cost nothing to make safe — it could
refuse to run against a dirty tree in the paths it restores — and that is worth more than
this paragraph, which is the second one written instead.

### 4.27 What S14b measured, and the battery that refused to start

D4 held the obligation sentence back until the census had printed, *because `test_spec` pins
a quote from the moment the sentence exists*. This is what it printed, over the eleven
committed surfaces and after S14a's repair landed:

| population | sites | below its bar |
|---|---:|---:|
| text, at 4.5:1 | 565 | **0** |
| marks D5 obliges, at 3.0:1 | 1 298 | **153**, all SVG |
| sites D5 does not oblige | 1 049 | 1 034 would fail were they inside |

Both figures the ADR predicted reproduce exactly: §7 said D6 leaves zero text failures and
the S14 row said 153 SVG sites stay below 3.0:1. The third row is the one neither document
carried, and it is the argument for D5 in one number — **the obligation excludes more sites
than it covers, and almost every excluded site would fail.** A key without D5 is not a strict
clause, it is a broken one.

**D6 is a choice of word and the corpus decided it.** *Occludes* means the ground walk stops
at the element; *candidate* would mean appending to `found`, and `_measured` takes the
`min()`, so the covered ancestor would still supply the worst reading. Occluding moves 28
readings and leaves 0 failures; appending moves 18 and leaves 2 — and those two are the
published buttons the whole re-derivation rests on. The distinction is invisible in prose and
decisive in the output.

**The battery refused to start, and that is the finding worth carrying.** Nine mutations, and
on the first run every one of them reported `BASELINE BAD` — zero tests collected. The cause
was not the mutations: **`-q` suppresses the `N passed` summary line in this environment**, so
the regex reading it found nothing and scored a passing run as an empty one. Without §3.6's
first observation the same argv would have reported nine RED verdicts over nine empty runs,
which is `0008` §4's own recorded trap arriving by a new route. `docs/audit/0010` §3.6 had
been written four hours earlier and is what caught it. Re-run without `-q`: **nine of nine
RED**, each over a collected green baseline of exactly one test, each reddening the guard that
names it, each reverting clean.

**One inconsistency the guards found rather than the author.** Making the two keys carriers of
`c1.s6` and `c1.s6b` left them in `spec.NOT_A_SENTENCE`, which names the keys `0007` §5-§6
says nothing about — so the registry simultaneously claimed and disclaimed them.
`test_the_two_exemption_sets_answer_different_questions_and_say_so` is the guard, and it
asserts the *relationship* between the two sets rather than either as a literal, which is why
it survived both sets changing in this commit and still fired on the one change that was wrong.

**What the closing review changed, and the first of them is why the stage nearly shipped a red
morning.** `contrast text` was written into `GATE` as `pending`, on a reason whose second half —
*never yet read over the wire on all twelve* — was **already false when it was typed**. One
`python -m tools.pagespec --fetch`, the command `CLAUDE.md` recommends for exactly this, reads
`wroclaw-air-insights  clear` and the fetching ratchet guard then *demands* promotion:
*"the second refutation is a promotion to GATED_STATE, which is the whole reason the state
exists"*. §4.15 records this trap biting after a merge, with the morning's `live` run going red
on work that was green. **This is the first time it was caught before the merge instead**, and
the thing that caught it was running the scheduled job's own command rather than reasoning
about it. `contrast text` is gated.

**And `contrast marks` entered `REPORT_ONLY_STATE`, which this row said it would not.** The row
says *does not enter `GATE` in any state*, and its argument is entirely about `pending`: a state
refutable in both directions cannot be held by a key that can never read clean. That argument
does not reach report-only, which is not a prediction about the corpus but an explanation. What
settled it was reading the run: five surfaces print `FAIL  contrast marks` and the checker exits
0, and `gate policy` — the block whose whole purpose is *the keys the gate does not refuse on,
and why* — said nothing. A run that fails visibly and passes silently is the shape that block
exists to refuse.

**Three more the review found in the record rather than in the code**, all repaired before the
merge on §4.26's precedent: the `GATE` comment still claimed every key a clause can fail on is
gated and that the portfolio has zero `FAIL` — both false in the commit that made them so;
`CLAUDE.md` still described this module as having no verdict branch, and `served` as the only
row under `gate policy`; and `0009` §7 row 12 still read `open` while `tools/spec.py` printed
*closed at S14b* on every run. Two artifacts, one question, two answers, and one of them
printed.

**One live defect, and the guard beside it could not see it.** `gate policy` formats its rows
`f"  {one.prefix:<12}{one.state}"`, and `contrast marks` is fourteen characters — so the first
run after the row landed printed `contrast marksreport-only`. The guard asserts `one.prefix in
printed and one.state in printed`, and both substrings *were* present, inside one unreadable
word. The width is now taken from the data and the guard asserts the two are separated, which
is what it was always trying to say.

**Left open, deliberately, and recorded so it is a decision.** `Ground.guaranteed` distinguishes
a ground an ancestor structurally contains from one geometry merely places under the element,
and **no verdict path reads it** — `_verdict` takes `min()` across all grounds. The review
measured the cost: **79 of the 153 mark failures fail only against a non-guaranteed ground**,
and would pass against the ancestor that contains them. `test_contrast` has said since S13 that
*S14 needs it to tell a `FAIL` it can stand behind from one it cannot*, and S14b does not. Text
is untouched by this — **zero text sites have a non-guaranteed ground** — so the key that gates
is safe, and the key that does not is precisely the one whose reason now says why.

### 4.28 What D8 measured — and the axis the row named turned out to be the wrong one

`0009` §7 row 12's remainder, opened 2026-09-10 after S14b closed. §4.27 left `Ground.guaranteed`
unread by any verdict path and the `contrast marks` `GATE` row named that as one of two things
standing between the key and a gate. **The decision was not the one the row anticipated**, and
`ADR-0008` §9 is the argument; what follows is what the pass measured.

**The scope was re-derived from the census first — §4.7's precedent for the sixth time — and it
partitioned the problem into four rather than one.** Of 153 obligated mark failures: **79** fail
only against a ground geometry places, **48** are the gridline and axis strokes `ADR-0008` §7
already records D5 as admitting wrongly, **9** are the `rect.cell` heatmap fills §7 records as
D5's untaken escape, and **17** are the remainder. The row had been costed as one decision.

**The axis the row named does not track defect.** All 79 clear their *guaranteed* ground between
3.98:1 and 8.16:1, while the near-bar reading an author had to sweep for — `auth-log-scan`'s
marks, 3.09:1 by the page's own arithmetic and 3.24:1 by the checker's, `ADR-0008` §9's third
bound — and the only live failure
this checker has ever caught — `.cell-share` at 2.69:1, `0009` §7 row 12, repaired by S12 — are
both read on a geometric ground. **A verdict resting on guaranteed grounds alone would have
scored the pre-S7 page clean and would never have seen `.cell-share` at all.**

**What was excluded instead, and the defect it turned out to be.** 65 of the 79 are
`auth-log-scan`'s `circle.ev-failed` measured against another `circle.ev-failed`: one rule, one
declared `var(--accent)`, differing only by the `fill-opacity` the data writes per element.
`_grounds` has excluded a ground of the site's own colour since S13 and its docstring names this
exact population — but it compared the site's **un-composited** colour with the ground's
**composited** one, so one token at two alphas escaped. **The rule was aimed at these sites and
missed on a unit mismatch, for two stages.** 966 failing (site, ground) pairs, about fifteen
overlapping neighbours per site.

**Measured before and after at `1760f60`:** 153 → **88**; `auth-log-scan` 101 → 36 and the other
four surfaces unchanged; the 966 excluded pairs counted under `same_colour` and printed by
`contrast ground`, so nothing disappeared; `contrast text` **byte-identical** on the eleven and
`ok` on all twelve under `--fetch`. That last was predicted structurally rather than hoped for —
`geometry.bounds` answers only for `rect` and `circle`, so no HTML element can be a geometric
ground and `paint.TEXT` is `{color}` — and a run that disagreed would have been a finding about
the argument rather than about the corpus.

**The 14 D8 leaves failing are a second decision and are recorded rather than folded in.** Each
is a mark against a *different* mark — `rect.ev-invalid` on `circle.ev-failed` at 1.30:1 ten
times, `ab-lab`'s `rect.marker-corrected` on `circle.marker-naive` at 1.27:1 twice, and two
singletons. `auth-log-scan/styles.css:133` answers them — *"shape carries the meaning and colour
repeats it"* — but that is a claim about **role**, which is D5's subject, and D5 already carries
two recorded errors of that kind. `ADR-0008` §9 states why folding it in here would put a role
judgement inside a ground rule.

**Seven new guards and one corrected, six distinct mutations, each red on its own assertion** over a collected green baseline,
green again after revert. Two of the five exist specifically to redden if a later reader finds
filtering by `guaranteed` attractive: one pins `auth-log-scan`'s band at its pre-S7 opacities,
the other pins `.cell-share`'s shape. **A sixth guard's docstring was corrected rather than
deleted** — `test_an_ancestor_is_a_guaranteed_ground_and_a_sibling_is_not` said S14 needs the
field *"to tell a `FAIL` it can stand behind from one it cannot"*, and D8 answered that it does
not. *And the second of `ADR-0008` §9's two stated bounds was met while it was being written: a
first fixture painted `.cell-share` the same token as its cell, the exclusion reached it, and
the guard went red — correctly.*

### 4.29 The 17 that were called page work, and are not

Taken 2026-09-10 as the one item in the marks census that needed no design decision — the
remainder after D5's recorded gridline error and D5's untaken escape. **The scope re-derivation
found the item does not exist.** §4.7's precedent for the seventh time, and §4.25's shape: the
row's central assumption was false.

All 17 are `ADR-0008` D5's partition admitting a paint whose role is not the one D5 obliges, in
**three shapes**, and none is a defect any page should repair.

| n | site | declared | worst | shape |
|---|---|---|---|---|
| 8 | `auth-log-scan` `rect.lane` | `var(--surface)` | 1.06:1 | a background drawn in SVG |
| 6 | `pl-review-sense` `rect.track` | `var(--border)` | 1.24:1 | the quiet half of a two-property element |
| 2 | `auth-log-scan` `rect.window-band` | `var(--accent-soft)` | 1.27:1 | a wash |
| 1 | `pl-review-sense` `polygon.band` | `var(--accent)` | 1.25:1 | a wash |

**Shape one — a background drawn in SVG.** `--surface` is the panel token, `#f6f8fa` on
`#ffffff`, and `.chart .lane` is the row background of a swimlane chart (`build.py:115`,
`charts.Lane`). `contrast.sites` already refuses this exact role: *"A background is a **ground
and not a site**"*, and it excludes `paint.GROUND` for that reason. It cannot reach this one,
because **in SVG a background is a `fill`** — the same property a data mark uses. The census comment
that states the rule and the partition that misses it are **adjacent lines** in one module —
`contrast.py:141-145` and `:146`. *An earlier version of this sentence said eleven lines apart,
which is a hand count and is wrong in the direction that weakens its own point.*

**And that comment adjudicated this exact ratio already.** It continues: *"Counting them as
marks put `<code> background **1.06:1**` at the head of six surfaces — true, and about a code
chip sitting on a card, which is a **design choice rather than a finding**."* `--surface` on
`--bg` is 1.0647:1 whichever way it is spelled. The checker decided this ratio was not a
finding for the HTML spelling and reports it as one for the SVG spelling, which makes shape one
a citation rather than an argument.

**Shape two — the quiet half of a two-property element, and the page measured it first.**
`pl-review-sense/src/pl_review_sense/site/assets/styles.css:155` carries the author's own
reasoning: *"the ceiling has to be drawn, because '17' means nothing without the 20 behind it —
and a fill of `--border` alone is **1.24:1 against the page**, which draws it without making it
visible. **The outline carries the extent; the fill stays quiet** so the bar inside it keeps the
emphasis."* The figure is the checker's, arrived at independently. And the outline is
measurable: **`.track`'s `stroke: var(--muted)` reads 5.98:1 and passes**, on the same element,
in the same run. So the information a reader needs clears the bar by double, and the checker
fails the property beside it that was designed not to carry.

**This is the shape §7 does not have.** Its two recorded errors are both *which elements* D5
admits. This one is *which property of one element*: role can sit on a sibling declaration, and
a partition by property name cannot see that a `stroke` next door is doing the work.

**Shape three — a wash, and it splits in two.** Both are `fill` at low alpha, and only one of
them is exempt on its author's own reasoning.

*The two `rect.window-band` sites are adversarial to repair, measured.* This is the span
`auth-log-scan`'s marks are drawn on, and `styles.css:142` records its author sweeping that
band's opacity **downward** — 0.45 to 0.25, 0.28 to 0.15 — *so the marks composited on it would
clear 3:1*, with the swept table printed in the stylesheet. **Raising the band to 3:1 would
undo the repair S7 shipped.** *Four further `.window-band` sites, the `--danger` flagged
variant, are unmeasured — two rules declare the alpha and the census has no cascade — so they
sit under `contrast ground` and are neither in the 17 nor exempt.*

*The one `polygon.band` site is **obliged by role and its author says so**, and it is the
place this row's first version overreached.* `pl-review-sense/…/styles.css:141` reads: *"Series:
one line, its seed-to-seed spread as a band behind it. **The band is the honest half of the
figure — without it a bumpy curve reads as structure.**"* That is SC 1.4.11's own wording —
*required to understand the content* — written by the page. Calling it decorative was wrong.

**What is refuted is the repair by opacity, and it is refuted by arithmetic rather than by
analogy.** The band and the series line are one token: `fill: var(--accent); opacity: 0.16`
behind a 2px `var(--accent)` line. Today the band reads 1.25:1 against the page and the line
reads **4.13:1 on the band**. The band reaches 3.0:1 only at **alpha 0.70**, and at that alpha
the line it exists to support reads **1.71:1** on it — below the line's own 3:1. Darkening the
wash walks it toward the colour of the thing it sits behind, so the two obligations move in
opposite directions by construction.

**The outline route is open and is not taken here.** Shape two's own pattern — carry the
extent on `stroke` and let the fill stay quiet — ships eleven lines above `.band` in the same
stylesheet at 5.98:1. Whether an outlined confidence band reads as a hard boundary where the
data has none is a design question for that repository, not a measurement for this one. **So
one of the 17 is an open question rather than an exemption**, and it is recorded as such.

**What this leaves.** Of the 88 obligated mark failures surviving D8: **65** are D5's partition
error — 48 gridline and axis strokes §7 already records, plus these 17 — **9** are the
`rect.cell` heatmap fills §7 records as D5's untaken escape, and **14** are
mark-against-a-different-mark, which `ADR-0008` §9 leaves as its own decision. **Zero of these
17 is a page defect that this repository could name**, and one — the `polygon.band` above — is an
open question for its own repository rather than an exemption. *An earlier version of this
sentence said zero of the **88** are a page defect, which resolves in one clause, and in the
convenient direction, the role question §9 expressly declines to settle: "Deciding it here would
fold a role judgement into a ground rule." The 14 remain open.* The `contrast marks` key cannot
gate, and the share of that reason belonging to the pages is now much smaller than the census
first suggested.

*No page was edited and no pointer moved. The stage this row was going to be does not exist;
what exists instead is a D5 amendment, which is a design decision and is not taken here.*


### 4.30 D5's partition amended — the role is in the token, and 88 becomes 26

`ADR-0008` §10, taken 2026-09-10 on the measurement §4.29 left. §7 had recorded D5's
property-name approximation wrong in two shapes and §4.29 measured four, 65 sites in one
direction and 3 in the other. **The rule did not move**: `0007` §5 clause 1 still says which
roles are owed the ratio, and no sentence of §5 changed. The instrument stopped guessing role
from the property name and started reading it from the token — `c1.s4`'s ground, *a token is
used in the role it names*.

**The scope re-derivation is the whole argument, and it is one table.** Partitioning the 739
sites **D5's old partition obligated** by what each declares — under the rule this section
installs the obligated population is 680, and labelling the table with the new figure would
make its own arithmetic unreproducible:

| declared | fails | passes |
|---|---:|---:|
| `--border`, `--surface` | **62** | **0** |
| every semantic token | 26 | 651 |

**Zero passes.** The two structure tokens are never a legible mark on any of the twelve, because
they are never a mark: gridlines, axis rules, swimlane backgrounds, the quiet half of a track.
Exempting them is not a tolerance fitted to failures — it is the role rule read off the
declaration that states it. And the residue is *exactly* the recorded open set: **9** heatmap
cells, **14** mark-against-a-different-mark, **3** washes. Nothing was resolved by accident,
which is the test a partition change has to pass.

**Measured before and after at `3193803`.** 88 → **26**. `it-job-radar` goes clean — its three
were axis strokes — so **four of the eleven surfaces report the key rather than five**, and
`CLAUDE.md` carried that figure and was corrected in the same commit. Three `accent-color` sites
entered the obligation, all at 4.85:1: two range sliders and a checkbox, which D5 had excluded
while admitting gridlines. The exempt tail now breaks out **65 structure-paint sites** — 62 the
old partition reported as failures, 3 the checker never resolved a ground for.

**The half that cannot be checked, and what stands in for checking it.** `clause_1_usage`
applies the role rule to the ground and border families and deliberately not to `fill`/`stroke`,
so a genuine data mark painted `var(--border)` is exempted with nothing objecting. Nothing can
object. So the population is **printed on every run** and a reader who sees it move is seeing
the only signal there is — `c1.s4c`'s answer to the same shape one property to the left.

**Two things found beside the decision.** `0007` §5 clause 1's owed-by sentence — the one D5
approximates — **was carried by no `tools/spec.py` row**; `c1.s6b`'s note glossed it. It enters
as `c1.s6d`. That is the second normative sentence this project has found carried by nothing
after `0009` §3.2's three, and both were found by a pass that had to quote the sentence to do
something else. Separately, **SVG `<text>` is held to 3.0:1 and nothing records that as a
decision**: `paint.TEXT` is `{"color"}`, so a label at 3.5:1 passes the marks key and fails
SC 1.4.3. That is `c1.s6`'s subject, not D5's, and is recorded open rather than folded in.

**Nine guards, ten mutations, each red on its own assertion** over a collected green baseline,
green after revert. Two are synthetic by necessity — the `color-mix` subset test and the
`<text>` bound — because no committed surface can redden either, and the `<text>` one is what
makes putting `--bg` in the structure set safe. One existing fixture had to change and said so
by going red: `test_the_marks_row_says_how_many_are_below_their_threshold` drew its second
failure from a lane painted `--surface`, which this amendment exempts. **That is a guard over a
printed count doing exactly what it was written for.**


## 5. What is carried, not scheduled

| item | state |
|---|---|
| ~~**L5** — the deprecated `license` table form~~ | **Done, Sx, 2026-09-07.** Eleven repositories carry a PEP 639 expression; `mini-traceroute`'s exemption is structural and reaches **both** halves of the sweep, not only this one. setuptools names a date — 2027-Feb-18 — which this row never had. §4.14 |
| ~~**`Author:`** — 70 fields, ten repositories~~ | **Done, Sx, 2026-09-07.** The header form now returns zero portfolio-wide. What follows is the decision as it was taken, kept because it is the reasoning and not the instruction: not a decision to take but **a migration to finish**: the newest document in each self-disagreeing repository already carries the name. Recommend `Piotr Cząstkiewicz` throughout |
| **The profile fields** — `name`, `bio`, `email`, `blog`, `hireable`, social accounts | The user's own action. The token carries no `user` scope, so nothing here can write them |
| **L2** — action pinning | Answered `0006` §3: do not pin, and the answer does not cover a third-party action if one is ever introduced |
| **The quotation rule has no carrier on `README.md`** | §4.10 applied `0007` §5.0 to `docs/index.html` and found ten of twelve READMEs carrying a figure no artifact prints. The figures were repaired; **nothing detects the next one.** Only `ab-lab` generates and byte-guards README regions (`<!-- generated: -->` at `README.md:14, 45, 49, 92, 96`). Twelve of thirteen are hand-typed prose with no carrier — the same structural shape as §4.11's two clauses, and it wants the same answer, but a README figure-provenance reader is a larger build than a separator and should follow S9 rather than ride inside it |
| **The S-gate residuals — one of three still stands** | **Closed by `#83`** (`0009` §7 row 2): `sources.py` carries the exception's cause instead of discarding it under a bare `except`, and the third-party marker is `sources.THIRD_PARTY`, declared once beside the only code that writes it and **compared** rather than searched for — mutation-proven, changing its text is now a no-op. **Still open:** `_with_styles` decides *third party* by URL prefix (`http://`, `https://`, `//`) where `_unread_same_origin`'s docstring says *"exist on our side"*. On the eleven committed surfaces the two agree; on the fetch-only surface they do not, so an absolute same-host URL there would be exempted from the gate. S9 does not make it reachable — only a page that writes its own origin absolutely would |
| **`wroclaw`'s scroller has no house name** | After S7 every other committed surface scrolls its tables in `.table-wrap`; this one uses `table { display: block; overflow-x: auto }` under `max-width: 640px`, so clause 3 reports `undecided` and will keep doing so. Neither the S7 row nor `0007` §9 row 6 names it, and S8a/S8b are the text layers — so it is unscheduled rather than skipped, and recorded here so the next reader does not go looking for it in a stage. **Not folded into S10**: that stage is clause 4, and this is clause 3 |
| ~~**No submodule ignores `.claude/`, and this repository's own `.gitignore` says why that matters**~~ | **Done, 2026-09-09 — and this row went on saying otherwise until 2026-09-10.** Five sibling pull requests (`ab-lab` #21, `auth-log-scan` #13, `car-price-ml` #31, `it-job-radar` #36, `mini-traceroute` #9), then `7461e5f` (#108) bumping those five pointers. Measured 2026-09-10 with `git -C <repo> status --porcelain` over all twelve: **zero report `?? .claude/`**, and the ignore is scoped rather than blanket — `.claude/sessions/`, `.claude/settings.local.json`, and `.claude/worktrees/` in the two that hold them, with `.claude/settings.json` left trackable because it is reviewable configuration. *`#108`'s own commit message quotes this row back at it, and the row still read "W1 did not take it … each still reporting `?? .claude/`" a day later — a closed item that a reader planning work would have costed at five pull requests, in the file whose §1 forbids exactly that. Found 2026-09-10 by an entry-state pass that asked the trees rather than reading this line: the third time this row has been written, and the first time by an instrument.* What follows is the row as it stood, kept because the price it records is the finding and the fix is not. Found 2026-09-09 by a working-tree sweep. Five submodules hold an untracked `.claude/` containing `sessions`, `settings.local.json` and in two cases `worktrees` — **exactly the three paths this repository ignores at its root**, with a comment giving the reason: on any other checkout the first permission grant writes one, `git status` sees it, and a standing false finding appears in the instrument whose whole value is that a finding means something. It is reproducing one level down: `git status` reports five submodules as ` M` while `python -m tools.entry_state` reports the tree clean, and §6's own row tells a reader that a dirty submodule means the checker is reading pages nobody published. The two instruments disagree and the working tree is in fact clean. **This repository cannot fix it** — it re-points submodules and does not edit them — but **S8a's W1 opens a pull request in all twelve anyway**, so one `.gitignore` line rides at zero marginal cost. Not folded into the stage's scope, because S8a is the text layers and this is repository hygiene; recorded here so W1 can take it without re-deriving it. **W1 did not take it.** Fourteen pull requests went out on 2026-09-09 and the `.gitignore` line rode in none of them, so the item that cost nothing while a stage was open now costs five separate sibling pull requests. The five are `ab-lab`, `auth-log-scan`, `car-price-ml`, `it-job-radar` and `mini-traceroute`, each still reporting `?? .claude/`; the other seven already ignore it. Recorded as the price of a zero-cost rider nobody picked up, which is the second time this row has been written |

## 6. Assumptions to verify before each stage, not once

Stated because two architecture passes on this block have now asserted account-side or live-page facts they had
no means to check, and three of five such claims were false.

| assumption | how, and the trap |
|---|---|
| `wroclaw`'s live page carries what `main` says it carries | Fetch the live URL. It commits **no HTML** — `.gitignore:25` — so `reports/site/` is an untracked local build and reading it has produced a wrong answer that survived a session. **The lag is closed**: `refresh.yml` now also triggers on a push touching `src/**`, so a code change publishes itself — §4.5. Its `og:description` and back-link are live as of 2026-09-06 |
| The four About descriptions are still as recorded | `gh api` per repository; they are an account surface, not a file |
| ~~Ten of eleven pages are still served byte-identical to their committed file~~ **No longer an assumption** | **Discharged by an instrument, `#90`.** The `served` finding hashes the served markup against the committed file on every scheduled run, folding line endings on both sides. §4.14 records the first measurement — eleven of eleven, and the row's *ten* was wrong. **Two limits, stated because the row now reads as fully covered and is not**: only the markup is hashed, so the external same-origin sheets on `mini-traceroute` and `car-price-ml/app` are outside it; and the key is report-only, for the reasons in `__main__`'s `GATED` comment |
| The working tree is what the record assumes — no submodule on an unmerged branch, no uncommitted file | **Check before quoting the checker.** §4.10's round left twelve `CLAUDE.md` and eight `README.md` uncommitted across the submodules for an hour, and two submodules checked out on a fix branch, so `python -m tools.pagespec` was reading two pages nobody had published. *The row had itself lost the separator between its two cells and rendered as one — found 2026-09-07 while discharging it* |
| No pull request is open and all twelve pointers still match | **`git fetch` first, then** `gh pr list` per repository + `git submodule status`. *`origin/main` is a local file a session inherits, and nothing refreshes it on its own. Discharged from a stale ref 2026-09-07, an hour after `#77` merged, this row reports the index as unmerged with no pull request open — which is what `gh pr list` says once the PR is **closed**, and what `git log origin/main` says while the ref still predates it. Two passes reached that conclusion independently and neither was reading the repository. §4.12* |
