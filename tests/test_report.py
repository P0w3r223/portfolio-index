"""The command line, and the gate `0008` S-gate turned on.

Until that stage the exit status was zero whatever the checker found, and this file asserted
it on a tree built to fail every clause. That test said *"the day someone turns this into a
gate, this test is where the decision surfaces"* — it did, and the tests below are what
replaced it. It was not deleted: the workflow named it as the guard on report-only mode, and
a guard that vanishes along with the thing it guarded is the silent-green shape this suite
exists to catch.

**Every test here runs with no submodule on disk.** That is the `core` job's contract, and it
is why the ratchet's corpus check lives in `test_published_surfaces.py` instead — a claim
about what `GATED` may contain can only be asserted against the real trees.
"""

from __future__ import annotations

from pathlib import Path

import pytest

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
    catch. `ADR-0004` §6 is the normative home and was amended in the same change."""
    assert report.main(["--root", str(tree), "--only", "mlops-car-price"]) == 1
    out = capsys.readouterr().out
    assert "gate — a clause in GATED failed" in out
    assert "1 tokens" in out


def test_a_page_failing_only_an_ungated_clause_still_passes(tree, capsys):
    """**The test that proves the ratchet is a ratchet.** Without it every guard here would
    also pass on a gate that simply gated everything — which would go red on S9's own first
    commit, and on every surface it had not reached yet.

    The page below fails exactly the two clauses outside `GATED`: a comma-grouped figure
    (clause 8) and a `<title>` leading with the directory (clause 4's `<title>` half). Both
    print, neither gates.
    """
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
    assert "  ab-lab                   clear, 1 undecided" in out
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
