# The review of the whole system

Date: 2026-09-07
Status: accepted
Author: Piotr Cząstkiewicz
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
| 2 | The three code defects before S9 touches five stylesheets: `_VAR_FALLBACK`, `clause_3_tables` per table, `sources.py:141`'s cause | W2, W3, N5 | S | open |
| 3 | A **`GATED` floor guard** — every key reporting zero `FAIL` must be in the tuple — plus the assertion repair in §5.2 row 2 and the rebuild of the ratchet test before it becomes unsatisfiable | §5.1 | S | open, and **S9/S10 both edit that tuple** |
| 4 | Clause 8's regex in the bound-preserving form (§4.1), and a stated decision on `n/a` and `U+2009` | §4.1, §5.2 | S | open — zero corpus delta, safe now |
| 5 | A **clause registry** — `CLAUSES` keyed by clause-sentence id, each carrying `carried_by: index \| repo-test \| review \| none`, with a `core`-job test that every entry has a check or an explicit reason | W1, and gives clause 9 and the geometry half an honest home | S | open — the artifact whose absence produced all three occurrences |
| 6 | Re-scope S9's first commit: no permanent source census; reconcile against the checker's existing per-surface inventory and let the ratchet carry recurrence | W4 | *a saving* | open — the ledger's own evidence supports it |
| 7 | S9 and S10, with `wroclaw/tests/test_report.py:1524` widened in the same commit that moves the separator | the two failing clauses | 2.5–3 d | open, per `0008` |
| 8 | The scheduled `live` job hashes all twelve fetched surfaces against their committed files, reporting a mismatch under its own finding key | **C1**, both halves | S | open |
| 9 | Split `0008`: ledger, **a failure-taxonomy document**, measurements to the report | §6.2 row 5 | S | open — after S9/S10, so the file is smaller when split |
| 10 | **Sx** — 11 `pyproject.toml`, 70 `Author:` fields | dead weight | 0.5 d | open, depends on nothing |
| 11 | Bring the **profile README** into the system — at minimum a `Surface` read by `--fetch` in `live`, plus the quotation rule | the asymmetry in §9 | S | open |
| 12 | **Contrast at the usage site** — a clause using the existing `colour.resolve()`/`composite()`, `UNDECIDED` for `color-mix`, `opacity < 1` and SVG paint order, threshold per usage site | N4, `0007` §7's largest gap | M | open — ships report-only, enters `GATED` only when a stage closes it |
| 13 | Registry-drift test (N1) · resolve N3 (implement the geometry half or amend `ADR-0004` §4 to say it is deferred and unowned) · clean `autoMode.environment` | N1, N3, §6.2 row 4 | S | open, each independent |

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
