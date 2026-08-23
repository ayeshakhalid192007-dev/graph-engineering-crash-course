# Project 5 · Give Every Edge a Receipt

**Difficulty:** Intermediate
**Time:** 30–45 minutes
**Concepts:** provenance, source records, schema-version tracking
**Maps to:** Step 8, Part 3, which covers attaching a provenance record to every claim instead of editing an old claim in place. That link is kept current in the [docs guide](../README.md)'s roadmap, not repeated here.

> **Throwaway repo, small data first.** Five inspection claims and a three-row log to cross-reference them against — everything fits on one screen.

## The scenario

Hollowmere Apiary Collective, a small volunteer-run beekeeping cooperative, has been logging hive-condition claims into a shared file for a season. Nobody attached a source to any of them — the claims exist, but nothing says which inspection produced which finding, or under which version of the inspection checklist. A new volunteer coordinator wants to trust the file enough to schedule follow-up visits from it, and can't, because there's no way to tell a carefully logged finding from a guess someone typed in from memory.

Your job is to retrofit a provenance record onto each claim by cross-referencing it against the cooperative's separate inspection log — without inventing a source for the one claim the log doesn't actually back up.

## Starting material

The claims, as they currently sit in `hive-claims.json`, with no provenance at all:

```json
{
  "claims": [
    { "id": "c1", "subject": "Hive-04", "relation": "has-condition", "object": "queen-failure" },
    { "id": "c2", "subject": "Hive-11", "relation": "has-condition", "object": "varroa-mite-load-high" },
    { "id": "c3", "subject": "Hive-11", "relation": "has-condition", "object": "brood-pattern-spotty" },
    { "id": "c4", "subject": "Hive-04", "relation": "has-condition", "object": "queen-failure", "confidence": 0.85 },
    { "id": "c5", "subject": "Hive-19", "relation": "has-condition", "object": "healthy" }
  ]
}
```text

The cooperative's separate inspection log, kept by hand and never linked to the claims file:

| Inspection ID | Inspector | Hive | Date | Checklist version |
| --- | --- | --- | --- | --- |
| insp-101 | R. Okafor | Hive-04 | 2026-04-02 | v1 (no confidence field) |
| insp-114 | R. Okafor | Hive-11 | 2026-04-09 | v1 (no confidence field) |
| insp-129 | T. Salas | Hive-04 | 2026-05-01 | v2 (adds confidence field) |

## Your task

1. In a throwaway repo, copy `hive-claims.json` above and add a `provenance` object to every claim you can genuinely back with an inspection log row — naming the inspection ID, the inspector, and the checklist version that was active.
2. Match claims to log rows by what each row could actually have produced, not by hive number alone. `insp-114` covers two separate findings on the same hive during one visit — both `c2` and `c3` point back to it.
3. `c1` and `c4` are the same finding — `Hive-04 has-condition queen-failure` — recorded twice, once under checklist v1 (no confidence field) and once under v2 (with one). Don't edit `c1` to add the confidence field. Instead, mark `c4` as the fuller re-recording of the same finding: give `c1` a `superseded` status and add a `supersedes` edge from `c1` to `c4`, leaving `c1`'s own fields and provenance exactly as they were.
4. `c5` has no matching row anywhere in the inspection log. Do not invent an inspection ID for it. Instead, add a `provenance` field that honestly says the source is unknown. Then note, in a sentence, the specific evidence that would have to surface before `c5` deserves a real receipt.
5. Check your result: for each claim with a real provenance record, could you hand just that one claim to someone else and have them find the exact log row it came from, with nothing else to go on?

## Done when

- Every claim that can be traced to an inspection log row has a `provenance` object naming that row's inspection ID, inspector, and checklist version.
- `c1` was never edited to add a confidence field. `c4` exists as its own claim with its own `v2` provenance record, and a `supersedes` edge points from `c1` to `c4`.
- `c5` carries an explicit "source unknown" provenance marker instead of a fabricated inspection ID, and you can state in one sentence what evidence would be needed to give it a real one.
- `c2` and `c3` both name `insp-114` as their source, showing that one inspection can produce more than one claim without needing two separate log rows invented to justify it.

## Reference solution

[`solutions/05-give-every-edge-a-receipt.md`](solutions/05-give-every-edge-a-receipt.md) — the fully retrofitted `hive-claims.json`, with every provenance record matched to its log row and the `c1`→`c4` supersession worked through in full.
