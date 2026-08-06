# supersession-chain Starter Kit

A single-tool (Claude Code) reference kit for the **supersession-chain**
pattern: correcting a wrong claim by adding a new node and a `supersedes`
edge, instead of overwriting the old node and losing the record that the
graph ever held the earlier belief. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Bellhaven Materials Lab and the two safety-data-sheet revisions below are
invented for this course, not drawn from any real lab, vendor, or polymer.

## Prerequisites

- Claude Code.
- No external services or API keys — the claim records below are
  everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the existing claims and the new evidence below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Existing claims (before this run)

- `claim-xr9-flashpoint-2019` — "Polymer XR-9 has a flash point of
  210°C." Source: 2019 SDS revision A, OCR-transcribed. Status: current.
- `claim-xr9-density-2019` — "Polymer XR-9 has a density of 1.14 g/cm³."
  Source: 2019 SDS revision A, same document. Status: current.

### New evidence

- 2024 SDS revision C, section 9 (Physical and Chemical Properties):
  "Flash point (closed cup, ASTM D93 retest): 185°C. Note: prior
  published value of 210°C reflected a transcription error in revision A
  and is corrected here." The density figure is not mentioned anywhere in
  revision C — nothing about it changed.

### Claude Code

1. Load the skill: `.claude/skills/supersede-claim/SKILL.md`.
2. Ask it to run: "Use the supersede-claim skill on the existing claims
   and new evidence in README.md."
3. It prints the new claim node, the `supersedes` edge, and the old
   node's updated status.

## Expected Output

- **New node:** `claim-xr9-flashpoint-2024` — "Polymer XR-9 has a flash
  point of 185°C (ASTM D93 retest)." Source: 2024 SDS revision C.
- **Edge:** `claim-xr9-flashpoint-2024 --supersedes--> claim-xr9-flashpoint-2019`.
- **Old node:** `claim-xr9-flashpoint-2019` retained in the graph,
  status changed from `current` to `stale`, value and source untouched.
- **Untouched:** `claim-xr9-density-2019` stays exactly as it was, status
  `current` — revision C says nothing about density, so nothing about
  this claim should change.

### Checking the result

- Confirm `claim-xr9-flashpoint-2019` still exists in the graph after the
  run, with its original 210°C value intact — it must not be deleted or
  edited in place.
- Confirm the `supersedes` edge points from the new node to the old one,
  not the reverse.
- Confirm `claim-xr9-density-2019` was left alone. A run that flags it
  stale too has confused "same source document" with "same claim
  contradicted."

## Modifying the Example

1. Replace the existing claims and new evidence with your own.
2. Re-run the skill and confirm exactly the claims the new evidence
   actually contradicts get superseded — nothing else in the graph moves.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/supersede-claim/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `claim-xr9-flashpoint-2019` disappears from the graph. | The skill overwrote the old node instead of adding a new one and linking it. Supersession never deletes. |
| `claim-xr9-density-2019` gets flagged stale too. | The skill treated "same source document as the corrected claim" as grounds for staling, instead of checking whether the new evidence actually contradicts that specific claim. |
| The `supersedes` edge runs the wrong direction. | The edge must point from the new (correcting) node to the old (corrected) node — check the skill didn't reverse it. |

## Next Steps

- Review `patterns/supersession-chain.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
