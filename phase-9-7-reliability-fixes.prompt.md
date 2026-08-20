---
mode: agent
---

# Phase 9.7 — Reliability fixes from the acceptance run

The clean-machine acceptance run found five judge-facing problems and four
documentation gaps. This round fixes the first three findings, which are all in the same
code path, and closes the doc gaps. Findings 4 and 5 are cosmetic and are a separate
round — do not touch them here.

`tests/acceptance/spool_probe.py` and `tests/acceptance/spool_timing.py` are in the repo
now. They are the reproduction of finding 1 and the starting point for this round.

## Ground rules

- These are defects in the code. Do **not** fix them by editing the documentation to
  describe the broken behaviour. You already made that call correctly during acceptance;
  hold it here.
- Each fix gets a failing test first, derived from the probes, and you show me the
  failure before the fix. Those tests stay in the suite permanently — the reason these
  bugs survived 437 tests is that nothing covered a short-lived agent against a dead
  collector.
- Fix the three findings in order. They are related but not identical, and I want to see
  which behaviour changes with which fix.
- Commit nothing until I have read the report.
- When the suite total moves, update README's count in the same change — the count guard
  will fail otherwise, and that guard failing is the system working.

## Finding 1 — a short-lived agent silently loses events

Measured: with the collector stopped, `flush(timeout=5)` returns `False` after ~5.2s and
the event reaches neither the store nor the spool. 5s lost, 15s lost, 30s spooled.
Meanwhile the agent prints "Telemetry sent." `outage_demo.py` only passes because it is
long-lived.

Two things are wrong and both need fixing:

1. **Events must not evaporate.** If `flush()` cannot deliver within its timeout, whatever
   is still in the queue belongs in the spool, not in nothing. Work out why the current
   path drops it instead of spooling — whether the spool write is on a code path that
   only runs on a longer timer, or whether the queue is discarded on timeout — and say
   what you found before you change it.
2. **`flush()` returning `False` must be visible to the caller.** The agent printing
   "Telemetry sent." after a failed flush is the actual embarrassment here. Decide
   whether the demo agents should check the return value, or whether the SDK should make
   this harder to get wrong, and tell me which you chose and why. A judge reads the demo
   agents.

Do not fix this by lengthening the default timeout. A longer timeout moves the cliff; it
does not remove it.

One more thing the committed probes exposed: `flush(timeout=30)` returns `True` after
13.7s having spooled the event, not delivered it. Decide and document what a `True`
return actually promises — delivered, or safely persisted somewhere it will be retried
from. Both are defensible; the current state, where the caller cannot tell which
happened, is not. Whatever you decide, the demo agents' "Telemetry sent." message must
match it.

## Finding 2 — the spool spends its retry budget on an unreachable collector

The `attempts < 5` budget exists to stop retrying something that will never succeed. But
a connection failure is not the same as a rejection: a collector that is down will come
back, a payload the collector refuses will not. Right now `init()` and each 60s retry
burn an attempt against an unreachable collector, so a long outage silently discards the
backlog the spool exists to protect.

Separate the two cases. A rejection should count against the budget. A connection failure
should not — or should count on a different, much larger budget. Say which you chose.

## Finding 3 — drops are invisible

`NullHandler` suppresses `lastResort`, so the warning never reaches a user who has not
configured logging, and `stats()['dropped']` stays at `0` regardless. The warning text
itself is good; nothing sees it.

`stats()` must count drops honestly — that is the programmatic surface and it is
currently lying. For the log path, the SDK is a library and should not hijack a host
application's logging config, so find the smallest change that makes a drop noticeable
without doing that, and explain the trade-off you picked.

## The four documentation gaps

These came from following the docs literally in a clean environment. Fix them where the
document is wrong, not where the code is:

1. README §8 calls the Checkup an adaptive interview you walk through. Nothing is typed —
   `run_checkup()` replays a scripted dict, with no `input()` and no TTY check. Say what
   it actually does.
2. The raw `/v1/events` payload shape is documented nowhere and cost two 422s during
   acceptance. Document it: `agent_name` (not `agent`), `sdk_version` and
   `python_version` required, and the body being a bare object or bare list rather than a
   wrapper.
3. USAGE-GUIDE §3 explains `fallback_to_os_user` at length but never shows how to turn it
   on; the syntax sits ~200 lines later in the options table. Put the call form where the
   explanation is.
4. The Quickstart uses `python -m pip` throughout, while "Installing the SDK in your own
   agent" uses bare `pip` and never says to create a venv first. Make them consistent and
   add the venv step.

## Verification

Re-run only what this round touched, not the whole acceptance:

- The three new tests, each shown failing first.
- The full suite, with the README count updated to match.
- The spool probes against the fixed code — the same 5s / 15s / 30s measurements, so we
  can put the before and after side by side.
- `claims_agent.py --once` with the collector stopped: the event must end up in the
  spool, and the agent must not claim it was sent.
- Environment B's wheel-only agent once more, since the SDK changed. A fresh wheel build
  is needed for that — say so rather than testing the old one.

## Report

What you found before each fix (the actual cause, not just the symptom), the two design
choices I asked you to make and why, the before/after probe numbers, the new suite total,
and anything this round touched that the acceptance record now describes incorrectly.

Then stop. Do not commit, do not clean up, and do not rebuild the release wheel until I
have read this.
