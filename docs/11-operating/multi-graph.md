# Multi-Graph Coordination

When you have multiple graphs that need to work together—either multiple instances of the same graph (sharding) or completely different graphs (federation)—coordination becomes critical.

## Why You Need Multiple Graphs

**Sharding (same graph, split across instances):**
- Your single graph is too large to fit on one server
- Write volume is too high for one database to handle
- Different regions need local copies with low latency

**Federation (different graphs, different teams):**
- Different teams own different domains (finance graphs, product graphs, HR graphs)
- Each team needs autonomy but needs to reference entities from other domains
- You need a governance layer above individual graphs

## Coordination Challenges

### Identity across graphs
How do you refer to a node in Graph A from Graph B?

- **Solution 1: Global IDs** — Assign globally unique IDs, maintain a registry
- **Solution 2: Federated IDs** — Use <graph-id>/<local-id>, allow cross-graph queries
- **Solution 3: Separate lookup** — Query the other graph via API when you need to reference it

### Consistency across graphs
What happens when Graph A's write fails but Graph B's succeeds?

- **Accept inconsistency** — Document it, monitor for it, handle it at application layer
- **Distributed transactions** — Expensive, slow, but gives you consistency guarantees
- **Eventual consistency** — Write to both, reconcile later

### Ownership and access
Who can write to each graph? Who can read?

- **Per-team graphs** — One team per graph, team owns all writes
- **Shared graphs with roles** — One graph, multiple teams with read/write permissions
- **Hybrid** — Core facts are shared and read-only; teams have private subgraphs

---

## Common Multi-Graph Patterns

See [Multi-Graph Federation](../advanced/multi-graph-federation.md) in Advanced for detailed patterns.

