---
name: contradiction-detector
category: E-checker
stage: read
cost: medium
tools: [Claude Code]
core: false
---

# contradiction-detector

This kit is the runnable companion to the `contradiction-detector` pattern
specification (`patterns/contradiction-detector.md`). It is an extended
kit — a single Claude Code reference implementation, lighter than the full
multi-tool anatomy the seven core kits carry. See `starters/README.md` for
that distinction.

## What it does

Scans the fact graph for pairs of edges that can't both hold true at the
same time and flags each such pair, whether or not any task currently
reading the graph happens to touch them. It runs on its own schedule, not
triggered by a query — a contradiction sitting in an unvisited corner of
the graph gets found the next time the scan runs, not only when a task
stumbles onto it.

## Inputs

- The current fact graph, or the portion of it touched by a recent write.

## Outputs

- A list of flagged edge pairs, each marked as mutually contradictory.

## Failure mode if skipped

Contradictions sit inside the graph indefinitely, surfacing only if
someone happens to notice two answers disagree — usually well after a
decision has already been made on the strength of one of them.

## Worked scenario

Thistlewood Water Utility, a fictional municipal water provider, keeps a
graph of pipe-segment conditions filed by independent inspection
contractors. In the same week, Ashgrove Inspections files a visual and
acoustic survey rating segment D7 `structurally-sound`, and Millrace NDT
files an ultrasonic thickness test on the same segment rating it
`requires-replacement` — two edges, same subject, same predicate,
directly opposed object values. Neither contractor's report references
the other, so nothing about the intake process would have caught the
clash on its own. The same week's filings also include two pairs that
look superficially similar but aren't contradictions: one segment with
two edges from different contractors on two different predicates
(material versus installation year), and another segment where two
contractors independently filed the same condition reading. See
`README.md` for the full set of filings and how the kit tells the three
cases apart.

## Link to starter kit

**Kit:** `starters/contradiction-detector/README.md`
