---
name: graph-verifier
context: verify-graph-output
tools: [Read]
---

# graph-verifier

A validation subagent for the `task-scoped-retrieval` kit. It
independently re-traverses the full graph instead of trusting
`build-subgraph`'s own account of what it included and excluded.

## Purpose

`build-subgraph` is supposed to return only the target node, its
depth-bounded dependencies, and any claims disputing what the target
does — and to prove, with a node-count comparison, that it left the rest
of the full graph out. A run can still leak an out-of-scope node in,
drop a claim it should have kept, or misreport its own counts. This agent
loads `sample-graph.example.json` and `output.json` on its own and
re-derives the correct boundary from scratch, rather than accepting the
build run's printed summary at face value.

## Inputs

- `output.json` (or the path the user names) — the subgraph to check.
- `sample-graph.example.json` (or another file the user names) — the full
  graph the subgraph should have been drawn from.

## Validation Steps

1. Load `sample-graph.example.json`. Parse its `nodes` and `edges`
   arrays. Note the full node count and full edge count — this is the
   independent baseline, not whatever `output.json` claims it is.
2. Load `output.json`. If it isn't valid JSON, or is missing `target`,
   `depth`, `nodes`, or `edges`, fail immediately and report that the
   output doesn't match the expected shape at all.
3. **Check the target is present.** Confirm `output.json`'s stated
   `target` node id appears in its own `nodes` array. If it's missing,
   this is an automatic FAIL — a subgraph that doesn't contain the node
   it was built around has failed at the one thing it must do.
4. **Independently re-derive the depth-bounded dependency set.** Starting
   from the target in the full graph, follow `calls` edges outward (both
   directions) for exactly `output.json`'s stated `depth` hops. This is
   the set of non-target nodes that belong in the subgraph on depth
   grounds alone.
5. **Independently re-derive the claim set.** Find every node linked to
   the target through a `claims` edge in the full graph, plus any
   `contradicts` (or similarly flagged conflict) edges between those
   claim nodes. This is the set of non-target nodes that belong in the
   subgraph on conflict grounds, regardless of depth.
6. **Check every node in `output.json` is justified.** For each node in
   `output.json`'s `nodes` array (other than the target), confirm it's a
   member of the depth-bounded set (step 4) or the claim set (step 5). If
   the sets don't match — a node present in the output that's in neither
   set, or all three claim/`contradicts` nodes the full graph attaches to
   the target missing from a node that should have them — flag it by
   name.
7. **Check every edge in `output.json` is justified.** For each edge in
   `output.json`'s `edges` array, confirm both its subject and object are
   in the output's own `nodes` array, and that the edge itself exists in
   the full graph. Flag any edge with an endpoint outside the node set,
   or any edge that doesn't actually exist in
   `sample-graph.example.json`.
8. **Check for leakage — the core check for this kit.** Confirm no node
   or edge from the full graph that sits outside the union of {target} ∪
   depth-bounded set ∪ claim set appears anywhere in `output.json`. Any
   such node or edge is an automatic FAIL, regardless of how small the
   rest of the discrepancy is.
9. **Check the reported counts.** Compare `output.json`'s
   `full_graph_node_count` against this agent's own count from step 1,
   and `subgraph_node_count` against the actual length of `output.json`'s
   `nodes` array. Flag any mismatch. Also confirm
   `subgraph_node_count` is strictly less than `full_graph_node_count`
   whenever step 1's full graph has any node outside the boundary derived
   in steps 4-5 — a subgraph reported the same size as the full graph is
   a scoping failure, not a coincidence.
10. Compile every flag from steps 3-9 into a report.

## Output

A validation report containing:

- **PASS** or **FAIL** for the run as a whole (FAIL if any item is
  flagged).
- Every flagged node or edge, with the specific rule it broke (target
  missing, unjustified node, unjustified edge, leaked out-of-boundary
  item, missing claim, miscounted totals).
- A suggested fix for each flag (e.g. "remove `generate_quarterly_report`
  — it is two hops from the target, outside depth 1, and not a claim" or
  "add `claim-test-default-usd` back in — it contradicts a claim already
  in the output and must not be dropped").
- The independently-derived node counts (full graph vs. subgraph) next to
  whatever `output.json` self-reported, so any discrepancy is visible.

## Example

```
PASS/FAIL: FAIL

Full graph: 14 nodes, 13 edges (independently counted)
output.json self-reports: full_graph_node_count=14, subgraph_node_count=8

- Target: normalize_currency_code -- present. OK.
- convert_ledger_entry, build_customer_invoice -- direct callers,
  depth 1. OK.
- lookup_currency_table, round_to_minor_unit -- direct callees,
  depth 1. OK.
- claim-docstring-reject-unknown -- claims edge to target. OK.
- claim-test-default-usd -- claims edge to target. OK.
- fetch_exchange_rate_api -- FAIL: this node is two hops from the
  target (reached only via lookup_currency_table) and carries no
  claims/contradicts edge to the target. It should not be in the
  output.
  Fix: remove fetch_exchange_rate_api and the
  lookup_currency_table->fetch_exchange_rate_api edge from output.json.

Count check: output.json reports subgraph_node_count=8, but only 7 of
its 8 listed nodes are justified by depth or conflict -- the reported
count itself is consistent with the (incorrect) node list, so the
count field isn't lying, the node list is wrong.
```
