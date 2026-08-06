---
name: gate-task-completion
description: Blocks a loop's proposed "done" signal for a task until the grounded checker's run log shows it actually ran against that exact task, returning a named block instead of a silent pass when the check is missing or mismatched
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# gate-task-completion

Reads a loop's proposed "done" signal for a task and the checker's run
log, and decides whether the task's own checker entry actually exists —
passing the loop through only when it does, and blocking with the
specific missing check named when it doesn't.

## Instructions

You are a Claude Code skill implementing the `early-victory-guard`
pattern. Follow these steps in order:

1. **Read the loop's proposed "done" signal for the task**, noting the
   task's own id exactly as the loop states it — this id is what you'll
   match the checker log against, not the ticket's subject matter or the
   plausibility of the resolution note.
2. **Read the checker's run log.** Default to the tickets and log in
   this kit's `README.md` unless the user gives you a different set.
3. **Search the run log for an entry whose task id exactly matches the
   proposed "done" signal's task id.** A near match — the right subject
   matter, the right loop, even the right day — does not count. Only an
   entry keyed to the exact task id counts as coverage.
4. **If no matching entry exists at all, block.** State plainly that the
   checker never ran against this task, and name the task id that's
   missing coverage. Do not let a well-written resolution note substitute
   for the missing run.
5. **If a matching entry exists but is keyed to a different task id that
   merely looks similar** (a typo, an adjacent ticket number, a logging
   mixup), treat this the same as no entry — block, and name the
   mismatch specifically: what task id the loop claimed versus what task
   id the log actually shows.
6. **If a matching entry exists for the exact task id, pass the loop
   through.** The guard's job is only to confirm the checker ran against
   this task at least once — it does not re-run the checker itself and
   does not second-guess a pass or fail the checker already recorded.
7. **Report one outcome per task**: `PASS` (with the matching log entry
   cited) or `BLOCKED` (with the specific missing or mismatched task id
   named). Never report a task without one of these two outcomes.

## Input

- A loop's proposed "done" signal for a task, naming that task's id
  (defaults to the tickets in this kit's `README.md`).
- The checker's run log, keyed by task id.

## Output

- `PASS`, allowing the loop to complete, or `BLOCKED`, returning the loop
  to its work with the specific missing or mismatched check named.

## Example Usage

```
Use the gate-task-completion skill on the tickets and checker log in
README.md.

Expected:
  HR-2231: BLOCKED
    Reason: no checker log entry exists for task id HR-2231 at all.
  HR-2244: PASS
    Matching entry: checker ran against HR-2244, result PASS.
  HR-2258: BLOCKED
    Reason: proposed done signal names task HR-2258, but the only nearby
      log entry is keyed to HR-2255 -- not a match, treat as uncovered.
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit. Before reporting, self-check that every `PASS` you issued
cites a log entry whose task id is an exact string match to the proposed
"done" signal's task id, not a lookalike, and that no task with a missing
or mismatched entry slipped through as `PASS` because its resolution note
read convincingly.
