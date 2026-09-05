"""Report mode — the command line, and the one thing it must never do yet.

`0008` S2 schedules the gate *after* the rollout rather than before it, because a gate
written before any page is green has no reference to gate against. So the exit status is
zero whatever the checker finds, and that is asserted here on a tree built to fail every
clause — the day someone turns this into a gate, this test is where the decision surfaces.
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


def test_the_checker_exits_zero_on_a_page_that_fails_every_clause_it_can(tree, capsys):
    """Report only. `ADR-0004` §6 and `0008` S2 both turn on this, and reversing it is a
    decision about the rollout rather than about the checker."""
    assert report.main(["--root", str(tree), "--only", "mlops-car-price"]) == 0
    assert "fail" in capsys.readouterr().out


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
    assert report.main(["--root", str(tmp_path)]) == 0


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
    report.main(["--root", str(tree), "--fetch", "--only", "wroclaw-air-insights"])
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
