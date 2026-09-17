# A clause may only be asked where the portfolio writes the bytes

Date: 2026-09-17
Status: accepted — the owner chose this over the alternatives on 2026-09-17, together with the
route for `0009` §7 row 11. **§6 carries the steps and their state**; the commit that introduces
this document also lands the first of them, so no sentence here says the work is pending.
*An earlier draft of this field read "No step has landed yet" in the commit that landed one —
`0011` §5's rule that a sentence preceding its state is the same defect as one outliving it.*
Author: Piotr Cząstkiewicz + Claude
Related to: [`0007`](../audit/0007_divergence-and-the-page-spec.md) §2 and §6 clause 9 (the rule
this refines and the sentence it repairs), [`0009`](../audit/0009_the-review-of-the-whole-system.md)
§7 row 11, §9 and §14 (the open row and its measurement),
[`0012`](../audit/0012_what-publication-invalidated.md) §4 F-1 and F-8 (the two findings this
answers), [`ADR-0004`](0004_what-carries-the-page-spec.md) §5 and K-c (what carries what),
[`failure-classes`](../reference/failure-classes.md) `ST-4`

---

## 0. The number, taken deliberately for the fourth time

`ADR-0010` collides with `docs/audit/0010`, the portfolio audit — after `ADR-0007`/`0007`,
`ADR-0008`/`0008` and `ADR-0009`/`0009`, each of which `CLAUDE.md` names.

*No ordinal is given, and this paragraph gave one until review.* It said *the fourth*, two
sentences before arguing that the count should be removed rather than corrected — and the ordinal
is not even well defined: `docs/adr/` runs 0001–0010 and `docs/audit/` 0001–0012, so **every**
number up to 0010 is taken on both sides, and the four `CLAUDE.md` lists are the ones whose bare
form is actually ambiguous in live prose. That narrower criterion is the useful one and it was
never written down, which is how a list can go stale the way a figure does.

`ADR-0009` §0 already refused the obvious escape — skipping to a free number moves the collision
rather than removing it, and a reader who learns *a bare number means the audit document* has a
rule that works everywhere. The rule is kept and the price is paid again.

**What changes is the bookkeeping, and it changes by subtraction.** `CLAUDE.md` said *three
numbers are now taken twice*; this document makes it four, and the count is **removed** rather
than corrected. `docs/reference/failure-classes.md` `ST-3` records why: `#125` repaired two stale
counts *"by removing the count rather than correcting it: a figure in prose beside an instrument
that computes it is the defect, and correcting it only sets the next staleness date."* The map now
says the collision exists and how to read it, and a reader who wants the number can count the
`docs/adr/` directory against the audit series.

## 1. The question, which two open items turn out to share

Two items had been open in the record for different reasons and are one question.

**`0007` §6 clause 9's second sentence** said agreement between two pages *"cannot be checked
without coupling two public repositories to a private index, so it is a review item"*. `0011` §6
route A published the index on 2026-09-17, so the premise went with it while the sentence stayed
byte-identical — `0012` F-1, class `ST-4`.

**`0009` §7 row 11** wants the profile README brought into the system, and §14 measured why the
row's own prescription — *"at minimum a `Surface` read by `--fetch` in `live`"* — fails: the
clauses it would arm are properties of GitHub's chrome and not of the README. §14 names the gap
precisely and leaves it: *"which clauses can even be asked of a surface somebody else renders"*.

Publication dissolved the first blocker and left the second. **Both are asking who owns the bytes
a verdict rests on**, and neither can be answered by the instrument: the checker reads whatever
surface it is pointed at and has no notion of authorship.

## 2. The decision

> **A clause may be asked of a surface only where the portfolio writes the bytes that decide the
> verdict.**
>
> The criterion is not an opinion. **If a verdict moved and no commit in the portfolio moved it,
> the clause belongs to the host.**

This **refines** `0007` §2 rather than contradicting it. §2 forbids answering about a rendered
page from something that is not that page; the authorship test forbids *asking a question the host
answers*. Both hold at once: read the real bytes, and ask only about what the author controls.
`wroclaw-air-insights` is not a counter-example — its page is rendered by Pages from a generator in
its own repository, so the bytes are the portfolio's even though no HTML is committed.

**Two limits, so the test cannot become a way out of any clause anyone dislikes.**

1. It applies **per (clause, surface) pair**, never to a clause in general. Clause 6 is the
   portfolio's on twelve committed pages and the host's on a rendered profile.
2. The answer must be **measured, not argued.** A claim that a clause is the host's needs a
   verdict that moved without a commit, or a reading of the markup showing which party emits it.

### The measurement this rests on

Between 2026-09-08 and 2026-09-17 the rendered profile moved, with **no commit in this portfolio
touching it**:

| what `0009` §14.1 read, 2026-09-08 | the same reading, 2026-09-17 |
|---|---|
| `<title>` `P0w3r223 (Piotr Cząstkiewicz) · GitHub` | `P0w3r223 (P0w3r223) · GitHub` |
| headline `Piotr Cząstkiewicz P0w3r223` | `P0w3r223 P0w3r223` |
| anchors ending at the profile **10** | **2** |

Taken the way §14.1 says it took the original — `sources._fetch` on `https://github.com/P0w3r223`,
parsed by `render.parse`. The README's own edit of 2026-09-17 cannot explain the anchor figure:
`clause_6_back_link` counts only anchors whose **path equals** the profile, which excludes every
repository URL, and the edit added repository links. **The chrome moved.** That is the test's own
instrument returning a positive on its first outing, and it is why a gated clause cannot rest on a
surface a third party renders.

## 3. Which clauses pass on the profile, and the convergence that settles the design

| clause | who writes the deciding bytes | may be asked |
|---|---|---|
| 1 (tokens, dark, literals, usage, composited, `contrast *`) | the host's stylesheets | no |
| 2 tiles, 3 tables | GFM sanitises the class names the clauses key on | no |
| 4 `<title>`, `4 h1`, `4 eyebrow` | the host composes the title and the account header; Markdown has no eyebrow mechanism | no |
| 5 card meta, favicon | the host | no |
| 6 back-link | **measured: the host** — 10 anchors to 2 with no commit | no |
| 7 webfont | the host's stylesheet | no |
| **8 separator** | the owner types the digits and the separator | **yes** |
| **§5.0's quotation rule** | the owner types the figures | **yes** |
| **9 bridge** | the owner types the numbers and the bridge | **yes** |

**The convergence is what decides the implementation, and it was not designed for.** The clauses
that pass the test are exactly the clauses **about text**, and clauses about text do not need HTML.
The mismatch §14.1 costed — *"the second is Markdown and the whole checker reads HTML"* — applies
only to the clauses the test already excludes. So the value row 11 is after (§14.3's `25–66 %`
against `ab-lab`'s `25.3 %`/`65.7 %`; §9's asymmetry) sits entirely inside the passing set, and the
row's prescription sits entirely inside the refused one. **Row 11 fails on authorship, not on
cost** — which is a stronger reason than §14.1 had, and it is why the row was never small.

## 4. What this answers

- **`0012` F-1.** Clause 9's limit is restated from the clause's own scope instead of from the
  world: which figures the clause reaches is a judgement `c9.s1b` already assigns to a reader, and
  no instrument makes it. A premise internal to the text cannot expire the way privacy did.
- **`0009` §7 row 11.** The prescription is refused and the value is kept. The owner's decision of
  2026-09-17 is the **separate instrument** — a module beside `tools/spec.py` and
  `tools/citations.py` reading the raw README, printing and exiting zero, with no contact with
  `SURFACES`, `GATE` or `_sweep`.
- **`0012` F-8.** Twenty-one lines in twelve `CLAUDE.md` call this repository the private index.
  The test says why the index cannot carry a guard for them: those bytes are the siblings'. The
  index may report the claim as a census; it may not refuse on it.

**It also answers `0012` F-1's "one stage" by refuting it.** F-1 argued the two must ship together
because each would amend `0007` §5–§6 and move `tools/spec.py`'s pin in the same commit — *"two
windows in which the one stable normative text is in flux."* Under this decision **row 11 does not
touch `0007` at all**; it adds this ADR and an instrument. The second window does not exist and the
cost F-1 reasoned from is zero, so it is two stages with clause 9 first. `0010` §3.5 also puts *a
change to `0007`* and *a new guard in `tools/`* in its second column **separately**, so one pass
arming both triggers has the larger blast radius, not the smaller.

## 5. Options considered and refused, each by a measurement

### For row 11 — the profile as a thirteenth `Surface`, with a clause mask

Refused on two mechanisms in the code, not on taste.

1. **A fetch-only surface on `github.com` can silence the ratchet for the twelve.**
   `sources.load` records `errors[surface.name]` when a `must_fetch` surface fails, and `_sweep`
   answers a non-empty `errors` with `pytest.skip("the corpus is incomplete, so neither half of
   the ratchet can claim anything about it")`. **A skip is a pass** (`0010` §3.6 observation 2).
   GitHub rate-limits CI runners, so every 429 would take the floor and the ceiling out for the
   eleven real pages. Today the only fetch-only surface is `wroclaw`, on its own Pages host.
2. **A 429 on a same-origin stylesheet gates.** `sources.origin_answered` treats any status
   below 500 as *the origin answered*, so a 429 lands in `unreadable` rather than `unreachable`;
   `_unread_same_origin` filters only `THIRD_PARTY`. An absolute `github.githubassets.com` href is
   safe, but a relative stylesheet href in the host's chrome resolves to `github.com` and a 429
   there would refuse the build. That breaks *a wire failure is `undecided`, never `fail`* in a way
   no decision here can guarantee, because the markup is the host's to change.
3. A clause mask is **the quiet clause drop-out** that
   `test_every_clause_reaches_a_verdict_on_every_published_surface` was written to refuse — but
   *that guard would not fire here*, and the distinction matters. It is parametrised over
   `COMMITTED`, which is `[s for s in SURFACES if not s.must_fetch]`, and the refused surface is
   fetch-only; a masked key simply reports no status, so no half of the ratchet sees it either.
   **So this third reason is an argument from the shape of the guard rather than a guard that
   fires**, and it is stated that way because mechanisms 1 and 2 are checkable in the code and
   this one is not. *An earlier draft cited it as though it would catch the mask.*

And the route would arm a latent defect it depends on: `clause_6_back_link` ignores the query
string, so `?tab=followers` and `?tab=following` count as links back to the profile. No committed
page has such an href, so the defect is unreachable on today's corpus — and pointing the clause at
the rendered profile is exactly what reaches it.

### For clause 9 — making it a carried verdict in the index

Refused by its own scope sentence. `c9.s1b` bounds the clause to *"a figure the page presents as a
result … not every integer on it"*, carried by `_human` with the note that **the bound is a
judgement**. An instrument can find a repeated digit string; it cannot decide which digits the
clause reaches, so a carried clause 9 would flood on `4` and `2026` — *"unenforceable and would be
ignored"*, in that sentence's own words. Two surfaces agreeing is also as unstable as `served` and
for the same reason, so even carried it could only enter as `report-only`.

*And `report-only` is what the prose means by "a review item"* — `contrast marks` and `served` are
the precedent, and S13 was a census before S14 was a verdict. The new wording says census
explicitly rather than leaving a later reader to rediscover that the vocabulary already existed.

### For clause 9's limit — resting it on the gitlink instead

Refused because it expires. *"The index reads each sibling at its pinned gitlink"* is true today and
stops being true the day `--fetch` becomes the default, which `0009` §3.1's C1 already contemplates.
A premise that can expire without a commit is the defect this document is repairing; choosing
another one would only set its date.

## 6. Consequences

Each row carries its state, so this list cannot be read as a plan after it stops being one.

1. **Landed with this document.** `0007` §6's closing paragraph is rewritten, with
   `tools/spec.py`'s `c9.s2` quote and carrier in the same commit — the guard compares normalised
   text and reddens on either half alone, proven by a battery that mutates each half in turn.
   `0007`'s `Status` field enumerates its amendments and gains this one.
2. **Landed.** The paragraph's trailing phrase goes with it. *"carried in §8's list"* names `0007`
   §8, which is **`## 8. Corrections to the record`** and holds no such list; the carrier is §7's
   bullet, and the list the phrase meant is §9 row 3, moved to `0008` by `ADR-0004` §5.
   `tools/citations.py` reports this resolved because the section exists — the blind spot `0012`
   §2 names, in a phrase being rewritten anyway.
3. **Open, and next.** Clause 6's query-string reading is repaired in its own pass, before any
   instrument is pointed at a rendered surface. It is a **false `FAIL`** on a gated clause, and
   `sources.py` states the policy: *a false gate is worse than a missing one*. `0009` §7 row 2 is
   the precedent for fixing a latent defect before the stage that would reach it.
4. **Landed.** `0009` §14.1's *"four gated clauses at once"* is an erratum: measured with
   `sources.load` and `clauses.check` against that surface, it is **six** — `1 tokens`, `1 dark`,
   `3 tables`, `4 eyebrow`, `4 title`, `6 back-link`. Clause 1's and clause 3's failures do not
   degrade to `UNDECIDED` because all seventeen profile stylesheets are absolute and therefore
   `THIRD_PARTY`, which `_undecided_where_the_stylesheet_is_incomplete` excludes. *An earlier draft
   of this row said three, having asked `clause_4_opening` alone* — which could only answer about
   clause 4, and is the same *reasoned rather than run* defect the erratum was written to fix. The
   six strengthen §3 rather than disturbing it: `1`, `3` and `4` are assigned to the host there.
5. **Landed.** `failure-classes.md` `ST-4` keeps `0007` §6 `c9.s2` in its *Defined* list with that
   site marked closed, and the class is not retired. **No tally is written into either file, and
   an earlier draft of this row wrote one** — it said *five of its six sites remain*, where `0012`
   §4 already marks F-2, F-3 and F-10 *corrected here*, so closing F-1 leaves **F-7 and F-8**. A
   count beside a table that answers it is what `ST-3` is about, and this row argued for removing
   one while adding another.
