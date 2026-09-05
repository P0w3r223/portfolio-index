"""Report mode: compute the conformance table instead of typing it.

`0007` §3 was corrected five times across two sessions because a per-page measurement was
kept in a normative document. This is what replaces it. **Report only** — it prints and exits
zero whatever it finds, because a gate written before any page is green has no reference to
gate against, and `0008` S2 schedules the gate after the rollout rather than before it.

    python -m tools.pagespec              # the twelve committed surfaces
    python -m tools.pagespec --fetch      # and wroclaw, from its live URL
    python -m tools.pagespec --detail     # every finding, not just the failures

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
            for _selector, _body, prop, role, _scheme in clauses._usage_sites(css):
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
    args = parser.parse_args(argv)

    known = {surface.name for surface in sources.SURFACES}
    if args.only and args.only not in known:
        # A tool whose product is a table must not answer a typo with an empty one.
        parser.error(f"no surface named {args.only!r}; known: "
                     + ", ".join(sorted(known)))

    print(f"pagespec — {len(sources.SURFACES)} published surfaces, "
          f"clauses 1-8 of 0007 §5\n")

    unread: list[str] = []
    sheets: list[tuple[str, str]] = []
    for surface in sources.SURFACES:
        if args.only and args.only != surface.name:
            continue
        loaded = sources.load(surface, args.root, allow_fetch=args.fetch)
        if loaded is None:
            # Telling a reader to pass a flag they passed hides a network or HTTP failure
            # as operator error, on the one surface that can only be read over the wire.
            if not surface.must_fetch:
                reason = "not found"
            elif args.fetch:
                reason = "fetch failed"
            else:
                reason = "needs --fetch"
            unread.append(f"{surface.name} ({reason})")
            continue

        sheets.append((surface.name, loaded.css))
        findings = clauses.check(loaded)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
