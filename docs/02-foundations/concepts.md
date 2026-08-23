# Concepts

## Hook

Eight months into a project, a graph has forty-odd edge labels, half of them added by one engineer who has since moved to a different team. A new hire needs to record that a service depends on a queue, and finds three existing edge labels that might mean roughly that — `depends-on`, `reads-from`, `requires` — with no note anywhere explaining how they differ or which one is correct for this case. She picks one, guesses wrong, and a downstream checker that was quietly relying on the distinction starts passing claims it should have rejected. Nobody notices for weeks.

## Explanation

That failure has a name, and it isn't a bug in the checker or a mistake by the new hire. It's **comprehension debt**: the gap between how much of a shared structure exists and how much of it any given person on the team actually understands well enough to use correctly.

Comprehension debt behaves a lot like the more familiar idea of technical debt in undocumented code — a function nobody fully understands anymore still runs, still returns answers, and still quietly accumulates risk every time someone edits it without knowing what else depends on its exact behavior. A graph is worse in one specific way: code that nobody understands usually still gets exercised by tests that catch a wrong change. A graph edge that nobody fully understands can be *added wrong* and nothing mechanical stops it, because from the graph's point of view a wrong edge and a right one look identical — both are just a labeled connection between two nodes.

The debt accumulates the same way financial debt does: a schema grows one convenient addition at a time, each one reasonable on its own, until the total shape of the thing outruns what any single person holds in their head. The interest on that debt gets paid by whoever touches the graph next without the full history — usually by adding one more near-duplicate label rather than untangling the ones that already exist, which makes the next person's version of this problem slightly worse.

The fix isn't "write better documentation" as an afterthought — it's treating a shared graph's schema the way you'd treat a public API: reviewed before it grows, named consistently, and small enough on purpose that a newcomer can hold the whole shape of it in their head within an afternoon.

## Diagram

```mermaid
flowchart TB
    subgraph "Normal Schema"
        E1["depends_on"]
        E2["reads_from"]
        E3["requires"]
        S["Schema (4 labels)"]
        E1 -- "understood" --> S
        E2 -- "understood" --> S
        E3 -- "understood" --> S
    end

    subgraph "Comprehension Debt"
        E4["depends_on (v2)"]
        E5["reads_from (v2)"]
        E6["requires (v2)"]
        E7["depends_on (v3)"]
        S2["Schema (11 labels)"]
        E4 -- "confusing?" --> S2
        E5 -- "confusing?" --> S2
        E6 -- "confusing?" --> S2
        E7 -- "confusing?" --> S2
    end

    subgraph "New Hire Confusion"
        NH["New hire"]
        NH -- "which label to use?" --> E4 & E5 & E6 & E7
        NH -. "guesses wrong" .-> D["Downstream checker passes wrong claims"]
    end

    style S fill:#4169E1,color:#FFFFFF
    style S2 fill:#D4AF37,color:#000000
```text

Each near-duplicate label increases the debt, because it adds one more thing a newcomer has to learn to tell apart from the others, without removing anything they already had to learn. The graph doesn't flag it because a graph has no built-in way to tell a redundant label from a genuinely new distinction — both are equally valid-looking edges to the structure itself. Catching this requires a human (or a deliberate review process) actively asking whether a new label is really needed, not something the graph will surface on its own.

---

**Comprehension debt.** The gap between how much of a shared structure exists and how much of it any given person on the team actually understands well enough to use correctly.

## Check yourself

A team adds a new edge label every time an existing one "almost fits, but not quite," rather than ever revisiting the ones already in use. What is this actually doing to the team's comprehension debt, and why doesn't the graph itself flag it as a problem?

<details>
<summary>Reveal the answer</summary>
