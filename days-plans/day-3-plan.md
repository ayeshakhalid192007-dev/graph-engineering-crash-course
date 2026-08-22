# Day 3 Implementation Plan — Pattern Library, Projects, Advanced Tier, Certification

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Execution mode:** This project uses **four separate, independent `/loop` instances — one per day — not one loop reused across days and not one combined loop spanning the whole project.** This document governs only Day 3's own dedicated loop, created fresh once the Day 2 approval gate clears — it shares no runtime state with Days 1–2's loops (both already stopped permanently) or with Day 4's loop (not yet created). Task 1 (registry scaffolding) runs first since later tasks populate it. Tasks 2 (starter template), 3–9 (seven core kits), 10 (sixteen extended kits, itself split into four parallel sub-batches), 11–14 (projects, cheatsheets, advanced tier, assessments), and 15 (remaining scripts) are then fanned out to parallel subagents. Task 16 (verification) runs last, sequentially. The loop then **stops permanently** and waits for user approval before Day 4's loop is created — it is never resumed or continued into Day 4.
>
> **Prerequisite:** Day 1 and Day 2 complete and approved. This plan assumes the full 17-step course, `docs/methods/`, `docs/operating/`, and `scripts/originality-check.mjs` + `scripts/verify-labs.sh` already exist and pass.

**Goal:** Ship Deliverable 1 (the complete GitHub learning system) to feature-complete, production-ready status: the pattern library (23 pattern specs, 7 full multi-tool starter kits, 16 single-tool-plus-porting-note kits), 8 practice projects with reference solutions, the advanced/Ultra-Pro tier, assessments, cheatsheets, and the three remaining quality-gate scripts — all four CI gates (link-check, registry-validate, originality-check, graph-ready-audit) green.

**Architecture:** `patterns/<name>.md` holds each pattern's concise spec (what/why/stage/cost); `starters/<name>/` holds the actual runnable kit, in the anatomy defined by graph-plan.md §18. Core kits get the full anatomy in both `.claude/` and `opencode/`; extended kits get one tool directory plus a `PORTING.md`. `patterns/registry.yaml` is the machine-readable index both `scripts/validate-registry.mjs` and `docs/methods/pattern-picker.md` (Day 2) point at.

**Tech Stack:** Markdown, YAML (`registry.yaml`), JSON (`schema.example.json`, `opencode.json.example`), Node.js (remaining scripts), Claude Code `SKILL.md`/agent format, OpenCode config format.

## Global Constraints

- **Originality policy (§2.1)** still applies to every `.md` file — pattern specs, kit READMEs, `PATTERN.md` files, project pages, cheatsheets, advanced-tier pages, assessments. Code/config/schema files (JSON, YAML) are not prose and aren't subject to the 8-word-run check, but any comments or docstrings inside them should still be original.
- **Honesty on scope (§27 Day 3 note):** exactly 7 patterns get full multi-tool kits; the other 16 get a single-tool reference implementation plus a documented porting path — this is not a placeholder, it's the deliberate, disclosed scope for this build window (stated openly in `starters/README.md`, Task 2).
- **Kit anatomy (§18):** `PATTERN.md` (what it does, inputs/outputs, failure mode if skipped) · `README.md` (quickstart) · `schema.example.json` (write-path patterns only) · `.claude/skills/<x>/SKILL.md` + `.claude/agents/graph-verifier.md` · `opencode/opencode.json.example` + `opencode/skills/`.
- **Every worked example in a kit is invented for this course** (§2.1 rule 4), same as the Day 2 step pages — no kit's scenario may be a source's own example re-narrated.
- **Definition of Done for Day 3** (§27 Day 3 + relevant slice of §29): all 23 patterns specced; 7 full kits + 16 single-tool kits with porting notes; `patterns/registry.yaml` validates; 8 projects + solutions; cheatsheets; advanced tier; assessments; all four CI gates green.

---

## Task 1: `patterns/` scaffolding + all 23 pattern specs

**Files:**
- Create: `patterns/README.md`
- Create: `patterns/pattern-template.md`
- Create: `patterns/registry.yaml`
- Create: `patterns/<name>.md` for all 23 patterns listed below

**Interfaces:**
- Consumes: graph-plan.md §17 (full catalog table, categories A–G), §14 (which step each stage maps to, for cross-links).
- Produces: `patterns/registry.yaml` is consumed by Task 15's `validate-registry.mjs` and by Day 2's `docs/methods/pattern-picker.md` (retroactively link-checked in Task 16). Every `starters/<name>/` kit (Tasks 3–10) must have a matching `patterns/<name>.md` entry with identical `name` and `stage`.

- [ ] **Step 1: Write `patterns/pattern-template.md`**

The blank template new pattern authors copy: front-matter fields (`name`, `category`, `stage`, `cost`, `tools`), then sections What it does / Inputs / Outputs / Failure mode if skipped / Link to starter kit.

- [ ] **Step 2: Write `patterns/README.md`**

Index: the catalog table (categories A–G, reproduced from graph-plan.md §17 with the same 23 pattern names — table structure, not source prose, so this is just data, not a §2.1 concern), which 7 are core (full kits) vs. 16 extended, and a link to `CONTRIBUTING.md`'s "how to add a pattern" section (Day 1).

- [ ] **Step 3: Write `patterns/registry.yaml`**

```yaml
patterns:
  - name: document-to-facts
    category: A-extraction
    stage: write
    cost: medium
    core: true
  - name: code-change-to-graph
    category: A-extraction
    stage: write
    cost: medium
    core: false
  - name: conversation-to-claims
    category: A-extraction
    stage: write
    cost: medium
    core: false
  - name: alias-merge-with-trail
    category: B-resolution
    stage: write
    cost: low
    core: true
  - name: confidence-scored-dedup
    category: B-resolution
    stage: write
    cost: medium
    core: false
  - name: reversible-merge-audit
    category: B-resolution
    stage: write
    cost: low
    core: false
  - name: receipt-per-edge
    category: C-provenance
    stage: write
    cost: low
    core: true
  - name: supersession-chain
    category: C-provenance
    stage: write
    cost: low
    core: false
  - name: versioned-schema-log
    category: C-provenance
    stage: write
    cost: low
    core: false
  - name: task-scoped-retrieval
    category: D-subgraph
    stage: read
    cost: low
    core: true
  - name: budget-capped-subgraph
    category: D-subgraph
    stage: read
    cost: low
    core: false
  - name: conflict-aware-bundle
    category: D-subgraph
    stage: read
    cost: medium
    core: false
  - name: grounded-triple-checker
    category: E-checker
    stage: read
    cost: medium
    core: true
  - name: contradiction-detector
    category: E-checker
    stage: read
    cost: medium
    core: false
  - name: early-victory-guard
    category: E-checker
    stage: read
    cost: low
    core: false
  - name: counter-metric-loop
    category: F-governance
    stage: governance
    cost: low
    core: true
  - name: arbitration-edge
    category: F-governance
    stage: governance
    cost: low
    core: false
  - name: audit-loop
    category: F-governance
    stage: governance
    cost: medium
    core: false
  - name: anchor-and-freeze
    category: F-governance
    stage: governance
    cost: low
    core: false
  - name: sqlite-backed-graph
    category: G-storage
    stage: storage
    cost: low
    core: true
  - name: file-graph-for-small-teams
    category: G-storage
    stage: storage
    cost: low
    core: false
  - name: postgres-backed-graph
    category: G-storage
    stage: storage
    cost: medium
    core: false
  - name: neo4j-at-scale
    category: G-storage
    stage: storage
    cost: high
    core: false
```

- [ ] **Step 4: Write all 23 `patterns/<name>.md` spec files**

Each follows `pattern-template.md`'s sections. Use this table as the concrete content source for every spec's "What it does" and "Failure mode if skipped" sections (original one-to-two-sentence elaboration per pattern, not copied between patterns):

| Pattern | What it does (mechanism) | Failure mode if skipped |
| --- | --- | --- |
| `document-to-facts` | Schema-first extraction from a source document into typed entity/relationship nodes (Step 6). | Free-form summaries that can't be queried or checked later. |
| `code-change-to-graph` | Extracts a diff's touched functions/modules as nodes with a `modifies` edge to the changed entity. | No durable record of what a change actually touched, beyond the diff text itself. |
| `conversation-to-claims` | Extracts claims asserted during an agent conversation into provisional fact-graph nodes pending resolution. | Claims made mid-conversation are lost the moment the transcript is discarded. |
| `alias-merge-with-trail` | Merges two surface names for one entity, keeping both original mentions linked (Step 7). | Silent merges that can't be undone if the merge turns out wrong. |
| `confidence-scored-dedup` | Same as above, but scores merge candidates and auto-merges only above a threshold, queuing the rest for review. | Either over-merging (auto-merge everything) or a review backlog no one processes. |
| `reversible-merge-audit` | A periodic job that re-checks past merges against new evidence and can un-merge one. | Merges become permanent even when later evidence contradicts them. |
| `receipt-per-edge` | Every edge stores its source document, extraction run ID, and schema version (Step 8). | A claim with no way to trace why the graph believes it. |
| `supersession-chain` | A claim found wrong gets a new node marked "supersedes" the old one, which is kept, marked stale. | Overwriting a wrong claim in place, destroying the record that it was ever believed. |
| `versioned-schema-log` | Tracks every schema version and which extraction runs used which version. | Silent schema drift where old and new data are incomparable without anyone noticing. |
| `task-scoped-retrieval` | Builds a bounded subgraph of only the nodes/edges relevant to one worker's task (Step 9). | A worker drowning in irrelevant context, or missing the one edge that mattered. |
| `budget-capped-subgraph` | Same as above with a hard node/edge/token budget enforced before handing the subgraph to a worker. | An unbounded subgraph that grows silently expensive as the graph grows. |
| `conflict-aware-bundle` | A subgraph that deliberately keeps contradicting claims visible together rather than picking one. | A worker (or human) never finds out two sources disagree. |
| `grounded-triple-checker` | Decomposes a claim into the specific edges required for it to be true and checks for them (Step 10). | A checker that approves confident-sounding but ungrounded claims. |
| `contradiction-detector` | Scans the fact graph for pairs of edges that can't both be true and flags them. | Contradictions sitting silently in the graph, discovered only by accident. |
| `early-victory-guard` | Blocks a loop from marking a task "done" until the grounded checker has run at least once. | A loop declaring success before anything has actually been verified. |
| `counter-metric-loop` | A second, independent, harder-to-game signal checked by a different party than the optimizing loop (Step 12). | The loop optimizes exactly what it's measured on, including the parts that don't matter. |
| `arbitration-edge` | A rule or third loop that decides who wins when two loops act on the same resource at once. | Two reasonable loops silently overwriting each other's work. |
| `audit-loop` | A separate loop with a wider vantage point that periodically reviews what the main loop can't see from inside its own scope. | An entire class of problem invisible to the loop meant to catch it. |
| `anchor-and-freeze` | At least one signal reaching outside the loop system, plus specific facts/rules no loop may rewrite (Step 13). | A governance graph that is internally consistent and collectively wrong. |
| `sqlite-backed-graph` | Stores nodes/edges as two SQLite tables with foreign keys, good for one team, one machine. | Reaching for a distributed graph database before the scale justifies its operational cost. |
| `file-graph-for-small-teams` | Stores the graph as plain JSON files in a git repo, diffable and reviewable in a PR. | Standing up a database for a graph a handful of JSON files would serve just as well. |
| `postgres-backed-graph` | Adjacency-list tables in Postgres, for a team already running Postgres who needs concurrent multi-writer access. | Multiple writers corrupting a file-based graph with no transaction guarantees. |
| `neo4j-at-scale` | A dedicated graph database for query patterns (multi-hop traversal) that relational adjacency tables handle poorly at scale. | Multi-hop queries becoming prohibitively slow or complex once the graph is large. |

For each pattern, the spec file also states: category (A–G), stage (write/read/governance/storage), cost (low/medium/high) — copied exactly from `registry.yaml` (Step 3) — and a "Kit" line linking to `starters/<name>/README.md` (created Tasks 3–10).

- [ ] **Step 5: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add patterns
git commit -m "Add patterns/ scaffolding: registry, template, and all 23 pattern specs"
```

---

## Task 2: `starters/` scaffolding

**Files:**
- Create: `starters/README.md`
- Create: `starters/_template/PATTERN.md`
- Create: `starters/_template/README.md`
- Create: `starters/_template/schema.example.json`
- Create: `starters/_template/.claude/skills/example-skill/SKILL.md`
- Create: `starters/_template/.claude/agents/graph-verifier.md`
- Create: `starters/_template/opencode/opencode.json.example`
- Create: `starters/_template/opencode/skills/example-skill/SKILL.md`

**Interfaces:**
- Consumes: graph-plan.md §18 (kit anatomy).
- Produces: Tasks 3–10 copy this template's structure for every real kit.

- [ ] **Step 1: Write `starters/README.md`**

Index listing all 23 kits, which 7 are full multi-tool (linking to their dirs) and which 16 are single-tool-plus-porting-note (naming which single tool each uses), and the honest scope note from Global Constraints above, stated plainly for a reader browsing on GitHub.

- [ ] **Step 2: Write the `_template/` scaffold**

`PATTERN.md`: placeholder sections with instructions in HTML comments for a new author (e.g. `<!-- Describe what this pattern does in 2-3 sentences -->`) — this is the one legitimate place in the whole repo for instructional placeholders, since `_template/` is explicitly never-rendered scaffolding for future authors, not shipped course content.
`README.md`: quickstart skeleton (prerequisites, run command, expected output).
`schema.example.json`: a minimal valid example (`{"entities": [], "relationships": []}`) with a comment (via a `"_comment"` key, since JSON has no native comments) explaining its purpose.
`.claude/skills/example-skill/SKILL.md` and `.claude/agents/graph-verifier.md`: minimal valid skill/agent front matter with placeholder instructions.
`opencode/opencode.json.example` and `opencode/skills/example-skill/SKILL.md`: OpenCode equivalents.

- [ ] **Step 3: Commit**

```bash
git add starters/README.md starters/_template
git commit -m "Add starters/ index and _template scaffold"
```

---

## Task 3: Core kit — `document-to-facts`

**Files:** `starters/document-to-facts/{PATTERN.md,README.md,schema.example.json}`, `starters/document-to-facts/.claude/skills/extract-facts/SKILL.md`, `starters/document-to-facts/.claude/agents/graph-verifier.md`, `starters/document-to-facts/opencode/opencode.json.example`, `starters/document-to-facts/opencode/skills/extract-facts/SKILL.md`

**Interfaces:**
- Consumes: Step 6's schema-first extraction concept (Day 2); `patterns/document-to-facts.md` (Task 1).
- Produces: a runnable (by a human following the README, not by CI) worked example a reader can clone and try.

- [ ] **Step 1: Write `PATTERN.md`** — what it does (schema-first document extraction), inputs (a source doc + a schema), outputs (typed entity/relationship JSON), failure mode if skipped (per Task 1's table).
- [ ] **Step 2: Write `README.md`** quickstart: point the skill at a sample doc (include one small original fictional incident-report doc inline or as a sibling `sample-input.md`), run the extraction, inspect the output JSON.
- [ ] **Step 3: Write `schema.example.json`** — a concrete schema for the incident-report scenario: entity types `Service`, `Incident`, `Cause`; relationship types `caused-by`, `affected`.
- [ ] **Step 4: Write `.claude/skills/extract-facts/SKILL.md`** — a real Claude Code skill: instructs the model to read the input doc and the schema, and emit JSON strictly matching the schema's entity/relationship types, rejecting anything outside them.
- [ ] **Step 5: Write `.claude/agents/graph-verifier.md`** — a subagent definition that checks the extracted JSON against `schema.example.json` and flags any entity/relationship type not in the schema.
- [ ] **Step 6: Write `opencode/opencode.json.example` and `opencode/skills/extract-facts/SKILL.md`** — OpenCode equivalents of Steps 4–5's behavior.
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/document-to-facts
git commit -m "Add core kit: document-to-facts"
```

---

## Task 4: Core kit — `alias-merge-with-trail`

**Files:** same anatomy as Task 3, under `starters/alias-merge-with-trail/`, skill name `merge-aliases`.

- [ ] **Step 1–6:** Same structure as Task 3, scenario: merging "the payments service" and "billing-svc" (Step 7's example) into one node while keeping both original mentions linked and queryable — `schema.example.json` models `{"entities": [...], "aliases": [{"canonical": "...", "mentions": [...]}]}`.
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/alias-merge-with-trail
git commit -m "Add core kit: alias-merge-with-trail"
```

---

## Task 5: Core kit — `receipt-per-edge`

**Files:** same anatomy under `starters/receipt-per-edge/`, skill name `attach-receipts`.

- [ ] **Step 1–6:** Scenario: the schema-v1/v2 supersession example from Step 8 — every edge in `schema.example.json` carries `source_doc`, `extraction_run_id`, `schema_version` fields; the skill refuses to write an edge missing any of the three.
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/receipt-per-edge
git commit -m "Add core kit: receipt-per-edge"
```

---

## Task 6: Core kit — `task-scoped-retrieval`

**Files:** same anatomy under `starters/task-scoped-retrieval/`, skill name `build-subgraph`. No `schema.example.json` required (this is a read-path pattern, per Global Constraints) — instead include `sample-graph.example.json` (a small fixed graph to query against).

- [ ] **Step 1–6:** Scenario: the Step 9 example (a worker fixing one function gets only its direct dependencies plus any conflicting claims) — the skill takes a target node and a depth, returns the bounded subgraph.
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/task-scoped-retrieval
git commit -m "Add core kit: task-scoped-retrieval"
```

---

## Task 7: Core kit — `grounded-triple-checker`

**Files:** same anatomy under `starters/grounded-triple-checker/`, skill name `check-claim`, `sample-graph.example.json` (same read-path exception as Task 6).

- [ ] **Step 1–6:** Scenario: the Step 10 example ("this PR doesn't touch the auth path") — the skill decomposes the claim, checks for the specific edge's absence/presence, and rejects a fabricated claim where the edge is present.
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/grounded-triple-checker
git commit -m "Add core kit: grounded-triple-checker"
```

---

## Task 8: Core kit — `counter-metric-loop`

**Files:** same anatomy under `starters/counter-metric-loop/`, skill name `counter-metric-check`, plus `.claude/agents/graph-verifier.md` repurposed here as the independent counter-metric checker (governance pattern, not a write/read pattern — no `schema.example.json`; include `governance-graph.example.json` instead, modeling the loop-nodes-and-edges structure from Step 11).

- [ ] **Step 1–6:** Scenario: the Step 12 metric-gaming example — a main loop optimizing a single count, and this kit's independent counter-metric loop catching it, exactly mirroring the `step-12-four-failure-modes.py` live lab from Day 2 but as a real dual-tool kit rather than a plain script.
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/counter-metric-loop
git commit -m "Add core kit: counter-metric-loop"
```

---

## Task 9: Core kit — `sqlite-backed-graph`

**Files:** `starters/sqlite-backed-graph/{PATTERN.md,README.md,schema.example.json,schema.sql}`, `.claude/skills/query-graph/SKILL.md`, `.claude/agents/graph-verifier.md`, `opencode/opencode.json.example`, `opencode/skills/query-graph/SKILL.md`.

- [ ] **Step 1: Write `schema.sql`** — two tables, `nodes(id, type, data)` and `edges(id, from_id, to_id, label, source_doc, extraction_run_id, schema_version)` (the last three columns dogfooding `receipt-per-edge`'s provenance fields), with foreign keys from `edges` to `nodes`.
- [ ] **Step 2–6:** Same anatomy as prior tasks; skill queries the SQLite-backed graph for a small worked example (reuse the five-service dependency scenario from Step 15, Day 2, since it's already small and self-contained).
- [ ] **Step 7: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/sqlite-backed-graph
git commit -m "Add core kit: sqlite-backed-graph"
```

---

## Task 10: Sixteen extended kits (single-tool + porting note)

**Files:** for each of the 16 extended patterns listed in Task 1 Step 3's registry (`code-change-to-graph`, `conversation-to-claims`, `confidence-scored-dedup`, `reversible-merge-audit`, `supersession-chain`, `versioned-schema-log`, `budget-capped-subgraph`, `conflict-aware-bundle`, `contradiction-detector`, `early-victory-guard`, `arbitration-edge`, `audit-loop`, `anchor-and-freeze`, `file-graph-for-small-teams`, `postgres-backed-graph`, `neo4j-at-scale`):
`starters/<name>/{PATTERN.md,README.md,PORTING.md}` + **one** tool directory (`.claude/skills/<skill-name>/SKILL.md` — Claude Code is the single tool chosen for all 16, for consistency; note this choice explicitly in `starters/README.md`, Task 2).

**Interfaces:**
- Consumes: each pattern's row in Task 1's mechanism table.
- Produces: nothing consumed later, but every kit must still pass the originality check and link-check.

**Parallelization:** split into four subagent batches of four patterns each (matching graph-plan.md's category grouping so each subagent stays inside one conceptual area):
- Batch A: `code-change-to-graph`, `conversation-to-claims`, `confidence-scored-dedup`, `reversible-merge-audit`
- Batch B: `supersession-chain`, `versioned-schema-log`, `budget-capped-subgraph`, `conflict-aware-bundle`
- Batch C: `contradiction-detector`, `early-victory-guard`, `arbitration-edge`, `audit-loop`
- Batch D: `anchor-and-freeze`, `file-graph-for-small-teams`, `postgres-backed-graph`, `neo4j-at-scale`

- [ ] **Step 1 (per pattern in each batch): Write `PATTERN.md` and `README.md`** using that pattern's row from Task 1 Step 4's table for the "what it does" / "failure mode" content, plus a short original one-paragraph worked scenario distinct from every other kit's scenario (including the 7 core kits').
- [ ] **Step 2 (per pattern): Write the single `.claude/skills/<skill-name>/SKILL.md`** implementing that pattern's mechanism concretely (not a stub — real instructions a model could follow), skill name derived from the pattern (e.g. `code-change-to-graph` → skill `diff-to-graph`).
- [ ] **Step 3 (per pattern): Write `PORTING.md`** — concrete notes on what would need to change to run this in OpenCode instead: the OpenCode config file location (`opencode.json` vs Claude Code's `.claude/` layout), how OpenCode's skill-invocation model differs, and any tool-call syntax the `SKILL.md` currently assumes that would need translating.
- [ ] **Step 4 (per batch): Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add starters/<pattern-1> starters/<pattern-2> starters/<pattern-3> starters/<pattern-4>
git commit -m "Add extended kits (batch <A|B|C|D>): single-tool reference + porting notes"
```

---

## Task 11: `docs/projects/` — 8 projects + solutions

**Files:**
- Create: `docs/projects/README.md`
- Create: `docs/projects/01-nodes-and-edges-by-hand.md`
- Create: `docs/projects/02-the-ratchet.md`
- Create: `docs/projects/03-extract-your-first-ten-facts.md`
- Create: `docs/projects/04-merge-without-losing-the-trail.md`
- Create: `docs/projects/05-give-every-edge-a-receipt.md`
- Create: `docs/projects/06-feed-a-worker-a-subgraph.md`
- Create: `docs/projects/07-catch-a-lie-with-a-checker.md`
- Create: `docs/projects/08-wire-two-loops-together-capstone.md`
- Create: `docs/projects/solutions/01-*.md` … `08-*.md` (matching filenames, `solutions/` prefix)

**Interfaces:**
- Consumes: graph-plan.md §20 (the 8 project one-liners), the corresponding Day 2 step pages (each project maps to specific steps — see mapping below), the "throwaway repo, small data first" banner requirement.
- Produces: nothing consumed later, but Task 16's link-check must confirm every project page links to its reference solution.

- [ ] **Step 1: Write `docs/projects/README.md`** — index table: project | difficulty | time | concepts | maps to which step(s).
- [ ] **Step 2: Write each of the 8 project pages**, each with: difficulty, time estimate, concepts used, "done when" criteria, and the throwaway-repo/small-data-first banner. Map each to its step(s) and give each a distinct original scenario (none reusing a Day 2 step's or another project's scenario verbatim):

| # | Project | Maps to | Original scenario |
| - | ------- | -------- | ------------------ |
| 1 | Nodes and edges by hand | Step 2 | Model one fact about a personal reading list (book → written-by → author) as plain JSON, no code. |
| 2 | The ratchet | Step 4 | A script ratcheting forward only improving attempts at tuning a toy recommendation score. |
| 3 | Extract your first ten facts | Step 6 | Schema-first extraction from a (provided, original) sample product-changelog document. |
| 4 | Merge without losing the trail | Step 7 | Reversible resolution on deliberately messy customer-name data (typos, nicknames, abbreviations). |
| 5 | Give every edge a receipt | Step 8 | Retrofitting provenance fields onto an existing toy graph provided as starting material. |
| 6 | Feed a worker a subgraph, not the graph | Step 9 | Bounded context construction for one task inside a small fictional ticket-routing graph. |
| 7 | Catch a lie with a checker | Step 10 | A grounded checker correctly rejecting an ungrounded claim about a fictional deployment. |
| 8 | Wire two loops together (capstone) | Steps 11–13 | A producer loop and a checker loop sharing one graph, with one real governance edge (an arbitration edge, reusing the `arbitration-edge` extended kit's mechanism as the concrete implementation). |

- [ ] **Step 3: Write each of the 8 reference solutions** in `docs/projects/solutions/` — a worked-through solution to that project's own scenario (not a different scenario), showing the expected output/graph state.
- [ ] **Step 4: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/projects
git commit -m "Add docs/projects: 8 practice projects with reference solutions"
```

---

## Task 12: `docs/appendix/cheatsheets/`

**Files:** `docs/appendix/cheatsheets/{claude-code.md,opencode.md,mcp.md}`

- [ ] **Step 1: Write `claude-code.md`** — quick-reference for the Claude Code patterns used across this course: `SKILL.md` shape, subagent definitions, the specific commands used in the dual-tool code tabs (Steps 1–17) and the pattern kits, collected in one scannable page.
- [ ] **Step 2: Write `opencode.md`** — same, for OpenCode's config/skill shape.
- [ ] **Step 3: Write `mcp.md`** — a short original page on where MCP fits relative to this course's patterns (e.g., a graph store exposed as an MCP resource/tool is one way to implement the storage-category patterns from G) — scoped, not a full MCP tutorial.
- [ ] **Step 4: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/appendix
git commit -m "Add docs/appendix/cheatsheets: claude-code, opencode, mcp"
```

---

## Task 13: `docs/advanced/` — Ultra-Pro tier

**Files:** `docs/advanced/{graphs-at-scale.md,multi-graph-federation.md,governance-at-org-scale.md}`

**Interfaces:**
- Consumes: graph-plan.md §12.1 (G4 · Ultra-Pro track description: "decide when not to build one; run graphs at scale; author new patterns").

- [ ] **Step 1: Write `graphs-at-scale.md`** — full §12 template. Original treatment of what changes once a graph outgrows `sqlite-backed-graph` (Task 9) — query patterns that need real multi-hop traversal, when `postgres-backed-graph` or `neo4j-at-scale` (Task 10) actually earn their cost.
- [ ] **Step 2: Write `multi-graph-federation.md`** — full §12 template. Original treatment of running several teams' graphs that need to interoperate without merging into one — a federation scenario invented for this course (e.g. two teams' fact graphs cross-referencing a shared entity without a full merge).
- [ ] **Step 3: Write `governance-at-org-scale.md`** — full §12 template. Extends Step 11–13's governance graph to many teams' loops, not just one team's — an original scenario of an org with several independently-run governance graphs needing a top-level arbitration policy.
- [ ] **Step 4: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/advanced
git commit -m "Add docs/advanced: Ultra-Pro tier (graphs at scale, federation, org governance)"
```

---

## Task 14: `docs/assessments/`

**Files:** `docs/assessments/{final-exam.md,capstone-rubric.md,graph-ready-certification.md}`

- [ ] **Step 1: Write `final-exam.md`** — original questions spanning all 17 steps (at least one question per step, 17+ questions total), mixed format (short answer + "spot the anti-pattern" using `docs/operating/anti-patterns.md`'s categories), answer key at the bottom behind a `<details>` fold.
- [ ] **Step 2: Write `capstone-rubric.md`** — grading rubric for Project 8 (the capstone): criteria drawn from the Graph Ready checklist (graph-plan.md §19) plus "has a real arbitration edge, not just a comment saying one exists."
- [ ] **Step 3: Write `graph-ready-certification.md`** — the certification page: the exact seven-item Graph Ready checklist from §19 (schema before extraction · reversible resolution · every edge has provenance · a subgraph budget is set · a grounded checker exists · at least one anchor · at least one frozen node), how to self-certify, and a pointer to the website's `CertificateGenerator` component (Day 4) for the interactive version.
- [ ] **Step 4: Run originality check and commit**

```bash
node scripts/originality-check.mjs
git add docs/assessments
git commit -m "Add docs/assessments: final exam, capstone rubric, certification"
```

---

## Task 15: Remaining scripts — `link-check.mjs`, `validate-registry.mjs`, `graph-ready-audit.mjs`

**Files:**
- Create: `scripts/link-check.mjs`
- Create: `scripts/validate-registry.mjs`
- Create: `scripts/graph-ready-audit.mjs`
- Modify: `.github/workflows/link-check.yml`, `registry-validate.yml`, `graph-ready-audit.yml` (remove the Day 1 existence guards now that the scripts exist)

- [ ] **Step 1: Write `scripts/link-check.mjs`**

```javascript
#!/usr/bin/env node
// Fails if any relative markdown link in docs/, patterns/, starters/, resources/,
// or the root-level .md files points at a file that doesn't exist.
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, extname, dirname, resolve } from "node:path";

const ROOTS = ["docs", "patterns", "starters", "resources", "."];
const LINK_RE = /\[[^\]]*\]\((\.{1,2}\/[^)#\s]+|[^)#\s:]+\.md)(#[^)]*)?\)/g;

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (entry === "node_modules" || entry === ".git" || entry === "web") continue;
    const p = join(dir, entry);
    const s = statSync(p);
    if (s.isDirectory()) walk(p, out);
    else if (extname(p) === ".md") out.push(p);
  }
  return out;
}

function main() {
  const files = new Set();
  for (const root of ROOTS) {
    if (!existsSync(root)) continue;
    if (statSync(root).isDirectory()) walk(root).forEach((f) => files.add(f));
    else if (extname(root) === ".md") files.add(root);
  }

  let broken = 0;
  for (const file of files) {
    const text = readFileSync(file, "utf8");
    let match;
    while ((match = LINK_RE.exec(text)) !== null) {
      const target = match[1];
      if (target.startsWith("http")) continue;
      const resolved = resolve(dirname(file), target);
      if (!existsSync(resolved)) {
        console.error(`broken link in ${file}: "${target}" -> ${resolved}`);
        broken++;
      }
    }
  }

  if (broken > 0) {
    console.error(`\nlink-check: ${broken} broken link(s) found.`);
    process.exit(1);
  }
  console.log(`link-check: ${files.size} files checked, 0 broken links.`);
}

main();
```

- [ ] **Step 2: Write `scripts/validate-registry.mjs`**

```javascript
#!/usr/bin/env node
// Validates patterns/registry.yaml against the pattern spec files and starter kits.
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { parse } from "node:module"; // placeholder import removed below
```

Actually implement without a YAML dependency (repo has no `package.json` yet at root — avoid introducing one just for this script): write a minimal YAML-list parser sufficient for this file's flat structure (this registry is a simple list of flat key/value maps, not general YAML), or store the registry as `registry.json` instead of `.yaml` for zero-dependency validation. **Flagging this as a Day 3 judgment call:** graph-plan.md §23 names the file `registry.yaml` explicitly, so keep the `.yaml` extension and filename, but parse it with a small hand-rolled parser scoped to exactly this file's shape (a top-level `patterns:` list of flat maps with string/bool scalar values) rather than pulling in a YAML library — document this scoping limitation in a comment at the top of the script.

```javascript
#!/usr/bin/env node
import { readFileSync, existsSync } from "node:fs";

function parseFlatYamlList(text) {
  const lines = text.split("\n");
  const items = [];
  let current = null;
  for (const line of lines) {
    if (/^\s*-\s+name:/.test(line)) {
      if (current) items.push(current);
      current = {};
    }
    const m = line.match(/^\s*(\w+):\s*(.+)\s*$/);
    if (m && current) {
      const [, key, rawVal] = m;
      current[key.replace(/^-\s*/, "")] = rawVal === "true" ? true : rawVal === "false" ? false : rawVal;
    }
  }
  if (current) items.push(current);
  return items;
}

function main() {
  const registryPath = "patterns/registry.yaml";
  if (!existsSync(registryPath)) {
    console.error("validate-registry: patterns/registry.yaml not found");
    process.exit(1);
  }
  const entries = parseFlatYamlList(readFileSync(registryPath, "utf8"));
  let errors = 0;

  for (const entry of entries) {
    const specPath = `patterns/${entry.name}.md`;
    const kitPath = `starters/${entry.name}/PATTERN.md`;
    if (!existsSync(specPath)) {
      console.error(`registry entry "${entry.name}" has no spec at ${specPath}`);
      errors++;
    }
    if (!existsSync(kitPath)) {
      console.error(`registry entry "${entry.name}" has no starter kit at ${kitPath}`);
      errors++;
    }
    if (entry.core === true && !existsSync(`starters/${entry.name}/opencode/opencode.json.example`)) {
      console.error(`registry entry "${entry.name}" is marked core but has no opencode/ directory`);
      errors++;
    }
  }

  if (errors > 0) {
    console.error(`\nvalidate-registry: ${errors} error(s) found.`);
    process.exit(1);
  }
  console.log(`validate-registry: ${entries.length} patterns validated, 0 errors.`);
}

main();
```

- [ ] **Step 3: Write `scripts/graph-ready-audit.mjs`**

```javascript
#!/usr/bin/env node
// Checks every starter kit satisfies the Graph Ready checklist shape (§19):
// this is a structural proxy check (files exist, required sections present),
// not a semantic check that the kit's logic is correct — that's covered by
// each kit's own README quickstart being manually runnable.
import { readFileSync, existsSync, readdirSync } from "node:fs";

const CHECKLIST_SECTIONS = [
  "What it does",
  "Failure mode if skipped",
];

function main() {
  const kits = readdirSync("starters").filter(
    (d) => d !== "_template" && d !== "README.md" && existsSync(`starters/${d}/PATTERN.md`)
  );
  let violations = 0;

  for (const kit of kits) {
    const patternMd = readFileSync(`starters/${kit}/PATTERN.md`, "utf8");
    for (const section of CHECKLIST_SECTIONS) {
      if (!patternMd.includes(section)) {
        console.error(`${kit}: PATTERN.md missing required section "${section}"`);
        violations++;
      }
    }
    if (!existsSync(`starters/${kit}/README.md`)) {
      console.error(`${kit}: missing README.md`);
      violations++;
    }
  }

  if (violations > 0) {
    console.error(`\ngraph-ready-audit: ${violations} violation(s) found.`);
    process.exit(1);
  }
  console.log(`graph-ready-audit: ${kits.length} kits audited, 0 violations.`);
}

main();
```

- [ ] **Step 4: Remove the Day 1 existence guards** in the three corresponding workflow files (they can now call the scripts unconditionally).
- [ ] **Step 5: Run all three scripts locally and confirm green**

```bash
node scripts/link-check.mjs
node scripts/validate-registry.mjs
node scripts/graph-ready-audit.mjs
```

- [ ] **Step 6: Commit**

```bash
git add scripts .github/workflows/link-check.yml .github/workflows/registry-validate.yml .github/workflows/graph-ready-audit.yml
git commit -m "Add link-check, validate-registry, graph-ready-audit scripts and un-guard their workflows"
```

---

## Task 16: Day 3 verification & close-out

**Files:** Modify `STATE.md`, `loop-run-log.md`.

- [ ] **Step 1: Run all four CI-gate scripts locally**

```bash
node scripts/originality-check.mjs
node scripts/link-check.mjs
node scripts/validate-registry.mjs
node scripts/graph-ready-audit.mjs
```
All four must exit 0.

- [ ] **Step 2: Spot-check that every one of the 23 patterns in `registry.yaml` has both a spec and a kit**, and that exactly 7 are marked `core: true` (matching Task 1's list).

- [ ] **Step 3: Update `STATE.md`** — mark Day 3 row `done`.

- [ ] **Step 4: Append to `loop-run-log.md`**

```markdown
## <date> — Day 3 complete

Pattern library complete: 23 specs, 7 full multi-tool core kits, 16
single-tool + porting-note extended kits. 8 projects + solutions,
cheatsheets, advanced tier, assessments written. All four CI gates
(originality, link-check, registry-validate, graph-ready-audit) green.
Deliverable 1 is feature-complete. Awaiting user approval before day-4-plan.md.
```

- [ ] **Step 5: Commit**

```bash
git add STATE.md loop-run-log.md
git commit -m "Day 3 complete: Deliverable 1 feature-complete, all CI gates green"
```

- [ ] **Step 6: STOP Day 3's loop permanently and report to the user.** Per the "separate loop per day" execution mode: this loop ends here — it is not paused or resumed later. Starting Day 4 means **creating a brand-new, separate `/loop` scoped to `day-4-plan.md`**, not reawakening this one.

---

## Day 3 Approval Gate

**Do not create Day 4's loop until the user has reviewed Day 3's output and explicitly said to proceed.** Flag the two judgment calls made this day for explicit sign-off: (1) all 16 extended kits use Claude Code as the single reference tool (not a mix), and (2) `registry.yaml` is validated with a hand-rolled scoped parser rather than a YAML library dependency. Once cleared, Day 4 starts as its **own independent `/loop`** — a fresh instance, not this one continuing.
