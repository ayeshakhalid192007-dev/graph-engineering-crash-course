---
name: early-victory-guard
category: E-checker
stage: read
cost: low
tools: [Claude Code]
core: false
---

# early-victory-guard

This kit is the runnable companion to the `early-victory-guard` pattern
specification (`patterns/early-victory-guard.md`). It is an extended
kit — a single Claude Code reference implementation, lighter than the full
multi-tool anatomy the seven core kits carry. See `starters/README.md` for
that distinction.

## What it does

Blocks a loop from marking its task complete until the grounded checker
has actually run against that specific task at least once, so "done"
always has at least one verification step behind it — never a plausible
draft that nobody separately confirmed.

## Inputs

- A loop's proposed "done" signal for a task.
- The checker's run log for that same task.

## Outputs

- Either a pass-through allowing the loop to complete, or a block that
  returns the loop to its work with the missing check named.

## Failure mode if skipped

A loop can declare victory before anything about its output has actually
been verified — the "done" signal and the checking step never had to
touch, and a confident-sounding draft closes the task exactly as easily
as a checked one would have.

## Worked scenario

Hollowreed Software, a fictional SaaS helpdesk provider, runs a
ticket-triage loop that reads a bug report, matches it to a suspected
root-cause edge in the graph, drafts a resolution note, and proposes
marking the ticket resolved. One ticket's proposed resolution names a
root-cause edge and a fix PR, but the checker's run log has no entry for
that ticket at all — the loop drafted a plausible note and moved straight
to "done" without anything separately confirming the cited edge exists.
A second ticket's proposed resolution has a matching checker entry that
actually ran against that ticket and returned pass. A third ticket's
proposed resolution has a checker entry too, but for a different ticket
id entirely — a logging mixup that looks like coverage at a glance and
isn't. See `README.md` for all three tickets and how the guard tells them
apart.

## Link to starter kit

**Kit:** `starters/early-victory-guard/README.md`
