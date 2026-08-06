---
name: counter-metric-check
description: Compares a watched loop's headline reading against an independently owned counter-metric reading for each period in a governance graph, and produces a governance edge for every period where the counter-metric crosses its recorded ceiling
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# counter-metric-check

Whatever the watched loop's own headline number did in a given period
plays no part in this skill's decision for that period. The only input
that matters is the second, independently owned reading and where it
sits relative to its ceiling.

## Instructions

You are a Claude Code skill implementing the `counter-metric-loop`
pattern. Work through these steps in order:

1. **Load the governance graph before anything else.** Open
   `governance-graph.example.json` (or the file the user names) and
   parse `nodes` and `edges`.
2. **Locate the two loop nodes.** One carries `role: "primary"` (the
   loop under watch); the other carries `role: "counter"` (the
   independent signal). In this kit's shipped graph those are
   `pr-approval-loop` and `release-pipeline`.
3. **Check isolation before doing anything that depends on it holding.**
   Walk every edge whose `subject` is the primary loop and confirm none
   of them reaches the counter loop, the threshold node, or a period
   under a predicate that would let the primary loop read the counter
   reading (`reads`, `consumes`, `receives`, or anything with that
   meaning). If one turns up, stop here and report it: a counter-metric
   the watched loop can see has stopped being a counter-metric, and
   nothing downstream of that fact is worth computing.
4. **Read the ceiling.** Follow the counter loop's `bound-by` edge to
   its threshold node and note the `ceiling` and `metric` fields there.
5. **Pick the periods to evaluate.** Absent a specific period from the
   user, use every `type: "period"` node in the graph — four in this
   kit's shipped scenario, `week-14` through `week-17`.
6. **Take both readings straight off the graph's `reported` edges** —
   the primary loop's edge into a period, and the counter loop's
   separate edge into that same period. Neither reading is something to
   estimate or infer; a period lacking either edge is UNVERIFIABLE, full
   stop.
7. **Let the counter reading alone decide the verdict.** Above the
   ceiling means FLAGGED. At or below it means CLEAN. Keep the primary
   reading in the record for context, but it never tips a verdict either
   way — a loud week on the headline number is not itself proof of
   anything, in either direction.
8. **Produce a governance edge for each FLAGGED period.** Fields:
   `subject` (counter loop), `predicate: "flags-divergence"`, `object`
   (primary loop), `period`, `primary_reading`, `counter_reading`,
   `metric`, `ceiling`. CLEAN and UNVERIFIABLE periods get no edge.
9. **Write `divergence-report.json`** (or wherever the user asked) at
   this kit's root, holding: `isolation_check` (the step-3 result and its
   detail), a `periods` array (one entry per period —`period_id`,
   `primary_reading`, `counter_reading`, `ceiling`, `verdict`, and
   `citation`, which is the counter loop's exact `reported` edge on a
   FLAGGED period and `null` everywhere else), and
   `new_governance_edges` holding step 8's output.
10. **Summarize on the way out.** State the CLEAN/FLAGGED/UNVERIFIABLE
    counts and, for every FLAGGED period, the reading pair that
    triggered it.

## Input

- `governance-graph.example.json` (or another file the user names) — the
  populated governance graph holding both loops' readings.
- A period id, or nothing (defaults to checking every period node in the
  graph).

## Output

- `divergence-report.json` (or user-specified path) — the isolation
  check, one verdict per period, and any new governance edges the run
  produced.
- A printed summary of how many periods landed in each verdict bucket.

## Example Usage

```
Use the counter-metric-check skill on governance-graph.example.json.

Expected verdicts (4 of 4 periods checked):
  week-14 -> CLEAN   (revert rate 0.08, ceiling 0.20)
  week-15 -> CLEAN   (revert rate 0.13, ceiling 0.20)
  week-16 -> FLAGGED (revert rate 0.34, ceiling 0.20)
    primary reading that week: 91 PRs approved, well above the ~55-65 baseline
  week-17 -> CLEAN   (revert rate 0.10, ceiling 0.20)
```

## Validation

`.claude/agents/graph-verifier.md` treats every number above as
unverified until it's re-derived. It re-pulls both readings for each
period straight from `governance-graph.example.json` and checks them
against the ceiling on its own, rather than taking
`divergence-report.json`'s account of what happened at face value.
