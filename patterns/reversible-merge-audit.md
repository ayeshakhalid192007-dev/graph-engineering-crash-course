---
name: reversible-merge-audit
category: B-resolution
stage: write
cost: low
tools: [Claude Code]
core: false
---

# reversible-merge-audit

## What it does

Runs periodically over the graph's past merges, re-checking each one
against evidence that's arrived since, and reverses a merge if that new
evidence contradicts it.

## Inputs

- The graph's merge history (which mentions were merged into which
  canonical node, and when).
- Any evidence gathered since each merge was made.

## Outputs

- A confirmation for each merge that still holds.
- An unmerge action, restoring the earlier separate entities, for any merge
  the new evidence contradicts.

## Failure mode if skipped

A merge made in good faith at the time becomes permanent by default, even
after later evidence makes clear the two entities were never actually the
same thing.

## Link to starter kit

**Kit:** `starters/reversible-merge-audit/README.md`
