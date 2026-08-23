# Infinite Graphs (Avoiding Runaway Traversals)

One of the easiest ways to break a graph system is to accidentally traverse infinitely or explore so much of the graph that you run out of memory/time.

## Why This Happens

Your graph has cycles. That's usually good—it models real-world relationships. But it means:
- Task A depends on Task B
- Task B depends on Task C
- Task C depends on Task A

If you naively traverse "all dependencies of Task A," you'll loop forever.

## Detection Patterns

### Pattern 1: Cycles in the graph
```text
Task A → depends-on → Task B
Task B → depends-on → Task C
Task C → depends-on → Task A
```text

**Detection:** Traversal returns the same node twice

**Fix:** Use a visited set (don't traverse a node twice)

### Pattern 2: Exponential branching
```text
Node A has 10 outgoing edges
Each of those has 10 outgoing edges
Each of those has 10 outgoing edges
...
At depth 10, you're exploring 10^10 = 10 billion nodes
```text

**Detection:** Memory spike, query timeout

**Fix:** Limit traversal depth or width

### Pattern 3: Transitive closure gone wrong
```text
"Find all reachable nodes from A"
If A can reach B, B can reach C, C can reach A...
You traverse the whole connected component
```text

**Detection:** Query is slow, returns huge result set

**Fix:** Limit the traversal or use a different query

## Prevention Strategies

### 1. Always limit depth
```text
Bad:  MATCH (a:Node)-[*]-(b:Node) RETURN b
Good: MATCH (a:Node)-[*1..5]-(b:Node) RETURN b
```text

### 2. Track visited nodes
```text
visited = Set()
to_visit = [start_node]
while to_visit:
  node = to_visit.pop()
  if node in visited:
    continue
  visited.add(node)
  to_visit.extend(node.neighbors)
```text

### 3. Limit result set size
```text
Bad:  SELECT * FROM reachable_nodes(start)
Good: SELECT * FROM reachable_nodes(start) LIMIT 10000
```text

### 4. Set query timeouts
```text
Query timeout: 30 seconds
If query hasn't returned by then, kill it
Investigate why it's slow
```text

### 5. Break cycles intentionally
Add a "frozen" property to nodes you don't want to traverse past, or mark certain edges as "do not traverse."

## What to Monitor

- **Query execution time** — Alert if > expected (query might be looping)
- **Query result size** — Alert if > expected (traversal might be exponential)
- **Memory spike during query** — Sign of exponential branching
- **Graph connectivity** — Run a connectivity analysis monthly (find isolated components)

---

See [Failure Modes](failure-modes.md) for what else can go wrong.

