"""Every normative sentence of `0007` §5-§6, and what carries it.

**The one rule this module's correctness depends on: it is authored by reading `0007` §5 top
to bottom, and never by reading `clauses.py`.** A registry composed from the checker's
function list reproduces the checker's omissions exactly and then reports full coverage over
them — which is the defect it exists to end, committed in the act of closing it. `0008` §3.7
names that substitution: *"composed from the frozen table's columns rather than from the
normative clauses' sentences."* Two of the uncarried rows below were found by walking the
prose this way, and neither was known before it.

**What this closes.** `0009` §3.2 records the same defect landing three times: a clause
sentence nobody carries, invisible because nothing enumerates the sentences. Enumerating them
is all this module does. It gates nothing about the pages — `python -m tools.spec` exits 0
whatever it finds — because `0007` §5's governing rule means no instrument can decide whether
an uncarried sentence is an open item or a decision. Its *guards*, in `tests/test_spec.py`,
gate on the registry being malformed: a quote that no longer appears in `0007`, a carrier
naming a finding key the checker does not emit, an uncarried row with nowhere to be picked up.

**What it does not close, stated because the gap is structural.** Nothing detects a sentence
that was never entered. Guard 1 catches a quote drifting from the document; the inverse — §5
gaining a sentence with no row — has no mechanism and cannot have one, because §5 interleaves
normative sentences with descriptive *"what is already true"* notes by design, so no parser
can tell them apart. Its only carriers are `ADR-0005` and the `code-reviewer` pass that closes
every stage. `0009` §10 is where that limit belongs, registered rather than implied.

    python -m tools.spec            # the coverage table, then every uncarried sentence
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

#: A finding prefix the index checker emits. Not a whole key: clause 1's per-scheme keys are
#: generated per token (`1 light --accent-soft`), so the key space is parameterised and only a
#: prefix is stable. `GATED` is keyed the same way and for the same reason, which is what lets
#: guard 5 compare the two vocabularies instead of adding a fifth list of the same words.
INDEX = "index"
#: A named citation into a sibling repository: `repo:path::needle`. Never a count — `0009`
#: §8 row 1 records three sweeps producing three answers to *how many repositories carry a
#: page test*, and a field asserting a number here would be the hand count this repository's
#: working rules forbid. And never a claim about the sibling's `main`: this repository reads
#: siblings at its own pinned gitlink (`0009` §3.1, C1), so a probed citation means *present
#: at the pointer we hold* and nothing stronger.
REPO = "repo"
#: Carried by a person, at the `code-reviewer` pass every stage closes with. `0007` §7 names
#: the sentences no instrument can carry; this records them as carried rather than as missing,
#: which is a different fact from an empty `carriers` and must not print as the same one.
HUMAN = "human"

KINDS = (INDEX, REPO, HUMAN)

#: Finding keys the checker emits that are **not** normative sentences of `0007` §5-§6, so no
#: row here claims them and the coverage guards skip them.
#:
#: **This is not `conftest.NOT_A_CLAUSE`, and the difference is the whole reason it exists.**
#: That set answers *can this key ever be `FAIL`* — it is the ratchet floor's exemption list,
#: and its pin test requires a proof of impossibility for every entry. This set answers *is
#: this key a sentence somebody wrote in the spec*. The two questions coincided for as long as
#: there was one key in either, and `served` is what separates them: it **can** fail, so it is
#: not exempt from the floor, and `0007` §5 says nothing about it, so no sentence carries it.
#: A single set would have forced one of two lies — a false proof of impossibility, or a
#: normative row for a sentence that does not exist.
#: *`contrast text` and `contrast marks` left this set at S14b, 2026-09-10, because `c1.s6` and
#: `c1.s6b` now claim them as carriers and a key cannot both carry a sentence and be exempt from
#: claiming one. `contrast ground` stays permanently, `ADR-0008` D3: it reports what the checker
#: could not read, which `0007` §5-§6 says nothing about and never will.*
NOT_A_SENTENCE = frozenset({"stylesheets", "served", "contrast ground"})


@dataclass(frozen=True)
class Carrier:
    kind: str
    ref: str


@dataclass(frozen=True)
class Clause:
    """One normative sentence, its citation, and what holds it.

    `carriers` is a tuple and not a single value because `ADR-0004`'s decision is K-c — one
    index checker **plus** assertions in the repositories — so clause 1's palette and clause
    6's back-link are genuinely carried twice. A single-valued field, as `0009` §7 row 5
    sketches it, would misreport the decision the ADR took.
    """

    id: str
    cite: str
    quote: str
    carriers: tuple[Carrier, ...] = ()
    #: Required when `carriers` is empty, and must cite a document that exists and that
    #: mentions the citation — guard 4. An uncarried sentence with nowhere to be picked up is
    #: how `0009` §3.2's third occurrence happened: clauses 8 and 4-`<title>` had no stage.
    why: str = ""
    #: The settled reading, where the sentence has more than one. This field is why the
    #: registry earns its place *before* S9 rather than after it: a stage whose scope depends
    #: on a reading nobody wrote down is scoped by whoever read it last.
    note: str = ""


def _index(*refs: str) -> tuple[Carrier, ...]:
    return tuple(Carrier(INDEX, ref) for ref in refs)


def _human(ref: str) -> tuple[Carrier, ...]:
    return (Carrier(HUMAN, ref),)


def _repo(*refs: str) -> tuple[Carrier, ...]:
    """`repo:path::needle`. The needle is a test *function name*, never assertion text.

    `tests/conftest.py` already warns that a test bound to the live content of another
    repository goes red when that repository legitimately changes, and a check that cries
    wolf is a check that gets deleted. A function name survives a page rewrite; the sentence
    inside it does not.
    """
    return tuple(Carrier(REPO, ref) for ref in refs)


CLAUSES: tuple[Clause, ...] = (
    Clause(
        id="gov",
        cite="0007 §5, the governing rule",
        quote="where a page has measured a reason and recorded it, that value wins. The "
              "majority decides only where nobody measured.",
        carriers=_human("review; the role census prints the minority as a question"),
        note="The reason the role census is printed and never asserted: no checker can read "
             "a reason, so a census that gated would redden on the first correctly-migrated "
             "page. `tools/pagespec/__main__.py` says so in its own docstring.",
    ),
    Clause(
        id="c1.s1",
        cite="0007 §5 clause 1, first sentence",
        quote="Colour and radius are the ten tokens in §4.1, with a "
              "`prefers-color-scheme: dark` override redefining the same colour names",
        carriers=_index("1 tokens", "1 dark"),
    ),
    Clause(
        id="c1.s2",
        cite="0007 §5 clause 1, the extension sentence",
        quote="Additive extensions are allowed and must be named in the page's own `:root`.",
        carriers=_index("1 usage refs"),
    ),
    Clause(
        id="c1.s3",
        cite="0007 §5 clause 1, the literal sentence",
        quote="No literal hex outside the token block.",
        carriers=_index("1 literals"),
    ),
    Clause(
        id="c1.s4",
        cite="0007 §5 clause 1, the role sentence",
        quote="A token is used in the role it names",
        carriers=_index("1 usage roles", "1 composited"),
        note="`1 composited` is the honest half: resolving a `color-mix()` needs the ground "
             "the mark is drawn over, so those usage sites report `undecided` rather than a "
             "verdict. `0008` §3.2. **It reads the markup as well as the stylesheet since "
             "`0008` S12**, because alpha reaches a pixel from three places and it read two: "
             "a *data-driven* alpha has nowhere to live but a presentation attribute, and the "
             "one surface that emits one was failing SC 1.4.3 underneath it.",
    ),
    Clause(
        id="c1.s4b",
        cite="0007 §5 clause 1, the condition on the four exception shapes",
        quote="All four hold only where the role in question is not a house role named above",
        carriers=_index("1 usage roles"),
        note="Entered on review, 2026-09-07. The first walk read it as part of the italic "
             "census block and left it out; it is bold, rule-bearing and load-bearing — "
             "`clauses.py` records the implementation being written twice before it was true "
             "and three review passes each finding one layer of it. Without the condition "
             "the sweep takes the rule from 55 of 97 conforming sites caught to 97 of 97. "
             "*Requoted by S14a, 2026-09-09: it read \"not one of the three named above\" "
             "until a fourth house role existed, at which point the sentence was false. "
             "Guard 1 compares this quote against the document and would have caught the two "
             "files disagreeing — it cannot catch them agreeing on a wrong count, and the "
             "replacement therefore carries none. `0008` §4.26.*",
    ),
    Clause(
        id="c1.s4c",
        cite="0007 §5 clause 1, the control-boundary role",
        quote="or `--border-control` where the border is a user-interface control's own "
              "boundary",
        carriers=_human("review — `1 usage roles` admits the name, not the placement"),
        note="Entered by S14a, 2026-09-09. **The half the checker enforces and the half it "
             "does not are different sizes, and this row exists so the gap prints rather "
             "than being inferred from source.** `clause_1_usage` asks whether a border's "
             "role is in `_BORDER_ROLES`; it has no notion of what element a selector "
             "reaches, so it admits `--border-control` on a table hairline exactly as "
             "readily as on a control. Making it strict was measured and refused: the "
             "page-aware form would answer through `selector.parse`, which returns a "
             "`Refusal` for `.field input[type=\"number\"]` — so on `mini-traceroute`'s own "
             "repair rule the strictest available design reports `undecided`, which never "
             "gates. `ADR-0008` D7 §2 records that trade; the placement is review's, and "
             "`c1.s7`'s closing sentence is what decides a page that stretches it.",
    ),
    Clause(
        id="c1.s5",
        cite="0007 §5 clause 1, the two split values",
        quote="the spec takes the measured one",
        carriers=_index("1 light", "1 dark "),
        note="The per-scheme keys pin the eight settled values and the two that split. Note "
             "the two prefixes one space apart: `1 dark` is the override's presence, `1 dark ` "
             "with a trailing space is a pinned value.",
    ),
    Clause(
        id="c1.s5b",
        cite="0007 §5 clause 1, the control-boundary values",
        quote="`--border-control` is pinned in both schemes, and it is measured on "
              "`--surface`, the ground a control's boundary faces",
        carriers=_index("1 light --border-control", "1 dark --border-control"),
        note="Entered by S14a, 2026-09-09, **and the row exists because the gate was "
             "refusing on an authority the document did not carry.** The two pinned keys "
             "are gated through `Ratchet(\"1 \", GATED_STATE)` and their detail line says "
             "`spec pins #808a9c`; until this sentence was written the spec said no such "
             "thing, and the finest-matching carrier was `c1.s5` — a row whose cite is *the "
             "two split values* and whose subject is `--accent-soft` and `--positive`. A "
             "reader auditing what licensed the refusal was sent to a sentence about two "
             "other tokens. Found by the review of `0008` §4.26, and it becomes load-bearing "
             "at S14b rather than here: `0007` §5.0 lets a page that measures and records "
             "its own reason win, and these are the first pages this key can refuse.",
    ),
    Clause(
        id="c1.s6",
        cite="0007 §5 clause 1, the threshold sentence",
        quote="The threshold is the one the page's own usage implies, and it is read per "
              "page, not per token",
        carriers=_index("contrast text", "contrast marks"),
        note="`0009` §7 row 12, closed at S14b. The sentence says which bar applies and the "
             "census applies it: a site painted as text is bucketed at 4.5:1 and one painted "
             "as a mark at 3.0:1, per page and never per token. *This row said until "
             "2026-09-10 that what is uncarried is the verdict — true from S13, when the "
             "census shipped `UNDECIDED` by construction, until S14b gave two of its three "
             "keys a verdict branch. It said until 2026-09-09 that `colour.resolve()` and "
             "`colour.composite()` ship unused, which S13 had already made false. Twice now "
             "this row has described a reach the checker had outgrown, in the one field the "
             "registry prints on every run precisely so an open row cannot go stale unseen.*",
    ),
    Clause(
        id="c1.s6b",
        cite="0007 §5 clause 1, the obligation sentence",
        quote="Where a site is owed its threshold it must meet it, measured against what the "
              "page paints behind it",
        carriers=_index("contrast text", "contrast marks"),
        note="`ADR-0008` D4, and the reason its wording waited: `test_spec` pins a quote from "
             "the moment the sentence exists, so writing it before the census had printed "
             "would have pinned a rule nobody had measured. What the census then decided is "
             "in the sentence — D5 gave *owed* its meaning, and D6 gave *behind it* its own. "
             "The obligation is carried by both keys and gated by neither yet: `contrast "
             "text` is gated — a fetching run reads it clean on all twelve, which is the "
             "refutation that demands promotion — and `contrast marks` is report-only, "
             "because SVG sites still measure below 3.0:1 and a key that can never read "
             "clean cannot hold a state refutable in both directions. *This note glossed "
             "the owed-by sentence as well until 2026-09-10 — it is c1.s6d now, entered by "
             "the pass that amended the decision resting on it. And this note carried "
             "the figure 153 until 2026-09-10, and D8 refuted it the same day. No number "
             "is typed here now: the run prints the count per surface. The GATE row's "
             "twin of this sentence was corrected in the same commit and this one was "
             "not, which is the two-spellings drift 0008 4.11 records. A third correction to "
             "this one field went unrecorded and is recorded now: it ended with a stray "
             "duplicated fragment, `Superseded: clean cannot hold...`, left by the D8 pass "
             "and deleted by the D5 one.*",
    ),
    Clause(
        id="c1.s6c",
        cite="0007 §5 clause 1, the same-mark sentence",
        quote="A ground painted by the same declaration as the site is not one of them",
        carriers=_index("contrast marks"),
        note="`ADR-0008` D8, taken 2026-09-10. Carried by the marks key alone and not by "
             "`contrast text`, and the reason is structural rather than a count: "
             "`geometry.bounds` answers only for `rect` and `circle`, so no HTML element can "
             "ever be a ground the geometry places, and `paint.TEXT` is `{color}` — an HTML "
             "property. A `color` site cannot acquire the kind of ground this sentence "
             "excludes. SVG text is painted with `fill` and is therefore a mark, which is "
             "where the one live failure this checker has caught actually lived.",
    ),
    Clause(
        id="c1.s6d",
        cite="0007 §5 clause 1, the owed-by sentence",
        quote="A site painted as a mark is owed it where the mark identifies a control or "
              "carries information the reader needs, and not where it is structure",
        carriers=_index("contrast marks"),
        note="Normative since the contrast sentences entered, and carried by no row until "
             "2026-09-10 — `c1.s6b`'s note glossed it, which is a defensible reading and is "
             "also how each of `0009` §3.2's three occurrences looked from inside. This "
             "module's own docstring names the only mechanism that finds one: *nothing "
             "detects a sentence that was never entered*, so its carriers are `ADR-0005` and "
             "the review pass. `ADR-0008` §10 was that pass — it amended D5, which is this "
             "sentence's approximation, and the amendment could not be written without "
             "quoting a sentence the registry did not hold.",
    ),
    Clause(
        id="c1.s7",
        cite="0007 §5 clause 1, the closing sentence",
        quote="A page adding a fifth shape is stating something this sentence does not "
              "describe, and the governing rule above decides it",
        carriers=_human("review — the exception list is closed, and `gov` decides the rest"),
    ),
    Clause(
        id="c2.s1",
        cite="0007 §5 clause 2",
        quote="A tile is `.kpi`.",
        carriers=_index("2 tiles"),
    ),
    Clause(
        id="c2.s2",
        cite="0007 §5.1, the tile binding",
        quote="Clause 2 binds where a committed artifact can source the figure, and names "
              "the fallback where it cannot: a lead paragraph carrying the claim, with the "
              "reason stated on the page",
        carriers=(*_human("review; `0008` §4.8 is the round that applied it"),
                  *_repo("mlops-car-price:tests/test_docs_page.py::"
                         "test_each_headline_tile_quotes_the_cell_it_summarises")),
        note="`0007` §5.0's quotation rule is what makes this checkable inside a repository "
             "and unreachable from here: the index cannot ask whether a committed artifact "
             "holds the cell a tile quotes without reading that repository's artifacts.",
    ),
    Clause(
        id="c2.s3",
        cite="0007 §5.1, the condition",
        quote="The condition is a question about a repository, not a list of pages.",
        carriers=_human("review — `git ls-files` in the repository being judged"),
    ),
    Clause(
        id="c3.s1",
        cite="0007 §5 clause 3, first sentence",
        quote="Every `<table>` sits in `.table-wrap`, which computes to `overflow-x: auto`.",
        carriers=_index("3 tables"),
    ),
    Clause(
        id="c3.s2",
        cite="0007 §5 clause 3, the geometry half",
        quote="The wrapper must actually have somewhere to scroll when the table needs it",
        why="0009 N3, resolved 2026-09-08 as deferred and unowned — the decision is now "
            "written into `ADR-0004` §4, where the sentence claiming this carrier stood. "
            "N3's evidence does not reproduce: `measure_page.py` has calls, and one drives a "
            "real Chromium. They all point it at the skill's own fixtures, and nothing has "
            "ever pointed it at a published surface — the instrument is tested and it is not "
            "aimed. `wroclaw` keeps that browser layer skipped in CI deliberately, so there "
            "is no green gate to inherit even where the dependency is paid for.",
        note="`3 tables` checks the ancestry and the declared `overflow-x`. Whether the "
             "wrapper has anywhere to scroll is a rendered width, which no static read gives.",
    ),
    Clause(
        id="c3.s3",
        cite="0007 §5 clause 3, the checkable form's escape",
        quote="or is a table the page declared with `data-scroll=\"by-design\"`",
        carriers=_index("3 tables"),
        note="**Carried since 2026-09-09.** `0009` §7 row 5 found the escape implemented "
             "nowhere: `data-scroll` did not appear in `tools/` at all. It is the rare "
             "omission that made the checker **stricter** than the spec rather than looser, "
             "which is exactly why it survived two audits — no page uses the escape, so "
             "nothing failed, and the page that used it would have been the one to find out. "
             "A table declaring it is exempt and counted; a page whose tables all declare it "
             "reports `n/a` with the count, rather than passing silently.",
    ),
    Clause(
        id="c4.s1",
        cite="0007 §5 clause 4, the eyebrow",
        quote="The page opens with an eyebrow",
        carriers=_index("4 eyebrow"),
    ),
    Clause(
        id="c4.s2",
        cite="0007 §5 clause 4, the h1",
        quote="an `h1` that states a claim, not the repository's name",
        carriers=(*_index("4 h1"),
                  *_human("`0007` §7 — whether it states a claim is a judgement")),
        note="`4 h1` fails mechanically on a missing `h1` or one equal to the repository's "
             "name, and is `undecided` otherwise. It is not undecided by design.",
    ),
    Clause(
        id="c4.s3",
        cite="0007 §5 clause 4, the title",
        quote="the `<title>` follows the `h1` rather than the directory",
        carriers=_index("4 title"),
        note="Reading settled 2026-09-07 and implemented the same day in "
             "`_leads_with_the_projects_identity`: the `<title>` must not *lead with* the project's "
             "identity, in either the directory spelling or the project's own prose spelling "
             "of it. Compared at the head of the string — a name appearing later is the house "
             "style `<claim> — <repo>` and passes. Derived against the corpus: a "
             "non-positional reading fails 11 of 12 surfaces, because seven of the eight "
             "conforming titles carry the name as a suffix. **S10's scope is computed rather "
             "than asserted now — `python -m tools.pagespec --detail` prints the roster.** No "
             "surface is named here: a typed list stales silently on the first one S10 fixes, "
             "in the field whose own argument is that a stage must not be scoped by whoever "
             "read it last.",
    ),
    Clause(
        id="c5.s1",
        cite="0007 §5 clause 5",
        quote="The page carries `description`, `og:type`, `og:title`, `og:description`, "
              "`og:url`, `twitter:card` and a favicon",
        carriers=_index("5 card meta"),
        note="The property list is named in the clause because `og:*` passes on any single "
             "tag. The clause requires the tags to exist; whether `og:description` says "
             "anything true is `0008` §4.9's finding and is carried per repository.",
    ),
    Clause(
        id="c6.s1",
        cite="0007 §5 clause 6",
        quote="The page carries exactly one link back to the profile.",
        carriers=_index("6 back-link"),
    ),
    Clause(
        id="c7.s1",
        cite="0007 §5 clause 7, first sentence",
        quote="Type is the system stack.",
        carriers=_index("7 webfont"),
        note="**Carried since 2026-09-09; it was `NOT CARRIED` for two days and the checker "
             "printed it anyway.** `0009` §7 row 5 found that `font-family` appeared nowhere "
             "in `tools/`: the clause read every way of *requesting* a font over the wire and "
             "then printed `system stack` as its passing detail, which is the second "
             "sentence's verdict wearing the first one's words. Both sentences now share the "
             "key, on `c8.s1`'s precedent that one key may carry more than one sentence of "
             "one clause. A family a reader may not have fails; a family the page's own "
             "`@font-face` ships does not, because clause 7's second sentence permits exactly "
             "that and the guard for it caught this reader counting a vendored face as a "
             "stranger.",
    ),
    Clause(
        id="c7.s2",
        cite="0007 §5 clause 7, second sentence",
        quote="No third-party font request.",
        carriers=_index("7 webfont"),
    ),
    Clause(
        id="c8.s1",
        cite="0007 §5 clause 8, the rule",
        quote="Thousands are separated by `U+202F`, the narrow no-break space",
        carriers=_index("8 separator"),
        note="`n/a` where the page groups nothing is the clause read as written — its subject "
             "is how a grouped figure separates its thousands. That leaves an escape once "
             "S9 gates it: deleting the grouping is cheaper than migrating. **The sentence "
             "this note and the checker's docstring both propose — a figure of four or more "
             "digits is grouped — was put to the corpus by S9c and not taken.** It is "
             "undecidable by a static read: `doc-extract` prints `9894 values` ungrouped on "
             "a page where it groups `183 798`, which the sentence would rightly catch, and "
             "`auth-log-scan`'s `2026-03-14` and `mini-traceroute`'s base port `33434`, "
             "which it would catch wrongly. `0007` §5 clause 8c is the record. **No count is "
             "stated for that population** — `ADR-0004` §5 admits a measurement once it is "
             "frozen, and this one could not be: four attempts, four answers. Other figures "
             "in this registry and in §5 are frozen and stand; `0008` §4.16 says what the "
             "unfreezable one cost.",
    ),
    Clause(
        id="c8.s2",
        cite="0007 §5 clause 8, the scoring rule",
        quote="Scored over whole grouped figures in each page's rendered text",
        carriers=_index("8 separator"),
        note="**Superseded in scope by c8.s4** (S9c, 2026-09-08), which widens the reading "
             "from the rendered text alone to that plus the metadata the page publishes. The "
             "sentence is still the document's, and the bound it states is still what makes "
             "this a measurement: three earlier "
             "tallies were wrong, twice because the pattern matched across two adjacent "
             "numbers.",
    ),
    Clause(
        id="c8.s3",
        cite="0007 §5 clause 8a, the specimen exemption",
        quote="A figure the page displays as a specimen of another system's format is "
              "quoted, not written, and this clause does not reach it",
        carriers=_index("8 separator"),
        note="Entered by S9c, 2026-09-08. The checkable form is a grouped figure inside "
             "`<code>`, and the element rather than a literal string is what `0008` §4.11 "
             "demands so the exemption can be censused. Every exempt figure prints with its "
             "element on every run, and the clause reports it in its own detail even where "
             "the page would otherwise read `n/a`.",
    ),
    Clause(
        id="c8.s4",
        cite="0007 §5 clause 8b, the widened scoring rule",
        quote="Scored over the page's rendered text and over the metadata it publishes",
        carriers=_index("8 separator"),
        note="Entered by S9c, 2026-09-08, superseding c8.s2's scope. `car-price-ml/app` "
             "writes `1<space>200` from two sites — its `<meta name=\"description\">` and "
             "its body — and the old rule reached only the second, so a stage fixing the "
             "body alone would have turned the surface green. Scoped to clause 5's six keys "
             "rather than to every attribute. Measured before amending: six grouped figures "
             "in metadata across three surfaces, and widening moved no verdict.",
    ),
    Clause(
        id="q.s1",
        cite="0007 §5.0, sentence 1",
        quote="A figure is a quotation when its digit sequence equals a cell's, character "
              "for character.",
        carriers=(*_human("review; `0008` §4.8 and §4.10 are the rounds that applied it, to "
                          "`docs/index.html` and then to `README.md`"),
                  *_repo("ab-lab:tests/test_site_committed.py::"
                         "test_the_committed_artefact_is_what_the_generator_produces",
                         "auth-log-scan:tests/test_readme.py::"
                         "test_the_sample_block_is_what_the_readmes_own_quoted_command_prints")),
        note="`0008` §5 carries the residual, and it shrank by one on 2026-09-11. **Two "
             "repositories carry this on a README now, and of different shapes**: `ab-lab` "
             "byte-guards generated regions against their generator, and `auth-log-scan` runs "
             "the command its README names and compares. The rest are hand-typed prose with "
             "no carrier. *No count is given: this note said `only ab-lab` and `twelve of "
             "thirteen` for four days, and correcting a hand-typed figure only sets its next "
             "staleness date — `docs/reference/failure-classes.md` ST-3.* A README "
             "figure-provenance reader is still the named follow-on to S9; what landed is one "
             "README, not the reader.",
    ),
    Clause(
        id="q.s1b",
        cite="0007 §5.0, sentence 1's carve-out",
        quote="The group separator, the minus sign and the presence or absence of a trailing "
              "zero are the page's typography and are not part of the quotation.",
        carriers=_human("review — and the checker depends on it: clause 8 could not be "
                        "satisfiable at the same time as the quotation rule without it"),
        note="Entered on review, 2026-09-07. §5.0 credits this sentence with making clause 8 "
             "satisfiable at all: `mlops-car-price` prints `9,278` with a comma, clause 8 "
             "mandates `U+202F`, and under a byte-for-byte reading no page could satisfy both.",
    ),
    Clause(
        id="q.s2",
        cite="0007 §5.0, sentence 2",
        quote="Rounding is not quoting.",
        carriers=_human("review — the friction is the point, and it is `ADR-0012`'s own"),
    ),
    Clause(
        id="q.s3",
        cite="0007 §5.0, sentence 3",
        quote="A ratio or a comparison is an argument, not a cell.",
        carriers=_human("review"),
    ),
    Clause(
        id="c9.s1",
        cite="0007 §6, clause 9",
        quote="a number that appears on more than one page names the measurement it comes "
              "from, and points at the other",
        carriers=(*_human("review, plus a within-repo test on each side of the pair"),
                  *_repo("mlops-car-price:tests/test_docs_page.py::"
                         "test_the_page_names_its_own_measurement_and_points_at_the_sibling"),
                  *_repo("car-price-ml:tests/test_site.py::"
                         "test_the_page_names_its_own_measurement_and_points_at_the_sibling")),
        note="`0008` S4 took the `mlops-car-price` half and S5 took `car-price-ml`'s, "
             "2026-09-08 — the pair is now carried from both sides. The second guard shipped "
             "one commit after the page change, because the page change alone left the bridge "
             "carried by CI's byte-diff, which asserts the page matches its template and would "
             "go on doing so with the bridge deleted from both. The clause stays outside the "
             "index checker: see c9.s2, which is the clause stating its own limit.",
    ),
    Clause(
        id="c9.s1b",
        cite="0007 §6, clause 9's scope",
        quote="Scope: a figure the page presents as a result — a metric, a size, a count of "
              "the corpus — not every integer on it.",
        carriers=_human("review — the bound is a judgement about what a page is claiming"),
        note="Entered on review, 2026-09-07. The clause states its own reason: one covering "
             "every integer *would be unenforceable and would be ignored*, so this sentence "
             "is what makes clause 9 a rule rather than a slogan.",
    ),
    Clause(
        id="c9.s2",
        cite="0007 §6, clause 9's enforcement limit",
        quote="That two pages agree cannot be checked without coupling two public "
              "repositories to a private index, so it is a review item",
        carriers=_human("the clause states its own limit; this row records that the absence "
                        "of an index check is the decision and not a gap"),
    ),
)


SPEC = (Path(__file__).resolve().parents[1] / "docs" / "audit"
        / "0007_divergence-and-the-page-spec.md")
#: The slice guard 1 searches. Bounded on both sides so a quote that exists only in §3's
#: descriptive prose cannot satisfy it — §3 restates several clause sentences as observations,
#: and matching there would let a normative quote drift with nothing noticing.
NORMATIVE_FROM = "## 5. The spec"
NORMATIVE_TO = "## 7. What this spec does not check"

_EMPHASIS = re.compile(r"[*]+")
_SPACE = re.compile(r"\s+")
#: Blockquote markers, at a line start only. Clause 9 is stated inside a blockquote, so its
#: sentence carries a `>` at every wrap; collapsing whitespace without stripping these welds
#: the marker into the middle of the sentence and the quote can never match. Anchored per
#: line so a `>` inside `<table>` or `overflow-x` is untouched.
_QUOTE_MARKER = re.compile(r"^[ \t]*>+[ \t]?", re.MULTILINE)


def normalise(text: str) -> str:
    """One spelling for both sides of guard 1's comparison.

    `0007` is hard-wrapped at about 100 columns, so every quote longer than a few words spans
    a line break; its normative sentences are bolded, so the asterisks sit inside the span;
    and clause 9's is inside a blockquote. Collapse whitespace, drop emphasis and blockquote
    markers, and nothing else — backticks stay, because they are part of the identifiers the
    clauses name, and dropping them would let `--radius` and `radius` match.
    """
    return _SPACE.sub(" ", _EMPHASIS.sub("", _QUOTE_MARKER.sub("", text))).strip()


def normative_text() -> str:
    """`0007` §5 through §6, normalised. Raises if either boundary heading has moved.

    The failure names the heading it could not find rather than reporting every quote as
    missing: a renamed section would otherwise arrive as twenty-odd drifted quotes, which is
    the wrong diagnosis printed twenty-odd times.
    """
    document = SPEC.read_text(encoding="utf-8")
    start = document.find(NORMATIVE_FROM)
    end = document.find(NORMATIVE_TO)
    if start < 0:
        raise AssertionError(f"{SPEC.name}: the heading {NORMATIVE_FROM!r} is not in the file")
    if end < 0:
        raise AssertionError(f"{SPEC.name}: the heading {NORMATIVE_TO!r} is not in the file")
    if end <= start:
        raise AssertionError(f"{SPEC.name}: {NORMATIVE_TO!r} precedes {NORMATIVE_FROM!r}")
    return normalise(document[start:end])


def uncarried() -> tuple[Clause, ...]:
    return tuple(clause for clause in CLAUSES if not clause.carriers)


def index_refs() -> frozenset[str]:
    """Every finding prefix the registry claims the checker emits."""
    return frozenset(carrier.ref for clause in CLAUSES
                     for carrier in clause.carriers if carrier.kind == INDEX)


def report() -> list[str]:
    """The coverage table, then every uncarried sentence and where it is picked up.

    Printed and never asserted, for the role census's reason: `0007` §5's governing rule means
    no instrument can decide whether an uncarried sentence is an open item or a decision. The
    count comes from the registry on every run and is typed into no document.
    """
    lines = ["spec — every normative sentence of 0007 §5-§6, and what carries it", ""]
    for clause in CLAUSES:
        held = ", ".join(f"{carrier.kind}:{carrier.ref}" for carrier in clause.carriers) \
            or "NOT CARRIED"
        lines.append(f"  {clause.id:<7} {clause.cite}")
        lines.append(f"          {held}")
        if clause.note:
            # The settled readings print. `note` is where c4.s3 records which of two readings
            # of clause 4 scopes S10, and a field arguing that a stage must not be *scoped by
            # whoever read it last* cannot itself be visible only in source.
            lines.append(f"          note: {clause.note}")
    lines.append("")
    lines.append("  emitted and carried by no sentence, by design: "
                 + ", ".join(sorted(NOT_A_SENTENCE))
                 + " — the checker reporting on its own inputs rather than on the page")
    open_rows = uncarried()
    lines.append("")
    lines.append(f"  {len(CLAUSES)} normative sentence(s); "
                 f"{len(open_rows)} carried by nothing")
    if open_rows:
        lines.append("")
        lines.append("carried by nothing — printed, never gated, because 0007 §5's governing")
        lines.append("rule means no instrument can tell an open item from a decision")
        for clause in open_rows:
            lines.append("")
            lines.append(f"  {clause.id}  {clause.cite}")
            lines.append(f"      \"{clause.quote}\"")
            lines.append(f"      why: {clause.why}")
    return lines


def main() -> int:
    for line in report():
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
