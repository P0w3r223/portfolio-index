"""Whether one shape covers another, from the coordinates the markup already writes.

`ADR-0008` D1: a candidate ground is decided by containment and not by *"every preceding
painted sibling"*, because on `auth-log-scan` 133 of 139 marks have a sibling of their own
colour and the sibling rule reports every one of them undecidable. The corpus makes this cheap
— every shape it paints carries its position as attributes, so *is this mark inside that rect*
is arithmetic on strings that are already in the file.

**This is not the geometry `ADR-0004` §4 defers, and the difference is the whole argument.**
That one — clause 3's *"the wrapper must actually have somewhere to scroll"* — needs a
rendered box: font metrics, available width, the reader's viewport, none of which is in the
document. Two shapes whose coordinates are written in one `viewBox` need none of that.

What the corpus paints, measured 2026-09-09 over the eleven committed surfaces:

    523  text      x, y                    278  circle  cx, cy, r
    333  rect      x, y, width, height     116  line    x1, y1, x2, y2
     32  svg       width, height             8  g       (none)
      6  path      d                         4  polyline / polygon  points

**`text` has an anchor and no bounds, on purpose.** Where a string ends needs font metrics,
which is the deferred question above; where it starts is `x, y`, which is in the file. So text
can be a site and never a ground, and that asymmetry is the same one `ADR-0008` draws between
what a document says and what a browser decides.

`path`, `polyline` and `polygon` get neither. Ten elements in the corpus, and a `d` attribute
is a language rather than a rectangle.

Attribute names arrive lowercased — `html.parser` folds them — so `viewBox` is read as
`viewbox` wherever it is read at all.
"""

from __future__ import annotations

import re

from .render import Element

#: `rotate(angle cx cy)` about the shape's own centre, which leaves that centre where it was.
#: Every `transform` in the corpus is this: 145 of them, all on `auth-log-scan`'s
#: `rect.ev-invalid` diamonds, and **none on `.ev-failed`, `.lane` or `.window-band`** — so the
#: page `0008` §3.11 works through is untouched by the case. Checked rather than assumed,
#: because a transform that moved a shape would make its attributes describe a place it is not.
_ROTATE_ABOUT = re.compile(r"^\s*rotate\(\s*(-?[\d.]+)[\s,]+(-?[\d.]+)[\s,]+(-?[\d.]+)\s*\)\s*$")

_NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")


def _number(element: Element, name: str) -> float | None:
    """A plain number, or `None`. A unit or a percentage is not resolvable from the file."""
    value = element.attributes.get(name, "").strip()
    return float(value) if _NUMBER.match(value) else None


def _numbers(element: Element, *names: str) -> tuple[float, ...] | None:
    found = tuple(_number(element, name) for name in names)
    return None if any(one is None for one in found) else found  # type: ignore[return-value]


def anchor(element: Element) -> tuple[float, float] | None:
    """The point a ground has to cover for this element to be painted on it.

    A shape's own centre, except for `text`, where SVG's `x, y` **is** the anchor the glyphs
    are placed from. Taking a rect's corner instead would put every cell of a confusion matrix
    exactly on its neighbour's boundary, which is the one place the answer is a coin toss.
    """
    if element.tag == "circle":
        found = _numbers(element, "cx", "cy")
        point = found if found else None
    elif element.tag == "rect":
        found = _numbers(element, "x", "y", "width", "height")
        point = (found[0] + found[2] / 2, found[1] + found[3] / 2) if found else None
    elif element.tag == "text":
        point = _numbers(element, "x", "y")
    elif element.tag == "line":
        found = _numbers(element, "x1", "y1", "x2", "y2")
        point = ((found[0] + found[2]) / 2, (found[1] + found[3]) / 2) if found else None
    else:
        point = None
    if point is None or "transform" not in element.attributes:
        return point
    turned = _ROTATE_ABOUT.match(element.attributes["transform"])
    if turned and (float(turned.group(2)), float(turned.group(3))) == point:
        return point
    return None


def bounds(element: Element) -> tuple[float, float, float, float] | None:
    """The box this element offers as a ground, or `None` where the file does not say.

    A transformed element offers none at all: `rotate` leaves a centre alone and does not
    leave a box alone, and the one thing worse than no ground is a ground in the wrong place.
    """
    if "transform" in element.attributes:
        return None
    if element.tag == "rect":
        found = _numbers(element, "x", "y", "width", "height")
        return (found[0], found[1], found[0] + found[2], found[1] + found[3]) if found else None
    if element.tag == "circle":
        found = _numbers(element, "cx", "cy", "r")
        return (found[0] - found[2], found[1] - found[2],
                found[0] + found[2], found[1] + found[2]) if found else None
    return None


def contains(outer: Element, inner: Element) -> bool | None:
    """Whether `outer` covers `inner`'s anchor. `None` where the file cannot say.

    `None` is not `False`, and the census reports it under its own key. A ground that cannot
    be resolved is the thing this checker exists to admit rather than to round off.
    """
    box, point = bounds(outer), anchor(inner)
    if box is None or point is None:
        return None
    return box[0] <= point[0] <= box[2] and box[1] <= point[1] <= box[3]
