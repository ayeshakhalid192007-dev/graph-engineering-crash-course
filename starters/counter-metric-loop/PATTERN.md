---
name: counter-metric-loop
category: F-governance
stage: governance
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# counter-metric-loop

This kit is the runnable companion to the `counter-metric-loop` pattern
specification (`patterns/counter-metric-loop.md`). Its worked scenario is a
fictional software company, Thornfield Systems: an automated
pull-request-approval loop chasing a single weekly headline count, and a
second, independently owned deployment loop whose revert-rate reading is
the only thing that catches the week the approval loop started cutting
corners.

## What it does

Reads a governance graph holding two loops' separately recorded readings
for the same stretch of time — one loop's own headline metric, and a
second loop's counter-metric, computed by a different owner and never
piped back to the first loop as input. For every period, this pattern
compares the counter-metric reading against its recorded ceiling and, on
any reading past that ceiling, produces a governance edge naming the two
loops, the period, both readings, and the breached threshold. A period
where the counter-metric stays under the ceiling produces no such edge.

## Inputs

- A governance graph with two loop nodes: the loop being watched and the
  loop computing its counter-metric, plus one period node per interval
  being compared.
- Each loop's reading for each period, recorded as an edge from that loop
  to the period node.
- A threshold node giving the counter-metric's ceiling and who set it.

## Outputs

- One governance edge per period where the counter-metric reading exceeds
  its ceiling, linking the counter-metric loop to the watched loop and
  citing both readings plus the threshold that was crossed.
- A confirmation, checked structurally rather than assumed, that no edge
  in the graph lets the watched loop read its own counter-metric.

## Failure mode if skipped

A loop scored on one number will eventually find the cheapest way to move
that number, whether or not the cheap way serves whatever the number was
supposed to stand for. Nothing about the number itself distinguishes a
week it rose because the underlying work improved from a week it rose
because the loop found a shortcut — both weeks look identical on the one
dashboard the loop is judged by, and no amount of staring harder at that
same number tells them apart.

## Link to starter kit

**Kit:** `starters/counter-metric-loop/README.md`
