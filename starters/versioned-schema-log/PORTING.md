# Porting `versioned-schema-log` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/log-schema-version/SKILL.md`. No OpenCode equivalent
ships with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/`
alone. OpenCode needs an `opencode.json` at the kit root declaring the
skill as a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "log-schema-version", "type": "skill", "path": "skills/log-schema-version/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "log", "tool": "log-schema-version", "input": { "schemaHistory": "schema-history.json", "runs": "runs.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the schema history (two versions, their
field lists and introduction dates) and the run list as prose tables for
a Claude Code model to read directly. Porting means splitting those into
`schema-history.json` and `runs.json`, since OpenCode workflow steps
consume file paths rather than a model reading a README section by hand.
Because a new schema version and new runs both tend to arrive as ongoing
pipeline events rather than one-off actions, an OpenCode port would also
benefit from a `schedule` or trigger entry on the `log` step, appending
to the log incrementally rather than re-deriving it from scratch each
time — Claude Code has no built-in equivalent; running this skill again
later just means asking it again with the updated inputs.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`log-schema-version` skill by name against a given schema history and
run list, in the same turn. OpenCode instead drives the equivalent
through `workflow.steps`: the `log` step above names the tool and its
inputs and runs structurally, triggered by the pipeline rather than by a
natural-language request. The seven-step process in `SKILL.md` — read
history, read runs, assign each run by date, keep field lists
per-version, catch orphaned runs, build entries, reconcile the count —
becomes the body of that step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The rule most worth preserving on the way over is step 3's date
comparison and step 4's refusal to merge field lists across versions —
both are plain data logic with nothing Claude-Code-specific about them,
so they port unchanged. The one place a port could quietly go wrong is
if "assign runs to versions" and "reconcile the total count" get split
into two separate workflow steps that could run out of order or against
stale intermediate data; keeping them as one atomic step, as `SKILL.md`
does here, avoids a log that silently drops a run between the two steps.
