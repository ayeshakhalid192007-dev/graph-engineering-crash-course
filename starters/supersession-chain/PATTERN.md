---
name: supersession-chain
category: C-provenance
stage: write
cost: low
tools: [Claude Code]
core: false
---

# supersession-chain

This kit is the runnable companion to the `supersession-chain` pattern
specification (`patterns/supersession-chain.md`). It is an extended kit —
a single Claude Code reference implementation, lighter than the full
multi-tool anatomy the seven core kits carry. See `starters/README.md` for
that distinction.

## What it does

When a claim already in the graph turns out to be wrong, this pattern adds
a brand-new node holding the corrected version instead of editing the old
node's fields in place. The old node stays exactly as it was, flagged
stale, and a `supersedes` edge runs from the new node back to it — so the
graph can still answer "what did we used to believe, and when did that
change" long after the correction lands.

## Inputs

- An existing claim node, still marked current.
- A newer claim that contradicts it, with its own source.

## Outputs

- A new node holding the corrected claim.
- A `supersedes` edge from the new node to the old one.
- The old node, retained in the graph and flagged stale rather than
  deleted or overwritten.

## Failure mode if skipped

Overwriting the wrong claim in place destroys the record that the graph
ever believed it, along with whatever evidence had once made that belief
look reasonable. Anything downstream that was built, decided, or shipped
on the strength of the old value — a report, a label, a prior sign-off —
becomes unexplainable after the fact, because the graph itself no longer
shows there was ever anything to explain.

## Worked scenario

Bellhaven Materials Lab, a fictional testing house, keeps a graph of
safety facts extracted from vendor safety-data sheets. A 2019 revision of
polymer XR-9's data sheet was OCR-transcribed into a claim node stating a
flash point of 210°C. A 2024 revision, retested under ASTM D93, states the
flash point is actually 185°C — the original figure was a transcription
error, not a change in the polymer itself. The lab's density claim for the
same polymer, extracted from the same 2019 sheet, is untouched by either
revision and should not be swept up in the correction. See `README.md` for
the full claim records and how the kit processes them.

## Link to starter kit

**Kit:** `starters/supersession-chain/README.md`
