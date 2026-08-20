---
mode: agent
---

# Phase 9.8 — Rebuild the wheel, and make staleness impossible to miss

Tree is committed at 448c1fa, suite green at 445. The SDK changed substantially in 9.7
and the timing round: queue.py, spool.py, transport.py, client.py and `__init__.py` all
moved. The wheel in `sdk/dist/` predates every one of those changes.

You flagged this yourself as arguably a sixth finding. This round closes it.

## Ground rules

- Commit nothing until I have read the report.
- Do not clean up any acceptance directory or stop any server yet.
- Write the record as you go, into RELEASE-VERIFICATION, rather than only at the end.

## 1 — The guard first, failing

Build the guard before the rebuild, so it fails against the wheel that is committed
right now. That failure is the proof the gap was real, and it is worth more than a green
run afterwards.

The existing wheel tests check version, module presence and metadata. None of them check
that the packaged bytes match the source they claim to package. Write the one that does.

Design questions to answer before writing it, not after:

- What exactly do you compare? Module-by-module content is the honest answer; anything
  cheaper (file count, total size, mtime) will pass on a stale wheel eventually.
- Where does the comparison read the wheel from? If it builds a fresh wheel to compare
  against, it is testing the builder rather than the artifact, and it will be slow. If it
  reads `sdk/dist/`, it is testing the thing we actually ship — prefer that, and say what
  it costs.
- Normalisation: compiled artifacts, `__pycache__`, line endings on Windows, and the
  metadata files that legitimately differ between builds. Say what you exclude and why
  each exclusion is safe rather than convenient.
- Naming, same discipline as before: it must not fall into any documented `-k` selection.
  Confirm `-k wheel` still reports the number the docs claim after you add it.

Show me it red against the current committed wheel before you rebuild anything.

## 2 — Version and rebuild

Bump to 0.2.1. This is not a cosmetic bump: the flush contract changed meaning, the retry
budget changed behaviour, and a caller who upgrades gets different semantics from the
same API. Say in the changelog or release notes what a caller would notice.

Then rebuild, and record the new artifact filenames, byte sizes and sha256. Confirm the
filename guard from the earlier round still selects the live citations correctly now that
the version moved — that guard exists precisely for this moment, so tell me whether it
caught anything that needed updating, or whether the docs were already right.

The new guard from step 1 must now be green. If it is not, the wheel and the source
genuinely disagree and I want to know that before anything else happens.

## 3 — Environment B, on the real wheel

The wheel-only environment has been testing a stale SDK for two rounds. Rebuild the
temporary venv from the new wheel and re-run it properly:

- Seven packages, nothing collector-side.
- The from-scratch agent from USAGE-GUIDE, since that is the document that proved
  self-sufficient.
- All four identity modes, including the drop case with no identify and no env var.
- Collector up: delivered. Collector down: spooled, honest message, warning visible on a
  host with no logging configured.
- The spool probes against the wheel-installed SDK, not the editable install — worst case
  at the default timeout, idle and with a drain in flight. I want to see the 5.0s bound
  hold from outside the repo.

## 4 — The acceptance record

`RELEASE-VERIFICATION.md` and `handoff.md` now describe behaviour that no longer exists:
findings 1-3, the old timing table, the "Telemetry sent." transcript, the discard note,
the NullHandler paragraph, and the 437 totals.

Do not rewrite them. They are dated records of runs that happened, and the evidence is
the point. Add a supersession banner at the head of the affected section pointing forward
to this round, in the same style as the one already at RELEASE-VERIFICATION:110 — beside
the evidence, not over it. One banner, not several; you were right last time that a
document with a banner every few screens stops reading as trustworthy.

## Report

The guard's red run against the old wheel and its green run against the new one. The new
artifact hashes. Environment B's results including the probe timings from the
wheel-installed SDK. What the version bump means for a caller. Anything you found that is
not on this list.

Then stop. Findings 4 and 5, cleanup, and the push are all separate.
