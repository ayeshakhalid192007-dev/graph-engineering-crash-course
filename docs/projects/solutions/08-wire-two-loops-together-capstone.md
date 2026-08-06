# Solution · Project 8: Wire Two Loops Together (Capstone)

This works through [Project 8](../08-wire-two-loops-together-capstone.md)'s Emberlynn Transit Co-op collision between `forecast-loop` and `gps-ground-loop` on Route 12.

## The governance graph

```json
{
  "loops": ["forecast-loop", "gps-ground-loop"],
  "edges": [
    { "from": "forecast-loop", "relation": "feeds", "to": "gps-ground-loop" },
    { "from": "gps-ground-loop", "relation": "checks", "to": "forecast-loop" },
    {
      "from": "gps-ground-loop",
      "relation": "can-overrule",
      "to": "forecast-loop",
      "scope": "predicted-arrival / actual-arrival field on a shared stop record",
      "reason": "gps-ground-loop's writes are anchored to a real, individually verifiable GPS geofence crossing; forecast-loop's writes are unanchored periodic model output that can be stale the moment it lands. First applied to the Route 12 / Elm & 5th collision on this Tuesday."
    }
  ],
  "frozen_nodes": [
    {
      "id": "on_time_window_minutes",
      "value": 2,
      "frozen": true,
      "note": "Neither forecast-loop nor gps-ground-loop may modify this value. Changing it is a human decision, made on the record, never a side effect of either loop trying to make a discrepancy disappear."
    }
  ]
}
```

`forecast-loop feeds gps-ground-loop` because the checker loop's job is to verify predictions against reality, which means the forecaster's output is the thing being checked. `gps-ground-loop checks forecast-loop` records that relationship explicitly, the same way Step 11's review loop checks its drafting loop. Only one `can-overrule` edge exists, and it runs one direction. The reverse edge — `forecast-loop` holding any authority over `gps-ground-loop` — is simply absent, so there's no ring to resolve.

## Applying the rule to the collision

| Loop | Value proposed | Timestamp | Anchored? |
| --- | --- | --- | --- |
| forecast-loop | `predicted-arrival = 14:07` | 14:02:00 | No — output of a scheduled model run, with no single real-world event standing behind it. |
| gps-ground-loop | `actual-arrival = 14:01:50` | 14:02:03 | Yes — tied to a real GPS geofence crossing that actually happened. |

The `can-overrule` edge's rule applies directly: an anchored write on the same field beats an unanchored one, regardless of which write landed second. `gps-ground-loop`'s three-second-later timestamp isn't why it wins — if the order had been reversed, with `forecast-loop` writing after `gps-ground-loop`, the anchored value would still win, because the rule is about anchoring, not about recency.

**Collision output:**

```json
{
  "stop": "Elm & 5th",
  "route": "Route 12",
  "collision": true,
  "accepted": { "loop": "gps-ground-loop", "value": "14:01:50", "reason": "anchored to a real GPS geofence crossing" },
  "rejected": { "loop": "forecast-loop", "value": "14:07", "reason": "unanchored periodic model estimate, preempted by gps-ground-loop can-overrule forecast-loop on this field" },
  "rule_applied": "event-anchored write beats unanchored periodic estimate on the same field"
}
```

`14:07` never disappears from the record — it's rejected, not deleted, with the specific reason it lost. A dashboard that only showed the accepted value would look identical to one that silently dropped the losing write; keeping both, labeled, is what makes the arbitration auditable later.

## Why the frozen node matters here

`on_time_window_minutes` is set to 2. The gap between the two proposed values — model says 14:07, GPS says 14:01:50, a difference of over five minutes — is well outside that window, which is part of why this collision is worth resolving at all rather than treated as noise.

Suppose `gps-ground-loop` could stretch `on_time_window_minutes` any time its anchored reading came in far off the forecast. It would be able to quietly redefine a five-minute miss as "still on time" by pushing the window up to six minutes, and the collision would stop being reported as a collision at all — not because the forecast got more accurate, but because the yardstick moved to match whatever discrepancy showed up. Freezing the value means a genuinely wide forecast miss stays visible as a genuinely wide forecast miss, and any real change to what counts as "on time" has to happen as a deliberate, logged decision instead of a side effect of one bad prediction.

## Confirming no cycle

The only `can-overrule` edge is `gps-ground-loop → forecast-loop`. Nothing in `governance.json` adds the reverse edge, so there's no ring: asking "who wins a collision between these two loops" always has exactly one answer, and it doesn't depend on which loop happens to be asked first.

## Checking your own attempt

- Does your `can-overrule` edge name a specific field it governs, rather than claiming blanket authority over everything `forecast-loop` does?
- Does your collision output show both the accepted and rejected values, with the rule named, rather than an averaged or blended result?
- Is `on_time_window_minutes` marked frozen, with a note explaining that neither loop may rewrite it?
- Can you state, from your own governance graph alone, why `gps-ground-loop` would still have won this collision even if `forecast-loop`'s write had landed after it?
