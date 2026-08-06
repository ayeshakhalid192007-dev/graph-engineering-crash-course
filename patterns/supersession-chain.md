---
name: supersession-chain
category: C-provenance
stage: write
cost: low
tools: [Claude Code]
core: false
---

# supersession-chain

## What it does

When a claim turns out to be wrong, adds a new node that supersedes it
rather than editing the old node in place — the old claim stays in the
graph, marked stale, instead of being erased.

## Inputs

- An existing claim node.
- A newer claim that contradicts it.

## Outputs

- A new node holding the corrected claim.
- A `supersedes` edge from the new node to the old one, with the old node
  retained and flagged stale rather than deleted.

## Failure mode if skipped

Overwriting the wrong claim in place destroys the record that the graph
ever believed it, along with whatever evidence had once made that belief
look reasonable.

## Link to starter kit

**Kit:** `starters/supersession-chain/README.md`
