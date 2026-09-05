"""WCAG arithmetic, checked against the ratios `0007` §4.1 wrote down.

Every expected value here is quoted from the **normative** part of the spec, not measured
off a page — `0007` §5 clause 1 and §4.1 are accepted rules with their ratios printed beside
the values, and `ADR-0004` §5 records that they are the stable half of that document. So
these are characterisation tests against a frozen source: they cannot be invalidated by a
page being edited, and if one ever disagrees, either the arithmetic drifted or the spec was
mis-transcribed, and both are worth stopping for.

The whole reason this half exists is that these two splits are **measured accessibility
fixes** that reached some pages and not others. A checker that quietly got the arithmetic
wrong would recommend reverting them.
"""

from __future__ import annotations

import pytest

from tools.pagespec import colour

# `0007` §4.1: the light and dark grounds these tokens are painted on.
LIGHT_BG, LIGHT_SURFACE = "#ffffff", "#f6f8fa"
DARK_BG, DARK_SURFACE = "#0f1319", "#161c25"


@pytest.mark.parametrize("value, ground, expected, note", [
    ("#5b93e4", LIGHT_BG, 3.12, "the measured light --accent-soft, which clears the 3:1 mark"),
    ("#93c5fd", LIGHT_BG, 1.80, "the majority light --accent-soft, which does not"),
    ("#4167a6", DARK_BG, 3.30, "the measured dark --accent-soft"),
    ("#2c4a7c", DARK_BG, 2.11, "the majority dark --accent-soft, live on five pages"),
    ("#047857", LIGHT_BG, 5.48, "the measured --positive, as text on --bg"),
    ("#047857", LIGHT_SURFACE, 5.15, "the measured --positive, as text on --surface"),
    ("#059669", LIGHT_BG, 3.77, "the majority --positive: clears 3:1 as a mark, fails as text"),
    ("#059669", LIGHT_SURFACE, 3.54, "the same, on the other ground a page paints on"),
    ("#34d399", DARK_SURFACE, 8.90, "dark --positive, uniform and safe"),
    ("#34d399", DARK_BG, 9.69, "dark --positive, on the other ground"),
    ("#dbe7ff", LIGHT_BG, 1.24, "wroclaw's third --accent-soft, declared and never painted"),
    ("#1e2c45", DARK_BG, 1.33, "the dark half of the same"),
])
def test_the_ratio_the_spec_records_is_the_ratio_the_arithmetic_produces(
        value, ground, expected, note):
    assert round(colour.contrast(value, ground), 2) == expected, note


def test_contrast_does_not_depend_on_which_colour_is_named_first():
    """The formula sorts by luminance, so ink-on-paper and paper-on-ink are one ratio."""
    assert colour.contrast("#1c2430", "#ffffff") == colour.contrast("#ffffff", "#1c2430")


@pytest.mark.parametrize("pair", [("#ffffff", "#000000"), ("#fff", "#000")])
def test_the_extremes_land_on_the_values_wcag_defines(pair):
    assert round(colour.contrast(*pair), 2) == 21.0


def test_a_colour_contrasted_with_itself_is_one_to_one():
    assert colour.contrast("#2563eb", "#2563eb") == pytest.approx(1.0)


def test_a_three_digit_hex_is_the_six_digit_one_it_abbreviates():
    """Shorthand appears in hand-written pages; read channel-by-channel it is a wrong colour."""
    assert colour.rgb("#fff") == colour.rgb("#ffffff")
    assert colour.rgb("#5b9") == colour.rgb("#55bb99")


def test_the_thresholds_are_the_ones_wcag_states():
    """0.86 rem at weight 600 is ~13.8 px, which is *normal* text — large starts at 18.66 px
    bold — so `mini-traceroute`'s `.probe-ok` takes 4.5 and not 3."""
    assert (colour.TEXT_MINIMUM, colour.GRAPHIC_MINIMUM) == (4.5, 3.0)


# -- compositing: what the browser paints, not what the stylesheet declares -----------------


def test_a_fully_opaque_top_layer_is_the_top_layer():
    assert colour.composite("#2563eb", "#ffffff", 1.0) == "#2563eb"


def test_a_fully_transparent_top_layer_is_the_ground():
    assert colour.composite("#2563eb", "#ffffff", 0.0) == "#ffffff"


def test_a_partly_transparent_mark_is_neither_of_its_two_colours():
    """`color-mix(in srgb, var(--accent) 28%, transparent)` over white is not `--accent`.

    Judging such a mark by its declared value is how a page passes a contrast check it fails
    on screen — the reason `auth-log-scan` was reverted from S1.
    """
    painted = colour.composite("#2563eb", "#ffffff", 0.28)
    assert painted == "#c2d3f9"
    assert colour.contrast(painted, "#ffffff") < colour.contrast("#2563eb", "#ffffff")


def test_the_ground_a_mark_is_drawn_over_changes_the_answer():
    """`0008` §3.2: the band and the marks are siblings, and the band is painted first, so
    the band is the marks' ground. Resolving against the page instead gives a different
    number — which is the third constraint that revert put on this checker."""
    over_band = colour.composite("#2563eb", "#eef1f6", 0.28)
    over_page = colour.composite("#2563eb", "#ffffff", 0.28)
    assert over_band != over_page


# -- resolution: what a declaration paints, or an honest refusal ----------------------------


PALETTE = {"accent": "#2563eb", "accent-soft": "#93c5fd", "bg": "#ffffff"}


@pytest.mark.parametrize("value, expected", [
    ("color-mix(in srgb, var(--accent) 28%, transparent)", ("#2563eb", 0.28)),
    ("color-mix(in srgb, var(--accent-soft) 100%, transparent)", ("#93c5fd", 1.0)),
    ("var(--accent)", ("#2563eb", 1.0)),
    ("  var( --accent )  ", ("#2563eb", 1.0)),
    ("#047857", ("#047857", 1.0)),
    ("1px solid #e3e7ee", ("#e3e7ee", 1.0)),
])
def test_a_value_this_can_resolve_comes_back_with_its_alpha(value, expected):
    assert colour.resolve(value, PALETTE) == expected


@pytest.mark.parametrize("value", [
    "currentColor",
    "var(--specialist)",
    "transparent",
    "",
])
def test_a_value_this_cannot_resolve_is_refused_rather_than_guessed(value):
    """Treating an unresolvable value as opaque black would report contrast failures nobody
    can act on, which is worse than reporting nothing — `0007` §7's rule, in code."""
    assert colour.resolve(value, PALETTE) is None


def test_a_gradient_is_refused_rather_than_read_as_its_first_stop():
    """`_HEX.search` finds `#2563eb` inside `linear-gradient(#2563eb, #93c5fd)`.

    A gradient has no single painted colour, so the first stop is not the answer — it is a
    plausible-looking one, which is worse. The docstring on `resolve` already says so.
    """
    assert colour.resolve("linear-gradient(#2563eb, #93c5fd)", PALETTE) is None


def test_a_mix_is_preferred_over_the_bare_variable_inside_it():
    """`color-mix(...)` contains `var(...)`; reading the variable first would drop the alpha
    and report the mark at full strength, which is exactly the value it is not painted at."""
    resolved = colour.resolve("color-mix(in srgb, var(--accent) 28%, transparent)", PALETTE)
    assert resolved == ("#2563eb", 0.28)
    assert resolved[1] != 1.0


@pytest.mark.parametrize("value", ["#f00a", "#aabbccdd", "#12345", "", "rebeccapurple"])
def test_a_colour_this_cannot_read_is_refused_rather_than_truncated(value):
    """4- and 8-digit hex carry alpha, and reading the first six digits is the worst
    available answer: `#aabbccdd` would measure exactly what `#aabbcc` measures, so a
    translucent colour reports the ratio of an opaque one and nothing looks wrong."""
    assert not colour.is_opaque_hex(value)
    with pytest.raises(ValueError):
        colour.rgb(value)


@pytest.mark.parametrize("value", ["#abc", "#aabbcc", "#FFFFFF", " #abc "])
def test_the_two_forms_it_can_read_are_accepted(value):
    assert colour.is_opaque_hex(value)
    assert len(colour.rgb(value)) == 3


def test_the_short_form_expands_to_the_long_one():
    assert colour.rgb("#abc") == colour.rgb("#aabbcc")
