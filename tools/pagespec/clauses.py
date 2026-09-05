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

#: `0007` §5 clause 1 — the eight settled tokens, and the two the governing rule pins to the
#: *measured* value rather than the majority one.
HOUSE_TOKENS = ("bg", "surface", "border", "text", "muted", "accent", "warn", "radius")
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
#: An `@import` or a `@font-face` `src:` pointing off-origin. Quotes are stripped by the
#: caller rather than matched here, which keeps the class free of quote characters.
_REMOTE_URL = re.compile(r"(?:@import|src\s*:)[^;{}]*?url\(([^)]*)\)", re.I)
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
