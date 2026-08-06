# Part 3 Flashcards

This Part introduced six terms: schema, extraction, resolution, reversible merge, provenance, and supersession. Cover the definition column and see whether you can recall each one before checking.

| Term | Definition |
| --- | --- |
| **Schema** | A fixed list of allowed entity and relationship types, settled on before extraction runs, so an item's fit is a checkable yes-or-no rather than a judgment call made fresh per document. |
| **Extraction** | Turning a raw source into nodes and edges checked against a predefined schema — anything outside the schema's allowed types is dropped at the gate, not reshaped to slip through. |
| **Resolution** | Recognizing that two separate mentions, pulled from different sources, point at one real-world thing, and combining them into a single node without losing the trace of either original mention. |
| **Reversible merge** | A merge that leaves the mentions it combined, plus a stated reason for combining them, still attached to the result — so the decision stays reviewable and, if wrong, undoable. |
| **Provenance** | The trail carried on a claim — source document, extraction run, schema version — that lets someone verify where the claim actually came from instead of just taking it on faith. |
| **Supersession** | Replacing an outdated claim with a newer, linked one while leaving the outdated claim exactly as recorded, its status flipped rather than its content edited or the record removed. |
