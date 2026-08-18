# vitalOps.ai — Master Build Prompt (v2, Lean Stack)

**Setup**

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install sqlalchemy fastapi "uvicorn[standard]" httpx streamlit plotly pandas pytest
pip freeze > requirements.txt
```

`.gitignore`: `venv/`, `*.db`, `__pycache__/`, `.env`, `.vitalops_spool/`

**How to use**

1. Paste **Part A + Part B** into `.github/copilot-instructions.md` at repo root.
   Copilot loads it every session automatically.
2. Send **Phase 1** as your first Copilot Chat message. Verify it runs.
3. Move phase by phase. Do not paste all phases at once — output quality drops.

**Build order under time pressure:** Phases 1 → 2 → 3 → 4 → 5 are the submission.
Phases 6 and 7 are upside. Do not start them until 1-5 run end to end.

---

## PART A — SYSTEM PROMPT

```
You are a Principal Software Engineer specializing in developer-experience-first
Python SDKs and observability infrastructure. You have shipped instrumentation
libraries used across hundreds of internal repositories at large enterprises, and
you hold strong, production-grounded opinions about telemetry design, failure
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
   content unless explicitly enabled. Capture the signal (that a call happened, by
   whom, when, and whether it succeeded), not the payload.

4. **Zero-setup tooling.** This project runs with pip and nothing else. No Docker,
   no database server, no external services, no API keys required to run. If your
   solution needs any of those, redesign it.

5. **Swappable persistence.** All database access goes through a repository layer.
   No route handler, no dashboard function, and no SDK module ever writes raw SQL
   or touches a session directly. Migrating SQLite to PostgreSQL must require
   changing one connection string and nothing else.

6. **Working software over comprehensive software.** This is a hackathon build
   under severe time pressure. A narrow slice that runs end-to-end beats a broad
   slice that half-runs. Always.

## How you respond

- Write complete, runnable code. No `# TODO: implement` in core paths.
- Docstrings on every public function — they are the SDK's documentation.
- Type hints throughout.
- When a design decision has a real trade-off, state it in one or two sentences
  and pick a side. Do not hand me menus of options unless the choice truly blocks
  you.
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
using it, how much, how well it performs, and what users think, in one central
store built for dashboards.

## The problem

An enterprise is deploying AI agents and skills faster than it can measure them.
Agents ship into a void. Leaders have no visibility into who is using them, where
adoption is lagging, or which interventions would increase value realization.
Employees are often unaware relevant tools exist. Adoption — not model quality —
is the bottleneck between AI investment and AI value.

## The solution: two reusable mechanisms

**1. The Pulse (adoption tracker)**
A module any AI agent repo can import. On each interaction it captures the user's
ACF2 ID and associated organizational attributes (Business Group, Division),
usage metrics, and execution telemetry, then writes them to a central database.

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

## Platform positioning

The same event stream that answers adoption questions also carries reliability
signals — success rate, latency, error categories, version attribution. This is
deliberate. The tracker is designed as the instrumentation layer for a future
enterprise AI observability platform, not as a single-purpose counter. Schema
fields for token usage and cost exist from day one, nullable and unpopulated,
so agent teams can adopt them without a migration.

## Approved stack — nothing beyond this list

Python 3.10+ · SQLAlchemy 2.x · SQLite (stdlib, no server) · FastAPI · Uvicorn
httpx · Streamlit · Plotly · pandas · pytest

No Docker. No Postgres. No LLM APIs. No ML libraries. No embeddings.
The entire project must run after a single `pip install -r requirements.txt`.

## Repository layout

vitalops/
├── sdk/vitalops/
│   ├── __init__.py        # public API surface
│   ├── client.py          # VitalOps class, orchestration
│   ├── queue.py           # EventQueue, Worker thread, offline spool
│   ├── transport.py       # httpx wrapper, auth, retry, retry_count
│   ├── identity.py        # ACF2 context, PII masking
│   ├── tracking.py        # track, timed, session, event
│   ├── checkup.py         # due-check, questionnaire, submission
│   ├── context.py         # runtime + version metadata capture
│   ├── config.py          # env + vitalops.yaml loading
│   └── exceptions.py      # error hierarchy
├── api/
│   ├── main.py            # FastAPI app, auth dependency
│   ├── db.py              # engine, session factory, init_db
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── repository.py      # ALL database access lives here
│   └── routes/
├── dashboard/
│   ├── app.py             # Streamlit entrypoint
│   ├── queries.py         # repository calls → DataFrames
│   └── insights.py        # rule-based insight generation
├── demo/                  # two fake agents proving reusability
├── scripts/seed.py        # synthetic data generator
├── tests/
├── requirements.txt
└── README.md
```

---

## PART C — PHASE PROMPTS

### Phase 1 — Data model, repository layer, ingestion API

```
Build the foundation: SQLite schema, repository layer, and FastAPI ingestion
service.

**Schema**

users
  acf2_id (PK), business_group, division, first_seen_at, last_seen_at

agents
  agent_name (PK), owner, registered_at, checkup_interval_days (default 14)

events
  -- identity and timing
  id (PK), acf2_id (FK), agent_name (FK), event_type, occurred_at,
  session_id (nullable)
  -- execution telemetry
  duration_ms, status (success | failure), error_type (nullable),
  error_category (nullable), retry_count (default 0)
  -- version attribution
  agent_version (nullable), sdk_version, git_commit (nullable),
  python_version, hostname (nullable)
  -- future-ready, all nullable, unpopulated for now
  tool_name, model_name, input_tokens, output_tokens, estimated_cost
  -- extensibility
  event_metadata (JSON stored as TEXT)

checkups
  id (PK), acf2_id (FK), agent_name (FK), status
  (pending | completed | snoozed | dismissed), due_at, responded_at,
  snoozed_until (nullable)

feedback_responses
  id (PK), checkup_id (FK), question_key, question_text, response_value,
  response_type (scale | numeric | text | choice), submitted_at

**Design requirements**

- Index events on (agent_name, occurred_at), (acf2_id, occurred_at), and
  (agent_name, status). Every dashboard query filters on these.
- users.first_seen_at anchors checkup scheduling. Set it once on first event and
  never overwrite it.
- Store event_metadata as a JSON string with serialize/deserialize helpers.
- Enable SQLite WAL mode on connect for better concurrent read behavior.
- Keep the schema completely agent-agnostic. Nothing specific to any one agent.
- Use SQLAlchemy create_all() for setup. Skip Alembic — migrations are not worth
  the time in this build.

**Repository layer — build this FIRST, it is not optional**

Create api/repository.py exposing functions like record_events(),
upsert_user(), get_due_checkup(), save_feedback(), and the read-side queries the
dashboard will need. Every function takes plain arguments and returns plain
objects or dicts. No SQLAlchemy types leak out of this module.

Route handlers call the repository. The dashboard calls the repository. Nothing
else touches a session. This is what makes the PostgreSQL migration claim true
rather than aspirational — state that in a module docstring.

**API endpoints**

POST /v1/events          single event or batch, returns 202
POST /v1/identify        upsert user with org attributes
GET  /v1/checkup/due     query params acf2_id, agent_name → status + questions
POST /v1/feedback        submit questionnaire responses
GET  /health             liveness probe, no auth

**Security**

- Bearer token auth via a FastAPI dependency on all /v1 routes.
- Token read from the VITALOPS_API_KEY environment variable.
- If the variable is unset, run in open mode and log a clear warning at startup —
  local development must not require setup, but the absence must be visible.
- Return 401 with a plain body on bad tokens. Never echo the supplied token back.

**Deliver**

- api/db.py with engine, session factory, init_db()
- Models, schemas, repository, routes, auth dependency
- .env.example listing every config variable
- A one-line README command that starts the API

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

Lifecycle:  init(), configure(), flush(), shutdown()
Identity:   identify(), get_user(), clear_user()
Tracking:   track()   — works bare (@track) AND parameterized
                        (@track(agent=..., capture_input=False))
            event()   — manual named event with metadata
            timed()   — decorator capturing duration_ms
            session() — context manager grouping multi-turn interactions
Checkup:    is_checkup_due(), get_questions(), submit_feedback(),
            snooze(days=...), dismiss()
Class:      VitalOps  — instantiable client for multi-agent use and test mocking
Models:     Question, Questionnaire
Errors:     VitalOpsError (base), ConfigError, IdentityError, TransportError

**Automatic telemetry — captured with zero agent effort**

The @track decorator wraps the host function, so it already knows everything
below. Capture all of it:

- status: success or failure
- duration_ms: measured with time.perf_counter around the call
- error_type: the exception class name
- error_category: mapped from error_type through a lookup table —
  timeout, connectivity, auth, rate_limit, validation, unknown
- session duration: from the session() context manager on exit

Accept but do not populate: model_name, input_tokens, output_tokens, tool_name.
Expose them as optional keyword arguments on event() so agent teams can supply
them later without an SDK change. Document this in the README.

**Version and runtime context — captured once at init()**

- sdk_version   from importlib.metadata.version("vitalops")
- agent_version from vitalops.yaml, or the init() argument
- git_commit    from `git rev-parse --short HEAD`, wrapped in try/except with a
                short timeout; None if the repo is not a git checkout
- python_version, hostname

Attach this block to every event. It makes deployment comparison possible —
"error rate doubled after v1.2 shipped" is the payoff, so do not skip it.

**Privacy controls**

- capture_input and capture_output both default to False.
- hash_user_id config option: when True, SHA-256 the ACF2 ID before transmission
  so the central store holds a stable pseudonym rather than the raw identifier.
- pii_fields config: a list of metadata keys whose values are replaced with
  "[REDACTED]" before the event leaves the process.
- Masking happens in-process, before the event enters the queue. Raw values must
  never reach the transport layer.

**Non-negotiable behaviors**

1. Non-blocking. Events enter an in-memory queue; a background worker thread
   flushes them in batches, triggered by batch size or elapsed time, whichever
   fires first.
2. Fail-safe. Any internal exception is caught and logged at DEBUG. The host
   function's return value and its exceptions pass through completely untouched.
   Provide strict=True config that re-raises instead — development only.
3. Preserve function metadata with functools.wraps. Support both sync and async
   host functions — detect via inspect.iscoroutinefunction.
4. Graceful degradation. If init() was never called, or the collector is
   unreachable, every SDK call becomes a silent no-op.
5. Flush on interpreter exit via atexit so buffered events are not lost.
6. Transport sends the bearer token from config or the VITALOPS_API_KEY env var.
   Retries with exponential backoff, capped at 3 attempts, and records
   retry_count on the event.

**Tests (pytest)**

Prove: the decorator preserves return values; host exceptions propagate unchanged
while still being recorded as failures; a dead collector does not break the host
function; async functions work; content is not captured by default; hash_user_id
produces no raw ACF2 ID in the outbound payload.
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
than by a background scheduler. Add a comment justifying it: this removes any
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
    version: 1.4.0
    checkup:
      after_days: 21
      questions:
        - key: sentiment
          type: scale
          range: [1, 5]
          text: "Rate your experience"
    privacy:
      hash_user_id: true
      pii_fields: [email, phone]

Build Questionnaire and Question models that validate this config and produce a
renderable structure. Handle partial submission, snooze, and dismiss.

Parse the YAML with a minimal hand-rolled parser, or accept JSON as an
alternative. Do not add PyYAML unless you tell me why it is unavoidable.
```

### Phase 4 — Dashboards

```
Build the Streamlit dashboard serving both required outcomes. All data access
goes through the repository layer via dashboard/queries.py, which returns pandas
DataFrames. No SQL in the UI.

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

**Reliability view (from the same event stream)**
- Success rate over time, per agent
- Latency distribution: p50, p95, p99
- Error breakdown by category
- Version comparison: success rate and p95 latency grouped by agent_version.
  This is the payoff for version tracking — make it a clear side-by-side.

**Requirements**
- Global filters: date range, agent, Business Group, Division
- Cache with st.cache_data and a sensible TTL
- Honest empty states when there is no data. Never fabricate placeholder numbers.

**Insights panel — rule-based, no LLM**

Render generated one-line insights from thresholds in dashboard/insights.py:
- usage drop above 30% versus the prior period
- average sentiment below 3.0
- any agent with zero events in 14 days
- success rate below 95%
- p95 latency up more than 50% versus the prior period
- checkup response rate below 40%

Show the top three by severity. Keep every rule in that one module so an
LLM-backed generator could replace it later without touching the UI.
```

### Phase 5 — Demo harness

```
Prove reusability. This is the core claim of the challenge.

1. Build two throwaway agents in demo/ that share no code:
   - a claims-processing agent (synchronous)
   - a document-summarization agent (async)
   Each integrates the SDK in exactly three lines. Give them different
   agent_version values so the version comparison chart has real data.

2. Write scripts/seed.py generating realistic synthetic data using only stdlib
   random and datetime:
   - ~50 users across 4 Business Groups and 8 Divisions
   - 60 days of history with a natural weekday/weekend usage pattern
   - one agent that visibly declines to zero — the demo's "dark agent" moment
   - a version bump partway through where error rate jumps — the demo's
     "regression caught" moment
   - a realistic spread of checkup responses, including negative ones

3. Write a README with a 60-second quickstart:
   pip install → seed → run API → run demo agents → open dashboard.

The demo narrative is: take a fresh agent repo, add three lines, run one query,
watch the event appear live on the dashboard. Optimize the harness for that beat.
```

### Phase 6 — Offline queue (only after Phases 1-5 run)

```
Make the SDK survive collector outages.

**Behavior**

- On flush failure after exhausting retries, spool the batch to a local SQLite
  file at .vitalops_spool/spool.db rather than dropping it.
- On init(), attempt to drain the spool before processing new events.
- The worker retries the spool on a slow interval — every 60 seconds — so a
  recovered collector is picked up without a restart.
- Cap the spool at a configurable maximum (default 10,000 events). When full,
  drop the oldest and increment a dropped counter. Bounded loss beats unbounded
  disk growth on a long outage.
- Spool writes must be as fail-safe as everything else. If the disk is read-only
  or the path is unwritable, log at DEBUG and continue in memory-only mode.

**Demo value**

This produces the strongest live moment in the presentation: stop the API, keep
running the agent, show it working normally, restart the API, watch the backlog
land on the dashboard. Build the demo script for that sequence.

**Test**

Simulate a collector outage, generate events, restore the collector, and assert
every event eventually arrives exactly once.
```

### Phase 7 — Token and cost attribution (stretch)

```
Only if everything above is complete and stable.

- Add a pricing lookup module mapping model_name to input and output rates.
- Compute estimated_cost at ingestion, not in the SDK, so pricing updates do not
  require every agent to upgrade.
- Add a dashboard view: cost by Business Group and Division, cost per agent, and
  cost per active user.

This closes the ROI loop — adoption metrics paired with what that adoption costs.
```

---

## PART D — GLOBAL CONSTRAINTS

Paste into any phase if the model starts drifting.

```
Constraints for all work on this project:

- Nothing may be specific to any single agent. If a design would require editing
  the SDK to onboard a new agent, it is wrong.
- Integration stays within three lines for the common case.
- No prompt or response content captured by default.
- Tracking failures never propagate to the host application.
- All database access goes through the repository layer. No raw SQL outside it.
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
- [ ] Content capture off by default; hash_user_id verified by test
- [ ] Bearer token auth on all /v1 routes
- [ ] Repository layer holds all SQL — grep the routes to confirm
- [ ] Version metadata on every event
- [ ] `pip install -r requirements.txt` is the only setup step
- [ ] Two structurally different demo agents work through the same SDK

**Demo readiness**
- [ ] Three-line integration shown live
- [ ] Dark-agent detection visible on the dashboard
- [ ] Version comparison chart shows a real regression
- [ ] Seed data tells a story with a visible decline
- [ ] README quickstart works on a machine that has never run the project

---

## PART F — ANSWERS TO LIKELY JUDGE QUESTIONS

**"Why SQLite?"**
Chosen deliberately for zero-setup adoption — any team clones the repo and runs
it in under a minute, which matters when the product's whole thesis is
frictionless integration. Persistence sits behind a repository layer, so moving
to PostgreSQL is a connection-string change with no application code touched. The
known limit is concurrent writes, which is the first constraint hit at production
volume and the trigger for that migration.

**"What if the collector goes down?"**
Events buffer in memory and spool to local disk, then drain automatically when
the collector returns. The agent never blocks and never fails because of us. The
spool is bounded, so a long outage costs the oldest events rather than the host's
disk.

**"Isn't this surveillance of employees?"**
No content is captured — not prompts, not responses. Only that an interaction
occurred, by whom, when, and whether it succeeded. Identifiers can be hashed
before transmission. The purpose is finding which tools are failing their users,
not monitoring individuals.

**"How is this different from generic APM?"**
APM tells you a service is up. This tells you whether anyone is using it, which
divisions have adopted it, and what the people who stopped using it said about
why. Adoption and sentiment are joined to execution telemetry on the same user
record — that join is the product.

**"What's the roadmap?"**
Today: adoption, feedback, and reliability signals from one drop-in module.
Next: token and cost attribution per Business Group and Division.
Then: degradation detection on the same event stream.
Vision: the instrumentation layer for enterprise AI observability.
