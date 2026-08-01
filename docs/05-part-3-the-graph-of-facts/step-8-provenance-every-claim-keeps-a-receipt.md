# Step 8 · Provenance — Every Claim Carries a Receipt

## Hook

`PM-2117`'s cause gets extracted under the schema from Step 6: entity types `Service`, `Incident`, `Cause`, relationship types `caused-by` and `affected` — nothing more. The resulting claim, `checkout-api caused-by expired internal CA cert`, is accurate and ships into the fact graph. Months later, two more postmortems disagree about whether a cert-expiry incident was actually preventable, and someone realizes the graph has no way to settle it: nothing on any `caused-by` claim says how confident the extraction was, so there's no way to weigh one claim against another. The schema gets a second version — `v2` — that adds a required `confidence` field to every `caused-by` claim. Someone re-runs extraction on `PM-2117` under the new schema and gets a `confidence` score this time. The easy move is to open the old claim and add the missing field to it. The move that doesn't quietly erase history is different.

## Explanation

Editing the old claim in place feels harmless — it's "the same fact," just more complete now. But the moment that edit lands, the graph loses something real: there is no longer any record that a `caused-by` claim without a `confidence` field ever existed, which means there's no way to tell, for any other `v1`-era claim still sitting in the graph, whether it's missing `confidence` because nobody re-extracted it yet or because it was silently backfilled with a guess. The claim's own history — what schema was live when it was made, what changed since — disappears the instant the record itself is rewritten.

**[Provenance](../02-foundations/glossary.md#provenance)** is what prevents that disappearance. Every claim in the fact graph carries a provenance record: which source document it came from, which extraction run produced it, and which version of the schema was active when that run happened. `PM-2117`'s original claim carries a provenance record naming schema `v1`; nothing about that record is optional, because it's the only thing that later lets anyone ask "was this claim made under the old rules or the new ones" and get a real answer instead of a guess.

When the `v2` re-extraction produces a more complete version of the same claim, it doesn't overwrite the `v1` provenance record — it creates a new claim, with its own provenance record naming schema `v2`, and connects the two with a `supersedes` edge. This is **[supersession](../02-foundations/glossary.md#supersession)**: the old claim's status changes to `superseded`, but the claim itself stays exactly where it was, provenance record intact, still readable by anything that queries the graph as of the moment `v1` was current. Nothing was deleted. Nothing was rewritten in place. A reader who needs to know "what did we believe about this cause, and under which schema" can walk the `supersedes` edge backward and get the honest sequence — not a single record that quietly changed shape underneath everyone at some unrecorded moment.

## Diagram

```mermaid
flowchart LR
    V1["Claim (v1)<br/>checkout-api --caused-by--> expired CA cert<br/>status: superseded"] -- "supersedes" --> V2["Claim (v2)<br/>checkout-api --caused-by--> expired CA cert<br/>confidence: 0.9<br/>status: active"]
    P1["Provenance record<br/>source: PM-2117<br/>run: extraction-014<br/>schema: v1"] -. "attached to" .-> V1
    P2["Provenance record<br/>source: PM-2117<br/>run: extraction-029<br/>schema: v2"] -. "attached to" .-> V2
```

The `v1` claim never leaves the graph — its status changes and a `supersedes` edge points forward from it, but its own provenance record is untouched. A query run against the graph as it stood before the `v2` extraction still gets a truthful answer, because nothing about that earlier moment was rewritten to look like the later one.

## Claude Code vs OpenCode

Both approaches follow the same rule on discovering a more complete claim: create a new claim with its own provenance record, link it back to the old one, and change the old one's status — never edit the old claim's fields directly.

### Claude Code

```markdown
---
name: claim-supersession-writer
description: Records a more complete re-extraction as a new claim that supersedes the old one, never edits the old claim in place.
---

1. Given an existing claim and a newly re-extracted version of it (same
   subject, same relation, same object, produced under a newer schema
   version), do not modify any field on the existing claim.
2. Create a new claim node carrying the new fields, and attach a
   provenance record to it naming the source document, the extraction
   run, and the schema version that produced it.
3. Add a `supersedes` edge from the old claim to the new one, and change
   the old claim's status to `superseded`. Leave every other field on the
   old claim, including its own provenance record, exactly as it was.
```

### OpenCode

```markdown
---
description: Supersede an outdated claim with a re-extracted one instead of editing it in place
---

When a re-extraction under a newer schema produces a fuller version of an
existing claim: never touch the existing claim's fields. Create a new
claim node with its own provenance record (source document, extraction
run, schema version), add a supersedes edge from the old claim to the new
one, and set the old claim's status to superseded. The old claim's
provenance record must stay exactly as it was recorded originally.
```

## Going Deeper

Provenance has a cost, and it isn't free just because it's the right habit — a provenance record on every claim means every extraction pass has to track and attach three extra fields, and every downstream consumer has to decide what to do with a claim that's `superseded` instead of quietly reading whatever's newest. That cost is worth paying exactly when something downstream might someday need to ask "where did this come from, and is it still current" — a fact graph feeding an automated checker, or a claim likely to be revised as schemas evolve, both qualify. A one-off summary nobody will ever re-derive from doesn't need the same discipline; the point isn't provenance everywhere, it's provenance wherever a claim might later need defending.

## Check Yourself

<details>
<summary>A teammate argues that supersession is overkill here: the v1 and v2 claims say the same thing about the same cause, so just add the confidence field to the existing claim and skip creating a second node. What breaks if the team does that? Reveal the answer.</summary>

The graph loses the ability to tell "this claim was always this complete" from "this claim was patched later to look complete." Once the v1 claim's fields are edited directly, its provenance record — which still says schema v1 — no longer matches what the claim actually contains, since a v1 extraction run could never have produced a confidence field. Anyone auditing the graph afterward has no way to trust any provenance record again, because they'd have no way of knowing whether it describes what actually produced the claim or was quietly left behind after an edit.

</details>

## Try With AI

In a scratch directory, write one claim into `claims.jsonl` as a single JSON line — invent any short factual statement and give it a `schema_version` field of `v1`. Ask Claude Code or OpenCode to imagine a `v2` schema that adds one new required field, "re-extract" the same claim under it (making up a plausible value for the new field), and append the result correctly: a new line for the `v2` claim with its own provenance fields, plus a status change on the original `v1` line to `superseded` and a `supersedes` reference pointing at the new line's id. Open `claims.jsonl` afterward and check: is the original line still there, still readable, still saying `v1` — or did the agent take the shortcut and edit it in place?

## When It Goes Wrong

**Symptom:** two people (or two agents) disagree about what the graph "used to say" about some claim, and there's no way to settle it because the record in question has already changed.

**Cause:** a claim was edited directly when new information came in, instead of being superseded by a new claim — so the provenance record now describes a version of the claim that no longer exists.

**Fix:** never modify a claim's recorded fields after the fact; create a new claim with its own provenance record, link it back with a `supersedes` edge, and flip only the old claim's status field, leaving everything else on it untouched. `labs/step-8-supersede-not-overwrite.py` builds exactly this v1-to-v2 handoff and asserts the v1 record still exists, marked superseded, rather than being deleted.

---

Back to [Part 3 overview](README.md) · On to [Part 4](../06-part-4-working-from-the-graph/), where a worker finally reads from this graph instead of just adding to it.
