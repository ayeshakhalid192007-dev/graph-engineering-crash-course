---
name: arbitration-edge
category: F-governance
stage: governance
cost: low
tools: [Claude Code]
core: false
---

# arbitration-edge

## What it does

Defines a rule — or a separate loop whose only job is this — that decides
which of two loops wins when both act on the same resource at the same
time, instead of leaving the outcome to whichever write lands last.

## Inputs

- A conflicting pair of proposed writes from two loops touching the same
  node or edge.

## Outputs

- A single accepted write.
- A record of which loop's write was rejected, and why.

## Failure mode if skipped

Two loops that are each individually reasonable overwrite each other's work
with neither one aware a collision ever happened.

## Link to starter kit

**Kit:** `starters/arbitration-edge/README.md`
