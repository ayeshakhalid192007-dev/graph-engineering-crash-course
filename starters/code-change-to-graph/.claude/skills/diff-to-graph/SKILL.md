---
name: diff-to-graph
description: Turns a diff's touched functions and modules into graph nodes, reusing entities the graph already tracks, and links the change itself to each one with a modifies edge
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# diff-to-graph

Reads a diff and produces graph structure from it: a node for the change,
a node for every function or module its hunks actually touch, and a
`modifies` edge from the change to each. Entities the graph already
tracks get reused by id, never recreated.

## Instructions

You are a Claude Code skill implementing the `code-change-to-graph`
pattern. Follow these steps in order:

1. **Read the existing graph inventory first.** This tells you which
   functions and modules already have nodes, and under what id. Hold
   this list in mind before you look at the diff — you need it to tell
   "touched something we already track" apart from "first time we've
   seen this."
2. **Read the diff.** Default to the sample diff in this kit's
   `README.md` unless the user gives you a different one. Parse it hunk
   by hunk, not just by file header — a file can have multiple hunks
   touching different functions inside it, and a hunk can introduce a
   function that didn't exist before.
3. **List every entity actually touched by a hunk.** An entity counts as
   touched only if a hunk changes, adds, or removes code inside it. A
   function or module named only in the commit message, with no
   corresponding hunk, does not count — don't let prose in the commit
   description invent an edge that the code changes themselves don't
   support.
4. **Resolve each touched entity against the inventory.** If it matches
   an existing node (by name and containing file), reuse that node's id
   exactly — do not create a second node for the same entity under a new
   id. If it has no match, create a new node and mark it explicitly as
   newly created in this run, so a reviewer can see at a glance which
   nodes are fresh.
5. **Create one node for the change itself**, using the commit hash or PR
   identifier as its id, typed as a change/commit node.
6. **Write one `modifies` edge per touched entity**, from the change node
   to that entity's node (reused or newly created). Do not write an edge
   for the containing module file when the hunk actually touches a
   specific function inside it — edge the entity that changed, not
   everything above it in the containment hierarchy.
7. **Report the result** as: the change node id, then each touched entity
   with a reused/new label, then the full list of `modifies` edges. If
   you deliberately excluded something the commit message mentions but
   no hunk supports, say so and explain why.

## Input

- The graph's current inventory of known function/module nodes.
- A diff or commit (defaults to the sample diff in `README.md`).

## Output

- One change node.
- One node per touched entity, labeled reused or newly created.
- One `modifies` edge per touched entity, from the change node to it.

## Example Usage

```
Use the diff-to-graph skill on the sample diff in README.md, against the
existing graph inventory listed there.

Expected:
  Change node: commit-a1e77f2
  Touched entities:
    calibrate_brake_torque (reused, brake-controller.c)
    read_ambient_temp_sensor (new, brake-controller.c)
    lock_door_interlock (reused, door-interlock.c)
  Edges:
    commit-a1e77f2 --modifies--> calibrate_brake_torque
    commit-a1e77f2 --modifies--> read_ambient_temp_sensor
    commit-a1e77f2 --modifies--> lock_door_interlock
```

## Notes

This kit has no companion verification agent — it is a single-tool
extended kit, not one of the seven core kits with full multi-tool
anatomy. Self-check your own output against step 4 (no duplicate nodes
for existing entities) and step 6 (edges point at the entity touched, not
its container) before reporting it as final.
