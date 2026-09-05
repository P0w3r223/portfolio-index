"""The page's complete stylesheet, and the four things the spec asks of it.

**Complete is the operative word.** `mini-traceroute` is the one page whose CSS is not
inlined, and reading only the `<style>` block recorded it wrongly for three sessions
(`0007` §2). Every function here takes CSS that a caller has already assembled from the
inline blocks *and* the same-origin `<link>`ed sheets.
"""

from __future__ import annotations

import re

_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_DARK_MEDIA = re.compile(r"@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{", re.IGNORECASE)
_CUSTOM_PROPERTY = re.compile(r"--([\w-]+)\s*:\s*([^;}]+)")
_OVERFLOW = re.compile(r"overflow(?:-x)?\s*:\s*(?:auto|scroll)", re.IGNORECASE)


def strip_comments(css: str) -> str:
    return _COMMENT.sub(" ", css)


def _balanced_block(css: str, opening_brace: int) -> tuple[str, int]:
    """The text between a `{` and its matching `}`, and the index just past that `}`.

    `@media` nests, so a non-greedy `\\{([^}]*)\\}` walks straight past the first inner rule
    and reports a fragment. Every earlier attempt in this portfolio used that pattern.
    """
    depth, index = 0, opening_brace
    while index < len(css):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[opening_brace + 1:index], index + 1
        index += 1
    return css[opening_brace + 1:], len(css)


def rules(css: str) -> list[tuple[str, str]]:
    """Every `selector { body }` pair, including those inside `@media`, flattened.

    The selector keeps its own text only; which media query it sat under is not carried,
    because no clause asks and pretending otherwise would invite a caller to trust it.
    """
    css = strip_comments(css)
    found: list[tuple[str, str]] = []
    index = 0
    while True:
        brace = css.find("{", index)
        if brace == -1:
            return found
        selector = css[index:brace].strip()
        body, index = _balanced_block(css, brace)
        if selector.startswith("@"):
            found.extend(rules(body))
        else:
            found.append((selector, body))


def split_schemes(css: str) -> tuple[str, str]:
    """The stylesheet minus every `prefers-color-scheme: dark` block, and those blocks alone.

    **The two halves are a partition**: every rule in the sheet appears in exactly one of them,
    once. `palettes()` only ever asked about `:root`, so it never depended on that; a usage
    site does, and `tests/test_css.py` now asserts it directly rather than through `palettes`.

    Extracted so a caller can ask *which half a rule is in*, which `rules()` deliberately does
    not carry — it drops the media condition, and pretending otherwise would invite a caller to
    trust it. A usage site needs the answer for exactly one question: whether a token declared
    only in the dark `:root` is legitimately painted there, or is a dangling reference in the
    light half where CSS discards it.
    """
    css = strip_comments(css)
    dark_css, light_css, index = "", "", 0
    for match in _DARK_MEDIA.finditer(css):
        if match.start() < index:
            # A dark query nested inside one already excised. `finditer` resumes just past
            # the opening brace rather than past the block, so without this the inner match
            # is taken a second time and `index` is rewound *behind itself* — the inner rules
            # are emitted twice, the outer block's remaining rules land in both halves, and
            # the rewound tail carries the outer `}` into the next selector.
            continue
        body, after = _balanced_block(css, match.end() - 1)
        light_css += css[index:match.start()]
        dark_css += body
        index = after
    return light_css + css[index:], dark_css


def palettes(css: str) -> dict[str, dict[str, str]]:
    """The light and dark custom properties, as the browser resolves them.

    Light is every `:root` outside a dark media query. Dark starts as a copy of light and is
    overwritten by the `prefers-color-scheme: dark` block, which is how these stylesheets are
    written — dark restates only what it changes.

    **The dark block is excised whole, not by its header.** A `re.sub` on the `@media ... {`
    match removes the header and leaves the body behind, so every dark declaration leaks into
    the light palette and overwrites it — which reports the dark value as the light one and
    then says there is no dark override, because the two palettes came out identical.
    """
    light_css, dark_css = split_schemes(css)

    light: dict[str, str] = {}
    for selector, body in rules(light_css):
        if ":root" in selector or selector.strip() == "html":
            light.update(_declared(body))

    dark = dict(light)
    for selector, body in rules(dark_css):
        if ":root" in selector or selector.strip() == "html":
            dark.update(_declared(body))

    return {"light": light, "dark": dark}


def _declared(body: str) -> dict[str, str]:
    return {name: value.strip() for name, value in _CUSTOM_PROPERTY.findall(body)}


def scrolling_classes(css: str) -> set[str]:
    """Every class the stylesheet gives a horizontal scrollbar.

    Read out of the CSS rather than named, so renaming the wrapper carries the check along
    instead of breaking it — `apply-scout`'s reasoning, kept.
    """
    classes: set[str] = set()
    for selector, body in rules(css):
        if _OVERFLOW.search(body):
            classes.update(re.findall(r"\.([\w-]+)", selector))
    return classes


def declarations(css: str, prop: str) -> list[tuple[str, str]]:
    """Every `selector, value` pair declaring `prop`, in source order.

    Source order is what makes paint order recoverable, and paint order is what the
    `auth-log-scan` revert turned on: a mark is drawn over the band, so the band is its
    ground even though the two are siblings.
    """
    found: list[tuple[str, str]] = []
    pattern = re.compile(rf"(?:^|;)\s*{re.escape(prop)}\s*:\s*([^;}}]+)", re.IGNORECASE)
    for selector, body in rules(css):
        for value in pattern.findall(body):
            found.append((selector, value.strip()))
    return found


def element_scrolls(css: str, element: str) -> bool:
    """Whether a bare element selector is itself given a scrollbar.

    `wroclaw-air-insights` writes `table { overflow-x: auto }` under `max-width: 640px`, which
    makes the table its own scroller and leaves it with no scrolling *ancestor* at all. That
    is the fourth mechanism `0007` §2 names, and it is the one that broke `measure_page.py`
    twice — a walk that starts at the table's parent cannot see it.
    """
    for selector, body in rules(css):
        if not _OVERFLOW.search(body):
            continue
        for part in selector.split(","):
            part = part.strip()
            if part == element or part.endswith(f" {element}"):
                return True
    return False
