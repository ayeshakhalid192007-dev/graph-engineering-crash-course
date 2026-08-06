# Porting `code-change-to-graph` to OpenCode

This kit ships one Claude Code skill, `.claude/skills/diff-to-graph/SKILL.md`.
There's no shipped OpenCode equivalent in this kit (unlike the seven core
kits, which carry both) — these are the concrete changes porting it would
take.

## Config file location

Claude Code discovers this skill by its path alone:
`.claude/skills/diff-to-graph/SKILL.md`, no separate registration file.
OpenCode instead needs an explicit `opencode.json` at the kit root
declaring the skill as a tool and wiring it into a workflow step, the same
shape `starters/receipt-per-edge/opencode/opencode.json.example` uses for
its `attach-receipts` skill:

```json
{
  "tools": [
    { "name": "diff-to-graph", "type": "skill", "path": "skills/diff-to-graph/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "extract", "tool": "diff-to-graph", "input": { "diff": "...", "inventory": "..." } }
    ]
  }
}
```

The diff and the existing graph inventory, which this README embeds
inline for Claude Code to read directly, would need to move to files
referenced by that `input` block instead (e.g. `diff.patch` and
`inventory.json`), since OpenCode's workflow steps pass explicit file
paths rather than a model reading prose out of a README.

## Skill-invocation model

Claude Code loads `SKILL.md` and a user (or another agent) asks for it by
name in natural language — "use the diff-to-graph skill on this diff."
There's no separate registration step; the file's presence under
`.claude/skills/` is enough. OpenCode instead resolves skills through the
`tools` array in `opencode.json` and runs them as a named step in
`workflow.steps` — invocation is structural (a workflow step referencing a
tool name), not conversational. Porting this skill means the seven
numbered steps in `SKILL.md`'s **Instructions** section become the body
of a single workflow-step handler rather than something invoked by asking
for it in plain language.

## Tool-call syntax to translate

`SKILL.md`'s frontmatter (`model: claude-opus-4-1-20250805`,
`temperature: 0`, `tools: [Read, Write]`) is Claude-Code-specific — it
grants the skill file-read and file-write tool access and pins the model
directly in the skill definition. OpenCode skills instead declare a
`context` field (see `opencode/skills/attach-receipts/SKILL.md` in the
`receipt-per-edge` kit for the pattern) and get their tool access from the
surrounding `opencode.json` workflow configuration rather than from their
own frontmatter. Porting `diff-to-graph` means dropping the `model` /
`temperature` / `tools` frontmatter block and replacing it with a
`context: pattern-implementation` field, then moving file I/O permissions
into the `opencode.json` tool declaration instead.

The one behavioral rule in this skill that has no Claude-Code-specific
syntax to translate is step 3's "no hunk, no edge" rule (don't create a
`modifies` edge for anything the commit message mentions but no diff hunk
actually touches) — that logic is tool-agnostic and can be copied over
unchanged into an OpenCode workflow-step handler.
