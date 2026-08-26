# Cheatsheet · OpenCode

The OpenCode half of every dual-tool example in this course, on one page. Same purpose as the [Claude Code sheet](claude-code.md): shapes to copy, not concepts to learn.

## Where files go

| Path | What lives there |
| --- | --- |
| `opencode/opencode.json` | The config. Kits ship it as `opencode.json.example`; copy it before use. |
| `opencode/skills/<skill-name>/SKILL.md` | One skill. |

Unlike Claude Code, path alone is not enough here. A skill has to be declared in the config's `tools` array before any workflow step can call it.

## Config shape

```json
{
  "version": "1.0",
  "name": "document-to-facts-opencode",
  "description": "Schema-first extraction of Service/Incident/Cause facts from an incident report, with independent schema verification of the output",
  "tools": [
    { "name": "extract-facts", "type": "skill", "path": "skills/extract-facts/SKILL.md" }
  ],
  "workflow": {
    "steps": [
      {
        "name": "extract",
        "tool": "extract-facts",
        "input": { "document": "../sample-input.md", "schema": "../schema.example.json" },
        "output": "output.json"
      },
      {
        "name": "verify",
        "tool": "extract-facts",
        "mode": "verify",
        "input": { "output": "output.json", "schema": "../schema.example.json" }
      }
    ]
  }
}
```text

| Field | Notes |
| --- | --- |
| `tools[].path` | Relative to the `opencode/` directory. |
| `workflow.steps[].input` | Relative to `opencode/` too — hence the `../` when reaching kit-root files like the schema. |
| `workflow.steps[].mode` | Free-form. The skill reads it and branches. |
| `_comment` | Kits use this to say what the config wires up and to warn that paths need adjusting if the kit moves. JSON has no comment syntax; this is the convention these kits settled on. |

## Skill front matter

```yaml
---
name: extract-facts
description: OpenCode equivalent of the Claude Code extract-facts skill and graph-verifier agent — extracts and verifies Service/Incident/Cause facts from an incident report against a fixed schema
context: pattern-implementation
---
```text

`context` replaces Claude Code's `model`/`temperature`/`tools` trio. There is no per-skill tool allowlist, which is worth knowing when you port a verifier: the read-only guarantee you get from `tools: [Read]` in Claude Code has no direct equivalent here, and has to be carried by the skill's instructions instead.

## No subagents — use modes

This is the difference that shapes every port. OpenCode has no separate subagent file, so a Claude Code skill-plus-verifier pair becomes **one skill with two modes**, selected by the calling step:

| Claude Code | OpenCode |
| --- | --- |
| `.claude/skills/x/SKILL.md` | `### Mode: extract` |
| `.claude/agents/graph-verifier.md` | `### Mode: verify` |
| Two files, invoked in two turns | One file, two workflow steps |

Write the branch explicitly at the top of the instructions, and give it a default:

> Which mode you run in is set by the `mode` field in the calling workflow step; default to `extract` if `mode` is absent.

Both modes must read the same schema file. That is what keeps the two halves from drifting apart on what "allowed" means — the single thing this arrangement is most likely to get wrong.

**What the merge costs you.** Two files cannot accidentally share state; two modes of one file can. The independence a separate verifier gives you for free has to be maintained deliberately here: have `verify` re-read the output artifact from disk rather than carrying anything forward from the `extract` run in the same process.

## Porting checklist

The sixteen extended kits ship a `PORTING.md` covering these four points. When you write your own:

1. **Config file** — declare the skill in `tools`, give it a workflow step.
2. **Inputs as files** — OpenCode steps consume paths. Prose embedded in a kit README for a Claude Code model to read has to be split into real files first (`claims.json`, `new-evidence.json`, and so on).
3. **Invocation** — conversational request becomes a named `workflow.steps` entry.
4. **Verification** — subagent becomes a second step with `"mode": "verify"`.

## Kits with an OpenCode implementation

The seven core kits: `document-to-facts`, `alias-merge-with-trail`, `receipt-per-edge`, `task-scoped-retrieval`, `grounded-triple-checker`, `counter-metric-loop`, `sqlite-backed-graph`. The remaining sixteen ship Claude Code plus porting notes — a disclosed scope choice, explained in [`starters/README.md`](../../../starters/README.md).
