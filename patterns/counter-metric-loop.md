---
name: counter-metric-loop
category: F-governance
stage: governance
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# counter-metric-loop

## What it does

Adds a second signal, measured independently by a different party than
whoever runs the optimizing loop, chosen specifically because it's harder
for that loop to game than its primary metric (the governance-wiring move
from Step 12).

## Inputs

- The optimizing loop's primary metric.
- A second metric, sourced independently of the loop being measured.

## Outputs

- A governance edge comparing the two signals and flagging any divergence
  between them.

## Failure mode if skipped

The loop optimizes exactly what it's measured on — including whichever
parts of that metric don't actually reflect the outcome anyone wanted in
the first place.

## Link to starter kit

**Kit:** `starters/counter-metric-loop/README.md`
