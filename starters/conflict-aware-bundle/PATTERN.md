---
name: conflict-aware-bundle
category: D-subgraph
stage: read
cost: medium
tools: [Claude Code]
core: false
---

# conflict-aware-bundle

This kit is the runnable companion to the `conflict-aware-bundle` pattern
specification (`patterns/conflict-aware-bundle.md`). It is an extended
kit — a single Claude Code reference implementation, lighter than the
full multi-tool anatomy the seven core kits carry. See `starters/README.md`
for that distinction.

## What it does

Assembles a subgraph that deliberately keeps two contradicting claims
both visible side by side, instead of silently picking a winner before
the worker — or the human reviewing its output — ever sees that the two
sources disagreed at all. Undisputed context in the same draw stays
undisputed; only the claims that actually conflict get the explicit
unresolved-contradiction tag.

## Inputs

- A task-scoped subgraph draw.
- Any known unresolved contradictions that touch nodes or edges inside
  it.

## Outputs

- A bundle that surfaces both sides of a contradiction explicitly, tagged
  as unresolved rather than collapsed into one answer.

## Failure mode if skipped

A worker, or the human reading its output afterward, never learns that
two sources disagreed at all — the subgraph quietly picked one and moved
on. A decision that depended on knowing there was genuine uncertainty
gets made as if the uncertainty never existed, with no trace afterward
that a second, contradicting reading was ever available to consult.

## Worked scenario

Saltmere Harbor Authority, a fictional coastal agency, runs two tide
gauges at its channel entrance. During a March storm surge, the primary
gauge logs peak tide at 4.8m at 23:10; the backup gauge, recalibrated
weeks earlier, logs peak tide at 5.6m at 23:14 for the same storm — an
0.8m disagreement that decides whether the surge cleared the harbor's
5.2m flood-defense threshold. A task-scoped draw for "what was peak tide
during the March storm" pulls in both readings plus undisputed context —
the storm event itself and the threshold value — and the kit must keep
both gauge readings visible as an unresolved pair rather than defaulting
to whichever gauge is nominally "primary." See `README.md` for the full
readings and how the kit bundles them.

## Link to starter kit

**Kit:** `starters/conflict-aware-bundle/README.md`
