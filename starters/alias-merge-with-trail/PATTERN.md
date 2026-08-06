---
name: alias-merge-with-trail
category: B-resolution
stage: write
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# alias-merge-with-trail

This kit is the runnable companion to the `alias-merge-with-trail` pattern
specification (`patterns/alias-merge-with-trail.md`). It works one concrete
scenario end to end: a fictional freight company's customer-support queue
and its infrastructure change log each describe the same backend system,
but neither one uses the other's name for it, and the kit has to decide
whether they're describing one thing or two.

## What it does

Takes surface names pulled from separate sources and decides, on the
strength of a stated, checkable reason, whether they belong to one
underlying entity. When they do, it produces a single canonical node but
keeps every surface string that fed into that decision sitting alongside
it as its own record, so a later lookup keyed on any one of the original
names still finds the entity and the evidence behind the merge. When the
evidence is thin, it declines to merge and says so, rather than guessing.

## Inputs

- Two (or more) surface names, each tied to the source document it came
  from, that might refer to the same underlying system. This kit ships
  `sample-input.md`, which pairs a customer-support ticket against an
  infrastructure change log for a fictional company, Meridian Freight.
- A schema fixing the shape of a canonical entity and of a retained
  mention record. This kit ships `schema.example.json`, which defines one
  `Service` entity type and one mention shape (`surface`, `source`,
  `retrievable`).

## Outputs

- One canonical entity per group of mentions judged to name the same
  system, carrying a `merge_reason` written in terms of a concrete,
  checkable fact.
- Every original surface string retained as its own mention record under
  that entity, marked retrievable — never deleted, renamed, or folded
  silently into the canonical label.
- A list of any candidate pairs considered and deliberately left
  unmerged, with the reason nothing was combined.

## Failure mode if skipped

Two sources naming the same system two different ways produce two
separate, individually correct nodes. Nothing forces them back together,
so a later query keyed on one of the names comes back with only half the
picture — and if someone does force them together by picking a winning
name and throwing the other away, there's no way to reconstruct what that
merge actually rested on, or to split it apart again if it's later found
to have folded together two things that were never the same.

## Worked scenario

`sample-input.md` gives two accounts of one incident at Meridian Freight:
a support ticket where a customer calls the affected system "the payments
service," and an infrastructure change log where the platform team only
ever calls it `billing-svc`. A shared outage window and an explicit ticket
cross-reference in the change log are what make the merge defensible —
not that the two names sound alike. The same file also includes a second,
unrelated pair of mentions with no such link between them, so the kit has
a case where the correct move is to leave two names unmerged. See
`README.md` for how to run the kit against it.

## Link to starter kit

**Kit:** `starters/alias-merge-with-trail/README.md`
