# code-change-to-graph Starter Kit

A single-tool (Claude Code) reference kit for the **code-change-to-graph**
pattern: recording every function or module a diff touches as a node,
linked back to the change itself by a `modifies` edge, so the graph keeps
a queryable trace of what a commit affected after the pull request that
introduced it has long since closed. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Redwald Systems, the fictional elevator-firmware company in this kit's
scenario, and the commit below, are invented for this course and not
based on any real company, product, or incident.

## Prerequisites

- Claude Code.
- No external services or API keys — everything the kit needs is in this
  file.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the sample diff and the existing graph inventory below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Sample diff

```
Commit a1e77f2 — "Fix brake torque calibration drift on cold starts"

--- a/brake-controller.c
+++ b/brake-controller.c
@@ calibrate_brake_torque(...)
-  apply_torque(default_offset);
+  float ambient = read_ambient_temp_sensor();
+  apply_torque(default_offset + cold_start_compensation(ambient));

+float read_ambient_temp_sensor(void) {
+  return adc_read(AMBIENT_TEMP_CHANNEL);
+}

--- a/door-interlock.c
+++ b/door-interlock.c
@@ lock_door_interlock(...)
-  release_lock();
+  wait_for_calibration(calibrate_brake_torque);
+  release_lock();
```

### Existing graph inventory (before this commit)

- `calibrate_brake_torque` — function node, in `brake-controller.c`.
- `lock_door_interlock` — function node, in `door-interlock.c`.
- `brake-controller.c` — module node.
- `door-interlock.c` — module node.

`read_ambient_temp_sensor` does not appear in this inventory — this
commit is the first time the graph would encounter it.

### Claude Code

1. Load the skill: `.claude/skills/diff-to-graph/SKILL.md`.
2. Ask it to run: "Use the diff-to-graph skill on the sample diff above,
   against the existing graph inventory listed in README.md."
3. It prints the change node, every touched-entity node (marking each as
   reused or newly created), and the `modifies` edges connecting them.

## Expected Output

- **Change node:** `commit-a1e77f2`.
- **Touched entities, three `modifies` edges:**
  - `commit-a1e77f2 --modifies--> calibrate_brake_torque` (reused —
    already in the inventory).
  - `commit-a1e77f2 --modifies--> read_ambient_temp_sensor` (new node —
    first appearance in the graph).
  - `commit-a1e77f2 --modifies--> lock_door_interlock` (reused —
    already in the inventory).
- `brake-controller.c` and `door-interlock.c` are not themselves given
  `modifies` edges here — the diff's hunks touch specific functions
  inside them, not the module files as a whole, and the kit should not
  blur that distinction by edging the containing file too.

### Checking the result

- Confirm `calibrate_brake_torque` and `lock_door_interlock` were reused,
  not recreated as duplicate nodes with a new id.
- Confirm `read_ambient_temp_sensor` was created fresh, and marked as
  such rather than silently treated as if the graph already knew it.
- Confirm no fourth `modifies` edge appears for anything mentioned only
  in the commit message and not actually present in a hunk.

## Modifying the Example

1. Replace the sample diff and inventory above with your own.
2. Re-run the skill and check that entities already in your inventory get
   reused rather than duplicated, and that new ones are flagged as new.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/diff-to-graph/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `read_ambient_temp_sensor` doesn't appear as a node. | The skill only scanned the diff's file paths, not the added function inside a hunk. Re-check that every hunk, not just the file header, gets scanned for touched entities. |
| `calibrate_brake_torque` gets created as a second, duplicate node. | The skill didn't check the existing inventory before creating a node. Node creation must always check for a reuse match first. |
| A `modifies` edge points at `brake-controller.c` itself. | The skill edged the containing module instead of the specific function the hunk touched. Edge the entity actually changed, not its container. |

## Next Steps

- Review `patterns/code-change-to-graph.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
