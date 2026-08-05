---
name: audit-loop
category: F-governance
stage: governance
cost: medium
tools: [Claude Code]
core: false
---

# audit-loop

This kit is the runnable companion to the `audit-loop` pattern
specification (`patterns/audit-loop.md`). It is an extended kit — a single
Claude Code reference implementation, lighter than the full multi-tool
anatomy the seven core kits carry. See `starters/README.md` for that
distinction.

## What it does

Runs a separate loop, positioned with a wider vantage point than the main
loop, that periodically reviews territory the main loop structurally
can't see from inside its own operating scope — not because the main
loop is careless, but because its scope was never built to hold more than
one item at a time.

## Inputs

- The main loop's outputs and history.
- A vantage point outside the main loop's own scope to review them from.

## Outputs

- A periodic report naming classes of problem the main loop couldn't have
  caught on its own.

## Failure mode if skipped

An entire category of problem stays invisible indefinitely, because the
only loop positioned to catch it is also the one structurally unable to
see it — each individual decision looks sound, and the pattern across
decisions never gets checked at all.

## Worked scenario

Marrow Creek Mutual, a fictional insurance cooperative, runs a
claims-adjustment loop that processes one claim at a time: read the
claim, check it against the policy's coverage terms, approve or flag for
review. That scope never holds more than one claim in view, so it
approved claim MC-8801 (fender damage, repair estimate from Alder Street
Auto Body) and, three days later, claim MC-8809 (an unrelated accident,
also estimated by Alder Street Auto Body) — each claim checked out
against its own policy terms on its own merits. Only a loop with a wider
vantage, reviewing the full week's claims together instead of one at a
time, can notice that the two estimates share a near-identical repair
line-item breakdown down to the dollar, from the same shop, across two
otherwise-unconnected policyholders — a pattern invisible to any loop
that only ever looks at one claim in isolation. A third claim from the
same shop that week has an unrelated line-item breakdown and shouldn't
be swept into the same flag just because the shop matches. See
`README.md` for all three claims and what the audit loop reports.

## Link to starter kit

**Kit:** `starters/audit-loop/README.md`
