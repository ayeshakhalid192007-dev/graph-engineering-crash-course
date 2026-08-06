---
name: log-schema-version
description: Maps every schema version an extraction pipeline has used to the run IDs performed under it, assigning each run by date against each schema's introduction date, so schema drift is a logged fact rather than an invisible shift
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# log-schema-version

Reads a pipeline's schema history and its list of extraction runs, and
produces one log entry per schema version: its fields as introduced, and
the complete set of run IDs that happened under it.

## Instructions

You are a Claude Code skill implementing the `versioned-schema-log`
pattern. Follow these steps in order:

1. **Read the full schema history first.** For each version, note its
   introduction date and its exact field list as of that introduction —
   not a running total, the list as it stood at that moment. Sort the
   versions by introduction date if they weren't given to you in order.
2. **Read the full run list.** Default to the schema history and runs in
   this kit's `README.md` unless the user gives you different ones. Note
   each run's id and the date it ran. Do not assume the list arrives
   sorted — treat run order in the input as meaningless and go strictly
   by date.
3. **Assign every run to exactly one schema version**, by comparing the
   run's date against each version's introduction date: a run belongs to
   the most recent schema version whose introduction date is on or before
   the run's date. A run happening on the exact day a new version is
   introduced belongs to the new version, not the old one.
4. **Do not merge field lists across versions.** Each version's log entry
   reports only the fields that version itself defines. A later version
   adding fields does not retroactively change what an earlier version's
   entry lists.
5. **Account for every run in the input.** A run with no schema version
   whose introduction date precedes it is an error condition — flag it
   rather than silently dropping it or guessing a version for it.
6. **Build one log entry per schema version**: version id, introduction
   date, its field list as introduced, and the sorted list of run IDs
   assigned to it.
7. **Report every version's entry together**, in version order, plus a
   note confirming the total run count assigned across all versions
   matches the total run count in the input — so a reader can see at a
   glance that no run was dropped or double-counted.

## Input

- The schema history: version id, introduction date, field list per
  version.
- The list of extraction runs: run id and date (defaults to the schema
  history and run list in this kit's `README.md`).

## Output

- One log entry per schema version: fields as introduced, and the run
  IDs performed under it.
- A total-run reconciliation note confirming every input run was
  assigned to exactly one version.

## Example Usage

```
Use the log-schema-version skill on the schema history and run list in
README.md.

Expected:
  Schema v1 (introduced 2026-01-05)
    Fields: species, timestamp, camera_id
    Runs: run-2026-01-14, run-2026-02-03, run-2026-03-01
  Schema v2 (introduced 2026-04-02)
    Fields: species, timestamp, camera_id, confidence_score, observer_id
    Runs: run-2026-04-10, run-2026-05-02
  Reconciliation: 5 runs in input, 5 runs assigned (3 + 2). None dropped.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that the reconciliation count
actually matches, that no version's field list absorbed fields from a
later version, and that a run dated exactly on an introduction date
landed in the new version rather than the old one.
