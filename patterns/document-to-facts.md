---
name: document-to-facts
category: A-extraction
stage: write
cost: medium
tools: [Claude Code, OpenCode]
core: true
---

# document-to-facts

## What it does

Runs extraction against a schema that's fixed before the first prompt is
written, turning a source document into typed entity and relationship
nodes instead of a prose summary. The schema decides in advance what shape
an acceptable answer takes, so the extraction step has something concrete
to check its own output against (this is the write-path move covered in
Step 6 of the course).

## Inputs

- A source document, or a chunk of one small enough for a single extraction
  pass.
- A schema describing which entity types and relationship types the graph
  accepts.

## Outputs

- One or more typed nodes representing entities found in the document.
- Typed edges connecting those nodes, each tagged with the document it was
  drawn from.

## Failure mode if skipped

Without a schema to extract against, the default is a free-form summary —
readable to a human in the moment, but nothing later can query it, cross
check it against another document, or verify a downstream claim against it.

## Link to starter kit

**Kit:** `starters/document-to-facts/README.md`
