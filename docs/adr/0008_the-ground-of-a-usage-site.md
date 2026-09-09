# The ground of a usage site, and why the census comes first

Date: 2026-09-09
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`0004_what-carries-the-page-spec.md`](0004_what-carries-the-page-spec.md) §4 (the
geometry half, deferred and unowned — this reaches part of it and says how it differs),
[`0005_the-clause-registry.md`](0005_the-clause-registry.md) (where `c1.s6b` enters),
[`0006_the-gate-registry-and-the-twelfth-surface.md`](0006_the-gate-registry-and-the-twelfth-surface.md)
§3 (the `pending` state D3 depends on),
[`../audit/0007_divergence-and-the-page-spec.md`](../audit/0007_divergence-and-the-page-spec.md)
§5 clause 1 and §7, [`../audit/0008_the-rollout-ledger.md`](../audit/0008_the-rollout-ledger.md)
§3.11 (the design this amends) and §4.23 (what the first commit measured),
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
