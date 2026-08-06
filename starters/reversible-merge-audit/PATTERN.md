---
name: reversible-merge-audit
category: B-resolution
stage: write
cost: low
tools: [Claude Code]
core: false
---

# reversible-merge-audit

This kit is the runnable companion to the `reversible-merge-audit`
pattern specification (`patterns/reversible-merge-audit.md`). It is an
extended kit — a single Claude Code reference implementation, lighter
than the full multi-tool anatomy the seven core kits carry. See
`starters/README.md` for that distinction.

## What it does

Looks back over merges the graph has already made and rechecks each one
against whatever evidence has arrived since. A merge that new evidence
directly contradicts gets reversed — split back into its original,
separate entities — and logged with the evidence that triggered the
reversal. A merge that still holds, including one new evidence actively
reaffirms, gets logged as confirmed rather than passed over in silence.

## Inputs

- The graph's merge history: which records were merged into which
  canonical node, and on what basis, and when.
- Evidence gathered since each merge — anything new that bears on
  whether the merge still holds.

## Outputs

- A confirmation entry for every merge the audit rechecked and found
  still valid.
- A reversal — restoring the pre-merge separate entities — for every
  merge that new evidence directly contradicts, with the contradicting
  evidence attached to the reversal record.

## Failure mode if skipped

A merge made in good faith at the time it happened becomes permanent by
default. Nothing ever goes back to ask whether it still holds, so once
evidence surfaces that the two original entities were never actually the
same thing, the graph keeps presenting them as one — quietly wrong for as
long as nobody happens to notice by hand.

## Worked scenario

Briarcombe University Library, a fictional institution, maintains a
citation graph where author identities occasionally get merged when two
name variants look like the same researcher. Six months ago, "J.
Alderman" and "James Alderman" were merged on the strength of a shared
department and overlapping publication years. A preprint posted last
week lists both names as separate co-authors on the same paper — direct
proof they're two different people. A second, older merge in the same
audit batch — "R. Kwan" and "Rachel Kwan," merged on a matching ORCID
id — gets reaffirmed rather than reversed, since the new evidence for
that one is a grant record repeating the same ORCID. See `README.md` for
the full merge history and evidence.

## Link to starter kit

**Kit:** `starters/reversible-merge-audit/README.md`
