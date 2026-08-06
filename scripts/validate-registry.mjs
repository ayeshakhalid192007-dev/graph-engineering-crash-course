#!/usr/bin/env node
// Validates patterns/registry.yaml against the pattern spec files and starter kits.
//
// Scoping note: this parser is NOT a general YAML implementation. It handles
// exactly the shape patterns/registry.yaml uses — a top-level `patterns:` key
// holding a list of flat maps whose values are unquoted string or boolean
// scalars. No nesting, no anchors, no multi-line scalars, no quoting rules.
// graph-plan.md §23 names this file `registry.yaml`, so the extension stays;
// parsing it this way avoids adding a YAML dependency (and a root package.json)
// for one file. If the registry ever grows a nested value, this parser must be
// replaced rather than extended.
import { readFileSync, existsSync } from "node:fs";

function parseFlatYamlList(text) {
  const lines = text.split("\n");
  const items = [];
  let current = null;
  for (const line of lines) {
    if (/^\s*-\s+name:/.test(line)) {
      if (current) items.push(current);
      current = {};
    }
    const m = line.match(/^\s*-?\s*(\w+):\s*(.+?)\s*$/);
    if (m && current) {
      const [, key, rawVal] = m;
      current[key] = rawVal === "true" ? true : rawVal === "false" ? false : rawVal;
    }
  }
  if (current) items.push(current);
  return items;
}

function main() {
  const registryPath = "patterns/registry.yaml";
  if (!existsSync(registryPath)) {
    console.error("validate-registry: patterns/registry.yaml not found");
    process.exit(1);
  }
  const entries = parseFlatYamlList(readFileSync(registryPath, "utf8"));
  let errors = 0;

  if (entries.length === 0) {
    console.error("validate-registry: registry parsed to zero entries — the file is empty or its shape changed");
    process.exit(1);
  }

  const seen = new Set();
  for (const entry of entries) {
    if (!entry.name) {
      console.error("registry entry is missing a name");
      errors++;
      continue;
    }
    if (seen.has(entry.name)) {
      console.error(`registry lists "${entry.name}" more than once`);
      errors++;
    }
    seen.add(entry.name);

    for (const field of ["category", "stage", "cost"]) {
      if (!entry[field]) {
        console.error(`registry entry "${entry.name}" is missing "${field}"`);
        errors++;
      }
    }

    const specPath = `patterns/${entry.name}.md`;
    const kitPath = `starters/${entry.name}/PATTERN.md`;
    if (!existsSync(specPath)) {
      console.error(`registry entry "${entry.name}" has no spec at ${specPath}`);
      errors++;
    }
    if (!existsSync(kitPath)) {
      console.error(`registry entry "${entry.name}" has no starter kit at ${kitPath}`);
      errors++;
    }
    if (entry.core === true && !existsSync(`starters/${entry.name}/opencode/opencode.json.example`)) {
      console.error(`registry entry "${entry.name}" is marked core but has no opencode/ directory`);
      errors++;
    }
  }

  if (errors > 0) {
    console.error(`\nvalidate-registry: ${errors} error(s) found.`);
    process.exit(1);
  }
  console.log(`validate-registry: ${entries.length} patterns validated, 0 errors.`);
}

main();
