# The clause registry

Date: 2026-09-07
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`0004_what-carries-the-page-spec.md`](0004_what-carries-the-page-spec.md) (the
carrier decision this refines), [`../audit/0007_divergence-and-the-page-spec.md`](../audit/0007_divergence-and-the-page-spec.md)
§5–§6 (the prose enumerated), [`../audit/0009_the-review-of-the-whole-system.md`](../audit/0009_the-review-of-the-whole-system.md)
§3.2 and §7 rows 5 and 13, and `#85`

---

## 1. The decision

`tools/spec.py` holds **one row per normative sentence** of `0007` §5–§6: an id, a citation, the
sentence quoted verbatim, its carriers, and — where the sentence has more than one reading — the
reading that was settled. `python -m tools.spec` prints the coverage table and every uncarried
sentence, and **exits 0 whatever it finds**. Its guards, in `tests/test_spec.py`, gate on the
registry being malformed and never on the pages' state.

## 2. The problem

`0009` §3.2 records the same defect landing three times: a clause sentence carried by nothing,
invisible because **nothing enumerated the sentences**. `0008` §3.7 had already prescribed the
remedy as a discipline — *"a thing to check for the whole of S6 and S7, not a one-off"* — and
§4.11 records the same substitution being made again, in the same document. An instruction that
was issued, acknowledged and then violated is the definition of a missing artifact.

## 3. The rule the registry's correctness depends on, which no test can carry

**It is authored by reading `0007` §5 top to bottom, and never by reading `clauses.py`.**

A registry composed from the checker's function list reproduces the checker's omissions exactly
and then reports full coverage over them — the defect it exists to end, committed in the act of
closing it. That is `0008` §3.7's *"composed from the frozen table's columns rather than from the
normative clauses' sentences"*, one artifact along.

The rule paid for itself immediately. Walking the prose found **two sentences carried by nothing
that the whole-system review had not seen**:

| sentence | state |
|---|---|
| clause 7's first, *"Type is the system stack"* | `font-family` appears nowhere in `tools/pagespec/`, and `clause_7_webfont`'s `PASS` detail string is literally `system stack` — **the checker prints the sentence as a verdict it never computed** |
| clause 3's `data-scroll="by-design"` escape | appears nowhere in `tools/pagespec/`. It makes the checker *stricter* than the spec rather than looser, which is why it survived |

*Both strings now occur in `tools/spec.py` — as the rows recording their absence, which is the registry doing its job and not a contradiction. The claim is about the checker.*

Neither was fixed. Both are uncarried rows citing where they are picked up, which is
`CLAUDE.md`'s *record a correction rather than quietly fixing it* applied to the registry's own
discoveries.

## 4. What gates, and what does not

`carriers == ()` is **never** a failure. `0007` §5's governing rule means no instrument can decide
whether an uncarried sentence is open work or a decision, which is the argument
`tools/pagespec/__main__.py` already makes for `UNDECIDED` and for the role census.

What the guards refuse is a registry that has stopped describing the world: a quote that no
longer appears in `0007`, a carrier naming a finding key the checker does not emit, an emitted key
no sentence claims, an uncarried row with nowhere to be picked up, a `GATED` prefix outside the
vocabulary. All of it in the `core` job — no submodule, no network, no dependency.

**`GATED` is untouched.** It stays a literal tuple that nobody derives, and the registry only
reads it. Deriving it from a `gated:` field on a row was considered and rejected: it would make
the ceiling guard's failure message incomplete (a third cause — *a registry row flipped* — that
the message does not name), and it would put the ratchet in a file edited routinely, against
`CLAUDE.md`'s rule that `GATED` is not hand-edited as part of unrelated work.

> *Amended 2026-09-08 — `GATED` **is** derived now, and by `ADR-0006`, which is a different
> derivation from the one refused here.* This paragraph refused deriving it from **this**
> registry, in `tools/spec.py`, and the second reason is why: that file is edited whenever a
> normative sentence is read, and the ratchet must not move with it. `ADR-0006` derives `GATED`
> from `GATE` in `__main__.py` — the ratchet's own file — so the second reason does not reach
> it and the decision above still holds for `tools/spec.py`.
>
> **The first reason does reach it, and was inherited unnamed for one commit.** The ceiling
> guard's message named two causes while a third — a row demoted from `gated` to `report-only`
> — un-gated a clause across all 510 tests, green. The `code-reviewer` pass on S11 found it and
> cited this paragraph, which had predicted the failure for a derivation nobody took. The
> message now names the third cause and `report_only()` is pinned. *A refusal's stated reason
> outliving the refusal is worth more than the refusal was.*

## 5. What the corpus refuted

Two invariants the design specified did not survive contact:

- ***every emitted key is claimed by exactly one row*** is false. `8 separator` carries clause 8's
  rule **and** its scoring definition, which `0007` states separately because §8.5 records the
  tally being wrong three times. The invariant is one **clause**, not one row.
- **prefix matching must attribute to the most specific claiming prefix.** `1 dark` is the
  override's presence and `1 dark --positive` is a pinned value — genuinely nested, and a plain
  sweep reads the second as claimed twice.

## 6. The limit, registered rather than implied

**Nothing detects a sentence that was never entered.** Guard 1 catches a quote drifting from the
document; the inverse has no mechanism and cannot have one, because §5 interleaves normative
sentences with descriptive *"what is already true"* notes by design, so no parser can tell them
apart. Its only carriers are this ADR and the `code-reviewer` pass that closes every stage.

That pass ran, and it returned **three normative fragments with no row and one truncated quote** —
clause 1's condition on the four exception shapes, clause 5's *"and a favicon"*, §5.0's typography
carve-out, and clause 9's scope sentence. All four are entered. The limit is real, and so is the
carrier: this is the carrier working, not an escape from it.

**Amending `0007` §5 means adding a row.** That sentence is the whole of the procedural half, and
it belongs here rather than in `0007`, which is `accepted` and whose stability is what makes
guard 1 affordable.
