# portfolio-index

This repository is the maintenance record behind my portfolio. To see the projects, start at my
profile: [github.com/P0w3r223](https://github.com/P0w3r223).

## What is here

- [`docs/adr/`](docs/adr): nine decision records about the portfolio itself, such as what carries the
  page specification and how the gate registry works.
- [`docs/audit/`](docs/audit): dated audits of how the portfolio presents itself. Each one reads as it
  was written on its date.
- [`tools/pagespec`](tools/pagespec): a standard-library checker. It reads the published pages of the
  twelve project repositories, prints a conformance table against the page specification
  ([`docs/audit/0007`](docs/audit/0007_divergence-and-the-page-spec.md) §5) and fails CI when a gated
  clause fails.
- The twelve project repositories as submodules, pinned to the commits the audits refer to.

## How I work

I build with Claude Code and review every change myself; the details are on
[my profile](https://github.com/P0w3r223#how-i-work).

## Run the checks

```bash
git clone --recurse-submodules https://github.com/P0w3r223/portfolio-index
cd portfolio-index
python -m tools.pagespec           # eleven committed pages, conformance table
python -m tools.pagespec --fetch   # all twelve pages, as served
python -m tools.spec               # every normative sentence and what enforces it
pytest
```

## Conventions

- Commits follow [Conventional Commits](https://www.conventionalcommits.org/); work goes through
  branches and pull requests.
- Every figure a page prints is a figure a committed artifact prints (`0007` §5.0).

---

<sub>This repository is the published copy of a private working repository, so `#N` in commit
messages refers to pull requests there.</sub>
