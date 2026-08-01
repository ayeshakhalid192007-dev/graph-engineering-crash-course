# Step 7 · Resolution — Merge Without Losing the Evidence

## Hook

Two documents feed the same fact graph in the same week. The first is a human-written incident retro, and in its prose it refers to *"the payments service"* — never anything more specific, because everyone in the room already knew which service that meant. The second is an automated deploy log, and it only ever names things by their exact deployment identifier: `billing-svc`. An extraction pass, run separately over each document, does exactly what Step 6 asked of it — it produces two `Service` nodes, one named `the payments service` and one named `billing-svc`, both schema-valid, both correctly extracted from what their source actually said. A week later someone queries the graph for "every incident that touched `billing-svc`" and gets one result, when the honest answer is two — the retro's incident is sitting on a node the query never thought to look at, under a name the query never typed.

## Explanation

Nothing in Step 6 catches this, and nothing should have to — the retro really did say "the payments service," the deploy log really did say `billing-svc`, and an extraction pass that stuck faithfully to its source produced two accurate nodes for two different surface forms. The gap between them is a separate problem with its own name: **[resolution](../02-foundations/glossary.md#resolution)**, the step of recognizing that two mentions extracted from two different sources actually name one underlying thing, and collapsing them down to a single node that a query finds no matter which name it was asked about.

The tempting version of resolution is the fast one: pick a canonical name, rewrite both mentions to point at it, and delete whichever node was decided to be the duplicate. That's also the version that quietly destroys evidence. Once `the payments service` node is gone, so is the fact that the incident retro is where that name came from — and if the merge turns out to be wrong later (a second, genuinely different `billing-svc-eu` shows up, say, and the original merge conflated two real services), there's no way back, because the thing being undone no longer exists anywhere to check against.

A **[reversible merge](../02-foundations/glossary.md#reversible-merge)** leaves both original mentions reachable from the resulting canonical node, instead of erasing either one. `the payments service` and `billing-svc` both stay reachable — each one a mention pointing at the same canonical `Service` node — alongside a short record of why they were judged to be the same thing (same deployment, same on-call rotation, same incident channel, whatever the actual reasoning was). Querying for `billing-svc` now correctly surfaces the retro's incident, because the merge didn't discard the connection between the two names — it recorded it. And if that merge is ever found to be wrong, undoing it is a matter of reading the attached reasoning and splitting the node back apart, not reconstructing evidence that was thrown away the moment the merge happened.

## Diagram

```mermaid
flowchart LR
    M1["Mention: 'the payments service'<br/>source: incident retro"] -- "mentioned_as" --> Svc["Service (canonical)<br/>billing-svc"]
    M2["Mention: 'billing-svc'<br/>source: deploy log"] -- "mentioned_as" --> Svc
    Svc -. "merge reasoning:<br/>same deployment target,<br/>same on-call rotation" .-> Rec["Merge record<br/>(reversible)"]
```

Both mentions still exist as their own nodes, each pointing at the merged `Service` node through a `mentioned_as` edge that names its own source. Nothing about folding them together required deleting either one — the merge record hanging off to the side is what makes the decision itself inspectable, and reversible, instead of a name swap nobody can trace back.

## Claude Code vs OpenCode

Both snippets keep both original mentions on record and attach the merge reasoning, rather than picking a winner and quietly discarding the other name.

### Claude Code

```markdown
---
name: service-mention-resolver
description: Merges two Service mentions into one canonical node only if it can name why they're the same thing, keeping both mentions attached.
---

1. Given two candidate mentions of a Service (e.g. "the payments service"
   and "billing-svc") plus the source each one came from, decide whether
   they name the same underlying service. Require a specific reason --
   shared deployment target, shared on-call rotation, explicit
   cross-reference in either document -- not just surface similarity.
2. If they're the same: create (or reuse) one canonical Service node, add
   a `mentioned_as` edge from each original mention to it, and attach the
   reason from step 1 as a merge record on the canonical node. Do not
   delete either mention node.
3. If they're not the same, or the evidence is too thin to be sure, leave
   both nodes unmerged and say so explicitly rather than guessing.
```

### OpenCode

```markdown
---
description: Resolve two Service mentions into one canonical node with a reversible, evidence-backed merge
---

Compare the two given Service mentions and their sources. Merge them only
with a concrete stated reason (shared deployment target, shared
on-call rotation, an explicit cross-reference) -- never on name
similarity alone. On merge: keep both original mention nodes, add a
mentioned_as edge from each to one canonical node, and record the reason
for the merge on that canonical node so it can be checked or reversed
later. If the evidence is too thin, leave both nodes separate and report
that the merge was skipped and why.
```

## Going Deeper

A merge that can't be reversed doesn't just risk being wrong once — it compounds. Every later fact that gets attached to the wrong side of an incorrect merge inherits the mistake, and by the time anyone notices, untangling means figuring out which of the graph's more recent additions belong to which of the two things that never should have been folded together in the first place. Requiring a stated reason for every merge doesn't just make a single merge more defensible; it's what makes that untangling possible at all, because the reason is exactly the thing a reviewer needs to decide whether a given merge should be split back apart.

## Check Yourself

<details>
<summary>Someone proposes a faster resolution rule: if two mention strings are similar enough (edit distance, fuzzy match, whatever), merge them automatically and don't bother keeping a record of why -- the merged node is obviously correct if the strings looked that close. What's the risk in dropping the "why"? Reveal the answer.</summary>

Similarity in spelling isn't evidence of sameness, and dropping the reason removes the only way to check the merge later. Two genuinely different services with similar names ("billing-svc" and "billing-svc-eu") would sail through a pure string-similarity rule, and without a recorded reason attached to the merge, nobody reviewing the graph afterward has anything to evaluate -- there's no stated claim to agree or disagree with, just a merged node that looks confident and might be wrong.

</details>

## Try With AI

Pick two real things from a project you know that get referred to by at least two different names in practice (a service and its repo name, a feature and its internal codename, a person and their username). Ask Claude Code or OpenCode to decide whether the two names refer to the same underlying thing, and require it to state a specific reason before treating them as a match — not just "these sound similar." If it agrees they're the same, have it write out what a reversible merge record would contain: both original mentions, their sources, and the reason. Check that record yourself — is the stated reason actually convincing, or did the agent merge on vibes and backfill a reason afterward?

## When It Goes Wrong

**Symptom:** looking a thing up by one of its known names comes back empty or incomplete, even though facts about that same thing definitely exist in the graph under a different name.

**Cause:** resolution merged the two mentions by picking one name and discarding the other, so the discarded name — and anything a query might search for under it — no longer points anywhere.

**Fix:** never let a merge delete a mention; keep every original mention attached to the canonical node it was folded into, along with the reason it was judged to be the same thing. `labs/step-7-reversible-merge.py` performs exactly this merge and asserts both original mentions are still individually retrievable afterward.

---

Merging fixed who a node refers to. The next page covers what a node needs to carry so a wrong claim can be found and fixed later instead of silently rewritten.
