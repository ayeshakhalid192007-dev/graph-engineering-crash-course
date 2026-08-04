---
name: check-claim
description: OpenCode equivalent of the Claude Code check-claim skill and graph-verifier agent -- reduces a claim to the single edge that decides it, checks a populated graph for that edge, and verifies every REJECT's citation independently
context: pattern-implementation
---

# check-claim (OpenCode)

OpenCode equivalent of this kit's Claude Code pair
(`.claude/skills/check-claim/SKILL.md` +
`.claude/agents/graph-verifier.md`). OpenCode's config doesn't have a
separate subagent file the way Claude Code does, so this single skill runs
in two modes, driven by `opencode.json.example`'s `workflow.steps`: **check**
(the reduce-and-look-up behavior) and **verify** (the independent
recheck). Both modes read the same `sample-graph.example.json`, so the two
never drift apart on what counts as the deciding edge for a claim.

## Instructions

You are an OpenCode skill implementing the `grounded-triple-checker`
pattern. Which mode you run in is set by the `mode` field in the calling
workflow step (`opencode.json.example`); default to `check` if `mode` is
absent.

### Mode: check

1. Read `sample-graph.example.json` (or whatever `input.graph` in the
   workflow step names) before doing anything else. Parse its `nodes` and
   `edges` arrays.
2. Resolve which claims to check from `input.claim_id`, if given; otherwise
   default to every `claim`-typed node in the graph (this kit's shipped
   scenario ships two: `claim-ch3002-no-license-touch` and
   `claim-ch3047-no-license-touch`).
3. For each claim, reduce it to the single edge that decides it, using
   the claim node's own `about` and `forbidden_module` fields directly —
   never the claim's free-text `text` field, and never the named change's
   `description` field. The assertion is: no `(about, "touches",
   forbidden_module)` edge exists.
4. Search the graph's edge list for that exact triple — subject,
   predicate, and object all matching.
5. Decide the verdict from presence alone: REJECT and cite the matching
   edge if it's present; ACCEPT if it's absent. If the claim's `about` or
   `forbidden_module` id isn't in the graph's nodes at all, report
   UNVERIFIABLE instead of defaulting to ACCEPT.
6. Write `verdicts.json` (or `input.output` if the workflow step names a
   different path): an array with one entry per claim, each holding
   `claim_id`, `about`, `forbidden_module`, `decomposed_edge`,
   `edge_found`, `verdict`, and `citation` (`null` unless the verdict is
   REJECT).
7. Return, alongside the JSON, a printed summary: how many claims landed in
   each verdict bucket, and the citation for every REJECT.

### Mode: verify

This mode does not trust the `check` step's self-reported verdicts or
citations — it independently re-decomposes and re-checks every claim, the
same way the Claude Code `graph-verifier` agent does.

1. Read `sample-graph.example.json` (or `input.graph`) and independently
   parse its `nodes` and `edges`.
2. Read `verdicts.json` (or `input.verdicts`). Fail immediately, with that
   stated as the failure, if it isn't valid JSON or any entry is missing
   `claim_id`, `about`, `forbidden_module`, `edge_found`, or `verdict`.
3. For each entry, confirm its `claim_id` exists as a claim node in the
   full graph and that its `about` / `forbidden_module` match that node's
   own fields exactly. Flag any mismatch or unknown claim_id.
4. Independently re-derive the deciding triple `(about, "touches",
   forbidden_module)` straight from the graph's claim node — not from the
   entry's own `decomposed_edge`.
5. Independently search the full graph's edge list for that triple.
6. Flag any entry whose `verdict` disagrees with this independent
   presence/absence result — an edge found present paired with ACCEPT, or
   found absent paired with REJECT, is an automatic FAIL for that entry.
7. For every REJECT, confirm its `citation` exists verbatim in the full
   graph and matches the re-decomposed triple exactly. Flag a REJECT whose
   citation is missing, vague, or names a different edge.
8. For every ACCEPT, confirm no matching edge exists anywhere in the full
   graph. Flag any ACCEPT that should have been a REJECT.
9. Check this kit's known scenario answers on unmodified sample data:
   `claim-ch3002-no-license-touch` must be ACCEPT and
   `claim-ch3047-no-license-touch` must be REJECT, citing `(CH-3047,
   touches, drm-license-issuer)`. Flag either one landing the other way.
10. Return a PASS/FAIL report: PASS only if nothing was flagged in steps
    3-9, otherwise FAIL with every flagged item, the rule it broke, and a
    suggested fix.

## Input

- `sample-graph.example.json` — the populated graph.
- check mode: a claim id, or nothing (`input.claim_id`, defaults to every
  claim node).
- verify mode: `verdicts.json` (or the path configured) to check.

## Output

- check mode: `verdicts.json` plus a printed verdict-bucket summary.
- verify mode: a PASS/FAIL validation report listing flagged items, the
  rule each one broke, and a suggested fix — matching the report shape in
  the Claude Code `graph-verifier` agent's Example section.

## Configuration

This skill uses `opencode.json.example`'s `workflow.steps` to know which
mode to run and where to find its input/output files:
- `input.graph` / `input.claim_id` — check mode's full graph and (optional)
  single claim to check.
- `input.verdicts` / `input.graph` — verify mode's verdicts-to-check and
  full graph paths.

## Integration

`check` mode mirrors the Claude Code `check-claim` skill's behavior exactly
(same graph, same decomposition off the claim node's own fields, same
never-read-the-description rule, same UNVERIFIABLE fallback). `verify` mode
mirrors the Claude Code `graph-verifier` subagent's behavior exactly (same
independent re-decomposition, same citation check, same known-scenario
answer check). Running both modes back to back over this kit's
`sample-graph.example.json` should produce the same two verdicts — ACCEPT
for `claim-ch3002-no-license-touch`, REJECT for
`claim-ch3047-no-license-touch` — as the Claude Code version.
