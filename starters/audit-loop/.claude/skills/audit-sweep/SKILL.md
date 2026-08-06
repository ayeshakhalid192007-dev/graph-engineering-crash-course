---
name: audit-sweep
description: Reviews a full set of the main loop's outputs together, from a wider vantage than any single one of them, looking specifically for cross-item patterns that a one-item-at-a-time loop is structurally unable to notice
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# audit-sweep

Reads every output the main loop produced over a review window as one
set, rather than one at a time, and checks for patterns that only become
visible once multiple outputs are held in view together — reporting each
pattern found, and naming which items it spans.

## Instructions

You are a Claude Code skill implementing the `audit-loop` pattern. Follow
these steps in order:

1. **Read the main loop's full output set for the review window as a
   single batch**, not item by item. Default to the claims in this kit's
   `README.md` unless the user gives you a different window. Holding the
   whole set in view at once is the entire point — this step is what the
   main loop structurally cannot do from inside its own one-item scope.
2. **Do not re-check any single item against its own governing rule.**
   The main loop already checked each item against the rule meant for it
   (e.g., a claim against its own policy terms); re-litigating that isn't
   this skill's job and duplicates work the main loop already did
   correctly.
3. **Look specifically for cross-item patterns**: repeated values,
   repeated actors, or repeated structures that recur across otherwise
   unconnected items in the set. In this kit's scenario, that means
   near-identical repair line-item breakdowns from the same shop
   recurring across claims filed by different, unrelated policyholders.
4. **Require the recurring detail to actually match, not merely the
   surface actor.** Two items sharing a vendor or shop name is not itself
   the pattern — the line items, amounts, or structure have to line up
   closely enough that coincidence is implausible. A third item from the
   same shop with an unrelated breakdown is not part of the pattern; note
   it as checked and cleared, not swept in because the shop name matched.
5. **Name every item the pattern spans**, not just the first one noticed.
   A flag that only cites one claim isn't useful to whoever reviews it
   next — cite all of them, with the specific matching detail that ties
   them together.
6. **Do not resolve the pattern.** This skill's job is to surface it with
   enough specificity for a human or a downstream process to act on — it
   does not deny a claim, reverse an approval, or contact the shop
   itself.
7. **Report every pattern found**, and separately report which items in
   the set were reviewed and cleared, so a reader can tell "reviewed, no
   pattern" apart from "not reviewed."

## Input

- The main loop's full set of outputs for the review window (defaults to
  the claims in this kit's `README.md`).

## Output

- One report per pattern found, naming every item it spans and the
  specific matching detail.
- An explicit clear note for items reviewed and found to have no
  cross-item pattern.

## Example Usage

```
Use the audit-sweep skill on the week's claims in README.md.

Expected:
  PATTERN FOUND:
    Claims: MC-8801 (Reyes), MC-8809 (Okafor)
    Shared detail: both estimated by Alder Street Auto Body, both listing
      an identical three-line breakdown ($1,050 / $890 / $200) despite
      unrelated policyholders and unrelated accidents.
    Note: the main loop could not have caught this -- each claim was
      checked in isolation and individually satisfied its own policy
      terms.

  Reviewed, no pattern:
    MC-8815 (also Alder Street Auto Body, but a distinct bumper-only
      breakdown, $410 -- shop match alone is not the pattern).
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that every flagged pattern
names a specific recurring detail beyond "same shop" or "same actor," and
that every item in the review window appears in the report as either part
of a named pattern or explicitly cleared.
