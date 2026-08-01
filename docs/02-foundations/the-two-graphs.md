# The Two Graphs

## Hook

A small support team runs an army of agents that triage incoming tickets. Ticket #482 comes in: "can't log in." One agent tries a password reset — doesn't fix it. A second agent restarts the user's session — still broken. A third agent notices the account's login token was issued thirty-one days ago, past the product's thirty-day expiry, and closes the ticket with the real cause identified. Three attempts happened, in a specific order, and one confirmed fact came out the other end. Those are not the same kind of thing, and treating them as if they were is where a lot of graph designs quietly go wrong.

## Explanation

The three attempts on ticket #482 belong in what this course calls a **work-history graph**: a trail of what was tried, by whom, in what order, and whether it worked. Its job is letting someone — human or agent — walk backward later and see exactly how a result was reached, and letting the next agent that touches a similar ticket see what's already been ruled out instead of re-trying the same dead ends. A work-history graph is expected to grow fast and include failures; a failed attempt is not noise here, it's exactly the kind of thing this graph exists to keep.

The confirmed cause — "this product's login tokens expire after thirty days, and an expired token produces this exact error" — belongs somewhere different: a **fact graph**. This is where the team keeps claims it has actually checked and is willing to have future agents build on without re-verifying from scratch. A fact graph should grow much more slowly than a work-history graph, and much more carefully, because every node in it is an implicit promise to whoever reads it next that the claim has already been checked.

Notice what goes wrong if the team keeps only one graph. If every attempt and every confirmed fact lands in the same undifferentiated pile, a future agent querying "what do we know about login failures" has no way to tell a one-off attempt that didn't pan out from the actual, checked cause — it all just looks like more nodes. Keep the two separate, even if they live in the same database, and that question has a clean answer: query the fact graph for what's known, query the work-history graph for what's been tried. This page only gets you the vocabulary and the shape of the split; the fuller treatment of exactly what collapsing them costs you, and how to keep them from blurring together in practice, comes later once you've built a bit more of the surrounding picture.
