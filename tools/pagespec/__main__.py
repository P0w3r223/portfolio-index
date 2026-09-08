"""The conformance table, computed instead of typed — and, since `0008` S-gate, a gate.

`0007` §3 was corrected five times across two sessions because a per-page measurement was
kept in a normative document. This is what replaces it.

**The gate is a ratchet, not a verdict on the page.** `GATE` names each finding prefix, what
the gate does with it, and why for anything it does not refuse on; a prefix is gated once it
reports zero `FAIL` across every surface read, and a stage that closes adds its own. `0008` §4.11
is why it exists at all: clauses 8 and 4-`<title>` drifted across seven surfaces while four
stages rebuilt those pages and five rebuild-and-compare guards passed, because a guard asking
*does the page still match its inputs* cannot ask *are the inputs right*.

*This docstring used to say the gate was scheduled by `0008` S2. It was not — not by S2, which
is the stage that built this file and is closed, and not by any other. Two other artifacts
said the same thing, and `0008` §4.11 records all three.*

    python -m tools.pagespec              # the committed surfaces, gated
    python -m tools.pagespec --fetch      # judge all twelve on the served bytes,
                                          #   and compare them with the committed files
    python -m tools.pagespec --detail     # every finding, not just the failures
    python -m tools.pagespec --report-only  # print and exit zero whatever it finds

After the per-surface rows comes the **role census**, which is the one reading no
per-repository test can take: which role each property family names across every surface at
once, and which surfaces are in the minority. It is printed, never asserted. `0008` S6 and S7
rewrite nine pages, so the first correctly-migrated page *becomes* the minority — a census
that gated would go red on the work it exists to guide, and a minority row is a question for
a reader rather than a verdict. `0007` §5's governing rule is why it can only ever be a
question: where a page measured a reason and recorded it, that value wins, and no checker
can read the reason.
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

from . import clauses, render, sources

_MARK = {clauses.PASS: "ok", clauses.FAIL: "FAIL",
         clauses.UNDECIDED: "?", clauses.NOT_APPLICABLE: "-"}

#: **The two guards read eleven surfaces, and the gate covers twelve.** `test_published_surfaces`
#: swept without `--fetch`, so neither the ceiling (no gated clause fails) nor the floor
#: (every clean clause is gated) could see `wroclaw-air-insights` — and the floor would then
#: *demand* a widening measured on eleven. S9 and S10 navigated that by hand. `0009` §7 row 13b
#: is the row that closes it, and `PENDING_STATE` below is the half of the answer this file
#: holds: the sweep now follows the mode, and a key clean on the eleven can be declared
#: pending until a fetching run has seen the twelfth.
GATED_STATE = "gated"
#: Clean on the eleven committed surfaces and **not yet confirmed on the twelfth**. The
#: fetchless floor accepts it; a fetching run that finds it clean over all twelve *demands*
#: its promotion, and one that finds it failing leaves it here. This is the state that was a
#: `CLAUDE.md` paragraph, a three-outcome failure message and a hand-watched `refresh.yml`
#: rebuild — the procedure S9 and S10 executed by reading rather than by running.
PENDING_STATE = "pending"
#: Prints, never gates, and **says why in the output rather than in a docstring**. Not the
#: same claim as `conftest.NOT_A_CLAUSE`, which is a proof that a key can never be `FAIL`;
#: this is a decision taken about a key that can.
REPORT_ONLY_STATE = "report-only"
STATES = (GATED_STATE, PENDING_STATE, REPORT_ONLY_STATE)


@dataclass(frozen=True)
class Ratchet:
    """One finding prefix and what the gate does with it.

    `reason` is required for every state except `gated`, and a guard enforces it. A gated
    prefix needs no prose — the measurement licenses it and the ceiling guard re-takes that
    measurement on every run. Anything *outside* the gate is a decision, and a decision with
    no reason recorded beside it is the silence this registry exists to end.
    """

    prefix: str
    state: str
    reason: str = ""


#: The ratchet — `0008` §4.11 — a tuple until `0009` §7 row 13b made it a registry.
#:
#: A prefix enters `gated` once a run reports zero `FAIL` for it across every surface read,
#: and each closing stage adds its own. **Keyed on the finding prefix rather than the clause
#: number, because clause 4's halves disagree**: `4 h1` and `4 eyebrow` have been clean on all
#: twelve surfaces since S6 while `4 title` failed — on three of the eleven committed
#: surfaces, and on four of the twelve once `--fetch` reads the twelfth. Gating by the number
#: would either pull `4 title` in before S10 or hold the other two out.
#:
#: Measured 2026-09-07 over twelve surfaces with `--fetch`: every `FAIL` in the portfolio was
#: `4 title` (**4**) or `8 separator` (7), and nothing else failed anywhere. *The `4 title`
#: figure read three until the audit of that evening: three is the eleven-surface count, and
#: that sentence said twelve. `#86` settled the reading that moved the twelfth and its own
#: commit body says four — a hand-typed figure the instrument had already refuted, in the
#: comment block `CLAUDE.md` sends a stage editor to.*
#:
#: **Both of those are now in, and the ratchet is complete over the clauses.** `0008` S9 and
#: S10 closed them together, and with `4 title` and `8 ` here every finding key a clause can
#: report `FAIL` on is gated: `_gated` and `status == FAIL` now coincide for everything except
#: `served`. Re-measured over twelve with `--fetch`, 2026-09-08: **zero `FAIL` portfolio-wide.**
#: That is what licenses these rows, and it starts refusing the moment one of them regresses.
#:
#: *`test_a_page_failing_only_an_ungated_clause_still_passes` in `tests/test_report.py` is the
#: test that keeps the distinction alive past this point, and it survives on purpose: it
#: constructs its ungated set by removing these two prefixes rather than borrowing whatever
#: `GATED` happens to hold. Removing them was a no-op before S9/S10 and is the whole test
#: after it — which its own docstring predicted, one stage early.*
GATE: tuple[Ratchet, ...] = (
    Ratchet("1 ", GATED_STATE),
    Ratchet("2 ", GATED_STATE),
    Ratchet("3 ", GATED_STATE),
    Ratchet("4 eyebrow", GATED_STATE),
    Ratchet("4 h1", GATED_STATE),
    Ratchet("4 title", GATED_STATE),
    Ratchet("5 ", GATED_STATE),
    Ratchet("6 ", GATED_STATE),
    Ratchet("7 ", GATED_STATE),
    Ratchet("8 ", GATED_STATE),
    Ratchet(
        "served", REPORT_ONLY_STATE,
        "a mismatch is routinely not a defect: this repository re-points submodules "
        "constantly, so served-differs-from-committed is the normal state between a sibling "
        "publishing and the index bumping its gitlink. Gated, it would redden the daily run "
        "as ordinary portfolio work proceeds. The reason it was outside the gate before "
        "0009 §7 row 13b — that neither ratchet guard could see it — has expired; this one "
        "has not, and it is the one that was always about the key rather than the guards",
    ),
)

#: Derived, so the two spellings of one vocabulary cannot diverge — `0009` N1's shape, which
#: this file would otherwise be a fresh instance of. Every guard and every monkeypatch that
#: predates the registry reads this name and keeps its meaning.
GATED: tuple[str, ...] = tuple(one.prefix for one in GATE if one.state == GATED_STATE)


def pending() -> tuple[str, ...]:
    """Prefixes clean on the eleven and not yet confirmed on the twelfth. Empty at rest."""
    return tuple(one.prefix for one in GATE if one.state == PENDING_STATE)


def report_only() -> dict[str, str]:
    """Prefixes that print and never gate, each with the reason it does not."""
    return {one.prefix: one.reason for one in GATE if one.state == REPORT_ONLY_STATE}


def explained(clause: str) -> Ratchet | None:
    """The registry entry covering this finding key, whatever its state.

    The floor guard's question, and it is a different one from `_gated`'s: *has anybody said
    anything about this key at all*. A clean key covered by no entry is the ratchet narrowed.
    """
    for one in GATE:
        if clause.startswith(one.prefix):
            return one
    return None


def clean_but_unexplained(statuses: dict[str, set[str]], *,
                          exempt: frozenset[str] | set[str] = frozenset()) -> list[str]:
    """Finding keys the corpus never reports failing that no row of `GATE` covers.

    **The ratchet's floor, as arithmetic rather than as a loop inside one test.** It lives
    here and not in the suite because it is a statement about this registry, and because the
    corpus that can exercise its `pending` branches does not exist: no clause fails anywhere
    today, so a guard written only against the working trees would ship both branches
    unexecuted. `tests/test_report.py` proves them over synthetic statuses in the `core` job,
    which needs no submodule and no wire.

    `exempt` is the caller's — `conftest.NOT_A_CLAUSE`, a set whose entries carry a proof that
    the key can never be `FAIL`. That is a different question from anything this registry
    answers, and `tools/spec.py`'s own comment records what it cost to have one set answer two.
    """
    clean = {clause for clause, seen in statuses.items()
             if clauses.FAIL not in seen} - set(exempt)
    return sorted(clause for clause in clean if explained(clause) is None)


def pending_refuted(statuses: dict[str, set[str]], *, fetching: bool) -> list[tuple[str, str]]:
    """Pending rows this corpus contradicts, each with what contradicts it.

    `pending` is a claim with two halves — *clean on the eleven*, and *the twelfth is not yet
    confirmed* — and each half is refutable by a different sweep:

    - **fetchless**, a pending prefix reporting `FAIL` refutes the first half. The state is a
      confirmation the registry is waiting on, not a waiting room for a key whose stage has
      not closed.
    - **fetching**, a pending prefix that fails nowhere across all twelve refutes the second:
      the confirmation has arrived and the row must be promoted. That promotion is what S9 and
      S10 did by hand, watching a sibling's rebuild before editing a tuple.
    """
    refuted: list[tuple[str, str]] = []
    for prefix in pending():
        matching = {clause: seen for clause, seen in statuses.items()
                    if clause.startswith(prefix)}
        failing = sorted(clause for clause, seen in matching.items() if clauses.FAIL in seen)
        if not fetching and failing:
            refuted.append((prefix, f"the {sum(1 for one in sources.SURFACES if not one.must_fetch)}"
                                    f" committed surfaces report {failing} failing"))
        # A prefix the run never emitted says nothing either way, and calling that a
        # confirmation would promote a key on the strength of its own absence.
        if fetching and matching and not failing:
            refuted.append((prefix, f"no failure on any of the {len(sources.SURFACES)} "
                                    "published surfaces, this run's fetch-only one included"))
    return refuted


def _unread_same_origin(loaded: sources.Loaded) -> list[str]:
    """Sheets the page names, that exist on our side, and that the run could not read.

    Every clause reading `loaded.css` then answers from a stylesheet it knows is incomplete,
    and the page reports `clear`. Measured: renaming a same-origin sheet carrying a webfont
    `@import` takes a surface from `FAIL 7 webfont` to `clear`, exit 1 to exit 0. That is
    policy 2's own argument one level down — a renamed *stylesheet* degrading to a green pass
    instead of a renamed *page* — so it gates for the same reason.

    Read off `loaded.unreadable` rather than off the finding's message, and off the
    structured pair rather than off a formatted one. A first version parsed the
    `stylesheets` detail with `split(", ")` and the third-party marker **contains that
    separator**, so every third-party sheet split into two fragments and the second gated.
    A later reader split on `" ("` and a change that added a cause before it broke that too.
    Three readers, three prose formats: `unreadable` carries `(href, why)` now, the marker
    is `sources.THIRD_PARTY` and is compared rather than searched for, and the sentence this
    docstring had already written — *the structured value was available the whole time* —
    stops being advice the module gives and does not take.
    """
    return [sources.describe((href, why)) for href, why in loaded.unreadable
            if why != sources.THIRD_PARTY]


def _gated(finding: clauses.Finding) -> bool:
    """Only `FAIL` gates *this list* — `_unread_same_origin` is the one condition outside it,
    and `main` prints it under its own header for exactly that reason.

    `UNDECIDED` and `n/a` never do, and the list of what that protects is longer than it
    looks: clause 4's `h1`, undecided on all twelve surfaces today because *"states a claim"*
    is a judgement no checker can make (`0007` §7) — though it still **fails** on a missing
    `h1` or one equal to the repository's name, so it is not undecided *by design*; clause 3
    where a media condition is unread; clause 2 as `n/a` on a page with no tiles; and clause
    1's `composited` on seven of twelve, because resolving a `color-mix()` needs the ground
    the mark is *drawn over* (`0008` §3.2). A gate that reddened on those would be a gate on
    the checker's own honesty.
    """
    return (finding.status == clauses.FAIL
            and any(finding.clause.startswith(prefix) for prefix in GATED))


def _unreachable_sheets(loaded) -> list[str]:
    """Same-origin sheets the wire could not deliver — printed, never gating.

    The twin of `_unread_same_origin`, and the split is the policy: a sheet that is *missing*
    is the page's business and refuses the build; a sheet the *network* dropped is not. Before
    `--fetch` read the eleven only `wroclaw` fetched a sheet at all, so this distinction cost
    nothing and did not exist; now every scheduled run fetches eleven more and a blip on either
    of the two surfaces with an external sheet would have refused a page that is fine.
    """
    return [sources.describe(entry) for entry in loaded.unreachable]


def _row(name: str, findings: list[clauses.Finding], *,
         answered_from_the_file: bool = False) -> str:
    """One surface's line, and — under `--fetch` — where its verdict came from.

    **A fetch that failed falls back to the committed file, and the verdict then says nothing
    about the page anybody can open.** That fallback is right (thirteen `FAIL`s on a DNS blip
    is worse than a missing answer), but printing `clear` unqualified under a job named for
    the bytes the public receives reinstates exactly the premise `0009` §3.1 removed — and
    `clauses.py`'s own opening line calls a confident verdict a checker did not earn "that
    failure automated". The caveat costs nothing and moves no gate.
    """
    failures = sum(1 for finding in findings if finding.status == clauses.FAIL)
    undecided = sum(1 for finding in findings if finding.status == clauses.UNDECIDED)
    verdict = f"{failures} fail" if failures else "clear"
    if undecided:
        verdict += f", {undecided} undecided"
    # Keyed on the fallback having happened, not on one of the two statuses that cause it.
    # It fired on `UNDECIDED` alone, so the benign case — a wire blip — was annotated and the
    # serious one — the page answered 4xx — was not. The serious one is exactly where every
    # `ok` above came from a file whose published counterpart is not being served.
    if answered_from_the_file:
        verdict += "  (from the committed file; the wire was not read)"
    return f"  {name:<24} {verdict}"


def _census(sheets: list[tuple[str, str]]) -> list[str]:
    """Role distribution per property family, across every surface read in this run.

    Counts declarations rather than surfaces, because one sheet can hold the same role in a
    family ten times and a per-surface tally would read them as one voice.
    """
    lines: list[str] = []
    for family, properties in (("background", clauses._GROUND_PROPERTIES),
                               ("border", clauses._BORDER_PROPERTIES)):
        tally: dict[str, int] = {}
        where: dict[str, set[str]] = {}
        for name, css in sheets:
            for _selector, _body, prop, role, _scheme, _fallback in clauses._usage_sites(css):
                if prop not in properties:
                    continue
                tally[role] = tally.get(role, 0) + 1
                where.setdefault(role, set()).add(name)
        if not tally:
            continue
        total = sum(tally.values())
        lines.append(f"  {family:<12} {total} var() reference(s); color-mix() is left out "
                     "here and reported under \"1 composited\"")
        for role, count in sorted(tally.items(), key=lambda pair: (-pair[1], pair[0])):
            share = f"{count:>3} ({count / total:>4.0%})"
            surfaces = ", ".join(sorted(where[role]))
            lines.append(f"      --{role:<14}{share}  {surfaces}")
    return lines


def _separator_census(pages: list[tuple[str, str]], detailed: bool) -> list[str]:
    """Every grouped figure the surfaces render, by separator and by where it sits.

    **What `0008` §4.13 asked for, and the half of it an instrument here can carry.** That
    erratum refuses to re-type the write-site count — three hand counts gave fifteen,
    eighteen and nineteen against a true twenty — and rules that *a stage scoped by a figure
    no instrument prints is scoped by whoever counted last.* The write sites are lines of
    Python in eleven other repositories and `sources.py` is the I/O boundary and nothing
    else, so they are not this module's to count; `0009` §7 row 6 is the decision to leave
    them out. **The figures those sites reach are these bytes**, and this counts them.

    It is how the twentieth site was found. §4.13 records the reconciliation by hand: the
    checker said `ab-lab` prints two comma figures where the census named one write site,
    and the second turned out to be `examples/validation_table.py:130` — a formatter the
    repository's own ADR names and no sweep of generators had looked for. That comparison is
    the method, and printing this side of it on every run is what makes it repeatable.

    Three things it prints that the clause-8 row cannot:

    - **Figures beside separators.** `clause_8_separator` counts separator *characters* and
      its docstring says the two are equal *"because none prints a figure at or above a
      million"* — an assumption about the corpus stated in a comment. Printing both measures
      it instead, and the first figure that reaches seven digits makes the two disagree here
      rather than silently in a tally.
    - **Where each figure sits.** `doc-extract` prints `3<U+00A0>466,62` inside `<code>` as a
      displayed specimen of a foreign invoice format. That is S9c's exemption, and §4.11
      requires it censused *"so the exemption cannot silently widen"*. An exemption scoped to
      an element is checkable; one scoped to a literal string is a carve-out.
    - **Which surfaces each separator is on**, which is S9's edit order.

    Printed and asserted by nothing, exactly as the role census is — a census that gated
    would be a second clause 8 under a key no normative sentence claims.
    """
    tally: dict[str, int] = {}
    spared: dict[str, int] = {}
    figures_total = 0
    where: dict[str, set[str]] = {}
    contexts: dict[str, dict[str, int]] = {}
    rows: list[str] = []
    detail: list[str] = []

    for name, html in pages:
        figures = clauses.grouped_figures(render.parse(html))
        if not figures:
            rows.append(f"  {name:<24} no grouped figure")
            continue
        per_surface: dict[str, int] = {}
        # One predicate, feeding the surface row and the portfolio roll-up. They were two
        # loops over the same list applying the same test — a quantity at two scopes written
        # in two places, which `sources.describe`'s docstring records this project paying for.
        spared_here: dict[str, int] = {}
        for figure in figures:
            for separator in figure.separators:
                per_surface[separator] = per_surface.get(separator, 0) + 1
                tally[separator] = tally.get(separator, 0) + 1
                if figure.exempt:
                    spared_here[separator] = spared_here.get(separator, 0) + 1
                    spared[separator] = spared.get(separator, 0) + 1
                where.setdefault(separator, set()).add(name)
                contexts.setdefault(separator, {})
                contexts[separator][figure.where] = (
                    contexts[separator].get(figure.where, 0) + 1)
        figures_total += len(figures)
        # Marked on the surface row too, not only in the portfolio roll-up: this row is the
        # first thing a stage reads to scope its edits, and an unmarked `U+00A0 1` sends it
        # to a page that needs no edit — the one page whose whole subject is quoting a
        # foreign format.
        inventory = " · ".join(
            f"{separator} {count}"
            + (" exempt" if spared_here.get(separator, 0) == count else "")
            for separator, count in sorted(per_surface.items()))
        rows.append(f"  {name:<24}{len(figures):>4} figure(s)   {inventory}")
        if detailed:
            for figure in figures:
                detail.append(f"      {name:<24}{figure.display:<28} "
                              f"in <{figure.where}>"
                              + ("   specimen, exempt (8a)" if figure.exempt else ""))

    if not tally:
        return []

    separators = sum(tally.values())
    lines = rows + [""]
    # Stated as an equality that holds today rather than as a fact, because the clause's own
    # tally is in the other unit and a reader comparing the two is owed the reason they match.
    agreement = ("one separator each" if separators == figures_total
                 else f"{separators - figures_total} figure(s) at or above a million")
    lines.append(f"  {'portfolio':<24}{figures_total:>4} figure(s), {separators} separator(s) "
                 f"— {agreement}")
    for separator, count in sorted(tally.items(), key=lambda pair: (-pair[1], pair[0])):
        # A separator every one of whose figures is a clause-8a specimen is not a finding
        # about the page: `not clause 8` there would name the codepoint correctly and the
        # page wrongly, and the census is read to scope a stage's edits.
        if separator != "U+202F" and spared.get(separator, 0) == count:
            verdict = "exempt (8a)"
        else:
            verdict = "clause 8" if separator == "U+202F" else "not clause 8"
        seen = ", ".join(sorted(where[separator]))
        placed = ", ".join(f"{element} {number}" for element, number
                           in sorted(contexts[separator].items(),
                                     key=lambda pair: (-pair[1], pair[0])))
        lines.append(f"      {separator:<10}{count:>4}  {verdict:<13} {seen}")
        lines.append(f"      {'':<10}{'':>4}  in {placed}")
    return lines + ([""] + detail if detail else [])


def _policy() -> list[str]:
    """Every key the gate does not refuse on, and the reason it does not.

    **Printed, because a decision legible only to somebody already reading `__main__.py` is
    the silence this registry replaced.** `served` sat outside the gate for two stages under
    an argument that lived in a comment block and a test docstring; a reader of the table saw
    `ok served` and no indication that the key could not refuse. `tools/spec.py` prints its own
    exemptions for the same reason, and `test_no_exempt_key_is_claimed_as_a_carrier` is the
    precedent for guarding that it does.

    Gated prefixes are deliberately absent: the table above already says what they decided,
    and a list of ten prefixes that behave as documented is noise around the four lines that
    do not.
    """
    outside = [one for one in GATE if one.state != GATED_STATE]
    if not outside:
        return []
    lines = ["gate policy — the keys the gate does not refuse on, and why\n"]
    for one in outside:
        lines.append(f"  {one.prefix:<12}{one.state}")
        lines.append(textwrap.fill(one.reason, width=92,
                                   initial_indent=" " * 6, subsequent_indent=" " * 6))
    return lines + [""]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pagespec", description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2],
                        help="the index repository's working tree")
    parser.add_argument("--fetch", action="store_true",
                        help="judge every surface on the bytes it actually serves, and compare "
                             "them against the committed files")
    parser.add_argument("--detail", action="store_true", help="print every finding")
    parser.add_argument("--only", help="check one surface by name")
    parser.add_argument("--report-only", action="store_true",
                        help="print and exit zero whatever the run finds")
    args = parser.parse_args(argv)

    known = {surface.name for surface in sources.SURFACES}
    if args.only and args.only not in known:
        # A tool whose product is a table must not answer a typo with an empty one.
        parser.error(f"no surface named {args.only!r}; known: "
                     + ", ".join(sorted(known)))

    print(f"pagespec — {len(sources.SURFACES)} published surfaces, "
          f"clauses 1-8 of 0007 §5\n")

    unread: list[str] = []
    blocked: list[str] = []
    unread_sheets: list[str] = []
    unreachable_sheets: list[str] = []
    gone: list[str] = []
    absent: list[str] = []
    fetch_errors: dict[str, str] = {}
    missing = False
    sheets: list[tuple[str, str]] = []
    markup: list[tuple[str, str]] = []
    for surface in sources.SURFACES:
        if args.only and args.only != surface.name:
            continue
        loaded = sources.load(surface, args.root, allow_fetch=args.fetch,
                              errors=fetch_errors)
        if loaded is None:
            # Telling a reader to pass a flag they passed hides a network or HTTP failure
            # as operator error, on the one surface that can only be read over the wire.
            if not surface.must_fetch:
                reason = "not found"
            elif args.fetch:
                reason = "fetch failed: " + fetch_errors.get(surface.name, "no detail")
            else:
                reason = "needs --fetch"
            unread.append(f"{surface.name} ({reason})")
            # An unread surface that *should* have been readable is a failure, not a
            # skip. Otherwise a renamed path degrades to a green pass on a page nobody
            # checked, which is the silent-green shape `0008` §3.7, §3.9 and §4.9 each
            # record. `needs --fetch` is the one benign reason: the push job is
            # deliberately offline, and only the scheduled run asks for the wire.
            missing = missing or reason != "needs --fetch"
            continue

        sheets.append((surface.name, loaded.css))
        markup.append((surface.name, loaded.html))
        findings = clauses.check(loaded)
        blocked += [f"{surface.name}  {finding.clause}: {finding.detail}"
                    for finding in findings if _gated(finding)]
        unread_sheets += [f"{surface.name}  {entry}"
                          for entry in _unread_same_origin(loaded)]
        unreachable_sheets += [f"{surface.name}  {entry}"
                               for entry in _unreachable_sheets(loaded)]
        # **Two input conditions that are unambiguous regressions, and both were exempt.**
        # The `served` key carried three different facts and the exemption was argued for
        # one of them — a digest mismatch, routine while a sibling has published and the
        # index has not bumped its pointer. These two are not that and neither was argued:
        # a page answering 4xx is not being served, and a committed page absent while the
        # wire answers is `0008` §4.11 policy 2's own case, which refused before `--fetch`
        # read these eleven and stopped refusing after.
        if loaded.served_gone:
            gone.append(f'{surface.name}  {loaded.served_error}')
        if (loaded.committed is None and not surface.must_fetch
                and loaded.repo_checked_out):
            absent.append(f'{surface.name}  {surface.repo}/{surface.path}')
        print(_row(surface.name, findings,
                   answered_from_the_file=args.fetch and loaded.served is None))
        for finding in findings:
            if args.detail or finding.status in (clauses.FAIL, clauses.UNDECIDED):
                print(f"      {_MARK[finding.status]:<5} {finding.clause:<20} {finding.detail}")
        print()

    separators = _separator_census(markup, args.detail) if not args.only else []
    if separators:
        print("separator census — every grouped figure, printed and never asserted\n")
        print("\n".join(separators))
        print()

    census = _census(sheets) if not args.only else []
    if census:
        print("role census — across every surface read, printed and never asserted\n")
        print("\n".join(census))
        print()

    for line in _policy():
        print(line)

    if unread:
        print("not read: " + ", ".join(unread))
        print("  wroclaw-air-insights commits no HTML; --fetch reads its live URL, and")
        print("  reports/site/ is a gitignored local build that has been 24 days stale.")

    if args.report_only:
        return 0
    # Three reasons, three headers. Printed separately because a reader told "a clause in
    # GATED failed" and then shown a row reading `clear` has been sent to the wrong rule —
    # the stylesheet condition is an UNDECIDED, and §4.11 policy 1 is the paragraph saying
    # UNDECIDED never gates. Naming the wrong reason is how a real finding reads as noise.
    if blocked:
        print("\ngate — a clause in GATED failed; 0008 §4.11 is why this refuses\n")
        for line in blocked:
            print(f"  {line}")
        print(f"\n  {len(blocked)} gated finding(s). Ungated clauses still print above "
              "and do not reach this list.")
    if unread_sheets:
        print("\ngate — a same-origin stylesheet the page names could not be read, so every "
              "clause\n       reading its CSS answered from an incomplete one; 0008 §4.12\n")
        for line in unread_sheets:
            print(f"  {line}")
    if unreachable_sheets:
        print("\nnot gated — a same-origin stylesheet the wire did not deliver. The network is"
              "\n           not the page, so this refuses nothing, and the clauses "
              "reading its CSS say"
              "\n           `undecided` rather than failing on a sheet they never read\n")
        for line in unreachable_sheets:
            print(f"  {line}")
    if gone:
        print("\ngate — the published page answered 4xx. That is the origin saying the page is"
              "\n       not being served, which is an answer about the page; a wire failure"
              "\n       is `undecided` and prints above without refusing\n")
        for line in gone:
            print(f"  {line}")
    if absent:
        print("\ngate — a surface that commits a page has none and the wire answered in its"
              "\n       place. Pages keeps serving the last deployment, so this is "
              "invisible until"
              "\n       somebody looks; it is `0008` §4.11 policy 2, restored\n")
        for line in absent:
            print(f"  {line}")
    if missing:
        print("\ngate — a surface that should have been readable was not read")
    return 1 if (blocked or unread_sheets or gone or absent or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
