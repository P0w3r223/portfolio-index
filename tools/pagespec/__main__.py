"""Report mode: compute the conformance table instead of typing it.

`0007` §3 was corrected five times across two sessions because a per-page measurement was
kept in a normative document. This is what replaces it. **Report only** — it prints and exits
zero whatever it finds, because a gate written before any page is green has no reference to
gate against, and `0008` S2 schedules the gate after the rollout rather than before it.

    python -m tools.pagespec              # the twelve committed surfaces
    python -m tools.pagespec --fetch      # and wroclaw, from its live URL
    python -m tools.pagespec --detail     # every finding, not just the failures
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

        findings = clauses.check(loaded)
        print(_row(surface.name, findings))
        for finding in findings:
            if args.detail or finding.status in (clauses.FAIL, clauses.UNDECIDED):
                print(f"      {_MARK[finding.status]:<5} {finding.clause:<20} {finding.detail}")
        print()

    if unread:
        print("not read: " + ", ".join(unread))
        print("  wroclaw-air-insights commits no HTML; --fetch reads its live URL, and")
        print("  reports/site/ is a gitignored local build that has been 24 days stale.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
