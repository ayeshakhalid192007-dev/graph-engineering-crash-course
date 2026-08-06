# arbitration-edge Starter Kit

A single-tool (Claude Code) reference kit for the **arbitration-edge**
pattern: deciding which of two loops wins when both act on the same
resource at the same time, by a stated rule rather than by whichever
write happens to land last. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Driftwood Outfitters and the two loops below are invented for this
course, not drawn from any real retailer or inventory system.

## Prerequisites

- Claude Code.
- No external services or API keys — the proposed writes below are
  everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the proposed writes below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Proposed writes (this run window)

- SKU `DO-4471`, field `stock-count`:
  - `restock-sync` proposes `142`, timestamp 14:01:50 — a periodic
    snapshot read from the warehouse system.
  - `returns-processing` proposes `138`, timestamp 14:02:01 — an
    increment anchored to a specific scanned return event.
- SKU `DO-5820`:
  - `restock-sync` proposes field `stock-count` = `64`, timestamp
    14:03:10 — a periodic snapshot.
  - `returns-processing` proposes field `reorder-flag` = `true`,
    timestamp 14:03:12 — an unrelated field on the same SKU.

### Arbitration rule

A write anchored to a specific, individually verifiable event (like an
increment tied to a scanned return) takes precedence over an unanchored
periodic snapshot on the same node and field, because the snapshot could
already be stale by the time it lands.

### Claude Code

1. Load the skill: `.claude/skills/arbitrate-collision/SKILL.md`.
2. Ask it to run: "Use the arbitrate-collision skill on the proposed
   writes in README.md."
3. It prints one outcome per (node, field) group: no collision, or
   collision resolved with the accepted write, the rejected write, and
   the rule applied.

## Expected Output

- **SKU `DO-4471`, field `stock-count`: COLLISION RESOLVED.** Accepted:
  `returns-processing`'s `138` (event-anchored). Rejected:
  `restock-sync`'s `142` (unanchored snapshot, preempted by the rule
  above).
- **SKU `DO-5820`: NO COLLISION.** `restock-sync` wrote `stock-count`;
  `returns-processing` wrote the unrelated `reorder-flag` field — both
  accepted independently, no arbitration needed.

### Checking the result

- Confirm the DO-4471 output names both the accepted and the rejected
  write, with the rule that decided between them stated explicitly.
- Confirm DO-5820's two writes are **not** treated as a collision — same
  SKU, different fields.
- Confirm neither output averages or blends the two `DO-4471` values
  into something neither loop actually proposed.

## Modifying the Example

1. Replace the proposed writes and the arbitration rule with your own
   loops, resource, and priority logic.
2. Re-run the skill and confirm it only treats same-node-same-field
   disagreements as collisions, and that every collision's report names
   the specific rule applied — not just which loop happened to win.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/arbitrate-collision/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| DO-5820's two writes get reported as a collision. | The skill grouped writes by node alone instead of by (node, field) — writes to different fields of the same node are never a real collision. |
| DO-4471's accepted value is an average or blend of 142 and 138. | The skill computed a compromise value instead of accepting one write outright per the stated rule. Arbitration picks a winner; it never blends. |
| The rejected write (142) doesn't appear anywhere in the output. | A collision's losing write must still be recorded with its value and the reason it lost — it can't just be dropped in favor of reporting the winner alone. |
| `restock-sync` wins the DO-4471 collision instead of `returns-processing`. | The skill didn't apply the stated rule (event-anchored beats unanchored snapshot) — check it read the rule from README.md rather than defaulting to "most recent timestamp wins" or "first loop wins." |

## Next Steps

- Review `patterns/arbitration-edge.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
