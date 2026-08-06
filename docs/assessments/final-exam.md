# Final Exam

Twenty questions covering all seventeen steps. Questions 1–17 follow the course in order, one per step. Questions 18–20 are anti-pattern spotting, drawn from the three categories in [`anti-patterns.md`](../operating/anti-patterns.md).

**How to take it.** Write your answers down before opening the key. Most questions want two or three sentences; a few want a decision plus the reason behind it. The key is a single fold at the bottom rather than one per question, so it is harder to check yourself into agreement one answer at a time.

**Passing.** There is no score to clear. The useful signal is *which* questions you could not answer without looking, because those map to specific steps worth rereading — the key names the step for each.

---

## Part 1 · The Memory Problem (Steps 1–3)

**1.** A team's agent keeps one Markdown file as memory. It works for months, then starts producing contradictory answers about the same subject within a single week. Nobody deleted anything, and the file is still readable. What changed, and why does adding more careful writing to the file not fix it?

**2.** Two people model the same situation. One writes a node labeled `payments` and an edge labeled `related-to` pointing at `checkout`. The other writes a node labeled `payments-service` and an edge labeled `calls` pointing at `checkout-api`. Both graphs are valid. Which one will still be answerable in six months, and what specifically makes the difference?

**3.** A team stores every claim their agents have verified and every attempt their agents have made in one graph, reasoning that both are just facts about the project. Name the two distinct questions this makes hard to answer, and say why merging the two makes *both* worse rather than trading one off against the other.

## Part 2 · The DAG of Work (Steps 4–5)

**4.** A ratchet records only attempts that improve on the current best. A teammate proposes dropping the non-improving attempts entirely, since by definition they did not move the number. What does the team lose the first time someone asks why an approach was abandoned?

**5.** A failed branch is kept in the work-history graph rather than deleted. Give one concrete question that becomes answerable *because* the failure is still queryable, and explain why storing it as a note in a document would not have answered it.

## Part 3 · The Graph of Facts (Steps 6–8)

**6.** An extraction run reads a document and returns an entity type the schema does not define. Two responses are available: drop the item and record why, or add the type to the schema so nothing is lost. One of these is compatible with having a schema at all. Which, and why is the other one self-defeating?

**7.** A resolution step merges two mentions into one canonical node and keeps both original mentions, but records no reason for the merge. The merged node is correct. Explain why this is still a defect, in terms of what a reviewer six months later can and cannot do.

**8.** An edge carries `source_document` and an extraction timestamp. A second edge, added by hand during an incident, carries neither. Both are true. Describe the specific situation in which this asymmetry becomes expensive, and say what it costs.

## Part 4 · Working From the Graph (Steps 9–10)

**9.** A worker is assigned one function to fix. The subgraph builder returns that function, its direct callers and callees, and — because two claims about the function contradict each other — only the more recently sourced one. What has the worker lost, and why is recency a poor place to resolve this?

**10.** A checker is asked to settle the claim "this deployment does not restart the billing service." Describe the query it should run, in terms of a single edge. Then say what a checker that instead evaluates how carefully the claim is worded will do when handed a confidently-written false claim.

## Part 5 · The Graph of Loops (Steps 11–13)

**11.** Two loops write to the same field. Both are individually sound. Neither one's implementation establishes any precedence between them. Describe what happens over a weekend, and name the single piece of graph structure that prevents it.

**12.** List all four failure modes a loop running on its own falls into. For each, give the check that catches it — not a general principle, but the specific thing that has to exist in the graph.

**13.** A team freezes its success threshold so its loops cannot edit it. A month later the threshold is genuinely wrong — the business changed. What does the frozen node oblige them to do that an unfrozen one would not have, and why is that obligation the point rather than the cost?

## Part 6 · One Graph, End to End (Steps 14–15)

**14.** Of the six questions to ask before building a graph, one is the most common reason a graph should not be built. Name it, and describe a project that clearly fails it.

**15.** The same small system is built twice in Step 15. What does the second build reveal that reading about the first cannot, and why is that specifically hard to learn from a worked example?

## Part 7 · Staying Grounded (Steps 16–17)

**16.** A team has a fixed set of about forty relationships that has not changed in two years and is not expected to. They are considering a graph. Make the case against, and then name the one thing that would change your answer.

**17.** Governance costs something. A four-person team with two loops is considering the full apparatus — governance graph, arbitration edges, counter-metrics, anchors, frozen nodes. Which of these would you keep, which would you defer, and what is the principle behind the split?

## Anti-Pattern Spotting (Questions 18–20)

For each scenario: name the anti-pattern, identify which of the three categories it belongs to (design, governance, or judgment), and give the fix.

**18.** A data team's extraction skill is prompted to "pull out the important entities and how they relate." Six months in, a query for all services touched by an incident has to check four different property names for what is conceptually the same field, because different runs shaped nodes differently. Someone proposes writing a normalization layer over the graph to smooth this out.

**19.** An organization runs five loops. Each one validates its output against the loop downstream of it, and the fifth validates against the first. Internal agreement is high — disagreement rates have fallen steadily for three quarters, and the team cites this as evidence the system is working.

**20.** A logistics team maintains a fact graph of carrier relationships. A claim entered eighteen months ago states that a particular carrier does not serve a region. It has never been re-examined, because it was verified when entered and nothing has flagged it since. A new routing loop reads it as current.

---

## Answer Key

<details>
<summary>Reveal the full answer key — twenty answers, each naming the step it comes from. Reveal the answer.</summary>

**1 · Step 1.** What changed is the number of things the file has to keep straight at once, not the quality of its writing. A single document has no structure that forces two statements about the same subject to meet, so as it grows, contradictions accumulate without ever being adjacent. Writing more carefully does not fix it because the problem is not the prose — nothing in a flat file makes a new claim confront the old claim it contradicts. Structure is what does that.

**2 · Step 2.** The second. `related-to` records that a connection exists but not what kind, so in six months nobody can tell from the graph whether `payments` calls `checkout`, depends on it, was replaced by it, or merely gets discussed alongside it. Specific labels — on both nodes and edges — are what make a graph answerable later. A vague edge is barely more useful than no edge, because the reader has to go find the original context anyway.

**3 · Step 3.** It makes "what have we tried" and "what do we actually know" both hard. The first gets polluted with claims that were never attempts; the second gets buried under attempts that verified nothing. Merging makes both worse rather than trading them off because each question's noise is the other question's signal — every record that helps one is an obstacle to the other, so there is no mixing ratio that serves either well.

**4 · Step 4.** The reason an approach was abandoned. A ratchet that keeps only improvements records the path taken and erases the paths rejected, so the next person to have the same idea has no way to learn it was already tried and why it did not work. They pay the cost again. Recording non-improving attempts is what makes the history a record of the search rather than a record of the winners.

**5 · Step 5.** For example: "has anyone tried this approach on this component before, and what happened?" This is answerable against a queryable failure because the branch, its target, and its outcome are all structured and can be matched against the current task. A note in a document answers it only if someone remembers the note exists and goes looking — which is exactly the failure mode of the single memory file from Step 1.

**6 · Step 6.** Dropping the item and recording why. Expanding the schema mid-run is self-defeating because a schema is a boundary agreed on before the data arrives; one that grows to accommodate whatever any document happened to mention is not a boundary at all, just a tally. The value of the constraint is entirely in its being fixed in advance, so a schema that yields under pressure has given up the only thing it was providing.

**7 · Step 7.** A reviewer can see *that* the merge happened and can reverse it, but cannot evaluate whether it was justified. Correctness now is not the issue — the defect is that the decision is unauditable, so a reviewer facing a questioned merge has no basis to either defend or overturn it beyond re-doing the original reasoning from scratch. The reason is what makes a reversible merge reviewable rather than merely undoable.

**8 · Step 8.** It becomes expensive the day one edge in the graph turns out to be false and the team has to work out what else came from the same source or run. Every edge with provenance can be checked and, if necessary, quarantined by source. The hand-added edge cannot be placed at all, so the team faces a choice between trusting it on faith and treating the whole graph as suspect — and the second is what usually happens, which means one unprovenanced edge devalues every provenanced one around it.

**9 · Step 9.** The worker has lost the knowledge that the graph does not have a settled answer. Recency is a poor place to resolve it for two reasons: it is a plausible-sounding tiebreaker that is frequently wrong, and — more importantly — applying it inside the builder hides that a decision was made at all. The worker sees one clean claim and cannot weigh the older one, or even know it exists. Whether to prefer the newer claim is a judgment for whoever reads the slice.

**10 · Step 10.** It should query for the existence of a single edge: `D-212 --restarts--> billing-service`. Present means the claim is rejected; absent means it is confirmed. A checker that evaluates wording will approve a confidently-written false claim exactly as readily as a true one, because confidence and truth are unrelated properties of a sentence. That is not a weaker check — it is not a check.

**11 · Step 11.** They overwrite each other repeatedly, each write locally correct under its own logic, and by Monday the field has a value that reflects whichever loop ran last rather than any decision anyone made. The structure that prevents it is an arbitration edge: a recorded precedence rule, scoped to that field, saying which loop's write governs and on what grounds.

**12 · Step 12.** (a) *Optimizing a metric that has come apart from the goal* — caught by a counter-metric tracked by a separate loop. (b) *Validating only against other loops, with nothing outside the ring* — caught by at least one anchor to something the loops did not produce. (c) *Rewriting the rule it is judged by* — caught by a frozen node the loop cannot modify. (d) *Racing another loop for the same resource* — caught by an arbitration edge recording precedence. In each case the check has to be a real structure in the graph; an intention to be careful is not one.

**13 · Step 13.** It obliges them to change the threshold as a deliberate, logged decision by someone with standing, rather than as a side effect of a loop's ordinary operation. That obligation is the point: the frozen node was never claiming the value would stay right forever, only that changing it must be visible. The cost — a slower change — buys the ability to distinguish "we got better" from "we moved the line," which is precisely what an unfrozen threshold destroys.

**14 · Step 14.** Whether the relationships are actually changing and growing. A project fails it when the relationship set is fixed and small — say, a list of forty accounts and their assigned representatives, stable for years. A schema, an extraction step, and a resolution step are ongoing costs, and paying them for something a table already handles is spending maintenance effort to gain nothing.

**15 · Step 15.** The second build reveals which parts of the first were load-bearing and which were incidental to how it happened to be written. That is hard to learn from a worked example because a finished example presents every decision with equal weight and none of the alternatives — you see what was chosen, never what it was chosen over, so you cannot tell a necessary choice from an arbitrary one until you make the choices yourself.

**16 · Step 16.** Against: forty fixed relationships is a table. The schema, extraction, resolution, and provenance apparatus are permanent costs incurred against a set that will not grow, and a spreadsheet answers every question you have today at a fraction of the maintenance. What would change the answer is evidence the set is about to stop being fixed — an acquisition, a new product line, or a pattern of one-off additions that have started arriving monthly rather than yearly. Growth is the thing that flips it, not size.

**17 · Step 17.** Keep the anchor and the frozen node: both are close to free, and both prevent failures that are expensive and hard to detect after the fact. Defer the governance graph and arbitration edges — with two loops, a person can hold the interaction in mind, and the machinery costs more than it saves. The counter-metric is the judgment call, and it depends on whether the loop's metric is one that can plausibly come apart from the goal. The principle: adopt the governance whose absence would cost you something you could not notice, and defer the governance that only formalizes something you can currently see directly.

**18 · Design — no schema before extraction.** The fix is a schema fixed in advance, with out-of-schema items dropped and reported. The proposed normalization layer is the anti-pattern compounding: it accepts inconsistent shapes as permanent and adds machinery to paper over them, so every future consumer inherits both the mess and the layer. Fix the extraction, then normalize what already exists once.

**19 · Governance — a ring of loops validating only one another, anchored to nothing external.** The falling disagreement rate is the alarm, not the evidence: a closed ring of loops converges on internal consistency regardless of whether it is consistent with anything real. The fix is at least one anchor — a measurement, a human sign-off, an external record — that no loop in the ring produces.

**20 · Judgment — treating the fact graph as permanent truth rather than the team's current best understanding.** Verified-when-entered is not the same as true-now, and "nothing has flagged it" is not a signal when nothing is doing the flagging. The fix is a re-examination path: claims carry the date and basis of their last check, and claims that feed automated decisions get revisited on a schedule rather than on incident.

</details>

---

Next: the [capstone rubric](capstone-rubric.md) for Project 8, and the [Graph Ready certification](graph-ready-certification.md).
