# Solution · Project 3: Extract Your First Ten Facts

This works through [Project 3](../03-extract-your-first-ten-facts.md)'s Fernbank changelog against the fixed schema — three entity types (`Release`, `Feature`, `Issue`), three relationship types (`introduces`, `fixes`, `deprecates`).

## The ten schema-valid items

| # | Subject | Relation | Object | Object type |
| - | --- | --- | --- | --- |
| 1 | v2.4.0 | introduces | bulk tag rename | Feature |
| 2 | v2.4.0 | introduces | pin-to-top shortcut | Feature |
| 3 | v2.4.0 | introduces | dark mode | Feature |
| 4 | v2.4.0 | fixes | mobile auto-lock data loss | Issue |
| 5 | v2.4.0 | deprecates | Notebooks sidebar view | Feature |
| 6 | v2.3.1 | fixes | search missing recent edits | Issue |
| 7 | v2.3.1 | fixes | stale collaborator list | Issue |
| 8 | v2.3.0 | introduces | offline mode | Feature |
| 9 | v2.3.0 | introduces | weekly digest email | Feature |
| 10 | v2.3.0 | fixes | PDF export cutoff | Issue |

Every subject is a `Release`; every item's relation is one of the three the schema allows; every object is either a `Feature` (for `introduces` and `deprecates`) or an `Issue` (for `fixes`). Ten lines in, ten lines matched.

## The rejected line

Look at the v2.3.0 bullet about the free-tier plan cap, moving the note ceiling from 200 up to 500 — that's the single line nothing in the schema can hold.

This line describes something that genuinely happened in that release, and it's phrased the same way as every other bullet in the document. It still doesn't fit: the schema has no `changes` relationship type, and the object — a numeric plan limit — isn't a `Feature` or an `Issue` either. Forcing it into `introduces` (nothing was newly added; the limit already existed at a lower number) or `fixes` (nothing was broken) would misstate what the item is. The honest move is to leave it out and flag it, not stretch an existing relationship type to cover it.

If this kind of item showed up often — plan limits, pricing, quotas — that would be a case for Step 6's "document that genuinely needs a new type" edge case: a deliberate, reviewed schema change adding a `Policy` entity type and a `changes` relationship, decided on its own, not smuggled in to make one line's extraction succeed.

## The resulting graph

**Nodes:**
- `Release`: v2.4.0, v2.3.1, v2.3.0
- `Feature`: bulk tag rename, pin-to-top shortcut, dark mode, Notebooks sidebar view, offline mode, weekly digest email
- `Issue`: mobile auto-lock data loss, search missing recent edits, stale collaborator list, PDF export cutoff

**Edges:** exactly the ten rows in the table above, each directed from its `Release` node to its `Feature` or `Issue` node.

## Checking your own attempt

- Did you write the schema down before reading the changelog as data, or did you adjust it after seeing which lines were awkward to fit?
- Do you have exactly ten items, none of them the free-tier line?
- Can you point to the specific reason the free-tier line fails — missing relationship type, missing entity type, or both — rather than a general sense that it "doesn't belong"?
- If you ran an agent's extraction independently, did it land on the same ten items and flag the same rejected line, or did it invent a fourth relationship type to absorb the free-tier change?
