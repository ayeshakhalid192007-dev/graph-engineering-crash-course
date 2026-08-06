# Porting `conflict-aware-bundle` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/bundle-conflicts/SKILL.md`. No OpenCode equivalent ships
with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/`
alone. OpenCode needs an `opencode.json` at the kit root declaring the
skill as a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "bundle-conflicts", "type": "skill", "path": "skills/bundle-conflicts/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "bundle", "tool": "bundle-conflicts", "input": { "draw": "task-draw.json", "contradictions": "known-contradictions.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the task-scoped draw (four nodes, two of
them undisputed) and the known contradiction as prose for a Claude Code
model to read directly. Porting means splitting those into
`task-draw.json` and `known-contradictions.json` — the latter naming
which claim ids each contradiction involves — since OpenCode workflow
steps consume file paths rather than a model reading a README section.
This step would typically sit right after the port of
`task-scoped-retrieval` in an OpenCode pipeline, taking its draw as
input.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`bundle-conflicts` skill by name against a draw and a contradiction list,
in the same turn, and the skill classifies and tags inline. OpenCode
instead drives the equivalent through `workflow.steps`: the `bundle` step
above names the tool and its inputs and runs as a distinct pipeline
stage between subgraph retrieval and whatever consumes the bundle next.
The eight-step process in `SKILL.md` — read the draw, read the known
contradictions, classify every node, pass undisputed nodes through
unchanged, include every side of each contradiction, never compute a
resolved value, tag with a stated reason, report in two groups — becomes
the body of that step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The rule that most needs to survive a port intact is step 5 and step 6
together: never drop a side of a contradiction because of a role label
like "primary," and never compute a resolved value in its place. Neither
depends on anything Claude-Code-specific, so the logic itself carries
over unchanged — but an OpenCode port that lets a later workflow step
(rather than this one) decide how to display "primary" versus "backup"
readings risks that later step quietly re-introducing the exact
resolved-value shortcut this pattern exists to prevent. Keeping the
tagging and the reporting in the same step, as `SKILL.md` does here,
keeps that risk contained to one place.
