---
name: transact-graph-write
description: Wraps every write to a shared graph edge in a transaction tied to the exact row version it was computed against, and retries a rejected write against the row's current state instead of dropping it or blindly reapplying stale values
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# transact-graph-write

Reads a shared edge row's current version before writing to it, commits
the write only if that version still matches, and on a rejected write
re-reads the row's new state and recomputes the writer's actual intent
against it before retrying — never dropping the write and never reapplying
stale values.

## Instructions

You are a Claude Code skill implementing the `postgres-backed-graph`
pattern. Follow these steps in order:

1. **Read the target edge row's current state inside a transaction**,
   including its `version` marker — never read the row and decide on a
   write outside a transaction boundary. Default to the
   `checkout-v2-flag` write sequence in this kit's `README.md` unless
   given a different one.
2. **Compute the intended write against the version just read**, and
   before committing, check that version still matches the row's current
   version. If it does, write the new state, increment the version, and
   commit — all inside the same transaction.
3. **If the version no longer matches** — someone else's write committed
   to this row since this write was computed — do not commit a blind
   overwrite. Abort this transaction.
4. **On abort, re-read the row's now-current state**, and recompute the
   writer's actual intent against that new state, not against the stale
   state the first attempt used. The retry must still accomplish what the
   writer originally meant (e.g. "roll back" is still "roll back"),
   reapplied to the row as it now stands — never a blind replay of the
   original write's literal values.
5. **Retry the write as a new transaction** against the current version,
   following the same check-then-commit logic as step 2. If it's rejected
   again, repeat steps 3–5.
6. **Never let two writers' transactions interleave a partial write to
   the same row.** Every write to a given edge happens as one atomic
   transaction, from the initial read-and-lock through commit, with
   nothing else touching that row in between.
7. **Log every committed write** with `updated_by` and `updated_at`, so a
   later reader can reconstruct the actual order writes landed in, not
   just infer it from the final value.
8. **Report, per writer**: the version it started from, the version it
   ended on, the final value it wrote, and whether it committed straight
   through or needed one or more retries due to a concurrent conflicting
   write.

## Input

- The table shape and starting row state (defaults to the
  `checkout-v2-flag` edge in this kit's `README.md`).
- The write sequence: each writer's read time, intended write, and
  attempted commit time (defaults to `rollout-controller` and
  `incident-bot` in `README.md`).

## Output

- The row's final committed state.
- A per-writer report: starting version, ending version, final value
  written, and whether a retry was needed.

## Example Usage

```
Use the transact-graph-write skill on the write sequence for
checkout-v2-flag in README.md.

Expected:
  rollout-controller:
    Read version 7 at 09:14:03.100 -> wrote rollout-55pct
    Committed straight through: version 7 -> 8

  incident-bot:
    Read version 7 at 09:14:03.140 -> wrote rolled-back
    First commit attempt REJECTED (row now at version 8)
    Re-read row: version 8, rollout-55pct
    Recomputed intent (roll back) against version 8 -> retried
    Committed: version 8 -> 9

  Final state: checkout-v2-flag --status--> rolled-back (version 9)
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check two things: that no writer's
report claims a clean single commit when a version conflict actually
occurred, and that every retry's committed value reflects the writer's
real intent recomputed against the current row, not a stale value carried
forward from its first, rejected attempt.
