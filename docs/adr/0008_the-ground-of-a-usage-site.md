# The ground of a usage site, and why the census comes first

Date: 2026-09-09
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: [`0004_what-carries-the-page-spec.md`](0004_what-carries-the-page-spec.md) §4 (the
geometry half, deferred and unowned — this reaches part of it and says how it differs),
[`0005_the-clause-registry.md`](0005_the-clause-registry.md) (where `c1.s6b` enters),
[`0006_the-gate-registry-and-the-twelfth-surface.md`](0006_the-gate-registry-and-the-twelfth-surface.md)
§3 (the `pending` state D3 depends on),
[`../audit/0007_divergence-and-the-page-spec.md`](../audit/0007_divergence-and-the-page-spec.md)
§5 clause 1 and §7, [`../audit/0008_the-rollout-ledger.md`](../audit/0008_the-rollout-ledger.md)
§3.11 (the design this amends), §4.23 (what the first commit measured) and §4.25 (S14's scope
re-derived, which is where D5 and D6 were measured),
[`../audit/0009_the-review-of-the-whole-system.md`](../audit/0009_the-review-of-the-whole-system.md)
§7 row 12

---

## 1. The decisions

| # | decision |
|---|---|
| **D1** | A candidate ground is resolved by **static-attribute containment** — a point-in-shape test on the coordinates the markup already writes — and not by *"every preceding painted sibling in the enclosing `<svg>`"*. `0008` §3.11's asymmetric verdict rule is amended, not implemented as written |
| **D2** | S13 ships as a **census**: three keys, `UNDECIDED` by construction, printing every usage site with its ratio and its resolved grounds. The verdicts become **S14** |
| **D3** | At S14 a verdict key enters `GATE` as **`Ratchet(prefix, PENDING_STATE, reason)`**, not `REPORT_ONLY_STATE`. `contrast ground` stays in `NOT_A_CLAUSE` and `NOT_A_SENTENCE` permanently. *Neither half of this row survived contact with the corpus.* It said **the two** verdict keys until 2026-09-10, and `0008` §4.25 had already re-derived that to one — which this row did not follow, the second time a count in this table outlived what it counted. Then S14b entered neither key as `pending`: `contrast text` is **gated**, because a fetching run reads it clean on all twelve and `ADR-0006` §3 makes that the refutation demanding promotion; and `contrast marks` is **report-only**, because the argument against `pending` — a state refutable in both directions, held by a key that can never read clean — says nothing about a state that is an explanation.* |
| **D4** | `0007` §5 clause 1 gains the sentence that makes a usage site's threshold an **obligation**, entering the registry as **`c1.s6b`**. Its wording is taken **after** the census prints, because `test_spec`'s guard pins the quote for as long as the sentence exists |
| **D5** | The marks key takes its obligation **by role** — visual information required to identify a user-interface component, and parts of a graphic required to understand the content — and **not** from structural decoration: table rules, card edges, the rule over an `<h2>`. The checker approximates that partition **by property name**, which is the instrument and not the rule; §7 names the places the approximation is known to be wrong — **two when D5 was taken and four since `0008` §4.29**. Taken 2026-09-09 against the census |
| **D6** | A site's own opaque **background occludes** what is behind it, so the ground walk starts at the element and stops there. Its own `fill` does not, and a **border faces outward** — measured against the other side of the boundary, never against what the element itself paints. §7 |
| **D7** | `0007` §5 clause 1 gains a **fourth house role, `--border-control`**, because D5 requires of a control boundary a ratio clause 1's one border role cannot reach. The checker admits the **name and not the placement** — the strict form was measured and refused — so the gap is recorded as `c1.s4c` and printed on every run. The token is **pinned in both schemes**, which is the only per-scheme value check the instrument has. §8 |

| **D8** | A verdict rests on **every ground the page paints behind a site**, whether containment is structural or read from the coordinates the markup writes. `Ground.guaranteed` is **not** a verdict input, and §9 is why: the guaranteed ground is never the binding one — 3.98:1 to 8.16:1 across all 79 sites whose only failing ground was geometric — while both failures with a history are read on a geometric one. What is excluded instead is a ground that is **another instance of the same mark**: two overlapping members of one series carry one meaning. The instrument approximates that by declaration identity, which is the `same`-colour rule corrected to compare like with like. **153 → 88**, `contrast text` byte-identical. §9 |

## 2. The problem, which is not the one `0008` §3.11 states

§3.11 bought its asymmetric verdicts to avoid a geometry engine, and called that *"the part
that would make it L"*. The purchase does not deliver on the corpus it was derived from.

`auth-log-scan` draws its event marks as runs of siblings inside one `<g class="row">`.
Measured with the element stream S13's first commit added: **133 of that page's 139
`.ev-failed` circles have a preceding sibling of their own class**, in runs of forty, sixteen
and twelve. Two marks of the same class are the same declared colour, so the candidate ratio
between them is **1.00:1** — and under a rule that a site must clear *every* preceding painted
sibling, each of those 133 sites reports `UNDECIDED`.

§3.11's own worked example says those marks `PASS`, at 3.98:1, 3.79:1 and 3.09:1. Both cannot
be true. The figures are right — all four reproduce from `colour.py` as shipped, and the
1.27:1 one matches the comment `auth-log-scan`'s stylesheet carries — so it is the rule that
is wrong, and it is wrong in the direction this checker exists to refuse: it would have
printed a confident `UNDECIDED` over a page that conforms, on **96 %** of that page's marks.

**133 is a lower bound.** It counts only same-class siblings, where the collapse is
arithmetically certain. A sibling of any other colour that happens to fail is one more.

## 3. Why containment, and why it is not the geometry `ADR-0004` §4 deferred

The corpus writes its coordinates. Every SVG element that paints carries them as attributes:

```
<rect class="lane" x="132" y="30.0" width="466" height="22">
<circle class="ev-failed" cx="132.0" cy="43.0" r="3">
<text class="cell-text" x="146.0" y="73.0">
```

So *is this mark inside that rect* is arithmetic on strings already in the markup: no layout,
no box model, no browser. Applied to the case above, the candidates for a mark reduce to
exactly the three grounds §3.11 names — its lane, its band and the page background — and the
clause produces §3.11's own three figures. On `pl-review-sense` a `.cell-text` at (146, 73)
falls inside one `<rect class="cell">` and no other, which is the single ground that carried
the real SC 1.4.3 failure S12 fixed.

**This is not `ADR-0004` §4's deferred geometry, and the distinction is the whole of D1.**
That half — `0007` §5 clause 3's *"the wrapper must actually have somewhere to scroll"* — is
deferred as unowned because it needs a rendered box: a wrapper's overflow depends on font
metrics, available width and the reader's viewport, none of which is in the file. Containment
between two shapes whose coordinates are both written in the same `viewBox` needs none of
that. One is a question about the browser; the other is a question about the document.

**Where containment cannot answer, the answer is `UNDECIDED` and not a guess.** An element
with no coordinates, a `transform` this checker does not compose, a `viewBox` scale between
nested `<svg>` — each yields the `contrast ground` key, which is what that key is for.

## 4. Why a census before verdicts

Four reasons, in the order they carry weight.

1. **The corpus is clean, so slowness costs nothing.** `0009` §7 row 12 promoted itself as
   *"the only open row where a published page can harm a reader"*. That harm — `.cell-share`
   at 2.69:1 — was closed by S12 **before** S13 was taken. There is no reader being harmed
   while this takes two stages instead of one, and §3.1's promotion rule no longer reaches
   the row. `0008` §4.23 records that expiry.
2. **A census decides D1 with an instrument rather than with this document.** §2's argument
   is a measurement plus a deduction, and this repository's own rule is that a scope figure
   not re-derived at the stage has been wrong every time it was checked. The census prints
   every site, its ratio and its grounds; whether containment resolves them is then a fact on
   the page rather than a claim in an ADR.
3. **A census cannot gate falsely.** `UNDECIDED` never gates, by policy and by construction,
   so the largest single piece of machinery this checker has taken on ships where its being
   wrong costs a wrong line of output and not a refused build.
4. **It pays for the same code either way.** The element stream, the matcher and the paint
   resolution are most of S14 and all of its risk. Nothing is built twice; what is paid twice
   is the registry pin edits, which is a known and small price.

## 5. Consequences

- **`0008` §3.11 is amended and not replaced.** Its element-not-selector finding, its
  three-key vocabulary, its warning that no key may start with `1 ` (because `_gated` tests
  `startswith` and `GATE` holds `"1 "`), and its measured figures all stand. The verdict table
  is what changes.
- **S13's size is what §3.11 said and S14's is not.** The census is M. The verdict half
  carries the cascade — an element needs *one* painted colour, and the corpus has
  `.diagram .node` against `.diagram .node.active`, `.chart .window-band` against
  `.chart .row.flagged .window-band` — which no existing clause-1 check has needed, because
  every one of them is per declaration.
- **`0007` §5 grows by a sentence.** D4. `c1.s6` chooses *which* threshold applies; the
  sentence making a usage site meet it lives today in `0007` §7, which `tools.spec`'s
  `NORMATIVE_TO` deliberately excludes from the guarded slice. Without D4, S14 would enforce
  a rule that is not in the normative text — the `data-scroll` shape from the other side, a
  checker stricter than its spec.
- **Two guards must be extended, and one of them ships green if forgotten.**
  `tests/test_spec.py`'s static source read takes its vocabulary from `clauses.__file__`, so
  a `Finding` literal in a new module is outside it and the guard keeps passing while
  covering less than it claims. And `NOT_A_CLAUSE <= spec.NOT_A_SENTENCE` is asserted, so
  `contrast ground` enters both sets or the guard reddens.

## 6. What was considered and refused

**§3.11's verdict rule as written.** §2. It is not a near miss: on the page the design
worked through, it is wrong on 96 % of the sites.

**`REPORT_ONLY_STATE` for the verdict keys**, which §3.11 chooses without arguing.
`test_the_report_only_set_is_pinned_because_it_is_policy_and_not_a_measurement` says in its
own words that report-only is the one state answering no question the corpus can ask. A key
that *can* gate, over a corpus reporting it clean, parked in report-only, is exactly the shape
that pin exists to make visible and cannot make end. `pending` is refutable in both
directions, and the fetching `live` run then demands the promotion. `ADR-0006` §3 built the
state for this and this is the first row to use it.

**Scoping S13 to `c1.s6` literally** — a per-page census of which threshold each token's usage
implies, and no clause. Half a day, no matcher, and it carries the sentence with nothing
behind it: it closes neither `0007` §7's gap nor the regression `0009` §7 row 12 names. The
sentence would be carried and the rule still unenforced, which is a worse state than the
honest `NOT CARRIED` the registry prints today.

**Deferring S13 entirely for `0009` §7 row 9**, the split of `0008`. Row 9's argument is
strong and got stronger — it has grown from 2 197 to 2 629 lines *because* it waits, and
§3.11 is one of the sections that grew it. It is not refused, only not taken first: the
element stream is what makes two of this repository's standing figures reproducible by an
instrument instead of by hand, and that is worth having before the record it feeds is split.

---

## 7. D5 and D6, taken 2026-09-09 once the census had printed

§4's reason 2 said the census would decide the open questions *"with an instrument rather than
with this document"*. These two are what it decided. `0008` §4.25 is the measurement; this
section is the decision and its bound.

### D5 — what the marks key is owed by

**Verdicts over marks with no such rule fail 1 195 of 1 785 measured sites**, on every surface
at once. The split says why, and it is not close:

| class | sites | measured | below 3.0:1 |
|---|---|---|---|
| CSS `border` / `outline` | 1 054 | 1 051 | **1 042** |
| `accent-color` | 3 | 3 | **0** |
| SVG `fill` / `stroke` | 1 290 | 731 | **153** |

The arithmetic is right and the obligation is not. SC 1.4.11 asks 3:1 of *user-interface
components* and of *graphical objects required to understand the content*. A hairline between
two rows of a table whose data is entirely text is neither: `--border` on white measures
1.17:1 and is required to measure nothing. **So the key without D5 is not a strict clause, it
is a broken one** — and it could not even ship `pending`, because `ADR-0006` §3's pending state
is refutable in both directions and this key would never read clean.

**The rule is the criterion's, and the partition is the instrument's.** D5 attaches the
obligation to *role*: visual information required to identify a user-interface component, and
parts of a graphic required to understand the content. The checker cannot read role, so it
approximates by property name — controls and SVG paint in, structural `border`/`outline` out.
*The first version of this section called that approximation "a reading of the criterion rather
than a policy". It is not; it is an approximation of a reading, and it is known to be wrong in
two places — **four since `0008` §4.29, which measured 17 more sites in two further shapes**:*

- **48 sites it admits that have the excluded role.** `line.grid` (22), `line.lane-line` (15),
  `line.axis-line` (8) and `line.axis` (3) are gridlines and axis rules, painted the same
  `--border` `#e3e7ee` at the same 1.17:1 as the table hairlines D5 excludes. They fall inside
  only because they are `<line stroke>` rather than `border-bottom`, and
  `car-price-ml/docs/index.html` carries the author's own comment on that rule — *"Gridlines
  are a reading aid, not data"*.
  *This bullet read **48** until 2026-09-10 and the true figure is **65**: `0008` §4.29
  measures 17 more in three shapes — 8 SVG backgrounds (`rect.lane`), 6 quiet fills whose
  element carries its role on `stroke` instead (`rect.track`, whose outline reads 5.98:1 in
  the same run), and 3 translucent washes that measure — four more are unjudged for want of a
  cascade. **The second of those is a shape this section did
  not have**: both bullets here are about *which elements* D5 admits, and that one is about
  *which property of one element*. The third is adversarial to repair — `auth-log-scan`'s
  author swept a band's opacity downward so the marks on it would clear 3:1.*
- **3 sites it excludes that have the included role.** `accent-color` on `car-price-ml/app`'s
  `#year-slider` and `#mileage-slider` and `mini-traceroute`'s `#numeric` is the visible part
  of a range slider and a checkbox — user-interface components by any reading. They pass at
  4.85:1, so nothing is hidden today; the classification is still the wrong way round.

**Links styled as buttons are outside D5, and this is a judgement rather than a measurement.**
Six `<a>` borders on `car-price-ml` measure 1.24:1, and `.actions a` gives them padding, weight
and a background, so "user-interface component boundary" reaches them on the wording. They are
excluded because the link is identified by its text and the border carries nothing the reader
needs. Stated here rather than left in `0008` §4.25's prose, because D5 claims to need no
judgement per page and this is one.

**Two bounds on what the control half can see**, both structural:

1. **The refused-selector list bounds the control count from below.**
   `mini-traceroute/docs/assets/styles.css:177` styles `#scenario` and `#base-port` from one
   declaration, and `.field input[type="number"]` is a `Refusal` — so the census found eight
   controls where there are nine.
2. **A control whose boundary is its own background is invisible by construction.**
   `contrast.sites` iterates `paint.PAINT - paint.GROUND`, so `#submit`, `#year-slider` and
   `#mileage-slider` — three controls declaring `border: none` — are never sites. Such a
   control can regress with the marks key green.

**The escape D5 does not take, stated because it was on the table.** SC 1.4.11 exempts a
graphical object whose information is also available in text, which would lift
`pl-review-sense`'s heatmap cells: **nine `rect.cell` fills below 3.0:1, two of them at
1.00:1**. *The first version of this paragraph said "the six 1.00:1 readings", which is neither
figure — portfolio-wide there are exactly two sites at 1.00:1 and both are these cells.* Taking
the escape needs the checker to tie a mark to the label carrying its value, which is a build
and not a rule. **Left out of D5 and available**: the cells report under the marks key until
something implements it.

### D6 — a site's own ground, and which way a boundary faces

The census measures a foreground against its ancestors and the preceding siblings that contain
it, so **an element that paints its own background is measured against what is behind that
background** rather than against it. Two published buttons read 1.00:1 and 1.06:1 for this
reason and are in fact 5.17:1 — a figure `car-price-ml/docs/app/styles.css:225` had already
written in prose.

**D6 says *occludes*, and the word is the decision.** An element's own opaque background hides
what is behind it, so the ground walk starts at the element and stops there — `_grounds`'s
ancestor loop already has that shape, since it `break`s at the first painted ancestor. *The
first version of this section said the own background is "a candidate ground", which in this
module's own vocabulary means appending to `found` — and `Site.ratios` returns one ratio per
ground while `_measured` takes the `min()`. Under that reading the two buttons keep 1.00:1 and
1.06:1 and the text half never goes clean.* Measured both ways over the eleven: occluding moves
28 readings and leaves **0** text failures; adding moves 18 and leaves **2** — the same two
buttons the whole re-derivation rests on.

**Two bounds, and the first was found by getting it wrong.** Reading a site's own ground
through `_GROUND_PROPERTIES` as shipped — which holds `fill` — makes every `<text>` its own
ground, because in SVG one property is a shape's paint *and* a text's foreground. That reading
reported 684 failures, all of them 1.00:1, every one the question *does this thing contrast
with itself*. So:

1. **Self-as-ground is `color` over `background`, never `fill`.**
2. **A border is a boundary and faces outward.** Its visibility comes from the colour on the
   other side, so it keeps the ancestor ground the census already uses. Correcting
   `mini-traceroute`'s `<button>` border to the button's own fill gives 1.00:1 — the wrong
   comparison, confidently computed.

### What both decisions cost — a repair in two schemes, and a key that still cannot gate

D5 admits the boundary of a real control, and **nine of those are failing**: seven form
controls on `car-price-ml/app` and two on `mini-traceroute`, every one
`1px solid var(--border)`. The owner took the repair on 2026-09-09 — a token for the control
boundary, `--border` unchanged everywhere else. **It is not two sibling pull requests**: `0007`
§5 clause 1 gives a border one house role and none of `_role_exception`'s four shapes reaches a
control boundary, which is still an edge — so the token fails a *gated* clause and the index is
amended before either sibling moves. `0008` §4.25 records the attempt and the two alternatives
it refused.

**Two things about that repair the census could not tell anyone.** The ninth control,
`#base-port`, is styled by a refused selector and so is absent from the figure the decision was
taken on. And **the census reads the light palette only** (`contrast.py:89`): the same border
measures **1.17:1 light and 1.29:1 dark**, so it fails in both and the repair is a two-scheme
repair. Every figure in this ADR and in `0008` §4.25 carries that qualifier.

**And the repair does not make the marks key gateable.** After it lands, **153 SVG sites still
measure below 3.0:1** — `auth-log-scan` 101, `ab-lab` 23, `pl-review-sense` 19, `car-price-ml`
7, `it-job-radar` 3 — and D5 puts SVG graphical objects inside the obligation. *The first
version of this section was headed "one repair and not a stage" and implied the key could enter
`GATE` once the controls landed.* It cannot, in any state: the argument this section makes
against the pre-D5 key — that it could never read clean — reaches the post-D5 key unchanged.
**S14b gates the text key and not the marks key**, and what would change that is the escape
above, or a further rule about which of the 153 a reader needs.

*This is the first time a decision in this ADR has required a page to change.* §4 reason 1
argued the census could be slow because the corpus was clean, and that was true of the harm it
knew about. It was not true of the corpus, and only the instrument could say so — and, as the
ninth control shows, not all of it even then.

## 8. D7 — the fourth house role, taken 2026-09-09 because D5 could not be applied without it

D5 says a user-interface component's boundary is owed 3:1. `0007` §5 clause 1's fourth
sentence says a border takes `--border`. On the two surfaces that carry a control those two
sentences cannot both be satisfied: `--border` measures **1.17:1** light and **1.29:1** dark
against `--surface`, the ground on the other side of the boundary. **The repair is not
unrepresentable in CSS; it is unrepresentable in this specification**, and that is what makes
this an index decision rather than a sibling one.

### The shape, and the two that were refused

**Refused — a fifth `_role_exception` shape.** Every one of the existing four is a case where
a border *stops being an edge*: a rail thicker than a hairline, a filled control's ground, a
border naming the role its own background names, an interaction state. A control boundary is
the box's edge — that is precisely what makes it the thing SC 1.4.11 asks about — so it takes
none of them, and a fifth would be role-agnostic like its siblings and would therefore exempt
`border: 1px solid var(--accent)` on a control just as readily. Wider than any sentence
licensing it.

**Refused — a page-aware rule.** The only design that could enforce *"on a control and nowhere
else"* answers through `selector.parse`, which returns a `Refusal` for
`.field input[type="number"]` — the selector on `mini-traceroute`'s own repair rule. The
strictest available design reports `undecided` on the one page the stage exists for, and
`undecided` never gates. It would also turn a pure CSS function into a page-dependent one.
*The most rigorous-looking option produces the weakest verdict where it matters, and only
tracing it against the corpus says so.*

**Taken — a second role in `_BORDER_ROLES`, and a fourth house role.** `border`, `border-color` and the four one-sided
borders now admit `--border` or `--border-control`. The edit is to `_BORDER_ROLES` and never
to `clause_1_usage`'s local `allowed`, because `_HOUSE_ROLES = _GROUND_ROLES | _BORDER_ROLES`
is derived and is the condition on all four exception shapes; widened locally, `_HOUSE_ROLES`
stays at three and a control token walks through the *filled control* exception as a ground.
A guard names that mutation and reddens on it.

### What the checker enforces, and what it does not

`1 usage roles` asks whether a border's role is in the set. It has no notion of which element
a selector reaches, so it admits `--border-control` on a table hairline exactly as readily as
on a control. **That gap is the decision, not an oversight**, and it is recorded as `c1.s4c`
with a `review` carrier so `python -m tools.spec` prints it on every run rather than leaving
it inferable from source. `c1.s7` — *"a page adding a fifth shape is stating something this
sentence does not describe, and the governing rule above decides it"* — is what decides a page
that stretches it.

The alternative wording, a family rule admitting any `--border-*` token, would have closed the
gap by making the sentence's claim exactly equal to the instrument's. It was refused because
it pins a **naming convention** where this clause's whole argument is that a role is what a
token means and not how it is spelled. `--border-control` is spelled so that the family rule
stays available later if that trade ever looks better.

### The pin, and the scheme nothing else can see

`--border-control` enters `PINNED` in both schemes: **`#808a9c` light** (3.27:1 on
`--surface`, 3.48:1 on `--bg`) and **`#596a89` dark** (3.14:1 on `--surface`, 3.41:1 on
`--bg`). `--surface` is the binding ground in both — it is the closer of the two grounds to
the token in either scheme, and it is the ground `0008` §4.25's 1.17:1 and 1.29:1 were
read on. The margin is deliberately close to 3:1, on `--accent-soft`'s precedent
(3.12:1 and 3.30:1): a boundary is a boundary and not an emphasis.

**The pin is doing work no other instrument here can do.** `contrast.py:89` takes
`palettes(css).get("light", {})`, so the census is structurally light-only, and
`clause_1_tokens`'s `PINNED` loop is the only per-scheme *value* check in the checker. Without
a dark pin, a surface that repairs its controls in the light `:root` and forgets the dark
override measures clean everywhere the instrument looks; with it, the dark palette inherits
the light value, which is not the pinned one, and the run says `FAIL 1 dark --border-control`.
The counter-argument — that `0007` §5.0 would rather each surface measured its own reason — is
real and loses to the fact that both surfaces share a palette to the byte, and that a
one-scheme repair is silent in every other direction.

### What this decision cannot prove, and what did prove it

**No published surface declares the token on the day the amendment lands**, so all eleven
committed surfaces print `1 light --border-control n/a — not declared` and the conformance
table is byte-identical before and after. The corpus cannot distinguish this change from its
absence. Five mutations can, and all five redden the guard that names them.

*One of those guards was designed wrong and the run corrected it.* The stage's design said
sweep all four exception shapes with `--border-control` as a second wrong role. Three of the
four then assert that a **conforming** declaration fails: `--border-control` on a border is
admitted by `role in allowed` and never reaches `_role_exception` at all. The sweep's own
comment already records that mistake being made once, one *shape* to the left; this was the
same mistake one *role* to the left. **Two of the four shapes discriminate, not one** — those
whose template declares a `background`, which are the filled control and *its own fill*. A
border-only shape cannot tell the difference, because a border admits the control role by the
rule and never reaches the branch. *The first version of this section said "only the ground
shape", which is one case narrower than the corpus, and the sweep shipped without that case
until the review measured all four.* **A guard whose premise is wrong fails on correct code,
which is the cheap direction; the expensive direction is a guard that passes over the defect
it names, and the two are told apart by running the mutation and not by reading the design.**

### What it does not do

It does not repair a page — the two sibling pull requests and the pointer bump follow, in that
order, and a page corrected before this amendment reddens a **gated** key. It does not make
the marks key gateable; §7's closing argument stands unchanged. And it does not reach every
control: `#speed` and `#numeric` on `mini-traceroute` carry **no author boundary at all**, so
after the repair two controls on that page keep the user agent's. That is a second mechanism
of census blindness beside the refused selector — *no rule reaches the element* rather than
*the rule is unreadable* — and it belongs beside D5's bound rather than being re-derived by
whoever notices the page next.

## 9. D8 — what a verdict may rest on, taken 2026-09-10 because §4.27 left it open

`0008` §4.27 recorded it as left open deliberately: `Ground.guaranteed` distinguishes a ground
an ancestor structurally contains from one geometry merely places under the element, and no
verdict path read it. The `contrast marks` `GATE` row named that as one of two things standing
between the key and a gate. This is the decision, and **it is not the one that row anticipated**.

**The question is not evidence quality.** A sibling ground is arithmetic on coordinates written
in one shared system — siblings share a parent, and `geometry.bounds` returns `None` for
anything carrying a `transform`. Its failure modes are over-inclusion at a shape's edge and the
absence of occlusion between two containing siblings; both make the checker *stricter* than the
page rather than wrong about it. What it is not is a weaker claim about what colour sits behind
the mark.

**Three measurements decided it, and two of them are in the pages rather than in the checker.**

1. `pl-review-sense`'s `.cell-share` at 2.69:1 — `0009` §7 row 12, **the only live failure this
   system has ever caught** — is an SVG `<text fill>` measured against the sibling `rect.cell`
   beneath it. `paint.TEXT` is `frozenset({"color"})`, so SVG text is a *mark*, and its ground
   is geometry-placed. Against the card it clears by an order of magnitude.
2. `auth-log-scan/src/auth_log_scan/site/assets/styles.css:142` records the author's own sweep:
   *"The event marks are emitted after the band at the same y and height, **so the band is
   their ground**"*, with five mark/band pairs under 3:1 as published before S7 and a repair
   made by moving the *band's* opacity from 0.45 to 0.25 and 0.28 to 0.15. **The page's own
   figure is 3.09:1 and the checker reads that pair at 3.24:1**, and the gap is a third bound
   rather than a discrepancy — see below. Either way it is the reading an author had to sweep
   opacities in 0.01 steps to reach, and its ground is geometry-placed.

   *The first version of this section said 3.09:1 reproduces from the markup and that it is
   the only reading in the corpus near the bar. Neither survived the review. `car-price-ml`'s
   `.chart .bar` sits at 3.12:1 nine times on a **guaranteed** ground, which is nearer the bar
   than the checker's figure for this pair. The claim that survives is narrower and is the one
   the argument needs: the near-bar reading an author deliberately swept to is geometric.*
3. Every one of the 79 sites whose only failing ground was geometric **clears its guaranteed
   ground between 3.98:1 and 8.16:1**. That range is not headroom, it is a signature: a mark's
   guaranteed ground is the page behind the chart, which any legible chart clears by
   construction. A rule resting verdicts on guaranteed grounds alone would refuse approximately
   nothing on an SVG chart, forever.

**So `guaranteed` was the wrong axis, and the right one was already in the module.** 65 of the
79 are `auth-log-scan`'s `circle.ev-failed` measured against **another `circle.ev-failed`** —
same rule, same declared `var(--accent)`, differing only by the `fill-opacity` the data writes
per element, giving 1.26:1 between two instances of one dot. **966 failing (site, ground) pairs
across 65 sites, about fifteen overlapping neighbours each.** `_grounds`' docstring has
described that population since S13 and calls it `0008` §3.11's collapse; the rule meant to
exclude it compared the site's *resolved, un-composited* colour with the ground's *composited*
one, so a shared token at two alphas escaped it. **The exclusion was aimed at these sites and
missed them on a unit mismatch rather than on a judgement.**

D8 states the rule where the criterion states it — a graphic is owed distinction from what it
is drawn on, not from other instances of itself — and has the instrument approximate it by
declaration identity, on D5's precedent: *the rule is the criterion's and the partition is the
instrument's.* `0007` §5 clause 1 carries it as `c1.s6c`.

### What it moved, measured at `1760f60` before and after

**153 → 88 obligated mark failures**, of 739 measured. Per surface: `auth-log-scan` 101 → 36,
and `ab-lab` 23, `pl-review-sense` 19, `car-price-ml` 7, `it-job-radar` 3 unchanged. The 65
excluded grounds are **counted under `same_colour` and printed by `contrast ground`** — 966
pairs — so nothing was dropped, and every one of the 65 sites keeps its ancestor ground and
stays measured.

**`contrast text` is byte-identical**, on the eleven committed surfaces and on all twelve under
`--fetch`. That was predicted structurally rather than hoped for: `geometry.bounds` answers only
for `rect` and `circle`, so no HTML element can ever be a geometry-placed ground, and `color` is
an HTML property in this corpus. A run that disagreed would have been a finding about the
structural argument.

### The 14 D8 leaves failing, and why they are a second decision

The 79 were not one population. Fourteen are a mark against a **different** mark, so declaration
identity does not reach them:

| surface | site | ground | ratio |
|---|---|---|---|
| `auth-log-scan` | `rect.ev-invalid` fill ×10 | `circle.ev-failed` | 1.30:1 |
| `ab-lab` | `rect.marker-corrected` fill ×2 | `circle.marker-naive` | 1.27:1 |
| `auth-log-scan` | `circle.ev-accepted` stroke ×1 | `circle.ev-failed` | 1.38:1 |
| `car-price-ml` | `line.spread-cap` stroke ×1 | `rect.bar served` | 2.50:1 |

**They are left failing on purpose, and the argument against them is not D8's to make.**
`auth-log-scan/styles.css:133` answers them directly — *"**Shape carries the meaning and colour
repeats it**, so the chart survives greyscale and colour blindness: a failure is a filled dot,
an accepted login a ring, a probe of a non-existent account a diamond"* — and the same holds for
`rect` against `circle` on `ab-lab`. If shape carries the distinction, colour contrast between
two mark classes is not what SC 1.4.11 asks for. But that is a claim about **role**, which is
D5's subject and not this one, and D5 already carries two recorded errors of exactly that kind.
Deciding it here would fold a role judgement into a ground rule.

### What this does not do

It does not make `contrast marks` gateable. The pages' half of the `GATE` row stands, and its
composition is now printed by the run rather than described in the reason: of the surviving 88,
**48 are the gridline and axis strokes §7 already records D5 as admitting wrongly**, 9 are the
`rect.cell` heatmap fills §7 records as the escape D5 left available and unimplemented, 14 are
the table above, and 17 were called a remainder. **`0008` §4.29 measured that remainder and it
is not a separate question**: all 17 are this same partition error in three shapes, which puts
it at 65 rather than 48. **Three separable questions, of which D8 is one.**

It does not touch `contrast text`, for the structural reason above. And it does not correct the
anchor-point approximation in `geometry.contains`, which tests the site's *anchor* against the
ground's bounds while its docstring says *covers*. Requiring full-shape containment would drop
the 65 as a side effect — two equal-radius circles cannot contain each other — and it is
**refused here**: `<text>` has an anchor and no bounds by design (`ADR-0004` §4's deferred
geometry), so it would blind the checker at exactly the site in measurement 1. It is worth
taking later, asymmetrically and for its own reason — a mark straddling a band edge is measured
today against a ground covering only part of it — and its corpus effect is unmeasured.

### Three bounds, stated because they are judgements

A page that genuinely needs two instances of one mark told apart — overlapping points that must
be counted — states that with a separator painted by a **different** declaration, which stays
measured; the exclusion cannot reach it. And a translucent overlay reusing the declaration of
the thing beneath it would be excluded wrongly; the site keeps its ancestor ground and stays
measured, so the cost is a missed reading and not a wrong one. *The second bound was met while
this was being written: a first fixture painted `.cell-share` the same token as its cell and the
guard went red, correctly.*

**Third: `_opaque_behind` walks ancestors only, so a translucent ground with an opaque
*sibling* under it composites over the ancestor instead.** `auth-log-scan`'s `.window-band` at
alpha 0.25 is read over `body` rather than over the `.lane` beneath it, giving 3.24:1 where the
page's own sweep computed 3.09:1. Five verdict-bearing readings in the corpus sit on that
shape, all on that surface, and **all of them err permissive** — the checker reports a ratio
better than the page's. It is stated here rather than repaired because the walk terminating is
what makes it structural, and a sibling walk needs the occlusion order this census does not
have. Found by the review of D8, on the very reading D8's second measurement rests on.
