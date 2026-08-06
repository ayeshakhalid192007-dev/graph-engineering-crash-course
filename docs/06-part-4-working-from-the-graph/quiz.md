# Part 4 Quiz

Two questions below, matched to Steps 9 and 10 in order. Answer each from memory first, then expand the reveal and compare.

## 1. Contradiction-aware subgraphs

A subgraph builder finds two claim nodes attached to the target function that disagree with each other, and resolves the disagreement by keeping only the claim from the more recently updated source before handing the slice to the worker. The worker never learns a second, older claim existed. What's lost by resolving the disagreement before the handoff instead of after?

<details>
<summary>Reveal the answer</summary>

What disappears is any trace that the graph held two incompatible accounts at once. Preferring the newer claim may well turn out to be the correct judgment — but a judgment made during slice construction, unannounced, is one the worker can never review, question, or overturn. Handing over a slice is supposed to hand over the disagreement with it; a builder that tidies the conflict away first has answered a question that was never its to answer.

</details>

## 2. Decomposing a claim before checking it

A reviewer bot is handed a pull request whose description promises the change leaves authentication alone. Rather than reducing that promise to a single edge it could look up, the bot skims the diff alongside the description and reports that the work "looks contained to the front end." As it happens, that impression is accurate. Is the check trustworthy?

<details>
<summary>Reveal the answer</summary>

No, even though this particular impression happened to be right. Nothing about reading a diff and forming an impression is grounded in a specific, checkable fact — the same procedure would have produced the same confident-sounding answer on a diff that buried a one-line auth import somewhere inside it. A check is only as trustworthy as the mechanism producing it, and "this looked contained" is not the same mechanism as "no PR --modifies--> auth-module edge exists," even on the runs where both happen to agree.

</details>
