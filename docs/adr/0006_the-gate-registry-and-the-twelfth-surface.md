# The gate registry, and the twelfth surface

Date: 2026-09-08
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`0004_what-carries-the-page-spec.md`](0004_what-carries-the-page-spec.md) §6 (the
ratchet this reshapes), [`0005_the-clause-registry.md`](0005_the-clause-registry.md) (the same
move, one vocabulary over), [`../audit/0008_the-rollout-ledger.md`](../audit/0008_the-rollout-ledger.md)
§4.11 (why the gate exists) and §4.18 (what this stage measured),
[`../audit/0009_the-review-of-the-whole-system.md`](../audit/0009_the-review-of-the-whole-system.md)
§7 rows 8, 12 and 13b

---

## 1. The decision

**`GATED`, a tuple of prefixes, becomes `GATE`, a registry of `(prefix, state, reason)` with
three states**, and **the ratchet's two guards take their corpus from the mode the run is in**
rather than from a constant.

| state | what the gate does | who demands it |
|---|---|---|
| `gated` | refuses the build on `FAIL` | the floor, in either mode |
| `pending` | refuses nothing; a key clean on the eleven whose twelfth is unconfirmed | the fetching floor **promotes** it |
| `report-only` | refuses nothing, ever, and says why in the run's own output | nothing; it is a decision |

`GATED` survives as a **derived** tuple, so every guard and every monkeypatch written against
the old name keeps its meaning. Two lists of one vocabulary tied by nothing is `0009` N1's
shape, and this file would otherwise have been its next instance.

## 2. The problem, which is not the one row 13b names

`0009` §7 row 13b asks for one thing: parametrise the sweep's fetch mode so the ratchet reads
the twelve surfaces the gate covers rather than the eleven that commit a file. Taken literally
and alone, **it does not land**, and the reason is three guards that were each right:

| guard | claim | where |
|---|---|---|
| the floor | every key the corpus never fails is in `GATED` | `test_published_surfaces.py` |
| the `served` pin | `served` is **not** in `GATED` | `test_report.py` |
| the two-set guard | `served` is **not** in `NOT_A_CLAUSE` | `test_spec.py` |

The moment the floor sweeps with `--fetch`, `served` is emitted and is `PASS` on eleven of
eleven. The first guard then demands what the second refuses, and the third closes the only
escape — correctly, because `NOT_A_CLAUSE`'s pin requires a proof that a key can *never* be
`FAIL`, and `served` fails whenever a sibling publishes ahead of a pointer bump. There is no
arrangement of the existing vocabulary that satisfies all three.

`0009` §7 row 8 had already noticed the shape of what was missing — *"`served` can be `FAIL`,
so it belongs in neither `NOT_A_CLAUSE` nor the clause registry, and the taxonomy needs a third
answer"* — and left it. This is that answer.

## 3. Why `pending` is a state and not a comment

The eleven/twelve gap is not an accident of the guards. `wroclaw-air-insights` commits no HTML
and republishes daily from a Pages artifact, so its page does not move when its pull request
merges. A stage that cleans a clause across the eleven therefore arms the floor's demand while
the twelfth may still fail — and a widening made on that demand merges green and reddens the
next morning's scheduled run.

Before this decision the procedure for that was carried by **five artifacts and no
instrument**: a paragraph of `CLAUDE.md`, a three-outcome failure message inside the floor
guard, a comment block in `__main__.py`, `0009` §11, and a test docstring. S9 and S10 each
executed it by reading — land the siblings, hold the pointers, confirm the twelfth by hand,
then bump and widen in one commit.

`pending` is that procedure run rather than read. A key clean on the eleven is declared
pending with its reason; the fetchless floor accepts it, so the pointer bump lands green; and
the next `live` run — which reads all twelve — either **demands its promotion** or leaves it,
which is exactly the question a person was answering by hand.

**It ships with no members, and that is stated rather than hidden.** Nothing fails anywhere in
the portfolio today, so the working trees cannot exercise either of its branches. The
arithmetic therefore lives in `__main__` as two pure functions and is proved in the `core` job
over synthetic statuses — `0009` §7 row 12's contrast clause is the admission that will use it
first.

## 4. What the corpus must not be allowed to hide

A fetching sweep has four ways to be incomplete, and three of them are silent:

1. the twelfth did not answer — the count catches this one;
2. one of the eleven could not be fetched and its verdict came from its committed file, so
   *clean on the twelve published surfaces* is a claim about a file nobody served;
3. a same-origin **stylesheet** the wire dropped, which
   `_undecided_where_the_stylesheet_is_incomplete` turns from `FAIL` into `UNDECIDED` on every
   clause-1 and clause-3 key — so a genuinely failing clause reads *clean* and the floor
   demands its admission on a sheet the run never opened;
4. the mode never reaching `sources.load` at all, which takes the wire away from all twelve and
   makes the corpus incomplete for a reason that is not the network's.

**All four skip, and skipping is the decision.** None of them is a statement about a page, and
a guard that reddens on a DNS blip is the check that gets silenced — `conftest.py` opens by
warning about exactly that. The gate itself is unaffected: `python -m tools.pagespec --fetch`
still refuses on a 404, on a committed page gone missing while the wire answers, and on an
unread same-origin sheet, each under its own header.

The fourth needed its own assertion, because a skip is a pass. With `_fetch` stubbed to answer
from disk no fetch can fail, so an incomplete corpus there has exactly one cause and the guard
fails instead of skipping. Measured: without that branch, hardcoding the mode back to `False`
left the test green with the row's whole subject unmeasured.

## 5. Consequences

- **A new clause enters the gate in two steps rather than one**, and the second is automatic.
  That is a price, and it is the smaller half of the trade: the first step is now safe to merge.
- **The policy is printed.** `gate policy` in the run's output names every key the gate does not
  refuse on, with its reason. `served` sat outside the gate for two stages under an argument
  that existed only in a comment block and a test docstring, where no reader of the table could
  find it. `tools/spec.py` prints its own exemptions for the same reason and
  `test_no_exempt_key_is_claimed_as_a_carrier` is the precedent for guarding that it does.
- **The scheduled `live` job now runs guards as well as the checker**, after the table and under
  `if: always()`. That order is deliberate and is the opposite of the `surfaces` job's: `live`
  is the only place the twelfth surface's findings are ever printed, so a guard failing first
  would suppress the one output a reader needs in order to act on it.
- **`--fetch` is the knob's spelling in pytest too**, and not `--live` or an environment
  variable. `test_the_wire_never_reaches_the_push_path` reads `pagespec.yml` and scans job lines
  for that literal string; a differently-spelled knob would open a door onto the merge path
  that the one guard against that door could not see. That guard's own docstring records it
  being too narrow twice, and `0009` §13.6 names the class.
- **`ADR-0004` §6's amendment stands unchanged.** The ratchet is still the index half of K-c and
  still gates per clause rather than per page; this decision is about the ratchet's shape, not
  about what carries the spec.
- **Reversible into the tuple** by deleting the non-`gated` rows and the two pure functions.
  Nothing outside `__main__` reads the states except the floor guard.

## 6. What was considered and refused

- **Have the twelfth commit a file**, collapsing eleven/twelve into twelve/twelve. Refused by
  the surface: `wroclaw` publishes a Pages artifact rebuilt daily from live PM2.5 data, so a
  committed copy is stale by construction and would fail its own `served` comparison every day.
- **Have `live` commit a machine-written record of the twelfth's verdict, read by the push-time
  floor.** `pagespec.yml` is `permissions: contents: read`, and giving CI write access to close
  a guard asymmetry is a large blast radius for a small problem. A cached measurement trusted at
  push time also reinstates the trusted-figure class `0007` §3 was split for.
- **Run the floor only in `live`,** dropping it from the push path. It closes the deadlock
  outright and gives up the thing `#83` was built for: a narrowing would then merge green and be
  caught up to a day later, and only if the wire cooperated. Its central invariant — *the floor
  runs in this job and not that one* — could only ever be guarded by reading YAML, which is the
  guard shape this repository has had too narrow three times.
