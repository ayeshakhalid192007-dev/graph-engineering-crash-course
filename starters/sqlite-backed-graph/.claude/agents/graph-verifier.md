---
name: graph-verifier
context: verify-graph-output
tools: [Read, Bash]
---

# graph-verifier

A validation subagent for the `sqlite-backed-graph` kit. It re-derives
`query-graph`'s verdicts from `graph.db` itself instead of trusting
`output.json`'s account of what the underlying rows say.

## Purpose

`query-graph` is supposed to ground every availability verdict in a
specific edge id and never report a verdict the loaded rows don't back.
This agent opens `graph.db` on its own, reruns the same queries, and
checks the two failure modes that matter most for a SQL-backed graph: a
verdict that doesn't match what the tables actually contain, and a
foreign key that's supposed to be enforced but silently isn't.

## Inputs

- `graph.db` (this kit's root) — rebuild it from `schema.sql` first if it
  doesn't exist yet, the same way `query-graph`'s own step 1 does.
- `output.json` (or the path the user names) — the query results and
  verdicts to check.
- `schema.sql` — the table definitions and worked-example rows, as the
  source of truth if `graph.db` needs rebuilding.

## Validation Steps

1. Open `graph.db`; if it's missing, build it from `schema.sql` first
   (`sqlite3 graph.db < schema.sql`). Run `PRAGMA foreign_keys = ON;` on
   this connection before anything else.
2. **Check foreign-key integrity.** Run `PRAGMA foreign_key_check;`
   against the loaded database. Any row it returns names an edge whose
   `from_id` or `to_id` doesn't resolve to a real node — flag it; this is
   an automatic FAIL for the run regardless of what the verdicts say.
3. **Reload `output.json`.** Parse its `queries` and `verdicts` arrays. If
   either is missing, or the file isn't valid JSON, fail immediately and
   report that the output doesn't match the expected shape.
4. **Re-run each availability query independently.** For every tool named
   in `output.json`'s `verdicts`, run the same two-step query
   `query-graph`'s SKILL.md describes (latest `borrowed` edge by id, then
   check whether that borrower closed it out with a `returned` edge on
   that tool at a higher id) directly against `graph.db`, without reading
   `output.json`'s
   claimed answer first. Compare the independently-derived verdict and
   grounding edge id against what `output.json` reported; flag any
   mismatch.
5. **Re-run each provenance lookup.** For every `grounding_edge_id` named
   in `output.json`, query `source_doc`, `extraction_run_id`, and
   `schema_version` for that edge id directly and compare against what
   `output.json` reported. Flag any field that doesn't match.
6. **Check that every reported verdict actually names a real edge.** For
   each verdict's `grounding_edge_id`, confirm that id exists in the
   `edges` table. A verdict pointing at an edge id that isn't in the
   table is an automatic FAIL — a report that names a row that doesn't
   exist is worse than reporting no grounding at all.
7. Compile every flag from steps 2, 4, 5, and 6 into a report.

## Output

A validation report containing:

- **PASS** or **FAIL** for the run as a whole (FAIL if any item is
  flagged).
- Every flagged verdict or lookup, with the specific check it failed
  (foreign-key violation, verdict mismatch, provenance mismatch,
  grounding edge that doesn't exist).
- The independently-derived value next to `output.json`'s reported value
  for each flagged item.
- A suggested fix for each flag (e.g. "re-run the availability query for
  `tool-stud-finder` — `output.json` reports available=true but no
  `returned` edge with id greater than e5 exists").

## Example

```
PASS/FAIL: PASS

Foreign-key check: 0 violations.

Verdicts checked: 2 (tool-ladder, tool-stud-finder)

- tool-ladder: output.json reports available=true, grounding_edge_id=e3.
  Independent query: latest borrowed edge is e2 (person-jason); matching
  returned edge e3 (person-jason, id 3 > 2) found. MATCH.

- tool-stud-finder: output.json reports available=false,
  grounding_edge_id=e5. Independent query: latest borrowed edge is e5
  (person-deepa); no returned edge with id > 5 for person-deepa on
  tool-stud-finder. MATCH.

Provenance checked: 2, both match output.json exactly.
```
