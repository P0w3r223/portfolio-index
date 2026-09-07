# CLAUDE.md — current_projects

Guidance for Claude Code (and any contributor) working in the portfolio index.

## What this repository is

The **private** index of a twelve-repository portfolio. It is not a package: nothing here is
installed, imported by a sibling, or published — `pyproject.toml` exists so `pytest` finds the
checker, and says so in its first line.

Two things live here and nowhere else, and they are the reason a session starts here at all:

- **The page specification.** `docs/audit/0007_divergence-and-the-page-spec.md` §5 is normative
  prose — eight clauses plus §6's clause 9 and §5.0's governing rule. The twelve published pages
  are held to it.
- **The instrument that enforces part of it.** `tools/pagespec` reads eleven committed surfaces
  from the submodule working trees and one from its live URL, prints a conformance table, and
  since `0008` S-gate **refuses** when a clause in `GATED` fails.

**The public landing surface is not this repository's `README.md`.** This repository is private;
the surface a recruiter reaches is the profile README at `github.com/P0w3r223`, which is a
separate public repository (`P0w3r223/P0w3r223`) and is **carried by nothing here** — no clause,
no test, no row of `SURFACES`. `README.md` in this repository is an internal index that happens
to be written in a recruiter's register. Do not repair one and assume the other moved.

## Architecture

```
tools/pagespec/       the checker — standard library only
  sources.py            the surface registry and the ONLY I/O; everything else is pure
  render.py             HTML -> Page (title, headline, tables with ancestry, rendered text)
  css.py                CSS -> rules, with comments stripped and media conditions flattened
  colour.py             WCAG arithmetic; contrast() ships, resolve()/composite() are unused
  clauses.py            clauses 1-8 as pure checks over one Loaded
  __main__.py           the report, the role census, and the GATED ratchet
tools/entry_state.py  0008 §6's two repository-state rows, at two depths
tests/                the guards; fixtures/ are reductions of record, see its README
docs/adr/             what carries what; 0004 is the load-bearing one
docs/audit/           the record: 0001-0006 earlier sessions, 0007 the spec, 0008 the plan
.github/workflows/    pagespec.yml — core (no submodules), surfaces (gates), live (scheduled)
<twelve directories>  the submodules; each is a standalone repository with its own CLAUDE.md
```

**Which document is which**, because they are not interchangeable and `ADR-0004` §5 is the rule
that separates them: `0007` §5 keeps the **rules**, the checker owns the **conformance table**,
and `0008` owns the **plan and its status**. A measurement written into a normative document
cannot be accepted without being frozen — `0007` §3 was corrected five times before that split.

## Commands

```bash
python -m tools.entry_state              # the entry state, quick
python tools/entry_state.py --hook       # verbatim what the session-start hook runs. By path,
                                         #   because the module form needs the root on sys.path
                                         #   and so depends on the hook's working directory;
                                         #   `--hook` is what keeps a real finding from reading
                                         #   as a broken hook
python -m tools.entry_state --full       # every pointer against its own remote, before a stage

python -m tools.pagespec                 # the conformance table; exits 1 if a GATED clause fails
python -m tools.pagespec --detail        # every finding, which is what CI runs
python -m tools.pagespec --report-only   # print and exit zero whatever it finds
python -m tools.pagespec --only ab-lab   # one surface
python -m tools.pagespec --fetch         # include wroclaw, which commits no HTML

python -m pytest                         # the whole suite
python -m pytest -m 'not submodules'     # what CI's `core` job runs — no sibling on disk
python -m pytest -m submodules           # only the tests that read a working tree
```

## Working rules

- Branches and pull requests, [Conventional Commits](https://www.conventionalcommits.org/),
  and a description that says **why**. One stage per pull request where the stage allows it.
- **Every stage closes with a `code-reviewer` pass** before it is proposed as merged work.
- **A guard is not proven until a mutation reddens it.** Break the thing the test names, watch
  it go red, put it back. `0008` records at least seven guards that shipped green over the
  defect they existed to catch, and every one was found this way and no other.
- **Figures come from an instrument, not from a hand count.** Clause 1's census and the role
  census are computed on every run for this reason; three hand-counts of clause 8's write sites
  produced fifteen, eighteen and nineteen against a true twenty.
- **Record a correction rather than quietly fixing it.** A reader carrying the old figure
  forward is how `0006` §2.4 happened. The errata sections of `0008` are the form.

## What not to do

- **Do not hand-edit `GATED`** (`tools/pagespec/__main__.py`) as part of unrelated work. It is a
  ratchet: it names the finding keys that report zero `FAIL` across every surface read, and a
  closing stage adds its own. Widening it past the measurement is caught by
  `test_the_ratchet_holds_no_clause_the_committed_surfaces_report_failing`; **narrowing it is
  not caught by anything** — every prefix can be removed with the suite green. Clause 8 enters
  with S9 and clause 4-`<title>` with S10, and both stages edit this tuple.
- **Do not weaken a guard to make it pass.** A guard that has started failing is a finding.
- **Do not add a dependency.** The checker is standard library only and `pytest` is the sole
  test dependency; the `core` CI job installs nothing else.
- **Do not commit a page from here.** The pages belong to their own repositories and are
  generated there; most carry a page test of their own. No count is given, because three
  different sweeps for one produced three different answers — ask the trees, and mind that a
  repository can guard its page without the string `docs/index.html` appearing in its tests.
  What is settled: **`mini-traceroute` holds no Python at all** — no `pyproject.toml`, zero
  `.py` files — so it can carry no local page test, which makes it the one surface the index
  checker guards alone. This repository re-points submodules; it does not edit them.
## The published surfaces, and what the gate does not say

Twelve surfaces: eleven read from committed files, and `wroclaw-air-insights`, which commits no
HTML at all and exists only at its URL — `--fetch` reads it, and only the scheduled `live` job
passes that flag. `reports/site/` in that repository is a gitignored local build and reading it
has produced a wrong answer that survived a session.

The gate is **deliberately partial**. `UNDECIDED` never gates, which is what lets the checker be
honest about `color-mix()`, an unread media condition, and a headline it cannot judge. Two
clauses print and do not gate — clause 8 (the thousands separator) and clause 4's `<title>` half
— and they are the open work, not an oversight. `python -m tools.pagespec` exiting 0 today
therefore means *no gated clause failed*, and not *every clause passes*.

Half the specification cannot be carried from here at all, by construction: a repository's own
artifacts, and `0007` §5.0's rule that every figure a surface prints is a figure a committed
artifact prints. Those are the submodules' own page tests. `ADR-0004` is the decision and its
amendments record how the split moved.

## Code intelligence

**There is no `.codegraph/` here.** Ten of the twelve submodules carry one and their `CLAUDE.md`
say so; `doc-extract` and `pl-jobs-lora` carry neither the index nor a mention of it. This
repository has none either, so the `codegraph_explore` MCP tool and the `codegraph` CLI answer
about whichever project you point them at and about nothing in `tools/` or `docs/`.

Grep, Glob and Read are the tools here, and the Python is small enough that this costs nothing.
**The record is the large thing** — `docs/` is several times the size of `tools/`, and `0008`
alone is longer than any module in it — so prefer reading a named section over reading a file,
and prefer the checker's own output over any figure the record quotes. No line count is written
down here on purpose: a figure in this file would be a hand-typed one, which is the practice the
section above forbids.

## Read the entry state before quoting anything

`0008` §6 is a table of assumptions to verify **before each stage, not once**. Two of its rows
are now `python -m tools.entry_state`; the rest are still yours to check, and the module's
docstring names which.

- **`git fetch` first.** `origin/main` is a local file a session inherits and nothing refreshes
  on its own. On 2026-09-07, an hour after `#77` merged, two passes independently reported the
  index as unmerged with no pull request open — which is exactly what a stale ref plus a
  *closed* (not never-opened) pull request looks like. Three signals agreed with the false
  hypothesis at once.
- **This repository squash-merges.** A branch commit is never reachable from `main` and never
  will be. Cite the commit on `main`; a cell citing the branch SHA is citing a commit that does
  not exist for any reader. `0008` §4.12 records the S-gate row doing it.
- **Check the working tree before quoting the checker.** A submodule on a fix branch, or a
  round of uncommitted edits, means `python -m tools.pagespec` is reading pages nobody has
  published. That has happened, for an hour, across twelve `CLAUDE.md` and eight `README.md`.

*This section sits last on purpose.* It is the one part of this file that has already been
paid for: two passes reached the same false conclusion on 2026-09-07 because none of it was
loaded, and a reader's attention is weakest in the middle of a document and strongest at its
end. Everything above tells you what this repository is; this tells you what to check before
you say anything about it.
