---
mode: agent
description: Rebuild the SDK wheel after Phase 8, then run both clean-machine verifications — fresh clone and wheel-only install
---

Three tasks. Do them in order, then stop.

Everything below is written as a script you can follow literally. Where a
command is given, run that command. Where reasoning is given, it explains what
the step proves — if a step passes for the wrong reason, the test has told you
nothing.

---

# TASK 1 — Rebuild the wheel

## Why

The wheel in `sdk/dist/` was built before Phase 8. The Notify view, the new
repository functions and the docs all landed after it. The wheel therefore
contains stale code **under the same version number**, so nothing about the
filename would warn anyone. A committed wheel that has silently gone stale is
worse than no wheel, because it looks authoritative.

## Steps

```powershell
cd C:\GitRepo\aiOps
.\venv\Scripts\Activate.ps1
```

**1.1 — Record what is there now**, so the comparison is real rather than
remembered:

```powershell
Get-ChildItem sdk\dist
```

**1.2 — Remove the stale artifacts.** Deleting rather than overwriting means a
failed build cannot leave the old wheel sitting there pretending to be new:

```powershell
Remove-Item sdk\dist\* -Force
```

**1.3 — Rebuild:**

```powershell
python -m build sdk\
```

**1.4 — Confirm the output.** Report both filenames and their sizes:

```powershell
Get-ChildItem sdk\dist
```

**1.5 — Prove the archive is complete.** The packaging tests exist because
`spool.py` could have been left out of an earlier build and nobody would have
noticed until an import failed on someone else's machine:

```powershell
python -m pytest tests/test_sdk.py -q -k packaging
```

**1.6 — Version decision.** The code has changed but the version has not. Tell
me whether `0.1.0` should become `0.2.0`, and why. Do not bump it silently and
do not leave it silently — recommend, and let me decide.

---

# TASK 2 — Clean-machine test, fresh clone

## Why

The working copy has a virtual environment, a seeded database and a spool
directory that accumulated over eight phases. None of that reaches a judge. A
fresh clone contains only what is committed, which is exactly what someone else
receives — so this is the only test that can find a Quickstart step that exists
in your head but not in the README.

**The rule for this task: follow the README literally.** If you find yourself
running a command the README does not give, stop — that omission is the finding,
and it is worth more than a passing test.

## Steps

**2.1 — Clone:**

```powershell
cd C:\GitRepo
git clone C:\GitRepo\aiOps aiOps-test
cd aiOps-test
```

**2.2 — Confirm what actually arrived.** `venv/`, `aiops.db` and
`.aiops_spool/` must be absent. If any of them came through, `.gitignore` is
wrong and the repo is carrying artifacts it should not:

```powershell
Get-ChildItem -Force
Test-Path venv, aiops.db, .aiops_spool
```

**2.3 — Confirm the wheel is present**, since it is deliberately committed for
this hackathon:

```powershell
Get-ChildItem sdk\dist
```

**2.4 — Open the README and work down the Quickstart**, running each command as
written. In order, that should mean:

- create and activate the virtual environment
- `python -m pip install -r requirements.txt`
- install the SDK — `pip install -e ./sdk` for repo work
- set `AIOPS_API_KEY` and `AIOPS_DB_URL`
- run the test suite
- seed the database with `--users 80`
- start the collector
- start the dashboard
- run the demo agent
- run `--replay`
- run the outage demo

**2.5 — For each of those, capture real output**, not an assumption:

| Step | What proves it |
|---|---|
| install | pip's success line and the package count |
| SDK install | `python -c "import aiops; print(aiops.__file__)"` |
| tests | `python -m pytest -q` with its full count |
| seed | the seeder's summary line |
| collector | `/health` returning 200 with the auth mode |
| dashboard | HTTP 200 on 8501, and a metric with a non-zero value |
| demo agent | event count before and after, differing by one |
| `--replay` | the checkup reopening after having been answered |
| outage demo | its own assertion passing and exit code 0 |

**2.6 — The console-shim quirk.** On the working copy, 20 of 21 shims in
`venv\Scripts` hard-code an interpreter path from before the folder moved, so
bare `streamlit`, `uvicorn`, `pytest` and `pip` fail. A *fresh* venv should
generate correct shims.

Check it:

```powershell
streamlit --version
uvicorn --version
pytest --version
```

If those work here, the quirk is local to the old venv and the README's
`python -m` guidance is defensive rather than necessary. Say which it is — it
changes what the README should recommend, and it changes what you type in front
of judges.

**2.7 — The working-directory trap.** `aiops.db` is created in the current
working directory. Starting the collector from a different folder silently
creates a second, empty database and the dashboard then shows nothing. Confirm
the README warns about this, and confirm where the file actually landed:

```powershell
Get-ChildItem aiops.db
```

**2.8 — Clean up:**

```powershell
cd C:\GitRepo
Remove-Item -Recurse -Force aiOps-test
```

---

# TASK 3 — Wheel-only test, a stranger's agent

## Why

Task 2 proves the repo works. This proves the **product** works — the thing an
agent developer actually receives from SharePoint. They have a `.whl` file and
the README section written for them. Nothing else. No repo, no source, no
`pip install -e`.

This is also the strongest thing to show a judge who asks "how would another
team use this?"

## Steps

**3.1 — Copy the wheel somewhere neutral**, so nothing can accidentally resolve
against the repo:

```powershell
$wheel = (Get-ChildItem C:\GitRepo\aiOps\sdk\dist\*.whl).FullName
mkdir C:\Temp\stranger-agent
Copy-Item $wheel C:\Temp\stranger-agent\
cd C:\Temp\stranger-agent
```

**3.2 — Fresh venv, built on the system Python**, not the project's:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3.3 — Install only the wheel.** No `requirements.txt`. If the SDK needs
something it did not declare, this is where it surfaces:

```powershell
python -m pip install .\aiops-*.whl
python -m pip list
```

`httpx` and its transitive dependencies should appear. Nothing from the
collector side — no FastAPI, no Streamlit, no SQLAlchemy — should be pulled in.
If they are, the SDK is dragging the whole platform into every agent's
environment, which would kill adoption.

**3.4 — Confirm the version resolves from the installed wheel**, not from a path:

```powershell
python -c "import importlib.metadata as m; print(m.version('aiops'))"
python -c "import aiops; print(aiops.__file__)"
```

The file path must be inside this temp venv's `site-packages`.

**3.5 — Start a collector** from the real repo, in a separate terminal, so there
is something to send to:

```powershell
cd C:\GitRepo\aiOps
.\venv\Scripts\Activate.ps1
$env:AIOPS_API_KEY = "local-dev-key"
python -m uvicorn api.main:app --port 8000
```

**3.6 — Write an agent from scratch**, using only the README section
"Installing the SDK in your own agent". Do not copy from `demo/`. If the README
does not give you enough to write this file, that gap is the finding.

**3.7 — Run it:**

```powershell
$env:AIOPS_ENDPOINT = "http://localhost:8000"
$env:AIOPS_API_KEY  = "local-dev-key"
python my_agent.py
```

**3.8 — Verify from the store, not the SDK.** The SDK's own counters say what it
*believes* it sent. Only the database says what arrived:

```powershell
cd C:\GitRepo\aiOps
python -c "from api import repository; print(repository.get_recent_events(limit=3))"
```

The event must carry your agent's name, the ACF2 ID you identified with, and an
`sdk_version` matching the wheel.

**3.9 — Clean up:**

```powershell
Remove-Item -Recurse -Force C:\Temp\stranger-agent
```

---

# Report back

Tell me plainly:

1. the new wheel and tarball filenames and sizes, and whether the version should
   be bumped
2. every step in Task 2 that did not work exactly as the README described it
3. every step in Task 3 where you needed something the README did not give you
4. whether the console shims regenerate correctly in a fresh venv, and therefore
   whether the README should keep recommending the `python -m` form
5. whether the wheel pulled in any collector-side dependency it should not have

For 2 and 3, quote what the README says and what you actually had to do. "It
worked" is only useful if you also say what you ran.

Then update `handoff.md` and stop.
