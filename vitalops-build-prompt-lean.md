# vitalOps.ai — Master Build Prompt (Lean Stack)

**Setup before you start**

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install sqlalchemy fastapi "uvicorn[standard]" httpx streamlit plotly pandas pytest
pip freeze > requirements.txt
```

Create `.gitignore` containing `venv/`, `*.db`, `__pycache__/`, `.env`.

**How to use this document**

1. Paste **Part A + Part B** into `.github/copilot-instructions.md` in your repo root.
   Copilot loads it automatically every session.
2. Send **Phase 1** as your first Copilot Chat message. Verify the code runs.
3. Move to Phase 2. One phase at a time — do not paste them all together.

---

## PART A — SYSTEM PROMPT

```
You are a Principal Software Engineer specializing in developer-experience-first
Python SDKs and observability infrastructure. You have shipped instrumentation
libraries used across hundreds of internal repositories at large enterprises, and
you have strong, production-grounded opinions about telemetry design, failure
isolation, and API ergonomics.

## Your operating principles

1. **The host application is sacred.** Instrumentation must never crash, block, or
   slow down the agent it measures. Every failure path degrades silently by
   default. A tracking library that takes down a production service is worse than
   no tracking at all.

2. **Integration budget is three lines.** If an agent owner needs more than three
   lines to get value, adoption of the SDK will fail — an ironic failure for an
   adoption-tracking tool. Optimize relentlessly for the first-run experience.

3. **Privacy by default, richness by opt-in.** Never capture prompt or response
   content unless explicitly enabled. Capture the signal (that a call happened,
   by whom, when), not the payload.

4. **Zero-setup tooling.** This project runs with pip and nothing else. No Docker,
   no database server, no external services, no API keys. If your solution needs
   any of those, redesign it.

5. **Working software over comprehensive software.** This is a hackathon build
   under severe time pressure. A narrow slice that runs end-to-end beats a broad
   slice that half-runs. Always.

## How you respond

- Write complete, runnable code. No `# TODO: implement` in core paths.
- Docstrings on every public function — they are the SDK's documentation.
- Type hints throughout.
- When a design decision has a real trade-off, state it in one or two sentences
  and pick a side. Do not hand me menus of options unless the choice genuinely
  blocks you.
- Flag risks proactively. If something I ask for will break under concurrency,
  fail at scale, or leak data, say so before writing it.
- Add no dependency outside the approved list without telling me why.
- If a requirement is ambiguous, make the most reasonable assumption, implement
  it, and note the assumption at the end of your response.
```

---

## PART B — PROJECT CONTEXT

```
## Project: vitalOps.ai

A drop-in Python SDK that gives every AI agent a heartbeat — capturing who is
using it, how much, and what they think, in one central store built for dashboards.

## The problem

An enterprise is deploying AI agents and skills faster than it can measure them.
Agents ship into a void. Leaders have no visibility into who is using them, where
adoption is lagging, or which interventions would increase value realization.
Employees are often unaware relevant tools exist. Adoption — not model quality —
is the bottleneck between AI investment and AI value.

## The solution: two reusable mechanisms

**1. The Pulse (adoption tracker)**
A module any AI agent repo can import. On each interaction it captures the user's
ACF2 ID and associated organizational attributes (Business Group, Division) along
with usage metrics, and writes them to a central database.

**2. The Checkup (feedback tracker)**
The same module records each user's first-use timestamp. After a configurable
interval (default 14 days), it surfaces a short questionnaire covering sentiment,
estimated time saved, barriers to use, and other value signals. Responses land in
the same central store, joined to the usage record.

## Required outcomes

- **Outcome 1:** A reusable mechanism to store and track agent adoption and usage,
  capable of powering a usage dashboard.
- **Outcome 2:** A reusable mechanism to store and track agent feedback, capable
  of powering a feedback dashboard.
- **Success vision:** One source of truth for AI adoption across the portfolio,
  enabling targeted change management and proactive notification of new releases.

## Approved stack — nothing beyond this list

Python 3.10+ · SQLAlchemy 2.x · SQLite (stdlib, no server) · FastAPI · Uvicorn
httpx · Streamlit · Plotly · pandas · pytest

No Docker. No Postgres. No LLM APIs. No ML libraries. No embeddings.
The entire project must run after a single `pip install -r requirements.txt`.

## Repository layout

vitalops/
├── sdk/vitalops/
│   ├── __init__.py        # public API surface
│   ├── client.py          # VitalOps class, transport, buffering
│   ├── identity.py        # ACF2 resolution, user context
│   ├── tracking.py        # track, timed, session, event
│   ├── checkup.py         # due-check, questionnaire, submission
│   ├── config.py          # env + vitalops.yaml loading
│   └── exceptions.py      # error hierarchy
├── api/
│   ├── main.py            # FastAPI app
│   ├── db.py              # engine, session, init_db
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── routes/
├── dashboard/
│   ├── app.py             # Streamlit entrypoint
│   └── queries.py         # all SQL → DataFrame functions
├── demo/                  # two fake agents proving reusability
├── scripts/seed.py        # synthetic data generator
├── tests/
├── requirements.txt
└── README.md
```

---

## PART C — PHASE PROMPTS

### Phase 1 — Data model and ingestion API

```
Build the foundation: SQLite schema and the FastAPI ingestion service.

**Schema**

users
  acf2_id (PK), business_group, division, first_seen_at, last_seen_at

agents
  agent_name (PK), owner, registered_at, checkup_interval_days (default 14)

events
  id (PK), acf2_id (FK), agent_name (FK), event_type, occurred_at,
  duration_ms (nullable), event_metadata (JSON as TEXT), session_id (nullable)

checkups
  id (PK), acf2_id (FK), agent_name (FK), status
  (pending | completed | snoozed | dismissed), due_at, responded_at,
  snoozed_until (nullable)

feedback_responses
  id (PK), checkup_id (FK), question_key, question_text, response_value,
  response_type (scale | numeric | text | choice), submitted_at

**Design requirements**

- Index events on (agent_name, occurred_at) and (acf2_id, occurred_at) —
  every dashboard query filters on these.
- users.first_seen_at anchors checkup scheduling. Set it once on the first event
  and never overwrite it.
- Store event metadata as a JSON string so agent teams attach arbitrary context
  without schema changes. Provide helpers that serialize and deserialize it.
- Enable SQLite WAL mode on connect for better concurrent read behavior.
- Keep the schema completely agent-agnostic. Nothing specific to any one agent.
- Use SQLAlchemy's create_all() for schema setup. Skip Alembic — migrations are
  not worth the time in this build.

**API endpoints**

POST /v1/events          single event or batch, returns 202
POST /v1/identify        upsert user with org attributes
GET  /v1/checkup/due     query params acf2_id, agent_name → due status + questions
POST /v1/feedback        submit questionnaire responses
GET  /health             liveness probe

**Deliver**

- api/db.py with engine, session factory, and init_db()
- All models, schemas, and routes
- A one-line command in the README that starts the API

Explain your indexing choices and any trade-off between write throughput and
query flexibility.
```

### Phase 2 — The SDK

```
Build the vitalops SDK package. This is the heart of the project and where
judging attention will land.

**Target integration — must work exactly as written**

    from vitalops import init, identify, track

    init(agent="claims-bot")
    identify(acf2_id=user.acf2)

    @track
    def handle_query(prompt): ...

**Public API surface**

Lifecycle:  init(), configure(), shutdown(), flush()
Identity:   identify(), get_user(), clear_user()
Tracking:   track()   — works bare (@track) AND parameterized
                        (@track(agent=..., capture_input=False))
            event()   — manual named event with metadata
            timed()   — decorator capturing duration_ms
            session() — context manager grouping multi-turn interactions
Checkup:    is_checkup_due(), get_questions(), submit_feedback(),
            snooze(days=...), dismiss()
Class:      VitalOps  — instantiable client for multi-agent use and test mocking
Errors:     VitalOpsError (base), ConfigError, IdentityError, TransportError

**Non-negotiable behaviors**

1. Non-blocking. Events enter an in-memory queue; a background worker thread
   flushes them in batches, triggered by batch size or elapsed time, whichever
   fires first.
2. Fail-safe. Any internal exception is caught and logged at DEBUG. The host
   function's return value and its exceptions pass through completely untouched.
   Provide strict=True config that re-raises instead — development only.
3. Never capture prompt or response content by default. capture_input and
   capture_output both default to False. Document this prominently in the README.
4. Preserve function metadata with functools.wraps. Support both sync and async
   host functions — detect via inspect.iscoroutinefunction.
5. Graceful degradation. If init() was never called, or the collector is
   unreachable, every SDK call becomes a silent no-op.
6. Flush on interpreter exit via atexit so buffered events are not lost.

**Tests (pytest)**

Prove: the decorator preserves return values; host exceptions propagate unchanged;
a dead collector does not break the host function; async functions work; content
is not captured by default.
```

### Phase 3 — Checkup engine

```
Implement the feedback trigger and questionnaire flow.

**Trigger logic**

A user is due for checkup on an agent when all of these hold:
- days_since(first_seen_at) >= agent.checkup_interval_days
- no completed checkup exists for that (user, agent) pair
- snoozed_until is null or in the past

Implement this as a lazy check inside the SDK, evaluated on interaction rather
than by a background scheduler. Add a comment justifying this: it removes any
need for cron or scheduler infrastructure, which matters enormously for a
drop-in library.

**Default question set (overridable per agent)**

sentiment     scale 1-5  "How would you rate your experience with this agent?"
time_saved    numeric    "Roughly how many minutes has this saved you per week?"
barriers      text       "What has made this agent harder to use than it should be?"
recommend     scale 1-5  "How likely are you to recommend this to a colleague?"
value_signal  text       "What would make this significantly more useful?"

**Configuration**

Agent teams override via vitalops.yaml in their repo root:

    agent: claims-bot
    checkup:
      after_days: 21
      questions:
        - key: sentiment
          type: scale
          range: [1, 5]
          text: "Rate your experience"

Build Questionnaire and Question models that validate this config and produce a
renderable structure. Handle partial submission, snooze, and dismiss.

Note: parse the YAML with a minimal hand-rolled parser or accept JSON as an
alternative — do not add PyYAML unless you tell me why it is unavoidable.
```

### Phase 4 — Dashboards

```
Build the Streamlit dashboard serving both required outcomes.

**Outcome 1 — Adoption view**
- Portfolio header: total agents, active users, total events
- Daily and weekly active users, per agent and portfolio-wide
- Adoption by Business Group and by Division (grouped bar charts)
- Dark Agents panel: agents with zero events in the last N days. Make this the
  most visually prominent element on the page — it is the single most actionable
  view for a leader.
- Retention curve: percentage of users still active N days after first use
- New vs returning user split

**Outcome 2 — Feedback view**
- Sentiment distribution, overall and per agent
- Average time saved, rolled up to an estimated hours-per-month figure
- Barriers as a raw response list, most recent first
- Checkup response rate: completed vs pending vs snoozed
- Cross-view: sentiment plotted against usage frequency

**Requirements**

- Global filters: date range, agent, Business Group, Division
- All SQL lives in dashboard/queries.py and returns pandas DataFrames. No SQL in
  the UI layer.
- Cache with st.cache_data and a sensible TTL
- Honest empty states when there is no data. Never fabricate placeholder numbers.

**Insights panel — rule-based, no LLM**

At the top of the page, render generated one-line insights from thresholds:
- usage drop above 30% versus the prior period
- average sentiment below 3.0
- any agent with zero events in 14 days
- checkup response rate below 40%

Show the top three by severity. Keep the rule set in one module so an LLM-backed
version could replace it later without touching the UI.
```

### Phase 5 — Demo harness

```
Prove reusability. This is the core claim of the challenge.

1. Build two throwaway agents in demo/ that share no code:
   - a claims-processing agent (synchronous)
   - a document-summarization agent (async)
   Each integrates the SDK in exactly three lines.

2. Write scripts/seed.py generating realistic synthetic data using only stdlib
   random and datetime:
   - ~50 users across 4 Business Groups and 8 Divisions
   - 60 days of history with a natural weekday/weekend usage pattern
   - one agent that visibly declines to zero — the demo's "dark agent" moment
   - a realistic spread of checkup responses, including negative ones

3. Write a README with a 60-second quickstart:
   pip install → seed → run API → run demo agents → open dashboard.

The demo narrative is: take a fresh agent repo, add three lines, run one query,
watch the event appear live on the dashboard. Optimize the harness for that beat.
```

---

## PART D — GLOBAL CONSTRAINTS

Paste this into any phase if the model starts drifting.

```
Constraints for all work on this project:

- Nothing may be specific to any single agent. If a design would require editing
  the SDK to onboard a new agent, it is wrong.
- Integration stays within three lines for the common case.
- No prompt or response content captured by default.
- Tracking failures never propagate to the host application.
- Approved dependencies only: sqlalchemy, fastapi, uvicorn, httpx, streamlit,
  plotly, pandas, pytest. Nothing else without justification.
- No Docker, no database server, no external APIs, no ML libraries.
- Prefer working end-to-end slices over complete-but-unrunnable layers.
- When you finish a phase, list what you assumed, what you deliberately left out,
  and what would break first at 100x scale.
```

---

## PART E — ACCEPTANCE CHECKLIST

**Challenge coverage**
- [ ] Generic tracker importable into any agent repo, no per-agent code changes
- [ ] Captures ACF2 ID plus Business Group and Division
- [ ] Usage metrics written to a central database
- [ ] Feedback triggers a configurable number of days past first use
- [ ] Questions cover sentiment, time saved, barriers, and value signals
- [ ] Feedback stored in the same central database
- [ ] Outcome 1 — usage dashboard running on real stored data
- [ ] Outcome 2 — feedback dashboard running on real stored data

**Engineering quality**
- [ ] SDK failures cannot break the host agent (a test proves it)
- [ ] Async and sync host functions both supported
- [ ] Content capture off by default
- [ ] `pip install -r requirements.txt` is the only setup step
- [ ] Two structurally different demo agents work through the same SDK

**Demo readiness**
- [ ] Three-line integration shown live
- [ ] Dark-agent detection visible on the dashboard
- [ ] Seed data tells a story with a visible decline
- [ ] README quickstart works on a machine that has never run the project

---

## PART F — WHAT TO SAY IF ASKED ABOUT SCALE

Judges often probe the SQLite choice. The honest answer:

SQLite was chosen deliberately for zero-setup adoption — any team clones the repo
and runs it in under a minute, which matters when the product's whole thesis is
frictionless integration. The persistence layer sits behind SQLAlchemy, so moving
to PostgreSQL is a one-line connection-string change with no application code
touched. The known limit is concurrent writes, which is the first thing to hit at
production volume and the trigger for that migration.
