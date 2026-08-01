# loop-constraints.md

`loop-budget.md` sets how much each loop named in `LOOP.md` may touch on a
normal run. This document is different: it's the short list of things
neither loop is ever allowed to do, at any budget, under any circumstance.
Where the budget is a dial a human could in principle turn up or down, these
are hard stops.

- **Never merge a `docs/` change while `originality-check` is red.** A
  failing originality check is not a warning to note and move past — it is a
  block on merging, full stop, regardless of how small the flagged passage
  looks or how close a deadline is.
- **Never edit `graph-plan.md`, automatically or otherwise.** Only the
  repository's human owner changes the master spec. No loop proposes a diff
  to it, and no loop applies one.
- **Never edit the source table in `resources/sources.md`, automatically or
  otherwise.** The ten attributed entries are a fixed record of where this
  course's ideas came from; adding, removing, or rewording an entry is a
  human-only action, same as editing `graph-plan.md` itself.
- **Never delete or rewrite an entry in `loop-run-log.md`.** The log is
  append-only, the same provenance discipline `graph-plan.md` §8 asks of
  every fact this course tracks: if a past entry turns out to be wrong, the
  fix is a new entry that says so and supersedes it, not a silent edit that
  erases what the log used to say.
