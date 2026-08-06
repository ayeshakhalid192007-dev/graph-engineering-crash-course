# document-to-facts Starter Kit

A runnable starter kit for the **document-to-facts** pattern: schema-first
extraction that converts a source document into typed, query-ready facts
rather than a free-form written summary. This kit's worked scenario is an invented
incident report, `INC-4482`, for a fictional company ("Northwind
Analytics") — not based on any real company or postmortem.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- No external services or API keys — the whole kit runs against the two
  local files described below.

## Quick Start

1. Review `PATTERN.md` to understand what schema-first extraction is
   solving for and what breaks without it.
2. Read `sample-input.md` — the incident report this kit extracts from.
3. Examine `schema.example.json` — the fixed list of entity types
   (`Service`, `Incident`, `Cause`) and relationship types (`caused-by`,
   `affected`) the extraction is allowed to produce.
4. Follow the tool-specific instructions below to run the kit.
5. Inspect `output.json` and confirm it matches the "Expected Output"
   section below — including the items that should have been rejected.

### Claude Code

1. Load the skill: `.claude/skills/extract-facts/SKILL.md`.
2. Ask it to run: "Use the extract-facts skill on sample-input.md with
   schema.example.json."
3. It writes `output.json` and prints a list of anything it dropped
   (with reasons).
4. Load the verifier: `.claude/agents/graph-verifier.md` and ask it to
   check `output.json` against `schema.example.json`. It independently
   confirms nothing outside the schema slipped through, and cross-checks
   its findings against the skill's own drop list.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json` (or point
   OpenCode at it directly).
2. Run the `extract` workflow step — it invokes
   `opencode/skills/extract-facts/SKILL.md` in extract mode over
   `sample-input.md` and writes `output.json`.
3. Run the `verify` workflow step — the same skill file, running in
   verify mode, independently re-checks `output.json` against
   `schema.example.json` and reports PASS/FAIL.

## Expected Output

Running extraction against `sample-input.md` should produce facts close
to this shape in `output.json`:

- **Entities:** `Service` nodes for `ingest-api`, `digest-scheduler`, and
  `alert-dispatcher`; an `Incident` node for `INC-4482`; a `Cause` node
  describing the leaked database connection in `ingest-api`'s CSV
  validation path.
- **Relationships:** `INC-4482 --caused-by--> <the leaked connection
  cause>`; `INC-4482 --affected--> digest-scheduler`; `INC-4482
  --affected--> alert-dispatcher`.
- **Rejected mentions:** the on-call engineer's name and the Slack
  channel named in the report should both appear in the drop list,
  since neither has an entity type in `schema.example.json`. Seeing them
  rejected — not silently absorbed into some other entity — is the
  behavior this kit exists to demonstrate.

If a run instead produces a `Person` entity for the engineer, or an
`escalated-to` relationship to the Slack channel, that's the schema not
being enforced — check that the skill read `schema.example.json` before
drafting candidates, not after.

## Modifying the Example

To adapt this kit to your own incident reports:

1. Replace `sample-input.md` with your own document.
2. Update `schema.example.json` if your domain needs different entity or
   relationship types — but treat that as a deliberate edit you review,
   not something extraction adds on the fly mid-run.
3. Re-run the skill and confirm `output.json` still matches the (possibly
   updated) schema, and that the verifier still passes.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `sample-input.md` — the invented `INC-4482` incident report this kit
  extracts from.
- `schema.example.json` — the fixed entity/relationship schema for this
  scenario.
- `.claude/skills/extract-facts/SKILL.md` — Claude Code extraction skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/extract-facts/SKILL.md` — OpenCode skill covering both
  extraction and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Output includes an entity type not in `schema.example.json` (e.g. `Person`). | The skill drafted candidates before reading the schema, or was asked to "just include everything." Re-run with the schema-first instruction intact. |
| Two runs over the same document produce different field names for the same fact. | The skill is falling back to free-form summarization instead of filtering against the schema. Check that step 1 of `SKILL.md` actually ran. |
| The verifier reports a discrepancy between its findings and the skill's self-reported drop list. | This is the verifier doing its job — it means the extraction's self-report undercounted or overcounted what it let through. Treat `output.json` as untrusted until the discrepancy is resolved. |

## Next Steps

- Review the pattern specification in `patterns/document-to-facts.md` in
  the course repo for the general (not scenario-specific) statement of
  this pattern.
- This is a core kit — see `starters/README.md` for how it relates to the
  other six core kits and the sixteen extended kits.
