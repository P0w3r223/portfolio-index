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
| *"62 `Author: P0w3r223` fields across nine repositories"* | **70 fields across ten.** The count omitted the index itself, which holds 8 — and the index is where `0003`–`0005` live. Both self-disagreeing repositories are already half-migrated: `apply-scout` 10 handle / 2 name, the index 8 / 2 |
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
| **S4** | **`mlops-car-price` + `pl-jobs-lora`** (`0007` row 2 = `0006` B4), with clause 9's `mlops` half in the same pass. **`pl-jobs-lora` gets a committed artifact first** — §5 | 2 hand-written pages, plus one generator or table that does not exist yet | 2–3 d | **open, and larger than recorded** |
| **S5** | **Clause 9 on `car-price-ml`** (`0007` row 3, other half) | 1 generated page + regeneration | 0.5 d | open |
| **S6** | **Back-link + card metadata** (`0007` row 4 = `0006` B5) | **9 repositories once S3 lands** — the back-link is what they need; `apply-scout` was the tenth and needed card metadata only, which S3 supplies. By *surface* it is ten, because `car-price-ml/docs/app/index.html` is a second published surface with neither. **Plus that surface's `button { color: #ffffff }`** — the one live defect the new literals clause found, §3.7 | 1.5 d | **next.** The one remaining stage with no unresolved decision and no unbuilt mechanism, and the one S3 unblocks by name |
| **S7** | **Naming, and `mini-traceroute`'s unwrapped `<figure>` table** (`0007` row 6) | `.tile`/`.stat`→`.kpi`, `.scroll`/`.ledger-wrap`/`.tablewrap`→`.table-wrap`, `--ink`/`--line`, `wroclaw`'s two absent tokens | 1.5 d | open |
| **S8** | **The text layers** (`0006` B6) — the four About codes **and their committed README twins**, L3, H3, `pl-review-sense` C3 | 4 About + ≥6 READMEs + 5 `CLAUDE.md` | 2–3 d | open |
| **Sx** | **L5 + the `Author:` finish**, as one sweep on the L1 pattern | 11 `pyproject.toml`; 70 fields / 10 repos | 0.5 d | open, schedulable anywhere |

Roughly **13–14 days**. S0–S2 are one unit; everything after S3 is schedulable separately, and S8 is last
because it is the one that can slip without blocking anything.

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

### 3.6 S3 was written and was not done — the defect it fixes was unguarded by both carriers

**Recorded as a blocker rather than as progress**, because the page and the checker both report it clean.

S3's substantive fix was a token migrated **by value instead of by role**: `#eef1f6` carried two roles on that
page, and the table separator was mapped to `--surface` where six sibling pages use `--border`. That is fixed.
What is not fixed is that **nothing detects it coming back**. Reintroducing exactly that line leaves
`apply-scout`'s 298 tests green and the checker reporting the page `clear`.

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

*The extraction was checked the way `0007` §3.5 checked the whole checker: `palettes()` after the
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
`ADR-0004` §6 gives: its ceiling is the seven repositories with a page test, and the four that
cannot see the rule are exactly `mini-traceroute`, `mlops-car-price`, `pl-jobs-lora` and
`wroclaw`. It is kept as the second carrier, not as the only one.

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

### 4.1 The consequence that makes S8 cheaper rather than harder

Removing B3 renumbers the tier: B4 → B3, B5 → B4. Those codes are published — in four GitHub About descriptions
*and* in the committed READMEs behind them (`auth-log-scan/README.md:11`, `mini-traceroute/README.md:13`,
`pl-review-sense/README.md:8`, `pl-jobs-lora/README.md:6`). Renumbering them across two surfaces each would be
work created by the fix.

**Measured, the renumbering costs nothing — and that is not the reason to remove the codes.** The two rows that
move are `pl-review-sense` (B4→B3) and `token-budget` (B5→B4), and **neither publishes its current B-code**:
`pl-review-sense/README.md:8` publishes `A4` and `token-budget/README.md:6` publishes `A6` — both stale codes
from before their demotion. `mini-traceroute` (B1) and `auth-log-scan` (B2) sit *above* the removed row and do
not move at all. So renumbering touches zero published surfaces.

*A first draft of this section argued the opposite — that keeping the codes would force a renumber across two
surfaces each, and so that L3 decided the other way would double S8. It cited four README lines that each
refute it. Corrected by review; the four precise references were what made an unmeasured cost case read as a
measured one.*

**The codes still come off the public surfaces, on the argument that was always sufficient:** `0006` §2.3's
finding that a recruiter cannot decode them, and that two repositories publish a code the index contradicts.
What L3 settles is narrower than a cost — it is *which* ranking the index holds once B3 is no longer a row,
and S8 cannot rewrite an opening line without knowing that.

### 4.2 S4's copy decision was taken, and it grew the stage

`0007` §5.1 records that `pl-jobs-lora` has **no tiles, no generator and no committed table to quote**, so a
tile mandate would make it print a figure no artifact produces — which this portfolio's own standard forbids.
Three ways out were put to the user: an honest headline about the baselines measured before the fine-tune
exists; dropping `pl-jobs-lora` from S4 and taking `mlops-car-price` alone; or **building the artifact first**.

**The user chose to build the artifact.** So S4 is no longer two page rewrites: it is one page rewrite
(`mlops-car-price`, the cheap case — its `examples/` scripts already regenerate its README tables) plus a
generator or committed table in `pl-jobs-lora` that does not exist today, and *then* its page. The estimate
moves from 1.5–2 days to 2–3, and the scope is stated here rather than discovered in the stage.

*This is the one option that removes the exception instead of recording it. §5.1's fallback exists because
two repositories cannot source a figure; after S4 only one of them cannot, and §5.1 should be re-read at that
point rather than left standing as though nothing changed.*

## 5. What is carried, not scheduled

| item | state |
|---|---|
| **L5** — the deprecated `license` table form | **eleven** repositories (§2.1). Take it as one sweep with SHAs, the way L1 went; record `mini-traceroute`'s structural exemption |
| **`Author:`** — 70 fields, ten repositories | Not a decision to take but **a migration to finish**: the newest document in each self-disagreeing repository already carries the name. Recommend `Piotr Cząstkiewicz` throughout |
| **The profile fields** — `name`, `bio`, `email`, `blog`, `hireable`, social accounts | The user's own action. The token carries no `user` scope, so nothing here can write them |
| **L2** — action pinning | Answered `0006` §3: do not pin, and the answer does not cover a third-party action if one is ever introduced |

## 6. Assumptions to verify before each stage, not once

Stated because two architecture passes on this block have now asserted account-side or live-page facts they had
no means to check, and three of five such claims were false.

| assumption | how, and the trap |
|---|---|
| `wroclaw`'s live page still carries the row `0007` §4.3 describes, and still lacks `og:description` | Fetch the live URL. It commits **no HTML** — `.gitignore:25` — so `reports/site/` is an untracked local build and reading it has produced a wrong answer that survived a session |
| The four About descriptions are still as recorded | `gh api` per repository; they are an account surface, not a file |
| Ten of eleven pages are still served byte-identical to their committed file | Hash the fetched bytes against the file (`0007` §2) |
| No pull request is open and all twelve pointers still match | `gh pr list` per repository + `git submodule status` |
