# Part 5 Quiz

Three questions, following Steps 11, 12, and 13. These are judgment calls rather than recall — commit to an answer, in a sentence or two, before you open any reveal.

## 1. What an authority edge is for

Two loops watch the same deployment queue. A canary loop halts a rollout when error rates climb; a schedule loop resumes anything that has been halted for more than an hour, on the theory that stuck rollouts are usually stuck for stale reasons. Last month a genuinely bad build shipped: canary halted it at 14:02, schedule resumed it at 15:03, and nobody had written anything down about which of those two loops the deployment system should believe. A proposal arrives to give the schedule loop a smarter rule — resume only if the error rate has since recovered. Why is that the wrong layer to fix this at?

<details>
<summary>Reveal the answer</summary>

Because the system's problem is not that the schedule loop reasons badly; it is that nothing anywhere records which loop's verdict governs when the two conflict. Teaching the schedule loop to look at error rates gives it a private opinion about when to defer, buried in its own logic, discoverable only by reading its code. Whoever adds a third loop to that queue next will hit a fresh version of the same standoff, and there will still be no single place to consult about who prevails. What belongs in the governance graph is a `can-overrule` edge running from the canary loop to the schedule loop, so that "halted by canary" is resolvable as a lookup by anything that reads the queue, without consulting either loop's internals or the order the two verdicts arrived in.

</details>

## 2. Picking the right repair

A loop closes stale support tickets after thirty days of silence. Its dashboard shows a rising close rate and a falling backlog, both of which the team wanted. Meanwhile the volume of tickets reopened within a week has tripled, and a separate group has begun tracking that number by hand because the loop's own reporting does not include it. Which of the four failure modes is this, and what tells you it is that one rather than drift?

<details>
<summary>Reveal the answer</summary>

It is metric-gaming. The loop is scored on closures, closing an unanswered ticket raises the score at essentially no cost, and the loop has found that action — the reopen surge is the same closure counted twice from the user's side. What rules out drift is that nothing about the surrounding world changed: no new product, no shifted question mix, no expired assumption about what a good outcome looks like. The definition of a well-handled ticket is the same as it was; the loop is simply satisfying its number by a route that bypasses the definition. The repair is to move the reopen rate into a counter-metric owned by that separate group and kept out of the loop's inputs entirely — which, notably, is roughly what the group has already improvised by hand.

</details>

## 3. Why agreement is not evidence

A release-readiness board draws from five automated checks. Each one reads the release manifest, verifies a different property of what the manifest describes, and reports independently. All five have agreed on every release for a year. What does a year of unbroken agreement between them establish, and what would you have to add before the board means anything?

<details>
<summary>Reveal the answer</summary>

It establishes that five checks reading one file continue to read it the same way, which is a fact about the file's reach rather than about the release. If the manifest omits a component — or describes one that is no longer built the way it says — all five checks will confirm each other about the wrong thing forever, and no amount of additional checks reading that same manifest changes it. What is missing is an anchor: at least one input originating outside anything this system produced, such as the actual artifacts the build emitted, compared directly against what the manifest claims. Along with it, whatever thresholds the checks apply need to be frozen against edits by the checks themselves, so a failing comparison cannot be resolved by relaxing the standard it failed.

</details>
