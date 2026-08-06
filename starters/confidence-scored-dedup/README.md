# confidence-scored-dedup Starter Kit

A single-tool (Claude Code) reference kit for the
**confidence-scored-dedup** pattern: scoring every candidate merge on a
fixed, weighted set of signals and letting that score — not a gut call —
decide whether a pair auto-merges or goes to a review queue. This is an
extended kit — see `starters/README.md` for how that differs from the
seven core kits.

Fenwick & Vance Procurement and the vendor records below are invented for
this course, not drawn from any real company's procurement data.

## Prerequisites

- Claude Code.
- No external services or API keys — the candidate set below is
  everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the scoring rule and the candidate pairs below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Scoring rule

Each candidate pair gets scored on three signals, summed:

- **Tax ID match** (exact match required): `+0.50`, else `0`.
- **Name token overlap** (fraction of shared significant words between
  the two names, e.g. "Ashgrove," "Steel"): scaled, `0` to `+0.35`.
- **Address match** (same registered address): `+0.15`, else `0`.

**Threshold: `0.75`.** A pair scoring at or above threshold auto-merges;
below it goes to the review queue with its score and signal breakdown
attached.

### Candidate pairs

**Pair A** — system 1: "Ashgrove Steel Co." / system 2: "Ashgrove Steel
Company"
- Tax ID: match (`+0.50`)
- Name overlap: very high, near-identical apart from "Co." vs "Company"
  (`+0.32`)
- Address: same registered address (`+0.15`)
- **Total: 0.97**

**Pair B** — system 1: "Bell Castle Ltd" / system 2: "Bellcastle
Logistics"
- Tax ID: no match (`0`)
- Name overlap: partial — "Bell(castle)" shares a root but "Ltd" vs
  "Logistics" diverge, and the businesses turn out to be unrelated
  (`+0.18`)
- Address: different city (`0`)
- **Total: 0.18**

**Pair C** — system 1: "Whitmore & Sons Supply" / system 2: "Whitmore
and Sons"
- Tax ID: match (`+0.50`)
- Name overlap: high — "Whitmore," "Sons" both present, "&" vs "and" is
  cosmetic (`+0.28`)
- Address: different — system 2's address turns out to be a satellite
  office of the same vendor, not a separate company (`0`)
- **Total: 0.78**

### Claude Code

1. Load the skill: `.claude/skills/score-and-merge/SKILL.md`.
2. Ask it to run: "Use the score-and-merge skill on the candidate pairs
   in README.md, using the scoring rule and threshold given there."
3. It prints each pair's score, which signals contributed, and whether
   it auto-merged or went to the review queue.

## Expected Output

- **Pair A — auto-merged** (0.97, well above threshold): canonical
  record combining both, tax ID and address agreeing.
- **Pair C — auto-merged** (0.78, above threshold despite the address
  mismatch): the tax-ID match alone carries most of the score; the
  address difference doesn't override it.
- **Pair B — review queue** (0.18, well below threshold): flagged with
  its score and the fact that neither tax ID nor address matched.

### Checking the result

- Confirm pair C merged despite the address mismatch — the point of this
  pair is that a strong tax-ID match can cross the threshold even with
  one signal missing, and the score should reflect that plainly rather
  than getting overridden by a manual "but the address is different"
  veto.
- Confirm pair B did not merge, and that its review-queue entry names
  which signals failed, not just a bare "below threshold."
- Confirm the score for each pair is shown, not just the merge/no-merge
  decision — the whole point of this pattern is that the decision is
  traceable back to a number.

## Modifying the Example

1. Replace the candidate pairs and/or the signal weights with your own.
2. Re-run the skill and confirm every pair's score is shown alongside its
   decision, and that nothing crosses the threshold without the score
   actually supporting it.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/score-and-merge/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Pair C ends up in the review queue instead of auto-merged. | The skill let the address mismatch veto the score instead of summing all three signals and comparing the total to the threshold. |
| Pair B auto-merges. | The skill treated partial name similarity as enough on its own. No single weak signal should cross 0.75 by itself. |
| A pair's decision is reported with no score attached. | The skill dropped the numeric breakdown. Every decision — merge or queue — must show the score and the signals that produced it. |

## Next Steps

- Review `patterns/confidence-scored-dedup.md` in the course repo for
  the general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
