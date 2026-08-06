---
name: alias-merge-with-trail
category: B-resolution
stage: write
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# alias-merge-with-trail

## What it does

Merges two surface names that refer to the same entity while keeping both
original mentions attached to the merged node as evidence, rather than
collapsing them into a single unlabeled record (this is the reversible
resolution move from Step 7).

## Inputs

- A candidate pair (or small cluster) of node names flagged as possible
  aliases for the same entity.

## Outputs

- One canonical entity node.
- Both original mentions retained and linked to it as evidence, not
  deleted.

## Failure mode if skipped

Merges happen silently and destructively — once the two original mentions
are gone, there's no way to trace why the merge happened or to undo it if
it turns out to be wrong.

## Link to starter kit

**Kit:** `starters/alias-merge-with-trail/README.md`
