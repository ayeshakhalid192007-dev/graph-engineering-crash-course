# sqlite-backed-graph Starter Kit

A runnable starter kit for the **sqlite-backed-graph** pattern: storing a
graph's nodes and edges as two related SQLite tables, joined by foreign
keys, and querying it with SQL instead of re-deriving the graph from
source material on every question. This kit's worked example reuses the
Elm Street tool-cabinet scenario from Step 15 of this course
(`docs/08-part-6-one-graph-end-to-end/step-15-build-the-same-graph-twice.md`)
— five real households sharing tools is fictional too, but it's already
this course's own worked system, not invented fresh for this kit.

## Prerequisites

- Claude Code, or OpenCode, or both (this kit ships a working
  implementation for each).
- A way to run SQLite: either the `sqlite3` CLI, or Python 3 (its
  standard library ships a `sqlite3` module, so no separate install is
  needed if `python3` is already on the machine). No external services,
  no API keys, no network calls — the whole kit runs against one local
  `.db` file.

## Quick Start

1. Review `PATTERN.md` to understand what this pattern solves for and
   what breaks without it.
2. Read `schema.sql` — the two `CREATE TABLE` statements, plus the
   `INSERT` statements that load the Elm Street worked example (four
   `Person` nodes, two `Tool` nodes, five edges).
3. Examine `schema.example.json` for the row shape reference: what fields
   a node row and an edge row each carry.
4. Follow the tool-specific instructions below to run the kit.
5. Inspect `output.json` and confirm it matches the "Expected Output"
   section below.

### Claude Code

1. Load the skill: `.claude/skills/query-graph/SKILL.md`.
2. Ask it to run: "Use the query-graph skill to check whether the ladder
   and the stud finder are available."
3. It builds `graph.db` from `schema.sql` (if not already built), runs
   the availability and provenance queries, writes `output.json`, and
   prints a summary of both verdicts.
4. Load the verifier: `.claude/agents/graph-verifier.md` and ask it to
   check `output.json` against `graph.db`. It independently re-runs both
   queries from scratch, checks foreign-key integrity, and cross-checks
   its findings against the skill's own report.

### OpenCode

1. Copy `opencode/opencode.json.example` to `opencode.json` (or point
   OpenCode at it directly).
2. Run the `load-and-query` workflow step — it invokes
   `opencode/skills/query-graph/SKILL.md` in query mode, building
   `graph.db` from `schema.sql` and writing `output.json`.
3. Run the `verify` workflow step — the same skill file, running in
   verify mode, independently re-derives both verdicts from `graph.db`
   and reports PASS/FAIL.

## Expected Output

Running the kit should produce verdicts close to this shape in
`output.json`:

- **`tool-ladder`:** `available: true`, grounded in edge `e3` — a
  `returned` edge from `person-jason` with a higher id than `e2`, the
  `borrowed` edge it closes out. Provenance: `source_doc:
  elm-street-chat.md, extraction_run_id: elm-street-extract-m3,
  schema_version: v1`.
- **`tool-stud-finder`:** `available: false`, `held_by: person-deepa`,
  grounded in edge `e5` — its `borrowed` row, nothing in the table
  closes it out. Provenance: `source_doc:
  elm-street-chat.md, extraction_run_id: elm-street-extract-m5,
  schema_version: v1`.

### Checking the database directly

Everything `query-graph` reports can be checked by hand against
`graph.db` with any SQLite client:

```sql
SELECT * FROM nodes;
SELECT * FROM edges ORDER BY id;
PRAGMA foreign_key_check;  -- should return zero rows
```

If `PRAGMA foreign_key_check` returns any row, an edge's `from_id` or
`to_id` doesn't resolve to a real node — that is exactly the failure
this kit's foreign keys exist to catch, and the verifier should flag it
(see "Symptom" table below).

## Modifying the Example

To adapt this kit to your own sqlite-backed-graph scenario:

1. Delete `graph.db` if one already exists (it's a build artifact of
   `schema.sql`, not something to hand-edit).
2. Replace the `INSERT` statements at the bottom of `schema.sql` with
   your own nodes and edges — keep every edge's `from_id`/`to_id`
   pointing at a node that's actually in the file, and keep all three
   receipt fields populated on every edge.
3. Update `schema.example.json` if your domain needs additional columns —
   but treat that as a deliberate schema change you review, not something
   a query step adds on the fly mid-run.
4. Re-run the skill and confirm `output.json` still names a real edge for
   every verdict, and that the verifier still passes.

## Architecture

- `PATTERN.md` — what this pattern does, its inputs/outputs, and the
  failure mode if you skip it.
- `schema.sql` — the two table definitions plus the Elm Street
  worked-example rows; running it builds `graph.db`.
- `schema.example.json` — the row shape reference for `nodes` and
  `edges`.
- `.claude/skills/query-graph/SKILL.md` — Claude Code load-and-query
  skill.
- `.claude/agents/graph-verifier.md` — Claude Code validation subagent.
- `opencode/opencode.json.example` — OpenCode workflow configuration.
- `opencode/skills/query-graph/SKILL.md` — OpenCode skill covering both
  querying and verification (see its "Mode" sections).

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `sqlite3: command not found` when building `graph.db`. | The `sqlite3` CLI isn't installed. Use the Python one-liner from "Prerequisites" instead — Python's standard library ships a `sqlite3` module, no install needed. |
| `PRAGMA foreign_key_check` returns a row. | An edge's `from_id` or `to_id` names a node id that isn't in the `nodes` table — check `schema.sql`'s `INSERT` statements for a typo'd id. |
| A verdict in `output.json` doesn't name a real edge id, or names one that isn't in `edges`. | The skill reported a verdict without grounding it in an actual row — re-run and confirm step 4 of `SKILL.md` (the availability query) ran before the verdict was written. |
| The verifier reports a mismatch between its independently-derived verdict and `output.json`'s. | This is the verifier doing its job — `graph.db` and `output.json` have drifted apart, most often because `graph.db` was rebuilt or hand-edited after `output.json` was written. Rebuild `graph.db` from `schema.sql` and re-run the skill. |
| Foreign keys don't seem to be enforced even though `schema.sql` declares them. | `PRAGMA foreign_keys = ON;` is per-connection in SQLite, not a database-wide setting — any tool opening `graph.db`, including a plain `sqlite3 graph.db` session, must run that pragma itself before the constraints apply. |

## Next Steps

- Review the pattern specification in `patterns/sqlite-backed-graph.md`
  in the course repo for the general (not scenario-specific) statement of
  this pattern.
- This is a core kit — see `starters/README.md` for how it relates to the
  other six core kits and the sixteen extended kits, including the two
  storage kits (`postgres-backed-graph`, `neo4j-at-scale`) that pick up
  once a graph outgrows what one SQLite file on one machine can serve.
