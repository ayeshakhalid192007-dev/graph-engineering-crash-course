#!/usr/bin/env node
// Fails if any relative markdown link in docs/, patterns/, starters/, resources/,
// or the root-level .md files points at a file that doesn't exist.
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, extname, dirname, resolve } from "node:path";

const ROOTS = ["docs", "patterns", "starters", "resources", "."];
const LINK_RE = /\[[^\]]*\]\((\.{1,2}\/[^)#\s]+|[^)#\s:]+\.md)(#[^)]*)?\)/g;

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (entry === "node_modules" || entry === ".git" || entry === "web") continue;
    const p = join(dir, entry);
    const s = statSync(p);
    if (s.isDirectory()) walk(p, out);
    else if (extname(p) === ".md") out.push(p);
  }
  return out;
}

function main() {
  const files = new Set();
  for (const root of ROOTS) {
    if (!existsSync(root)) continue;
    if (statSync(root).isDirectory()) walk(root).forEach((f) => files.add(f));
    else if (extname(root) === ".md") files.add(root);
  }

  let broken = 0;
  for (const file of files) {
    const text = readFileSync(file, "utf8");
    LINK_RE.lastIndex = 0;
    let match;
    while ((match = LINK_RE.exec(text)) !== null) {
      const target = match[1];
      if (target.startsWith("http")) continue;
      const resolved = resolve(dirname(file), target);
      if (!existsSync(resolved)) {
        console.error(`broken link in ${file}: "${target}" -> ${resolved}`);
        broken++;
      }
    }
  }

  if (broken > 0) {
    console.error(`\nlink-check: ${broken} broken link(s) found.`);
    process.exit(1);
  }
  console.log(`link-check: ${files.size} files checked, 0 broken links.`);
}

main();
