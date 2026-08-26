# Graph Design Checklist

Use this checklist before you start building a graph system. It covers the four layers and helps you make intentional choices.

## Pre-Build Phase

### 1. Problem Definition
- [ ] What problem are you solving? (state it in one sentence)
- [ ] Who are the stakeholders? (who needs to query this?)
- [ ] What decisions will this graph inform?
- [ ] What are the success metrics?

### 2. Data Model (Layer 1)
- [ ] What are the core entities? (nodes)
- [ ] What relationships matter? (edges)
- [ ] How will you identify each node? (natural key or generated ID?)
- [ ] What metadata must you track? (properties)
- [ ] Are there cycles? (if yes, how will you handle them?)

### 3. Storage Choice (Layer 2)
- [ ] How big will this graph be? (rough size estimate)
- [ ] How fast does data need to be? (real-time, hourly, daily?)
- [ ] Do you need history? (immutable log or mutable store?)
- [ ] Who owns the data? (single team, shared, distributed?)
- [ ] Database choice: Graph DB / SQL / Document Store / Files?

### 4. Query Patterns (Layer 3)
- [ ] What are your top 3 queries? (rank by frequency)
- [ ] How deep do traversals go? (1 hop? 5 hops? variable?)
- [ ] What filters do you need? (by type, property, relationship strength?)
- [ ] Do you need aggregations? (counts, sums, averages?)
- [ ] How fresh does data need to be? (real-time or eventual?)

### 5. Update Patterns (Layer 4)
- [ ] How often do nodes/edges change? (per-minute, per-hour, per-day?)
- [ ] Can writes conflict? (will two writes ever try to change the same thing?)
- [ ] Do you need rollback? (undo capability?)
- [ ] What consistency guarantees do you need?
- [ ] Who can write? (one source or multiple?)

---

## Build Phase

### 6. Implementation
- [ ] Implement Layer 1: Create node/edge types and properties
- [ ] Implement Layer 2: Set up storage with necessary indexes
- [ ] Implement Layer 3: Build query layer for your top 3 queries
- [ ] Implement Layer 4: Build write/update logic with conflict handling
- [ ] Add validation: Check that data model matches reality

### 7. Testing
- [ ] Test Layer 1: Can you create and retrieve all node types?
- [ ] Test Layer 2: Are queries fast? (benchmark against targets)
- [ ] Test Layer 3: Do your queries return correct results?
- [ ] Test Layer 4: Can you handle concurrent writes?
- [ ] Negative tests: What breaks if you violate assumptions?

### 8. Deployment
- [ ] Data migration: How do you get existing data into the graph?
- [ ] Rollback plan: How do you revert if it fails?
- [ ] Monitoring: What metrics tell you it's working?
- [ ] Documentation: Can someone else understand this?
- [ ] Runbook: What do you do when it breaks?

---

## Post-Launch Phase

### 9. Validation
- [ ] Are queries actually fast? (measure real performance)
- [ ] Is the data consistent? (spot-check for corruption)
- [ ] Do new queries fit the model? (or do you need to expand?)
- [ ] Are there bottlenecks? (what's slowest?)

### 10. Iteration
- [ ] What queries are slowing you down?
- [ ] What data model changes would help?
- [ ] Do you need new node or edge types?
- [ ] Should you change storage or indexing strategy?

---

## Red Flags (Stop and Reconsider)

- [ ] You don't know your top 3 queries
- [ ] Your data model has > 20 node types
- [ ] Your queries traverse > 10 hops
- [ ] Updates are happening faster than you can write them
- [ ] You need real-time consistency but your storage is eventual
- [ ] Multiple teams own pieces of the graph without governance
- [ ] You're denormalizing the same data across multiple nodes (suggests wrong model)

---

## Success Criteria

Your graph system is working when:

- ✓ Your top 3 queries run in < 100ms
- ✓ Data is consistent (no orphaned edges, no stale caches)
- ✓ New stakeholders can understand the model in < 30 minutes
- ✓ Adding a new query doesn't require schema changes
- ✓ You can answer "Why is this edge here?" (provenance)
- ✓ You can roll back a bad write
- ✓ Monitoring alerts you before problems affect users

