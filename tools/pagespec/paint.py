"""What colour an element is painted, and at what alpha — every candidate, not the winner.

`ADR-0008` D2 ships the census without a cascade, so this returns **all** the declarations
that reach an element for a property, each with the specificity it would carry. How often two
rules reach one element is then a figure the corpus prints rather than one the design assumed,
and S14 applies the cascade with that in hand.

**The property set is measured, not imagined.** Enumerating every declaration in the eleven
committed surfaces whose value carries a colour gives exactly these eleven names. Two traps
are on the record because both cost a wrong first count: reading the *value* rather than the
name pulls in `border-radius: var(--radius)` and `font-family: var(--mono)`, which paint
nothing; and **`background-color` occurs nowhere** — every ground in this corpus is written
with the `background` shorthand, so a property list assembled from intuition misses 63 sites.

**Alpha reaches a pixel by three routes and this reads all three**, which `clause_1_composited`
learned one at a time: `color-mix()` in the value (`colour.resolve`), an `opacity` declaration
in a rule, and a presentation attribute in the markup. `fill-opacity` and `stroke-opacity`
apply to their own property and `opacity` applies to everything, which is why the multiplier
is asked for per property rather than per element.

**`var()` chains are not followed, and that is a measurement rather than a shortcut.** All
**238 palette tokens across the corpus resolve in a single hop** — there is no
`--a: var(--b); --b: #fff` anywhere — so `colour.resolve`'s one hop is complete here and
`clauses._resolve_chain` stays where it is. `ADR-0008` §5 left that move open; this closes it
the other way. A chained token would come back unresolved and be reported under
`contrast ground`, which is an admitted unknown and not a wrong colour.
"""

from __future__ import annotations

from typing import NamedTuple

from . import colour, css as cssmod, selector as sel
from .render import Element, Page

#: Every property in the eleven committed surfaces whose value carries a colour, by name.
TEXT = frozenset({"color"})
MARK = frozenset({"fill", "stroke"})
GROUND = frozenset({"background", "background-color"})
NON_TEXT = frozenset({"border", "border-color", "border-top", "border-right", "border-bottom",
                      "border-left", "outline", "outline-color", "accent-color"})
PAINT = TEXT | MARK | GROUND | NON_TEXT

#: What a child takes from its parent when nothing reaches the child.
#:
#: `background` is absent because CSS does not inherit it, and a checker that did would report
#: every element as sitting on its own copy of the page ground rather than on the nearest one
#: that paints.
#:
#: **`color` is absent for a different reason, and it is a measurement.** CSS does inherit it,
#: but inheriting it here made every element on a page a text site: `auth-log-scan` reported
#: **589**, nearly all of them `<div>`, `<g>` and `<rect>` that render no glyphs, and the
#: census's worst text ratio came from a `<rect>`. Whether an element paints text needs the
#: text, which this layer does not hold — so a `color` site is one the stylesheet reaches
#: directly, and a site inheriting its text colour is left to S14 along with the cascade.
#: SVG paint is the case where inheritance is the real mechanism and it stays.
INHERITED = MARK

_ALPHA_FOR = {"fill": "fill-opacity", "stroke": "stroke-opacity"}


class Rule(NamedTuple):
    """One parsed selector and the paint it declares. Refused selectors never become one."""

    selector: sel.Selector
    declarations: dict[str, str]


class Candidate(NamedTuple):
    """One declaration that reaches an element, resolved as far as the file allows.

    `colour` is `None` where the value names something unresolvable — a gradient,
    `currentColor`, a token the palette does not hold. The declaration is still returned, so
    the census can say *this site is painted by a rule whose colour I cannot read* rather than
    dropping the site and reporting nothing about it.
    """

    prop: str
    selector: str
    specificity: tuple[int, int, int]
    declared: str
    colour: str | None
    alpha: float
    inherited_from: int | None


def read_rules(css: str) -> tuple[list[Rule], list[sel.Refusal]]:
    """Every paint-carrying rule this can match, and every one it refuses, both by name.

    The refusals come back rather than being dropped because they are a census row of their
    own: 26 over the eleven surfaces, 22 of them a `:focus-visible` state that no parser
    closes. A reader who sees only the matched rules cannot tell a page with no focus ring
    from one whose focus ring this cannot judge.
    """
    matched: list[Rule] = []
    refused: list[sel.Refusal] = []
    for selector_text, body in cssmod.rules(css):
        if selector_text.startswith("@"):
            continue
        declared = {name: value for name, value in _declarations(body)
                    if name in PAINT or name in ("opacity", "fill-opacity", "stroke-opacity")}
        if not declared:
            continue
        for one in (part.strip() for part in selector_text.split(",")):
            if not one or one.startswith(":root"):
                continue
            parsed = sel.parse(one)
            if isinstance(parsed, sel.Refusal):
                refused.append(parsed)
            else:
                matched.append(Rule(parsed, declared))
    return matched, refused


def candidates(page: Page, element: Element, prop: str, rules: list[Rule],
               palette: dict[str, str]) -> list[Candidate]:
    """Every declaration of `prop` that reaches `element`, in stylesheet order.

    Nothing here picks a winner. Where the element is reached by none and the property
    inherits, the nearest ancestor that *is* reached answers instead — and the candidate says
    which ancestor, because a colour taken from three levels up is a different claim about the
    page than one declared on the element itself.
    """
    direct = [_candidate(rule, prop, element, page, palette, None)
              for rule in rules if prop in rule.declarations
              and sel.matches(page, element, rule.selector)]
    if direct or prop not in INHERITED:
        return direct
    for ancestor in page.ancestors(element):
        from_above = [_candidate(rule, prop, element, page, palette, ancestor.index)
                      for rule in rules if prop in rule.declarations
                      and sel.matches(page, ancestor, rule.selector)]
        if from_above:
            return from_above
    return []


def opacity(page: Page, element: Element, prop: str, rules: list[Rule]) -> float | None:
    """The multiplier between what `prop` declares and what the pixel gets, or `None`.

    A presentation attribute multiplies with a rule's declaration rather than replacing it:
    `pl-review-sense` writes `fill-opacity` per cell from the data, and a rule setting
    `opacity` on the same element applies on top of it. Taking whichever is smaller, or the
    last one seen, would report a cell as more legible than it is.

    **`None` where two rules declare the same alpha for one element**, because choosing
    between them is a cascade and `ADR-0008` D2 ships the census without one. Multiplying
    them instead produces a number no browser paints — measured, this is **four elements on
    `auth-log-scan`**, both rules declaring `opacity`, and it is the whole of the case in the
    eleven committed surfaces. The site is reported under `contrast ground` rather than given
    a made-up alpha.
    """
    factor = 1.0
    for name in ("opacity", _ALPHA_FOR.get(prop)):
        if name is None:
            continue
        declared = [rule.declarations[name] for rule in rules
                    if name in rule.declarations and sel.matches(page, element, rule.selector)]
        if len(declared) > 1:
            return None
        attribute = _number(element.attributes.get(name))
        if attribute is not None:
            factor *= attribute
        if declared:
            # An alpha this cannot read is not an alpha of 1: `opacity: calc(1 - var(--x))`
            # would paint something and `None` says so, where skipping it would claim opaque.
            value = _number(declared[0])
            if value is None:
                return None
            factor *= value
    return max(0.0, min(1.0, factor))


def _candidate(rule: Rule, prop: str, element: Element, page: Page,
               palette: dict[str, str], inherited_from: int | None) -> Candidate:
    """`alpha` here is the declaration's own — `color-mix()`'s percentage and nothing else.

    The element's `opacity` is deliberately **not** folded in: it belongs to the element
    rather than to any one declaration, so multiplying it in per candidate applies the
    markup's `fill-opacity` once for every rule that reaches the element. Two functions, two
    questions; the consumer multiplies them once.
    """
    declared = rule.declarations[prop]
    resolved = colour.resolve(declared, palette)
    hex_value, mix_alpha = resolved if resolved else (None, 1.0)
    return Candidate(prop, rule.selector.text, rule.selector.specificity, declared,
                     hex_value, mix_alpha, inherited_from)


def _declarations(body: str) -> list[tuple[str, str]]:
    """`name: value` pairs at this rule's own level, custom properties left out.

    Split on `;` rather than by regex over the whole body, so a value holding a colon —
    `background: url(data:image/svg+xml,...)` — keeps it.
    """
    found: list[tuple[str, str]] = []
    for part in body.split(";"):
        name, separator, value = part.partition(":")
        if separator and not name.strip().startswith("--"):
            found.append((name.strip().lower(), value.strip()))
    return found


def _number(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.strip())
    except ValueError:
        return None
