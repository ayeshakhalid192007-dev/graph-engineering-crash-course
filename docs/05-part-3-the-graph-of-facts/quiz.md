# Part 3 Quiz

Three questions follow, one tied to each step. Work through each one on your own before revealing the answer.

## 1. Schema-first extraction

An extraction pass over a postmortem produces an item naming a relationship type the schema never defined. A teammate suggests folding that relationship type into the schema right then, so nothing pulled from the document goes to waste. What does taking that shortcut give up?

<details>
<summary>Reveal the answer</summary>

The whole reason a schema exists in the first place: a boundary agreed on ahead of time, not one that bends to match whatever a given document happened to say. Let any single run expand it and the "schema" becomes a running log of every item any document has ever produced — the same shapeless, inconsistent output extraction was supposed to replace, just arrived at gradually rather than in one obvious mistake.

</details>

## 2. Reversible merges

Two mentions of the same underlying service — one from prose, one from a deploy log — get merged into a single canonical node. Someone proposes speeding this up: skip recording why the merge happened, since the merged node is right there and obviously correct. What's lost by skipping the reason?

<details>
<summary>Reveal the answer</summary>

A way for anyone else to check the decision. Without a stated reason sitting on the merge, there's nothing for a later reviewer to weigh if the merge is ever questioned — just a node that carries no explanation for why it exists in its current shape. Keeping the original mentions but dropping the reasoning behind combining them still leaves the merge impossible to evaluate or walk back.

</details>

## 3. Supersession, not silent overwrite

A claim extracted under schema v1 gets re-extracted under schema v2, which adds a field the v1 claim never had. A teammate suggests just adding the new field to the existing v1 claim directly, since it's the same underlying fact, only more complete now. What breaks if the team does that?

<details>
<summary>Reveal the answer</summary>

The link between a claim and the record of how it was actually produced. Editing the v1 claim in place leaves its provenance still pointing at schema v1, even though the field that got added couldn't have come from a v1 run — so that provenance record now describes something that never happened. Once one record has been quietly patched like that, every other provenance record in the graph becomes something to double-check rather than something to trust outright.

</details>
