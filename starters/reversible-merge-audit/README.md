# reversible-merge-audit Starter Kit

A single-tool (Claude Code) reference kit for the
**reversible-merge-audit** pattern: periodically rechecking past merges
against evidence gathered since, reversing any merge that new evidence
directly contradicts, and logging a confirmation for every merge that
still holds. This is an extended kit — see `starters/README.md` for how
that differs from the seven core kits.

Briarcombe University Library and the two author merges below are
invented for this course, not drawn from any real institution's citation
records.

## Prerequisites

- Claude Code.
- No external services or API keys — the merge history and evidence
  below are everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the merge history and new evidence below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Merge history

**Merge 1** — six months ago, canonical node `author-alderman-j`:
- Merged: "J. Alderman" and "James Alderman"
- Basis: both listed in the Physics department, publication years
  overlap (2019-2024 for both name variants)

**Merge 2** — one year ago, canonical node `author-kwan-r`:
- Merged: "R. Kwan" and "Rachel Kwan"
- Basis: both records carry ORCID `0000-0002-4471-XXXX`

### New evidence gathered since

- A preprint posted last week, "Distributed Load Balancing in
  Superconducting Qubit Arrays," lists two separate co-authors: "James
  Alderman" (PI, Physics) and "J. Alderman" (postdoc, Applied
  Mathematics) — the acknowledgments section thanks "both Almandine
  fellows, J. and James Alderman, for their independent contributions."
  Two people cannot be co-authors as themselves on the same paper.
- A grant record filed last month for "R. Kwan" repeats ORCID
  `0000-0002-4471-XXXX` — the same id merge 2 was based on.

### Claude Code

1. Load the skill: `.claude/skills/recheck-merges/SKILL.md`.
2. Ask it to run: "Use the recheck-merges skill on the merge history and
   new evidence in README.md."
3. It prints, for each merge, whether it was confirmed or reversed, and
   the evidence behind that decision.

## Expected Output

- **Merge 1 — reversed.** The preprint's co-author list is direct
  contradicting evidence: "J. Alderman" and "James Alderman" appear
  together as two distinct people on the same paper, which is
  incompatible with them being the same person. `author-alderman-j`
  splits back into its two pre-merge entities, with the preprint
  attached as the reversal's evidence.
- **Merge 2 — confirmed.** The grant record reaffirms the same ORCID the
  original merge was based on; nothing contradicts it. `author-kwan-r`
  stays merged, logged as rechecked and confirmed — not silently skipped.

### Checking the result

- Confirm merge 1's reversal names the preprint specifically as the
  contradicting evidence, not a vague "new information."
- Confirm merge 2 produces an explicit confirmation entry, not just an
  absence of action — an audit that only reports reversals leaves no
  trace that the untouched merges were actually checked.
- Confirm the reversal for merge 1 restores two separate entities rather
  than leaving one of the two names orphaned or dropped.

## Modifying the Example

1. Replace the merge history and evidence with your own.
2. Re-run the skill and confirm every merge in your history gets either a
   confirmation or a reversal — never silence.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/recheck-merges/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Merge 1 isn't reversed. | The skill treated the preprint's co-author list as unrelated context instead of recognizing two names appearing as distinct co-authors as direct proof they aren't the same person. |
| Merge 2 gets reversed too. | The skill reversed on any new evidence touching a merge, rather than only evidence that actually contradicts it. A reaffirming record must not trigger a reversal. |
| Merge 2 produces no output at all. | The skill only reported reversals and skipped logging the merges it rechecked and confirmed. Every merge in the history needs an explicit outcome. |

## Next Steps

- Review `patterns/reversible-merge-audit.md` in the course repo for the
  general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
