---
mode: agent
description: Phase 3.5 — reset the database after the question-key rename, before Phase 4
---

Delete `aiops.db` and recreate it. The question-key rename means the existing
database holds two vocabularies, and Phase 4's dashboard would show both. There
is no demo data worth keeping yet, so a clean database is the right call rather
than a migration.

Confirm the file is gone, the schema recreates on next startup, and note in
`handoff.md` that the database was reset here so Phase 5's seed script is the
first thing that populates it.

Then stop. Do not start Phase 4.
