---
name: conversation-to-claims
category: A-extraction
stage: write
cost: medium
tools: [Claude Code]
core: false
---

# conversation-to-claims

This kit is the runnable companion to the `conversation-to-claims`
pattern specification (`patterns/conversation-to-claims.md`). It is an
extended kit — a single Claude Code reference implementation rather than
the full multi-tool anatomy the seven core kits carry. See
`starters/README.md` for what that distinction means here.

## What it does

Walks a conversation turn by turn and pulls out every sentence that
asserts something about the world — as opposed to a question, a request,
or small talk — and writes it out as a provisional claim node. Nothing
gets resolved, merged, or upgraded to a confirmed fact at this stage;
hedged language ("might be," "I think," "not certain") stays marked as
hedged rather than getting smoothed into a flat assertion.

## Inputs

- A conversation transcript, either complete or a live stream of turns.
- The claim-node schema the pattern writes into (subject/predicate/object
  where the sentence supports it, plus speaker, turn number, and a
  confidence flag for hedged language).

## Outputs

- One provisional claim node per factual assertion found, each flagged
  unresolved and awaiting whatever downstream stage does resolution.

## Failure mode if skipped

An assertion made mid-conversation exists only inside that transcript.
Once the transcript gets summarized for a handoff, trimmed for context
budget, or simply closed, whatever was said is gone — there was never a
second place it got written down, so a later reader has no way to check
what was actually claimed versus what a summary later implied.

## Worked scenario

A customer support chat for Coldharbor Appliances, a fictional
manufacturer of household refrigerators, runs between a customer and a
support agent about a rattling noise coming from a unit. Across six turns
the customer states when the compressor was last serviced and when the
rattling started, the agent states the unit's warranty end date, and the
agent also offers a guess about the cause that's explicitly hedged rather
than stated outright. See `README.md` for the full transcript and how the
kit turns it into claim nodes.

## Link to starter kit

**Kit:** `starters/conversation-to-claims/README.md`
