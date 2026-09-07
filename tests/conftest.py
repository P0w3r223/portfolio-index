"""Shared scaffolding for the page-spec checker's tests.

Two kinds of input, and the difference between them is the design of this suite.

**Synthetic pages**, built inline by `page()` and `loaded()`, carry the mechanism tests. Each
is the smallest markup or stylesheet that makes one defect visible, so a test that passes
proves the fix is present rather than proving the portfolio happens to be in a good mood.

**Fixtures of record**, under `fixtures/`, are reductions of the real pages that demonstrated
the defect, frozen with their provenance in `fixtures/README.md`. They are committed rather
than read out of the sibling working trees, because a test bound to the live content of
another repository goes red when that repository legitimately changes — and a check that
cries wolf is a check that gets deleted. The live trees are swept in
`test_published_surfaces.py`, which asserts only what a page rewrite cannot invalidate.

Nothing here touches the network. `sources._fetch` is the single seam, and
`test_sources.py` stubs it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.pagespec import render, sources

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"

#: Emitted by `clauses.check` and not a clause: the checker reporting on its own inputs. It is
#: `UNDECIDED` by construction and can never be `FAIL`, and the gate refuses on it through
#: `_unread_same_origin` — a separate reason with its own header — so requiring it in `GATED`
#: would demand a prefix that gates nothing and says the wrong thing about why.
NOT_A_CLAUSE = frozenset({"stylesheets"})


def fixture(name: str) -> str:
    """One fixture of record, read as text. See `fixtures/README.md` for provenance."""
    return (FIXTURES / name).read_text(encoding="utf-8")


def page(html: str) -> render.Page:
    return render.parse(html)


def loaded(html: str = "", css: str = "", *, name: str = "surface", repo: str = "surface",
           unreadable: list[tuple[str, str]] | None = None) -> sources.Loaded:
    """A `Loaded` assembled by hand, so the clauses can be exercised without any I/O.

    `repo` defaults to `name` because clause 4 compares the `<title>` against the project's
    identity — the directory string *and* the prose spelling of it, since the reading was
    settled on 2026-09-07 — and a test that wants that comparison to bite has to set it.
    """
    surface = sources.Surface(name, repo, "docs/index.html")
    return sources.Loaded(surface, html, css, unreadable=list(unreadable or []))


def status_of(findings, clause: str) -> str:
    """The status recorded for one clause, or a readable failure naming what was found."""
    for finding in findings:
        if finding.clause == clause:
            return finding.status
    raise AssertionError(
        f"no finding for clause {clause!r}; the check reported "
        f"{[found.clause for found in findings]}"
    )


def detail_of(findings, clause: str) -> str:
    for finding in findings:
        if finding.clause == clause:
            return finding.detail
    raise AssertionError(f"no finding for clause {clause!r}")


@pytest.fixture(scope="session")
def index_root() -> Path:
    """The index repository's working tree — the `--root` the checker is pointed at."""
    return ROOT


def require_submodule(repo: str, relative: str = "docs/index.html") -> Path:
    """The path to a sibling's published page, skipping the test when it is not checked out.

    The twelve submodules are populated in a working session and empty in a fresh clone, so
    every test that reads one has to be able to sit down quietly. Failing here would make CI
    red for a reason that has nothing to do with the checker.
    """
    path = ROOT / repo / relative
    if not path.is_file():
        pytest.skip(f"{repo} is not checked out; run `git submodule update --init {repo}`")
    return path
