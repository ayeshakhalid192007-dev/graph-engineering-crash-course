# Solution · Project 6: Scoping the Helpdesk Graph to One Ticket

This works through [Project 6](../06-feed-a-worker-a-subgraph.md)'s Fernglade Systems helpdesk graph, scoped to ticket `T-501`.

## Building the subgraph

Starting from `T-501` as the target:

1. **Direct routing neighbor:** `routed_to` says `T-501 → Identity-Access`. That edge, and the `Identity-Access` node, come in.
2. **One hop further along the routing path:** `escalates_to` says `Identity-Access → App-Platform`. That's the team the ticket would move to next if Identity-Access can't close it — relevant to an engineer deciding whether to loop that team in early. `App-Platform` comes in.
3. **Every claim attached to `T-501`:** both `cl1` and `cl2` are pulled, in full, along with the fact that they disagree. Neither gets dropped in favor of the other.
4. **Everything belonging only to `T-502` or `T-503`:** left out entirely. `Endpoint-Hardware`, `Network-Ops`, and `cl3` never enter the subgraph, because nothing about `T-501`'s own edges reaches them.

## The task-scoped subgraph

```json
{
  "target_ticket": "T-501",
  "nodes": ["T-501", "Identity-Access", "App-Platform"],
  "edges": [
    { "from": "T-501", "relation": "routed_to", "to": "Identity-Access" },
    { "from": "Identity-Access", "relation": "escalates_to", "to": "App-Platform" }
  ],
  "claims": [
    { "id": "cl1", "source": "triage-bot", "diagnosis": "expired SSO certificate on the identity provider" },
    { "id": "cl2", "source": "agent-note (D. Ibrahim)", "diagnosis": "VPN client misconfigured after last week's rollout, unrelated to SSO" }
  ],
  "note": "cl1 and cl2 disagree about root cause and, implicitly, about which team should own the fix -- cl1 points at Identity-Access (where the ticket already sits), cl2 points at Network-Ops (a team not currently routed to this ticket at all). Neither claim was dropped or preferred."
}
```text

**Node count:** the full graph has 7 distinct entity nodes — `T-501`, `T-502`, `T-503`, `Identity-Access`, `Network-Ops`, `Endpoint-Hardware`, `App-Platform`. The subgraph keeps 3 of them: `T-501`, `Identity-Access`, `App-Platform`. Dropped: `T-502`, `T-503`, `Network-Ops`, `Endpoint-Hardware` — plus `cl3`, the one claim that belongs to a different ticket entirely.

## Why Network-Ops stays out

`cl2`'s diagnosis text names Network-Ops as the team it thinks is actually responsible — but naming a team inside a claim's free-text diagnosis isn't the same as an edge connecting `T-501` to `Network-Ops` in the graph. The subgraph is built by walking real edges (`routed_to`, `escalates_to`, `claims`), not by parsing what a diagnosis happens to mention. `cl2` itself travels into the subgraph intact, which is enough — the engineer reading it sees Network-Ops named right there in the claim text and can decide to pull that team in, but the subgraph-building step doesn't need to guess at which text mentions deserve to become graph nodes. Doing that would blur the line between "this is an edge the graph actually has" and "this is a word that appeared in a diagnosis," and the whole reason `cl1` and `cl2` were kept as separate claims rather than merged into one summary is to preserve exactly that distinction.

## The sentence that matters

What this subgraph tells the engineer, and the full graph would have buried: **two independent sources disagree about which team owns `T-501`'s fix — the triage bot says Identity-Access via an expired certificate, a support agent says the actual cause is upstream in Network-Ops and unrelated to identity at all.** Scrolling the full 8-node, 3-ticket graph, that contradiction is one claim among three, sitting next to `T-502` and `T-503`'s unrelated hardware and printer issues, with nothing marking it as the thing that actually needs a decision before work starts.

## Checking your own attempt

- Does your subgraph contain exactly `T-501`, `Identity-Access`, and `App-Platform` — no team or ticket belonging only to `T-502` or `T-503`?
- Are both `cl1` and `cl2` present, with the disagreement between them stated rather than resolved?
- Did you correctly leave `Network-Ops` out, even though `cl2`'s text names it, because no edge in the graph connects it to `T-501`?
- Is your reported node count 3 kept out of 7 total, with the four dropped nodes named specifically?
