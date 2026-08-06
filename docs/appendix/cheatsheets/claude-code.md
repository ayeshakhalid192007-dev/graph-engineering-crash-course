# Cheatsheet · Claude Code

Everything this course asks you to write in Claude Code, collected on one page. This is a lookup sheet for people who have already worked through the steps — it repeats shapes, not explanations. For why any of it exists, go back to the step or the kit it came from.

## Where files go

| Path | What lives there |
| --- | --- |
| `.claude/skills/<skill-name>/SKILL.md` | One skill. The directory name is the skill name. |
| `.claude/agents/<agent-name>.md` | One subagent, as a single file. |
| `schema.example.json` | The kit's fixed type list, at the kit root. |
| `sample-input.md` | The document or record a kit's skill reads by default. |

Claude Code picks both up from the path alone. There is no separate registration file, and nothing has to be listed anywhere else before it can be invoked.

## Skill front matter

```yaml
---
name: extract-facts
description: Extracts Service/Incident/Cause facts from an incident-report document against a fixed schema, rejecting anything the schema doesn't define
model: claude-opus-4-1-20250805
temperature: 0
tools: [Read, Write]
---
```

| Field | Notes |
| --- | --- |
| `name` | Matches the containing directory. |
| `description` | One sentence, written so a reader can tell what gets rejected, not just what gets produced. |
| `model` | Pin it when a kit's behavior depends on the model; omit to inherit. |
| `temperature` | Every kit in this course sets `0`. Extraction and checking are not places you want sampling variety. |
| `tools` | Least privilege. An extraction skill gets `[Read, Write]`; a verifier gets `[Read]` only, so it cannot repair what it is supposed to be judging. |

## Skill body

The kits use the same five headings in the same order:

| Heading | Holds |
| --- | --- |
| `## Instructions` | Numbered steps, in execution order. Step 1 is nearly always "read the schema before you read anything else." |
| `## Input` | Each file the skill opens, and what it is for. |
| `## Output` | Each artifact written, plus anything printed for a human. |
| `## Example Usage` | A concrete run with its expected result — **including the expected drops**. |
| `## Validation` | Which agent or mode re-checks this skill's output. |

Two habits carry most of the weight across every kit:

- **Freeze the schema at step 1.** Say so in the instructions. A skill told to read the type list first, and to treat it as fixed for the rest of the run, is much harder to talk into inventing a type mid-extraction.
- **Make the drop list an output, not a side effect.** A run that reports only what it kept cannot be reviewed. Every extraction kit here prints what it rejected and which check each item failed.

## Subagent front matter

```yaml
---
name: graph-verifier
context: verify-graph-output
tools: [Read]
---
```

Body headings used by the kits: `## Purpose`, `## Inputs`, `## Validation Steps`, `## Output`, `## Example`.

A verifier in this course is written to do an independent pass, not to read the producing skill's self-report and agree with it. Three rules make that real:

1. It re-derives the allowed set from the schema itself.
2. It reads the output file directly, rather than being handed a summary.
3. It cross-checks the producing skill's claimed drop list against what it actually found, and flags any disagreement as its own finding — a mismatch is evidence the run's self-report cannot be trusted.

Give it `tools: [Read]`. A verifier that can write can quietly fix what it should be reporting.

## Verdict shape

Checkers in this course report a decision plus the single piece of evidence it rested on:

```text
PASS/FAIL: FAIL

- affected: INC-4482 -> "Priya Raman" — FAIL: endpoint type is Person,
  not Service. "affected" must run Incident -> Service.
  Fix: drop this relationship; Person is not a schema entity type.
```

Name the rule broken and the fix. A bare `FAIL` sends the reader back to re-run the check by hand to find out what happened.

## Invoking

Claude Code invocation is conversational — ask for the skill by name and name the files it should work on:

```text
Run the extract-facts skill on sample-input.md using schema.example.json.
```

Then run the verifier as its own turn. Keeping the two apart is the point: a producer asked to check itself in the same breath tends to grade its own work generously.

## Kits with a Claude Code implementation

All 23. The seven core kits ship a Claude Code implementation and an OpenCode one; the other sixteen ship Claude Code plus a `PORTING.md`. See [`starters/README.md`](../../../starters/README.md) for the split, and [`opencode.md`](opencode.md) for the other half of the pair.
