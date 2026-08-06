#!/usr/bin/env node
// Checks every starter kit satisfies the Graph Ready checklist shape (§19):
// this is a structural proxy check (files exist, required sections present),
// not a semantic check that the kit's logic is correct — that's covered by
// each kit's own README quickstart being manually runnable.
import { readFileSync, existsSync, readdirSync } from "node:fs";

const CHECKLIST_SECTIONS = [
  "What it does",
  "Failure mode if skipped",
];

function main() {
  const kits = readdirSync("starters").filter(
    (d) => d !== "_template" && d !== "README.md" && existsSync(`starters/${d}/PATTERN.md`)
  );
  let violations = 0;

  for (const kit of kits) {
    const patternMd = readFileSync(`starters/${kit}/PATTERN.md`, "utf8");
    for (const section of CHECKLIST_SECTIONS) {
      if (!patternMd.includes(section)) {
        console.error(`${kit}: PATTERN.md missing required section "${section}"`);
        violations++;
      }
    }
    if (!existsSync(`starters/${kit}/README.md`)) {
      console.error(`${kit}: missing README.md`);
      violations++;
    }
  }

  if (violations > 0) {
    console.error(`\ngraph-ready-audit: ${violations} violation(s) found.`);
    process.exit(1);
  }
  console.log(`graph-ready-audit: ${kits.length} kits audited, 0 violations.`);
}

main();
