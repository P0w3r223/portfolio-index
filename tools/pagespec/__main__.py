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
    python -m tools.pagespec --fetch      # and wroclaw, from its live URL
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

from . import clauses, sources

_MARK = {clauses.PASS: "ok", clauses.FAIL: "FAIL",
         clauses.UNDECIDED: "?", clauses.NOT_APPLICABLE: "-"}

#: The ratchet — `0008` §4.11. A finding key enters here once a run reports zero `FAIL` for it
#: across every surface read, and each closing stage adds its own. **Keyed on the finding
#: prefix rather than the clause number, because clause 4's halves disagree**: `4 h1` and
#: `4 eyebrow` have been clean on all twelve surfaces since S6 while `4 title` fails on three.
#: Gating by the number would either pull `4 title` in before S10 or hold the other two out.
#:
#: Measured 2026-09-07 over twelve surfaces with `--fetch`: every `FAIL` in the portfolio is
#: `4 title` (3) or `8 separator` (7), and nothing else fails anywhere. So this set costs no
#: page change today — it starts refusing the moment one of them regresses, which is the point.
#: `8 separator` enters with S9; `4 title` with S10.
#:
#: **The two guards on this tuple read eleven surfaces, not twelve.** `test_published_surfaces`
#: sweeps without `--fetch`, so neither the ceiling (no gated clause fails) nor the floor
#: (every clean clause is gated) can see `wroclaw-air-insights`. Widen this tuple only after
#: `python -m tools.pagespec --fetch` agrees: the `surfaces` job cannot see the twelfth
#: surface, so a widening that is premature merges green and reddens the scheduled `live`
#: run instead.
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


def _row(name: str, findings: list[clauses.Finding]) -> str:
    failures = sum(1 for finding in findings if finding.status == clauses.FAIL)
    undecided = sum(1 for finding in findings if finding.status == clauses.UNDECIDED)
    verdict = f"{failures} fail" if failures else "clear"
    if undecided:
        verdict += f", {undecided} undecided"
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pagespec", description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2],
                        help="the index repository's working tree")
    parser.add_argument("--fetch", action="store_true",
                        help="also read the surfaces that exist only at a live URL")
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
    fetch_errors: dict[str, str] = {}
    missing = False
    sheets: list[tuple[str, str]] = []
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
        findings = clauses.check(loaded)
        blocked += [f"{surface.name}  {finding.clause}: {finding.detail}"
                    for finding in findings if _gated(finding)]
        unread_sheets += [f"{surface.name}  {entry}"
                          for entry in _unread_same_origin(loaded)]
        print(_row(surface.name, findings))
        for finding in findings:
            if args.detail or finding.status in (clauses.FAIL, clauses.UNDECIDED):
                print(f"      {_MARK[finding.status]:<5} {finding.clause:<20} {finding.detail}")
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
    if missing:
        print("\ngate — a surface that should have been readable was not read")
    return 1 if (blocked or unread_sheets or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
