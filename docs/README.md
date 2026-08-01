# Graph Engineering Course — Docs

This directory is the whole course. Everything readable on GitHub and everything rendered by the companion website is generated from these same markdown files — there is exactly one copy of the content, not two that can drift apart.

If you haven't been here before, don't start on this page. Visit [the router](00-start-here/README.md) first and answer a couple of quick questions about where you're coming from; it will point you at the right entry point below.

## Two ways through the material

**The core path (roughly two hours).** Steps 1 through 13, plus Projects 1 through 4. This gets you from "I have one loop and one memory file" to "I can build a fact graph, feed a worker a bounded slice of it, and check a claim against real edges instead of trusting how confident it sounds." Most readers stop here on a first pass and that's a complete, useful stopping point.

**The second read.** Steps 14 through 17, Projects 5 through 8, the full pattern library, and the advanced tier. This is where governance, scale, and the judgment calls about when *not* to build a graph live. Come back for it once the core path has had time to sink in, or once you're actually running more than one loop against a shared graph and need the harder material.

## Skill tracks

| Track | Level | Walking in, you already know… | Walking out, you can… | Where it lives |
| --- | --- | --- | --- | --- |
| **G1 · Foundations** | New to graphs | The Loop Engineering vocabulary — heartbeat, spine, maker/checker | Say exactly why a single memory file stops being enough once a second loop shows up, and separate a record of attempts from a store of facts | Prerequisites + Foundations + Part 1 |
| **G2 · Practitioner** | Comfortable with the two-graph split | That work-history and facts are different graphs with different jobs | Push a real claim through extraction, resolution, and provenance, then hand a worker a bounded subgraph and check its output against real edges | Parts 2–4 + Projects 2–6 |
| **G3 · Engineer** | Can stand up a single working graph | How one graph is built and read | Connect several loops into a governance graph, and name — and patch — each of the four ways a lone loop quietly goes wrong | Part 5 + Projects 7–8 + pattern library |
| **G4 · Ultra-Pro** | Has shipped a graph already | How to run a graph as production infrastructure | Recognize when a graph is the wrong tool for a job, scale one across a bigger system, and write a new pattern for someone else to reuse | Parts 6–7 + advanced tier + certification |

## Before Part 1

| Section | What it's for |
| --- | --- |
| [`00-start-here/`](00-start-here/README.md) | A short router — 2–3 questions that point you at the right starting page |
| [`01-prerequisites/`](01-prerequisites/README.md) | Confirms you have Loop Engineering and Harness Engineering, with recap primers if you want a refresher |
| [`02-foundations/`](02-foundations/glossary.md) | Vocabulary and mental models this whole course leans on: the glossary, the two-graph split at an intro level, and "comprehension debt" |

## The 17-step roadmap

Links below point at where Day 2 of this build will place each step's page. Until then they're placeholders for the shape of the course, not live pages — that's expected at this stage of the build.

### Part 1 — The Memory Problem

1. [Why loops outgrow a single memory file](03-part-1-the-memory-problem/step-1-why-loops-outgrow-a-single-memory-file.md)
2. [Graphs in plain terms](03-part-1-the-memory-problem/step-2-graphs-in-plain-terms.md)
3. [Keep your two graphs separate](03-part-1-the-memory-problem/step-3-keep-your-two-graphs-separate.md)

### Part 2 — The DAG of Work

4. [Recording attempts without losing the trail](04-part-2-the-dag-of-work/step-4-recording-attempts-without-losing-the-trail.md)
5. [Letting failed branches stay queryable](04-part-2-the-dag-of-work/step-5-letting-failed-branches-stay-queryable.md)

### Part 3 — The Graph of Facts

6. [Extraction: schema first, prose second](05-part-3-the-graph-of-facts/step-6-extraction-schema-first-prose-second.md)
7. [Resolution: merging without losing the evidence](05-part-3-the-graph-of-facts/step-7-resolution-merging-without-losing-the-evidence.md)
8. [Provenance: every claim keeps a receipt](05-part-3-the-graph-of-facts/step-8-provenance-every-claim-keeps-a-receipt.md)

### Part 4 — Working From the Graph

9. [Subgraphs: give a worker a slice, not the graph](06-part-4-working-from-the-graph/step-9-subgraphs-give-a-worker-a-slice-not-the-graph.md)
10. [The grounded checker](06-part-4-working-from-the-graph/step-10-the-grounded-checker.md)

### Part 5 — The Graph of Loops

11. [Wiring loops together](07-part-5-the-graph-of-loops/step-11-wiring-loops-together.md)
12. [Four ways a lone loop fails itself](07-part-5-the-graph-of-loops/step-12-four-ways-a-lone-loop-fails-itself.md)
13. [Anchors and frozen nodes](07-part-5-the-graph-of-loops/step-13-anchors-and-frozen-nodes.md)

### Part 6 — One Graph, End to End

14. [Six questions before you build](08-part-6-one-graph-end-to-end/step-14-six-questions-before-you-build.md)
15. [Build the same graph twice](08-part-6-one-graph-end-to-end/step-15-build-the-same-graph-twice.md)

### Part 7 — Staying Grounded

16. [When to skip graph engineering entirely](09-part-7-staying-grounded/step-16-when-to-skip-graph-engineering-entirely.md)
17. [Complexity budgets and staying the engineer](09-part-7-staying-grounded/step-17-complexity-budgets-and-staying-the-engineer.md)

## Reference material

| Section | What it's for |
| --- | --- |
| [`methods/`](methods/README.md) | The build-a-graph method, the pattern picker, and the pre-build decision framework |
| [`operating/`](operating/README.md) | Anti-patterns, failure modes, safety notes, and observability guidance |
| [`advanced/`](advanced/README.md) | The Ultra-Pro (G4) tier: scale, federation, and org-level governance |
| [`projects/`](projects/README.md) | The eight hands-on projects, from a first hand-drawn graph to the two-loop capstone |
| [`appendix/cheatsheets/`](appendix/cheatsheets/README.md) | Quick-reference sheets per tool |
| [`assessments/`](assessments/README.md) | The final exam, capstone rubric, and Graph Ready certification |

## Patterns and starter kits

Runnable material lives outside `docs/` at the repo root: [`patterns/`](../patterns/README.md) for the pattern catalog and [`starters/`](../starters/README.md) for clone-and-run kits. Full attribution for every idea this course draws on is in [`resources/sources.md`](../resources/sources.md).
