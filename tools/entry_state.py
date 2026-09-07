"""Entry state — the two rows of `0008` §6 that are pure repository state, as an instrument.

§6 is a table of assumptions to verify *before each stage, not once*. Two of its rows are
answerable from git and the GitHub API alone, and those two are the ones that have actually
been mis-discharged:

    The working tree is what the record assumes — no submodule on an unmerged branch,
    no uncommitted file
    No pull request is open and all twelve pointers still match

The second was discharged from a stale ref on 2026-09-07, an hour after `#77` merged, by two
passes independently — `origin/main` is a local file a session inherits and nothing refreshes
on its own. This module refreshes it first and then answers, which is the whole of its value:
**a row that says "`git fetch` first" is a row that depends on somebody remembering.**

Two depths, because the cost is not uniform. Measured on this machine, 2026-09-07:

    index fetch                          1.1 s
    twelve submodule fetches             9.5 s
    open pull requests, one search call  1.2 s
    open pull requests, thirteen lists   7.5 s

`--quick` is the session-start banner and buys speed with a known inaccuracy: `gh search prs`
is served from an index with documented lag, so a just-opened pull request can read as absent.
That is the false-clean direction, so it is stated in the report rather than left in a
docstring. `--full` is what runs before a stage and lists per repository, which is what §6 row
5 prescribes; it also asks whether each pointer still equals its own `origin/main`.

**Every command's exit status is read, and an unread input is part of the verdict.** This took
three passes to get right and the middle one is worth recording, because it is the shape this
repository keeps catching. The first version ignored the status outright, so a `git fetch` that
failed left the run answering from exactly the stale ref it exists to refresh. The second read
the status and appended a *note* — and nothing consulted the notes, so `clean` stayed true, the
run still exited 0, and the report printed `origin/main: level` and *"every pointer matches the
index, nothing uncommitted"* three lines above the reason none of that had been read. The fix
moved the failure from silence to a line, which is not the same as fixing it.

So the verdict is a **tri-state**, and it is derived rather than remembered: `findings` says the
entry state is wrong, `undetermined` says an input this depth promised to read could not be, and
`clean` requires both to be empty. That is `tools/pagespec`'s own rule — a failing clause gates
there, and so does a surface that should have been readable and was not.

**What this deliberately does not check**, so that a clean run is not read as more than it is:
the live pages (that is `python -m tools.pagespec --fetch`), the byte-identity of a served page
against its committed file (§6 row 3, still manual), and the four About descriptions (row 2, an
account surface). Naming them here is cheaper than a reader inferring coverage that does not
exist.

`ahead` is reported and is deliberately **not** a finding: unpushed commits on a working branch
are the normal state of a session that is doing something, and a check that fires on them is a
check that gets ignored.

Usage:

    python -m tools.entry_state              # quick; exit 1 if the entry state needs attention
    python -m tools.entry_state --full       # every pointer against its own remote
    python -m tools.entry_state --hook       # quick, and always exit 0 — the session-start banner

The exit code means one thing wherever it is meaningful: **0 the entry state is clean, 1
something needs attention.** `--hook` suppresses it rather than redefining it, because a
session-start banner reporting a real finding must not read as a broken hook.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

#: The account every portfolio repository lives under. One place, because the pull-request query
#: needs it and a second spelling is a second thing to keep in step.
OWNER = "P0w3r223"

#: The index's own repository name. The twelve others are derived from `.gitmodules` rather than
#: typed — `0008` §5's registry shape: a list that exists in four places drifts in three of them.
INDEX = "current_projects"

#: How many open pull requests one search call will return. Reaching it is not an answer, it is
#: a truncation, and the report says so rather than reading the 51st as absent.
SEARCH_LIMIT = 50

#: Seconds, per subprocess. The bound that matters is the *run's*, not one call's: `--quick`
#: makes two network calls and about five local ones, so a per-call 10 against the hook's 20
#: gave 10 + 10 + local ≈ 21 — the failure then arrives as a killed hook and the line saying
#: why never prints, which is the outcome the ordering exists to prevent. 8 against a hook
#: budget of 30 leaves 8 + 8 + local ≈ 19 with room, and the happy path measures 2.4.
TIMEOUT = 8

ROOT = Path(__file__).resolve().parents[1]

PullRequest = tuple[str, int, str]


@dataclass(frozen=True)
class Run:
    """One subprocess, with the half the first version of this module threw away.

    `_git` returned `done.stdout` and looked at neither the exit status nor stderr, so a failed
    `git fetch` was indistinguishable from a fetch that found nothing to do. Keeping the three
    together makes the failure impossible to drop silently at a call site.
    """

    out: str
    code: int
    err: str

    @property
    def ok(self) -> bool:
        return self.code == 0

    @property
    def reason(self) -> str:
        first = self.err.strip().splitlines()
        return first[0] if first else f"exit {self.code}"


@dataclass(frozen=True)
class Pointer:
    """One submodule as `git submodule status` reports it, plus what `--full` adds."""

    name: str
    sha: str
    #: ' ' matches the index, '+' checked-out commit differs, '-' not initialised, 'U' conflicts.
    flag: str
    remote: str | None = None
    branch: str | None = None
    dirty: bool | None = None
    #: True once `--full` has probed this pointer, whether or not each read succeeded. Without
    #: it, "not asked" and "asked and could not be read" are the same `None`, and the second
    #: reads as agreement in the depth that promised the comparison. It governs all three
    #: reads, not just the remote — `branch` and `dirty` carry the same sentinel.
    probed: bool = False
    #: Why each read failed, when that is known. Carried on the pointer so the derived line
    #: states cause and consequence together instead of the collector adding a second line
    #: beside it — on a network outage that was two lines per submodule. The de-duplication
    #: that introduced this covered the remote alone and dropped the cause from the other two,
    #: where there had been no pair to remove: one recorded line became one bare line, which is
    #: a loss in the depth that runs before a stage.
    remote_reason: str | None = None
    branch_reason: str | None = None
    tree_reason: str | None = None

    @property
    def initialised(self) -> bool:
        return self.flag != "-"

    @property
    def matches_index(self) -> bool:
        return self.flag == " "

    @property
    def matches_remote(self) -> bool | None:
        """None while the question has not been answered — asked or not."""
        return None if self.remote is None else self.sha == self.remote

    @property
    def remote_unread(self) -> bool:
        return self.probed and self.remote is None

    @property
    def branch_unread(self) -> bool:
        return self.probed and self.branch is None

    @property
    def tree_unread(self) -> bool:
        return self.probed and self.dirty is None


@dataclass(frozen=True)
class EntryState:
    head: str
    branch: str
    ahead: int | None
    behind: int | None
    uncommitted: tuple[str, ...]
    pointers: tuple[Pointer, ...]
    open_prs: tuple[PullRequest, ...]
    foreign_prs: tuple[PullRequest, ...]
    full: bool
    #: Inputs this depth promised to read and could not, where the fact is not derivable from
    #: another field. Not findings — the entry state may be perfectly fine — but the run cannot
    #: say so, which is a different thing from saying so.
    unread: tuple[str, ...] = field(default=())
    #: Why `ahead`/`behind` are `None`, when that is known. Carried rather than appended to
    #: `unread`, so the derived line and the recorded reason are one line and not two.
    distance_reason: str | None = None

    @property
    def undetermined(self) -> tuple[str, ...]:
        """Everything unread, including what is derivable from the pointers themselves.

        Derived rather than trusted: a caller that forgot to record an unread remote would
        otherwise hand back a state that calls itself clean. The first version of this module
        made exactly that mistake one level up — a failed command appended a note, and nothing
        consulted the notes, so `clean` stayed true and the run exited 0 while its own report
        printed the reason three lines below the word "clean".

        **Where the rule stops, said here so a later pass does not go looking.** `uncommitted`
        and `pointers` cannot be derived: an empty tuple is a legitimate answer for both, so
        nothing in the value distinguishes *read, and there was nothing* from *not read*. Those
        two rest on `collect` recording the failure, which it does. Every field that carries a
        **sentinel** — a value impossible when the read succeeded — is derived instead, and
        that is now all five of them: `head`/`branch`, the distance, and a pointer's remote,
        branch and working tree.
        """
        def because(reason: str | None) -> str:
            return f" — {reason}" if reason else ""

        out = list(self.unread)
        if not self.head or not self.branch:
            out.append("the index's own HEAD was not read")
        if self.ahead is None or self.behind is None:
            out.append("the distance from origin/main was not computed"
                       + because(self.distance_reason))
        for pointer in self.pointers:
            if pointer.remote_unread:
                out.append(f"{pointer.name}: origin/main could not be read, so the pointer "
                           f"was not compared" + because(pointer.remote_reason))
            if pointer.branch_unread:
                out.append(f"{pointer.name}: its branch was not read"
                           + because(pointer.branch_reason))
            if pointer.tree_unread:
                out.append(f"{pointer.name}: its working tree was not read"
                           + because(pointer.tree_reason))
        return tuple(out)

    @property
    def clean(self) -> bool:
        """Nothing is wrong **and** nothing went unread. Both, because either alone lies.

        `tools/pagespec` gates on a failing clause *and* on a surface that should have been
        readable and was not; this is the same rule, and the module was inconsistent with
        itself until it applied it here as well as to a pointer's remote.
        """
        return not self.findings and not self.undetermined

    @property
    def findings(self) -> tuple[str, ...]:
        """Every reason this entry state is not the one the record assumes, in one place.

        Accumulated into one list rather than kept as separate flags joined at the end: that
        second shape is what `__main__.py` carries for the gate, and the review that found a
        branch missing from its own assertion (`0008` §4.12) found it there. The same lesson,
        applied before rather than after.
        """
        out: list[str] = []
        if self.behind:
            out.append(f"the index is {self.behind} commit(s) behind origin/main")
        if self.uncommitted:
            out.append(f"{len(self.uncommitted)} uncommitted change(s) in the index")
        for pointer in self.pointers:
            if not pointer.initialised:
                out.append(f"{pointer.name}: not checked out")
            elif not pointer.matches_index:
                out.append(f"{pointer.name}: checked-out commit differs from the pointer")
            elif pointer.matches_remote is False:
                out.append(f"{pointer.name}: pointer is not its own origin/main")
            # `HEAD` is what `rev-parse --abbrev-ref` answers for a detached checkout, which is
            # the normal state after `git submodule update` and the state every CI checkout is
            # in. It is only worth reporting when the commit also moved, and the `+` flag above
            # already says that — so detached-and-matching is silence, not a finding.
            if pointer.branch not in (None, "main", "HEAD"):
                out.append(f"{pointer.name}: on branch {pointer.branch}, not main")
            if pointer.dirty:
                out.append(f"{pointer.name}: uncommitted changes in the working tree")
        for repo, number, title in self.open_prs:
            out.append(f"{repo}#{number} is open — {title[:48]}")
        return tuple(out)


def parse_pointers(text: str) -> tuple[Pointer, ...]:
    """`git submodule status` into rows. The leading character is the whole point of the line.

    It sits in column 0 and is a space in the healthy case, so any parse that strips leading
    whitespace first loses exactly the signal this function exists to read.
    """
    out: list[Pointer] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        flag, rest = line[0], line[1:]
        parts = rest.split()
        if len(parts) < 2:
            continue
        out.append(Pointer(name=parts[1], sha=parts[0], flag=flag))
    return tuple(out)


def portfolio_prs(payload: str, repos: frozenset[str]) -> tuple[tuple[PullRequest, ...],
                                                                tuple[PullRequest, ...]]:
    """Split the account's open pull requests into the portfolio's and everything else.

    The account holds repositories the portfolio deliberately dropped — `infra-docker-workmate`
    was unpinned in `0004` §9 and still accepts pull requests. Reporting those under the same
    heading would make an unrelated open pull request read as portfolio work; dropping them
    silently would hide one. So: two lists, and the second is labelled as not a finding.

    Raises `ValueError` on a payload that is not the expected JSON, which the caller turns into
    an unread entry. A malformed answer is not an empty answer.
    """
    mine: list[PullRequest] = []
    foreign: list[PullRequest] = []
    for row in pull_requests(payload):
        (mine if row[0] in repos else foreign).append(row)
    return tuple(sorted(mine)), tuple(sorted(foreign))


def pull_requests(payload: str, *, repo: str | None = None) -> tuple[PullRequest, ...]:
    """Decode one `gh` answer into rows, for either depth.

    Both depths parse the same shape and only the source of the repository name differs — a
    search row carries it, a per-repository listing does not. This existed twice for one
    revision: `portfolio_prs` refused a malformed row while `--full`'s inline loop called
    `.get` straight through, so the hardening the commit claimed reached only the depth that
    was already hardened, and `--full` raised `AttributeError` out of `collect` — a traceback
    where the report should be.

    Every shape that is not a list of objects naming a repository raises `ValueError`; the
    caller records that as unread rather than as an empty answer.
    """
    data = json.loads(payload or "[]")
    if not isinstance(data, list):
        raise ValueError(f"expected a list of rows, got {type(data).__name__}")
    out: list[PullRequest] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"expected an object per row, got {type(item).__name__}")
        name = repo or (item.get("repository") or {}).get("name", "")
        if not name:
            # Not tolerated into the foreign list. A row with no repository is malformed, and
            # filing it as an unnamed foreign pull request would turn a broken answer into a
            # quiet line nobody can act on — the shape this whole module argues against.
            raise ValueError("a row names no repository")
        number, title = item.get("number"), item.get("title")
        if not isinstance(number, int) or not isinstance(title, str):
            # `.get("number", 0)` filled a missing field with a pull request number that does
            # not exist — the same fabricated fallback as the `(0, 0)` that printed as
            # `origin/main: level`. A row missing either field is malformed, and at the
            # per-repository depth it is the only thing left to check, since the name comes
            # from the query rather than from the answer.
            raise ValueError("a row is missing its number or title")
        out.append((name, number, title))
    return tuple(out)


def submodule_names(gitmodules: str) -> tuple[str, ...]:
    """The paths `.gitmodules` declares. Derived, so a thirteenth project is one edit and not four.

    These are checkout *paths*, and `_open_prs` spends them as GitHub repository *names*. That
    holds for all twelve today and is not guaranteed by anything; a path that diverged from its
    repository name would make `gh pr list -R` fail, which becomes an unread entry rather than a
    false clean — so it fails in the safe direction, but it is a conflation and not a fact.
    """
    out = [line.split("=", 1)[1].strip()
           for line in gitmodules.splitlines() if line.strip().startswith("path")]
    return tuple(sorted(out))


def _run(argv: tuple[str, ...], cwd: Path | None) -> Run:
    # `GIT_TERMINAL_PROMPT=0` alone. Setting `GIT_ASKPASS` to the empty string does not disable
    # the helper — git tries to exec it and falls back — so it bought nothing and read as
    # though it were doing the work this variable actually does.
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        done = subprocess.run(argv, cwd=cwd or ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=TIMEOUT, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        return Run("", 1, f"{type(exc).__name__}: {exc}")
    return Run(done.stdout, done.returncode, done.stderr)


def _git(*args: str, cwd: Path | None = None) -> Run:
    """Raw stdout, deliberately unstripped — see `parse_pointers`.

    This returned a stripped string for one revision, and `git submodule status` puts its flag
    in column 0 where a healthy row is a space: stripping ate the first row's flag, so `ab-lab`
    alone reported *"checked-out commit differs from the pointer"* against a tree where it did
    not. `parse_pointers` already said in prose that a parse must not strip first; the rule was
    right and was applied one layer too shallow, which is `0008` §3.2's lesson about a token's
    ground. Callers that want a scalar strip at the call site.

    `GIT_TERMINAL_PROMPT=0` because `capture_output` gives a credential prompt a stdin nobody
    is reading, and the session-start hook would then block until the harness killed it.
    """
    return _run(("git", *args), cwd)


def _gh(*args: str) -> Run:
    return _run(("gh", *args), None)


def _open_prs(gh, repos: frozenset[str], full: bool,
              unread: list[str]) -> tuple[tuple[PullRequest, ...], tuple[PullRequest, ...]]:
    """The open pull requests, at the depth asked for.

    `--full` lists per repository, which is §6 row 5's own prescription and is authoritative.
    `--quick` uses one search call, which is six times faster and is served from an index with
    lag — so it can report a just-opened pull request as absent, which is the false-clean
    direction. The report names which of the two answered.
    """
    if full:
        mine: list[PullRequest] = []
        for repo in sorted(repos):
            run = gh("pr", "list", "-R", f"{OWNER}/{repo}", "--state", "open",
                     "--json", "number,title")
            if not run.ok:
                unread.append(f"{repo}: open pull requests not read — {run.reason}")
                continue
            try:
                mine.extend(pull_requests(run.out, repo=repo))
            except (ValueError, TypeError, AttributeError) as exc:
                unread.append(f"{repo}: open pull requests unreadable — {exc}")
        return tuple(sorted(mine)), ()

    run = gh("search", "prs", "--owner", OWNER, "--state", "open",
             "--json", "repository,number,title", "--limit", str(SEARCH_LIMIT))
    if not run.ok:
        unread.append(f"open pull requests not read — {run.reason}")
        return (), ()
    try:
        mine_t, foreign_t = portfolio_prs(run.out, repos)
    except (ValueError, TypeError, AttributeError) as exc:
        unread.append(f"open pull requests unreadable — {exc}")
        return (), ()
    if len(mine_t) + len(foreign_t) >= SEARCH_LIMIT:
        unread.append(f"the search returned its limit of {SEARCH_LIMIT}; there may be more")
    return mine_t, foreign_t


def collect(full: bool, *, git=_git, gh=_gh) -> EntryState:
    """Read the entry state. `git` and `gh` are injectable so the failure paths are testable.

    Without the seam the only untested function in this module would be the one that turns a
    failed command into a verdict — which is where the first version's defect lived.
    """
    unread: list[str] = []

    fetched = git("fetch", "--quiet", "origin")
    if not fetched.ok:
        unread.append(f"origin/main not refreshed — {fetched.reason}")

    # No `unread.append` here either: an empty `head` or `branch` is a sentinel, so
    # `undetermined` derives it — the fifth field the rule reaches.
    named = git("rev-parse", "--short", "HEAD")
    on = git("rev-parse", "--abbrev-ref", "HEAD")
    head, branch = named.out.strip(), on.out.strip()

    counted = git("rev-list", "--left-right", "--count", "HEAD...origin/main")
    counts = counted.out.split()
    distance_reason = None
    # `isdecimal`, not `isdigit`: `'²'.isdigit()` is True and `int('²')` raises. Unreachable
    # from `git rev-list`, and the wrapper in `main` would catch the escape — but it would cost
    # the whole banner where this costs one field, which is the opposite of the intent.
    if counted.ok and len(counts) == 2 and all(part.isdecimal() for part in counts):
        ahead, behind = int(counts[0]), int(counts[1])
    else:
        # `None` and not `(0, 0)`: the fallback printed as `origin/main: level`, which is a
        # fabricated fact standing beside the line saying it could not be computed. Adding the
        # note without removing the fabrication left the reader two answers and no ranking.
        ahead, behind = None, None
        distance_reason = counted.reason

    # `--ignore-submodules=dirty` because an untracked `.claude/` inside a submodule renders here
    # as ` M <name>`, and that is not an uncommitted change *in the index*. Submodule trees are
    # answered below by `--full`, where the answer can name the submodule.
    status = git("status", "--porcelain", "--ignore-submodules=dirty")
    if not status.ok:
        unread.append(f"the index's working tree was not read — {status.reason}")
    uncommitted = tuple(line for line in status.out.splitlines() if line.strip())

    listed = git("submodule", "status")
    if not listed.ok:
        unread.append(f"the submodule pointers were not read — {listed.reason}")
    pointers = parse_pointers(listed.out)

    if full:
        resolved: list[Pointer] = []
        for pointer in pointers:
            path = ROOT / pointer.name
            if not pointer.initialised or not path.exists():
                resolved.append(pointer)
                continue
            # Read, not fired and forgotten. Dropping this status let `rev-parse origin/main`
            # succeed against the ref the fetch had failed to refresh, so a pointer was
            # reported as agreeing with a remote nobody had contacted — the module's founding
            # defect, relocated into the depth whose whole promise is that comparison.
            refreshed = git("fetch", "--quiet", "origin", cwd=path)
            remote = git("rev-parse", "origin/main", cwd=path) if refreshed.ok else None
            reason = None if refreshed.ok else refreshed.reason
            if remote is not None and not remote.ok:
                reason = remote.reason

            head_of = git("rev-parse", "--abbrev-ref", "HEAD", cwd=path)
            # `--untracked-files=no` here and untracked files *counted* for the index above.
            # The asymmetry is deliberate: an untracked file in the index is work in progress
            # that §6's row is about, while an untracked `.claude/` inside a submodule is a
            # per-machine directory that says nothing about whether that page was published.
            tree = git("status", "--porcelain", "--untracked-files=no", cwd=path)

            # No `unread.append` here: every one of these three failures is derivable from the
            # pointer, and `undetermined` derives it. Recording it in both places printed two
            # lines per submodule for one cause — twelve of them on a network outage, in the
            # depth that runs before a stage.
            resolved.append(Pointer(
                name=pointer.name, sha=pointer.sha, flag=pointer.flag,
                remote=(remote.out.strip()[:len(pointer.sha)]
                        if remote is not None and remote.ok and remote.out.strip() else None),
                branch=head_of.out.strip() if head_of.ok else None,
                dirty=bool(tree.out.strip()) if tree.ok else None,
                probed=True, remote_reason=reason,
                branch_reason=None if head_of.ok else head_of.reason,
                tree_reason=None if tree.ok else tree.reason,
            ))
        pointers = tuple(resolved)

    try:
        declared = submodule_names((ROOT / ".gitmodules").read_text(encoding="utf-8"))
    except OSError as exc:
        # The one input outside the `Run` discipline, and unreadable it would be a traceback in
        # the banner rather than a line in it.
        declared = ()
        unread.append(f".gitmodules was not read — {exc}")
    repos = frozenset({INDEX, *declared})
    open_prs, foreign_prs = _open_prs(gh, repos, full, unread)

    return EntryState(head=head, branch=branch, ahead=ahead, behind=behind,
                      uncommitted=uncommitted, pointers=pointers, open_prs=open_prs,
                      foreign_prs=foreign_prs, full=full, unread=tuple(unread),
                      distance_reason=distance_reason)


def report(state: EntryState) -> str:
    depth = "full" if state.full else "quick"
    checked = "pointer vs its own origin/main" if state.full else "pointer vs the index"
    lines = [f"entry state ({depth}) — index {state.head} on {state.branch}, "
             f"{len(state.pointers)} submodules, {checked}"]

    if state.ahead is None or state.behind is None:
        lines.append("  origin/main: not computed")
    elif state.ahead or state.behind:
        lines.append(f"  origin/main: {state.ahead} ahead, {state.behind} behind")
    else:
        lines.append("  origin/main: level")

    if state.findings:
        lines.append("")
        lines.extend(f"  ! {finding}" for finding in state.findings)

    if state.undetermined:
        lines.append("")
        lines.append("  not read — the entry state may be fine; this run cannot say so:")
        lines.extend(f"  ? {item}" for item in state.undetermined)

    if state.clean:
        agree = ("every pointer matches its own origin/main" if state.full
                 else "every pointer matches the index")
        lines.append(f"  clean — no open portfolio pull request, {agree}, nothing uncommitted")

    if state.foreign_prs:
        lines.append("")
        lines.append("  outside the portfolio (not a finding, and not nothing):")
        lines.extend(f"    {repo}#{number} — {title[:56]}"
                     for repo, number, title in state.foreign_prs)

    lines.append("")
    if state.full:
        # Said rather than left to be noticed: the authoritative depth queries the portfolio's
        # own repositories, so it cannot see an unpinned one. A reader who met that block in
        # `--quick` would otherwise read its absence here as "none open".
        lines.append("  pull requests listed per portfolio repository; a repository outside the "
                     "portfolio is not queried at this depth")
    else:
        lines.append("  pull requests read from the search index, which lags; "
                     "before a stage: python -m tools.entry_state --full")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="entry_state", description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="fetch every submodule, compare each pointer to its own remote, "
                             "and list pull requests per repository")
    parser.add_argument("--hook", action="store_true",
                        help="quick, and always exit zero — the session-start banner")
    args = parser.parse_args(argv)

    # The whole body, not just `collect`. The wrapper covered the read and left the two
    # statements around it bare — including `print`, which is the operation the encoding fix
    # below is about: a consumer that stopped reading raises `BrokenPipeError` out of `print`,
    # and a detached buffer raises out of `reconfigure`. Both produced the traceback and the
    # non-zero exit that the `--hook` contract exists to prevent, and the guard could not see
    # them because it mutates `collect`.
    try:
        # `errors="replace"` alone changed the handler and not the encoding, so the banner went
        # out in this machine's cp1250: the em dash in the header, in every finding and in the
        # clean sentence became byte 0x97, and the hook's whole output failed a strict UTF-8
        # decode at offset 20. The consumer is the hook harness, so UTF-8 is the answer rather
        # than dropping the dash. `errors` stays because the encoding cannot be assumed to hold
        # for every consumer of this text, and a lone surrogate in a title is still possible.
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")

        state = collect(full=args.full)
        print(report(state))
    except Exception as exc:  # noqa: BLE001 — the alternative is a traceback in the banner
        try:
            print(f"entry state could not be read: {type(exc).__name__}: {exc}")
        except Exception:  # noqa: BLE001
            # The failure can be stdout itself, in which case saying so is not available
            # either. The exit code is the half of the contract that still works.
            pass
        return 0 if args.hook else 1

    return 0 if (args.hook or state.clean) else 1


if __name__ == "__main__":
    sys.exit(main())
