"""The census — and the four readings its own first output refuted.

Every guard below pins something the module got wrong before the corpus was asked. That is the
argument for `ADR-0008` D2 in one file: each of these would have shipped as a verdict.

The mutation each test is written against is named in its docstring.
"""

from __future__ import annotations

import pytest

from conftest import detail_of, loaded
from tools.pagespec import clauses, colour, contrast, render

PALETTE = ":root { --bg: #ffffff; --surface: #f6f8fa; --accent: #2563eb; --ink: #111111 }"


def _sites(html: str, css: str) -> list[contrast.Site]:
    return contrast.sites(render.parse(html), PALETTE + css)[0]


def _one(html: str, css: str, tag: str, prop: str, *, last: bool = False) -> contrast.Site:
    """The first site of that tag and property, or the last — a run's second member is where a
    preceding sibling of the same colour exists at all, and asking for the first quietly tests
    the case with no siblings. The first version of this file did exactly that."""
    matching = [one for one in _sites(html, css) if one.tag == tag and one.prop == prop]
    return matching[-1] if last else matching[0]


# -- what counts as a site at all -------------------------------------------------------------


def test_a_background_is_a_ground_and_never_a_site():
    """Counting backgrounds as marks put `<code> background 1.06:1` at the head of six
    surfaces — true, and about a code chip sitting on a card, which no success criterion asks
    anything of. Drop `- paint.GROUND` from the sweep and the census's worst figure becomes a
    design choice again."""
    found = _sites('<div class="card"><code class="chip">x</code></div>',
                   ".card { background: var(--surface) } .chip { background: var(--bg) }")
    assert [one.prop for one in found] == [], "a background is measured against, not measured"


def test_text_implies_four_and_a_half_and_a_mark_implies_three():
    """`0007` §5 clause 1's threshold sentence, which is the only judgement this module makes.
    Swap the two and every text site on the corpus is scored against the mark bar."""
    page = ('<div class="lead">x</div>'
            '<svg><rect class="lane" x="0" y="0" width="9" height="9"/>'
            '<circle class="m" cx="4" cy="4" r="1"/></svg>')
    css = ".lead { color: var(--ink) } .lane { fill: var(--bg) } .m { fill: var(--accent) }"
    assert _one(page, css, "div", "color").threshold == contrast.TEXT_THRESHOLD
    assert _one(page, css, "circle", "fill").threshold == contrast.MARK_THRESHOLD


# -- the grounds ------------------------------------------------------------------------------


def test_an_ancestor_is_a_guaranteed_ground_and_a_sibling_is_not():
    """Containment by an ancestor is structural; a sibling's is geometric. Marking both
    `guaranteed` erases the distinction `ADR-0008` D1 turns on, and S14 needs it to tell a
    `FAIL` it can stand behind from one it cannot."""
    site = _one('<div class="card"><svg><rect class="lane" x="0" y="0" width="9" height="9"/>'
                '<circle class="m" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } .lane { fill: var(--surface) } "
                ".m { fill: var(--accent) }", "circle", "fill")
    assert [one.guaranteed for one in site.grounds] == [True, False]


def test_a_sibling_the_geometry_does_not_place_under_the_mark_is_not_a_ground():
    """Take every preceding sibling and `auth-log-scan`'s candidate grounds go from 1 088 back
    to 6 525. The lane here ends at x = 9 and the mark sits at x = 40."""
    site = _one('<div class="card"><svg><rect class="lane" x="0" y="0" width="9" height="9"/>'
                '<circle class="m" cx="40" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } .lane { fill: var(--surface) } "
                ".m { fill: var(--accent) }", "circle", "fill")
    assert [one.guaranteed for one in site.grounds] == [True], "only the ancestor survives"


def test_a_ground_of_the_marks_own_colour_is_counted_and_not_measured():
    """`0008` §3.11's collapse, handled rather than reported as a verdict.

    A ratio of 1.00:1 against a sibling of the same declared colour is true and says nothing;
    reported as a ratio it becomes the worst figure on the page and buries every real one.
    `auth-log-scan` has 133 of 139 marks in this shape. Count it, and let S14 decide.
    """
    site = _one('<div class="card"><svg><circle class="m" cx="4" cy="4" r="4"/>'
                '<circle class="m" cx="5" cy="4" r="4"/></svg></div>',
                ".card { background: var(--bg) } .m { fill: var(--accent) }", "circle", "fill",
                last=True)
    assert site.same_colour == 1
    assert all(one.colour != "#2563eb" for one in site.grounds)


# -- the ground's own alpha, which the first version ignored ------------------------------------


def test_a_translucent_ground_is_composited_over_what_is_behind_it():
    """The defect the corpus found within one run of the census.

    `pl-review-sense` fills every confusion-matrix cell `var(--accent)` and writes
    `fill-opacity` per cell from its data. Reading the declared colour back made each cell full
    `#2563eb`, so every label on one measured 1.00:1 — on the page that carried the live SC
    1.4.3 failure S12 fixed, which is the one place the census could least afford to be blind.
    """
    site = _one('<div class="card"><svg><rect class="cell" x="0" y="0" width="9" height="9" '
                'fill-opacity="0.1"/><circle class="m" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } .cell { fill: var(--accent) } "
                ".m { fill: var(--ink) }", "circle", "fill")
    painted = [one.colour for one in site.grounds if not one.guaranteed]
    # Against `colour.composite` rather than a hex typed here. The first version of this line
    # carried a hand-computed `#e9eefd` and the true value is `#e9effd` — one bit out, in a
    # file whose whole subject is that hand-computed figures are wrong. The claim being pinned
    # is that the cell's alpha was applied over what is behind it, not the arithmetic, which
    # `test_colour` owns.
    assert painted == [colour.composite("#2563eb", "#ffffff", 0.1)], (
        "the cell is 10 % accent over white, not full accent")


def test_a_translucent_ground_with_nothing_opaque_behind_it_is_not_a_ground():
    """Compositing over an assumed white would be a confident wrong colour — the one failure
    this package exists to refuse. With no opaque ancestor the file does not say what the cell
    sits on, so the site falls to `contrast ground`."""
    site = _one('<div><svg><rect class="cell" x="0" y="0" width="9" height="9" '
                'fill-opacity="0.1"/><circle class="m" cx="4" cy="4" r="1"/></svg></div>',
                ".cell { fill: var(--accent) } .m { fill: var(--ink) }", "circle", "fill")
    assert site.grounds == () and site.ratios == ()


# -- what the census refuses to score -----------------------------------------------------------


def test_two_rules_reaching_one_site_leaves_it_unresolved_rather_than_scored():
    """`ADR-0008` D2: no cascade. Scoring the last declaration would be source order, which is
    a cascade rule, and the census would be reporting a colour it chose."""
    site = _one('<div class="card"><svg><circle class="m out" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } .m { fill: var(--accent) } "
                ".out { fill: var(--ink) }", "circle", "fill")
    assert "no cascade" in site.unresolved and site.ratios == ()


def test_the_three_keys_are_emitted_on_every_page_whatever_it_contains():
    """A key that appears only on pages that have sites would make the census's absence
    indistinguishable from a page with nothing to say — and `test_spec`'s corpus guard reads
    the emitted set, so a conditional key would drift out of the registry unnoticed."""
    emitted = [one.clause for one in contrast.census(render.parse("<p>nothing</p>"), "")]
    assert emitted == ["contrast text", "contrast marks", "contrast ground"]


# -- the crash the audit found, and it took the whole table with it --------------------------


@pytest.mark.parametrize("value", [
    "var(--deep)",                    # a chained alias; `0008` S7 migrates exactly this shape
    "rebeccapurple",                  # a named colour
    "rgb(37 99 235)",                 # modern space-separated notation
    "#11111180",                      # eight-digit hex, an alpha this cannot resolve
    "light-dark(#111111, #eeeeee)",   # a function whose answer depends on the scheme
    "oklch(0.5 0.1 250)",             # a colour space `colour.rgb` does not read
])
def test_a_token_that_is_not_a_plain_hex_is_reported_and_does_not_take_the_table_down(value):
    """**`colour.resolve` returns whatever the palette holds, not only a hex.**

    Every value here comes back non-`None` — so nothing marked the site unresolved, it reached
    `colour.composite`, and `ValueError` left `clauses.check`. One token on one page killed the
    whole twelve-surface run. Measured: six of six notations fatal.

    The class was already guarded one module to the left: `test_clauses.py` asserts each of
    these is handled honestly by `clause_1_tokens`, and every one of those tests calls the
    clause directly rather than `check`. The defect moved and the guard did not, which is this
    codebase's characteristic failure and why the assertion below goes through `check`.

    Found by the test audit of 2026-09-09, hours after `paint.py`'s docstring claimed a chained
    token *"would come back unresolved and be reported under `contrast ground`"*. It did not.
    """
    css = (":root { --bg: #ffffff; --deep: #123456; --text: " + value + " } "
           "body { background: var(--bg) } .card { color: var(--text) }")
    findings = clauses.check(loaded(
        "<html><head><title>A claim about the data</title></head><body>"
        '<p class="eyebrow">Data</p><h1>A claim</h1><div class="card">x</div></body></html>',
        css=css))
    assert "1 site(s) without a resolved ground" in detail_of(findings, "contrast ground")


def test_a_site_whose_colour_is_not_a_hex_scores_nothing_rather_than_raising():
    """The same guard at the arithmetic rather than at the report, because a `Site` built any
    other way reaches `ratios` too. `is not None` was the check that let this through."""
    site = contrast.Site(0, "div", "color", "var(--x)", "var(--deep)", 1.0,
                         contrast.TEXT_THRESHOLD, True,
                         (contrast.Ground(1, "#ffffff", True),), 0, 1, "")
    assert site.ratios == ()


# -- D6, a site's own ground and which way a boundary faces -----------------------------------


def test_a_foreground_is_measured_against_the_background_its_own_element_paints():
    """`ADR-0008` D6. The ancestor walk alone measured two published buttons at 1.00:1 and
    1.06:1 against a ground they cover; their real values are 5.17:1, which one of the two
    pages had already written in a comment.

    The mutation: delete the self-ground branch in `_grounds`. The label then reaches the card
    behind the chip and reads 1.00:1 - a number that is arithmetically right and answers the
    wrong question."""
    site = _one('<div class="card"><p class="chip">x</p></div>',
                ".card { background: #ffffff } .chip { background: #111111; color: #ffffff }",
                "p", "color")
    assert [one.colour for one in site.grounds] == ["#111111"]
    assert min(site.ratios) > 4.5


def test_the_own_ground_stops_the_walk_rather_than_joining_it():
    """D6 says *occludes*, and the word is the decision. Appending the own background as one
    more candidate leaves the ancestor in `grounds` too, and `_measured` takes the `min()` -
    so the covered ground still supplies the worst reading and the text half never goes clean.
    Measured over the eleven: occluding leaves 0 text failures, appending leaves 2.

    The mutation: `found.append(...)` instead of the early `return`."""
    site = _one('<div class="card"><p class="chip">x</p></div>',
                ".card { background: #ffffff } .chip { background: #111111; color: #ffffff }",
                "p", "color")
    assert len(site.grounds) == 1, (
        "the element's own background is a stop, not a candidate: with the ancestor still in "
        "the list the min() reading is against a ground the element covers")


def test_a_site_is_never_its_own_ground_through_fill():
    """D6's first bound, found by getting it wrong: reading self-as-ground through
    `_GROUND_PROPERTIES` - which holds `fill` - makes every SVG `<text>` its own ground,
    because there one property is a shape's paint *and* a text's foreground. That reading
    reported 684 failures, all 1.00:1, every one the question *does this thing contrast with
    itself*.

    The mutation: add `fill` to `_OWN_GROUND_PROPERTIES`."""
    site = _one('<div class="card"><span class="lbl">x</span></div>',
                ".card { background: #111111 } .lbl { color: #ffffff; fill: #ffffff }",
                "span", "color")
    assert [one.colour for one in site.grounds] == ["#111111"]
    assert min(site.ratios) > 4.5


def test_a_border_keeps_the_ground_behind_it_because_a_boundary_faces_outward():
    """D6's second bound. A border's visibility comes from the colour on the *other* side of
    it, so it keeps the ancestor ground. Correcting `mini-traceroute`'s `<button>` border to
    the button's own fill gives 1.00:1 - the wrong comparison, confidently computed.

    The mutation: widen the self-ground branch past `paint.TEXT`."""
    site = _one('<div class="card"><button class="btn">x</button></div>',
                ".card { background: #ffffff } "
                ".btn { background: #2563eb; border: 1px solid #2563eb }",
                "button", "border")
    assert [one.colour for one in site.grounds] == ["#ffffff"]


# -- D5, what the marks key is owed by --------------------------------------------------------


def test_a_structural_border_carries_no_obligation():
    """`ADR-0008` D5. SC 1.4.11 asks 3:1 of user-interface components and of graphics required
    to understand the content. A hairline between two rows of a table whose data is entirely
    text is neither, and `--border` on white measures 1.17:1 - required to measure nothing.
    Without D5 the marks key fails 1 195 of 1 785 sites and is not a strict clause but a
    broken one.

    The mutation: make `_obligated` true for any border."""
    site = _one('<div class="card"><p class="row">x</p></div>',
                ".card { background: #ffffff } .row { border-bottom: 1px solid #e3e7ee }",
                "p", "border-bottom")
    assert site.obligated is False
    assert min(site.ratios) < 3.0, "the fixture is only meaningful while this border fails"


def test_a_border_in_the_control_role_does_carry_one():
    """The exception that is not a property name, and the whole reason D7 gave the control
    role a token: a user-interface component boundary is inside D5 by any reading, and the
    checker recognises it by the role its declaration names.

    The mutation: drop the `_CONTROL_ROLE` clause from `_obligated`."""
    site = _one('<div class="card"><input class="ctl"></div>',
                ":root { --border-control: #808a9c } .card { background: #ffffff } "
                ".ctl { border: 1px solid var(--border-control) }",
                "input", "border")
    assert site.obligated is True


def test_svg_paint_carries_the_obligation_and_is_what_the_marks_key_is_over():
    """The included half of D5's partition, and the population that keeps the marks key out of
    `GATE`: 153 SVG sites still measure below 3.0:1."""
    site = _one('<div class="card"><svg><circle class="mark" r="1"></circle></svg></div>',
                ".card { background: #ffffff } .mark { fill: #f2f2f2 }",
                "circle", "fill")
    assert site.obligated is True
    assert min(site.ratios) < 3.0


# -- the verdicts themselves ------------------------------------------------------------------


def test_a_population_with_nothing_measurable_is_undecided_and_not_a_pass():
    """A page must not go clean on the strength of the checker's own blindness. `0008` §3.11's
    collapse is 133 of 139 marks on one surface; scoring an unmeasured site as a pass would
    have called that surface clean for exactly the reason it could not be read.

    The mutation: `return PASS` when `measured` is empty."""
    unmeasured = contrast.Site(0, "circle", "fill", "var(--x)", None, 1.0,
                               contrast.MARK_THRESHOLD, True, (), 0, 1, "unreadable")
    assert contrast._verdict([unmeasured]) == clauses.UNDECIDED


def test_one_site_below_its_threshold_fails_the_whole_key():
    """A key is a claim about the page, not about its best element.

    The mutation: `all(...)` for `any(...)`, or a threshold comparison the wrong way round."""
    ground = (contrast.Ground(1, "#ffffff", True),)
    good = contrast.Site(0, "p", "color", "x", "#111111", 1.0, contrast.TEXT_THRESHOLD, True,
                         ground, 0, 1, "")
    bad = contrast.Site(2, "p", "color", "x", "#f2f2f2", 1.0, contrast.TEXT_THRESHOLD, True,
                        ground, 0, 1, "")
    assert contrast._verdict([good]) == clauses.PASS
    assert contrast._verdict([good, bad]) == clauses.FAIL
