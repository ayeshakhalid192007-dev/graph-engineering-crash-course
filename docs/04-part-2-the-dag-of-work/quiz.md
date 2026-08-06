# Part 2 Quiz

Two questions here, one for each step above. Give each a real attempt before opening the reveal.

## 1. The ratchet

A loop searching for a better summarization prompt tries five candidates overnight. Someone suggests simplifying the ratchet rule: keep appending every candidate to durable history in the order it was tried, instead of only appending the ones that strictly beat the current best. What does that change actually break?

<details>
<summary>Reveal the answer</summary>

It breaks the one property durable history is supposed to have: that the chain only ever moves toward better results. Appending every candidate regardless of score means a reader skimming durable history can no longer tell "this was an improvement" from "this was just tried next" -- the chain stops being a record of progress and becomes a record of activity, which is exactly the unfiltered, hard-to-read log the ratchet exists to avoid.

</details>

## 2. Queryable failed branches

Two agents already tried and failed to fix a bug earlier today. A third agent picks up the ticket, reads the bug's current status, and proposes a fix -- without looking at what the first two agents already attempted. The bug's current status is accurate and up to date. Is that enough?

<details>
<summary>Reveal the answer</summary>

No. The bug's current status only says what's true right now; it says nothing about what's already been ruled out. Without querying the failed attempts specifically, the third agent has no way to know whether its proposal repeats an approach that was already tried and already disproven -- the current status and the history of attempts answer two different questions, and reading only one of them leaves the other one unanswered.

</details>
