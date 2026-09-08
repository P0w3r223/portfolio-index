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

from conftest import NOT_A_CLAUSE, ROOT, require_submodule
from tools.pagespec import __main__ as report
from tools.pagespec import clauses, render, sources

COMMITTED = [surface for surface in sources.SURFACES if not surface.must_fetch]
#: Reported for every surface whatever it holds. `1 dark` is deliberately not among them:
#: a page declaring no custom properties gets one finding naming the cause instead of a
#: second one restating it, which is `0007` §5 clause 1's *"the same fact twice"*.
#:
#: `4 eyebrow` was missing from this tuple until the clause registry tied the four lists of
#: this vocabulary together. It is emitted on every surface by `clause_4_opening` and it is in
#: `GATED`, so a change that stopped emitting it would have taken a gated half of clause 4 out
#: of the gate with every test still green — `0009` N1's shape, in the file that guards it.
CLAUSES = ("1 tokens", "1 usage refs", "1 usage roles", "1 literals",
           "2 tiles", "3 tables", "4 eyebrow", "4 h1", "4 title",
           "5 card meta", "6 back-link", "7 webfont", "8 separator")


pytestmark = pytest.mark.submodules


def _sweep(allow_fetch: bool = False) -> tuple[int, dict[str, set[str]]]:
    """One pass over the published surfaces: how many were read, and each key's statuses.

    Shared by the ratchet's two halves on purpose. They make opposite claims about `GATED`
    against the same corpus, and a corpus assembled twice is a corpus that can diverge once —
    `0008` §4.12 is the record of a fix applied to one of two tests that shared a defect and
    not to the other, five lines away. The `require_submodule` loop lives here for the same
    reason: neither half can now run against a partial checkout while the other does not.

    **The mode is a parameter since `0009` §7 row 13b**, and that is the whole of the
    eleven/twelve asymmetry as it reaches this file. Fetchless, this reads the eleven
    surfaces that commit a page. Fetching, it reads all twelve — the same corpus the gate
    covers — and the expected count follows the mode rather than being fixed at eleven.

    **An incomplete fetching corpus skips rather than fails, and the list of ways it can be
    incomplete is longer than "the twelfth was unreachable".** Each one makes the floor's
    claim false in the direction that matters, because each one turns a clause that was never
    answered into a clause reporting no failure:

    - the twelfth did not answer, so `load` returns `None` and the count is eleven;
    - a committed surface's fetch failed and the verdict silently came from its file, so
      *"clean on the twelve published surfaces"* is a claim about a file nobody served;
    - a same-origin **stylesheet** the wire did not deliver, which
      `_undecided_where_the_stylesheet_is_incomplete` turns from `FAIL` into `UNDECIDED` on
      every clause-1 and clause-3 key — so a genuinely failing clause reads clean and the
      floor would *demand* its admission on a sheet the run never read.

    A skip is right and a failure is not: none of the four is a statement about a page, and a
    guard that reddens on a DNS blip is the cries-wolf check `conftest.py` opens by warning
    about. The gate itself is unaffected — `python -m tools.pagespec --fetch` still refuses on
    a 404 and on an unread same-origin sheet, under its own headers.
    """
    for surface in COMMITTED:
        require_submodule(surface.repo, surface.path)
    errors: dict[str, str] = {}
    read = 0
    statuses: dict[str, set[str]] = {}
    for surface in sources.SURFACES:
        loaded = sources.load(surface, ROOT, allow_fetch=allow_fetch, errors=errors)
        if loaded is None:
            continue
        if allow_fetch and loaded.served is None:
            # `load` already recorded the exception under this surface's name, so the cause is
            # in `errors`. The *consequence* is what makes the corpus unusable and it is not
            # derivable from the cause by a reader at 07:00: the verdict below came from a
            # file, under a job named for the bytes the public receives.
            errors[surface.name] = (errors.get(surface.name, "the wire was not read")
                                    + "; the verdict came from the committed file")
        if loaded.unreachable:
            errors.setdefault(surface.name, "a same-origin stylesheet the wire did not "
                                            "deliver: " + sources.describe(loaded.unreachable[0]))
        read += 1
        for finding in clauses.check(loaded):
            statuses.setdefault(finding.clause, set()).add(finding.status)
    if errors:
        pytest.skip("the corpus is incomplete, so neither half of the ratchet can claim "
                    "anything about it: "
                    + "; ".join(f"{name} — {why}" for name, why in sorted(errors.items())))
    return read, statuses


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
    accounted = set(loaded.stylesheets) | {href for href, _why in loaded.unreadable}
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


def test_the_report_runs_over_the_whole_index_and_the_gate_is_green(capsys):
    """The end-to-end path, at the size it actually runs: twelve surfaces, no network.

    Named for the exit code until `0008` S-gate, when the zero stopped meaning *"this checker
    does not decide"* and started meaning *"nothing in `GATED` failed"*. Same assertion, and
    a different claim — which is worth the rename, because the old name would now read as a
    guarantee that the checker never refuses.

    **Every committed surface is required, not just one**, and the gate is why. This ran
    behind a single `require_submodule("ab-lab")` for one commit — the same guard the
    ratchet test below had already been corrected for, five lines away, in the commit that
    named the correction. Before the gate a missing sibling was a `not read:` line and this
    test passed; since S-gate an unread committed surface *gates*, so on any checkout that
    is partial rather than empty `main` returns 1 and this file's own docstring — *"every
    test skips when its submodule is not checked out"* — is false. Reproduced on a root
    holding only `ab-lab/docs`: exit 1, `gate — a surface that should have been readable was
    not read`, and nothing in the message about submodules. *A fix applied to one of two
    tests that share a defect is the displacement this branch is named for.*
    """
    for surface in COMMITTED:
        require_submodule(surface.repo, surface.path)
    assert report.main(["--root", str(ROOT), "--detail"]) == 0
    out = capsys.readouterr().out
    assert "wroclaw-air-insights (needs --fetch)" in out


def _expected(allow_fetch: bool) -> int:
    """How many surfaces the sweep must read, **derived from the mode rather than pinned**.

    `0009` §7 row 13b's own sentence: *make the expected surface count follow that mode*. Both
    directions are guarded, because a constant here is green in one mode and vacuous in the
    other, and n−1 of n on a two-way branch is the shape this suite has paid for repeatedly —
    `test_report.py`'s `startswith("pagespec")` repair is the same lesson one file away.
    """
    return len(sources.SURFACES) if allow_fetch else len(COMMITTED)


def test_the_ratchet_holds_no_clause_the_committed_surfaces_report_failing(fetching):
    """The ratchet cannot be widened past the measurement that licenses it.

    `GATED` is a claim about the trees: those keys report zero `FAIL` on every surface read.
    This asserts the claim rather than trusting the tuple, so adding `8 separator` before S9
    has landed turns it red — which is exactly when it should.

    It lives here and not beside the gate's own tests because it needs the real working
    trees, and `test_report.py` is the `core` job's file: that job runs with no submodule on
    disk and is the one that must never be allowed to go red.

    **Vacuity is guarded on what was read, not on what failed** — and getting there took two
    goes. `assert failing` fails rather than skips in a fresh clone, and would fail *again*
    once S9 and S10 close, because then nothing fails and `failing` is empty: **a guard that
    reddens on the success of the work it guards.** But `assert read` with a single
    `require_submodule("ab-lab")` above it was no better — that call checks the very path
    `sources.load` checks, so the assertion could not fire, and `read == 1` passed happily
    while proving the ratchet against **one** surface of eleven. §3.10's sentence is the
    whole point: *a corpus sweep proves the rule against the corpus*, so the corpus has to be
    all of it or the test has to skip.
    """
    read, statuses = _sweep(fetching)
    assert read == _expected(fetching), (
        f"the sweep read {read} of {_expected(fetching)} surfaces")

    failing = {clause for clause, seen in statuses.items() if clauses.FAIL in seen}
    for clause in sorted(failing):
        assert not any(clause.startswith(prefix) for prefix in report.GATED), (
            f"{clause} fails on a published surface and is in GATED. **Three causes, and the "
            "third arrived with the registry**: a page regressed; the ratchet was widened "
            "before its stage closed; or a row that used to be `pending` or `report-only` was "
            "promoted to `gated` without the measurement that licenses it. `ADR-0005` §4 named "
            "the third when it refused to derive this tuple, and `ADR-0006` derived it anyway "
            "— so the cause is real and this message is where it is named.")


def test_the_ratchet_cannot_be_narrowed_either_every_clean_clause_is_gated(fetching):
    """The other direction, which nothing guarded until now.

    Its twin above asserts *gated implies no failure*. That is one-way: removing a prefix from
    `GATED` cannot violate it, because fewer gated keys is trivially still zero failures. So the
    suite's entire protection of the ratchet's **content** was *"`GATED` must be non-empty"* —
    measured, dropping any single one of the eight prefixes left all 311 tests green, and
    `GATED = ("1 ",)`, which un-gates seven clauses at once, was green too.

    **This matters now rather than in the abstract.** `0008` S9 and S10 both edit that tuple. An
    edit adding `"8 "` while dropping `"5 "` would ship green and clause 5 would silently stop
    gating twelve surfaces — the displacement shape §3.9, §3.10, §4.9 and §4.12 each record.

    With both halves the tuple is no longer a claim checked in one direction: **`GATED` is
    exactly the set of finding keys that report no failure on the corpus**, derived from the
    sweep rather than typed. A stage closing moves a key from failing to clean, and this test is
    then what *requires* the widening its twin permits.

    **One exemption, and the first version of this test claimed there were none.** That claim —
    *"the gate's other two reasons are not clause findings at all, so they never reach this
    set"* — is false: `clauses.check` emits a `stylesheets` finding whenever a sheet could not
    be read (`clauses.py`, the `loaded.unreadable` branch). It is `UNDECIDED` by construction,
    can never be `FAIL`, and the gate already refuses on it through `_unread_same_origin`, which
    is a different reason with its own header. So it is clean-and-ungated the moment any page
    has an unreadable sheet — and no committed surface has one today, which is exactly why the
    claim survived being written. Reproduced against a hand-built `Loaded` rather than waited
    for.

    The exemption is one name and a reason. That is the difference between an exemption and a
    place for a key to hide.

    *This paragraph used to continue: **and it is also the route for a clause that ships
    report-only**, naming `0009` §7 row 12's contrast clause and telling a stage editor to add
    its key to `NOT_A_CLAUSE` with a reason. **That instruction was refused by the check five
    lines below it**, which admits no key the corpus reports `PASS` or `FAIL` — and a contrast
    clause passes on a conforming page, which is the point of it. The documented route for
    report-only was closed by the guard beside it, and the two shipped in one commit. The
    route is `Ratchet(prefix, REPORT_ONLY_STATE, reason)` in `__main__.GATE`, which is the
    third state `0009` §7 row 8 said the taxonomy needed and row 13b is what built.*

    *The alternative — deriving `clean` from keys observed `PASS` at least once — was measured
    and rejected. `1 composited` and `4 h1` are `UNDECIDED` on every surface and never `PASS`,
    so both would drop out of the demanded set and their removal from `GATED` would go
    unnoticed; `4 h1` is failable by construction (a missing `<h1>`, or one equal to the
    repository's name), so that is a real hole in the direction this guard exists to close.*

    **Scope follows the mode, and that is `0009` §7 row 13b.** Fetchless — every push and
    every pull request — this reads the eleven committed surfaces and accepts a clean key
    under *any* row of `GATE`, `pending` included. Fetching, in the scheduled `live` job, it
    reads all twelve and `pending` stops being an answer: a key clean on the twelfth must be
    promoted.

    *Until row 13b this sweep was fixed at eleven while the gate covered twelve, and the
    consequence was a deadlock with no green state: the committed pages could go clean on a
    clause while the fetch-only one still failed, this guard would then* demand *the widening,
    the `surfaces` job could not see the twelfth, and the morning's `live` run went red on a
    merge that was green. S9 and S10 navigated it by hand, watching `refresh.yml` rebuild
    before the tuple moved. `pending` is that procedure, run rather than read.*
    """
    read, statuses = _sweep(fetching)
    assert read == _expected(fetching), (
        f"the sweep read {read} of {_expected(fetching)} surfaces")

    # The exemption set earns its keys rather than holding them. An entry that the corpus ever
    # reports `PASS` or `FAIL` is a clause that can gate, and exempting one would un-gate it in
    # silence — measured: adding `5 card meta` and `6 back-link` left all 390 tests green.
    for exempt in sorted(NOT_A_CLAUSE):
        assert not statuses.get(exempt, set()) & {clauses.PASS, clauses.FAIL}, (
            f"{exempt} is exempted from the floor but the corpus reports it "
            f"{sorted(statuses[exempt])}: only a key that cannot gate belongs in NOT_A_CLAUSE")

    assert {clause for clause, seen in statuses.items() if clauses.FAIL not in seen}, \
        "no clause is clean on the corpus, which cannot be true while the gate is green"

    assert not report.clean_but_unexplained(statuses, exempt=NOT_A_CLAUSE), (
        f"{report.clean_but_unexplained(statuses, exempt=NOT_A_CLAUSE)} report no failure on "
        "any published surface and no row of GATE covers them: the ratchet was narrowed, so a "
        "clause that passes everywhere has stopped gating. Four answers, and each is one "
        "row:\n"
        "  - clean on all twelve -> Ratchet(prefix, GATED_STATE); that is the ratchet "
        "working.\n"
        "  - clean on these eleven, the twelfth unconfirmed -> Ratchet(prefix, PENDING_STATE, "
        "reason). Confirm with `python -m tools.pagespec --fetch` locally or a `live` "
        "dispatch; the fetching half of this guard then demands the promotion.\n"
        "  - it prints and is deliberately never to gate -> Ratchet(prefix, "
        "REPORT_ONLY_STATE, reason), which the run prints under `gate policy` so the decision "
        "is legible to a reader of the output rather than only to a reader of the source.\n"
        "  - it can never fail by construction -> NOT_A_CLAUSE, which is checked above and "
        "will refuse a key the corpus reports PASS or FAIL.")

    refuted = report.pending_refuted(statuses, fetching=fetching)
    assert not refuted, (
        "a pending row is contradicted by the corpus it is a claim about: "
        + "; ".join(f"{prefix!r} — {why}" for prefix, why in refuted)
        + ".\nPending claims two things: clean on the eleven, and the twelfth not yet "
        "confirmed. The fetchless sweep refutes the first half and the fetching sweep the "
        "second — and the second refutation is a promotion to GATED_STATE, which is the whole "
        "reason the state exists.")


def _from_disk(url: str) -> bytes:
    """The wire, answered out of the working trees. The seam is `sources._fetch` and nothing
    else, so a test can put the sweep in fetching mode without touching the network."""
    for surface in COMMITTED:
        if surface.published == url:
            return (ROOT / surface.repo / surface.path).read_bytes()
    return b"<html><head><title>x</title></head><body><h1>x</h1></body></html>"


def test_a_wire_failure_skips_the_fetching_sweep_rather_than_reddening_it(monkeypatch):
    """A DNS blip is not a statement about a page, and the ratchet must not read it as one.

    Both halves assert a count that follows the mode, so an unreachable twelfth takes `read`
    to eleven against an expectation of twelve and **both** go red — on a scheduled run, at
    07:00, about nothing. `_local_sheet`'s argument one level out: a false gate is worse than
    a missing one.
    """
    def dead(url):
        raise OSError("dns")

    monkeypatch.setattr(sources, "_fetch", dead)
    with pytest.raises(pytest.skip.Exception, match="corpus is incomplete"):
        _sweep(allow_fetch=True)


def test_a_fetch_that_fell_back_to_the_committed_file_skips_it_too(monkeypatch):
    """The quiet half, and the one no count catches.

    When *one* of the eleven cannot be fetched, `sources.load` falls back to its committed
    file and the sweep still reads twelve. The count is satisfied and the corpus is a mixture:
    the floor would then certify a key as clean on *the twelve published surfaces* on the
    strength of a file nobody served. `_row`'s own caveat — *"from the committed file; the
    wire was not read"* — is the same finding one layer up, and it exists because printing
    `clear` unqualified reinstates the premise `0009` §3.1 removed.
    """
    def one_page_down(url):
        if url == COMMITTED[0].published:
            raise OSError("dns")
        return _from_disk(url)

    monkeypatch.setattr(sources, "_fetch", one_page_down)
    with pytest.raises(pytest.skip.Exception, match="the verdict came from"):
        _sweep(allow_fetch=True)


def test_a_stylesheet_the_wire_dropped_skips_the_fetching_sweep(monkeypatch):
    """The dangerous one, because it makes a failing clause read *clean*.

    `_undecided_where_the_stylesheet_is_incomplete` rewrites every clause-1 and clause-3
    `FAIL` to `UNDECIDED` when a sheet could not be read — correctly, since a clause cannot
    fail on a stylesheet it never read. But `UNDECIDED` is not `FAIL`, so the floor sees the
    key as clean and *demands* its admission to the gate, on a sheet the run never opened.
    Two of the twelve link an external same-origin sheet, so this is one blip away on every
    scheduled run.
    """
    def sheets_down(url):
        if url.endswith(".css"):
            raise OSError("dns")
        return _from_disk(url)

    monkeypatch.setattr(sources, "_fetch", sheets_down)
    with pytest.raises(pytest.skip.Exception, match="stylesheet the wire did not deliver"):
        _sweep(allow_fetch=True)


def test_the_fetching_sweep_reads_the_twelfth_surface_the_fetchless_one_cannot(monkeypatch):
    """The row's whole subject, as an assertion rather than as a mode flag.

    `wroclaw-air-insights` commits no HTML, so the fetchless sweep reads eleven and the gate
    covers twelve. This is the difference, measured: same corpus, two modes, two counts — and
    the expectation follows the mode rather than being pinned at either.
    """
    monkeypatch.setattr(sources, "_fetch", _from_disk)
    fetchless, _ = _sweep(allow_fetch=False)
    try:
        fetched, statuses = _sweep(allow_fetch=True)
    except pytest.skip.Exception as incomplete:
        # **A skip is a pass, and that is what makes this branch necessary.** Every other
        # assertion here is reached only if the sweep returns, so a mode that never arrives at
        # `sources.load` takes the wire away from all twelve surfaces, marks the corpus
        # incomplete, and skips — green, silently, with the row's whole subject unmeasured.
        # Measured: hardcoding `allow_fetch=False` back into the loop leaves this test green
        # without it. With `_fetch` stubbed to answer from disk no fetch can fail, so
        # incomplete here has exactly one cause and it is the plumbing.
        pytest.fail(f"the wire is stubbed and cannot fail, and the sweep still called its "
                    f"corpus incomplete: {incomplete}. The mode is not reaching sources.load")
    assert fetchless == len(COMMITTED) == _expected(False)
    assert fetched == len(sources.SURFACES) == _expected(True)
    assert fetched == fetchless + 1
    assert "served" in statuses, (
        "the fetching sweep emits no `served` key, so the floor cannot see the one finding "
        "whose exemption row 13b exists to make honest")


def test_the_computed_table_does_not_depend_on_set_iteration_order():
    """Classes, scrolling wrappers and ancestries are all sets, and several of them reach the
    printed detail. Two runs under different hash seeds must produce the same table, or the
    output that replaces `0007` §3 would differ between the person writing it down and the
    person checking it.
    """
    require_submodule("ab-lab")

    def run(seed: str) -> str:
        environment = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
        # `--report-only` is what decouples this from the gate's exit code — on that path
        # `main` returns 0 whatever it finds — so the test can fail for exactly one reason.
        # With the gate on and `check=True` it reddened under four mutations that are about
        # the gate and none about set iteration order.
        finished = subprocess.run(
            [sys.executable, "-m", "tools.pagespec", "--detail", "--report-only"],
            cwd=ROOT, env=environment, capture_output=True, text=True,
            encoding="utf-8", check=False,
        )
        # `check=False` on top of that removed the last assertion that the subprocess did
        # anything at all: with the checker raising on its first line, both runs produced
        # empty output, the two empties compared equal, and this test passed. It is the
        # suite's **only** test that runs the module as a process, so an argparse
        # regression, an import failure, or a `UnicodeEncodeError` under the encoding this
        # test pins — live on Windows, where the table is full of em-dashes — was invisible
        # to every test there is. Relaxing a coupled assertion is not the same as removing
        # it, and the first fix did the second.
        #
        # `startswith("pagespec")` was that first fix, and it reaches only a failure that
        # happens **before** the first print — the header is emitted above the surface loop.
        # Reproduced: with `clauses.check` raising, both seeds emit the header and nothing
        # else, the two compare equal, and this test passed. So the exit code is asserted
        # too. Under `--report-only` `main` returns 0 whatever it finds (`__main__.py`), so a
        # non-zero code here means the process died rather than that the gate refused — the
        # coupling this flag exists to break stays broken, and the assertion is restored to
        # full strength. Not `check=True`: `CalledProcessError` hides the two tables.
        assert finished.returncode == 0, (
            f"the checker exited {finished.returncode} under --report-only, where it "
            f"returns 0 whatever it finds\n{finished.stderr}")
        assert finished.stdout.startswith("pagespec"), (
            f"the checker printed no table; exit {finished.returncode}\n{finished.stderr}")
        return finished.stdout

    assert run("0") == run("12345")
