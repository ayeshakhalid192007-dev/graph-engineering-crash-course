---
name: extract-facts
description: Extracts Service/Incident/Cause facts from an incident-report document against a fixed schema, rejecting anything the schema doesn't define
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---

# extract-facts

Turns an incident-report document into typed entity and relationship JSON
matching `schema.example.json`, instead of a prose summary. Nothing goes
into the output unless its entity type and relationship type both appear
in the schema.

## Instructions

You are a Claude Code skill implementing the `document-to-facts` pattern.
Do not summarize the document. Do not invent an entity or relationship
type just because the source text mentions something that isn't on the
list. Follow these steps in order:

1. **Read the schema first, before reading the document.** Open
   `schema.example.json` in this kit and write down its two lists side by
   side: the three entity types it names (`Service`, `Incident`,
   `Cause`) and the two relationships, each with its required direction
   (a `caused-by` edge always runs from an `Incident` to a `Cause`; an
   `affected` edge always runs from an `Incident` to a `Service`). Note
   the required properties listed for each type. Treat this list as
   frozen for the whole run — nothing gets added to it mid-extraction.
2. **Read the source document.** Default to `sample-input.md` in this kit
   unless the user points you at a different file.
3. **Draft candidate facts.** For every statement in the document that
   looks like an entity or a relationship, write down a candidate in the
   form `{entity_type, entity_properties}` or `{relationship_type, from,
   to}`. Be generous at this stage — over-collect rather than
   under-collect.
4. **Filter every candidate against the schema from step 1.** Keep a
   candidate only if:
   - for an entity: its `entity_type` is one of `Service`, `Incident`,
     `Cause`, and its properties are a subset of that type's allowed
     properties;
   - for a relationship: its `relationship_type` is one of `caused-by` or
     `affected`, and the types of its `from` and `to` entities match what
     the schema declares for that relationship.
   Drop everything else. Do not rename a candidate's type to make it fit
   (e.g. do not relabel a `Person` as a `Service`) — a mismatched
   candidate is dropped, not reshaped.
5. **Record every dropped candidate** with the reason it failed (unknown
   entity type, unknown relationship type, or a `from`/`to` type
   mismatch). The on-call engineer's name and the Slack channel mentioned
   in `sample-input.md` are expected to be dropped here — that's the
   schema working as intended, not a bug to fix.
6. **Emit the surviving facts as JSON** shaped like
   `schema.example.json`'s `entities` and `relationships` arrays, with
   each relationship tagged with a `source_document` property naming the
   file you read in step 2. Write the result to `output.json` in the
   kit's root (or the path the user requested) and also print it.
7. **Print the drop list from step 5** alongside the JSON so a human can
   see what was excluded and why, without having to re-run the extraction
   to find out.

## Input

- `schema.example.json` — the fixed list of entity/relationship types and
  their properties.
- `sample-input.md` — the incident report to extract from (or another
  file the user names).

## Output

- `output.json` (or user-specified path) — entities and relationships
  matching the schema, each relationship carrying `source_document`.
- A printed drop list of candidates that failed the schema check, with
  reasons.

## Example Usage

```
Run the extract-facts skill on sample-input.md using schema.example.json.
Expected surviving facts:
  Service: ingest-api, digest-scheduler, alert-dispatcher
  Incident: INC-4482
  Cause: leaked database connection in ingest-api's CSV validation path
  caused-by: INC-4482 -> leaked database connection ...
  affected: INC-4482 -> digest-scheduler
  affected: INC-4482 -> alert-dispatcher
Expected drops:
  "Priya Raman" — no Person entity type in schema
  "#northwind-incidents" — no Channel entity type in schema
```

## Validation

The companion agent (`.claude/agents/graph-verifier.md`) independently
re-checks `output.json` against `schema.example.json` and flags any
entity or relationship type that slipped through outside the allowed
list.
