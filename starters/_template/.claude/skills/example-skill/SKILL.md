---
name: example-skill
description: An example Claude Code skill demonstrating this pattern
model: claude-opus-4-1-20250805
temperature: 0
tools: []
---

# example-skill

<!-- Replace this with a concise description of what this skill does -->

## Instructions

You are a Claude Code skill implementing the [pattern-name] pattern. Your job is to:

<!-- 1. Clearly state the input: what the skill expects to read (e.g., a document, existing graph, schema) -->
<!-- 2. State the transformation: what you will do with that input -->
<!-- 3. State the output: what you will produce (e.g., entities, relationships, JSON) -->

## Input

<!-- Describe the input format and source -->

The skill receives:
- A sample input file (e.g., a document, a graph snapshot, user input)
- A schema definition (usually `schema.example.json`)

## Processing

<!-- Outline the algorithm or steps the skill will take -->

1. Read and parse the input
2. Apply the pattern logic (<!-- describe the core transformation -->)
3. Validate against the schema
4. Produce structured output

## Output

<!-- Describe the output format and structure -->

The skill produces:
- A JSON file matching the schema
- Structured entities and/or relationships
- Any validation errors or warnings

## Example Usage

```
<!-- Provide a concrete example of how to invoke this skill -->
```

## Validation

The companion agent (`graph-verifier.md`) validates that all output:
- Matches the schema
- Contains required fields
- Has no structural errors
