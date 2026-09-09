"""Guards for the entry-state instrument.

The suite's own split applies here: the pure functions are exercised on literal text, the
failure paths through the injectable `git` and `gh` seams, and two tests shell out to assert
contracts that hold in any checkout. Nothing needs a sibling on disk and nothing touches the
network, so all of it belongs to the `core` job.

Three of these exist because a previous version of the module got them wrong, and the middle
one is the most instructive:

- `_git` ignored the exit status, so a failed `git fetch` left the run answering from the
  stale ref it exists to refresh.
- Then the status was read and appended to a *note* — and nothing consulted the notes, so
  `clean` stayed true and the run exited 0 while its report printed the reason three lines
  below the word "clean". A guard here pinned that: it asserted `"clean" in rendered` for an
  unread `gh`, so the suite held the defect in place. **The verdict is a tri-state now**, and
  `test_an_unread_input_is_part_of_the_verdict` is what that guard should have been.
- The guard for the original strip defect was `line[0] in " +-U"` over real `git submodule
  status` output, which reddens only where the flags are spaces. In a fresh clone every flag
  is `-`, `.strip()` removes nothing from a `-`, and it passed green over the defect — in
  exactly the `core` job. It is a contract test now: `_git` must return what the subprocess
  returned, byte for byte.

The two shelling tests are the boundary the seams cannot reach. Every failure test injects a
fake that constructs `Run` itself, so without them nothing asserts that a real subprocess's
non-zero status ever becomes a non-`ok` `Run` — which is the same shape as the defect above: a
guard positioned where it cannot see the failure.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools import entry_state
from tools.entry_state import Run
from tools.pagespec.sources import SURFACES

ROOT = Path(__file__).resolve().parents[1]

#: Exactly what `git submodule status` writes: a flag in column 0, a space in the healthy case.
#: The names are real submodules because `collect(full=True)` only resolves a pointer whose
#: directory exists, and a fake name would skip the branch under test.
HEALTHY = (
    " 433083df38b3a07a3d5b1e13d271029b2f644d21 ab-lab (heads/main)\n"
    " a2e9cd32a3c3d1cb7ddc60a11cef0b88e26dce90 apply-scout (heads/main)\n"
)

#: The one submodule with no published page, so the registry guard below states a set rather
#: than a count. `README.md` shows its Site column empty and says why; `0004` §9 settles it.
NO_PAGE = frozenset({"token-budget"})

_DEFAULTS = {
    "rev-parse --short HEAD": "80987c4\n",
    "rev-parse --abbrev-ref HEAD": "main\n",
    "rev-list --left-right --count HEAD...origin/main": "0\t0\n",
    "status --porcelain --ignore-submodules=dirty": "",
    "submodule status": HEALTHY,
    "fetch --quiet origin": "",
    "rev-parse origin/main": "433083df38b3a07a3d5b1e13d271029b2f644d21\n",
    "status --porcelain --untracked-files=no": "",
}


class FakeGit:
    """A `git` that answers from a table, and fails on demand for the paths that matter."""

    def __init__(self, fails: tuple[str, ...] = (), **out: str):
        self.calls: list[tuple[str, Path | None]] = []
        self.fails = fails
        self.out = {**_DEFAULTS, **{key.replace("_", " "): value for key, value in out.items()}}

    def __call__(self, *args: str, cwd: Path | None = None) -> Run:
        joined = " ".join(args)
        self.calls.append((joined, cwd))
        if any(fail in joined for fail in self.fails):
            return Run("", 128, "fatal: Could not read from the remote repository\n")
        return Run(self.out.get(joined, ""), 0, "")


class FakeGh:
    """A `gh` that answers every call with the same payload, or fails."""

    def __init__(self, payload: str = "[]", *, ok: bool = True, err: str = "gh: not found"):
        self.calls: list[tuple[str, ...]] = []
        self.payload, self.ok, self.err = payload, ok, err

    def __call__(self, *args: str) -> Run:
        self.calls.append(args)
        return Run(self.payload, 0, "") if self.ok else Run("", 1, self.err)


def clean_state(**overrides) -> entry_state.EntryState:
    """A state with nothing wrong with it, so a test can introduce exactly one thing."""
    base = dict(head="80987c4", branch="main", ahead=0, behind=0, uncommitted=(),
                pointers=entry_state.parse_pointers(HEALTHY), open_prs=(), foreign_prs=(),
                full=False, unread=())
    return entry_state.EntryState(**{**base, **overrides})


def portfolio_size() -> int:
    """Derived, not typed: a thirteenth submodule must not redden a pull-request guard."""
    return len(entry_state.submodule_names(
        (ROOT / ".gitmodules").read_text(encoding="utf-8"))) + 1


# --- the boundary the seams cannot reach ---------------------------------------------------


def test_the_shell_returns_what_the_subprocess_returned_byte_for_byte():
    """`_git`'s contract, asserted where the strip actually lived.

    Not `line[0] in " +-U"` over the real output: in a fresh clone every flag is `-`, a strip
    removes nothing from a `-`, and that assertion passes with the defect reinstated — which is
    precisely the `core` job. Byte equality with an unmodified subprocess is false for *any*
    strip, including the trailing newline, and is true whatever is checked out.
    """
    raw = subprocess.run(("git", "submodule", "status"), cwd=ROOT, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")

    assert entry_state._git("submodule", "status").out == raw.stdout


def test_a_real_command_that_fails_produces_a_run_that_says_so():
    """The other half of the contract, and the half no injected fake can prove.

    Every failure test below builds its own `Run`, so without this nothing asserts that a real
    non-zero exit ever reaches one — a guard positioned where it cannot see the failure, which
    is the defect class this module keeps meeting. Needs no network and no submodule: a branch
    that cannot exist fails locally in any checkout.
    """
    failed = entry_state._git("rev-parse", "--verify", "refs/heads/no-such-branch-ever")

    assert not failed.ok
    assert failed.code != 0
    assert failed.reason and failed.reason != "exit 0"

    assert entry_state._git("rev-parse", "--short", "HEAD").ok


# --- the flag column, which a strip anywhere in the stack destroys -------------------------


def test_the_first_row_keeps_its_flag_column():
    """Column 0 is the signal, and the first row is where a strip takes it from."""
    pointers = entry_state.parse_pointers(HEALTHY)

    assert [pointer.name for pointer in pointers] == ["ab-lab", "apply-scout"]
    assert all(pointer.matches_index for pointer in pointers)
    assert pointers[0].sha.startswith("433083df")


# --- the verdict, which is a tri-state -----------------------------------------------------


@pytest.mark.parametrize("fails, expected", [
    (("fetch",), "origin/main not refreshed"),
    (("rev-list",), "the distance from origin/main was not computed"),
    (("status --porcelain --ignore-submodules",), "the index's working tree was not read"),
    (("submodule status",), "the submodule pointers were not read"),
])
def test_an_unread_input_is_part_of_the_verdict(fails, expected):
    """A note nobody consults is silence with extra steps.

    The version this replaces read every exit status and appended a note — and `clean` was
    `not findings`, which notes never entered. So a failed fetch printed `origin/main: level`,
    then *"clean — … every pointer matches the index, nothing uncommitted"*, then the reason
    none of it had been read. Every one of those four commands is an input the depth promised
    to read, so failing to read one is part of the answer.
    """
    state = entry_state.collect(full=False, git=FakeGit(fails=fails), gh=FakeGh())

    matching = [item for item in state.undetermined if expected in item]
    assert matching
    # Asserted through `collect`, not on a hand-built state: whether the reason is *wired* is a
    # different claim from whether `undetermined` renders one, and only this end sees the wire.
    assert all("fatal" in item for item in matching), "the cause travels with the line"
    assert not state.clean, "an unread input must not report as clean"
    rendered = entry_state.report(state)
    assert "clean —" not in rendered, "the clean sentence asserts facts that were not read"
    assert "not read — the entry state may be fine" in rendered


def test_a_failed_gh_is_not_read_as_no_open_pull_request():
    state = entry_state.collect(full=False, git=FakeGit(),
                                gh=FakeGh(ok=False, err="gh: not found"))

    assert any("not read — gh: not found" in item for item in state.undetermined)
    assert not state.clean
    assert "clean —" not in entry_state.report(state)


def test_a_failed_rev_list_does_not_print_a_distance_it_did_not_compute():
    """The note was added and the fabrication was left, which gave the reader two answers."""
    state = entry_state.collect(full=False, git=FakeGit(fails=("rev-list",)), gh=FakeGh())

    assert state.ahead is None and state.behind is None
    assert "origin/main: not computed" in entry_state.report(state)
    assert "level" not in entry_state.report(state)


# --- `--full`, whose whole promise is the comparison ---------------------------------------


def test_the_full_depth_does_not_compare_a_pointer_against_a_ref_it_failed_to_refresh():
    """The founding defect, relocated. `rev-parse origin/main` succeeds against a stale ref.

    Dropping the submodule fetch's status let the comparison run anyway, so a pointer was
    reported as agreeing with a remote nobody had contacted — in the depth that exists to make
    exactly that comparison.
    """
    state = entry_state.collect(full=True, git=FakeGit(fails=("fetch --quiet origin",)),
                                gh=FakeGh())

    pointer = state.pointers[0]
    assert pointer.remote is None, "a stale ref must not be read as the remote"
    assert pointer.matches_remote is not True
    assert pointer.remote_unread
    assert not state.clean
    assert any("origin/main could not be read" in item and "fatal" in item
               for item in state.undetermined), "cause and consequence on one line"
    for_ab_lab = [item for item in state.undetermined if item.startswith("ab-lab:")]
    assert len(for_ab_lab) == 1, (
        "one line per pointer: recording the cause in `unread` and deriving the consequence "
        "from the pointer printed both, which is twelve pairs on a network outage")


def test_the_full_depth_reports_a_remote_it_could_not_read():
    """And carries why: `remote.ok` is a second failure path, distinct from the fetch's."""
    state = entry_state.collect(full=True, git=FakeGit(fails=("rev-parse origin/main",)),
                                gh=FakeGh())

    assert not state.clean
    assert any("could not be read" in item and "fatal" in item
               for item in state.undetermined)


@pytest.mark.parametrize("fails, expected", [
    (("rev-parse --abbrev-ref HEAD",), "ab-lab: its branch was not read"),
    (("status --porcelain --untracked-files=no",), "ab-lab: its working tree was not read"),
])
def test_the_full_depth_reports_the_branch_and_tree_reads_it_could_not_make(fails, expected):
    """`remote` got the third state; its two siblings answer §6's other half and had none."""
    state = entry_state.collect(full=True, git=FakeGit(fails=fails), gh=FakeGh())

    matching = [item for item in state.undetermined if expected in item]
    assert matching
    assert all("fatal" in item for item in matching), "the cause travels with the line"
    assert not state.clean


def test_a_pointer_whose_remote_could_not_be_read_is_not_reported_as_agreeing():
    # Only the remote is unread: `branch` and `dirty` carry the same sentinel, so leaving them
    # at `None` would derive three lines and hide which one this test is about.
    unread = entry_state.Pointer(name="ab-lab", sha="433083d", flag=" ", remote=None,
                                 branch="main", dirty=False, probed=True)

    assert unread.remote_unread
    assert not unread.branch_unread and not unread.tree_unread
    assert unread.matches_remote is None
    state = clean_state(full=True, pointers=(unread,))
    assert not state.clean
    assert state.undetermined == (
        "ab-lab: origin/main could not be read, so the pointer was not compared",)


def test_a_pointer_nobody_fetched_does_not_claim_to_agree():
    """`--quick` never asks the remote, and a question not asked is not a question answered."""
    quick = entry_state.parse_pointers(HEALTHY)[0]

    assert quick.matches_remote is None and not quick.remote_unread
    assert clean_state(pointers=(quick,)).clean

    stale = entry_state.Pointer(name="ab-lab", sha="433083d", flag=" ", remote="0000000",
                                probed=True)
    assert stale.matches_remote is False
    assert "ab-lab: pointer is not its own origin/main" in clean_state(
        pointers=(stale,)).findings


def test_a_detached_submodule_is_not_a_finding_when_its_commit_still_matches():
    """`git submodule update` and every CI checkout leave a detached HEAD; the `+` flag is
    what says the commit moved, and this reported the normal state as a problem."""
    detached = entry_state.Pointer(name="ab-lab", sha="433083d", flag=" ", remote="433083d",
                                   branch="HEAD", dirty=False, probed=True)

    assert clean_state(full=True, pointers=(detached,)).clean


# --- the pull requests ---------------------------------------------------------------------


def test_the_two_depths_ask_two_different_questions():
    """§6 row 5 prescribes a list per repository; the search that replaces it in `--quick` lags."""
    quick, full = FakeGh(), FakeGh()

    entry_state.collect(full=False, git=FakeGit(), gh=quick)
    entry_state.collect(full=True, git=FakeGit(), gh=full)

    assert len(quick.calls) == 1 and quick.calls[0][0] == "search"
    assert all(call[0] == "pr" for call in full.calls)
    assert len(full.calls) == portfolio_size()
    assert "read from the search index, which lags" in entry_state.report(clean_state())
    assert "not queried at this depth" in entry_state.report(clean_state(full=True))


@pytest.mark.parametrize("payload", ["not json", "\n", '[{"repository": null}]', "null", "5",
                                     '{"a": 1}', "[1]"])
@pytest.mark.parametrize("full", [False, True])
def test_a_malformed_payload_is_unread_at_either_depth(payload, full):
    """The hardening reached one depth for one revision: `--full` parsed inline and raised.

    `json.loads` raises `ValueError`, a null `repository` raised `AttributeError`, and a bare
    `null` or `5` raises `TypeError` — none of them a `RuntimeError`, and only the first was
    caught. A traceback where the banner should be is the failure mode the third state exists
    to prevent.
    """
    state = entry_state.collect(full=full, git=FakeGit(), gh=FakeGh(payload))

    assert state.open_prs == ()
    assert any("unreadable" in item for item in state.undetermined)
    assert not state.clean


def test_the_search_limit_is_reported_as_truncation_and_not_as_an_answer():
    payload = json.dumps([{"repository": {"name": "other"}, "number": n, "title": "t"}
                          for n in range(entry_state.SEARCH_LIMIT)])

    state = entry_state.collect(full=False, git=FakeGit(), gh=FakeGh(payload))

    assert any("returned its limit" in item for item in state.undetermined)
    assert not state.clean


def test_an_unpinned_repository_is_reported_apart_from_the_portfolio():
    """`infra-docker-workmate` was unpinned in `0004` §9 and still accepts pull requests."""
    payload = json.dumps([
        {"repository": {"name": "ab-lab"}, "number": 12, "title": "the separator"},
        {"repository": {"name": "infra-docker-workmate"}, "number": 73, "title": "stan"},
    ])

    mine, foreign = entry_state.portfolio_prs(payload, frozenset({"ab-lab", "current_projects"}))

    assert mine == (("ab-lab", 12, "the separator"),)
    assert foreign == (("infra-docker-workmate", 73, "stan"),)


def test_a_per_repository_listing_takes_its_name_from_the_repository_asked():
    """The listing payload carries no `repository` field; the search payload does."""
    rows = entry_state.pull_requests('[{"number": 7, "title": "t"}]', repo="ab-lab")

    assert rows == (("ab-lab", 7, "t"),)


def test_no_pull_request_at_all_is_read_as_no_pull_request():
    assert entry_state.portfolio_prs("[]", frozenset({"ab-lab"})) == ((), ())


# --- the findings list, and the registry ---------------------------------------------------


@pytest.mark.parametrize("overrides, expected", [
    ({"behind": 3}, "the index is 3 commit(s) behind origin/main"),
    ({"uncommitted": (" M tools/pagespec/clauses.py",)}, "1 uncommitted change(s) in the index"),
    ({"open_prs": (("ab-lab", 12, "the separator"),)}, "ab-lab#12 is open — the separator"),
])
def test_each_reason_reaches_the_findings_on_its_own(overrides, expected):
    """One reason at a time, because the shape this replaces hid a branch from its own assertion."""
    assert clean_state().clean
    state = clean_state(**overrides)
    assert not state.clean
    assert expected in state.findings


def test_being_ahead_is_reported_and_is_deliberately_not_a_finding():
    """Unpushed commits are the normal state of a session doing something."""
    state = clean_state(ahead=3)

    assert state.clean
    assert "3 ahead" in entry_state.report(state)


def test_an_uninitialised_submodule_is_not_reported_as_a_pointer_that_agrees():
    pointers = entry_state.parse_pointers(
        "-433083df38b3a07a3d5b1e13d271029b2f644d21 ab-lab\n")

    assert not pointers[0].initialised
    assert "ab-lab: not checked out" in clean_state(pointers=pointers).findings


def test_a_checkout_that_moved_off_the_pointer_is_named_as_that_and_not_as_something_else():
    pointers = entry_state.parse_pointers(
        "+433083df38b3a07a3d5b1e13d271029b2f644d21 ab-lab (heads/main)\n")

    assert clean_state(pointers=pointers).findings == (
        "ab-lab: checked-out commit differs from the pointer",)


def test_a_submodule_left_on_a_branch_is_a_finding_even_when_its_pointer_agrees():
    """§6's row is two claims, and a matching pointer discharges only the first of them."""
    on_branch = entry_state.Pointer(name="car-price-ml", sha="832979d", flag=" ",
                                    remote="832979d", branch="fix/the-title", dirty=False,
                                    probed=True)

    assert on_branch.matches_index and on_branch.matches_remote
    assert clean_state(pointers=(on_branch,)).findings == (
        "car-price-ml: on branch fix/the-title, not main",)


def test_a_submodule_with_uncommitted_changes_is_a_finding_even_when_its_pointer_agrees():
    """The other half of §6's working-tree row, and **the half nothing tested.**

    Measured by the test audit of 2026-09-09: `if pointer.dirty:` could be deleted with all
    576 tests green, because no test anywhere constructed `dirty=True` — three build
    `dirty=False` and one `dirty=None`. The branch half above has had a guard since it was
    written; this is the n-1-of-n shape the record names seven times.

    It is not a hypothetical half. `CLAUDE.md` spends a paragraph on what it cost: twelve
    `CLAUDE.md` and eight `README.md` left uncommitted for an hour with two submodules on fix
    branches, so `python -m tools.pagespec` was reading pages nobody had published.
    """
    dirty = entry_state.Pointer(name="doc-extract", sha="832979d", flag=" ", remote="832979d",
                                branch="main", dirty=True, probed=True)

    assert dirty.matches_index and dirty.matches_remote
    assert clean_state(pointers=(dirty,)).findings == (
        "doc-extract: uncommitted changes in the working tree",)


def test_the_repository_list_is_derived_from_gitmodules_and_not_typed():
    names = entry_state.submodule_names(
        '[submodule "b"]\n\tpath = b\n\turl = x\n[submodule "a"]\n\tpath = a\n\turl = y\n')

    assert names == ("a", "b")


def test_the_two_registries_still_name_the_same_repositories():
    """`.gitmodules` and `sources.SURFACES` are two lists of the same thing, tied by nothing."""
    declared = set(entry_state.submodule_names(
        (ROOT / ".gitmodules").read_text(encoding="utf-8")))
    with_a_page = {surface.repo for surface in SURFACES}

    assert declared - with_a_page == NO_PAGE
    assert not with_a_page - declared, "a surface names a repository .gitmodules does not"


def test_a_sentinel_nobody_recorded_is_still_part_of_the_verdict():
    """The derivation rule reached one sentinel field of four.

    `collect` records all of them today, so this was latent — but the argument that justifies
    deriving the pointer's remote (*a caller that forgot to record one would otherwise hand
    back a state that calls itself clean*) applies with identical force to the distance and to
    a pointer's branch and working tree, and those were trusted rather than derived.
    """
    assert not clean_state(ahead=None, behind=None).clean
    assert "the distance from origin/main was not computed" in clean_state(
        ahead=None, behind=None).undetermined
    assert "clean —" not in entry_state.report(clean_state(ahead=None, behind=None))

    # One of the two, not both: `or` and `and` are indistinguishable when a test only ever
    # passes both as `None`, and the asymmetric case is exactly what "a caller that forgot to
    # record one" means. Under `and`, this state called itself clean again.
    assert not clean_state(ahead=None, behind=0).clean
    assert not clean_state(ahead=0, behind=None).clean

    # And the reason travels with the line, or the operator gets a bare statement of fact.
    with_reason = clean_state(ahead=None, behind=None, distance_reason="fatal: bad revision")
    assert with_reason.undetermined == (
        "the distance from origin/main was not computed — fatal: bad revision",)

    blind = entry_state.Pointer(name="ab-lab", sha="433083d", flag=" ", remote="433083d",
                                branch=None, dirty=None, probed=True,
                                branch_reason="fatal: not a git repository",
                                tree_reason="fatal: unable to read index")
    assert blind.branch_unread and blind.tree_unread
    state = clean_state(full=True, pointers=(blind,))
    assert not state.clean
    assert state.undetermined == (
        "ab-lab: its branch was not read — fatal: not a git repository",
        "ab-lab: its working tree was not read — fatal: unable to read index",
    )

    # The fifth sentinel: an unread HEAD leaves both empty, and `index  on ,` is not clean.
    assert not clean_state(head="", branch="").clean


@pytest.mark.parametrize("argv, expected", [(["--hook"], 0), ([], 1)])
def test_an_unexpected_failure_is_a_line_and_not_a_traceback(monkeypatch, capsys, argv, expected):
    """`main` wrapped nothing, so any escaping exception exited 1 — a broken hook.

    That is the exact reading the `--hook` contract exists to prevent, and the module already
    argues the case one function over, where an unreadable `.gitmodules` is a line rather than
    a traceback in the banner.
    """
    def boom(**_):
        raise RuntimeError("the index vanished")

    monkeypatch.setattr(entry_state, "collect", boom)

    assert entry_state.main(argv) == expected
    assert "could not be read: RuntimeError: the index vanished" in capsys.readouterr().out


@pytest.mark.parametrize("argv, expected", [(["--hook"], 0), ([], 1)])
def test_a_stdout_that_fails_mid_banner_is_not_a_traceback_either(monkeypatch, argv, expected):
    """The wrapper covered the read and left the two statements around it bare.

    `print` is the operation the encoding fix is about, and a consumer that stopped reading
    raises `BrokenPipeError` out of it. The guard above mutates `collect`, so it is blind to
    exactly the statement most likely to fail — a guard positioned where it cannot see the
    failure, which is the shape this suite exists to refuse.
    """
    class Stdout:
        def reconfigure(self, **_kwargs):
            pass

        def write(self, _text):
            raise BrokenPipeError(32, "the reader went away")

        def flush(self):
            pass

    monkeypatch.setattr(entry_state, "collect", lambda **_: clean_state())
    monkeypatch.setattr(sys, "stdout", Stdout())

    assert entry_state.main(argv) == expected


def test_the_banner_is_written_as_utf8(monkeypatch):
    """`errors="replace"` changed the handler and not the encoding.

    So the banner went out in this machine's cp1250 and its em dash — which is in the header,
    in every finding, in the "not read" heading and in the clean sentence — became byte 0x97.
    The hook's whole output failed a strict UTF-8 decode at offset 20. The consumer is the
    hook harness, so the encoding is the thing to set; `replace` stays for a pull-request
    title outside it.
    """
    seen: dict[str, object] = {}
    written: list[str] = []

    class Stdout:
        def reconfigure(self, **kwargs):
            seen.update(kwargs)

        def write(self, text):
            written.append(text)
            return len(text)

        def flush(self):
            pass

    monkeypatch.setattr(entry_state, "collect", lambda **_: clean_state())
    monkeypatch.setattr(sys, "stdout", Stdout())
    entry_state.main(["--hook"])

    assert seen.get("encoding") == "utf-8", "the handler was set and the encoding was not"
    assert seen.get("errors") == "replace"
    assert "—" in "".join(written), "the character the encoding is about"


def test_the_report_says_which_depth_answered_it():
    """A reader who cannot tell the two tiers apart will read the cheap one as the expensive one."""
    quick = entry_state.report(clean_state())
    full = entry_state.report(clean_state(full=True))

    assert "pointer vs the index" in quick
    assert "every pointer matches the index" in quick

    assert "pointer vs its own origin/main" in full
    assert "every pointer matches its own origin/main" in full


def test_a_real_finding_under_the_hook_flag_still_exits_zero(monkeypatch, capsys):
    """The `--hook` contract's whole point, and it was untested.

    The module's own docstring: *a session-start banner reporting a real finding must not read
    as a broken hook*. `CLAUDE.md` wires `--hook` to `SessionStart`, so a non-zero exit there
    is the harness saying the hook is broken — over a state the hook read correctly.

    **Mutating `return 0 if (args.hook or state.clean) else 1` to `return 0 if state.clean
    else 1` survived the whole suite.** The two tests that parametrise `(["--hook"], 0)` both
    force an exception and so exercise the `except` branch's own return; the third passes a
    clean state, where both spellings agree. The one case the contract exists for — hook flag,
    real finding — was reached by nothing.
    """
    monkeypatch.setattr(entry_state, "collect",
                        lambda **kwargs: clean_state(uncommitted=("docs/x.md",)))
    assert entry_state.main(["--hook"]) == 0, "a real finding read as a broken hook"
    assert entry_state.main([]) == 1, "and without the flag it must still refuse"
    assert "uncommitted" in capsys.readouterr().out


def test_the_account_the_two_depths_query_is_the_portfolio_owner(monkeypatch):
    """`OWNER` and `INDEX` were bound by nothing.

    Mutating `OWNER` sends every `gh` query to somebody else's repositories, which answers
    empty — the false-clean direction. Mutating `INDEX` drops this repository out of `repos`,
    so an open pull request **here** files under *"outside the portfolio (not a finding)"*,
    which is precisely the 2026-09-07 misreading the module exists to prevent.

    `FakeGh` already recorded the arguments; nothing looked at them.
    """
    quick, full = FakeGh(), FakeGh()
    entry_state.collect(full=False, git=FakeGit(), gh=quick)
    entry_state.collect(full=True, git=FakeGit(), gh=full)

    # The quick depth asks one search, scoped by account.
    assert any(entry_state.OWNER in one for call in quick.calls for one in call), (
        "the session-start query names a different account, which answers empty — the "
        "false-clean direction"
    )
    # The full depth asks per repository, and this repository has to be one of them.
    assert any(entry_state.INDEX in one for call in full.calls for one in call), (
        "the index is not among the repositories queried, so an open pull request here "
        "files as `outside the portfolio` — the 2026-09-07 misreading, mechanised"
    )
    assert entry_state.OWNER == "P0w3r223" and entry_state.INDEX == "current_projects"


def test_a_conflicted_submodule_does_not_read_as_matching_the_index():
    """`U` is documented at `tools/entry_state.py:127` and asserted nowhere.

    It is the flag `git submodule status` gives a submodule with a merge conflict — a tree
    that is neither at the pointer nor cleanly anywhere else. Both readings below are the ones
    that matter: it must not read as matching the index, and it must not read as
    uninitialised, because those two are different findings with different repairs.
    """
    conflicted = entry_state.Pointer(name="ab-lab", sha="433083d", flag="U")

    assert conflicted.matches_index is False
    assert conflicted.initialised is True


def test_git_is_run_with_the_credential_prompt_disabled(monkeypatch):
    """`GIT_TERMINAL_PROMPT=0`, and `entry_state.py`'s own docstring says what it costs.

    `capture_output` gives a credential prompt a stdin nobody is watching, so a repository
    that asks for one **blocks the session-start hook until it is killed**. Removing the
    variable left all 576 tests green: the one line standing between a slow start and a hung
    one was carried by nothing.
    """
    seen = {}

    def _run(argv, **kwargs):
        seen.update(kwargs)
        raise OSError("not actually running git")

    monkeypatch.setattr(entry_state.subprocess, "run", _run)
    entry_state._run(("git", "status"), None)

    assert seen["env"]["GIT_TERMINAL_PROMPT"] == "0"
    assert "PATH" in seen["env"], (
        "the variable is added to the inherited environment and does not replace it — "
        "a bare {'GIT_TERMINAL_PROMPT': '0'} satisfies the line above, loses PATH, and "
        "fails where nothing is watching: at runtime on a machine, not in CI")
