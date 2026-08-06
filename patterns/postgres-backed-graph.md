---
name: postgres-backed-graph
category: G-storage
stage: storage
cost: medium
tools: [Claude Code]
core: false
---

# postgres-backed-graph

## What it does

Represents the graph as adjacency-list tables inside Postgres, aimed at a
team already operating Postgres that needs several writers touching the
graph at once with real transaction guarantees.

## Inputs

- The node and edge schema, laid out as relational tables.
- The concurrent write load the graph needs to support.

## Outputs

- A transactionally consistent graph store, shared safely across multiple
  concurrent writers.

## Failure mode if skipped

Multiple writers touching a file-based graph at the same time corrupt it,
with no transaction to roll back to and no lock to have stopped them.

## Link to starter kit

**Kit:** `starters/postgres-backed-graph/README.md`
