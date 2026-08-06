# Advanced Tier · Ultra-Pro (G4)

The fourth skill track from the course roadmap. It assumes you have already shipped a graph — Parts 1–7, the pattern library, and at least one of the later projects behind you. Every page here starts where the core course stops: not with how to build the thing, but with what changes once it is running and something about the situation has outgrown the design.

| Page | The question it answers |
| --- | --- |
| [Graphs at Scale](graphs-at-scale.md) | The store is straining. Is that a traversal problem, a query problem, or neither — and when does a dedicated graph store actually earn its cost? |
| [Multi-Graph Federation](multi-graph-federation.md) | Two graphs must reference the same real-world thing, under different schemas, provenance rules, and owners. How do they interoperate without merging? |
| [Governance at Org Scale](governance-at-org-scale.md) | Several teams each built a sound governance graph, independently. What happens where they meet, and who decides? |

A theme runs through all three, and it is worth naming before you start: each page argues *against* the consolidating move that seems obvious. Do not migrate on size alone. Do not merge two graphs that answer to different authorities. Do not standardize three arbitration rules that each encode a lesson learned expensively. In every case the recommended design is a thin, explicit, jointly-owned seam between things that stay separate — and the reason is the same each time. Consolidation buys uniformity by discarding local knowledge it cannot see it is discarding.

The complexity-budget question from Step 17 applies to everything on these pages, and applies hardest here. Nothing in this tier is machinery you should reach for early.
