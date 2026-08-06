# Solution · Project 5: Give Every Edge a Receipt

This works through [Project 5](../05-give-every-edge-a-receipt.md)'s five Hollowmere Apiary hive claims against the cooperative's three-row inspection log.

## Matching claims to log rows

| Claim | Finding | Matching log row | Why it matches |
| --- | --- | --- | --- |
| c1 | Hive-04 queen-failure | insp-101 | Only Hive-04 row before c4's date; checklist v1, which is why c1 has no `confidence` field. |
| c2 | Hive-11 varroa-mite-load-high | insp-114 | Only inspection on record for Hive-11. |
| c3 | Hive-11 brood-pattern-spotty | insp-114 | Same visit as c2 — one inspection, two separate findings written up as two separate claims. |
| c4 | Hive-04 queen-failure, confidence 0.85 | insp-129 | Checklist v2 explains the `confidence` field; same hive, same finding as c1, later date. |
| c5 | Hive-19 healthy | none | No log row mentions Hive-19 at all. |

c1 and c4 report the exact same finding about the exact same hive — that's the giveaway that this is a supersession, not two independent claims about two different things. c4's checklist version (v2) is the only reason it has a field c1 doesn't; nothing about the underlying finding changed between the two visits.

## The retrofitted graph

```json
{
  "claims": [
    {
      "id": "c1",
      "subject": "Hive-04",
      "relation": "has-condition",
      "object": "queen-failure",
      "status": "superseded",
      "supersedes_note": "see supersedes edge to c4",
      "provenance": { "inspection_id": "insp-101", "inspector": "R. Okafor", "date": "2026-04-02", "checklist_version": "v1" }
    },
    {
      "id": "c2",
      "subject": "Hive-11",
      "relation": "has-condition",
      "object": "varroa-mite-load-high",
      "provenance": { "inspection_id": "insp-114", "inspector": "R. Okafor", "date": "2026-04-09", "checklist_version": "v1" }
    },
    {
      "id": "c3",
      "subject": "Hive-11",
      "relation": "has-condition",
      "object": "brood-pattern-spotty",
      "provenance": { "inspection_id": "insp-114", "inspector": "R. Okafor", "date": "2026-04-09", "checklist_version": "v1" }
    },
    {
      "id": "c4",
      "subject": "Hive-04",
      "relation": "has-condition",
      "object": "queen-failure",
      "confidence": 0.85,
      "status": "active",
      "provenance": { "inspection_id": "insp-129", "inspector": "T. Salas", "date": "2026-05-01", "checklist_version": "v2" }
    },
    {
      "id": "c5",
      "subject": "Hive-19",
      "relation": "has-condition",
      "object": "healthy",
      "provenance": { "source": "unknown", "note": "No inspection log row names Hive-19. Likely phoned in by a volunteer rather than logged during a scheduled visit. Would need a matching log entry — or an explicit 'phone report' log type added to the inspection log itself — before this claim could carry a real receipt." }
    }
  ],
  "supersedes_edges": [
    { "from": "c1", "to": "c4" }
  ]
}
```

## Why c1 wasn't edited

Editing `c1` to add `confidence: 0.85` would make it look like a v1 checklist can produce a confidence score, which it can't — that field didn't exist in v1. Anyone reading `c1`'s provenance afterward would see `checklist_version: v1` sitting next to a field that checklist could never have generated, and would have no way to tell whether that mismatch means the record was patched or the checklist metadata is wrong. Leaving `c1` untouched and letting `c4` carry the fuller version keeps both records honest about what each inspection actually produced.

## Why c5 wasn't given a fake receipt

It would have been easy to write `"inspection_id": "insp-101"` on `c5` just to fill the field in — Hive-04 already appears there, so it might look plausible at a glance. But nothing in the log connects Hive-19 to any inspection, and a fabricated ID is worse than an honest gap: it would tell a future reader that a receipt exists when it doesn't, which defeats the entire point of retrofitting provenance in the first place.

## Checking your own attempt

- Does every claim's `provenance` object name a log row that could actually have produced that specific finding — not just any row mentioning the same hive?
- Is `c1` byte-for-byte unchanged in its own fields, with only a status change and an outgoing `supersedes` edge added?
- Does `c5` say "unknown" rather than pointing at a log row that doesn't actually cover it?
- Could you hand `c2` alone to someone else and have them find `insp-114` in the log without being told which row to look for?
