"""Guards for the citation resolver — `ADR-0009` §3 step 1.

**What these gate on, and what they deliberately do not.** `unresolved` is the failing set: a
line names a document and the section is not in it. `unattributed` is printed and never gated,
because the obvious attribution rule is wrong in both directions and a wrong attribution
resolves *green* — `tools/citations.py`'s docstring carries the measurement.

The mutation battery for this file is `0010` §3.6's six observations, not a local invention.
Two of them have teeth here and are worth naming at the top. **Observation 2** — a mutation
must redden *this guard's own assertion*, not merely produce a non-zero exit: if `git ls-files`
returned nothing the loops below would pass vacuously, which is why the vacuity guard below
exists at all. **Observation 6** — a guard can be empty because the tool it shells to
excludes its subject by default. Here that tool is `git ls-files` and its default exclusion is
*untracked files*; after `actions/checkout` everything is tracked, so no mutation can reach it
and it is recorded as a stated bound rather than a tested one.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools import citations

#: The shape `_VACUOUS` has in `tests/test_spec.py`, for the reason recorded there: on
#: 2026-09-09 `spec.uncarried()` mutated to `return ()` left 576 tests green, because every
#: guard over it iterated an empty tuple and asserted nothing.
_FLOORS = {"citations": 500, "corpus": 40, "documents": 10, "unattributed": 100}


def test_the_resolver_is_not_vacuous_because_an_empty_sweep_passes_every_other_guard():
    """Every guard below iterates a collection. An empty one asserts nothing and reads green.

    The floors are deliberately far below what the run prints, and no measured figure is
    written here on purpose: this guard exists to catch a collapse to zero, not to pin
    a census. A pinned census here would redden on every ordinary edit to `docs/`, which is
    the failure mode `0008` §4.11 records for hand-typed figures.
    """
    assert len(citations.citations()) >= _FLOORS["citations"]
    assert len(citations.corpus()) >= _FLOORS["corpus"]
    assert len(citations._documents()) >= _FLOORS["documents"]
    # `unattributed()` is here because nothing else in this file asserts it. Collapsed to an
    # empty tuple it reddens nothing, the report prints a backlog of zero, and the resolver
    # announces full attribution over a backlog it never looked at. Written after the mutation
    # battery for this file found exactly that — observation 6 working, one module on.
    assert len(citations.unattributed()) >= _FLOORS["unattributed"]
    # Files the sweep could not open are collected rather than skipped silently; a dozen
    # dropping out sits far below every floor above, so only this says so.
    assert not citations.UNREADABLE, f"unreadable: {citations.UNREADABLE}"


def test_no_citation_names_a_document_and_a_section_that_is_not_in_it():
    """The one gating assertion. `unresolved` must be empty.

    It was **not** empty when this resolver first ran: `ADR-0001` cited `0001` section 160,
    which is a line number in the section position, and the ledger cited section 4.19 of the
    review, which does not exist — the claim it names is in `0009` §7 row 12, and the ledger's
    own §4.19 is where it was measured. Both are repaired in the commit that adds this file,
    with an erratum each.
    """
    bad = citations.unresolved()
    assert not bad, "\n".join(f"{c.path}:{c.line} cites {c.owner} §{c.ref}, which is not there"
                              for c in bad)


def test_unresolved_can_actually_find_something_which_the_guard_above_cannot_show():
    """The positive control for the only assertion in this file that gates.

    The guard above asserts a set is **empty**, so a function that always returns an empty set
    satisfies it — and mutating `unresolved()` to `return ()` left all seven guards green. That
    is `spec.uncarried() -> return ()` leaving 576 tests green, one module on, and the docstring
    of the vacuity guard cites that precedent while not covering the one function that gates.

    Synthetic citations, so this says nothing about the corpus and cannot go stale with it.
    """
    ghost = citations.Citation("synthetic", 1, "9.99", "0008")
    real = citations.Citation("synthetic", 2, "4.11", "0008")
    assert citations.unresolved((ghost, real)) == (ghost,)

    # And the fourth state: an owner this index does not carry is neither resolved nor
    # unresolved, and was counted as resolved until the review of the first commit.
    foreign = citations.Citation("synthetic", 3, "2", "ADR-0012")
    assert citations.unresolved((foreign,)) == ()
    assert citations.unknown_document((foreign,)) == (foreign,)
    assert citations.unknown_document((real,)) == ()


def test_the_four_states_partition_the_sweep_so_nothing_can_be_green_by_subtraction():
    """`resolved` is counted, never inferred.

    The report computed it as *total minus the other buckets*, so a citation belonging to no
    named bucket joined the green column silently. One real citation does exactly that —
    `0007`:528 names `ADR-0012`, a sibling repository's decision document — and so would every
    mistyped document number, which is the likeliest way a citation breaks at all.
    """
    found = citations.citations()
    index = citations._index()
    resolved = [c for c in found if c.owner in index and c.ref in index[c.owner]]
    total = (len(resolved) + len(citations.unresolved(found))
             + len(citations.unattributed(found)) + len(citations.unknown_document(found)))
    assert total == len(found), "the four states no longer partition the sweep"
    assert citations.unknown_document(found), (
        "the premise moved: no citation names a document outside this index, so this guard "
        "and the `foreign` row it defends are both asserting over nothing")


def test_a_link_to_an_adr_is_attributed_to_the_adr_and_not_to_the_audit_document():
    """Every cross-reference to an ADR here is a markdown link, so the adjacent token is a path.

    Reading the number out of that path and keying it bare answered about
    `docs/audit/0004_session1-recruiter-triage.md` while the link label beside it read
    `ADR-0004` — on six lines, each resolving **green** against the wrong document's §5,
    because both documents have one. The defect the module docstring is about, committed by
    the module. Found by the review of the first commit.
    """
    link = "[`ADR-0004`](../adr/0004_what-carries-the-page-spec.md) §5 (the"
    assert citations._owner_at(link, link.index("§"), "docs/audit/0008_x.md") == "ADR-0004"

    # A link target with no directory: the same filename means the ADR from inside `docs/adr/`
    # and the audit document from inside `docs/audit/`.
    bare = "[`0004_what-carries-the-page-spec.md`](0004_what-carries-the-page-spec.md) §5"
    assert citations._owner_at(bare, bare.index("§"), "docs/adr/0009_x.md") == "ADR-0004"
    assert citations._owner_at(bare, bare.index("§"), "docs/audit/0002_x.md") == "0004"

    relative = "`../audit/0008_the-rollout-ledger.md` §4"
    assert citations._owner_at(relative, relative.index("§"), "docs/adr/0009_x.md") == "0008"


def test_one_key_never_hides_a_document_behind_alphabetical_order():
    """`0010` is three files — the portfolio audit and its two prompts.

    Keeping only the last one read hid the other two, and which one survived was decided by
    sorting. The prompts declare no numbered section, so the union is exact today; this guard
    is what says so out loud if one of them grows a `### N.M` and starts answering for `0010`.
    """
    documents = citations._documents()
    assert len(documents["0010"]) == 3, "the premise moved: `0010` is no longer three files"
    declaring = [path.name for path in documents["0010"] if citations.headings(path)]
    assert declaring == ["0010_the-portfolio-audit.md"], (
        f"more than one file under `0010` declares numbered sections: {declaring}. The union "
        f"below is no longer exact and a citation of `0010` cannot say which it means")
    assert "3.4" in citations._index()["0010"]


def test_the_ledger_reader_fails_by_naming_the_document_it_could_not_parse(tmp_path):
    """A moved or renamed `0008` must arrive as one diagnosis, not as every citation of it.

    `tools/spec.py`'s `normative_text()` sets this precedent and `tests/test_spec.py` proves it
    red. Without it, renaming the ledger reports 171 drifted pointers — the wrong diagnosis,
    printed once per citation of it.
    """
    empty = tmp_path / "0008_the-rollout-ledger.md"
    empty.write_text("# A ledger with no numbered subsection\n\nprose\n", encoding="utf-8")
    original = citations.LEDGER
    try:
        citations.LEDGER = empty
        with pytest.raises(AssertionError, match=r"0008_the-rollout-ledger\.md"):
            citations.ledger_headings()
    finally:
        citations.LEDGER = original


def test_the_heading_index_is_bounded_by_depth_and_refuses_a_list_item():
    """`0008` carries 22 `####` headings whose text starts with a digit. They are not sections.

    `#### 1. Two submodule tests do assert a separator` and its siblings are ordered-list items
    inside §4.13, §4.14 and §4.17. An unbounded reader admits sections 7 through 11 from them, so
    a reference to section 11 of the ledger would resolve green against a list item — the
    guard passing over the defect it exists to catch, which is the class `0008` §3.7 names.
    """
    text = citations.LEDGER.read_text(encoding="utf-8")
    deep = [line for line in text.splitlines() if re.match(r"^#### \d", line)]
    assert deep, "the premise moved: no `#### <digit>` heading in the ledger to be fooled by"

    found = citations.ledger_headings()
    assert "4.11" in found and "4" in found, "the reader stopped seeing real sections"
    for ref in ("7", "8", "9", "10", "11"):
        assert ref not in found, (
            f"§{ref} was admitted as a ledger section; it comes from a `####` list item, and "
            f"the ledger has only six `##` sections")


def test_attribution_is_adjacent_and_never_the_nearest_preceding_token():
    """The rule that resolves green when it is wrong, refused in both of its directions.

    `0008`:120 writes *"lost between `0006` §2.3 and §4.11"* where `§4.11` is `0008`'s. A
    nearest-preceding rule claims it for `0006`; a list-continuation rule claims it for `0006`
    too, and that version of this resolver was written, run, and removed on the strength of
    this line. Against it, six `§4.x` outside `docs/` belong to `0007` and would be claimed for
    `0008`. Both mistakes resolve, so neither can be caught downstream.
    """
    owner = citations._owner_at("lost between `0006` §2.3 and §4.11; §4.20", len("lost between `0006` §2.3 and "))
    assert owner is None, f"a non-adjacent token was claimed as the owner: {owner!r}"

    assert citations._owner_at("`0008` §4.11", len("`0008` ")) == "0008"
    assert citations._owner_at("ADR-0008 §9", len("ADR-0008 ")) == "ADR-0008"
    assert citations._owner_at("[`0006`](0006_x.md) §4.2", len("[`0006`](0006_x.md) ")) == "0006"


def test_a_bare_number_means_the_audit_document_and_the_adr_prefix_is_kept_apart():
    """`CLAUDE.md`'s rule, encoded. `ADR-0008` and `0008` are different documents.

    Two numbers were taken twice before `ADR-0009` §0 took a third. A resolver folding the
    prefix would answer about the contrast ADR when asked about the rollout ledger — which is
    the mistake an earlier hand count of this same graph actually made.
    """
    documents = citations._documents()
    assert all(path.parent.name == "audit" for path in documents["0008"])
    assert all(path.parent.name == "adr" for path in documents["ADR-0008"])
    assert set(documents["0008"]).isdisjoint(documents["ADR-0008"])
    assert "4.11" in citations._index()["0008"]
    assert "4.11" not in citations._index()["ADR-0008"], (
        "the contrast ADR has no numbered subsections at all; if it grows one, the adjacency "
        "rule still tells them apart, but this assertion's premise has moved")


def test_the_corpus_is_read_from_the_index_and_reaches_more_than_python():
    """`git ls-files`, not a walk, and not only `.py`.

    A filesystem walk sees gitignored content no clone has — a count of this same graph once
    read 81 across 22 files because ten were in `.claude/sessions/`. And the corpus has to
    reach the prose: the citations that matter most sit in `.md`, in a `.css` fixture, in the
    CI workflow and in `CLAUDE.md`, none of which a `*.py` sweep would see.
    """
    corpus = citations.corpus()
    assert "CLAUDE.md" in corpus, "the root file carrying seven citations of the ledger"
    assert any(name.endswith(".md") and name.startswith("docs/") for name in corpus)
    assert any(name.endswith(".css") for name in corpus)
    assert ".github/workflows/pagespec.yml" in corpus
    # `git ls-files` prints a gitlink as the bare directory name, `ab-lab`, with no
    # separator — so an earlier form of this assertion, which required `"/" in name`, could
    # not be true for the entry it named and passed whatever `corpus()` did.
    assert "ab-lab" not in corpus and "doc-extract" not in corpus, "a gitlink was read as a file"


def test_the_report_prints_every_state_and_the_triage_can_name_a_candidate():
    """The module's only output, and the only place its arithmetic is checked.

    `report()` was the largest untested surface here: mutated to `return []` it reddened
    nothing, and so did `candidates()` collapsed to an empty tuple — which would have moved
    every backlog citation into the *no candidate anywhere* row and printed the whole backlog
    as findings. The partition assertion lives inside `report()` because that is where the
    subtraction used to be; this guard is what makes it run.
    """
    lines = citations.report()
    assert lines[0].startswith("citations —")
    body = "\n".join(lines)
    for state in ("unresolved", "resolved", "foreign", "unattributed"):
        assert state in body, f"the {state} row is not printed"

    found = citations.candidates(citations.Citation("synthetic", 1, "4.11", None))
    assert "0008" in found, "the triage cannot name the ledger for one of its own sections"
    assert not citations.candidates(citations.Citation("synthetic", 1, "99.99", None))


def test_a_file_the_sweep_cannot_open_is_recorded_rather_than_skipped(monkeypatch):
    """`citations()` was the one reader here that swallowed its error.

    `headings()` and `corpus()` both raise; this one caught `OSError` and `UnicodeDecodeError`
    and moved on, so a dozen files dropping out of the sweep sat far under every floor above
    and nothing said so. The guard for it cannot be reddened by the corpus — no tracked file is
    unreadable today — so the failure is injected here. Without this, mutating the recording
    line to `pass` is green, which is the mutation that found the gap.
    """
    original = Path.read_text

    def refuse(self, *args, **kwargs):
        if self.name == "CLAUDE.md":
            raise OSError("injected")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refuse)
    citations.citations()
    assert any(name.startswith("CLAUDE.md") for name in citations.UNREADABLE), (
        "a file that could not be read left no trace in the sweep")


def test_both_workflow_filters_name_the_paths_this_guard_reads():
    """A guard reading files whose paths are not in the `paths:` filter runs in **no job**.

    `ADR-0009` §3 step 1 is built on that sentence, and `0008` §3's Sx cell is the measurement
    behind it: a commit touching only `docs/**` had no CI run at all. The resolver's whole
    subject lives in `docs/` and in `CLAUDE.md`, so if either drops out of a filter this guard
    stops running on exactly the class of change it watches — silently, which is the failure
    shape this repository keeps finding in itself.

    Nothing else asserts the filters' literal contents: the guard that used to,
    `tests/test_audit_identifiers.py`, was deleted with the identifier sweep on 2026-09-11.
    """
    workflow = (Path(citations.ROOT) / ".github" / "workflows" / "pagespec.yml")
    lists = re.findall(r"paths:\s*\[(.*?)\]", workflow.read_text(encoding="utf-8"), re.S)
    assert len(lists) == 2, (
        f"expected a `paths:` filter on push and on pull_request, parsed {len(lists)}; the "
        f"workflow's shape has moved under this guard")
    for index, filter_body in enumerate(lists):
        for needed in ("'docs/**'", "'CLAUDE.md'", "'tools/**'", "'tests/**'"):
            assert needed in filter_body, (
                f"filter {index} does not name {needed}; `python -m tools.citations` and its "
                f"guards would not run on a change to the files they read")
