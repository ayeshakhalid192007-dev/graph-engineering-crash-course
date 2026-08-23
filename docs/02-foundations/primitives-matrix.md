# Graph Primitives Matrix

A reference table for the three core primitives and how they appear in different contexts.

## Quick Reference

| Primitive | Definition | Examples | When You Use It |
| --- | --- | --- | --- |
| **Node** | Discrete entity or concept | Person, Task, Document, Claim | Representing things |
| **Edge** | Directed relationship | authored, verified, caused | Representing relationships |
| **Property** | Metadata on nodes/edges | timestamp, confidence, status | Adding nuance and evidence |

## Nodes in Different Domains

| Domain | Node Type | Examples | Natural Key |
| --- | --- | --- | --- |
| **Task Management** | Task | Bug #42, Feature PR #99 | task_id |
| | Person | alice@example.com, bob | email or username |
| **Knowledge Graphs** | Claim | "Coffee is a stimulant" | content_hash |
| | Source | paper_id, url | URL or DOI |
| **Code Systems** | File | src/main.py, README.md | filepath |
| | Commit | abc123def456 | commit_hash |
| **Temporal** | Event | "Bug discovered" | timestamp + type |
| | Checkpoint | Day 5 checkpoint | date or milestone |

## Edges in Different Domains

| Domain | Edge Type | Source | Target | Meaning |
| --- | --- | --- | --- | --- |
| **Task Management** | assigned-to | Task | Person | Who owns this? |
| | depends-on | Task | Task | What blocks this? |
| **Knowledge Graphs** | verified-by | Claim | Person | Who checked this? |
| | contradicts | Claim | Claim | What conflicts? |
| **Code Systems** | changed-by | File | Commit | What touched this? |
| | breaks | Commit | Test | What failed? |
| **Temporal** | preceded-by | Event | Event | What came first? |
| | causes | Event | Event | What led to this? |

## Properties: Metadata Examples

### On Nodes

```text
Node: task-42
Properties:
  created_at: 2026-08-15T09:00:00Z      (when)
  created_by: alice@example.com         (who)
  status: in-progress                   (state)
  priority: 3                           (scoring)
  confidence: 0.92                      (uncertainty)
  source: user-input                    (provenance)
```text

### On Edges

```text
Edge: alice --[authored]--> doc-v2
Properties:
  timestamp: 2026-08-22T09:15:00Z       (when)
  confidence: 1.0                       (how sure)
  reason: "Fixed typos"                 (why)
  count: 47                             (how many)
  trace_id: "req-abc-123"               (audit trail)
```text

## Combining Primitives: Common Patterns

### Pattern 1: Timeline (nodes + temporal edges)

```text
Event A
  ↓ preceded-by
Event B
  ↓ preceded-by
Event C
```text

**Use case:** Audit logs, deployment history, state machines

### Pattern 2: Hierarchy (nodes + structural edges)

```text
Organization
  ├─ owns ─→ Team A
  │           ├─ owns ─→ Project 1
  │           └─ owns ─→ Project 2
  └─ owns ─→ Team B
```text

**Use case:** Org structure, file systems, document hierarchy

### Pattern 3: Causation Chain (nodes + causal edges)

```text
Root Cause
  ↓ causes
Intermediate Effect
  ↓ causes
Observable Problem
```text

**Use case:** Incident investigation, bug tracking, root cause analysis

### Pattern 4: Verification Trail (nodes + attributed edges)

```text
Claim
  ← verified-by: Alice (timestamp, confidence)
  ← verified-by: Bob (timestamp, confidence)
  ← contradicted-by: Charlie (timestamp, confidence)
```text

**Use case:** Collaborative fact-checking, scientific citations, compliance audits

### Pattern 5: State Machine (nodes with properties + transitions)

```text
Node: task-42
  status: pending → assigned → in-progress → review → done
  
Edges track the transitions:
  task-42 --[transitioned-to]--> state-in-progress
    timestamp: 2026-08-22T10:00:00Z
    triggered-by: alice@example.com
```text

**Use case:** Workflows, approval processes, task lifecycles

## Scaling the Primitives

| Scale | Challenge | Solution |
| --- | --- | --- |
| **Small (< 1K nodes)** | Simplicity over completeness | Keep 3–5 node types, 5–10 edge types |
| **Medium (1K–1M nodes)** | Query performance | Add indexes, partition by type |
| **Large (1M+ nodes)** | Storage and traversal | Use graph database, implement subgraph queries |

## Design Checklist

When designing a graph, ask:

**Nodes:**

- [ ] What's my natural key? (or should I generate IDs?)
- [ ] How many node types do I actually need? (5–10 is typical)
- [ ] What properties must every node have?
- [ ] What properties are optional but valuable?

**Edges:**

- [ ] What relationships do I actually query? (start there)
- [ ] Do any edges need direction reversals? (if you query both ways)
- [ ] Should I store properties on edges?
- [ ] Are there cycles I need to detect or break?

**Properties:**

- [ ] How will timestamps help me? (created, updated, verified)
- [ ] Do I need confidence or certainty levels?
- [ ] What's my audit trail requirement?
- [ ] Can I defer this property or query it separately?

---

Use this matrix to:

- **Design:** Pick patterns and primitives that match your domain
- **Communicate:** Show stakeholders what data you're modeling
- **Validate:** Check that your choices match your queries
- **Scale:** Recognize when you're hitting primitive limits and need refactoring

