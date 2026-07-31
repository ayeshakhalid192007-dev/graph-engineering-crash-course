# Day 2 Implementation Plan — The Full 17-Step Course + Assessments

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Execution mode:** Runs under one `/loop`. Tasks 1–9 (the seven Part tasks + methods + operating) are independent of each other — the loop fans them out to parallel subagents simultaneously, then Task 10 (verification) runs sequentially once all nine land. The loop self-stops after Task 10 and waits for user approval before `day-3-plan.md` starts.
>
> **Prerequisite:** `day-1-plan.md` must be complete and approved — this plan assumes `docs/00-start-here/`, `docs/01-prerequisites/`, `docs/02-foundations/`, `scripts/originality-check.mjs`, and the directory stubs from Day 1 Task 6 Step 11 already exist.

**Goal:** Author all 17 step pages (the complete conceptual course body, Parts 1–7), each part's quiz and flashcards, the three `methods/` pages, and the four `operating/` pages — 100% original prose, each passing `scripts/originality-check.mjs`.

**Architecture:** One `docs/0N-part-*/` folder per Part (already stubbed Day 1), populated with its step pages + `quiz.md` + `flashcards.md` + one live-lab script per step page. Live-lab scripts are colocated at `docs/0N-part-*/labs/step-N-<slug>.sh` (or `.py`) — a new `scripts/verify-labs.sh` aggregates and runs every one of them (see Task 10). This colocation choice isn't specified in graph-plan.md §23's tree diagram; flagging it now as a judgment call for the Day 2 approval gate rather than assuming silently.

**Tech Stack:** Markdown, mermaid (fenced diagrams), bash/python3 (live labs, dependency-free per §21), Claude Code + OpenCode config snippets (dual-tool code tabs).

## Global Constraints

- **Originality policy (§2.1)** applies to every file in this plan, same as Day 1. Run `node scripts/originality-check.mjs` after every task before committing.
- **Page template (§12)** is fully in force for all 17 step pages now (unlike Day 1's lighter treatment): hook → plain-English explanation → mermaid diagram → dual-tool code tabs (Claude Code ↔ OpenCode) → going-deeper callout → check-yourself quiz question → Try With AI exercise → when-it-goes-wrong → glossary popovers (linking to terms in `docs/02-foundations/glossary.md`).
- **Every diagram, code sample, and worked example is invented for this course** (§2.1 rule 4) — no step's scenario may reuse another step's scenario, and none may resemble a source's own example re-narrated.
- **`docs/02-foundations/the-two-graphs.md` (Day 1) vs. Step 3:** Step 3 (Task 1 below) goes deeper on the same split but must use a different concrete example than the Day 1 foundations page (which used a support-ticket scenario) — pick something new, e.g. a multi-agent code-review scenario.
- **Live labs (§21):** each of the 17 scripts requires no API key and no network, runs via a single interpreter (`bash` or `python3`), and is checkable by `scripts/verify-labs.sh` (Task 10) — meaning each script must either print an unambiguous PASS/FAIL line or exit nonzero on failure, so the aggregator can detect it.
- **Definition of Done for Day 2** (§27 Day 2): the entire conceptual course (G1–G3 body — Parts 1–7, all 17 steps) is complete, readable, and passes the originality check; every part has its `quiz.md` and `flashcards.md`; `methods/` and `operating/` are complete.

---

## Task 1: Part 1 — The Memory Problem (Steps 1–3)

**Files:**
- Create: `docs/03-part-1-the-memory-problem/step-1-why-loops-outgrow-a-single-memory-file.md`
- Create: `docs/03-part-1-the-memory-problem/step-2-graphs-in-plain-terms.md`
- Create: `docs/03-part-1-the-memory-problem/step-3-keep-your-two-graphs-separate.md`
- Create: `docs/03-part-1-the-memory-problem/quiz.md`
- Create: `docs/03-part-1-the-memory-problem/flashcards.md`
- Create: `docs/03-part-1-the-memory-problem/labs/step-1-two-writers-one-file.sh`
- Create: `docs/03-part-1-the-memory-problem/labs/step-2-label-the-arrow.py`
- Create: `docs/03-part-1-the-memory-problem/labs/step-3-split-the-graphs.py`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 1 bullets (Steps 1–3 one-line descriptions), §6 (what Graph Engineering is), §7 (two graphs), `docs/02-foundations/the-two-graphs.md` (must not reuse its support-ticket example).
- Produces: this Part's pages are linked from `docs/README.md` (Day 1) — verify those links resolve in Task 10.

- [ ] **Step 1: Write `step-1-why-loops-outgrow-a-single-memory-file.md`**

Full §12 template. Outline (from graph-plan.md §14): the thin-memory trick (one loop, one file, one reader/writer, never concurrent) and precisely where it breaks — two writers clobbering an update, a reader unable to tell a settled fact from a half-finished guess. Original scenario: invent a concrete two-agent collision (e.g., two parallel code-review agents both appending "verdict: safe" to the same notes file at once, one overwriting the other's caveat) — must be a new scenario, not reused from graph-plan.md §6's own framing. Mermaid diagram: two writer nodes racing to one file node. Dual-tool code: a minimal Claude Code skill snippet and an OpenCode equivalent, both showing "read file, decide, write file" without any locking — illustrating the failure, not fixing it yet.

- [ ] **Step 2: Write `step-2-graphs-in-plain-terms.md`**

Full §12 template. Outline: nodes, edges, direction — what a labeled, directed arrow is actually claiming (e.g., an edge `A --wrote--> B` claims something specific and falsifiable, unlike a loose mention in prose). Original example: model a small real-world fact (e.g., "the auth middleware depends on the session store") as three nodes and one directed, labeled edge. Mermaid diagram of that exact example.

- [ ] **Step 3: Write `step-3-keep-your-two-graphs-separate.md`**

Full §12 template. Outline: work-history graph vs. fact graph (§7), what each answers, why collapsing them produces something too noisy to trust and too sparse to reconstruct. New scenario (per Global Constraints: a multi-agent code-review setup, distinct from Day 1's support-ticket example) showing the same underlying event recorded twice — once as a work-history node ("agent X reviewed PR #42, flagged issue"), once as a fact-graph node ("function `foo` has no null check") — and why merging those two records into one node would corrupt both.

- [ ] **Step 4: Write `quiz.md`**

One question per step (3 total), each with a revealed answer, in this course's own original phrasing — not lifted from the step pages verbatim in full sentences (paraphrase the question).

- [ ] **Step 5: Write `flashcards.md`**

One card per key term introduced in this Part (thin-memory trick, node, edge, directed edge, work-history graph, fact graph) — term + one-sentence original definition.

- [ ] **Step 6: Write the three live-lab scripts**

`step-1-two-writers-one-file.sh`: a bash script with no dependencies that spins up two sequential (not truly concurrent, to stay deterministic and network-free) writes to a shared file and shows the second silently clobbering the first's content — prints `FAIL (expected): writer B overwrote writer A's caveat` to make the point, then exits 0 (the "failure" being demonstrated is the point of the demo, not a bug in the script).
`step-2-label-the-arrow.py`: builds the auth-middleware/session-store example as an in-memory adjacency structure (plain dict, no libraries) and prints the one directed edge with its label, asserting the edge direction is meaningful (asserts `A->B != B->A` are treated distinctly) — exits 0 on success, 1 if the assertion fails.
`step-3-split-the-graphs.py`: builds both a tiny work-history list and a tiny fact list for the code-review scenario, merges them naively into one list, and asserts (and prints) that the naive merge loses the distinction between "agent claimed X" and "X is true" — exits 0 when the demo runs, printing the corruption it causes as the lesson.

- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/03-part-1-the-memory-problem
git commit -m "Add Part 1 (Steps 1-3): the memory problem"
```

---

## Task 2: Part 2 — The DAG of Work (Steps 4–5)

**Files:**
- Create: `docs/04-part-2-the-dag-of-work/step-4-recording-attempts-without-losing-the-trail.md`
- Create: `docs/04-part-2-the-dag-of-work/step-5-letting-failed-branches-stay-queryable.md`
- Create: `docs/04-part-2-the-dag-of-work/quiz.md`
- Create: `docs/04-part-2-the-dag-of-work/flashcards.md`
- Create: `docs/04-part-2-the-dag-of-work/labs/step-4-the-ratchet.py`
- Create: `docs/04-part-2-the-dag-of-work/labs/step-5-failed-branch-stays.py`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 2, source #4 (Karpathy `autoresearch` ratchet mechanism — idea only, no source text), source #5 (Karpathy `AgentHub` search-graph mechanism — idea only).
- Produces: none consumed by later Parts directly, but Task 6 (Part 5, governance) may reference "the ratchet" by name — ensure the term is defined here first.

- [ ] **Step 1: Write `step-4-recording-attempts-without-losing-the-trail.md`**

Full §12 template. Outline: the ratchet mechanism in this course's own words — keep only the improving attempts as durable history, log the rest, so the record doesn't grow unboundedly noisy. Original scenario: a hyperparameter-search-style loop trying several prompts for a summarization task, ratcheting forward only when a new attempt's score beats the prior best. Mermaid diagram: a chain of "kept" nodes with side branches of "logged, not kept" attempts.

- [ ] **Step 2: Write `step-5-letting-failed-branches-stay-queryable.md`**

Full §12 template. Outline: why a discarded attempt should remain a queryable node rather than vanish — a later worker can see "this was tried and didn't work" instead of re-discovering the same dead end. Original scenario distinct from Step 4's: a multi-agent bug-fix session where three different fix approaches are tried, two fail and stay in the graph as failed-but-queryable nodes, so a fourth agent starting later doesn't repeat them.

- [ ] **Step 3: Write `quiz.md` and `flashcards.md`** (same structure as Task 1 Steps 4–5, scoped to this Part's two steps and terms: ratchet, durable history, queryable failed branch).

- [ ] **Step 4: Write the two live-lab scripts**

`step-4-the-ratchet.py`: runs a tiny scored loop over a fixed list of five candidate scores, keeps only strictly-improving ones as "commits," logs the rest, and prints the final kept chain vs. the discarded list — exits 0.
`step-5-failed-branch-stays.py`: models three fix-attempt nodes (two marked failed), queries "what's already been tried for this bug" and prints all three including the failed ones, asserting the failed ones are still present in the query result (not deleted) — exits 1 if a failed node is missing from the query result, 0 otherwise.

- [ ] **Step 5: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/04-part-2-the-dag-of-work
git commit -m "Add Part 2 (Steps 4-5): the DAG of work"
```

---

## Task 3: Part 3 — The Graph of Facts (Steps 6–8)

**Files:**
- Create: `docs/05-part-3-the-graph-of-facts/step-6-extraction-schema-first-prose-second.md`
- Create: `docs/05-part-3-the-graph-of-facts/step-7-resolution-merging-without-losing-the-evidence.md`
- Create: `docs/05-part-3-the-graph-of-facts/step-8-provenance-every-claim-keeps-a-receipt.md`
- Create: `docs/05-part-3-the-graph-of-facts/quiz.md`
- Create: `docs/05-part-3-the-graph-of-facts/flashcards.md`
- Create: `docs/05-part-3-the-graph-of-facts/labs/step-6-schema-first-extraction.py`
- Create: `docs/05-part-3-the-graph-of-facts/labs/step-7-reversible-merge.py`
- Create: `docs/05-part-3-the-graph-of-facts/labs/step-8-supersede-not-overwrite.py`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 3, §8 (lifecycle of a fact: extraction/resolution/provenance), source #6 (Anthropic Knowledge Graph Construction Cookbook — schema-first extraction idea only).
- Produces: this Part defines "schema," "resolution," "provenance" precisely — Task 5 (Part 5 grounded checker) and Day 3's pattern kits (`document-to-facts`, `alias-merge-with-trail`, `receipt-per-edge`) depend on these definitions being unambiguous; keep the terminology exactly consistent (e.g. always "provenance record," never switch to "source record" partway through).

- [ ] **Step 1: Write `step-6-extraction-schema-first-prose-second.md`**

Full §12 template. Outline: define the shape of an acceptable answer (entity types, relationship types) before asking a model to produce one; the schema as a contract, not decoration. Original scenario: extracting facts from a fictional incident postmortem doc into a small schema (entities: Service, Incident, Cause; relationships: caused-by, affected). Dual-tool code: a Claude Code structured-output prompt/schema snippet and an OpenCode equivalent.

- [ ] **Step 2: Write `step-7-resolution-merging-without-losing-the-evidence.md`**

Full §12 template. Outline: the same real-world entity appearing under different surface names, merging them into one node reversibly — original mentions and merge reasoning stay attached. Original scenario: two documents referring to "the payments service" and "billing-svc" as the same underlying service; show the merge keeping both original mentions linked to the merged node.

- [ ] **Step 3: Write `step-8-provenance-every-claim-keeps-a-receipt.md`**

Full §12 template. Outline: every claim carries source document, extraction run, schema version; when a claim is later found wrong, it's marked superseded and replaced, never silently overwritten. Original scenario: a claim extracted under schema v1 is later found incomplete after a schema v2 adds a needed field — show the supersession record, not a silent edit.

- [ ] **Step 4: Write `quiz.md` and `flashcards.md`** (terms: schema, extraction, resolution, reversible merge, provenance, supersession).

- [ ] **Step 5: Write the three live-lab scripts**

`step-6-schema-first-extraction.py`: defines a plain-dict schema (allowed entity/relationship types), runs a fake "extraction" over a hardcoded small text (no LLM call — deterministic, network-free), and asserts every extracted item matches the schema, rejecting one deliberately-malformed item to prove the schema is enforced.
`step-7-reversible-merge.py`: merges the two service-name mentions into one node, then asserts both original mentions are still individually retrievable from the merged node (reversibility check) — exits 1 if either original mention is lost.
`step-8-supersede-not-overwrite.py`: creates a v1 claim, "discovers" it's incomplete, creates a v2 claim marked as superseding v1, and asserts the v1 record still exists (marked superseded) rather than being deleted — exits 1 if v1 was removed instead of superseded.

- [ ] **Step 6: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/05-part-3-the-graph-of-facts
git commit -m "Add Part 3 (Steps 6-8): the graph of facts"
```

---

## Task 4: Part 4 — Working From the Graph (Steps 9–10)

**Files:**
- Create: `docs/06-part-4-working-from-the-graph/step-9-subgraphs-give-a-worker-a-slice-not-the-graph.md`
- Create: `docs/06-part-4-working-from-the-graph/step-10-the-grounded-checker.md`
- Create: `docs/06-part-4-working-from-the-graph/quiz.md`
- Create: `docs/06-part-4-working-from-the-graph/flashcards.md`
- Create: `docs/06-part-4-working-from-the-graph/labs/step-9-task-scoped-subgraph.py`
- Create: `docs/06-part-4-working-from-the-graph/labs/step-10-grounded-checker.py`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 4, §9 (working from the graph: subgraphs, grounded checkers), Task 3's provenance/schema vocabulary (the grounded checker in Step 10 checks for specific missing edges, which only makes sense once "edge" and "schema" are well defined).
- Produces: Step 9's "subgraph" and Step 10's "grounded checker" are exactly the mechanisms Day 3's `task-scoped-retrieval` and `grounded-triple-checker` patterns implement — keep definitions consistent for that reuse.

- [ ] **Step 1: Write `step-9-subgraphs-give-a-worker-a-slice-not-the-graph.md`**

Full §12 template. Outline: no worker should see the whole graph; a task-scoped subgraph keeps context small and focused; a contradiction inside the relevant slice should travel into the subgraph rather than being silently resolved before the worker sees it. Original scenario: a single worker fixing one function gets a subgraph of just that function's direct dependencies and any conflicting claims about its behavior, not the whole codebase graph.

- [ ] **Step 2: Write `step-10-the-grounded-checker.md`**

Full §12 template. Outline: a checker built on the graph verifies claims mechanically — decomposing a claim into the specific edges that would have to exist, and looking for them, rather than asking "does this sound right." Original scenario: a checker verifying the claim "this PR doesn't touch the auth path" by checking for the absence of a specific edge (`PR --modifies--> auth-module`) rather than reading the PR description's tone.

- [ ] **Step 3: Write `quiz.md` and `flashcards.md`** (terms: subgraph, task-scoped context, contradiction-aware bundle, grounded checker, decomposed claim).

- [ ] **Step 4: Write the two live-lab scripts**

`step-9-task-scoped-subgraph.py`: builds a small graph (10+ nodes), extracts a bounded subgraph for one task (only direct neighbors of a target node, depth 1), and asserts the subgraph's node count is smaller than the full graph's and still contains a deliberately-inserted contradicting pair of edges (proving contradictions travel with the slice rather than being filtered out).
`step-10-grounded-checker.py`: given a small graph and a claim ("PR does not modify auth-module"), decomposes the claim into the edge that would have to exist for it to be false, checks for that edge's absence, and correctly rejects a second, fabricated claim where the edge *is* present — exits 1 if the checker approves the fabricated claim.

- [ ] **Step 5: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/06-part-4-working-from-the-graph
git commit -m "Add Part 4 (Steps 9-10): working from the graph"
```

---

## Task 5: Part 5 — The Graph of Loops (Steps 11–13)

**Files:**
- Create: `docs/07-part-5-the-graph-of-loops/step-11-wiring-loops-together.md`
- Create: `docs/07-part-5-the-graph-of-loops/step-12-four-ways-a-lone-loop-fails-itself.md`
- Create: `docs/07-part-5-the-graph-of-loops/step-13-anchors-and-frozen-nodes.md`
- Create: `docs/07-part-5-the-graph-of-loops/quiz.md`
- Create: `docs/07-part-5-the-graph-of-loops/flashcards.md`
- Create: `docs/07-part-5-the-graph-of-loops/labs/step-11-governance-graph.py`
- Create: `docs/07-part-5-the-graph-of-loops/labs/step-12-four-failure-modes.py`
- Create: `docs/07-part-5-the-graph-of-loops/labs/step-13-anchor-and-freeze.py`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 5, §10 (the graph of loops, four failure modes, anchors/frozen nodes), source #8 (Carlos E. Perez four-failure-mode framing — idea only). This repo's own `LOOP.md`/`loop-constraints.md` (Day 1) are a real running example of Step 13's anchor-and-frozen-node concepts — Step 13 may reference them by name as a live, dogfooded instance without quoting their text verbatim.
- Produces: the four failure modes named here (metric-gaming, blind spot, collision, drift) are exactly what Day 3's `counter-metric-loop`, `audit-loop`, `arbitration-edge`, and `anchor-and-freeze` patterns implement 1:1 — keep the four names consistent for that mapping.

- [ ] **Step 1: Write `step-11-wiring-loops-together.md`**

Full §12 template. Outline: draw loops as nodes and their relationships (feeds, checks, overrules) as edges — a governance graph on top of the fact graph. Original scenario: three loops (a drafting loop, a review loop, an escalation loop) wired with explicit "checks" and "can overrule" edges for a content-publishing pipeline.

- [ ] **Step 2: Write `step-12-four-ways-a-lone-loop-fails-itself.md`**

Full §12 template. Outline: the four failure modes and their fixes, each illustrated with its own small original scenario — (1) optimizing the metric instead of the goal → counter-metric; (2) blind to a class of problem inside its own scope → wider-vantage audit loop; (3) two individually-reasonable loops colliding on one resource → arbitration edge; (4) "good" drifting as the system changes → periodic edge back to a human/fresher reference. Four distinct short scenarios, not one scenario reused four ways.

- [ ] **Step 3: Write `step-13-anchors-and-frozen-nodes.md`**

Full §12 template. Outline: a governance graph made only of loops checking each other can be entirely self-consistent and collectively wrong; an anchor (a signal reaching outside the loop system) and frozen nodes (facts/rules no loop may rewrite) prevent that. May cite this repo's own `loop-constraints.md` (Day 1) as a real frozen-node example.

- [ ] **Step 4: Write `quiz.md` and `flashcards.md`** (terms: governance graph, counter-metric, audit loop, arbitration edge, drift, anchor, frozen node).

- [ ] **Step 5: Write the three live-lab scripts**

`step-11-governance-graph.py`: builds the three-loop publishing pipeline as nodes/edges and prints a topological check that "escalation loop can overrule review loop" is a real edge in the structure, not just asserted in prose.
`step-12-four-failure-modes.py`: simulates a toy loop gaming a single metric (e.g., maximizing a count with no quality signal) across a few iterations, then reruns it with a counter-metric added and shows the gamed behavior gets caught — prints both runs' outcomes for contrast.
`step-13-anchor-and-freeze.py`: builds a small governance graph where every loop's report is internally consistent with its neighbors but collectively wrong (a planted scenario), then shows an anchor check (comparing against a fixed, unmanipulated reference value) catching what no inter-loop check could — exits 1 if the anchor fails to catch the planted inconsistency.

- [ ] **Step 6: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/07-part-5-the-graph-of-loops
git commit -m "Add Part 5 (Steps 11-13): the graph of loops"
```

---

## Task 6: Part 6 — One Graph, End to End (Steps 14–15)

**Files:**
- Create: `docs/08-part-6-one-graph-end-to-end/step-14-six-questions-before-you-build.md`
- Create: `docs/08-part-6-one-graph-end-to-end/step-15-build-the-same-graph-twice.md`
- Create: `docs/08-part-6-one-graph-end-to-end/quiz.md`
- Create: `docs/08-part-6-one-graph-end-to-end/labs/step-14-six-questions-checklist.py`
- Create: `docs/08-part-6-one-graph-end-to-end/labs/step-15-build-twice-verify-parity.sh`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 6, §11 (when not to build one — the six-question checklist is a fresh operationalization of the situations listed there), §15 (the build-a-graph method A–F, which Task 8's `methods/build-a-graph-method.md` documents in full — Step 15 walks through it once concretely rather than redefining it).
- Produces: Step 15's dual-tool worked system is the direct forerunner of Day 3's seven core pattern kits — its scenario should be small and self-contained, not one of the seven pattern names itself (avoid stepping on Day 3's `document-to-facts` etc.).

- [ ] **Step 1: Write `step-14-six-questions-before-you-build.md`**

Full §12 template (note: this Part's `quiz.md` only, no `flashcards.md` per graph-plan.md §23's tree — Part 6 is listed with "dual-tool walkthroughs, quiz" only). Outline: six honest pre-build questions, original phrasing, each derived from a §11 situation (independent tasks needing a queue, not a graph; a single document needing a good prompt, not a graph; a small fixed relationship set needing a table, not a graph; no downstream need to ask "where did this come from"; team size vs. maintenance cost; how fast the domain changes).

- [ ] **Step 2: Write `step-15-build-the-same-graph-twice.md`**

Full §12 template. A complete small worked system (schema → extraction → resolution → provenance → subgraph → checker) built once in Claude Code and once in OpenCode, using one new, small, original scenario (e.g., tracking which of a team's five services depend on which, from a handful of fictional architecture-doc snippets) — deliberately smaller than any Day 3 core pattern so it doesn't duplicate them.

- [ ] **Step 3: Write `quiz.md`** (six-questions checklist + the worked system, terms: pre-build checklist, dual-tool parity).

- [ ] **Step 4: Write the two live-lab scripts**

`step-14-six-questions-checklist.py`: encodes the six questions as a small CLI-style checklist that takes hardcoded yes/no answers for three example scenarios (a queue-shaped task set, a single-document Q&A, and a genuinely graph-shaped multi-service system) and prints "build a graph: yes/no" for each, matching the expected verdict for each planted example.
`step-15-build-twice-verify-parity.sh`: runs the two worked-system implementations' output (as plain JSON/text, no real tool invocation needed — a deterministic stand-in for "the Claude Code version" and "the OpenCode version" of the same logic) and diffs them, asserting they produce the same final graph structure — exits 1 on any diff.

- [ ] **Step 5: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/08-part-6-one-graph-end-to-end
git commit -m "Add Part 6 (Steps 14-15): one graph, end to end"
```

---

## Task 7: Part 7 — Staying Grounded (Steps 16–17)

**Files:**
- Create: `docs/09-part-7-staying-grounded/step-16-when-to-skip-graph-engineering-entirely.md`
- Create: `docs/09-part-7-staying-grounded/step-17-complexity-budgets-and-staying-the-engineer.md`
- Create: `docs/09-part-7-staying-grounded/quiz.md`
- Create: `docs/09-part-7-staying-grounded/flashcards.md`
- Create: `docs/09-part-7-staying-grounded/labs/step-16-skip-decision.py`
- Create: `docs/09-part-7-staying-grounded/labs/step-17-complexity-budget.py`

**Interfaces:**
- Consumes: graph-plan.md §14 Part 7, §11 (concrete situations that don't justify a graph), §16 (judgment anti-patterns — "building a graph for a job a spreadsheet already does").
- Produces: `docs/00-start-here/README.md` (Day 1) routes readers here directly if they mainly want the "do we need one" answer — verify that link still makes sense once this page exists (Task 10).

- [ ] **Step 1: Write `step-16-when-to-skip-graph-engineering-entirely.md`**

Full §12 template. Outline: the concrete situations from §11 as a decision aid — a genuinely independent task set (use a queue), a single-document single-answer job (use a good prompt), a small fixed relationship set that never grows (use a relational table), nothing downstream ever asking for provenance (skip it). New original scenario per situation, distinct from Step 14's six-questions scenarios (different concrete examples, not reused).

- [ ] **Step 2: Write `step-17-complexity-budgets-and-staying-the-engineer.md`**

Full §12 template. Outline: sizing a graph to the actual job, not building governance edges (§10–13) you don't have evidence you need yet — add them only after a real failure has shown the need (echoes §15 point F). Original scenario: a team that added all four governance fixes from Step 12 on day one, before any of the four failure modes had actually occurred, and paid unnecessary maintenance cost for edges nothing had shown were needed.

- [ ] **Step 3: Write `quiz.md` and `flashcards.md`** (terms: complexity budget, premature governance, decision aid).

- [ ] **Step 4: Write the two live-lab scripts**

`step-16-skip-decision.py`: runs the four §11 situations as planted scenarios through a small decision function and asserts each resolves to "don't build a graph" plus the correct lighter-weight alternative (queue/prompt/table/no-provenance-needed) — exits 1 on any mismatch.
`step-17-complexity-budget.py`: simulates the over-eager team adding all four governance edges up front vs. a team adding them only after each corresponding failure is observed, and prints a simple maintenance-cost tally showing the up-front team paying more for unused edges — illustrative, not a strict pass/fail assertion (prints the comparison; exits 0).

- [ ] **Step 5: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/09-part-7-staying-grounded
git commit -m "Add Part 7 (Steps 16-17): staying grounded"
```

---

## Task 8: `docs/methods/`

**Files:**
- Create: `docs/methods/build-a-graph-method.md`
- Create: `docs/methods/pattern-picker.md`
- Create: `docs/methods/decision-framework.md`

**Interfaces:**
- Consumes: graph-plan.md §15 (the build-a-graph method A–F), §14 Part 6 Step 14 (six questions, referenced not repeated), §17 (pattern catalog categories A–G, for the picker).
- Produces: `docs/methods/decision-framework.md` is explicitly "the six pre-build questions from Step 14" per graph-plan.md §22 — it must reference Step 14's page rather than re-deriving the six questions independently, to avoid a second, possibly-drifted copy of the same checklist.

- [ ] **Step 1: Write `build-a-graph-method.md`**

Full method write-up (not full §12 template — this is a reference/method page, hook + explanation suffice): the six-part method A (decide if you need one, linking Step 14/16) · B (pick the shape) · C (schema before extraction, linking Step 6) · D (write path: extraction → resolution → provenance, linking Steps 6–8) · E (read path: subgraph + grounded checker, linking Steps 9–10) · F (add governance edges only once a real failure shows the need, linking Steps 11–13 and Step 17).

- [ ] **Step 2: Write `pattern-picker.md`**

A decision aid mapping a reader's situation to a pattern category (A–G from §17): "extracting facts from documents → category A," "same entity, different names → category B," etc. Framed as guidance for choosing among Day 3's pattern kits once they exist — note inline that specific pattern names/links get filled in once `patterns/registry.yaml` exists (Day 3); for now this links to `patterns/README.md` (stubbed Day 1) generically by category.

- [ ] **Step 3: Write `decision-framework.md`**

References (does not duplicate) the six questions from `docs/08-part-6-one-graph-end-to-end/step-14-six-questions-before-you-build.md` — a short intro plus a direct link, framed as "the reference-card version of Step 14" rather than a rewritten copy.

- [ ] **Step 4: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/methods
git commit -m "Add docs/methods: build-a-graph method, pattern picker, decision framework"
```

---

## Task 9: `docs/operating/`

**Files:**
- Create: `docs/operating/anti-patterns.md`
- Create: `docs/operating/failure-modes.md`
- Create: `docs/operating/safety.md`
- Create: `docs/operating/observability.md`

**Interfaces:**
- Consumes: graph-plan.md §16 (anti-patterns: design/governance/judgment categories), §10 (four failure modes, for `failure-modes.md`).
- Produces: `docs/operating/failure-modes.md` and Step 12 (Task 5) cover the same four failure modes at different depth — this page is the compact reference version; Step 12 is the full teaching page. Keep the four names identical between them.

- [ ] **Step 1: Write `anti-patterns.md`**

Three sections exactly matching graph-plan.md §16's three categories: Design anti-patterns (no schema before extraction, silent irreversible merges, edges with no provenance, a subgraph big enough to be the whole graph again, a checker trusting tone over evidence), Governance anti-patterns (a loop grading its own metric with no counter-signal, no anchor to outside reality, no frozen nodes, two loops racing with no arbitration edge), Judgment anti-patterns (building a graph for a spreadsheet's job, treating the fact graph as permanent truth, blurring work-history and fact graphs). Each bullet gets one original sentence of elaboration, not a repeat of the master-plan phrasing.

- [ ] **Step 2: Write `failure-modes.md`**

Compact reference version of Step 12's four failure modes (metric-gaming, blind spot, collision, drift) — table format: failure mode | symptom | fix | linked pattern (leave the pattern-name column as "see `patterns/registry.yaml`, ships Day 3" for now).

- [ ] **Step 3: Write `safety.md`**

Original page on what can go wrong operationally with a shared graph beyond the four governance failure modes: a bad actor (or buggy loop) with write access corrupting shared state, the case for append-only history plus a supersession discipline (linking Step 8) as a safety net, and a short note on access scoping (not every worker needs write access to the whole graph, echoing Step 9's subgraph principle).

- [ ] **Step 4: Write `observability.md`**

Original page: what to actually monitor once a graph is running — growth rate of the fact graph (should be slow and deliberate per §7), how often the grounded checker (Step 10) rejects a claim (a rising rejection rate is itself a signal), how often supersession happens (Step 8) vs. silent correction (which shouldn't happen at all).

- [ ] **Step 5: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/operating
git commit -m "Add docs/operating: anti-patterns, failure-modes, safety, observability"
```

---

## Task 10: `scripts/verify-labs.sh` + Day 2 verification & close-out

**Files:**
- Create: `scripts/verify-labs.sh`
- Modify: `STATE.md` (mark Day 2 row `done`)
- Modify: `loop-run-log.md` (append close-out entry)

**Interfaces:**
- Consumes: every `docs/0N-part-*/labs/*` script from Tasks 1–7 (17 scripts total: 3+2+3+2+3+2+2).
- Produces: the go/no-go signal for the Day 2 approval gate.

- [ ] **Step 1: Write `scripts/verify-labs.sh`**

```bash
#!/usr/bin/env bash
# Discovers and runs every live-lab script under docs/**/labs/, per graph-plan.md §21:
# "runnable via a single ./verify.sh that checks every demo still behaves as documented."
set -uo pipefail
fail=0
for script in docs/*/labs/*; do
  [ -f "$script" ] || continue
  case "$script" in
    *.py) runner="python3" ;;
    *.sh) runner="bash" ;;
    *) echo "SKIP (unknown type): $script"; continue ;;
  esac
  echo "--- running $script ---"
  if $runner "$script"; then
    echo "PASS: $script"
  else
    echo "FAIL: $script"
    fail=1
  fi
done
exit $fail
```

- [ ] **Step 2: Make it executable and run it**

```bash
chmod +x scripts/verify-labs.sh
./scripts/verify-labs.sh
```
Expected: all 17 scripts print `PASS`. Fix any script whose acceptance criteria (defined in its Task above) doesn't hold — do not weaken the criteria to make it pass.

- [ ] **Step 3: Run the originality check across all of Day 2's new content**

```bash
node scripts/originality-check.mjs
```
Expected: `0 violations`. Pay particular attention to the two most collision-prone pairs flagged in Global Constraints: Step 3 vs. `docs/02-foundations/the-two-graphs.md`, and Step 12 vs. `docs/operating/failure-modes.md` (same four failure-mode names are expected to repeat — that's fine, single words/short phrases; only 8+-word verbatim runs are violations).

- [ ] **Step 4: Manually verify no broken relative links**

Check every cross-link added in Tasks 1–9 (Step-to-Step links, Step-to-glossary links, methods-to-Step links, `docs/README.md`'s 17-step table of contents from Day 1 now resolving for real) actually resolves.

- [ ] **Step 5: Update `STATE.md`** — mark the Day 2 row `done`.

- [ ] **Step 6: Append to `loop-run-log.md`**

```markdown
## <date> — Day 2 complete

All 17 step pages, 7 quizzes, 6 flashcard sets (Part 6 has quiz only, per
§23), methods/, operating/, and 17 live-lab scripts written.
originality-check: 0 violations. verify-labs.sh: 17/17 PASS.
Awaiting user approval before day-3-plan.md.
```

- [ ] **Step 7: Commit**

```bash
git add scripts/verify-labs.sh STATE.md loop-run-log.md
git commit -m "Day 2 complete: verify-labs.sh added, all labs passing, STATE.md updated"
```

- [ ] **Step 8: STOP the loop and report to the user.**

---

## Day 2 Approval Gate

**Do not proceed to `day-3-plan.md` until the user has reviewed Day 2's output and explicitly said to proceed.** Flag any originality-check collisions that required a rewrite, and confirm the `docs/**/labs/` colocation choice (noted in Architecture above) is acceptable before Day 3 builds on the same convention for pattern kits.
