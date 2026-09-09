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
| **D3** | At S14 the two verdict keys enter `GATE` as **`Ratchet(prefix, PENDING_STATE, reason)`**, not `REPORT_ONLY_STATE`. `contrast ground` stays in `NOT_A_CLAUSE` and `NOT_A_SENTENCE` permanently |
| **D4** | `0007` §5 clause 1 gains the sentence that makes a usage site's threshold an **obligation**, entering the registry as **`c1.s6b`**. Its wording is taken **after** the census prints, because `test_spec`'s guard pins the quote for as long as the sentence exists |
| **D5** | The marks key takes its obligation **by role** — visual information required to identify a user-interface component, and parts of a graphic required to understand the content — and **not** from structural decoration: table rules, card edges, the rule over an `<h2>`. The checker approximates that partition **by property name**, which is the instrument and not the rule; §7 names the two places the approximation is known to be wrong. Taken 2026-09-09 against the census |
| **D6** | A site's own opaque **background occludes** what is behind it, so the ground walk starts at the element and stops there. Its own `fill` does not, and a **border faces outward** — measured against the other side of the boundary, never against what the element itself paints. §7 |

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
two places:*

- **48 sites it admits that have the excluded role.** `line.grid` (22), `line.lane-line` (15),
  `line.axis-line` (8) and `line.axis` (3) are gridlines and axis rules, painted the same
  `--border` `#e3e7ee` at the same 1.17:1 as the table hairlines D5 excludes. They fall inside
  only because they are `<line stroke>` rather than `border-bottom`, and
  `car-price-ml/docs/index.html` carries the author's own comment on that rule — *"Gridlines
  are a reading aid, not data"*.
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
