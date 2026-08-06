---
name: anchor-and-freeze
category: F-governance
stage: governance
cost: low
tools: [Claude Code]
core: false
---

# anchor-and-freeze

This kit is the runnable companion to the `anchor-and-freeze` pattern
specification (`patterns/anchor-and-freeze.md`). It is an extended kit — a
single Claude Code reference implementation, lighter than the full
multi-tool anatomy the seven core kits carry. See `starters/README.md`
for that distinction.

## What it does

Wires in at least one check that reaches outside the loop system
entirely — a source no loop wrote, touched, or can revise — and marks a
named set of facts or rules as frozen, meaning no loop may rewrite them,
however self-consistent its latest reasoning pass looks.

## Inputs

- A candidate signal source that sits outside every loop in the system.
- The specific facts or rules proposed for the frozen set.

## Outputs

- One external check, wired in and consulted before any decision the
  frozen facts bear on is finalized.
- An explicit list of frozen nodes, each marked off-limits to every loop
  in the system.

## Failure mode if skipped

A governance graph can keep converging on answers that agree with
themselves indefinitely, built only from facts its own loops wrote or
re-derived — and stay collectively wrong about something none of those
loops was ever positioned to check from outside its own reasoning.

## Worked scenario

Cinder Hollow Grantmakers, a fictional community grant fund, runs an
internal scoring loop that re-reviews its pending 2026-cycle applications
each review pass, reading each applicant's budget, mission-alignment, and
prior-grant-compliance nodes and adjusting a computed eligibility-score
edge. Over three passes the loop converged one applicant, Tallow Ridge
Youth Makers, from borderline to eligible — but every fact that
convergence rested on was itself either written or re-derived by an
earlier pass of the same loop; nothing about the applicant's actual
real-world status ever entered from outside it. The county's public
business-registry lookup, a source the loop was never wired to consult,
has listed Tallow Ridge Youth Makers as administratively dissolved for
four months. A separate review pass, trying to make a different
borderline applicant's numbers work, proposes loosening the definition of
one of the fund's own baseline eligibility criteria rather than simply
scoring against it. See `README.md` for the full three-applicant review
set and how anchoring the registry lookup, plus freezing the criteria
themselves, changes both outcomes.

## Link to starter kit

**Kit:** `starters/anchor-and-freeze/README.md`
