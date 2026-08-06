---
name: extract-facts
description: OpenCode equivalent of the Claude Code extract-facts skill and graph-verifier agent — extracts and verifies Service/Incident/Cause facts from an incident report against a fixed schema
context: pattern-implementation
---

# extract-facts (OpenCode)

OpenCode equivalent of this kit's Claude Code pair
(`.claude/skills/extract-facts/SKILL.md` +
`.claude/agents/graph-verifier.md`). OpenCode's config doesn't have a
separate subagent file the way Claude Code does, so this single skill
runs in two modes, driven by `opencode.json.example`'s `workflow.steps`:
**extract** (Steps 4's behavior) and **verify** (Step 5's behavior). Both
modes read the same `schema.example.json`, so the two never drift apart
on what "allowed" means.

## Instructions

You are an OpenCode skill implementing the `document-to-facts` pattern.
Which mode you run in is set by the `mode` field in the calling workflow
step (`opencode.json.example`); default to `extract` if `mode` is absent.

### Mode: extract

1. Read `schema.example.json` before reading anything else. Note the
   allowed entity types (`Service`, `Incident`, `Cause`) with their
   properties, and the allowed relationship types (`caused-by`:
   `Incident` -> `Cause`, `affected`: `Incident` -> `Service`).
2. Read the input document (`sample-input.md` by default, or whatever
   `input.document` in the workflow step names).
3. Draft candidate entities and relationships from the document — over-
   collect rather than under-collect at this stage.
4. Filter every candidate against the schema from step 1: keep an entity
   only if its type and properties are on the allowed list; keep a
   relationship only if its type and its `from`/`to` endpoint types match
   the schema exactly. Never rename a candidate's type to force a match.
5. Write survivors to `output.json` as `entities` and `relationships`
   arrays matching `schema.example.json`'s shape, tagging every
   relationship with a `source_document` property.
6. Return, alongside the JSON, the list of candidates you dropped and why
   (unknown type, or a `from`/`to` mismatch). The document's person name
   and Slack channel mention are expected to appear in this drop list.

### Mode: verify

This mode does not trust the drop list `extract` mode reported — it
independently re-checks the output file against the schema, the same way
the Claude Code `graph-verifier` agent does.

1. Read `schema.example.json` and build the allowed set (same as extract
   mode step 1).
2. Read `output.json` (or whatever `input.output` in the workflow step
   names). Fail immediately, with that stated as the failure, if it isn't
   valid JSON or is missing `entities`/`relationships` arrays.
3. Check every entity: flag any whose `type` isn't one of the three
   allowed types, or whose properties include one the schema doesn't list
   for that type.
4. Check every relationship: flag any whose `type` isn't `caused-by` or
   `affected`, whose `from`/`to` endpoint types don't match the schema for
   that relationship type, or that's missing `source_document`.
5. If a drop list from extract mode is available, compare it against what
   this pass independently found. Flag any discrepancy — something
   claimed dropped but actually present in `output.json`, or the reverse.
6. Return a PASS/FAIL report: PASS only if nothing was flagged in steps
   3-5, otherwise FAIL with every flagged item, the specific rule it
   broke, and a suggested fix.

## Input

- `schema.example.json` — fixed entity/relationship types and properties.
- extract mode: the source document (`sample-input.md` by default).
- verify mode: `output.json` (or the path configured), and optionally the
  drop list extract mode reported.

## Output

- extract mode: `output.json` plus a printed drop list with reasons.
- verify mode: a PASS/FAIL validation report listing flagged items,
  the rule each one broke, and a suggested fix — matching the report
  shape in the Claude Code `graph-verifier` agent's Example section.

## Configuration

This skill uses `opencode.json.example`'s `workflow.steps` to know which
mode to run and where to find its input/output files:
- `input.document` / `input.schema` — extract mode's source document and
  schema paths.
- `input.output` / `input.schema` — verify mode's output-to-check and
  schema paths.

## Integration

`extract` mode mirrors the Claude Code `extract-facts` skill's behavior
exactly (same schema, same filter-then-report logic). `verify` mode
mirrors the Claude Code `graph-verifier` subagent's behavior exactly
(same independent re-check, same self-report cross-check). Running both
modes back to back over this kit's `sample-input.md` should produce the
same surviving facts and the same flagged discrepancies as the Claude
Code version.
