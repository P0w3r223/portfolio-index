"""Which elements a rule reaches — and the refusals, which are half of what this module is.

The corpus decided this module's scope rather than CSS did: 373 paint-carrying selectors over
the eleven committed surfaces, 347 of them answerable, and the 26 refusals split into a state
the document is not in (22, all `:focus-visible`) and a shape this does not parse (4). The
tests below use the corpus's own selectors wherever one makes the point, because a synthetic
`.a .b` proves the mechanism and not the coverage.

The mutation each test is written against is named in its docstring.
"""

from __future__ import annotations

from tools.pagespec import render, selector as sel


def _parsed(text: str) -> sel.Selector:
    parsed = sel.parse(text)
    assert isinstance(parsed, sel.Selector), f"{text!r} was refused: {parsed}"
    return parsed


# -- what it reaches -----------------------------------------------------------------------


def test_a_compound_requires_every_class_it_names_and_not_merely_one():
    """`step.classes <= element.classes` mutated to `&` — any instead of all.

    `.diagram .node.active` and `.diagram .node.silent` paint different colours onto the same
    element type on `mini-traceroute`. Under an any-of reading a plain `.node` matches both
    and the census reports two grounds for a shape that has one.
    """
    page = render.parse('<div class="diagram"><circle class="node active"/>'
                        '<circle class="node"/></div>')
    reached = sel.reaches(page, _parsed(".diagram .node.active"))
    assert [one.classes for one in reached] == [frozenset({"node", "active"})]


def test_a_tag_led_compound_requires_the_tag():
    """Drop the tag comparison in `_step_matches` and `tbody tr.flagged td.ip` — a real
    selector on `auth-log-scan` — reaches every `.ip` in the document, including the four in
    the table head that the rule does not paint."""
    page = render.parse('<table><tbody><tr class="flagged"><td class="ip">a</td>'
                        '<th class="ip">b</th></tr></tbody></table>')
    reached = sel.reaches(page, _parsed("tbody tr.flagged td.ip"))
    assert [one.tag for one in reached] == ["td"]


def test_a_descendant_chain_is_matched_against_ancestors_in_order():
    """The mutation that matters, and the one a left-to-right walk gets wrong.

    Here the `.row` encloses the `.chart`, not the other way round. `.chart .row .cell` must
    not reach the cell: its ancestors hold both classes, but not in the order the selector
    demands. Replace the ordered walk in `matches` with a subset test over all ancestor
    classes and this passes — and `auth-log-scan` has exactly this shape inverted, where the
    answer must be yes.
    """
    inverted = render.parse('<div class="row"><div class="chart">'
                            '<span class="cell">x</span></div></div>')
    assert sel.reaches(inverted, _parsed(".chart .row .cell")) == []
    upright = render.parse('<div class="chart"><div class="row">'
                           '<span class="cell">x</span></div></div>')
    assert len(sel.reaches(upright, _parsed(".chart .row .cell"))) == 1


def test_a_descendant_need_not_be_a_child():
    """`.chart .row.flagged .window-band` reaches a band nested three levels down on
    `auth-log-scan`. Requiring adjacency would answer `0` where the page paints four."""
    page = render.parse('<svg class="chart"><g class="row flagged"><g><g>'
                        '<rect class="window-band"/></g></g></g></svg>')
    assert len(sel.reaches(page, _parsed(".chart .row.flagged .window-band"))) == 1


def test_the_same_selector_reaches_elements_with_different_grounds():
    """§3.11's finding, as an assertion rather than as prose.

    Measured on `auth-log-scan`: `.ev-failed` reaches 139 circles and `.chart .ev-failed`
    reaches 138. The one it misses is the legend swatch, an `<svg>` inside `<ul class="legend">`
    with no `chart` class — a different ground for the same declared colour, which is why a
    check keyed on the rule instead of the element is wrong about one of them.
    """
    page = render.parse('<svg class="chart"><circle class="ev-failed"/></svg>'
                        '<ul class="legend"><li><svg><circle class="ev-failed"/></svg></li></ul>')
    assert len(sel.reaches(page, _parsed(".ev-failed"))) == 2
    assert len(sel.reaches(page, _parsed(".chart .ev-failed"))) == 1


def test_what_it_reaches_comes_back_in_document_order():
    """`reaches` walks `page.elements`, which is document order by construction. A set
    comprehension here would lose the order that decides which sibling precedes which."""
    page = render.parse('<div class="c"><i class="m">1</i><b class="m">2</b></div>')
    assert [one.tag for one in sel.reaches(page, _parsed(".c .m"))] == ["i", "b"]


# -- specificity, computed and applied to nothing ------------------------------------------


def test_specificity_counts_classes_and_types_and_this_module_applies_it_to_neither():
    """`ADR-0008` D2: the census prints it so the corpus can say how often two rules reach one
    element. Nothing here sorts by it — a cascade is S14, and asserting the number now is what
    makes that a decision rather than a drift."""
    assert _parsed(".chart .row.flagged .window-band").specificity == (0, 4, 0)
    assert _parsed("tbody tr.flagged td.ip").specificity == (0, 2, 3)
    assert _parsed(".ledger thead th").specificity == (0, 1, 2)


# -- the refusals, which are the other half ------------------------------------------------


def test_a_pseudo_class_is_refused_as_a_state_and_not_as_a_bad_shape():
    """The distinction is 22 of the corpus's 26 refusals and it is not cosmetic.

    A shape refusal is a gap this parser could close; a state refusal is a fact about static
    reading that no parser closes. Collapse the two into one kind and the census reports a
    permanent limit as outstanding work.
    """
    for text in ("a:focus-visible", "summary:focus-visible", "input:focus-visible"):
        refused = sel.parse(text)
        assert isinstance(refused, sel.Refusal)
        assert refused.kind == sel.STATE, f"{text} is a state, not a shape"


def test_every_shape_the_corpus_writes_and_this_does_not_parse_is_refused_by_name():
    """Each of these is a real selector from the eleven surfaces, or a shape the corpus does
    not write at all. Delete any branch and `parse` falls through to the compound reader,
    which would silently drop the part it cannot read: `.field input[type="number"]` would
    become `.field input` and match every input on the page."""
    for text, fragment in (('.field input[type="number"]', "attribute"),
                           (".chart .range.muted ~ .range-dot", "general-sibling"),
                           ("#diagram .node", "id"),
                           ("* .node", "universal"),
                           (".card > .kpi", "child"),
                           (".kpi + .kpi", "adjacent"),
                           (".card::before", "pseudo-element")):
        refused = sel.parse(text)
        assert isinstance(refused, sel.Refusal), f"{text} must be refused"
        assert refused.kind == sel.SHAPE
        assert fragment in refused.detail, f"{text}: {refused.detail!r} does not name it"


def test_a_selector_list_is_refused_by_name_and_not_merely_by_accident():
    """`rules()` hands back the selector text verbatim, commas and all.

    **This asserts the detail, because the verdict alone cannot see the branch.** Delete the
    comma check and all four of these are still refused — the compound reader rejects `card,`
    as a class and `div,` as a type — so a test asserting only `SHAPE` would pass over a
    deleted branch. What the branch buys is the printed reason, and the census prints it.
    """
    for text in (".card, .kpi", ".card,.kpi", "div, span", ".a , .b"):
        refused = sel.parse(text)
        assert isinstance(refused, sel.Refusal) and refused.kind == sel.SHAPE
        assert "selector list" in refused.detail, (
            f"{text!r} was refused as {refused.detail!r}, which does not tell the reader that "
            f"the caller was supposed to split it")


def test_an_unreadable_token_is_refused_rather_than_dropped():
    """The general case behind the branch list: anything the compound reader cannot validate
    stops the parse. A `continue` here instead of a return is the silent-widening failure
    `0008` §4.11 forbids — the selector would match on the tokens that happened to parse."""
    for text in (".1bad", "9tag .node", ".."):
        assert isinstance(sel.parse(text), sel.Refusal), f"{text} must be refused"
