---
mode: agent
---

# Final fresh-clone run — Environment A, for the last time

Everything is committed. The tree has not changed since the 9.9 handoff entry, and
nothing further is planned before the freeze. This is the last chance for the repository
to be wrong in a way nobody has noticed.

Environment B was re-run on the 0.2.1 wheel in 9.8 and does not need repeating. This is
the teammate-facing path only: someone clones the repo and follows the README.

## The rule

Follow the documentation literally. If you run a command the docs do not give you, that
omission is the finding, and it is worth more than a passing test. Record every such
moment.

Do not fix anything you find. Record it and keep going unless it blocks the run.

## Before you start

Clone into a fresh directory outside the working tree, and **tell me which branches and
refs arrive in the clone**. The pre-rewrite backup branch still exists deliberately; I
want to see it in the clone listing rather than discover it later. Do not delete
anything.

Fresh venv. Dump the environment first and record which `AIOPS_*` variables are already
set in the shell — unset them, since a value inherited from the dev shell would make an
identity check pass for the wrong reason.

## A.1 — What arrived

`venv/`, `aiops.db` and the spool directories must be absent. `sdk/dist/` must hold the
0.2.1 artifacts and nothing else. Confirm the wheel hash against the one recorded in
RELEASE-VERIFICATION.

`setup.ps1` must be absent. The scratch probes deleted in 9.9 must be absent. The
directory extract must be absent — it is gitignored, so if it appears the ignore rule is
wrong.

## A.2 — Quickstart, literally

Work down the README Quickstart running each command exactly as written, from inside the
clone. Record command / documented / actual for every step.

Specific things that have moved since the last fresh-clone run and are therefore the most
likely to be wrong: the test count, the venv step, the `python -m pip` form, the
`/v1/events` payload section, the flush-contract wording, and every version string.

## A.3 — Full regression

`python -m pytest -q`. Report the count and compare against what the docs claim. Then
confirm the guards by name: the docs-selector guard, the packaging tests, the
wheel-filename guard, the bytes-match guard, the count guard, the org-attribute rendering
guard, the three dashboard legibility guards, and the Phase 9 concurrency tests.

## A.4 — Every surface

Capture real output. "It worked" is only useful with the command and the result beside it.

Collector, seed, and all four dashboard tabs. The org charts with labels rendered in full
— that was fixed in 9.9 and this is the first fresh-clone check of it. The Notify draft
subject line, which is the other 9.9 fix. Demo agent, `--replay`, outage demo.

The offline spool: stop the collector, run `claims_agent.py --once`, confirm the event
reaches the spool and the agent's message is honest, restart the collector and confirm it
drains. This is the scenario the whole reliability arc was about and it has never been
exercised from a fresh clone.

## A.5 — Org resolution

Run the promoted probe, `tests/acceptance/org_resolution_live.py`. It was written against
the dev database; this is the first time it runs against a freshly seeded one. If the
seed does not populate the org map in a fresh clone, that is a finding and a serious one.

## Report

1. Every step where the documentation did not match what you had to do, quoting both.
2. The branches and refs the clone carried.
3. The regression count and any difference from the recorded count.
4. Each surface in A.4 with its command and actual output.
5. The spool result and the org-resolution result.
6. Anything that would embarrass this project in front of a judge.
7. Your go / no-go on freezing, with the reason. A no-go is a perfectly good outcome.

Write the results into RELEASE-VERIFICATION as you go rather than only at the end, and
add a handoff entry for this run.

Commit nothing until I have read it. Do not clean up, do not delete any ref, do not run
gc, and leave the servers alone.
