"""The guards for `tools/queue.py` — the refusing half the module itself deliberately lacks.

`tools.queue` prints and exits 0, like `tools.spec` and `tools.citations`, because no
instrument can tell a row that is open from a row somebody repaired and forgot to mark. What
*can* be refused is narrower and lives here: a queue whose order sentence and session span
disagree, an `Open` item that is not an id and a state word, a row for a repository the queue
does not contain, and an `Index SHA` no reader can resolve.

**The ancestry guard has a precondition and this file asserts it twice.** `git merge-base`
cannot answer in a shallow checkout, and `actions/checkout` is shallow by default — so the
guard would have skipped in CI for ever, which is a pass. `test_the_core_job_runs_the_queue_and_can_answer_an_ancestry_question` reads the workflow and
refuses a `core` job without `fetch-depth: 0`. That
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
PROMPTS = ROOT / "docs" / "audit"
AUDIT = PROMPTS / "0010_the-portfolio-audit.md"


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


def test_the_queue_and_the_rows_account_for_every_submodule_the_index_carries():
    """The twelve are each either scanned or remaining, counted against `.gitmodules`.

    *This guard asserted something weaker until the review of the stage that wrote it*: that
    `scanned()` and `remaining()` do not overlap, which they cannot — `remaining()` is defined
    by subtracting one from the other, so the assertion was a tautology dressed as a statement
    about the record. The arithmetic below is anchored outside both functions, which is the
    only version of this that can fail.
    """
    declared = {name.strip() for name in
                re.findall(r"^\s*path = (.+)$", (ROOT / ".gitmodules").read_text(encoding="utf-8"),
                           flags=re.MULTILINE)}
    scanned_repos = {row.repo for row in queue.rows() if row.repo in declared}
    left_repos = {one.subject for one in queue.remaining() if one.subject in declared}
    assert scanned_repos | left_repos == declared
    assert len(scanned_repos) + len(left_repos) == len(declared)


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


def test_the_state_vocabulary_answers_to_the_document_and_to_both_prompts():
    """`STATES` against the four places that spell it, which is the half a registry forgets.

    `malformed()` refuses a cell using a word outside `STATES`. Nothing refused the opposite
    direction until the review measured it: adding a sixth state to the tuple, renaming a
    bullet in §4's header, and rewriting the list in the scan prompt were **all three green**,
    while the guard above it claimed in its own docstring that the vocabulary is defined in the
    document rather than in the code. `order()` against `.gitmodules` is the pattern this
    borrows — a registry has to answer to something outside its own file, `0010` §5.
    """
    section = AUDIT.read_text(encoding="utf-8").split("## 4. The rows")[1]
    declared = re.findall(r"^- `([a-z]+)` — ", section.split("\n| # | Repo |")[0],
                          flags=re.MULTILINE)
    assert set(declared) == set(queue.STATES), (
        f"§4's header defines {sorted(declared)} and `tools/queue.py` carries "
        f"{sorted(queue.STATES)}")
    spelled = " · ".join(queue.STATES)
    for prompt in (PROMPTS / "0010_scan-prompt.md", PROMPTS / "0010_repair-prompt.md"):
        assert spelled in prompt.read_text(encoding="utf-8"), (
            f"{prompt.name} no longer spells the vocabulary as `{spelled}`, so a session "
            f"reading the prompt and a session reading §4 would write different cells")


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
    assert verdicts <= {"on main", "off main", "unresolved", "shallow", "not checked out",
                        "beyond the gitlink", "pin unreadable"}


@pytest.mark.submodules
def test_a_commit_past_the_pin_reads_beyond_the_gitlink_and_the_pin_itself_reads_on_main():
    """Both branches of the gitlink question, against a pin supplied rather than read.

    **The pin is injected on purpose, and the alternative is a guard that skips.** Every
    gitlink in this repository is level with its sibling's `origin/main` whenever the
    portfolio is at rest, so a test looking for a real commit past a real pin finds none and
    passes by skipping — which `0010` §3.6 has already convicted once. Seeding `pins` exercises
    the comparison itself: the tip against its own parent as the pin is *beyond*, and the tip
    against itself is not.

    The defect this covers is `0010` §4's A-5 repair: between `766203a` and its correction the
    row read seven × `closed` while the gitlink held none of the repairs, and the census called
    that `on main` because it never asked this question.

    **Scope, stated because the first draft of this guard did not state it.** `core` deselects
    `submodules`, and `surfaces` and `live` check out at `actions/checkout`'s default depth, so
    `queue.shallow()` is true and this skips: **no CI job runs it.** That is the same position
    `sibling_citations()` argues for itself — an instrument for a working session — and giving
    `surfaces` a full history to change it would buy the adjacency heuristic a job, which that
    docstring calls the wrong order. The two guards below need no git and do run in `core`.
    """
    if queue.shallow():
        pytest.skip("a shallow checkout cannot answer an ancestry question")
    exercised = 0
    for name in queue.order():
        tree = ROOT / name
        if not (tree / ".git").exists() or queue.shallow(tree):
            continue
        tip = queue._git("rev-parse", "origin/main", cwd=tree).out.strip()
        parent = queue._git("rev-parse", "origin/main^", cwd=tree).out.strip()
        if not tip or not parent:
            continue
        assert queue._against_the_pin(name, tip, tree, {name: parent}) == "beyond the gitlink", (
            f"{name}: `{tip[:7]}` is one commit past the pin `{parent[:7]}` and the census "
            f"called it something else")
        assert queue._against_the_pin(name, tip, tree, {name: tip}) == "on main", (
            f"{name}: `{tip[:7]}` pinned exactly by the gitlink is not `beyond` it")
        # **A pin the clone cannot resolve is not a verdict.** `merge-base --is-ancestor`
        # answers 1 for *not an ancestor* and errors with everything else — 128 here — and
        # reading the error as `beyond the gitlink` would hand the gated guard a checkout
        # problem dressed as a record defect.
        assert queue._against_the_pin(name, tip, tree, {name: "dead" * 10}) == "pin unreadable", (
            f"{name}: an unresolvable pin must read as unanswerable, not as a finding")
        exercised += 1
    assert exercised, ("no submodule answered the gitlink question, so this guard proved "
                       "nothing — which is the shape it exists to refuse")


@pytest.mark.submodules
def test_no_row_claims_closed_over_a_commit_this_repository_does_not_pin():
    """§4's `pending` read by an instrument instead of by a reader who happens to look.

    Printed by `tools.queue` and refused here, which is the split this file's docstring
    describes: the census cannot gate, because its attribution is adjacency on a line, but a
    row that claims **no open work at all** while citing a repair the gitlink predates is the
    one shape where a wrong attribution still leaves a real question — the pointer is either
    bumped or it is not, and `0010` §4 has a word for the answer.

    **This one skips in every CI job too**, for the reason the guard above states, and it is a
    state assertion over a record that is currently clean — so the pairing it rests on is
    guarded separately and without git in
    `test_unpinned_closures_names_a_row_over_a_stale_pin_and_leaves_the_others_alone`.
    """
    if queue.shallow():
        pytest.skip("a shallow checkout cannot answer an ancestry question")
    bad = queue.unpinned_closures()
    assert not bad, "\n".join(
        f"§4 row {row.number} ({row.repo}) reads {states} and cites `{sha}`, which is merged "
        f"in the sibling and past the gitlink this repository pins — §4 calls that `pending`"
        for row, sha, states in bad)


def test_the_gitlink_is_read_from_the_commit_and_not_from_the_working_tree(monkeypatch):
    """`gitlink()`'s argv, pinned — because the thing it promises is invisible to a comparison.

    The gitlink and the submodule's checked-out `HEAD` are the same commit whenever the
    portfolio is at rest, so a guard that compares them passes over the one mutation that
    matters: reading the working tree instead of the commit. Replacing the body with
    `rev-parse HEAD` in the submodule left the whole suite green — which is `0008`'s
    shipped-green-over-its-own-defect shape, and the reason this asserts the call rather than
    the answer. In the scenario the feature exists for, a session that has moved a sibling
    forward would get `on main` out of the mutated reading and miss the unbumped pointer.

    It also pins *how* the gitlink is told from an ordinary directory — the tree entry's mode,
    `160000`, because `HEAD:docs` resolves perfectly well to a tree and `cat-file -t` cannot be
    the check: the commit a gitlink names is not in this repository's object database at all.
    """
    seen: list[tuple[tuple[str, ...], object]] = []

    def fake(*args: str, cwd=None):
        seen.append((args, cwd))
        return queue.Run(f"160000 commit {'a' * 40}\t{args[-1]}\n", 0)

    monkeypatch.setattr(queue, "_git", fake)
    got = queue.gitlink("doc-extract")

    assert seen[0] == (("ls-tree", "HEAD", "--", "doc-extract"), None), (
        "the gitlink must be read from this repository's own commit, with no `cwd`: "
        f"{seen[0]} asks something else")
    assert got == "a" * 40


def test_unpinned_closures_names_a_row_over_a_stale_pin_and_leaves_the_others_alone():
    """The pairing itself, against an injected census — no git, no submodules, runs in `core`.

    **The guard above it is a state assertion over a record that is currently clean**, so it
    passes over any implementation: `return ()` as the first line of `unpinned_closures()`
    keeps this file green, and so does inverting the state filter. This one refuses both.
    """
    found = queue.rows()
    settled = [row for row in found
               if row.items and not {item.state for item in row.items} & {"open", "pending"}]
    assert settled, "§4 carries no row with all its work settled, so this guard proved nothing"
    row = settled[0]

    named = queue.unpinned_closures((("A-0", row.repo, "0123456", "beyond the gitlink"),), found)
    assert [got.number for got, _, _ in named] == [row.number], (
        f"a commit past the pin in `{row.repo}` must name row {row.number}, whose cells are "
        "settled")

    assert queue.unpinned_closures((("A-0", row.repo, "0123456", "on main"),), found) == (), (
        "a commit the gitlink already contains is not a finding")

    with_work = [r for r in found if any(item.state == "open" for item in r.items)]
    if with_work:
        open_row = with_work[0]
        assert queue.unpinned_closures(
            (("A-0", open_row.repo, "0123456", "beyond the gitlink"),), found) == (), (
            f"row {open_row.number} still declares open work, so an unbumped pointer is the "
            "ordinary state and not a claim of closure")
