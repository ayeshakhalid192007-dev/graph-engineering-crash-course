---
name: early-victory-guard
category: E-checker
stage: read
cost: low
tools: [Claude Code]
core: false
---

# early-victory-guard

## What it does

Blocks a loop from marking its task complete until the grounded checker has
actually run against that task at least once, so "done" always has at
least one verification step behind it.

## Inputs

- A loop's proposed "done" signal for a task.
- The checker's run log for that same task.

## Outputs

- Either a pass-through allowing the loop to complete, or a block that
  returns the loop to its work with the missing check named.

## Failure mode if skipped

A loop can declare victory before anything about its output has actually
been verified — the "done" signal and the checking step never had to touch.

## Link to starter kit

**Kit:** `starters/early-victory-guard/README.md`
