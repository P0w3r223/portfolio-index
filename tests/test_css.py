"""The stylesheet, and the two shapes that made it answer confidently and wrongly.

Both are structural rather than arithmetic, and both are invisible in the output: a dark
block excised by its header alone reports the dark value as the light one *and* then reports
no dark override, because the two palettes came out identical. There is no error and no
missing field — just a table of wrong colours.
"""

from __future__ import annotations

import pytest

from conftest import fixture
from tools.pagespec import css as cssmod

HOUSE_LIGHT = {"bg": "#ffffff", "surface": "#f6f8fa", "border": "#e3e7ee", "text": "#1c2430",
               "muted": "#5b6472", "accent": "#2563eb", "warn": "#b45309", "radius": "10px"}


# -- defect 3: the dark block is excised whole, not by its header --------------------------


def test_a_dark_override_does_not_leak_into_the_light_palette():
    """`re.sub` on the `@media ... {` match removes the header and leaves the body behind.

    Every dark declaration then lands in `light` and overwrites it. Both halves of the damage
    are asserted, because either one alone would still look plausible in the report.
    """
    palettes = cssmod.palettes(
        ":root { --bg: #ffffff; --text: #1c2430; }"
        "@media (prefers-color-scheme: dark) { :root { --bg: #0f1319; --text: #e6eaf2; } }"
    )
    assert palettes["light"]["bg"] == "#ffffff", "a dark declaration leaked into light"
    assert palettes["dark"]["bg"] == "#0f1319"
    assert palettes["light"] != palettes["dark"], "the two palettes collapsed into one"


def test_the_recorded_house_stylesheet_resolves_to_two_distinct_palettes():
    """The doc-extract reduction — the eight settled tokens and the two that split."""
    palettes = cssmod.palettes(fixture("house_palette.css"))
    assert {name: palettes["light"][name] for name in HOUSE_LIGHT} == HOUSE_LIGHT
    assert palettes["dark"]["accent-soft"] == "#2c4a7c"
    assert palettes["dark"]["radius"] == "10px", (
        "--radius does not vary by scheme, so dark inherits it from light"
    )


def test_dark_restates_only_what_it_changes_and_inherits_the_rest():
    """These stylesheets never repeat the whole palette in the dark block."""
    palettes = cssmod.palettes(
        ":root { --bg: #ffffff; --radius: 10px; }"
        "@media (prefers-color-scheme: dark) { :root { --bg: #0f1319; } }"
    )
    assert palettes["dark"] == {"bg": "#0f1319", "radius": "10px"}


def test_a_dark_block_containing_a_nested_query_is_still_excised_whole():
    """`@media` nests, and `\\{([^}]*)\\}` stops at the first inner `}`.

    A non-greedy match would end the dark block early and hand its tail — here a light-looking
    `:root` — back to the light palette.
    """
    palettes = cssmod.palettes(
        ":root { --bg: #ffffff; }"
        "@media (prefers-color-scheme: dark) {"
        "  :root { --bg: #0f1319; }"
        "  @media (max-width: 640px) { :root { --bg: #000000; } }"
        "}"
    )
    assert palettes["light"]["bg"] == "#ffffff"
    assert palettes["dark"]["bg"] == "#000000"


def test_a_page_that_declares_nothing_reports_an_empty_light_palette():
    """Clause 1 turns this into one honest failure; a crash or a default would not."""
    assert cssmod.palettes("body { color: #1c2430; }") == {"light": {}, "dark": {}}


def test_a_comment_carrying_a_declaration_is_not_a_declaration():
    """Two published pages carry the `--accent-soft` reason in a comment beside the value.

    A commented-out token read as declared would report a page as holding a value it does not
    ship — the same confident wrong number, from the other direction.
    """
    # The comment sits **after** the live declaration on purpose. With it above, dict
    # last-wins returns the right answer whether or not comments are stripped, so the
    # test passes against a `strip_comments` that does nothing — which it did.
    palettes = cssmod.palettes(
        ":root { --accent-soft: #5b93e4; /* was #93c5fd, 1.80:1 */ }"
    )
    assert palettes["light"]["accent-soft"] == "#5b93e4"


def test_a_commented_out_rule_does_not_contribute_a_scrolling_class():
    """Stripping is load-bearing for the block walker, not only for declarations.

    Unstripped, `/* .a { overflow-x: auto } */ .b { color: red }` splits into selectors
    `/* .a` and `*/ .b`, so `.a` is harvested as a scrolling class out of a rule the page
    does not ship — a false green on clause 3. `mini-traceroute` already carries a
    top-level comment of this shape.
    """
    css = "/* .scroll-x { overflow-x: auto } */ .wrap { color: red }"
    assert cssmod.scrolling_classes(css) == set()


def test_a_comment_containing_braces_does_not_unbalance_the_walker():
    css = "/* } stray brace { */ .wrap { overflow-x: auto }"
    assert cssmod.scrolling_classes(css) == {"wrap"}


def test_a_custom_property_outside_root_is_not_counted_as_a_house_token():
    """The `:root`/`html` restriction is what makes the count §3's tokens column holds.

    Without it, a component declaring its own two properties reads as a page declaring
    twelve house tokens where it declares ten.
    """
    palettes = cssmod.palettes(
        ":root { --bg: #ffffff; } .card { --pad: 12px; --gap: 8px; }")
    assert palettes["light"] == {"bg": "#ffffff"}


# -- the block walker ---------------------------------------------------------------------


def test_a_rule_inside_a_media_query_is_flattened_out_whole():
    """`@media` bodies are recursed into, and the inner rule keeps its whole body."""
    assert cssmod.rules("@media (max-width: 640px) { .a { color: red; background: blue } }") == \
        [(".a", " color: red; background: blue ")]


def test_the_second_rule_in_a_media_query_is_not_swallowed_by_the_first():
    """The failure mode of `\\{([^}]*)\\}`: the walk ends at the first inner `}`."""
    found = cssmod.rules("@media screen { .a { color: red } .b { overflow-x: auto } }")
    assert [selector for selector, _ in found] == [".a", ".b"]


def test_an_unbalanced_stylesheet_yields_what_it_has_rather_than_nothing():
    """A truncated sheet is a fetch that went wrong; reporting no rules would read as a page
    with no CSS, which is a portfolio-wide false failure rather than one unread file."""
    assert cssmod.rules(".a { overflow-x: auto") == [(".a", " overflow-x: auto")]


# -- what the clauses ask of the sheet -----------------------------------------------------


def test_every_class_given_a_scrollbar_is_named_however_the_page_spells_it():
    """Read out of the CSS rather than named, so a rename carries the check along."""
    assert cssmod.scrolling_classes(
        ".table-wrap, .chart-wrap { overflow-x: auto }"
        ".ledger-wrap { max-height: 20rem; overflow: auto }"
        ".card { overflow: hidden }"
    ) == {"table-wrap", "chart-wrap", "ledger-wrap"}


def test_the_table_can_be_its_own_scroller():
    """`wroclaw` writes `table { overflow-x: auto }` under `max-width: 640px`.

    The table then has no scrolling *ancestor* at all, which is why a walk starting at its
    parent cannot see it — the trap that broke `measure_page.py` twice.
    """
    assert cssmod.element_scrolls(fixture("wroclaw_scroller.css"), "table") is True


def test_a_wrapper_class_whose_name_contains_the_element_is_not_the_element():
    """`.table-wrap` must not read as `table`.

    A substring match here would make every table in the portfolio its own scroller, and
    clause 3 would pass every page — the largest single false green available.
    """
    assert cssmod.element_scrolls(".table-wrap { overflow-x: auto }", "table") is False
    assert cssmod.element_scrolls(".table { overflow-x: auto }", "table") is False


def test_a_descendant_selector_still_names_the_element_it_ends_with():
    assert cssmod.element_scrolls(".card table { overflow-x: auto }", "table") is True


def test_an_element_given_only_a_vertical_scrollbar_is_not_a_horizontal_scroller():
    assert cssmod.element_scrolls("table { overflow-y: auto }", "table") is False


@pytest.mark.parametrize("value, scrolls", [
    ("auto", True), ("scroll", True), ("hidden", False), ("clip", False), ("visible", False),
])
def test_only_auto_and_scroll_give_somewhere_to_scroll(value, scrolls):
    """A box that clips is the case `0007` §2 names: an outer scroller with nothing left."""
    assert bool(cssmod.scrolling_classes(f".w {{ overflow-x: {value} }}")) is scrolls


def test_declarations_are_returned_in_source_order():
    """Source order is what makes paint order recoverable, and paint order is what the
    `auth-log-scan` revert turned on: a mark drawn over a band has the band as its ground."""
    assert cssmod.declarations(
        ".band { fill: #eef1f6 } .mark { fill: #2563eb } .mark.served { fill: #047857 }", "fill"
    ) == [(".band", "#eef1f6"), (".mark", "#2563eb"), (".mark.served", "#047857")]


def test_a_longer_property_that_ends_with_the_one_asked_for_is_not_it():
    """`background-color` read as `color` would resolve every card's ground as its ink."""
    assert cssmod.declarations(".a { background-color: #f6f8fa; color: #1c2430 }", "color") == \
        [(".a", "#1c2430")]


def test_the_media_query_a_rule_sat_under_is_deliberately_not_carried():
    """A known widening, pinned so that narrowing it later is a decision rather than a drift.

    `rules()` flattens `@media` and drops the condition, so a scroller declared only at phone
    widths reads as scrolling everywhere. `0007` §3.1 measured the geometry separately at five
    widths and found nothing unhandled, which is what makes the widening affordable — the
    static half checks the mechanism exists, not the width at which it engages.
    """
    css = "@media (min-width: 1200px) { .table-wrap { overflow-x: auto } }"
    assert cssmod.scrolling_classes(css) == {"table-wrap"}


def test_the_two_scheme_halves_are_a_partition():
    """`_usage_sites` walks light and dark separately, so every rule must land in exactly one
    half, once. `palettes()` never depended on that — it only ever asked about `:root` — which
    is why the property went unasserted until a second consumer started leaning on it.

    A sheet nesting a dark query inside a dark query is the case that breaks it: `finditer`
    resumes just past the opening brace rather than past the block, so the inner match is
    taken again and the excision index is rewound behind itself. **It fails silently green** —
    rules are duplicated, misattributed, or welded onto the next selector, and nothing raises.
    """
    sheet = ("""
    .light-only { color: red; }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #000; }
      @media (prefers-color-scheme: dark) { .nested { color: blue; } }
      .after-nested { color: green; }
    }
    .tail { color: black; }
    """)
    light, dark = cssmod.split_schemes(sheet)
    light_selectors = [selector for selector, _ in cssmod.rules(light)]
    dark_selectors = [selector for selector, _ in cssmod.rules(dark)]

    assert light_selectors == [".light-only", ".tail"], light_selectors
    assert sorted(dark_selectors) == [".after-nested", ".nested", ":root"], dark_selectors
    both = set(light_selectors) & set(dark_selectors)
    assert not both, f"{both} landed in both halves"
    assert len(dark_selectors) == len(set(dark_selectors)), "a rule was emitted twice"


def test_the_partition_keeps_a_selector_off_the_end_of_an_excised_block():
    """The welding half of the same defect: a rewound tail carries the closing `}` of the
    outer block into the next selector, so `.tail` is read as `}\n.tail`."""
    sheet = ("@media (prefers-color-scheme: dark) {"
             " @media (prefers-color-scheme: dark) { .inner { color: blue; } } }"
             ".tail { color: black; }")
    light, _ = cssmod.split_schemes(sheet)
    assert [selector for selector, _ in cssmod.rules(light)] == [".tail"]


def test_the_last_declaration_in_a_block_keeps_no_space_before_the_brace():
    """`[^;}]+` captures the space before `}`, so the **last** declaration of every block
    carries a trailing one unless it is stripped.

    Measured by the audit: without the strip, `1 light --accent-soft` reports
    `FAIL — "#5b93e4  (3.12:1 on --bg); spec pins #5b93e4"`. A page failed against the exact
    value it declares, on a key the gate refuses on — a false gate, which this repository
    ranks worse than a missing one. Nothing asserted the strip.
    """
    palette = cssmod.palettes(":root { --a: #ffffff; --accent-soft: #5b93e4 }")["light"]
    assert palette["accent-soft"] == "#5b93e4", "the last declaration keeps no trailing space"


def test_a_palette_declared_on_html_is_read_like_one_declared_on_root():
    """Reachable and asserted nowhere. Drop the `html` half and a page declaring its tokens
    there reports `1 tokens FAIL — no custom properties declared at all`: another false gate
    on a gated clause, over a page that is entirely conforming."""
    assert cssmod.palettes("html { --bg: #ffffff }")["light"]["bg"] == "#ffffff"


def test_the_dark_override_is_found_whatever_case_the_at_rule_is_written_in():
    """`_DARK_MEDIA` carries `re.IGNORECASE` and nothing asserted it. CSS at-rules and property
    names are case-insensitive, so a sheet written `@MEDIA (PREFERS-COLOR-SCHEME: DARK)` is
    valid and would have its whole dark palette read as light — every dark token then reported
    against the wrong ground on a gated clause."""
    light, dark = cssmod.split_schemes(
        ":root { --bg: #ffffff } @MEDIA (PREFERS-COLOR-SCHEME: DARK) { :root { --bg: #0f1319 } }")
    assert "#0f1319" in dark and "#0f1319" not in light


def test_a_property_name_is_matched_whatever_case_it_is_written_in():
    """The same capability one function over, equally unasserted. `COLOR: #fff` is valid CSS
    and a case-sensitive reader would report the declaration as absent."""
    assert cssmod.declarations(".a { COLOR: #ffffff }", "color") == [(".a", "#ffffff")]
