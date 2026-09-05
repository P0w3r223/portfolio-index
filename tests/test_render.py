"""What a reader meets on the page — the parser, and the three ways it lied before.

`render.py` carries three of the four defects the checker found in itself, and all three are
of one class: they produced a **confident wrong number** rather than an error. So each is
pinned twice — once by the smallest markup that makes the mechanism visible, and once by the
reduction of the real page that demonstrated it, frozen in `fixtures/`.

The mutation each test is written against is named in its docstring. If a test here can pass
with the fix reverted, it is not doing its job.
"""

from __future__ import annotations

import pytest

from conftest import fixture, page
from tools.pagespec import clauses, render

NARROW = "\u202f"
NBSP = "\u00a0"


# -- defect 1: str.split() destroys the codepoints clause 8 exists to count ---------------


def test_a_narrow_no_break_space_survives_being_flattened():
    """`str.split()` splits on Unicode whitespace, and U+202F is Unicode whitespace.

    The obvious `" ".join(text.split())` rewrites the two codepoints clause 8 measures into
    ordinary spaces, so every page would read as separating thousands with a plain space.
    Revert `_ASCII_WHITESPACE` to `\\s+` and this fails.
    """
    assert render._flat(f"183{NARROW}798") == f"183{NARROW}798"
    assert render._flat(f"3{NBSP}466,62") == f"3{NBSP}466,62"


def test_flattening_still_collapses_the_whitespace_markup_introduces():
    """The fix must not stop doing the job: indentation and line breaks still collapse."""
    assert render._flat("  in 183 798\n\tbytes;\r\n XSD 1.0  ") == "in 183 798 bytes; XSD 1.0"


def test_the_page_that_prints_narrow_spaces_still_prints_them_after_parsing():
    """The doc-extract reduction: three U+202F figures in the text and one written `&nbsp;`.

    `convert_charrefs` turns `&nbsp;` into the codepoint, which is the reading this checker
    takes — clause 8 measures what a reader sees, not how the byte was spelled.
    """
    text = page(fixture("narrow_spaces.html")).rendered_text
    assert text.count(NARROW) == 3, "the narrow no-break spaces were normalised away"
    assert text.count(NBSP) == 1, "the &nbsp; entity did not survive as U+00A0"


def test_a_figure_that_lives_only_in_an_attribute_is_not_text_the_page_prints():
    """`<meta name="description">` carries a fourth narrow-spaced figure and must not count.

    A description is not rendered text. Counting attributes would inflate every page's
    separator tally by whatever its card metadata repeats.
    """
    source = fixture("narrow_spaces.html")
    assert source.count(NARROW) == 4, "the fixture no longer holds the attribute figure"
    assert page(source).rendered_text.count(NARROW) == 3


# -- defect 2: adjacent text nodes weld into a figure the page does not print -------------


def test_two_neighbouring_cells_do_not_weld_into_one_grouped_figure():
    """`<td>0</td><td>684</td>` concatenated reads as `0 684`, which nothing on the page says.

    This is the mechanism behind every wrong separator tally in the record. Join
    `rendered_text` with a space instead of a newline and this fails.
    """
    text = page("<table><tr><td>0</td><td>684</td></tr></table>").rendered_text
    assert "0\n684" == text
    assert "0 684" not in text


def test_the_break_between_nodes_is_a_character_no_separator_class_counts():
    """The guard holds only while the joiner sits outside clause 8's separator class.

    Changing the join character to any separator would restore the weld silently, so the
    property is read back off the output rather than left implied by the case above.
    """
    text = page("<td>5</td><td>315</td>").rendered_text
    assert text == "5\n315"
    assert text[1] not in clauses._SEPARATOR_NAMES


def test_a_grouped_figure_inside_one_node_is_still_read_as_one_figure():
    """The break forbids welding; it must not forbid the real thing.

    A grouped figure lives inside one text node or it is not one figure — so the separator
    a page genuinely prints has to survive.
    """
    assert page(f"<p>183{NARROW}798 bytes</p>").rendered_text == f"183{NARROW}798 bytes"


def test_the_recorded_table_of_neighbouring_numbers_yields_no_welded_figure():
    """The pl-review-sense reduction: the table whose cells produced nine false tallies."""
    text = page(fixture("welded_cells.html")).rendered_text
    for welded in ("0 684", "34 650", "684 0.376"):
        assert welded not in text, f"adjacent cells welded into {welded!r} again"


# -- defect 4: an SVG carries its own <title> for accessibility ---------------------------


def test_a_chart_title_does_not_become_the_documents_title():
    """SVG `<title>` is the chart's accessible name, not the page's.

    Taking the last `<title>` seen makes the document title read as the name of the final
    chart on the page — which is what five of the eleven surfaces would report today.
    """
    parsed = page(fixture("svg_titles.html"))
    assert parsed.title.startswith("A 5% test is only 5% if you look once")
    assert "cost of asking more than one question" not in parsed.title


def test_a_page_whose_only_title_is_inside_an_svg_has_no_title_at_all():
    """The `_in_svg` guard on its own, with the first-wins rule taken out of the picture.

    Reporting no `<title>` is the fail-closed direction: clause 4 then says so, instead of
    passing the page on the name of a chart.
    """
    assert page("<body><svg><title>Median advert price by age</title></svg></body>").title == ""


def test_a_self_closed_shape_inside_an_svg_does_not_disturb_the_open_stack():
    """`<line ... />` is XHTML-style and not a void element; ab-lab's charts are full of it.

    Left on the stack it would report the page as unclosed, which turns clause 3 undecided
    on a page that is fine.
    """
    assert page(fixture("svg_titles.html")).unclosed == 0


# -- the ancestry guard `_Rendered` bought the hard way -----------------------------------


def test_a_wrapper_that_never_closes_is_counted_rather_than_ignored():
    """A wrapper left open makes every table below it read as wrapped — a false green.

    `unclosed` is what lets clause 3 refuse to answer instead of answering wrongly.
    """
    parsed = page('<div class="table-wrap"><table></table><table></table>')
    assert parsed.unclosed == 1
    own, ancestors = parsed.tables[1]
    assert "table-wrap" in ancestors, "the second table inherits an ancestry that is not real"


def test_void_elements_never_join_the_open_stack():
    """`<img>`, `<meta>` and `<link>` have no end tag; on the stack they would never leave."""
    assert page('<p><img src="a.png"><br><meta charset="utf-8"></p>').unclosed == 0


def test_a_self_closed_link_is_read_once_and_leaves_nothing_open():
    assert page('<head><link rel="stylesheet" href="a.css"/></head>').stylesheet_hrefs() == \
        ["a.css"]


# -- what the head is asked for ------------------------------------------------------------


@pytest.mark.parametrize("markup, key, expected", [
    ('<meta name="description" content="d">', "description", "d"),
    ('<meta property="og:title" content="t">', "og:title", "t"),
    ('<meta name="twitter:card" content="summary">', "twitter:card", "summary"),
    ('<meta name="description" content="d">', "og:description", None),
])
def test_card_metadata_is_read_under_either_name_or_property(markup, key, expected):
    """`og:*` is a `property` and `description` is a `name`; a checker needs both."""
    assert page(markup).meta(key) == expected


def test_only_stylesheet_links_are_offered_as_stylesheets():
    """A favicon and a preconnect are `<link>`s too, and neither carries CSS."""
    parsed = page(
        '<link rel="icon" href="data:image/svg+xml,x">'
        '<link rel="preconnect" href="https://fonts.gstatic.com">'
        '<link rel="stylesheet" href="assets/styles.css">'
    )
    assert parsed.stylesheet_hrefs() == ["assets/styles.css"]


def test_stylesheet_and_script_bodies_are_not_text_the_reader_sees():
    """CSS declarations are full of numbers; counted as text they would score as figures."""
    parsed = page(
        "<style>.a { width: 183798px }</style><script>var n = 183798;</script><p>seen</p>"
    )
    assert parsed.rendered_text == "seen"
    assert parsed.inline_styles == [".a { width: 183798px }"]


def test_the_first_h1_is_the_headline_and_a_later_one_does_not_replace_it():
    parsed = page("<h1>A claim about the work</h1><h1>Appendix</h1>")
    assert parsed.headline == "A claim about the work"


def test_a_self_closing_skipped_tag_does_not_swallow_the_rest_of_the_page():
    """The guard whose absence is silent, total, and reports no error at all.

    `handle_starttag` raises `_skipped` for `<script>` and `<style>`. An XHTML-style
    `<script src="a.js" />` never reaches `handle_endtag`, so without the matching decrement
    in `handle_startendtag` the counter stays raised for the whole parse and **every later
    text node is dropped**. The page then reports an empty title, an empty `h1` and "no
    grouped figure" — four clauses reading a blank page, each with a confident verdict.
    """
    page = render.parse(
        '<html><head><script src="a.js" /><title>A claim about the work</title></head>'
        '<body><h1>A claim</h1><p>183\u202f798 bytes</p></body></html>'
    )
    assert page.title == "A claim about the work"
    assert page.headline == "A claim"
    assert "183\u202f798" in page.rendered_text


def test_a_self_closing_style_tag_does_not_swallow_the_rest_of_the_page():
    """The same guard, on the other skipped element."""
    page = render.parse(
        '<html><head><style /></head><body><p>1\u202f000</p></body></html>')
    assert "1\u202f000" in page.rendered_text


def test_a_self_closing_svg_does_not_leave_the_document_title_unreachable():
    """`_in_svg` is raised alongside `_skipped` and has to come back down with it."""
    page = render.parse(
        '<html><body><svg /><title>Not the document title</title></body></html>')
    assert page.title == "Not the document title"
