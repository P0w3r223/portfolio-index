"""Every section reference in this index, and whether the section it names exists.

The resolver `ADR-0009` §3 step 1 calls for. `0008` is 3413 lines cited from 28 tracked files
in prose — comments, docstrings, a CI workflow, `CLAUDE.md` — and **nothing reads it**:
`tools/spec.py` opens `0007` and is the only record reader in `tools/`. So a renumbered or
renamed section arrives as silently wrong pointers, with no guard to redden before the move.
That is this repository's own worst failure class, and `0008` §3.7, §3.9 and §3.10 are where
it is named.

**Three states, and only one of them can fail.** A citation is `resolved` when the document it
names holds the heading it names; `unresolved` when the document is named and the heading is
not there — the only failing state; and `unattributed` when the line names no document at all,
which is printed and never gated. The third state is the load-bearing one and the reason this
module refuses to guess: the obvious rule, *take the nearest preceding document number*, was
measured on this corpus and is wrong **in both directions**. It reads `0007`'s own
*"lost between `0006` §2.3 ... and §4.11"* as a citation of `0006`, and it would claim six
`§4.x` outside `docs/` for `0008` that belong to `0007`. Wrong attributions resolve **green**,
which is worse than no guard at all.

**Why `git ls-files` rather than a walk, and why not `git grep`.** A filesystem walk sees
gitignored content no clone has — `ADR-0009` §1 records a count of this same graph reading 81
across 22 files because ten of them were in `.claude/sessions/`. And `git grep` prints
`path:line:content`, which is exactly what the first measurement of these buckets classified
by mistake, reading `0008` in the path `docs/adr/0008_...md` as a citation of that document.
Reading the files here means **the path never enters the string being classified**: the erratum
is made impossible rather than avoided.

**Heading indexes are bounded by depth, and that is not tidiness.** `0008` carries 22 `####`
headings whose text begins with a digit — `#### 1. Two submodule tests do assert a separator`
and its siblings are ordered-list items inside §4.13, §4.14 and §4.17, not sections. An
unbounded reader admits sections 7 through 11 from them, so a reference to section 11 of the
ledger would resolve green against a list item. `tools/spec.py`'s `NORMATIVE_FROM`/`NORMATIVE_TO` bound exists against the same
shape one document over.

**Prose about a broken citation may not write one.** This module and its tests are in the
corpus, so an example written literally — a docstring naming a document and a section number
that is not in it — is read as that very citation and reported. Both files were rewritten to name such
sections in words for that reason. It is not a defect to fix: excluding the resolver's own
source would be the resolver declining to read the one file guaranteed to talk about citations.

*Found by the commit that added this module, and it is `0010` §3.6's observation 6 arriving
from the other side. `git ls-files` excludes untracked files, so while these two files were
unstaged the resolver could not see itself and the suite was green; `git add` put them in the
corpus and three of its own sentences turned up as findings. The bound the plan for this step
called untestable is real, and it bit in the direction nobody costed.*

`python -m tools.citations` prints and exits 0, like `tools.spec`. Its guards, in
`tests/test_citations.py`, are what fail.
"""

from __future__ import annotations

import functools
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: The document this resolver is built for. Others are resolved too — every numbered document
#: under `docs/` — but `0008` is the one `ADR-0009` §1 measures and the one the later steps of
#: that decision move around.
LEDGER = ROOT / "docs" / "audit" / "0008_the-rollout-ledger.md"

TIMEOUT = 30

#: `## 4. L3 — the recommendation` and `### 4.11 The two clauses ...`, and nothing deeper.
#: The depth bound is the whole point — see the module docstring.
_TOP = re.compile(r"^##[ \t]+(\d+)\.[ \t]")
_SUB = re.compile(r"^###[ \t]+(\d+\.\d+)[ \t]")

#: A document token, in the four shapes this repository writes. The directory group is the
#: load-bearing one: **every cross-reference to an ADR is a markdown link**, so the token
#: adjacent to the `§` is the link *target* — a bare filename — and not the `ADR-NNNN` label
#: the reader sees. Keying that on the number alone answered about the audit document while
#: the label beside it said `ADR-0004`, on six lines, all resolving green against the wrong
#: document's §5. Found by the review of this module's first commit, which is the defect its
#: own docstring claims to be about.
_TOKEN = re.compile(r"(?P<dir>(?:\.\./)*(?:docs/)?(?P<kind>adr|audit)/)?"
                    r"(?P<adr>ADR[- ])?"
                    r"(?P<num>\d{4})"
                    r"(?P<file>_[A-Za-z0-9_.\-]+?\.md)?")

#: A reference: `§4.11`, `§4`, `§5.0`. Section numbers only — `§5 clause 1` is a reference to
#: §5 and the clause part is prose.
_REF = re.compile(r"§(?P<ref>\d+(?:\.\d+)?)")

#: What may sit between a document token and the `§` it owns: a closing backtick, bracket or
#: paren, and whitespace. Nothing else — adjacency is the rule.
_GAP = re.compile(r"^[`\]\)\s]*$")

#: There is deliberately no list-continuation rule, and it was written and then removed.
#: `` `0008` §3.7, §3.9 and §4.9 `` reads as one document's sections, so inheriting the owner
#: across `,` and ` and ` looks free — and `0008`:120's *"lost between `0006` §2.3 and §4.11"*
#: is **the identical shape meaning two documents**, with `§4.11` belonging to `0008`. The two
#: cannot be told apart by syntax, so the rule produced a wrong `unresolved` here and would
#: produce a wrong `resolved` elsewhere. Six sites lose their owner and become backlog, which
#: is this module's whole position: a citation nobody attributed is a citation nobody
#: attributed. Found by running the resolver, on its first pass, against its own design.

#: Extensions this resolver reads. The corpus is every tracked file; these are the ones whose
#: bytes are text an author writes a citation into.
_TEXT = frozenset({".py", ".md", ".yml", ".yaml", ".toml", ".css", ".html", ".json", ".cfg",
                   ".ini", ".txt", ".sh", ".gitignore", ".gitmodules"})


@dataclass(frozen=True)
class Citation:
    """One `§N` or `§N.M`, where it is written, and which document it names."""

    path: str
    line: int
    ref: str
    #: The document's stem as written — `0008`, `ADR-0008` — or `None` when the line names
    #: none and this module refuses to guess.
    owner: str | None


@dataclass(frozen=True)
class Run:
    out: str
    code: int
    #: Kept because the only caller puts it in a failure message. `tools/entry_state.py`'s
    #: `_run` holds it for the same reason, and dropping it here printed `git ls-files
    #: failed:` with nothing after the colon.
    err: str = ""


def _git(*args: str) -> Run:
    """`tools/entry_state.py`'s `_run`, minus the parts only the entry state needs."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        done = subprocess.run(("git", *args), cwd=ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=TIMEOUT, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        return Run("", 1, f"{type(exc).__name__}: {exc}")
    return Run(done.stdout, done.returncode, done.stderr)


def headings(path: Path) -> frozenset[str]:
    """Every section number `path` declares, bounded to `##` and `###`.

    A document with no numbered subsection is ordinary — six of the ADRs have none — so this
    is permissive. The loud failure belongs to the one document this resolver is built for and
    lives in `ledger_headings()`.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AssertionError(f"{path.name}: cannot be read ({exc})") from exc
    lines = text.splitlines()
    top = {match.group(1) for match in (_TOP.match(line) for line in lines) if match}
    subs = {match.group(1) for match in (_SUB.match(line) for line in lines) if match}
    return frozenset(top | subs)


def ledger_headings() -> frozenset[str]:
    """`0008`'s sections, and the one place this module fails loudly.

    Raises naming the document when it parses no `### N.M` at all. A renamed or moved `0008`
    would otherwise arrive as every citation of it going unresolved at once — the wrong
    diagnosis printed a hundred-odd times. `tools/spec.py`'s `normative_text()` fails the same
    way for the same reason, and `tests/test_spec.py` proves that one red.
    """
    found = headings(LEDGER)
    if not any("." in ref for ref in found):
        raise AssertionError(
            f"{LEDGER.name}: no `### N.M` subsection heading parsed — the file has moved, been "
            f"renamed, or changed its heading form")
    return found


def _documents() -> dict[str, tuple[Path, ...]]:
    """Every numbered document tracked under `docs/`, keyed as it is cited.

    **From the index, not from a walk**, for the reason the module docstring gives for the
    corpus: an untracked local draft under `docs/` would otherwise contribute headings no
    clone has, turning an `unresolved` into a `resolved` on one machine only.

    **A key may hold more than one file, and that is measured rather than assumed.** `0010` is
    three — the portfolio audit and its two prompts — and keeping only the last one read hid
    the other two behind alphabetical order. The prompts declare no numbered section, so the
    union is exact today; `ledger_headings()`-style loudness for the case where two files
    under one key both declare sections lives in `tests/test_citations.py`.
    """
    out: dict[str, list[Path]] = {}
    for name in corpus():
        if not name.startswith("docs/") or not name.endswith(".md"):
            continue
        path = ROOT / name
        if path.parent.name not in {"adr", "audit"}:
            continue
        stem = path.name.split("_")[0].split("-")[0]
        if not stem.isdigit():
            continue
        out.setdefault(stem if path.parent.name == "audit" else f"ADR-{stem}", []).append(path)
    return {key: tuple(sorted(paths)) for key, paths in out.items()}


def _owner_at(line: str, start: int, citing: str = "docs/audit/x.md") -> str | None:
    """The document token immediately before `start`, keyed as the index keys documents.

    `citing` is the path of the file the line is in, and it is not decoration: a link target
    written without a directory — `](0004_what-carries-the-page-spec.md)` — means the ADR when
    the link sits in an ADR and the audit document when it sits in an audit document. Reading
    the number alone is how six lines resolved green against the wrong document's §5 while the
    link label beside them read `ADR-0004`.
    """
    before = line[:start]
    for match in reversed(list(_TOKEN.finditer(before))):
        if not _GAP.match(before[match.end():]):
            # A token that is not adjacent does not own this reference, and no earlier token
            # can be adjacent either — the gap only grows.
            break
        number = match.group("num")
        if match.group("dir"):
            return f"ADR-{number}" if match.group("kind") == "adr" else number
        if match.group("adr"):
            return f"ADR-{number}"
        if match.group("file"):
            return f"ADR-{number}" if "/adr/" in citing.replace("\\", "/") else number
        # A bare number. `CLAUDE.md`: *a bare number in this repository means the audit
        # document*, and `ADR-0009` §0 is the third collision that rule has to survive.
        return number
    return None


def _line_citations(path: str, number: int, line: str) -> list[Citation]:
    out: list[Citation] = []
    for match in _REF.finditer(line):
        out.append(Citation(path, number, match.group("ref"),
                            _owner_at(line, match.start(), path)))
    return out


def corpus() -> tuple[str, ...]:
    """Every tracked text file, from `git ls-files`, gitlinks excluded.

    `-z` because `core.quotepath` escapes non-ASCII paths; the twelve submodules appear here
    as mode `160000` entries, which are directories and not files.
    """
    run = _git("ls-files", "-z")
    if run.code != 0:
        raise AssertionError(f"git ls-files failed: {(run.err or run.out).strip()}")
    names = [name for name in run.out.split("\0") if name]
    out = []
    for name in names:
        path = ROOT / name
        if not path.is_file():
            continue
        if path.suffix in _TEXT or path.name in _TEXT or path.name.startswith("."):
            out.append(name)
    return tuple(out)


#: Files the sweep could not read. A list rather than a silent `continue`: `citations()` is
#: the only reader here that swallowed its error, while `headings()` and `corpus()` both
#: raise, and a dozen files dropping out sits far under any floor a guard can set. Reported.
UNREADABLE: list[str] = []


def citations() -> tuple[Citation, ...]:
    out: list[Citation] = []
    UNREADABLE.clear()
    for name in corpus():
        try:
            text = (ROOT / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            UNREADABLE.append(f"{name}: {type(exc).__name__}")
            continue
        if "§" not in text:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if "§" in line:
                out.extend(_line_citations(name, number, line))
    return tuple(out)


def unresolved(found: tuple[Citation, ...] | None = None) -> tuple[Citation, ...]:
    """Attributed citations whose named document does not hold the section. The failing set."""
    index = _index()

    return tuple(c for c in (found if found is not None else citations())
                 if c.owner in index and c.ref not in index[c.owner])


@functools.lru_cache(maxsize=1)
def _index() -> dict[str, frozenset[str]]:
    """Section numbers per document key, with `0008` read through its loud reader.

    Cached because `report()` asks for it once per unattributed citation — a thousand-odd
    times — and each miss re-reads nineteen documents. Uncached, the report took 36 seconds
    to print twelve lines.
    """
    out = {key: frozenset().union(*(headings(path) for path in paths))
           for key, paths in _documents().items()}
    out["0008"] = ledger_headings()
    return out


def unattributed(found: tuple[Citation, ...] | None = None) -> tuple[Citation, ...]:
    """Citations naming no document. Printed, never gated — the module docstring is why."""
    return tuple(c for c in (found if found is not None else citations()) if c.owner is None)


def unknown_document(found: tuple[Citation, ...] | None = None) -> tuple[Citation, ...]:
    """Citations naming a document this index does not carry. The fourth state, and it exists
    because the first three let this one through **as `resolved`**.

    `unresolved()` filters on `owner in index`, and the report computed `resolved` by
    subtracting the other buckets from the total — so a citation whose owner is not in the
    index was in none of the named buckets and silently joined the green column. One is
    legitimate and out of scope: `0007`:528 cites `ADR-0012`, a sibling repository's decision
    document. **Every mistyped document number is in this class too** — `0018`, `ADR-0010` —
    which is the likeliest way a citation breaks at all. Printed, not gated: a legitimate
    cross-repository citation must not redden `core`.
    """
    index = _index()
    return tuple(c for c in (found if found is not None else citations())
                 if c.owner is not None and c.owner not in index)


#: Where a citation of the ledger is a pointer from working code into narrative, rather than
#: one document referring to another. `ADR-0009` §3 step 4 migrates these onto the ids in
#: `docs/reference/failure-classes.md` as each file is touched for another reason.
_CODE_SIDE = ("tools/", "tests/", ".github/")


def code_side(found: tuple[Citation, ...] | None = None) -> tuple[Citation, ...]:
    """Citations of `0008` written in code, tests or CI. The population step 4 drives down.

    **Printed, never gated, and deliberately not a ratchet.** A pinned ceiling was considered
    and refused: not every citation of the ledger from code is wrong — `tools/spec.py` cites a
    frozen measurement, `__main__.py` cites the stage a `GATE` row closed — so a rule refusing
    new ones would be a rule this corpus refutes. What step 4 needs is a number that moves, and
    a reader who can see it move; that is this, and `0009` §7 row 9 reads it rather than
    promising a signal nothing emits.
    """
    return tuple(c for c in (found if found is not None else citations())
                 if c.owner == "0008"
                 and (c.path.startswith(_CODE_SIDE) or c.path == "CLAUDE.md"))


def candidates(citation: Citation) -> tuple[str, ...]:
    """Which documents could hold an unattributed reference. The triage, not the answer."""
    return tuple(sorted(key for key, refs in _index().items() if citation.ref in refs))


def report() -> list[str]:
    found = citations()
    index = _index()
    bad = unresolved(found)
    loose = unattributed(found)
    foreign = unknown_document(found)
    resolved = tuple(c for c in found
                     if c.owner in index and c.ref in index[c.owner])
    assert len(resolved) + len(bad) + len(loose) + len(foreign) == len(found), (
        "the four buckets no longer partition the sweep — the arithmetic below is the exact "
        "shape that let an unknown document count as resolved")

    lines = [f"citations — {len(found)} section reference(s) in {len(corpus())} tracked "
             f"file(s), against {len(index)} numbered document(s)", ""]
    lines.append(f"  unresolved   {len(bad)} — a document is named and the section is not there")
    for citation in bad:
        lines.append(f"      {citation.path}:{citation.line}  {citation.owner} §{citation.ref}")
    lines.append("")

    ledger = sum(1 for c in resolved if c.owner == "0008")
    lines.append(f"  resolved     {len(resolved)}, of which {ledger} name `0008`")
    lines.append(f"  foreign      {len(foreign)} — names a document this index does not carry; "
                 f"printed, never gated")
    for citation in foreign:
        lines.append(f"      {citation.path}:{citation.line}  {citation.owner} §{citation.ref}")
    lines.append(f"  unattributed {len(loose)} — no document named on the line; never gated, "
                 f"because guessing resolves green in both directions")

    self_cited = one = none = many = 0
    orphans = []
    for citation in loose:
        stem = Path(citation.path).name.split("_")[0].split("-")[0]
        key = stem if "/audit/" in citation.path else f"ADR-{stem}"
        options = candidates(citation)
        if key in options:
            self_cited += 1
        elif len(options) == 1:
            one += 1
        elif not options:
            none += 1
            orphans.append(citation)
        else:
            many += 1
    lines.append(f"      {self_cited} the file's own section · {one} exactly one candidate · "
                 f"{many} ambiguous · {none} no candidate anywhere")
    if orphans:
        lines.append("      the last group is a finding: the section exists in no document")
        for citation in orphans:
            lines.append(f"          {citation.path}:{citation.line}  §{citation.ref}")
    code = code_side(found)
    files = sorted({c.path for c in code})
    lines.append("")
    lines.append(f"  code-side    {len(code)} citation(s) of `0008` in {len(files)} file(s) of "
                 f"code, tests or CI")
    lines.append("      the population `ADR-0009` §3 step 4 migrates onto the ids in")
    lines.append("      docs/reference/failure-classes.md, as each file is touched for another")
    lines.append("      reason. Printed and never gated: citing the ledger from code is not")
    lines.append("      always wrong, so a rule refusing it would be one the corpus refutes")

    if UNREADABLE:
        lines.append("")
        lines.append(f"  unreadable   {len(UNREADABLE)} file(s) the sweep could not open")
        for name in UNREADABLE:
            lines.append(f"      {name}")
    return lines


def main() -> int:
    for line in report():
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
