# @graph-engineering-kits/graph-kit

Install a ready-to-run graph pattern kit into any project. One command, no clone, no course.

```bash
npx @graph-engineering-kits/graph-kit list
npx @graph-engineering-kits/graph-kit document-to-facts
```

Each kit is a working implementation of one pattern for building and operating knowledge graphs that agents can actually use — extraction, resolution, provenance, bounded retrieval, grounded checking, governance, and storage. Kits run against a small worked example that ships with them. **No API keys and no external services** are needed to try one.

From the [Graph Engineering Crash Course](https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course).

## Usage

```text
graph-kit list                      show all 23 kits, grouped by tier
graph-kit <kit-name>                install that kit into the current directory
graph-kit new <name>                scaffold a blank kit from the template
```

| Option | |
| --- | --- |
| `--dir <path>` | Where to install (default: current directory) |
| `--tool <t>` | `claude`, `opencode`, or `both` (default: whatever the kit ships) |
| `--force` | Overwrite an existing directory |
| `--dry-run` | Print what would be written, write nothing |
| `--help` | Full help |
| `--version` | Print the version |

## The two tiers

**Core kits (7)** ship a Claude Code implementation, an OpenCode implementation, and a verifier subagent:

`document-to-facts` · `alias-merge-with-trail` · `receipt-per-edge` · `task-scoped-retrieval` · `grounded-triple-checker` · `counter-metric-loop` · `sqlite-backed-graph`

**Extended kits (16)** ship a Claude Code implementation plus a `PORTING.md` documenting what a port to another tool needs — config shape, file inputs, and how the skill-invocation model differs.

`graph-kit list` marks which is which. Asking for `--tool opencode` on an extended kit tells you so and points at the porting notes rather than failing silently.

## What you get

```text
document-to-facts/
├── SPEC.md                 what the pattern is for (category, stage, cost)
├── PATTERN.md              inputs, outputs, failure mode if you skip it
├── README.md               quickstart, expected output, troubleshooting
├── schema.example.json     the fixed type list
├── sample-input.md         the worked example's source document
├── .claude/
│   ├── skills/…/SKILL.md   the Claude Code skill
│   └── agents/…            the verifier subagent
└── opencode/               core kits only
    ├── opencode.json.example
    └── skills/…/SKILL.md
```

Read `SPEC.md`, then `PATTERN.md`, then `README.md`. The READMEs list expected output **including what should be rejected** — for extraction kits, seeing the right things dropped is the behavior worth checking.

## The 23 patterns

| Category | Patterns |
| --- | --- |
| A · Extraction | `document-to-facts` `code-change-to-graph` `conversation-to-claims` |
| B · Resolution | `alias-merge-with-trail` `confidence-scored-dedup` `reversible-merge-audit` |
| C · Provenance | `receipt-per-edge` `supersession-chain` `versioned-schema-log` |
| D · Subgraph | `task-scoped-retrieval` `budget-capped-subgraph` `conflict-aware-bundle` |
| E · Checker | `grounded-triple-checker` `contradiction-detector` `early-victory-guard` |
| F · Governance | `counter-metric-loop` `arbitration-edge` `audit-loop` `anchor-and-freeze` |
| G · Storage | `sqlite-backed-graph` `file-graph-for-small-teams` `postgres-backed-graph` `neo4j-at-scale` |

`postgres-backed-graph` and `neo4j-at-scale` are reasoning walkthroughs — they do not connect to a live database. `sqlite-backed-graph` ships a real `schema.sql` that loads as-is.

## Requirements

Node 18+. Claude Code or OpenCode to run a kit's skill.

## Contributing

Kits live at [`starters/`](https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course/tree/main/starters) in the course repo — that is the single source of truth. This package bundles a copy at publish time. Fixes and new patterns go through [CONTRIBUTING.md](https://github.com/ayeshakhalid192007-dev/graph-engineering-crash-course/blob/main/CONTRIBUTING.md).

MIT.
