"""The command line, and the gate `0008` S-gate turned on.

Until that stage the exit status was zero whatever the checker found, and this file asserted
it on a tree built to fail every clause. That test said *"the day someone turns this into a
gate, this test is where the decision surfaces"* — it did, and the tests below are what
replaced it. It was not deleted: the workflow named it as the guard on report-only mode, and
a guard that vanishes along with the thing it guarded is the silent-green shape this suite
exists to catch.

**Every test here runs with no submodule on disk.** That is the `core` job's contract, and it
is why the ratchet's corpus checks live in `test_published_surfaces.py` instead — a claim
about what `GATED` may contain can only be asserted against the real trees.

The one `GATED`-adjacent test that does live here is the `NOT_A_CLAUSE` pin, and the split is
the same rule read the other way: the floor and ceiling are *measurements* and need the
corpus, while the exemption set is a **policy list** and its pin compares two frozensets. It
sits in the job a contributor runs while editing that constant, which is the job that would
otherwise not see it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import urllib.error

from conftest import NOT_A_CLAUSE, ROOT
from tools.pagespec import __main__ as report
from tools.pagespec import clauses, sources

#: Every clause 1 value as `0007` §5 pins it — the eight settled tokens, and the measured
#: half of the two splits rather than the majority half. Built here rather than reduced from
#: a page because no page satisfies it yet; that is what `0008` S3–S8 are for.
CONFORMING_CSS = """
:root {
  --bg: #ffffff; --surface: #f6f8fa; --border: #e3e7ee; --text: #1c2430;
  --muted: #5b6472; --accent: #2563eb; --warn: #b45309; --radius: 10px;
  --accent-soft: #5b93e4; --positive: #047857;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #0f1319; --accent-soft: #4167a6; --positive: #34d399; }
}
.table-wrap { overflow-x: auto; }
.card { background: var(--surface); border: 1px solid var(--border); }
"""


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """A root holding one surface that fails a good deal and one that satisfies the spec."""
    (tmp_path / "mlops-car-price" / "docs").mkdir(parents=True)
    (tmp_path / "mlops-car-price" / "docs" / "index.html").write_text(
        "<html><head><title>mlops-car-price — MLOps</title></head>"
        "<body><h1>mlops-car-price</h1></body></html>", encoding="utf-8")

    (tmp_path / "ab-lab" / "docs").mkdir(parents=True)
    (tmp_path / "ab-lab" / "docs" / "index.html").write_text(
        "<html><head>"
        "<title>A 5% test is only 5% if you look once — ab-lab</title>"
        f"<style>{CONFORMING_CSS}</style>"
        + "".join(f'<meta property="{key}" content="x">' for key in clauses.CARD_META)
        + '<link rel="icon" href="f.svg">'
        "</head><body>"
        '<p class="eyebrow">Applied statistics</p>'
        "<h1>A 5% test is only 5% if you look once</h1>"
        '<li class="kpi">4</li>'
        '<a href="https://github.com/P0w3r223">More work</a>'
        "</body></html>", encoding="utf-8")
    return tmp_path


def test_a_page_failing_a_gated_clause_makes_the_checker_refuse(tree, capsys):
    """The reversal of `test_the_checker_exits_zero_...`, which stood here until `0008`
    S-gate and is replaced rather than deleted: it was the guard on report-only mode, and
    the workflow named it as such, so dropping it silently is the shape this suite exists to
    catch. `ADR-0004` §6 is the normative home and was amended in the same change.

    **The clause is asserted below the header, not anywhere in the output.** `assert "1 tokens"
    in out` was satisfied by the ordinary per-surface detail line, which prints for any `FAIL`
    whether or not it gated — so under `GATED = ("6 ",)`, where `1 tokens` is not gated at all,
    this test still passed: the fixture also fails `6 back-link` and gated on that instead. It
    proved *some clause gated*, under a name promising it was this one.
    """
    assert report.main(["--root", str(tree), "--only", "mlops-car-price"]) == 1
    out = capsys.readouterr().out
    header = "gate — a clause in GATED failed"
    assert header in out
    assert "1 tokens" in out.split(header, 1)[1], (
        "the clause is in the report but not in the gate's own list, so what refused the "
        "build was a different clause")


def test_a_page_failing_only_an_ungated_clause_still_passes(tree, capsys, monkeypatch):
    """**The test that proves the ratchet is a ratchet.** Without it every guard here would
    also pass on a gate that simply gated everything — which would go red on S9's own first
    commit, and on every surface it had not reached yet.

    The page below fails exactly two clauses: a comma-grouped figure (clause 8) and a `<title>`
    leading with the directory (clause 4's `<title>` half). Both print, neither gates.

    **The ungated set is constructed rather than borrowed**, and that is what keeps this test
    alive. It read the two real gaps in `GATED`, and those gaps are exactly what `0008` S9 and
    S10 exist to close: once both land, `GATED` covers every key that can be `FAIL`, `_gated`
    becomes equivalent to `status == FAIL`, and this test has no construction left — it would
    be deleted as unsatisfiable at precisely the moment it is the last guard on the
    distinction. Removing the two prefixes here is a no-op today and is the whole test
    afterwards.
    """
    monkeypatch.setattr(report, "GATED",
                        tuple(prefix for prefix in report.GATED
                              if prefix not in ("8 ", "4 title")))
    page = (tree / "ab-lab" / "docs" / "index.html").read_text(encoding="utf-8")
    page = page.replace("<title>A 5% test is only 5% if you look once — ab-lab</title>",
                        "<title>ab-lab — A 5% test is only 5% if you look once</title>")
    page = page.replace("</body>", "<p>1,234 resamples</p></body>")
    (tree / "ab-lab" / "docs" / "index.html").write_text(page, encoding="utf-8")

    assert report.main(["--root", str(tree), "--only", "ab-lab"]) == 0
    out = capsys.readouterr().out
    assert "FAIL  8 separator" in out and "FAIL  4 title" in out
    assert "gate —" not in out


def test_a_committed_surface_that_cannot_be_read_gates(tree, capsys):
    """Policy 2 of `0008` §4.11. A renamed or deleted path must not degrade to a green skip
    — that is the silent-green shape §3.7, §3.9 and §4.9 each record, and a checker that
    passes a page it never opened is worse than one that fails."""
    (tree / "ab-lab" / "docs" / "index.html").unlink()
    assert report.main(["--root", str(tree), "--only", "ab-lab"]) == 1
    assert "a surface that should have been readable was not read" in capsys.readouterr().out


def test_needing_fetch_is_the_one_unread_reason_that_does_not_gate(tree, capsys):
    """The other half of policy 2, asserted separately — `0008` §4.4's lesson is that a guard
    proved on one shape of two is a guard on neither. The push job is deliberately offline,
    so `wroclaw` being unread there is the design and not a defect; only the scheduled run
    asks for the wire.

    `--only` is doing real work here rather than tidying: a first version ran over the whole
    fixture tree, where nine committed surfaces are also absent, so it gated on *those* and
    proved nothing about the reason it names. The test has to be able to fail for one reason.
    """
    assert report.main(["--root", str(tree), "--only", "wroclaw-air-insights"]) == 0
    out = capsys.readouterr().out
    assert "wroclaw-air-insights (needs --fetch)" in out
    assert "gate —" not in out


def test_a_same_origin_stylesheet_the_run_could_not_read_gates(tree, capsys):
    """Policy 2 one level down, and it was found by review rather than by the tests.

    Every clause reading `loaded.css` answers from whatever was assembled; a sheet the page
    names and the run could not open makes those answers a reading of an incomplete
    stylesheet, and the page then reports `clear`. Renaming a sheet carrying a webfont
    `@import` moved a surface from `FAIL 7 webfont` to `clear`, exit 1 to exit 0 — a renamed
    *stylesheet* degrading to a green pass, where policy 2 already refuses a renamed *page*.
    """
    page = (tree / "ab-lab" / "docs" / "index.html").read_text(encoding="utf-8")
    (tree / "ab-lab" / "docs" / "index.html").write_text(
        page.replace("</head>", '<link rel="stylesheet" href="absent.css"></head>'),
        encoding="utf-8")
    assert report.main(["--root", str(tree), "--only", "ab-lab"]) == 1
    out = capsys.readouterr().out
    assert "a same-origin stylesheet the page names could not be read" in out
    assert "ab-lab  absent.css" in out
    # The header has to be the right one. This gated under "a clause in GATED failed" at
    # first, on a row printing `clear`, with `stylesheets` being an UNDECIDED that is not in
    # GATED — pointing the reader at §4.11 policy 1, the paragraph that says UNDECIDED never
    # gates. Naming the wrong reason is how a real finding gets read as noise.
    assert "a clause in GATED failed" not in out


def test_a_third_party_stylesheet_is_unread_by_design_and_does_not_gate(tree, capsys):
    """The other half, asserted separately. A third-party sheet is skipped deliberately —
    fetching one would put a page's verdict on somebody else's CDN — so it must not gate,
    and `0008` §3.6 already records clause 7 being *quiet rather than silent* about it.

    This pair also pins the bug the first fix shipped with: it parsed the `stylesheets`
    message with `split(", ")`, and the third-party marker *contains* that separator, so
    every exempt sheet split in two and the fragment gated. The structured list was there
    the whole time.
    """
    page = (tree / "ab-lab" / "docs" / "index.html").read_text(encoding="utf-8")
    (tree / "ab-lab" / "docs" / "index.html").write_text(
        page.replace("</head>",
                     '<link rel="stylesheet" href="https://cdn.example/x.css"></head>'),
        encoding="utf-8")
    assert report.main(["--root", str(tree), "--only", "ab-lab"]) == 0
    assert "gate —" not in capsys.readouterr().out


def test_report_only_prints_the_same_table_and_refuses_to_decide(tree, capsys):
    """The escape hatch, and it is deliberately not the default. A gate reached only by
    remembering a flag is one a later workflow edit drops without anyone noticing; gating by
    default costs nothing today, because `GATED` is clean on all twelve surfaces."""
    assert report.main(["--root", str(tree), "--only", "mlops-car-price",
                        "--report-only"]) == 0
    assert "gate —" not in capsys.readouterr().out


def test_a_surface_that_satisfies_the_spec_reports_clear_and_still_says_what_it_could_not_judge(
        tree, capsys):
    """*"States a claim"* stays undecided even on a conforming page, so `clear` and an
    undecided count appear together. A row that read plainly `clear` would be the checker
    claiming the one verdict `0007` §7 says it cannot reach."""
    report.main(["--root", str(tree), "--only", "ab-lab"])
    out = capsys.readouterr().out
    assert "  ab-lab                   clear, 4 undecided" in out
    assert "FAIL" not in out


def test_only_selects_one_surface_and_leaves_the_rest_unread(tree, capsys):
    report.main(["--root", str(tree), "--only", "ab-lab"])
    out = capsys.readouterr().out
    assert "mlops-car-price" not in out


def test_a_surface_that_could_not_be_read_is_listed_with_its_reason(tmp_path, capsys):
    """Silence here would read as twelve clean pages. The reason matters too: *not found* is
    a submodule that is not checked out, and *needs --fetch* is the one page that exists only
    at a live URL."""
    report.main(["--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert "not read:" in out
    assert "wroclaw-air-insights (needs --fetch)" in out
    assert "ab-lab (not found)" in out


def test_nothing_is_fetched_unless_fetching_is_asked_for(tmp_path, monkeypatch, capsys):
    """A checker that reached the network by default would make a page's verdict depend on
    whether the machine running it happened to be online."""
    def refuse(url):
        raise AssertionError(f"the report fetched {url} without --fetch")

    monkeypatch.setattr(report.sources, "_fetch", refuse)
    # 1, not 0: every committed surface is absent from an empty root, and `0008` §4.11's
    # policy 2 gates on a surface that should have been readable. The subject of this test is
    # the network, and the exit code moved underneath it when the gate landed.
    assert report.main(["--root", str(tmp_path)]) == 1


def test_detail_prints_the_findings_that_are_not_failures(tree, capsys):
    """Without `--detail` the report prints failures and undecided findings only, so a passing
    clause is invisible — which is fine for a work list and useless for the table `0007` §3
    used to hold by hand."""
    report.main(["--root", str(tree), "--only", "ab-lab"])
    brief = capsys.readouterr().out
    report.main(["--root", str(tree), "--only", "ab-lab", "--detail"])
    full = capsys.readouterr().out
    assert "2 tiles" not in brief
    assert "ok    2 tiles" in full


@pytest.mark.parametrize("statuses, expected", [
    ([clauses.PASS, clauses.PASS], "clear"),
    ([clauses.FAIL], "1 fail"),
    ([clauses.FAIL, clauses.FAIL, clauses.UNDECIDED], "2 fail, 1 undecided"),
    ([clauses.PASS, clauses.UNDECIDED], "clear, 1 undecided"),
    ([clauses.NOT_APPLICABLE], "clear"),
])
def test_the_row_counts_failures_and_undecided_findings_separately(statuses, expected):
    """An undecided finding is not a failure and must not be counted as one — that is the
    whole of `0007` §7 in one line of formatting."""
    findings = [clauses.Finding("c", status, "") for status in statuses]
    assert report._row("surface", findings).split(maxsplit=1)[1] == expected


def test_the_report_names_the_document_and_the_clause_range_it_computes(tree, capsys):
    """The output replaces a table in a normative document, so it has to say which one."""
    report.main(["--root", str(tree)])
    assert "clauses 1-8 of 0007 §5" in capsys.readouterr().out


def test_the_default_root_is_the_index_repository_itself():
    """`--root` defaults two directories up from `__main__.py`, which is the working tree
    holding the twelve submodules."""
    from tools import pagespec

    assert Path(pagespec.__file__).resolve().parents[2] == \
        Path(__file__).resolve().parents[1]


def test_a_failed_fetch_is_not_reported_as_a_flag_the_reader_forgot(tree, capsys, monkeypatch):
    """`--fetch` given and the network down must not print "needs --fetch".

    That message tells the reader to pass a flag they passed, and hides an HTTP or DNS
    failure as operator error — on the one surface that exists nowhere but the wire, in the
    scheduled run the workflow adds precisely to keep that row fresh.
    """
    def refuse(url):
        raise OSError("connection refused")

    monkeypatch.setattr(sources, "_fetch", refuse)
    # The exit code, and it was missing: `missing` has **three** reasons and only two were
    # asserted, so `reason == "not found"` — dropping the fetch-failure branch entirely —
    # left the whole suite green. That branch is the sole mechanism behind the `live` job's
    # stated purpose, and `0008` §4.12's mutation table had no row for it. n-1 of n on a
    # three-way branch, which is §4.4's shape.
    assert report.main(["--root", str(tree), "--fetch",
                        "--only", "wroclaw-air-insights"]) == 1
    out = capsys.readouterr().out
    assert "fetch failed" in out
    assert "needs --fetch" not in out


def test_without_the_flag_the_same_surface_says_which_flag_is_missing(tree, capsys):
    report.main(["--root", str(tree), "--only", "wroclaw-air-insights"])
    assert "needs --fetch" in capsys.readouterr().out


def test_an_unknown_surface_name_is_refused_rather_than_answered_with_an_empty_table(tree):
    """A tool whose product is a table must not answer a typo with a blank one."""
    with pytest.raises(SystemExit) as raised:
        report.main(["--root", str(tree), "--only", "car-price-mI"])
    assert raised.value.code == 2


def test_the_census_counts_references_per_family_and_names_the_minority():
    """`0008` §3.8 leans on the census as S6's report-only observation, and nothing reached
    it. It counts `var()` references rather than surfaces, because one sheet holding a role
    ten times is ten voices and a per-surface tally would read it as one."""
    palette = ":root { --bg: #fff; --surface: #eee; --border: #ddd; --warn: #b45309; }"
    sheets = [
        ("one", palette + ".a { background: var(--surface); }"
                          ".b { background: var(--surface); }"
                          ".c { border: 1px solid var(--border); }"),
        ("two", palette + ".d { background: var(--bg); }"
                          ".e { border-left: 3px solid var(--warn); }"),
    ]
    lines = report._census(sheets)
    text = "\n".join(lines)
    assert "background" in text and "border" in text
    assert "--surface" in text and "--bg" in text and "--warn" in text
    surface = next(line for line in lines if "--surface" in line)
    assert "  2 " in surface and "one" in surface and "two" not in surface
    warn = next(line for line in lines if "--warn" in line)
    assert "two" in warn


def test_a_family_no_sheet_paints_is_left_out_rather_than_printed_empty():
    lines = report._census([("one", ":root { --bg: #fff; } .a { background: var(--bg); }")])
    assert any("background" in line for line in lines)
    assert not any(line.startswith("  border") for line in lines)


def test_the_census_is_suppressed_when_one_surface_was_asked_for(tree, capsys):
    """A distribution over one sheet is not a distribution, and printing it under `--only`
    would invite reading a single page's choices as the portfolio's.

    **Through the fixture, not the real tree.** A first draft called `main` with the default
    root, so in the `core` CI job — which checks out no submodule and is the job that must
    never go red — there was no page on disk, the census was empty either way, and the
    assertion held whether or not the suppression existed.
    """
    report.main(["--root", str(tree), "--only", "ab-lab"])
    out = capsys.readouterr().out
    assert "ab-lab" in out, "the surface asked for was not reported at all"
    assert "role census" not in out


def test_the_census_is_printed_when_every_surface_was_read(tree, capsys):
    """The other half: suppression that suppressed always would pass the test above."""
    report.main(["--root", str(tree)])
    assert "role census" in capsys.readouterr().out


def test_the_exemption_set_is_pinned_because_it_is_policy_and_not_a_measurement():
    """Adding a key here must take two deliberate edits and carry a proof.

    The corpus check in the floor guard refuses an exempt key the eleven surfaces report
    `PASS` or `FAIL`, which catches the careless case with a good message. It cannot catch the
    dangerous one: `1 composited` and `4 h1` are `UNDECIDED` on every surface, so the check is
    vacuous on exactly the two keys the floor guard's own docstring names when it rejects the
    PASS-derived alternative. Measured — dropping `"4 h1"` from `GATED` **and** adding it here
    left all 394 tests green and the checker exiting 0, with clause 4's `h1` silently no longer
    gating twelve surfaces.

    So this set is pinned. Every other floor here is derived from the corpus on purpose, and
    this one is not a measurement at all: it is a policy list, and a policy list that can be
    extended by one word in one place is the hiding place the docstring below says it is not.
    An addition means editing this assertion too, and bringing what `stylesheets` brought —
    `test_the_stylesheets_finding_can_never_fail_which_is_what_makes_its_exemption_safe`, a
    proof that the key cannot reach `FAIL` rather than an observation that it has not yet.
    """
    assert NOT_A_CLAUSE == frozenset({"stylesheets", "contrast ground"}), (
        "NOT_A_CLAUSE changed. Every entry needs a test proving the key can never be FAIL — "
        "the corpus check in the floor guard is a weaker, corpus-scoped proxy and is vacuous "
        "for a key that is UNDECIDED everywhere, which is what the dangerous ones are.")


# -- the gate registry, and the two branches no corpus can exercise ---------------------------
#
# `0009` §7 row 13b turned `GATED` from a tuple into `GATE`, a registry of `(prefix, state,
# reason)`. Its `pending` state exists for a situation that arises once per clause admission —
# three times in this system's life — so **the working trees cannot exercise it**: nothing
# fails anywhere today, and a guard written only against the corpus would ship both of its
# branches unexecuted. That is why the arithmetic is in `__main__` and proved here, in the job
# that runs with no submodule on disk.


def _statuses(**pairs) -> dict[str, set[str]]:
    """A corpus sweep's product, fabricated. The keys are finding keys, the values statuses."""
    return {clause: set(seen) for clause, seen in pairs.items()}


def test_every_row_the_gate_does_not_refuse_on_carries_a_reason():
    """The difference between an exemption and a place for a key to hide is one sentence.

    A gated prefix needs none — the ceiling guard re-takes its licensing measurement on every
    run over the real trees. Anything outside the gate is a decision instead of a measurement,
    and `served` spent two stages outside it under an argument that lived in a comment block
    and a test docstring, where no reader of the table could find it.
    """
    for one in report.GATE:
        if one.state == report.GATED_STATE:
            continue
        assert one.reason.strip(), (
            f"{one.prefix!r} is {one.state} and says nothing about why. A state outside the "
            "gate is a decision; a decision with no reason beside it is the silence this "
            "registry replaced.")


def test_the_registry_holds_one_row_per_prefix_and_every_state_is_a_known_one():
    """Two ways a second membership axis becomes the hiding place it was built to close.

    A prefix in two rows makes its treatment depend on iteration order — `explained` returns
    the first match and `GATED` collects every gated one, so a key could be both refused on
    and exempted from the floor. A misspelled state is worse and quieter: it matches no
    derivation at all, so the prefix silently stops gating *and* stops being demanded.

    **Nested, not only identical** — and the identical-strings version of this test shipped
    while its own docstring claimed the stronger property. `explained` matches by
    `startswith`, so `Ratchet("4 ", REPORT_ONLY_STATE, …)` declared above `4 eyebrow` answers
    for every clause-4 key while `GATED` still contains all three: one clause, two
    descriptions, arbitrated by tuple order. Measured green across all 510 tests. Clause 4's
    split is the registry's stated reason for keying on prefixes at all, and `ADR-0005` §5
    records `1 dark` / `1 dark --positive` as a live pair in the same vocabulary — so this is
    a shape the corpus already has, not a hypothetical.
    """
    prefixes = [one.prefix for one in report.GATE]
    assert len(prefixes) == len(set(prefixes)), f"a prefix is declared twice: {prefixes}"
    nested = [(a, b) for a in prefixes for b in prefixes if a != b and a.startswith(b)]
    assert not nested, (
        f"one row's prefix is inside another's: {nested}. `explained` returns whichever comes "
        "first in the tuple, so the registry would describe one clause two ways and the "
        "answer would depend on declaration order")
    for one in report.GATE:
        assert one.state in report.STATES, (
            f"{one.prefix!r} is {one.state!r}, which is not one of {report.STATES}: it would "
            "gate nothing and be demanded by nothing")


def test_the_report_only_set_is_pinned_because_it_is_policy_and_not_a_measurement():
    """**The narrowing route the registry added, and the floor cannot see.**

    Under the tuple there was one way to un-gate a clause — delete the prefix — and
    `clean_but_unexplained` catches it, because the key is then covered by no row. The
    registry adds a second: leave the row and change its state. `Ratchet("8 ",
    REPORT_ONLY_STATE, "a stage is mid-flight")` un-gates clause 8 permanently, `GATED`
    silently becomes nine prefixes, and **all 510 tests pass** — measured, with the fetching
    floor simulated from the working trees: `clean_but_unexplained` returns nothing, because
    a report-only row *is* an explanation.

    `GATED_STATE → PENDING_STATE` is caught, by the fetching floor demanding the promotion.
    `report-only` is the hole, and it is a hole precisely because report-only is the one state
    that answers no question the corpus can ask.

    So this set is pinned, exactly as `NOT_A_CLAUSE` is pinned five tests up and for the
    reason that test's docstring gives: *a policy list that can be extended by one word in one
    place is the hiding place*. An addition means editing this assertion too — which is the
    second deliberate edit, and the reason to write down why.

    *`ADR-0005` §4 predicted this when it refused to derive `GATED` from the clause registry:
    deriving it would add "a third cause — a registry row flipped — that the message does not
    name". `ADR-0006` took the derivation anyway, on different grounds, and inherited the cause
    without the message. The ceiling guard now names it.*
    """
    assert set(report.report_only()) == {"served", "contrast marks"}, (
        "report_only() changed. It is a policy list and not a measurement: every entry is a "
        "decision that a key which CAN fail will never gate, and nothing in the corpus can "
        "refute one. Adding a row here un-gates whatever it covers, silently, in every job.")


def test_gated_is_derived_from_the_registry_rather_than_typed_beside_it():
    """`0009` N1's shape — two lists of one vocabulary tied by nothing — refused in the file
    that would otherwise be its next instance. Every guard and monkeypatch predating the
    registry reads `GATED`, so the derivation is what keeps their meaning."""
    assert report.GATED == tuple(one.prefix for one in report.GATE
                                 if one.state == report.GATED_STATE)
    # Pairwise, and the first version chained all three with `&`. That is empty whenever *any*
    # one of them is, and `pending()` is empty by design — so the assertion could not fire:
    # a prefix duplicated into `gated` and `report-only` left it passing. An intersection of
    # three sets is not three intersections, and one of the three is always empty here.
    gated, waiting, printed = set(report.GATED), set(report.pending()), set(report.report_only())
    assert not gated & waiting and not gated & printed and not waiting & printed, (
        f"a prefix is in two states at once: gated={sorted(gated & (waiting | printed))}, "
        f"pending∩report-only={sorted(waiting & printed)}")


def test_the_run_prints_every_key_the_gate_does_not_refuse_on(tree, capsys):
    """Policy legible to a reader of the output, not only to a reader of the source.

    The precedent is `test_no_exempt_key_is_claimed_as_a_carrier` in `test_spec.py`, which
    makes the same claim about `NOT_A_SENTENCE`: a list that decides what an instrument will
    not say must appear in what the instrument says.

    **Asserted through `main`, not through `_policy()`** — and the first version of this test
    did the latter, under a name saying *the run prints*. Deleting the two lines in `main` that
    print the block left all 510 tests green. That is verbatim the defect
    `test_a_stylesheet_the_wire_dropped_is_printed_and_refuses_nothing` records this suite
    having already paid for once: *"The previous guard asserted `report._unreachable_sheets`
    — the helper, never the output … Nothing was printed."* Same shape, same file, one stage
    later, in the guard for `ADR-0006`'s headline consequence.

    It carries more than a docstring's worth here, because with the registry's demotion route
    the printed block is the **only** trace a reader of CI output has that a key stopped
    gating.
    """
    report.main(["--root", str(tree), "--report-only"])
    printed = capsys.readouterr().out
    assert "gate policy" in printed, "the run does not print the keys it refuses to refuse on"
    for one in report.GATE:
        if one.state == report.GATED_STATE:
            # The gated rows are deliberately absent: the table above already says what they
            # decided. Asserted, because `outside = list(GATE)` is one edit and turns the
            # block into ten lines of noise around the rows that matter — green, measured.
            assert f"  {one.prefix:<12}{report.GATED_STATE}" not in printed, (
                f"{one.prefix!r} gates and is listed under `gate policy`, which is the list "
                "of what does not")
            continue
        assert f"{one.prefix} " in printed and one.state in printed, (
            f"{one.prefix!r} is outside the gate and the run does not say so")
        # Separated, not merely both present. `contrast marks` welded itself to its state as
        # `contrast marksreport-only` under a fixed `<12` column, and this assertion passed —
        # it asked whether two substrings existed, which they did, inside one unreadable word.
        assert f"{one.prefix}{one.state}" not in printed, (
            f"{one.prefix!r} is printed against its state with no separator, so the one trace "
            f"a reader of CI output has that a key stopped gating is a single run-on word")
        assert one.reason.split(":")[0][:40] in printed, (
            f"{one.prefix!r} is printed without its reason, which is the half that matters")


def test_a_clean_key_no_row_covers_is_what_the_floor_reports():
    """The floor's own arithmetic, over statuses rather than over the twelve trees."""
    statuses = _statuses(**{"1 tokens": [clauses.PASS], "9 novel": [clauses.PASS],
           "stylesheets": [clauses.UNDECIDED]})
    assert report.clean_but_unexplained(statuses) == ["9 novel", "stylesheets"]
    assert report.clean_but_unexplained(
        statuses, exempt=NOT_A_CLAUSE) == ["9 novel"]
    # A key that fails is not the floor's business — that is the ceiling's, and conflating the
    # two is how the ratchet came to be guarded in one direction only (`0009` §5.1).
    assert report.clean_but_unexplained(_statuses(**{"9 novel": [clauses.FAIL]})) == []


def test_a_pending_row_the_eleven_report_failing_is_refuted(monkeypatch):
    """Pending is a confirmation the registry is waiting on, not a waiting room."""
    monkeypatch.setattr(report, "GATE",
                        report.GATE + (report.Ratchet("9 ", report.PENDING_STATE, "under test"),))
    refuted = report.pending_refuted(_statuses(**{"9 novel": [clauses.FAIL]}), fetching=False)
    assert refuted and refuted[0][0] == "9 " and "failing" in refuted[0][1]


def test_a_pending_row_clean_on_the_twelve_demands_its_promotion(monkeypatch):
    """The fetching half, and the reason `pending` is not simply `report-only` with a wish.

    This is S9's and S10's hand navigation as an assertion: the twelfth was confirmed by a
    person running `--fetch` and watching `refresh.yml` rebuild, and the tuple then moved
    because they remembered to move it.
    """
    monkeypatch.setattr(report, "GATE",
                        report.GATE + (report.Ratchet("9 ", report.PENDING_STATE, "under test"),))
    refuted = report.pending_refuted(_statuses(**{"9 novel": [clauses.PASS]}), fetching=True)
    assert refuted and refuted[0][0] == "9 " and "published surfaces" in refuted[0][1]


def test_a_pending_row_the_run_never_emitted_is_not_a_confirmation(monkeypatch):
    """Absence is not a measurement.

    Without the `matching` test, a pending prefix for a clause that emits nothing at all —
    a stage half-landed, a key renamed — reports no failure and would be promoted into the
    gate on the strength of never having been asked.
    """
    monkeypatch.setattr(report, "GATE",
                        report.GATE + (report.Ratchet("9 ", report.PENDING_STATE, "under test"),))
    assert report.pending_refuted(_statuses(**{"1 tokens": [clauses.PASS]}), fetching=True) == []


# -- the served page, and the wire that must stay off the push path ---------------------------


def _fetched(monkeypatch, tree, body, *, error=None, code=None):
    """One surface loaded with `_fetch` stubbed. The seam, and nothing else, is faked."""
    def stub(url):
        if error is not None:
            raise error
        return body
    monkeypatch.setattr(sources, "_fetch", stub)
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    return sources.load(surface, tree, allow_fetch=True), surface


def test_no_served_finding_is_emitted_when_nothing_was_fetched(tree):
    """The silence is load-bearing, not tidiness.

    If `served` appeared as `n/a` on the fetchless sweep, the ratchet's floor guard would see
    it clean-and-ungated and demand it in `GATED` on the first commit — forcing the gating
    decision before one measurement exists. Staying out of that sweep is what lets it ship
    report-only.
    """
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    loaded = sources.load(surface, tree, allow_fetch=False)
    assert loaded is not None
    assert not [one for one in clauses.check(loaded) if one.clause == "served"]


def test_served_bytes_equal_to_the_committed_file_pass(monkeypatch, tree):
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    body = (tree / surface.repo / surface.path).read_bytes()
    loaded, _ = _fetched(monkeypatch, tree, body)
    finding = next(one for one in clauses.check(loaded) if one.clause == "served")
    assert finding.status == clauses.PASS
    assert "served" in finding.detail and "committed" in finding.detail


def test_a_page_differing_only_in_line_endings_still_passes(monkeypatch, tree):
    """`core.autocrlf` rewrites the working-tree copy on Windows. Measured 2026-09-07:
    un-normalised, five of the eleven committed pages differ from what is served and every
    one of the five differs *only* in line endings — the delta equals the file's CRLF count
    exactly. Without the fold this reports five regressions on a developer's machine and none
    in CI, which is worse than not having the instrument."""
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    committed = (tree / surface.repo / surface.path).read_bytes()
    # **The served body must be the *other* spelling of whatever is on disk.** A first version
    # always built the CRLF form — and this checkout writes CRLF, so the two byte strings came
    # out identical and the test passed with the fold deleted. It was green over the defect it
    # names, in the guard for the one constraint this stage found by measuring rather than by
    # reasoning. Caught by the mutation, which is why the mutation exists.
    folded = clauses._lf(committed)
    other = folded if committed != folded else folded.replace(clauses._LF, clauses._CRLF)
    assert other != committed, "the two spellings are identical; this test would be vacuous"
    assert clauses._lf(other) == folded, "the two spellings must be one page after folding"
    crlf = other
    loaded, _ = _fetched(monkeypatch, tree, crlf)
    finding = next(one for one in clauses.check(loaded) if one.clause == "served")
    assert finding.status == clauses.PASS


def test_served_bytes_that_differ_fail_and_name_both_hypotheses(monkeypatch, tree):
    """The checker cannot tell a stale pointer from a broken publish, and must not guess. It
    names the discriminator instead — `entry_state --full` is the instrument that asks whether
    each pointer equals its own `origin/main`."""
    loaded, _ = _fetched(monkeypatch, tree, b"<html><title>something else</title></html>")
    finding = next(one for one in clauses.check(loaded) if one.clause == "served")
    assert finding.status == clauses.FAIL
    assert "pointer" in finding.detail and "publish" in finding.detail
    assert "entry_state" in finding.detail


def test_a_wire_failure_is_undecided_and_does_not_gate(monkeypatch, tree, capsys):
    """A DNS blip must not read as eleven page regressions. This is `_local_sheet`'s own
    argument — a false gate is worse than a missing one — one level out."""
    loaded, _ = _fetched(monkeypatch, tree, None, error=OSError("dns"))
    finding = next(one for one in clauses.check(loaded) if one.clause == "served")
    assert finding.status == clauses.UNDECIDED
    assert not report._gated(finding)


def test_a_page_that_is_gone_fails_rather_than_reading_as_a_wire_failure(monkeypatch, tree):
    """404 is an answer about the page, not about the network, and the two must not arrive as
    one line — `0007` §2's subject is exactly this distinction."""
    gone = urllib.error.HTTPError("http://x", 404, "Not Found", {}, None)
    loaded, _ = _fetched(monkeypatch, tree, None, error=gone)
    finding = next(one for one in clauses.check(loaded) if one.clause == "served")
    assert finding.status == clauses.FAIL
    assert "gone" in finding.detail


def test_the_wire_never_reaches_the_push_path():
    """`--fetch` reaches no job that runs on a push or a pull request.

    Three mechanisms keep the network off a merge: the key is emitted only when bytes were
    fetched, `_gated` never fires on `UNDECIDED`, and this — the one that nothing guarded.

    **Twice too narrow before now.** It first scoped to lines containing `run:`, and the block
    scalar spelling puts `--fetch` on a line with no `run:` on it. Then it excluded comments
    but asked `job in ("core", "surfaces")` — two names typed out — so a *third* job added on
    the push trigger was the same single edit the docstring warns about, and passed. It asks
    which jobs the triggers reach now, and reads that from the file too.

    Comments are excluded rather than `run:` lines included, because the file names `--fetch`
    three times in prose explaining why it is absent — an occurrence count ships broken.
    """
    workflow = (ROOT / ".github" / "workflows" / "pagespec.yml").read_text(encoding="utf-8")
    lines = workflow.splitlines()

    def block(name):
        """The lines of one top-level block, by indentation rather than by a typed list."""
        start = next((i for i, one in enumerate(lines) if one.rstrip() == f"{name}:"), None)
        assert start is not None, f"{name}: is not in the workflow"
        out = []
        for one in lines[start + 1:]:
            if one.strip() and not one.startswith(" "):
                break
            out.append(one)
        return out

    triggers = block("on")
    push_events = [one.strip().rstrip(":") for one in triggers
                   if one.strip().rstrip(":") in ("push", "pull_request")]
    assert push_events, "the workflow no longer runs on a push; this guard has no subject"

    #: A job is off the merge path only if it says so. `live` gates itself with an `if:` on
    #: the event name; anything without one runs on every push there is.
    guarded, job, offenders = set(), None, []
    for one in block("jobs"):
        stripped = one.strip()
        if one.startswith("  ") and not one.startswith("    ") and stripped.endswith(":"):
            job = stripped[:-1]
        # **A *job-level* `if:`, at exactly four spaces.** A step's `if:` sits at eight and
        # guards that step's execution, not the job's trigger — so reading one as a job guard
        # exempts every `--fetch` in the job from this check. Measured: a step in `surfaces`
        # carrying `if: always()` and `python -m tools.pagespec --fetch` passed this guard with
        # the wire on the merge path. **The enabling edit is in the same commit as this fix**:
        # `live`'s new `if: always()` is the first step-level `if:` this workflow has ever had,
        # so the shape went from hypothetical to demonstrated inside the file the guard reads.
        # Fourth time this predicate has been too narrow, and the first time it was widened
        # before something used it.
        indent = len(one) - len(one.lstrip(" "))
        if job and stripped.startswith("if:") and indent == 4:
            # **Guarded means the condition excludes the push triggers, not that it mentions
            # a dispatch.** Asking for the substring `workflow_dispatch` read
            # `if: github.event_name == 'schedule'` as unguarded — a false red — and
            # `... == 'workflow_dispatch' || ... == 'pull_request'` as guarded, which is the
            # single edit this guard exists to catch. Third time this predicate was a typed
            # literal in disguise.
            if not any(f"'{event}'" in stripped for event in push_events):
                guarded.add(job)
        if "--fetch" in stripped and not stripped.startswith("#"):
            offenders.append((job, stripped))

    on_the_push_path = [(job, line) for job, line in offenders if job not in guarded]
    assert not on_the_push_path, (
        f"the wire is on the merge path: {on_the_push_path}. A job fetches unless its `if:` "
        f"restricts it to a schedule or a dispatch; guarded jobs here are {sorted(guarded)}"
    )
    assert offenders, "no job fetches at all — the live surface stops being read by anything"

    #: And the ratchet's own fetching run, which is a *different* claim from "something
    #: fetches". Dropping `--fetch` from the pytest step leaves the checker's own `--fetch`
    #: line above satisfying `offenders`, so the assertion passes while the two ratchet halves
    #: silently sweep eleven surfaces in the one job built to sweep twelve — and `pending`
    #: would then be promoted by nothing, ever. That is the whole of `0009` §7 row 13b at the
    #: CI layer, reverted by deleting six characters. Measured green before this line existed.
    swept = [(job, line) for job, line in offenders
             if "pytest" in line and "-m submodules" in line]
    assert swept, (
        "no job runs `pytest -m submodules --fetch`, so the ratchet's corpus is eleven "
        "surfaces everywhere and the gate covers twelve — the asymmetry 0009 §7 row 13b "
        "closed, reopened without a red test")
    assert all(job in guarded for job, _line in swept), (
        f"the fetching ratchet runs on the merge path: {swept}")


def test_served_is_deliberately_outside_the_gate_and_the_reason_is_recorded():
    """**Report-only, and this is where that decision lives rather than in a silence.**

    The ratchet's rule is that a key reporting zero `FAIL` across every surface read must be
    gated, and `served` reports exactly that — eleven of eleven, measured 2026-09-07. So the
    rule says gate it. It is not gated, for a reason the rule does not cover:

    **neither ratchet guard can see this key.** Both derived from `_sweep()`, which hardcoded
    `allow_fetch=False`, and `served` is emitted only when bytes were fetched. Putting it in
    `GATED` would add a prefix that the ceiling guard cannot check and the floor guard cannot
    demand — *a place for a key to hide*, which is the phrase the floor guard's own docstring
    is written against.

    *That reason expired with `0009` §7 row 13b, and this test now asserts the one that did
    not.* The sweep takes its mode as a parameter, so the fetching floor **does** see this key
    — and sees it clean, eleven of eleven, which under the floor's own rule is a demand that it
    be gated. There was no green state: `test_the_ratchet_cannot_be_narrowed_either…` demanded
    the gating, this test refused it, and `test_spec.py` closed the obvious escape by refusing
    `served` in `NOT_A_CLAUSE` — correctly, since that set's pin demands a proof the key can
    never be `FAIL` and `served` fails whenever a sibling publishes ahead of a pointer bump.
    Three guards, no arrangement satisfying all three. `REPORT_ONLY_STATE` is the third answer
    the taxonomy needed, and `0009` §7 row 8 is where it was first noticed missing.

    So the claim asserted here is now the *substantive* one, which was always the stronger
    half: a mismatch is routinely not a defect, so gating this key would redden the daily run
    as ordinary portfolio work proceeds. It is in the registry, it prints under `gate policy`
    with that reason, and it does not gate.
    """
    assert "served" not in report.GATED
    assert not any("served".startswith(prefix) for prefix in report.GATED), (
        "a GATED prefix now covers `served`, and a mismatch is routinely not a defect"
    )
    assert "served" in report.report_only(), (
        "served has left the registry: report-only is a recorded decision, and a key that "
        "gates nothing while no row explains it is the silence row 13b closed")
    assert "publishing" in report.report_only()["served"]


def test_the_clauses_are_answered_from_the_served_bytes_and_not_from_the_file(
        monkeypatch, tree):
    """C1's *first* half, which the `served` finding does not cover.

    A hash mismatch says the two disagree; it does not say which clause the public page now
    fails. Under `--fetch` the verdicts have to come from the wire, or the table still
    describes the pinned page while claiming to be the live job — the founding failure `0007`
    §2 names, committed by the instrument built to end it.

    Built as a page *conforming on disk and broken on the wire*, because the reverse would
    pass under either behaviour.

    **It read the real working tree in its first version**, so it passed here and failed in
    the `core` job, which runs without a single page on disk: with no committed file there is
    nothing to serve *against*, the `served` key is not emitted at all, and the eyebrow
    assertion was satisfied for the wrong reason — the served bytes were simply the only
    source. `0009` §8 row 3 is the same class, and it is why `core` exists.
    """
    served = b"<html><head><title>a claim</title></head><body><p>no eyebrow</p></body></html>"
    loaded, _ = _fetched(monkeypatch, tree, served)
    assert loaded is not None and loaded.served == served
    assert loaded.committed is not None, "the fixture must commit a page to serve against"
    findings = {one.clause: one.status for one in clauses.check(loaded)}
    assert findings["4 eyebrow"] == clauses.FAIL, (
        "the eyebrow verdict came from the committed file, not from what was served"
    )
    assert findings["served"] == clauses.FAIL


def test_a_committed_page_that_has_gone_missing_is_not_masked_by_a_successful_fetch(
        monkeypatch, tree):
    """The fetching twin of `test_a_committed_surface_that_cannot_be_read_gates`.

    Without `--fetch`, a missing `docs/index.html` makes `load` return `None`, which the report
    counts as `missing` and refuses on — `0008` §4.11 policy 2. Once the wire could answer for
    the file, that gate stopped firing: Pages keeps serving the last deployment, so a sibling
    deleting or renaming its page would read `clear` and exit 0 for as long as nobody looked.

    **The `served` key goes silent exactly where the two disagree most**, which is the opposite
    of what it is for.
    """
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    body = (tree / surface.repo / surface.path).read_bytes()
    (tree / surface.repo / surface.path).unlink()

    loaded, _ = _fetched(monkeypatch, tree, body)
    assert loaded is not None and loaded.committed is None
    finding = next(one for one in clauses.check(loaded) if one.clause == "served")
    assert finding.status == clauses.FAIL
    assert "missing" in finding.detail


def test_the_fetch_only_surface_still_emits_nothing_when_it_has_no_committed_file(
        monkeypatch, tree):
    """The other half of the same branch, so the repair cannot turn a design into a defect.

    `wroclaw` commits no HTML — `.gitignore:25` — so *no committed page* is its normal state
    and a `FAIL` there would be the instrument reporting the design as a regression.
    """
    monkeypatch.setattr(sources, "_fetch", lambda url: b"<html><title>x</title></html>")
    wroclaw = next(one for one in sources.SURFACES if one.must_fetch)
    loaded = sources.load(wroclaw, tree, allow_fetch=True)
    assert loaded is not None and loaded.committed is None
    assert not [one for one in clauses.check(loaded) if one.clause == "served"]


def test_a_row_answered_from_the_file_says_so_rather_than_printing_clear(monkeypatch, tree):
    """A fetch that failed falls back to the committed file — right, and silent until now.

    `clear` under a job named for the bytes the public receives, when the wire was never read,
    reinstates the premise C1 removed. The caveat moves no gate; it stops the line claiming
    more than the run earned.

    **It was keyed on the finding's status and so missed the case that needs it most.** A wire
    blip is `UNDECIDED` and a page answering 4xx is `FAIL`; both fall back to the file, and the
    caveat fired only on the first. The second is where every `ok` above came from a file whose
    published counterpart is not being served. Both are asserted here, and so is the negative.
    """
    for label, error in (("a wire blip", OSError("dns blip")),
                         ("the page answering 404",
                          urllib.error.HTTPError("http://x", 404, "Not Found", {}, None))):
        loaded, _ = _fetched(monkeypatch, tree, None, error=error)
        row = report._row("surface", clauses.check(loaded), answered_from_the_file=True)
        assert "the wire was not read" in row, (
            f"{label}: the verdicts came from the file and the row does not say so"
        )
    # And it must not fire when the wire *was* read, or the caveat means nothing.
    good = (tree / next(one for one in sources.SURFACES if not one.must_fetch).repo
            / "docs" / "index.html").read_bytes()
    loaded, _ = _fetched(monkeypatch, tree, good)
    assert "the wire was not read" not in report._row(
        "surface", clauses.check(loaded), answered_from_the_file=False)


def test_a_stylesheet_the_wire_dropped_does_not_gate_but_a_missing_one_still_does(
        monkeypatch, tree, capsys):
    """The policy this branch newly exposed, settled rather than inherited.

    Before `--fetch` read the eleven, only `wroclaw` fetched a stylesheet, so *a sheet the
    network dropped* and *a sheet that is missing* could share one gate without anyone
    noticing. Every scheduled run now fetches eleven more, and two of them link an external
    same-origin sheet — so a blip would have refused a page that is fine, which is the false
    gate `_local_sheet`'s own docstring argues against.

    A 404 is the page answering and still gates: a stylesheet that is gone is a real defect.
    """
    page = b'<html><head><link rel="stylesheet" href="a.css">' \
           b'<title>a claim</title></head><body></body></html>'

    def blip(url):
        if url.endswith("a.css"):
            raise OSError("dns")
        return page

    monkeypatch.setattr(sources, "_fetch", blip)
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    loaded = sources.load(surface, tree, allow_fetch=True)
    assert loaded.unreachable and not loaded.unreadable
    assert not report._unread_same_origin(loaded), "a wire blip must not reach the gate"
    assert report._unreachable_sheets(loaded), "and it must still be printed"

    def gone(url):
        if url.endswith("a.css"):
            raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
        return page

    monkeypatch.setattr(sources, "_fetch", gone)
    loaded = sources.load(surface, tree, allow_fetch=True)
    assert report._unread_same_origin(loaded), "a 404 on a sheet is the page, and still gates"


# -- what the gate does with an input it could not read, asserted on the exit code ------------


def _run(tmp, monkeypatch, fetch_impl, *, only=None, fetch=True):
    """One full `main` run with the wire stubbed. **The exit code is the assertion.**

    Every guard written for these branches asserted a *finding's status* and none asserted the
    run's verdict, which is exactly how three conditions came to print `FAIL` and exit 0.
    """
    monkeypatch.setattr(sources, "_fetch", fetch_impl)
    argv = ["--root", str(tmp)] + (["--only", only] if only else []) + (["--fetch"] if fetch else [])
    return report.main(argv)


def test_a_published_page_answering_404_refuses_the_run(tree, monkeypatch, capsys):
    """It printed `FAIL served — the page is gone` and exited **0**.

    The exemption argued for the `served` key is about a *digest mismatch*, which is routine
    while a sibling has published and the index has not bumped its pointer. A page that is not
    being served is never routine, and it inherited the exemption without anyone arguing it.
    """
    surface = next(one for one in sources.SURFACES if not one.must_fetch)

    def gone(url):
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)

    assert _run(tree, monkeypatch, gone, only=surface.name) == 1
    assert "answered 4xx" in capsys.readouterr().out


def test_a_committed_page_that_is_absent_refuses_even_when_the_wire_answers(
        tree, monkeypatch, capsys):
    """`0008` §4.11 policy 2, restored. It refused before `--fetch` read these eleven; the wire
    then answered in the file's place and the run exited 0, indefinitely, because Pages keeps
    serving the last deployment."""
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    body = (tree / surface.repo / surface.path).read_bytes()
    (tree / surface.repo / surface.path).unlink()

    assert _run(tree, monkeypatch, lambda url: body, only=surface.name) == 1
    assert "commits a page has none" in capsys.readouterr().out


def test_the_surface_that_commits_no_page_does_not_refuse_for_having_none(
        tree, monkeypatch, capsys):
    """The negative, without which the guard above would be a rule that fails the design.

    `wroclaw` commits no HTML — `.gitignore:25` — so having no committed file is its normal
    state, and refusing on it would be the instrument reporting a decision as a regression.

    It serves the fixture's *conforming* page, so the run turns on the absent file rather than
    on this page's own quality: a synthetic page failing clause 5 would make the exit code say
    1 for a reason this test is not about, which is how its first version passed for nothing.
    """
    wroclaw = next(one for one in sources.SURFACES if one.must_fetch)
    body = (tree / "ab-lab" / "docs" / "index.html").read_bytes()
    assert _run(tree, monkeypatch, lambda url: body, only=wroclaw.name) == 0
    assert "commits a page has none" not in capsys.readouterr().out


def test_a_stylesheet_the_wire_dropped_is_printed_and_refuses_nothing(
        tree, monkeypatch, capsys):
    """The whole of the fix, asserted on the run rather than on a helper.

    The previous guard asserted `report._unreachable_sheets(loaded)` — the helper, never the
    output — under a message that said *"and it must still be printed"*. Nothing was printed,
    and the run refused anyway: the CSS clauses failed on a sheet they never read, so the gate
    moved from a key naming the cause to two keys naming a consequence, and the output stopped
    mentioning the stylesheet at all.

    Built from the fixture's conforming page with its inline CSS moved out to a sheet the wire
    drops, because the question is whether an undelivered sheet refuses the run and a page that
    fails a gated clause on its own could not answer it.
    """
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    committed = (tree / "ab-lab" / "docs" / "index.html").read_text(encoding="utf-8")
    start, end = committed.index("<style>"), committed.index("</style>") + len("</style>")
    page = (committed[:start] + '<link rel="stylesheet" href="a.css">'
            + committed[end:]).encode("utf-8")

    def blip(url):
        if url.endswith("a.css"):
            raise OSError("dns")
        return page

    assert _run(tree, monkeypatch, blip, only=surface.name) == 0
    out = capsys.readouterr().out
    assert "not gated — a same-origin stylesheet the wire did not deliver" in out
    assert "a.css" in out, "the operator is never told which sheet, or why"
    assert "FAIL  1 " not in out and "FAIL  3 " not in out, (
        "a clause failed on a stylesheet it never read"
    )


@pytest.mark.parametrize("status, refuses", [
    (404, True), (410, True),      # the page is not there
    (403, False), (429, False),    # the origin declined *this* request
    (503, False),                  # a deploy in flight
])
def test_only_the_statuses_that_mean_the_page_is_gone_refuse(tree, monkeypatch, status, refuses):
    """`served_gone` widened from `(404, 410)` to any 4xx at the same moment it started gating.

    A `429` from a runner fetching twelve pages and their stylesheets, a `403`, or a `304`
    then refused the build under a sentence saying *the page is not being served* — false about
    the event, and the cries-wolf shape `conftest.py` warns about. Neither boundary was
    guarded in either direction: narrowing back left the suite green, and so did widening to
    *any HTTP status*, which is the Pages-503 defect the split was written to end.
    """
    surface = next(one for one in sources.SURFACES if not one.must_fetch)

    def answer(url):
        raise urllib.error.HTTPError(url, status, "x", {}, None)

    assert _run(tree, monkeypatch, answer, only=surface.name) == (1 if refuses else 0)


def test_a_submodule_nobody_checked_out_is_not_a_page_somebody_deleted(
        tree, monkeypatch, capsys):
    """`committed is None` conflates three states, and the restored gate saw only two.

    No file expected (`wroclaw`), the file is gone (a regression), and **the submodule is not
    checked out** — a condition of the machine. `--fetch` is a documented local command, so a
    developer with a partial checkout was told a perfectly good repository had lost its page,
    and the run exited 1.

    That is the instrument blaming the page for the state of the disk, which is the class the
    branch that added this gate spent the evening removing. Found by checking the repair rather
    than by a later pass.
    """
    surface = next(one for one in sources.SURFACES if not one.must_fetch)
    body = (tree / surface.repo / surface.path).read_bytes()

    # The gitlink directory as `actions/checkout` leaves it without `submodules: true`, and as
    # a developer has it before `git submodule update --init`.
    empty = tree / "not-checked-out"
    (empty / surface.repo).mkdir(parents=True)
    monkeypatch.setattr(sources, "_fetch", lambda url: body)
    assert report.main(["--root", str(empty), "--only", surface.name, "--fetch"]) == 0
    assert "commits a page has none" not in capsys.readouterr().out

    # **And the finding, not only the verdict.** Two mechanisms answer this question — the
    # gate in `__main__` and the `served` finding in `clauses` — and asserting the exit code
    # alone left the second one unguarded, which is the shape this whole branch is about.
    loaded = sources.load(surface, empty, allow_fetch=True)
    assert not [one for one in clauses.check(loaded) if one.clause == "served"], (
        "the served key accused a repository nobody has checked out"
    )

    # And a repository that *is* checked out and has lost its page still refuses, or the
    # discrimination has bought the false negative instead of the false positive.
    populated = tree / "checked-out"
    (populated / surface.repo).mkdir(parents=True)
    (populated / surface.repo / "README.md").write_text("here", encoding="utf-8")
    assert report.main(["--root", str(populated), "--only", surface.name, "--fetch"]) == 1
    assert "commits a page has none" in capsys.readouterr().out


# -- the separator census, which 0008 §4.13 requires of S9's first commit --------------------

NARROW = "\u202f"
NBSP = "\u00a0"


def _group(tree: Path, repo: str, figure: str) -> None:
    """Put one grouped figure on a surface, leaving the rest of the page alone.

    The `tree` fixture's two pages print none, which is correct for what they were built to
    exercise and is why the census has to be given something to count. **Appended rather
    than written over**, because `ab-lab`'s fixture page satisfies every other clause and the
    exit-status guard below needs a surface whose only failure is the one being added.
    """
    target = tree / repo / "docs" / "index.html"
    original = target.read_text(encoding="utf-8")
    # A `replace` that matches nothing returns the string unchanged, so a fixture losing its
    # `</body>` would leave every caller asserting against a page with no figure on it. Four
    # tests would go red loudly and one — the `--only` guard — would go **green**, which is
    # the second time that guard has been at risk of passing for the wrong reason.
    assert "</body>" in original, f"{repo}'s fixture has no </body> for the figure to precede"
    target.write_text(original.replace("</body>", f"<p>{figure}</p></body>"), encoding="utf-8")


def test_the_census_prints_every_grouped_figure_and_asserts_nothing(tree, capsys, monkeypatch):
    """`0008` §4.13: *a stage scoped by a figure no instrument prints is scoped by whoever
    counted last.* Three hand counts of the write sites gave fifteen, eighteen and nineteen
    against a true twenty.

    The write sites are lines of Python in eleven other repositories, and `0009` §7 row 6 is
    the decision not to bring them here — `sources.py` is the I/O boundary and nothing else.
    **The figures those sites reach are these bytes**, and this is what the checker can count
    honestly. It prints and it decides nothing: the exit status must not move.

    **The seeded figure is non-conforming, and that is the whole guard.** Seeded with a
    U+202F figure this test was green over a census that appends to `blocked` — the census
    had nothing to object to, so a gating census and a printing one behaved identically. It
    is the second time in this stage a guard was written against the conforming case and
    proved nothing; the first is recorded in `0008` §4.15.

    `GATED` drops `"8 "` so clause 8's own `FAIL` stays out of the gate, which leaves the
    census as the only thing that could move the status. One surface, so nothing is unread.
    """
    _group(tree, "ab-lab", "1 234 resamples")

    monkeypatch.setattr(sources, "SURFACES",
                        tuple(one for one in sources.SURFACES if one.name == "ab-lab"))
    monkeypatch.setattr(report, "GATED",
                        tuple(prefix for prefix in report.GATED if prefix != "8 "))

    assert report.main(["--root", str(tree)]) == 0, (
        "the census moved the exit status, which is what `printed and never asserted` denies")
    out = capsys.readouterr().out

    assert "separator census" in out
    assert "printed and never asserted" in out
    assert "gate —" not in out, "a census that gated would be a second clause 8"

    # **Not `--report-only`, and that is the finding this line records.** With the flag,
    # `main` returns 0 at the `if args.report_only` branch *before* any gate section is
    # printed, so both assertions above hold whether the census gates or not. Measured: a
    # census appending to `blocked` left this green and reddened exactly one test in the
    # suite — in `test_published_surfaces.py`, whose module is `submodules`-marked. A pull
    # request green on `core` alone proved nothing about the invariant this guard is named
    # for, which is the hazard `CLAUDE.md` states about `GATED`. Found by review.


def test_the_verdict_column_says_which_separator_is_the_conforming_one():
    """`assert "clause 8" in out` was the whole guard on this column, and `not clause 8`
    contains it.

    Measured: inverting the conditional, and replacing it with the constant `"clause 8"`,
    both left the **entire suite** green — a census telling a reader that every separator on
    the portfolio conforms would have shipped, and S9 reads its edit order off this column.
    The row is asserted rather than a token in it. `0009` §12.1.2 records the same substring
    shape costing a figure in a document; this is it costing a verdict in an instrument.

    Called directly, which is the role census's own precedent
    (`test_the_census_counts_references_per_family_and_names_the_minority`) and reaches four
    things `main` cannot be made to show cheaply.
    """
    lines = report._separator_census(
        [("conforming", f"<p>1{NARROW}234</p>"), ("not", "<p>5 678</p><td>9,012</td>")], False)

    # Selected by what the row *starts* with: a per-surface row names its separators too,
    # and picking the first line containing "U+202F" finds that one instead.
    narrow = next(line for line in lines if line.strip().startswith("U+202F"))
    assert "not clause 8" not in narrow, "the conforming separator was labelled non-conforming"
    assert "clause 8" in narrow

    for wrong in ("space", "comma"):
        row = next(line for line in lines if line.strip().startswith(wrong))
        assert "not clause 8" in row, f"{wrong} was labelled as satisfying clause 8"


def test_the_census_prints_both_units_so_a_seven_digit_figure_makes_them_disagree():
    """The reason for printing figures *and* separators, and no fixture ever exercised it.

    `clause_8_separator`'s docstring says the two counts are equal *"because none prints a
    figure at or above a million"* — an assumption about the corpus. The census exists to
    turn that into a printed fact, so the branch that fires when it stops being true is the
    claim, and collapsing it to the constant left the whole suite green.
    """
    one_each = report._separator_census([("s", f"<p>1{NARROW}234</p>")], False)
    assert "1 figure(s), 1 separator(s) — one separator each" in chr(10).join(one_each)

    over_a_million = report._separator_census([("s", f"<p>1{NARROW}234{NARROW}567</p>")], False)
    assert "1 figure(s), 2 separator(s) — 1 figure(s) at or above a million" in (
        chr(10).join(over_a_million))


def test_the_summary_names_where_each_separator_was_found():
    """The **other** `in` column, and the one that prints without `--detail`.

    There are two: the per-figure row `in <code>` that `--detail` prints, and this summary
    row — `in code 1, p 1` — that every run prints under the portfolio totals. The guard
    below covered the first, and deleting the second left the **whole suite** green. Found by
    the second review pass, which also noted the consequence: the element distribution that
    was briefly hand-typed into `render.py`'s docstring was a hand sum across these rows, and
    the line that would have kept it honest was the unguarded one. The docstring no longer
    carries the figure; this makes the row that replaces it checkable.
    """
    lines = report._separator_census(
        [("s", f"<code>3{NBSP}466</code><p>1{NBSP}234</p>")], False)

    placed = [line for line in lines if line.strip().startswith("in ")]
    assert placed, (
        "the portfolio summary names no element at all; the row that says where each "
        "separator was found is gone. Census was: " + chr(10).join(lines))
    assert "code 1" in placed[0] and "p 1" in placed[0], (
        f"the summary does not say where the figures were found: {placed[0]!r}")


def test_the_detail_row_names_the_element_each_figure_sits_in():
    """The `in <element>` column is S9c's discriminator, and dropping it left the suite
    green. Asserted here rather than through `main` because `--detail` output is long and a
    substring of it is what the two findings above were."""
    lines = report._separator_census([("s", f"<code>3{NBSP}466,62</code>")], True)
    assert any("in <code>" in line and "3<U+00A0>466" in line for line in lines), (
        "the figure is `3<U+00A0>466`; `,62` is the Polish decimal tail and `_GROUPED`'s "
        "trailing bound ends the token there, which is the pattern behaving as written")


def test_the_census_names_its_separators_rather_than_printing_them(tree, capsys):
    """The first run of this census died on `UnicodeEncodeError` in the `--detail` mode CI
    runs, on a console whose codepage cannot encode U+202F. Naming the codepoint is not a
    formatting preference here — it is what lets the report reach a terminal at all, and it
    is what makes four invisibly-different separators tellable apart."""
    _group(tree, "ab-lab", f"1{NARROW}234</p><p>5{NBSP}678")

    assert report.main(["--root", str(tree), "--report-only", "--detail"]) == 0
    out = capsys.readouterr().out

    assert "1<U+202F>234" in out and "5<U+00A0>678" in out
    census = out[out.index("separator census"):]
    assert NARROW not in census and NBSP not in census, (
        "the census emitted the codepoint it is reporting on")


def test_one_surface_gets_no_census_because_a_census_of_one_is_a_row(tree, capsys):
    """The role census makes the same choice, for the same reason: both are portfolio-wide
    distributions, and `--only` is the flag for looking at a single page.

    **The figure is what makes this assert anything**, and its first version had none. With
    the fixture's pages as built, no surface groups a thousand, so the census returns nothing
    to print and the test passed whether `--only` suppressed it or not — green over the
    mutation removing the suppression. It is put on the surface being selected, so the census
    has something to say and silence can only mean the flag.
    """
    _group(tree, "ab-lab", f"1{NARROW}234")

    report.main(["--root", str(tree), "--report-only", "--only", "ab-lab"])
    assert "census" not in capsys.readouterr().out


def test_a_page_with_no_grouped_figure_is_listed_rather_than_omitted(tree, capsys):
    """An absent row and a row reading zero are different claims, and only one of them is
    checkable. Four of the twelve surfaces print no grouped figure at all; a census that
    simply left them out would be indistinguishable from a census that failed to read them —
    the silent-green shape `0008` §3.7, §3.9 and §4.9 each record in another guard."""
    _group(tree, "ab-lab", f"1{NARROW}234")

    assert report.main(["--root", str(tree), "--report-only"]) == 0
    out = capsys.readouterr().out
    assert "mlops-car-price          no grouped figure" in out


def test_the_census_calls_an_exempt_separator_exempt_and_not_non_conforming():
    """`not clause 8` on a separator every one of whose figures is a clause-8a specimen names
    the codepoint correctly and the page wrongly.

    The census is what a stage reads to scope its edits, so a row telling S9 that
    `doc-extract` has a non-conforming separator would send it to a page that needs no edit —
    and the page it would edit is the one whose whole point is quoting a foreign format.
    """
    lines = report._separator_census([("d", f"<code>3{NBSP}466</code>")], False)
    row = next(line for line in lines if line.strip().startswith("U+00A0"))

    assert "exempt (8a)" in row, f"an exempt-only separator was called non-conforming: {row!r}"
    assert "not clause 8" not in row


def test_a_separator_with_one_exempt_and_one_ordinary_figure_is_not_exempt():
    """The boundary, and it is where a per-separator verdict could go wrong.

    The census tallies by separator and the exemption is per *figure*, so a page mixing a
    specimen with an ordinary figure of the same codepoint must not have the ordinary one
    hidden behind the exemption. Without this, one `<code>` block would clear a whole
    separator across a surface.
    """
    lines = report._separator_census(
        [("d", f"<code>3{NBSP}466</code><p>9{NBSP}999</p>")], False)
    row = next(line for line in lines if line.strip().startswith("U+00A0"))

    assert "not clause 8" in row, f"one specimen exempted an ordinary figure too: {row!r}"


def test_the_detail_row_marks_which_figure_took_the_exemption():
    """Two figures, same codepoint, one exempt — and `--detail` is where a reader checks which."""
    lines = report._separator_census(
        [("d", f"<code>3{NBSP}466</code><p>9{NBSP}999</p>")], True)
    rows = [line for line in lines if "<code>" in line or "<p>" in line]

    assert any("specimen, exempt (8a)" in line and "3<U+00A0>466" in line for line in rows)
    assert not any("specimen" in line and "9<U+00A0>999" in line for line in rows)


def test_the_surface_row_marks_the_exemption_where_a_stage_actually_looks():
    """The portfolio roll-up said `exempt (8a)`; the per-surface row did not.

    `doc-extract  5 figure(s)  U+00A0 1 · U+202F 4` read identically to a non-conforming
    surface, and the surface row is the first thing a stage reads to scope its edits — an
    unmarked `U+00A0 1` sends it to the one page whose whole subject is quoting a foreign
    format. Found by review, after the roll-up had been guarded and this had not.
    """
    rows = report._separator_census(
        [("spared", f"<code>3{NBSP}466</code>"), ("plain", f"<p>9{NBSP}999</p>")], False)

    spared = next(line for line in rows if line.strip().startswith("spared"))
    plain = next(line for line in rows if line.strip().startswith("plain"))
    assert "U+00A0 1 exempt" in spared, f"the surface row hides the exemption: {spared!r}"
    assert "exempt" not in plain, f"an ordinary figure was marked exempt: {plain!r}"

    # **Both figures on one surface, which is the case the two above cannot reach.** With the
    # exemption and the ordinary figure on separate surfaces, "all of them are exempt" and
    # "any of them is exempt" behave identically, so the guard was green over the widening.
    # Here the counts differ — two U+00A0, one spared — and only the strict reading is right:
    # marking the row `exempt` would tell a stage the surface needs no edit when it does.
    mixed = report._separator_census(
        [("both", f"<code>3{NBSP}466</code><p>9{NBSP}999</p>")], False)
    row = next(line for line in mixed if line.strip().startswith("both"))
    assert "U+00A0 2" in row and "exempt" not in row, (
        f"one specimen marked the whole separator exempt on this surface: {row!r}")
