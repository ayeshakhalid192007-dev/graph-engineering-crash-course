# Graph Primitives

Graph engineering is built on a small set of primitives that recur in every system. Understanding these primitives — what they are, how they combine, and when each matters — is the foundation for everything that follows.

## The Three Primitives

### 1. Nodes

A node is a discrete entity or concept in your graph. Every node has:

- **Identity** — a unique identifier (URI, UUID, or natural key)

- **Type** — what kind of thing it is (Person, Task, Claim, etc.)

- **Attributes** — data that describes it

```text
Node: "alice@example.com"
Type: Person
Attributes:
  name: "Alice"
  role: "Engineer"

```

### 2. Edges

An edge is a directed relationship between two nodes. Every edge has:

- **Source** — the node the edge originates from

- **Type** — what kind of relationship it is (knows, caused, verified, etc.)

- **Target** — the node the edge points to

- **Attributes** — metadata about the relationship (timestamp, confidence, etc.)

```text
Edge: alice --[authored]--> task-123
Type: authored
Timestamp: 2026-08-22T09:00:00Z

```

### 3. Properties

Properties are key-value pairs attached to nodes or edges. They store:

- Immutable facts (created_at, node_id)

- Mutable state (status, score, label)

- Evidence (source, confidence, proof)

```text
Node.task-123.properties:
  title: "Fix login bug"
  status: "in-progress"
  priority: 3
  created_by: "alice@example.com"

```

## How Primitives Combine

Most real graphs are built from these three primitives in combination:

- **Two nodes + one edge** = a simple relationship (person knows person)

- **Multiple nodes + multiple edges** = a path (task → subtask → subtask)

- **Cycles** = mutual relationships or recursive structures

- **Properties on edges** = nuanced, timestamped, or scored relationships

## Nodes: Identity and Type

The first decision in any graph is what counts as a node.

### Natural keys vs. generated IDs

**Natural key:** Use the entity's own identity  
Example: email address, filename, username

Pros:

- Human-readable

- Deduplication is natural (same email = same person)

- No lookup table needed

Cons:

- Changes break identity (email changes, file moved)

- Some entities have no natural key

**Generated ID:** Assign a unique identifier  
Example: UUID, auto-increment, hash

Pros:

- Immutable

- Works for any entity

- Fast lookups

Cons:

- Deduplication requires a lookup table

- Less human-readable

### Typing decisions

Every node needs a type. The question is: how specific?

Too broad (everything is `Entity`):

- Loses information

- Queries become expensive

- No semantic meaning

Too narrow (separate types for every variant):

- Explosion of types

- Hard to query across related things

- Maintenance burden

**Middle ground:** Use a small set of types that correspond to how you'll query and reason about the graph.

```text
✓ Good types: Person, Task, Document, Event
✗ Too narrow: Engineer, Manager, Contractor, Consultant
✗ Too broad: Entity, Thing, Object

```

## Edges: Relationship Types

The second decision is what counts as an edge.

Relationship types should reflect:

- **How you'll query:** "Find all tasks assigned to Alice"

- **What you'll constrain:** "A person can only author one version of a document"

- **What you'll measure:** "How many claims did Bob verify?"

### Common edge types in production systems

- **Ownership:** person owns project, project owns task

- **Assignment:** task assigned-to person

- **Causation:** bug caused-by code-change, code-change caused-by task

- **Verification:** claim verified-by person

- **Temporal:** event preceded-by event

- **Structural:** part-of, related-to, supercedes

Start with 5–10 edge types. Add more only when you have queries that need them.

## Properties: Metadata and Evidence

Properties answer the questions that node identity and edge type don't:

**On nodes:**

- When was this created?

- What's its current status?

- How confident are we in it?

**On edges:**

- When did this relationship start?

- Who created it and why?

- How strong is this relationship?

Properties are cheap to add and easy to query, so err on the side of capturing more rather than less.

## From Primitives to Systems

A working graph is these three primitives combined with:

- **A storage layer** (database, file system, memory)

- **Query patterns** (how you traverse the graph)

- **Update patterns** (how you add/change nodes and edges)

- **Consistency rules** (what's allowed and what isn't)

We'll cover each of those next.

---

## Key Takeaway

All graphs — whether you're tracking tasks, claims, code changes, or organizational structure — are made from these three things: nodes (entities), edges (relationships), and properties (metadata). The art is deciding:

1. What counts as a node?

2. What relationships matter?

3. What properties do I need to track?

Get those three decisions right, and the rest follows naturally.
