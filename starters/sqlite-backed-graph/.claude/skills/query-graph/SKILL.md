---
name: query-graph
description: Loads schema.sql into a local SQLite file, then answers availability and provenance questions against the nodes/edges tables with real SQL instead of re-reading source material
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Bash, Write]
---

# query-graph

Turns `schema.sql` into a queryable `graph.db` file, then answers a
question against the two tables it defines — an availability check on a
tool, or a provenance lookup on a specific edge — by running SQL, not by
re-reasoning over the Elm Street chat from scratch each time.

## Instructions

You are a Claude Code skill implementing the `sqlite-backed-graph`
pattern. Follow these steps in order:

1. **Load the database if it isn't already loaded.** Check whether
   `graph.db` exists in this kit's root. If it doesn't, build it by
   running `schema.sql` against a fresh file:
   `sqlite3 graph.db < schema.sql`, or, if the `sqlite3` CLI isn't
   available, the Python equivalent:
   `python3 -c "import sqlite3; sqlite3.connect('graph.db').executescript(open('schema.sql').read())"`.
   If `graph.db` already exists, leave it as is rather than reloading it —
   this step must be safe to skip on a second run.
2. **Turn on foreign key enforcement for this connection.** SQLite does
   not enforce `REFERENCES` constraints unless the connection asks for it,
   so every query in this skill must run `PRAGMA foreign_keys = ON;`
   first, even against an already-loaded `graph.db`.
3. **Resolve the question.** Default to this kit's worked question if the
   user doesn't name one: check whether the stud finder can be borrowed
   right now, and confirm the ladder's status too — which means running
   the availability query from step 4
   against both `tool-ladder` and `tool-stud-finder`.
4. **Run the availability query per tool.** For a given tool id, find its
   most recent `borrowed` edge by `id` (edge ids climb in the same order
   the source messages arrived, so the highest `id` is the latest
   `borrowed` edge):
   ```sql
   SELECT id, from_id FROM edges
   WHERE label = 'borrowed' AND to_id = :tool_id
   ORDER BY id DESC LIMIT 1;
   ```
   If no row comes back, the tool has never left its `owns` edge and is
   available. If a row comes back, check for a matching `returned` edge
   with a higher id:
   ```sql
   SELECT id FROM edges
   WHERE label = 'returned' AND to_id = :tool_id AND from_id = :borrower
     AND id > :borrowed_edge_id;
   ```
   A match means available (the tool came back); no match means still out
   with `:borrower`. Name the specific edge id(s) that produced the
   verdict — never report a verdict without the row backing it.
5. **Run the provenance query on request, or on the edge that grounded
   step 4's verdict.** For a specific edge id:
   ```sql
   SELECT source_doc, extraction_run_id, schema_version FROM edges
   WHERE id = :edge_id;
   ```
   This is the receipt-per-edge fields doing their job here: naming which
   source document, which extraction run, and which schema version
   produced the edge the verdict rests on.
6. **Write the result** to `output.json` (or the path the user requested)
   in this kit's root, with this shape: `queries` (an array, one entry per
   tool or edge checked, each carrying the SQL text run and its raw
   result), and `verdicts` (one entry per tool, with `tool`, `available`,
   `grounding_edge_id`, and — if not available — `held_by`).
7. **Report a summary** alongside the file: each tool's verdict, the edge
   id(s) it rests on, and that verdict's provenance (source document, run
   id, schema version) via step 5's lookup.

## Input

- `schema.sql` (this kit's root) — table definitions plus the worked
  example's `INSERT` statements.
- A question, from the user's request — a tool id to check availability
  for, or an edge id to look up provenance for. Defaults to checking both
  `tool-ladder` and `tool-stud-finder`.

## Output

- `graph.db` — the loaded SQLite database (created once, reused after).
- `output.json` (or user-specified path) — the queries run and their
  verdicts, per the shape in step 6.
- A printed summary matching what's in `output.json`.

## Example Usage

```
Use the query-graph skill to check whether anyone can currently borrow the stud finder.

Expected verdict:
  tool: tool-stud-finder
  available: false
  grounding_edge_id: e5 (borrowed, person-deepa, no later returned edge)
  provenance: source_doc=elm-street-chat.md,
    extraction_run_id=elm-street-extract-m5, schema_version=v1

Expected verdict for the ladder, run the same way:
  tool: tool-ladder
  available: true
  grounding_edge_id: e3 (returned, person-jason, closes out e2's borrowed edge)
```

## Validation

The companion agent (`.claude/agents/graph-verifier.md`) independently
re-loads `graph.db` (or rebuilds it from `schema.sql` if needed), reruns
the availability and provenance queries itself, and cross-checks its
findings against `output.json` — including a foreign-key integrity check
this skill doesn't perform on its own.
