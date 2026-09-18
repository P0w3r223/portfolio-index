"""The guards for `tools/queue.py` — the refusing half the module itself deliberately lacks.

`tools.queue` prints and exits 0, like `tools.spec` and `tools.citations`, because no
instrument can tell a row that is open from a row somebody repaired and forgot to mark. What
*can* be refused is narrower and lives here: a queue whose order sentence and session span
disagree, an `Open` item that is not an id and a state word, a row for a repository the queue
does not contain, and an `Index SHA` no reader can resolve.

**The ancestry guard has a precondition and this file asserts it twice.** `git merge-base`
cannot answer in a shallow checkout, and `actions/checkout` is shallow by default — so the
guard would have skipped in CI for ever, which is a pass. `test_the_core_job_can_answer_an_
ancestry_question` reads the workflow and refuses a `core` job without `fetch-depth: 0`. That
is the same shape as `0012` §8's finding one file over: the guard was well built and its
precondition was unasserted.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import ROOT
from tools import queue

WORKFLOW = ROOT / ".github" / "workflows" / "pagespec.yml"


def test_the_order_sentence_names_exactly_the_submodules_the_index_carries():
    """§3.1's order is a list of twelve names in prose, and `.gitmodules` is the tree.

    The strongest available check on a sentence: it is answered against something outside the
    document. A repository dropped from the order would otherwise leave the queue one session
    short with every count in `tools/queue.py` agreeing with itself.
    """
    declared = set(re.findall(r"^\s*path = (.+)$",
                              (ROOT / ".gitmodules").read_text(encoding="utf-8"),
                              flags=re.MULTILINE))
    assert set(queue.order()) == {name.strip() for name in declared}


def test_every_session_the_queue_names_carries_a_kind_the_document_defines():
    """`scan`, `repair`, `done`, `secrets only` — and a fifth word is a table nobody updated."""
    kinds = {one.kind for one in queue.sessions()}
    assert kinds <= {"scan", "repair", "done", "secrets only"}, (
        f"§3.1's Kind column carries {sorted(kinds)}, and `tools/queue.py` filters on those "
        f"words to answer what is left")


def test_the_queue_and_the_rows_partition_the_twelve():
    """Every submodule is either scanned or remaining, and never both.

    The arithmetic is the guard. `0010` §5's own bullet about a census going stale four lines
    from the instrument that produced it is the argument for asserting this rather than
    printing it.
    """
    scanned = queue.scanned()
    left = {one.subject for one in queue.remaining()}
    assert not (scanned & left)
    assert scanned | (left & set(queue.order())) == set(queue.order())


def test_the_row_numbers_follow_the_order_the_method_sets():
    """Row *n* is the *n*-th repository of §3.1's order, or the queue has drifted from it."""
    order = queue.order()
    for row in queue.rows():
        if not row.number.isdigit():
            continue
        index = int(row.number) - 1
        assert 0 <= index < len(order), f"row {row.number} is outside the twelve"
        assert row.repo == order[index], (
            f"§4's row {row.number} is `{row.repo}` and §3.1's order puts `{order[index]}` "
            f"there")


def test_every_open_item_is_an_id_and_a_state_word():
    """0.4's carrier. Without it the column is prose again and the tool reports `?`.

    This is the test that makes the vocabulary real, and it is the reason the states are
    defined in §4's header rather than in this file: a registry that answers only to itself is
    the shape `0010` §5 promoted from an observation to a rule.
    """
    bad = queue.malformed()
    assert bad == (), "\n".join(
        f"row {item.row}: {item.id!r} is not `<id> <state>` with a state from "
        f"{list(queue.STATES)}" for item in bad)


# *A second test stood here and was deleted before this file was committed.* It asserted that
# every state word in use is one `STATES` declares — which is `malformed()` restated: an item
# that does not parse carries the state `"?"`, and `"?"` is not in `STATES`, so one assertion
# already covers both halves. Two tests over one property is `0009` §15.4's duplicate class, and
# the deletion is recorded here rather than left silent because the file would otherwise look
# like it protects two things.


def test_no_row_cites_an_index_sha_a_reader_cannot_resolve():
    """The transplant guard, and the class it exists for has reached this record twice.

    Sessions 4 and 5 were written on a branch in the repository that became the archive, and
    one of their rows cited **its own working commit** — a SHA no clone of this repository
    holds. Both were removed by hand during the port, by a reviewer who happened to read the
    paragraph. This is that reading, taken by an instrument.

    A `pending` row is exempt: its repair exists and is not on `main` yet, which is the whole
    reason `0010` §4's header names that state.
    """
    if queue.shallow():
        pytest.skip("a shallow checkout cannot answer an ancestry question; the `core` job "
                    "sets fetch-depth: 0, and the guard below refuses a job that does not")
    pending = {row.number for row in queue.rows()
               if any(item.state == "pending" for item in row.items)}
    bad = [(row, how) for row, how in queue.ancestry()
           if how not in {"ancestor", "none"} and row.number not in pending]
    assert not bad, "\n".join(
        f"§4 row {row.number} cites `{row.index_sha}`, which {how} in this checkout"
        for row, how in bad)


def test_the_core_job_runs_the_queue_and_can_answer_an_ancestry_question():
    """The precondition of the guard above, asserted where it is configured.

    Two halves, and the second is the one that matters. `actions/checkout` clones at depth 1
    unless told otherwise, and in a shallow checkout `git merge-base` cannot answer — so the
    ancestry guard would skip, for ever, in the one place it is meant to run. A skip is a pass
    (`0010` §3.6, observation 2), so the guard would have read as green over every defect it
    was written for.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    core = text.split("  surfaces:")[0]
    assert "python -m tools.queue" in core, (
        "the `core` job no longer prints the queue; `tools/spec.py` and `tools/citations.py` "
        "are printed there for the same reason — a census nobody reads is a census that rots")
    assert "fetch-depth: 0" in core, (
        "the `core` job's checkout is shallow again, which turns "
        "`test_no_row_cites_an_index_sha_a_reader_cannot_resolve` into a permanent skip")


def test_the_report_names_every_state_including_the_ones_with_no_instance():
    """A declared state with an empty bucket must stay visible, or it is a word in a document
    and nothing else. `declined` and `pending` are the two, and the report says so beside the
    count rather than omitting the row."""
    printed = "\n".join(queue.report())
    for state in queue.STATES:
        assert state in printed


@pytest.mark.submodules
def test_the_sibling_citation_census_is_computable_and_says_only_what_it_can_see():
    """The census runs and every verdict is a word this module defines.

    **Deliberately not a gate**, and the reason is measured rather than modest: the
    attribution is adjacency on a line, and on its first run — before `_bodies()` was bounded
    to §4 — it reported an *index* SHA as an unresolvable commit in `it-job-radar` because
    that repository's name appeared in the same §6 cell. `tools/citations.py` refuses to guess
    an owner for exactly this reason, and a wrong attribution here would redden a build over a
    sentence rather than a defect.
    """
    verdicts = {how for _, _, _, how in queue.sibling_citations()}
    assert verdicts <= {"on main", "off main", "unresolved", "shallow", "not checked out"}
