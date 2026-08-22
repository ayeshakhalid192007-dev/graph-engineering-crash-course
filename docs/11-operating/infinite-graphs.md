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
```
Task A → depends-on → Task B
Task B → depends-on → Task C
Task C → depends-on → Task A
```

**Detection:** Traversal returns the same node twice

**Fix:** Use a visited set (don't traverse a node twice)

### Pattern 2: Exponential branching
```
Node A has 10 outgoing edges
Each of those has 10 outgoing edges
Each of those has 10 outgoing edges
...
At depth 10, you're exploring 10^10 = 10 billion nodes
```

**Detection:** Memory spike, query timeout

**Fix:** Limit traversal depth or width

### Pattern 3: Transitive closure gone wrong
```
"Find all reachable nodes from A"
If A can reach B, B can reach C, C can reach A...
You traverse the whole connected component
```

**Detection:** Query is slow, returns huge result set

**Fix:** Limit the traversal or use a different query

## Prevention Strategies

### 1. Always limit depth
```
Bad:  MATCH (a:Node)-[*]-(b:Node) RETURN b
Good: MATCH (a:Node)-[*1..5]-(b:Node) RETURN b
```

### 2. Track visited nodes
```
visited = Set()
to_visit = [start_node]
while to_visit:
  node = to_visit.pop()
  if node in visited:
    continue
  visited.add(node)
  to_visit.extend(node.neighbors)
```

### 3. Limit result set size
```
Bad:  SELECT * FROM reachable_nodes(start)
Good: SELECT * FROM reachable_nodes(start) LIMIT 10000
```

### 4. Set query timeouts
```
Query timeout: 30 seconds
If query hasn't returned by then, kill it
Investigate why it's slow
```

### 5. Break cycles intentionally
Add a "frozen" property to nodes you don't want to traverse past, or mark certain edges as "do not traverse."

## What to Monitor

- **Query execution time** — Alert if > expected (query might be looping)
- **Query result size** — Alert if > expected (traversal might be exponential)
- **Memory spike during query** — Sign of exponential branching
- **Graph connectivity** — Run a connectivity analysis monthly (find isolated components)

---

See [Failure Modes](failure-modes.md) for what else can go wrong.

