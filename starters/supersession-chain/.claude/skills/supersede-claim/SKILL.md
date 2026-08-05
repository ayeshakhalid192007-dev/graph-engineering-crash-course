---
name: supersede-claim
description: Corrects a wrong claim by adding a new node holding the correction and a supersedes edge back to the old node, which stays in the graph flagged stale rather than being edited or deleted
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# supersede-claim

Reads an existing claim and a piece of new evidence, decides whether the
new evidence actually corrects that claim, and if so adds a new node for
the correction plus a `supersedes` edge — leaving the old node in place,
flagged stale, never overwritten.

## Instructions

You are a Claude Code skill implementing the `supersession-chain`
pattern. Follow these steps in order:

1. **Read every existing claim first**, noting its id, its stated value,
   its source, and its current status. Hold the full set in mind — you
   need to check the new evidence against all of them, not just the one
   you expect it to correct.
2. **Read the new evidence.** Default to the claims and evidence in this
   kit's `README.md` unless the user gives you different ones.
3. **For each existing claim, decide whether the new evidence directly
   corrects it.** "Directly corrects" means the new evidence states a
   different value for the same fact the claim asserts, or explicitly
   says the old value was wrong. Evidence that comes from the same source
   document but addresses a different fact does not correct anything —
   check each claim on its own terms, not by association with whatever
   else in the document changed.
4. **For every claim the new evidence does not correct, leave it
   untouched.** Do not change its status, its value, or anything else
   about it. Say explicitly in your report that you checked it and found
   no correction, so a reader can tell "checked and unaffected" apart
   from "never looked at."
5. **For every claim the new evidence does correct, create a new node**
   holding the corrected value and its own source (the new evidence),
   with a fresh id distinct from the old claim's id.
6. **Add one `supersedes` edge per correction**, from the new node to the
   old node it corrects. The direction matters: the new node supersedes
   the old one, never the reverse.
7. **Update the old node's status to `stale`.** Do not delete it, do not
   overwrite its value or source fields — the only thing that changes on
   the old node is its status.
8. **Report the result**: for every existing claim, either "unchanged"
   (with a one-line reason) or "superseded" (with the new node's id, the
   edge, and the old node's new status). Never report a claim without one
   of these two outcomes.

## Input

- The graph's existing claim nodes (id, value, source, status).
- New evidence to check against them (defaults to the evidence listed in
  this kit's `README.md`).

## Output

- One outcome per existing claim: unchanged, or superseded with a new
  node, a `supersedes` edge, and the old node's status flipped to stale.

## Example Usage

```
Use the supersede-claim skill on the existing claims and new evidence in
README.md.

Expected:
  claim-xr9-flashpoint-2019: SUPERSEDED
    New node: claim-xr9-flashpoint-2024 ("185°C, ASTM D93 retest")
    Edge: claim-xr9-flashpoint-2024 --supersedes--> claim-xr9-flashpoint-2019
    Old node status: current -> stale (value and source unchanged)
  claim-xr9-density-2019: UNCHANGED
    Reason: 2024 revision C does not mention density; nothing to correct.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check two things: that no existing
node's value or source field was edited (only status may change, and only
on nodes actually superseded), and that every claim not touched by the
new evidence still shows an explicit "unchanged" outcome rather than
being silently dropped from the report.
