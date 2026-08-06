---
name: postgres-backed-graph
category: G-storage
stage: storage
cost: medium
tools: [Claude Code]
core: false
---

# postgres-backed-graph

This kit is the runnable companion to the `postgres-backed-graph` pattern
specification (`patterns/postgres-backed-graph.md`). It is an extended
kit — a single Claude Code reference implementation, lighter than the
full multi-tool anatomy the seven core kits carry. See
`starters/README.md` for that distinction.

## What it does

Lays the graph out as adjacency-list tables inside Postgres — a `nodes`
table and an `edges` table — and wraps every write to a shared edge in a
transaction with a version check, so two writers touching the same edge
at nearly the same moment serialize into two well-ordered commits
instead of racing to overwrite each other.

## Inputs

- The node and edge schema, laid out as relational tables.
- The concurrent write load the graph needs to support.

## Outputs

- A transactionally consistent graph store, shared safely across
  multiple concurrent writers.

## Failure mode if skipped

Two writers touching a file-based graph at nearly the same instant can
each read the same starting state, each compute their own new version of
it, and each save their own copy — with no lock to have stopped either
one and no transaction to roll either one back to. Whichever save lands
last simply overwrites the other, and the write that got overwritten
never existed as far as anyone reading the graph afterward can tell.

## Worked scenario

Copperlow Analytics, a fictional SaaS observability company, already runs
Postgres for its feature-flag rollout graph. At 09:14:03, an automated
rollout controller reads the current `status` edge for the
`checkout-v2-flag` node and starts writing an advance, from
`rollout-45pct` to `rollout-55pct`. Forty milliseconds later, an
incident-response bot — triggered by an error-rate alert that fired a
moment earlier — reads that same starting edge and starts writing a
rollback, straight to `rolled-back`. Both writers read the identical
starting state before either one had committed. Without a transaction
and a version check tying each write to the exact row state it was
computed against, whichever writer's save lands second would silently
clobber the first — and if that second writer happens to be the rollout
controller, the incident bot's rollback disappears entirely, with
nothing in the graph to show a rollback was ever attempted. See
`README.md` for the full sequence and how a version-checked transaction
keeps both writes from being lost.

## Link to starter kit

**Kit:** `starters/postgres-backed-graph/README.md`
