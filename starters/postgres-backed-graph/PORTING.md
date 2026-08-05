# Porting `postgres-backed-graph` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/transact-graph-write/SKILL.md`. No OpenCode equivalent
ships with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/`
alone. OpenCode needs an `opencode.json` at the kit root declaring the
skill as a tool, plus a database connection the tool can reach — a
Postgres DSN referenced through an environment variable rather than
anything embedded in the skill file itself:

```json
{
  "tools": [
    { "name": "transact-graph-write", "type": "skill", "path": "skills/transact-graph-write/SKILL.md", "env": ["GRAPH_DB_URL"] }
  ],
  "workflow": {
    "steps": [
      { "name": "rollout-advance", "tool": "transact-graph-write", "input": { "edge": "checkout-v2-flag", "writer": "rollout-controller" } },
      { "name": "incident-rollback", "tool": "transact-graph-write", "input": { "edge": "checkout-v2-flag", "writer": "incident-bot" } }
    ]
  }
}
```

This kit's `README.md` embeds the table shape and write sequence as
prose for a Claude Code model to reason through directly. Porting means
pointing both workflow steps at the same live `edges` table over the
connection named by `GRAPH_DB_URL`, since OpenCode workflow steps act on
real state rather than a model walking through a described sequence.

## Skill-invocation model

Claude Code invocation is conversational — a single turn walks through
both `rollout-controller`'s and `incident-bot`'s writes together,
reasoning about their interaction as one narrated sequence. OpenCode
instead drives the equivalent through `workflow.steps`, and this
pattern's two writers map naturally onto two genuinely independent
steps — `rollout-advance` triggered by the rollout schedule,
`incident-rollback` triggered by an alert — that can fire concurrently
for real, rather than being narrated as concurrent by one model. The
eight-step process in `SKILL.md` — read inside a transaction, check the
version, commit or abort, re-read and recompute on abort, retry, never
interleave, log, report — becomes the shared body every writer's step
calls into, not logic that's easy to inline separately in each step's own
handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern), and this skill's
actual database access — currently just `Read`/`Write` tool calls a
Claude Code model composes against a described table — would need to
become a declared database tool in `opencode.json`, since a real
Postgres connection needs its own connection string, driver, and
transaction-isolation setting rather than a generic file read/write.

## Kit-specific porting risk

Because `rollout-advance` and `incident-rollback` are naturally two
independent OpenCode workflow steps rather than two writers narrated
inside one Claude Code turn, the real porting risk is each step's port
re-implementing its own "read version, write, commit" logic separately
instead of both calling one shared transactional write function. If
`incident-rollback`'s ported step is written in a hurry and skips the
version check that `rollout-advance`'s keeps — say, because someone
assumes an alert-triggered write should always win regardless of what
else is happening — the exact race this pattern exists to prevent
reappears, just relocated: not "no transactions at all" but "one of two
steps forgot to use one," and Copperlow Analytics loses the same
rollback all over again, this time from a system that was supposed to
have already fixed it.
