# ADR 0003 — P5 metric design: rules derived from defects found in P3 and P4

Date: 2026-08-18
Status: accepted
Author: Piotr Cząstkiewicz + Claude
Related to: [0001_p5-doc-extract-thesis.md](0001_p5-doc-extract-thesis.md), [0002_p5-corpus-strategy.md](0002_p5-corpus-strategy.md)

---

## Context

P5's thesis is that a validator can be used as a label-free error detector. That claim is only as
good as the measurement behind it, so the measurement layer is the part most worth designing
deliberately — and the two sibling projects supply a precise list of what goes wrong when it is
not.

Both code reviews found the same class of failure in both repositories: **metrics that reward the
absence of a prediction, and metrics that cannot vary.** These are not exotic. They are the bugs
most extraction harnesses have, which is why getting them right — and documenting why — is itself
a differentiator.

### The defects, as found in committed code and committed numbers

| Repo | Defect | Evidence |
|---|---|---|
| P4 | `_score_salary` returns `1` on every sub-metric when both sides are `None`; ~69 % of gold has no salary | `bielik-1.5b-gguf__zero` scores **0.75/0.87/0.74 on salary at 0.049 JSON validity** |
| P4 | `SetMetric.add` credits `exact += int(ps == gs)` for empty-vs-empty | `tech_optional` exact_match 0.60 for a model predicting nothing |
| P4 | A partial predictions file scores on its own subset; the report header prints the **gold** count | a run dying at record 5 of 142 renders as full coverage |
| P4 | "JSON validity" measures post-repair schema conformance; raw output and failure reason are discarded, prediction files gitignored | no post-hoc error analysis is possible without paying for the run again |
| P4 | Three of six scored fields are not recoverable from the model's input, two reported as if they were | `tech_expected` gold comes from a widget stripped from the input; every variant scores 0.01–0.02 on `tech_optional`, yet it is one of four equal terms in the headline `mean_field_f1` |
| P3 | `citation_fidelity` can only fall if the model cites a URL absent from the report it just wrote | **1.00 on both models across all 8 tasks** — zero variance |
| P3 | `unsupported_after=0.0` is a literal constant, reported as half of a before/after measurement | ADR-0003 there sells the pair as the differentiator |
| P3 | `requirement_f1` is `strip().lower()` set matching over free-text phrases | **Haiku 0.31 > Opus 4.8 0.25** — a string-formatting lottery read as a capability finding |
| P3 | `completed` means "no exception was raised" | the deliberately planted JS-only failure task scored *completed* on both models |
| P3 | cost and call counts aggregated over completed runs only | a model that burns budget then fails contributes nothing to reported cost |

## Decision

Nine rules, written into the project's `CLAUDE.md` as constraints rather than left as intentions.

1. **Empty-versus-empty never earns a point.** Every field metric reports `support` (how many gold
   records carry the field) and separates **detection** — the present/absent decision, scored over
   all records — from **value accuracy given the field is present**, scored over supported records
   only. This is the direct fix for `_score_salary` and for `exact_match`.

2. **Coverage is asserted, then rendered.** The scorer refuses to run when predictions are fewer
   than gold, and `coverage` is a column in the table rather than a field in a JSON file nobody
   opens. The rendered `n` is the number scored, never the number of gold records.

3. **Every prediction row carries a failure class**: `ok | no_json | schema_error | truncated |
   refused | api_error`, plus `stop_reason` and a truncated `raw`. **Prediction files are
   committed.** Without them no error analysis is possible without re-paying for the run — the
   dead end P4 is currently in.

4. **Matching is field-type aware.** Exact after normalization for NIP and dates; ±0.01 tolerance
   for money; an explicit, documented alignment rule for line items. One F1 over everything is the
   bug that produced "Haiku beats Opus".

5. **No constant metrics.** A metric identical across every variant is fixed or removed. A number
   that cannot vary is not measuring anything, and publishing it as a headline is worse than
   publishing nothing.

6. **No metric may be a hardcoded value.** If a quantity is `0.0` by construction, it is an
   assertion in a test, not a column in a results table.

7. **Cost is computed over all attempts, not successes**, and **both sides are priced as numbers**.
   A dash in the cost column makes the comparison rhetorical rather than arithmetic; the local side
   gets an amortized figure (GPU-hour price × measured throughput) or an explicit `0.0`, never
   `None` rendered as `-`.

8. **`stop_reason` is handled explicitly.** `max_tokens` and `refusal` must not fall into the
   success branch — an invoice truncated mid-JSON is otherwise indistinguishable from a successful
   extraction. Extraction and repair get **separate** `max_tokens` ceilings; P3's shared 4096 turns
   a long document into truncation → `ValidationError` → retry → identical truncation, three times
   at full price.

9. **A metric may not be validated against model-generated ground truth.** P3's guardrail derives
   its set of "real" URLs from a report that is itself an unconstrained LLM output. P5's
   equivalent — grounding — is checked against the **source document**: every extracted value must
   resolve to a span in the text, matched exactly, after normalization, or numerically.

### The two headline metrics

Neither exists anywhere else in the portfolio.

- **Detector quality.** Does `invariants_pass ∧ fully_grounded` predict "all critical fields
  correct"? Reported as precision, recall and a confusion matrix, with base rates alongside so the
  numbers can be read against chance.
- **Selective prediction.** The coverage–accuracy curve, with human review cost as the second
  axis. This is the number a buyer of such a system actually asks for, and it is entirely absent
  from both siblings.

## Alternatives considered

- **Port P4's scorer and patch the known bugs.** Rejected: the bugs are structural (the metric
  definition credits absence), not incidental, and the shared-code path is exactly the ~600 LOC
  overlap that would make P5 a reskin.
- **Use an LLM judge for field correctness.** Rejected for the same reason P3's ADR-0003 rejects it
  for the guardrail, and more strongly here: with exact gold from the generator, correctness is a
  comparison, not a judgement call. Reserve model judgement for things that need it.

## Consequences

- Reported numbers will look **worse** than a naive harness would produce, because silence stops
  earning credit. That is the point, and the README must say so explicitly — otherwise the project
  compares unfavourably against siblings whose numbers are inflated.
- Committing prediction files costs a few hundred KB and makes every published number
  re-derivable and re-scorable by a reader. This is a hard requirement, not a nicety.
- Rules 1 and 2 must be enforced by tests that fail loudly, not by convention. Specifically: a test
  in which an **invalid** prediction is scored against gold whose field is absent, asserting it
  earns nothing — the test P4 lacks, because its equivalent only exercises gold that *has* the
  field.
- Rule 9 means grounding is implemented before the detector study, since the detector's second
  conjunct depends on it.

## Open question, deliberately not decided here

P4's headline `mean_field_f1` gives equal weight to a field no model can recover from the input.
The choices are to drop such fields, to weight by support, or to keep them as an explicit
hallucination probe reported separately. This changes what a project *claims*, not just how it
computes, so it is recorded as a decision to take with eyes open in each project rather than
settled by fiat here.
