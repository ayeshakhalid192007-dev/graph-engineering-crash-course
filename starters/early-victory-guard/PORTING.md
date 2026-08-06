# Porting `early-victory-guard` to OpenCode

This kit ships one Claude Code skill,
`.claude/skills/gate-task-completion/SKILL.md`. No OpenCode equivalent
ships with this kit; here's what porting it would take.

## Config file location

Claude Code finds this skill from its path under `.claude/skills/` alone.
OpenCode needs an `opencode.json` at the kit root declaring the skill as
a tool and giving it a workflow step, matching the shape
`starters/receipt-per-edge/opencode/opencode.json.example` uses for its
`attach-receipts` skill:

```json
{
  "tools": [
    { "name": "gate-task-completion", "type": "skill", "path": "skills/gate-task-completion/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      { "name": "gate", "tool": "gate-task-completion", "input": { "done_signals": "proposed-done.json", "checker_log": "checker-run-log.json" } }
    ]
  }
}
```

This kit's `README.md` embeds the three proposed "done" signals and the
checker log as prose for a Claude Code model to read directly. Porting
means splitting those into `proposed-done.json` (each ticket's id and
resolution note) and `checker-run-log.json` (each log entry's task id and
result), since OpenCode workflow steps consume file paths rather than a
model reading a README section. In an OpenCode pipeline, the `gate` step
would typically sit as the very last step before whatever step actually
closes the task, so a `BLOCKED` result can halt the workflow run rather
than merely getting logged after the fact.

## Skill-invocation model

Claude Code invocation is conversational — a user asks for the
`gate-task-completion` skill by name against a proposed done signal and a
checker log, in the same turn, and the skill matches and reports inline.
OpenCode instead drives the equivalent through `workflow.steps`: the
`gate` step above names the tool and its inputs and would need its output
wired as a precondition on whatever step marks the task actually closed —
OpenCode workflows don't have an implicit "block the rest of the run"
behavior the way returning `BLOCKED` mid-conversation does in Claude
Code, so the port has to make that precondition explicit in the workflow
graph itself. The seven-step process in `SKILL.md` — read the proposed
done signal, read the checker log, search for an exact task-id match,
block on no match, block on a mismatched-but-similar id, pass through on
an exact match, report one outcome per task — becomes the body of the
`gate` step's handler.

## Tool-call syntax to translate

The `model: claude-opus-4-1-20250805`, `temperature: 0`, and
`tools: [Read, Write]` frontmatter fields are Claude-Code-specific.
OpenCode skill frontmatter uses a `context` field instead (see
`receipt-per-edge`'s OpenCode skill for the pattern) and takes its
file-access permissions from the `opencode.json` tool declaration rather
than from the skill file itself.

The detail most worth preserving on a port is step 5's exact-match
requirement — `HR-2258`'s block in this kit's worked example depends on
treating a log entry keyed to the look-alike id `HR-2255` as no coverage
at all, not a near-enough match. That's a plain string-equality check
with no model judgment involved, and it's tempting on a port to route
task-id matching through the same general-purpose comparison logic an
OpenCode workflow might already use elsewhere for fuzzy ticket lookup.
Doing that would silently turn this pattern's hard gate into a soft one —
the whole point of `early-victory-guard` is that "close enough" isn't
close enough, so the id match needs to stay a strict equality check
wherever it lands in the ported workflow.
