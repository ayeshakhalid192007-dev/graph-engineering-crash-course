# early-victory-guard Starter Kit

A single-tool (Claude Code) reference kit for the **early-victory-guard**
pattern: blocking a loop from marking a task complete until the grounded
checker has actually run against that exact task, so "done" always has a
verification step behind it. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Hollowreed Software and the support tickets below are invented for this
course, not drawn from any real company or product.

## Prerequisites

- Claude Code.
- No external services or API keys — the tickets and checker log below
  are everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the tickets and checker log below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Proposed "done" signals (from the triage loop)

- `HR-2231` — "Export button times out for accounts with >10k rows."
  Proposed resolution: "Root cause is pagination limit in
  export-service (edge: export-service --root-cause-->
  pagination-limit-hardcoded), fixed in PR #884." Proposed done.
- `HR-2244` — "Dashboard widget shows stale data." Proposed resolution:
  "Root cause is cache-invalidation delay in widget-service, fixed in PR
  #891." Proposed done.
- `HR-2258` — "Notification emails duplicate on retry." Proposed
  resolution: "Root cause is missing idempotency key in
  notification-service, fixed in PR #897." Proposed done.

### Checker's run log

- `HR-2244` — checker ran, result: PASS. Confirmed the cited
  cache-invalidation edge exists and the cited PR matches the graph's
  fix record.
- `HR-2255` — checker ran, result: PASS. (Note: this entry is for ticket
  HR-2255, not HR-2258.)

`HR-2231` has no entry in the run log at all.

### Claude Code

1. Load the skill: `.claude/skills/gate-task-completion/SKILL.md`.
2. Ask it to run: "Use the gate-task-completion skill on the tickets and
   checker log in README.md."
3. It prints one outcome — PASS or BLOCKED — per ticket, with reasons.

## Expected Output

- **`HR-2231`: BLOCKED.** No checker log entry exists for `HR-2231` at
  all — the resolution note is plausible, but nothing separately
  confirmed the cited root-cause edge.
- **`HR-2244`: PASS.** The checker log has an entry keyed to `HR-2244`
  itself, and it ran and passed.
- **`HR-2258`: BLOCKED.** The only nearby log entry is keyed to
  `HR-2255` — a different ticket id. That's not coverage for `HR-2258`,
  even though it's easy to misread at a glance.

### Checking the result

- Confirm `HR-2244` is the only ticket marked PASS, and that the PASS
  cites the exact matching log entry.
- Confirm both `HR-2231` and `HR-2258` are BLOCKED, each with the
  specific reason named (no entry at all, versus a mismatched entry).
- Confirm no ticket's outcome depends on how convincing its resolution
  note reads — only on whether the checker log has a matching entry.

## Modifying the Example

1. Replace the tickets and checker log with your own task ids and run
   log.
2. Re-run the skill and confirm it blocks any task without an exact
   task-id match in the log, including near-miss mismatches, and passes
   only genuine matches.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/gate-task-completion/SKILL.md` — the Claude Code
  skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `HR-2231` is marked PASS. | The skill let a well-written resolution note substitute for an actual checker log entry. Re-run and check step 4 of `SKILL.md` ran before any pass decision. |
| `HR-2258` is marked PASS. | The skill matched `HR-2255`'s log entry to `HR-2258` on rough similarity instead of requiring an exact task-id match. |
| `HR-2244` is marked BLOCKED. | The skill failed to find the log entry that does exist for `HR-2244` — check the id comparison isn't doing something like trimming or reformatting the id before matching. |
| A ticket is missing an outcome entirely. | Every proposed "done" signal needs a stated PASS or BLOCKED outcome — silence on any ticket is itself a bug in the report. |

## Next Steps

- Review `patterns/early-victory-guard.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
