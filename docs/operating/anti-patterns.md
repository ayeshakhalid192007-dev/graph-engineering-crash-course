# Anti-Patterns

## Hook

None of the mistakes below show up as a stack trace. Each one is a graph that keeps running, keeps answering queries, and keeps looking healthy on a dashboard while quietly becoming useless or actively wrong. This page collects them by the layer they live in, so a team can name what's actually broken instead of reaching for a generic "the graph feels off."

## Explanation

Three layers, three different kinds of damage. A design anti-pattern is a structural flaw baked in at build time — the graph itself is unsound. A governance anti-pattern only appears once more than one loop shares a graph, and it lives in the missing edges between loops rather than in either loop's code. A judgment anti-pattern isn't a flaw in any graph at all — it's reaching for a graph, or trusting one, in a situation that called for something else entirely. Fixing the wrong layer doesn't help: adding a counter-metric to a loop won't repair a graph with no schema, and a tighter schema won't stop a team from treating a two-month-old claim as gospel.

### Design anti-patterns

- **No schema before extraction.** Once an extraction prompt is allowed to invent entity and relationship types as it goes, every later query has to first work out which of several inconsistent shapes a given node happens to use, which turns "look this up" into "reverse-engineer this one first."
- **Silent, irreversible merges.** A resolution step that folds two mentions into one node and throws away which mentions they were forecloses the only way anyone later finds out the merge was wrong, so a bad merge simply becomes the record.
- **Edges with no provenance.** An edge nobody can trace to a source document or extraction run can't be defended when challenged, which means a team either has to trust it on faith or treat the whole graph as suspect the day one edge turns out to be false.
- **A subgraph big enough to be "the whole graph again."** Widening a task-scoped slice past what the task actually needs doesn't make a worker better informed, it just reintroduces the cost a subgraph exists to avoid — a worker sifting through material with no bearing on the job in front of it.
- **A checker that trusts tone over evidence.** A checker that approves a claim because the surrounding prose reads confidently will approve a false claim written confidently just as readily as it approves a true one written the same way, which makes the check theater rather than verification.

### Governance anti-patterns

- **A loop grading its own metric with no counter-signal.** A loop that only ever consults the number it's optimizing has no way to notice the day that number and the actual goal come apart, because from where it sits the two still look identical.
- **Every loop checking only its neighbors, with no anchor to outside reality.** A ring of loops that only validate each other's output can reach total internal agreement on something false, because nothing in the ring is answerable to anything the loops didn't produce themselves.
- **No frozen nodes, so a loop can rewrite the rule it's judged by.** Leaving a success threshold editable by the same loops it grades turns "did we get better" into a question those loops can answer however they like, at which point the metric stops meaning anything.
- **Two loops racing on the same resource with no arbitration edge.** Two individually sound loops that both assume they have exclusive claim to something will occasionally act at the same moment, and without a recorded precedence rule the outcome depends on whichever one happened to run first that day.

### Judgment anti-patterns

- **Building a graph for a job a spreadsheet already does.** A schema, an extraction pipeline, and a resolution step are all real, ongoing costs, and paying them for a small fixed set of relationships that never grows just means maintaining infrastructure a plain table would have handled for less.
- **Treating the fact graph as permanent truth instead of the team's current best understanding.** A fact graph is a snapshot of what's been checked and believed so far, not a verdict that closes the question, and a team that stops re-examining old claims will eventually build new work on top of one that quietly stopped being true.
- **Letting the work-history graph and the fact graph blur into one.** Once every attempt and every checked claim live in the same undifferentiated graph, there's no way to ask either question cleanly — "what did we try" gets polluted with unverified claims, and "what do we actually know" gets buried under the much larger volume of ordinary attempts.

## Related

- [`failure-modes.md`](failure-modes.md) — the compact reference for the four ways a single loop fails itself, which sit one level below the governance anti-patterns here.
- [`safety.md`](safety.md) — operational risks to a shared graph that go beyond any one anti-pattern above.
