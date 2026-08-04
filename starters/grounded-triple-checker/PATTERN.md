---
name: grounded-triple-checker
category: E-checker
stage: read
cost: medium
tools: [Claude Code, OpenCode]
core: true
---

# grounded-triple-checker

This kit is the runnable companion to the `grounded-triple-checker` pattern
specification (`patterns/grounded-triple-checker.md`). It works one concrete
scenario end to end: two changes submitted against a fictional
video-encoding company each carry a "doesn't touch the license issuer"
claim in their own description, and the kit has to work out which claim is
actually true by querying the graph's own edges, without giving any weight
to how persuasive either change's write-up happens to be.

## What it does

Given a claim shaped like "change `<id>` does not touch module `<name>`",
this pattern identifies which edge, if it turned up in the graph, would
break the claim, then scans a populated graph's own edges for a subject,
predicate, and object match against it, leaving the change's own
description out of the decision entirely. Reports ACCEPT when the edge is
absent and REJECT — naming the specific edge that was found — when it is
present.

## Inputs

- A claim naming a change id and a module it allegedly leaves untouched
  (this kit reads these claims off `claims`-linked claim nodes already
  present in the sample graph, one per change).
- The graph to check it against. This kit ships
  `sample-graph.example.json`, a small, fixed, already-populated graph — 10
  nodes, 7 edges — standing in for a much larger production graph. It
  covers a fictional streaming company, Cobalt Stream: three changes, five
  modules, and two claim nodes, each naming a change/module pair someone
  asserted is not connected by a `touches` edge.

## Outputs

- A verdict per claim: ACCEPT or REJECT (or UNVERIFIABLE if the claim names
  a change or module the graph doesn't have).
- For every REJECT, the specific edge that contradicts the claim — never a
  bare "this looks wrong."

## Failure mode if skipped

A checker that instead weighs how a change's description reads will wave
through an author who genuinely believed their own summary right alongside
one who didn't — a change that quietly reaches into a sensitive module
gets the same pass as one that never goes near it, because nothing
required checking the edge that actually separated the two. The graph
carried that edge the entire time; the check simply never queried it.

## Link to starter kit

**Kit:** `starters/grounded-triple-checker/README.md`
