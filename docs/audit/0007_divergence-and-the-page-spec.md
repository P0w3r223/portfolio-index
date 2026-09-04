# The divergence, measured — and the page spec it turns out to describe

Date: 2026-09-04
Status: proposed
Author: Piotr Cząstkiewicz
Related to: [0006_session3-4-presentation-block.md](0006_session3-4-presentation-block.md) B2 and B3,
[0003_portfolio-review-plan.md](0003_portfolio-review-plan.md) §3 (Session 4) and §4 (the two families),
[0004_session1-recruiter-triage.md](0004_session1-recruiter-triage.md) §3.2, §6.4, §6.5,
`apply-scout/docs/decisions/0012_the_page_quotes_the_artifacts.md`

---

## 1. What this is

`0003` §3 commissions Session 4 as *a divergence table across all 12 pages, at desktop and at 375 px, and
one design spec covering layout, typography, KPI tiles and table overflow*. This document is both, because
the measurement turned out to answer the spec rather than merely to motivate it.

**The finding that decides the shape of everything below: there is nothing to invent.** A single design
system is already implemented across **all eleven** published pages. **Eight** hold it in named CSS custom
properties; three hold the same values as hand-typed literals and have drifted on three roles. The spec's
job is therefore to *name what exists*, reconcile the naming variants inside it, and move three pages onto
it — not to choose a house style. Six pages have something to change; three of them have only a name.

**And the rule for resolving a divergence is not the majority.** Of the ten house tokens, eight hold one
value everywhere and two do not — and the larger of those two splits is a **measured accessibility fix**
that reached two pages of seven, with the contrast ratio written in the source beside it. A spec that
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

## 3. The divergence table

Measured 2026-09-04 against the live pages at **375 px** (the plan's gate) and **390 px**, with every CSS
answer read from the complete stylesheet, and the geometry taken with `measure_page.py` as it stands on
`wroclaw-air-insights#29` — **open at the time of writing**, so a later reader re-running this table should
check which version of that instrument they have.

| page | `h1` | eyebrow | tiles | scroller | tokens | dark | card meta | back-link | webfont |
|---|---|:-:|---|---|:-:|:-:|:-:|:-:|:-:|
| `doc-extract` | claim | yes | `.kpi` ×4 | `.table-wrap` | **10** | yes | yes | **yes** | — |
| `it-job-radar` | claim | yes | `.kpi` ×4 | `.table-wrap` | **10** | yes | yes | no | — |
| `car-price-ml` | claim | yes | `.kpi` ×4 | `.table-wrap` | **11** | yes | yes | no | — |
| `auth-log-scan` | claim | yes | `.kpi` ×5 | `.table-wrap` | **11** | yes | yes | no | — |
| `pl-review-sense` | claim | yes | `.kpi` ×4 | `.table-wrap` | **10** | yes | yes | no | — |
| `mini-traceroute` | **descriptive** | yes | `.kpi` ×4 | **`.ledger-wrap`** | **13** | yes | yes | no | — |
| `ab-lab` | claim | yes | **`.tile`** ×4 | **`.scroll`** | **11** | yes | yes | no | — |
| `apply-scout` | claim | yes | `.kpi` ×4 | **`.tablewrap`** | **0** | **no** | **no** | **yes** | Inter |
| `mlops-car-price` | **repo name** | **no** | **none** | **`.tablewrap`** | **0** | **no** | **no** | no | Inter |
| `pl-jobs-lora` | **repo name** | **no** | **none** | **`.tablewrap`** | **0** | **no** | **no** | no | Inter |
| `wroclaw-air-insights` | claim | yes | **`.stat`** ×4 | `.chart-wrap` + *the table itself* | **9, two aliased** | yes | yes | no | — |

Geometry, both widths: **no page scrolls sideways.** 42 tables; **17 are wider than the space their card
gives them at 375 px** (16 at 390 — a count of wide tables that does not name its width is not a
measurement), and **every one of the 17 is inside something that scrolls**. There is no unhandled table
overflow anywhere in the portfolio.

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

**Two tokens split, and the larger split is not drift.** An earlier draft of this section claimed all ten
were identical; it had measured seven of them. The two it had not:

| token | value | pages | is it drift? |
|---|---|---|---|
| `--accent-soft` | `#93c5fd` | `doc-extract`, `car-price-ml`, `auth-log-scan`, `mini-traceroute` | — |
| | `#5b93e4` | `it-job-radar`, `pl-review-sense`, `ab-lab` | — |
| `--positive` | `#059669` | five pages | — |
| | `#047857` | `car-price-ml`, `ab-lab` | undocumented, but darker — the same direction |

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

In both schemes the **majority value is the failing one**. The dark row was found because two pages wrote
the ratio in a comment; the light row had no comment and was found only by computing it, which is the
governing rule's own argument for not counting pages. `--positive`'s split runs the same direction
(`#047857` is the darker on white) but is never used as a non-text mark, so it stays a candidate in §7.

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
   `:root`. No literal hex outside the token block. The eight settled values are as printed; for the two
   that split, the spec takes the **measured** one — `--accent-soft: #5b93e4` light (3.12:1 against
   `#93c5fd`'s 1.80:1) and `#4167a6` dark (3.30:1 against `#2c4a7c`'s 2.11:1). `--positive` is left open
   in §7: it splits the same direction and is never painted as a non-text mark, so nothing decides it.
   *True of seven pages. `wroclaw` holds **eight** of the ten — six by name and value, two under aliases
   (`--ink` for `--text`, `--line` for `--border`) — **lacks `--positive` and `--radius` entirely** (it
   inlines `border-radius: 10px` as a literal) and carries a **third** `--accent-soft`, `#dbe7ff`, on
   neither side of the split below. The three literal-colour pages carry no tokens and no dark override at
   all.*
2. **A tile is `.kpi`.** *True of seven of the nine pages that have tiles.*
3. **Every `<table>` sits in `.table-wrap`, which computes to `overflow-x: auto`.** The wrapper must
   actually have somewhere to scroll when the table needs it; a wrapper that clips, or one outside the
   card, does not count. *Five pages use that name; `.tablewrap`, `.scroll` and `.ledger-wrap` are the
   same rule under **three more names across five more pages**, and `wroclaw` additionally makes the
   table itself the scroller under `max-width: 640px`.*

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
   `<title>` follows the `h1` rather than the directory.** *Today: **eight** `h1`s state a claim — including `wroclaw`'s
   *"Live 24-hour PM2.5 forecast"*, which an earlier draft called the project's name because it read the
   local build, where it was — `mini-traceroute`'s is descriptive (*"A traceroute, one TTL at a time"*),
   and two are the repository's. The `<title>` half is further behind and is a **different surface
   with a different reader** — the search result and the shared link. **Five** titles lead with the
   directory name, including `apply-scout`, whose `h1` was fixed in `#32` and whose title was not, and
   `auth-log-scan` and `mini-traceroute`, whose `h1`s were never in question.*
5. **The page carries `description`, `og:type`, `og:title`, `og:description`, `og:url`, `twitter:card`
   and a favicon** — the property list, named, because `og:*` passes on any single tag and a checker needs
   to know which. *True of seven pages exactly; `wroclaw` carries three of the four `og:` properties and
   is missing `og:description`; the three literal-colour pages carry none of it.*
6. **The page carries exactly one link back to the profile.** *True of two pages; `0003` §7 settled the
   shape (hub-and-spoke, one link) and it has never been rolled out.*
7. **Type is the system stack.** No third-party font request. *True of eight pages; **three** fetch Inter
   from `fonts.googleapis.com` — a request to a third party from a page whose subject is provenance.
   `wroclaw` is not among them: it dropped the webfont in `#27` and the stale committed copy is why an
   earlier draft said four.*
8. **Thousands are separated by `U+202F`, the narrow no-break space** — the codepoint, not an HTML
   entity, so a checker can test for it.

   *Measured from the decoded text of every page, over **whole grouped figures** — `1-3 digits, then one
   or more (separator + exactly three digits)`, with nothing numeric and no `:` or `.` touching either
   end. **Eight pages print a grouped figure at all**; `apply-scout`, `auth-log-scan` and
   `mini-traceroute` print none. Of the eight: a plain space on **six** (`it-job-radar` 40 occurrences,
   `car-price-ml` 16, `pl-review-sense` 7, `doc-extract` 5, `ab-lab` 1, `pl-jobs-lora` 1), a comma on
   **three** (`mlops-car-price` 3, `wroclaw` 3, `ab-lab` 2), `U+202F` on **two** (`car-price-ml` 9,
   `doc-extract` 3), `U+00A0` on one (`doc-extract`). `ab-lab` uses two of them.*

   *Two earlier counts of this were wrong in the same way and are worth the warning: a pattern of
   `digit SEP digit digit digit` matches **across two adjacent numbers**, so `07:00 203.0.113.42` scored
   as a grouped figure and gave `auth-log-scan` nineteen it does not have. The bound on the whole token
   is what makes this a measurement.*

   An earlier draft claimed this clause had "no majority to appeal to" and named `&nbsp;`, an HTML entity
   a checker cannot test for. There **is** a majority — six of the eight pages that group at all — and it
   loses to the governing rule anyway: `car-price-ml` and `doc-extract`, the two that print the most
   figures, had already left it, because a plain space breaks across a line and cuts a number in half.
   The majority here is the unconsidered choice and `U+202F` is the considered one.

### 5.1 The tile rule, against ADR-0012

`mlops-car-price` and `pl-jobs-lora` have no tiles, no generator, and no committed table to quote. A
mandate to grow four tiles would make them print figures no artifact produces, which the portfolio's own
standard forbids.

**So clause 2 binds where a committed artifact can source the figure, and names the fallback where it
cannot: a lead paragraph carrying the claim, with the reason stated on the page** — so a later reader does
not read the exemption as sloppiness. `mlops-car-price` already has `examples/` scripts that regenerate its
README's tables and is the cheap case; `pl-jobs-lora`'s honest headline is a claim about baselines measured
before the fine-tune exists, which is a copy decision that has to be taken before any tile can be filled.

### 5.2 What carries the spec

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
- **Contrast, beyond the one pair clause 1 now pins.** Nothing in §5 computes a ratio, and §4.1 shows the portfolio already
  carries a measured contrast finding that only two pages act on — including a **2.11:1** dark
  `--accent-soft` still live on five. Clause 1 pins the corrected value; it does not check the others, and
  `--positive`'s split has no measurement at all behind it.
- **Desktop.** `0003` §3 commissions the table *"at desktop and at 375 px"*, and §3 delivers 375 and 390
  only. 414, 768 and 1200 were observed and are not in the table. **That is a gap against the commission,
  not a scoping decision**, and it is the first thing a later reader should re-run.
- **The twelfth page.** The commission says twelve; there are eleven. `token-budget` has no page and
  returns 404, which is the fact that demoted it.
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
one, which nobody had commented. Computed, the light majority fails at **1.80:1**. A rule that only fires
where somebody left a note is a rule that fires by luck; clause 1 now pins both.

## 9. Rollout

Ordered so the spec is proved before it is applied widely.

| | scope | why here |
|---|---|---|
| 1 | **`apply-scout`** — finish the migration it started: tokens, dark override, card metadata, `.table-wrap`, drop Inter | It already carries the names; it is the smallest gap and the one whose source comment is waiting on this document |
| 2 | **`mlops-car-price` + `pl-jobs-lora`** — clause 4 (claim `h1`, eyebrow), then the rest | `0004` §8 calls this *"the single highest-value presentation change identified"*, and §5.1 has to be settled per page first |
| 3 | **§6 clause 9** on `car-price-ml` and `mlops-car-price` | A published contradiction outranks a missing convention |
| 4 | **Back-link + card metadata** on the pages that lack them | Nine and **three** repositories, mechanical once the spec exists |
| 5 | **The `--accent-soft` fix, light and dark, onto the pages that lack it** | The one item here a reader can be *harmed* by. Five pages declare the failing dark `#2c4a7c` and **three paint it** (`car-price-ml`, `auth-log-scan`, `mini-traceroute`); `doc-extract` and `ab-lab` declare the token and never use it. The light majority `#93c5fd` fails at 1.80:1 wherever it is painted |
| 6 | **`ab-lab`, `mini-traceroute`, `wroclaw`** — naming (`.tile`/`.stat`→`.kpi`, `.scroll`/`.ledger-wrap`→`.table-wrap`, `--ink`/`--line`→`--text`/`--border`), `wroclaw`'s two absent tokens and third `--accent-soft`, and `mini-traceroute`'s unwrapped `<figure>` table | Lowest value: these pages are already right, only differently named. `wroclaw` moved from last to here once its row was read live, and any change to it must survive a daily rebuild |
