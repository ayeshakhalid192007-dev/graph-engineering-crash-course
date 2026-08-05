---
name: arbitration-edge
category: F-governance
stage: governance
cost: low
tools: [Claude Code]
core: false
---

# arbitration-edge

This kit is the runnable companion to the `arbitration-edge` pattern
specification (`patterns/arbitration-edge.md`). It is an extended kit — a
single Claude Code reference implementation, lighter than the full
multi-tool anatomy the seven core kits carry. See `starters/README.md` for
that distinction.

## What it does

Defines a rule that decides which of two loops wins when both act on the
same resource at the same time, instead of leaving the outcome to
whichever write happens to land last. The losing write isn't silently
dropped — it's recorded, with the reason it lost.

## Inputs

- A conflicting pair of proposed writes from two loops touching the same
  node or edge.

## Outputs

- A single accepted write.
- A record of which loop's write was rejected, and why.

## Failure mode if skipped

Two loops that are each individually reasonable overwrite each other's
work with neither one aware a collision ever happened — the graph ends up
holding whichever write physically landed last, with no record that a
competing write ever existed.

## Worked scenario

Driftwood Outfitters, a fictional outdoor-gear retailer, runs two loops
that both write to stock-count fields in its inventory graph:
`restock-sync`, which polls the warehouse system every fifteen minutes
and writes an absolute snapshot count, and `returns-processing`, which
increments the count each time a scanned return re-enters inventory. On
one SKU, both loops fire within seconds of each other — `restock-sync`
writes a snapshot taken just before a return was scanned, and
`returns-processing` writes an increment anchored to that same return
event, and the two proposed counts disagree. On a different SKU in the
same run, the two loops write to two different fields entirely — one
touches the stock count, the other a reorder flag — which only looks like
a collision until you check which field each write actually targets. See
`README.md` for both cases and the rule the kit applies to each.

## Link to starter kit

**Kit:** `starters/arbitration-edge/README.md`
