---
name: arbitrate-collision
description: Detects when two loops have proposed conflicting writes to the same node and field at close to the same time, applies a stated priority rule to accept exactly one, and records the rejected write with the reason it lost
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# arbitrate-collision

Reads two loops' proposed writes for the same run window, checks each
pair for a genuine field-level collision, and applies a stated arbitration
rule to accept one write and reject the other — recording the rejection
and its reason rather than letting the later write silently overwrite the
earlier one.

## Instructions

You are a Claude Code skill implementing the `arbitration-edge` pattern.
Follow these steps in order:

1. **Read every proposed write from both loops for the run window.**
   Default to the writes in this kit's `README.md` unless the user gives
   you a different pair of loops or a different run.
2. **Group proposed writes by (node, field).** Two writes are only a real
   collision if they target the same node and the same field. Two writes
   to the same node but different fields are not a collision — both can
   be accepted independently, and neither needs arbitration.
3. **For each (node, field) group with more than one proposed write,**
   confirm the values actually disagree. If both loops proposed the same
   value, accept it once and note the duplicate — this isn't a
   collision either, just redundant agreement.
4. **Apply the stated arbitration rule to any genuine collision.** This
   kit's rule: a write anchored to a specific, individually verifiable
   event (e.g., an increment tied to a scanned return) takes precedence
   over a write that is an unanchored periodic snapshot, because the
   snapshot could already be stale by the time it lands. State the rule
   you applied explicitly in your report — never accept a write without
   naming why it won.
5. **Never silently drop the losing write.** Record it in full (its
   loop, its proposed value, its timestamp) alongside the reason it lost.
   A rejected write is data — the point of this pattern is that the
   collision itself becomes visible, not just its outcome.
6. **Never merge or average the two colliding values.** Arbitration picks
   one write as authoritative; it does not compute a compromise value
   that neither loop actually proposed.
7. **Report per (node, field) group**: either "no collision" (both writes
   accepted, or duplicate noted) or "collision resolved" (the accepted
   write, the rejected write, and the rule that decided between them).

## Input

- Proposed writes from two loops for the same run window, each naming
  the node, field, value, and timestamp (defaults to the writes in this
  kit's `README.md`).
- The arbitration rule to apply when a genuine collision is found.

## Output

- One accepted write per genuine collision, plus the rejected write and
  the reason it lost.
- Writes to different fields of the same node, passed through
  independently with no arbitration applied.

## Example Usage

```
Use the arbitrate-collision skill on the proposed writes in README.md.

Expected:
  SKU DO-4471, field stock-count: COLLISION RESOLVED
    Accepted: returns-processing, value 138, event-anchored (return scan
      at 14:02:01)
    Rejected: restock-sync, value 142, periodic snapshot taken 14:01:50
    Rule applied: event-anchored write beats unanchored periodic snapshot
      within the collision window.
  SKU DO-5820: NO COLLISION
    restock-sync wrote field stock-count (64); returns-processing wrote
      field reorder-flag (true) -- different fields, both accepted.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that every "collision
resolved" outcome names the specific rule applied (not just which loop
won), and that no pair of writes to different fields on the same node got
treated as a collision just because they shared a node id.
