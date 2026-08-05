# budget-capped-subgraph Starter Kit

A single-tool (Claude Code) reference kit for the
**budget-capped-subgraph** pattern: trimming a task-scoped subgraph down
to a hard node-count ceiling, keeping the anchor plus the highest-relevance
nodes and recording exactly where the cutoff fell, instead of handing a
worker an ever-growing draw with no limit. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Northbridge Legal Aid Clinic and the client case below are invented for
this course, not drawn from any real clinic or client's records.

## Prerequisites

- Claude Code.
- No external services or API keys — the candidate subgraph below is
  everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the candidate subgraph and the budget below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Candidate subgraph (before budget applied)

Anchor node (always kept): `client-ferreira-o`.

Other nodes, by relevance score:

| Node | Relevance |
| --- | --- |
| `filing-eviction-notice-2026-03` | 0.95 |
| `filing-answer-2026-03` | 0.90 |
| `hearing-2026-04-12` | 0.88 |
| `party-landlord-hollis-mgmt` | 0.80 |
| `statute-tenant-protection-act-12` | 0.75 |
| `filing-motion-continuance-2026-04` | 0.60 |
| `party-co-tenant-vasquez` | 0.55 |
| `note-intake-call-2026-02` | 0.50 |
| `party-prior-attorney-ng` | 0.40 |
| `filing-unrelated-parking-dispute-2024` | 0.20 |
| `party-property-manager-other` | 0.15 |

Edges:

- `client-ferreira-o --subject_of--> filing-eviction-notice-2026-03`
- `client-ferreira-o --subject_of--> filing-answer-2026-03`
- `client-ferreira-o --scheduled_for--> hearing-2026-04-12`
- `filing-eviction-notice-2026-03 --filed_by--> party-landlord-hollis-mgmt`
- `filing-answer-2026-03 --cites--> statute-tenant-protection-act-12`
- `client-ferreira-o --filed--> filing-motion-continuance-2026-04`
- `client-ferreira-o --shares_lease_with--> party-co-tenant-vasquez`
- `client-ferreira-o --subject_of--> note-intake-call-2026-02`
- `note-intake-call-2026-02 --taken_by--> party-prior-attorney-ng`
- `client-ferreira-o --party_to--> filing-unrelated-parking-dispute-2024`
- `filing-unrelated-parking-dispute-2024 --filed_by--> party-property-manager-other`

### Budget

Maximum 8 nodes per draw (the clinic's intake assistant's fixed ceiling).

### Claude Code

1. Load the skill: `.claude/skills/trim-to-budget/SKILL.md`.
2. Ask it to run: "Use the trim-to-budget skill on the candidate subgraph
   and budget in README.md."
3. It prints the kept nodes, the dropped nodes, the surviving edges, and
   the trimming rule it applied.

## Expected Output

- **Kept (8 nodes):** `client-ferreira-o` (anchor, forced), plus the top
  seven by relevance — `filing-eviction-notice-2026-03` (0.95),
  `filing-answer-2026-03` (0.90), `hearing-2026-04-12` (0.88),
  `party-landlord-hollis-mgmt` (0.80),
  `statute-tenant-protection-act-12` (0.75),
  `filing-motion-continuance-2026-04` (0.60),
  `party-co-tenant-vasquez` (0.55).
- **Dropped (4 nodes):** `note-intake-call-2026-02` (0.50),
  `party-prior-attorney-ng` (0.40),
  `filing-unrelated-parking-dispute-2024` (0.20),
  `party-property-manager-other` (0.15).
- **Trimming rule recorded:** "Anchor kept unconditionally; remaining
  nodes kept in descending relevance order until the 8-node budget was
  filled; cutoff fell at relevance 0.55, dropping everything at or below
  0.50."
- **Surviving edges (7):** the seven edges whose both endpoints are among
  the 8 kept nodes.
- **Dropped edges (4):** the four edges that touched at least one of the
  dropped nodes (both edges involving `note-intake-call-2026-02`, and
  both edges involving `filing-unrelated-parking-dispute-2024`).

### Checking the result

- Confirm the kept set is exactly 8 nodes, not 7 or 9 — an off-by-one on
  the anchor is the most common way this goes wrong.
- Confirm every dropped edge touches at least one dropped node, and no
  surviving edge does.
- Confirm the trimming rule is stated explicitly in the output, naming
  the actual cutoff score (0.55) — not just "some nodes were dropped."

## Modifying the Example

1. Replace the candidate subgraph, relevance scores, and budget with your
   own.
2. Re-run the skill and confirm the anchor is always kept regardless of
   budget size, and that the cutoff score reported matches the lowest
   relevance score actually kept.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/trim-to-budget/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| The kept set has 9 nodes. | The skill counted the anchor separately from the budget instead of counting it as one of the 8. |
| A surviving edge points at a dropped node. | The skill trimmed nodes but forgot to re-check every edge's endpoints against the final kept set afterward. |
| The trimming rule doesn't name the cutoff score. | The skill reported which nodes were dropped without stating the relevance threshold that decided it — the rule must be legible on its own, not just implied by the node list. |

## Next Steps

- Review `patterns/budget-capped-subgraph.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
