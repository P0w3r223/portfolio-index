"""Containment from the file's own coordinates — and the three places it must say `None`.

`ADR-0008` D1 rests on this being cheap and honest: cheap because every shape the corpus
paints writes its position as attributes, honest because where the file does not say, the
answer is `None` and not `False`. Measured on `auth-log-scan`, containment cuts the candidate
grounds for its 139 marks from 6 525 to 1 088, and reduces the last mark's to exactly the two
shapes `0008` §3.11 names — its lane and its window band, with the page background arriving
by ancestry rather than by geometry.

The mutation each test is written against is named in its docstring.
"""

from __future__ import annotations

from tools.pagespec import geometry, render


def _only(html: str, tag: str) -> render.Element:
    page = render.parse(html)
    return next(one for one in page.elements if one.tag == tag)


# -- the anchor, which is what a ground has to cover ----------------------------------------


def test_a_rect_is_anchored_at_its_centre_and_not_at_its_corner():
    """Return `(x, y)` instead and every confusion-matrix cell sits exactly on its
    neighbour's boundary — `pl-review-sense` tiles them at x = 96, 200, 304, each 100 wide, so
    a corner reading makes the answer depend on whether the comparison is `<` or `<=`."""
    assert geometry.anchor(_only('<rect x="96" y="46" width="100" height="54"/>', "rect")) == (146, 73)


def test_a_circle_is_anchored_at_its_centre_and_text_at_the_point_svg_places_it_from():
    """Two different rules for a reason. A circle's `cx, cy` **is** its centre; a `text`
    element's `x, y` is the anchor glyphs are laid out from, not the middle of the string.
    Treating text like a rect would need a width, which is the font-metric question
    `ADR-0004` §4 defers."""
    assert geometry.anchor(_only('<circle cx="132" cy="43" r="3"/>', "circle")) == (132, 43)
    assert geometry.anchor(_only('<text x="146" y="73">323</text>', "text")) == (146, 73)


def test_a_shape_with_no_coordinates_has_no_anchor():
    """`<g>` groups eight elements in the corpus and carries no geometry at all. Returning
    `(0, 0)` for a missing attribute would place every one of them at the origin, inside
    whatever shape happens to start there."""
    assert geometry.anchor(_only("<g><rect/></g>", "g")) is None
    assert geometry.anchor(_only('<rect x="1" y="2"/>', "rect")) is None


def test_a_measurement_with_a_unit_or_a_percentage_is_not_a_number():
    """`float("50%")` raises and `float("10px")` raises, so a bare `float()` would turn an
    unresolvable coordinate into a crash rather than a `None`. The corpus writes plain numbers
    today; this is the branch that keeps that from being an assumption."""
    assert geometry.anchor(_only('<rect x="0" y="0" width="50%" height="10"/>', "rect")) is None
    assert geometry.bounds(_only('<rect x="0" y="0" width="10px" height="10"/>', "rect")) is None


# -- transforms, all 145 of which are one shape ---------------------------------------------


def test_a_rotation_about_a_shapes_own_centre_leaves_that_centre_where_it_was():
    """Every `transform` in the corpus is this: `rotate(45 294.0 77.0)` on a 6.4-square rect at
    (290.8, 73.8), whose centre is exactly (294.0, 77.0). Refusing the anchor outright would
    throw away 145 usage sites for a rotation that does not move the point being asked about.
    """
    diamond = _only('<rect class="ev-invalid" transform="rotate(45 294.0 77.0)" '
                    'x="290.8" y="73.8" width="6.4" height="6.4"/>', "rect")
    assert geometry.anchor(diamond) == (294.0, 77.0)


def test_a_rotation_about_any_other_point_moves_the_shape_and_the_anchor_goes():
    """The mutation: accept `rotate(...)` without comparing its centre to the shape's. The
    element is then reported at a place it is not, which is the one failure this checker is
    built to refuse — a confident wrong answer rather than an admitted unknown."""
    moved = _only('<rect transform="rotate(45 0 0)" x="290.8" y="73.8" width="6.4" height="6.4"/>', "rect")
    assert geometry.anchor(moved) is None
    shifted = _only('<rect transform="translate(10 10)" x="0" y="0" width="4" height="4"/>', "rect")
    assert geometry.anchor(shifted) is None


def test_a_transformed_shape_offers_no_bounds_at_all():
    """A rotation leaves a centre alone and does not leave a box alone: the corpus's diamonds
    are 6.4 square before the turn and 9.05 across after it. `bounds` returning the untransformed
    box would report a ground in the wrong place, and 1 816 of `auth-log-scan`'s candidate
    grounds are these."""
    assert geometry.bounds(_only('<rect transform="rotate(45 3 3)" x="0" y="0" '
                                 'width="6" height="6"/>', "rect")) is None


# -- the bounds, and what deliberately has none ---------------------------------------------


def test_a_rect_and_a_circle_offer_bounds_and_text_and_lines_do_not():
    """`text` and `line` are `None` **by design and not by omission**: where a string ends
    needs font metrics, and a line has no area to be a ground. Give either one a box and
    `auth-log-scan`'s `.lane-line` starts answering for marks drawn over it."""
    assert geometry.bounds(_only('<rect x="132" y="30" width="466" height="22"/>', "rect")) == (132, 30, 598, 52)
    assert geometry.bounds(_only('<circle cx="10" cy="10" r="4"/>', "circle")) == (6, 6, 14, 14)
    assert geometry.bounds(_only('<text x="1" y="2">a</text>', "text")) is None
    assert geometry.bounds(_only('<line x1="0" y1="0" x2="9" y2="0"/>', "line")) is None


# -- containment -----------------------------------------------------------------------------


def test_a_mark_inside_its_lane_and_band_is_contained_and_one_past_the_band_is_not():
    """The measured case, from `auth-log-scan`: a lane 132..598 wide, a band ending at 490.5,
    and marks at 132 and at 560. Flip either comparison to a strict `<` and the mark sitting
    exactly on the lane's left edge — which is where the first mark of every row sits — falls
    out of its own ground."""
    page = render.parse('<g><rect class="lane" x="132" y="30" width="466" height="22"/>'
                        '<rect class="band" x="132" y="30" width="358.5" height="22"/>'
                        '<circle class="a" cx="132" cy="43" r="3"/>'
                        '<circle class="b" cx="560" cy="43" r="3"/></g>')
    lane, band, first, late = (next(one for one in page.elements if key in one.classes)
                              for key in ("lane", "band", "a", "b"))
    assert geometry.contains(lane, first) is True
    assert geometry.contains(band, first) is True
    assert geometry.contains(lane, late) is True
    assert geometry.contains(band, late) is False


def test_a_ground_the_file_cannot_place_is_none_and_none_is_not_false():
    """The whole of `ADR-0008`'s honesty clause in one assertion. `is None` rather than a
    falsey check, because `False` means *measured, and it does not cover this* while `None`
    means *the file does not say* — and the census reports them under different keys."""
    page = render.parse('<g><text class="label" x="1" y="2">n</text>'
                        '<circle class="m" cx="1" cy="2" r="3"/></g>')
    label, mark = (next(one for one in page.elements if key in one.classes)
                   for key in ("label", "m"))
    verdict = geometry.contains(label, mark)
    assert verdict is None
    assert verdict is not False
