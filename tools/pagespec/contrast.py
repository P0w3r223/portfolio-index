"""The contrast census: every usage site, its implied threshold, and what it is painted on.

`ADR-0008` D2. Three keys, all `UNDECIDED` **by construction** — there is no `PASS` and no
`FAIL` branch in this module, which is what makes its exemption from the ratchet floor a proof
rather than an observation. S14 adds the verdicts; this establishes what they would be over.

The sentence behind it is `0007` §5 clause 1's: *the threshold is the one the page's own usage
implies, and it is read per page, not per token*. A site painted as text implies 4.5:1 and one
painted as a mark implies 3.0:1, and that reading is the whole of what this applies. The
sentence making a site **meet** its threshold is not in §5 at all — it is in §7, outside the
range `tools.spec` guards — which is why nothing here fails anything. `ADR-0008` D4 is the
amendment that would change that, and its wording waits on what this prints.

**Grounds come from two places and they are not equal.** An ancestor contains the element
structurally, whatever the geometry says. A preceding sibling may or may not be under it, and
`geometry.contains` answers that from the coordinates the markup writes — which on
`auth-log-scan` cuts the candidates for 139 marks from 6 525 to 1 088 and leaves the last mark
exactly the two shapes `0008` §3.11 names. Where the file cannot say, the site is counted
under `contrast ground` and given no ratio.
"""

from __future__ import annotations

from typing import NamedTuple

from . import colour, css as cssmod, geometry, paint
from .clauses import Finding, UNDECIDED
from .render import Element, Page

#: `0007` §5 clause 1's reading, and the only judgement this module makes. Text carries the
#: higher bar because SC 1.4.3 is about reading words; a mark or a border is SC 1.4.11.
TEXT_THRESHOLD = 4.5
MARK_THRESHOLD = 3.0

#: What a ground is painted with. `fill` is here because an SVG shape's ground is another
#: SVG shape, and `background` because an element's ground outside SVG is a box.
_GROUND_PROPERTIES = ("background", "background-color", "fill")


class Ground(NamedTuple):
    """One thing a site may be painted on, and how sure the document is that it is."""

    element: int
    colour: str
    guaranteed: bool


class Site(NamedTuple):
    """One usage site: an element, a property it paints, and what can be said about it."""

    element: int
    tag: str
    prop: str
    declared: str
    colour: str | None
    alpha: float | None
    threshold: float
    grounds: tuple[Ground, ...]
    same_colour: int
    competing: int
    unresolved: str

    @property
    def ratios(self) -> tuple[float, ...]:
        """The measured ratio against each resolved ground, in the order they were found."""
        if self.colour is None or self.alpha is None:
            return ()
        return tuple(colour.contrast(colour.composite(self.colour, one.colour, self.alpha),
                                     one.colour) for one in self.grounds)


def sites(page: Page, css: str) -> tuple[list[Site], list[str]]:
    """Every painted usage site on the page, and the selectors this could not read.

    A site is an element and a property, not a rule: the same declaration reaches three
    different grounds on `auth-log-scan` and a rule-keyed reading has to pick one of them.
    """
    rules, refused = paint.read_rules(css)
    palette = cssmod.palettes(css).get("light", {})
    found: list[Site] = []
    for element in page.elements:
        # A background is a **ground and not a site**: it is what a thing is measured
        # against, and no success criterion asks a background to contrast with the one behind
        # it. Counting them as marks put `<code> background 1.06:1` at the head of six
        # surfaces — true, and about a code chip sitting on a card, which is a design choice
        # rather than a finding. Found by reading the census's own first output.
        for prop in sorted(paint.PAINT - paint.GROUND):
            candidates = paint.candidates(page, element, prop, rules, palette)
            if not candidates:
                continue
            multiplier = paint.opacity(page, element, prop, rules)
            chosen = candidates[-1]
            found.append(_site(page, element, prop, chosen, candidates, multiplier, palette, rules))
    return found, [one.text for one in refused]


def census(page: Page, css: str) -> list[Finding]:
    """Three findings, none of which can be anything but `UNDECIDED`.

    The counts are what S14 needs and what `0008` §4.19's hand measurement could not take: how
    many sites there are, how many have a ground the file resolves, and what the worst measured
    ratio is on a corpus that today fails nothing.
    """
    found, refused = sites(page, css)
    text = [one for one in found if one.threshold == TEXT_THRESHOLD]
    marks = [one for one in found if one.threshold == MARK_THRESHOLD]
    blind = [one for one in found if one.unresolved or not one.grounds]
    return [Finding("contrast text", UNDECIDED, _measured(text)),
            Finding("contrast marks", UNDECIDED, _measured(marks)),
            Finding("contrast ground", UNDECIDED, _unresolved(blind, refused))]


def _site(page: Page, element: Element, prop: str, chosen: paint.Candidate,
          candidates: list[paint.Candidate], multiplier: float | None,
          palette: dict[str, str], rules: list[paint.Rule]) -> Site:
    threshold = TEXT_THRESHOLD if prop in paint.TEXT else MARK_THRESHOLD
    reasons = []
    if chosen.colour is None:
        reasons.append(f"unreadable value {chosen.declared!r}")
    if multiplier is None:
        reasons.append("two rules declare its alpha and the census has no cascade")
    if len(candidates) > 1:
        reasons.append(f"{len(candidates)} rules reach it and the census has no cascade")
    grounds, same = _grounds(page, element, rules, palette, chosen.colour) if not reasons else ((), 0)
    if not grounds and not reasons:
        reasons.append(f"{same} ground(s) of its own colour" if same
                       else "no ground the document places under it")
    return Site(element.index, element.tag, prop, chosen.declared, chosen.colour, multiplier,
                threshold, grounds, same, len(candidates), "; ".join(reasons))


def _grounds(page: Page, element: Element, rules: list[paint.Rule], palette: dict[str, str],
             own: str | None) -> tuple[tuple[Ground, ...], int]:
    """Ancestors first — containment there is structural — then siblings the file places.

    **A ground painted the element's own colour is counted and not measured.** The ratio is
    1.00:1 by definition, so reporting it as the worst on the page buries every real figure
    under it: `auth-log-scan` draws forty `.ev-failed` circles as siblings inside one
    `<g class="row">`, and each one overlaps the next. That population is `0008` §3.11's
    collapse — 133 of 139 marks — and what it needs is a count, which S14 can act on, rather
    than a number that is true and says nothing.
    """
    found: list[Ground] = []
    same = 0
    for ancestor in page.ancestors(element):
        painted = _painted_ground(page, ancestor, rules, palette)
        if painted:
            found.append(Ground(ancestor.index, painted, True))
            break
    for sibling in page.preceding_siblings(element):
        if geometry.contains(sibling, element) is not True:
            continue
        painted = _painted_ground(page, sibling, rules, palette)
        if not painted:
            continue
        if own is not None and painted.lower() == own.lower():
            same += 1
        else:
            found.append(Ground(sibling.index, painted, False))
    return tuple(found), same


def _painted_ground(page: Page, element: Element, rules: list[paint.Rule],
                    palette: dict[str, str]) -> str | None:
    """What this element actually paints, **its own alpha composited in**.

    Returning the declared colour was a defect and the corpus found it within a run:
    `pl-review-sense` fills every confusion-matrix cell `var(--accent)` and writes
    `fill-opacity` per cell from the data — 0.014 in one, 0.524 in another — so a cell reading
    back as full `#2563eb` made every label on it measure 1.00:1 and buried the page's real
    figures. That page is the one that carried the live SC 1.4.3 failure S12 fixed, so getting
    it wrong here would have made the census blind exactly where it has already been blind.

    A translucent ground is composited over the nearest **ancestor** that paints opaquely,
    which is structural and therefore terminates. A translucent ground with nothing opaque
    behind it is `None`: the file does not say what it sits on, and the site is reported under
    `contrast ground` rather than measured against a guess.
    """
    for prop in _GROUND_PROPERTIES:
        candidates = paint.candidates(page, element, prop, rules, palette)
        if not candidates or not candidates[-1].colour:
            continue
        chosen = candidates[-1]
        multiplier = paint.opacity(page, element, prop, rules)
        if multiplier is None:
            return None
        alpha = multiplier * chosen.alpha
        if alpha >= 1.0:
            return chosen.colour if colour.is_opaque_hex(chosen.colour) else None
        behind = _opaque_behind(page, element, rules, palette)
        return colour.composite(chosen.colour, behind, alpha) if behind else None
    return None


def _opaque_behind(page: Page, element: Element, rules: list[paint.Rule],
                   palette: dict[str, str]) -> str | None:
    """The nearest ancestor painting an opaque colour. Ancestors only, so the walk ends."""
    for ancestor in page.ancestors(element):
        for prop in _GROUND_PROPERTIES:
            candidates = paint.candidates(page, ancestor, prop, rules, palette)
            if not candidates or not candidates[-1].colour:
                continue
            if (paint.opacity(page, ancestor, prop, rules) == 1.0
                    and candidates[-1].alpha >= 1.0
                    and colour.is_opaque_hex(candidates[-1].colour)):
                return candidates[-1].colour
    return None


def _measured(found: list[Site]) -> str:
    measured = [(min(one.ratios), one) for one in found if one.ratios]
    if not found:
        return "no site"
    if not measured:
        return f"{len(found)} site(s), none with a ground the document resolves"
    worst, site = min(measured, key=lambda pair: pair[0])
    return (f"{len(found)} site(s), {len(measured)} measured, worst {worst:.2f}:1 "
            f"against {site.threshold:.1f}:1 at <{site.tag}> {site.prop}")


def _unresolved(blind: list[Site], refused: list[str]) -> str:
    parts = [f"{len(blind)} site(s) without a resolved ground"]
    own = sum(one.same_colour for one in blind)
    if own:
        parts.append(f"{own} ground(s) of the site's own colour, which measure 1.00:1")
    if refused:
        parts.append(f"{len(refused)} selector(s) this does not read")
    return "; ".join(parts)
