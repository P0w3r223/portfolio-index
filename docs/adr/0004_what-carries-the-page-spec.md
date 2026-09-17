# What carries the page spec

Date: 2026-09-05
Status: accepted
Author: Piotr Cząstkiewicz + Claude
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

*Amended 2026-09-08 — the geometry half is **deferred and unowned**, and the present tense above was an
intention.* `0009` N3 named it; the trees confirm the conclusion and **refute the evidence it was given**.

**What reproduces.** `measure_page.py` is tracked at that path and `wroclaw` tests it properly: a pure layer
that runs everywhere, and a browser layer — `test_the_walk_returns_the_verdict_the_fixture_expects` — that
calls `measure_page.measure()` against a real Chromium and skips where there is none. So N3's *"it appears in
two comments and no call"* is wrong: there are calls, and one of them drives the engine.

**What has no carrier is narrower and worse.** Every one of those calls points the instrument at **the skill's
own fixtures**. Nothing points it at a published surface. `measure()` has never been run against the twelve as
a scheduled or gated act, so the geometry column the sentence above promises does not exist and never has —
the instrument is tested and it is not aimed. *A sweep asking "is this file called?" answers yes and moves on;
the question the ADR's sentence actually makes is "is it called **on the pages**", and the two have opposite
answers.*

**The resolution is this amendment rather than the implementation, and two arguments agree.** §2.2 prices the
rendered half at `requests`, `websocket-client` and a Chromium binary, while the sentence directly above chose
K-c on *"no vendoring, no pin, no new CI wiring, no new dependency"* — so building the geometry column into the
index checker spends exactly the currency K-c was selected for, which reopens K-c rather than closing a task
inside it. And the repository that owns the instrument has already reached the same place independently:
`test_verify_published_page.py:18-22` keeps its browser layer **skipped in CI on purpose**, on the grounds that
*"the walk is measured in a real engine or it is not measured at all — reimplementing CSS overflow in Python to
keep CI green would test the reimplementation."* A gate that skips wherever it runs is not a gate, and that is
the honest state of the only mechanism there is.

**Where the gap is visible now.** `tools/spec.py` carries clause 3's geometry sentence as `c3.s2` with a `why`
and **no carrier**, so `python -m tools.spec` prints it uncarried on every run. That is the home `ADR-0005` was
taken for and it is stronger than this paragraph: prose can be read past, and the registry's guards refuse a
clause that claims a carrier it does not have.

**What would reopen it**, stated so the deferral reads as a decision and not an omission: a static proxy for
*"has somewhere to scroll"* that needs no browser; or `wroclaw`'s existing browser layer aimed at the published
surfaces rather than at its fixtures, which costs **that** repository the dependency it already carries instead
of costing it to all twelve — §2.4's pattern, applied to the one clause half this ADR could not place.

Coverage of all twelve, stated here rather than discovered later. The seven of §2.4 carry assertions of their
own **and** are read by the index checker. Three more — **`mini-traceroute`, `mlops-car-price` and
`pl-jobs-lora`**, the hand-written pages in repositories with no Python page test — are covered by the index
checker alone. `token-budget` has no page and is out of scope entirely.

> **Amended 2026-09-06, twice, and both times because a repository could host a test §2.4 had not counted.**
> `wroclaw-air-insights` joined in S6 and S7: `tests/test_report.py` now asserts clause 6's *exactly one*
> back-link, clause 5's seven tags, that no card description quotes a figure the run measured, and that every
> token the charts paint is one the stylesheet declares. §2.4 excluded that repository because
> `test_verify_published_page.py` exercises the instrument rather than the page — which was true of that file
> and not of the repository.
>
> **S4 adds `mlops-car-price` and `pl-jobs-lora`.** Both have a live pytest suite and a CI workflow; what they
> lacked was a page test, not the means to host one. And S4 needs one: the constraint that every figure is a
> committed artifact's cell is **unenforceable by the index checker**, which reads a page's HTML and CSS and
> cannot see its repository's artifacts. So is clause 2's binding, for the same reason — `clause_2_tiles`
> grants §5.1's fallback to any page with no tiles.
>
> **Seven becomes ten, and the uncovered set becomes one.** `mini-traceroute` is the remainder: no
> `pyproject.toml`, a C++ suite, and no place to put a Python assertion — a structural exemption rather than
> an omission. This is not a retreat from K-c toward K-a: nothing is vendored, nothing is copied, no checker
> is duplicated. Each test asserts only what is local to its own repository, which is exactly what §2.4's
> seven do.

**`wroclaw-air-insights` is the twelfth and it is a different case, which K-b as stated does not cover.**
"Run over all twelve working trees" assumes every page is committed bytes; this one is not. `.gitignore:25`
ignores `reports/site/`, the page ships as a Pages artifact, and `git ls-files '*.html'` returns only the
measuring skill's fixtures — **a static core reading the working tree finds no page there at all.** So the
index checker must take that page **by fetch, from the live URL**, exactly as `0007` §2 requires and as
`measure_page.py` already does natively (it accepts a URL or a path). This is a source rule, not an
exemption: the page is checked, from the only surface that exists.

> **Amended 2026-09-07 — `#90`, and the twelfth stops being the different case.** The source
> rule above is now the rule for *all* twelve, not the exception for one: under `--fetch` the
> checker answers every clause from the served bytes, and the eleven that also commit a file get
> a `served` finding comparing the two. `0009` §3.1 records why — reading a committed file at
> the superproject's pinned gitlink answers a question about a *published* page from something
> that is not it, which is `0007` §2's founding failure inside the instrument built to end it.
>
> **K-c's index half is unchanged in shape and changed in source.** One checker, no vendoring,
> no pin, no new dependency; the push path still reads working trees and never the network, and
> the fetch lives in the scheduled job alone. What moved is which bytes the `live` job judges.
> Recorded here because §6's gate bullet was amended on the same principle — *turning on a gate
> while the ADR licensing the instrument still says report-only first would be the same defect
> facing the other way* — and changing which bytes K-c judges is the same size of move.

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

  *Amended 2026-09-07 — the deferral was right and its reason expired.* It is stated of **a page**, and per
  page it still holds: three of twelve read `clear`. But the gate does not have to be per page. Measured
  across all twelve surfaces, clauses 1, 2, 3, 5, 6 and 7 report **zero `FAIL`** and clause 4's `h1` and
  eyebrow halves do too — so per **clause** there is a reference to gate against, and it costs no page change.
  `0008` S-gate makes the index half a **ratchet**: `GATED` in `tools/pagespec/__main__.py` names the keys
  that are clean everywhere, a closing stage adds its own, and `UNDECIDED` never gates.

  **This bullet is why the amendment is written here rather than only in the code.** `0008` §3.8 records the
  inverse — a rule in code that no document states — and turning on a gate while the ADR licensing the
  instrument still says *report-only first* would be the same defect facing the other way. Two other artifacts
  carried the un-amended claim in a stronger form: `pagespec.yml` and the checker's own docstring both said
  `0008` scheduled the gate, and it scheduled none (`0008` §4.11).
- **K-c is reversible into K-a** if a repository ever needs to enforce the spec without the index present. The
  reverse is the expensive direction, which is why the cheap one is taken first.
- The counter-argument stays on the record: a checker in the *private* index means the twelve public
  repositories carry no visible proof that a spec governs them. Seven of them will carry assertions, which is
  the partial answer; the other **four** will not — the three of §4 plus `wroclaw`, whose own test covers the
  instrument rather than the page — and a reader of those four cannot see the rule.

  *Amended 2026-09-06: the four are one.* `wroclaw` gained page assertions in S6 and S7, and S4 gives them to
  `mlops-car-price` and `pl-jobs-lora`, leaving `mini-traceroute` alone — where the exemption is structural.
  **The cost recorded here was real and it was paid down by stages doing other work**, which is worth noting:
  each of those three got its test because a stage needed a carrier the index checker could not be, not
  because anyone set out to close this gap.

  *Amended 2026-09-17: the premise of the cost is gone, and what survives it is smaller and different in
  kind.* `0011` §6 route A published this index as `P0w3r223/portfolio-index`, so the word **private** in the
  bullet above stopped being true — and with it the reason a reader of `mini-traceroute` could not see the
  rule. The spec, the checker and the conformance table now sit at a public URL any sibling's README can
  link. **What is left is not visibility but locality**: `mini-traceroute` still carries no assertion of its
  own, holds no Python at all, and remains the one surface the index checker guards alone, so a reader who
  clones *that* repository and runs *its* tests still learns nothing about the page spec. That is K-c's
  actual residual cost, and it was always the smaller half of the two this bullet conflated. *Recorded
  rather than struck, because the bullet is part of the reasoning K-c was accepted on: a decision whose
  stated cost has quietly expired is a decision nobody can re-examine. `0012` §2 names the class.*
