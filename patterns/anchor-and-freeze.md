---
name: anchor-and-freeze
category: F-governance
stage: governance
cost: low
tools: [Claude Code]
core: false
---

# anchor-and-freeze

## What it does

Wires at least one signal that reaches outside the loop system entirely,
and marks a specific set of facts or rules that no loop is permitted to
rewrite, no matter how consistent its own internal reasoning looks (the
governance safeguard from Step 13).

## Inputs

- A candidate signal source that sits outside the loop system.
- The set of facts or rules proposed as frozen.

## Outputs

- One anchored external check wired into the governance graph.
- A list of frozen nodes flagged as off-limits to every loop.

## Failure mode if skipped

The governance graph can stay perfectly self-consistent while being
collectively wrong about something none of its own loops was ever able to
check independently.

## Link to starter kit

**Kit:** `starters/anchor-and-freeze/README.md`
