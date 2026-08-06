---
name: attach-receipts
description: Attaches source_doc/extraction_run_id/schema_version receipts to every edge at write time, and refuses to write any edge missing one of the three
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# attach-receipts

Turns a batch of candidate edges — each proposed alongside the metadata of
the run that produced it — into written edges that carry a full receipt,
or into a refusal with a stated reason. No edge gets written with a
guessed or blank receipt field.

## Instructions

You are a Claude Code skill implementing the `receipt-per-edge` pattern.
A receipt is not optional metadata to fill in when convenient — it's a
precondition for writing the edge at all. Follow these steps in order:

1. **Read the schema first.** Open `schema.example.json` and note the
   fixed edge shape: `subject`, `predicate`, `object`, plus the three
   receipt fields `source_doc`, `extraction_run_id`, `schema_version`.
   Note what `v1` and `v2` each additionally require of a `caused-by`
   edge (`v2` adds `impact_scope`). Treat this shape as fixed for the
   run.
2. **Read the source material.** Default to `sample-input.md` in this kit
   unless the user names a different file. Pull out every write request
   it lists, each with its candidate edge and the run metadata attached
   to it.
3. **Check the schema-version-specific fields first.** For each candidate
   edge, confirm it carries every field its stated `schema_version`
   requires (e.g. a `v2` `caused-by` edge must carry `impact_scope`). If
   a schema-version-specific field is missing, refuse the edge and report
   which field and which schema version required it.
4. **Check all three receipt fields next — this is the step that must
   never be skipped.** For every candidate edge that passed step 3,
   confirm `source_doc`, `extraction_run_id`, and `schema_version` are
   all present and non-empty. If any one of the three is missing, blank,
   or `null`, refuse to write that edge. Do not substitute a placeholder,
   do not infer a run id from context, and do not write the edge with the
   field left out "for now" — a missing receipt field is a hard stop, not
   a warning.
5. **Write every candidate edge that passed both checks**, with its
   subject/predicate/object, any schema-version-specific fields, and all
   three receipt fields populated exactly as given. Write the result to
   `output.json` (or the path the user requested) in this kit's root,
   following `schema.example.json`'s edge shape.
6. **Report every refused candidate edge** by its subject/predicate/object
   and the specific missing field, alongside the written edges. A run
   that silently drops a refused edge without saying why has failed this
   step just as much as one that wrote the edge anyway.
7. **Confirm distinguishability before finishing:** if more than one
   written edge shares the same subject/predicate/object (as write
   requests A and B do in this kit's scenario), check that their receipt
   fields alone are enough to tell them apart — different
   `extraction_run_id`, different `schema_version`. State this check
   explicitly in your output rather than assuming it.

## Input

- `schema.example.json` — the fixed edge shape and the schema-version
  requirements for `caused-by` edges.
- `sample-input.md` — the source document and candidate write requests
  (or another file the user names).

## Output

- `output.json` (or user-specified path) — every written edge, matching
  `schema.example.json`'s shape, with all three receipt fields populated.
- A printed list of any candidate edges refused for a missing receipt
  field (or a missing schema-version-specific field), naming the field.

## Example Usage

```
Run the attach-receipts skill on sample-input.md using schema.example.json.
Expected writes:
  charge-dock-3 --caused-by--> voltage-sensor-drift
    receipt: source_doc=RCA-3309, extraction_run_id=rca3309-extract-a, schema_version=v1
  charge-dock-3 --caused-by--> voltage-sensor-drift
    impact_scope: haul-bot-12, haul-bot-15 delayed charging ~40 min
    receipt: source_doc=RCA-3309, extraction_run_id=rca3309-extract-b, schema_version=v2
Expected refusal:
  charge-dock-3 --caused-by--> voltage-sensor-drift (run rca3309-extract-c)
    refused: extraction_run_id missing
```

## Validation

The companion agent (`.claude/agents/graph-verifier.md`) independently
re-checks `output.json` against `schema.example.json` and flags any
written edge missing a receipt field, or any refused edge that made it
into the output anyway.
