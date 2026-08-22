# The Four Layers of Graph Systems

Graph engineering works in four distinct layers. Each layer has its own concerns, patterns, and failure modes. Understanding how they stack is key to building systems that scale.

## Layer 1: Primitives (Data Model)

**What it is:** Nodes, edges, and properties—the raw stuff of your graph.

**Decisions you make:**

- What counts as a node? (natural key vs. generated ID)

- What relationships matter? (which edges to store)

- What properties do you need? (metadata, confidence, provenance)

**When it breaks:**

- Your node type ontology is wrong (too broad or too narrow)

- You didn't model an edge type you actually query

- Missing properties force expensive recomputation

**Example:**

```
Nodes: Person, Task, Document
Edges: authored, verified, depends-on
Properties: created_at, confidence, source

```

---

## Layer 2: Storage (Persistence)

**What it is:** Where and how the graph actually lives—database, file system, cache, or in-memory.

**Decisions you make:**

- Database choice (graph DB, SQL, document store, flat files)

- Indexing strategy (what queries should be fast?)

- Partitioning (how to split large graphs?)

- Replication (how many copies, where?)

**When it breaks:**

- Query patterns change and your indexes don't match

- The graph grows and your storage can't handle it

- Consistency requirements conflict with availability

- Updates are too slow or too frequent for your storage

**Example:**

```

Storage: Neo4j
Indexes: (Person, email), (Task, created_at)
Partitions: By year for time-series data
Replication: 3-node cluster for redundancy

```

---

## Layer 3: Query Patterns (Access)

**What it is:** How you traverse the graph to answer questions.

**Decisions you make:**

- What queries must be fast? (traversal depth, result size)

- How deep do you traverse? (2 hops vs. 10 hops?)

- How do you filter? (by property, by type, by relationship strength?)

- Do you need aggregations? (count verified claims, sum priorities?)

**When it breaks:**

- A new use case requires a query you didn't optimize for

- Traversals are slow (query hits millions of nodes)

- You can't express business logic in your query language

- Result sets are too large to process

**Example:**

```

Fast queries: "Give me all tasks assigned to Alice"
Slow queries: "Find all 5-hop paths in the task graph"
Filters: status = "in-progress" AND priority > 2
Aggregation: COUNT verified claims grouped by source

```

---

## Layer 4: Update Patterns (Write Logic)

**What it is:** How you add, modify, and delete nodes and edges while maintaining consistency.

**Decisions you make:**

- When do you insert vs. update? (append-only or mutable?)

- How do you handle conflicts? (last-write-wins, merge, reject?)

- Do you need version history? (audit trail, rollback?)

- What consistency guarantees do you need? (immediate or eventual?)

**When it breaks:**

- Two writers create conflicting nodes/edges (deduplication fails)

- Updates are lost because of race conditions

- You can't roll back a bad write

- Consistency checks are too expensive

**Example:**

```

Insert: Create new task node once per task
Update: Modify task properties (append timestamp, track changes)
Conflict handling: If two people edit simultaneously, keep latest
Consistency: Within single graph, no dangling edges

```

---

## How the Layers Stack

```

┌─────────────────────────────────────┐
│ Layer 4: Update Patterns            │ How you change the graph
├─────────────────────────────────────┤
│ Layer 3: Query Patterns             │ How you read from the graph
├─────────────────────────────────────┤
│ Layer 2: Storage                    │ Where the graph lives
├─────────────────────────────────────┤
│ Layer 1: Primitives (Data Model)    │ Nodes, edges, properties
└─────────────────────────────────────┘

```

Each layer depends on the one below it:

- Your **query patterns** must work with your **storage**

- Your **update patterns** must preserve your **primitives**

- Your **data model** dictates what **queries** are even possible

---

## Example: Task Management Graph

### Layer 1: Primitives

```

Nodes: Task, Person, Project
Edges: assigned-to, depends-on, belongs-to
Properties: status, priority, created_at, assigned_by

```

### Layer 2: Storage

```

Database: PostgreSQL with JSON edges
Indexes: (Task, project_id), (Person, email)
Partitioning: By project_id for horizontal scaling
Replication: Read replicas for reporting

```

### Layer 3: Query Patterns

```

Fast: "All tasks assigned to Alice in project X"
Slow: "Find all 5-hop dependency chains"
Filter: status = 'in-progress' AND priority > 2
Aggregation: COUNT tasks grouped by assignee

```

### Layer 4: Update Patterns

```

Insert: New task gets unique ID, immutable created_at
Update: Task.status changes trigger timestamp update
Conflict: If two edits happen simultaneously, last-write-wins
Consistency: No dangling task.assigned_to references

```

---

## Design Trade-offs by Layer

### Layer 1: Primitives

- **Fewer node types** (fast queries, simple schema) vs. **more types** (richer semantics)

- **Natural keys** (deduplication is natural) vs. **generated IDs** (immutable, lookup-heavy)

- **Dense properties** (rich metadata) vs. **sparse properties** (lean schema)

### Layer 2: Storage

- **Graph database** (fast traversals) vs. **SQL** (flexible, familiar)

- **Append-only** (natural history, large storage) vs. **mutable** (small storage, complex updates)

- **Single copy** (simple, fast writes) vs. **replicated** (resilient, slower writes)

### Layer 3: Query Patterns

- **Deep traversals** (rich answers) vs. **shallow traversals** (fast queries)

- **Complex filters** (precise results) vs. **simple filters** (easy to cache)

- **Real-time** (fresh data) vs. **eventual consistency** (fast reads)

### Layer 4: Update Patterns

- **Immediate consistency** (no conflicts, slow writes) vs. **eventual consistency** (fast writes, merge conflicts)

- **Append-only** (perfect audit trail) vs. **mutable** (flexible, no history)

- **Strict validation** (no invalid states) vs. **permissive** (fast ingestion, validate later)

---

## When to Revisit Each Layer

**Layer 1 (Primitives):** When business logic changes, when you discover a missing query
**Layer 2 (Storage):** When queries slow down, when data grows, when consistency requirements change
**Layer 3 (Query Patterns):** When use cases expand, when new stakeholders need access
**Layer 4 (Update Patterns):** When conflicts emerge, when audit requirements change, when consistency matters more

---

## Key Takeaway

A working graph system is not just a collection of nodes and edges. It's primitives + storage + queries + updates working together. Get one layer wrong, and the whole system breaks.

- Bad primitives → queries are slow or impossible

- Bad storage → queries are correct but too slow

- Bad query patterns → system works, but you're asking wrong questions

- Bad update logic → data gets corrupted or conflicts

Master each layer, and you'll know exactly where to look when something goes wrong.
