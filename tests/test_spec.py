"""The clause registry's guards — on the registry's shape, never on the pages' state.

**The split matters and is the whole design.** `carriers == ()` is never a failure here: an
uncarried sentence is honest open work, and `0007` §5's governing rule means no instrument can
tell one from a decision. What these guards refuse is a registry that has stopped describing
the world — a quote that no longer appears in `0007`, a carrier naming a finding key the
checker does not emit, an emitted key no row claims, an uncarried row with nowhere to be
picked up, and a `GATED` prefix outside the vocabulary. `tools/pagespec/__main__.py`'s
`_gated` docstring makes the same argument about `UNDECIDED`: a gate that reddened on those
would be a gate on the checker's own honesty.

Everything here runs in the `core` job. Not one guard needs a submodule on disk or a network,
which is deliberate — the registry's subject is this repository's own claim about what it
carries, and that claim must stay checkable when the twelve trees are absent.
"""

from __future__ import annotations

import pathlib
import re

import pytest

from conftest import NOT_A_CLAUSE, fixture, loaded
from tools import spec
from tools.pagespec import __main__ as report
from tools.pagespec import clauses

#: A page rich enough to emit the whole finding vocabulary, so guards 2 and 3 can compare
#: against what the checker really says rather than against a list of what it is believed to
#: say. Measured 2026-09-07: this emits every key the eleven committed surfaces emit, plus
#: `stylesheets`, which they do not currently produce because none of them has an unreadable
#: same-origin sheet. `1 composited` needs a `color-mix()` usage site and nothing else does.
_EVERY_KEY_HTML = (
    '<html><head><title>a claim</title></head><body>'
    '<p class="eyebrow">eyebrow</p><h1>a claim about something</h1>'
    '<div class="kpi">1</div>'
    '<div class="table-wrap"><table><tr><td>1 000</td></tr></table></div>'
    '<a href="https://github.com/P0w3r223">profile</a>'
    '</body></html>'
)
#: `clause_1_composited` scans `background`, `background-color`, `fill`, `stroke` and `color`
#: for `color-mix(`, and `opacity` for a value strictly between 0 and 1. A first version of
#: this rule used `border-color`, which is in neither list, so the key was never emitted and
#: the width guard above is what said so.
_COMPOSITED = "\n.mark { background: color-mix(in srgb, var(--accent) 40%, transparent); }"


def _emitted() -> set[str]:
    css = fixture("house_palette.css") + _COMPOSITED
    findings = clauses.check(
        loaded(_EVERY_KEY_HTML, css, unreadable=[("local.css", "unreadable")]))
    return {finding.clause for finding in findings}


def test_the_synthetic_corpus_still_reaches_every_key_the_registry_claims():
    """Guards 2 and 3 are only as wide as this page. If it stops emitting a key, they stop
    checking it — silently, and in the direction that reports more coverage than exists.

    So the width is asserted first and separately, and the failure names the key. This is
    `0008` §4.4's lesson: a guard proved on one shape of two is a guard on neither.
    """
    emitted = _emitted()
    for prefix in spec.index_refs():
        assert any(key.startswith(prefix) for key in emitted), (
            f"the registry claims {prefix!r} and the synthetic page emits no such key; "
            f"guards 2 and 3 would pass while covering less than they say"
        )


def test_the_synthetic_corpus_reaches_every_key_the_checker_can_name():
    """The other direction, and the one the width guard above cannot see.

    That guard asserts *registry → synthetic page*. A clause added to `clauses.py` whose key
    this page never triggers would be claimed by no row with nothing reddening — `0009` §3.2's
    own class, one level up from the sentences the registry enumerates. Read statically off
    the source rather than by calling anything, because the point is to find a key the
    synthetic page does *not* produce.
    """
    source = pathlib.Path(clauses.__file__).read_text(encoding="utf-8")
    literals = set(re.findall(r'Finding\(\s*"([^"]+)"', source))
    # Only what needs exempting. Subtracting the whole set also excused `stylesheets`,
    # which this page *does* reach — half the guard switched off to accommodate one key.
    needs_a_fetch = frozenset({"served"})
    unreached = sorted(literals - _emitted() - needs_a_fetch)
    assert not unreached, (
        f"`clauses.py` can name {unreached}, which the synthetic page never emits — so no "
        f"guard here would notice those keys having no normative sentence behind them"
    )


def test_every_quote_is_still_the_document_s_own_words():
    """Guard 1. The registry's rows are quotations, and a quotation that has drifted from the
    document is a rule nobody is enforcing under a name somebody trusts."""
    normative = spec.normative_text()
    missing = [clause.id for clause in spec.CLAUSES
               if spec.normalise(clause.quote) not in normative]
    assert not missing, (
        f"{missing} no longer appear in 0007 §5-§6 — either the document moved and the "
        f"registry did not follow, or the quote was never the document's own words"
    )


def test_the_normative_slice_fails_by_naming_the_heading_it_could_not_find():
    """A renamed section must not arrive as twenty-odd drifted quotes.

    Guard 1's failure mode is the thing being guarded here: `normative_text` raising with the
    heading's name is what stops a section rename from being diagnosed as portfolio-wide
    quote drift, which is the wrong answer printed once per row.
    """
    original = spec.NORMATIVE_FROM
    spec.NORMATIVE_FROM = "## 5. A heading this document does not have"
    try:
        with pytest.raises(AssertionError, match="is not in the file"):
            spec.normative_text()
    finally:
        spec.NORMATIVE_FROM = original


def test_the_slice_is_bounded_below_so_a_descriptive_restatement_cannot_satisfy_a_quote():
    """§3 restates several clause sentences as observations and §8 records corrections to
    them. A quote matching in either would let a normative sentence drift out of §5 with the
    guard still green.

    **This guard shipped green over its own defect and was caught in review.** Its first
    version asserted a quote's occurrence count in the *whole document* and then restated
    what `normative_text` already raises on — so moving `NORMATIVE_FROM` to the document's
    title, which pulls all of §3 into the slice, left the entire file passing. The fix is to
    assert against the slice and to name text that exists only outside it. The ninth
    appearance of the class `0008` §3.9 records, in the stage whose subject is that class.
    """
    normative = spec.normative_text()
    assert spec.normalise("A tile is `.kpi`.") in normative, "the slice lost §5"
    assert "The conformance table" not in normative, "the lower bound has let §3 in"
    assert "Corrections to the record" not in normative, "the upper bound has let §8 in"


def test_every_index_carrier_names_a_key_the_checker_actually_emits():
    """Guard 2. A row pointing at a finding key that does not exist reports coverage the
    instrument does not provide — which is the registry telling the lie it exists to stop."""
    emitted = _emitted()
    for clause in spec.CLAUSES:
        for carrier in clause.carriers:
            if carrier.kind != spec.INDEX:
                continue
            assert any(key.startswith(carrier.ref) for key in emitted), (
                f"{clause.id} claims index:{carrier.ref!r}, which no finding key begins with"
            )


def test_every_key_the_checker_emits_is_claimed_by_exactly_one_row():
    """Guard 3 — the direction that catches a new clause with no registry row.

    **Attributed to the most specific claiming prefix, not to every one that matches.** The
    vocabulary is genuinely nested: `1 dark` is the override's presence and `1 dark --positive`
    is a pinned value, and those are two different normative sentences. A plain `startswith`
    sweep reports the second as claimed twice and demands one of the sentences be deleted —
    the guard mistaking the key space's shape for a defect in the registry.

    **And a key may carry more than one sentence of the same clause.** `8 separator` carries
    both clause 8's rule and its scoring definition, and those are two normative sentences by
    `0007`'s own construction — §8.5 records the tally being wrong three times, which is why
    the measurement is stated separately from the rule. So the invariant is not *exactly one
    row*, which the corpus refutes; it is *exactly one clause*. Two different clauses claiming
    one key is the real ambiguity, and it stays refused.

    `spec.NOT_A_SENTENCE` is excepted — the keys where the checker reports on its own inputs
    rather than on the page. **Not `conftest.NOT_A_CLAUSE`**, which answers a different
    question: that set is the ratchet floor's exemption list and demands a proof each entry can
    never be `FAIL`. `served` can fail, so it belongs in one set and not the other, and using
    the wrong one here would have forced a false proof of impossibility.
    """
    for key in _emitted() - spec.NOT_A_SENTENCE:
        matching = [(len(carrier.ref), clause.id) for clause in spec.CLAUSES
                    for carrier in clause.carriers
                    if carrier.kind == spec.INDEX and key.startswith(carrier.ref)]
        assert matching, f"{key!r} is claimed by no row; every emitted key needs a sentence"
        finest = max(length for length, _ in matching)
        claiming = sorted(one for length, one in matching if length == finest)
        owners = {one.split(".")[0] for one in claiming}
        assert len(owners) == 1, (
            f"{key!r} is claimed at equal specificity by {claiming}, which are sentences of "
            f"different clauses ({sorted(owners)}); one finding key cannot enforce two"
        )


def test_an_uncarried_sentence_says_where_it_is_picked_up():
    """Guard 4 — the one that would have caught `0009` §3.2's third occurrence.

    Clauses 8 and 4-`<title>` drifted across seven surfaces with no stage owning either. An
    uncarried row is allowed; an uncarried row with nowhere to be picked up is not.
    """
    for clause in spec.uncarried():
        assert clause.why, f"{clause.id} is carried by nothing and says nothing about where"
        assert any(token in clause.why for token in ("0008", "0009", "ADR-")), (
            f"{clause.id}'s why does not cite a document that could pick it up: {clause.why!r}"
        )


def test_a_carried_sentence_does_not_also_claim_to_be_open():
    """`why` is the uncarried row's field. A row with both reads as carried in the table and
    as open in the tail, and a reader has no way to tell which the author meant."""
    for clause in spec.CLAUSES:
        if clause.carriers:
            assert not clause.why, f"{clause.id} has carriers and a why"


def test_the_gate_gates_nothing_outside_the_registry_s_vocabulary():
    """Guard 5. `GATED` and the registry are two spellings of the same finding prefixes, and
    `0009` N1 is the class where two lists of one vocabulary are tied by nothing.

    Compared as prefixes in both directions, because `GATED` is coarser than the registry on
    purpose: `1 ` gates every clause-1 key at once, while the registry names them one
    sentence at a time.
    """
    refs = spec.index_refs()
    for prefix in report.GATED:
        assert any(ref.startswith(prefix) or prefix.startswith(ref) for ref in refs), (
            f"GATED gates {prefix!r}, which belongs to no normative sentence in the registry"
        )


def test_the_two_exemption_sets_answer_different_questions_and_say_so():
    """`conftest.NOT_A_CLAUSE` and `spec.NOT_A_SENTENCE` were one set until `served` existed.

    They are not the same question. `NOT_A_CLAUSE` is the ratchet floor's exemption list and
    its pin test demands a proof that each entry can never be `FAIL`; `NOT_A_SENTENCE` names
    the keys `0007` §5-§6 says nothing about. `served` can fail *and* is not a sentence, which
    is what forced the split — a single set would have required either a false proof of
    impossibility or a normative row for a sentence nobody wrote.

    Asserted as the relationship rather than as two literals, so the guard survives either set
    growing for its own reason.
    """
    assert NOT_A_CLAUSE <= spec.NOT_A_SENTENCE, (
        "a key exempt from the ratchet floor because it can never fail is the checker "
        "reporting on its own inputs, so it cannot be a normative sentence either"
    )
    assert "served" in spec.NOT_A_SENTENCE and "served" not in NOT_A_CLAUSE, (
        "served is the key that separates the two sets; if it has moved into NOT_A_CLAUSE "
        "somebody has claimed it can never be FAIL, which is the opposite of its purpose"
    )
    assert not (spec.NOT_A_SENTENCE & spec.index_refs()), (
        "a key the registry claims as a carrier cannot also be exempt from claiming"
    )


def test_no_exempt_key_is_claimed_as_a_carrier():
    """The other half of guard 5. `NOT_A_CLAUSE` is the set that can never be `FAIL`; a row
    citing one as its carrier would claim a sentence is enforced by something that gates
    nothing and says the wrong thing about why."""
    refs = spec.index_refs()
    for key in NOT_A_CLAUSE:
        assert not any(key.startswith(ref) for ref in refs), (
            f"{key!r} is exempt from the ratchet and is claimed as a carrier"
        )


def test_every_row_is_wellformed():
    """Ids unique, kinds known, citations present. The cheap half, asserted because a
    duplicate id makes guard 3's `exactly one` ambiguous rather than false."""
    ids = [clause.id for clause in spec.CLAUSES]
    assert len(ids) == len(set(ids)), "two rows share an id"
    for clause in spec.CLAUSES:
        assert clause.cite, f"{clause.id} carries no citation"
        assert clause.quote, f"{clause.id} carries no quote"
        for carrier in clause.carriers:
            assert carrier.kind in spec.KINDS, f"{clause.id}: unknown kind {carrier.kind!r}"
            assert carrier.ref, f"{clause.id}: a {carrier.kind} carrier with no reference"


def test_a_repo_citation_is_shaped_so_it_can_be_probed():
    """`repo:path::needle`, and the needle is a test function name.

    Asserted as a shape rather than probed here, because probing needs the sibling on disk —
    `test_a_repo_citation_still_points_at_something` is the `submodules` half.
    """
    for clause in spec.CLAUSES:
        for carrier in clause.carriers:
            if carrier.kind != spec.REPO:
                continue
            repo, _, rest = carrier.ref.partition(":")
            path, sep, needle = rest.partition("::")
            assert repo and path and sep and needle, (
                f"{clause.id}: {carrier.ref!r} is not repo:path::needle"
            )
            assert needle.startswith("test_"), (
                f"{clause.id}: {needle!r} is not a test function name — an assertion's text "
                f"goes stale when the sibling legitimately changes"
            )


def test_the_report_prints_every_uncarried_sentence_with_its_reason():
    """The visibility layer is the whole point of the uncarried rows, so it is asserted.

    Without this, a row could be uncarried, correct, and invisible — which is the state the
    registry was built to end.
    """
    printed = "\n".join(spec.report())
    for clause in spec.uncarried():
        assert clause.id in printed
        assert clause.quote[:40] in printed
        assert clause.why[:40] in printed
    assert "NOT CARRIED" in printed


def test_a_settled_reading_is_printed_and_not_only_readable_in_source():
    """`note` carries the readings a stage's scope turns on — c4.s3 is S10's four surfaces or
    three. A field whose whole argument is that a stage must not be *scoped by whoever read it
    last* cannot itself be visible only to someone already reading the module.

    Raised in review as a question rather than a defect, and it is the right question: the
    module made the visibility argument for the report and then did not extend it to the field
    carrying the settled readings.
    """
    printed = "\n".join(spec.report())
    noted = [clause for clause in spec.CLAUSES if clause.note]
    assert noted, "no row carries a settled reading, which would make this guard vacuous"
    for clause in noted:
        assert clause.note[:50] in printed, f"{clause.id}'s note is not printed"


def test_the_registry_reports_a_count_it_computed():
    """The count is printed and typed into no document — `CLAUDE.md`'s rule, and `0009` §8
    row 1's precedent after three sweeps produced three answers."""
    printed = "\n".join(spec.report())
    assert f"{len(spec.CLAUSES)} normative sentence(s)" in printed
    assert f"{len(spec.uncarried())} carried by nothing" in printed


def test_normalise_collapses_a_wrap_a_bold_and_a_blockquote_marker():
    """The three shapes `0007` actually puts between a quote's words. Clause 9 is inside a
    blockquote, so without the marker rule its sentence can never match — and the failure
    would read as a drifted quote rather than as a normaliser missing a case."""
    assert spec.normalise("a\n  b") == "a b"
    assert spec.normalise("**bold**") == "bold"
    assert spec.normalise("> quoted\n> across") == "quoted across"
    assert spec.normalise("`--radius`") == "`--radius`", "backticks are part of the identifier"
    assert spec.normalise("<table>") == "<table>", "a > that is not a line marker stays"


def test_the_keys_no_sentence_carries_are_printed_and_not_only_in_source():
    """`NOT_A_SENTENCE` is policy of exactly the kind this module argues must be visible.

    `report()` prints the uncarried rows and the settled readings on the ground that policy
    must not be legible only to somebody already reading the module. This set says which
    emitted keys are deliberately outside the registry, which is the same kind of claim.
    """
    printed = "\n".join(spec.report())
    for key in spec.NOT_A_SENTENCE:
        assert key in printed, f"{key} is exempt from the registry and the report does not say so"
