# Example Pattern Starter Kit

A runnable starter kit for the **example-pattern** pattern. This kit demonstrates the pattern with a concrete scenario and sample data.

## Prerequisites

<!-- List what you need before running this kit (e.g. Python 3.11+, a Claude Code instance, etc.) -->

## Quick Start

<!-- Provide step-by-step instructions for running the example -->

1. Review `PATTERN.md` to understand what this pattern does.
2. Examine `schema.example.json` to see the data structure.
3. Follow the tool-specific instructions below to run the kit.

### Claude Code

<!-- Provide Claude Code-specific instructions -->

To use this kit in Claude Code:

1. Load the skill: `SKILL.md` in `.claude/skills/example-skill/`
2. Run the skill on the sample data
3. Inspect the output in the generated JSON

### OpenCode

<!-- Provide OpenCode-specific instructions -->

To use this kit in OpenCode:

1. Load the config: `opencode.json.example`
2. Run the specified operation
3. Check the results

## Expected Output

<!-- Describe what successful output looks like and how to interpret it -->

## Modifying the Example

To adapt this kit to your own data:

1. Replace the sample input with your own data
2. Update `schema.example.json` if your data structure differs
3. Re-run the skill and verify the output matches your schema

## Architecture

- `PATTERN.md` — Detailed pattern specification
- `schema.example.json` — Example data schema
- `.claude/skills/example-skill/SKILL.md` — Claude Code skill
- `.claude/agents/graph-verifier.md` — Validation agent
- `opencode/opencode.json.example` — OpenCode configuration
- `opencode/skills/example-skill/SKILL.md` — OpenCode skill

## Troubleshooting

<!-- Add troubleshooting section if relevant -->

## Next Steps

- Check `PORTING.md` (if this is an extended kit) for guidance on adapting this pattern to other tools.
- Review the pattern specification in `patterns/example-pattern.md` in the course repo.
