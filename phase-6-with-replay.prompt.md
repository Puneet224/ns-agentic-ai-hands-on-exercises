---
mode: agent
description: Phase 6 — offline SQLite spool, plus the --replay demo flag folded in
---

Two things, then Phase 6.

## 1. Fold `--replay` into Phase 6

The checkup demo being single-use is a real demo risk — one rehearsal run closes
it permanently and the live demo then shows "no checkup due".

Add a `--replay` flag to the demo script that reopens the pinned demo user's
checkup so the flow can be shown repeatedly. Document it in the README quickstart
next to the pinned ACF2 ID.

## 2. Accepted trade-offs, not open decisions

On the plaintext HTTP and unsalted `hash_user_id` items: **no action**. The
warnings, the `hash_salt` option, and the handoff notes are the right level for
this build. Record them as accepted trade-offs, not open decisions.

Disk space is no longer a concern — 7.63 GB free.

## Then run Phase 6 as specified

- SQLite spool at `.aiops_spool/spool.db`
- Cap by event count (default 10,000) with a dropped counter, not by file count
- Drain the spool on `init()`, not only on a successful flush cycle
- Retry the spool every 60 seconds so a recovered collector is picked up without
  a restart
- A demo script for the outage sequence: stop API → keep running the agent →
  restart API → backlog lands on the dashboard
- A test that simulates an outage and asserts every event arrives exactly once

Fix the head-of-line blocking defect while you are in there — a spool file that
always fails currently blocks every later file behind it.

---

Stop after Phase 6. Do not start Phase 7.
