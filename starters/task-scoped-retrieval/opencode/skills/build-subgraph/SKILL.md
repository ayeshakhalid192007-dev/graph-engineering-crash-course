---
name: build-subgraph
description: OpenCode equivalent of the Claude Code build-subgraph skill and graph-verifier agent -- traverses a full graph to return a bounded subgraph around one target node, and verifies nothing outside the boundary leaked in
context: pattern-implementation
---

# build-subgraph (OpenCode)

OpenCode equivalent of this kit's Claude Code pair
(`.claude/skills/build-subgraph/SKILL.md` +
`.claude/agents/graph-verifier.md`). OpenCode's config doesn't have a
separate subagent file the way Claude Code does, so this single skill
runs in two modes, driven by `opencode.json.example`'s `workflow.steps`:
**build** (the traversal behavior) and **verify** (the independent
recheck). Both modes read the same `sample-graph.example.json`, so the
two never drift apart on what counts as inside the boundary.

## Instructions

You are an OpenCode skill implementing the `task-scoped-retrieval`
pattern. Which mode you run in is set by the `mode` field in the calling
workflow step (`opencode.json.example`); default to `build` if `mode` is
absent.

### Mode: build

1. Read `sample-graph.example.json` (or whatever `input.graph` in the
   workflow step names) before doing anything else. Parse its `nodes`
   and `edges` arrays and record the full node count and full edge
   count — the baseline the boundedness check compares against later.
2. Resolve the target node id and depth from `input.target` /
   `input.depth` (defaulting to `normalize_currency_code` and `1`, this
   kit's shipped scenario, if either is absent). Confirm the target
   exists among the graph's nodes; stop and report if it doesn't, rather
   than guessing a near match.
3. Follow `calls` edges outward from the target, both directions, for
   exactly `depth` hops, to build the depth-bounded dependency set. At
   depth 1 this is direct callers and direct callees only.
4. Separately, ignoring `depth` for this step, find every claim node
   linked to the target through a `claims` edge, and every `contradicts`
   edge between those claim nodes. Carry every attached claim through —
   never drop one to leave a single "winning" answer.
5. Assemble the subgraph: nodes = target + depth-bounded set (step 3) +
   claim set (step 4); edges = every full-graph edge whose subject and
   object are both in that node set.
6. Before writing anything, compare the full graph's node count (step 1)
   against the subgraph's node count (step 5) and list which node ids
   were excluded. If the full graph has nodes outside the boundary and
   the subgraph's count still equals the full graph's, treat this as a
   sign the traversal is wrong and re-check steps 3-5 — a "subgraph" the
   same size as the graph it came from hasn't scoped anything.
7. Write `output.json` (or `input.output` if the workflow step names a
   different path) with: `target`, `depth`, `nodes`, `edges`,
   `full_graph_node_count`, `subgraph_node_count`, and
   `excluded_node_ids`.
8. Return, alongside the JSON, a printed summary: the target, depth used,
   included vs. full-graph node/edge counts, and which claim nodes were
   pulled in for disagreement rather than depth.

### Mode: verify

This mode does not trust the `build` step's self-reported counts or node
list — it independently re-traverses the full graph, the same way the
Claude Code `graph-verifier` agent does.

1. Read `sample-graph.example.json` (or `input.graph`) and independently
   record the full node count, full edge count, and the graph's actual
   `calls`/`claims`/`contradicts` edges.
2. Read `output.json` (or `input.output`). Fail immediately, with that
   stated as the failure, if it isn't valid JSON or is missing `target`,
   `depth`, `nodes`, or `edges`.
3. Confirm `output.json`'s `target` appears in its own `nodes` array.
   Flag (and treat as an automatic FAIL) if it doesn't.
4. Independently re-derive the depth-bounded dependency set by walking
   `calls` edges from the target, both directions, for `output.json`'s
   stated `depth` hops.
5. Independently re-derive the claim set: every node linked to the
   target through a `claims` edge, plus any `contradicts` edges between
   those claim nodes.
6. For every node in `output.json`'s `nodes` array other than the
   target, confirm it belongs to the depth-bounded set or the claim set.
   Flag any that belongs to neither.
7. For every edge in `output.json`'s `edges` array, confirm both
   endpoints are in the output's node set and the edge actually exists in
   the full graph. Flag any edge that fails either check.
8. Confirm nothing from outside the union of {target} ∪ depth-bounded set
   ∪ claim set appears anywhere in `output.json` — this is the core
   check for this kit. Any leaked node or edge is an automatic FAIL.
9. Compare `output.json`'s `full_graph_node_count` and
   `subgraph_node_count` against this pass's own independently-derived
   counts. Flag any mismatch, and flag a `subgraph_node_count` equal to
   `full_graph_node_count` whenever the full graph has nodes outside the
   boundary.
10. Return a PASS/FAIL report: PASS only if nothing was flagged in steps
    3-9, otherwise FAIL with every flagged item, the rule it broke, and a
    suggested fix.

## Input

- `sample-graph.example.json` — the full graph.
- build mode: a target node id and depth (`input.target` /
  `input.depth`).
- verify mode: `output.json` (or the path configured) to check.

## Output

- build mode: `output.json` plus a printed scope-reduction summary.
- verify mode: a PASS/FAIL validation report listing flagged items, the
  rule each one broke, and a suggested fix — matching the report shape in
  the Claude Code `graph-verifier` agent's Example section.

## Configuration

This skill uses `opencode.json.example`'s `workflow.steps` to know which
mode to run and where to find its input/output files:
- `input.graph` / `input.target` / `input.depth` — build mode's full
  graph, target node, and depth.
- `input.output` / `input.graph` — verify mode's output-to-check and full
  graph paths.

## Integration

`build` mode mirrors the Claude Code `build-subgraph` skill's behavior
exactly (same graph, same depth-bounded traversal, same unconditional
claim pull, same boundedness proof). `verify` mode mirrors the Claude
Code `graph-verifier` subagent's behavior exactly (same independent
re-traversal, same leakage check, same count cross-check). Running both
modes back to back over this kit's `sample-graph.example.json` at
target `normalize_currency_code`, depth `1` should produce the same
7-node subgraph and the same list of excluded nodes as the Claude Code
version.
