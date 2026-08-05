---
name: counter-metric-check
description: OpenCode equivalent of the Claude Code counter-metric-check skill and graph-verifier agent -- compares each period's independently owned counter-metric reading against its recorded ceiling, flags divergence, and independently re-verifies every flag
context: pattern-implementation
---

# counter-metric-check (OpenCode)

Claude Code splits this pattern across two files: a skill that produces
`divergence-report.json`, and a separate `graph-verifier` agent that
double-checks it. OpenCode has no equivalent split, so one skill file
plays both parts, switched by the `mode` value that
`opencode.json.example`'s `workflow.steps` passes in. Both parts read the
identical `governance-graph.example.json`, which is what keeps a
disagreement between the two from ever being explained away as "they were
looking at slightly different data."

## Instructions

You are an OpenCode skill implementing the `counter-metric-loop` pattern.
`mode` in the calling workflow step picks which half of this file runs;
treat a missing `mode` as `check`.

### Mode: check

1. Before touching anything else, load `governance-graph.example.json`
   (`input.graph` if the workflow step overrides it) and parse its
   `nodes` and `edges`.
2. Locate the loop with `role: "primary"` and the loop with
   `role: "counter"`. This kit ships `pr-approval-loop` and
   `release-pipeline`, respectively.
3. Walk the primary loop's outgoing edges and check that none of them
   reaches the counter loop, the threshold node, or a period through a
   predicate meaning `reads`, `consumes`, or `receives`. Finding one
   means the isolation this pattern depends on is already gone —
   report that and don't proceed to the comparisons below, since
   nothing they'd produce would mean anything at that point.
4. Get the ceiling by following the counter loop's `bound-by` edge to
   its threshold node and reading `ceiling` and `metric` there.
5. Take the period list from `input.period_id` if the workflow step sets
   one; otherwise use every `type: "period"` node in the graph (four of
   them ship with this kit: `week-14` through `week-17`).
6. For each period, get both loops' numbers from their own `reported`
   edges into that period — never a guess, never an average. A period
   where either loop lacks a `reported` edge comes back UNVERIFIABLE
   instead.
7. The counter reading is the only thing that decides the verdict:
   above the ceiling is FLAGGED, at or under it is CLEAN. Keep the
   primary reading in the output for context, but don't let it swing a
   verdict either way.
8. Build one `flags-divergence` governance edge per FLAGGED period —
   `subject` the counter loop, `object` the primary loop, plus
   `period`, `primary_reading`, `counter_reading`, `metric`, `ceiling`.
9. Write `divergence-report.json` (`input.output` if set): an
   `isolation_check` object, a `periods` array (`period_id`,
   `primary_reading`, `counter_reading`, `ceiling`, `verdict`, and a
   `citation` — the counter loop's exact `reported` edge for a FLAGGED
   period, `null` elsewhere), and `new_governance_edges` from step 8.
10. Alongside the file, report how many periods landed CLEAN, FLAGGED,
    or UNVERIFIABLE, and which reading pair triggered each FLAGGED one.

### Mode: verify

Nothing from the `check` run is taken on faith here — every reading gets
pulled again straight from the graph, the same discipline the Claude
Code `graph-verifier` agent applies.

1. Load `governance-graph.example.json` (`input.graph`) fresh, parsing
   `nodes` and `edges` independently of anything the check run said
   about them.
2. Load `divergence-report.json` (`input.report`). A file that isn't
   valid JSON, or is missing `isolation_check`, `periods`, or a required
   field on any period entry, fails right here — say so and stop.
3. Redo the isolation scan on the primary loop's outgoing edges
   yourself. A mismatch against the report's `isolation_check.passed`
   gets flagged.
4. Confirm every `period_id` names a real period node in the graph;
   flag whichever ones don't.
5. Pull each period's readings again from the graph's own `reported`
   edges and compare them to what the entry restated. A restated number
   that doesn't match what the graph actually holds is a flag, however
   small the gap.
6. Re-derive the ceiling from the threshold node on your own, and flag
   any entry whose `ceiling` disagrees.
7. Flag any entry sitting on the wrong side of the above/at-or-under
   comparison against its own re-pulled counter reading — the primary
   reading never factors into this check.
8. For every period that should be FLAGGED, confirm
   `new_governance_edges` contains a matching edge — same subject,
   object, readings, metric, ceiling. Flag it if the edge is missing or
   any field is off.
9. Compare against the shipped scenario's known answers: `week-14`,
   `week-15`, and `week-17` are CLEAN; `week-16` is FLAGGED at a counter
   reading of `0.34` against a `0.20` ceiling. A different result on
   unmodified sample data is a flag by itself.
10. Return PASS if steps 3-9 found nothing; otherwise FAIL, with every
    flag, the rule it broke, and how to fix it.

## Input

- `governance-graph.example.json` — the populated governance graph.
- check mode: a period id, or nothing (`input.period_id`, defaults to
  every period node).
- verify mode: `divergence-report.json` (or the path configured) to
  check.

## Output

- check mode: `divergence-report.json` plus a printed verdict-bucket
  summary.
- verify mode: a PASS/FAIL report — flagged items, the rule broken, a
  fix for each — in the same shape as the Claude Code `graph-verifier`
  agent's Example section.

## Configuration

`opencode.json.example`'s `workflow.steps` supplies the mode and the file
paths:
- `input.graph` / `input.period_id` for check mode's graph and (optional)
  single period.
- `input.report` / `input.graph` for verify mode's report-to-check and
  the graph to check it against.

## Integration

Running `check` here against this kit's shipped
`governance-graph.example.json` should land on the same four verdicts as
the Claude Code skill — CLEAN, CLEAN, FLAGGED, CLEAN, week-14 through
week-17 — because both read the same edges under the same rules. Running
`verify` afterward should agree with what `graph-verifier` would say
about the same report, for the same reason: neither trusts a number it
hasn't pulled from the graph itself.
