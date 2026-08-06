# file-graph-for-small-teams Starter Kit

A single-tool (Claude Code) reference kit for the
**file-graph-for-small-teams** pattern: storing the graph as plain JSON
in a git repository so a change to it is an ordinary, diffable pull
request rather than a database migration. This is an extended kit — see
`starters/README.md` for how that differs from the seven core kits.

Larkspur Tape Archive and the reels below are invented for this course,
not drawn from any real archive, station, or recording.

## Prerequisites

- Claude Code.
- No external services or API keys — `graph.json` below and the
  proposed additions are everything the kit needs.

## Quick Start

1. Review `PATTERN.md` for what this pattern solves and what breaks
   without it.
2. Read the current `graph.json` state and the two proposed additions
   below.
3. Follow the Claude Code instructions to run the kit.
4. Compare what it produces against "Expected Output" below.

### Current `graph.json` (already merged, shared history)

```json
{
  "nodes": [
    { "id": "reel:LT-0398", "type": "reel", "found": "spring 1987" },
    { "id": "program:nightline-request-hour", "type": "program" },
    { "id": "host:dana-voss", "type": "host", "announcer_id": "D.V." },
    { "id": "host:renata-kwan", "type": "host", "announcer_id": "R.K." }
  ],
  "edges": [
    { "subject": "reel:LT-0398", "predicate": "recorded-during", "object": "program:nightline-request-hour" },
    { "subject": "reel:LT-0398", "predicate": "hosted-by", "object": "host:dana-voss" }
  ]
}
```

### Proposed addition 1 — reel LT-0447 (uncontested)

A volunteer cataloging a second newly found reel proposes:

```json
{ "id": "reel:LT-0447", "type": "reel", "found": "estimated spring 1987" }
{ "subject": "reel:LT-0447", "predicate": "recorded-during", "object": "program:nightline-request-hour" }
{ "subject": "reel:LT-0447", "predicate": "hosted-by", "object": "host:dana-voss" }
```

The reel's own on-tape announcer identification, logged elsewhere on the
box, reads "D.V." — matching `host:dana-voss`'s `announcer_id`.

### Proposed addition 2 — reel LT-0452 (misattributed)

A different volunteer, working from a box label alone, proposes:

```json
{ "id": "reel:LT-0452", "type": "reel", "found": "estimated spring 1987" }
{ "subject": "reel:LT-0452", "predicate": "recorded-during", "object": "program:nightline-request-hour" }
{ "subject": "reel:LT-0452", "predicate": "hosted-by", "object": "host:renata-kwan" }
```

The reel's own on-tape announcer identification reads "D.V." — the box
label's handwriting was misread as an "R" rather than a "D."

### Claude Code

1. Load the skill: `.claude/skills/propose-graph-diff/SKILL.md`.
2. Ask it to run: "Use the propose-graph-diff skill on both proposed
   additions against the current graph.json in README.md."
3. It prints a minimal diff for each proposed addition, plus a separate
   flagged-for-review list for anything that doesn't match an existing
   cross-reference already on file.

## Expected Output

- **Reel LT-0447 — diff only, no flag.** The proposed `hosted-by` edge
  names `host:dana-voss`, matching the reel's own on-tape announcer ID
  ("D.V."). The diff is minimal: three new lines (one node, two edges),
  nothing about the existing reels touched.
- **Reel LT-0452 — diff, plus flagged for review.** The proposed
  `hosted-by` edge names `host:renata-kwan`, but the reel's own on-tape
  announcer ID ("D.V.") matches `host:dana-voss`'s `announcer_id`, not
  `host:renata-kwan`'s ("R.K."). The skill still emits the diff line as
  proposed — it does not silently correct it to the host it thinks is
  right — but flags it explicitly as conflicting with an existing
  cross-reference, for a human reviewer to resolve in the PR.
- Neither proposal is written directly into `graph.json` by the skill
  itself — both come back as a diff for a human to review and merge.

### Checking the result

- Confirm LT-0447's diff has no flag attached — a run that flags an
  uncontested addition is being too aggressive.
- Confirm LT-0452's diff is still produced (not silently dropped or
  silently corrected), and that the flag names the specific conflict:
  the announcer ID on file for `host:dana-voss` versus the host named in
  the proposed edge.
- Confirm neither diff is described as already merged — the skill's
  output is something for a second volunteer to review, not a completed
  write to the shared file.

## Modifying the Example

1. Replace `graph.json` and the proposed additions with your own team's
   graph and catalog entries.
2. Re-run the skill and confirm it still produces a minimal diff for
   every proposal, and still flags only the proposals that actually
   conflict with an existing on-file cross-reference — not every
   proposal touching a node with more than one recorded fact about it.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if skipped.
- `.claude/skills/propose-graph-diff/SKILL.md` — the Claude Code skill.
- `PORTING.md` — notes on adapting this kit to OpenCode.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| LT-0452's misattributed edge gets written with no flag. | The skill didn't cross-check the proposed host against the announcer ID already on file for the existing host nodes. |
| LT-0447 gets flagged even though nothing conflicts. | The skill is flagging every proposal touching a node with more than one existing fact, instead of only proposals that actually contradict an on-file cross-reference. |
| The skill "fixes" LT-0452's host to `dana-voss` on its own. | This pattern's skill proposes a diff and flags a conflict; it does not resolve which host is correct — that decision belongs to the human reviewing the PR. |
| The diff for either proposal includes unrelated lines from elsewhere in `graph.json`. | The diff must be minimal — only the new or changed lines for the proposal at hand, so a PR reviewer sees exactly what changed. |

## Next Steps

- Review `patterns/file-graph-for-small-teams.md` in the course repo for
  the general (not scenario-specific) statement of this pattern.
- This is an extended kit — see `starters/README.md` for how it relates
  to the seven core kits and the other fifteen extended kits.
