---
name: budget-capped-subgraph
category: D-subgraph
stage: read
cost: low
tools: [Claude Code]
core: false
---

# budget-capped-subgraph

This kit is the runnable companion to the `budget-capped-subgraph`
pattern specification (`patterns/budget-capped-subgraph.md`). It is an
extended kit — a single Claude Code reference implementation, lighter
than the full multi-tool anatomy the seven core kits carry. See
`starters/README.md` for that distinction.

## What it does

Builds a task-scoped subgraph the same way `task-scoped-retrieval` does,
then enforces a hard ceiling on how much of it a worker actually
receives. Nodes below the anchor are kept in relevance order until the
ceiling is reached; everything past that point is dropped, along with any
edge that would otherwise point at a dropped node — and the rule used to
decide the cutoff is recorded alongside the trimmed subgraph, not left
implicit.

## Inputs

- A candidate task-scoped subgraph, with each non-anchor node carrying a
  relevance score.
- A budget ceiling expressed as a node count.

## Outputs

- A subgraph trimmed to fit inside the budget.
- The trimming rule used (the relevance cutoff and which nodes it
  dropped), recorded alongside the trimmed subgraph rather than silently
  applied and discarded.

## Failure mode if skipped

The subgraph grows without any limit as the underlying graph grows, so
what started cheap quietly becomes an expensive context to build and to
hand off — with no one having decided that was an acceptable tradeoff.
A caseworker or assistant relying on the draw eventually can't tell
whether something is missing because it was irrelevant or because the
draw simply ran out of room, since nothing recorded that a cutoff ever
happened.

## Worked scenario

Northbridge Legal Aid Clinic, a fictional nonprofit practice, runs an
intake assistant that pulls a task-scoped subgraph before a caseworker
meets a client. For a client with a multi-year eviction-defense history —
filings, hearings, related parties, an old and unrelated parking dispute
from two years prior — the candidate draw runs to twelve nodes. The
clinic's assistant is capped at eight nodes per draw so a caseworker's
prep view never balloons past what's actually useful in a single sitting.
See `README.md` for the full candidate list, relevance scores, and how
the kit trims it.

## Link to starter kit

**Kit:** `starters/budget-capped-subgraph/README.md`
