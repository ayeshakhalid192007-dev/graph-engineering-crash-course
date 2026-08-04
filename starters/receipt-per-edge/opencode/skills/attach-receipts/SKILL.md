---
name: attach-receipts
description: OpenCode equivalent of the Claude Code attach-receipts skill and graph-verifier agent — attaches receipts to written edges and verifies none is missing one
context: pattern-implementation
---

# attach-receipts (OpenCode)

OpenCode equivalent of this kit's Claude Code pair
(`.claude/skills/attach-receipts/SKILL.md` +
`.claude/agents/graph-verifier.md`). OpenCode's config doesn't have a
separate subagent file the way Claude Code does, so this single skill
runs in two modes, driven by `opencode.json.example`'s `workflow.steps`:
**attach** (the write behavior) and **verify** (the independent recheck).
Both modes read the same `schema.example.json`, so the two never drift
apart on what counts as a complete receipt.

## Instructions

You are an OpenCode skill implementing the `receipt-per-edge` pattern.
Which mode you run in is set by the `mode` field in the calling workflow
step (`opencode.json.example`); default to `attach` if `mode` is absent.

### Mode: attach

1. Read `schema.example.json` before reading anything else. Note the
   fixed edge shape (`subject`, `predicate`, `object`, plus the three
   receipt fields) and what schema `v2` additionally requires of a
   `caused-by` edge (`impact_scope`).
2. Read the input document (`sample-input.md` by default, or whatever
   `input.document` in the workflow step names) and pull out every write
   request, each with its candidate edge and run metadata.
3. For each candidate edge, check its schema-version-specific fields
   first (e.g. `impact_scope` for `v2`). Refuse it, naming the missing
   field, if one is absent.
4. For each candidate edge that passes step 3, check all three receipt
   fields — `source_doc`, `extraction_run_id`, `schema_version`. If any
   one is missing, empty, or null, refuse the edge outright. Never
   substitute a placeholder or guess a value to fill the gap.
5. Write every candidate edge that passed both checks to `output.json`,
   following `schema.example.json`'s edge shape, with every field —
   receipts included — populated exactly as given.
6. Return, alongside the JSON, the list of candidate edges you refused
   and the specific field each was missing. This kit's write request C
   (missing `extraction_run_id`) is expected to appear in this list.

### Mode: verify

This mode does not trust the refusal list `attach` mode reported — it
independently re-checks the output file against the schema, the same way
the Claude Code `graph-verifier` agent does.

1. Read `schema.example.json` and build the expected edge shape and
   schema-version requirements (same as attach mode step 1).
2. Read `output.json` (or whatever `input.output` in the workflow step
   names). Fail immediately, with that stated as the failure, if it isn't
   valid JSON or is missing an `edges` array.
3. For each written edge, confirm `source_doc`, `extraction_run_id`, and
   `schema_version` are all present and non-empty. Flag any edge missing
   one — this is the core check for this kit.
4. For each written edge with `schema_version: v2`, confirm `impact_scope`
   is present. Flag any that's missing it.
5. Confirm any two written edges sharing the same
   `subject`/`predicate`/`object` are still distinguishable by their
   receipt fields (different `extraction_run_id` and `schema_version`).
   Flag a pair that isn't as a duplicate write.
6. Confirm the write request with no `extraction_run_id` (write request C
   in this kit's scenario) does not appear among the written edges. Flag
   it if it does.
7. If a refusal list from attach mode is available, compare it against
   what this pass independently found. Flag any discrepancy — an edge
   claimed refused that's actually present in `output.json`, or the
   reverse.
8. Return a PASS/FAIL report: PASS only if nothing was flagged in steps
   3-7, otherwise FAIL with every flagged item, the rule it broke, and a
   suggested fix.

## Input

- `schema.example.json` — fixed edge shape and schema-version
  requirements.
- attach mode: the source document (`sample-input.md` by default).
- verify mode: `output.json` (or the path configured), and optionally the
  refusal list attach mode reported.

## Output

- attach mode: `output.json` plus a printed refusal list with reasons.
- verify mode: a PASS/FAIL validation report listing flagged items, the
  rule each one broke, and a suggested fix — matching the report shape in
  the Claude Code `graph-verifier` agent's Example section.

## Configuration

This skill uses `opencode.json.example`'s `workflow.steps` to know which
mode to run and where to find its input/output files:
- `input.document` / `input.schema` — attach mode's source document and
  schema paths.
- `input.output` / `input.schema` — verify mode's output-to-check and
  schema paths.

## Integration

`attach` mode mirrors the Claude Code `attach-receipts` skill's behavior
exactly (same schema, same two-stage check, same refusal on any missing
receipt field). `verify` mode mirrors the Claude Code `graph-verifier`
subagent's behavior exactly (same incomplete-receipt check, same
schema-version-field check, same distinguishability check, same
self-report cross-check). Running both modes back to back over this
kit's `sample-input.md` should produce the same two written edges and the
same refused write request as the Claude Code version.
