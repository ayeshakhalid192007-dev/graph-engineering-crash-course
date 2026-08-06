# The Build-a-Graph Method

## Hook

An engineer who has already concluded, honestly, that a job needs a graph now faces a different problem: what to build first. Open a schema file too early and there's nothing yet to extract into it. Wire an audit loop before either graph holds a single claim and it has nothing to audit. This page names the order that keeps that from happening — six lettered stages, A through F, meant to be read as a build sequence rather than a menu of unrelated concerns.

## The six stages

Read top to bottom the first time through. After that, treat each letter as a place to jump back to when the corresponding piece of a real build is what's actually in front of you — the linked step is the full worked treatment, and this table is the map, not the territory.

| Stage | What happens | Full coverage |
| --- | --- | --- |
| **A. Confirm the job is graph-shaped** | Check whether a queue, a careful prompt, or a plain table would do the job for less, before opening a schema file. | Step 16, over in [the staying-grounded Part](../09-part-7-staying-grounded/); the [decision framework](decision-framework.md) |
| **B. Pick which graph the job needs** | A work-history graph and a fact graph solve different problems. Many real systems need both, connected by a pointer, never merged into one. | [The two graphs](../02-foundations/the-two-graphs.md) |
| **C. Design the schema** | Entity types, relationship types, and what counts as a valid claim all get decided on paper first — not discovered by whatever an extraction run happens to produce. | Step 6, which opens [the fact-graph material](../05-part-3-the-graph-of-facts/) |
| **D. Wire the write path** | Extraction, then resolution, then provenance, in that order. Nothing gets edited in place — a superseded claim is marked superseded, never rewritten. | Steps 6 through 8, all inside [the fact-graph material](../05-part-3-the-graph-of-facts/) |
| **E. Wire the read path** | A worker gets a bounded subgraph sized to its task, never the whole graph, and its output gets checked against real edges rather than how confident it sounds. | Steps 9 and 10, in [this course's fourth part](../06-part-4-working-from-the-graph/) |
| **F. Add governance edges only after evidence** | The named failure patterns a lone loop falls into each get their own fix, installed only once that specific failure has actually shown up — not on day one, against a risk that's still hypothetical. | Three fixes live in [this course's fifth part](../07-part-5-the-graph-of-loops/); the sizing discipline for all of them closes out [staying grounded](../09-part-7-staying-grounded/) |

## Why the order matters

Getting stage B wrong early — building only one graph when the job needed both, or blurring the two together — is one of this course's recurring judgment failures, and it's cheapest to catch before either graph has any content in it. Stage D's ordering matters for the same reason: a claim that skips straight to being "confirmed" without first surviving extraction and resolution has nowhere to record how it got there. And stage F sits last on purpose — installing it early is precisely the mistake Step 17 walks through in detail.

## Related

- [Decision framework](decision-framework.md) — the stage-A gate, on its own.
- [Pattern picker](pattern-picker.md) — matching a specific situation to a pattern once stage B has settled which graph you're building.
