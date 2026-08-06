---
name: receipt-per-edge
category: C-provenance
stage: write
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# receipt-per-edge

This kit is the runnable companion to the `receipt-per-edge` pattern
specification (`patterns/receipt-per-edge.md`). It works one concrete
scenario end to end: a fictional warehouse-robotics company's root-cause
report gets extracted twice, once under an older schema and once under a
newer one, and the kit has to attach a receipt to every edge it writes so
the two extractions stay distinguishable instead of blurring together.

## What it does

Attaches three receipt fields — `source_doc`, `extraction_run_id`,
`schema_version` — to every edge at the moment it's written, and refuses
to write any edge missing one of them. A candidate edge with a claim but
no run id, or a schema version but no source document, doesn't get
written with a blank spot to fill in later; it gets rejected outright and
reported as rejected, the same way a schema-mismatched entity gets
reported as dropped in `document-to-facts`.

## Inputs

- A batch of candidate edges to write, each proposed alongside the
  metadata of the run that produced it: source document, extraction run
  id, schema version in effect. This kit ships `sample-input.md`, which
  pairs a root-cause report for a fictional warehouse-robotics company,
  Talus Robotics, with three candidate edges spanning two schema
  versions.
- A schema fixing the shape every written edge must match. This kit ships
  `schema.example.json`, which defines a single edge shape carrying
  `subject`/`predicate`/`object` plus the three receipt fields, and
  states what `caused-by` edges require differently between schema `v1`
  and schema `v2`.

## Outputs

- Every edge that gets written, carrying all three receipt fields
  populated — never blank, never a placeholder.
- A list of any candidate edges refused for missing one of the three
  receipt fields, with the specific field named.

## Failure mode if skipped

Strip the receipt fields off and an edge becomes an unattributed
assertion — nobody reading the graph later can pin down where it entered,
under what rules, or from which pass of the extraction pipeline. Two
edges making the same claim under two different schema versions collapse
into duplicates with no field left to tell them apart, and a run that
quietly dropped its own logging looks identical to a run that never
happened at all, since both leave the same blank behind.

## Worked scenario

`sample-input.md` gives a root-cause report, `RCA-3309`, describing a
charging-dock fault in Talus Robotics's warehouse-robot fleet. The report
gets extracted twice: once under schema `v1`, which only asks a
`caused-by` edge to carry the bare claim, and once under schema `v2`,
which adds a required `impact_scope` field naming which robots the fault
delayed. Both extraction passes carry complete receipts and should be
written. A third candidate edge — from a run whose logging dropped its
own extraction run id before the edge reached the write step — has every
other field filled in and should still be refused. See `README.md` for
how to run the kit against it.

## Link to starter kit

**Kit:** `starters/receipt-per-edge/README.md`
