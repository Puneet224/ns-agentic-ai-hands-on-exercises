mode - agent

# Final clean-machine acceptance and full regression

Run this once Phase 9 is complete and the tree is committed. This is the last
verification before freeze. Nothing new gets built here — if you find yourself
writing a feature, stop and report instead.

Two environments, in order. Do not skip to the second.

**Rule for both: follow the documentation literally.** If you run a command the
docs do not give, that omission is the finding, and it is worth more than a
passing test. Record every such moment.

---

# ENVIRONMENT A — Fresh clone, the repo as a teammate receives it

```
cd C:\GitRepo
git clone C:\GitRepo\aiOps aiOps-accept
cd aiOps-accept
```

## A.1 — What arrived

`venv/`, `aiops.db` and `.aiops_spool/` must be absent. The wheel in `sdk/dist/`
must be present. Confirm both, and confirm the wheel's hash matches the one
recorded in `RELEASE-VERIFICATION.md`.

## A.2 — Quickstart, literally

Work down the README Quickstart running each command exactly as written. Start
the collector from inside the clone — `aiops.db` is created relative to the
working directory, and starting it elsewhere silently produces a second empty
database and a dashboard showing nothing.

## A.3 — Full regression

```
python -m pytest -q
```

Report the count. Compare it against the count recorded in the docs. Any
difference is either a doc that went stale or a test that vanished — say which.

Then confirm the guard tests specifically:

- the docs-selector guard (`test_every_pytest_command_in_the_docs_selects_something`)
- the wheel/packaging tests (`-k wheel`)
- the org-attribute rendering guard (`test_missing_org_attributes_never_render_as_none`)
- the concurrency isolation tests added in Phase 9

## A.4 — Every surface, exercised

For each item, capture real output. "It worked" is only useful with the command
and the result beside it.

**Collector** — `/health` returning 200; auth enforced (show a rejected call as
well as an accepted one).

**Seed** — the seeder's summary line with its full counts.

**Adoption tab** — HTTP 200 on 8501; the org chart rendering; the Division and
Business Group filters, including the `unknown` bucket; confirm the sum across
all filter options equals the unfiltered total.

**Feedback tab** — the questionnaire prompting at the configured day offset;
a checkup moving `pending -> completed -> reopened`; the adaptive branching
visible.

**Reliability tab** — a non-zero metric; error categories populated.

**Notify tab** — all three audiences, each with count, table, CSV download, and
editable draft. Confirm it sends nothing.

**Demo agent** — event count before and after, differing by exactly one.

**`--replay`** — the checkup reopening after having been answered.

**Outage demo** — its own assertion passing and exit code 0.

**Offline spool** — stop the collector, run an agent, confirm events spool to
disk; restart the collector, confirm they drain and arrive. This is the one
nobody exercises and the one a judge will ask about.

## A.5 — Org resolution end to end

- An ACF2 ID present in the org map resolves BG and Division without the caller
  passing them.
- An ACF2 ID absent from the map lands in `unknown` and is reachable by filter.
- The precedence rule decided in Phase 9 actually holds — construct the case
  where caller and map disagree, and show which wins.

## A.6 — Multi-user and multi-agent

- Concurrent traffic from several ACF2 IDs attributes correctly, verified from
  the database rather than the SDK's own counters.
- One ACF2 ID across three agents rolls up correctly, and the per-user agent
  breakdown renders.

## A.7 — Clean up

```
cd C:\GitRepo
Remove-Item -Recurse -Force aiOps-accept
```

---

# ENVIRONMENT B — Wheel only, a stranger's agent

The person who receives this from SharePoint has a `.whl` file and the README
section written for them. No repo, no source, no `pip install -e`.

## B.1 — Neutral ground

Copy the wheel to `C:\Temp\accept-agent`, build a fresh venv on the system
Python — not the project's — and install only the wheel. No `requirements.txt`.

## B.2 — Dependency footprint

`python -m pip list`. Nothing collector-side may appear: no FastAPI, no
Streamlit, no SQLAlchemy, no pandas, no pytest. If any of them are there, the
SDK is dragging the platform into every agent's environment.

Confirm `aiops.__file__` resolves inside this venv's `site-packages`, not a
repo path.

## B.3 — Write an agent from scratch

Using only the README section "Installing the SDK in your own agent". Do not
copy from `demo/`. If the README does not give you enough to write the file,
that gap is the finding — record it verbatim rather than filling it from
memory.

Run it against a collector started from the real repo, then verify from the
database, not the SDK's counters: the event must carry the agent name, the ACF2
ID, an `sdk_version` matching the wheel, and BG/Division resolved from the map.

## B.4 — Identity modes

Exercise each documented mode and report which worked without extra knowledge:

- explicit per-request `identify()`
- `fallback_to_os_user`
- the environment-variable path, if Phase 9 kept one

## B.5 — Clean up

```
Remove-Item -Recurse -Force C:\Temp\accept-agent
```

---

# Documents to update

Only where reality and the document disagree. For each change, quote the old
line and the new one.

- `README.md`
- `sdk/docs/USAGE-GUIDE.md`, `ARCHITECTURE.md`, `BUILD-JOURNEY.md`
- `RELEASE-VERIFICATION.md` — this run becomes its record
- `handoff.md` — one entry for the acceptance run

If a document is already accurate, say so. Do not edit docs to look busy.

# Report back

1. every step where the documentation did not match what you had to do, quoting
   both
2. the regression count, and any difference from the recorded count
3. each surface in A.4 with the command and its actual output
4. the org-resolution and precedence results
5. the concurrency and multi-agent results, from the database
6. the wheel-only dependency list
7. anything that would embarrass this project in front of a judge
8. docs changed, docs deliberately left alone

Commit nothing until I have read this. Show me the diffs.
