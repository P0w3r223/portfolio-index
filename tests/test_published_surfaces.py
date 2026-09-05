"""The sweep over the real working trees — deliberately assertion-poor.

Everything else in this suite runs against frozen input. This file is the one place the
checker meets the twelve pages as they are today, and that is exactly why it asserts almost
nothing about what it finds: **a test bound to the live content of a sibling repository goes
red when that repository legitimately changes**, and a check that cries wolf is a check that
gets silenced. The rollout of `0008` S3–S8 will change every one of these pages on purpose.

So the properties here are the ones a page rewrite cannot invalidate — the checker completes,
reports every clause exactly once, emits no status the report cannot print, and never answers
a CSS question from an incomplete stylesheet. The *values* live in the checker's own output,
which is the point of `ADR-0004` §5: the table is computed, not typed.

Every test skips when its submodule is not checked out, so the suite is green in a fresh
clone with no `git submodule update`.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROOT, require_submodule
from tools.pagespec import __main__ as report
from tools.pagespec import clauses, render, sources

COMMITTED = [surface for surface in sources.SURFACES if not surface.must_fetch]
#: Reported for every surface whatever it holds. `1 dark` is deliberately not among them:
#: a page declaring no custom properties gets one finding naming the cause instead of a
#: second one restating it, which is `0007` §5 clause 1's *"the same fact twice"*.
CLAUSES = ("1 tokens", "1 usage refs", "1 usage roles", "1 literals",
           "2 tiles", "3 tables", "4 h1", "4 title",
           "5 card meta", "6 back-link", "7 webfont", "8 separator")

pytestmark = pytest.mark.submodules


def _load(surface: sources.Surface) -> sources.Loaded:
    require_submodule(surface.repo, surface.path)
    loaded = sources.load(surface, ROOT, allow_fetch=False)
    assert loaded is not None, f"{surface.name} is on disk but did not load"
    return loaded


@pytest.mark.parametrize("surface", COMMITTED, ids=lambda one: one.name)
def test_every_clause_reaches_a_verdict_on_every_published_surface(surface):
    """Completing is the assertion. A clause that raises on one page's markup would take the
    whole table down, and a clause that quietly drops out leaves a column nobody misses."""
    findings = clauses.check(_load(surface))
    reported = [finding.clause for finding in findings]
    for clause in CLAUSES:
        assert reported.count(clause) == 1, f"{clause} reported {reported.count(clause)}×"
    assert all(finding.detail for finding in findings), "a finding carries no detail"


@pytest.mark.parametrize("surface", COMMITTED, ids=lambda one: one.name)
def test_the_dark_column_is_reported_exactly_when_there_are_tokens_to_darken(surface):
    """The conditional column, stated as the condition rather than as a per-page expectation.

    Three pages hold the design system as hand-typed literals; a `1 dark` finding on those
    would be a second sentence about a page that has no `:root` at all.
    """
    findings = clauses.check(_load(surface))
    declared = "no custom properties declared at all" not in \
        next(one.detail for one in findings if one.clause == "1 tokens")
    assert any(one.clause == "1 dark" for one in findings) is declared


@pytest.mark.parametrize("surface", COMMITTED, ids=lambda one: one.name)
def test_no_surface_produces_a_status_the_report_cannot_print(surface):
    statuses = {finding.status for finding in clauses.check(_load(surface))}
    assert statuses <= set(report._MARK)


@pytest.mark.parametrize("surface", COMMITTED, ids=lambda one: one.name)
def test_no_css_question_is_answered_from_an_incomplete_stylesheet(surface):
    """`0007` §2's first failure: every same-origin sheet the page links is either read or
    declared unread, and never simply absent from both lists.

    Stated as a property of the page's own `<link>`s, so it holds whatever the pages become —
    including after S7 renames every wrapper class in the portfolio.
    """
    loaded = _load(surface)
    linked = render.parse(loaded.html).stylesheet_hrefs()
    accounted = set(loaded.stylesheets) | {entry.split(" (")[0] for entry in loaded.unreadable}
    assert set(linked) <= accounted, (
        f"{surface.name} links a stylesheet that was neither read nor reported"
    )


@pytest.mark.parametrize("surface", COMMITTED, ids=lambda one: one.name)
def test_a_clause_that_cannot_trust_the_ancestry_says_so_instead_of_passing(surface):
    """The two are tied: unclosed markup must produce `undecided` on clause 3, never `pass`.

    Asserted as an implication rather than as `unclosed == 0`, because whether a page's markup
    balances is the page's business and this file does not review the pages.
    """
    loaded = _load(surface)
    page = render.parse(loaded.html)
    finding = clauses.clause_3_tables(page, loaded.css)
    if page.unclosed:
        assert finding.status == clauses.UNDECIDED
    else:
        assert finding.status != clauses.UNDECIDED


def test_the_report_runs_over_the_whole_index_and_still_exits_zero(capsys):
    """The end-to-end path, at the size it actually runs: twelve surfaces, no network."""
    require_submodule("ab-lab")
    assert report.main(["--root", str(ROOT), "--detail"]) == 0
    out = capsys.readouterr().out
    assert "wroclaw-air-insights (needs --fetch)" in out


def test_the_computed_table_does_not_depend_on_set_iteration_order():
    """Classes, scrolling wrappers and ancestries are all sets, and several of them reach the
    printed detail. Two runs under different hash seeds must produce the same table, or the
    output that replaces `0007` §3 would differ between the person writing it down and the
    person checking it.
    """
    require_submodule("ab-lab")

    def run(seed: str) -> str:
        environment = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
        finished = subprocess.run(
            [sys.executable, "-m", "tools.pagespec", "--detail"],
            cwd=ROOT, env=environment, capture_output=True, text=True,
            encoding="utf-8", check=True,
        )
        return finished.stdout

    assert run("0") == run("12345")
