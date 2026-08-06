---
name: code-change-to-graph
category: A-extraction
stage: write
cost: medium
tools: [Claude Code]
core: false
---

# code-change-to-graph

This kit is the runnable companion to the `code-change-to-graph` pattern
specification (`patterns/code-change-to-graph.md`). It is an extended kit:
a single Claude Code reference implementation, not the full multi-tool
anatomy the seven core kits carry. See `starters/README.md` for what that
distinction means and why it's the deliberate scope for this phase.

## What it does

Turns a diff into graph structure instead of leaving it as text that only
means something at review time. Every function or module a diff's hunks
actually touch becomes a node — reusing the node if the graph already
tracks that entity, creating one if this is the first time the graph has
seen it — and the commit itself becomes a node with a `modifies` edge
running from it to each entity it changed.

## Inputs

- A diff or commit, with enough context (file paths, function names,
  hunk contents) to identify what it touches.
- The graph's current inventory of known code entities — which functions
  and modules already have nodes, so the kit can tell "touched an
  existing entity" apart from "this function is new to the graph."

## Outputs

- One node representing the change itself (commit or PR), plus a node
  for each function or module its hunks touch — reusing existing node
  ids where the entity is already tracked.
- A `modifies` edge from the change node to every touched entity node.

## Failure mode if skipped

Without this pattern, the diff is the only record of what a change
affected. A reviewer can read it while the pull request is open, but once
the branch merges and that review context is gone, nothing in the graph
remembers that this particular commit was the one that altered a given
function — later questions like "what has touched this function in the
last year" have no answer except grepping commit history by hand.

## Worked scenario

Redwald Systems, a fictional maker of embedded firmware for elevator
control panels, ships a fix for brake-torque drift on cold starts. The
commit touches an existing function the graph already tracks
(`calibrate_brake_torque`), introduces a brand-new one
(`read_ambient_temp_sensor`), and touches a second existing function in a
different file (`lock_door_interlock`) to make it wait on calibration
before releasing. See `README.md` for the full diff and how the kit
processes it.

## Link to starter kit

**Kit:** `starters/code-change-to-graph/README.md`
