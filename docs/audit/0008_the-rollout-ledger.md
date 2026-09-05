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
| **S2** | **The checker**, report mode, over all twelve. Static core composed from the two halves of `ADR-0004` §2.1; geometry by invoking `measure_page.py` | one module in the index | 1.5–2 d | **next** |
| **S3** | **`apply-scout`** (`0007` row 1) — tokens, dark override, card metadata, `.table-wrap`, drop Inter | 1 hand-written page, constrained by `tests/test_docs_page.py` | 1 d | open |
| **S4** | **`mlops-car-price` + `pl-jobs-lora`** (`0007` row 2 = `0006` B4), with clause 9's `mlops` half in the same pass | 2 hand-written pages | 1.5–2 d | open |
| **S5** | **Clause 9 on `car-price-ml`** (`0007` row 3, other half) | 1 generated page + regeneration | 0.5 d | open |
| **S6** | **Back-link + card metadata** (`0007` row 4 = `0006` B5) | **10 repositories** — nine need the back-link, `apply-scout` needs card metadata only. By *surface* it is eleven, because `car-price-ml/docs/app/index.html` is a second published surface with neither | 1.5 d | open |
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
