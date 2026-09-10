"""The census — and the four readings its own first output refuted.

Every guard below pins something the module got wrong before the corpus was asked. That is the
argument for `ADR-0008` D2 in one file: each of these would have shipped as a verdict.

The mutation each test is written against is named in its docstring.
"""

from __future__ import annotations

from pathlib import Path

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
    `guaranteed` erases the distinction, and dropping the geometric one erases the ground.

    *This docstring said S14 needs the field "to tell a `FAIL` it can stand behind from one it
    cannot". **`ADR-0008` D8 answered that it does not** — measured, the guaranteed ground is
    never the binding one, and both failures with a history are read on a geometric ground. The
    field's job is the detail line a reader acts on, not the verdict. The guard stays and its
    reason changed, which is the erratum this repository records rather than quietly fixes.*"""
    site = _one('<div class="card"><svg><rect class="lane" x="0" y="0" width="9" height="9"/>'
                '<circle class="m" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } .lane { fill: var(--surface) } "
                ".m { fill: var(--accent) }", "circle", "fill")
    assert [one.guaranteed for one in site.grounds] == [True, False]


# -- ADR-0008 §10: the role is in the token ---------------------------------------------------


def test_a_mark_declaring_a_structure_role_is_owed_nothing():
    """§10's subject. A gridline is `0007` §5 clause 1's *"line under a heading"* drawn in an
    SVG coordinate system, and D5's property-name axis could not see that: `fill` and `stroke`
    paint a gridline and a data mark with one word. Delete the structure test and this stroke
    is obliged again, which is 48 of the 65 sites §10 measured."""
    site = _one('<div class="card"><svg><line class="grid" x1="0" y1="4" x2="9" y2="4"/></svg>'
                '</div>',
                ".card { background: var(--bg) } .grid { stroke: var(--border) }",
                "line", "stroke")

    assert not site.obligated


def test_a_background_drawn_in_svg_is_exempt_by_role_where_the_html_one_is_exempt_by_property():
    """`contrast.sites` already refuses this role — *"A background is a ground and not a site"* —
    and its refusal is keyed on the property name, so it reaches `background` and cannot reach
    `fill: var(--surface)`. The rule and the blind spot were adjacent lines. Drop `surface` from
    `STRUCTURE_ROLES` and `auth-log-scan`'s eight swimlane rows are marks again."""
    site = _one('<div class="card"><svg><rect class="lane" x="0" y="0" width="9" height="9"/>'
                '</svg></div>',
                ".card { background: var(--bg) } .lane { fill: var(--surface) }",
                "rect", "fill")

    assert not site.obligated


def test_a_wash_naming_a_semantic_token_is_still_owed_its_ratio():
    """The exemption is by **role**, not by faintness. A wash painted from a semantic token
    stays obliged however low its alpha, which is what leaves `0008` §4.29's three sites exactly
    where that section left them. Widen `STRUCTURE_ROLES` by one semantic role and they go."""
    site = _one('<div class="card"><svg><rect class="band" x="0" y="0" width="9" height="9"/>'
                '</svg></div>',
                ".card { background: var(--bg) } "
                ".band { fill: var(--accent); opacity: 0.16 }",
                "rect", "fill")

    assert site.obligated


def test_a_declaration_naming_a_structure_role_and_a_semantic_one_is_still_owed_its_ratio():
    """`named <= STRUCTURE_ROLES`, not `named & STRUCTURE_ROLES`, and **the corpus cannot redden
    this**: no committed surface mixes the two in one `fill`. `color-mix()` is live in the
    ground and border families, so the notation is not hypothetical — it is one page away.
    Synthetic by necessity, on the precedent of the property-conjunct guard above.

    **The structure role is written first on purpose.** With `--accent` first, a `roles_named`
    truncated to its first reference still obliges this site and the guard stays green over a
    scan that had stopped being exhaustive — measured, uncaught, by the review of §10. Ordered
    this way the one fixture reddens both the `&`-for-`<=` mutation and the truncated scan."""
    site = _one('<div class="card"><svg><rect class="mix" x="0" y="0" width="9" height="9"/>'
                '</svg></div>',
                ".card { background: var(--bg) } "
                ".mix { fill: color-mix(in srgb, var(--surface) 70%, var(--accent) 30%) }",
                "rect", "fill")

    assert site.obligated


def test_svg_text_is_never_exempted_by_the_token_that_paints_it():
    """The bound that makes including `--bg` safe. `mini-traceroute` carries
    `.probe-ttl { fill: var(--bg); font-size: 9px; font-weight: 700 }` and `it-job-radar`
    `.series-dot.observed { fill: var(--bg) }`; `--bg` shows zero measured sites today and that
    zero is the checker's blindness, not the corpus's — a cascade turns them on. Drop
    `_TEXT_TAGS` and the partition goes blind on SVG labels at the stage that makes them
    visible, which is where the only live failure this system has caught actually lived."""
    page = ('<div class="card"><svg><text class="ttl" x="4" y="4">7'
            '<tspan class="unit" x="6" y="4">ms</tspan></text></svg></div>')
    css = ".card { background: var(--bg) } .ttl, .unit { fill: var(--bg) }"

    assert _one(page, css, "text", "fill").obligated
    assert _one(page, css, "tspan", "fill").obligated, (
        "`tspan` is half of `_TEXT_TAGS` and the first version of this guard pinned only "
        "`text`, so dropping it from the set went uncaught"
    )


def test_a_knockout_marker_is_exempt_and_its_ring_is_what_stays_obliged():
    """The one non-text `--bg` mark the corpus holds, pinned so the next partition change has
    to answer it rather than inherit it.

    `it-job-radar`'s `.chart .series-dot.observed { fill: var(--bg); stroke: var(--accent) }`
    is three live sites, and `ADR-0008` §10's `<text>` bound **cannot reach them** — they are
    circles. They were obliged under D5's property-name partition and are exempt under §10's,
    and the review of §10 found the record citing them as evidence for a bound that does not
    apply to them.

    **Exempt is the reading, and the ring is why.** A knockout fill is the absence of the
    series colour; what identifies an observed point against a projected one is the
    `--accent` ring, which names a semantic role, stays obliged, and passes. The fill carries
    no information the ring does not. *That argument is `0008` §4.29's shape two — role
    sitting on a sibling declaration — which §10 says is closed by coincidence rather than by
    rule. Here the coincidence is stated as the decision instead of inherited as one.*"""
    page = ('<div class="card"><svg>'
            '<circle class="series-dot observed" cx="4" cy="4" r="2"/></svg></div>')
    css = (".card { background: var(--bg) } "
           ".series-dot.observed { fill: var(--bg); stroke: var(--accent) }")

    assert not _one(page, css, "circle", "fill").obligated
    assert _one(page, css, "circle", "stroke").obligated, (
        "the ring is what carries the marker's identity; if it stops being obliged the "
        "exemption above loses its whole argument"
    )


def test_a_controls_own_paint_is_owed_its_ratio_even_though_no_border_declares_it():
    """The half D5 had backwards. `accent-color` is the visible part of a range slider and a
    checkbox — a user-interface component by any reading — and the property-name partition
    excluded it while admitting gridlines. Three live sites, all at 4.85:1, so nothing was
    hidden; the classification was inverted. Drop `_CONTROL_PROPERTIES` and it inverts again."""
    site = _one('<div class="card"><input class="slider" type="range"></div>',
                ".card { background: var(--bg) } .slider { accent-color: var(--accent) }",
                "input", "accent-color")

    assert site.obligated


def test_a_mark_naming_no_role_at_all_is_owed_its_ratio():
    """`named and …`. A literal hex or `currentColor` names no role, and the instrument cannot
    read a role it was never given — so it obliges, which is the direction that gets found.
    Invert the default and every un-tokenised mark in the portfolio goes quiet at once."""
    site = _one('<div class="card"><svg><circle class="dot" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } .dot { fill: #f2f4f7 }",
                "circle", "fill")

    assert site.obligated


def test_the_role_vocabulary_has_one_spelling():
    """`contrast.py` carried `_CONTROL_ROLE = "--border-control"` and `clauses.py` carried
    `"border-control"` inside `_BORDER_ROLES`, one fact typed twice with different affixes and
    tied by nothing — `0009` N1's shape, which is why `GATED` is derived from `GATE`.

    *This docstring said "re-type either literal and this reddens", and the review of §10
    measured three mutations that say otherwise: re-typing the literal in `contrast.py`, or
    in `_BORDER_ROLES`, left the whole suite green, because every assertion here read only
    `clauses` constants and `CONTROL_ROLE in _BORDER_ROLES` is a tautology while that set is
    built from the constant. The claim is now carried by a **static read of `contrast.py`'s
    own source**, which is the technique this file already used to prove the module had no
    verdict branch — the one shape a constant cannot pin from the inside.*

    The containments are the pins that keep the sets meaning what their names say: a structure
    role must be a colour role clause 1 knows, and the control role must never drift into the
    set that exempts."""
    source = (Path(contrast.__file__)).read_text(encoding="utf-8")

    assert clauses.STRUCTURE_ROLES <= set(clauses.COLOUR_ROLES)
    assert clauses.CONTROL_ROLE not in clauses.STRUCTURE_ROLES
    quoted = [clauses.CONTROL_ROLE + mark for mark in ("'", '"')]

    assert not any(one in source for one in quoted), (
        "`contrast.py` names the control role again as a string literal. It reads it from "
        "`clauses.CONTROL_ROLE`; a second spelling is what this guard exists to refuse. "
        "*Matched on the name followed by a closing quote, so both the bare and the "
        "`--`-prefixed literal are caught and the prose mention in `_obligated`'s docstring "
        "— `var(--border-control)`, followed by a bracket — is not. The first version "
        "forbade the substring outright and reddened on that documentation.*"
    )


def test_the_structure_exemption_reaches_the_run_and_not_only_the_predicate():
    """§10's one unverifiable direction, and the whole mitigation for it.

    `clause_1_usage` applies the role rule to the ground and border families and deliberately
    not to `fill`/`stroke`, so a data mark painted `var(--border)` is exempted with nothing
    objecting. Nothing *can* object — so the population is printed, and a reader who sees it
    move is seeing the only signal there is. Stop computing it and the exemption becomes
    invisible, which is the shape the guard two above this one was written for."""
    page = ('<div class="card"><svg>'
            '<line class="grid" x1="0" y1="4" x2="9" y2="4"/>'
            '<circle class="dot" cx="4" cy="4" r="1"/></svg></div>')
    css = (".card { background: var(--bg) } .grid { stroke: var(--border) } "
           ".dot { fill: #f2f4f7 }")
    detail = detail_of(contrast.census(render.parse(page), PALETTE + css), "contrast marks")

    assert "1 of them structure paint" in detail, detail


def test_a_ground_painted_by_the_same_declaration_is_not_measured_even_when_the_alphas_differ():
    """`ADR-0008` D8. Revert `_the_same_mark` to resolved-colour equality and this site picks
    up a ~1.26:1 ground that is another instance of itself.

    Two `.ev` circles, one declaration, `fill-opacity` written per element the way
    `auth-log-scan` writes it from the data. The colours differ because the alphas do, which is
    exactly why comparing composited colours missed 65 sites and 966 (site, ground) pairs."""
    site = _one('<div class="card"><svg>'
                '<circle class="ev" cx="4" cy="4" r="3" fill-opacity="0.3"/>'
                '<circle class="ev" cx="4" cy="4" r="1" fill-opacity="0.85"/></svg></div>',
                ".card { background: var(--bg) } .ev { fill: var(--accent) }",
                "circle", "fill", last=True)

    assert [one.guaranteed for one in site.grounds] == [True]
    assert site.same_colour == 1


def test_an_excluded_same_mark_ground_is_counted_and_not_dropped():
    """The difference between an exclusion and a disappearance. Drop the `same += 1` and the
    ground vanishes from `contrast ground`'s census while the site still reports clean, which
    is a checker quietly narrowing its own subject — `0009` §3.2's shape."""
    site = _one('<div class="card"><svg>'
                '<circle class="ev" cx="4" cy="4" r="3" fill-opacity="0.3"/>'
                '<circle class="ev" cx="4" cy="4" r="1" fill-opacity="0.85"/></svg></div>',
                ".card { background: var(--bg) } .ev { fill: var(--accent) }",
                "circle", "fill", last=True)

    assert site.same_colour == 1


def test_the_exclusion_reaches_the_run_and_not_only_the_dataclass():
    """The half `same_colour` alone cannot promise: that a reader ever sees the exclusion.

    `_unresolved` summed `same_colour` over the **blind** sites, and by D8's own structural
    argument an excluded site is never blind — it keeps its ancestor ground. So 966 pairs left
    the verdict with no line anywhere in a full run while three documents said they were
    printed. The guard beside this one asserts `Site.same_colour`, a field no reader sees, and
    stayed green over exactly that. Sum `blind` again and this reddens; that is the mutation.

    Asserted on the rendered detail rather than on the object, because the defect was the gap
    between the two."""
    page = ('<div class="card"><svg>'
            '<circle class="ev" cx="4" cy="4" r="3" fill-opacity="0.3"/>'
            '<circle class="ev" cx="4" cy="4" r="1" fill-opacity="0.85"/></svg></div>')
    css = ".card { background: var(--bg) } .ev { fill: var(--accent) }"
    detail = detail_of(contrast.census(render.parse(page), PALETTE + css), "contrast ground")

    assert "excluded as the same mark" in detail, (
        f"the exclusion is invisible to a reader of the run: {detail!r}"
    )


def test_the_marks_row_says_how_many_are_below_their_threshold():
    """The figure the `contrast marks` GATE row points at, and the reason it can.

    That row used to carry a hand-typed `153`. Removing it was right and left a reader with
    neither the count nor a way to get it, on the one key whose whole reason for being
    report-only *is* that count. `_measured` prints it now. Drop the `below` clause and the
    row's claim that the run prints it goes back to being false.

    Two, and they are the two circles. *The first version of this fixture got its second
    failure from the lane, which is a `fill` and was therefore a mark itself. `ADR-0008` §10
    exempts it — the lane declares `--surface`, a structure role — so the count dropped to one
    and this guard went red on the day the partition changed. That is the guard working: it is
    over the printed count, and the count moved. The second circle restores the population
    without restoring the assumption.*"""
    page = ('<div class="card"><svg>'
            '<rect class="lane" x="0" y="0" width="9" height="9"/>'
            '<circle class="m" cx="4" cy="4" r="1"/>'
            '<circle class="n" cx="6" cy="6" r="1"/></svg></div>')
    css = (".card { background: var(--bg) } .lane { fill: var(--surface) } "
           ".m { fill: #f2f4f7 } .n { fill: #f2f4f7 }")
    detail = detail_of(contrast.census(render.parse(page), PALETTE + css), "contrast marks")

    assert "2 below" in detail, detail


def test_the_same_declared_value_on_a_different_property_is_not_the_same_mark():
    """The `prop ==` half of `_the_same_mark`, which the corpus cannot redden.

    Drop that conjunct and every test stayed green — the review that found it measured the
    corpus too, and **zero pairs are kept only by it**, so no run could have caught it either.
    That is the `0008` shape counted seven times: a guard positioned where it cannot see its
    own subject. It needs a synthetic fixture and this is it.

    A mark and the box it sits in may name one token. `fill: var(--accent)` on a graphic and
    `background: var(--accent)` on the thing under it are not two instances of one mark — the
    property is what makes one a graphic and the other the furniture it is drawn on.

    The alphas differ on purpose: with both opaque the two resolve to one colour and the
    older equality branch excludes the ground before the property is ever consulted, so a
    fixture without it proves nothing about this conjunct. The first version of this test was
    exactly that fixture and went red saying so."""
    site = _one('<div class="card"><svg>'
                '<rect class="pad" x="0" y="0" width="9" height="9"/>'
                '<circle class="dot" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } "
                ".pad { background: var(--accent); opacity: 0.5 } "
                ".dot { fill: var(--accent) }",
                "circle", "fill", last=True)

    assert any(not one.guaranteed for one in site.grounds), (
        "a background declaring the mark's token is furniture, not another instance of it"
    )


def test_a_geometry_placed_ground_of_a_different_declaration_still_carries_a_verdict():
    """The half D8 refuses to give up, and the reason it refused option B.

    A mark on a band it fails against must `FAIL`. The opacities are `auth-log-scan`'s as
    published before S7 — `styles.css:152-157` records the author's own sweep, five pairs under
    3:1 — and the shipped page clears at 3.09:1, the only reading in the corpus near the bar.
    Filter `grounds` by `guaranteed` and this site passes at its ancestor's ratio instead."""
    site = _one('<div class="card"><svg>'
                '<rect class="window" x="0" y="0" width="9" height="9"/>'
                '<circle class="ev" cx="4" cy="4" r="1"/></svg></div>',
                ".card { background: var(--bg) } "
                ".window { fill: var(--accent); fill-opacity: 0.45 } "
                ".ev { fill: #d7e2f8 }",
                "circle", "fill", last=True)
    geometric = [r for r, g in zip(site.ratios, site.grounds) if not g.guaranteed]

    assert geometric, "the band is not a ground at all"
    assert min(geometric) < contrast.MARK_THRESHOLD


def test_svg_text_is_measured_against_the_cell_under_it_because_that_is_where_the_failure_was():
    """`0009` §7 row 12's `.cell-share` at 2.69:1 — the one live failure this system has caught
    — is an SVG `<text fill>` on a sibling `rect.cell`. `paint.TEXT` is `{"color"}`, so SVG text
    is a **mark**, and against the card it clears by an order of magnitude.

    This is the guard against a future reader who finds filtering by `guaranteed` attractive:
    that filter scores this page clean, and S12 had to repair it."""
    site = _one('<div class="card"><svg>'
                '<rect class="cell" x="0" y="0" width="9" height="9" fill-opacity="0.9"/>'
                '<text class="cell-share" x="4" y="4">18%</text></svg></div>',
                ".card { background: var(--bg) } .cell { fill: var(--accent) } "
                ".cell-share { fill: #6b7280 }",
                "text", "fill")
    by_ground = dict(zip((g.guaranteed for g in site.grounds), site.ratios))

    assert set(by_ground) == {True, False}, "the cell is not a ground at all"
    assert by_ground[True] >= contrast.MARK_THRESHOLD, "the card must clear, or this proves nothing"
    assert by_ground[False] < contrast.MARK_THRESHOLD


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
