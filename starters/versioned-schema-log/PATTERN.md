---
name: versioned-schema-log
category: C-provenance
stage: write
cost: low
tools: [Claude Code]
core: false
---

# versioned-schema-log

This kit is the runnable companion to the `versioned-schema-log` pattern
specification (`patterns/versioned-schema-log.md`). It is an extended
kit — a single Claude Code reference implementation, lighter than the
full multi-tool anatomy the seven core kits carry. See `starters/README.md`
for that distinction.

## What it does

Keeps a running log mapping every schema version the graph's extraction
pipeline has used to the specific run IDs performed under it. When the
schema changes — a field gets added, renamed, or dropped — that change
becomes its own logged version rather than an invisible shift underneath
runs that look identical from the outside.

## Inputs

- Each schema revision, as it's introduced: what fields it defines and
  when it took effect.
- The run IDs of every extraction performed against a given schema
  version.

## Outputs

- A log entry per schema version, listing its fields, its introduction
  date, and the full set of run IDs performed under it.

## Failure mode if skipped

The schema drifts underneath the graph without anyone noticing, and data
extracted before and after the drift ends up incomparable with no record
of when — or why — the shape changed. A field that's simply absent from
older runs looks like a data-quality bug rather than a known, documented
boundary, and nobody querying the graph later has any way to tell the
two apart.

## Worked scenario

Kestrel Wildlife Trust, a fictional highland reserve, runs camera traps
whose images feed an extraction pipeline that logs sightings into a
graph. From January through March, the pipeline ran under a schema
capturing only species, timestamp, and camera ID. In April, after several
wind-triggered false positives were misidentified as pine marten with no
way to flag the uncertainty, the trust's ecologists added two fields —
confidence score and the verifying ranger's ID — and started a new schema
version. Three runs happened under the old schema, two under the new one.
See `README.md` for the full version history and run list.

## Link to starter kit

**Kit:** `starters/versioned-schema-log/README.md`
