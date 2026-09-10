# The review of the whole system

Date: 2026-09-07
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: [`0008_the-rollout-ledger.md`](0008_the-rollout-ledger.md) (the plan this reviews, and
which keeps the plan — §7 below is a recommendation and not a schedule),
[`0007_divergence-and-the-page-spec.md`](0007_divergence-and-the-page-spec.md) §5 (the spec),
[`../adr/0004_what-carries-the-page-spec.md`](../adr/0004_what-carries-the-page-spec.md) (the carrier),
and `#81`, which closes §7's first row

---

## 1. What this is, and what it is not

A review of the system as a whole — its architecture, the checker's code, its guards, and the
workflow that runs all three — taken 2026-09-07 against `main` at `80987c4`. Three passes ran in
parallel over the same tree (architecture, code, tests) and a fourth question, *what is this
project's agent configuration doing*, was answered in the session that commissioned them.

**It is a record and not a plan.** `ADR-0004` §5's split holds here as everywhere: `0007` §5 keeps
the rules, the checker owns the conformance table, `0008` owns the plan and its status. This file
owns *what the review found*. §7 states a sequence because findings that unblock other findings
are worth ordering, but nothing here schedules anything — a row moves into `0008` when it is taken.

**Every figure was reproduced against the trees before being written here**, which is `0008` §3's
rule applied to a document that reviews it. Where a pass asserted something that did not reproduce,
that is recorded in §8 rather than quietly dropped, including three cases where the wrong claim was
this session's own.

## 2. The state the review was taken against

`main` at `80987c4`; twelve submodule pointers equal to their own `origin/main` after a `git fetch`;
no open pull request in any of the thirteen repositories; CI green on `main` at `0e0c35b`; the
working tree clean apart from an untracked `.claude/`. `python -m tools.pagespec` exits 0 —
correctly, since the only `FAIL`s are clauses 8 and 4-`<title>`, both outside `GATED` until S9 and
S10.

Live conformance at that commit, read from the checker rather than from any document:

| clause | failing surfaces |
|---|---|
| 8 separator | `ab-lab`, `car-price-ml`, `car-price-ml/app`, `doc-extract`, `it-job-radar`, `pl-review-sense` (+ `wroclaw`, fetch-only) |
| 4 `<title>` | `auth-log-scan`, `car-price-ml/app`, `mini-traceroute` (+ `wroclaw`) |

Which is S9's seven surfaces and S10's four, exactly as `0008` scopes them.

**One arithmetic correction to the plan.** §3's headline reads *"roughly 13–14 days … +3–3.5"*,
i.e. 16–17.5. The stage rows sum to **14.5–16.5**. The headline predates the re-scopings that
followed it (S7 to nine repositories, S8 to its two halves, S9 to 2–2.5 days) and was never
re-derived — the same shape §4.13's second erratum records about the census, applied to the
schedule. It is the last hand-typed figure in a document whose rule is that figures come from an
instrument.

## 3. Architecture

### 3.1 The checker answers a question about the published page by reading a file — C1

***Closed 2026-09-07, both halves*** — `#90`. Under `--fetch` the clauses are answered from
the served bytes and a `served` finding compares them with the committed file; measured on
eleven of eleven, in CI and locally, with the digests equal across both platforms. What is
**not** closed is the gitlink half's other consequence: the `surfaces` job still reads the
eleven at the pinned pointer, and only the scheduled `live` job fetches. The section below
is left in the present tense because it is the diagnosis this closure was built from.

Two gaps compose. `sources.py` reads `root / repo / path`, and CI checks submodules out at the
**superproject's pinned gitlink** rather than at each repository's `main`: a page can regress in a
public repository and stay invisible to the index gate until somebody commits a pointer bump.
And nothing compares the committed bytes to the served bytes — `sources.py:7` states the premise
as fact, and `0008` §6 carries it as a *manual* row.

Together they reproduce, structurally and for eleven of twelve surfaces, the founding failure
`0007` §2 names: *answering a question about the rendered page from something that is not the
rendered page*. The system's own instrument is subject to the defect the system was built to end.

The whole of the recognition is a comment in a submodule —
`apply-scout/tests/test_docs_page.py:827`: *"the index checker … only sees this page after somebody
bumps a submodule pointer. Everything below can regress inside this repository, on a green build,
with nothing to notice it until then."* It appears in neither `ADR-0004` nor `0008`.

**Two consequences that look like independent defects until the cause is visible:**

- **The palette duplication in `apply-scout` is not redundancy, it is compensation.** Fix the
  property and it becomes optional; leave the property and it is *correct*. Only that one
  repository carries it, so the second carrier's coverage is uneven and nothing states which repo
  covers what.
- **`mini-traceroute` is uncovered twice over.** It holds no `pyproject.toml` and zero `.py` files,
  so it can host no local page test — and it is also where the pointer lag has no backstop. It is
  the one surface the index checker guards alone.

*Also: the daily `schedule` runs `surfaces` against the same pinned bytes it read yesterday. For
the eleven committed surfaces the scheduled run adds nothing; only `live` earns its cron.*

### 3.2 Nothing enumerates the clauses, and the same defect has landed three times — W1

The spec is prose. The checker, the per-repository tests and the plan are three independent hand
translations of it, with no addressable link from a sentence to its carrier. The record already
contains three instances of one failure mode, at three different layers:

| where | what happened | recorded |
|---|---|---|
| the checker | clause 1's third sentence had **no check at all** — *"composed from the frozen table's columns rather than from the normative clauses' sentences"* | `0008` §3.7 |
| the docstring and the spec | both said the role-rule guard covered four exception shapes; the code had three | §3.10 |
| the plan | clauses 8 and 4-`<title>` had **no stage** — *"composed from §9's rows rather than from §5's clauses"* | §4.11 |

§3.7 says explicitly this *"is a thing to check for the whole of S6 and S7, not a one-off"*, and
§4.11 then records it being checked for the program and not for the plan. **Three occurrences of
one shape is a missing artifact, not a discipline problem.** Nothing enumerates the obligations, so
nothing can be checked against them.

### 3.3 The rest, by what it costs

| # | finding | when it bites |
|---|---|---|
| **W2** | `clause_3_tables` short-circuits per-table analysis on a **sheet-global** flag (`clauses.py:538`): one bare `table { overflow-x: auto }` anywhere — including inside a flattened `@media` — makes `unwrapped` zero for every table on the page | Not live. It fires the moment `wroclaw`'s scroller gets a house name, which `0008` §5 carries as wanted-but-unscheduled: the page flips `UNDECIDED → PASS` and per-table analysis goes silent on the one surface with no committed HTML |
| **W3** | `_VAR_FALLBACK` accepts only a hex literal, so `var(--radius, 10px)` on an undeclared token reports *"names a token that resolves to nothing"* — a confident wrong sentence about CSS the browser paints. The key `1 usage refs` matches `"1 "` in `GATED`, so it **refuses the build** | **Found independently by two passes.** S7 and S9 both rewrite stylesheets; one defensive fallback is a red CI |
| **W4** | S9's write-site census needs a **source-tree** axis. The analogy licensing it (*"the way clause 1's census and the role census went"*) is false: those compute from the pages' CSS, which `sources` already loads. `sources.py:1` defines the module as *"the I/O boundary, and nothing else"* | S9's first commit, as currently scoped |
| **N1** | Registry drift: twelve surfaces in `sources.SURFACES`, eleven repositories **twice** in `pagespec.yml`, twelve in `.gitmodules`, and `12`/`11` as literals in `test_sources.py:148`. Nothing ties any to any | A thirteenth project needs four edits; the one that fails silently is the workflow — the page would be checked when the workflow ran, and the workflow would not run when that pointer moved |
| **N3** | `ADR-0004` §4 says `measure_page.py` is *"invoked"* for the geometry column. The file exists and is tracked in `wroclaw-air-insights/.claude/skills/`, and is **invoked from nowhere** — it appears in two comments and no call | The ADR is a document the repository refutes, in the record whose signature finding is that shape |
| **N4** | `colour.resolve()` and `colour.composite()` are built, tested, and **called only by their own tests**. Contrast is the one class `0008` §3.1 says a reader can be *harmed* by, and the only class with no clause | Every contrast repair so far — S1, the §3.2 revert, S7's sweep — was hand-measured |
| **N2** | The gate encodes *pinned wins* where `0007` §5's governing rule says *measured wins*. A page that does what the rule licenses is refused until §5 is amended | May well be intended; no artifact says so, and `__main__`'s census docstring reasons the other way for the role census |

## 4. The checker's code

Every item below was reproduced by running the code.

### 4.1 Clause 8's regex has three defects, and the obvious fix has a fourth

| text | reported |
|---|---|
| `8 612.50 PLN` | `n/a — no grouped figure on the page` |
| `1 234 567.89` | `space 1` — the `567` group is dropped |
| `HTTP 200 404 500` | `FAIL space 2` |

**S9 brings this clause into `GATED`**, so the gate would not protect a decimal-tailed figure, and
`car-price-ml` prints PLN amounts throughout: rewriting `8 612` as `8 612.50` moves a surface from
`FAIL` to `n/a` and past the gate while still using a plain space.

**The prescription offered with the finding would have reddened a clear surface.** Relaxing the
trailing bound to `(?![\d:])` and allowing a decimal tail was measured against the corpus:

```
auth-log-scan   current=0  proposed=4   '40 198.51.100.77', '24 203.0.113.7'
```

Four false `FAIL`s out of IP addresses, on a page that passes clause 8 today — which is precisely
what the bound exists to prevent, and what `_GROUPED`'s comment says it was written for.

**A variant that keeps the bound and applies it after the tail** fixes both the false negative and
the undercount, still rejects the dotted quad, and produces **zero delta across all eleven
committed surfaces** — so it can land before S9 without moving a census figure:

```python
r"(?<![\d.:])(\d{1,3})((?:[   ,](?:\d{3}))+)(?:\.\d+)?(?![\d.:])"
#                        the class stays spelled out, as `_GROUPED` already spells it:
#                        `\s` matches the newline `rendered_text` puts between adjacent
#                        nodes, and would weld two numbers into one grouped figure.
```

The `HTTP 200 404 500` false positive survives both forms and needs its own decision — requiring
separator consistency within one figure is the candidate.

### 4.2 The rest

| finding | reproduction |
|---|---|
| **`4 title` compares against the hyphenated directory string** (`clauses.py:568`, `startswith`) | `Auth Log Scan — what a brute-force attack looks like` reports **PASS**. All three current failures clear by replacing hyphens with spaces: same defect, green gate. Settle *name* or *directory string* before S10 makes it a ratchet |
| **Clause 7 reads raw CSS**, so a commented-out `@import` gates | `/* never do this: @import url(https://fonts.googleapis.com/x); */` → `FAIL`, and `"7 "` is in `GATED`. Inconsistent with `clause_1_literals`, which goes through `rules()` and strips comments |
| **`--report-only` returns 0 above all three gate blocks** (`__main__.py:208`) | The mode whose natural use is *"read the would-gate list and work it down" prints the table and nothing else. Its docstring promises *"print and exit zero whatever it finds"* and it prints strictly less. Also leaves the three printing blocks with no determinism coverage |
| **`sources.py` treats an href as a bare path** | `styles.css?v=2` → unreadable → gates, on a file that exists. The `--fetch` branch handles it through `urljoin`; only the local branch does not |
| **`_LENGTH` matches `px` only** (`clauses.py:71`) | A rail at `0.2rem` reports `1 usage roles FAIL`, and that key gates. S6–S8 rewrite nine pages |
| **`sources.py:141`** files an unreadable stylesheet under a bare `except Exception` and discards the cause, on a path that now gates daily | Already carried as a residual in `0008` §5; S9 makes it reachable |

## 5. The guards

Thirty mutations were run against `tools/pagespec`; **twenty-two reddened the guard that names
them.** The suite is genuinely strong, and the holes are concentrated in the gate's *configuration*
and the *fetch path*, not in the clauses.

### 5.1 `GATED` is guarded in one direction only

`test_the_ratchet_holds_no_clause_the_committed_surfaces_report_failing` asserts that no gated
clause currently fails. Removing a prefix cannot violate that — fewer gated keys is trivially still
zero failures. So the suite's whole protection of the ratchet's *content* is **"`GATED` must be
non-empty"**. Measured:

| mutation | result |
|---|---|
| add `"8 "` | **3 red** — the guard works upward |
| drop any single one of the eight prefixes | **green, all eight** |
| `GATED = ("1 ",)` — seven clauses un-gated at once | **green** (311 tests) |
| `GATED = ()` | 1 red — the only floor |

**This matters now.** S9 and S10 both edit this tuple. A hand edit adding `"8 "` while dropping
`"5 "` ships green and clause 5 silently stops gating twelve surfaces — the displacement shape
§3.9, §3.10, §4.9 and §4.12 record four times.

*The guard this wants:* pin `GATED` against a derived floor — every finding key reporting zero
`FAIL` across the surfaces read **must** be in it. Then the tuple is the consequence of the sweep
in both directions rather than a claim checked in one.

### 5.2 The rest

| finding | reproduction |
|---|---|
| **The `live` job's success path is unguarded end to end.** `main` is called with `--fetch` once, and only on the failure branch | `allow_fetch=args.fetch → False` makes `--fetch` a **complete no-op** and the suite stays green: the fetch-only surface falls to `"fetch failed: no detail"`, which still satisfies the assertion. `live` is the only thing gating `wroclaw`, and `wroclaw` is where S10's fix is observable |
| **An assertion weaker than its test's name.** `test_a_page_failing_a_gated_clause_makes_the_checker_refuse` asserts `"1 tokens" in out` | That string is the ordinary per-surface detail line for any `FAIL`. Under `GATED = ("6 ",)`, where `1 tokens` is not gated at all, the test still passes. It proves *some* clause gated |
| **Clause 8's `n/a` is an unrecorded gate escape** | `1234` → `n/a`. Once gated, **deleting the grouping is cheaper than migrating to `U+202F`**. `1 234` (thin space) also reads `n/a`, and that is the codepoint a hand edit reaches for during a narrow-space migration. Defensible under the spec; it needs to be a *stated* reading with a test before S9 gates it |
| **The "ratchet is a ratchet" test dissolves at S10.** `test_a_page_failing_only_an_ungated_clause_still_passes` is built from exactly the two clauses about to be gated | After S9+S10, `GATED` covers every key that can be `FAIL`, `_gated` becomes equivalent to `status == FAIL`, and the test has no construction left. Rebuild it on a monkeypatched `GATED` **before** S9 |
| **Clause 4 implements only the negative half of the `<title>` rule** | `<title>Home</title>` and `<title>Untitled document</title>` both **pass** beside an unrelated `h1`. `og:title` content is read by nothing — clause 5 requires the tag to exist. This is §4.9's `og:description` finding one clause over |
| **The `<title>` first-wins rule is unguarded; its `h1` twin is pinned** | Dropping `and not self.title` from `render.py:93` is green; the same mutation on the `h1` branch reddens a named test. `test_render.py:119` names the missing case in its own docstring |

## 6. The workflow, which is this project's agent configuration

Reviewed against the `agent-engineering-guide` skill. **The workflow is not incidental to this
system — it is how the system is built**, so it is reviewed with the same instrument as the code.

### 6.1 What was already right, and is worth not losing

- **It is a textbook long-running-agent loop.** Git and a committed document are the memory; the
  ledger carries decisions and blockers, the briefs carry the handoff, commits are the checkpoints.
  It works: **286** merged pull requests across the thirteen repositories as of this date, eight of
  fourteen stages closed, and discipline visibly held for weeks.
- **The verification loop is external, not self-review.** `code-reviewer` as a separate role,
  mutation as the proof, and *a guard that passes on a mutation* as a named defect class. The
  literature puts external verification at a 2–3× quality effect; here it is implemented better
  than in most teams, and this file exists because of it.
- **The twelve `CLAUDE.md` are factual maps, not directive stacks.** Zero occurrences of
  `NEVER`/`MUST`/`ALWAYS`/`CRITICAL` across all twelve — the preferred shape, because a fact
  internalises as understanding of the system while a directive sits on top and needs maintenance.

### 6.2 The gaps, in order of leverage

1. **No `CLAUDE.md` at the index root** — the repository where sessions start. The hardest-won
   operating rules lived in §6 of a 1 453-line document nothing loads on its own. *The evidence
   that this cost something:* two passes on 2026-09-07 reached the same false conclusion
   independently, and §6 held the row that would have prevented it. **Closed by `#81`.**
2. **No `SessionStart` hook.** §6 is a table of assumptions *"to verify before each stage, not
   once"*, and four of its rows are one shell command each. Harness beats prompt: a hook turns a
   documented assumption into an enforced fact. **Closed by `#81`** — `tools/entry_state.py` at two
   depths, the cheap one wired to session start.
3. **`.claude/` was untracked**, so the loop's memory lived on one machine, in a project whose
   thesis is *a plan that is not a document is not a plan*. **Half-closed by `#81`**: the
   configuration is tracked, the briefs deliberately are not — they are a per-machine handoff, and
   the decisions that outlive a session belong here.
4. **`autoMode.environment` in the user's global settings carries another project's facts**,
   including a contradictory trust-boundary line (*"repo has no git remotes at all — treat as
   local-only, not yet published"*) beside the correct entry for this repository. An agent
   operating here reads two incompatible descriptions of the world it acts in. **Open**, and it is
   a factual correction rather than a new rule.
5. **`0008` is now the shape `0007` was split for.** 1 453 lines mixing the three lifetimes
   `ADR-0004` §5 separates, with thirteen errata subsections and a section numbering that runs
   3.5 → 3.3 → 3.4 → 3.6 → 3.7 → 3.9 → 3.10 → 3.8. **The taxonomy of defect shapes is the most
   reusable asset this repository has produced and it is unfindable** — three sentences state the
   whole method and they sit near lines 435, 650 and 1 200 of one file.

## 7. What to do, and in what order

Ordered by what unblocks what. Nothing here is scheduled; a row enters `0008` when it is taken.

| # | change | closes | size | state |
|---|---|---|---|---|
| 1 | Session-start hook + a root `CLAUDE.md` | §6.2 rows 1–3 | S | **done — `#81`, `743cb34`** |
| 2 | The three code defects before S9 touches five stylesheets: `_VAR_FALLBACK`, `clause_3_tables` per table, `sources.py:141`'s cause | W2, W3, N5 | S | **done — `#83`**, and widened: see the note below |
| 3 | A **`GATED` floor guard** — every key reporting zero `FAIL` must be in the tuple — plus the assertion repair in §5.2 row 2 and the rebuild of the ratchet test before it becomes unsatisfiable | §5.1 | S | **done — `#83`** |
| 4 | Clause 8's regex in the bound-preserving form (§4.1), and a stated decision on `n/a` and `U+2009` | §4.1, §5.2 | S | **done — `#83`**; the `n/a` reading is stated and left to S9 as a spec question |
| 5 | A **clause registry** — `CLAUSES` keyed by clause-sentence id, each carrying `carried_by: index \| repo-test \| review \| none`, with a `core`-job test that every entry has a check or an explicit reason | W1, and gives clause 9 and the geometry half an honest home | S | **done — `#85`, `35ae5a9`**, and it found two more occurrences on its first walk: clause 7's first sentence and clause 3's `data-scroll` escape. `ADR-0005` is the decision; §12. **Both of those are carried as of 2026-09-09** — clause 7 now reads `font-family` through the palette, and clause 3 honours the escape it had been overruling. They were open for two days with the checker reporting on them the whole time, which is the cost of a walk that finds a gap and enters it nowhere schedulable |
| 6 | Re-scope S9's first commit: no permanent source census; reconcile against the checker's existing per-surface inventory and let the ratchet carry recurrence | W4 | *a saving* | **done — taken 2026-09-08**, over an architecture pass recommending a probed `WRITE_SITES` registry in `sources.py`. That pass's own measurement is the best argument for this row: a discovery sweep is ~80 % false positive, and a declared registry records the hand count rather than replacing it. The census counts the **figures** the write sites reach, which the checker already holds. `0008` §4.15 |
| 7 | S9 and S10, with `wroclaw/tests/test_report.py:1524` widened in the same commit that moves the separator | the two failing clauses | 2.5–3 d | **done — 2026-09-08, in one ratchet cycle rather than two.** Eight sibling pull requests, then one index commit bumping seven pointers and admitting both keys. The row's `:1524` is right and incomplete: `:1530`'s strip is equally load-bearing, and the guard's fixture carries no four-digit figure, so widening the pattern alone would have left the branch unreached. `0008` §4.17 |
| 8 | The scheduled `live` job hashes all twelve fetched surfaces against their committed files, reporting a mismatch under its own finding key | **C1**, both halves | S | **done — `#90`**. Eleven, not twelve: `wroclaw` has no committed file. And it grew a half the row did not name — a hash says the two *disagree*, not which clause the public page now fails, so the clauses are answered from the served bytes too |
| 9 | Split `0008`: ledger, **a failure-taxonomy document**, measurements to the report | §6.2 row 5 | ~~S~~ **M**, and it needs a design decision first | open — **scope re-derived 2026-09-10 at `e3a7f31`, before the stage rather than during it, which is §4.7's precedent for the sixth time. The row is neither the size nor the urgency it carries.** *Not `S`.* §4 is **2 597 of 3 207 lines**, and **71 citations of `0008` §4.x live in 18 tracked files outside `0008`**, measured at `e3a7f31`: `tools/pagespec/__main__.py` 9, `tests/test_report.py` 9, `tests/test_clauses.py` 8, `tools/spec.py` 7, this file 7, `ADR-0008` 7, `tools/pagespec/clauses.py` 6, `ADR-0007` 5, `0007` 2, `CLAUDE.md` 2, `.github/workflows/pagespec.yml` 2, and seven files with one apiece — production code, the CI workflow and the contributor map among them. **The submodules are not reached**, which is the one fact keeping this an index-only stage: they cite `0008` §3.6 and nothing else (`apply-scout` 3, `auth-log-scan` 2), and §3 stays in the ledger. *The first version of this figure read 81 across 22 files, ten of them in four session briefs, and argued that those ten must not move. They are not in the repository at all: `.claude/sessions/` is gitignored at `.gitignore:25` and `git ls-files` returns none of them, so they are one machine's local state — nothing to re-point and nothing a clone has. The figure was taken from the filesystem where every other figure in this row comes from git.* **And 71 is a floor rather than the scope.** It matches on the literal string `0008`, and this document is also cited **bare**: `render.py:98`, `CLAUDE.md:158`, `ADR-0005:26`, and `ADR-0006:9` twice — five sites carrying no document number, which a mechanical re-point cannot find by grepping `0008` at all. **69 bare `§4.x` sit in 19 tracked files** whose line names no document; most are a document citing itself, and telling those apart from `0008`'s takes a read per site. That is the strongest argument in this row for `@architect`, and it is that the mechanical half is not mechanical. Same shape as row 13b, which this table also sized `S` and which §7's own note admits was *"reasoned rather than run"* — the second time this column has been wrong the same way, which is what makes it a pattern rather than an estimate. *And the reason to take it next has expired.* The row argues from **2 197 → 2 470**, today **3 207**, and the file grew because **each stage added a §4.x section**. `0008` now has no open stage: S8c is the only row not `closed` and it is a refusal on measurement, not scheduled work. The growth stopped when S14b closed, so the waiting stopped costing at the same moment — the argument for urgency expired on the day it was loudest. *What is left is a design decision and not a move.* The row names three destinations, and a §4.x section mixes all three inside one paragraph: *"What closing SX measured"* carries status, a recurring failure class and figures at once. Re-pointing 81 citations is mechanical only if the section numbers survive, and they cannot survive a partition that reads for meaning. `@architect` before `@Plan` |
| 10 | **Sx** — 11 `pyproject.toml`, 70 `Author:` fields | dead weight | 0.5 d | **done** — eleven sibling pull requests plus `b416c83` and `d550066`. Both figures now read **0**. `d550066` is green on `main`; `b416c83` is `docs/**` only, which the paths filter excludes, so it has no run. `0008` §4.14 records what the stage measured, including a deprecation date the record did not have |
| 11 | Bring the **profile README** into the system — ~~at minimum a `Surface` read by `--fetch` in `live`~~, plus the quotation rule | the asymmetry in §9 | **M, not S** | open, and **re-scoped by measurement 2026-09-08** — §14 |
| 12 | **Contrast at the usage site** — a clause using the existing `colour.resolve()`/`composite()`, `UNDECIDED` for `color-mix`, `opacity < 1` and SVG paint order, threshold per usage site | N4, `0007` §7's largest gap | M | **closed at S14b, 2026-09-10** — `contrast text` gated, `contrast marks` report-only, `c1.s6b` in `0007` §5 clause 1. What is still open is not this row. **`Ground.guaranteed` was closed 2026-09-10 as `ADR-0008` D8** — and the answer was that it is not a verdict input at all: the guaranteed ground is never the binding one, while both failures with a history are read on a geometric ground. What a verdict excludes instead is a ground that is another instance of the same mark, which took the marks census **153 → 88** and left `contrast text` byte-identical. The pages' half stands, and the census now partitions it: 48 gridline strokes D5 admits wrongly, 9 heatmap cells D5's untaken escape would lift, 14 mark-against-a-different-mark, 17 remainder. `0008` §4.28. *Was: open, and* **next after row 13b** — it is the only open row where a published page can harm a reader, which is §3.1's promotion rule. ~~Ships report-only with a `NOT_A_CLAUSE` entry stating that as a decision~~ — **that route was refused by the guard beside it**, found 2026-09-08 by the architecture pass on this row: the floor's exemption check admits no key the corpus reports `PASS` or `FAIL`, and a contrast clause passes on a conforming page. It ships as `Ratchet(prefix, REPORT_ONLY_STATE, reason)` in `__main__.GATE`, which is what row 13b built and why that row was due first. **Row 13b is now closed.** The row was then *opened by measurement* rather than by building: `0008` S12 took the finding and the instrument's own blind spot, and left the clause itself as **S13**. Three claims did not survive the measurement — `--accent-soft` on `--surface` is not live anywhere (35 `<svg>`, none inside a `.card`), a rule-keyed clause is 59 findings of which ~0 are real, and the one live SC 1.4.3 failure was in a **presentation attribute** neither carrier read. `0008` §4.19. **Taken 2026-09-09 as two stages** — `0008` S13 (the census) and S14 (the verdicts), `ADR-0008`. And **this row's promotion argument has expired**: the harm it names was closed by S12 before S13 was taken, so §3.1's rule no longer reaches it and the order against row 9 is open again. `0008` §4.23 |
| 13b | **Close the eleven/twelve asymmetry in the instrument** — parametrise `_sweep()`'s fetch mode in `tests/test_published_surfaces.py`, make the expected surface count follow that mode, and give the scheduled `live` job a `pytest -m submodules` step | the trap `CLAUDE.md` spends a paragraph on | S | **done — 2026-09-08**, `0008` S11 and `ADR-0006`; entered as *designed and deliberately not taken during S9/S10*, because §13.6 forbids repairing a guard in the window that guard is carrying a stage. Its feasibility is reasoned rather than run: `live` already checks out submodules and the fetch-refusal guard in `tests/test_report.py:484` permits it there, but the mode-dependent count needs its own mutation proof and a wire failure must not be able to redden a floor guard. **Take it before row 12, not during** — row 12's key is the next admission to `GATED`, and this is the procedure that admission needs. **done — 2026-09-08, `0008` S11 and `ADR-0006`.** The row as written does not land, and the reason is worth more than the row: **three guards formed a closed contradiction.** A fetching floor sees `served` clean and demands it gated; `test_report` refuses it in `GATED`; `test_spec` refuses it in `NOT_A_CLAUSE`, correctly, because that set's pin demands a proof the key can never be `FAIL`. No arrangement of the existing vocabulary satisfies all three, so the stage built the third state row 8 said the taxonomy needed. It also found **four** ways a fetching corpus is incomplete where the row implies one, and the fourth — the mode never reaching `sources.load` — degrades the guard to a *skip*, which is a pass. Size **M**, not the S the row carries; §7's own note that its feasibility was reasoned rather than run is why |
| 13 | Registry-drift test (N1) · resolve N3 (implement the geometry half or amend `ADR-0004` §4 to say it is deferred and unowned) · clean `autoMode.environment` | N1, N3, §6.2 row 4 | S | **N1 and N3 done — 2026-09-08.** N1: the workflow's two `paths:` filters are tied to `sources.SURFACES` by a `core` test, which is the half §12.4 leaves and the one this row correctly calls the silent failure. N3: deferred and unowned, in `ADR-0004` §4 and `tools/spec.py` `c3.s2` — **its evidence did not reproduce**, §8 row 7. `autoMode.environment` is **open** and is the user's global settings rather than this repository |

**Rows 2, 3 and 4 landed together in `#83`, and row 2 grew.** It was written as three defects
and took five: the two others are §4.2's `sources.py` query string (an href joined verbatim, so
`styles.css?v=2` reported a file that exists as unreadable — a *false* gate, which is worse than
a missing one) and §4.2's `_LENGTH` and clause-7 pair, which the review escalated on the grounds
that the argument for taking the first three applies to them verbatim: all five are invisible
today and all five become reachable when S9 rewrites five stylesheets. Two things that turned up
while closing them are recorded in §11.

**What not to change:** `UNDECIDED` as a status that never gates; fail-closed on an unread surface;
the `core`/`surfaces` job split; and `ADR-0004`'s K-c decision against vendoring. Each is
load-bearing and each has its evidence on the record.

## 8. What this review got wrong

Recorded because a review that only reports other people's errors is not being held to its own
standard, and three of these were this session's.

1. **"Eleven of the twelve submodules carry a page test."** Three sweeps produced three answers.
   The first draft said ten, it was "corrected" to eleven, and the reviewer showed ten was right for
   the words used — `token-budget` has no `docs/` at all. **The number is not typed anywhere now**:
   `CLAUDE.md` carries only what is settled, which is that `mini-traceroute` holds no
   `pyproject.toml` and zero `.py` files. §4.13's refusal to type a fourth census, applied.
2. **"The twelve submodules each carry a `.codegraph/`."** Ten do. `doc-extract` and `pl-jobs-lora`
   carry neither the index nor a mention of it — and that is the section telling a session which
   tool to reach for first.
3. **A guard proved red on one machine's incidental state.** `#81`'s first version asserted that a
   mutation reddened a guard reading real `git submodule status` output. It does — where the
   submodules are checked out and the flags are spaces. In a fresh clone every flag is `-`,
   `.strip()` removes nothing from a `-`, and the guard passed green over the defect **in exactly
   the `core` job the same paragraph cited**. The eighth appearance of the class §3.9 names, and
   the first one this record can attribute to itself.
4. **A prescription that would have reddened a clear surface** — §4.1's proposed clause-8 fix,
   four false `FAIL`s on `auth-log-scan` from IP addresses. The diagnosis was right and the
   remedy was not, which is why remedies are measured against the corpus and not only reasoned about.
5. **The architecture pass ran without a shell** and marked the index's visibility as unverified
   rather than asserting it. That was the correct call, and it resolved to the answer with
   consequences — §9.
6. **A naive `git grep -c "Author: P0w3r223"` returns 71 across the portfolio, not 70.** The
   seventy-first is `0008` §2.1 quoting the pattern it is counting. The ledger's figure is right;
   an instrument for Sx must match the header form `^Author: `, not the substring.
7. **N3's evidence is wrong and its conclusion is right — found closing it, 2026-09-08.** The row
   reads *"it appears in two comments and no call"*. `measure_page.py` has calls:
   `wroclaw-air-insights/tests/test_verify_published_page.py` loads it by path, exercises its pure
   layer everywhere, and at `:271-280` calls `measure_page.measure()` against a **real Chromium**.
   A sweep asking *is this file called* answers yes.

   **What is uncarried is narrower than the row said, and worse.** Every call points the instrument
   at the skill's **own fixtures**; nothing has ever pointed it at a published surface. So the
   sentence in `ADR-0004` §4 is false for a reason the row did not reach — not *"the tool is dead"*
   but *"the tool is alive, tested, and aimed somewhere else"*. **The two readings prescribe
   different work**: the row's implies wiring up a call, and the true one implies aiming a
   browser-dependent instrument at twelve public URLs, which is the K-c decision reopened. Resolved
   as **deferred and unowned** in `ADR-0004` §4 and in `tools/spec.py`'s `c3.s2`.

   *This is the seventh entry in this section and the third of its exact shape* — row 1's page-test
   census, row 6's `Author:` substring, and now this. All three are sweeps whose **query** was
   narrower than the **claim** built on the answer, and all three were found by someone acting on
   the claim rather than by re-reading it. A sweep is worth what its query is worth, and the query
   is the part that does not appear in the finding.

## 9. The asymmetry worth naming

`current_projects` is **private** (`gh repo view`, 2026-09-07); all twelve submodules are public.
The public landing surface is the profile README at `P0w3r223/P0w3r223` — public, last changed
2026-09-03 — and it is **carried by nothing**: not a clause, not a test, not a row of `SURFACES`,
and not a submodule. `0007` §5.0's quotation rule was applied to `docs/index.html` in S4 and to
`README.md` in §4.10, where ten of twelve carried a figure no artifact printed. It has never been
applied to the one surface a recruiter actually reaches, and the stage that would touch it (S8a,
carrying H3) is the one stage blocked.

**Twelve of thirteen surfaces have an instrument, a gate and a ratchet. The thirteenth — the one
the audience sees — has prose and memory.**

The same fact reads the other way round for the code: `tools/pagespec` is the most sophisticated
single artifact in the portfolio and it is the one thing the portfolio's audience cannot open. That
is a product decision with a real cost — it becomes a versioned dependency, and part of `ADR-0004`
K-a's decay argument returns — so it belongs in its own ADR rather than folded into a cleanup.

## 10. What this review did not check

Stated so a later reader does not infer coverage that does not exist, which is `0008` §6's own
discipline turned on this file.

- **The live pages.** Nothing here fetched a published URL; the conformance table in §2 is the
  checker over committed files plus `wroclaw` unread.
- **Byte-identity of served against committed.** §6 row 3, still manual, and §7 row 8 is the
  proposal to close it.
- **The four About descriptions**, which are an account surface and not a file.
- **The submodules' own suites.** Three passes read the index repository; the submodules were read
  only where they carry part of the spec.
- **Anything about `pl-jobs-lora`'s or `doc-extract`'s open milestones.** They are portfolio work,
  not page-spec work, and `doc-extract` M7's one genuinely open item — a real held-out set on
  documents nobody generated — is recorded in its own repository.

## 11. Two things `#83` turned up, neither of them about `#83`

**The twelfth surface's `3 tables` detail moves, and its status does not.** Clause 3 now
classifies each table rather than the stylesheet, so `wroclaw-air-insights` reads
*4 table(s), scroller(s): the table itself; 4 rest on the bare `table` rule, whose media
condition is not read* where it read *no wrapper class, and the media condition is not read*.
`UNDECIDED` both ways, no cell and no gate moves — but "the conformance table is byte-identical"
is true of the eleven committed surfaces and not of the twelfth, and the only place that text is
printed is the scheduled `live` job. Stated because a reader meeting the new line there would
otherwise have to work out whether something had changed.

***Settled and implemented 2026-09-07 — `#86`, `2c53f04`. The paragraph below is the question as it stood; `named_after_the_directory` no longer exists and the answer is four surfaces, computed rather than asserted.***

**`wroclaw`'s `<title>` passes clause 4 while leading with the project's name.** Fetched
2026-09-07: `Wrocław Air Insights — live PM2.5 forecast` reports `ok`, because
`named_after_the_directory` is `startswith(repo.lower())` and `wrocław air insights` is not a
prefix of `wroclaw-air-insights` — a different letter and no hyphens. That is §4.2's `4 title`
weakness with a live instance rather than a constructed one, and it bears directly on S10:
**the stage's scope is four surfaces or three depending on whether the rule compares the
repository's *name* or its *directory string*.** `0008` S10's row says four. Settle the reading
before the stage, because after it the answer is a ratchet.

**A sequencing constraint S9 inherits, and it is the floor guard's doing.** The guard sweeps
the eleven committed surfaces; the gate covers twelve. So when S9 cleans clause 8 on the
committed pages while `wroclaw-air-insights` still prints a comma, the guard reddens and
demands the widening — and widening reddens the scheduled `live` job instead, because the
`surfaces` job never fetches. There is no green path between those two states, and that is
correct rather than a defect: **the stage owns both halves, so the index pointer bump that
cleans the eleven must not land before the twelfth is done.** The guard's failure message
names all three outcomes rather than the one it used to imply. Recorded here because it is a
constraint on *how S9 is landed*, which is `0008`'s business and not this file's.

*Two qualifications, because the first telling of this was wider than the fact.* The deadlock
is the invariant's consequence rather than an accident — `GATED` is one tuple read by two jobs
that see different corpora, so **any** floor derived from eleven surfaces will demand something
the twelve-surface gate cannot honour. But the commit calling it *"resolved, in the only
direction it can be"* was overstated: at least one other direction exists and was never weighed
— leave only the ceiling assertion in the `surfaces` job and run the floor over `--fetch` in
`live`. That trades a push-time guard for a scheduled one, which is a real cost and the reason
the workflow keeps the wire off the push path; it is not, however, no direction. And
`pagespec.yml`'s `live` job is `workflow_dispatch`able, so the twelfth surface can be **read on
a chosen ref before a merge** rather than trusted — the one lever that makes the sequencing
constraint verifiable instead of a promise, and neither the guard's message nor this paragraph
named it. Both do now.

**One residual is closed and a second of the same shape survives, named rather than implied.**
`#83` made `unreadable` a `(href, why)` pair and `sources.THIRD_PARTY` a constant compared
rather than searched, which closes §5's *"the marker is prose built in one module and matched
in two others"* for the stylesheet case — mutation-proven: changing the marker's text is now a
no-op. The same shape survives at `__main__`'s `"needs --fetch"`, built as prose in one place
and compared in another; it is guarded (the end-to-end test asserts both the exit code and the
string), so it is a smaller instance and not the one §5 describes, but the claim *"the residual
is closed"* is true of the stylesheet marker only.

## 12. What the passes of 2026-09-07 got wrong, including this file

§8's discipline applied to the session that closed §7 rows 5 and 10 and settled §11's first
question. Every figure below was recomputed rather than re-read.

### 12.1 In this document

1. **§2's conformance table lists `wroclaw` under the clause-4 failures, and the instrument read
   `ok`.** §11 of this same file says so nine sections later. The cell was `0008`'s *scope* figure
   printed in a column labelled as the checker's reading — the substitution `ADR-0004` §5 exists to
   prevent, in the document that quotes that rule. The outcome has since moved for a different
   reason (the reading was settled and `wroclaw` now fails), which is exactly why the method error
   is worth recording separately from the number.
2. **§8 row 6's naive count was 72 on the day it was written, not 71.** The row diagnosed the
   off-by-one correctly and, *by quoting the pattern it was counting*, added the second instance
   itself. Since Sx the header form is **0** portfolio-wide. The tracked naive count was **2** —
   §8 row 6 and `0008` §2.1, both records of a measurement rather than fields.

   ***And this commit made it 3.*** The Sx status cell written in the same change quoted the
   pattern while reporting it as zero, which is the third occurrence of the shape this very
   item was written to diagnose — the first in `0008` §2.1, the second in §8 row 6 correcting
   the first, the third here correcting the second. The cell is rewritten to name the thing
   instead of spelling it, which is what this item does and is why this item did not add a
   fourth. **The count is the wrong instrument and that is the finding**: a figure whose
   measurement is a substring of the document reporting it cannot be stated in that document
   without moving. The header form does not have this property, which is why it is the one
   the ledger tracks.

### 12.2 In the architecture passes commissioned this session

Both were substantively right and both carried a figure that did not reproduce, which is the
reason `CLAUDE.md` says to reproduce before building on one.

| claim | measured |
|---|---|
| un-normalised, a served-versus-committed hash *"would report all eleven as mismatched"* on this machine | **five of eleven** — only five working-tree files carry CRLF |
| `pagespec.yml` mentions `--fetch` twice, so a naive `count == 1` ships broken | **three times**. The conclusion is right and stronger than stated |
| a non-positional clause-4 reading fails 10 of 12 surfaces | **11 of 12** — the first count compared without folding `ł`, so it could not see `wroclaw` |
| eight conforming titles are `<claim> — <repo>` | **seven of the eight**; `apply-scout` carries the name nowhere |

The last two were this session's own, propagated from `main` into two new sites before the review
caught them.

### 12.3 In the work, found by the reviews that blocked it

Three guards shipped green over the defect they name, and all three were in stages whose subject
is that class:

1. **The registry's lower-bound guard could not fail.** It asserted a quote's occurrence count in
   the *whole document* and then restated what `normative_text()` already raises on, so moving the
   bound to the document's title — pulling all of §3 into the normative slice — left the entire
   file passing. It was not among the fourteen mutations run before the stage was proposed.
2. **The subsumption claim in clause 4's fold was false as written.** `_fold` subsumes the raw
   comparison *with the word boundary applied*, which is what the exhaustive check compared; it does
   not subsume the bare `startswith` this replaced on `main`. The two moves go in opposite
   directions — the fold relaxes spelling, the boundary restricts the match end. The guard asserting
   the property iterated four rows that all end on a boundary, **the one class where the two cannot
   disagree**, under a docstring claiming to assert the property rather than an example.
3. **The combining-mark strip was reached by nothing.** Every test exercising `_fold` used `ł`, and
   `_UNDECOMPOSED` handles `ł` before NFKD is consulted — so deleting the strip left the whole suite
   green, one line below the trap the branch was written to close.

**And one was caught before review, which is new.** The raw directory comparison was dead code and
it shipped with a test whose name claimed to guard the difference it could not fail on. Every prior
appearance of this class in the record was found by a later pass; this one was found by suspecting
the code while writing it.

### 12.4 Two corrections to §7's own rows

- **Row 13 overstates N1.** It is already half closed:
  `tests/test_entry_state.py::test_the_two_registries_still_name_the_same_repositories` ties
  `.gitmodules` to `sources.SURFACES`. What remains untied is `pagespec.yml`'s two hard-coded
  eleven-repository path lists and `test_sources.py`'s `12`/`11` literals — and the workflow list is
  the one row 13 correctly calls the silent failure.
- **Row 5's `carried_by: index | repo-test | review | none` is single-valued and the decision it
  describes is not.** `ADR-0004`'s K-c is one checker **plus** assertions in the repositories, so
  clause 1's palette and clause 6's back-link are genuinely carried twice. `ADR-0005` ships a tuple.

### 12.5 A false-positive path in the entry state, found by tripping it

A tool that rewrites a file byte-identically leaves `git status` — and therefore
`tools/entry_state.py` — reporting uncommitted changes that `git diff` denies, until a `git add`
refreshes the index. It happened here to a mutation driver restoring its own edits, and the entry
state read `! 2 uncommitted change(s)` over two files identical to `HEAD`.

Recorded rather than fixed. It is the mirror of the stale-`origin/main` false finding §4.12
records: the instrument reports what git reports, and what git reports is not always what changed.

## 13. The four-pass audit of the same evening, and the regression it found

Commissioned after the six stages of 2026-09-07 had merged, on the reasoning that each had been
reviewed alone and none against the others. Four passes over one tree: the architecture, the
whole of `tools/` as code rather than as a diff, the whole suite by mutation, and the day read
as one body of work. Every pass was told that the author of all six stages was the one asking.

**It found a regression introduced that day, by the stage whose subject was closing the finding
it regressed.**

### 13.1 The gate that stopped firing, under a comment saying it fires

`#90` closed §3.1's C1 by making `--fetch` answer the clauses from the served bytes. It also
routed **three different facts through one finding key**, and argued the report-only exemption
for one of them:

| fact | routine? | was it argued? |
|---|---|---|
| the served markup differs from the committed file | **yes** — the normal state between a sibling publishing and the index bumping its pointer | yes, at length |
| the published page answers 4xx | never | no |
| the committed page is absent while the wire answers | never | no |

The second and third inherited the first's exemption. Measured: a deleted `docs/index.html`
refused the run **without** `--fetch` and exited **0** with it; a page answering 404 printed
`FAIL served — the page is gone` and exited **0**. The twelfth surface exits 1 on the same 404,
because it has no file to fall back to — *the same event, opposite verdicts, decided by whether
a fallback happens to exist.*

And `clauses.py` said, of the second condition, *"A gate that stopped firing, and this is where
it fires again."* It did not fire. **Every guard written for these branches asserted a finding's
status and none asserted the run's exit code**, which is how three conditions came to print
`FAIL` and exit 0 under three separate reviews.

### 13.2 A false gate that was reported as removed and had only moved

The same stage split *a stylesheet the network dropped* from *a stylesheet that is missing*, so
that a blip would stop refusing the build. The split was right and the false gate survived it:
`loaded.css` came back empty, clause 1 then reported `no custom properties declared at all` and
clause 3 `no class in the stylesheet scrolls`, and **both of those gate**. The refusal moved
from a key naming the cause to two keys naming a consequence — and the list of dropped sheets
was collected and never printed, so the output stopped mentioning stylesheets at all. A daily
blip refused the build under what reads as a portfolio-wide CSS regression.

*This is `0008` §4.12's displacement pattern, committed by a commit message that cites it.*

### 13.3 What the suite audit found, and what it did not

108 mutations, roughly 95 killed — usually by the test whose docstring names that exact defect.
**The suite is strong**, and the residue is small and specific. The two worth carrying:

- **`test_a_repo_citation_still_points_at_something` was named in a docstring and never
  written.** All three `REPO` carriers could cite a repository, a file and a function that do
  not exist, and `python -m tools.spec` would print the sentence as *carried*. `ADR-0005` §2's
  own failure mode, one carrier-kind to the left, inside the registry built to end it.
- **A guard for the record's most-repeated wrong answer was red on one laptop and green in
  CI.** It asserted against `ROOT`, where `wroclaw`'s gitignored local build exists only on a
  machine that has run the site generator — and the test is unmarked, so it runs in the `core`
  job, which checks out no submodules. It had been that way for its whole life.

Writing the repair for the first of those reproduced the class a third time in one evening: the
new probe used `require_submodule`, which **skips** on a missing path — conflating *the sibling
is not checked out* with *the citation is wrong* — and was green over two of its own three
mutations before that was noticed.

### 13.4 The record's own errata, and one recurrence with a name

- **`#86` appears nowhere in `docs/` or `CLAUDE.md`.** The day's only change to a clause's
  semantics went unrecorded, and four artifacts went on asserting what it replaced — including
  the `GATED` comment block `CLAUDE.md` sends a stage editor to, which typed `4 title` (3)
  where the instrument computes 4, and §11 of this file, which still said *"settle the reading
  before the stage"* three hours after it was settled.
- **`0008` §5's carried list still instructed a reader to do Sx**, which §4.14 in the same
  document records as done.
- **`CLAUDE.md` said narrowing `GATED` "is not caught by anything."** False since `#83` — and
  true of the `core` job, which is not what it said. The most safety-critical instruction in
  the repository, understating the protection that exists.
- **The refuted clause-4 figures survived in a third place: a test docstring.** `0008` §3.10
  records that exact shape — *"corrected in two documents and left standing in a third place, a
  test docstring"* — so §12.3's *"propagated into two new sites"* was itself one short.

### 13.5 What this says about the method

Nine review passes across the day found a real defect in the round of fixes before them, and a
tenth found a defect in the round that closed the ninth's findings. That is not a failing loop:
every one of these was found, and the ones that reached `main` were found within hours. But two
things generalise.

**A stage that argues an exemption must say which facts it covers.** `#90`'s argument was
correct and its scope was assumed. Three facts under one key with one argument is the shape.

**Assert the verdict, not the finding.** Every one of §13.1's defects would have been caught by
one assertion on the exit code, and every guard written for them asserted a status instead. The
same sentence covers §13.2: the guard asserted a helper's return value under a message that
said *"and it must still be printed"*.

*A note on how this audit was run, because it cost something.* Four passes were given the same
working tree, and two of them mutate files to prove guards. The result was that the parent's own
test runs were unreliable for a stretch, and one unexplained working-tree edit had to be traced
before it could be dismissed. Read-only passes can share a tree; mutating ones want their own.

### 13.6 The remediation displaced three times, and that is the finding

The review of §13's own repair blocked with three HIGHs, every one of them the pattern §13.2
had just been written to describe. They are worth listing together, because the shape is the
same three times and it is not carelessness:

| what was fixed | what the fix did instead |
|---|---|
| clause 7 read one and a half of three routes | the widening made the two spellings **compete for one match**, so `src: local("Inter"), url(https://…)` — the canonical line — matched `"Inter"` and never examined the remote URL |
| a false gate on a dropped stylesheet | the incompleteness rule treated *third party, not read* as incomplete, so a page adding Google Fonts had its clause-7 `FAIL` rewritten to `UNDECIDED` — **a false pass on the clause whose entire subject is a third-party font** |
| two collectors that were never lowered | they were lowered for *every* self-closed tag, so `<h1>Fast <br/> answers</h1>` reported `no <h1>` on a page that has one |

**Each repair was correct about the defect and wrong about its boundary.** Clause 7's widening
was right that a second spelling existed and wrong that an alternation reads both. The
incompleteness rule was right that a clause cannot fail on a sheet it never read and wrong that
every entry in `unreadable` is such a sheet. The collector reset was right that the sinks must
come down and wrong about when.

That is a sharper statement than *"fixes displace defects"*, and it is the one worth carrying:
**a repair inherits the blast radius of the thing it repairs, and the review that found the
defect did not measure that radius — it measured the defect.** Every one of these three was
found by asking *what else does this now do*, on inputs a page could plausibly write, and every
one was invisible to the guard written alongside the fix, because that guard was built from the
failing case rather than from the neighbourhood around it.

*Two smaller instances in the same round, recorded because they are the same shape at lower
cost:* one predicate answering two questions widened a page's refusal from `(404, 410)` to any
4xx at the moment it started gating, so a `429` from a runner fetching twelve pages refused the
build; and the guard on the wire never reaching the push path was **a typed literal in disguise
for the third consecutive time** — first two job names, then a substring in an `if:` condition.

### 13.7 Checking the repair instead of waiting for a pass to check it

§13.6 says a repair inherits the blast radius of the thing it repairs. The obvious next move is
to measure that radius yourself, before the next review does. It found two.

**One introduced, by the gate restored two commits earlier.** `committed is None` conflates
three states — no file expected, the file is gone, and *the submodule is not checked out* — and
the restored `absent` gate saw two. `--fetch` is a documented local command, so a developer with
a partial checkout was told a good repository had lost its page and the run exited 1: **the
instrument blaming the page for the state of the disk**, which is the class the same branch had
spent the evening removing.

*And the first guard for it asserted only the exit code*, leaving the half of the repair that
lives in `clauses.py` unguarded — this file's own §13.5 lesson, needed again one commit after it
was written down. Two mechanisms answer that question and a guard has to reach both.

**One inherited, and it is the third instance of a lesson this file already records twice.**
`(?:@import|src\s*:)` has no left boundary, so `mask-src:` matched and a remote image in a mask
refused the build as a third-party *font* — a false gate on a gated clause. It reproduces at
`aeb643a`, before any of the day's work. `clauses.py`'s own comments on `_LENGTH` and
`_WIDTH_KEYWORD` say, a few lines above it, that `\b` is not a boundary against `-`.

### 13.8 The measurement that says the day moved no page

Run this morning's checker and this evening's over the same eleven committed surfaces:

> **byte-identical output, apart from three detail strings** where clause 4 now reads *the
> project's name* instead of *the repository's name*.

Every clause, every verdict, every census row, every other detail: unchanged. That is what the
day's twenty-odd defects and their repairs cost the pages, and it is the number this record
should be read against — the instrument moved a great deal and the portfolio moved not at all.

*Which is also the honest limit of it.* Nothing above was found by a page regressing; it was
found by looking at the instrument. The instrument is now considerably better at refusing things
that have never happened, and the two clauses that actually fail on real pages — the separator
and the `<title>` — are exactly where they were this morning.


## 14. The landing surface, measured — and why §7 row 11 cannot be done the way it is written

Taken 2026-09-08, straight after S9/S10 closed, because row 11's cost was entirely determined
by a measurement nobody had taken and the measurement costs one fetch. §9 argues the asymmetry;
this is what is actually on the other side of it.

### 14.1 The row's own prescription fails on contact

Row 11 says *"at minimum a `Surface` read by `--fetch` in `live`"*. Fetched
`https://github.com/P0w3r223` and parsed it with the checker's own `render.parse`:

| what the checker would read | value |
|---|---|
| `<title>` | `P0w3r223 (Piotr Cząstkiewicz) · GitHub` |
| headline | `Piotr Cząstkiewicz P0w3r223` |
| `.eyebrow` | absent |
| `og:title` | `P0w3r223 - Overview` |
| anchors ending at the profile | **10** |
| grouped figures | 0 |

**Adding that surface to `SURFACES` today reddens the `live` job on its first run**, on four
gated clauses at once: `4 title` (leads with the identity), `4 h1` (equals the profile name),
`4 eyebrow` (absent) and `6 back-link` (the clause asks for exactly one; there are ten).

And every one of those four is a property of **GitHub's chrome, not of the README**. The title,
the header, the navigation and nine of the ten profile links are markup this portfolio does not
author and cannot change. The clauses were written for a self-hosted `docs/index.html` where the
repository owns every byte; pointed at a rendered profile they measure the host.

*So the row is not "small" and it is not "add a Surface". It is a scoping decision the record
has never taken: **which clauses can even be asked of a surface somebody else renders.*** Two
routes exist and both were confirmed reachable — the rendered fragment isolates cleanly at
`<article class="markdown-body …">`, and the raw markdown is 4320 bytes at
`raw.githubusercontent.com`. Neither is free: the first parses a container GitHub can rename,
the second is Markdown and the whole checker reads HTML.

### 14.2 What the surface actually says, which is the stronger half of §9's argument

**Six of the twelve are linked from it. Six are not.**

| linked | `ab-lab`, `apply-scout`, `car-price-ml`, `doc-extract`, `mlops-car-price`, `token-budget` |
|---|---|
| **not linked** | `auth-log-scan`, `it-job-radar`, `mini-traceroute`, `pl-jobs-lora`, `pl-review-sense`, `wroclaw-air-insights` |

§9 says the landing surface has no instrument. The sharper fact is that it **omits half the
portfolio** — including every one of the six repositories S9 and S10 spent a day polishing. A
recruiter arriving at the profile cannot reach `wroclaw`'s live forecast, `it-job-radar`'s forty
figures or `pl-review-sense` at all. *Whether that is an editorial decision or an omission is
not something an instrument can answer, which is exactly why it belongs in this document and
not in the checker.*

> **Corrected 2026-09-09, while opening S8a — the last sentence of that paragraph is false and the
> table above is measuring one thing while the prose claims another.** The README is unchanged since
> 2026-09-03, so this is a reading error and not drift. **All twelve are reachable**: the six in the
> "not linked" row each appear in the *Live demos* table as a bare `https://p0w3r223.github.io/…`
> URL, which GFM autolinks. What the table actually counts is **repository** links, and there the
> split holds — six get a `github.com` link, five of them as a described row in the main table and
> `token-budget` as a bullet under *Also on the profile*; the other six get a *Live demos* row with
> a raw URL and no repository link at all.
>
> *The finding survives in the weaker and more useful form:* the profile does not omit half the
> portfolio, it **demotes** half of it to a link with no description. §9's asymmetry argument does
> not depend on the half that was wrong, and §7 row 11's priority is unchanged. **What the error
> cost is the point**: a row 11 planned on "six projects are unreachable" would have been scoped as
> a rescue and is in fact a copy edit — which is `0008` §4.1's *"a citation can be invalidated by
> your own correctness"* in its other direction, a conclusion overreaching a table that was right.

### 14.3 And it quotes two figures, one of which is already rounded past its artifact

The README carries two claims with figures, both sourced from other repositories:

| claim | artifact says |
|---|---|
| *"the Ministry's KSeF FA(3) schema carries **328** enumerations"* | `doc-extract/docs/index.html` prints `328 enumerations` — **agrees** |
| *"turn a true null into a **25–66%** false positive rate"* | `ab-lab/docs/index.html` prints **`25.3%`** and **`65.7%`** |

The second is prose rounding and defensible as prose. It is also, precisely, what `0007` §5.0
governs — *every figure a surface prints is a figure a committed artifact prints* — and **nothing
anywhere checks it.** `ab-lab` re-recorded its evidence during S9 (§4.17 item 5 in `0008`); the
rates happened to reproduce to the digit, so the profile survived. A seed change, a package
change or a re-run on different data moves `65.7` and the landing surface goes stale silently,
on the one page a reader reaches first.

*This is `0008` §5's carried README row — twelve of thirteen READMEs hand-typed with no carrier
— arriving at the thirteenth and worst instance. The row says a provenance reader "should follow
S9 rather than ride inside it." S9 has now landed, and this is the surface that should be its
first target rather than its last.*

### 14.4 What this changes about the order

Row 11 stops being an S-sized "add a surface" and becomes an M-sized stage with a decision in
front of it. It also stops being interchangeable with `0008` §5's README-provenance row: they
are the same build aimed at the same class of defect, and §14.3 is the evidence that the
profile is where that build pays first.

**It does not move ahead of row 12.** A page that fails WCAG harms a reader now; a figure that
may go stale harms one later, and the artifact it quotes reproduced this week. §3.1's promotion
rule reaches row 12 and not this one.

## 15. The test audit of 2026-09-09, and the commit that merged into no branch

§13 is this document's form for an audit and this is the second one. It was commissioned hours
after S13 merged, on the same reasoning: the stage had shipped five new modules and its guards
had been reviewed against the stage rather than against each other. **The method is the one
`CLAUDE.md` states and no other — break the thing a test names, watch it go red, put it back.**

*Recorded here a day late, and that is the first finding.* For one day the whole audit existed
in commit messages and test docstrings and **nowhere under `docs/`** — which is §13.4's first
erratum happening again, in the same shape and to the same class of content. The part that
could not survive there at all is §15.4's.

### 15.1 A production crash, and the guard was one module to the left

`colour.resolve()` returns whatever the palette holds, not only a hex. A token carrying
`rebeccapurple`, `rgb(37 99 235)`, `#11111180`, `light-dark(…)`, `oklch(…)` or another `var()`
comes back **non-`None`**, nothing marked the site unresolved, and it reached
`colour.composite()` and raised out of `clauses.check`. **One token on one page killed the
whole twelve-surface run** — six of six notations fatal, control passing.

Three things make it this codebase's characteristic failure rather than an ordinary bug, and
all three are on the record already in other words:

1. **`paint.py`'s docstring claimed the opposite, while arguing that a repair was
   unnecessary** — *"a chained token would come back unresolved and be reported under
   `contrast ground`, which is an admitted unknown and not a wrong colour."* It was not
   unresolved. The paragraph was corrected in place rather than deleted, because the reasoning
   it carried is the reasoning that was wrong.
2. **The class was already guarded one module to the left.** Four tests in `test_clauses.py`
   assert that every one of these notations is handled honestly, and **every one of them calls
   `clause_1_tokens` directly rather than `check`** — so the defect moved and the guard did
   not:
   - `test_a_ground_that_is_not_a_hex_colour_is_reported_rather_than_raised`
   - `test_an_alpha_hex_token_is_reported_without_a_ratio_rather_than_crashing`
   - `test_a_colour_notation_this_reader_cannot_parse_is_undecided_not_failed`
   - `test_a_named_colour_is_undecided_rather_than_failed`
3. The first of those four carries a docstring describing this exact crash **in the past
   tense**: *"a `ValueError` that took the whole twelve-surface table down with it."*

*Those four were cited by line number in this section's first version and were each seven low
by the time it shipped, because the sibling commit in this same pull request inserted a
seven-line section header above them. A test name cannot drift that way — and this section
ships alongside two test deletions, which is what makes the point practical rather than
stylistic.*

It was also one commit from firing on a real stage: `0008` S7 migrates the `--ink`/`--line`
aliases, and `test_an_alias_that_actually_resolves_is_not_reported` proves `--text: var(--ink)`
is a shape the plan commits to. The fix is `is_opaque_hex` and not `is not None`; the site now
reports under `contrast ground` with what the token resolved to, which is what the census is
for. Guarded twice — parametrised over all six notations **through `clauses.check`**, and at
`Site.ratios`, because a `Site` built any other way reaches the arithmetic too.

### 15.2 Guards that could not see what they named

Every one of these left the suite green while the thing it names was broken, and each was
reproduced before anything was written. Five of the first six are on **gated** keys, which is
where a blind guard costs a refused build or an accepted defect rather than a wrong line:

- **A dirty submodule stopped being a finding.** No test anywhere constructed `dirty=True`.
  `CLAUDE.md` spends a paragraph on what that costs — twelve `CLAUDE.md` and eight `README.md`
  uncommitted for an hour with `pagespec` reading pages nobody had published.
- **`_CSS_DERIVED` could drop clause 3**, because the guard naming both clauses ran over a
  fixture page with no table, so its clause-3 half was unfalsifiable.
- **`origin_answered`'s 5xx boundary was unguarded on the stylesheet path** — widened, a Pages
  503 mid-deploy refuses the build; the defect that function's docstring exists to end.
- **A trailing space survived on the last declaration of every block**, which fails a value
  against the exact value it declares: a *false* gate, which this repository ranks worse than
  a missing one.
- **A palette declared on `html` was read by nothing**, reporting *"no custom properties
  declared at all"* on a conforming page.
- **First-wins on `<title>` was claimed by two docstrings and covered by neither** — one of
  them says it tests the SVG rule *with first-wins taken out of the picture*, which is exactly
  true and left the rule itself unguarded. Two `<title>` in one `<head>` separates them.
- **Three loops over `spec.uncarried()` went vacuous together.** Returning `()` left the suite
  green while `report()` printed *"0 carried by nothing"* and suppressed the block — **full
  coverage announced over the omissions**, which is verbatim what `tools/spec.py`'s opening
  lines say the registry exists to end.
- **Five documented capabilities no guard could see**: case-insensitive at-rules and property
  names (dropping the first reads a whole dark palette as light, on a gated clause); the `U`
  flag for a conflicted submodule, documented in `entry_state.py`'s own comment; a `<meta>`
  carrying both `name` and `property`; and `_where`'s tuple order, where **no verdict moves**
  — which is exactly why nothing caught it.

### 15.3 The lower-severity list nobody had measured: 0 of 8

The audit's §2 carried a second list, and the first summary of the audit omitted it as
housekeeping. Measured, **none of the eight was caught**. Three have real teeth:

- **`strip_comments` substituted a space and nothing said why.** With `""`, `.a/*c*/.b` becomes
  `.a.b` — a compound selector matching one element carrying both classes, where the page wrote
  a descendant. Two different rules, one invented by the reader.
- **`GIT_TERMINAL_PROMPT=0` was carried by nothing.** `capture_output` gives a credential
  prompt a stdin nobody watches, so the session-start hook blocks until it is killed.
- **`repo_checked_out` defaulted to `True`, and the direction is the decision** — fail-open on
  the key deciding whether a missing page refuses the build.

### 15.4 Two duplicates, and the deletion is the half that needed a record

Two guards were deleted: a focus ring and a rail exemption, each a bare restatement of a
neighbour that carries the reasoning, each asserted a second time with no docstring. **The
deletion is proved rather than argued** — breaking what each one covered still reddens the
suite, measured — and that proof is why this section exists. *A green suite cannot detect a
deleted test.* The proof lived in one commit message on a branch that squash-merge makes
unreachable, which is precisely §13.4's `#86` shape, and this paragraph is where it becomes
durable.

### 15.5 The counts, and which two of them are hand counts

Taken from the collector rather than from a summary, because this section is about guards that
could not count what they claimed:

| point | collected |
|---|---|
| `93f79f4`, S13's entry | 519 |
| `7461e5f`, S13 merged and the pointers bumped | 576 |
| `d9fd048`, the audit's first four commits (`#109`) | 600 |
| the lower-severity list and the two deletions | 605 |

`#109` adds **13 test functions** and two parametrisations for **+24** collected;
the last commit adds **7** and removes **2**, for **+5**. `#109`'s title says *eleven* guards
and the last commit's message says *eight* items — **both are hand counts of findings, not of
functions**, and they do not reconcile with the table because they were never meant to: one
guard asserts two knobs (the single network call's user agent *and* its timeout). Neither
figure is wrong; **no instrument prints guards-per-finding**, so under this repository's own
rule they are labelled rather than repeated.

### 15.6 A commit that merged into no branch, and the CI hole under it

The last commit was authored at **15:55 +0200**. Its pull request, `#109`, had squash-merged
**eighteen minutes earlier, at 15:37 +0200** — the same instant `gh` reports as `13:37Z`, and
the first version of this sentence put the two figures side by side in different frames, which
read as a gap of two hours. So the commit sat on a remote branch whose pull request was
**closed**, and:

- `push` in `pagespec.yml` is filtered to `main`, and `pull_request` needs an open one — so the
  commit had **no CI run at all**, and in particular never met `core`, the job that checks out
  no submodules and the only one that would catch a guard depending on a sibling being present.
- `gh pr list` shows nothing, and `git rev-list --count` reports *five ahead* — four of which
  are the squash. **Counting says unmerged work; only comparing trees says which.** The method
  that settles it is the one already on the record: locate the content on `main`, not the
  commits.

*And the hole is wider than the commit.* `docs/**` appears in neither `paths:` filter, so a
documentation-only pull request receives no run — `0008`'s Sx row recorded that for `b416c83`
and it is still true. **That is why this section ships in the same pull request as the guards
rather than after them**: bundled, the audit's record rides behind a green `core`; split, it
would be checked by nobody, and the deletions in §15.4 would reach `main` unrun a second time.
