# Project 6 · Feed a Worker a Subgraph, Not the Graph

**Difficulty:** Intermediate
**Time:** 45–60 minutes
**Concepts:** subgraphs, bounded context, task-scoped retrieval
**Maps to:** Step 9, Part 4, which builds the case for handing a worker a task-scoped slice of a graph instead of everything in it. Find the exact link via the [docs guide](../README.md)'s own roadmap section.

> **Throwaway repo, small data first.** A dozen nodes, three tickets, four teams — small enough that you can tell by eye whether your subgraph left something important out.

## The scenario

Fernglade Systems runs an internal IT helpdesk with an automated routing graph: every ticket gets a `routed-to` edge pointing at the team currently handling it, and teams have `escalates-to` edges recording which team a ticket goes to next if the first team can't resolve it. Two different sources have also each attached a diagnosis claim to one specific ticket, and the two claims disagree about what's actually wrong.

A support engineer picks up that one ticket and asks for context before touching anything. Handing them the whole company-wide routing graph — every team's ticket queue, every escalation path, two other tickets that have nothing to do with this one — would bury the one thing that actually matters: the graph doesn't have a settled answer about what's wrong, and the engineer needs to know that before they start fixing the wrong thing.

## Starting material

The full routing graph, `helpdesk-graph.json`:

```json
{
  "tickets": [
    { "id": "T-501", "summary": "Users in the Denver office can't reach internal apps over VPN" },
    { "id": "T-502", "summary": "Laptop won't power on after firmware update" },
    { "id": "T-503", "summary": "Printer on 4th floor offline" }
  ],
  "teams": ["Identity-Access", "Network-Ops", "Endpoint-Hardware", "App-Platform"],
  "routed_to": [
    { "ticket": "T-501", "team": "Identity-Access" },
    { "ticket": "T-502", "team": "Endpoint-Hardware" },
    { "ticket": "T-503", "team": "Network-Ops" }
  ],
  "escalates_to": [
    { "from": "Identity-Access", "to": "App-Platform" },
    { "from": "Network-Ops", "to": "App-Platform" },
    { "from": "Endpoint-Hardware", "to": "App-Platform" }
  ],
  "claims": [
    { "id": "cl1", "ticket": "T-501", "source": "triage-bot", "diagnosis": "expired SSO certificate on the identity provider" },
    { "id": "cl2", "ticket": "T-501", "source": "agent-note (D. Ibrahim)", "diagnosis": "VPN client misconfigured after last week's rollout, unrelated to SSO" },
    { "id": "cl3", "ticket": "T-502", "source": "triage-bot", "diagnosis": "firmware update corrupted the boot partition" }
  ]
}
```

`cl1` implicates Identity-Access, the team T-501 is currently routed to. `cl2` implicates Network-Ops instead, a team T-501 isn't routed to at all — and the two claims were never reconciled.

## Your task

1. In a throwaway repo, save the graph above and identify the task: an engineer has been assigned `T-501` and needs exactly the context relevant to working it.
2. Build a task-scoped subgraph for `T-501` containing: the ticket itself, the team it's currently `routed_to`, that team's `escalates_to` target, and every claim attached to `T-501` — both of them, contradiction intact. Do not pick the more plausible-sounding claim and drop the other.
3. Exclude everything that belongs to `T-502` or `T-503` — their tickets, and any team relationship that only matters because of them. `Endpoint-Hardware` and its escalation edge should not appear in `T-501`'s subgraph just because it exists somewhere in the full graph.
4. Write one sentence stating what the subgraph is telling the engineer that the full graph, read all at once, would have buried: that two sources disagree about which team actually owns the fix.
5. Count the nodes you kept, count the nodes in the original file, and write both numbers down. A scope reduction you haven't measured is a scope reduction you're only guessing at.

## Done when

- The subgraph contains `T-501`, `Identity-Access`, `App-Platform` (the escalation target), and both `cl1` and `cl2` — nothing dropped, nothing silently resolved to one "winning" diagnosis.
- `T-502`, `T-503`, `Endpoint-Hardware`, `Network-Ops`, and `cl3` do not appear anywhere in the subgraph, even though `Network-Ops` is the team `cl2`'s diagnosis actually points at.
- Your one-sentence note names the disagreement explicitly — not just "there's more context available," but which two teams are implicated and by which source.
- Your reported node count is smaller than the full graph's, with the specific nodes kept and dropped both stated.

## Reference solution

[`solutions/06-feed-a-worker-a-subgraph.md`](solutions/06-feed-a-worker-a-subgraph.md) — the full task-scoped subgraph for `T-501`, with the node-count comparison and an explanation of why `Network-Ops` stays out despite being named in one of the claims.
