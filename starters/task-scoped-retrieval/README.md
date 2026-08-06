# task-scoped-retrieval Starter Kit

A runnable starter kit for the **task-scoped-retrieval** pattern: given a
target node and a depth, returning a bounded subgraph — the target, its
depth-bounded dependencies, and any disputed claims attached to it — while
proving the rest of a larger graph was deliberately left out. This kit's
worked scenario involves a fictional e-commerce analytics company
("Verdant Metrics") and an invented currency-normalizing function — not
based on any real company or codebase.

This is a **read-path** kit, unlike `document-to-facts`,
`alias-merge-with-trail`, and `receipt-per-edge`. There's no document to
extract from and no `schema.example.json` — instead there's
`sample-graph.example.json`, a small, fixed, already-populated graph to
query against.

## The scenario

A ticket comes in: `normalize_currency_code`, the function that turns a
raw currency code string into its canonical ISO 4217 form before an
amount gets priced, is occasionally letting unrecognized currency codes
through priced as if they were USD, when some part of the codebase
insists it should reject them outright. Two disagreeing records already
exist in the graph about what the function is supposed to do — a
docstring says it raises on an unrecognized code, a test suite says it
defaults to USD — and neither has been reconciled.

A worker picks up the ticket to fix `normalize_currency_code`. Handing
that worker the entire graph — 14 nodes standing in for what would be a
few thousand in a real codebase — buries the two claims that actually
matter under callers, callees, and an entirely unrelated cluster of
invoice-archiving functions that have nothing to do with currency
handling. This kit's skill builds the worker a bounded slice instead:
the target, its direct callers and callees, and both contradicting claims
attached to it — nothing else.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- No external services or API keys — the whole kit runs against the one
  local file described below.

## Quick Start

1. Review `PATTERN.md` to understand what this pattern solves for and
   what breaks without it.
2. Examine `sample-graph.example.json` — the fixed 14-node, 13-edge graph
   this kit queries. Note the target function (`normalize_currency_code`),
   its direct callers/callees, its two contradicting claim nodes, and the
   unrelated cluster of functions that should never appear in its
   subgraph.
3. Follow the tool-specific instructions below to run the kit.
4. Inspect `output.json` and confirm it matches the "Expected Output"
   section below — including the node-count comparison and the excluded
   node list.

### Claude Code

1. Load the skill: `.claude/skills/build-subgraph/SKILL.md`.
2. Ask it to run: "Use the build-subgraph skill on
   sample-graph.example.json with target=normalize_currency_code and
   depth=1."
3. It writes `output.json` and prints a summary of the scope reduction —
   nodes included versus the full graph's total, and which claim nodes
   were pulled in for disagreement.
4. Load the verifier: `.claude/agents/graph-verifier.md` and ask it to
   check `output.json` against `sample-graph.example.json`. It
   independently re-traverses the full graph and confirms nothing outside
   the target's depth-1 boundary (or its attached claims) leaked into the
   output.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json` (or point
   OpenCode at it directly).
2. Run the `build` workflow step — it invokes
   `opencode/skills/build-subgraph/SKILL.md` in build mode over
   `sample-graph.example.json` and writes `output.json`.
3. Run the `verify` workflow step — the same skill file, running in
   verify mode, independently re-traverses `sample-graph.example.json`
   and reports PASS/FAIL on `output.json`.

## Expected Output

Running the kit with `target=normalize_currency_code`, `depth=1` should
produce a subgraph close to this shape in `output.json`, out of the full
graph's 14 nodes / 13 edges:

- **Included (7 nodes):** `normalize_currency_code` (target);
  `convert_ledger_entry`, `build_customer_invoice` (direct callers);
  `lookup_currency_table`, `round_to_minor_unit` (direct callees);
  `claim-docstring-reject-unknown`, `claim-test-default-usd` (both
  attached claims, kept intact along with the `contradicts` edge between
  them — neither one dropped in favor of the other).
- **Excluded (7 nodes):** `generate_quarterly_report`,
  `fetch_exchange_rate_api` (two hops out — not direct dependencies);
  `archive_old_invoices`, `send_email_receipt`, `rotate_log_files`,
  `sync_warehouse_inventory` (the unrelated cluster); and
  `claim-unrelated-archive-retention` (a claim attached to
  `archive_old_invoices`, a different node — proof a claim on the wrong
  node doesn't leak in just because claims as a category are in scope).
- **Counts:** `full_graph_node_count: 14`, `subgraph_node_count: 7`,
  `excluded_node_ids` listing the 7 nodes above.

### Checking the boundary

The whole point of this kit is that the subgraph is provably smaller than
the full graph, not just "probably fine." To confirm it:

- Open `output.json` and check `subgraph_node_count` is strictly less
  than `full_graph_node_count` (7 vs. 14 in the default scenario).
- Confirm both `claim-docstring-reject-unknown` and
  `claim-test-default-usd` appear together, along with the `contradicts`
  edge between them — neither claim should be missing.
- Confirm none of the 7 excluded node ids above appear anywhere in
  `output.json`'s `nodes` or `edges`.

If `subgraph_node_count` equals `full_graph_node_count`, or an excluded
node shows up in the output anyway, the skill returned the whole graph
(or a leak from it) instead of a scoped slice — that is exactly the
failure this kit exists to catch, and the verifier should flag it (see
"Symptom" table below).

## Modifying the Example

To adapt this kit to your own task-scoped-retrieval scenario:

1. Replace `sample-graph.example.json` with your own graph — any set of
   nodes and edges works, as long as you keep a way to mark a
   node-to-node dependency relationship (this kit uses `calls`) and a
   way to attach disputed claims to a node (this kit uses `claims` /
   `contradicts`).
2. Pick a new target node and depth when you invoke the skill — nothing
   about the traversal logic is hardcoded to `normalize_currency_code`.
3. Re-run the skill and confirm `output.json` still reports a
   `subgraph_node_count` smaller than `full_graph_node_count`, still
   keeps every attached claim intact, and that the verifier still passes.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `sample-graph.example.json` — the fixed 14-node Verdant Metrics graph
  this kit queries (replaces `schema.example.json` for this read-path
  kit — see `starters/README.md`'s anatomy note).
- `.claude/skills/build-subgraph/SKILL.md` — Claude Code traversal skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/build-subgraph/SKILL.md` — OpenCode skill covering
  both building and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `output.json`'s `subgraph_node_count` equals `full_graph_node_count`. | The depth or claim-set logic was applied too loosely and stopped excluding anything. Re-check `SKILL.md` step 6 (the boundedness proof) ran before the write. |
| One of `claim-docstring-reject-unknown` / `claim-test-default-usd` is missing from `output.json`. | The skill picked a "winning" claim instead of carrying every claim attached to the target. A disagreement must survive the handoff, not get resolved during traversal. |
| A node from the unrelated cluster (`archive_old_invoices`, `send_email_receipt`, `rotate_log_files`, `sync_warehouse_inventory`) or `fetch_exchange_rate_api` / `generate_quarterly_report` appears in `output.json`. | The depth traversal went further than the stated `depth`, or treated a two-hop node as if it were one hop. Re-check step 3 of `SKILL.md` counted hops correctly. |
| `claim-unrelated-archive-retention` appears in `output.json`. | The skill pulled in claims attached to some other node instead of only the target. Step 4 of `SKILL.md` must filter claims by the `claims` edge pointing specifically at the target. |
| The verifier reports a discrepancy between its independently-derived counts and `output.json`'s self-reported counts. | This is the verifier doing its job — it means the build run's self-report undercounted or overcounted what it actually returned. Treat `output.json` as untrusted until the discrepancy is resolved. |

## Next Steps

- Review the pattern specification in `patterns/task-scoped-retrieval.md`
  in the course repo for the general (not scenario-specific) statement of
  this pattern.
- This is a core kit — see `starters/README.md` for how it relates to the
  other six core kits and the sixteen extended kits.
