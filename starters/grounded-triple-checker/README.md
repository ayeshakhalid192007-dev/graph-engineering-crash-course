# grounded-triple-checker Starter Kit

A runnable starter kit for the **grounded-triple-checker** pattern. Its
worked case is a "this change doesn't touch that module" claim, and the
verdict comes from exactly one source: whether the graph's edge list
already contains a matching subject/predicate/object triple for that
change and module. How convincingly — or how worryingly — the change's
own write-up is worded never factors in. This kit's worked scenario
involves a fictional video-encoding and streaming company ("Cobalt
Stream") and two invented changes against its pipeline — not based on any
real company or codebase.

This is a **read-path** kit, unlike `document-to-facts`,
`alias-merge-with-trail`, and `receipt-per-edge`. There's no document to
extract from and no `schema.example.json` — instead there's
`sample-graph.example.json`, a small, fixed, already-populated graph to
query against.

## The scenario

Two changes land against Cobalt Stream's video pipeline in the same week.
`CH-3002`'s description describes a thumbnail-batching cleanup and claims
it never goes near the DRM license issuer — a module sensitive enough that
a reviewer wants that specific claim double-checked before merging.
`CH-3047`'s description reads just as reassuring: a small subtitle-retry
fix, also claiming no contact with the license issuer. Only one of the two
claims is actually true. `CH-3047` also swaps in a cache helper pulled
straight out of the license module — a detail its own description never
mentions — and the graph, assembled from the diff rather than from either
change's prose, already contains that exact edge.

A checker that only reads the two descriptions has no reason to treat them
differently — both sound equally confident. This kit's skill instead asks
one narrow question per claim — is there a `touches` edge linking the named
change to `drm-license-issuer` in the graph — and lets the answer alone
decide the outcome: ACCEPT `CH-3002`'s claim, REJECT `CH-3047`'s, and name
the exact edge that gives it away.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- No external services or API keys — the whole kit runs against the one
  local file described below.

## Quick Start

1. Review `PATTERN.md` to understand what this pattern solves for and what
   breaks without it.
2. Examine `sample-graph.example.json` — the fixed 10-node, 7-edge graph
   this kit queries. Note the two claim nodes, the `drm-license-issuer`
   module they're both about, and the single `touches` edge that separates
   a true claim from a fabricated one.
3. Follow the tool-specific instructions below to run the kit.
4. Inspect `verdicts.json` and confirm it matches the "Expected Output"
   section below — including which claim was REJECTed and the edge cited.

### Claude Code

1. Load the skill: `.claude/skills/check-claim/SKILL.md`.
2. Ask it to run: "Use the check-claim skill on
   sample-graph.example.json." (With no claim id given, it checks every
   claim node in the graph — both of this kit's shipped claims.)
3. It writes `verdicts.json` and prints a summary of each verdict and,
   for any REJECT, the specific edge it cited.
4. Load the verifier: `.claude/agents/graph-verifier.md` and ask it to
   check `verdicts.json` against `sample-graph.example.json`. It
   independently re-decomposes and re-checks each claim rather than trusting
   the check run's own account.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json` (or point
   OpenCode at it directly).
2. Run the `check` workflow step — it invokes
   `opencode/skills/check-claim/SKILL.md` in check mode over
   `sample-graph.example.json` and writes `verdicts.json`.
3. Run the `verify` workflow step — the same skill file, running in
   verify mode, independently re-checks `verdicts.json` and reports
   PASS/FAIL.

## Expected Output

Running the kit over the shipped graph should produce `verdicts.json` with
two entries:

- **`claim-ch3002-no-license-touch` -> ACCEPT.** Decomposed edge
  `(CH-3002, touches, drm-license-issuer)` is absent from the graph —
  `CH-3002` only touches `thumbnail-renderer` and `cdn-purger`. `citation`
  is `null`.
- **`claim-ch3047-no-license-touch` -> REJECT.** Decomposed edge
  `(CH-3047, touches, drm-license-issuer)` is present in the graph —
  `CH-3047` also touches `subtitle-sync`, but that edge isn't why the
  claim is rejected; the license-issuer edge is. `citation` names that
  exact edge.

`CH-3118`, the unrelated metrics-exporter change, has no claim attached and
should never appear in `verdicts.json` at all.

### Checking the verdicts

Every verdict in this kit should be defensible by pointing at one edge in
the graph — never by describing how safe or risky the change generally
felt. To confirm it:

- Open `verdicts.json` and check `claim-ch3047-no-license-touch`'s
  `citation` names `{"subject": "CH-3047", "predicate": "touches",
  "object": "drm-license-issuer"}` exactly — not a paraphrase, not a
  different edge.
- Confirm `claim-ch3002-no-license-touch`'s `citation` is `null` and its
  `verdict` is ACCEPT.
- Confirm neither verdict was decided by reading either change's
  `description` field — the decomposed edge and the graph's edge list are
  the only inputs that should have mattered.

If `claim-ch3047-no-license-touch` comes back ACCEPT, the checker fell back
to trusting the change's own description instead of the graph — exactly
the failure this kit exists to catch, and the verifier should flag it (see
"Symptom" table below).

## Modifying the Example

To adapt this kit to your own grounded-triple-checker scenario:

1. Replace `sample-graph.example.json` with your own graph — any set of
   nodes and edges works, as long as you keep a way to record a
   change-to-module relationship (this kit uses `touches`) and a way to
   attach a claim about a specific change/module pair (this kit uses
   `claim` nodes with `about` / `forbidden_module` fields, linked to their
   change by a `claims` edge).
2. Add or edit claim nodes to test new scenarios — nothing about the
   decomposition logic is hardcoded to `drm-license-issuer` or Cobalt
   Stream.
3. Re-run the skill and confirm `verdicts.json` still cites a real edge for
   every REJECT and still passes the verifier.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `sample-graph.example.json` — the fixed 10-node Cobalt Stream graph this
  kit queries (replaces `schema.example.json` for this read-path kit — see
  `starters/README.md`'s anatomy note).
- `.claude/skills/check-claim/SKILL.md` — Claude Code decompose-and-check
  skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/check-claim/SKILL.md` — OpenCode skill covering both
  checking and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `verdicts.json` shows ACCEPT for `claim-ch3047-no-license-touch`. | The skill read the change's `description` field instead of searching the graph's edge list — re-check `SKILL.md` step 5 ran the edge search before deciding anything. |
| A REJECT entry has `citation: null` or a citation that doesn't match the decomposed edge. | Step 5 decided REJECT correctly but skipped naming the edge, or named a different one. A REJECT must always cite the exact matching edge, not just assert one exists. |
| A claim comes back ACCEPT when its `about`/`forbidden_module` id isn't even in the graph. | Step 6 was skipped — an unresolvable claim must be reported UNVERIFIABLE, not defaulted to ACCEPT. |
| `verdicts.json` includes an entry for `CH-3118` or any change with no claim node. | Step 2 checked a change directly instead of limiting itself to the claim nodes the graph actually contains. |
| The verifier reports a discrepancy between its independently-derived edge presence and `verdicts.json`'s self-reported `edge_found`. | This is the verifier doing its job — it means the check run got the lookup wrong. Treat `verdicts.json` as untrusted until the discrepancy is resolved. |

## Next Steps

- Review the pattern specification in
  `patterns/grounded-triple-checker.md` in the course repo for the general
  (not scenario-specific) statement of this pattern.
- This is a core kit — see `starters/README.md` for how it relates to the
  other six core kits and the sixteen extended kits.
