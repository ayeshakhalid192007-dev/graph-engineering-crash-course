# Solution · Project 1: Nodes and Edges by Hand

This walks through one way to complete [Project 1](../01-nodes-and-edges-by-hand.md) using an invented two-book reading list. Your own book and author will differ — check your file against the shape of this one, not the specific titles.

## The reading list

- **The Glass Orchard**, by Marisol Aduba — the book you've already looked up.
- **Low Tide at Cassin Point** — on the list, author not looked up yet.

## The finished `reading-list.json`

```json
{
  "nodes": [
    { "id": "book-1", "type": "Book", "title": "The Glass Orchard" },
    { "id": "author-1", "type": "Author", "name": "Marisol Aduba" },
    { "id": "book-2", "type": "Book", "title": "Low Tide at Cassin Point" }
  ],
  "edges": [
    { "from": "book-1", "label": "written_by", "to": "author-1" }
  ]
}
```

## Why it's shaped this way

**Three nodes, one edge.** `book-1` and `author-1` are connected; `book-2` sits by itself. That's not a gap in the file — it's an accurate statement that nobody has looked up who wrote *Low Tide at Cassin Point* yet. Adding a placeholder author, or a `written_by` edge to an empty string, would replace an honest "unknown" with a false "known."

**The label is `written_by`, not `related_to`.** `written_by` is a claim you could falsify by checking the book's copyright page: either Marisol Aduba wrote it, or she didn't. `related_to` would technically connect the same two nodes but wouldn't tell you what to go check — it could mean "wrote it," "translated it," "reviewed it," or nothing in particular.

**Direction matters.** The edge runs `book-1 → author-1`, not the reverse. `The Glass Orchard --written_by--> Marisol Aduba` and `Marisol Aduba --written_by--> The Glass Orchard` read almost the same to a human skimming past, but only one of them is the sentence anyone actually meant — a `written_by` edge pointing from the author to the book would claim the author was written by the book, which is nonsense the direction is supposed to rule out automatically.

## Checking your own attempt

- Does your file have a node for the book and a separate node for the author, rather than cramming both into one node's fields?
- Is your edge's label something you could imagine disputing with evidence, not just a vague connector?
- Does the second book in your file genuinely have no edge, or did you add a guess "just to fill it in"?
- Could a stranger read your JSON with no other context and correctly restate the one fact it claims?
