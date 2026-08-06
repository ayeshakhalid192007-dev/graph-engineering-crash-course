# Root Cause Report: RCA-3309, With Two Extraction Passes

**Company:** Talus Robotics (fictional, invented for this kit)

Talus Robotics runs a fleet of autonomous warehouse haul-bots. This file
holds one root-cause report and three separate write requests derived
from it — two complete, one missing a receipt field — for the
`attach-receipts` skill to process.

## Source document — RCA-3309 (root cause report)

> **Fault:** Charging dock `charge-dock-3` stopped accepting haul-bots
> for a 40-minute window overnight.
>
> **Finding:** A voltage sensor on `charge-dock-3` began reporting drift
> outside its calibrated range three days before the fault, but nothing
> consumed that signal until the dock's controller finally rejected every
> connecting haul-bot as "unsafe to charge." Two haul-bots on the night
> shift, `haul-bot-12` and `haul-bot-15`, queued at the dock and could not
> charge until a technician recalibrated the sensor at 04:50.
>
> **Conclusion:** `charge-dock-3`'s fault was caused by the uncorrected
> voltage-sensor drift.

## Write request A — extracted under schema v1

- Run: `rca3309-extract-a`
- Schema version in effect: `v1` (no `impact_scope` field defined yet)
- Candidate edge:
  - subject: `charge-dock-3`
  - predicate: `caused-by`
  - object: `voltage-sensor-drift`
  - source_doc: `RCA-3309`
  - extraction_run_id: `rca3309-extract-a`
  - schema_version: `v1`

## Write request B — re-extracted under schema v2

Schema `v2` shipped after write request A, adding a required
`impact_scope` field to every `caused-by` edge. `RCA-3309` gets
re-extracted under the new schema, several weeks later, once `v2` is
live.

- Run: `rca3309-extract-b`
- Schema version in effect: `v2` (requires `impact_scope` on `caused-by`
  edges)
- Candidate edge:
  - subject: `charge-dock-3`
  - predicate: `caused-by`
  - object: `voltage-sensor-drift`
  - impact_scope: `haul-bot-12, haul-bot-15 delayed charging ~40 min`
  - source_doc: `RCA-3309`
  - extraction_run_id: `rca3309-extract-b`
  - schema_version: `v2`

## Write request C — incomplete receipt

A third run also re-extracted `RCA-3309` under schema `v2`, around the
same time as write request B. Its extraction pipeline hit a logging bug
that dropped the run's own id before the candidate edge reached the write
step — every other field, including `impact_scope`, came through fine.

- Run: (missing — this is the point of including this request)
- Schema version in effect: `v2`
- Candidate edge:
  - subject: `charge-dock-3`
  - predicate: `caused-by`
  - object: `voltage-sensor-drift`
  - impact_scope: `haul-bot-12, haul-bot-15 delayed charging ~40 min`
  - source_doc: `RCA-3309`
  - extraction_run_id: *(missing)*
  - schema_version: `v2`

This kit's schema requires `extraction_run_id` on every edge regardless of
which schema version produced it — the point of including write request C
is to see the skill refuse it outright rather than write it with a blank
or guessed run id.

---

*This is an invented scenario written for the `receipt-per-edge` starter
kit. Talus Robotics, `RCA-3309`, and all identifiers above are fictional.*
