---
name: conversation-to-claims
category: A-extraction
stage: write
cost: medium
tools: [Claude Code]
core: false
---

# conversation-to-claims

## What it does

Watches an agent conversation for facts asserted along the way and writes
each one out as a provisional claim node, pending resolution, instead of
leaving those assertions to live only inside the transcript.

## Inputs

- A conversation transcript, or a live stream of agent turns.
- The claim-node schema the pattern writes into.

## Outputs

- Provisional claim nodes, unresolved and unmerged, each flagged for the
  resolution stage to pick up.

## Failure mode if skipped

Anything asserted mid-conversation disappears the moment that transcript
gets summarized, trimmed, or closed — there was never a second place it was
recorded.

## Link to starter kit

**Kit:** `starters/conversation-to-claims/README.md`
