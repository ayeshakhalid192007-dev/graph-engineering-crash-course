---
name: query-graph
description: OpenCode equivalent of the Claude Code query-graph skill and graph-verifier agent -- loads schema.sql into graph.db, answers availability/provenance questions, and independently re-checks the result
context: pattern-implementation
---

# query-graph (OpenCode)

OpenCode equivalent of this kit's Claude Code pair
(`.claude/skills/query-graph/SKILL.md` +
`.claude/agents/graph-verifier.md`). OpenCode's config doesn't have a
separate subagent file the way Claude Code does, so this single skill
runs in two modes, driven by `opencode.json.example`'s `workflow.steps`:
**query** (load `graph.db` and answer the question) and **verify** (the
independent recheck). Both modes run the same SQL against the same
`graph.db`, so the two never drift apart on what a "later" edge means or
what counts as grounded.

## Instructions

You are an OpenCode skill implementing the `sqlite-backed-graph` pattern.
Which mode you run in is set by the `mode` field in the calling workflow
step (`opencode.json.example`); default to `query` if `mode` is absent.

### Mode: query

1. If `graph.db` doesn't exist yet at the path `input.database` names,
   build it from `input.schema` (`schema.sql` by default):
   `sqlite3 graph.db < schema.sql`, or the Python equivalent if the CLI
   isn't installed. Leave an existing `graph.db` alone.
2. Run `PRAGMA foreign_keys = ON;` on the connection before any other
   query.
3. Resolve the question from the workflow step, or default to checking
   both `tool-ladder` and `tool-stud-finder`.
4. For each tool, find its latest `borrowed` edge by `id` (`ORDER BY id
   DESC LIMIT 1`). No row means the tool never left its `owns` edge and is
   available. A row means checking for a `returned` edge on the same tool
   from the same `from_id` with a higher `id` — found means available,
   not found means still out with that borrower. Record the specific edge
   id(s) behind the verdict.
5. For the edge id grounding each verdict, look up
   `source_doc`/`extraction_run_id`/`schema_version` directly from the
   `edges` table.
6. Write `output.json` (or the path `output` in the workflow step names)
   with `queries` (SQL text and raw result per query run) and `verdicts`
   (`tool`, `available`, `grounding_edge_id`, `held_by` if not available).

### Mode: verify

This mode does not trust `output.json`'s reported verdicts — it
independently re-derives each one from `graph.db`, the same way the
Claude Code `graph-verifier` agent does.

1. Open `graph.db` (build it from `input.schema` first if missing).
   Run `PRAGMA foreign_keys = ON;`.
2. Run `PRAGMA foreign_key_check;`. Any row returned is a foreign-key
   violation and an automatic FAIL for the run.
3. Read `output.json` (`input.output`). Fail immediately, with that
   stated as the failure, if it isn't valid JSON or is missing `queries`
   or `verdicts`.
4. For each tool in `output.json`'s `verdicts`, independently re-run the
   query-mode step 4 logic against `graph.db` — without reading
   `output.json`'s claimed answer first — and compare. Flag any verdict
   or grounding edge id that doesn't match.
5. For each `grounding_edge_id`, independently re-run the provenance
   lookup and compare `source_doc`/`extraction_run_id`/`schema_version`
   against what `output.json` reported. Flag any mismatch.
6. Confirm every `grounding_edge_id` named in `output.json` actually
   exists in the `edges` table. Flag any that doesn't — a verdict
   grounded in a nonexistent row is a FAIL on its own.
7. Return a PASS/FAIL report: PASS only if nothing was flagged in steps
   2 and 4-6, otherwise FAIL with every flagged item, the independently-
   derived value, and a suggested fix.

## Input

- `input.schema` — path to `schema.sql` (table definitions plus the
  worked example's `INSERT` statements).
- `input.database` — path to `graph.db` (built if it doesn't exist).
- query mode: an optional tool id or edge id to check; defaults to both
  worked-example tools.
- verify mode: `input.output` — the `output.json` to independently check.

## Output

- query mode: `graph.db` plus `output.json` (queries run, verdicts).
- verify mode: a PASS/FAIL validation report listing flagged items, the
  independently-derived value, and a suggested fix — matching the report
  shape in the Claude Code `graph-verifier` agent's Example section.

## Configuration

This skill uses `opencode.json.example`'s `workflow.steps` to know which
mode to run and where to find its input/output files:
- `input.schema` / `input.database` — query mode's schema and database
  paths.
- `input.database` / `input.schema` / `input.output` — verify mode's
  database, schema (for a rebuild if needed), and output-to-check paths.

## Integration

`query` mode mirrors the Claude Code `query-graph` skill's behavior
exactly (same load-once-then-reuse rule, same latest-borrowed-then-check-
returned query, same provenance lookup). `verify` mode mirrors the Claude
Code `graph-verifier` subagent's behavior exactly (same foreign-key
check, same independent re-derivation, same nonexistent-grounding-edge
check). Running both modes back to back over this kit's `schema.sql`
should produce the same two verdicts and the same provenance records as
the Claude Code version.
