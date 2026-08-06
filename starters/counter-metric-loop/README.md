# counter-metric-loop Starter Kit

A runnable starter kit for the **counter-metric-loop** pattern. Two loops
in a fictional software company, Thornfield Systems, each keep their own
record of the same four weeks — one loop's headline dashboard number, and
a second, separately owned loop's independent reading of how much of that
headline actually held up. The verdict this kit produces for each week
comes entirely from where the second number sits against its ceiling; the
first number rides along for context and decides nothing. Thornfield
Systems and its pull-request-approval loop are invented for this kit —
they are not based on any real company, codebase, or incident.

Earlier kits in this series write facts into a graph or query one for a
single grounded answer. This one does neither — it's a governance-stage
kit, and what it reads is `governance-graph.example.json`: a small, fixed
graph holding two loops' recorded numbers across four weeks plus the
threshold that separates an ordinary week from a flagged one. There's no
`schema.example.json` here for the same reason the read-path kits ship no
schema of their own — see `starters/README.md`'s note on kit anatomy.

## The scenario

`pr-approval-loop` waves a pull request through once its checks pass and
queues it for the next release train. The review-bot team that built it
watches one number: approvals per week. Deploying whatever gets approved
is a different loop entirely, `release-pipeline`, owned by release
engineering — a separate team that tracks its own number, the share of
merges it has to roll back inside 72 hours, and has no channel for
handing that number to `pr-approval-loop`.

Three of this kit's four sample weeks look unremarkable on both counts:
approvals in the fifties or sixties, reverts under one in ten. Week 16
breaks that pattern twice at once — approvals jump to 91, and the revert
share jumps with them, past one in three. Looking only at the approval
count, week 16 reads as the loop's best week on record. Looking at what
release engineering was tracking the entire time, it's the one week that
actually crossed the line.

`counter-metric-check` never lets the approval count argue its case. It
pulls week 16's revert-rate reading straight off `release-pipeline`'s own
recorded edge, checks it against the ceiling release engineering set
ahead of time, and stops there. Three weeks clear that check. Week 16
gets a governance edge naming both loops, both readings, and the
threshold it crossed.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- No external services or API keys — the whole kit runs against the one
  local file described below.

## Quick Start

1. Review `PATTERN.md` for what this pattern is solving and what breaks
   without it.
2. Open `governance-graph.example.json`. Note the `role` field on each
   loop node, the four period nodes, the `reported` edges that carry
   each week's actual number, and the `revert-ceiling` threshold node.
3. Run the kit using whichever tool-specific instructions below apply.
4. Open `divergence-report.json` afterward and check it against
   "Expected Output" — specifically, which week got flagged and what it
   was flagged with.

### Claude Code

1. Load `.claude/skills/counter-metric-check/SKILL.md`.
2. Tell it: "Use the counter-metric-check skill on
   governance-graph.example.json." Leaving out a period id means it
   checks all four shipped weeks.
3. It writes `divergence-report.json` and prints each week's verdict,
   plus the reading pair behind any FLAGGED week.
4. Point `.claude/agents/graph-verifier.md` at `divergence-report.json`
   and `governance-graph.example.json`. It re-derives every week's
   verdict from the graph on its own rather than taking the check run's
   summary as given.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json`, or run
   OpenCode against it directly.
2. Run the `check` step. It calls
   `opencode/skills/counter-metric-check/SKILL.md` in check mode over
   `governance-graph.example.json` and writes `divergence-report.json`.
3. Run the `verify` step. Same skill file, verify mode this time,
   checking `divergence-report.json` independently and reporting
   PASS/FAIL.

## Expected Output

Running the kit against the shipped graph should leave
`divergence-report.json` looking like this:

- **`isolation_check.passed: true`.** Nothing in the graph gives
  `pr-approval-loop` a path to `release-pipeline`'s readings or the
  threshold node.
- **`week-14` → CLEAN.** Revert rate 0.08, ceiling 0.20. `citation` is
  `null`.
- **`week-15` → CLEAN.** Revert rate 0.13, ceiling 0.20. `citation` is
  `null`.
- **`week-16` → FLAGGED.** Revert rate 0.34, ceiling 0.20. That week's
  approval count (91) is recorded for context, but it isn't what earned
  the flag — the revert-rate edge is. `citation` names that edge
  precisely, and `new_governance_edges` carries a `flags-divergence`
  edge from `release-pipeline` to `pr-approval-loop` scoped to `week-16`.
- **`week-17` → CLEAN.** Revert rate 0.10, ceiling 0.20. `citation` is
  `null`.

### Checking the verdicts

Nothing here should be defended by describing how the approval count
looked that week — only by pointing at one `reported` edge and one
ceiling. Confirm that's actually what happened:

- `week-16`'s `citation` should read exactly `{"subject":
  "release-pipeline", "predicate": "reported", "object": "week-16",
  "value": 0.34}` — the real edge, not a summary of it and not a
  different week.
- `week-14`, `week-15`, and `week-17` all carry `verdict: "CLEAN"` and
  `citation: null`.
- `isolation_check.passed` reads `true`, and no verdict shifted because
  a week's approval count looked high or low.

A `week-16` that comes back CLEAN means something read the approval
spike as reassurance in place of checking the number that was actually
supposed to catch it — the exact mistake this kit is built to surface,
and the verifier below should call it out.

## Modifying the Example

Adapting this kit to a scenario of your own:

1. Swap in your own graph in place of `governance-graph.example.json`.
   Any pair of loops works as long as you keep the `role: "primary"` /
   `role: "counter"` pair, a `bound-by` edge to a threshold node, and a
   `reported` edge per loop per period.
2. Add or edit period nodes and their `reported` edges to try new
   numbers — the comparison logic has nothing hardcoded about
   `revert_rate_72h` or Thornfield Systems in it.
3. Re-run the skill and make sure every FLAGGED period still cites a
   real edge, and the verifier still passes.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `governance-graph.example.json` — the fixed Thornfield Systems graph
  this kit reads (stands in for `schema.example.json` in this
  governance-stage kit — see `starters/README.md`'s anatomy note).
- `.claude/skills/counter-metric-check/SKILL.md` — Claude Code
  compare-and-flag skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/counter-metric-check/SKILL.md` — OpenCode skill
  covering both checking and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `week-16` comes back CLEAN in `divergence-report.json`. | The approval-count spike got treated as evidence instead of context — recheck that `SKILL.md` step 7 is deciding from the counter reading alone. |
| A FLAGGED entry's `citation` is `null`, or names a different week. | Step 8 got the verdict right but didn't cite the matching edge, or cited the wrong one. Every FLAGGED period needs its exact `reported` edge named, not just an assertion that the ceiling was crossed. |
| `isolation_check.passed` reads `true` despite an edge from `pr-approval-loop` reaching `release-pipeline`'s readings. | Step 3's scan either didn't run against the primary loop's outgoing edges, or only matched the literal word `reads` and missed an equivalent predicate. |
| `divergence-report.json` has an entry for a period missing one loop's `reported` edge. | That period should have come back UNVERIFIABLE in step 6, not been given an invented reading. |
| The verifier's independently re-pulled readings don't match what `divergence-report.json` claims. | That's the verifier working as intended — the check run's restated numbers drifted from the graph's own edges. Treat `divergence-report.json` as unproven until that gap is closed. |

## Next Steps

- Read `patterns/counter-metric-loop.md` in the course repo for this
  pattern's general statement, apart from this kit's specific scenario.
- This is one of seven core kits — `starters/README.md` explains how it
  fits alongside the other six and the sixteen extended kits.
