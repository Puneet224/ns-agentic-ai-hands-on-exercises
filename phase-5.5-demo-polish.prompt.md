---
mode: agent
description: Phase 5.5 — pin a working ACF2 ID for the feedback demo, and reseed at rollout scale
---

Two things before we finish.

## 1. Pin a working ACF2 ID for the feedback demo

The `--feedback` demo needs a seeded ACF2 ID that is genuinely due, not a fresh
one. Put a specific working ACF2 ID directly in the README quickstart and in the
demo script's `--help` text, with a one-line note on why a fresh ID shows
nothing.

This is the exact gotcha that breaks a live demo.

## 2. Reseed at rollout scale

Run `--users 80` and reseed so the store reads as a rollout rather than a pilot.
Confirm seeding still completes in a few seconds and the dashboard still renders.

---

Then update `handoff.md` and stop.
