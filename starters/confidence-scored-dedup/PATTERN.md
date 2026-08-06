---
name: confidence-scored-dedup
category: B-resolution
stage: write
cost: medium
tools: [Claude Code]
core: false
---

# confidence-scored-dedup

This kit is the runnable companion to the `confidence-scored-dedup`
pattern specification (`patterns/confidence-scored-dedup.md`). It is an
extended kit — a single Claude Code reference implementation, lighter
than the full multi-tool anatomy the seven core kits carry. See
`starters/README.md` for that distinction.

## What it does

Takes a batch of candidate merge pairs and computes an explicit numeric
confidence score for each one from a fixed set of weighted signals,
rather than eyeballing which pairs "look like" duplicates. Pairs that
clear a stated threshold get merged automatically; everything below it
goes to a review queue with the score and the signals behind it attached,
so a human reviewer isn't starting from nothing.

## Inputs

- A set of candidate merge pairs — two records proposed as possibly the
  same underlying entity.
- A similarity signal set per pair (this kit uses tax-ID match, name
  token overlap, and address match) that combines into one confidence
  score, plus the threshold that separates auto-merge from review.

## Outputs

- The subset of candidate pairs whose score cleared the threshold,
  merged into a single canonical record.
- A review queue holding every pair that didn't clear it, each carrying
  its score and which signals did and didn't match.

## Failure mode if skipped

Without scoring, a team ends up doing one of two things badly: merging
every candidate pair on sight regardless of how weak the match actually
is, silently corrupting records that were never the same entity, or
piling up every unresolved candidate in a backlog that keeps growing
because nothing distinguishes an obvious match from a genuinely uncertain
one worth a human's time.

## Worked scenario

Fenwick & Vance Procurement, a fictional purchasing firm, merges its
vendor database with an acquired company's after a buyout. Three
candidate pairs come out of that merge: one where the same tax ID and a
near-identical name make the match obvious, one where the names are
superficially similar but the tax ID and address both differ, and one
where the tax ID matches exactly but the two addresses point to what
turns out to be a satellite office of the same vendor. See `README.md`
for the full candidate set and how the kit scores each pair.

## Link to starter kit

**Kit:** `starters/confidence-scored-dedup/README.md`
