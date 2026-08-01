# Glossary

Short, one-paragraph definitions for the vocabulary this course uses. Each entry is written for how the term is used *in this course specifically* — if you've seen a slightly different definition somewhere else, that's expected; graph terminology varies more across communities than most people expect.

**Graph.** A structure made of two kinds of thing: nodes, which stand for something (an entity, an event, an attempt), and edges, which stand for a specific, named relationship between two nodes. A graph is useful precisely because it forces every relationship to be named instead of left implicit in a paragraph of prose somewhere.

**Node.** A single tracked thing in a graph — a person, a function, a ticket, an attempt, a claim. On its own a node carries almost no meaning; it becomes useful once edges connect it to other nodes.

**Edge.** A labeled, directed connection between two nodes that asserts something specific and checkable — "wrote," "depends on," "contradicts," "was informed by." A good edge is a small falsifiable claim, not a vague association; if you can't say what would make an edge wrong, it probably isn't specific enough yet.

**Work-history graph.** The graph that tracks what was attempted, in what order, by whom, and with what outcome — successful and unsuccessful attempts both. Its purpose is retracing: given a strange result, can you walk backward through it and see exactly how that result was produced.

**Fact graph.** The graph that tracks claims the team has checked and is willing to build further work on. It grows more slowly and more carefully than a work-history graph, because every node in it is implicitly a promise that the claim has been looked at, not just proposed.

**Extraction.** The step of turning an unstructured source — a document, a transcript, a diff — into structured nodes and edges that match a schema decided on beforehand. Extraction done well produces something a program can check; extraction done poorly produces a summary that only reads like structure.

**Resolution.** The step of recognizing that two different mentions actually refer to the same real thing, and merging them into a single node without discarding the fact that they started out as separate mentions. A resolution step that can't be undone is a resolution step that will eventually merge two things that shouldn't have been merged.

**Provenance.** The record attached to a node or edge of where it came from — which source, which extraction pass, which version of the schema that was active at the time. Provenance is what lets a wrong claim be traced, marked wrong, and replaced later instead of silently vanishing.

**Subgraph.** A deliberately small slice of a larger graph, scoped to exactly what one worker needs for one task. Handing a worker the whole graph defeats the purpose of having a graph at all — a subgraph is how you keep an agent's context small without keeping it uninformed.

**Grounding.** The property of a claim being traceable to specific supporting edges in a graph, rather than resting on how plausible or confident it sounds. A grounded claim can be checked mechanically; an ungrounded one can only be argued about.

**Governance graph.** A graph whose nodes are loops (or agents) rather than facts, and whose edges describe authority and accountability between them — who feeds whom input, who checks whose output, who is allowed to overrule whom. It's the layer you reach for once more than one loop is running against the same shared memory.

**Anchor.** A signal inside a governance graph that comes from outside the loop system entirely — a real test suite, a real user's response, an actual clock. Anchors matter because a group of loops that only check each other can end up perfectly self-consistent and completely wrong at the same time.

**Frozen node.** A node in a graph that no loop is permitted to rewrite, no matter how convenient rewriting it would be in the moment — often a rule, a threshold, or a definition of success. Freezing the right node is what stops a loop from quietly redefining its way to a passing grade.

**Counter-metric.** A second measurement, independent of whatever a loop is being optimized against and ideally invisible to the loop itself, used to catch the loop gaming its primary metric instead of actually achieving the underlying goal.
