---
name: confidence-scored-dedup
category: B-resolution
stage: write
cost: medium
tools: [Claude Code]
core: false
---

# confidence-scored-dedup

## What it does

Scores every candidate merge for confidence, auto-merging only the ones
that clear a set threshold and routing the rest to a review queue, instead
of treating every candidate the same way.

## Inputs

- A set of candidate merge pairs.
- A similarity signal (name distance, embedding proximity, shared
  attributes) that produces a confidence score per pair.

## Outputs

- A smaller set of entities merged automatically, above threshold.
- A review queue of below-threshold candidates awaiting a human or a
  second pass.

## Failure mode if skipped

Without scoring, a team either merges every candidate indiscriminately —
correctness be damned — or lets a growing backlog of undecided duplicates
pile up that nobody ever works through.

## Link to starter kit

**Kit:** `starters/confidence-scored-dedup/README.md`
