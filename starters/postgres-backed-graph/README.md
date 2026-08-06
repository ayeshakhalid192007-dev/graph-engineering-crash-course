# postgres-backed-graph Starter Kit

A single-tool (Claude Code) reference kit for the **postgres-backed-graph**
pattern: laying the graph out as adjacency-list tables in Postgres and
wrapping every write to a shared edge in a transaction with a version
check, so concurrent writers serialize into well-ordered commits instead
of silently overwriting each other. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Copperlow Analytics and the rollout sequence below are invented for this
course, not drawn from any real company, incident, or deployment.

## Prerequisites

- Claude Code.
- No external services or API keys — the schema sketch and the write
  sequence below are everything the kit needs. This kit walks through
  the transactional reasoning a real Postgres connection would enforce;
  it doesn't require a running database to work through.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the table shape and the write sequence below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Table shape (adjacency-list)

```
edges(id, subject, predicate, object, version, updated_by, updated_at)
```

### Starting row (already committed)

`checkout-v2-flag --status--> rollout-45pct`, `version = 7`,
`updated_by = rollout-controller`, `updated_at = 09:14:02`.

### The write sequence

- **09:14:03.100** — `rollout-controller` reads the row at `version 7`
  and starts a transaction to write `rollout-55pct` (advancing the
  rollout further), computed against `version 7`.
- **09:14:03.140** — `incident-bot`, triggered by an error-rate alert
  that fired at `09:14:02.9`, independently reads the same row, still at
  `version 7` (this read happens before `rollout-controller`'s
  transaction has committed), and starts its own transaction to write
  `rolled-back`, also computed against `version 7`.
- **09:14:03.210** — `rollout-controller`'s transaction commits first:
  row moves to `version 8`, `rollout-55pct`.
- **09:14:03.245** — `incident-bot`'s transaction attempts to commit its
  write, still computed against `version 7`.

### Claude Code

1. Load the skill: `.claude/skills/transact-graph-write/SKILL.md`.
2. Ask it to run: "Use the transact-graph-write skill on the write
   sequence for checkout-v2-flag in README.md."
3. It prints the outcome of each writer's transaction, the row's final
   state, and whether either writer needed a retry.

## Expected Output

- **`rollout-controller`: straight through.** Version `7 → 8`,
  `checkout-v2-flag --status--> rollout-55pct`. Its transaction commits
  cleanly — it was first, and its write matched the version it was
  computed against.
- **`incident-bot`: rejected, then retried.** Its first commit attempt,
  still computed against `version 7`, is rejected — the row is already at
  `version 8`. The skill does not silently drop the write or discard the
  rollback intent: it re-reads the row's current state (`version 8`,
  `rollout-55pct`), recomputes the same intent — roll back — against that
  new state, and commits a fresh transaction: version `8 → 9`,
  `checkout-v2-flag --status--> rolled-back`.
- **Final state: `version 9`, `rolled-back`.** Both writers' intents
  landed, in a well-defined order, and the report shows the retry
  explicitly rather than presenting the outcome as if `incident-bot`'s
  write went through on the first try.

### Checking the result

- Confirm the final row state is `rolled-back` at `version 9` — the
  rollback must not be lost, even though it lost the race for `version
  8`.
- Confirm the report shows `incident-bot`'s write as rejected-then-
  retried, not as a single clean write — a report that hides the retry
  is hiding the exact mechanism this pattern depends on.
- Confirm no intermediate state shows a corrupted or interleaved value
  (such as a value that mixes fragments of both writers' intents) — every
  transition in the row's history should be one writer's complete,
  coherent write.

## Modifying the Example

1. Replace the table shape and the write sequence with your own
   concurrent-writer scenario.
2. Re-run the skill and confirm a writer whose write is rejected for a
   stale version always recomputes its actual intent against the new
   state before retrying, rather than either dropping the write or
   blindly reapplying its original stale values.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/transact-graph-write/SKILL.md` — the Claude Code
  skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Final state is `rollout-55pct`; the rollback never lands. | `incident-bot`'s stale-version write was silently dropped instead of being retried against the row's new state. |
| The row's version jumps straight from 7 to 9, skipping 8. | Both writers were allowed to write inside a shared transaction instead of each committing its own atomic, serialized transaction. |
| The retried write re-applies `rollout-controller`'s numbers instead of `incident-bot`'s rollback intent. | The retry replayed the original stale write instead of recomputing the writer's actual intent (roll back) against the current row state. |
| The report doesn't mention that `incident-bot` needed a retry. | Every write needs its outcome reported honestly — straight through, or rejected-then-retried — not simplified to just the final value. |

## Next Steps

- Review `patterns/postgres-backed-graph.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
