# Part 6 Quiz

Two questions ahead, Step 14 first and Step 15 second. Settle on your own answer before opening either reveal — both of these reward a specific answer over a general one.

## 1. The book club's reading log

An eight-member book club has met monthly for three years and wants to start tracking, properly this time, which member has actually read which of the group's picks — right now it lives in someone's memory and the occasional "wait, did you finish it?" in the group chat. The list grows by exactly one book a month, membership hasn't changed in over a year, and nobody has ever needed to prove *when* a member finished a book, only whether they did. Run this through the six pre-build questions. Which one ends it, and what should the club build instead of a graph?

<details>
<summary>Reveal the answer</summary>

It ends on the question about whether the relationship set is small, fixed, and table-shaped, or genuinely growing in a way a table can't hold. Eight members by however many books the club has read is exactly a grid — one row per member, one column per book, a checkmark in each cell for "read it" — and adding one column a month for years doesn't change that shape, it just makes the grid longer. Nothing here needs a schema, an extraction step, or a **pre-build checklist** entry about provenance, because nobody has ever needed to trace a "read" mark back to a specific message — a shared spreadsheet with one tab already does everything this group actually wants. The other five questions might have looked fine too; a single "no" on the table question is enough to close the case.

</details>

## 2. Two configurations, one silent disagreement

Two teammates each build a version of a small lending-tracker pipeline from the same five source messages, independently, without comparing notes first. One resolves two different names in the messages into a single person, on the reasoning that they clearly refer to the same borrower; the other, moving faster, leaves the two names as two separate people because nothing in its instructions explicitly required a resolution step. Neither configuration errors out — both run cleanly and both look, read side by side, like reasonable ways to build the same pipeline. What does comparing the two *final graphs* reveal that comparing the two *instructions* would not?

<details>
<summary>Reveal the answer</summary>

Reading the two prompts side by side wouldn't catch this, because neither one is wrong on its face — omitting an explicit resolution step isn't an error, it's a gap that only shows up in what gets produced. Diff the final graphs and it surfaces immediately: one version has a single person-node with both a borrow and a return edge attached, so the item correctly reads as available; the other has two separate person-nodes, one holding the borrow edge and the other holding nothing, so the item incorrectly reads as still out, because the edge that would close the loan is sitting on a node the checker never associates with the borrower. **Dual-tool parity** is a claim about output, and the only way to check a claim about output is to compare the output — two configurations that read as equally reasonable can still diverge the moment either one makes a silent judgment call the other didn't make the same way.

</details>
