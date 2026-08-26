# Project 8 · Wire Two Loops Together (Capstone)

**Difficulty:** Capstone
**Time:** 90–120 minutes
**Concepts:** governance graph, arbitration, anchors, frozen nodes
**Maps to:** Steps 11–13, Part 5: wiring loops together with authority edges, the failure modes a lone loop falls into, and anchors plus frozen nodes. The [docs guide](../README.md) carries all three links in its roadmap; they aren't duplicated here.

> **Throwaway repo, small data first.** Two loops, one shared stop, one collision to resolve — the whole exercise fits in a couple of small files.

## The scenario

Emberlynn Transit Co-op runs two automated loops that both write to a shared route-status graph for its bus network.

`forecast-loop` runs every few minutes and writes a `predicted-arrival` value for each upcoming stop, computed from a traffic model — an estimate, not a measurement of anything that actually happened yet.

`gps-ground-loop` watches each bus's live GPS feed. When a bus's GPS position crosses a stop's geofence, it writes an `actual-arrival` record anchored to that real crossing event — a fact the loop didn't compute, just observed.

The two loops were built by different people, months apart, and neither was written with the other in mind. On a Tuesday, both loops write to the record for the same stop on Route 12 within three seconds of each other: `forecast-loop` recomputes a new predicted time from its model at 14:02:00, and `gps-ground-loop` logs a real GPS crossing at 14:02:03 showing the bus already passed that stop — earlier than the fresh prediction says it will. Two proposed values now sit on one record, and nothing in either loop's code says which one the dashboard should trust.

Your job is to wire the two loops into a governance graph with one real authority edge that settles this — modeled on the same rule the `arbitration-edge` kit uses (event-anchored beats unanchored), applied here to a transit system instead of a warehouse — and to add one frozen node so a loop can't quietly widen its own definition of "on time" to make a discrepancy disappear.

## Starting material

The route-status record both loops write to, before either write lands, `route-12-status.json`:

```json
{
  "stop": "Elm & 5th",
  "route": "Route 12",
  "on_time_window_minutes": 2,
  "records": []
}
```text

The two competing writes:

- `forecast-loop`, 14:02:00: proposes `predicted-arrival = 14:07`, unanchored — a periodic recomputation from the traffic model, not tied to any specific observed event.
- `gps-ground-loop`, 14:02:03: proposes `actual-arrival = 14:01:50`, anchored to a real GPS geofence crossing.

## Your task

1. In a throwaway repo, build a small governance graph, `governance.json`, with two loop nodes (`forecast-loop`, `gps-ground-loop`) and these edges: `forecast-loop feeds gps-ground-loop` (the checker loop verifies against the forecaster's output), and `gps-ground-loop checks forecast-loop`.
2. Add the one authority edge this project is about: `gps-ground-loop can-overrule forecast-loop`, scoped specifically to the `predicted-arrival`/`actual-arrival` field on a shared stop record — not blanket authority over everything the forecast loop does.
3. State the rule behind that edge in your own words, applying the same underlying logic the `arbitration-edge` kit uses for its inventory collision: a write anchored to a real, individually verifiable event outranks an unanchored periodic estimate on the same field, because the estimate could already be stale by the time it lands.
4. Resolve the Route 12 collision above using that rule: record which value is accepted, which is rejected, and why — the rejected value must still appear in your output, not be silently dropped.
5. Add `on_time_window_minutes: 2` to `governance.json` as a frozen node, with a note stating neither loop may modify it. Explain in one sentence what would happen to this collision's reporting if `gps-ground-loop` were allowed to widen that window whenever its own reading disagreed with the forecast.
6. Confirm your `can-overrule` edge doesn't form a cycle — check that no edge anywhere points authority back from `forecast-loop` to `gps-ground-loop`.

## Done when

- `governance.json` has both loop nodes, a `feeds` edge, a `checks` edge, and exactly one `can-overrule` edge, scoped to the specific field it governs rather than stated as blanket authority.
- The Route 12 collision output names both proposed values (`14:07` unanchored and `14:01:50` anchored), states which one wins, and states the rule by name — never an average of the two, never "most recent write wins."
- The rejected value (`14:07`) is still visible in your output, with the reason it lost.
- `on_time_window_minutes` is marked frozen, and your one-sentence answer explains specifically what discrepancy a loop could hide by being allowed to widen it.
- No authority cycle exists between the two loops.

## Reference solution

[`solutions/08-wire-two-loops-together-capstone.md`](solutions/08-wire-two-loops-together-capstone.md) — the full governance graph, the resolved Route 12 collision, and the frozen-node reasoning worked through in detail.
