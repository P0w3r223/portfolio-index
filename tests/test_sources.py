"""The I/O boundary — where each surface's bytes come from, and what happens when they don't.

`0007` §2 names one failure that every earlier attempt made: **answering a question about the
rendered page from something that is not the rendered page.** It has three shapes here, and
each has a test — reading the HTML and calling it the page, reading a stale local build
instead of the live URL, and reading an empty page as a page.

No test in this file touches the network. `_fetch` is the single seam and it is stubbed.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import ROOT, fixture
from tools.pagespec import sources


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """A working tree holding one repository whose CSS is not inlined."""
    docs = tmp_path / "mini-traceroute" / "docs"
    (docs / "assets").mkdir(parents=True)
    (docs / "index.html").write_text(
        fixture("mini_traceroute_shape/index.html"), encoding="utf-8")
    (docs / "assets" / "styles.css").write_text(
        fixture("mini_traceroute_shape/assets/styles.css"), encoding="utf-8")
    return tmp_path


PAGE = sources.Surface("mini-traceroute", "mini-traceroute", "docs/index.html")


# -- the complete stylesheet, not the inline half -------------------------------------------


def test_a_linked_same_origin_sheet_is_read_alongside_the_inline_blocks(tree):
    """This is the trap that recorded `mini-traceroute` as having no `overflow-x` rule across
    three sessions: it is the one page whose CSS is not inlined."""
    loaded = sources.load(PAGE, tree, allow_fetch=False)
    assert ".scroll-x { overflow-x: auto; }" in loaded.css
    assert loaded.stylesheets == ["assets/styles.css"]


def test_inline_blocks_come_first_and_the_linked_sheet_follows(tree):
    """Order is not cosmetic: `declarations()` returns rules in source order so that paint
    order stays recoverable, and a caller reading the concatenation depends on it."""
    page = tree / "mini-traceroute" / "docs" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "</head>", "<style>.inline { overflow-x: scroll }</style></head>"), encoding="utf-8")
    loaded = sources.load(PAGE, tree, allow_fetch=False)
    assert loaded.stylesheets == ["<style>", "assets/styles.css"]
    assert loaded.css.index(".inline") < loaded.css.index(".scroll-x")


def test_a_third_party_sheet_is_declared_unread_rather_than_fetched(tree):
    """Three pages fetch Inter from `fonts.googleapis.com`. Reading it would put a third
    party's CSS into a portfolio measurement, and not saying so would hide that clause 1 was
    answered from an incomplete sheet."""
    page = tree / "mini-traceroute" / "docs" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "</head>",
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">'
        "</head>"), encoding="utf-8")
    loaded = sources.load(PAGE, tree, allow_fetch=False)
    assert loaded.unreadable == [
        "https://fonts.googleapis.com/css2?family=Inter (third party, not read)"]
    assert "Inter" not in loaded.css


def test_a_protocol_relative_sheet_is_third_party_too(tree):
    page = tree / "mini-traceroute" / "docs" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "</head>", '<link rel="stylesheet" href="//cdn.example/x.css"></head>'),
        encoding="utf-8")
    assert sources.load(PAGE, tree, allow_fetch=False).unreadable == [
        "//cdn.example/x.css (third party, not read)"]


def test_a_same_origin_sheet_that_is_missing_is_reported_rather_than_skipped(tree):
    """Silently skipping it would report the page as having no scroller rule — the same
    wrong answer as never looking, with no trace that anything was missed."""
    (tree / "mini-traceroute" / "docs" / "assets" / "styles.css").unlink()
    loaded = sources.load(PAGE, tree, allow_fetch=False)
    assert loaded.unreadable == ["assets/styles.css"]
    assert loaded.stylesheets == []


# -- a page that cannot be read is not an empty page ---------------------------------------


def test_a_surface_whose_file_is_absent_comes_back_as_none(tmp_path):
    """An empty page satisfies no clause and would be reported as a dozen failures, which
    reads as a portfolio-wide regression when the truth is that a submodule is not checked
    out. `None` is the difference between "not measured" and "measured and bad"."""
    assert sources.load(PAGE, tmp_path, allow_fetch=False) is None


def test_the_fetch_only_surface_is_not_read_from_disk_when_fetching_is_off():
    """`wroclaw-air-insights` commits no HTML at all. `reports/site/` is a gitignored local
    build that has been 24 days stale and produced a wrong answer that survived a session."""
    wroclaw = next(one for one in sources.SURFACES if one.must_fetch)
    assert sources.load(wroclaw, ROOT, allow_fetch=False) is None


def test_a_fetch_that_fails_comes_back_as_none_rather_than_as_a_blank_page(monkeypatch):
    def refuse(url):
        raise OSError("network is unreachable")

    monkeypatch.setattr(sources, "_fetch", refuse)
    wroclaw = next(one for one in sources.SURFACES if one.must_fetch)
    assert sources.load(wroclaw, ROOT, allow_fetch=True) is None


def test_a_fetched_page_resolves_its_linked_sheet_against_the_pages_url(monkeypatch):
    """The live surface is the only one that exists for that page, so its sheets have to be
    resolved relative to the URL rather than to any path on this machine."""
    asked: list[str] = []

    def record(url):
        asked.append(url)
        if url.endswith("page.css"):
            return ".chart-wrap { overflow-x: auto }"
        return '<html><head><link rel="stylesheet" href="assets/page.css"></head></html>'

    monkeypatch.setattr(sources, "_fetch", record)
    wroclaw = next(one for one in sources.SURFACES if one.must_fetch)
    loaded = sources.load(wroclaw, ROOT, allow_fetch=True)
    assert asked == [wroclaw.url, wroclaw.url + "assets/page.css"]
    assert ".chart-wrap" in loaded.css


# -- the registry ----------------------------------------------------------------------------


def test_every_surface_is_named_once():
    """The report keys its rows by name, and `--only` selects by it."""
    names = [surface.name for surface in sources.SURFACES]
    assert len(names) == len(set(names))


def test_the_registry_holds_twelve_surfaces_across_eleven_repositories():
    """`0007` §3 measures eleven pages and names `car-price-ml`'s second surface as the
    twelfth; `token-budget` has no page and is not a surface. `ADR-0004` §4 states the
    coverage the other way round — twelve repositories, one of which is out of scope."""
    assert len(sources.SURFACES) == 12
    assert len({surface.repo for surface in sources.SURFACES}) == 11
    assert "token-budget" not in {surface.repo for surface in sources.SURFACES}


def test_car_price_ml_publishes_two_surfaces_from_one_repository():
    """`0008` §2.1: the contrast rollout scopes by token *source*, and a per-page reading of
    a per-repository fact undercounts it."""
    surfaces = [one for one in sources.SURFACES if one.repo == "car-price-ml"]
    assert {one.path for one in surfaces} == {"docs/index.html", "docs/app/index.html"}


def test_exactly_one_surface_exists_only_at_a_live_url():
    fetch_only = [one for one in sources.SURFACES if one.must_fetch]
    assert [one.name for one in fetch_only] == ["wroclaw-air-insights"]
    assert fetch_only[0].url.startswith("https://")


def test_a_surface_with_a_committed_path_is_never_fetched():
    for surface in sources.SURFACES:
        assert surface.must_fetch is (surface.path is None)
