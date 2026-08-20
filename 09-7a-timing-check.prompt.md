---
mode: agent
---

# 9.7a — Timing check before I read the diff

Four things about timing. Answer with measurements, not description.

## 1 — The probe output, before and after

Full lines as the probe prints them, not a summary. All three timeouts: 5s, 15s, 30s.

## 2 — The default flush timeout

What is it, and with the collector down, what is the longest a caller now waits inside
`flush()` at that default? Measure it, do not reason about it.

This is the number the demo will actually show, and the probe does not cover it because
the probe passes explicit timeouts.

## 3 — The happy path

Whether your fix changed how long anything takes when the collector is **up**. Time one
normal flush against a live collector, before and after.

A reliability fix that adds latency to the happy path is a different trade-off from the
one I approved, and I want to know if I am making it.

## 4 — What a judge runs

What `claims_agent.py --once` now prints and how long it takes, collector down, start to
exit. That is the exact thing a judge runs.

## If anything got slower

Say so plainly and tell me why the extra time is necessary. I would rather ship a slow
honest flush than a fast lying one, but I want to choose it rather than discover it
during the demo.
