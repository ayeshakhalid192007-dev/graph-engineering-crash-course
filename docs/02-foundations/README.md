# Foundations

Core vocabulary and concepts for graph engineering — building on the loop discipline you already know.

## What You'll Learn

This section establishes the mental models and terminology used throughout the entire course:

- Why graphs exist: the exact moment one loop becomes a problem (two loops, same file)
- The critical distinction between work-history and fact graphs
- Key terminology used throughout the course
- How comprehension debt accumulates in shared structures

## Contents

1. **[Mental Models](mental-models.md)** — From single loops to many: why graphs exist
2. **[The Two Graphs](the-two-graphs.md)** — Why work-history and facts must stay separate
3. **[Glossary](glossary.md)** — Precise definitions for all key terms
4. **[Concepts](concepts.md)** — Comprehension debt and team understanding

## Diagram

```mermaid
flowchart TB
    LOOP["🔄 Loop Engineering<br/>heartbeat · spine · maker-checker"]
    
    START["Foundations"]
    
    MM["Mental Models<br/>Why graphs exist"]
    TG["The Two Graphs<br/>Work vs Facts"]
    GL["Glossary<br/>Key terms"]
    CO["Concepts<br/>Comprehension debt"]
    
    LOOP --> START
    START --> MM --> TG --> GL --> CO
    
    CO --> NEXT["Part 1:<br/>The Memory Problem"]
    
    style LOOP fill:#06b6d4,stroke:#0f172a,color:#fff
    style START fill:#4169E1,color:#FFFFFF
    style MM fill:#E2E8F0,color:#000000
    style TG fill:#E2E8F0,color:#000000
    style GL fill:#E2E8F0,color:#000000
    style CO fill:#E2E8F0,color:#000000
    style NEXT fill:#D4AF37,color:#000000
```

## Learning Thread

**Start here** if you've finished Loop Engineering and are ready to scale to many loops. This section answers "what is a graph and why do I need one?" — grounded in the loop vocabulary you already know.

**Your knowledge transfer:**
- Heartbeat stays the same (read → decide → write)
- Spine stays the same (append-only log)
- Maker-checker stays the same (propose + verify)

What's new: coordinating multiple loops without races, conflicts, or lost work.

**Suggested path**: Read mental models → the two graphs → skim glossary → read concepts. Return to the glossary as a reference when you encounter unfamiliar terms later.

## Skills Assessment

Can you:

- ✓ Explain why a single memory file works for one loop but fails for two
- ✓ Distinguish between work-history graphs and fact graphs
- ✓ Define: node, edge, extraction, resolution, provenance
- ✓ Recognize when comprehension debt is accumulating

**Ready?** Continue to [Part 1 - The Memory Problem](../03-part-1-the-memory-problem/)
