"""What an element is painted with — every candidate, and the alphas that reach the pixel.

`ADR-0008` D2: no cascade here. These guards pin that as a decision rather than an omission —
`candidates` returns competing declarations and `opacity` refuses to choose between two.

The mutation each test is written against is named in its docstring.
"""

from __future__ import annotations

from tools.pagespec import paint, render

PALETTE = {"accent": "#2563eb", "bg": "#ffffff", "danger": "#f87171"}


def _page_and_rules(html: str, css: str):
    return render.parse(html), paint.read_rules(css)[0]


# -- which rules reach an element ------------------------------------------------------------


def test_every_rule_that_reaches_an_element_comes_back_and_none_of_them_wins():
    """The decision `ADR-0008` D2 takes, asserted so a later cascade is a change and not a
    drift. `.diagram .node` and `.diagram .node.active` both reach an active node on
    `mini-traceroute`; returning one would make the census silent about the other."""
    page, rules = _page_and_rules(
        '<div class="diagram"><circle class="node active"/></div>',
        ".diagram .node { fill: var(--bg) } .diagram .node.active { fill: var(--accent) }")
    node = next(one for one in page.elements if "node" in one.classes)
    found = paint.candidates(page, node, "fill", rules, PALETTE)
    assert [one.colour for one in found] == ["#ffffff", "#2563eb"]
    assert [one.specificity for one in found] == [(0, 2, 0), (0, 3, 0)]


def test_a_property_the_corpus_writes_only_as_a_shorthand_is_still_read():
    """`background-color` appears **nowhere** in the eleven surfaces — every ground is the
    `background` shorthand. Drop the shorthand from `PAINT` and 63 sites vanish silently."""
    page, rules = _page_and_rules('<div class="card">x</div>',
                                  ".card { background: var(--bg) }")
    card = next(one for one in page.elements if "card" in one.classes)
    assert [one.colour for one in paint.candidates(page, card, "background", rules, PALETTE)] == ["#ffffff"]


def test_a_declaration_whose_colour_cannot_be_read_still_comes_back_as_a_site():
    """Dropping it would make the census silent about a painted element rather than honest
    about it. `colour.resolve` returns `None` for a gradient; the candidate survives with
    `colour is None` so the site is reported and not lost."""
    page, rules = _page_and_rules('<div class="hero">x</div>',
                                  ".hero { background: linear-gradient(#fff, #000) }")
    hero = next(one for one in page.elements if "hero" in one.classes)
    found = paint.candidates(page, hero, "background", rules, PALETTE)
    assert len(found) == 1 and found[0].colour is None and found[0].declared.startswith("linear-gradient")


# -- inheritance ------------------------------------------------------------------------------


def test_fill_is_taken_from_the_nearest_ancestor_that_declares_it_and_says_which():
    """SVG paint inherits. Without the walk, a `<text>` inside a `<g class="row">` that sets
    `fill` reports no colour at all and lands under `contrast ground` — an unknown invented by
    the checker rather than found on the page."""
    page, rules = _page_and_rules(
        '<svg class="chart"><g class="row"><text x="1" y="2">n</text></g></svg>',
        ".chart .row { fill: var(--accent) }")
    label = next(one for one in page.elements if one.tag == "text")
    row = next(one for one in page.elements if "row" in one.classes)
    found = paint.candidates(page, label, "fill", rules, PALETTE)
    assert [(one.colour, one.inherited_from) for one in found] == [("#2563eb", row.index)]


def test_a_background_is_not_inherited_because_css_does_not_inherit_it():
    """Put `background` in `INHERITED` and every element reports the nearest painted ground as
    its own, so a mark on a card would be measured against the card twice and never against
    what is actually behind it."""
    page, rules = _page_and_rules('<div class="card"><span class="kpi">1</span></div>',
                                  ".card { background: var(--bg) }")
    kpi = next(one for one in page.elements if "kpi" in one.classes)
    assert paint.candidates(page, kpi, "background", rules, PALETTE) == []


def test_a_direct_declaration_stops_the_walk_upwards():
    """Return both and an element that overrides its parent reports the parent's colour as a
    live candidate for itself, which is the confident wrong ground again."""
    page, rules = _page_and_rules(
        '<svg class="chart"><g class="row"><circle class="m"/></g></svg>',
        ".chart .row { fill: var(--accent) } .m { fill: var(--danger) }")
    mark = next(one for one in page.elements if "m" in one.classes)
    found = paint.candidates(page, mark, "fill", rules, PALETTE)
    assert [(one.colour, one.inherited_from) for one in found] == [("#f87171", None)]


# -- the three routes an alpha takes ----------------------------------------------------------


def test_a_presentation_attribute_and_a_rule_multiply_rather_than_replace():
    """`pl-review-sense` writes `fill-opacity` per cell from its data; a rule setting
    `opacity` on the same element applies over it. Returning whichever is smaller, or the last
    seen, reports the cell as more legible than the page paints it."""
    page, rules = _page_and_rules('<svg><rect class="cell" fill-opacity="0.5"/></svg>',
                                  ".cell { opacity: 0.5 }")
    cell = next(one for one in page.elements if "cell" in one.classes)
    assert paint.opacity(page, cell, "fill", rules) == 0.25


def test_an_alpha_applies_to_its_own_property_and_opacity_applies_to_everything():
    """`stroke-opacity` must not dim a fill. Keying both to one attribute name would make a
    dashed outline's alpha decide the contrast of the shape's interior."""
    page, rules = _page_and_rules('<svg><rect class="c" stroke-opacity="0.2"/></svg>', "")
    cell = next(one for one in page.elements if "c" in one.classes)
    assert paint.opacity(page, cell, "stroke", rules) == 0.2
    assert paint.opacity(page, cell, "fill", rules) == 1.0


def test_two_rules_declaring_one_alpha_is_undecidable_and_not_a_product():
    """Measured: **four elements on `auth-log-scan`**, both rules declaring `opacity`.

    Multiplying them gives a number no browser paints; picking one is a cascade, which the
    census does not have. `None` hands the site to `contrast ground`. Replace the length check
    with a product and this passes while the checker invents an alpha.
    """
    page, rules = _page_and_rules('<svg><rect class="ev out"/></svg>',
                                  ".ev { opacity: 0.85 } .out { opacity: 0.32 }")
    mark = next(one for one in page.elements if "ev" in one.classes)
    assert paint.opacity(page, mark, "fill", rules) is None


def test_an_alpha_this_cannot_read_is_not_an_alpha_of_one():
    """Skipping an unparseable value claims the element is opaque. `calc()` paints something,
    and `None` says the file did not tell us what."""
    page, rules = _page_and_rules('<svg><rect class="c"/></svg>', ".c { opacity: calc(1 - 0.2) }")
    mark = next(one for one in page.elements if "c" in one.classes)
    assert paint.opacity(page, mark, "fill", rules) is None


def test_a_declarations_own_alpha_is_its_mix_and_not_the_elements_opacity():
    """The bug this guard was written after finding: folding the element's `opacity` into each
    candidate applies the markup's attribute once per rule that reaches the element, so two
    rules squared it. Two functions, two questions."""
    page, rules = _page_and_rules('<svg><rect class="c" fill-opacity="0.5"/></svg>',
                                  ".c { fill: color-mix(in srgb, var(--accent) 25%, transparent) }")
    mark = next(one for one in page.elements if "c" in one.classes)
    only = paint.candidates(page, mark, "fill", rules, PALETTE)[0]
    assert only.alpha == 0.25, "the candidate carries the mix, not the element's attribute"
    assert paint.opacity(page, mark, "fill", rules) == 0.5


# -- the refusals come back as a row of their own ---------------------------------------------


def test_a_refused_selector_is_returned_and_not_dropped():
    """A reader seeing only matched rules cannot tell a page with no focus ring from one whose
    focus ring this cannot judge. 22 of the corpus's 26 refusals are exactly that."""
    matched, refused = paint.read_rules(
        ".card { color: var(--accent) } a:focus-visible { outline: 2px solid var(--accent) }")
    assert [one.selector.text for one in matched] == [".card"]
    assert [(one.text, one.kind) for one in refused] == [("a:focus-visible", "state")]


def test_a_value_holding_a_colon_survives_being_split_into_declarations():
    """Splitting the body by a regex over `name: value` would cut
    `background: url(data:image/svg+xml,...)` at the inner colon and read the property as
    `url(data`. Split on `;` and partition once."""
    matched, _ = paint.read_rules('.i { background: url(data:image/svg+xml,<svg/>); color: #fff }')
    assert matched[0].declarations["background"].startswith("url(data:image")
    assert matched[0].declarations["color"] == "#fff"
