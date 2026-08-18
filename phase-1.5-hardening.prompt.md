---
mode: agent
description: Phase 1.5 — idempotency, reserved span column, and the Phase 1 test suite
---

Three changes before Phase 2. Do all three, then stop.

## 1. IDEMPOTENCY ON EVENTS

You flagged this correctly — the SDK adds retries in Phase 2, so a timeout retry
would double-count. Add a client-generated `event_id` (UUID string) column with a
UNIQUE constraint on the events table.

POST /v1/events accepts it as an optional field, generates one server-side when
absent, and silently skips duplicates rather than erroring — return the existing
row's id in `event_ids` so the SDK sees success either way. Add a test proving
the same event_id posted twice results in one row.

## 2. RESERVED COLUMN FOR MULTI-AGENT SPANS

Add a nullable `parent_span_id` column to the events table, alongside session_id.
Leave it unpopulated. It is the anchor for future multi-agent span nesting —
supervisor to sub-agent trees in orchestration frameworks like LangGraph or
CrewAI, where session_id groups a run and parent_span_id builds the tree within
it.

Document in handoff.md that it is intentionally reserved so no later phase
removes it as dead weight. Do not index it and do not build nesting logic now.

## 3. REAL PYTEST SUITE FOR PHASE 1

tests/ is empty and `pytest -q` still reports "no tests ran". Write a
re-runnable suite — use api.db.reset_engine() with a temporary database per test
so it never depends on a fresh aiops.db, and never leaves a script that fails on
second run.

Cover:
- auth: 401 on missing token, 401 on wrong token, open mode when the key is unset
- events: single, batch, unknown field 422, duplicate event_id dedup
- checkup due logic: not_yet_due, interval_elapsed, already_completed, snoozed
- feedback: save, snooze, dismiss, unknown checkup_id 404
- repository read side: every read function against seeded rows

Confirm `pytest -q` reports passing tests with a real count.

Then update handoff.md — including the revised Phase 2 contract with the new
event_id field and dedup behavior — and stop. Do not start Phase 2.
