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
    assert render.flatten(f"183{NARROW}798") == f"183{NARROW}798"
    assert render.flatten(f"3{NBSP}466,62") == f"3{NBSP}466,62"


def test_flattening_still_collapses_the_whitespace_markup_introduces():
    """The fix must not stop doing the job: indentation and line breaks still collapse."""
    assert render.flatten("  in 183 798\n\tbytes;\r\n XSD 1.0  ") == "in 183 798 bytes; XSD 1.0"


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


def test_a_self_closed_title_or_heading_does_not_strand_its_collector():
    """`handle_startendtag`'s own docstring: *every counter `handle_starttag` raises has to
    come back down here*. Two did not, and the consequence is a wrong verdict rather than a
    missing one.

    `<title/>` opens the collector and no `handle_endtag` follows, so it stays open and every
    later text node is appended to it. A stray `</title>` anywhere after — malformed markup,
    but markup a browser forgives — then commits the page's **body text as its title**. Clause
    4's `<title>` half would judge that, and `4 title` enters `GATED` with S10.

    Measured both ways before this was written: with the reset the title is empty, without it
    it is `A claim about latency`.
    """
    stranded = render.parse(
        "<html><head><title/></head><body><p>A claim about latency</p></title></body></html>")
    assert stranded.title == "", (
        "the page's body text was committed as its title by a collector nothing closed"
    )
    # And the ordinary shape still works, so the reset has not broken the common case.
    ordinary = render.parse(
        "<html><head><title>The real title</title></head>"
        "<body><h1>The real claim</h1><p>body</p></body></html>")
    assert ordinary.title == "The real title" and ordinary.headline == "The real claim"


def test_a_self_closed_tag_inside_a_heading_does_not_clear_the_collector():
    """The first repair lowered the collectors for **every** self-closed tag.

    `<h1>Fast <br/> answers</h1>` cleared `_heading`, so `handle_endtag("h1")` found it `None`
    and never committed it — `clause_4_opening` then reported `4 h1 FAIL — no <h1>` on a page
    that has one, and `"4 h1"` gates. `<br/>`, `<img/>` and `<wbr/>` inside a heading are
    ordinary markup; `<h1/>` is not. Strictly more reachable than the hole it closed.
    """
    for inner in ("<br/>", "<img src='x.svg'/>", "<wbr/>"):
        parsed = render.parse(
            f"<html><head><title>A claim</title></head>"
            f"<body><h1>Fast {inner} answers</h1></body></html>")
        assert parsed.headline == "Fast answers", f"{inner} cleared the heading collector"
        assert parsed.title == "A claim", f"{inner} did not, but check the title too"
    # **No assertion about a tag inside `<title>`, deliberately.** A first version had one and
    # it passed here and failed in CI: `html.parser` treats `<title>`'s content as RCDATA in
    # some 3.12 patch releases and as markup in others, so `A <meta/> claim` comes back whole
    # on one interpreter and stripped on another. That is a property of CPython and not of
    # this module, and binding a guard to it is the class this suite was just audited for.
    # The heading cases above are the subject, and `<title/>`'s own shape is pinned by
    # `test_a_self_closed_title_or_heading_does_not_strand_its_collector`.


def test_the_rendered_text_is_exactly_its_text_nodes_joined():
    """One flattening rule, in one place, read by two callers.

    `rendered_text` answers clauses 4 and 8; `text_nodes` answers the separator census and
    `0008` S9c's element exemption. They were one list of strings until the census needed the
    ancestry, and the risk in adding it is that the two drift — a census describing text the
    clauses never saw is worse than no census. Derived rather than parallel, so they cannot.
    """
    parsed = render.parse("<p>one</p><style>.x{}</style><p>  two   three </p><script>y</script>")

    assert parsed.rendered_text == chr(10).join(text for text, _ in parsed.text_nodes)
    assert [text for text, _ in parsed.text_nodes] == ["one", "two three"], (
        "runs of ASCII whitespace collapse, <style> and <script> stay out, empties drop")


def test_a_text_node_carries_the_tags_enclosing_it_outermost_first():
    parsed = render.parse("<body><div><p>deep</p></div></body>")
    assert parsed.text_nodes == [("deep", ("body", "div", "p"))]


def test_a_self_closed_tag_pops_the_ancestry_and_a_void_one_never_pushed_it():
    """`_tags` is pushed and popped in lockstep with `_open`, in all three places it moves.

    `_open` already carries this hazard on the record: `handle_startendtag`'s counters *"did
    not come back down"*, and the repair that fixed it then broke `<br/>` inside a heading by
    lowering them for **every** self-closed tag. A second stack popping in only two of the
    three places would drift silently — the ancestry stays a tuple of plausible tag names,
    just the wrong ones, and no clause notices because only the census reads it.

    **Both shapes, because the first version of this guard had only the second and shipped
    green over the mutation it was written for.** `<br/>` and `<img>` are in `_VOID`, so they
    never enter the branch that pops at all; a test built from those exercises nothing. It
    takes a **non-void** self-closed tag — `<span/>` here, `<h1/>` in the comment that records
    the earlier repair — to reach it. Found by mutating, which is the only way it could be.
    """
    parsed = render.parse(
        "<body><p>before<br/>after<img src='x'>end</p><span/><div>outside</div></body>")

    assert [ancestry for _, ancestry in parsed.text_nodes] == [
        ("body", "p"), ("body", "p"), ("body", "p"), ("body", "div")], (
        "a void tag must not push, and a self-closed non-void tag must pop what it pushed")
    assert parsed.unclosed == 0, "the class stack came back down too"


def test_a_paint_alpha_in_the_markup_is_collected_with_the_element_that_carries_it():
    """SVG's three alpha presentation attributes, and the element they belong to.

    Collected here rather than grepped out of the HTML because an attribute is structure, and
    `0007` §2's whole subject is answering a question about the rendered page from something
    that is not it. The classes travel with it **for the clause that will name the site** —
    `1 composited` prints a count and not the sites today, exactly as it does for its CSS
    branch, and S13's walk is what needs to say *which* rect. Recorded that way round because
    the first version of this sentence described a detail line the checker does not print.
    """
    parsed = render.parse(
        '<svg><rect class="cell dense" fill-opacity="0.524"></rect>'
        '<line stroke-opacity="0.3"/><g opacity="0.85"><circle/></g></svg>')

    assert parsed.paint_alphas == [
        ("rect", frozenset({"cell", "dense"}), "fill-opacity", "0.524"),
        ("line", frozenset(), "stroke-opacity", "0.3"),
        ("g", frozenset(), "opacity", "0.85"),
    ]


def test_a_self_closed_element_contributes_its_alpha_exactly_once():
    """`handle_startendtag` delegates to `handle_starttag` and then unwinds the stacks, so a
    collector added to the start handler runs once — and would run twice if it were also added
    to the end-tag path.

    Asserted because every counter in this parser has been wrong in one of those directions at
    least once, and this collector sits in the same handler as all of them.
    """
    parsed = render.parse('<svg><rect fill-opacity="0.4"/><rect fill-opacity="0.4"></rect></svg>')
    assert len(parsed.paint_alphas) == 2
    assert parsed.unclosed == 0


def test_a_void_element_carrying_an_alpha_is_collected_too():
    """The other direction, and **the docstring above claimed it before this test existed.**

    It read *"or zero times if it were added only to the branch that pushes"* — a claim of
    coverage the guard did not have. `<rect>` is not in `_VOID`, so the push branch runs for
    both of its spellings and the case above cannot tell the two placements apart: moving the
    collector inside `if tag not in _VOID:` left all 502 tests green. Found by the
    `code-reviewer` pass mutating inside the space the docstring named, which is the one place
    a claim of coverage can be checked.

    A void tag is where the two placements differ, and the collector belongs outside the push
    branch because an alpha is an attribute of the element rather than of its subtree.
    """
    parsed = render.parse('<img opacity="0.4"><svg><rect fill-opacity="0.3"/></svg>')
    assert [one[0] for one in parsed.paint_alphas] == ["img", "rect"], (
        "a void element carries no subtree, so a collector inside the branch that pushes one "
        "never sees it")


def test_a_colour_in_a_presentation_attribute_is_not_a_paint_alpha():
    """`fill="#2563eb"` is still the declared colour. Only an alpha changes the value between
    the declaration and the pixel, which is what `1 composited` is about."""
    parsed = render.parse('<svg><rect fill="#2563eb" stroke="var(--accent)"/></svg>')
    assert parsed.paint_alphas == []


# -- the element stream: the ancestry `paint_alphas` flattened away ----------------------
#
# `paint_alphas` answers *this page composites somewhere* and cannot answer *this cell is
# painted on that rect*, because it keeps a tag and a class set and drops the structure. A
# contrast question is asked per usage site and a usage site is an element — `0008` §3.11 —
# so the stream is the first thing that stage needs and the last thing it can fake.


def test_an_element_records_the_one_enclosing_it_and_never_itself():
    """Append before the stack moves, or every element becomes its own parent.

    Move `self.elements.append(...)` below the `if tag not in _VOID:` block and the parent of
    each non-void element is the index just pushed — its own — so the `ancestors` walk never
    terminates. The root's `-1` is what makes that walk finite, and it is the whole contract.
    """
    parsed = render.parse('<div class="card"><svg><rect/></svg></div>')
    assert [(one.tag, one.parent) for one in parsed.elements] == [
        ("div", -1), ("svg", 0), ("rect", 1)]


def test_a_void_element_is_recorded_and_adopts_nothing_after_it():
    """Two mutations in opposite directions, and this corpus reaches both.

    Put the append inside `if tag not in _VOID:` and every `<img>`, `<link>` and `<meta>`
    leaves the stream — `paint_alphas` has a test of its own proving a void element can carry
    paint, so dropping them loses usage sites. Push a void element onto `_element_stack`
    instead and nothing ever pops it, so every element after it on the page reads as its
    child: on a page whose `<head>` carries four `<meta>`, the whole body would.
    """
    parsed = render.parse("<section><img><p>after</p></section>")
    assert [(one.tag, one.parent) for one in parsed.elements] == [
        ("section", -1), ("img", 0), ("p", 0)]


def test_a_self_closed_element_pops_the_element_stack_with_the_other_two():
    """Drop `self._element_stack.pop()` from either pop site and the three stacks drift.

    `_open` and `_tags` have carried this case since `apply-scout`; a third stack is in
    lockstep only if it is popped in the same place, and `unclosed` cannot see the difference
    because it counts `_open`. With the pop missing from `handle_startendtag` the circle reads
    as the rect's child — so a mark's ground would resolve against a shape that never
    contained it, which is the wrong answer given confidently.
    """
    parsed = render.parse("<svg><g><rect/><circle/></g></svg>")
    positions = {one.tag: one for one in parsed.elements}
    assert positions["circle"].parent == positions["g"].index
    assert parsed.unclosed == 0


def test_an_element_that_has_closed_does_not_adopt_what_comes_after_it():
    """The other pop site, and **the six guards above all shipped green over it.**

    Drop `self._element_stack.pop()` from `handle_endtag` and the whole suite stayed green:
    every case above opens its elements before any of them closes, so the stack is never read
    after a pop and the mutation has nowhere to show. A closed element followed by a sibling
    is where the two versions differ — the commonest shape on every page in the corpus, and
    the one no test had. Found by the battery, which is the only way it could have been.
    """
    parsed = render.parse("<div><span>a</span><p>after</p></div>")
    positions = {one.tag: one for one in parsed.elements}
    assert positions["p"].parent == positions["div"].index, (
        "an element that has closed cannot be the parent of the one after it")
    assert parsed.unclosed == 0


def test_the_ancestors_run_nearest_first_and_a_root_element_has_none():
    """Nearest first, because a ground is resolved outwards until one is opaque.

    Reverse the append order and the walk still terminates and still holds the same
    elements — so this asserts the order and not the membership, which is the half a
    `set`-shaped assertion would miss.
    """
    parsed = render.parse('<figure><div class="chart-wrap"><svg><g><rect/></g></svg></div></figure>')
    rect = next(one for one in parsed.elements if one.tag == "rect")
    assert [one.tag for one in parsed.ancestors(rect)] == ["g", "svg", "div", "figure"]
    assert parsed.ancestors(parsed.elements[0]) == []


def test_preceding_siblings_are_the_earlier_elements_under_the_same_parent():
    """Three mutations, and each returns a ground the element is not painted on.

    `elements[:index]` widened to `[:index + 1]` hands an element itself as a candidate
    ground, which scores 1.00:1 and turns every site undecidable. Dropping the `parent`
    filter returns cousins — on `auth-log-scan` that is every shape of the previous chart
    row. And a *later* sibling is painted over this one rather than under it, so the slice
    bound is the direction of the whole question.
    """
    parsed = render.parse(
        "<svg><g><rect/><circle/><text>1</text></g><g><line/></g></svg>")
    elements = {one.tag: one for one in parsed.elements}
    assert [one.tag for one in parsed.preceding_siblings(elements["text"])] == ["rect", "circle"]
    assert parsed.preceding_siblings(elements["rect"]) == []
    assert parsed.preceding_siblings(elements["line"]) == []


def test_a_run_of_marks_are_siblings_of_one_another_and_the_stream_says_so():
    """The shape `0008` §3.11's worked example turns on, reduced to one row.

    Measured on `auth-log-scan` with this stream: **133 of its 139 `.ev-failed` circles have
    a preceding sibling of their own class**, in runs of forty, sixteen and twelve inside a
    `<g class="row">`. The six without one are each first in a run, plus the legend swatch,
    which hangs directly under `svg.chart`. That is a lower bound — same-class is where the
    candidate ratio is a guaranteed 1.00:1 — and it is why §3.11's rule that a site must
    clear *every* preceding sibling cannot stand as written. The structure is pinned here;
    what a verdict does with it is not this module's question.
    """
    parsed = render.parse(
        '<svg class="chart"><g class="row"><rect class="lane"/><rect class="window-band"/>'
        '<circle class="ev-failed"/><circle class="ev-failed"/></g></svg>')
    marks = [one for one in parsed.elements if "ev-failed" in one.classes]
    assert [one.tag for one in parsed.ancestors(marks[0])] == ["g", "svg"]
    assert [one.classes for one in parsed.preceding_siblings(marks[0])] == [
        frozenset({"lane"}), frozenset({"window-band"})], (
        "the first mark of a run has the shapes it is drawn on and no mark before it")
    assert [one.classes for one in parsed.preceding_siblings(marks[1])] == [
        frozenset({"lane"}), frozenset({"window-band"}), frozenset({"ev-failed"})], (
        "every mark after the first has one of its own colour behind it, which is the "
        "1.00:1 candidate that collapses the verdict")
