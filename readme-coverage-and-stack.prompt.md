---
mode: agent
description: README additions — tech stack, Challenge #1 requirement coverage table, and what we built beyond the challenge
---

Three additions to the README, done carefully.

# 1. Tech stack — near the top

- Python 3.10+ (developed on 3.14)
- SQLAlchemy 2.x + SQLite — central store, no server to install
- FastAPI + Uvicorn — collector API
- httpx — the SDK's only runtime dependency
- Streamlit + Plotly — dashboards
- pandas — analytics
- pytest — 299 tests

State plainly that the whole project runs after one
`pip install -r requirements.txt` — no Docker, no database server, no external
APIs, no API keys required to run locally.

**Do not upgrade any package versions.** The pinned versions in
`requirements.txt` are what the test suite passes against.

# 2. "Challenge #1 requirement coverage"

A table mapping every stated requirement from the challenge to where it is
implemented and how to verify it. Three columns:
**Requirement | Implementation | How to verify**.

Cover these, in this order — Objective first, then Expected Outcomes, then Pain
Points.

## Objective

- generic adoption tracker addable to any AI agent repo
- captures the user's ACF2 ID
- captures associated data — Business Group, Division
- captures usage metrics
- uploads to a central database
- generic feedback tracker addable to any repo
- triggers a set number of days past first use
- the interval is changeable (e.g. 14 days)
- a list of questions is asked
- sentiment
- time saved
- barriers to use
- other value signals
- responses stored in the central database
- both adoption and feedback tracked per agent

## Expected outcomes

- Outcome 1 — reusable mechanism to store and track adoption and usage
- Outcome 1 — usable to build a usage dashboard
- Outcome 2 — reusable mechanism to store and track feedback
- Outcome 2 — usable to build a feedback dashboard
- Success vision — track adoption, usage and feedback together
- Success vision — target change management tactics
- Success vision — notify people of new releases

## Pain points

- leaders have limited visibility into who is using AI tools
- no visibility into where adoption is lagging
- unclear which interventions would increase value realization
- employees unaware of relevant tools

The **"How to verify"** column must contain something a judge can actually do —
a command to run, a dashboard tab to open, a test name to run, a file to read.
Not prose.

# 3. "Beyond the challenge"

A shorter table of what we built that the challenge did not ask for, and why it
belongs. One line each on the value it adds:

- execution telemetry and error categorisation
- version attribution
- adaptive checkup branching
- bearer auth and PII controls
- the repository layer
- the offline spool
- the distributable wheel
- the reserved `parent_span_id` column

# How to write these

Verify every row against the actual code before writing it. Open the file, check
the function exists, run the command. **Do not write a row from memory or from
`handoff.md` alone** — handoff records intent, the code is the truth.

If any row is only partially true, say so in the table in plain words rather
than overclaiming. A judge who finds one inflated claim will distrust the whole
table, and an honest partial is worth more than a false complete.

---

Tell me at the end which rows, if any, you had to qualify.

Then update `handoff.md` and stop.
