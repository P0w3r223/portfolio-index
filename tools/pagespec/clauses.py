"""The eight clauses of `0007` §5, as checks over one loaded surface.

Pure functions over already-read bytes: no file access, no network. What a clause cannot
decide, it says so rather than guessing — `0007` §7 exists because the instrument that
produced the original table was wrong three times, twice caught only by review, and a
checker that reports a confident verdict it did not earn is that failure automated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import colour, css as cssmod, render

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
#: with nothing numeric and no `:` or `.` touching either end. The bound is what makes this a
#: measurement — without it `07:00 203.0.113.42` scores as a grouped figure, which is how one
#: page was credited with nineteen it does not have. The separator class is spelled out
#: rather than using `\s`, because `\s` matches the newline `rendered_text` puts between
#: adjacent nodes and would weld two numbers back together.
_GROUPED = re.compile(
    r"(?<![\d.:])(\d{1,3})((?:[ \u202f\u00a0,](?:\d{3}))+)(?![\d.:])"
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
_LENGTH = re.compile(r"(\d+(?:\.\d+)?)px")
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

#: The token a `var()` names, and the literal a `var()` falls back to.
_VAR_NAME = re.compile(r"var\(\s*(--[\w-]+)")
_VAR_FALLBACK = re.compile(r"var\(\s*--[\w-]+\s*,\s*(#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?)\s*\)")

#: An `@import` or a `@font-face` `src:` pointing off-origin. Quotes are stripped by the
#: caller rather than matched here, which keeps the class free of quote characters.
_REMOTE_URL = re.compile(r"(?:@import|src\s*:)[^;{}]*?url\(([^)]*)\)", re.IGNORECASE)
_SEPARATOR_NAMES = {" ": "space", " ": "U+202F", " ": "U+00A0", ",": "comma"}


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
            # value with a literal fallback is usable even though its first hop goes nowhere.
            fallback = _VAR_FALLBACK.search(value)
            return (fallback.group(1), "") if fallback else (None, _DANGLING)
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
        width = _LENGTH.search(_declaration(body, prop) or "")
        if width and float(width.group(1)) > 1:
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
    """Every `(selector, body, property, role, scheme)` a token is painted at, outside `:root`.

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
                for name in _VAR_NAME.findall(value):
                    yield selector.strip(), body, prop, name.lstrip("-"), scheme


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
    for selector, body, prop, role, scheme in _usage_sites(css):
        site = selector + " {" + prop + ": var(--" + role + ")}"
        if role not in declared[scheme]:
            broken.append(site + " — undeclared")
            continue
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

    unwrapped = sum(1 for own, ancestors in page.tables
                    if not ((own | ancestors) & scrolling) and not table_itself)
    named = sorted(scrolling & set().union(*(own | anc for own, anc in page.tables)))
    wrappers = [f".{name}" for name in named] + (["the table itself"] if table_itself else [])
    detail = f"{len(page.tables)} table(s), scroller(s): {', '.join(wrappers) or 'none'}"
    if unwrapped:
        return Finding("3 tables", FAIL, f"{detail}; {unwrapped} with nothing that scrolls")
    if table_itself and not named:
        # The whole verdict rests on a rule this reader cannot width-scope: `rules()`
        # deliberately drops the media condition, so a scroller declared only under
        # `max-width: 640px` reads as scrolling everywhere. Say so rather than print a bare
        # ok — clause 4 already returns `undecided` for the half it cannot judge.
        return Finding("3 tables", UNDECIDED,
                       f"{detail}; no wrapper class, and the media condition is not read")
    return Finding("3 tables", PASS, detail)


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
    if page.headline and page.headline.strip().lower() == repo.lower():
        headline = Finding("4 h1", FAIL, f"the repository's name: {page.headline}")
    named_after_the_directory = page.title.strip().lower().startswith(repo.lower())
    title = Finding(
        "4 title",
        FAIL if named_after_the_directory or not page.title else PASS,
        (page.title[:60] or "no <title>")
        + (" (leads with the repository's name)" if named_after_the_directory else ""),
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
    profile = PROFILE.lower()
    profile_only = [href for href in page.anchors
                    if href.rstrip("/").lower().endswith(profile)]
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
    for target in _REMOTE_URL.findall(css):
        target = target.strip().strip(chr(34)).strip(chr(39))
        if target.startswith(("http://", "https://", "//")):
            third_party.append(target)
    if third_party:
        return Finding("7 webfont", FAIL, ", ".join(sorted(set(third_party))))
    return Finding("7 webfont", PASS, "system stack")


def clause_8_separator(page) -> Finding:
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
    if loaded.unreadable:
        findings.append(Finding("stylesheets", UNDECIDED,
                                "unread: " + ", ".join(loaded.unreadable)))
    return findings
