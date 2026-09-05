# What carries the page spec

Date: 2026-09-05
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`0007_divergence-and-the-page-spec.md`](../audit/0007_divergence-and-the-page-spec.md) §5.2 (the
carrier this supersedes), [`0006_session3-4-presentation-block.md`](../audit/0006_session3-4-presentation-block.md)
§4 (options C-a…C-d) and §3 L2 (the pinning precedent this argues from),
[`0008_the-rollout-ledger.md`](../audit/0008_the-rollout-ledger.md) (the plan this unblocks)

---

## 1. Context

`0007` §5.2 settled the spec's carrier as *"prose plus a per-repo acceptance test, computed by **one vendored
checker** — the pattern `doc-extract` already uses for its XSDs and fonts"*, hash-pinned per repository. That is
`0006` §4's option C-b, taken together with C-a.

It was chosen without measuring three things, all of which are now measured and two of which refute it.

## 2. What was measured, 2026-09-05

### 2.1 Most of the checker already exists, in two halves, green in CI

`0007` §5.2 speaks of the checker as work not started. It is roughly two thirds built, in two repositories, and
no audit document notices that the two halves compose.

**The static half** — `apply-scout/tests/test_docs_page.py:92`, `class _Rendered(HTMLParser)`. It already
collects `metas` (`:115`, clause 5), `headline` (`:111`, clause 4), `tables` (`:112`) and
`table_ancestors` (`:114`, clause 3), and `_scrolling_classes()` (`:696`) parses `overflow(-x): auto|scroll` out of the page's own
`<style>`. It carries fail-closed logic bought the hard way: a `_VOID` element set (`:104`) and an `unclosed`
counter (`:177`), because a wrapper that never closes makes every table below it read as wrapped — a false green
in the direction that matters.

**The contrast half** — `pl-review-sense/tests/test_palette.py:62`, a working WCAG `contrast()` with
`TEXT_MINIMUM = 4.5` and `GRAPHIC_MINIMUM = 3.0` (`:24-25`), asserting `accent-soft` against `bg` at the graphic
minimum (`:92`). That is clause 1's contrast half, built and passing.

### 2.2 The spec splits into a static half and a rendered half, and only the rendered half needs a browser

Clauses 1, 2, 4, 5, 6, 7 and 8 are text and DOM checks over committed bytes: no browser, standard library only.
Clause 3 splits — the *name* `.table-wrap` is static, but *"computes to `overflow-x: auto` and has somewhere to
scroll"* needs layout, which is what `measure_page.py` provides at the cost of `requests`, `websocket-client`
and a Chromium binary.

This is the fact that decides the checker's shape, and no document states it.

### 2.3 The vendoring pattern does not generalise — it fails outright on two repositories

`wroclaw-air-insights/.gitignore:42-43` reads `.claude/*` then `!.claude/skills/`: the tool is committed
*because that repository un-ignores it on purpose*. Measured across the other eleven:

| repository | rule |
|---|---|
| `pl-jobs-lora` | `.gitignore:55` — `.claude/`, **the whole directory** |
| `apply-scout` | `:33` — `.claude/sessions/` only |
| `doc-extract` | `:29`, `:33` — `sessions/` and `worktrees/` only |
| `pl-review-sense` | `:27` — `settings.local.json` only |
| seven others | **no `.claude` rule at all** |

A checker vendored under `.claude/skills/` would be silently untracked in `pl-jobs-lora`. And `mini-traceroute`
is C++/CMake with **no `pyproject.toml` and no Python test suite** — it cannot host a per-repo Python acceptance
test at all.

Eleven hash-pinned copies also re-run this portfolio's own worst pattern. `0006` §3 L2 refused SHA-pinning
first-party actions with the reason: *"a SHA pin in a portfolio with no bot to move it decays into a stale
action — which is precisely the state `0003` §6 had to dig this portfolio out of, eleven repositories at
once."* Eleven pinned checker copies with no bot to move them is that argument verbatim, one layer up.

### 2.4 Seven repositories already have a test that reads the published page

| repository | file |
|---|---|
| `ab-lab` | `tests/test_site_committed.py` — byte-equality of the committed page against the generator |
| `apply-scout` | `tests/test_docs_page.py` — the `_Rendered` parser of §2.1 |
| `auth-log-scan` | `tests/test_site.py` — parses the page with `HTMLParser` |
| `car-price-ml` | `tests/test_site.py` |
| `doc-extract` | `tests/test_site_claims.py`, `tests/test_site_committed.py`, `tests/test_degrade_page.py` |
| `it-job-radar` | `tests/test_site.py` |
| `pl-review-sense` | `tests/test_site.py`, `tests/test_palette.py` |

`wroclaw-air-insights/tests/test_verify_published_page.py` is **not** in this list: it exercises the measuring
instrument's fixtures, not the page's conformance. It is the repository that *hosts* the rendered half, which is
a different role.

## 3. Options

| | carrier | cost | drift resistance | covers `mini-traceroute`? | covers `pl-jobs-lora`? |
|---|---|---|---|---|---|
| **K-a** | Eleven hash-pinned vendored copies — `0007` §5.2 as written | high: 11 CI wirings, 11 pins, no bot | high while pinned, then decays | **no** — no `pyproject.toml` | **no** — `.gitignore:55` |
| **K-b** | One checker in the index repo, run over all twelve working trees | low: one copy, one CI | highest — one copy cannot diverge | yes | yes |
| **K-c** | K-b **plus** assertions appended to the seven page tests that already exist | low+ | highest, and pre-merge in seven repositories | yes, via K-b | yes, via K-b |

## 4. Decision

**Take K-c.**

One checker lives in the index repository and runs over all twelve submodule working trees. The seven
repositories of §2.4 additionally get three to five assertions appended to a test file that already exists — no
vendoring, no pin, no new CI wiring, no new dependency.

**Split it by §2.2.** The static core is standard-library only and runs everywhere for free. The rendered half
stays exactly where it is — `wroclaw-air-insights/.claude/skills/verify-published-page/measure_page.py`, already
merged and already generalised over two review rounds — and is *invoked* for the geometry column rather than
copied.

Coverage of all twelve, stated here rather than discovered later. The seven of §2.4 carry assertions of their
own **and** are read by the index checker. Three more — **`mini-traceroute`, `mlops-car-price` and
`pl-jobs-lora`**, the hand-written pages in repositories with no Python page test — are covered by the index
checker alone. `token-budget` has no page and is out of scope entirely.

**`wroclaw-air-insights` is the twelfth and it is a different case, which K-b as stated does not cover.**
"Run over all twelve working trees" assumes every page is committed bytes; this one is not. `.gitignore:25`
ignores `reports/site/`, the page ships as a Pages artifact, and `git ls-files '*.html'` returns only the
measuring skill's fixtures — **a static core reading the working tree finds no page there at all.** So the
index checker must take that page **by fetch, from the live URL**, exactly as `0007` §2 requires and as
`measure_page.py` already does natively (it accepts a URL or a path). This is a source rule, not an
exemption: the page is checked, from the only surface that exists.

### 4.1 Two constraints the implementation must carry

- **The static core must read same-origin external stylesheets, not only the inline `<style>`.**
  `_scrolling_classes()` reads `<style>` alone, which is precisely the trap that recorded `mini-traceroute`
  wrongly for three sessions (`0007` §2): that page is the one whose CSS is not inlined.
- **`measure_page.py`'s exit status is not the geometry verdict.** Its `marker_ok` feeds `healthy`, so it exits
  non-zero on the ten pages that print no build stamp, regardless of whether their tables fit. The index checker
  reads the table lines, not the exit code. `0006` §4.2 flagged this and it was never settled; it is settled
  here.

## 5. And the spec document splits with it

`0007` mixes three things with three different lifetimes, and every correction round — §8.1 through §8.5, some
twenty-six recorded corrections — has landed in the perishable two while the normative part stood untouched.

| part | lifetime | disposition |
|---|---|---|
| §5 clauses 1–8, §5.1, §6 clause 9, the governing rule | stable — a set of rules | **accepted as normative** |
| §3 and §3.1, the conformance table | perishable — corrected five times | **frozen with a date, superseded by the checker's output at S2** |
| §9, the rollout | perishable — a plan, not a measurement | **moved to `0008`, the ledger** |

A document that states measurements cannot be accepted without freezing them; a document that states rules can.
This is the structural fix for §8.2–§8.5, and it is the reason those sections kept growing rather than closing.

`0007` §4.1 makes the argument about itself: it names `pl-review-sense/tests/test_palette.py` as *"a fourth
surface — and the only one that fails when the value drifts."* Every one of its own corrections is in prose and
none is in a test.

## 6. Consequences

- `apply-scout/docs/index.html:18-20`'s shipped `Provisional: … until that spec lands` comment can be closed —
  a published page's source comment has been waiting on this decision.
- The rollout can start before the checker exists, because K-c's index half is report-only first (`0008` S2): a
  gate written before any page is green has no reference to gate against.
- **K-c is reversible into K-a** if a repository ever needs to enforce the spec without the index present. The
  reverse is the expensive direction, which is why the cheap one is taken first.
- The counter-argument stays on the record: a checker in the *private* index means the twelve public
  repositories carry no visible proof that a spec governs them. Seven of them will carry assertions, which is
  the partial answer; the other **four** will not — the three of §4 plus `wroclaw`, whose own test covers the
  instrument rather than the page — and a reader of those four cannot see the rule.
