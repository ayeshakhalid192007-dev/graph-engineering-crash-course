---
name: conflict-aware-bundle
category: D-subgraph
stage: read
cost: medium
tools: [Claude Code]
core: false
---

# conflict-aware-bundle

## What it does

Assembles a subgraph that deliberately keeps two contradicting claims both
visible side by side, instead of silently picking a winner before the
worker (or the human reviewing its output) ever sees the disagreement.

## Inputs

- A task-scoped subgraph draw.
- Any known unresolved contradictions that touch nodes or edges inside it.

## Outputs

- A bundle that surfaces both sides of a contradiction explicitly, tagged
  as unresolved rather than collapsed into one answer.

## Failure mode if skipped

A worker, or the human reading its output afterward, never learns that two
sources disagreed at all — the subgraph quietly picked one and moved on.

## Link to starter kit

**Kit:** `starters/conflict-aware-bundle/README.md`
