---
name: graph-verifier
context: verify-graph-output
---

# graph-verifier

A validation agent for this pattern's output.

## Purpose

<!-- Describe what this agent verifies about the pattern's output -->

This agent checks that the output produced by the pattern:
- Matches the schema defined in `schema.example.json`
- Contains all required fields and entity/relationship types
- Has no structural errors or type mismatches
- Follows the pattern's input/output contract

## Inputs

The agent receives:
- The output JSON from the skill
- The `schema.example.json` specification
- Any additional context about what was expected

## Validation Steps

<!-- Outline the validation logic -->

1. Parse the output JSON
2. Compare against the schema structure
3. Check for required fields
4. Verify entity/relationship types match the schema
5. Report any violations with specific line numbers and fixes

## Output

The agent produces:
- A validation report (pass/fail)
- Specific errors or warnings, if any
- Suggestions for fixing violations

## Example

```
<!-- Provide an example validation report showing both passing and failing cases -->
```
