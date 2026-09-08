"""The conformance table, computed instead of typed — and, since `0008` S-gate, a gate.

`0007` §3 was corrected five times across two sessions because a per-page measurement was
kept in a normative document. This is what replaces it.

**The gate is a ratchet, not a verdict on the page.** `GATED` names the finding keys that
report zero `FAIL` across every surface read; a stage that closes adds its own. `0008` §4.11
is why it exists at all: clauses 8 and 4-`<title>` drifted across seven surfaces while four
stages rebuilt those pages and five rebuild-and-compare guards passed, because a guard asking
*does the page still match its inputs* cannot ask *are the inputs right*.

*This docstring used to say the gate was scheduled by `0008` S2. It was not — not by S2, which
is the stage that built this file and is closed, and not by any other. Two other artifacts
said the same thing, and `0008` §4.11 records all three.*

    python -m tools.pagespec              # the twelve committed surfaces, gated
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
from pathlib import Path

from . import clauses, render, sources

_MARK = {clauses.PASS: "ok", clauses.FAIL: "FAIL",
         clauses.UNDECIDED: "?", clauses.NOT_APPLICABLE: "-"}

#: The ratchet — `0008` §4.11. A finding key enters here once a run reports zero `FAIL` for it
#: across every surface read, and each closing stage adds its own. **Keyed on the finding
#: prefix rather than the clause number, because clause 4's halves disagree**: `4 h1` and
#: `4 eyebrow` have been clean on all twelve surfaces since S6 while `4 title` fails — on
#: three of the eleven committed surfaces, and on four of the twelve once `--fetch` reads the
#: twelfth.
#: Gating by the number would either pull `4 title` in before S10 or hold the other two out.
#:
#: Measured 2026-09-07 over twelve surfaces with `--fetch`: every `FAIL` in the portfolio is
#: `4 title` (**4**) or `8 separator` (7), and nothing else fails anywhere. *The `4 title`
#: figure read three until the audit of that evening: three is the eleven-surface count, and
#: this sentence says twelve. `#86` settled the reading that moved the twelfth and its own
#: commit body says four — a hand-typed figure the instrument had already refuted, in the
#: comment block `CLAUDE.md` sends a stage editor to.* So this set costs no
#: page change today — it starts refusing the moment one of them regresses, which is the point.
#: `8 separator` enters with S9; `4 title` with S10.
#:
#: **The two guards on this tuple read eleven surfaces, not twelve.** `test_published_surfaces`
#: sweeps without `--fetch`, so neither the ceiling (no gated clause fails) nor the floor
#: (every clean clause is gated) can see `wroclaw-air-insights`. Widen this tuple only after
#: `python -m tools.pagespec --fetch` agrees: the `surfaces` job cannot see the twelfth
#: surface, so a widening that is premature merges green and reddens the scheduled `live`
#: run instead.
#: **`served` is deliberately absent, and the reason is not that it fails.** It reports zero
#: `FAIL` across every surface read, which is this tuple's own entry condition. It is out
#: because *neither ratchet guard can see it*: both derive from a sweep hardcoding
#: `allow_fetch=False`, so gating it adds a prefix the ceiling cannot check and the floor
#: cannot demand — a place for a key to hide. And the stronger reason, which is about the key
#: rather than the guards: **a mismatch is routinely not a defect at all.** This repository
#: re-points submodules constantly, so served-differs-from-committed is the normal state
#: between a sibling publishing and the index bumping its gitlink. Gated, this key would redden
#: the daily run as ordinary portfolio work proceeds — the cries-wolf failure `conftest.py`
#: warns about. It may be that gating it is never right; that is worth settling deliberately
#: rather than inheriting.
GATED: tuple[str, ...] = ("1 ", "2 ", "3 ", "4 eyebrow", "4 h1", "5 ", "6 ", "7 ")




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
        for figure in figures:
            for separator in figure.separators:
                per_surface[separator] = per_surface.get(separator, 0) + 1
                tally[separator] = tally.get(separator, 0) + 1
                where.setdefault(separator, set()).add(name)
                contexts.setdefault(separator, {})
                contexts[separator][figure.where] = (
                    contexts[separator].get(figure.where, 0) + 1)
        figures_total += len(figures)
        inventory = " · ".join(
            f"{separator} {count}" for separator, count in sorted(per_surface.items()))
        rows.append(f"  {name:<24}{len(figures):>4} figure(s)   {inventory}")
        if detailed:
            for figure in figures:
                detail.append(f"      {name:<24}{figure.display:<28} "
                              f"in <{figure.where}>")

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
        verdict = "clause 8" if separator == "U+202F" else "not clause 8"
        seen = ", ".join(sorted(where[separator]))
        placed = ", ".join(f"{element} {number}" for element, number
                           in sorted(contexts[separator].items(),
                                     key=lambda pair: (-pair[1], pair[0])))
        lines.append(f"      {separator:<10}{count:>4}  {verdict:<13} {seen}")
        lines.append(f"      {'':<10}{'':>4}  in {placed}")
    return lines + ([""] + detail if detail else [])


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
