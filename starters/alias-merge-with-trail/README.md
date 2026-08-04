# alias-merge-with-trail Starter Kit

A runnable starter kit for the **alias-merge-with-trail** pattern: folding
two surface names for the same entity into one canonical node while
keeping every original mention individually retrievable. This kit's worked
scenario involves a fictional freight company ("Meridian Freight") and an
invented backend system — not based on any real company or incident.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- No external services or API keys — the whole kit runs against the two
  local files described below.

## Quick Start

1. Review `PATTERN.md` to understand what this pattern solves for and
   what breaks without it.
2. Read `sample-input.md` — the two source excerpts this kit merges
   mentions from.
3. Examine `schema.example.json` — the fixed shape of a canonical
   `Service` entity and of a retained mention record.
4. Follow the tool-specific instructions below to run the kit.
5. Inspect `output.json` and confirm it matches the "Expected Output"
   section below — including the pair that should have been left
   unmerged.

### Claude Code

1. Load the skill: `.claude/skills/merge-aliases/SKILL.md`.
2. Ask it to run: "Use the merge-aliases skill on sample-input.md with
   schema.example.json."
3. It writes `output.json` and prints the list of any candidate pairs it
   chose not to merge, with reasons.
4. Load the verifier: `.claude/agents/graph-verifier.md` and ask it to
   check `output.json` against `schema.example.json`. It independently
   confirms no mention was lost, no reason was watered down to bare name
   similarity, and nothing was over-merged.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json` (or point
   OpenCode at it directly).
2. Run the `merge` workflow step — it invokes
   `opencode/skills/merge-aliases/SKILL.md` in merge mode over
   `sample-input.md` and writes `output.json`.
3. Run the `verify` workflow step — the same skill file, running in
   verify mode, independently re-checks `output.json` against
   `schema.example.json` and reports PASS/FAIL.

## Expected Output

Running the merge against `sample-input.md` should produce facts close to
this shape in `output.json`:

- **Merged:** one canonical `Service` entity named `billing-svc`, with
  `merge_reason` naming the shared 14:03-14:24 UTC window on
  2026-03-03 and the explicit cross-reference to support ticket #5821 in
  the change log. Its `mentions` array holds two entries — `"the payments
  service"` (from Support Ticket #5821, `retrievable: true`) and
  `"billing-svc"` (from the Infrastructure Change Log, `retrievable:
  true`).
- **Left unmerged:** the decoy pair — `"the notifications thing"` and
  `notify-svc` — stays as two separate entities, since nothing in
  `sample-input.md` links their sources beyond appearing in the same two
  documents.

### Checking retrievability

The whole point of this kit is that neither original name goes dark once
the merge happens. To confirm it:

- Look up `"the payments service"` in `output.json`: it should resolve to
  the `billing-svc` canonical entity and surface both mentions, including
  itself.
- Look up `"billing-svc"` the same way: it should resolve to the same
  canonical entity and surface both mentions, including the support
  ticket's wording.

If either lookup comes back empty, or only shows one of the two mentions,
the merge silently dropped a mention — that is exactly the failure this
kit exists to catch, and the verifier should flag it (see "Symptom" table
below).

## Modifying the Example

To adapt this kit to your own alias-merge scenario:

1. Replace `sample-input.md` with your own pair (or cluster) of sources
   describing a shared entity under different names.
2. Update `schema.example.json` if your domain needs a different entity
   type or different mention properties — but treat that as a deliberate
   edit you review, not something the merge step adds on the fly mid-run.
3. Re-run the skill and confirm `output.json` still keeps every original
   mention retrievable, and that the verifier still passes.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `sample-input.md` — the Meridian Freight support ticket and change log
  this kit merges mentions from.
- `schema.example.json` — the fixed canonical-entity and mention-record
  shape for this scenario.
- `.claude/skills/merge-aliases/SKILL.md` — Claude Code merge skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/merge-aliases/SKILL.md` — OpenCode skill covering both
  merging and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| A lookup by `"the payments service"` or `"billing-svc"` returns nothing, or returns only one of the two mentions. | The merge overwrote or discarded a mention instead of appending it. Re-run and check that step 4 of `SKILL.md` kept both entries. |
| The two decoy mentions (`"the notifications thing"` / `notify-svc`) got merged into one entity. | The skill matched on name resemblance instead of requiring a shared timestamp or cross-reference. Check that step 3 of `SKILL.md` actually looked for concrete evidence before grouping. |
| `merge_reason` just says the names are similar or "probably the same." | The skill accepted a weak justification. A reason must name a specific shared fact — a timestamp window, a ticket reference — not a description of the names themselves. |
| The verifier reports a discrepancy between its findings and the skill's self-reported skip list. | This is the verifier doing its job — it means the merge run's self-report undercounted or overcounted what it actually combined. Treat `output.json` as untrusted until the discrepancy is resolved. |

## Next Steps

- Review the pattern specification in `patterns/alias-merge-with-trail.md`
  in the course repo for the general (not scenario-specific) statement of
  this pattern.
- This is a core kit — see `starters/README.md` for how it relates to the
  other six core kits and the sixteen extended kits.
