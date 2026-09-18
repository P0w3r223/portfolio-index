"""The queue's state, computed from `0010` rather than counted by hand.

`CLAUDE.md` sends a session asking *what next* to `0010` §3.1 and §4. That document is 2 800
lines, and the answer is spread across a session table, a sentence naming the order of the
twelve, and a table of rows whose `Open` column was prose until 2026-09-18 — so the answer was
a hand count, in the repository whose first standing rule is that a figure comes from an
instrument and whose three hand counts of one population read 15, 18 and 19 against a true 20.

**What this module claims, and what it cannot.** It reports what the document *says*: which
sessions have a row, what state each row item carries, and whether the commits the rows cite
resolve. It cannot tell a row someone repaired and forgot to mark from a row that is genuinely
open — that is `ST-1`, a sentence outliving the state it describes, and no parser sees it. The
half it does carry is the half an instrument can: an id with no state word, a state word
outside the vocabulary, a span and an order sentence that disagree about how many sessions
there are, and a commit citation no reader can resolve.

**Printed, never gated**, like `tools.spec` and `tools.citations`. The refusing half lives in
`tests/test_queue.py`, which is where a malformed cell or an unresolvable `Index SHA` fails.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "audit" / "0010_the-portfolio-audit.md"

TIMEOUT = 30

#: The five words an `Open` cell may carry; §4's header defines them. Two have no instance
#: today and are declared anyway, which that header states as a decision rather than leaving
#: a reader to find an empty bucket and wonder.
STATES = ("open", "closed", "declined", "deferred", "pending")

#: `A-4 open`, `B-4a open`, `R-1 deferred`. The id shape is the document's own, collisions and
#: all — `A-4` names row 4 as well as that row's A-axis finding, and §4's header records the
#: collision rather than renumbering the 25 sites a repair would move.
_ITEM = re.compile(r"^(?P<id>[A-Z]-\d+[a-z]?) (?P<state>[a-z]+)$")

#: The sentence that sets the order of sessions 1–12, matched on its opening rather than on
#: its content: the repositories are read out of it, so a pattern naming them would be the
#: registry this module exists to avoid.
_ORDER = re.compile("^Order for 1[–-]12:")

#: A session number in §3.1's first column: `0`, `1–12`, `13`, `13b`, `13c`. Both dashes,
#: because an en dash and a hyphen are indistinguishable to a reader and not to a parser.
_SPAN = re.compile("^(?P<from>\\d+)[–-](?P<to>\\d+)$")

_TICKED = re.compile(r"`([^`]+)`")

#: A commit citation in a row body: a backticked 7-to-40 hex token. Bounded below at seven on
#: purpose — `0007` and `0008` are backticked four-digit document numbers on nearly every line
#: of this record, and an unbounded reader calls every one of them a commit.
_SHA = re.compile(r"`([0-9a-f]{7,40})`")


@dataclass(frozen=True)
class Item:
    """One `id state` pair out of an `Open` cell."""

    row: str
    id: str
    state: str


@dataclass(frozen=True)
class Row:
    """One line of §4's table."""

    number: str
    repo: str
    index_sha: str
    items: tuple[Item, ...]


@dataclass(frozen=True)
class Session:
    """One line of §3.1's table, with a span expanded into its members."""

    number: str
    subject: str
    kind: str


@dataclass(frozen=True)
class Run:
    out: str
    code: int
    err: str = ""


def _git(*args: str, cwd: Path | None = None) -> Run:
    """`tools/citations.py`'s `_git`, plus a working directory: this module asks a submodule
    the same question it asks the index."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        done = subprocess.run(("git", *args), cwd=cwd or ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=TIMEOUT, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        return Run("", 1, f"{type(exc).__name__}: {exc}")
    return Run(done.stdout, done.returncode, done.stderr)


def _lines() -> list[str]:
    try:
        return AUDIT.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise AssertionError(f"{AUDIT.name}: cannot be read ({exc})") from exc


def _section(heading: str) -> list[str]:
    """The lines of one section, bounded by the next heading of the same depth or shallower.

    **The bound is the whole of this function**, and it was added after the first version
    reported 109 sessions: a three-column table is a common shape in this record, and a reader
    that takes every one of them answers about whichever sections happen to be written that
    way. `tools/citations.py` bounds its heading index by depth for the same reason, one
    document over, where an unbounded reader admitted ordered-list items as sections.
    """
    out: list[str] = []
    inside = False
    depth = heading.split(" ")[0]
    for line in _lines():
        if line.startswith(heading):
            inside = True
            continue
        if inside:
            if line.startswith("#") and len(line.split(" ")[0]) <= len(depth):
                break
            out.append(line)
    if not inside:
        raise AssertionError(f"{AUDIT.name}: no heading beginning {heading!r}")
    return out


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def order() -> tuple[str, ...]:
    """The twelve submodules in the order §3.1 sets, read from the sentence that sets it.

    Fails loudly when that sentence moves. A queue tool that silently reported an empty order
    would answer *nothing left to scan*, which is the worst wrong answer available to it and
    the shape `tools/citations.py`'s `ledger_headings()` guards one document over.
    """
    lines = _section("### 3.1 ")
    for number, line in enumerate(lines):
        if not _ORDER.match(line):
            continue
        # **The sentence is a paragraph, not a line**, and reading only the line it opens on
        # returned two repositories out of twelve — a queue eleven sessions short, reported
        # without complaint. The span check in `sessions()` is what caught it, which is the
        # argument for having written the two halves to disagree out loud.
        paragraph = []
        for text in lines[number:]:
            if not text.strip():
                break
            paragraph.append(text)
        return tuple(_TICKED.findall(" ".join(paragraph)))
    raise AssertionError(
        f"{AUDIT.name}: no line beginning `Order for 1–12:` — §3.1's order sentence "
        f"has moved or been reworded, and the queue cannot be read without it")


def sessions() -> tuple[Session, ...]:
    """§3.1's table, with `1–12` expanded against `order()`.

    The expansion is the cross-check worth having: a span of twelve beside an order sentence
    naming eleven repositories is a queue that has lost one, and neither half says so alone.
    """
    names = order()
    found: list[Session] = []
    for line in _section("### 3.1 "):
        if not line.startswith("| "):
            continue
        cells = _cells(line)
        if len(cells) != 3 or cells[0] == "#" or set(cells[0]) <= {"-"}:
            continue
        span = _SPAN.match(cells[0])
        if span:
            first, last = int(span.group("from")), int(span.group("to"))
            count = last - first + 1
            if count != len(names):
                raise AssertionError(
                    f"{AUDIT.name}: §3.1's span `{cells[0]}` covers {count} session(s) and its "
                    f"order sentence names {len(names)}")
            found.extend(Session(str(first + n), name, cells[2])
                         for n, name in enumerate(names))
            continue
        found.append(Session(cells[0], cells[1], cells[2]))
    if not found:
        raise AssertionError(f"{AUDIT.name}: §3.1's session table parsed as empty")
    return tuple(found)


def rows() -> tuple[Row, ...]:
    """§4's table, one `Row` per line, with the `Open` cell parsed into items."""
    found: list[Row] = []
    inside = False
    width = 0
    for line in _lines():
        if line.startswith("| # | Repo | Index SHA"):
            inside = True
            width = len(_cells(line))
            continue
        if not inside:
            continue
        # The separator row is `|---|---|`, with no space after the pipe, so the bound has to
        # be "not a table line at all" rather than "does not open like a row". Written as the
        # narrower test first, which parsed the table as empty and said so loudly rather than
        # reporting a queue with nothing in it.
        if not line.startswith("|"):
            break
        cells = _cells(line)
        if set(cells[0]) <= {"-"}:
            continue
        # **A malformed row is loud, and the reason is the answer it would otherwise give.**
        # Dropping a row silently takes its number out of `scanned()` and puts the session back
        # into `remaining()` — so the queue answers *scan this again* about work already done,
        # which costs a session. Every other bound in this module raises; this one returned
        # `continue` until the review of the stage that wrote it measured what the silence
        # produced.
        #
        # **The width comes from the header rather than from a literal**, and the difference is
        # not cosmetic: written as `< 9` against a ten-column table, this admitted a row with a
        # column missing, shifted every cell after the gap by one, and read the `Not checked`
        # prose as the `Open` cell. The mutation that removed a column went green and the
        # battery said so — which is `0010` §3.6 working, one observation later than it should
        # have been needed.
        if len(cells) != width:
            raise AssertionError(
                f"{AUDIT.name}: §4's header declares {width} column(s) and a row carries "
                f"{len(cells)}: {line[:60]}...")
        items = []
        for raw in cells[8].split("·"):
            text = raw.strip().strip("*")
            if not text:
                continue
            match = _ITEM.match(text)
            items.append(Item(cells[0], match.group("id"), match.group("state"))
                         if match else Item(cells[0], text, "?"))
        found.append(Row(cells[0], cells[1].strip("`*"), cells[2].strip("`"), tuple(items)))
    if not found:
        raise AssertionError(f"{AUDIT.name}: §4's row table parsed as empty")
    return tuple(found)


def malformed(found: tuple[Row, ...] | None = None) -> tuple[Item, ...]:
    """Every `Open` item that is not an id followed by one word from `STATES`."""
    return tuple(item for row in (found if found is not None else rows()) for item in row.items
                 if item.state not in STATES)


def scanned(found: tuple[Row, ...] | None = None) -> frozenset[str]:
    """The **session numbers** §4 already holds a row for.

    Keyed on the number rather than on the repository, and that is not a detail. Three of the
    fifteen sessions have no submodule as their subject — 13 is this repository, 13b the
    profile README, 13c four repositories outside the portfolio — so a set of repository names
    can never contain them and they would sit in `remaining()` for ever, with no instruction in
    either prompt telling anyone how to take them out. Found by the review of the stage that
    wrote this function, which asked how sessions 13 to 13c ever close.
    """
    return frozenset(row.number for row in (found if found is not None else rows())
                     if row.number and not set(row.number) <= {"\u2014", "-"})


def remaining() -> tuple[Session, ...]:
    """Every session with no row, in §3.1's order. The answer to *what next*."""
    done = scanned()
    return tuple(one for one in sessions()
                 if one.kind not in {"done", "repair"} and one.number not in done)


def shallow(cwd: Path | None = None) -> bool:
    """Whether this checkout has a truncated history, which no ancestry question survives."""
    return _git("rev-parse", "--is-shallow-repository", cwd=cwd).out.strip() == "true"


def gitlink(name: str) -> str | None:
    """The commit this repository pins for a submodule, read from `HEAD`'s tree.

    **`HEAD:` and not the checkout**, and the difference is the whole reason this exists: the
    working tree is what a session may have moved a minute ago, and the gitlink is what a
    reader who clones `main` actually gets. A submodule the index does not pin returns `None`
    rather than raising — `0010` §3.1's session 13b and 13c name repositories outside the
    twelve, and a row may legitimately cite one.
    """
    done = _git("rev-parse", f"HEAD:{name}")
    return done.out.strip() if done.code == 0 else None


def ancestry() -> tuple[tuple[Row, str], ...]:
    """Each row's `Index SHA` against the checkout this runs in.

    **The question is asked of `HEAD` and not of `origin/main`**, which is a choice with a
    cost: a row citing a commit on the branch under review is an ancestor of `HEAD` there and
    stops being one once the squash lands, so that defect is refused on `main` rather than in
    the pull request. `origin/main` is not a ref every checkout has — `actions/checkout` fetches
    the ref it was asked for — and a guard that skipped in CI would refuse nothing at all.

    Four answers. `ancestor` is the good one. `unresolved` means no such commit exists here,
    which is the transplant class: a row written in the archive citing a commit this
    repository does not carry, removed by hand twice already. `off` means the commit resolves
    and is not reachable — a branch SHA quoted after its squash landed, which `CLAUDE.md` has
    a paragraph about and no instrument. `shallow` means the checkout cannot answer, and the
    workflow is what keeps that from being the answer in CI.
    """
    if shallow():
        return tuple((row, "shallow") for row in rows())
    out = []
    for row in rows():
        sha = row.index_sha
        if not sha or not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            # A numbered row with no readable SHA is a row whose scan cannot be reproduced;
            # the portfolio-wide row legitimately has none. The two were one verdict until the
            # review, and `none` printed nowhere — a state declared with no instance and no
            # carrier, which is the shape §4's header had just named about `declined`.
            out.append((row, "none" if not row.number[:1].isdigit() else "missing"))
        elif _git("cat-file", "-e", f"{sha}^{{commit}}").code != 0:
            out.append((row, "unresolved"))
        elif _git("merge-base", "--is-ancestor", sha, "HEAD").code != 0:
            out.append((row, "off"))
        else:
            out.append((row, "ancestor"))
    return tuple(out)


def _bodies() -> dict[str, list[str]]:
    """Each row's body, keyed by its heading id — `### A-4 — ...` down to the next `###`.

    Bounded to §4, and the bound is not tidiness. Read against the whole file, the last row's
    body never ends: `current` survives `## 5.` and `## 6.`, so §6's correction table joins A-3
    and `sibling_citations()` reported an **index** SHA as an unresolvable commit in
    `it-job-radar`, on the strength of that repository's name appearing in the same cell. The
    census caught it on its first run and the finding was false. Second instance in this module
    of a reader answering about sections nobody pointed it at.
    """
    out: dict[str, list[str]] = {}
    current = None
    for line in _section("## 4. "):
        if line.startswith("### "):
            head = line[4:].split(" ")[0].strip()
            current = head if _ITEM.match(f"{head} open") else None
            if current:
                out.setdefault(current, [])
        elif current is not None:
            out[current].append(line)
    return out


def sibling_citations() -> tuple[tuple[str, str, str, str], ...]:
    """Commits a row body cites in a sibling repository: row, repo, sha, verdict.

    **Attributed by adjacency, never by guessing**, which is `tools/citations.py`'s position
    one module over: a hex token counts only where a submodule's name is backticked earlier on
    its own line, and a token with no repository on the line is dropped rather than credited
    to the nearest one. A wrong attribution resolves green, which is worse than no reading.

    **In CI this census says nothing and that is by design.** `core` checks out no submodule,
    so every verdict is `not checked out`; `surfaces` checks them out at the depth
    `actions/checkout` chooses, so every verdict is `shallow`. It is an instrument for a
    working session, and the guard over it asserts only that its vocabulary holds — giving
    `surfaces` a full history to make it speak would buy a heuristic a job, which is the wrong
    order.

    Printed and never gated, and that is a measurement rather than modesty: the attribution is
    a heuristic over a population small enough to read, and this portfolio has already
    convicted one source-text heuristic for punishing the better pattern — `0010` §5, closed
    at `apply-scout` `78d9899`.
    """
    repos = set(order())
    pins: dict[str, str | None] = {}
    out = []
    for row, body in _bodies().items():
        for line in body:
            names = [tick for tick in _TICKED.findall(line) if tick in repos]
            if not names:
                continue
            tree = ROOT / names[0]
            for sha in _SHA.findall(line):
                if not (tree / ".git").exists():
                    how = "not checked out"
                elif shallow(tree):
                    how = "shallow"
                elif _git("cat-file", "-e", f"{sha}^{{commit}}", cwd=tree).code != 0:
                    how = "unresolved"
                elif _git("merge-base", "--is-ancestor", sha, "origin/main", cwd=tree).code != 0:
                    how = "off main"
                else:
                    how = _against_the_pin(names[0], sha, tree, pins)
                out.append((row, names[0], sha, how))
    return tuple(out)


def _against_the_pin(name: str, sha: str, tree: Path,
                     pins: dict[str, str | None]) -> str:
    """`on main` splits in two once the question is asked of the gitlink as well.

    A commit merged in the sibling and not yet pointed at is on that repository's `main` and
    invisible to every reader of this one — which is exactly `0010` §4's definition of
    `pending`, and what let `766203a` write seven × `closed` over a pointer still holding none
    of the repairs. The old reading called that `on main` and said nothing.
    """
    if name not in pins:
        pins[name] = gitlink(name)
    pin = pins[name]
    if pin is None:
        return "on main"
    return ("on main" if _git("merge-base", "--is-ancestor", sha, pin, cwd=tree).code == 0
            else "beyond the gitlink")


def unpinned_closures() -> tuple[tuple[Row, str, str], ...]:
    """Rows claiming no open work while citing a commit this repository does not pin yet.

    **Printed, never gated, and for the same measured reason as the census it reads.** The
    attribution underneath is adjacency on a line; a wrong one here would redden a build over
    a sentence. What it buys is that the state has a name in the report instead of being
    invisible — the defect this closes was not that the row was wrong but that no instrument
    could say so.

    A row is only paired with a citation **in its own repository**: a row body citing some
    other sibling's commit is ordinary cross-reference and says nothing about this row's
    pointer.
    """
    by_repo = {row.repo: row for row in rows()}
    out: list[tuple[Row, str, str]] = []
    for _, repo, sha, how in sibling_citations():
        if how != "beyond the gitlink":
            continue
        row = by_repo.get(repo)
        if row is None:
            continue
        states = {item.state for item in row.items}
        if states & {"open", "pending"}:
            continue
        out.append((row, sha, " · ".join(sorted(states))))
    return tuple(out)


def _state_block(found: tuple[Row, ...], items: list[Item],
                 counted: dict[str, int]) -> list[str]:
    """The tally, with every declared state printed including the empty ones.

    An empty bucket that prints nothing is a state that exists only in a document, which is
    what §4's header says `declined` and `pending` must not become.
    """
    lines = [f"  rows         {len(items)} item(s) across {len(found)} row(s)"]
    for state in STATES:
        note = "" if counted[state] else "   — declared, no instance yet"
        lines.append(f"    {state:<10} {counted[state]}{note}")
    return lines


def report() -> list[str]:
    found = rows()
    # `done` is session 0, this document, and `repair` is `R1…Rn`, which is not a queue but a
    # kind. §3.1's own sentence says **fifteen sessions, not sixteen**, and this is that
    # sentence computed rather than quoted.
    queue = tuple(one for one in sessions() if one.kind not in {"done", "repair"})
    left = remaining()
    items = [item for row in found for item in row.items]
    counted = {state: sum(1 for item in items if item.state == state) for state in STATES}

    lines = [f"queue — {len(queue)} session(s) in `0010` §3.1, "
             f"{len(queue) - len(left)} with a row in §4, {len(left)} to go", ""]
    def _name(one: Session) -> str:
        """A session's subject, short enough for a queue line. §3.1 writes three of them as a
        sentence with its scope attached, and the scope belongs in §3.1 rather than here."""
        return one.subject.split(" — ")[0].replace("**", "").strip()

    lines.append(f"  next         {left[0].number} {_name(left[0])}" if left
                 else "  next         nothing: every session in the queue has a row")
    if left:
        lines.append("  remaining    "
                     + " · ".join(f"{one.number} {_name(one)}" for one in left))
    lines.append("")
    lines.extend(_state_block(found, items, counted))

    for state in STATES:
        by_row = [(row, [one for one in row.items if one.state == state]) for row in found]
        by_row = [(row, got) for row, got in by_row if got]
        if state == "closed" or not by_row:
            continue
        lines.append("")
        lines.append(f"  {state}")
        for row, got in by_row:
            who = row.repo if row.repo else "portfolio-wide"
            lines.append(f"    {row.number:<3} {who:<21} "
                         + " · ".join(one.id for one in got))

    bad = malformed(found)
    lines.append("")
    if bad:
        lines.append(f"  malformed    {len(bad)} `Open` item(s) outside the vocabulary")
        for item in bad:
            lines.append(f"      row {item.row}: {item.id!r}")
    else:
        lines.append("  malformed    0 — every `Open` item is an id and a state word")

    verdicts = ancestry()
    good = sum(1 for _, how in verdicts if how == "ancestor")
    lines.append(f"  index SHAs   {len(verdicts)} cited, {good} reachable from HEAD")
    for row, how in verdicts:
        if how != "ancestor":
            lines.append(f"      row {row.number}: `{row.index_sha}` — {how}")

    cited = sibling_citations()
    if cited:
        tally: dict[str, int] = {}
        for _, _, _, how in cited:
            tally[how] = tally.get(how, 0) + 1
        lines.append(f"  sibling SHAs {len(cited)} cited in row bodies — "
                     + ", ".join(f"{count} {how}" for how, count in sorted(tally.items())))
        for row, repo, sha, how in cited:
            if how in {"unresolved", "off main", "beyond the gitlink"}:
                lines.append(f"      {row}: {repo} `{sha}` — {how}")
        lines.append("      attributed by adjacency, printed and never gated: a wrong")
        lines.append("      attribution resolves green, and this population is small enough")
        lines.append("      for a reader to take the list apart by hand")

        unpinned = unpinned_closures()
        if unpinned:
            lines.append(f"  unpinned     {len(unpinned)} row(s) claiming no open work over a "
                         "commit this repository does not pin")
            for row, sha, states in unpinned:
                lines.append(f"      row {row.number} {row.repo}: `{sha}` — cells read "
                             f"{states}, which §4 defines as `pending`")
            lines.append("      the repair is merged in the sibling and the gitlink still")
            lines.append("      predates it, so no reader of this repository can see it")
    return lines


def main() -> int:
    for line in report():
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
