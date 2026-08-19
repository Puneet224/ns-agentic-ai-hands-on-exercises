---
mode: agent
description: Build the SDK as a distributable wheel, verify it in a clean venv, and document the install path
---

Build the SDK as a distributable wheel and document the install path.

## 1. Check the package metadata

Confirm `sdk/pyproject.toml` declares `httpx` as a runtime dependency, plus
correct name (`aiops`), version, description, and `python_requires`.

Anything the SDK imports at runtime must be declared — a wheel that installs but
fails on import is worse than no wheel.

## 2. .gitignore — keep `dist/` tracked

Add `build/` and `*.egg-info/` to `.gitignore`, but do **NOT** ignore `dist/`.

The wheel is committed deliberately for this hackathon so judges can see and
install it straight from the repo. Note in the README that in production it
would be published to an internal package index instead. Add `dist/` and `*.whl`
to `.gitignore` later, not now.

## 3. Build it

Run `python -m build sdk/` and confirm the output filename.

## 4. Verify it properly

Create a throwaway venv **outside this repo**, install the wheel into it, and run
a three-line integration script that imports `aiops`, tracks a call, and confirms
the event reaches a running collector.

Show me the real output. This proves the wheel works for someone who has never
seen this repo.

## 5. Document the install path

Add a README section **"Installing the SDK in your own agent"** with:

- the wheel install command
- the two env vars (`AIOPS_ENDPOINT`, `AIOPS_API_KEY`)
- the three-line integration

Write it for an agent developer who has no access to this repo — they have the
wheel file and nothing else.

---

Then update `handoff.md` and stop.
