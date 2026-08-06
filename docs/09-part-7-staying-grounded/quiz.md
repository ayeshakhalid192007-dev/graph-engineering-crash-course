# Part 7 Quiz

Two questions ahead, Step 16 first and Step 17 second. Both reward a specific, committed answer more than a hedge — work one out fully before you check either reveal.

## 1. Naming the right lighter-weight fix

A neighborhood mutual-aid group keeps a running list of who's offered to drive elderly neighbors to appointments this month. Nine volunteers have signed up for nine separate rides, none of them connected to any other — Tuesday's driver has no bearing on Thursday's. The organizer, excited after reading about knowledge graphs, starts sketching a schema with `Volunteer`, `Ride`, and `Neighbor` node types before anyone's driven anywhere. Which of the four situations from Step 16 does this match, and what should replace the schema?

<details>
<summary>Reveal the answer</summary>

This is the independent-task-set pattern — nine rides with no dependency between them is close to the textbook case. Nothing about Tuesday's ride succeeding or failing changes anything about Thursday's, which is exactly the test for whether a piece of work needs shared memory at all. What the group actually needs is a queue: a list of open ride requests, claimed as drivers volunteer for them, with nothing more elaborate required to track who's doing what. A schema and node types would still technically hold this data — there is very little a graph structure genuinely can't represent — but holding the data isn't the same test as being the cheapest way to get the job done, and a queue costs a fraction of the design and upkeep a graph would.

</details>

## 2. Reading a maintenance-cost tally correctly

Six months into a new loop's life, a team pulls up their governance dashboard and finds an audit loop that has filed reports every night, all clean, and an arbitration edge that has never once been consulted. Someone argues both should stay exactly as they are, "since nothing has gone wrong." What's the flaw in treating a clean six-month history as proof the two edges are working as intended?

<details>
<summary>Reveal the answer</summary>

A clean report from an edge with no matching incident behind it is consistent with two very different explanations, and "it's working" is only one of them. The other is that the edge was never needed in the first place — the audit loop is scanning for a defect category this particular loop was never exposed to, or the arbitration edge names a collision between two loops that structurally never touch the same resource. Six months of silence can't distinguish those two cases from inside the dashboard; only checking whether the edge was ever installed against a real, specific incident can. Treating an unproven edge's silence as validation is how **premature governance** becomes permanent governance — the ongoing cost never gets weighed against the evidence, because the absence of a failure gets read as the edge succeeding rather than as the edge possibly never having had a job to do.

</details>
