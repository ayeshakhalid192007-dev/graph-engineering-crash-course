---
name: neo4j-at-scale
category: G-storage
stage: storage
cost: high
tools: [Claude Code]
core: false
---

# neo4j-at-scale

## What it does

Hands multi-hop traversal queries to a dedicated graph database once
relational adjacency tables start struggling to answer them at the graph's
current scale.

## Inputs

- The graph's existing schema, migrated into native graph storage.
- The multi-hop traversal queries the graph needs to answer.

## Outputs

- Multi-hop query results returned at a latency relational joins can no
  longer match.

## Failure mode if skipped

Multi-hop queries against relational tables get slower and more convoluted
to write as the graph grows, until a query that used to take one join takes
five and still times out.

## Link to starter kit

**Kit:** `starters/neo4j-at-scale/README.md`
