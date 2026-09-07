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
        ("https://fonts.googleapis.com/css2?family=Inter", sources.THIRD_PARTY)]
    assert "Inter" not in loaded.css


def test_a_protocol_relative_sheet_is_third_party_too(tree):
    page = tree / "mini-traceroute" / "docs" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "</head>", '<link rel="stylesheet" href="//cdn.example/x.css"></head>'),
        encoding="utf-8")
    assert sources.load(PAGE, tree, allow_fetch=False).unreadable == [
        ("//cdn.example/x.css", sources.THIRD_PARTY)]


def test_a_missing_same_origin_sheet_is_reported_with_the_reason(tree):
    """Silently skipping it would report the page as having no scroller rule — the same
    wrong answer as never looking, with no trace that anything was missed.

    **And the cause travels with it.** This entry gates, through `_unread_same_origin`, on a
    path the scheduled job walks daily; a rename, a permission error and a file that was never
    written arrive as one identical line when the `except` discards the exception. `0008` §5
    carried that as a residual from the S-gate review, and the fetch branch beside it had
    already made the same argument for itself.
    """
    (tree / "mini-traceroute" / "docs" / "assets" / "styles.css").unlink()
    loaded = sources.load(PAGE, tree, allow_fetch=False)
    assert len(loaded.unreadable) == 1
    href, why = loaded.unreadable[0]
    assert href == "assets/styles.css", "the href is carried, not spelled into prose"
    assert why.startswith("FileNotFoundError"), (
        "the fact without the cause is one line for three faults")
    assert loaded.stylesheets == []


def test_a_cache_busting_query_string_names_a_file_that_can_be_read(tree):
    """An href is a URL reference and not a path, and this one gated a page that is fine.

    `styles.css?v=2` was joined to the directory verbatim, so the read failed on a file
    sitting right there — and an unread same-origin sheet refuses the build. The fetch branch
    has always been right about this, through `urljoin`; only the local branch was not.
    """
    page = tree / "mini-traceroute" / "docs" / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        'href="assets/styles.css"', 'href="assets/styles.css?v=2"'), encoding="utf-8")

    loaded = sources.load(PAGE, tree, allow_fetch=False)

    assert loaded.unreadable == []
    assert loaded.stylesheets == ["assets/styles.css?v=2"]
    assert loaded.css.strip(), "the sheet was located but nothing was read from it"


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


def test_a_percent_encoded_href_reaches_the_file_it_names(tree):
    """`%20` means a space. The fetch branch has always decoded it through `urljoin`."""
    docs = tree / "mini-traceroute" / "docs"
    (docs / "assets" / "my styles.css").write_text(".spaced { overflow-x: auto }",
                                                   encoding="utf-8")
    page = docs / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        'href="assets/styles.css"', 'href="assets/my%20styles.css"'), encoding="utf-8")

    loaded = sources.load(PAGE, tree, allow_fetch=False)

    assert loaded.unreadable == []
    assert ".spaced" in loaded.css


def test_a_file_whose_name_really_contains_a_percent_is_read_rather_than_gated(tree):
    """Decoding is right by the spec and a false gate is worse than a missing one.

    A file literally called `my%20x.css` would be reported unreadable by decoding alone — and
    an unread same-origin sheet refuses the build. The literal spelling is tried second, so
    either name on disk answers the question the clauses are about to ask.
    """
    docs = tree / "mini-traceroute" / "docs"
    (docs / "assets" / "my%20x.css").write_text(".literal { overflow-x: auto }",
                                                encoding="utf-8")
    page = docs / "index.html"
    page.write_text(page.read_text(encoding="utf-8").replace(
        'href="assets/styles.css"', 'href="assets/my%20x.css"'), encoding="utf-8")

    loaded = sources.load(PAGE, tree, allow_fetch=False)

    assert loaded.unreadable == []
    assert ".literal" in loaded.css


def test_the_reason_does_not_repeat_the_absolute_path_the_href_already_names(tree):
    """`str(error)` on a missing file is the whole absolute path, and it reaches gate output."""
    (tree / "mini-traceroute" / "docs" / "assets" / "styles.css").unlink()

    _href, why = sources.load(PAGE, tree, allow_fetch=False).unreadable[0]

    assert str(tree) not in why, "the machine path is in the message the gate prints"
    # `startswith`, not equality: `strerror` is locale-dependent on Linux, and a contributor
    # on a localised desktop would get a red test about a property this one does not assert.
    assert why.startswith("FileNotFoundError: ")
    # Not `!= "FileNotFoundError:"`: the value is built as `f"{type}: {why}"`, so it always
    # carries the colon and a space — that inequality held with the cause deleted entirely,
    # which is the one thing this line exists to catch.
    assert why.removeprefix("FileNotFoundError:").strip(), (
        "the cause is the half that was missing")
