# versioned-schema-log Starter Kit

A single-tool (Claude Code) reference kit for the **versioned-schema-log**
pattern: recording every schema version an extraction pipeline has used
and which run IDs happened under each one, so schema drift is a logged
fact instead of something a reader has to reconstruct by comparing field
lists by hand. This is an extended kit — see `starters/README.md` for how
that differs from the seven core kits.

Kestrel Wildlife Trust and the camera-trap runs below are invented for
this course, not drawn from any real reserve's monitoring program.

## Prerequisites

- Claude Code.
- No external services or API keys — the version history and run list
  below are everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the schema history and run list below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Schema history

**Schema v1** — introduced 2026-01-05. Fields: `species`, `timestamp`,
`camera_id`.

**Schema v2** — introduced 2026-04-02. Fields: `species`, `timestamp`,
`camera_id`, `confidence_score`, `observer_id`. Reason recorded at
introduction: "Wind-triggered captures were being logged as pine marten
sightings with no way to flag them as uncertain; adding confidence score
and a verifying ranger's ID."

### Extraction runs (unsorted, as they'd arrive from the pipeline log)

- `run-2026-02-03` — ran 2026-02-03
- `run-2026-04-10` — ran 2026-04-10
- `run-2026-01-14` — ran 2026-01-14
- `run-2026-05-02` — ran 2026-05-02
- `run-2026-03-01` — ran 2026-03-01

### Claude Code

1. Load the skill: `.claude/skills/log-schema-version/SKILL.md`.
2. Ask it to run: "Use the log-schema-version skill on the schema history
   and run list in README.md."
3. It prints one log entry per schema version, each with its fields and
   the run IDs performed under it.

## Expected Output

- **Schema v1** (introduced 2026-01-05, fields: species, timestamp,
  camera_id): runs `run-2026-01-14`, `run-2026-02-03`, `run-2026-03-01` —
  the three runs that happened before v2's 2026-04-02 introduction date.
- **Schema v2** (introduced 2026-04-02, fields: species, timestamp,
  camera_id, confidence_score, observer_id): runs `run-2026-04-10`,
  `run-2026-05-02` — the two runs on or after the introduction date.

### Checking the result

- Confirm every run ID from the list appears under exactly one schema
  version — none dropped, none duplicated across both.
- Confirm the assignment is by run date relative to each schema's
  introduction date, not by the order the runs happened to be listed in
  above (the list is intentionally unsorted).
- Confirm each version's field list is the field list as introduced, not
  a merged or cumulative list — v1's entry should list three fields, not
  five.

## Modifying the Example

1. Replace the schema history and run list with your own.
2. Re-run the skill and confirm a run landing exactly on an introduction
   date gets logged under the new version, not the old one.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/log-schema-version/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `run-2026-04-10` gets logged under schema v1. | The skill compared run order in the list instead of run date against each schema's introduction date — the run list is deliberately unsorted to catch this. |
| Schema v1's entry lists five fields. | The skill merged v2's fields into v1's entry instead of keeping each version's field list as it stood when introduced. |
| A run ID is missing from both entries. | The skill only logged runs it happened to be told about explicitly instead of accounting for every run in the input list — every run needs a version. |

## Next Steps

- Review `patterns/versioned-schema-log.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
