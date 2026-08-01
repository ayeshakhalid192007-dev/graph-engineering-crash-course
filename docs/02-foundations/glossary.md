# Glossary

Short, one-paragraph definitions for the vocabulary this course uses. Each entry is written for how the term is used *in this course specifically* — if you've seen a slightly different definition somewhere else, that's expected; graph terminology varies more across communities than most people expect.

<a id="thin-memory-trick"></a>**Thin-memory trick.** The setup that's genuinely fine for exactly one automated loop: a lone plain-text file, checked at the start of a run and updated once at the end, with nothing else ever touching it in between runs. Its safety depends entirely on there being just one reader and one writer, taking turns — add a second process sharing that same file and the arrangement stops being fine without any code changing at all.

**Graph.** A structure made of two kinds of thing: nodes, which stand for something (an entity, an event, an attempt), and edges, which stand for a specific, named relationship between two nodes. A graph is useful precisely because it forces every relationship to be named instead of left implicit in a paragraph of prose somewhere.

<a id="node"></a>**Node.** A single tracked thing in a graph — a person, a function, a ticket, an attempt, a claim. On its own a node carries almost no meaning; it becomes useful once edges connect it to other nodes.

<a id="edge"></a>**Edge.** A labeled, directed connection between two nodes that asserts something specific and checkable — "wrote," "depends on," "contradicts," "was informed by." A good edge is a small falsifiable claim, not a vague association; if you can't say what would make an edge wrong, it probably isn't specific enough yet.

<a id="work-history-graph"></a>**Work-history graph.** A chronological record of attempts — what got tried, who tried it, what came before it, and whether it panned out, failures included. Read it backward from a puzzling outcome and the sequence of decisions behind it becomes something you can trace, not something you have to guess at.

<a id="fact-graph"></a>**Fact graph.** The graph that tracks claims the team has checked and is willing to build further work on. It grows more slowly and more carefully than a work-history graph, because every node in it is implicitly a promise that the claim has been looked at, not just proposed.

<a id="ratchet"></a>**Ratchet.** A rule for extending a work-history graph that only advances the record forward when a new attempt strictly beats whatever the current best attempt was — anything that doesn't clear that bar gets logged, not deleted, but also doesn't become the new reference point. The name is mechanical on purpose: like a socket wrench that only turns one way, the chain of kept attempts can only move toward "better than before," never quietly slide backward because a mediocre attempt got treated as progress.

<a id="durable-history"></a>**Durable history.** The specific chain of attempts a ratchet keeps — each one strictly better than the attempt before it, retained permanently as the record of how the current best result was actually reached. Durable history stays short precisely because it excludes the attempts that didn't improve on anything; the length of the chain measures how many times real progress happened, not how many times anything was tried.

<a id="queryable-failed-branch"></a>**Queryable failed branch.** An attempt that didn't make it into durable history but still exists as a node another worker can find and read later — what was tried, and specifically why it didn't work. The value isn't in celebrating the failure; it's in making that failure something a later worker can look up before spending a session rediscovering it firsthand.

<a id="schema"></a>**Schema.** The fixed list of entity types and relationship types a graph agrees to hold, settled before any extraction runs rather than expanded afterward to fit whatever a source happened to mention. A schema is a contract on what counts as an acceptable item, not a rough guideline extraction is free to talk its way around.

<a id="extraction"></a>**Extraction.** The step of turning an unstructured source — a document, a transcript, a diff — into structured nodes and edges checked against a schema decided on beforehand. An item that doesn't match the schema's allowed types gets rejected at this step, not reshaped until it looks close enough to pass.

<a id="resolution"></a>**Resolution.** The step of recognizing that two different mentions actually refer to the same real thing, and folding them into a single node without discarding the fact that they started out as separate mentions. Resolution that can't be undone is resolution that will eventually merge two things that never should have been merged.

<a id="reversible-merge"></a>**Reversible merge.** A resolution merge that keeps both of the original mentions, plus the stated reason they were judged to be the same underlying thing, attached to the node they were folded into. Nothing about a reversible merge is final the moment it happens — a reviewer can still inspect why it was made, and split it back apart if the reasoning turns out to be wrong.

<a id="provenance"></a>**Provenance.** The record attached to a claim stating where it came from — which source document, which extraction run, which schema version was active at the time. A claim's provenance record is what lets it be traced, checked, and superseded later instead of quietly rewritten with no trace of what it used to say.

<a id="supersession"></a>**Supersession.** Marking an existing claim as replaced by a newer one, linked to it by a direct edge, while leaving the old claim itself untouched apart from a flipped status field — never editing or deleting it outright. A superseded claim keeps its original content in place, letting a later reader trace what the graph used to hold and exactly when that changed.

**Subgraph.** A deliberately small slice of a larger graph, scoped to exactly what one worker needs for one task. Handing a worker the whole graph defeats the purpose of having a graph at all — a subgraph is how you keep an agent's context small without keeping it uninformed.

**Grounding.** The property of a claim being traceable to specific supporting edges in a graph, rather than resting on how plausible or confident it sounds. A grounded claim can be checked mechanically; an ungrounded one can only be argued about.

**Governance graph.** A graph whose nodes are loops (or agents) rather than facts, and whose edges describe authority and accountability between them — who feeds whom input, who checks whose output, who is allowed to overrule whom. It's the layer you reach for once more than one loop is running against the same shared memory.

**Anchor.** A check wired into a governance graph from outside the loop system altogether — nothing any loop authored or can nudge, like a passing integration test, an actual human's reaction, or the plain time on a clock. Without at least one, a set of loops checking only each other can settle into confident agreement on something false, with every internal signal insisting it's fine.

**Frozen node.** A fact or rule that stays off-limits to every loop's write access, full stop — not because changing it wouldn't help some loop in the moment, but because that exact temptation is the risk being guarded against. Success thresholds and safety rules are typical candidates. Skip this and a system of loops can gradually edit its own definition of success until every check passes while nothing underneath has actually improved.

**Counter-metric.** A second measurement, independent of whatever a loop is being optimized against and ideally invisible to the loop itself, used to catch the loop gaming its primary metric instead of actually achieving the underlying goal.
