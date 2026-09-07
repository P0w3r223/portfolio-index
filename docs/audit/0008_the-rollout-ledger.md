# The rollout ledger

Date: 2026-09-05
Status: accepted
Author: Piotr Cząstkiewicz + Claude
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
| **S5** | **Clause 9 on `car-price-ml`** (`0007` row 3, other half) | 1 generated page + regeneration | 0.5 d | open — **taken inside the `car-price-ml` pass with S9b and S10's app title**, which regenerate the same page and edit three adjacent lines of `docs/app/index.html`; §4.13 |
| **S6** | **Back-link + card metadata** (`0007` row 4 = `0006` B5) | 9 repositories, 10 surfaces, measured at entry and reproducing the recorded scope exactly. Card metadata only where a surface had none — §4.3 | 1.5 d | **closed** — nine repositories on `main`, CI green **on `main`**. Clause 6 passes on all eleven committed surfaces; §4.3 says what was deliberately left |
| **S7** | **Naming, the pinned values where nothing paints them, and two live SC 1.4.11 repairs** (`0007` row 6, plus §3.2's two carried items) | **Nine repositories** — the row named four items and one set; the stage re-derived it to nine, §4.6 | 1.5 d | **closed** — nine repositories on `main`, CI green **on `main`**. Clauses 2 and 3 now pass on every committed surface |
| **S-gate** | **Make the checker able to fail**, by clause. A ratchet: gate on the set reporting zero `FAIL` across every surface read, and extend it by one clause as each stage closes | `tools/pagespec/__main__.py`, `.github/workflows/pagespec.yml`, the two tests that pin the exit code, **and `ADR-0004` §6** — the normative home, which still read *"report-only first"*. **No page changes** — §4.11 | 0.5 d | **closed** — `current_projects` `297e3c5` on `main` with CI green **on `main`**. *The first version of this cell cited `043bf72` + `38f26a9`, which are branch commits: this repository squash-merges, so neither is reachable from `main` and neither ever will be — §4.12's last paragraph.* **Fifteen** mutations — twelve red on the guard that names them, one red on nothing in this repository by design (row 8), and **two that reddened nothing at all** until a later pass found the guard absent or out of reach (rows 9 and 15). **Four review passes**, the last three finding fixes that displaced a defect rather than removing it; §4.12 |
| **S9** | **The separator** (clause 8), scoped by formatter rather than by page. **S9a** four repositories, **not build-only in two of them** · **S9b** `car-price-ml`, both surfaces · **S9c** `doc-extract`, a spec amendment and not an edit | **20 non-conforming write sites in 14 files across five repositories and six surfaces**; 7 failing surfaces. *The count is not re-typed again — §4.13 routes the census into the checker's output, and that is S9's first commit* | **2–2.5 d** | open — **first commit prints the census; the commit that changes `wroclaw`'s separator widens `test_report.py:1524` in the same change**, §4.13 |
| **S10** | **Clause 4's `<title>` half** — `auth-log-scan` mechanical; `mini-traceroute`, `car-price-ml/app` and `wroclaw` copy decisions. Folds in the guard defect §4.11 records, **which is what makes it four rather than three** | **4 surfaces** · 1 guard | 0.5 d + copy | open — the `car-price-ml/app` title is `docs/app/index.html:6` and rides with S9b's `:7` and `:27`; §4.13 |
| **S8a** | **The text layers, public half** — the four About codes and their README twins, L3, H3, `pl-review-sense` C3 | **8 READMEs** publish a code, not ≥6 — §4.11 | 1.5–2 d | open, blocked on L3 |
| **S8b** | **The text layers, contributor half** — the portfolio code in `CLAUDE.md` | **all 12**, not 5. A different audience and a different argument — §4.11 | 0.5 d | open |
| **Sx** | **L5 + the `Author:` finish**, as one sweep on the L1 pattern | 11 `pyproject.toml`; 70 fields / 10 repos. **Both reproduce to the field, 2026-09-07** | 0.5 d | open — **the only open item depending on no gate, no clause and no other stage**; §4.13 |

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

## 5. What is carried, not scheduled

| item | state |
|---|---|
| **L5** — the deprecated `license` table form | **eleven** repositories (§2.1). Take it as one sweep with SHAs, the way L1 went; record `mini-traceroute`'s structural exemption |
| **`Author:`** — 70 fields, ten repositories | Not a decision to take but **a migration to finish**: the newest document in each self-disagreeing repository already carries the name. Recommend `Piotr Cząstkiewicz` throughout, and do **not** retroactively add `+ Claude` — co-authorship is unknowable per document at this distance, and saying so is more honest than guessing |
| **The profile fields** — `name`, `bio`, `email`, `blog`, `hireable`, social accounts | The user's own action. The token carries no `user` scope, so nothing here can write them |
| **L2** — action pinning | Answered `0006` §3: do not pin, and the answer does not cover a third-party action if one is ever introduced |
| **The quotation rule has no carrier on `README.md`** | §4.10 applied `0007` §5.0 to `docs/index.html` and found ten of twelve READMEs carrying a figure no artifact prints. The figures were repaired; **nothing detects the next one.** Only `ab-lab` generates and byte-guards README regions (`<!-- generated: -->` at `README.md:14, 45, 49, 92, 96`). Twelve of thirteen are hand-typed prose with no carrier — the same structural shape as §4.11's two clauses, and it wants the same answer, but a README figure-provenance reader is a larger build than a separator and should follow S9 rather than ride inside it |
| **Three residuals from S-gate's fourth review** | Not blocking, and none is live on a committed surface today. `sources.py:141` files an unreadable stylesheet under `except Exception` and discards the cause — on a path that now **gates daily**, so a rename, a permission error and a 404 arrive as one line. `_with_styles` decides *third party* by URL prefix (`http://`, `https://`, `//`) where `_unread_same_origin`'s docstring says *"exist on our side"*: on the eleven committed surfaces the two agree, on the fetch-only surface they do not, so an absolute same-host URL there would be exempted from the gate. And the marker `" (third party, not read)"` is still prose built in one module and matched in two others — the `split(", ")` defect §4.12 records, moved rather than removed. **S9 makes the first two reachable**: it edits generators in five repositories, and `car-price-ml/app` is hand-written |
| **`wroclaw`'s scroller has no house name** | After S7 every other committed surface scrolls its tables in `.table-wrap`; this one uses `table { display: block; overflow-x: auto }` under `max-width: 640px`, so clause 3 reports `undecided` and will keep doing so. Neither the S7 row nor `0007` §9 row 6 names it, and S8a/S8b are the text layers — so it is unscheduled rather than skipped, and recorded here so the next reader does not go looking for it in a stage. **Not folded into S10**: that stage is clause 4, and this is clause 3 |

## 6. Assumptions to verify before each stage, not once

Stated because two architecture passes on this block have now asserted account-side or live-page facts they had
no means to check, and three of five such claims were false.

| assumption | how, and the trap |
|---|---|
| `wroclaw`'s live page carries what `main` says it carries | Fetch the live URL. It commits **no HTML** — `.gitignore:25` — so `reports/site/` is an untracked local build and reading it has produced a wrong answer that survived a session. **The lag is closed**: `refresh.yml` now also triggers on a push touching `src/**`, so a code change publishes itself — §4.5. Its `og:description` and back-link are live as of 2026-09-06 |
| The four About descriptions are still as recorded | `gh api` per repository; they are an account surface, not a file |
| Ten of eleven pages are still served byte-identical to their committed file | Hash the fetched bytes against the file (`0007` §2) |
| The working tree is what the record assumes — no submodule on an unmerged branch, no uncommitted file | **Check before quoting the checker.** §4.10's round left twelve `CLAUDE.md` and eight `README.md` uncommitted across the submodules for an hour, and two submodules checked out on a fix branch, so `python -m tools.pagespec` was reading two pages nobody had published. *The row had itself lost the separator between its two cells and rendered as one — found 2026-09-07 while discharging it* |
| No pull request is open and all twelve pointers still match | **`git fetch` first, then** `gh pr list` per repository + `git submodule status`. *`origin/main` is a local file a session inherits, and nothing refreshes it on its own. Discharged from a stale ref 2026-09-07, an hour after `#77` merged, this row reports the index as unmerged with no pull request open — which is what `gh pr list` says once the PR is **closed**, and what `git log origin/main` says while the ref still predates it. Two passes reached that conclusion independently and neither was reading the repository. §4.12* |
