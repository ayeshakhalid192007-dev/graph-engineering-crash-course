# Solution · Project 7: Settling Two Release Notes Against the Deploy Graph

This works through [Project 7](../07-catch-a-lie-with-a-checker.md)'s two Cascade Media Group deployment claims against `deploy-graph.json`.

## Decomposing each claim

Neither claim is directly queryable as written — "does not restart the billing-service" is prose. Each decomposes into one falsifying edge:

- **Claim A** ("D-207 does not restart billing-service") is false only if `D-207 --restarts--> billing-service` exists.
- **Claim B** ("D-212 does not restart billing-service") is false only if `D-212 --restarts--> billing-service` exists.

## Running the query

Scanning `deploy-graph.json`'s `restarts` list for each edge:

| Deployment | Edge searched for | Found? |
| --- | --- | --- |
| D-207 | `D-207 --restarts--> billing-service` | No. D-207's only two recorded restarts are `rate-limiter` and `retry-config`. |
| D-212 | `D-212 --restarts--> billing-service` | Yes. It's the second of D-212's two recorded restarts, alongside `session-cache`. |

## Verdicts

- **Claim A: CONFIRMED.** No `D-207 --restarts--> billing-service` edge exists in the graph. D-207's two restarts, `rate-limiter` and `retry-config`, are both unrelated to billing.
- **Claim B: REJECTED.** `D-212 --restarts--> billing-service` is a real edge in the graph, extracted directly from D-212's manifest. The release note is wrong regardless of how confidently it reads — the engineer who wrote it evidently didn't realize billing-service was bundled into this deployment.

## Why session-cache doesn't matter here

D-212 restarts two services, `session-cache` and `billing-service`, and it would be easy for a checker to see two hits under `D-212` and treat that as confirmation something's wrong without checking which service the claim was actually about. Claim B is specifically about `billing-service`. The `session-cache` restart is real, and would matter if some other claim asserted D-212 doesn't touch session-cache — but it plays no role in deciding Claim B. A grounded checker matches the decomposed edge exactly, not "this deployment has restarts on record, therefore something's off."

## Checking your own attempt

- Did you decompose each claim into the exact `<deployment> --restarts--> billing-service` edge before looking at the graph at all?
- Is Claim A's confirmation stated as "no such edge exists," not "the note sounds credible"?
- Is Claim B's rejection stated as "this specific edge exists," naming it, not "this deployment looks risky"?
- Did you avoid citing `D-212 --restarts--> session-cache` as the reason Claim B fails, since that edge is real but isn't what the claim was about?
