---
mode: agent
description: Phase 2.5 — reverse the OS-username identity fallback; fail loudly instead of silently polluting data
---

One change to the identity fallback, then stop.

The OS-username fallback is the wrong trade-off. A wrong-but-plausible ACF2 ID is
more dangerous than a missing one — it silently pollutes the adoption data, and
no one downstream can tell a real identifier from an OS login. Silent bad data is
worse than a loud gap.

Change it to: when `identify()` has not been called, log a clear WARNING once per
process naming the agent, and drop the event. Add a config flag
`fallback_to_os_user` defaulting to `False`, so a team that genuinely wants the
old behavior can opt in explicitly.

Update the test that pins the current behavior, add one asserting events are
dropped and the warning fires when identity is missing, and record the reversal
in `handoff.md` so no later phase reintroduces it.

Then stop. Do not start Phase 3.
