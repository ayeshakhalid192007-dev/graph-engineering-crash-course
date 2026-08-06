---
name: sqlite-backed-graph
category: G-storage
stage: storage
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# sqlite-backed-graph

## What it does

Stores nodes and edges as two related SQLite tables joined by foreign keys
— a storage shape sized for one team working on one machine, not a
distributed system.

## Inputs

- The node and edge schema, expressed as two table definitions.

## Outputs

- A single queryable local database file holding the entire graph.

## Failure mode if skipped

A team reaches for a distributed graph database and takes on its
operational overhead — backups, networking, a service to keep running —
before the scale of the graph ever justified paying that cost.

## Link to starter kit

**Kit:** `starters/sqlite-backed-graph/README.md`
