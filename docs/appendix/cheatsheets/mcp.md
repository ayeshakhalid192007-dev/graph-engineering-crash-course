# Cheatsheet · Where MCP Fits

This is not an MCP tutorial. It answers one question the course otherwise leaves open: you have built a graph using these patterns, and you want more than one agent — possibly in more than one tool — to reach it. Where does the Model Context Protocol sit in that picture?

Read the [Claude Code](claude-code.md) and [OpenCode](opencode.md) sheets first. Those cover how a single agent runs a pattern. This one covers what changes when the graph has to outlive any one of them.

## The one-sentence version

MCP is a way to put a graph behind an interface an agent can call, instead of behind a file path an agent has to know about.

## What it replaces

Every kit in `starters/` reaches its graph the same way: the skill opens a file sitting next to it — `schema.example.json`, `graph.db`, `claims.json`. That is deliberate. It keeps each kit runnable on its own, with nothing to install, which is what you want while learning a pattern.

It also has a ceiling. Two agents in different repositories cannot share a file path. A skill that hardcodes `../graph.db` cannot be pointed at a staging copy without editing the skill. And every kit that touches the graph has to re-implement the same read and write logic, which is exactly the duplication category G's storage patterns exist to concentrate in one place.

Exposing the graph through an MCP server moves that boundary:

| Concern | File-path kit | Behind an MCP server |
| --- | --- | --- |
| Who can reach the graph | Whatever runs in that directory | Any client that can connect |
| Where query logic lives | Restated in every skill | Once, in the server |
| Swapping the store | Edit every skill | Change the server; clients don't move |
| What a client must know | The schema *and* the file layout | The tool signatures |

## Mapping to the pattern library

MCP is an implementation choice for **category G (storage)**. It is not a new pattern, and it does not replace any of the other six categories.

- [`sqlite-backed-graph`](../../../starters/sqlite-backed-graph/) — the natural first thing to put behind a server. The tables stay exactly as they are; the server wraps the queries the kit already runs.
- [`postgres-backed-graph`](../../../starters/postgres-backed-graph/) and [`neo4j-at-scale`](../../../starters/neo4j-at-scale/) — the two kits where a server earns its cost fastest, because the connection details you would otherwise copy into every skill collapse into one place.
- [`file-graph-for-small-teams`](../../../starters/file-graph-for-small-teams/) — the one where it usually does not. If the graph is JSON in a repo that everyone already clones, a server adds a moving part and takes away the ability to read the graph in a text editor.

The rest of the library is unaffected, and this is the part most worth being clear about. A grounded checker still has to reduce each claim to the one edge whose presence would sink it. A subgraph still needs a budget. A merge still needs to be reversible, and an edge still needs a receipt. Serving the graph over a protocol changes *how the query is delivered* and nothing about *what makes the answer trustworthy* — which is the entire subject of Parts 3 through 5.

## What a server should expose

Two shapes, and the difference between them matters more than it first looks:

- **Resources** — addressable things a client reads. A subgraph, a claim and its provenance, a schema version.
- **Tools** — operations a client invokes. Extract facts from a document, merge two nodes, check a claim.

Keep the write path narrow. The reason is the same one behind every provenance pattern in Part 3: an edge that can be created by a general-purpose write call is an edge whose receipt depends on the caller having chosen to attach one. A server that exposes `add_edge(from, to, type)` has made provenance optional, no matter what the schema says. A server that exposes `record_claim(subject, relation, object, source)` has made it structural. Push the invariant into the signature, where it cannot be skipped, rather than into documentation, where it can.

Two more that follow from the same reasoning:

- **Return budgets, not everything.** A `get_subgraph` tool with no cap is the failure Step 9 is about, relocated to the server side.
- **Surface conflicts rather than resolving them.** If two claims disagree, both belong in what the client receives. A server that silently picks a winner has moved arbitration somewhere the calling agent cannot see it or audit it later.

## When to bother

Not yet, in most cases. The honest sequence is the one Part 7 argues for generally: get the graph correct as files, confirm the patterns hold, and add the server when a second consumer actually exists — not in anticipation of one. A protocol boundary is easy to add to a graph you understand and painful to add to one you are still deciding the shape of.

Reach for it when at least one of these is true:

- More than one agent, in more than one tool, needs the same graph.
- The store is real infrastructure — Postgres, Neo4j — with credentials you do not want copied into every skill.
- You need one enforcement point for write rules, because you have stopped being able to review every writer by hand.

Until then, the file next to the kit is not a compromise. It is the cheaper thing that works, and swapping it out later costs less than guessing wrong about the interface now.
