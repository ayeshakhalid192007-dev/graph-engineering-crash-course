---
name: bundle-conflicts
description: Assembles a task-scoped bundle that keeps two contradicting claims visible side by side and tagged unresolved, rather than silently picking a winner before the worker or a human reviewer ever sees the disagreement
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# bundle-conflicts

Reads a task-scoped subgraph draw plus a list of known unresolved
contradictions, and produces a bundle where undisputed context passes
through untouched and any contradicting claims stay both present, tagged
as an unresolved pair, with the reason they conflict stated in the
output.

## Instructions

You are a Claude Code skill implementing the `conflict-aware-bundle`
pattern. Follow these steps in order:

1. **Read the full task-scoped draw first**, noting every node in it.
   Default to the draw and known contradiction in this kit's `README.md`
   unless the user gives you a different one.
2. **Read the list of known unresolved contradictions**, noting exactly
   which node ids each one names.
3. **Classify every node in the draw as either "touched by a known
   contradiction" or "undisputed."** A node counts as touched only if a
   known contradiction explicitly names it — do not invent a
   contradiction for two claims that merely differ in detail but weren't
   flagged, and do not treat a node as disputed just because it sits near
   a disputed one in the graph.
4. **Pass undisputed nodes through unchanged.** No conflict tag, no
   alteration to their value or source — the bundle should not make
   settled information look uncertain.
5. **For every contradiction, include every claim it names, never a
   subset.** Do not drop one side because it's labeled "backup," lower-
   confidence, or secondary in some other field — the pattern exists
   specifically so a role label like "primary" can't quietly settle a
   disagreement that hasn't actually been resolved.
6. **Never compute or report a resolved value for a contradiction** —
   no average, no pick-the-primary-source default, no "most likely"
   answer. The bundle's job is to surface the disagreement, not settle
   it.
7. **Tag each contradiction explicitly**, naming the claims involved and
   stating in plain language why they conflict (what they both claim,
   and why those claims can't both be true at once).
8. **Report the bundle in two clearly separated groups**: undisputed
   nodes as-is, then each unresolved-contradiction pair with its tag and
   reason. A reader should be able to tell at a glance which nodes in the
   bundle are settled and which are still actively disputed.

## Input

- A task-scoped subgraph draw (defaults to the draw in this kit's
  `README.md`).
- A list of known unresolved contradictions, each naming the specific
  claim ids it involves.

## Output

- Undisputed nodes, unchanged.
- Each contradiction's full set of claims, tagged
  `unresolved-contradiction` with a stated reason, never collapsed to one
  value.

## Example Usage

```
Use the bundle-conflicts skill on the task-scoped draw and known
contradiction in README.md.

Expected:
  Undisputed:
    storm-event-2026-03-14
    harbor-flood-threshold
  Unresolved-contradiction pair:
    claim-tide-peak-gaugeA ("4.8m at 23:10", Gauge A, primary)
    claim-tide-peak-gaugeB ("5.6m at 23:14", Gauge B, backup, recalibrated
      2026-02-28)
    Reason: both claim to report the single peak-tide value for the same
      storm event and disagree by 0.8m; gauge role alone does not
      resolve which is correct.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that no contradiction in the
output has been reduced to a single value, that every claim a known
contradiction names actually appears in the bundle, and that no
undisputed node picked up a conflict tag it wasn't given.
