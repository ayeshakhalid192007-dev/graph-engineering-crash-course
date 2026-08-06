---
name: score-and-merge
description: Scores candidate merge pairs on weighted signals and auto-merges only pairs clearing a stated threshold, routing the rest to a review queue with their score and signal breakdown attached
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# score-and-merge

Computes a numeric confidence score for every candidate merge pair from a
fixed set of weighted signals, then splits the batch into auto-merged
pairs and a review queue based purely on whether that score clears the
threshold — never on how similar the pair "looks."

## Instructions

You are a Claude Code skill implementing the `confidence-scored-dedup`
pattern. Follow these steps for every candidate pair in the batch:

1. **Read the scoring rule before touching any pair.** Note each
   signal's weight (tax ID match, name token overlap, address match in
   this kit's rule) and the threshold that separates auto-merge from
   review queue. Treat these as fixed for the run — don't invent an
   extra signal or adjust a weight mid-pass because one pair "feels"
   borderline.
2. **Score each signal independently.** For tax ID and address, this is
   a binary match/no-match. For name token overlap, compare the
   significant words in each name (ignoring corporate suffixes like
   "Co.," "Ltd," "Inc." when judging overlap, but still recording if
   only the suffix differs) and estimate the overlap fraction, then scale
   it by the signal's weight.
3. **Sum the signals into one total score per pair.** Show your work —
   report each signal's contribution, not just the final number, so a
   reviewer can see why a pair scored the way it did.
4. **Compare the total to the threshold, and only the total.** A single
   strong or weak signal must not override the sum — a pair with a
   matching tax ID but a mismatched address is decided by whether the
   sum of all three signals clears the threshold, not by treating the
   address mismatch as an automatic veto.
5. **Route pairs at or above threshold to auto-merge.** Produce one
   canonical record per merged pair, and state which two source records
   fed into it.
6. **Route pairs below threshold to the review queue.** Each queue entry
   must carry the pair, its total score, and the per-signal breakdown —
   never just "below threshold" with no explanation of which signals
   failed.
7. **Report both outputs together**: the auto-merged set with scores, and
   the review queue with scores and signal breakdowns. A run that reports
   only the merges, or only the queue, has not finished this step.

## Input

- The scoring rule: signals, their weights, and the threshold (defaults
  to the rule given in this kit's `README.md`).
- A batch of candidate merge pairs (defaults to the three pairs in
  `README.md`).

## Output

- Auto-merged pairs, each with its total score and a canonical record
  combining the two sources.
- A review queue of below-threshold pairs, each with its total score and
  per-signal breakdown.

## Example Usage

```
Use the score-and-merge skill on the candidate pairs in README.md, using
the scoring rule and 0.75 threshold given there.

Expected:
  Pair A (Ashgrove Steel Co. / Ashgrove Steel Company): 0.97 -> auto-merge
  Pair B (Bell Castle Ltd / Bellcastle Logistics): 0.18 -> review queue
  Pair C (Whitmore & Sons Supply / Whitmore and Sons): 0.78 -> auto-merge
    (tax ID match carries the score despite the address mismatch)
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that every merge decision
traces back to a shown score, and that no single signal was allowed to
override the threshold comparison on its own.
