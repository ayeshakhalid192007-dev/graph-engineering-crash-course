---
name: contradiction-detector
category: E-checker
stage: read
cost: medium
tools: [Claude Code]
core: false
---

# contradiction-detector

## What it does

Scans the fact graph for pairs of edges that can't both hold true at the
same time and raises a flag on each pair it finds, independent of whatever
task happens to be reading the graph at that moment.

## Inputs

- The current fact graph, or the portion of it touched by a recent write.

## Outputs

- A list of flagged edge pairs, each marked as mutually contradictory.

## Failure mode if skipped

Contradictions sit inside the graph indefinitely, surfacing only if someone
happens to notice two answers disagree — usually well after a decision has
already been made on one of them.

## Link to starter kit

**Kit:** `starters/contradiction-detector/README.md`
