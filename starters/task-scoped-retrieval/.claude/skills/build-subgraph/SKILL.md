---
name: build-subgraph
description: Traverses a full graph and returns a bounded subgraph around one target node -- its depth-bounded dependencies plus any disputed claims attached to it -- while proving everything else was left out
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# build-subgraph

Turns a target node id, a depth, and a full graph into a bounded
subgraph: the target, its dependency neighborhood out to that depth, and
any claim nodes attached to it that disagree with each other — nothing
else. The boundedness is the point of this skill, not a side effect, so
the output must state how much of the full graph it left out, not just
imply it.

## Instructions

You are a Claude Code skill implementing the `task-scoped-retrieval`
pattern. Follow these steps in order:

1. **Read the full graph first.** Open `sample-graph.example.json` (or
   the file the user names) and parse its `nodes` and `edges` arrays.
   Record the full node count and full edge count before doing anything
   else — this is the baseline the boundedness check compares against
   later.
2. **Resolve the target and depth.** Take the target node id and depth
   from the user's request. Default to target `normalize_currency_code`
   and depth `1` if the user doesn't specify either — this kit's shipped
   scenario. Confirm the target id actually exists among the graph's
   nodes; if it doesn't, stop and report that the target was not found
   rather than guessing a near match.
3. **Build the depth-bounded dependency set.** Starting from the target,
   follow `calls` edges outward (both directions — subject-to-object as
   "calls", object-to-subject as "called_by") for exactly `depth` hops.
   At depth 1, this is the target's direct callers and direct callees
   only — not their callers or callees in turn.
4. **Separately, pull every claim attached to the target.** Ignoring
   `depth` entirely for this step, find each node linked to the target
   through a `claims` edge — there may be one, several, or none, and they
   may or may not agree with each other. Then find every `contradicts`
   (or similarly flagged conflict) edge running between those claim
   nodes. Do not pick one claim as the "right" one and drop the rest —
   carry every attached claim and every conflict edge between them into
   the result.
5. **Assemble the subgraph.** The result's node set is: the target, the
   depth-bounded dependency set from step 3, and the claim nodes from
   step 4. The result's edge set is exactly the edges from the full graph
   whose subject and object are both in that node set — no edge gets
   included on its own if one of its endpoints didn't make the cut.
6. **Prove the boundary, don't just assert it — this step must never be
   skipped.** Compare the full graph's node count (step 1) against the
   subgraph's node count (step 5). List, or at minimum count, which node
   ids from the full graph were excluded. If the full graph has any node
   outside the boundary and the subgraph's node count still equals the
   full graph's, treat that as a signal the traversal is wrong — a
   "subgraph" that isn't smaller than the graph it was drawn from hasn't
   scoped anything, and you should re-check steps 3-5 before returning a
   result.
7. **Write the result** to `output.json` (or the path the user requested)
   in this kit's root, with this shape: `target`, `depth`, `nodes` (the
   included node objects), `edges` (the included edge objects),
   `full_graph_node_count`, `subgraph_node_count`, and
   `excluded_node_ids` (every node id in the full graph not present in
   `nodes`).
8. **Report a summary** alongside the file: the target, the depth used,
   how many nodes/edges were included versus the full graph's totals, and
   which (if any) claim nodes were pulled in for disagreement rather than
   depth.

## Input

- `sample-graph.example.json` (or another file the user names) — the
  full graph to traverse.
- A target node id and a depth, from the user's request (defaults: target
  `normalize_currency_code`, depth `1`).

## Output

- `output.json` (or user-specified path) — the bounded subgraph, plus
  `full_graph_node_count`, `subgraph_node_count`, and
  `excluded_node_ids`.
- A printed summary of the scope reduction and any conflict-flagged
  claims included.

## Example Usage

```
Use the build-subgraph skill on sample-graph.example.json with
target=normalize_currency_code and depth=1.

Expected subgraph (7 of 14 full-graph nodes):
  normalize_currency_code (target)
  convert_ledger_entry, build_customer_invoice (direct callers)
  lookup_currency_table, round_to_minor_unit (direct callees)
  claim-docstring-reject-unknown, claim-test-default-usd (attached
    claims, contradicting each other -- included regardless of depth)

Expected exclusions (7 nodes):
  generate_quarterly_report, fetch_exchange_rate_api (two hops out,
    not direct dependencies)
  archive_old_invoices, send_email_receipt, rotate_log_files,
    sync_warehouse_inventory (unrelated cluster)
  claim-unrelated-archive-retention (a claim attached to a different
    node, not the target)
```

## Validation

The companion agent (`.claude/agents/graph-verifier.md`) independently
re-traverses `sample-graph.example.json` and checks `output.json` for
three things: the target is present, every included node/edge is within
the stated depth or is a flagged conflict touching the target, and
nothing from outside that boundary leaked in.
