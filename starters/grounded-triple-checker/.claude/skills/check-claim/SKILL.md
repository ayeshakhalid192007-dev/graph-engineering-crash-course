---
name: check-claim
description: Pins a "change does not touch module" claim to one graph edge -- the only fact that can make it false -- scans the populated graph's own edge list for a subject/predicate/object match, and reports ACCEPT or REJECT naming the edge it relied on
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# check-claim

A claim like "this change doesn't touch that module" rises or falls on one
underlying fact: whether an edge connecting the two actually exists in the
graph. This skill isolates that fact and checks for it directly, without
letting how convincing or alarming the change's own description sounds
affect the outcome. The verdict comes from what the graph contains, not
from a gut sense of the description's tone.

## Instructions

You are a Claude Code skill implementing the `grounded-triple-checker`
pattern. Follow these steps in order:

1. **Read the full graph first.** Open `sample-graph.example.json` (or the
   file the user names) and parse its `nodes` and `edges` arrays before
   doing anything else.
2. **Resolve which claim(s) to check.** If the user names a specific claim
   id, check only that one. Otherwise default to every `claim`-typed node
   in the graph — this kit's shipped scenario has two:
   `claim-ch3002-no-license-touch` and `claim-ch3047-no-license-touch`.
3. **Name the edge whose presence in the graph would break this claim.**
   Pull the claim node's own `about` (the change id) and `forbidden_module`
   fields — do not parse these back out of the claim's free-text `text`
   field, and do not open the change node's `description` at this step.
   The decomposed assertion is: no edge of the form `(about, "touches",
   forbidden_module)` exists in the graph.
4. **Scan every edge in the graph, looking for one whose subject,
   predicate, and object all three line up with that triple.** A `touches`
   edge from the right change to a different module doesn't count, and
   neither does an edge of a different predicate between the same two
   nodes.
5. **Decide the verdict from presence alone.** A match found among the
   graph's edges means REJECT, with that exact edge cited as the reason;
   no match anywhere in the graph means ACCEPT. Do not consult the
   change's `description` field to double-check either outcome — a
   description that sounds convincing is not evidence, and neither is one
   that sounds suspicious.
6. **Handle the unverifiable case explicitly.** If the claim's `about`
   change id or `forbidden_module` module id isn't found among the graph's
   nodes at all, report that claim as UNVERIFIABLE rather than defaulting
   it to ACCEPT. An edge that can't be looked up is not the same thing as
   an edge that's confirmed absent.
7. **Write the results** to `verdicts.json` (or the path the user
   requested) in this kit's root: an array with one entry per claim, each
   holding `claim_id`, `about`, `forbidden_module`, `decomposed_edge`,
   `edge_found`, `verdict`, and `citation` (the exact matching edge for a
   REJECT, or `null` for ACCEPT/UNVERIFIABLE).
8. **Report a summary** alongside the file: how many claims came back
   ACCEPT, REJECT, or UNVERIFIABLE, and the citation for every REJECT.

## Input

- `sample-graph.example.json` (or another file the user names) — the
  populated graph to check claims against.
- A claim id, or nothing (defaults to checking every claim node in the
  graph).

## Output

- `verdicts.json` (or user-specified path) — one entry per claim, with the
  decomposed edge, whether it was found, the verdict, and the citation.
- A printed summary of how many claims landed in each verdict bucket.

## Example Usage

```
Use the check-claim skill on sample-graph.example.json.

Expected verdicts (2 of 2 claims checked):
  claim-ch3002-no-license-touch -> ACCEPT
    decomposed edge (CH-3002, touches, drm-license-issuer) -- absent
  claim-ch3047-no-license-touch -> REJECT
    decomposed edge (CH-3047, touches, drm-license-issuer) -- present
    citation: { "subject": "CH-3047", "predicate": "touches",
                "object": "drm-license-issuer" }
```

## Validation

The companion agent (`.claude/agents/graph-verifier.md`) independently
re-derives each claim's decomposed edge from `sample-graph.example.json`
and re-checks it from scratch, rather than trusting `verdicts.json`'s own
account of what it found.
