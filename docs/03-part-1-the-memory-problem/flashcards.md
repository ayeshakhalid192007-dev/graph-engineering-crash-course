# Part 1 Flashcards

One card per term introduced in this Part. Cover the right-hand side and see if you can say it back in your own words first.

| Term | Definition |
| --- | --- |
| **Thin-memory trick** | Getting by on a single flat file as a lone loop's entire memory — workable only because exactly one process reads and rewrites it, with no second reader or writer ever sharing that moment. |
| **Node** | One tracked thing in a graph — a service, a file, an agent, an attempt, a claim — that carries little meaning on its own until an edge connects it to something else. |
| **Edge** | A connection between two nodes that names, specifically, what kind of relationship holds between them — the part of a graph that turns two loosely mentioned things into an actual, checkable statement. |
| **Directed edge** | An edge that points from one particular node to another, so that the relationship is understood to run in that direction and not automatically in reverse. |
| **Work-history graph** | The graph that records what was attempted — by whom, in what order, with what result — so a trail of past attempts stays available to walk back through later. |
| **Fact graph** | The graph that records claims about the world (or the code, or the domain) that have actually been checked, kept deliberately smaller and slower-growing than the work-history graph because each entry is a promise that it's been verified. |
