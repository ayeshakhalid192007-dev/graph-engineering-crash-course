# conflict-aware-bundle Starter Kit

A single-tool (Claude Code) reference kit for the **conflict-aware-bundle**
pattern: assembling a task-scoped bundle that keeps two contradicting
claims visible side by side, tagged unresolved, instead of quietly
resolving the disagreement before anyone downstream sees it happened.
This is an extended kit — see `starters/README.md` for how that differs
from the seven core kits.

Saltmere Harbor Authority and the two tide-gauge readings below are
invented for this course, not drawn from any real harbor's records.

## Prerequisites

- Claude Code.
- No external services or API keys — the readings and context below are
  everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the task-scoped draw and the known contradiction below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Task-scoped draw: "peak tide during the March storm"

- `storm-event-2026-03-14` — undisputed. "Storm surge event, night of
  March 14, 2026, Saltmere channel entrance."
- `harbor-flood-threshold` — undisputed. "Harbor flood-defense design
  threshold: 5.2m."
- `claim-tide-peak-gaugeA` — "Peak tide during the March 14 storm: 4.8m
  at 23:10." Source: Gauge A (primary, automatic log).
- `claim-tide-peak-gaugeB` — "Peak tide during the March 14 storm: 5.6m
  at 23:14." Source: Gauge B (backup, recalibrated 2026-02-28).

### Known unresolved contradiction touching this draw

`claim-tide-peak-gaugeA` and `claim-tide-peak-gaugeB` both purport to
report the single peak-tide value for the same storm event, and disagree
by 0.8m. The two values cannot both be the peak — this is a direct,
already-flagged, unresolved contradiction, not a rounding difference.

### Claude Code

1. Load the skill: `.claude/skills/bundle-conflicts/SKILL.md`.
2. Ask it to run: "Use the bundle-conflicts skill on the task-scoped draw
   and known contradiction in README.md."
3. It prints the bundle: undisputed context as-is, and the two
   contradicting claims tagged as an unresolved pair rather than
   collapsed to one value.

## Expected Output

- **Undisputed, included as-is:** `storm-event-2026-03-14`,
  `harbor-flood-threshold` — no contradiction touches either, so neither
  gets any conflict tag.
- **Unresolved-contradiction pair, both included:**
  - `claim-tide-peak-gaugeA` — "4.8m at 23:10" (Gauge A, primary).
  - `claim-tide-peak-gaugeB` — "5.6m at 23:14" (Gauge B, backup,
    recalibrated 2026-02-28).
  - Tag: `unresolved-contradiction`, reason: "both claim to report the
    single peak-tide value for the same storm event and disagree by
    0.8m; not resolved by gauge role alone."
- **Not present in the bundle:** any single "peak tide" value picked as
  the answer. The bundle must not average the two, and must not silently
  prefer Gauge A for being labeled primary.

### Checking the result

- Confirm both gauge claims appear in the output — a bundle showing only
  Gauge A's reading has silently resolved the contradiction instead of
  surfacing it.
- Confirm the contradiction tag names both claims and states why they
  conflict, not just "conflicting data present."
- Confirm the undisputed nodes (`storm-event-2026-03-14`,
  `harbor-flood-threshold`) are not tagged as part of the contradiction —
  only the two claims that actually disagree should carry the tag.

## Modifying the Example

1. Replace the draw, the undisputed context, and the contradicting claims
   with your own.
2. Re-run the skill and confirm it never resolves a flagged contradiction
   on its own — including one where a node has a "primary" or
   higher-confidence label attached.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/bundle-conflicts/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Only `claim-tide-peak-gaugeA` appears in the bundle. | The skill treated "primary" as a tiebreaker and dropped the contradicting claim instead of keeping both visible. |
| The bundle reports a single averaged tide value (e.g. 5.2m). | The skill tried to resolve the contradiction numerically instead of leaving it as an explicit unresolved pair. |
| `harbor-flood-threshold` gets tagged as part of the contradiction. | The skill over-applied the conflict tag to context in the draw that the known contradiction doesn't actually touch. |

## Next Steps

- Review `patterns/conflict-aware-bundle.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
