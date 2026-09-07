"""The eight clauses of `0007` §5, as checks over one loaded surface.

Pure functions over already-read bytes: no file access, no network — still true of every
function here, though the module now imports `sources` for one thing: `describe`, the single
rendering of an unreadable-stylesheet pair. The pair is `sources` data, so its formatter
lives with it; nothing on this side calls anything that opens a file. What a clause cannot
decide, it says so rather than guessing — `0007` §7 exists because the instrument that
produced the original table was wrong three times, twice caught only by review, and a
checker that reports a confident verdict it did not earn is that failure automated.
"""

from __future__ import annotations

import hashlib
import re
import urllib.parse
import unicodedata
from dataclasses import dataclass

from . import colour, css as cssmod, render, sources

PASS, FAIL, UNDECIDED, NOT_APPLICABLE = "pass", "fail", "undecided", "n/a"

#: `0007` §5 clause 1 — *"the ten tokens in §4.1"*: the eight settled ones, and the two the
#: governing rule pins to the *measured* value rather than the majority one.
#:
#: **It was eight here for one session.** `PINNED` then reported an absent `--accent-soft` or
#: `--positive` as `n/a — not declared`, so the two the clause argues hardest about were the
#: two whose *absence* it could not report at all — and §4.1 records `wroclaw` as lacking
#: `--positive` entirely. Every surface with a `:root` already declares all ten, so this
#: closes the hole without moving a single cell of the computed table.
HOUSE_TOKENS = ("bg", "surface", "border", "text", "muted", "accent", "warn", "radius",
                "accent-soft", "positive")
#: The roles that must resolve to a colour. `--radius` is a length and extensions like
#: `mini-traceroute`'s `--mono` are font stacks, so neither is asked to be one.
COLOUR_ROLES = ("bg", "surface", "border", "text", "muted", "accent", "warn",
                "accent-soft", "positive", "danger")
PINNED = {
    "light": {"accent-soft": "#5b93e4", "positive": "#047857"},
    "dark": {"accent-soft": "#4167a6", "positive": "#34d399"},
}
CARD_META = ("description", "og:type", "og:title", "og:description", "og:url", "twitter:card")
PROFILE = "github.com/P0w3r223"

#: A whole grouped figure: 1-3 digits, then one or more (separator + exactly three digits),
#: an optional decimal tail, and nothing numeric and no `:` or `.` touching either end. The
#: bound is what makes this a measurement — without it `07:00 203.0.113.42` scores as a grouped
#: figure, which is how one page was credited with nineteen it does not have. The separator
#: class is spelled out rather than using `\s`, because `\s` matches the newline
#: `rendered_text` puts between adjacent nodes and would weld two numbers back together.
#:
#: **The decimal tail sits inside the bound, not instead of it.** Without it `8 612.50` matched
#: nothing at all and the page read `n/a — no grouped figure`, and `1 234 567.89` scored one
#: separator instead of two: `car-price-ml` prints PLN amounts throughout, so once `0008` S9
#: brings this clause into `GATED`, rewriting `8 612` as `8 612.50` would have moved a surface
#: from `FAIL` to `n/a` and past the gate while still using a plain space. The obvious repair —
#: relaxing the trailing bound to `(?![\d:])` — was measured against the corpus and reddens
#: `auth-log-scan` with four `FAIL`s out of `40 198.51.100.77` and its neighbours, which is
#: exactly what the bound was written to prevent. Re-applying it *after* the tail keeps both.
#:
#: **U+2009 is in the class because it is a wrong separator and not an absent one.** The thin
#: space is what a hand edit reaches for during a migration to the narrow no-break space, and
#: while it was outside the class `1<U+2009>234` matched nothing and the page reported
#: `n/a — no grouped figure`: a page grouping its thousands with the wrong codepoint read as a
#: page grouping nothing. Both shapes measure zero on all eleven committed surfaces today, so
#: neither change moves a cell of the table.
_GROUPED = re.compile(
    r"(?<![\d.:])(\d{1,3})((?:[ \u2009\u202f\u00a0,](?:\d{3}))+)(?:\.\d+)?(?![\d.:])"
)
#: Why CSS discarded a declaration, and the sentence the report prints for each. A cycle
#: and a dangling reference have the same effect and different causes, and naming the wrong
#: one is a confident wrong sentence over a correct verdict.
_SELF, _CYCLE, _DANGLING = "self", "cycle", "dangling"
_DISCARDED = {
    _SELF: "refers to itself, so CSS discards it as a cycle",
    _CYCLE: "is in a cycle of var() references, so CSS discards it",
    _DANGLING: "names a token that resolves to nothing",
}

#: The two property families §5 clause 1's fourth sentence speaks about, the roles each one
#: takes, and the shapes `_role_exception` reads. `border-radius` is deliberately absent: it
#: is a length rather than a colour role, and `1 tokens` is what asks whether it is declared.
_GROUND_PROPERTIES = ("background", "background-color")
_SIDE_BORDERS = ("border-top", "border-right", "border-bottom", "border-left")
_BORDER_PROPERTIES = ("border", "border-color") + _SIDE_BORDERS
_GROUND_ROLES = frozenset({"bg", "surface"})
_BORDER_ROLES = frozenset({"border"})
#: The three roles the fourth sentence assigns. A role in here is never what makes an
#: exception an exception: every one of the four shapes is about a surface deliberately
#: painted *outside* the house scheme, so a house role appearing there is the defect rather
#: than the exemption.
_HOUSE_ROLES = _GROUND_ROLES | _BORDER_ROLES
#: **`_LENGTH` had the identical hole and was fixed one commit later**, which is the shape
#: this branch is named for: the repair landed on one of two sibling patterns, three lines
#: apart, and the commit message called the other one safe. It is not — it reads a number
#: and a unit straight out of a token's name, and it is evaluated *first*, so it shadows the
#: anchored branch in both directions. `border-left: solid var(--rule-2rem)` exempted a
#: hairline; `border-left: thick solid var(--rule-1px)` scavenged `1px` from the name, beat
#: the keyword, and failed a genuine 5px rail.
#: A border width in `px`, `rem` or `em` — the three a stylesheet here writes. `pt` and the
#: viewport units are not read and report as no width at all, which is the old defect at a
#: smaller radius; narrow the sentence rather than claim coverage. `px` alone was the whole
#: pattern, so a rail written `0.2rem` matched nothing, took no exemption, and reported
#: `1 usage roles FAIL` — a key `"1 "` gates on, about a page that is conforming. `0008` S9
#: rewrites five stylesheets, which is where a unit changes.
#:
#: The root font size is not read and 16 is CSS's initial value. That is an assumption and
#: it is a safe one here: this distinguishes a **rail** from a hairline, so the threshold is
#: 1px against widths that are three to five times it, not a measurement anything turns on.
_LENGTH = re.compile(r"(?<![-\w.])(\d+(?:\.\d+)?|\.\d+)(px|rem|em)(?![-\w])")
_PER_UNIT = {"px": 1.0, "rem": 16.0, "em": 16.0}
#: The keyword widths, at their usual computed values. `medium` is the CSS initial value for
#: `border-width`, so `border-left: medium solid var(--warn)` is a rail written without a
#: number — and it read as no width at all.
#:
#: **Both patterns are anchored past the hyphen, because `\b` is not.** The keyword version
#: searched the whole
#: declaration for the bare word, and a declaration always contains `var(--<role>)`: `-` is a
#: non-word character, so `\bthick\b` matched inside `var(--thick-rule)` and exempted a
#: hairline as a rail. A false *exemption* on a key `"1 "` gates — the silent-green shape
#: §3.9 and §4.9 record.
#:
_WIDTH_KEYWORD = re.compile(r"(?<![-\w])(thin|medium|thick)(?![-\w])")
_WIDTH_KEYWORDS = {"thin": 1.0, "medium": 3.0, "thick": 5.0}
#: The states a border may change colour under without being the box's edge. Not a list of
#: pseudo-classes in general: `:first-child` is not a state a reader entered.
#:
#: It matches inside `:not(...)` too, so `a:not(:hover)` reads as a state and is exempted. No
#: surface writes that and the reading is wrong; it is recorded rather than handled because
#: excluding it means parsing the selector rather than searching it, and `0008` §3.10's own
#: conclusion is that reading the branches against each other is what catches this class.
_INTERACTION_STATE = re.compile(r":(?:hover|focus|active)\b")
#: Any hex literal, including the 4- and 8-digit alpha forms `colour.rgb` refuses to
#: measure. A translucent literal outside the token block is still a literal outside the
#: token block. Spelled the same way `apply-scout`'s own page test spells it, because the
#: two carriers disagreeing on what counts is what this clause is here to end.
_HEX_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b")

#: The token a `var()` names. **The fallback is not matched here**, and the missing constant is
#: worth a sentence: `_VAR_FALLBACK` was a regex accepting a 3- or 6-digit hex and nothing else,
#: so every other legal fallback fell through to `_DANGLING` and `var(--stack, monospace)`
#: reported *"names a token that resolves to nothing"* about a declaration the browser paints.
#: A regex could not be widened into the repair — a fallback may hold a nested `var()` and
#: `[^)]*` stops at the inner close paren — so `_fallback_argument` balances instead.
_VAR_NAME = re.compile(r"var\(\s*(--[\w-]+)")

#: An `@import` or a `@font-face` `src:` pointing off-origin. Quotes are stripped by the
#: caller rather than matched here, which keeps the class free of quote characters.
#: `@import` and `src:` reach a host by two spellings, and this read one of them — then, on
#: being widened, read the *first* of them and stopped. `src: local("Inter"), url(https://…)`
#: is the canonical `@font-face` line, and an alternation makes the two spellings compete for
#: one match: `"Inter"` won, the remote URL was never examined, and the page reported
#: `ok 7 webfont system stack`. **Closing one false `PASS` on a gated clause opened another on
#: the same clause.** So the declaration is anchored once and every target inside it is read.
#: **Anchored past the hyphen, which is the third pattern in this file to need it** —
#: `_LENGTH` and `_WIDTH_KEYWORD` both record the same lesson above. Unanchored,
#: `mask-src:` matched, so a remote image in a mask read as a third-party *font* and
#: refused the build: a false gate on a gated clause. Inherited rather than introduced —
#: it reproduces at `aeb643a`, before any of the 2026-09-07 work — and found by auditing
#: this pattern's own repair.
_REMOTE_DECLARATION = re.compile(r"(?:@import|(?<![-\w])src\s*:)([^;{}]*)",
                                 re.IGNORECASE)
_TARGET = re.compile(r"""url\(([^)]*)\)|["']([^"']*)["']""")
_SEPARATOR_NAMES = {" ": "space", " ": "U+2009", " ": "U+202F",
                    " ": "U+00A0", ",": "comma"}


@dataclass
class Finding:
    clause: str
    status: str
    detail: str


def _tile_classes(classes: set[str]) -> set[str]:
    return classes & {"kpi", "tile", "stat"}


def clause_1_tokens(page, css: str) -> list[Finding]:
    palettes = cssmod.palettes(css)
    light, dark = palettes["light"], palettes["dark"]

    if not light:
        return [Finding("1 tokens", FAIL, "no custom properties declared at all")]

    missing = [name for name in HOUSE_TOKENS if name not in light]
    findings = [Finding(
        "1 tokens",
        PASS if not missing else FAIL,
        f"{len(light)} declared" + (f"; missing {', '.join(missing)}" if missing else ""),
    )]

    findings.append(Finding(
        "1 dark",
        PASS if dark != light else FAIL,
        "prefers-color-scheme override present" if dark != light else "no dark override",
    ))

    findings += _unusable_values(palettes)

    for scheme, pins in PINNED.items():
        for token, expected in pins.items():
            actual = palettes[scheme].get(token)
            if actual is None:
                findings.append(Finding(f"1 {scheme} --{token}", NOT_APPLICABLE, "not declared"))
            elif actual.lower() == expected:
                findings.append(Finding(f"1 {scheme} --{token}", PASS, actual))
            else:
                ground = palettes[scheme].get("bg", "#ffffff")
                measurable = colour.is_opaque_hex(actual) and colour.is_opaque_hex(ground)
                against = (f" ({colour.contrast(actual, ground):.2f}:1 on --bg)"
                           if measurable else "")
                findings.append(Finding(
                    f"1 {scheme} --{token}", FAIL,
                    f"{actual}{against}; spec pins {expected}",
                ))
    return findings


def _fallback_argument(value: str, start: int) -> str | None:
    """The fallback of the `var(` opening at `start`, balanced to its own closing paren.

    `None` when that `var()` has no comma at its own depth — which is the only shape CSS
    discards when the token is undeclared. Anything else is painted, whatever its type, so
    this returns the text rather than judging it: a fallback the reader cannot measure is
    `_unusable_values`' UNDECIDED to give, not this function's FAIL.
    """
    depth, comma = 0, -1
    for index in range(start, len(value)):
        char = value[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                if comma < 0:
                    return None
                argument = value[comma + 1:index].strip()
                return argument or None
        elif char == "," and depth == 1 and comma < 0:
            comma = index
    return None


def _resolve_chain(name: str, palette: dict[str, str]) -> tuple[str | None, str]:
    """The value a role finally paints, and — when there is none — *why* there is none.

    Returns `(value, "")` when CSS keeps the declaration, and `(None, reason)` when CSS
    discards it: `_CYCLE` for a cycle of any length, `_DANGLING` for a reference to a token
    nothing declares. Both are invalid at computed-value time.

    **The terminal value comes back whatever its type.** An earlier draft returned only an
    opaque hex, which made an alias ending at a length or a font stack indistinguishable from
    one ending nowhere: `--radius: var(--card-radius)` and `--mono: var(--stack)` both
    reported `resolves to nothing`. `0008` S7 migrates `--ink`/`--line` and `wroclaw`'s absent
    `--radius` — exactly those two shapes — so the instrument is repaired *before* the stage
    that leans on it. Repairing it inside that stage is the mechanism of §3.2.

    **The reason is carried rather than re-derived by the caller.** A caller inspecting the
    declared value can only see a *direct* self-reference, so `--a: var(--b); --b: var(--a)`
    was reported as a dangling reference — the right verdict under the wrong sentence, which
    is the one thing this package is not allowed to print.
    """
    seen: set[str] = set()
    value = palette.get(name)
    if value is None:
        return None, _DANGLING
    first = True
    while True:
        reference = _VAR_NAME.search(value)
        if reference is None:
            return value.strip(), ""
        target = reference.group(1).lstrip("-")
        if target == name:
            # `--border: var(--border)` is the defect this whole clause exists for, and it
            # earns its own sentence. Reaching the same name after a hop is a mutual cycle,
            # which is a different thing to say.
            return None, _SELF if first else _CYCLE
        if target in seen:
            return None, _CYCLE
        seen.add(target)
        first = False
        if target not in palette:
            # `var(--brand, #2563eb)` paints the fallback when the token is undeclared, so a
            # value with a fallback is usable even though its first hop goes nowhere — and
            # the fallback need not be a hex. `var(--stack, monospace)` is painted too, and
            # calling it a dangling reference is the confident wrong sentence over a wrong
            # verdict. The scan is anchored at *this* `var(`, not searched across the whole
            # value: a second `var()` later in the same declaration has its own fallback and
            # is not this one's.
            fallback = _fallback_argument(value, reference.start())
            return (fallback, "") if fallback else (None, _DANGLING)
        value = palette[target]


def _unusable_values(palettes: dict[str, dict[str, str]]) -> list[Finding]:
    """A declared property that CSS will discard, and a colour role that is not a colour.

    Presence is not usability, and the distance between them let a real defect through: a
    find-and-replace that wrote `--border: var(--border)` left every token *present*, so the
    clause reported the page clear while CSS discarded both properties as a cycle.

    **The cycle test runs over every declared property, not only the colour roles.** A
    self-reference is unusable whatever the value's type, and the same accident lands just as
    easily on `--radius: var(--radius)` — which `.card` and `.kpi` both paint. Gating the
    cycle test on `COLOUR_ROLES` reproduced the original defect one role to the left.
    """
    findings: list[Finding] = []
    light = palettes["light"]
    for scheme, palette in palettes.items():
        for name, value in palette.items():
            # Report the dark row only where dark actually overrode: the dark palette starts
            # as a copy of light, so restating it doubles every finding and reads as a page
            # in twice the ruin it is.
            if scheme != "light" and palette.get(name) == light.get(name):
                continue
            resolved, reason = _resolve_chain(name, palette)
            if resolved is None:
                findings.append(Finding(f"1 {scheme} --{name} value", FAIL,
                                        f"{value} — {_DISCARDED[reason]}"))
            elif name in COLOUR_ROLES and not colour.is_opaque_hex(resolved):
                # A usable colour written in a notation this reader cannot parse is not a
                # defect, and calling it one would be the confident wrong verdict this
                # package exists to refuse.
                findings.append(Finding(
                    f"1 {scheme} --{name} value", UNDECIDED,
                    f"{value} — a colour notation this reader cannot measure"))
    return findings


def clause_1_composited(css: str) -> list[Finding]:
    """Usages whose painted value is not the declared one.

    Reported, never decided. Resolving these needs the ground each mark is *drawn over*, and
    paint order inside an SVG is not recoverable from the stylesheet alone — which is exactly
    what the `auth-log-scan` revert turned on: the band and the marks are siblings, and the
    band is still the marks' ground because it is painted first.
    """
    composited: list[str] = []
    for prop in ("background", "background-color", "fill", "stroke", "color"):
        for selector, value in cssmod.declarations(css, prop):
            if "color-mix(" in value:
                composited.append(f"{selector.strip()} {{{prop}: color-mix(...)}}")
    for selector, value in cssmod.declarations(css, "opacity"):
        try:
            if 0 < float(value.strip()) < 1:
                composited.append(f"{selector.strip()} {{opacity: {value.strip()}}}")
        except ValueError:
            continue
    if not composited:
        return []
    return [Finding("1 composited", UNDECIDED,
                    f"{len(composited)} usage(s) paint a value that is not the declared one; "
                    "resolve by paint order, not by nearest card")]


def _is_palette(selector: str) -> bool:
    """The blocks `cssmod.palettes` reads. Everything else in the sheet is a usage site."""
    return ":root" in selector or selector.strip() == "html"


def _unquoted(selector: str) -> str:
    """The selector with quoted strings removed, so `[data-state=":focus"]` is not a state."""
    return re.sub(r"([\"'])(?:(?!\1).)*\1", " ", selector)


def _declaration(body: str, prop: str) -> str | None:
    """One property's value out of a rule body, or `None`. Longhand names are exact, so
    `border` never matches `border-left` and `background` never matches `background-color`."""
    match = re.search(r"(?:^|;)\s*" + re.escape(prop) + r"\s*:\s*([^;}]+)", body,
                      re.IGNORECASE)
    return match.group(1).strip() if match else None


def _role_exception(selector: str, body: str, prop: str, role: str) -> str | None:
    """Which of the four measured shapes exempts this declaration, or `None`.

    Censused **at S3 close, before S4 tokenised `mlops-car-price` and `pl-jobs-lora`**, over the
    eleven published surfaces on disk and `wroclaw`'s own source. It is a dated snapshot rather
    than the current tree: S4 added conforming sites to both pages and two rails to
    `pl-jobs-lora`, so re-deriving it today gives larger numbers. The report prints a live role
    census on every run, which is where the current figure belongs. The snapshot: 141
    token-naming declarations in the two families, of which 11 are `color-mix()`
    and out of this walk. Of the 130 that remain, 112 already name the house role. Every one
    of the remaining eighteen is one of these four, and
    each is recognised by what the rule *does* rather than by its selector text, so a rename
    carries the exemption along instead of breaking it:

    * **a rail** (12) — `border-left: 3px solid var(--warn)` on seven `.card.caution`, four
      `--accent`/`--danger`/`--positive` rails in `car-price-ml/docs/app`, and `wroclaw`'s
      `.verdict`. A one-sided
      border thicker than a hairline, *in a role the house does not name*, is a semantic mark
      rather than the box's edge — `.result.pending` paints exactly that shape in `--border`
      and is an edge, which is why the thickness alone cannot carry this.
    * **a filled control** (3) — `button` twice and `.terminal .cursor`, each declaring
      `color` in the same rule *and* naming a role that is not one of the house three. A rule
      painting its own text in an accent has chosen a ground rather than inherited the page's.
    * **its own fill** (1) — `mini-traceroute`'s `button { border: 1px solid var(--accent) }`,
      whose border names the role its own `background` names two declarations above — again
      only where that shared role is not a house one.
    * **an interaction state** (2) — a `border-color` under `:hover`, `:focus` or `:active`
      in a role the house does not name. `car-price-ml/docs/app`'s `input:focus-visible` and
      `wroclaw`'s `nav.toc a:hover`, whose pill lights its border and its text together. The
      shape is a border that *signals* rather than encloses, and `:focus` was only ever the
      instance in front of the author: `wroclaw`'s appeared the moment its `--line` was
      renamed to `--border` and the clause could decide the family at all.

    **`role not in _HOUSE_ROLES` is on all four shapes, and it is the whole guard.** Without
    it every shape is a keyhole rather than an exception, because each one's condition is
    satisfied by the very declarations it was meant to distinguish itself *from* — and this
    sentence was written twice before it was true, once with the condition on two shapes and
    once with it on three:

    * swap `.card { background: var(--surface); border: 1px solid var(--border) }` to
      `var(--surface)` and the border now matches its own background — *"its own fill"* fires
      on the mutation;
    * `body { background: var(--bg); color: var(--text) }` declares a `color`, so any ground
      swapped there is a *"filled control"*;
    * `.result.pending { border-left: 3px solid var(--border) }` is a thick one-sided border,
      so swapping its role to a ground leaves it a *"rail"*.

    Swept declaration by declaration over the nine surfaces on disk that declare tokens — each
    conforming site mutated on its own, to the other family's house role — the guard takes the
    checker from **55 of 97 to 97 of 97**; over all twelve surfaces it is **112 of 112**.
    *The 31 reproduces only when a border site is mutated to **both** ground roles; to
    `--surface` alone it is 28, and a reader re-deriving it lands there and thinks the
    record is wrong.*
    Unguarded it misses 42 of the 97: **31 of 56** in the border family and **11 of 41** in the
    ground family. *The exemption census is unmoved by the guard either way*, because those
    sites name a non-house role today and this function is never consulted for the conforming
    ones — which is why the census cannot show the hole and the sweep can.

    **Three review passes were needed and each found one layer of it.** The first found two
    shapes keyed on a sibling declaration. The fix guarded three, leaving the rail: the sweep
    stood at 96 of 97, one live declaration, on the surface CI does not byte-diff. *That* fix
    guarded the rail and left the focus ring — no live declaration, so the sweep read 97 of
    97 and said so, while `input:focus-visible { border-color: var(--surface) }` passed.

    *A guard put on n−1 shapes of n is the same defect as no guard, narrowed. The sweep is
    what caught the third layer and could not catch the fourth, because no page writes that
    shape today — only reading the four branches against each other could, which is the
    argument for keeping them in one function where they can be read together.*

    `color-mix()` is not among them: `clause_1_composited` already reports those `undecided`,
    and `0007` §5 clause 1's *"the same fact twice"* is why they are not reported again.
    """
    if prop in _SIDE_BORDERS and role not in _HOUSE_ROLES:
        declared = _declaration(body, prop) or ""
        width = _LENGTH.search(declared)
        keyword = _WIDTH_KEYWORD.search(declared)
        pixels = (float(width.group(1)) * _PER_UNIT[width.group(2)] if width
                  else _WIDTH_KEYWORDS[keyword.group(1)] if keyword else None)
        if pixels is not None and pixels > 1:
            return "rail"
    if (prop in _GROUND_PROPERTIES and _declaration(body, "color")
            and role not in _HOUSE_ROLES):
        return "filled control"
    if prop in _BORDER_PROPERTIES:
        for ground in _GROUND_PROPERTIES:
            painted = _declaration(body, ground) or ""
            if (role in [name.lstrip("-") for name in _VAR_NAME.findall(painted)]
                    and role not in _HOUSE_ROLES):
                return "its own fill"
        if (prop == "border-color" and role not in _HOUSE_ROLES
                and _INTERACTION_STATE.search(_unquoted(selector))):
            return "interaction state"
    return None


def _usage_sites(css: str):
    """Every `(selector, body, property, role, scheme, fallback)` a token is painted at,
    outside `:root`.

    **Sites come light-half first, then dark**, rather than in source order: the two halves
    are walked separately. No caller depends on the order — `declarations()` is where source
    order is load-bearing, for paint order, and it is untouched — but a report truncating to
    the first few findings shows light-half ones first, and that is worth knowing rather than
    discovering.

    The scheme is carried because `rules()` drops the media condition by design, and one
    question needs it: a token only the dark `:root` declares is legitimately painted inside
    the dark block and is a dangling reference outside it. Admitting it everywhere would be
    a rule wider than the sentence licensing it — the shape this same review pass found in
    the focus ring, facing the other way.

    **A blind spot worth stating: this reads CSS rules, and a page can paint a token without
    writing one.** `wroclaw`'s `charts.py` substitutes token references into the SVG it emits
    as *presentation attributes* — `fill="var(--border)"` — which `cssmod.rules()` never sees.
    S7 renamed two of that page's tokens and left three such attributes pointing at names that
    no longer existed; this clause reported the page clean, and a sweep of the repository's
    tracked files is what found it. Reading attributes here would mean parsing the document
    rather than the stylesheet, which is a different instrument; until then, a rename in a
    repository that paints through attributes needs the sweep.

    **Every property, not only the two families the role rule speaks about.** A `var()` that
    names nothing is discarded by CSS whatever property it sits in, and `0008` §3.6's third
    example is `--radius` deleted while `.card` and `.kpi` still write
    `border-radius: var(--radius)` — a property no colour rule has an opinion about. Walking
    only the colour families would have left that example uncaught by the clause written to
    close it, which is the shape of the finding that blocked S3 in the first place.
    """
    light_css, dark_css = cssmod.split_schemes(css)
    for scheme, half in (("light", light_css), ("dark", dark_css)):
        for selector, body in cssmod.rules(half):
            if _is_palette(selector):
                continue
            for declaration in body.split(";"):
                prop, _, value = declaration.partition(":")
                prop = prop.strip().lower()
                if not prop or "var(" not in value or "color-mix(" in value:
                    continue
                for reference in _VAR_NAME.finditer(value):
                    # The fallback travels with the site. Computing it here rather than in the
                    # caller keeps the one paren-balancing scan in one place, and keeps a
                    # caller from re-searching the value and finding a *different* `var()`'s
                    # fallback — the shape the palette half already had.
                    yield (selector.strip(), body, prop, reference.group(1).lstrip("-"),
                           scheme, _fallback_argument(value, reference.start()))


def clause_1_usage(css: str) -> list[Finding]:
    """Clause 1 read at the usage sites rather than inside the token block.

    **This is the half both carriers were missing.** Every other clause-1 check reads `:root`,
    so a role swapped for another *declared* role is invisible to all of them: `apply-scout`
    shipped `border-bottom: 1px solid var(--surface)` where seven sibling pages write
    `var(--border)`, and reintroducing exactly that line left 300 repository tests green and
    this checker reporting the page `clear`. The same blind spot passes `--radius` deleted
    while `.card` and `.kpi` still paint it.

    Two findings, because they are two different claims and only one of them is contested:

    * **`1 usage refs`** — every `var()` names a token the palette holds and CSS keeps. No
      semantics and no threshold; a page failing this is broken however it names its roles.
    * **`1 usage roles`** — the role named is the role the property takes (§5 clause 1's
      fourth sentence), with `_role_exception`'s four measured shapes allowed.

    A page whose palette does not hold the house role at all — `wroclaw` writes `--line` for
    `--border` — reports **`undecided`, never `fail`**. `0008` S7 is the stage that renames
    those, and a checker calling a planned stage's starting state a defect turns S7's own
    targets red before S7 runs.
    """
    palettes = cssmod.palettes(css)
    palette = palettes["light"]
    # A site inside the dark block may legitimately paint a token only the dark `:root`
    # declares; the same reference in the light half is discarded by CSS. So the set a site is
    # checked against is its own scheme's, not the union. The role rule stays on light, which
    # is the scheme every page writes in full. No surface holds a dark-only token today; S7
    # rewrites nine palettes, which is when one could appear.
    declared = {"light": set(palette), "dark": set(palettes["dark"])}
    if not palette:
        # The hand-typed pages paint no token at all. `1 tokens` already names that, and a
        # second finding restating it is the doubling `1 dark` is written to avoid.
        return [Finding("1 usage refs", NOT_APPLICABLE, "no custom properties to paint with"),
                Finding("1 usage roles", NOT_APPLICABLE, "no custom properties to paint with")]

    broken: list[str] = []
    wrong: list[str] = []
    unnamed = False
    for selector, body, prop, role, scheme, fallback in _usage_sites(css):
        site = selector + " {" + prop + ": var(--" + role + ")}"
        if role not in declared[scheme]:
            # The same hole the palette half had, one level out: this branch did not consult
            # the fallback at all, so `.card { color: var(--brand, #2563eb) }` on an
            # undeclared `--brand` reported *undeclared* about a declaration CSS paints. It
            # is dead on today's corpus — `1 usage refs` is PASS on all eleven surfaces — so
            # repairing it moves nothing, which is the reason to repair it before S9 rewrites
            # five stylesheets rather than during.
            if fallback is None:
                broken.append(site + " — undeclared")
                continue
            # The reference is kept, and the role rule below still applies: naming a token
            # the palette does not declare for a ground or a border is not excused by having
            # somewhere to fall back to.
        else:
            resolved, reason = _resolve_chain(role, palettes[scheme])
            if resolved is None:
                broken.append(site + " — " + _DISCARDED[reason])
                continue
        if prop in _GROUND_PROPERTIES:
            allowed = _GROUND_ROLES
        elif prop in _BORDER_PROPERTIES:
            allowed = _BORDER_ROLES
        else:
            # Reference integrity is asked of every property; the role rule is not. `color`,
            # `fill` and `stroke` carry the portfolio's semantic palette by design, and
            # `border-radius` is a length. §5 clause 1's fourth sentence names two families
            # and this walks exactly those two.
            continue
        if role in allowed or _role_exception(selector, body, prop, role):
            continue
        if not allowed & set(palette):
            unnamed = True
            continue
        wrong.append(site + " — expected "
                     + "/".join("--" + one for one in sorted(allowed)))

    if broken:
        refs = Finding("1 usage refs", FAIL, str(len(broken)) + ": " + "; ".join(broken[:3]))
    else:
        refs = Finding("1 usage refs", PASS, "every var() at a usage site resolves")

    if wrong:
        roles = Finding("1 usage roles", FAIL, str(len(wrong)) + ": " + "; ".join(wrong[:3]))
    elif unnamed:
        roles = Finding("1 usage roles", UNDECIDED,
                        "a family's house role is not in this palette, so the sites naming "
                        "an alias cannot be compared; a naming item, and S7's starting state")
    else:
        roles = Finding("1 usage roles", PASS, "every token is painted in the role it names")
    return [refs, roles]


def clause_1_literals(css: str) -> Finding:
    """Clause 1's third sentence: *no literal hex outside the token block*.

    **The checker carried no such check at all.** The rule lived only in `apply-scout`'s own
    page test — one surface of twelve, and there only in the light half. The cause is
    structural rather than an oversight: `0007` §3 has no literals column, because it encodes
    literals-versus-tokens as a page-level binary, and this checker was composed from §3's
    columns rather than from §5's sentences.

    Both schemes are read. A literal inside the dark block is outside `:root` exactly as
    surely as one in the light half, and the dark half is the one nobody was looking at.
    """
    palette = cssmod.palettes(css)["light"]
    if not palette:
        return Finding("1 literals", NOT_APPLICABLE, "the page has no token block")
    outside: list[str] = []
    for selector, body in cssmod.rules(css):
        if _is_palette(selector):
            continue
        for literal in _HEX_LITERAL.findall(body):
            outside.append(selector.strip() + " {" + literal + "}")
    if outside:
        return Finding("1 literals", FAIL,
                       str(len(outside)) + " outside :root: " + "; ".join(outside[:3]))
    return Finding("1 literals", PASS, "no hex outside the token block")


def clause_2_tiles(page) -> Finding:
    tiles = _tile_classes(page.classes)
    if not tiles:
        return Finding("2 tiles", NOT_APPLICABLE, "no tiles; §5.1 fallback applies")
    if tiles == {"kpi"}:
        return Finding("2 tiles", PASS, ".kpi")
    return Finding("2 tiles", FAIL, ", ".join(sorted("." + name for name in tiles)))


def clause_3_tables(page, css: str) -> Finding:
    if page.unclosed:
        return Finding("3 tables", UNDECIDED,
                       f"{page.unclosed} element(s) never closed; ancestry unreliable")
    if not page.tables:
        return Finding("3 tables", NOT_APPLICABLE, "no tables")
    scrolling = cssmod.scrolling_classes(css)
    table_itself = cssmod.element_scrolls(css, "table")
    if not scrolling and not table_itself:
        return Finding("3 tables", FAIL, "no class in the stylesheet scrolls")

    # **A table with no wrapper is `undecided`, not silently `pass`.** `table_itself` is a
    # property of the sheet, and it used
    # to zero `unwrapped` for *every* table on the page: one bare `table { overflow-x: auto }`
    # anywhere — including inside a `@media` block, which `rules()` flattens by design — made
    # each table read as handled. The caveat was then attached to the *report* branch
    # (`table_itself and not named`), so a page holding both a named wrapper and the element
    # rule printed a flat `ok` while a table wearing neither was invisible.
    #
    # Not live: `table_itself` is False on all eleven committed surfaces, and `wroclaw` — the
    # only page with the rule — is fetch-only and reports `undecided` today because it has no
    # house scroller name. It becomes reachable the moment that name is given, which `0008` §5
    # carries as wanted-but-unscheduled, on the one surface with no committed HTML to diff.
    rest = [table for table in page.tables
            if not ((table[0] | table[1]) & scrolling)]
    # A table with no wrapper class is carried by the bare `table` rule if the sheet has one —
    # and whether that rule applies at this width is the thing the reader cannot know.
    by_the_element = rest if table_itself else []
    unwrapped = [] if table_itself else rest

    named = sorted(scrolling & set().union(*(own | anc for own, anc in page.tables)))
    wrappers = [f".{name}" for name in named] + (["the table itself"] if table_itself else [])
    detail = f"{len(page.tables)} table(s), scroller(s): {', '.join(wrappers) or 'none'}"
    if unwrapped:
        return Finding("3 tables", FAIL,
                       f"{detail}; {len(unwrapped)} with nothing that scrolls")
    if by_the_element:
        # Say so rather than print a bare ok — clause 4 already returns `undecided` for the
        # half it cannot judge, and this is the same refusal for the same kind of reason.
        return Finding("3 tables", UNDECIDED,
                       f"{detail}; {len(by_the_element)} rest on the bare `table` rule, "
                       "whose media condition is not read")
    return Finding("3 tables", PASS, detail)


#: Letters with no canonical decomposition, so NFKD leaves them whole and a
#: strip-the-combining-marks normaliser silently does nothing to them. **`ł` is the one that
#: matters and it is the one the obvious fix fails on**: `unicodedata.normalize("NFKD", "ł")`
#: is one character, so an NFKD-only fold would leave `wrocław` unequal to `wroclaw` — a guard
#: too weak to fail, on exactly the character that produced the finding. Measured 2026-09-07;
#: `đ` behaves the same way. The others are here because the same property holds of them and
#: a later page in another language would meet it, not because any surface uses them today.
_UNDECOMPOSED = str.maketrans({
    "ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ø": "o", "Ø": "O",
    "ß": "ss", "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE", "ħ": "h", "ŧ": "t",
})
_SEPARATORS = re.compile(r"[-_\s]+")


def _fold(text: str) -> str:
    """One spelling for a directory string and for the prose a page writes it as.

    `wroclaw-air-insights` and `Wrocław Air Insights` are the same identity under two
    encodings: a different letter, and hyphens where the prose has spaces. Fold the
    diacritics, treat the separators alike, and case-fold.
    """
    decomposed = unicodedata.normalize("NFKD", text.translate(_UNDECOMPOSED))
    unmarked = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return _SEPARATORS.sub(" ", unmarked).strip().casefold()


def _leads_with_the_projects_identity(title: str, repo: str) -> bool:
    """Clause 4's `<title>` half, read positionally and in both spellings.

    **The reading, settled 2026-09-07 and recorded in `tools/spec.py` at `c4.s3`.** The clause
    says the `<title>` *follows the `h1` rather than the directory*, and glosses its own reason:
    the two halves are *"different surfaces with different readers — the page, and the search
    result or the shared link."* **A search result shows a reader a name, never a directory**,
    so the directory string alone is the wrong comparison — `Wrocław Air Insights — live PM2.5
    forecast` commits precisely the failure the clause describes, to precisely the reader it
    names, and passed.

    Positional, because the alternative was measured and refuted: any reading that asks
    whether the name appears *anywhere* fails **11 of the 12** surfaces, since seven of the
    eight conforming titles are `<claim> — <repo>` and the name is a suffix. The house style
    is not the defect. *(Both figures were wrong when first written — 10 and eight — and both
    are recomputed by `python -m tools.pagespec --detail`. `apply-scout` is the one conforming
    title that carries the name nowhere at all.)*

    The match must end on a word boundary. Without that, `ab-lab` would lead `Ab labs are
    cheap` — a prefix of a longer word is not the name.

    **The honest limit, stated the way clause 3 states its checkable form**, and wider than
    a first draft of this paragraph said. Two shapes are not caught:

    - a *reworded* identity — `ReviewSense PL` for `pl-review-sense`;
    - the same words with the separators **deleted** rather than spaced — `DocExtract`,
      `AuthLogScan`, `MiniTraceroute`. `_fold` turns a separator into a space, so it cannot
      reach a spelling that has none, and this is a common way a project writes its own prose
      name. Swept over the twelve pinned pages: none uses one today, so the paragraph is
      about what this function claims rather than about a live gap.

    That is the same residual `4 h1` carries, and it is why this key can gate on the
    mechanical failure without claiming the semantic one.
    """
    # **One comparison, not two — and the reason is narrower than a first version claimed.**
    # An earlier revision also compared the raw directory string, and the comment said `_fold`
    # was *"a strict relaxation"* that subsumed it. That is true only of the raw comparison
    # **as this function had already written it**, with the word-boundary rule applied. It is
    # false of the comparison this replaced on `main`, which was a bare `startswith`:
    #
    #     repo `ab-lab`, title `ab-labs are cheaper`   ->  bare startswith: a lead
    #                                                      here:            not a lead
    #
    # `_fold` relaxes spelling — separators, diacritics, case — and the boundary rule
    # *restricts* at the match end, so the two moves go in opposite directions and neither
    # comparison contains the other. **The loosening is deliberate**: `ab-labs` is a different
    # word, not the project's name, and `main` failed that title. Stated because a reader who
    # believed the subsumption claim would think re-adding the raw comparison is a no-op, and
    # it is not — it would restore that `FAIL`.
    #
    # `needle` is empty only if `repo` folds to nothing, which `SURFACES` cannot produce; the
    # guard is here so a caller passing one gets `False` rather than every title matching.
    haystack, needle = _fold(title), _fold(repo)
    return bool(needle) and haystack.startswith(needle) \
        and not haystack[len(needle):][:1].isalnum()


def clause_4_opening(page, repo: str) -> list[Finding]:
    """Eyebrow, `h1` and `<title>` — clause 4 states all three, and §3 has a column each.

    Whether the `h1` *states a claim* stays `undecided` forever: §7 names it the one
    normative clause a checker cannot carry. Whether an eyebrow is present is not that, and
    leaving it out made the report claim "clauses 1-8" while silently dropping one of them.
    """
    headline = Finding(
        "4 h1", UNDECIDED if page.headline else FAIL,
        page.headline[:60] or "no <h1>",
    )
    # The same comparison as the `<title>` half, and clause 4's own words are why: it says
    # *not the repository's **name*** for the `h1` and *rather than the **directory*** for the
    # title, so if either half deserved the identity reading it was this one. It was left on
    # the raw directory string when the title half moved, which put the two halves of one
    # clause in disagreement about what the name is. Measured before changing it: both
    # comparisons are `False` on all twelve surfaces, so `4 h1` — which *is* in `GATED` —
    # cannot move on the corpus today.
    if page.headline and _fold(page.headline) == _fold(repo):
        headline = Finding("4 h1", FAIL, f"the repository's name: {page.headline}")
    leads_with_identity = _leads_with_the_projects_identity(page.title, repo)
    title = Finding(
        "4 title",
        FAIL if leads_with_identity or not page.title else PASS,
        (page.title[:60] or "no <title>")
        + (" (leads with the project's name)" if leads_with_identity else ""),
    )
    eyebrow = Finding(
        "4 eyebrow",
        PASS if "eyebrow" in page.classes else FAIL,
        "present" if "eyebrow" in page.classes else "no .eyebrow on the page",
    )
    return [eyebrow, headline, title]


def clause_5_card_meta(page) -> Finding:
    missing = [key for key in CARD_META if not page.meta(key)]
    favicon = any("icon" in link.get("rel", "").lower() for link in page.links)
    if not favicon:
        missing.append("favicon")
    if missing:
        return Finding("5 card meta", FAIL, "missing " + ", ".join(missing))
    return Finding("5 card meta", PASS, "all seven present")


def clause_6_back_link(page) -> Finding:
    # `endswith(PROFILE)` already excludes /issues, /pulls and every repository URL, so no
    # second filter is needed. Case-folded because GitHub URLs are not case-sensitive.
    # **Bounded at the host, not only at the suffix.** `endswith(PROFILE)` already excludes
    # `/issues`, `/pulls` and every repository URL, which is what its comment says — but it
    # also accepted `https://notgithub.com/P0w3r223`, because that ends in the same characters.
    # The clause is about a link back to the profile, and a different host is a different
    # profile. Compared on the parsed netloc so a subdomain cannot spoof it either.
    profile = PROFILE.lower()
    host, _, path = profile.partition("/")
    profile_only = []
    for href in page.anchors:
        parsed = urllib.parse.urlsplit(href.rstrip("/"))
        if parsed.netloc.lower() != host:
            continue
        if parsed.path.lstrip("/").lower() == path:
            profile_only.append(href)
    if len(profile_only) == 1:
        return Finding("6 back-link", PASS, profile_only[0])
    if not profile_only:
        return Finding("6 back-link", FAIL, "no link back to the profile")
    return Finding("6 back-link", FAIL, f"{len(profile_only)} links back; the clause asks for one")


def clause_7_webfont(page, css: str) -> Finding:
    """A third-party font request, by any of the three routes a page can make one.

    Reading `<link>` alone passes a page that reaches the same host through `@import` or a
    `@font-face` `src:` — and the complete stylesheet is already in hand from `sources`.
    """
    third_party = [link["href"] for link in page.links
                   if link.get("href", "").startswith(("http://", "https://", "//"))
                   and "font" in link.get("href", "").lower()]
    # Comments stripped first. `clause_1_literals` goes through `rules()` and therefore
    # already does; this read the raw sheet, so `/* never do this: @import url(...) */`
    # reported `FAIL 7 webfont` — and `"7 "` gates, so a comment refused the build.
    # Two groups now — `url(...)` and the bare-string spelling — so each match is a pair and
    # exactly one side of it is filled. A first version kept `.strip()` on the tuple.
    for declaration in _REMOTE_DECLARATION.findall(cssmod.strip_comments(css)):
        for parenthesised, quoted in _TARGET.findall(declaration):
            target = (parenthesised or quoted).strip().strip(chr(34)).strip(chr(39))
            if target.startswith(("http://", "https://", "//")):
                third_party.append(target)
    if third_party:
        return Finding("7 webfont", FAIL, ", ".join(sorted(set(third_party))))
    return Finding("7 webfont", PASS, "system stack")


def clause_8_separator(page) -> Finding:
    """The separator inventory of every grouped figure the page prints.

    **`n/a` means the page groups nothing, and that is the clause read as written.** §5 clause
    8 says *thousands are separated by U+202F*: its subject is how a grouped figure separates
    its thousands, so a page printing `1234` has no separator to be wrong about. The reading is
    stated here rather than left implicit because it leaves a real escape once `0008` S9 brings
    this clause into `GATED` — **deleting the grouping is a cheaper route to green than
    migrating to U+202F**, and nothing here would notice.

    That escape is a gap in the spec and not a defect in the checker, and closing it means §5
    gaining a sentence it does not have — *a figure of four or more digits is grouped* — which
    is an amendment to `0007` and not a change to this function. Recorded for whoever takes
    S9: the instrument implements the clause it was given, and says so.
    """
    counts: dict[str, int] = {}
    for _, tail in _GROUPED.findall(page.rendered_text):
        for character in tail:
            if character in _SEPARATOR_NAMES:
                counts[_SEPARATOR_NAMES[character]] = counts.get(
                    _SEPARATOR_NAMES[character], 0) + 1
    # The unit here is separator *characters*, which equals the figure count on every page
    # today because none prints a figure at or above a million. The first that does makes
    # this inventory non-comparable with §3, which counts figures.
    if not counts:
        return Finding("8 separator", NOT_APPLICABLE, "no grouped figure on the page")
    inventory = ", ".join(f"{name} {count}" for name, count in sorted(counts.items()))
    if set(counts) == {"U+202F"}:
        return Finding("8 separator", PASS, inventory)
    return Finding("8 separator", FAIL, inventory)


#: The two line endings, spelled by codepoint so no escape sequence appears in this file.
_CRLF, _LF = bytes([13, 10]), bytes([10])


def _lf(raw: bytes) -> bytes:
    """CRLF folded to LF. See `served_matches_committed` for why this is not cosmetic."""
    return raw.replace(_CRLF, _LF)


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()[:12]


def served_matches_committed(loaded) -> list[Finding]:
    """Does the public receive the **markup** this repository committed?

    **The markup, and not the whole surface.** Only the HTML is hashed. `mini-traceroute` and
    `car-price-ml/app` link an external same-origin sheet, and for those the CSS carrying
    clauses 1, 3 and 7 is outside this comparison — so `ok served` on them means the HTML
    matches, which is less than the question a reader would assume. Narrowed here rather than
    widened, because reading the assembled CSS from both sides is a larger change than this
    finding is, and a claim wider than the measurement is the defect this file exists to end.

    **This is not a clause.** `0007` §5 has nothing to say about it; it is the checker
    reporting on its own inputs, which is why it is emitted under a key no normative sentence
    claims and why `tools/spec.NOT_A_SENTENCE` names it. It is `0009` §3.1's C1, second half:
    nothing compared the served bytes to the committed ones, and `sources.py:7` stated the
    identity as fact while `0008` §6 carried it as a *manual* row.

    **Emitted only when there is something to compare**, and that silence is load-bearing
    rather than tidy. If this key appeared as `n/a` on the fetchless sweep, the ratchet's floor
    guard would see it clean-and-ungated and *demand* it in `GATED` on the first commit —
    forcing the gating decision before a single measurement exists. Staying out of that sweep
    is what lets it ship report-only and enter the gate under the ratchet's own rule.

    **One normalisation, and it is not cosmetic.** Line endings are folded on both sides
    because `core.autocrlf` rewrites the working-tree copy on Windows. Measured 2026-09-07:
    un-normalised, five of the eleven committed pages differ from what is served, and every
    one of the five differs *only* in line endings — the byte delta equals the file's CRLF
    count exactly. Without the fold this instrument reports five regressions on a developer's
    machine and none in CI, which is worse than not having it.
    """
    if loaded.served is None:
        if loaded.served_error is None or loaded.committed is None:
            return []
        # A page that answers 404 is gone, and that is a regression rather than a wire
        # failure. Every other exception is the network and must not read as a page changing.
        if loaded.served_gone:
            return [Finding("served", FAIL, f"the page is gone: {loaded.served_error}")]
        return [Finding("served", UNDECIDED, f"not read: {loaded.served_error}")]
    if loaded.committed is None:
        if loaded.surface.must_fetch or not loaded.repo_checked_out:
            # Two states that are not a missing page. `wroclaw` commits no HTML by design;
            # and a submodule nobody has initialised is a condition of the machine, which
            # `--fetch` meets every time it is run on a partial checkout.
            return []
        # **A gate that stopped firing, and this is where it fires again.** Before `--fetch`
        # read these eleven, a missing or renamed `docs/index.html` made `load` return `None`,
        # which the report counts as `missing` and refuses on. Now the wire answers instead —
        # and Pages keeps serving the last deployment — so a sibling deleting or renaming its
        # page would read `clear` and exit 0, indefinitely. `committed is None` conflated *no
        # file expected* with *the file is gone*, and only the surface knows which.
        return [Finding("served", FAIL,
                        "no committed page to compare: the file the eleven-surface sweep "
                        "reads is missing, and the wire is answering in its place")]
    served, committed = (_lf(loaded.served), _lf(loaded.committed))
    digests = f"markup: served {_digest(served)}, committed {_digest(committed)}"
    if served == committed:
        return [Finding("served", PASS, digests)]
    return [Finding("served", FAIL,
                    f"{digests} — either the pointer this repository holds is behind the "
                    f"public repository, or the publish is broken; "
                    f"`python -m tools.entry_state --full` is what tells the two apart")]


#: The clauses whose verdict is read out of the assembled stylesheet. Clauses 2, 4, 5, 6 and 8
#: read the markup and are unaffected by a sheet that could not be assembled.
#: `7 ` is deliberately absent: clause 7 reads `page.links` as well as the sheet, so a
#: dropped stylesheet does not excuse a third-party `<link>` sitting in the markup.
_CSS_DERIVED = ("1 ", "3 ")


def _undecided_where_the_stylesheet_is_incomplete(findings, loaded):
    """A clause cannot fail on a stylesheet it never read.

    **This is where a false gate was hiding after it was reported as removed.** Splitting
    *a sheet the network dropped* from *a sheet that is missing* took the wire off the
    stylesheet gate — and the run still refused, because `loaded.css` was empty and clause 1
    then reported `no custom properties declared at all` and clause 3 `no class in the
    stylesheet scrolls`, both of which **are** gated. The gate moved from a key naming the
    cause to two keys naming a consequence, and the output stopped mentioning the stylesheet
    at all. A daily blip refused the build under what reads as a portfolio-wide CSS regression.

    So the fix is not only to print the dropped sheet: it is that a clause reading an
    incomplete sheet has not earned a verdict. `0007` §7's whole argument, and this module's
    opening line — *a checker that reports a confident verdict it did not earn is that failure
    automated.* The gate for a sheet that is genuinely missing is unaffected: it lives in
    `_unread_same_origin`, under a header that names the cause.
    """
    # **A sheet declared third party is not read *by design*, and is not incomplete.**
    # `_unread_same_origin` filters that marker before gating and this did not — so a page
    # adding Google Fonts had every clause-1, -3 and -7 `FAIL` rewritten to `UNDECIDED`, and
    # `UNDECIDED` never gates. The repair for a false gate had made a false pass on the clause
    # whose entire subject is a third-party font.
    incomplete = [entry for entry in loaded.unreadable
                  if entry[1] != sources.THIRD_PARTY] + list(loaded.unreachable)
    if not incomplete:
        return findings
    why = ", ".join(sources.describe(entry) for entry in incomplete)
    return [
        Finding(one.clause, UNDECIDED,
                f"{one.detail} — not decided: the stylesheet is incomplete ({why})")
        if one.status == FAIL and one.clause.startswith(_CSS_DERIVED) else one
        for one in findings
    ]


def check(loaded) -> list[Finding]:
    """Every clause, over one loaded surface."""
    page = render.parse(loaded.html)
    findings = clause_1_tokens(page, loaded.css)
    findings += clause_1_usage(loaded.css)
    findings.append(clause_1_literals(loaded.css))
    findings += clause_1_composited(loaded.css)
    findings.append(clause_2_tiles(page))
    findings.append(clause_3_tables(page, loaded.css))
    findings += clause_4_opening(page, loaded.surface.repo)
    findings.append(clause_5_card_meta(page))
    findings.append(clause_6_back_link(page))
    findings.append(clause_7_webfont(page, loaded.css))
    findings.append(clause_8_separator(page))
    findings += served_matches_committed(loaded)
    findings = _undecided_where_the_stylesheet_is_incomplete(findings, loaded)
    if loaded.unreadable or loaded.unreachable:
        findings.append(Finding("stylesheets", UNDECIDED,
                                "unread: " + ", ".join(
                                    sources.describe(entry)
                                    for entry in list(loaded.unreadable)
                                    + list(loaded.unreachable))))
    return findings
