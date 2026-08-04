---
name: task-scoped-retrieval
category: D-subgraph
stage: read
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# task-scoped-retrieval

This kit is the runnable companion to the `task-scoped-retrieval` pattern
specification (`patterns/task-scoped-retrieval.md`). It works one concrete
scenario end to end: a fictional analytics company's currency-normalizing
function is under repair, and the kit has to hand the worker fixing it a
bounded slice of the codebase graph — not the whole thing — while making
sure a live disagreement about what the function is supposed to do
survives the handoff intact.

## What it does

Given a target node id and a depth (number of hops), traverses a full
graph and returns a bounded subgraph: the target node, its dependencies
and dependents up to that depth via `calls`/`called_by` edges, and any
claim nodes attached to the target that are flagged as disputed or
contradicting each other — regardless of whether those claims sit within
the depth boundary. Everything else in the graph is deliberately left
out, even when the full graph is far larger than what gets returned. The
kit does not just claim to have scoped the result — it reports the full
graph's node count against the returned subgraph's node count, so the
exclusion is a checkable fact, not an assumption.

## Inputs

- A target node id (the function under repair) and a depth (how many
  `calls`/`called_by` hops out from the target to include).
- The full graph to draw the subgraph from. This kit ships
  `sample-graph.example.json`, a small, fixed, already-populated graph —
  14 nodes, 13 edges — standing in for a much larger production graph. It
  covers a fictional company, Verdant Metrics, and its
  `normalize_currency_code` function, with two contradicting claims
  attached to that function and an unrelated cluster of functions the
  subgraph must exclude.

## Outputs

- A bounded subgraph: the target node, its depth-bounded dependency set,
  and its full set of attached claims (contradictions included), plus
  only the edges connecting members of that set.
- A stated node count for the full graph and for the returned subgraph,
  so the scope reduction is visible rather than assumed.

## Failure mode if skipped

Hand a worker the whole graph instead of a scoped slice and it either
drowns in a few thousand nodes that have nothing to do with its task, or
— just as likely — the one claim node that actually mattered gets lost
somewhere in everything else it wasn't given a reason to read. Worse,
if a subgraph builder does exist but resolves a disagreement between two
attached claims before handing the slice over, the worker only ever sees
a single confident-looking answer, with nothing in the returned slice to
suggest the underlying graph is still split on the question — it fixes
the function according to whichever claim happened to survive the
boundary-drawing step, unaware a second, contradicting claim ever
existed.

## Link to starter kit

**Kit:** `starters/task-scoped-retrieval/README.md`
