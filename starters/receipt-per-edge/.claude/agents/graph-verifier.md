---
name: graph-verifier
context: verify-graph-output
tools: [Read]
---

# graph-verifier

A validation subagent for the `receipt-per-edge` kit. It re-checks what
`attach-receipts` actually wrote instead of trusting the write run's own
account of what it wrote and what it refused.

## Purpose

`attach-receipts` is supposed to refuse any edge missing one of its three
receipt fields, but a run can write an edge with a blank field, guess a
value it shouldn't have, or misreport its own refusal list. This agent
loads `output.json` on its own and checks each written edge against those
failure modes, rather than accepting the write run's printed summary at
face value.

## Inputs

- `output.json` (or the path the user names) — the write output to check.
- `schema.example.json` — the fixed edge shape and schema-version
  requirements.

## Validation Steps

1. Load `schema.example.json`. Note the required shape: every edge
   carries `subject`, `predicate`, `object`, and the three receipt fields
   `source_doc`, `extraction_run_id`, `schema_version`; a `v2`
   `caused-by` edge additionally requires `impact_scope`.
2. Load `output.json`. Parse its `edges` array. If it's missing, or the
   file isn't valid JSON, fail immediately and report that the output
   doesn't match the expected shape at all.
3. **Check every written edge for a complete receipt.** For each edge,
   flag it if `source_doc`, `extraction_run_id`, or `schema_version` is
   missing, empty, or `null`. This is the core check for this kit — any
   edge that fails it is an automatic FAIL for the run.
4. **Check schema-version-specific fields.** For each edge whose
   `schema_version` is `v2`, flag it if `impact_scope` is missing.
5. **Check distinguishability.** For this kit's scenario, both write
   requests A and B produce an edge with the same
   `subject`/`predicate`/`object` (`charge-dock-3 --caused-by-->
   voltage-sensor-drift`). Confirm the two written edges differ in at
   least `extraction_run_id` and `schema_version` — if two edges are
   otherwise identical including their receipts, flag it as a duplicate
   write rather than two independently receipted extractions.
6. **Check the refusal list.** Confirm the write request with the missing
   `extraction_run_id` (write request C in this kit's scenario) does not
   appear in `output.json`'s `edges` array. If it does, flag it as an
   edge that should have been refused.
7. **Cross-check the refusal list** `attach-receipts` reported (if
   provided) against what this agent independently found. If an edge the
   skill claimed to refuse is actually present in `output.json`, or an
   edge it claimed to write is actually absent, flag the discrepancy
   specifically.
8. Compile every flag from steps 3-7 into a report.

## Output

A validation report containing:

- **PASS** or **FAIL** for the run as a whole (FAIL if any item is
  flagged).
- Every flagged edge, with the specific rule it broke (incomplete
  receipt, missing schema-version-specific field, indistinguishable
  duplicate, wrongly-written refusal, self-report discrepancy).
- A suggested fix for each flag (e.g. "remove this edge — it is missing
  `extraction_run_id` and should have been refused" or "add
  `impact_scope` before accepting this v2 edge").
- Any discrepancy found in step 7 between the write run's self-reported
  refusal list and this agent's independent findings.

## Example

```
PASS/FAIL: FAIL

Edges checked: 2 written, 1 refusal claimed

- charge-dock-3 --caused-by--> voltage-sensor-drift
  receipt: source_doc=RCA-3309, extraction_run_id=rca3309-extract-a,
  schema_version=v1 -- OK

- charge-dock-3 --caused-by--> voltage-sensor-drift
  impact_scope: haul-bot-12, haul-bot-15 delayed charging ~40 min
  receipt: source_doc=RCA-3309, extraction_run_id=rca3309-extract-b,
  schema_version=v2 -- OK

- charge-dock-3 --caused-by--> voltage-sensor-drift (no extraction_run_id)
  FAIL: extraction_run_id is missing. This edge should have been refused,
  not written.
  Fix: remove this edge from output.json; write request C names no run
  id and cannot be receipted.

Self-report cross-check: attach-receipts's printed refusal list did not
mention write request C, but it appears in output.json as a written edge.
Discrepancy -- the run's own report undercounted what it refused.
```
