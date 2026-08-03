# Pattern Picker

## Hook

Seven categories of ready-to-run pattern ship with this course's pattern library on Day 3, and none of their names mean anything to a reader who hasn't built one yet. What's useful before that library exists — and just as useful once it does — is a way to go from "here's the situation I'm actually stuck on" to "here's which shelf to look on." This page is that lookup, organized by situation rather than by pattern name.

## Explanation

Each row below names a situation a reader might actually be facing, the pattern category it maps to, and — where this course has already built the matching material — which step covers the underlying idea in full. The specific pattern kits themselves (their names, their READMEs, their starter code) land in `patterns/registry.yaml` once Day 3 ships; until then, every category below points generically to [`patterns/README.md`](../../patterns/README.md), which is still a stub. Come back to this page once the registry exists and the category you need will resolve to a named, runnable kit instead.

**Category A — Extraction.** *"I have documents, code changes, or conversation logs, and I need structured claims out of them."* This is the write path's first stage: turning unstructured source material into entities and relationships under a schema, rather than free text. Step 6 works through the schema-first approach this course's extraction patterns build on.

**Category B — Resolution.** *"The same real-world thing is showing up under two different names, or I'm not sure if this new claim is actually new."* This is the check that runs right after extraction: deciding whether an incoming claim is genuinely new, a duplicate, or an update to something the graph already holds, and keeping a trail back to whatever gets merged. Covered at Step 7, also Part 3.

**Category C — Provenance.** *"I need to be able to say where a claim came from, or prove it later to someone who's asking."* Every claim that survives resolution needs a record of its source, its run, and its schema version — not bolted on after the fact, but written the moment the claim is created. Covered at Step 8, closing out Part 3.

**Category D — Subgraph / context-construction.** *"I'm handing a worker or an agent a slice of the graph, and I don't want to hand it the whole thing."* This covers bounding what a worker sees to what its current task actually needs, instead of dumping the entire graph into context. Covered at Step 9.

**Category E — Checker.** *"I have an output and I want to know whether it's actually backed by the graph, not just confidently worded."* A checker in this category verifies a claim against real edges rather than against how the output reads. Covered at Step 10, right after it in Part 4.

**Category F — Governance-wiring.** *"My loops are stepping on each other, gaming their own metrics, drifting without anyone noticing, or fighting over the same resource."* Each of these four situations gets its own dedicated fix, worked through at Steps 11 to 13 (the Part covering loops that share a graph): a metric a loop can't see or nudge, a separate loop whose only job is watching the first, an edge that settles who has the final say, and a fact frozen against every loop's write access. Read Step 17, back in Part 7, before reaching for any of them — this category is the one most likely to get installed ahead of the evidence that actually justifies it.

**Category G — Storage & scale.** *"I know what my graph needs to do; now I need to know what to actually store it in, at the size my team runs at."* This category isn't tied to a single step page in the core roadmap — it's a separate axis, about picking a storage backend proportional to team size and data volume rather than reaching for the heaviest option by default. It ships as part of the Day 3 pattern library.

## Using this page

Start from your situation, not from a pattern name — nobody arrives already knowing they want `alias-merge-with-trail`. Find the row that matches what's actually stuck, go read the step it names for the underlying idea, and check back once the Day 3 registry ships for the named kit that implements it end to end.
