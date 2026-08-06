# Porting `conversation-to-claims` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/transcript-to-claims/SKILL.md`. There's no shipped
OpenCode equivalent bundled with this kit — here's what porting it would
actually involve.

## Config file location

Claude Code finds this skill purely by its path under `.claude/skills/`.
OpenCode needs it declared in an `opencode.json` at the kit root, as a
named tool wired into a workflow step — following the same shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses:

```json
{
  "tools": [
    { "name": "transcript-to-claims", "type": "skill", "path": "skills/transcript-to-claims/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "extract", "tool": "transcript-to-claims", "input": { "transcript": "transcript.txt" } }
    ]
  }
}
```

The sample transcript, embedded directly in this kit's `README.md` for
Claude Code to read as prose, would need to become a standalone file
(e.g. `transcript.txt`) referenced by that `input.transcript` path —
OpenCode workflow steps take file paths, not README sections.

## Skill-invocation model

In Claude Code, a user or agent invokes this skill conversationally: "use
the transcript-to-claims skill on this transcript," and the model reads
`SKILL.md`'s instructions directly. In OpenCode, invocation runs through
the `workflow.steps` array — the `extract` step above names the tool and
its input, and OpenCode drives execution structurally rather than through
a natural-language request. The turn-by-turn walk this skill performs
(steps 1 through 7 in `SKILL.md`) would become the body of that step's
handler, executed once per workflow run rather than once per
conversational ask.

## Tool-call syntax to translate

`SKILL.md`'s frontmatter grants Claude-Code-specific settings —
`model: claude-opus-4-1-20250805`, `temperature: 0`,
`tools: [Read, Write]` — none of which OpenCode's skill frontmatter
uses. Following the pattern in `receipt-per-edge`'s OpenCode skill, this
would become a `context: pattern-implementation` field, with read/write
access granted through the `opencode.json` tool declaration instead of
the skill file itself.

One thing that ports over unchanged: the hedge-detection rule in step 4
("might," "I think," "not certain" set a `hedged: true` flag rather than
getting smoothed away) is plain extraction logic with no Claude-Code
syntax baked in — it moves into an OpenCode workflow handler exactly as
written. The one piece that needs rethinking rather than just
re-declaring is step 5's instruction not to resolve or merge overlapping
claims — in a multi-step OpenCode workflow it's worth making that
explicit as a comment on the `extract` step, since a later `resolve` step
could otherwise be tempted to fold that logic in early.
