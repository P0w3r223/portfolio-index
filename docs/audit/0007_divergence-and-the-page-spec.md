# The divergence, measured — and the page spec it turns out to describe

Date: 2026-09-04
Status: accepted in part — §5, §5.1 and §6's clause 9 are normative; §9 and §5.2 are superseded; every other section is frozen at its 2026-09-04 measurement. **§5 clause 1 amended 2026-09-05** with the role sentence — see the note below
Author: Piotr Cząstkiewicz + Claude
Related to: [0006_session3-4-presentation-block.md](0006_session3-4-presentation-block.md) B2 and B3,
[0003_portfolio-review-plan.md](0003_portfolio-review-plan.md) §3 (Session 4) and §4 (the two families),
[0004_session1-recruiter-triage.md](0004_session1-recruiter-triage.md) §3.2, §6.4, §6.5,
`apply-scout/docs/decisions/0012_the_page_quotes_the_artifacts.md`,
[`../adr/0004_what-carries-the-page-spec.md`](../adr/0004_what-carries-the-page-spec.md) (the carrier, which
supersedes §5.2), [`0008_the-rollout-ledger.md`](0008_the-rollout-ledger.md) (the plan, which supersedes §9)

---

> **This document was split on 2026-09-05, and the split is the point.** It mixed three things with three
> different lifetimes, and every one of the ~26 corrections in §8–§8.5 landed in the perishable two while the
> normative part stood untouched. **A document that states measurements cannot be accepted without freezing
> them; a document that states rules can.** So: **§5, §5.1 and §6's clause 9 are accepted as normative** and are
> the part later work quotes. **§3 and §3.1 are frozen** as measured 2026-09-04 — they are a photograph, not a
> live table, and the checker of [`ADR-0004`](../adr/0004_what-carries-the-page-spec.md) takes that role at S2.
> **§9 is superseded** by [`0008`](0008_the-rollout-ledger.md), which also corrects its row-5 scope and moves
> that row first. §5.2's carrier is superseded by `ADR-0004`.
>
> **And everything else here is frozen with §3, for the same reason.** §1, §2, §4, §7 and §8 were left
> un-dispositioned by the first pass of this split — caught by review — which mattered because §1 and §4 are
> not narrative: they carry counts (*"**eight** hold it in named CSS custom properties"*, *"six pages have
> something to change"*) taken on the same day and ageing the same way. Treat every section but §5, §5.1 and
> §6 as a photograph dated 2026-09-04. §8's correction log stays as it is: a record of what was wrong is not
> a measurement that can go stale.
>
> **§5 clause 1 was amended on 2026-09-05, and the amendment is what the split permits.** A document
> stating rules can be accepted, and an accepted rule can be amended; that is the whole distinction this
> split turns on. The added sentence — *a token is used in the role it names* — was already being enforced
> in one repository's source comment and by nothing else, and `0008` §3.6 records what that cost. The
> alternative was a rule living in the checker's code with no normative document stating it, which is this
> record's own signature failure inverted. The sentence is written as a **description with its exceptions
> counted**, in §5's stated method, so it can be re-derived from the repositories rather than believed.

---

## 1. What this is

`0003` §3 commissions Session 4 as *a divergence table across all 12 pages, at desktop and at 375 px, and
one design spec covering layout, typography, KPI tiles and table overflow*. This document is both, because
the measurement turned out to answer the spec rather than merely to motivate it.

**The finding that decides the shape of everything below: there is nothing to invent.** A single design
system is already implemented across **all eleven** published pages. **Eight** hold it in named CSS custom
properties; three hold the same values as hand-typed literals and have drifted on three roles. The spec's
job is therefore to *name what exists*, reconcile the naming variants inside it, and move three pages onto
it — not to choose a house style. Six pages have something to change, and only some of it is naming: one
of the six carries a live WCAG failure (§9 row 5) and one a table with no scroller at all (§9 row 6).
*Re-scoped 2026-09-05: **three** of the six carry a live WCAG AA failure, not one — `mini-traceroute` fails the
text criterion and `car-price-ml` and `auth-log-scan` fail the 3:1 non-text one on a mark they paint. See
[`0008`](0008_the-rollout-ledger.md) §2.2.*

**And the rule for resolving a divergence is not the majority.** Of the ten house tokens, eight hold one
value everywhere and two do not — and **both** of those splits are **measured accessibility fixes** that
reached some pages and not others, each with its contrast ratio written in the source beside it. A spec that
unified on the count would revert it. So: *where a page has measured a reason and recorded it, that value
wins; the majority decides only where nobody measured.* §5 is built on that, and §4.1 is why.

## 2. Method, and the two ways every earlier attempt was wrong

Both failures were real, both produced a wrong answer that survived, and both are the same mistake:
**answering a question about the rendered page from something that is not the rendered page.**

**Reading `index.html` and calling it the page.** `0004` §6.5 recorded `mini-traceroute` as *"two tables
and zero wrappers"* and bound that to this spec so it could not be lost. It is the one page in the
portfolio whose CSS is not inlined — `docs/assets/styles.css` carries `.scroll-x { overflow-x: auto }` at
line 125 and `.ledger-wrap { … overflow: auto }` at 248. Every check, across three sessions and including
the first pass of this one, grepped the HTML. **Every CSS answer in §3 is therefore read from inline
`<style>` plus any same-origin external stylesheet.**

**Trusting the instrument.** `measure_page.py` decided whether a wide table was acceptable by reading one
HTML attribute that only `wroclaw-air-insights` sets. Pointed at the eleven pages it called **seventeen**
wide tables defects, and every one of them was already inside a box that scrolls. Generalised to walk the
DOM for a scrolling ancestor, it was then reviewed and blocked twice more: it walked past a clipping box
(naming an outer scroller with nothing left to scroll), and — starting at the table's *parent* — it could
not see `wroclaw`'s own rule, which makes the table itself the scroller at phone widths. Both were
demonstrated on fixtures before being fixed. The instrument used for §3 starts at the table, stops at a
clipping box, requires the box it names to have somewhere to scroll, and stops at the card.

**And this document did it a third time, in its own first draft.** The `wroclaw` row of §3 was read off
an untracked local build of `reports/site/index.html` while §7 asserted it had been taken from the live URL. It had not.
That page is rebuilt daily and was restyled by `wroclaw-air-insights#27` on 2026-08-20, so the committed
artifact is three weeks behind its own site — and the row was wrong on six columns, in the direction that
made the divergence look worse than it is. Caught by review, not by me, and left visible in §8 rather than
quietly corrected, because it is the same mistake as the other two: **a question about the published page,
answered from a file.**

Freshness is not the tool's marker either. Ten of the eleven pages are served **byte-identical** from a
committed `docs/index.html` — verified by hashing the fetched bytes against the file — so the whole page
is the check, and it needs the page to print nothing. `wroclaw` is the exception by design: CI rebuilds it
daily, it publishes `reports/site/` as a Pages artifact and **commits no HTML at all** (`.gitignore:25`; `git ls-files '*.html'` is empty), so its build stamp is the only handle.

## 3. The conformance table

> **Frozen 2026-09-05.** Correct as measured 2026-09-04 and **not maintained past that date**. This table was
> corrected five times across two sessions (§8.1, §8.2, §8.3, §8.4, §8.5), which is what a measurement inside a
> normative document costs. From S2 it is replaced by the checker's computed output
> ([`ADR-0004`](../adr/0004_what-carries-the-page-spec.md) §5); until then, re-measure before quoting a cell
> rather than citing this one. **Its row unit is already known to mislead for one purpose:** the contrast
> rollout scopes by *token source*, and this table's row is a *page* — `car-price-ml` has one source feeding
> two published surfaces, so a per-page reading of it undercounts ([`0008`](0008_the-rollout-ledger.md) §2.1).

**This is the one place the per-page facts live.** §5's clauses state rules and point here; §9's rollout
scopes itself from here. One measured value in one place is the whole reason this table exists — §8.2 and
§8.4 are what happens when the same fact is kept in five.

Measured 2026-09-04 against the **live** pages, every CSS answer read from the complete stylesheet, the
`<title>` and separator columns from the page's rendered text, and the geometry with `measure_page.py` at
`wroclaw-air-insights` `fae496e` — merged, so a later reader has a fixed instrument to re-run rather than a
branch to find.

| page | `h1` | `<title>` | eyebrow | tiles | scroller | tokens | dark | card meta | back-link | webfont | separator |
|---|---|---|:-:|---|---|:-:|:-:|:-:|:-:|:-:|---|
| `doc-extract` | claim | claim | yes | `.kpi` ×4 | `.table-wrap` | **10** | yes | yes | **yes** | — | `U+202F` 3, `U+00A0` 1 |
| `it-job-radar` | claim | claim | yes | `.kpi` ×4 | `.table-wrap` | **10** | yes | yes | no | — | **space** 40 |
| `car-price-ml` | claim | claim | yes | `.kpi` ×4 | `.table-wrap` | **11** | yes | yes | no | — | **space** 16, `U+202F` 12 |
| `auth-log-scan` | claim | **repo name** | yes | `.kpi` ×5 | `.table-wrap` | **11** | yes | yes | no | — | none |
| `pl-review-sense` | claim | claim | yes | `.kpi` ×4 | `.table-wrap` | **10** | yes | yes | no | — | **space** 4 |
| `mini-traceroute` | **descriptive** | **repo name** | yes | `.kpi` ×4 | **`.ledger-wrap`** | **13** | yes | yes | no | — | none |
| `ab-lab` | claim | claim | yes | **`.tile`** ×4 | **`.scroll`** | **11** | yes | yes | no | — | **comma** 2, **space** 1 |
| `apply-scout` | claim | **repo name** | yes | `.kpi` ×4 | **`.tablewrap`** | **0** | **no** | **no** | **yes** | Inter | none |
| `mlops-car-price` | **repo name** | **repo name** | **no** | **none** | **`.tablewrap`** | **0** | **no** | **no** | no | Inter | **comma** 3 |
| `pl-jobs-lora` | **repo name** | **repo name** | **no** | **none** | **`.tablewrap`** | **0** | **no** | **no** | no | Inter | none |
| `wroclaw-air-insights` | claim | **repo name** | yes | **`.stat`** ×4 | `.chart-wrap` + *the table itself* | **9, two aliased** | yes | yes | no | — | **comma** 3 |

`car-price-ml` publishes a **twelfth surface** this table does not measure — `docs/app/index.html`, the
valuation form (§7).

### 3.1 Geometry, at every width the commission named

`0003` §3 commissioned this *"at desktop and at 375 px"*, and the first draft delivered 375 and 390 only.
Closing that gap needed no new tool — `DEFAULT_WIDTHS` already carried all five — only the tabulation. Run
in one pass so that every row describes one state of the pages.

| width | tables wider than their card | unhandled | document scrolls sideways |
|---|---|---|---|
| 375 px | **17** | 0 | no page |
| 390 px | 16 | 0 | no page |
| 414 px | 14 | 0 | no page |
| 768 px | 4 | 0 | no page |
| 1200 px | 3 | 0 | no page |

42 tables. **Every wide table, at every width, is inside something that scrolls** — `.scroll` ×2,
`.tablewrap` ×7, `.table-wrap` ×4, `.ledger-wrap` ×1 at 414 px, which is §4.4's four names for one job seen
from the side. *A count of wide tables that does not name its width is not a measurement.*

The three that survive 1200 px are `apply-scout`'s two and `pl-jobs-lora`'s one, and they surface something
the phone widths hid: **beyond about 768 px the card stops growing.** It gives 671 px of room at 768 and
only 778 px at 1200, so `apply-scout`'s 1268 px table scrolls on every viewport that exists. Desktop is not
the width at which these tables come right; there is no such width.

## 4. What the divergence is

### 4.1 One design system, two encodings

Seven pages declare the same ten custom properties. **Eight of the ten hold one value across all seven:**

```css
--bg: #ffffff;  --surface: #f6f8fa;  --border: #e3e7ee;  --text: #1c2430;
--muted: #5b6472;  --accent: #2563eb;  --warn: #b45309;  --radius: 10px;
```

Extensions are additive — three add `--danger`, `mini-traceroute` adds `--mono`, `--slate`, `--violet` —
and none of the ten is missing anywhere. Six carry the `.kpi` rule byte-for-byte identically. All seven
pair the block with a `prefers-color-scheme: dark` override redefining the same names, so the pages are
light by default and follow the reader's preference.

**Two tokens split, and neither split is drift.** An earlier draft of this section claimed all ten
were identical; it had measured seven of them. The two it had not:

| token | value | pages | is it drift? |
|---|---|---|---|
| `--accent-soft` | `#93c5fd` | `doc-extract`, `car-price-ml`, `auth-log-scan`, `mini-traceroute` | — |
| | `#5b93e4` | `it-job-radar`, `pl-review-sense`, `ab-lab` | — |
| `--positive` | `#059669` | five pages | — |
| | `#047857` | `car-price-ml`, `ab-lab` | **no — a documented, measured fix.** `ab-lab/sitegen/theme.py:13`; **5.15:1** against `#059669`'s **3.54:1** on `--surface`, and both holders paint it as text |

And in the **dark** override, `it-job-radar` and `pl-review-sense` carry the reason in the source:

```css
--accent-soft: #4167a6;  /* 3.30:1 on the dark page; #2c4a7c was 2.11:1 */
```

Five pages still hold `#2c4a7c`, a **2.11:1** ratio these two measured and rejected. So this divergence is
a **measured accessibility fix that reached two pages of seven** — and a spec that unified on the majority
would revert the fix on those two and freeze the failing ratio on the other five. **And the light values split the same way, which nobody had written down.** Computed here against
`--bg: #ffffff`, for a token used as `fill:`/`stroke:` on chart marks, where WCAG's non-text threshold is
3:1:

| | majority | minority |
|---|---|---|
| light `--accent-soft` | `#93c5fd` — **1.80:1** ✗ | `#5b93e4` — **3.12:1** ✓ |
| dark `--accent-soft` | `#2c4a7c` — **2.11:1** ✗ | `#4167a6` — **3.30:1** ✓ |

In both schemes the **majority value is the failing one**. Both rows were commented, and **both comments are
in stylesheets** — `it-job-radar` and `pl-review-sense` carry the light `--accent-soft` reason directly above
the declaration, and **both ship it in the published page**; `car-price-ml` carries
`--positive`'s the same way, published page included. `ab-lab`'s generator records both a third time. So the
governing rule's argument is **not** that the reason lived somewhere unreadable: the sweep read those very
files and read past the comment. `pl-review-sense/tests/test_palette.py` asserts the `--accent-soft`
threshold as a test, which is a fourth surface — and the only one that fails when the value drifts.

**`--positive` is the same finding a second time, and it is not a clean split by role.** Recomputed:
`#047857` is **5.48:1** on `--bg` and **5.15:1** on `--surface`; `#059669` is **3.77:1** and **3.54:1**.
Five pages hold the failing majority; four of them never paint it as text — `it-job-radar` `fill:`,
`auth-log-scan` `stroke:`, `doc-extract` and `pl-review-sense` declare it and never use it — where the 3:1
non-text rule applies and `#059669` passes. **`mini-traceroute` paints it as text**: `.ledger td.probe-ok`
at 0.86 rem / weight 600 and `.verdict .ok` at 0.85 rem / weight 700. Parsed rather than inferred from the
stylesheet, both sit at `html > body > div` — outside every card, so the ground is `body`'s `--bg`
`#ffffff` and the ratio is **3.77:1**. At ~13.8 px, weight 600 is *normal* text under WCAG — large starts
at 18.66 px bold — so the threshold is 4.5:1 and the page fails it.
The two pages holding `#047857` are the two that paint it as text and pass. So this is not a candidate for §7:
it is a measured accessibility fix that reached two pages of three, exactly like `--accent-soft`, and the
dark side (`#34d399`, 8.90:1 on `--surface`) is uniform and safe.

**This is the document's own thesis occurring inside the family it holds up as the original** — which
strengthens the case for a checker and destroys the case for stating identity. It is also why §5's
governing rule is *the measured value wins*, not *the majority wins*.

**The three pages with zero tokens are not a second design. They are the same one, transcribed by hand.**
`apply-scout`, `mlops-car-price` and `pl-jobs-lora` hardcode `#1c2430`, `#2563eb` and `#e3e7ee` — the exact
values of `--text`, `--accent` and `--border`. They diverge on **three** roles:

| role | house token | family B literal |
|---|---|---|
| muted text (`color:`) | `--muted: #5b6472` | `#667085` |
| surface (`background:`) | `--surface: #f6f8fa` | `#eef1f6` |
| warning | `--warn: #b45309` | `#d97706` (`pl-jobs-lora`) |

**And `pl-jobs-lora` has drifted against itself**, which is the sharper half: it carries `#475467` as a
*second* muted (`th { color: … }`) and `#f8fafc` as a *second* surface (`tr.ours td { background: … }`),
inside one page. §5.2 argues that between-page divergence costs the reader nothing and within-page
divergence costs everything; here is a page paying that cost, with no name for either value to be
compared against.

So the divergence between the families is **not a design decision anybody made**. It is one system held in
two places, one of which has no name for its values and has therefore drifted three ways outward and twice
inward — *one fact, several surfaces, no rule about which one leads*, expressed in CSS.

### 4.2 `apply-scout` is mid-migration, and nothing records it

It has `.kpi` ×4 and an eyebrow — family A's **names**, adopted in `#32` — over family B's **encoding**:
zero tokens, Inter, no dark override, no card metadata, `.tablewrap`. Its `.kpi` rule hardcodes `#e3e7ee`,
which is `--border`'s value, and sets `border-radius: 12px` where the house token is `10px`. A hand copy
that got the colour right and the radius wrong by two pixels.

Its own source says so and blames the absence of this document:

> `/* Provisional: three tile conventions exist across the portfolio's twelve pages and the`
> `   Session 4 design spec unifies them. '.kpi' is the majority, so it is what this page uses`
> `   until that spec lands. */`

The author picked the majority **name** because nobody had ever written down that a **rule** existed and
was shared, byte-for-byte, by six pages.

### 4.3 `wroclaw` is in the house style, under two aliases

**Read live rather than from its stale committed copy, this row barely diverges at all.** Its `:root`
holds `--bg: #ffffff`, `--surface: #f6f8fa`, `--muted: #5b6472`, `--accent: #2563eb`, `--warn: #b45309` —
house names *and* house values — plus `--line: #e3e7ee` and `--ink: #1c2430`, which are the house values of
`--border` and `--text` under two aliases, and one addition, `--specialist`. Its dark override holds the
house dark values. It carries an eyebrow, card metadata, a claim `h1` (*"Live 24-hour PM2.5 forecast"*) and
no webfont.

What is left of its divergence is **two token aliases, two absent tokens, a third `--accent-soft`, and `.stat` for `.kpi`** — the smallest gap of the
four pages this spec has to move, not the largest. The earlier draft said the opposite because it read the
file instead of the page; see §2 and §8.

It remains the one page rebuilt daily by CI, so any change to it must survive `refresh.yml`, and its row
must always be taken from the live URL.

### 4.4 Three names for one job, inside the house style

*Derived from §3's tiles and scroller columns — the counts live there and this is the shape of them.*

| tiles | pages | scroller | pages |
|---|---|---|---|
| `.kpi` | 7 | `.table-wrap` (+`.chart-wrap`) | 5, and `.chart-wrap` on `wroclaw` |
| `.tile` | 1 (`ab-lab`) | `.tablewrap` | 3 |
| `.stat` | 1 (`wroclaw`) | `.scroll` | 1 (`ab-lab`) |
| none | 2 | `.ledger-wrap` | 1 (`mini-traceroute`) |

`wroclaw` also makes the table itself the scroller under `max-width: 640px`, which is a fourth mechanism
and the one that broke the measuring instrument (§2).

## 5. The spec

**The governing rule, before any clause: where a page has measured a reason and recorded it, that value
wins. The majority decides only where nobody measured.** §4.1 is why — the largest token split in the
portfolio is a contrast fix with its ratio in the source, and a spec that counted pages would have
reverted it.

Each clause states the rule, then **what is already true**, so a reader can see it is a description before
it is an instruction.

1. **Colour and radius are the ten tokens in §4.1, with a `prefers-color-scheme: dark` override
   redefining the same **colour** names** — `--radius` does not vary by scheme and no page redefines it. Additive extensions are allowed and must be named in the page's own
   `:root`. No literal hex outside the token block. **A token is used in the role it names**: `background`
   and `background-color` take `--bg` or `--surface`; `border`, `border-color` and the four one-sided
   borders take `--border`.
   *Measured on 2026-09-06 across the eleven published surfaces on disk and `wroclaw`'s own source, which
   its page is rebuilt from daily — that page commits no HTML, and `--fetch` shows the pre-S7 palette until
   the next publish: **141** declarations in those two families name a token; **11** of
   them are `color-mix()`, which clause 1's composited half already reports `undecided` and this sentence
   does not reach. Of the **130** that remain, **112** already name the house role. Every one of the
   remaining eighteen is one of four shapes, and they are the exception rather than a
   tolerance — a one-sided border thicker than a hairline
   (12 — `.card.caution`'s rail on seven pages, four more in `car-price-ml/docs/app`, and `wroclaw`'s
   `.verdict`; its `dd` is a 2px rail in `--border`, which is the house role, so it counts among the 112
   rather than here — the thickness alone never carried this); a rule declaring its
   own `color` beside its background (3 — two `button`s and `.terminal .cursor`, which have chosen a ground
   rather than inherited the page's); a border naming the role its own background names (1 —
   `mini-traceroute`'s `button`); and a `border-color` under an interaction state — `:hover`, `:focus`, `:active` — (2), which
   signals rather than encloses. *`car-price-ml/docs/app`'s `input:focus-visible` and `wroclaw`'s
   `nav.toc a:hover`. The second appeared only when S7 renamed that page's `--line` to `--border`:
   until then its palette held no house border role, so the clause reported `undecided` and could
   decide nothing. A rename made a clause able to answer, and the first thing it answered was a real
   question — which is the argument for the `undecided` in the first place.*
   **All four hold only where the role in question is not one of the three named above** — `--bg`,
   `--surface`, `--border` — and that condition is the whole of what makes them exceptions rather than
   holes: each describes a surface deliberately painted *outside* the house scheme, so a house role
   appearing there is the defect and not the exemption. Without it,
   `.card { background: var(--surface); border: 1px solid var(--surface) }` reads as a border matching its
   own fill; `body { background: var(--border); color: var(--text) }` as a control painting its own text;
   and `.result.pending { border-left: 3px solid var(--surface) }` as a rail, though that declaration is
   the box's edge and `car-price-ml/docs/app` paints it in `--border` today. Swept declaration by
   declaration over the eleven surfaces on disk, the condition takes the rule from **55 of 97 conforming
   sites caught to 97 of 97**; over all twelve it is **112 of 112**.*

   *A first draft of this census counted eleven surfaces and then reported the interaction-state shape as
   **2**, which is its count on twelve — so the four shapes summed to seventeen under a sentence saying
   sixteen. One cell of a six-number census was moved and the other five were left, which is `0007` §8.2's
   own finding: a correction that does not propagate is a new error.*

   **A page adding a fifth shape is stating something this sentence does not describe, and the governing
   rule above decides it — not this list.**

   **This sentence exists because `apply-scout` had it as a source comment and that was not enough.** One
   literal can serve two roles: `#eef1f6` was both `code`'s background and the table separator, so a
   migration done by *value* rather than by *role* produced a page whose tokens were all declared, all
   resolvable, and one of them wrong. `0008` §3.6 is what that cost, and §3.6's HIGH is that neither carrier
   could see it — both read `:root`, and this is the only clause-1 sentence that cannot be checked there.
   The eight settled values are as printed; for the two
   that split, the spec takes the **measured** one — `--accent-soft: #5b93e4` light (3.12:1 against
   `#93c5fd`'s 1.80:1) and `#4167a6` dark (3.30:1 against `#2c4a7c`'s 2.11:1) — and `--positive: #047857`
   light, which clears AA as text on both grounds a page paints on (**5.48:1** on `--bg`, **5.15:1** on
   `--surface`) where `#059669` clears neither (**3.77:1** and **3.54:1**), and `#34d399` dark, which every
   page holds and which clears both thresholds on either ground (8.90:1 on `--surface`, 9.69:1 on `--bg`).
   **The threshold is the one the page's own usage implies, and it is read per page, not per token**:
   `--positive` is painted as body text on one page and as a `fill:`/`stroke:` mark on three (§4.1), so a
   page painting it as text is held to AA's 4.5:1 and a page painting it as a mark to the non-text 3:1.
   `--accent-soft` is only ever a mark, on every page that paints it.
   *The tokens and dark columns of §3 — where the tokens column counts **declared** properties, so
   `wroclaw`'s `9` and the `8` house tokens below are two different quantities.* Two rows need a word the
   table cannot hold. `wroclaw` reaches it
   eight under two aliases (`--ink` for `--text`, `--line` for `--border`), **lacked `--positive` and
   `--radius` entirely** — it inlined `border-radius: 10px` as a literal — and carried a **third**
   `--accent-soft`, `#dbe7ff` light and `#1e2c45` dark, on neither side of the split below; those measured
   1.24:1 and 1.33:1 against their own grounds, and **nothing painted them** — declared twice in `page.css`
   and used nowhere — so no threshold applied and it was a naming item rather than a defect.

   ***All of that is now past tense.*** `0008` S7 renamed both aliases, declared `--radius` and
   `--positive` at the pinned values, and took the third `--accent-soft` to `#5b93e4`/`#4167a6`; the page
   holds all ten house tokens under the house names. *The paragraph is left standing rather than deleted
   because the amendment thirty lines above it describes the same rename, and a clause whose descriptive
   notes are maintained in one place and stale in another is worse than one that is stale throughout —
   which is `0007` §8.2's own finding, caught here by review.* And the three pages reading `0` carry no
   dark override either, which is the same fact twice and is why those two columns move together.
2. **A tile is `.kpi`.** *The tiles column of §3, frozen 2026-09-04: two of the nine pages that have tiles
   use another name. Both converged in S7 — `ab-lab`'s `.tile` and `wroclaw`'s `.stat` — so every page
   with tiles now uses `.kpi` **in its source**; `wroclaw`'s published artifact follows at its next
   rebuild, which is the one surface where those are different things.*
3. **Every `<table>` sits in `.table-wrap`, which computes to `overflow-x: auto`.** The wrapper must
   actually have somewhere to scroll when the table needs it; a wrapper that clips, or one outside the
   card, does not count. *The scroller column of §3: one rule under four names, plus `wroclaw` making the
   table itself the scroller under `max-width: 640px`. §3.1 measures the **wide** tables and finds none
   unhandled at any of the five widths — so on ten pages a rollout changes the name and not the behaviour.
   On `mini-traceroute` it changes the behaviour: its second table sits in a bare `<figure>` with no
   scroller and passes on margin, which is why this clause keeps `0004` §6.5's* every *table (§9 row 6).*

   **The checkable form**, which is what `measure_page.py` already tests: *every `<table>` has an ancestor
   at or below its card whose computed `overflow-x` is `auto` or `scroll` and which has somewhere to
   scroll — or is a table the page declared with `data-scroll="by-design"`.* `.table-wrap` is the name to
   converge on; the rule is about behaviour, and only the name needs a rollout.

   *This clause deliberately keeps `0004` §6.5's wording — **every** table, not every **wide** table.* A
   draft narrowed it, which would have let `pl-review-sense` (7 tables, none wide) and `it-job-radar` (1,
   none wide) pass on the accident of their content, and dropped `mini-traceroute`'s unwrapped
   `<figure>` table to the bottom of §9. §6.5 bound the wider criterion here precisely so it could not be
   lost, and gave the reason: *"they do not overflow today only because they happen to be narrow
   enough."*
4. **The page opens with an eyebrow and an `h1` that states a claim, not the repository's name — and the
   `<title>` follows the `h1` rather than the directory.** *The `h1`, eyebrow and `<title>` columns of §3.*
   The two halves are **different surfaces with different readers** — the page, and the search result or
   the shared link — and the `<title>` half is further behind, which is why it is a column of its own.
   `apply-scout` is the case that makes the point: its `h1` was fixed in `#32` and its title was not.
   *`wroclaw`'s `h1` was called the project's name by an earlier draft, which had read the local build,
   where it was.*
5. **The page carries `description`, `og:type`, `og:title`, `og:description`, `og:url`, `twitter:card`
   and a favicon** — the property list, named, because `og:*` passes on any single tag and a checker needs
   to know which. *The card-meta column of §3. `wroclaw`'s `yes` is the one that is not whole: it carries
   three of the four `og:` properties and is missing `og:description`.*
6. **The page carries exactly one link back to the profile.** *The back-link column of §3. `0003` §7
   settled the shape — hub-and-spoke, one link — and it has never been rolled out.*
7. **Type is the system stack.** No third-party font request. *The webfont column of §3; the three that
   fetch Inter from `fonts.googleapis.com` are making a request to a third party from a page whose subject
   is provenance. `wroclaw` is not among them — it dropped the webfont in `#27`, and the stale committed
   copy is why an earlier draft said four.*
8. **Thousands are separated by `U+202F`, the narrow no-break space** — the codepoint, not an HTML
   entity, so a checker can test for it.

   *Scored over **whole grouped figures** in each page's rendered text — `1-3 digits, then one or more
   (separator + exactly three digits)`, with nothing numeric and no `:` or `.` touching either end. The
   per-page inventory is the separator column of §3.* **Seven pages print a grouped figure at all**; four
   print none. A plain space on **four**, a comma on **three**, `U+202F` on **two**, `U+00A0` on one.
   `doc-extract`, `car-price-ml` and `ab-lab` each use two — though no single figure mixes them.

   *The bound on the whole token is what makes this a measurement, and it is stated here because
   **three** earlier tallies were wrong. Twice the pattern matched across two adjacent numbers, so
   `07:00 203.0.113.42` scored as a grouped figure and gave `auth-log-scan` nineteen it does not have. The
   third was wrong differently and is the subject of §8.5: it disagreed with the pages on four rows, and
   three of those four pages had not changed since it was taken.*

   An earlier draft claimed this clause had "no majority to appeal to" and named `&nbsp;`, an HTML entity
   a checker cannot test for. There **is** a majority — the plain space, on four of the seven pages that
   group at all, and by volume a larger one still: **61 of the portfolio's 85 grouped figures carry it**.
   It loses to the governing rule anyway. **`doc-extract` is the one page that has left it entirely**, and
   **`car-price-ml` is mid-migration in public** — 16 figures with a plain space against 12 with `U+202F`,
   on one page. The reason is in the glyph: a plain space breaks across a line and cuts a number in half.
   The majority here is the unconsidered choice and `U+202F` is the considered one.

### 5.0 What counts as quoting a cell

`ADR-0012` says the page quotes and never retypes, and every stage since has leaned on that without the
portfolio ever stating what *quoting* permits. S4 could not proceed without it: both its target pages print
figures today that no artifact prints, and calling that a violation needs a rule rather than a preference.

1. **A figure is a quotation when its digit sequence equals a cell's, character for character.** The group
   separator, the minus sign and the presence or absence of a trailing zero are the *page's typography* and
   are not part of the quotation. The reference implementation already exists and predates this sentence:
   `car-price-ml/src/car_price_ml/site/charts.py:76` is `f"{value:,.0f}".replace(",", "\u202f")` — the
   generator holds the value, the page holds the glyph. `wroclaw`'s `formatting.fmt` is the same pattern.
2. **Rounding is not quoting.** `727,554` → `728k`, `2.25` → `2.3` and `0.23` → `23 %` are new numbers, and
   a reader cannot check them against anything. To publish a figure at a coarser precision, change the
   generator's precision and regenerate; the friction is the point, and it is `ADR-0012`'s own — *to publish
   a new number, extend the generator.*
3. **A ratio or a comparison is an argument, not a cell.** `ADR-0012` §2 already says so; it is restated here
   because clause 1 of this section is otherwise read as forbidding prose.

*This is what makes clause 8 satisfiable at all.* `mlops-car-price/reports/artifact_cost.md` prints `9,278`
with a comma and clause 8 mandates `U+202F`; under a byte-for-byte reading no page could satisfy both, and
that repository holds no `U+202F` anywhere. Sentence 1 is the resolution, and it is the one the portfolio was
already implementing.

### 5.1 The tile rule, against ADR-0012

**Clause 2 binds where a committed artifact can source the figure, and names the fallback where it cannot:
a lead paragraph carrying the claim, with the reason stated on the page** — so a later reader does not read
the exemption as sloppiness.

**The condition is a question about a repository, not a list of pages.** Does `git ls-files` show a committed
artifact holding the cell the tile would quote? A list is what let the paragraph below stand wrong for two
weeks, and a list cannot be checked by anyone who is not maintaining it.

> ~~`mlops-car-price` and `pl-jobs-lora` have no tiles, no generator, and no committed table to quote. A
> mandate to grow four tiles would make them print figures no artifact produces, which the portfolio's own
> standard forbids. … `pl-jobs-lora`'s honest headline is a claim about baselines measured before the
> fine-tune exists, which is a copy decision that has to be taken before any tile can be filled.~~

**Struck 2026-09-06: every clause of that was false when it was written, and the fallback applies to
neither page.** Measured with `git ls-files` rather than read:

| | committed artifacts | generator |
|---|---|---|
| `mlops-car-price` | `reports/artifact_cost.md`, `reports/detector_evaluation.md`, `reports/drift_scenarios.md` | `examples/artifact_cost.py`, `examples/detector_evaluation.py`, `examples/drift_scenarios.py` |
| `pl-jobs-lora` | `results/eval/report.md`, `results/eval/report.json` | `src/pl_jobs_lora/eval/report.py`, covered by `tests/test_eval_report.py` |

`pl-jobs-lora`'s page has quoted that report since **2026-08-21**, two weeks before this document said the
table did not exist. So the exemption was granted against the repositories rather than from them — the
failure this record's own §2 method exists to prevent, committed in the section that grants an exemption.

**Clause 2 therefore binds on both, and eight tiles are sourceable today**: `mlops-car-price` from
`9,278` PLN and `3.3` MB against `338.5` MB and `5.0%` false alarms; `pl-jobs-lora` from `0.51` field F1,
`0.05` JSON validity, a `0.28` recall ceiling and `142` gold records.

**And the index checker cannot carry this clause either way.** `clause_2_tiles` returns
`n/a — no tiles; §5.1 fallback applies` for *any* page with no tiles, because a checker reading one page's
HTML cannot see its repository's artifacts. It reports `n/a` before and `ok` after and never reports the
state in between, so the binding is carried by a test in the repository — which is what `ADR-0004` §4's
amendment provides.

### 5.2 What carries the spec

> **Superseded 2026-09-05 by [`ADR-0004`](../adr/0004_what-carries-the-page-spec.md).** The argument below —
> prose plus a per-repo acceptance test, and the rejection of a shared stylesheet — **stands**. What does not
> is *"one vendored checker"*, hash-pinned per repository: measured, that pattern cannot reach two of the
> twelve (`pl-jobs-lora` ignores all of `.claude/`; `mini-traceroute` has no `pyproject.toml`), and it
> re-runs the decay `0006` §3 L2 refused for action pins. It also assumed the checker was unbuilt; roughly
> two thirds of it is already green in CI, in `apply-scout/tests/test_docs_page.py` and
> `pl-review-sense/tests/test_palette.py`.

Prose plus **a per-repo acceptance test**, computed by **one vendored checker** — the pattern `doc-extract`
already uses for its XSDs and fonts. A prose spec applied by hand to eleven repositories is eleven copies of
a dozen properties with no source of truth, which is the defect in §4.1 restated one layer up.

A shared stylesheet is **rejected**: the reader this portfolio is built for opens one page, so divergence
*between* pages costs them nothing while divergence *inside* one costs them everything. The counter-argument
— that a hiring manager who opens three links does form an impression of coherence — is recorded in `0006`
§4 and would roughly double the rollout.

## 6. The rule the pages were missing: what a page owes its siblings

`ADR-0012` binds a page to its **own** repository's artifacts. By construction it cannot see two pages
disagreeing, because each is true of what it quotes. That space is where the portfolio's sharpest
contradiction currently lives.

`car-price-ml`'s `h1` reads *"A 13.9 MB model prices this market better than a 590 MB one"*, from LightGBM
8 612 against RandomForest 8 798 — **pooled out-of-fold MAE over 5-fold cross-validation on 111 018
adverts**. `mlops-car-price`, which introduces itself as *"An MLOps layer around the used-car price model
(project A3)"*, reports LightGBM 9 278 and RandomForest 8 908 and says *"the random forest achieves the
lowest error"* — **on a frozen holdout of 23 571 rows, from models trained on a 60 % split**, over the same
raw dataset and through the same cleaning code (`dataset.py`: *"cleaned by the same code … so the MLOps
layer never grows its own second"*).

Both are correct, and the ordering flips for a reason neither page states. **This document asserted that
reason without measuring it**, which is the failure it keeps naming: an earlier draft said the flip
follows from the smaller training split. The split differs, but so does the corpus — `mlops-car-price`'s
`manifest.json` records 117 927 raw rows cleaned to **117 859**, against `car-price-ml`'s **111 018** from
the same 117 927, because the manifest predates a de-duplication step. And `car_price_ml/data.py:139-147`
documents the competing explanation directly: the duplicates *"flatter RandomForest by 256 PLN of MAE …
against LightGBM's 19 PLN"*, which is the same order as the 370 PLN gap that produces the flip.

So what is measured is that **the two numbers come from differently-cleaned corpora**, and the cause of
the flip is a question neither repository has answered. That is a result either way, and today it reads as
an error, because neither page names the other's measurement. The
reconciliation exists in `mlops-car-price`'s README, which links `car-price-ml` three times and gives the
split table. Its **page** mentions `car-price-ml` zero times, `23 571` zero times, `train_initial` zero
times. `car-price-ml`'s page mentions MLOps, holdout or its sibling zero times.

**And the MAE is only half of it.** `car-price-ml`'s `h1` says *"a 13.9 MB model … a 590 MB one"* — a 43×
ratio. `mlops-car-price`'s table reports the same two families at **3.3 MB** and **338.5 MB**, roughly
100×. Same dataset, same cleaning code, different training split, so both are true and the sizes move for
the same reason the errors do. Neither page says so, and this pair is the portfolio's most prominent
headline, so it is the strongest instance of what clause 9 is for.

> **Clause 9 — a number that appears on more than one page names the measurement it comes from, and points
> at the other.** *Scope: a figure the page presents as a result — a metric, a size, a count of the corpus
> — not every integer on it. A clause that covered `4` and `2026` would be unenforceable and would be
> ignored.* Not one number: the two measurements answer different questions and unifying them would
> delete a real distinction. What is forbidden is a reader meeting both with no bridge.

Enforcement is honest about its limit: a within-repo test can assert *this page names its measurement*,
which is checkable. That two pages agree cannot be checked without coupling two public repositories to a
private index, so it is a review item — carried in §8's list, not asserted as automatic.

## 7. What this spec does not check

Stated because the instrument that produced §3 has now been wrong three times, twice caught only by review.

- **Whether the page reads well.** Eleven pages can satisfy every clause and still be bad. The skill this
  spec's checker comes from says it outright: *"whether the page reads well … is a judgement made by looking."*
- **Any colour, spacing or type value beyond the token block.** Two pages can share all ten tokens and look
  quite different, and clause 1 is content with that.
- **That two pages agree on a shared fact** — see §6.
- **Whether an `h1` states a claim.** Clause 4's `<title>` half is checkable; *"states a claim"* is a
  human judgement, and it is the one normative clause a vendored checker cannot carry.
- **Contrast, beyond the two pairs clause 1 now pins.** Nothing in §5 computes a ratio, and §4.1 shows the
  portfolio carries **two** measured contrast findings that reached some pages and not others — including a
  **2.11:1** dark `--accent-soft` still live on five, and a `--positive` that fails AA as text on one page.
  Clause 1 pins both corrected values; it checks no other pair, and no page's *usage* is checked against the
  threshold that usage implies, which is the step that found the `--positive` failure at all.
- ~~**Desktop.**~~ **Closed** — §3.1 carries 414, 768 and 1200 alongside 375 and 390, measured in one pass
  so every row describes one state of the pages. `0003` §3 commissioned the table *"at desktop and at
  375 px"* and the first draft delivered two phone widths, which was a gap against the commission rather
  than a scoping decision. The finding it produced is in §3.1: **desktop is not the width at which the wide
  tables come right**, because the card stops growing at about 768 px.
- **The twelfth page.** The commission says twelve; there are eleven. `token-budget` has no page and
  returns 404, which is the fact that demoted it.
- **The twelfth surface.** A *page* here is a row of §3; a *surface* is any published HTML. `car-price-ml`
  publishes two surfaces and §3 measures one: the report and
  `docs/app/index.html`, the in-browser valuation form, linked from the report and in no row of §3. It is
  the only hand-written HTML in a repository whose page is otherwise generated and byte-diffed in CI, so
  clauses 4, 5 and 6 apply to it with nothing regenerating it. Every acceptance condition for
  `car-price-ml` must name both surfaces.
- **`wroclaw`'s local build**, which is gitignored, published as a Pages artifact rather than committed,
  and 24 days behind its own site on this machine. Its row in §3 must be — and now is — taken from the
  live URL. A later reader will not find a committed page to distrust; there is none.

## 8. Corrections to the record

Four, all of them mine or this review's, and all the same class: a claim wider than the measurement under
it.

| statement | where | the repository |
|---|---|---|
| *"`mini-traceroute`: two tables, no `overflow-x`"* — `0006` M3, from `0004` §6.5 | carried three sessions, **bound** to this spec | its rules are in an external stylesheet. **But not fully closed either:** `.ledger-wrap` wraps one table; the second sits in a bare `<figure>` with no scroller and passes on margin (+77 px at 375), not on structure |
| *"only `--winter` is `wroclaw`-specific"* — `0006` §4.2 | this session | `data-scroll="by-design"` was the second, and it made the tool call seventeen sound tables defects |
| *"Family A: theme dark; Family B: light"* — `0003` §4 | | all eleven are **light by default**; **eight** carry a `prefers-color-scheme: dark` override and **three** ignore the reader's preference |
| *"seventeen wide tables"* | this session, unqualified | true at **375 px**; sixteen at 390, which was then the tool's default width |

### 8.1 And five in this document's own first draft, all found by review

Listed rather than silently fixed, because four of the five are the class §8 exists to name and the first
is the class §2 exists to prevent.

| claim | the repositories |
|---|---|
| the `wroclaw` row, and §7's *"taken from the live URL"* | **taken from an untracked local build**, 24 days stale — and `reports/site/` is gitignored, so on a fresh clone that file does not exist at all. Wrong on six columns, all in the direction that made the divergence look worse. Live, that page is in the house style under two aliases |
| *"every shared token holds the identical value"* | **eight of ten.** `--accent-soft` splits 4/3 and `--positive` 5/2. Seven tokens had been measured and ten were claimed |
| the two split tokens read as drift | `--accent-soft` is a **measured contrast fix**, `3.30:1` against `2.11:1`, with the ratio in the source. Unifying on the majority would have reverted it — which changed the spec's governing rule from *majority* to *measured* |
| *"they differ on precisely two"* of family B | **three** roles, plus `pl-jobs-lora` carrying a second muted and a second surface **inside one page** |
| *"43 tables"*, and clause 8's separator tally | 42; and the separator inventory was wrong on both counts and omitted `U+202F`, which two pages already use |

### 8.2 And six more, from the review of the corrections

The pattern in every one: `533fcd3` corrected §3 and §4.3 and **did not sweep the clauses that consumed
the old values**. A correction that does not propagate is a new error, which is the reason this section
keeps growing rather than closing.

| claim | the repositories |
|---|---|
| *"the **committed** `reports/site/index.html`"*, four times | `reports/site/` is **gitignored** and the repository commits no HTML at all; the page is published as a Pages artifact. The misread file is an untracked local build, so on a fresh clone the hazard §7 described does not exist |
| clause 4's *"`wroclaw`'s is the project's name"* | left at the pre-correction reading while §3 and §4.3 were fixed — its live `h1` is a claim, and the count is **eight**, not seven |
| clause 1's *"true of eight pages"* | `wroclaw` **lacks `--positive` and `--radius` entirely** and carries a **third** `--accent-soft`; it holds eight of ten, not ten |
| §8's *"seven … and four ignore the reader"* | **eight and three**, derived from the old `wroclaw` row |
| §6's *"the ordering flips because the training set is smaller"* | asserted, never measured. The corpora also differ — 111 018 against 117 859 — and `car-price-ml`'s own source names de-duplication as a competing explanation of the same magnitude |
| the separator tally, **twice** | a `digit SEP digit digit digit` pattern matches across two adjacent numbers, so `07:00 203.0.113.42` counted as a grouped figure. Bounded properly: six pages, not seven, and three pages group no figures at all |

**One finding of the review was not an error but a gap in the rule**: the governing rule was applied to
the dark `--accent-soft` split, because two pages had written the ratio in a comment, and not to the light
one — whose comment is in the stylesheets and in the published pages too, and which the sweep read past
(§8.3, §8.4). Computed, the light majority fails at **1.80:1**. A rule that fires only where a reader
happens to notice the reason is a rule that fires by luck; clause 1 now pins both, and `--positive` besides.

### 8.3 And five more, from reading what consumes the values

Found while designing the rollout, by reading generators, usage sites, and the comments already sitting in
the stylesheets. The first three are one claim wearing several faces, which is §8.2's class again — a
correction that did not propagate — arriving before the correction did.

| claim | the repositories |
|---|---|
| `--positive` *"undocumented"* (§4.1), *"left open in §7 … nothing decides it"* (clause 1), *"no measurement at all behind it"* (§7) | **three surfaces of one wrong claim.** It is measured in `car-price-ml`'s `tokens.css:21` and in its published `docs/index.html`, and again in `ab-lab/sitegen/theme.py:13`: *"3.5:1 on `--surface` — below AA for text this size"*. Recomputed 3.54:1 on `--surface` and 3.77:1 on `--bg`, against `#047857`'s 5.15 and 5.48 |
| *"the light row had no comment"*, and §8.2's closing argument built on it | it has one in `it-job-radar` and `pl-review-sense`, directly above the declaration, and `it-job-radar` publishes it in the page's inline `<style>`. `pl-review-sense/tests/test_palette.py` asserts the threshold besides. The conclusion — pin the measured value — is unchanged; the reason is not that nobody wrote it down but that **the sweep read the file and read past the comment** |
| `--positive` *"is never painted as a non-text mark, so it stays a candidate"* | **false twice over.** It *is* painted as a non-text mark, on three pages — `it-job-radar` `fill:`, `auth-log-scan` `stroke:`, `mini-traceroute` both — where it passes at 3:1. And on a fourth usage it is painted as **body text**: `mini-traceroute`'s `.ledger td.probe-ok` and `.verdict .ok`, 0.86 and 0.85 rem, both `html > body > div` and so on `--bg`, at **3.77:1** against AA's 4.5:1. A second live accessibility defect, of the same shape as the `--accent-soft` one, and now in §9 row 5 — *which is [`0008`](0008_the-rollout-ledger.md) S1 since 2026-09-05* |
| clause 1's *"a **third** `--accent-soft`, `#dbe7ff`"* — named, never measured | **1.24:1** on `--bg` and **1.17:1** on `--surface`; the dark half `#1e2c45` is **1.33:1** and was not named at all. But `page.css` declares the token twice and **nothing paints it**, so no threshold applies today — it is a naming item, not a live defect, and the distinction is the one this document's own closing paragraph insists on |
| §3 measures eleven pages | **there are twelve surfaces.** `car-price-ml/docs/app/index.html` is a second published page, linked from the report at `docs/index.html:268` and in no row of §3. It is also the only **hand-written** HTML in that repository: `form.py` generates `docs/app/styles.css` and `config.json`, and CI's byte-diff covers those two and `docs/index.html` — **not** the page itself |

**What the five have in common is narrower than a method.** Three came from reading the *usage* sites — which
threshold applies is decided by how a value is painted, not by its declaration — and that half of the thesis
survives review. The other half did not: an earlier draft of this section said the reasons lived only in a
generator, *"a surface a sweep that reads CSS cannot see"*. They do not. Two of the three `--accent-soft`
holders and both `--positive` holders carry the measurement as a CSS comment above the declaration, published
inline in the page. The sweep read those files and read past the comment, which is a duller finding and the
true one. §8.4 records what that draft cost.

### 8.4 And six from the review of §8.3, which committed the class §8.3 was written to name

The section that named *a claim wider than the measurement under it* made five of them. Recorded because
the shape is now three rounds old and the lesson has moved: §8.2's cause was a correction that failed to
propagate; §8.3's was a correction that propagated a **generalisation the evidence did not carry**.

| claim | the repositories |
|---|---|
| *"neither comment was in a stylesheet … the note and the value are not on the same surface"* | false on both halves. `it-job-radar/src/it_job_radar/site/assets/styles.css:12`, `pl-review-sense`'s equivalent, `car-price-ml/src/car_price_ml/site/assets/tokens.css:21` — and all three ship it in the published page. The generalisation was built from one holder and stated of all |
| the `mini-traceroute` failure at **3.54:1**, *"inside `.card`"* | parsed, `.ledger-wrap` and `.verdict` are `html > body > div`. The ground is `--bg`, so the ratio is **3.77:1**. The 3.54 was `car-price-ml`'s comment describing `car-price-ml`'s ground, carried across to a page it does not describe — in the one row the document calls the item a reader can be harmed by |
| `#dbe7ff` *"1.22:1 on `--surface`"* | **1.17:1**. 1.22 is `#1e2c45` on the *dark* surface — the other half's second ratio, attached to the first half |
| `wroclaw`'s pair as *"the worst pair in the portfolio"* | true as arithmetic, wrong as a finding: `page.css` declares the token twice and nothing paints it. Asserting a defect no reader can reach is the mirror of missing one, and §8.3's own closing rule forbids it |
| clause 1 left ending *"…and on / all."* | the sweep of clause 1 deleted the sentence recording that the three literal-colour pages carry no tokens and no dark override — a correction damaging what it did not intend to touch, inside the normative spec |
| clause 1's *"six by name and value"* | five; `--accent-soft` matches by name only, as the clause now says two lines later. Eight of ten still holds |

**Two of the six are the correction that generalises**, which is this round's signature: rows 1 and 2 each
began as a true observation about one repository and were then stated of a class. The other four are their
own failures and the table names them separately — a figure carried across the halves of one page, a defect
asserted where no reader can reach it, a sweep deleting what it did not mean to touch, and a miscount. The
rule earned here is the one rows 1 and 2 pay for: *a finding names the file it was read in, and a claim
about a class is a claim that has to be checked in every member of it.*

### 8.5 And the separator tally, wrong a third time

§8 warned about this table twice. The third version was wrong differently, and it is recorded here because
the previous two warnings did not prevent it — which says the warning was not the useful part.

Re-measured 2026-09-04 from each page's rendered text in a real engine, and independently from the fetched
HTML, both giving the same answer on all eleven pages. Four rows disagreed with the recorded inventory:

| page | recorded | measured |
|---|---|---|
| `pl-review-sense` | space 7 | **4** |
| `pl-jobs-lora` | space 1 | **0** — it groups no figures at all |
| `car-price-ml` | `U+202F` 9 | **12** |
| `doc-extract` | space 5 | **0** |

**Three of the four are decisive.** `pl-review-sense`, `pl-jobs-lora` and `car-price-ml` last changed their
page on 2026-09-02, 2026-08-21 and 2026-09-02 — before the recorded tally — and each live page is
byte-identical to its committed file today. The page measured then and the page measured now are the same
bytes, so the difference is the measurement. `doc-extract` is not decisive: its page changed the same day,
in `05ed544`.

Nor is it a counting convention. Per figure, per separator occurrence, and with the whole-token bound
removed entirely, all three variants return the measured numbers.

**What it changes:** seven pages group a figure, not eight; the plain space is on four pages, not six; and
`pl-jobs-lora` joins the three that print none. Clause 8's **conclusion** is unaffected — `U+202F` still
wins as the value with a reason behind it — but its **supporting example was not**, and this correction did
not reach it either: the closing sentence still appealed to *"the two that print the most figures"*, which
the new column refutes. It is rewritten there. That is also the honest verdict on §3: the inventory now
lives in one cell, but **a clause that argues from a tally still has to be swept**, and this one was not
until review found it.

## 9. Rollout

> **Superseded 2026-09-05 by [`0008_the-rollout-ledger.md`](0008_the-rollout-ledger.md)**, which carries the
> plan and its status. Two substantive changes rather than a restatement: **row 5 moves to first**, because
> the ordering principle below (*prove the spec before applying it widely*) does not reach a row that proves
> nothing and stops harm; and **its scope is re-derived by token source rather than by page**, which makes it
> three repositories and four surfaces. Kept here unstruck because the reasoning in the rows is still the
> reasoning `0008` builds on.

Ordered so the spec is proved before it is applied widely.

| | scope | why here |
|---|---|---|
| 1 | **`apply-scout`** — finish the migration it started: tokens, dark override, card metadata, `.table-wrap`, drop Inter | It already carries the names; it is the smallest gap and the one whose source comment is waiting on this document |
| 2 | **`mlops-car-price` + `pl-jobs-lora`** — clause 4 (claim `h1`, eyebrow), then the rest | `0004` §8 calls this *"the single highest-value presentation change identified"*, and §5.1 has to be settled per page first |
| 3 | **§6 clause 9** on `car-price-ml` and `mlops-car-price` | A published contradiction outranks a missing convention |
| 4 | **Back-link + card metadata** on the pages that lack them | Nine and **three** repositories, mechanical once the spec exists |
| 5 | **The contrast fixes, light and dark, onto the pages that lack them** | The one item here a reader can be *harmed* by. `--accent-soft`: five pages declare the failing dark `#2c4a7c` and **three paint it** (`car-price-ml`, `auth-log-scan`, `mini-traceroute`); `doc-extract` and `ab-lab` declare the token and never use it; the light majority `#93c5fd` fails at 1.80:1 wherever it is painted. `--positive`: **`mini-traceroute` alone** is a live failure — it is the one page painting `#059669` as body text, at 3.77:1 against AA's 4.5:1. The four other holders paint it as a mark or not at all, so their divergence from clause 1's pinned value is **conformance, not harm**, and it moves to row 6 |
| 6 | **`ab-lab`, `mini-traceroute`, `wroclaw`** — naming (`.tile`/`.stat`→`.kpi`, `.scroll`/`.ledger-wrap`→`.table-wrap`, `--ink`/`--line`→`--text`/`--border`), `wroclaw`'s two absent tokens and third `--accent-soft`, and `mini-traceroute`'s unwrapped `<figure>` table | Lowest value: these pages are already right, only differently named. `wroclaw` moved from last to here once its row was read live, and any change to it must survive a daily rebuild |
