# Part 2 Flashcards

This Part introduced three terms. Hide the right column and try to state each definition yourself before checking it.

| Term | Definition |
| --- | --- |
| **Ratchet** | A comparison rule that only extends a work record when a fresh attempt clears the current best outright -- anything that falls short gets set aside, never treated as the new baseline, and never thrown away either. |
| **Durable history** | The short chain of attempts a ratchet actually promotes forward, each one an improvement on the last, serving as the trustworthy record of how the present best result was reached. |
| **Queryable failed branch** | A discarded attempt that stays reachable in the graph after it stops being the current best, complete with what was tried and why it fell short, so nobody has to rediscover the same dead end firsthand. |
