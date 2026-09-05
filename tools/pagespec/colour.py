"""WCAG contrast arithmetic, and the two ways a stylesheet hides the value it paints.

Lifted from `pl-review-sense/tests/test_palette.py`, which had the whole of this working
before the spec existed. Two things are added here, and both are the reason `auth-log-scan`
was reverted from S1: a `color-mix()` reader, and the fact that a composited value has to be
resolved against the element it is *drawn over* rather than against the page.

Thresholds are WCAG 2.2. 4.5:1 for body-sized text (SC 1.4.3); 3:1 for a graphical object
that carries meaning (SC 1.4.11), which is also Level AA. Large text starts at 18.66 px bold
or 24 px regular, so 0.86 rem at weight 600 is *normal* text and takes the 4.5.
"""

from __future__ import annotations

# Only `contrast()` is on the checker's shipped path today. `resolve()` and `composite()`
# are the paint-order half of `0008` §3.2, built and tested ahead of the clause that will
# call them — so coverage here is not coverage of what the report prints.

import re

TEXT_MINIMUM = 4.5
GRAPHIC_MINIMUM = 3.0

#: `color-mix(in srgb, var(--x) 28%, transparent)` — the one form the portfolio uses.
_COLOR_MIX = re.compile(
    r"color-mix\(\s*in\s+srgb\s*,\s*var\(\s*(--[\w-]+)\s*\)\s+([\d.]+)%\s*,\s*transparent\s*\)",
    re.IGNORECASE,
)
_VAR = re.compile(r"var\(\s*(--[\w-]+)\s*\)")
_HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")


def rgb(value: str) -> tuple[float, float, float]:
    """The three channels of a 3- or 6-digit hex colour.

    **Four- and eight-digit hex carry alpha, and this refuses them rather than reading
    the first six digits.** `#aabbccdd` would otherwise return the same channels as
    `#aabbcc` and measure the same ratio, which is a confident wrong number about a
    colour that is in fact translucent; `#f00a` would raise deep inside a comprehension.
    Both forms are valid CSS Color 4 and are one edit away in any of these stylesheets.
    """
    if not is_opaque_hex(value):
        raise ValueError(
            f"{value!r} is not a 3- or 6-digit hex colour; alpha forms carry a "
            "transparency this cannot resolve without knowing what is underneath"
        )
    digits = value.strip().lstrip("#")
    if len(digits) == 3:
        digits = "".join(channel * 2 for channel in digits)
    return tuple(int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4))


def is_opaque_hex(value: str) -> bool:
    """Whether `rgb()` can read this value. Callers ask before measuring."""
    return bool(_HEX.fullmatch(value.strip()))


def luminance(colour: tuple[float, float, float]) -> float:
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in colour]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first: str, second: str) -> float:
    high, low = sorted((luminance(rgb(first)), luminance(rgb(second))), reverse=True)
    return (high + 0.05) / (low + 0.05)


def composite(top: str, bottom: str, alpha: float) -> str:
    """What the browser paints when `top` is drawn at `alpha` over `bottom`."""
    a, b = rgb(top), rgb(bottom)
    mixed = [alpha * a[i] + (1 - alpha) * b[i] for i in range(3)]
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in mixed)


def resolve(value: str, palette: dict[str, str]) -> tuple[str, float] | None:
    """The colour a declaration paints, and the alpha it paints it at.

    Returns `None` rather than guessing when the value names something this cannot resolve —
    a gradient, `currentColor`, a variable the palette does not hold. A checker that silently
    treated an unresolvable value as opaque black would report contrast failures nobody can
    act on, which is worse than reporting nothing.
    """
    value = value.strip()

    mix = _COLOR_MIX.search(value)
    if mix:
        token, percent = mix.group(1), float(mix.group(2)) / 100
        colour = palette.get(token.lstrip("-"))
        return (colour, percent) if colour else None

    var = _VAR.search(value)
    if var:
        colour = palette.get(var.group(1).lstrip("-"))
        return (colour, 1.0) if colour else None

    if "gradient" in value.lower():
        # A gradient has no single painted colour. Returning its first stop is a
        # confident wrong value, which is the class this whole package exists to stop.
        return None

    literal = _HEX.search(value)
    if literal:
        return (literal.group(0), 1.0)

    return None
