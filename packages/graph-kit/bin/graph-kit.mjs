#!/usr/bin/env node
// Installs a graph kit into the user's project.
// Replaces `git clone` + `cp -r starters/<pattern> .`, which needed the whole course.
//
//   npx @graph-engineering/graph-kit list
//   npx @graph-engineering/graph-kit document-to-facts
//   npx @graph-engineering/graph-kit new my-pattern --tool claude
//
// The kits are bundled into the tarball at publish time, so nothing is fetched at run
// time and nothing but the kits and their specs is downloaded.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Two layouts run this file: the published package (kits bundled beside bin/) and a
// checkout of the course repo (kits at the repo root, three levels up from bin/). Probe
// for the marker file rather than guessing, so both work unchanged.
function findAssetRoot() {
  const candidates = [path.resolve(__dirname, ".."), path.resolve(__dirname, "..", "..", "..")];
  for (const dir of candidates) {
    if (fs.existsSync(path.join(dir, "starters", "_template", "PATTERN.md"))) return dir;
  }
  return candidates[0];
}

const pkgRoot = findAssetRoot();
const startersDir = path.join(pkgRoot, "starters");
const patternsDir = path.join(pkgRoot, "patterns");
const registryPath = path.join(patternsDir, "registry.yaml");

const REPO_SLUG = "ayeshakhalid192007-dev/graph-engineering-crash-course";
const REPO_BLOB = `https://github.com/${REPO_SLUG}/blob/main`;
const INVOKE = "npx @graph-engineering/graph-kit";
const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;

function die(msg) {
  console.error(msg);
  process.exit(1);
}

// A relative path is friendlier right up until it escapes the cwd and turns into a stack
// of "../". Past that point the absolute path is the readable one.
function displayPath(target) {
  const rel = path.relative(process.cwd(), target);
  if (rel === "") return ".";
  return rel.startsWith("..") ? target : rel;
}

function parseArgs(argv) {
  const opts = { dir: process.cwd(), tool: null, force: false, dryRun: false };
  const positional = [];
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dir") opts.dir = path.resolve(argv[++i] ?? ".");
    else if (arg === "--tool") opts.tool = argv[++i] ?? "both";
    else if (arg === "--force") opts.force = true;
    else if (arg === "--dry-run") opts.dryRun = true;
    else if (arg === "--help" || arg === "-h") opts.help = true;
    else if (arg === "--version" || arg === "-v") opts.version = true;
    else if (arg.startsWith("-")) die(`Unknown flag "${arg}". Run with --help.`);
    else positional.push(arg);
  }
  if (opts.tool !== null && !["claude", "opencode", "both"].includes(opts.tool)) {
    die(`--tool must be claude, opencode, or both (got "${opts.tool}").`);
  }
  return { opts, positional };
}

function listKits() {
  if (!fs.existsSync(startersDir)) return [];
  return fs
    .readdirSync(startersDir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && e.name !== "_template")
    .map((e) => e.name)
    .sort();
}

// registry.yaml is a flat list of "- name:" blocks; this reads the one-line fields the
// CLI prints, without pulling in a YAML dependency. Same scoping limit as the course's
// scripts/validate-registry.mjs: if the registry ever grows a nested value, replace this
// rather than extend it.
function readRegistry() {
  if (!fs.existsSync(registryPath)) return new Map();
  const entries = new Map();
  let current = null;
  for (const line of fs.readFileSync(registryPath, "utf8").split("\n")) {
    const nameMatch = line.match(/^\s*-\s*name:\s*["']?([a-z0-9-]+)["']?\s*$/);
    if (nameMatch) {
      current = { name: nameMatch[1] };
      entries.set(current.name, current);
      continue;
    }
    if (!current) continue;
    const fieldMatch = line.match(/^\s+([a-z_]+):\s*["']?(.*?)["']?\s*$/);
    if (fieldMatch) {
      const [, key, raw] = fieldMatch;
      current[key] = raw === "true" ? true : raw === "false" ? false : raw;
    }
  }
  return entries;
}

// Whether a kit actually ships an OpenCode implementation, read from disk rather than
// from the registry's `core` flag — the flag says what tier the pattern is in, this says
// what is on disk. They should agree; trusting the disk means a mismatch degrades into a
// clear message instead of a crash.
function hasOpenCode(kit) {
  return fs.existsSync(path.join(startersDir, kit, "opencode"));
}

function hasClaude(kit) {
  return fs.existsSync(path.join(startersDir, kit, ".claude"));
}

function copyDir(src, dest, { skip = [], dryRun = false, onFile }) {
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (skip.includes(entry.name)) continue;
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      if (!dryRun) fs.mkdirSync(to, { recursive: true });
      copyDir(from, to, { skip: [], dryRun, onFile });
    } else {
      if (!dryRun) fs.cpSync(from, to);
      onFile?.(to);
    }
  }
}

function help() {
  console.log(`
graph-kit — install a graph pattern kit into your project

USAGE
  ${INVOKE} list                        show every kit, grouped by tier
  ${INVOKE} <kit-name>                  install that kit here
  ${INVOKE} new <name>                  scaffold a blank kit from the template

OPTIONS
  --dir <path>     where to install         (default: current directory)
  --tool <t>       claude | opencode | both (default: whatever the kit ships)
  --force          overwrite an existing directory
  --dry-run        print what would be written, write nothing
  --help, -h       this message
  --version, -v    print the version

EXAMPLES
  ${INVOKE} list
  ${INVOKE} document-to-facts
  ${INVOKE} sqlite-backed-graph --tool opencode
  ${INVOKE} receipt-per-edge --dir ./my-project --dry-run
  ${INVOKE} new my-own-pattern --tool claude

TIERS
  Core kits ship both a Claude Code and an OpenCode implementation.
  Extended kits ship Claude Code plus a PORTING.md describing what an
  OpenCode port would need. \`list\` marks which is which.

Course: https://github.com/${REPO_SLUG}
`.trim());
}

function cmdList() {
  const kits = listKits();
  if (kits.length === 0) die("No kits found. This package looks damaged — please reinstall.");
  const registry = readRegistry();

  const core = [];
  const extended = [];
  for (const kit of kits) (hasOpenCode(kit) ? core : extended).push(kit);

  const describe = (kit) => {
    const meta = registry.get(kit) ?? {};
    const bits = [meta.category, meta.stage, meta.cost && `cost: ${meta.cost}`].filter(Boolean);
    return `  ${kit.padEnd(28)} ${bits.join(" · ")}`;
  };

  console.log(`\n${kits.length} kits available.\n`);
  console.log(`CORE — Claude Code + OpenCode (${core.length})`);
  core.forEach((k) => console.log(describe(k)));
  console.log(`\nEXTENDED — Claude Code + PORTING.md (${extended.length})`);
  extended.forEach((k) => console.log(describe(k)));
  console.log(`\nInstall one:  ${INVOKE} <kit-name>`);
  console.log(`Full catalog: ${REPO_BLOB}/patterns/README.md\n`);
}

function suggestSimilar(name, kits) {
  const near = kits.filter((k) => k.includes(name) || name.includes(k) || k.split("-").some((p) => name.includes(p)));
  return near.slice(0, 3);
}

function cmdInstall(name, opts) {
  const kits = listKits();
  if (!kits.includes(name)) {
    const near = suggestSimilar(name, kits);
    const hint = near.length ? `\n\nDid you mean:\n${near.map((k) => `  ${k}`).join("\n")}` : "";
    die(`No kit named "${name}".${hint}\n\nRun \`${INVOKE} list\` to see all ${kits.length}.`);
  }

  const src = path.join(startersDir, name);
  const isCore = hasOpenCode(name);

  // Default to whatever the kit actually ships, so the common case needs no flag.
  let tool = opts.tool ?? (isCore ? "both" : "claude");

  // The one place the two tiers genuinely differ. An extended kit has no OpenCode
  // implementation to install, so asking for one is a real dead end — say so, say why,
  // and point at both the porting notes and a core kit that would work.
  if (tool === "opencode" && !isCore) {
    const alt = kits.filter((k) => hasOpenCode(k)).slice(0, 3);
    die(
      `"${name}" is an extended kit — it ships a Claude Code implementation only.\n\n` +
        `There is no OpenCode implementation to install. What ships instead is PORTING.md,\n` +
        `which documents what an OpenCode port needs: config shape, file inputs, and how\n` +
        `the skill-invocation model differs.\n\n` +
        `  Install it with the porting notes:  ${INVOKE} ${name}\n` +
        `  Read them first:                    ${REPO_BLOB}/starters/${name}/PORTING.md\n\n` +
        `Kits that do ship OpenCode:\n${alt.map((k) => `  ${k}`).join("\n")}`
    );
  }
  if (tool === "claude" && !hasClaude(name)) {
    die(`"${name}" has no .claude/ directory — this package looks damaged.`);
  }

  const dest = path.join(opts.dir, name);
  if (fs.existsSync(dest) && !opts.force) {
    die(`${displayPath(dest)} already exists. Pass --force to overwrite.`);
  }

  const skip = [];
  if (tool === "claude") skip.push("opencode");
  if (tool === "opencode") skip.push(".claude");

  const written = [];
  if (!opts.dryRun) {
    fs.rmSync(dest, { recursive: true, force: true });
    fs.mkdirSync(dest, { recursive: true });
  }
  copyDir(src, dest, { skip, dryRun: opts.dryRun, onFile: (p) => written.push(p) });

  // Ship the one-page spec alongside the implementation. Without it the user has a kit
  // and no statement of the problem it solves.
  const spec = path.join(patternsDir, `${name}.md`);
  if (fs.existsSync(spec)) {
    const specDest = path.join(dest, "SPEC.md");
    if (!opts.dryRun) fs.cpSync(spec, specDest);
    written.push(specDest);
  }

  const rel = displayPath(dest);
  const verb = opts.dryRun ? "Would install" : "Installed";
  console.log(`\n${verb} ${name} (${isCore ? "core" : "extended"}, --tool ${tool})`);
  console.log(`${rel}/  — ${written.length} files\n`);
  for (const f of written.slice(0, 12)) console.log(`  ${path.relative(dest, f)}`);
  if (written.length > 12) console.log(`  ... and ${written.length - 12} more`);

  if (opts.dryRun) {
    console.log(`\nDry run — nothing was written.\n`);
    return;
  }
  console.log(`
Next, in ${rel}/ :
  1. SPEC.md      what this pattern is for
  2. PATTERN.md   inputs, outputs, failure mode if skipped
  3. README.md    quickstart, expected output, troubleshooting
${!isCore ? "  4. PORTING.md   what a port to another tool needs\n" : ""}
No API keys or external services are needed to run the worked example.
`);
}

function cmdNew(name, opts) {
  if (!name) die(`Usage: ${INVOKE} new <name>`);
  if (!KEBAB.test(name)) {
    die(`"${name}" must be kebab-case: lowercase letters, digits, single hyphens.\ne.g. my-own-pattern`);
  }
  const src = path.join(startersDir, "_template");
  if (!fs.existsSync(src)) die("Template not found. This package looks damaged — please reinstall.");

  const dest = path.join(opts.dir, name);
  if (fs.existsSync(dest) && !opts.force) {
    die(`${displayPath(dest)} already exists. Pass --force to overwrite.`);
  }

  const tool = opts.tool ?? "both";
  const skip = [];
  if (tool === "claude") skip.push("opencode");
  if (tool === "opencode") skip.push(".claude");

  const written = [];
  if (!opts.dryRun) {
    fs.rmSync(dest, { recursive: true, force: true });
    fs.mkdirSync(dest, { recursive: true });
  }
  copyDir(src, dest, { skip, dryRun: opts.dryRun, onFile: (p) => written.push(p) });

  const rel = displayPath(dest);
  console.log(`\n${opts.dryRun ? "Would scaffold" : "Scaffolded"} ${name} (--tool ${tool})`);
  console.log(`${rel}/  — ${written.length} files\n`);
  if (opts.dryRun) return;
  console.log(`Fill in PATTERN.md first — what it does, its inputs and outputs, and what
breaks if you skip it. If the failure mode is hard to name, the pattern
probably isn't one yet.

Contributing it back: ${REPO_BLOB}/CONTRIBUTING.md
`);
}

function main() {
  const { opts, positional } = parseArgs(process.argv.slice(2));
  if (opts.help || (positional.length === 0 && !opts.version)) return help();
  if (opts.version) {
    const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "package.json"), "utf8"));
    return console.log(pkg.version);
  }

  const [command, ...rest] = positional;
  if (command === "list" || command === "ls") return cmdList();
  if (command === "new") return cmdNew(rest[0], opts);
  return cmdInstall(command, opts);
}

main();
