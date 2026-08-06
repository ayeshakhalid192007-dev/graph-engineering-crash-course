---
name: trim-to-budget
description: Trims a task-scoped candidate subgraph down to a hard node-count budget, keeping the anchor plus the highest-relevance nodes, dropping any edge that touches a dropped node, and recording the exact cutoff score used
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# trim-to-budget

Reads a candidate task-scoped subgraph — an anchor node plus relevance-
scored surrounding nodes and their edges — and a node-count budget, then
produces the largest allowed slice: the anchor, plus as many of the
highest-relevance remaining nodes as fit, with every edge re-checked
against the final kept set.

## Instructions

You are a Claude Code skill implementing the `budget-capped-subgraph`
pattern. Follow these steps in order:

1. **Identify the anchor node.** It is always kept, and it always counts
   as one of the budget's node slots — never treat it as free.
2. **Read every other candidate node and its relevance score.** Default
   to the candidate subgraph and budget in this kit's `README.md` unless
   the user gives you a different one. Sort these nodes by relevance,
   highest first.
3. **Fill the remaining budget slots in relevance order.** With a budget
   of N nodes, the anchor takes one slot and the top (N-1) remaining
   nodes by relevance take the rest. Everything past that point is
   dropped. If two nodes tie exactly on relevance at the cutoff boundary,
   note the tie explicitly rather than picking one arbitrarily and saying
   nothing about it.
4. **Record the trimming rule as a legible statement**, not just a list:
   name the budget, confirm the anchor was kept unconditionally, and
   state the exact relevance score at which the cutoff fell (the lowest
   score still kept, and the highest score dropped, if they differ).
5. **Re-check every edge in the candidate subgraph against the final kept
   node set.** An edge survives only if both of its endpoints are in the
   kept set. Do this as its own explicit pass after node trimming is
   decided — don't try to decide node and edge survival in the same
   pass, since an edge's fate depends on a node-trimming decision that
   has to be finished first.
6. **Report four things together**: the kept nodes, the dropped nodes,
   the surviving edges, and the trimming rule statement from step 4.
   Never report just the kept subgraph without also naming what got cut
   and why — a cutoff nobody can see is indistinguishable from no budget
   at all.

## Input

- A candidate task-scoped subgraph: one anchor node, other nodes each
  with a relevance score, and the edges among them.
- A budget expressed as a maximum node count (defaults to the budget in
  this kit's `README.md`).

## Output

- The kept node set (anchor plus highest-relevance nodes up to budget).
- The dropped node set.
- The surviving edges (both endpoints kept) and the dropped edges
  (touching at least one dropped node).
- A trimming-rule statement naming the budget and the cutoff score.

## Example Usage

```
Use the trim-to-budget skill on the candidate subgraph and budget in
README.md.

Expected:
  Kept (8): client-ferreira-o (anchor), filing-eviction-notice-2026-03
    (0.95), filing-answer-2026-03 (0.90), hearing-2026-04-12 (0.88),
    party-landlord-hollis-mgmt (0.80), statute-tenant-protection-act-12
    (0.75), filing-motion-continuance-2026-04 (0.60),
    party-co-tenant-vasquez (0.55)
  Dropped (4): note-intake-call-2026-02 (0.50), party-prior-attorney-ng
    (0.40), filing-unrelated-parking-dispute-2024 (0.20),
    party-property-manager-other (0.15)
  Rule: budget 8, anchor kept unconditionally, cutoff at relevance 0.55
    (lowest kept); everything at or below 0.50 dropped.
  Surviving edges: 7 (all edges between two kept nodes).
  Dropped edges: 4 (each touches note-intake-call-2026-02 or
    filing-unrelated-parking-dispute-2024).
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that the kept node count
exactly equals the budget (never one over, and never under unless the
candidate set itself has fewer nodes than the budget), and that every
edge you report as surviving genuinely has both endpoints in the kept
set — re-verify this rather than trusting your first pass.
