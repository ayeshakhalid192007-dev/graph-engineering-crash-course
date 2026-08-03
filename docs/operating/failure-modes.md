# Failure Modes

## Hook

Four names, one table. This is the lookup version of the four recurring ways a single automated loop goes wrong on its own — for skimming during an incident, or for checking a proposed loop before it ships, not for learning the ideas for the first time. The fuller version, with a worked scenario behind each name, is Step 12 (Part 5); read that one first if any of the four names below is new to you.

## Explanation

Read the table left to right per row: the name a team should use out loud when diagnosing a stuck loop, what tips a team off that this particular mode is live, the shape of the fix, and where the runnable version of that fix will eventually live.

| Failure mode | Symptom | Fix | Linked pattern |
| --- | --- | --- | --- |
| Metric-gaming | The headline number keeps improving while people downstream of the loop quietly start working around its output. | A counter-metric: a second number, computed by someone other than the loop and never fed back into it. | see `patterns/registry.yaml`, ships Day 3 |
| Blind spot | Every individual unit the loop touches looks fine, yet a failure shows up in how two or more of those units interact. | A wider audit loop that reads several units together in one pass, on its own schedule. | see `patterns/registry.yaml`, ships Day 3 |
| Collision | Two loops each report success, but something downstream broke only on the nights both happened to run close together. | An arbitration edge: a recorded precedence rule stating which loop wins the shared resource. | see `patterns/registry.yaml`, ships Day 3 |
| Drift | The loop's own numbers hold steady or improve while the thing it's judging has visibly moved on. | A periodic edge back to a human, who resamples current reality and refreshes the reference. | see `patterns/registry.yaml`, ships Day 3 |

A fast way to tell these apart under pressure: ask whether the loop, given only what it can see and what it's scored on, could ever have caught this itself. If the answer is no because the score rewards the failure, that's metric-gaming. If the answer is no because the evidence lives outside any single run, that's a blind spot. If the answer is no because another loop is invisible to it, that's a collision. If the answer is no because the yardstick itself moved, that's drift.

## Related

- [`anti-patterns.md`](anti-patterns.md) — the governance anti-patterns section names the missing edge behind each of these four modes.
