# Project 7 · Catch a Lie with a Checker

**Difficulty:** Advanced
**Time:** 45–60 minutes
**Concepts:** grounding, checkers that reject an ungrounded claim
**Maps to:** Step 10, Part 4, which settles a claim by querying the graph for one specific edge rather than judging how confidently the claim reads. Check the [docs guide](../README.md)'s roadmap for that page's current link.

> **Throwaway repo, small data first.** Two deployments, four `restarts` edges between them — small enough to check the checker's answer by eye once it reports.

## The scenario

Cascade Media Group ships two deployments in the same release window. Each deployment's manifest gets run through an extraction pass that records, as `restarts` edges, exactly which services that deployment brings down and back up — not a guess about what the deployment "probably" touches, a fact pulled straight from the manifest itself.

An on-call engineer writes up a release note for each deployment claiming which services were left untouched, to reassure a downstream team that nothing they depend on needs re-checking. One of the two release notes is correct. The other one is wrong — a service restart got bundled into the deployment for an unrelated reason, and the engineer who wrote the note didn't know it was in there. Your job is to build a checker that catches the wrong one by querying the deploy graph, not by reading either note and deciding which one sounds more careful.

## Starting material

The deploy graph, built from the two deployments' manifests, `deploy-graph.json`:

```json
{
  "restarts": [
    { "deployment": "D-207", "service": "rate-limiter" },
    { "deployment": "D-207", "service": "retry-config" },
    { "deployment": "D-212", "service": "session-cache" },
    { "deployment": "D-212", "service": "billing-service" }
  ]
}
```text

The two release-note claims to check:

- **Claim A:** "Deployment D-207 does not restart the billing-service."
- **Claim B:** "Deployment D-212 does not restart the billing-service."

## Your task

1. Set up a throwaway repo, drop `deploy-graph.json` into it, and copy both release-note claims out as plain text alongside it.
2. For each claim, decompose it into the single edge that would have to exist in `deploy-graph.json` for the claim to be false: `<deployment> --restarts--> billing-service`.
3. Query the graph for exactly that edge — do not read anything else about either deployment, and do not weigh how plausible either claim sounds.
4. Report each claim as CONFIRMED (the falsifying edge is absent) or REJECTED (the falsifying edge is present), naming the specific edge your decision rested on either way.
5. For the rejected claim, state which of `D-212`'s two restarts on record the checker actually found, since `deploy-graph.json` lists more than one service per deployment and the checker has to find the right one, not just notice the deployment has entries.

## Done when

- Claim A is reported CONFIRMED, citing the absence of a `D-207 --restarts--> billing-service` edge.
- Claim B is reported REJECTED, citing the presence of the actual `D-212 --restarts--> billing-service` edge.
- Neither verdict mentions the wording of the release notes, how confident they sound, or anything other than the specific edge checked.
- Your write-up states plainly that `D-212 --restarts--> session-cache` exists too, but that it isn't what settles Claim B — `billing-service` is the specific edge the claim was about.

## Reference solution

[`solutions/07-catch-a-lie-with-a-checker.md`](solutions/07-catch-a-lie-with-a-checker.md) — both claims worked through against the deploy graph, with the exact query run for each and why Claim B fails while Claim A holds.
