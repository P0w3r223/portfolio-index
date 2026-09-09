"""Which elements a rule reaches, and the shapes this refuses to answer for.

Clause 1's threshold is read per usage site and a usage site is an element — `0007` §5
clause 1, `0008` §3.11, `ADR-0008` — so something has to say which elements a selector
reaches. This does, for the shapes the corpus writes, and **refuses the rest by name instead
of guessing at them**.

Measured over the eleven committed surfaces, 2026-09-09: **373 selectors carry a colour** and
this answers for 347. The 26 it refuses are two different questions and are reported apart:

- **a state the document is not in** — 22 sites, every one a `:focus-visible` ring on `a`,
  `summary`, `input`, `select` or `button`. A static read cannot know a focus state, and no
  amount of parser is going to change that. They appeared only once the census was widened to
  borders: against `color`, `background`, `fill` and `stroke` alone the corpus has **no**
  pseudo-class carrying paint at all.
- **a shape this does not parse** — 4 sites: `.field input[type="number"]`,
  `.field input[type="range"]`, `.control input[type="range"]` and one general sibling,
  `.chart .range.muted ~ .range-dot`.

Neither `#id` nor `*` occurs in a paint-carrying selector anywhere in the corpus, so both are
refused rather than supported. A branch for a shape nobody writes is a claim with no evidence
under it, and it would be the only part of this module no corpus could redden.

The chain is descendant-only, which is what 373 selectors minus one general sibling means.
Depth reaches four — `.chart .range.muted ~ .range-dot` aside, the deepest is three.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from .render import Element, Page

#: A pseudo-class. The element may match it at some moment and the document does not say so.
STATE = "state"
#: A selector shape this parser does not reach. Widening it is a code change; `STATE` is not.
SHAPE = "shape"

_TAG = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]*$")
_CLASS = re.compile(r"^-?[_a-zA-Z][\w-]*$")


class Step(NamedTuple):
    """One compound in a descendant chain: an optional tag and the classes it requires."""

    tag: str | None
    classes: frozenset[str]


class Selector(NamedTuple):
    """A parsed selector, with the specificity it would carry in a cascade.

    `specificity` is computed and **this module applies it to nothing**. `ADR-0008` D2 ships
    the census without a cascade so that how often two rules reach one element is a figure the
    corpus produces rather than one this design assumes; the number rides here so the census
    can print it beside each match.
    """

    text: str
    steps: tuple[Step, ...]
    specificity: tuple[int, int, int]


class Refusal(NamedTuple):
    """Why a selector is not answered for. `kind` is `STATE` or `SHAPE`; both are printed."""

    text: str
    kind: str
    detail: str


def parse(text: str) -> Selector | Refusal:
    """One selector — not a comma-separated list, which the caller splits.

    Refusing on the first unreadable token rather than dropping it is the whole contract: a
    parser that skipped `[type="number"]` would report `.field input` as the rule, match every
    input on the page, and hand a confident ground to a site the stylesheet never painted.
    """
    text = text.strip()
    if not text:
        return Refusal(text, SHAPE, "empty")
    if "," in text:
        return Refusal(text, SHAPE, "a selector list, which the caller splits")
    if "::" in text:
        return Refusal(text, SHAPE, "pseudo-element: a generated box, not an element of the document")
    if ":" in text:
        return Refusal(text, STATE, "pseudo-class: the document does not say whether it holds")
    for character, reason in (("[", "attribute selector"), ("#", "id selector"),
                              ("*", "universal selector"), (">", "child combinator"),
                              ("+", "adjacent-sibling combinator"), ("~", "general-sibling combinator")):
        if character in text:
            return Refusal(text, SHAPE, reason)

    steps: list[Step] = []
    for compound in text.split():
        tokens = compound.split(".")
        tag = tokens[0] or None
        if tag is not None and not _TAG.match(tag):
            return Refusal(text, SHAPE, f"unreadable type {tag!r}")
        classes = tokens[1:]
        if any(not _CLASS.match(one) for one in classes):
            return Refusal(text, SHAPE, f"unreadable class in {compound!r}")
        steps.append(Step(tag.lower() if tag else None, frozenset(classes)))

    classes_total = sum(len(step.classes) for step in steps)
    tags_total = sum(1 for step in steps if step.tag)
    return Selector(text, tuple(steps), (0, classes_total, tags_total))


def matches(page: Page, element: Element, selector: Selector) -> bool:
    """Whether `selector` reaches `element` on `page`.

    Right to left, which is how a descendant chain is decided: the last compound must be the
    element itself, and the ones before it must appear among its ancestors **in order** but
    not necessarily adjacently. Matching left to right instead would accept
    `.chart .row .window-band` against a band whose row sits outside its chart.
    """
    if not _step_matches(selector.steps[-1], element):
        return False
    remaining = list(selector.steps[:-1])
    for ancestor in page.ancestors(element):
        if remaining and _step_matches(remaining[-1], ancestor):
            remaining.pop()
    return not remaining


def reaches(page: Page, selector: Selector) -> list[Element]:
    """Every element on the page the selector reaches, in document order."""
    return [element for element in page.elements if matches(page, element, selector)]


def _step_matches(step: Step, element: Element) -> bool:
    if step.tag is not None and step.tag != element.tag:
        return False
    return step.classes <= element.classes
