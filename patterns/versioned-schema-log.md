---
name: versioned-schema-log
category: C-provenance
stage: write
cost: low
tools: [Claude Code]
core: false
---

# versioned-schema-log

## What it does

Keeps a running record of every schema version the graph has used, and
which extraction runs were performed under each one, so schema drift is
visible instead of implicit.

## Inputs

- Each schema revision as it's introduced.
- The run IDs of every extraction performed against a given schema version.

## Outputs

- A log entry mapping each schema version to the set of runs that used it.

## Failure mode if skipped

The schema drifts underneath the graph without anyone noticing, and data
extracted before and after the drift ends up incomparable with no record
of when — or why — the shape changed.

## Link to starter kit

**Kit:** `starters/versioned-schema-log/README.md`
