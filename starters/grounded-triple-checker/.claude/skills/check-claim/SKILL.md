---
name: check-claim
description: Reduces a "change does not touch module" claim to the single edge that decides it, checks a populated graph directly for that edge, and reports ACCEPT or REJECT with the specific edge cited
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# check-claim

Turns a "doesn't touch that module" claim into the one fact that would have
to be true for the claim to fail, then answers strictly from whether that
fact is sitting in the graph — never from how the change's own description
reads. The point of this skill is that the verdict is a lookup, not an
impression.

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
3. **Reduce each claim to the single edge that decides it.** Pull the
   claim node's own `about` (the change id) and `forbidden_module` fields —
   do not parse these back out of the claim's free-text `text` field, and
   do not open the change node's `description` at this step. The decomposed
   assertion is: no edge of the form `(about, "touches", forbidden_module)`
   exists in the graph.
4. **Search the graph's edge list for exactly that edge.** Subject,
   predicate, and object must all match — a `touches` edge from the right
   change to a different module doesn't count, and neither does an edge of
   a different predicate between the same two nodes.
5. **Decide the verdict from presence alone.** If the edge is present in
   the graph, REJECT the claim and cite that exact edge as the reason. If
   the edge is absent, ACCEPT the claim. Do not consult the change's
   `description` field to double-check either outcome — a description that
   sounds convincing is not evidence, and neither is one that sounds
   suspicious.
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
