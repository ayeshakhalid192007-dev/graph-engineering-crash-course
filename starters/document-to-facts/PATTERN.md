---
name: document-to-facts
category: A-extraction
stage: write
cost: medium
tools: [Claude Code, OpenCode]
core: true
---

# document-to-facts

This kit is the runnable companion to the `document-to-facts` pattern
specification (`patterns/document-to-facts.md`). It works one concrete
scenario end to end: an invented incident report for a fictional analytics
company, `Northwind Analytics`, gets turned into a small set of typed facts
instead of a paragraph summary.

## What it does

Locks down the shape of an acceptable answer — a list of entity types and
a list of relationship types — before any text gets read. The extraction
pass then reads the source document once and only keeps items that match
one of those shapes exactly; everything else, however plausible it reads,
is discarded and reported as discarded rather than folded in. The point
isn't to summarize the document better. It's to produce output a second
process can query, diff, or cross-reference without first guessing what
field names a particular run happened to choose.

## Inputs

- A source document narrow enough for one extraction pass. This kit ships
  `sample-input.md`, an invented incident report (`INC-4482`) about a
  fictional company's ingestion pipeline.
- A schema spelling out, in advance, the fixed list of node kinds and
  edge kinds the graph will hold. This kit ships `schema.example.json`,
  which restricts the scenario to three entity types (`Service`,
  `Incident`, `Cause`) and two relationship types (`caused-by`,
  `affected`).

## Outputs

- Entity nodes — one per `Service`, `Incident`, or `Cause` the document
  actually names — each carrying only the properties the schema lists for
  its type.
- Relationship edges — `caused-by` linking an `Incident` to a `Cause`, and
  `affected` linking an `Incident` to a `Service` — with the source
  document recorded on each edge.
- A list of anything the document mentioned that didn't fit the schema,
  so a rejected mention is visible rather than silently absorbed.

## Failure mode if skipped

Ask a model to "pull the facts" out of a document with no schema in hand
and you get a fluent, competent summary — a different fluent, competent
summary on the next run, with different field names, different
granularity, and no guarantee the same fact survives twice. That's fine
for a human reading it once. It breaks the moment anything downstream
tries to query the result, compare it against a second document, or
detect that two runs disagree about the same incident, because there was
never a fixed shape for "disagree" to be measured against.

## Worked scenario

`sample-input.md` describes `INC-4482`: daily digest emails going out
roughly fourteen hours late because a leaked database connection in
`ingest-api`'s CSV validation path exhausted its connection pool, which
then starved `digest-scheduler` and `alert-dispatcher`. The document also
mentions an on-call engineer and a Slack channel by name — deliberately,
so the extraction has something to reject. See `README.md` for how to run
the kit against it.

## Link to starter kit

**Kit:** `starters/document-to-facts/README.md`
