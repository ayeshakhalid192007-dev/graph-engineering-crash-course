# Operating Graphs in Production

This section covers what happens after you've built your graph and deployed it to production. The concerns here are different from building—instead of correctness, you're optimizing for resilience, observability, and cost.

## The Operating Reality

A graph that works in development often breaks in production because:

1. **Data grows** — Your indexing strategy that worked for 10K nodes doesn't work for 10M nodes
2. **Query patterns change** — Stakeholders discover new questions your schema doesn't support well
3. **Writes conflict** — Multiple sources try to update the same node simultaneously
4. **Infrastructure fails** — Databases crash, networks partition, disks fill up
5. **Costs explode** — Graph traversals are more expensive than you budgeted for

This section helps you handle all five.

## What's Covered

- **Anti-patterns** — Common mistakes that break production graphs
- **Failure modes** — What can go wrong and how to detect it early
- **Observability** — What metrics you need to monitor
- **Safety** — How to make breaking changes without losing data
- **Recovery playbook** — What to do when something breaks

## Quick Navigation

**I'm experiencing:**
- [Slow queries](#) → Check indexing strategy in Storage layer
- [Data inconsistency](#) → Check write validation in Updates layer
- [Disk space blowing up](#) → Consider partitioning or archive strategy
- [High costs](#) → Profile your most expensive queries
- [Replication lag](#) → Check network and replica configuration

**I want to:**
- [Add a new query type](#) → Expect query layer changes, possibly storage changes
- [Change the data model](#) → Expect migration, possibly downtime
- [Scale to 100M nodes](#) → Partition by business unit or time period
- [Reduce latency by 50%](#) → Profile first, then optimize storage or queries
- [Add audit compliance](#) → Add immutable transaction log, not retrofit

---

## Principles for Operating Graphs

1. **Monitor early, alert loud** — Know something is wrong before users do
2. **Degrade gracefully** — Slow is better than broken
3. **Partition for scale** — One graph per team/domain, not one graph for everything
4. **Plan migrations** — Changing the schema is expensive; do it deliberately
5. **Document operational decisions** — Future you will thank present you

---

See the sections below for specific guidance on each area.

