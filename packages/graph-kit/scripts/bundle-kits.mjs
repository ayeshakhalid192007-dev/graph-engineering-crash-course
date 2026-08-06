#!/usr/bin/env node
// Copies the kits into this package right before it is packed or published.
//
// The kits live once, at the repo root, because the course reads them too — that is the
// single-source-of-truth rule. But the published package must carry ONLY the kits, their
// specs, and the CLI — not the course. So the copy is a build artifact: generated on
// `npm pack` / `npm publish`, gitignored, never edited by hand.
//
//   npm run bundle    # refresh the copy without packing

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const pkgDir = path.resolve(here, "..");
const repoRoot = path.resolve(pkgDir, "..", "..");

// Everything the CLI reads at run time. Nothing else ships.
//
// `patterns/` comes along whole rather than just registry.yaml: a kit installed from npm
// should carry the one-page spec explaining what the pattern is for, otherwise the user
// has the implementation and no statement of the problem it solves.
const ASSETS = [
  ["starters", "starters"],
  ["patterns", "patterns"],
  ["LICENSE", "LICENSE"],
];

function fail(msg) {
  console.error(`bundle-kits: ${msg}`);
  process.exit(1);
}

if (!fs.existsSync(path.join(repoRoot, "starters", "_template", "PATTERN.md"))) {
  fail(`cannot find starters/_template/PATTERN.md above ${pkgDir} — run this from a full checkout.`);
}

for (const [from, to] of ASSETS) {
  const src = path.join(repoRoot, from);
  const dest = path.join(pkgDir, to);
  if (!fs.existsSync(src)) fail(`missing source: ${from}`);
  fs.rmSync(dest, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.cpSync(src, dest, { recursive: true });
}

const kits = fs
  .readdirSync(path.join(pkgDir, "starters"), { withFileTypes: true })
  .filter((e) => e.isDirectory() && e.name !== "_template").length;

const specs = fs
  .readdirSync(path.join(pkgDir, "patterns"))
  .filter((f) => f.endsWith(".md") && f !== "README.md" && f !== "pattern-template.md").length;

// A mismatch here means the registry, the specs, and the kits have drifted apart. Better
// to fail at publish time than to ship a package whose `list` output promises a kit the
// tarball doesn't contain.
if (kits !== specs) {
  fail(`staged ${kits} kits but ${specs} specs — these must match. Run validate-registry.mjs.`);
}

console.log(`bundle-kits: staged ${kits} kits + ${specs} specs + the blank template into ${path.relative(repoRoot, pkgDir)}`);
