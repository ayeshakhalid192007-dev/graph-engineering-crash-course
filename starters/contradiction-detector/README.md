# contradiction-detector Starter Kit

A single-tool (Claude Code) reference kit for the **contradiction-detector**
pattern: scanning the fact graph for edges that can't both hold true at
once and flagging every such pair, running on its own rather than only
when a task happens to notice. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Thistlewood Water Utility and the pipe-segment filings below are invented
for this course, not drawn from any real utility, contractor, or
inspection report.

## Prerequisites

- Claude Code.
- No external services or API keys — the filings below are everything
  the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the pipe-segment filings below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Pipe-segment filings (this week's run)

- `pipe-segment-D7 --condition--> structurally-sound` — filed by Ashgrove
  Inspections, Monday, based on a visual and acoustic survey.
- `pipe-segment-D7 --condition--> requires-replacement` — filed by
  Millrace NDT, Wednesday, based on an ultrasonic thickness test.
- `pipe-segment-E2 --material--> cast-iron` — filed by Ashgrove
  Inspections.
- `pipe-segment-E2 --installation-year--> 1968` — filed by Millrace NDT.
- `pipe-segment-F9 --condition--> minor-corrosion-noted` — filed by
  Ashgrove Inspections.
- `pipe-segment-F9 --condition--> minor-corrosion-noted` — filed by
  Millrace NDT, independently, same week.

### Claude Code

1. Load the skill: `.claude/skills/scan-contradictions/SKILL.md`.
2. Ask it to run: "Use the scan-contradictions skill on the pipe-segment
   filings in README.md."
3. It prints every flagged contradictory pair, plus an explicit note for
   every other group it checked and cleared.

## Expected Output

- **Flagged:** `pipe-segment-D7`'s two `condition` edges —
  `structurally-sound` (Ashgrove, Mon) versus `requires-replacement`
  (Millrace, Wed). Same subject, same predicate, mutually exclusive
  values — a segment cannot be both at once.
- **Cleared, `pipe-segment-E2`:** the two edges address different
  predicates (`material` versus `installation-year`) — not comparable,
  not a contradiction, regardless of the two contractors disagreeing on
  other segments elsewhere.
- **Cleared, `pipe-segment-F9`:** both contractors independently reported
  the same `condition` value — corroboration, not contradiction.

### Checking the result

- Confirm the D7 pair appears in the flagged list with both edges' full
  detail (source, date, value) intact.
- Confirm E2 and F9 do **not** appear in the flagged list — a run that
  flags either has confused "different contractors filed something about
  this segment" with "these two edges assert incompatible things."
- Confirm the skill's report states an explicit outcome for all three
  segments, not just the one it flagged.

## Modifying the Example

1. Replace the pipe-segment filings with your own edges and sources.
2. Re-run the skill and confirm it flags only genuine same-subject,
   same-predicate, opposed-value pairs — and states an explicit cleared
   outcome for everything else it checked.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/scan-contradictions/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| E2's two edges get flagged as contradictory. | The skill compared edges across different predicates instead of requiring a shared subject *and* predicate before comparing values. |
| F9's two edges get flagged as contradictory. | The skill treated two independent sources reporting the same value as disagreement instead of corroboration — check it's comparing the actual object values, not just counting how many sources touched the subject. |
| D7's contradiction is missing from the flagged list. | The skill may have deduplicated the two `condition` edges as if they were the same claim instead of recognizing they assert different, incompatible values. |
| The report is missing an explicit outcome for one of the three segments. | Every group checked needs a stated result — flagged or cleared — not silence. Re-run and check step 6 of `SKILL.md` covered all three. |

## Next Steps

- Review `patterns/contradiction-detector.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
