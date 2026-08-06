# Pattern Picker

## Hook

Seven categories of ready-to-run pattern ship with this course's pattern library on Day 3, and none of their names mean anything to a reader who hasn't built one yet. What's useful before that library exists — and just as useful once it does — is a way to go from "here's the situation I'm actually stuck on" to "here's which shelf to look on." This page is that lookup, organized by situation rather than by pattern name.

## Explanation

Each row names a situation a reader might actually be facing, what that category covers, and — where this course has already built the matching material — which step covers the underlying idea in full. The specific pattern kits themselves (their names, their READMEs, their starter code) land in `patterns/registry.yaml` once Day 3 ships; until then, every category below points generically to [`patterns/README.md`](../../patterns/README.md), which is still a stub.

| Category | If your situation sounds like... | It covers | Full coverage |
| --- | --- | --- | --- |
| **A. Extraction** | "I have documents, code changes, or conversation logs, and I need structured claims out of them." | Turning unstructured source material into entities and relationships under a schema, rather than free text. | Step 6 |
| **B. Resolution** | "The same real-world thing is showing up under two different names, or I'm not sure if this new claim is actually new." | Deciding whether an incoming claim is genuinely new, a duplicate, or an update to something already held — keeping a trail back to whatever gets merged. | Step 7 |
| **C. Provenance** | "I need to be able to say where a claim came from, or prove it later to someone who's asking." | A record of source, run, and schema version, written the moment a claim is created, not bolted on afterward. | Step 8 |
| **D. Subgraph / context-construction** | "I'm handing a worker or an agent a slice of the graph, and I don't want to hand it the whole thing." | Bounding what a worker sees to what its current task actually needs, instead of dumping the entire graph into context. | Step 9 |
| **E. Checker** | "I have an output and I want to know whether it's actually backed by the graph, not just confidently worded." | Verifying a claim against real edges rather than against how the output reads. | Step 10 |
| **F. Governance-wiring** | "My loops are stepping on each other, gaming their own metrics, drifting without anyone noticing, or fighting over the same resource." | Four dedicated fixes: a metric a loop can't see or nudge, a separate loop whose only job is watching the first, an edge that settles who has final say, and a fact frozen against every loop's write access. | Steps 11-13 — but read Step 17 first; this category is the one most likely to get installed ahead of the evidence that justifies it |
| **G. Storage & scale** | "I know what my graph needs to do; now I need to know what to actually store it in, at the size my team runs at." | Picking a storage backend proportional to team size and data volume, rather than reaching for the heaviest option by default. | Ships with the Day 3 pattern library |

## Using this page

Start from your situation, not from a pattern name — nobody arrives already knowing they want `alias-merge-with-trail`. Find the row that matches what's actually stuck, go read the step it names for the underlying idea, and check back once the Day 3 registry ships for the named kit that implements it end to end.

## Related

- [Decision framework](decision-framework.md) — confirm a graph is warranted at all before picking a category here.
- The [six-stage build sequence](build-a-graph-method.md) shows where these categories fit once a graph is underway.
