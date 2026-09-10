"""The contrast verdicts, and the census the two of them could not be taken without.

`ADR-0008` D2. **This module named no verdict until S14b**, and that was a proof rather than an
observation: `UNDECIDED` was the only status it could build, which is what kept its three keys
out of the ratchet floor. S14b ends that. Two keys now take a verdict and the third cannot —
`contrast ground` reports what the checker could not read, and a page is not less conforming
for being hard to read. The exemption those two used to hold is now a row in `__main__.GATE`,
which is where it belongs and where narrowing it is guarded.

*Until 2026-09-10 the paragraph above said there is no `PASS` and no `FAIL` branch here, and a
guard read this file statically to prove it. Both were true for exactly as long as the census
was the whole of the stage.*

Two sentences of `0007` §5 clause 1 stand behind it. `c1.s6` sets the bar — *the threshold is
the one the page's own usage implies, and it is read per page, not per token* — and `c1.s6b`,
which `ADR-0008` D4 held back until the census had printed, is what makes meeting it an
obligation. D5 says which sites are owed that obligation and D6 says what a site is measured
against; neither is arithmetic, and both were taken against the corpus rather than in advance.

**Grounds come from two places and they are not equal.** An ancestor contains the element
structurally, whatever the geometry says. A preceding sibling may or may not be under it, and
`geometry.contains` answers that from the coordinates the markup writes — which on
`auth-log-scan` cuts the candidates for 139 marks from 6 525 to 1 088 and leaves the last mark
exactly the two shapes `0008` §3.11 names. Where the file cannot say, the site is counted
under `contrast ground` and given no ratio.
"""

from __future__ import annotations

from typing import NamedTuple

from . import clauses as clausemod, colour, css as cssmod, geometry, paint
from .clauses import FAIL, Finding, PASS, UNDECIDED
from .render import Element, Page

#: `0007` §5 clause 1's reading, and the only judgement this module makes. Text carries the
#: higher bar because SC 1.4.3 is about reading words; a mark or a border is SC 1.4.11.
TEXT_THRESHOLD = 4.5
MARK_THRESHOLD = 3.0

#: What a ground is painted with. `fill` is here because an SVG shape's ground is another
#: SVG shape, and `background` because an element's ground outside SVG is a box.
_GROUND_PROPERTIES = ("background", "background-color", "fill")

#: What a site's **own** ground is painted with, which is not the same tuple. `ADR-0008` D6's
#: first bound: reading self-as-ground through `_GROUND_PROPERTIES` makes every `<text>` its
#: own ground, because in SVG one property is a shape's paint *and* a text's foreground. That
#: reading was measured and reported 684 failures, all of them 1.00:1 and every one the
#: question *does this thing contrast with itself*.
_OWN_GROUND_PROPERTIES = ("background", "background-color")

#: A control's own paint, which no border declares and which the border family therefore
#: cannot reach. `accent-color` is the visible part of a range slider and a checkbox — a
#: user-interface component by any reading of SC 1.4.11 — and D5's property-name partition
#: excluded it. `ADR-0008` §10.
_CONTROL_PROPERTIES = frozenset({"accent-color"})

#: Words are words wherever they are painted, and this is a **bound** rather than a detail.
#: `ADR-0008` §10 exempts SVG paint declaring only structure roles; without this set that
#: exemption would reach an SVG label. `mini-traceroute`'s stylesheet carries
#: `.probe-ttl { fill: var(--bg); font-size: 9px; font-weight: 700 }` and `it-job-radar`'s
#: `.series-dot.observed { fill: var(--bg) }` — and `--bg` shows **zero** measured sites in the
#: census today, which is this checker's blindness rather than the corpus's: a cascade turns
#: those on. A partition trusting that zero would go blind on SVG labels at exactly the stage
#: that makes them visible, and SVG text is where the only live failure this system has caught
#: actually lived.
_TEXT_TAGS = frozenset({"text", "tspan"})


class Painted(NamedTuple):
    """What an element paints as a ground, and the declaration that painted it.

    The declaration rides with the colour because `ADR-0008` D8 excludes a ground that is
    another instance of the same mark, and *same* is a fact about declarations rather than
    about resolved colours: one token at two alphas composites to two colours and is one mark.
    """

    colour: str
    prop: str
    declared: str


class Ground(NamedTuple):
    """One thing a site may be painted on, and how sure the document is that it is.

    **`guaranteed` is not a verdict input**, `ADR-0008` D8. It separates a ground an ancestor
    structurally contains from one the markup's own coordinates place under the site, and D8
    measured that the distinction does not track defect **for the population it moved**: all 79
    sites whose only failing ground was geometric clear their guaranteed ground between 3.98:1
    and 8.16:1, while both failures with a history are read on a geometric ground. Read more
    generally it is false and the instrument says so — of the 88 failures that survive D8, 64
    fail on their guaranteed ground alone. The field is reporting, not gating.
    """

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
    obligated: bool
    grounds: tuple[Ground, ...]
    same_colour: int
    competing: int
    unresolved: str

    @property
    def ratios(self) -> tuple[float, ...]:
        """The measured ratio against each resolved ground, in the order they were found.

        **`is_opaque_hex` and not merely `is not None`, because `colour.resolve` returns a
        palette value whatever its type.** A token holding `rebeccapurple`, `rgb(37 99 235)`,
        `#11111180`, `light-dark(...)`, `oklch(...)` or another `var()` comes back non-`None`,
        reaches `composite`, and raises out of `clauses.check` — taking the whole
        twelve-surface table down over one token on one page. Measured on six notations, all
        six fatal, and `0008` S7 migrates `--ink`/`--line` aliases, so the alias shape was one
        commit from firing. The guard for this class was written for `clause_1_tokens` and the
        defect moved one module to the left of it.
        """
        if self.alpha is None or not (self.colour and colour.is_opaque_hex(self.colour)):
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
    """Two verdicts and one census, `ADR-0008` D2's second half.

    S13 shipped all three `UNDECIDED` by construction; S14b is the stage that may fail one.
    What each key is owed by is D5's, and what a site is measured against is D6's — this
    function only counts.

    **`contrast ground` stays `UNDECIDED` permanently**, D3. It reports the sites no verdict
    could be taken over, and a key whose subject is *the checker could not read this* has
    nothing to pass or fail: a page that resolves every ground and one that resolves none are
    both conforming pages as far as `0007` §5 can say.
    """
    found, refused = sites(page, css)
    text = [one for one in found if one.prop in paint.TEXT]
    marks = [one for one in found if one.obligated and one.prop not in paint.TEXT]
    exempt = [one for one in found if not one.obligated]
    blind = [one for one in found if one.unresolved or not one.grounds]
    return [Finding("contrast text", _verdict(text), _measured(text)),
            Finding("contrast marks", _verdict(marks), _measured(marks, exempt)),
            Finding("contrast ground", UNDECIDED, _unresolved(blind, refused, found))]


def _verdict(found: list[Site]) -> str:
    """`FAIL` on one measured site below its threshold, `PASS` when none is.

    **A site with no measured ratio is not a pass and not a failure**, and it is already
    counted under `contrast ground`. Reading it as a pass would let a page go clean by being
    unreadable, which is the direction that matters: `0008` §3.11's collapse is 133 of 139
    marks on one surface, and a rule that scored those as passes would have called that
    surface clean on the strength of the checker's own blindness.
    """
    measured = [(min(one.ratios), one.threshold) for one in found if one.ratios]
    if not measured:
        return UNDECIDED
    return FAIL if any(ratio < bar for ratio, bar in measured) else PASS


def _site(page: Page, element: Element, prop: str, chosen: paint.Candidate,
          candidates: list[paint.Candidate], multiplier: float | None,
          palette: dict[str, str], rules: list[paint.Rule]) -> Site:
    threshold = TEXT_THRESHOLD if prop in paint.TEXT else MARK_THRESHOLD
    obligated = _obligated(element.tag, prop, chosen.declared)
    reasons = []
    if chosen.colour is None:
        reasons.append(f"unreadable value {chosen.declared!r}")
    elif not colour.is_opaque_hex(chosen.colour):
        # `resolve` hands back what the palette holds, hex or not. Saying so here is what
        # turns a crash into the `contrast ground` row the census exists to print.
        reasons.append(f"{chosen.declared} resolves to {chosen.colour!r}, "
                       f"which this cannot read as a colour")
    if multiplier is None:
        reasons.append("two rules declare its alpha and the census has no cascade")
    if len(candidates) > 1:
        reasons.append(f"{len(candidates)} rules reach it and the census has no cascade")
    grounds, same = (_grounds(page, element, prop, rules, palette, chosen.colour,
                              chosen.declared)
                     if not reasons else ((), 0))
    if not grounds and not reasons:
        reasons.append(f"{same} ground(s) of its own colour" if same
                       else "no ground the document places under it")
    return Site(element.index, element.tag, prop, chosen.declared, chosen.colour, multiplier,
                threshold, obligated, grounds, same, len(candidates), "; ".join(reasons))


def _obligated(tag: str, prop: str, declared: str) -> bool:
    """Whether `ADR-0008` D5 asks this site to meet its threshold at all.

    **The rule is D5's and unchanged; the axis is §10's.** Obligation attaches to *role*, and
    D5 approximated role by property name — which cannot work, because `fill` paints a gridline
    and a data mark with one word. §10 reads the role off the declaration instead, on `c1.s4`'s
    ground that *a token is used in the role it names*: across the twelve, `--border` and
    `--surface` measure below the bar 62 times and above it **zero** times, while every
    semantic token passes in the hundreds.

    The order of the tests is load-bearing:

    - **Text first and unconditionally.** SC 1.4.3 is about reading words.
    - **The control role and a control's own paint next**, so `border: 1px solid
      var(--border-control)` never reaches the boundary exclusion below. D7 minted that role
      because no existing token could carry a control boundary's ratio.
    - **A boundary that bounds no control is owed nothing**, exactly as under D5.
    - **An SVG label is never exempted by the token painting it** — `_TEXT_TAGS`, and the
      constant's own comment is why that bound is not cosmetic.
    - **`named <= STRUCTURE_ROLES` and not `named & STRUCTURE_ROLES`.**
      `color-mix(in srgb, var(--accent) 30%, var(--surface))` names both and must stay obliged;
      the corpus cannot redden that conjunct, so its guard is synthetic.
    - **`named and …`** — a declaration naming no token at all stays obliged. The instrument
      cannot read a role it was never given, and fail-loud is the direction that gets found.
    """
    if prop in paint.TEXT:
        return True
    named = clausemod.roles_named(declared)
    if clausemod.CONTROL_ROLE in named or prop in _CONTROL_PROPERTIES:
        return True
    if prop not in paint.MARK:
        return False
    if tag in _TEXT_TAGS:
        return True
    return not (named and named <= clausemod.STRUCTURE_ROLES)


def _grounds(page: Page, element: Element, prop: str, rules: list[paint.Rule],
             palette: dict[str, str], own: str | None,
             declared: str) -> tuple[tuple[Ground, ...], int]:
    """The element's own background first, then ancestors, then the siblings the file places.

    **`ADR-0008` D6, and the word in it is *occludes*.** An element painting its own opaque
    background hides what is behind it, so for a foreground the walk starts at the element and
    stops there. Appending it as one more candidate instead was measured and is the wrong
    reading: `Site.ratios` returns one ratio per ground and `_measured` takes the `min()`, so
    the two published buttons this rests on keep 1.00:1 and 1.06:1 against a ground they cover.
    Occluding moves 28 readings and leaves 0 text failures; adding moves 18 and leaves 2.

    **Only a foreground, and only over `background`.** `fill` is excluded by
    `_OWN_GROUND_PROPERTIES`, and a border is excluded here: a boundary faces outward, its
    visibility comes from the colour on the other side, and measuring `mini-traceroute`'s
    `<button>` border against the button's own fill gives 1.00:1 — the wrong comparison,
    confidently computed.

    **A ground painted the element's own colour is counted and not measured.** The ratio is
    1.00:1 by definition, so reporting it as the worst on the page buries every real figure
    under it: `auth-log-scan` draws forty `.ev-failed` circles as siblings inside one
    `<g class="row">`, and each one overlaps the next. That population is `0008` §3.11's
    collapse — 133 of 139 marks — and what it needs is a count, which S14 can act on, rather
    than a number that is true and says nothing.
    """
    found: list[Ground] = []
    same = 0
    if prop in paint.TEXT:
        own_ground = _painted_ground(page, element, rules, palette, _OWN_GROUND_PROPERTIES)
        if own_ground:
            return (Ground(element.index, own_ground.colour, True),), 0
    for ancestor in page.ancestors(element):
        painted = _painted_ground(page, ancestor, rules, palette)
        if painted:
            found.append(Ground(ancestor.index, painted.colour, True))
            break
    for sibling in page.preceding_siblings(element):
        if geometry.contains(sibling, element) is not True:
            continue
        painted = _painted_ground(page, sibling, rules, palette)
        if not painted:
            continue
        if _the_same_mark(prop, declared, own, painted):
            same += 1
        else:
            found.append(Ground(sibling.index, painted.colour, False))
    return tuple(found), same


def _the_same_mark(prop: str, declared: str, own: str | None, painted: Painted) -> bool:
    """Whether this ground is another instance of the site itself — `ADR-0008` D8.

    Two overlapping members of one series carry one meaning, and a reader is owed no way to
    tell them apart. `0007` §5 clause 1's `c1.s6c` is the rule; this is the approximation, on
    D5's precedent that *the rule is the criterion's and the partition is the instrument's*.

    **Two tests, and the second is the one D8 added.** Identical resolved colour was always
    excluded, because that ratio is 1.00:1 by definition and reporting it buries every real
    figure under it. What that test could not see is the same declaration at two alphas: a
    site's colour arrives here **un-composited** — `_site` passes `chosen.colour` — while
    `painted` is composited, so `auth-log-scan`'s `.ev-failed` circles, all `fill:
    var(--accent)` with a `fill-opacity` the data writes per element, read 1.26:1 against each
    other and escaped. **65 sites and 966 (site, ground) pairs, and the rule meant to exclude
    them missed on a unit mismatch rather than on a judgement.** `_grounds`' docstring has
    described that population since S13.

    **Property as well as value**, because `fill: var(--accent)` and a background declaring the
    same token are not the same mark; the property is what makes one a graphic and the other
    the furniture it sits on.

    What this deliberately does *not* exclude is a ground painted by a **different**
    declaration — the band under `auth-log-scan`'s marks, at the 3.09:1 its author swept for,
    and the `rect.cell` under `pl-review-sense`'s `.cell-share` at the 2.69:1 that is the one
    live failure this checker has ever caught. `ADR-0008` §9 measures both.
    """
    if own is not None and painted.colour.lower() == own.lower():
        return True
    return prop == painted.prop and declared.strip().lower() == painted.declared.strip().lower()


def _painted_ground(page: Page, element: Element, rules: list[paint.Rule],
                    palette: dict[str, str],
                    properties: tuple[str, ...] = _GROUND_PROPERTIES) -> Painted | None:
    """What this element actually paints, **its own alpha composited in**, and by what.

    **The declaration rides back with the colour since D8**, and one function returns both on
    purpose: `_the_same_mark` needs to compare like with like, and a second function that
    re-derived which declaration won would be a second spelling of this selection — the shape
    `0009` N1 names, where two registries of one vocabulary drift and nothing notices.

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
    for prop in properties:
        candidates = paint.candidates(page, element, prop, rules, palette)
        if not candidates or not candidates[-1].colour:
            continue
        chosen = candidates[-1]
        multiplier = paint.opacity(page, element, prop, rules)
        if multiplier is None:
            return None
        alpha = multiplier * chosen.alpha
        if alpha >= 1.0:
            return (Painted(chosen.colour, prop, chosen.declared)
                    if colour.is_opaque_hex(chosen.colour) else None)
        behind = _opaque_behind(page, element, rules, palette)
        if not behind:
            return None
        return Painted(colour.composite(chosen.colour, behind, alpha), prop, chosen.declared)
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


def _measured(found: list[Site], exempt: list[Site] | None = None) -> str:
    """The population, the worst reading in it, and — for marks — what D5 left out of it.

    The exempt count is printed rather than dropped because it is the largest single number
    this module knows and the one a reader is likeliest to want back: structural borders and
    outlines, nearly all of them below 3.0:1 and required to measure nothing. Leaving it
    unprinted would make `contrast marks` look like a reading of every non-text site, which it
    deliberately is not. *This paragraph carried the figures 1 049 and 1 034 until 2026-09-10,
    when `ADR-0008` §10 moved both; the run prints them and this does not.*

    **The structure-paint share is broken out, and it is the whole mitigation for §10's one
    unverifiable direction.** `clause_1_usage` applies the role rule to the ground and border
    families and deliberately not to `fill`/`stroke`, so a genuine data mark painted
    `var(--border)` is exempted with nothing objecting. Nothing can object — but the count is
    on every run, so a new one appearing moves a number a reader sees. `c1.s4c`'s answer to
    the same shape one property to the left.
    """
    measured = [(min(one.ratios), one) for one in found if one.ratios]
    structural = sum(1 for one in (exempt or ()) if one.prop in paint.MARK
                     and (named := clausemod.roles_named(one.declared))
                     and named <= clausemod.STRUCTURE_ROLES)
    share = f", {structural} of them structure paint" if structural else ""
    tail = f"; {len(exempt)} outside D5's obligation{share}" if exempt else ""
    if not found:
        return "no site" + tail
    if not measured:
        return f"{len(found)} site(s), none with a ground the document resolves" + tail
    worst, site = min(measured, key=lambda pair: pair[0])
    below = sum(1 for ratio, one in measured if ratio < one.threshold)
    failing = f", {below} below" if below else ""
    return (f"{len(found)} site(s), {len(measured)} measured{failing}, worst {worst:.2f}:1 "
            f"against {site.threshold:.1f}:1 at <{site.tag}> {site.prop}" + tail)


def _unresolved(blind: list[Site], refused: list[str], every: list[Site] | None = None) -> str:
    """What the checker could not read, and what it deliberately did not measure.

    **The same-mark count is summed over every site and not over `blind`**, `ADR-0008` D8, and
    the first version of this summed `blind` alone. That was vacuous by D8's own structural
    argument: a site whose sibling ground is excluded keeps its ancestor, so it is never blind,
    so its count was never reached. 966 excluded pairs left the verdict with no line anywhere
    in the run while three documents said they were printed here — the *checker quietly
    narrowing its own subject* shape, in the commit that added a guard citing it. Found by the
    review that blocked that commit.
    """
    parts = [f"{len(blind)} site(s) without a resolved ground"]
    own = sum(one.same_colour for one in (every if every is not None else blind))
    if own:
        parts.append(f"{own} ground(s) excluded as the same mark, ADR-0008 D8")
    if refused:
        parts.append(f"{len(refused)} selector(s) this does not read")
    return "; ".join(parts)
