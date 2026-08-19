---
mode: agent
description: Phase 8 — the Notify view that closes the success vision, plus three reference documents in sdk/docs
---

Two pieces of work. Do them in order, then stop.

# PART 1 — The Notify view

The challenge's success vision ends with "notify people of new releases", and the
pain points mention "employees are often unaware of relevant tools". The system
already knows *who* to notify — it just never surfaces it. Close that gap.

Add a **Notify** tab to the dashboard. It identifies audiences and drafts the
message. It does not send anything — no email, no Teams, no integration. Say so
plainly in the UI.

## Three audiences, derived from data we already hold

**1. Users on an older agent version**
Query the version breakdown per agent. For any agent where more than one
`agent_version` has been seen, list the ACF2 IDs still on a non-latest version,
with their Business Group and Division and the date of their last event.

**2. Divisions with no adoption of an agent**
For a selected agent, list Business Groups and Divisions that appear in `users`
but have zero events for that agent. These are the teams who may not know it
exists — the pain point, made concrete.

**3. Users of a dark agent**
For each agent with no events in N days, list the people who used to use it.
They are the ones who can say why they stopped.

## Output

For each audience:

- a count and a table (ACF2 ID, Business Group, Division, last seen)
- a CSV download button
- a draft message in a copyable text area, generated from a template with the
  agent name, version, and audience filled in

Keep the message templates in `dashboard/notify.py` as plain strings with
placeholders — no LLM, no external calls. Three templates: version upgrade, new
tool introduction, win-back for a dark agent.

## Constraints

- All data access goes through the repository layer. Add read functions there if
  needed; no SQL in the UI.
- Honest empty states — "every user is on the latest version" is a real and good
  answer.
- Label the tab clearly as identification and drafting only. A judge must not
  think we are claiming to send email.
- Add tests for the new repository functions against the seeded dataset.

# PART 2 — Three reference documents in sdk/docs/

Create `sdk/docs/` and write three documents. Write them for a reader who has
never seen this project. Use real file paths, real function names, and real
commands taken from the codebase and from `handoff.md` — not invented ones.

## Document 1 — `sdk/docs/BUILD-JOURNEY.md`

How this project was built, start to finish.

Structure it phase by phase, following `handoff.md`, which is the record of what
actually happened. For each phase:

- what was built and why that came before the next thing
- the design decisions taken, and what was traded away for them — the repository
  layer, SQLite over PostgreSQL, lazy checkup evaluation over a scheduler,
  fail-safe over strict, no PyYAML, event-count spool cap over file count
- the reversals and what prompted them, in particular the identity fallback
  reversal in Phase 2.1 and the database resets
- the bugs the work surfaced (the `DocumentTooLarge` categorisation walking
  `__mro__`, the test suite spooling into the repo root, the dashboard
  `TypeError` caught by AppTest) and what each one taught
- the exact commands to reproduce that phase

Close with the phases deliberately not built (Phase 7, cost attribution) and the
reasoning. This document should let a reader rebuild the project, and more
importantly understand *why* it is shaped the way it is.

## Document 2 — `sdk/docs/ARCHITECTURE.md`

A complete structural analysis of the codebase.

- a directory tree with a one-line purpose for every file that matters
- the four layers — SDK, collector API, store, dashboard — and exactly what
  crosses each boundary
- the data model: all five tables, every column, why each index exists, and the
  write/read trade-off behind them
- the SDK's internals: how `@track` wraps a call, how the queue and worker thread
  move an event, how the transport retries, how the spool survives an outage.
  Trace one event end to end, from decorator to dashboard row.
- the public API surface: every exported function and class with its signature
- the repository layer: all read and write functions and why nothing bypasses it
- request flow diagrams in ASCII for the two main paths — an event being tracked,
  and a checkup being triggered and answered
- where the extension points are: `parent_span_id`, the token and cost columns,
  the config-driven questionnaire

## Document 3 — `sdk/docs/USAGE-GUIDE.md`

When, how, and why to use aiOps. Written for an agent developer deciding whether
to adopt it.

Answer these directly:

- **What problem does it solve, and when should I not bother?** Be honest about
  when it is overkill.
- **Do I add it while building an agent, or to one already in production, or
  both?** Cover all three cases with concrete steps for each. This is the
  question most readers will arrive with — a new agent, an existing agent, and a
  multi-agent framework each have a different answer.
- **Installation** — the wheel, the two environment variables, the three lines.
- **What gets captured automatically** versus what I have to pass myself.
- **What is never captured** — no prompt or response content by default, and how
  `hash_user_id` and `pii_fields` work when I need more.
- **Configuration** — every `aiops.yaml` key and every environment variable, in a
  table, with defaults.
- **Multi-agent and orchestration frameworks** — what works today (every event
  carries agent identity, `session_id` groups a run) and what is reserved for
  later (`parent_span_id` for supervisor-to-sub-agent trees).
- **Common patterns** — a sync agent, an async agent, a multi-turn session, a
  manual event with metadata, custom checkup questions.
- **Failure modes and what I will see** — collector down, `identify()` not
  called, spool full, no API key set.
- **FAQ** — will it slow my agent, what if the collector is down, can it break my
  service, what does it cost me to adopt.

---

Then update `README.md` — link the three documents from a Documentation section,
add the Notify view to the dashboard description, and make sure the quickstart
still matches what the code actually does today.

Update `handoff.md` and stop.
