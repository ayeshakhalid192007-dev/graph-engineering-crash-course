---
name: recheck-merges
description: Rechecks each past merge in the graph's history against evidence gathered since, reversing any merge new evidence directly contradicts and logging an explicit confirmation for every merge that still holds
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# recheck-merges

Walks the graph's merge history and, for every past merge, decides
whether new evidence leaves it standing or contradicts it outright. A
contradicted merge gets reversed and the contradiction recorded; every
other merge gets an explicit confirmation entry, never silence.

## Instructions

You are a Claude Code skill implementing the `reversible-merge-audit`
pattern. For every merge in the history, in order:

1. **Read the merge's original basis first.** Know exactly what claim
   the merge rested on (shared department and overlapping publication
   years, a matching ORCID, or whatever the history records) before
   looking at new evidence — you need to know what would actually
   contradict it.
2. **Gather every piece of new evidence tied to this merge.** Evidence
   "tied to" a merge means it bears on whether the two originally-merged
   entities are really one thing — not just any new record that happens
   to mention one of the names.
3. **Test each piece of evidence against the merge's basis, specifically
   for direct contradiction.** Direct contradiction means the evidence
   is incompatible with the merge being correct — for example, the same
   paper listing both name variants as two separate co-authors, which
   cannot happen if they're the same person. A record that's merely
   silent on the question, or that talks about one name variant without
   addressing the other, is not a contradiction.
4. **Reaffirming evidence is not grounds for anything except
   confirmation.** If new evidence repeats or reinforces the merge's
   original basis (the same ORCID showing up again, for instance), that
   strengthens the case for leaving the merge alone — it must never be
   read as grounds to reverse.
5. **If you found a direct contradiction, reverse the merge.** Split the
   canonical node back into its original separate entities, and record
   the specific evidence that triggered the reversal alongside it — a
   reversal with no stated evidence is not distinguishable from an
   accidental un-merge and should never be produced.
6. **If you found no direct contradiction, confirm the merge.** Write an
   explicit confirmation entry — not just an absence of a reversal
   entry — naming which evidence was checked and that none of it
   contradicted the original basis. Every merge in the history needs one
   of these two outcomes; neither is optional and neither should be
   inferred by silence.
7. **Report every merge's outcome together**, in history order:
   confirmed or reversed, and the evidence that decided it either way.

## Input

- The graph's merge history: canonical node, the entities merged into
  it, and the original basis for each merge.
- New evidence gathered since each merge (defaults to the evidence listed
  in this kit's `README.md`).

## Output

- One outcome per merge in the history: confirmed (with evidence
  checked) or reversed (with the split entities and the contradicting
  evidence).

## Example Usage

```
Use the recheck-merges skill on the merge history and evidence in
README.md.

Expected:
  Merge 1 (author-alderman-j): REVERSED
    Evidence: preprint listing J. Alderman and James Alderman as two
    separate co-authors on the same paper — direct contradiction.
    Restored: "J. Alderman" and "James Alderman" as separate entities.
  Merge 2 (author-kwan-r): CONFIRMED
    Evidence checked: grant record repeating ORCID 0000-0002-4471-XXXX —
    reaffirms the original basis, no contradiction found.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that every merge in the
history has exactly one outcome (never zero, never both), and that any
reversal names the specific contradicting evidence rather than a general
sense that "something changed."
