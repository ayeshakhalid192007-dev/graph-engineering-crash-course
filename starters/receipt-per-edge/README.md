# receipt-per-edge Starter Kit

A runnable starter kit for the **receipt-per-edge** pattern: attaching a
receipt — source document, extraction run id, schema version — to every
edge at the moment it's written, and refusing to write an edge that's
missing one. This kit's worked scenario involves a fictional
warehouse-robotics company ("Talus Robotics") and an invented root-cause
report — not based on any real company or incident.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- No external services or API keys — the whole kit runs against the two
  local files described below.

## Quick Start

1. Review `PATTERN.md` to understand what this pattern solves for and
   what breaks without it.
2. Read `sample-input.md` — the root-cause report and the three candidate
   edges this kit attaches receipts to.
3. Examine `schema.example.json` — the fixed edge shape, and what schema
   `v1` and schema `v2` each require of a `caused-by` edge.
4. Follow the tool-specific instructions below to run the kit.
5. Inspect `output.json` and confirm it matches the "Expected Output"
   section below — including the candidate edge that should have been
   refused.

### Claude Code

1. Load the skill: `.claude/skills/attach-receipts/SKILL.md`.
2. Ask it to run: "Use the attach-receipts skill on sample-input.md with
   schema.example.json."
3. It writes `output.json` and prints the list of any candidate edges it
   refused to write, with reasons.
4. Load the verifier: `.claude/agents/graph-verifier.md` and ask it to
   check `output.json` against `schema.example.json`. It independently
   confirms every written edge carries all three receipt fields
   populated, and cross-checks its findings against the skill's own
   refusal list.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json` (or point
   OpenCode at it directly).
2. Run the `attach` workflow step — it invokes
   `opencode/skills/attach-receipts/SKILL.md` in attach mode over
   `sample-input.md` and writes `output.json`.
3. Run the `verify` workflow step — the same skill file, running in
   verify mode, independently re-checks `output.json` against
   `schema.example.json` and reports PASS/FAIL.

## Expected Output

Running the kit against `sample-input.md` should produce edges close to
this shape in `output.json`:

- **Written (schema v1):** `charge-dock-3 --caused-by--> voltage-sensor-drift`,
  receipt `{source_doc: RCA-3309, extraction_run_id: rca3309-extract-a,
  schema_version: v1}`.
- **Written (schema v2):** `charge-dock-3 --caused-by--> voltage-sensor-drift`,
  now also carrying `impact_scope: "haul-bot-12, haul-bot-15 delayed
  charging ~40 min"`, receipt `{source_doc: RCA-3309, extraction_run_id:
  rca3309-extract-b, schema_version: v2}`.
- **Refused:** the third candidate edge (run `rca3309-extract-c`) — every
  field is present except `extraction_run_id`, which the run's own
  logging dropped before the edge reached the write step. It should
  appear in the refusal list, not in `output.json` with a blank or
  guessed run id.

### Checking receipts

The whole point of this kit is that no edge gets written without a full
receipt. To confirm it:

- Open `output.json` and check both written edges: each must have all
  three of `source_doc`, `extraction_run_id`, and `schema_version`
  populated with non-empty values.
- Confirm the two written edges are distinguishable from each other by
  `schema_version` alone (`v1` vs `v2`), even though they share the same
  `subject`/`predicate`/`object`.

If either written edge is missing a receipt field, or the refused
candidate shows up in `output.json` anyway, the skill wrote an edge it
should have refused — that is exactly the failure this kit exists to
catch, and the verifier should flag it (see "Symptom" table below).

## Modifying the Example

To adapt this kit to your own receipt-per-edge scenario:

1. Replace `sample-input.md` with your own source document and candidate
   edges.
2. Update `schema.example.json` if your domain needs different edge
   fields or a different set of schema versions — but treat that as a
   deliberate edit you review, not something the write step adds on the
   fly mid-run.
3. Re-run the skill and confirm `output.json` still keeps every written
   edge fully receipted, and that the verifier still passes.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `sample-input.md` — the Talus Robotics root-cause report and candidate
  edges this kit attaches receipts to.
- `schema.example.json` — the fixed edge shape and schema-version
  requirements for this scenario.
- `.claude/skills/attach-receipts/SKILL.md` — Claude Code write skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/attach-receipts/SKILL.md` — OpenCode skill covering
  both writing and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| An edge in `output.json` has an empty or missing `source_doc`, `extraction_run_id`, or `schema_version`. | The skill wrote the edge before checking all three receipt fields were present. Re-run and check that step 4 of `SKILL.md` ran before the write. |
| The refused candidate edge (run `rca3309-extract-c`) shows up in `output.json` anyway. | The skill filled in a missing field instead of refusing the edge outright. A missing receipt field must block the write, not get patched with a guess or a placeholder. |
| The two `v1`/`v2` edges for the same claim can't be told apart. | `schema_version` (or another receipt field) was dropped or overwritten on one of the edges. Each edge's receipt must independently reflect the run that produced it. |
| The verifier reports a discrepancy between its findings and the skill's self-reported refusal list. | This is the verifier doing its job — it means the write run's self-report undercounted or overcounted what it actually refused. Treat `output.json` as untrusted until the discrepancy is resolved. |

## Next Steps

- Review the pattern specification in `patterns/receipt-per-edge.md` in
  the course repo for the general (not scenario-specific) statement of
  this pattern.
- This is a core kit — see `starters/README.md` for how it relates to the
  other six core kits and the sixteen extended kits.
