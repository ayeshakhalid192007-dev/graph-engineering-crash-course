---
name: merge-aliases
description: OpenCode equivalent of the Claude Code merge-aliases skill and graph-verifier agent — folds surface names for one system into a canonical entity, keeping every original mention retrievable, and verifies no mention was lost
context: pattern-implementation
---

# merge-aliases (OpenCode)

OpenCode equivalent of this kit's Claude Code pair
(`.claude/skills/merge-aliases/SKILL.md` +
`.claude/agents/graph-verifier.md`). OpenCode's config doesn't have a
separate subagent file the way Claude Code does, so this single skill runs
in two modes, driven by `opencode.json.example`'s `workflow.steps`:
**merge** (the merging behavior) and **verify** (the independent recheck).
Both modes read the same `schema.example.json`, so the two never drift
apart on what counts as an acceptable merge.

## Instructions

You are an OpenCode skill implementing the `alias-merge-with-trail`
pattern. Which mode you run in is set by the `mode` field in the calling
workflow step (`opencode.json.example`); default to `merge` if `mode` is
absent.

### Mode: merge

1. Read `schema.example.json` before reading anything else. Note the
   `Service` entity shape (`canonical_name`, `merge_reason`) and the
   mention record shape (`surface`, `source`, `retrievable`).
2. Read the input document (`sample-input.md` by default, or whatever
   `input.document` in the workflow step names) and pull out every
   surface string used for a system, its source section, and any
   timestamp or reference number attached to it.
3. Group candidate surface strings that might name the same system. Merge
   a group only when its sources share a concrete, checkable link — a
   shared timestamp window, an explicit cross-reference, a shared ticket
   or deployment identifier. Never merge on name resemblance alone.
4. For a group with real evidence: create one canonical `Service` entity,
   state the concrete evidence in `merge_reason`, and add one `mentions`
   entry per original surface string, each with its own `source` and
   `retrievable: true`. Keep every original surface string as its own
   entry — never overwrite or collapse them into the canonical name.
5. For a group with no real evidence (including this kit's decoy pair):
   leave the mentions unmerged and report the pair by name with the
   reason nothing was combined.
6. Write survivors to `output.json` following `schema.example.json`'s
   `entities`/`aliases` shape, and return the list of groups you chose not
   to merge, with reasons.

### Mode: verify

This mode does not trust the skip list `merge` mode reported — it
independently re-checks the output file against the schema, the same way
the Claude Code `graph-verifier` agent does.

1. Read `schema.example.json` and build the expected shapes (same as merge
   mode step 1).
2. Read `output.json` (or whatever `input.output` in the workflow step
   names). Fail immediately, with that stated as the failure, if it isn't
   valid JSON or is missing `entities`/`aliases` arrays.
3. For each alias group, confirm every surface string that should have
   fed into it is present as its own `mentions` entry with
   `retrievable: true`. Flag a group if a known surface string is missing
   or was collapsed into another entry.
4. Flag any `merge_reason` that only claims the names look or sound
   alike, rather than naming a concrete, checkable fact.
5. Flag any canonical entity that covers a pair with no concrete link
   between its sources (an over-merge) — for this kit's scenario, that
   means checking whether the decoy pair was wrongly folded together.
6. If a skip list from merge mode is available, compare it against what
   this pass independently found. Flag any discrepancy — a pair claimed
   skipped that's actually merged in `output.json`, or the reverse.
7. Return a PASS/FAIL report: PASS only if nothing was flagged in steps
   3-6, otherwise FAIL with every flagged item, the rule it broke, and a
   suggested fix.

## Input

- `schema.example.json` — fixed entity and mention-record shapes.
- merge mode: the source document (`sample-input.md` by default).
- verify mode: `output.json` (or the path configured), and optionally the
  skip list merge mode reported.

## Output

- merge mode: `output.json` plus a printed list of pairs deliberately left
  unmerged, with reasons.
- verify mode: a PASS/FAIL validation report listing flagged items, the
  rule each one broke, and a suggested fix — matching the report shape in
  the Claude Code `graph-verifier` agent's Example section.

## Configuration

This skill uses `opencode.json.example`'s `workflow.steps` to know which
mode to run and where to find its input/output files:
- `input.document` / `input.schema` — merge mode's source document and
  schema paths.
- `input.output` / `input.schema` — verify mode's output-to-check and
  schema paths.

## Integration

`merge` mode mirrors the Claude Code `merge-aliases` skill's behavior
exactly (same schema, same evidence-first filter, same refusal to merge on
name resemblance alone). `verify` mode mirrors the Claude Code
`graph-verifier` subagent's behavior exactly (same lost-mention check,
same weak-reason check, same over-merge check, same self-report
cross-check). Running both modes back to back over this kit's
`sample-input.md` should produce the same canonical entity, the same two
retained mentions, and the same skipped decoy pair as the Claude Code
version.
