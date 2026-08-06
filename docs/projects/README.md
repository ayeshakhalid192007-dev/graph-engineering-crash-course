# Practice Projects

Eight original, hands-on projects, easy to capstone. Each one exercises exactly one idea from the 17-step course by putting it to work on a scenario invented for that project — not the worked example from the step page itself. Every project ships with a reference solution under `solutions/` so you can check your own attempt once you've made one.

**Throwaway repo, small data first.** Every project here is meant to be run in a repo you're willing to delete afterward, against data small enough to read end to end in one sitting. That's not a limitation of the exercises — it's the whole point. A graph you can hold in your head while you build it is the fastest way to learn what a graph actually does.

Work through Projects 1–4 alongside Steps 1–13 (the core path); save 5–8 for the second read, once Parts 3–5 are behind you.

## Index

| # | Project | Difficulty | Time | Concepts | Maps to |
| - | ------- | ---------- | ---- | -------- | ------- |
| 1 | [Nodes and edges by hand](01-nodes-and-edges-by-hand.md) | Beginner | 15–20 min | node, edge, direction, label specificity | Step 2, Part 1 |
| 2 | [The ratchet](02-the-ratchet.md) | Beginner–Intermediate | 45–60 min | ratchet, durable history, non-improving attempts logged | Step 4, Part 2 |
| 3 | [Extract your first ten facts](03-extract-your-first-ten-facts.md) | Intermediate | 30–45 min | fixed schema, extraction, rejecting out-of-schema items | Step 6, Part 3 |
| 4 | [Merge without losing the trail](04-merge-without-losing-the-trail.md) | Intermediate–Advanced | 45–60 min | resolution, reversible merges, evidence over similarity | Step 7, Part 3 |
| 5 | [Give every edge a receipt](05-give-every-edge-a-receipt.md) | Intermediate | 30–45 min | provenance, source records, schema-version tracking | Step 8, Part 3 |
| 6 | [Feed a worker a subgraph](06-feed-a-worker-a-subgraph.md) | Intermediate | 45–60 min | subgraphs, bounded context, task-scoped retrieval | Step 9, Part 4 |
| 7 | [Catch a lie with a checker](07-catch-a-lie-with-a-checker.md) | Advanced | 45–60 min | grounding, rejecting claims the graph can't back up | Step 10, Part 4 |
| 8 | [Wire two loops together (capstone)](08-wire-two-loops-together-capstone.md) | Capstone | 90–120 min | governance graph, arbitration, anchors, frozen nodes | Steps 11–13, Part 5 |

Each project page names its step(s) again up top and points to the [course-wide docs guide](../README.md) for the exact link — that guide's roadmap is the single place step links are kept, so it's the one place they won't drift out of date.

## How to use these

1. Read the step(s) a project maps to first — the project assumes you've already met the concept, and won't re-explain it. Use the [docs guide](../README.md)'s roadmap to jump to the right page.
2. Set up the throwaway repo the project's banner asks for, and pull in only the small starting material the project provides (if any).
3. Do the project yourself before opening its reference solution. The solution shows one concrete, checkable answer to that project's own scenario — not the only correct answer, but one you can compare your work against.
4. If your result diverges from the solution, that's not automatically wrong — check whether the divergence still satisfies the project's "done when" criteria before assuming you made a mistake.

## Solutions

Every project's reference solution lives under `solutions/`, at the path matching its own filename — Project 1's solution sits alongside Project 1's page, and so on down the list. Each project page links directly to its own solution at the bottom.
