---
name: budget-capped-subgraph
category: D-subgraph
stage: read
cost: low
tools: [Claude Code]
core: false
---

# budget-capped-subgraph

## What it does

Builds a task-scoped subgraph the same way `task-scoped-retrieval` does,
but enforces a hard ceiling on node count, edge count, or token count
before that subgraph is handed to a worker.

## Inputs

- A candidate task-scoped subgraph.
- A budget ceiling expressed in nodes, edges, or tokens.

## Outputs

- A subgraph trimmed to fit inside the budget, with the rule used to trim
  it recorded alongside it.

## Failure mode if skipped

The subgraph grows without any limit as the underlying graph grows, so what
started cheap quietly becomes an expensive context to build and to hand off
— with no one having decided that was an acceptable tradeoff.

## Link to starter kit

**Kit:** `starters/budget-capped-subgraph/README.md`
