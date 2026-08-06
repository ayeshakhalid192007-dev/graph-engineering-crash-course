---
name: receipt-per-edge
category: C-provenance
stage: write
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# receipt-per-edge

## What it does

Attaches the source document, the extraction run ID, and the schema
version to every edge at the moment it's written, so provenance travels
with the claim from the start instead of being reconstructed after the
fact (the write-path habit from Step 8).

## Inputs

- A newly created edge.
- The metadata of the run that produced it: source document, run ID,
  schema version in effect.

## Outputs

- The same edge, now carrying three provenance fields alongside its
  subject/predicate/object.

## Failure mode if skipped

A claim sits in the graph with no way to trace which document, which
extraction run, or which schema version put it there — so nothing can
check it, and nothing can un-trust it if the source turns out unreliable.

## Link to starter kit

**Kit:** `starters/receipt-per-edge/README.md`
