---
name: traverse-multi-hop
description: Expresses a multi-hop lineage question as a single variable-length path match against native graph storage, bounded by an explicit hop depth and an explicit relationship-type allowlist, instead of a recursive relational join that grows one level per hop
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# traverse-multi-hop

Given a starting node and a lineage question, follows only a named set of
relationship types outward to a bounded depth, tags every node reached
with its hop count and the exact path that reached it, and reports the
deepest hop the traversal actually needed — without walking into an
unrelated part of the graph or looping on a cycle.

## Instructions

You are a Claude Code skill implementing the `neo4j-at-scale` pattern.
Follow these steps in order:

1. **Take the starting node and the traversal question as given.**
   Default to reagent lot RL-2291 and this kit's derivation question in
   `README.md` unless told otherwise. Do not express this as a
   fixed-depth join or a recursive relational query — treat it as a
   single variable-length path match against native graph storage, since
   the entire reason this pattern exists is that relational joins get
   more expensive with every added hop while native traversal does not.
2. **Name the exact relationship types the traversal is allowed to
   follow**, and the direction each one traverses in. Default to
   `USED_IN`, `PRODUCES`, and `DERIVED_FROM` as given in `README.md`. Do
   not follow a relationship type that isn't on this list, even if it
   happens to connect two nodes that are also connected through an
   allowed path — an unrelated edge crossing the same two nodes is not
   part of the lineage being traced.
3. **Set an explicit upper bound on hop depth** for the traversal (e.g.
   `*1..10`). Native traversal doesn't degrade with depth the way
   relational joins do, but an unbounded match can still wander into an
   unrelated, distant part of the graph if the allowed relationship types
   turn out to be looser than intended — the bound is a safety limit, not
   a performance workaround.
4. **Guard against cycles.** A derivation graph like this one should be
   acyclic, but a bookkeeping error could introduce one. If the
   traversal would revisit a node already on its current path, detect
   and report that as a cycle rather than looping or silently truncating
   the results.
5. **Do not include a node reached only by a property coincidence** —
   sharing a date, a facility, or any other attribute with a node on the
   path is not itself a relationship. Only nodes reached by walking an
   allowed relationship type, in the allowed direction, count as part of
   the traversal's results.
6. **Tag every node reached with its hop count and the specific sequence
   of relationship types that reached it** — "used directly" (hop 1)
   must stay distinguishable from "three derivation steps removed"
   (hop 3) in the output, not collapsed into one flat list.
7. **Report the deepest hop the traversal actually needed for this run**,
   separately from the configured upper bound, so a reader can see how
   far the real chain reached without having to count entries.

## Input

- A starting node (defaults to RL-2291 in this kit's `README.md`).
- An allowed relationship-type list and traversal direction for each
  (defaults to `USED_IN`, `PRODUCES`, `DERIVED_FROM`).
- A hop-depth bound (defaults to `*1..10`).

## Output

- Every node reached, tagged with its hop count and the relationship
  path that reached it.
- The deepest hop actually reached this run.
- An explicit cycle report if one was detected, instead of a silently
  truncated or hanging result.

## Example Usage

```
Use the traverse-multi-hop skill starting from RL-2291 in README.md,
following USED_IN, PRODUCES, and DERIVED_FROM, bounded to 10 hops.

Expected:
  Hop 1 (USED_IN): R-88701, R-88702, R-88703
  Hop 2 (PRODUCES -> DERIVED_FROM -> USED_IN): RL-2340, then R-88750, R-88761
  Hop 3 (PRODUCES -> reference dataset entry -> unrelated lab pipeline): R-88812

  Deepest hop reached: 3 (bound was 10)
  No cycle detected.
  R-91004 excluded: shares date and facility with R-88701 but no allowed
    relationship connects it to this chain.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check two things: that nothing in
the result set is there only because it shares a property with a node on
the path rather than an actual relationship, and that every result's hop
count matches the length of the specific relationship path reported for
it, not a guess based on how "far" the node feels from the start.
