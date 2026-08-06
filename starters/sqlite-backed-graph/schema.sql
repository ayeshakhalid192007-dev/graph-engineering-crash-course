-- schema.sql -- sqlite-backed-graph starter kit
--
-- Two tables, nodes and edges, joined by a foreign key. Running this file
-- against a fresh database creates both tables and loads this kit's
-- worked example in one step:
--
--   sqlite3 graph.db < schema.sql
--
-- or, if the sqlite3 CLI isn't installed, the same thing through Python's
-- built-in sqlite3 module:
--
--   python3 -c "import sqlite3; sqlite3.connect('graph.db').executescript(open('schema.sql').read())"
--
-- SQLite ignores REFERENCES constraints unless a connection turns
-- enforcement on for itself -- this pragma only affects the connection
-- that ran this script, so any tool opening graph.db later (including
-- the query-graph skill and graph-verifier agent) must set it again
-- before relying on the foreign keys below. See README.md.

PRAGMA foreign_keys = ON;

CREATE TABLE nodes (
  id   TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  data TEXT NOT NULL  -- JSON object; type-specific fields live here, since
                       -- SQLite has no native column type for one
);

CREATE TABLE edges (
  id                TEXT PRIMARY KEY,
  from_id           TEXT NOT NULL REFERENCES nodes(id),
  to_id             TEXT NOT NULL REFERENCES nodes(id),
  label             TEXT NOT NULL,
  source_doc        TEXT NOT NULL,
  extraction_run_id TEXT NOT NULL,
  schema_version    TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- Worked example: the Elm Street tool-cabinet scenario this course
-- already built once in docs/08-part-6-one-graph-end-to-end/step-15
-- -build-the-same-graph-twice.md, here loaded as rows instead of held
-- in an agent's working memory for one pass. Four people, two tools,
-- five messages worth of owns/borrowed/returned edges.
--
-- "Jay" (named in message 2) and "Jason R." (named in message 3) were
-- already resolved to a single Person before this file was written --
-- that merge is a different kit's job (alias-merge-with-trail); this
-- kit only has to store the already-resolved result and answer
-- questions against it correctly. Both surface forms are kept on the
-- one node's data column so the resolution stays visible.
-- ---------------------------------------------------------------------

INSERT INTO nodes (id, type, data) VALUES
  ('person-kavita',    'Person', '{"name":"Kavita","aliases":["Mrs K"]}'),
  ('person-marcus',    'Person', '{"name":"Marcus","aliases":[]}'),
  ('person-jason',     'Person', '{"name":"Jason R.","aliases":["Jay"]}'),
  ('person-deepa',     'Person', '{"name":"Deepa","aliases":[]}'),
  ('tool-ladder',      'Tool',   '{"name":"ladder"}'),
  ('tool-stud-finder', 'Tool',   '{"name":"stud finder"}');

-- Edge ids climb e1..e5 in the same order the five source messages were
-- posted, which is what lets a query on this table answer "which of two
-- edges on the same tool happened later" without a separate timestamp
-- column -- see query-graph's SKILL.md for the query that leans on this.

INSERT INTO edges (id, from_id, to_id, label, source_doc, extraction_run_id, schema_version) VALUES
  ('e1', 'person-kavita', 'tool-ladder',      'owns',     'elm-street-chat.md', 'elm-street-extract-m1', 'v1'),
  ('e2', 'person-jason',  'tool-ladder',      'borrowed', 'elm-street-chat.md', 'elm-street-extract-m2', 'v1'),
  ('e3', 'person-jason',  'tool-ladder',      'returned', 'elm-street-chat.md', 'elm-street-extract-m3', 'v1'),
  ('e4', 'person-marcus', 'tool-stud-finder', 'owns',     'elm-street-chat.md', 'elm-street-extract-m4', 'v1'),
  ('e5', 'person-deepa',  'tool-stud-finder', 'borrowed', 'elm-street-chat.md', 'elm-street-extract-m5', 'v1');
