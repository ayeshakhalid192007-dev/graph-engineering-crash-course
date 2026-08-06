---
name: sqlite-backed-graph
category: G-storage
stage: storage
cost: low
tools: [Claude Code, OpenCode]
core: true
---

# sqlite-backed-graph

This kit is the runnable companion to the `sqlite-backed-graph` pattern
specification (`patterns/sqlite-backed-graph.md`). It works one concrete
scenario end to end: the Elm Street tool-cabinet chat this course already
built once in Step 15, now stored as two related tables in a single local
`.db` file and queried with ordinary SQL, instead of held together only
inside one agent's working memory for the length of a single pass.

## What it does

Loads a `nodes` table and an `edges` table into one SQLite database, the
edges table pointing back into the nodes table through a pair of foreign
keys, and answers questions about the stored graph by querying those two
tables directly rather than re-deriving the graph from source material
every time a question comes up. Every edge also carries the three receipt
fields this course's `receipt-per-edge` pattern defines — `source_doc`,
`extraction_run_id`, `schema_version` — as ordinary columns, so a
provenance lookup is a `WHERE` clause, not a separate system bolted on
after the fact.

## Inputs

- `schema.sql`, which this kit ships already carrying both halves of what
  a run needs: the `CREATE TABLE` statements for `nodes` and `edges`, and
  a set of `INSERT` statements loading this kit's worked example — six
  nodes and five edges drawn from the Elm Street scenario.
- A question to answer against the loaded database: an availability check
  ("does anyone currently have the stud finder?") or a provenance lookup
  ("which message, run, and schema version produced a given edge?").

## Outputs

- `graph.db`, a queryable SQLite file holding the full loaded graph.
- `output.json`, recording the specific query or queries run, the SQL
  text used, and the result — an availability verdict naming the edge(s)
  that grounded it, or a provenance record naming the source document,
  run id, and schema version behind a given edge.

## Failure mode if skipped

Without a table with an enforced foreign key, nothing stops a write from
landing an edge whose `from_id` or `to_id` names a node that was never
created — the row sits there silently until a query that happens to join
through it comes back short, and by then it's unclear whether the node
was deleted, mistyped, or never written at all. Holding the graph only in
an agent's context instead has its own cost: every session that needs an
answer has to re-read and re-derive the whole thing from source material
again, and two sessions answering the same question can silently diverge
if either one re-derives it slightly differently.

## Worked scenario

`schema.sql` loads six nodes — four `Person` rows (Kavita, Marcus, Jason
R., Deepa) and two `Tool` rows (ladder, stud finder) — and five edges,
one per message in the Elm Street chat: an `owns` edge for each tool's
original holder, a `borrowed` edge each time someone took a tool, and one
`returned` edge closing out the ladder's loan. The person node behind
message 2's "Jay" and message 3's "Jason R." is a single row carrying
both names in its `data` column — that merge already happened before this
file was written, so this kit's job is limited to storing and querying
the result faithfully, not re-deciding it. Querying the loaded database
for the stud finder's status turns up its `borrowed` row with nothing
closing it out, so the answer comes back "still out" — grounded in
one row this kit's `query-graph` skill can name, not a summary of the
chat. See `README.md` for how to load and query it.

## Link to starter kit

**Kit:** `starters/sqlite-backed-graph/README.md`
