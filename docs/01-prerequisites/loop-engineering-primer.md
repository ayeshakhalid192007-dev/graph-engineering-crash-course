# Loop Engineering Primer

## Hook

Imagine a bot that watches a support inbox overnight. Every few minutes it wakes up, checks whether a new ticket arrived, drafts a reply if one has, files it, and goes back to sleep. Nobody is standing over it. By morning there's a stack of drafted replies waiting for a human to approve. That small, self-running cycle — wake, check, act, sleep, repeat — is the entire shape of a loop, and this course assumes you've already spent real time building one.

## Explanation

Three words carry most of the weight in Loop Engineering, and this course leans on all three without re-teaching them.

**Heartbeat** is whatever causes the loop to wake up and take its next turn — a timer, a webhook, a human hitting "go again." It's the thing that turns a script you'd have to babysit into something that keeps moving on its own. Without a heartbeat, a loop is just a function waiting to be called.

**Spine** is the one piece of durable state the loop reads at the start of a turn and writes back at the end — a running log of tickets handled, a queue of what's left, a note to itself about what it tried last time. The spine is what lets a loop pick up exactly where the last turn left off instead of starting from nothing every time it wakes.

**Maker/checker** is the split between the part of the loop that produces work and the part that judges whether the work is good enough to count as done. A loop that only makes and never checks will happily ship its own mistakes forever; a loop that separates the two roles — even crudely, even inside the same run — catches a meaningful share of them before they go out the door.

## Diagram

```mermaid
flowchart LR
    H["⏱ Heartbeat\nwhen it runs"]
    B["🤖 Body\ndoes the work"]
    C{"✅ Checker\ngrades it"}
    S["🧠 Spine\nremembers"]
    X["🛑 Provable stop"]

    H --> B
    B --> C
    C -- "not done" --> S
    S --> H
    C -- "success · run limit · no progress" --> X
    X --> U["🧑‍💻 You — the engineer"]

    style H fill:#4169E1,color:#FFFFFF
    style B fill:#0B1325,color:#FFFFFF
    style C fill:#D4AF37,color:#000000
    style S fill:#E2E8F0,color:#000000
```

**Three core ideas.** Heartbeat, Spine, Maker/checker — the shape of a loop that keeps moving on its own.

## Check yourself

A single support-bot loop keeps its ticket queue in one JSON file that it reads at the top of each turn and overwrites at the bottom. What has to be true about who touches that file for this setup to keep working safely?

<details>
<summary>Reveal the answer</summary>

Exactly one process may read and write that file, and it can never be doing so at the same moment as another process — there is no second writer to race against and no second reader to hand a half-written version to. The moment either of those stops being true, the setup needs something more than a single file.

</details>

---

That last condition — one reader, one writer, never both at once — is precisely the assumption a lone loop's spine gets to make and a shared graph cannot. Graph Engineering starts exactly where that assumption breaks.
