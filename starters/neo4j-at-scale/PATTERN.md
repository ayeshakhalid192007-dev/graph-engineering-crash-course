---
name: neo4j-at-scale
category: G-storage
stage: storage
cost: high
tools: [Claude Code]
core: false
---

# neo4j-at-scale

This kit is the runnable companion to the `neo4j-at-scale` pattern
specification (`patterns/neo4j-at-scale.md`). It is an extended kit — a
single Claude Code reference implementation, lighter than the full
multi-tool anatomy the seven core kits carry. See `starters/README.md`
for that distinction.

## What it does

Hands a multi-hop traversal query to native graph storage once
relational adjacency tables start straining to answer it — replacing a
recursive join that grows one join level deeper for every extra hop with
a single variable-length path match whose cost doesn't scale with depth
the same way.

## Inputs

- The graph's existing schema, migrated into native graph storage.
- The multi-hop traversal queries the graph needs to answer.

## Outputs

- Multi-hop query results returned at a latency relational joins can no
  longer match.

## Failure mode if skipped

A multi-hop query against relational adjacency tables gets slower and
more convoluted to express as the graph grows — a trace that used to
resolve in one join needs a recursive common-table expression at five or
six join levels to reach the same answer, and at real scale it starts
timing out before it finishes, well before anyone gets to read the
result it was supposed to return.

## Worked scenario

Amberlynn Genomics Consortium, a fictional multi-lab research
collaborative, tracks reagent lots, the sequencing runs that consume
them, and the experiment results those runs produce, across several
hundred thousand run records built up over years. When reagent lot
RL-2291 is found contaminated, the consortium needs every downstream
result connected to it through any number of derivation steps — not just
the three runs that used it directly, but a run whose output was later
repackaged into a new lot used in two further runs, and, three
derivation steps removed, one further run in an entirely different lab
that pulled a public reference dataset entry traceable back to that same
repackaged lot six months later. Expressed as a relational recursive
query against the adjacency tables, tracing that chain needs five
self-joins over the run table and occasionally exceeds the platform's
query timeout before it finishes. See `README.md` for the full
derivation chain and the traversal that returns it well within a second.

## Link to starter kit

**Kit:** `starters/neo4j-at-scale/README.md`
