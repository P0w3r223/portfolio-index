"""The eight clauses of `0007` §5, over pages built to make each verdict inevitable.

A clause has four verdicts and three of them are not `fail`, which is the part that needs
testing hardest. `0007` §7 exists because the instrument that produced the original table was
wrong three times: **a checker that reports a confident verdict it did not earn is that
failure automated.** So `undecided` and `n/a` are asserted as deliberately as `pass`, and the
tests that matter most are the ones where a plausible implementation would have said `pass`.
"""

from __future__ import annotations

import pytest

from conftest import detail_of, fixture, loaded, page, status_of
from tools.pagespec import clauses

NARROW = "\u202f"
NBSP = "\u00a0"

HOUSE = fixture("house_palette.css")


# -- clause 1: the ten tokens, and the two the governing rule pins -------------------------


def test_a_page_with_no_custom_properties_fails_once_rather_than_ten_times():
    """`apply-scout`, `mlops-car-price` and `pl-jobs-lora` transcribe the system by hand.

    One finding naming the cause reads as one item of work; ten findings naming ten absent
    tokens reads as a page in ruins, and the two are the same page.
    """
    findings = clauses.clause_1_tokens(page(""), "body { color: #1c2430 }")
    assert [finding.clause for finding in findings] == ["1 tokens"]
    assert findings[0].status == clauses.FAIL
    assert findings[0].detail == "no custom properties declared at all"


def test_the_house_tokens_are_checked_by_name_and_absence_is_named():
    """`wroclaw` holds `--border` and `--text` under the aliases `--line` and `--ink`.

    §4.3 calls that a naming item, not a defect — but the clause is about the names, so it
    reports them missing and says which. An alias-aware check would hide a real rollout item.
    """
    findings = clauses.clause_1_tokens(page(""), fixture("wroclaw_scroller.css"))
    assert status_of(findings, "1 tokens") == clauses.FAIL
    assert detail_of(findings, "1 tokens") == "9 declared; missing border, text, radius"


def test_a_page_holding_all_eight_settled_tokens_passes_the_naming_half():
    findings = clauses.clause_1_tokens(page(""), HOUSE)
    assert status_of(findings, "1 tokens") == clauses.PASS
    assert detail_of(findings, "1 tokens") == "10 declared"


def test_a_dark_override_is_reported_present_when_the_two_palettes_differ():
    assert status_of(clauses.clause_1_tokens(page(""), HOUSE), "1 dark") == clauses.PASS


def test_a_page_with_no_dark_override_is_reported_as_having_none():
    """The three pages reading zero tokens carry no dark override either — the same fact
    twice, which is why `0007` §3's two columns move together."""
    findings = clauses.clause_1_tokens(page(""), ":root { --bg: #ffffff; }")
    assert status_of(findings, "1 dark") == clauses.FAIL


@pytest.mark.parametrize("value, status", [
    ("#5b93e4", clauses.PASS),
    ("#5B93E4", clauses.PASS),
    ("#93c5fd", clauses.FAIL),
])
def test_the_pinned_token_takes_the_measured_value_not_the_majority_one(value, status):
    """§5's governing rule: where a page measured a reason and recorded it, that value wins.

    `#93c5fd` is on four pages and `#5b93e4` on three, and the majority is the failing one at
    1.80:1. A checker that counted pages would recommend reverting the fix.
    """
    findings = clauses.clause_1_tokens(page(""), f":root {{ --accent-soft: {value}; }}")
    assert status_of(findings, "1 light --accent-soft") == status


def test_a_failing_pin_is_reported_with_the_ratio_that_makes_it_actionable():
    """A hex against a hex tells a reader nothing; the ratio is the reason for the change."""
    findings = clauses.clause_1_tokens(
        page(""), ":root { --bg: #ffffff; --accent-soft: #93c5fd; }")
    assert detail_of(findings, "1 light --accent-soft") == \
        "#93c5fd (1.80:1 on --bg); spec pins #5b93e4"


def test_a_token_a_page_never_declares_is_not_applicable_rather_than_failing():
    """`wroclaw` lacks `--positive` entirely. Marking that a failure would put a page on the
    contrast rollout for a colour it does not paint."""
    findings = clauses.clause_1_tokens(page(""), ":root { --bg: #ffffff; }")
    assert status_of(findings, "1 light --positive") == clauses.NOT_APPLICABLE
    assert status_of(findings, "1 dark --positive") == clauses.NOT_APPLICABLE


def test_a_composited_usage_is_reported_and_never_decided():
    """Paint order inside an SVG is not recoverable from the stylesheet alone.

    `0008` §3.2 is the whole argument: a checker that resolved this against the nearest card
    would have cleared the change that had to be reverted. Reporting `undecided` is the
    honest verdict, and the one clause 1 is allowed to reach here.
    """
    findings = clauses.clause_1_composited(
        ".mark { fill: color-mix(in srgb, var(--accent) 28%, transparent) }"
        ".band { opacity: 0.4 }"
    )
    assert [finding.status for finding in findings] == [clauses.UNDECIDED]
    assert "2 usage(s)" in findings[0].detail


def test_a_fully_opaque_stylesheet_reports_no_composited_usage():
    """`opacity: 1` and `opacity: 0` paint exactly what they declare, so neither is a finding."""
    assert clauses.clause_1_composited(".a { opacity: 1 } .b { opacity: 0 }") == []


def test_a_non_numeric_opacity_is_skipped_rather_than_crashing():
    """`opacity: var(--x)` is legal CSS and would raise on `float()`."""
    assert clauses.clause_1_composited(".a { opacity: var(--fade) }") == []


# -- clause 2: a tile is .kpi ---------------------------------------------------------------


@pytest.mark.parametrize("markup, status, detail", [
    ('<li class="kpi"></li>', clauses.PASS, ".kpi"),
    ('<li class="tile"></li>', clauses.FAIL, ".tile"),
    ('<div class="stat"></div>', clauses.FAIL, ".stat"),
    ('<li class="kpi"></li><li class="tile"></li>', clauses.FAIL, ".kpi, .tile"),
])
def test_the_tile_name_is_reported_as_the_page_spells_it(markup, status, detail):
    finding = clauses.clause_2_tiles(page(markup))
    assert (finding.status, finding.detail) == (status, detail)


def test_a_page_with_no_tiles_falls_to_the_fallback_rather_than_failing():
    """§5.1: `mlops-car-price` and `pl-jobs-lora` have no committed artifact to source a
    figure from, and a mandate to grow four tiles would make them print numbers nothing
    produces — which `ADR-0012` forbids."""
    finding = clauses.clause_2_tiles(page("<p>a lead paragraph carrying the claim</p>"))
    assert finding.status == clauses.NOT_APPLICABLE


# -- clause 3: every table sits in something that scrolls -----------------------------------


def test_a_table_inside_a_scrolling_wrapper_passes_under_whatever_the_wrapper_is_called():
    finding = clauses.clause_3_tables(
        page('<div class="ledger-wrap"><table></table></div>'),
        ".ledger-wrap { max-height: 20rem; overflow: auto }",
    )
    assert finding.status == clauses.PASS
    assert ".ledger-wrap" in finding.detail


def test_a_table_that_is_its_own_scroller_passes_with_nothing_above_it():
    """The fourth mechanism, and the one that broke `measure_page.py` twice: a walk that
    starts at the table's parent cannot see a rule written against the table.

    Seen, but not passed. The rule is inside `@media (max-width: 640px)` and `rules()`
    drops the media condition, so the reader cannot tell a scroller that engages at every
    width from one that engages below 640 px. `undecided` is the honest verdict, and the
    detail says which half is missing.
    """
    finding = clauses.clause_3_tables(
        page("<body><table></table></body>"), fixture("wroclaw_scroller.css"))
    assert finding.status == clauses.UNDECIDED
    assert "the table itself" in finding.detail
    assert "media condition is not read" in finding.detail


def test_the_table_carrying_the_scrolling_class_itself_is_not_missed_either():
    """`wroclaw` also writes `.metrics` on the table element rather than on a wrapper."""
    finding = clauses.clause_3_tables(
        page('<table class="scroll-x"></table>'), ".scroll-x { overflow-x: auto }")
    assert finding.status == clauses.PASS


def test_a_bare_table_with_nothing_that_scrolls_is_counted_and_named():
    """`mini-traceroute`'s second table sits in a bare `<figure>` and passes on margin.

    §6.5 bound the wider criterion — *every* table, not every *wide* table — precisely so a
    page could not pass on the accident of its content being narrow today.
    """
    finding = clauses.clause_3_tables(
        page('<div class="scroll-x"><table></table></div><figure><table></table></figure>'),
        ".scroll-x { overflow-x: auto }",
    )
    assert finding.status == clauses.FAIL
    assert "1 with nothing that scrolls" in finding.detail


def test_a_stylesheet_with_no_scroller_at_all_fails_before_counting_tables():
    finding = clauses.clause_3_tables(page("<table></table>"), ".card { overflow: hidden }")
    assert (finding.status, finding.detail) == \
        (clauses.FAIL, "no class in the stylesheet scrolls")


def test_a_page_with_no_tables_is_not_applicable():
    finding = clauses.clause_3_tables(page("<p>prose only</p>"), ".table-wrap { overflow: auto }")
    assert finding.status == clauses.NOT_APPLICABLE


def test_an_unclosed_wrapper_makes_the_clause_refuse_rather_than_pass_everything():
    """A wrapper that never closes makes every table below it read as wrapped.

    That is a false green in the direction that matters, and it is the guard `_Rendered`
    bought the hard way. Drop the `unclosed` check and this page reports `pass`.
    """
    finding = clauses.clause_3_tables(
        page('<div class="table-wrap"><table></table><table></table>'),
        ".table-wrap { overflow-x: auto }",
    )
    assert finding.status == clauses.UNDECIDED
    assert "ancestry unreliable" in finding.detail


def test_the_recorded_unwrapped_figure_table_is_still_found_through_an_external_sheet():
    """`mini-traceroute`'s reduction, whose scroller rule is not in the HTML at all."""
    markup = fixture("mini_traceroute_shape/index.html")
    sheet = fixture("mini_traceroute_shape/assets/styles.css")
    finding = clauses.clause_3_tables(page(markup), sheet)
    assert finding.status == clauses.FAIL
    assert "2 table(s), scroller(s): .scroll-x; 1 with nothing that scrolls" == finding.detail


# -- clause 4: the opening, and the two surfaces it has ------------------------------------


def test_a_title_that_leads_with_the_directory_name_fails():
    findings = clauses.clause_4_opening(
        page("<title>apply-scout — an LLM job-matching agent</title>"), "apply-scout")
    assert status_of(findings, "4 title") == clauses.FAIL
    assert "leads with the repository's name" in detail_of(findings, "4 title")


def test_a_title_that_states_the_claim_first_passes_even_when_it_ends_with_the_directory():
    """`ab-lab`'s title ends `— ab-lab`; the clause asks what the title *leads* with, because
    the reader of a search result sees the front of it."""
    findings = clauses.clause_4_opening(
        page("<title>A 5% test is only 5% if you look once — ab-lab</title>"), "ab-lab")
    assert status_of(findings, "4 title") == clauses.PASS


def test_a_page_with_no_title_fails_rather_than_passing_on_an_empty_string():
    findings = clauses.clause_4_opening(page("<h1>A claim</h1>"), "ab-lab")
    assert status_of(findings, "4 title") == clauses.FAIL
    assert detail_of(findings, "4 title") == "no <title>"


def test_a_headline_that_is_the_repository_name_fails():
    findings = clauses.clause_4_opening(
        page("<h1>mlops-car-price</h1><title>x</title>"), "mlops-car-price")
    assert status_of(findings, "4 h1") == clauses.FAIL
    assert detail_of(findings, "4 h1") == "the repository's name: mlops-car-price"


def test_a_headline_that_is_not_the_repository_name_is_undecided_rather_than_passed():
    """*"States a claim"* is a human judgement — `0007` §7 names it as the one normative
    clause a vendored checker cannot carry. Reporting `pass` here would be the checker
    claiming a verdict it did not earn."""
    findings = clauses.clause_4_opening(
        page("<h1>A traceroute, one TTL at a time</h1><title>x</title>"), "mini-traceroute")
    assert status_of(findings, "4 h1") == clauses.UNDECIDED


def test_a_missing_headline_fails_rather_than_being_left_open():
    findings = clauses.clause_4_opening(page("<title>x</title>"), "ab-lab")
    assert status_of(findings, "4 h1") == clauses.FAIL
    assert detail_of(findings, "4 h1") == "no <h1>"


def test_a_title_spelled_as_prose_does_not_read_as_the_directory_it_resembles():
    """The judgement the checker deliberately does not settle.

    `0007` §3 calls `wroclaw`'s `<title>` the repository name; mechanically *"Wrocław Air
    Insights"* does not lead with the directory `wroclaw-air-insights`, so the check passes
    it. That is a difference of reading, not a defect on either side, and §7 says a checker
    cannot carry it. Pinned here so that changing the reading is a decision, not a drift.
    """
    findings = clauses.clause_4_opening(
        page("<title>Wrocław Air Insights — live PM2.5 forecast</title>"),
        "wroclaw-air-insights")
    assert status_of(findings, "4 title") == clauses.PASS


# -- clause 5: the six card properties and a favicon ----------------------------------------


CARD = "".join(f'<meta property="{key}" content="x">' for key in clauses.CARD_META)


def test_a_page_carrying_all_six_properties_and_a_favicon_passes():
    finding = clauses.clause_5_card_meta(page(CARD + '<link rel="icon" href="f.svg">'))
    assert (finding.status, finding.detail) == (clauses.PASS, "all seven present")


def test_the_one_missing_property_is_named_rather_than_the_group_failing():
    """`og:*` passes on any single tag, so `wroclaw`'s `yes` in §3 is the one that is not
    whole: three of the four `og:` properties, missing `og:description`."""
    markup = "".join(f'<meta property="{key}" content="x">'
                     for key in clauses.CARD_META if key != "og:description")
    finding = clauses.clause_5_card_meta(page(markup + '<link rel="icon" href="f.svg">'))
    assert (finding.status, finding.detail) == (clauses.FAIL, "missing og:description")


def test_a_property_declared_empty_counts_as_missing():
    """An `og:description` with no content is a tag, not a description."""
    markup = CARD.replace('property="og:url" content="x"', 'property="og:url" content=""')
    finding = clauses.clause_5_card_meta(page(markup + '<link rel="icon" href="f.svg">'))
    assert finding.detail == "missing og:url"


@pytest.mark.parametrize("rel", ["icon", "shortcut icon", "apple-touch-icon"])
def test_a_favicon_counts_however_its_rel_is_spelled(rel):
    finding = clauses.clause_5_card_meta(page(CARD + f'<link rel="{rel}" href="f.svg">'))
    assert finding.status == clauses.PASS


def test_a_page_with_no_favicon_has_it_named_among_the_missing():
    finding = clauses.clause_5_card_meta(page(CARD))
    assert finding.detail == "missing favicon"


# -- clause 6: exactly one link back to the profile -----------------------------------------


def test_one_link_back_to_the_profile_passes_and_is_quoted():
    finding = clauses.clause_6_back_link(
        page('<a href="https://github.com/P0w3r223">More work</a>'))
    assert (finding.status, finding.detail) == \
        (clauses.PASS, "https://github.com/P0w3r223")


def test_a_trailing_slash_is_the_same_link():
    finding = clauses.clause_6_back_link(page('<a href="https://github.com/P0w3r223/">x</a>'))
    assert finding.status == clauses.PASS


def test_a_link_to_this_repository_is_not_a_link_back_to_the_profile():
    """Every page links its own repository; counting that would pass all twelve at once."""
    finding = clauses.clause_6_back_link(
        page('<a href="https://github.com/P0w3r223/doc-extract">Source</a>'))
    assert (finding.status, finding.detail) == \
        (clauses.FAIL, "no link back to the profile")


def test_two_links_back_fail_because_the_clause_asks_for_one():
    """`0003` §7 settled the shape — hub-and-spoke, one link — and two is a different shape."""
    finding = clauses.clause_6_back_link(page(
        '<a href="https://github.com/P0w3r223">Profile</a>'
        '<a href="https://github.com/P0w3r223/">More</a>'
    ))
    assert finding.status == clauses.FAIL
    assert "2 links back" in finding.detail


# -- clause 7: type is the system stack ------------------------------------------------------


def test_a_third_party_font_request_is_named_in_full():
    """A page whose subject is provenance, fetching its type from a third party."""
    finding = clauses.clause_7_webfont(page(
        '<link rel="preconnect" href="https://fonts.gstatic.com">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">'
    ), "")
    assert finding.status == clauses.FAIL
    assert finding.detail.count("https://") == 2


def test_a_page_with_no_font_request_passes():
    finding = clauses.clause_7_webfont(page(
        '<link rel="stylesheet" href="assets/styles.css">'
        '<link rel="icon" href="data:image/svg+xml,x">'
    ), "")
    assert (finding.status, finding.detail) == (clauses.PASS, "system stack")


def test_a_same_origin_stylesheet_is_not_a_third_party_request():
    """A local sheet named `fonts.css` is served from the page's own origin."""
    finding = clauses.clause_7_webfont(page('<link rel="stylesheet" href="assets/fonts.css">'), "")
    assert finding.status == clauses.PASS


def test_a_font_fetched_by_import_is_found_where_reading_link_alone_would_miss_it():
    """The second of the three routes to a third-party font.

    A page can reach `fonts.googleapis.com` without a single `<link>` to it. Checking the
    markup alone passes that page, and the complete stylesheet was already in hand.
    """
    finding = clauses.clause_7_webfont(
        page("<body>x</body>"),
        "@import url(https://fonts.googleapis.com/css2?family=Inter);")
    assert finding.status == clauses.FAIL
    assert "fonts.googleapis.com" in finding.detail


def test_a_font_face_pointing_off_origin_is_found_too():
    finding = clauses.clause_7_webfont(
        page("<body>x</body>"),
        "@font-face { font-family: X; src: url(https://cdn.example/x.woff2) format(woff2); }")
    assert finding.status == clauses.FAIL


def test_a_font_face_served_from_the_page_s_own_origin_passes():
    """The vendored-font pattern `doc-extract` uses. Same clause, opposite verdict."""
    finding = clauses.clause_7_webfont(
        page("<body>x</body>"),
        "@font-face { font-family: X; src: url(assets/x.woff2) format(woff2); }")
    assert finding.status == clauses.PASS


# -- clause 8: thousands are separated by U+202F ---------------------------------------------


@pytest.mark.parametrize("text, status, detail", [
    (f"183{NARROW}798 bytes", clauses.PASS, "U+202F 1"),
    ("183 798 bytes", clauses.FAIL, "space 1"),
    ("183,798 bytes", clauses.FAIL, "comma 1"),
    (f"183{NBSP}798 bytes", clauses.FAIL, "U+00A0 1"),
    (f"1{NARROW}000 and 2 000", clauses.FAIL, "U+202F 1, space 1"),
])
def test_the_separator_inventory_is_reported_per_codepoint(text, status, detail):
    """`car-price-ml` is mid-migration in public — 16 plain spaces against 12 U+202F on one
    page — so a clause that reported only the majority would call it settled."""
    finding = clauses.clause_8_separator(page(f"<p>{text}</p>"))
    assert (finding.status, finding.detail) == (status, detail)


def test_a_page_that_groups_no_figure_is_not_applicable_rather_than_passing():
    """Four of the eleven surfaces print no grouped figure at all. `pass` would credit them
    with a convention they have never had occasion to follow."""
    finding = clauses.clause_8_separator(page("<p>108 failed logins in 7.1 hours</p>"))
    assert (finding.status, finding.detail) == \
        (clauses.NOT_APPLICABLE, "no grouped figure on the page")


@pytest.mark.parametrize("text", [
    "07:00 203.0.113.42",
    "0.0 113",
    "1 2345",
    "10 12",
    "version 1.2 345",
])
def test_something_that_is_not_a_grouped_figure_does_not_score_as_one(text):
    """The bound on the whole token is what makes this a measurement, and it is here because
    three earlier tallies were wrong — twice by matching across two adjacent numbers, which
    credited `auth-log-scan` with nineteen figures it does not have."""
    assert clauses.clause_8_separator(page(f"<p>{text}</p>")).status == clauses.NOT_APPLICABLE


def test_the_pattern_itself_refuses_to_reach_across_the_break_between_nodes():
    """The separator class is spelled out rather than written `\\s`, and this asserts that.

    Asserted at the pattern rather than through a verdict on purpose: `\\s` would match across
    the newline `rendered_text` inserts, but the newline is not in `_SEPARATOR_NAMES`, so the
    tally absorbs the difference and every one of the eleven surfaces reports the same
    inventory either way. The guard is therefore invisible in the output today and one edit
    from becoming load-bearing — swap the joiner, or count `len(tail)` instead of naming the
    characters, and `\\s` silently restores the weld that produced every wrong tally in the
    record. Two guards that are each redundant while the other holds need the pair tested,
    not the pair's current effect.
    """
    assert clauses._GROUPED.findall("5\n315") == []
    assert clauses._GROUPED.findall(f"5{NARROW}315") == [("5", f"{NARROW}315")]


def test_a_figure_grouped_twice_over_counts_both_of_its_separators():
    finding = clauses.clause_8_separator(page(f"<p>12{NARROW}345{NARROW}678</p>"))
    assert (finding.status, finding.detail) == (clauses.PASS, "U+202F 2")


def test_the_recorded_narrow_spaced_page_reproduces_its_inventory():
    """The doc-extract reduction — the row `0007` §3 records as `U+202F` 3, `U+00A0` 1."""
    finding = clauses.clause_8_separator(page(fixture("narrow_spaces.html")))
    assert (finding.status, finding.detail) == (clauses.FAIL, "U+00A0 1, U+202F 3")


def test_the_recorded_welding_table_reports_no_figure_at_all():
    """Welded, this table alone credited `pl-review-sense` with nine separators."""
    finding = clauses.clause_8_separator(page(fixture("welded_cells.html")))
    assert finding.status == clauses.NOT_APPLICABLE


def test_a_separator_written_as_an_entity_is_read_as_the_codepoint_it_renders():
    """Clause 8 names the codepoint *"not an HTML entity, so a checker can test for it"*, and
    the reading taken here is the rendered one: `&#8239;` renders as U+202F and passes.

    Pinned because it is a judgement, not an accident of the parser — a source-bytes reading
    would fail `doc-extract`'s `&nbsp;` cell for a different reason than the one that matters.
    """
    assert clauses.clause_8_separator(page("<p>183&#8239;798</p>")).status == clauses.PASS


# -- the whole check over one surface --------------------------------------------------------


def test_every_clause_reports_exactly_once_over_a_page_that_satisfies_none_of_them():
    """A clause that silently drops out of the table is a column nobody notices is missing."""
    findings = clauses.check(loaded("<html></html>", ""))
    reported = [finding.clause for finding in findings]
    for expected in ("1 tokens", "2 tiles", "3 tables", "4 h1", "4 title",
                     "5 card meta", "6 back-link", "7 webfont", "8 separator"):
        assert reported.count(expected) == 1, f"{expected} reported {reported.count(expected)}×"


def test_a_stylesheet_that_could_not_be_read_is_declared_rather_than_ignored():
    """Reading only the inline blocks is the trap that recorded `mini-traceroute` wrongly
    across three sessions. A sheet that cannot be read makes the CSS clauses provisional, and
    the report has to say so."""
    findings = clauses.check(loaded("<html></html>", "", unreadable=["assets/styles.css"]))
    assert status_of(findings, "stylesheets") == clauses.UNDECIDED
    assert "assets/styles.css" in detail_of(findings, "stylesheets")


def test_a_surface_with_nothing_unread_carries_no_stylesheet_finding():
    assert all(finding.clause != "stylesheets" for finding in clauses.check(loaded("", "")))


def test_every_status_the_check_can_emit_is_one_the_report_can_print():
    """`__main__._MARK` has a symbol per status; a fifth status would print a `KeyError`."""
    from tools.pagespec import __main__ as report

    findings = clauses.check(loaded(fixture("svg_titles.html"), HOUSE))
    assert {finding.status for finding in findings} <= set(report._MARK)


def test_a_ground_that_is_not_a_hex_colour_is_reported_rather_than_raised():
    """`contrast()` was guarded on the value and not on the ground.

    `--bg: var(--paper)` and `--bg: light-dark(#fff, #000)` are both valid CSS, and either
    one turned a single non-conforming token on a single page into a `ValueError` that took
    the whole twelve-surface table down with it. The clause still has something true to say
    without a ratio, so it says that.
    """
    css = ":root { --bg: var(--paper); --accent-soft: #93c5fd; }"
    findings = clauses.clause_1_tokens(page("<body>x</body>"), css)
    detail = detail_of(findings, "1 light --accent-soft")
    assert status_of(findings, "1 light --accent-soft") == clauses.FAIL
    assert "#93c5fd" in detail and "spec pins" in detail
    assert ":1" not in detail, "no ratio can be quoted against a ground that is not a colour"


def test_a_ground_that_is_a_hex_colour_still_carries_its_ratio():
    """The other half of the same guard: withholding the ratio when it *is* measurable would
    be the mirror defect, and a spec violation with no number beside it is easy to ignore."""
    css = ":root { --bg: #ffffff; --accent-soft: #93c5fd; }"
    findings = clauses.clause_1_tokens(page("<body>x</body>"), css)
    assert "1.80:1" in detail_of(findings, "1 light --accent-soft")


def test_an_alpha_hex_token_is_reported_without_a_ratio_rather_than_crashing():
    """`#93c5fdcc` is valid CSS Color 4 and one edit away in any of these stylesheets.

    Reading its first six digits would report the ratio of the opaque colour, which is a
    confident wrong number about a value that is in fact translucent.
    """
    css = ":root { --bg: #ffffff; --accent-soft: #93c5fdcc; }"
    findings = clauses.clause_1_tokens(page("<body>x</body>"), css)
    assert status_of(findings, "1 light --accent-soft") == clauses.FAIL
    assert ":1" not in detail_of(findings, "1 light --accent-soft")
