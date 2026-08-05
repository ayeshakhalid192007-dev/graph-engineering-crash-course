---
name: scan-contradictions
description: Scans the fact graph for pairs of edges that cannot both hold true at once and flags each such pair, running as its own standing pass rather than as part of whatever task happens to be reading the graph
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# scan-contradictions

Reads every edge in the graph (or the portion touched by a recent write),
groups edges by subject and predicate, and checks each group for object
values that can't all be true of the same subject at once — flagging
those pairs and only those pairs.

## Instructions

You are a Claude Code skill implementing the `contradiction-detector`
pattern. Follow these steps in order:

1. **Read the full set of edges to scan.** Default to the filings in this
   kit's `README.md` unless the user gives you a different graph or
   subset. Do not scope the scan to any particular task's needs — this
   skill runs standalone, independent of what any task currently wants
   from the graph.
2. **Group edges by (subject, predicate) pair.** Two edges can only
   possibly contradict each other if they name the same subject and the
   same predicate — an edge about a segment's `material` and an edge
   about the same segment's `installation-year` are never in tension with
   each other, no matter how different their values look, because they
   aren't asserting anything about the same fact.
3. **Within each group, compare the object values pairwise.** For each
   pair of edges sharing a subject and predicate:
   - If the object values are the same (or state-compatible — e.g., two
     independent readings that agree), this is **corroboration**, not a
     contradiction. Do not flag it.
   - If the object values assert mutually exclusive states of the same
     subject at the same predicate (a segment cannot be both
     `structurally-sound` and `requires-replacement` at once), this is a
     **contradiction**. Flag the pair.
4. **Do not infer contradictions across different predicates or
   different subjects**, even when the two edges come from the same
   source document or the same contractor. Same-source proximity is not
   evidence of contradiction — only a shared subject and predicate with
   opposed values is.
5. **Do not resolve the contradiction.** This skill's job stops at
   flagging the pair — it never decides which reading is correct, drops
   either edge, or picks a "more trustworthy" source. That decision
   belongs to whatever process consumes the flag.
6. **Report every flagged pair** with both edges' full detail (subject,
   predicate, object, source), and separately confirm which groups were
   checked and found to corroborate rather than conflict, so a reader can
   tell "checked, no contradiction" apart from "never checked."

## Input

- The graph's edges to scan (defaults to the filings in this kit's
  `README.md`).

## Output

- A list of flagged edge pairs, each marked mutually contradictory, with
  both edges' full detail.
- For groups checked and found not to conflict, an explicit note of that
  outcome (corroboration or unrelated predicate), not silence.

## Example Usage

```
Use the scan-contradictions skill on the pipe-segment filings in README.md.

Expected:
  CONTRADICTION:
    pipe-segment-D7 --condition--> structurally-sound (Ashgrove Inspections, Mon)
    pipe-segment-D7 --condition--> requires-replacement (Millrace NDT, Wed)
    Reason: same subject, same predicate, mutually exclusive values.

  Checked, not flagged:
    pipe-segment-E2: material (Ashgrove) and installation-year (Millrace)
      -- different predicates, not comparable.
    pipe-segment-F9: condition=minor-corrosion-noted (Ashgrove) and
      condition=minor-corrosion-noted (Millrace) -- same value, corroboration.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check two things: that no flagged
pair actually shares only a source document rather than a genuine
subject-and-predicate match, and that every group you compared shows up
in the report as either flagged or explicitly cleared — never omitted.
