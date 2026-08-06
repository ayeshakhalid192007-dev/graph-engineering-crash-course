# Part 1 Quiz

Three questions, one per step. Try answering before you expand each one.

## 1. The thin-memory trick

Two agents are both writing to a single shared notes file at roughly the same time. Naming the exact condition that breaks — not just "it's risky," but the specific setup that a lone loop gets to assume and this scenario no longer has — what is that condition?

<details>
<summary>Reveal the answer</summary>

A single flat file only stays safe under one reader, one writer, never both active at once. Two agents writing to the same file at the same time violates the "one writer" part directly, and whichever write lands last simply replaces the file — there's no merge step to reconcile the two.

</details>

## 2. Direction and labels on an edge

Someone claims that writing `X --uses--> Y` and `Y --uses--> X` into the same graph is basically harmless — a little redundant, maybe, but not actually wrong. Is that right?

<details>
<summary>Reveal the answer</summary>

No. Each direction is its own separate, checkable claim about the codebase, and most real dependencies only run one way. Adding both usually means one of the two edges is simply false, not that the graph is being extra thorough — and now that false edge has to be found and removed on its own.

</details>

## 3. Splitting work-history from facts

A team merges "an agent flagged this issue" and "this issue is confirmed real" into one graph node, reasoning that it saves a step since both entries are about the same underlying bug. Name one concrete question this merge makes harder to answer later.

<details>
<summary>Reveal the answer</summary>

Several work: "was this specific claim ever independently verified, or did we only ever take one agent's word for it," and "in what order did the review actually happen, and who raised it first." A merged node can't cleanly answer either, because the confirmation step and the event that produced the flag both got flattened into a single sentence.

</details>
