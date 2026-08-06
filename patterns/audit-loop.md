---
name: audit-loop
category: F-governance
stage: governance
cost: medium
tools: [Claude Code]
core: false
---

# audit-loop

## What it does

Runs a separate loop, positioned with a wider vantage point than the main
loop, that periodically reviews territory the main loop structurally can't
see from inside its own operating scope.

## Inputs

- The main loop's outputs and history.
- A vantage point outside the main loop's own scope to review them from.

## Outputs

- A periodic report naming classes of problem the main loop couldn't have
  caught on its own.

## Failure mode if skipped

An entire category of problem stays invisible indefinitely, because the
only loop positioned to catch it is also the one structurally unable to see
it.

## Link to starter kit

**Kit:** `starters/audit-loop/README.md`
