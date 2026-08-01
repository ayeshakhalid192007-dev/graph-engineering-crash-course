#!/usr/bin/env node
// Enforces graph-plan.md §2.1 rule 2: no run of 8+ consecutive words in any
// docs/ page may match an 8+ word run in a cached source text.

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, extname } from "node:path";

const DOCS_DIR = "docs";
const CACHE_DIR = ".originality-cache";
const MIN_RUN = 8;
const ALLOWED_QUOTE_MARKER = "<!-- attributed-quote:steinberger -->";

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    const s = statSync(p);
    if (s.isDirectory()) out.push(...walk(p));
    else if (extname(p) === ".md") out.push(p);
  }
  return out;
}

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);
}

function ngrams(tokens, n) {
  const set = new Set();
  for (let i = 0; i + n <= tokens.length; i++) set.add(tokens.slice(i, i + n).join(" "));
  return set;
}

function stripAttributedQuoteBlocks(text) {
  const lines = text.split("\n");
  const kept = [];
  let skipping = false;
  for (const line of lines) {
    if (line.includes(ALLOWED_QUOTE_MARKER)) { skipping = true; continue; }
    if (skipping && line.trim() === "") { skipping = false; continue; }
    if (!skipping) kept.push(line);
  }
  return kept.join("\n");
}

function main() {
  if (!existsSync(DOCS_DIR)) {
    console.error(`originality-check: ${DOCS_DIR}/ not found`);
    process.exit(1);
  }

  const docFiles = walk(DOCS_DIR);
  let sourceNgrams = null;

  if (existsSync(CACHE_DIR)) {
    sourceNgrams = new Set();
    for (const f of walk(CACHE_DIR)) {
      for (const g of ngrams(tokenize(readFileSync(f, "utf8")), MIN_RUN)) sourceNgrams.add(g);
    }
  } else {
    console.warn(
      `originality-check: ${CACHE_DIR}/ not present — skipping cross-source check, ` +
      `running self-duplication check only. See scripts/README.md.`
    );
  }

  let violations = 0;
  const seenBySelf = new Map();

  for (const file of docFiles) {
    const cleaned = stripAttributedQuoteBlocks(readFileSync(file, "utf8"));
    const grams = ngrams(tokenize(cleaned), MIN_RUN);

    for (const g of grams) {
      if (sourceNgrams && sourceNgrams.has(g)) {
        console.error(`originality violation in ${file}: matches cached source text: "${g}"`);
        violations++;
      }
      if (seenBySelf.has(g) && seenBySelf.get(g) !== file) {
        console.error(`self-duplication in ${file}: matches ${seenBySelf.get(g)}: "${g}"`);
        violations++;
      } else if (!seenBySelf.has(g)) {
        seenBySelf.set(g, file);
      }
    }
  }

  if (violations > 0) {
    console.error(`\noriginality-check: ${violations} violation(s) found.`);
    process.exit(1);
  }
  console.log(`originality-check: ${docFiles.length} files checked, 0 violations.`);
}

main();
