---
mode: agent
---

# Phase 9.9 — Loose ends before the final run

Six items, all small. Four you surfaced yourself in 9.8 and did not fix; two are the
cosmetic findings from the acceptance run that have been waiting.

Nothing here is architectural. The point of this round is that after it, nothing is left
that I know about and have not decided on.

## Ground rules

- Commit nothing until I have read the report.
- No cleanup, no server shutdown, no wheel rebuild unless item 3 forces one — and if it
  does, say so before doing it.

## 1 — Phase 9.7 has no record

This is the largest item on the list and the one most against the spirit of everything
this project has done.

Five SDK modules, both demo agents and three documents changed in 9.7 and the timing
round, and the only record is a commit message. `handoff.md` has no entry.
`BUILD-JOURNEY.md` has no chapter. A reader of the narrative document goes from Phase 9.6
straight past the single largest reliability change in the SDK's life.

Write both, in the voice of the existing entries:

- The handoff entry, in the shape the other phase entries use.
- The BUILD-JOURNEY chapter. Include the reasoning that is worth keeping and would
  otherwise be lost: why the probes only reproduced against a black-holing endpoint and
  not a refusing one, why durability was coupled to give-up time, what `True` was decided
  to mean and why "delivered" was rejected, why a connection failure costs no retry
  attempt (bound the store, not the patience), and that the NullHandler intended to
  surface warnings was the thing suppressing them.
- The Reversals table gets the flush contract change, on the same reasoning as last time:
  it is a reversal, and leaving it out is the stale-by-omission gap this all exists to
  close.

Append. Do not rewrite the existing Phase 9 chapter.

## 2 — USAGE-GUIDE's install line

Finding 14, your own. The README's bare `pip install` was fixed in 9.7; the document that
this round proved is the self-sufficient one was not fixed with it. One line, same form
as the README's.

While you are in there, check whether anything else in USAGE-GUIDE drifted from the
README's 9.7 corrections — the two were fixed separately and may have separated again.

## 3 — The lexicographic version sort

`test_the_committed_wheel_matches_the_declared_version` sorts with `sorted(...)[-1]`, so
a stray `0.10.0` in `dist/` is invisible while a `0.3.0` fails. You recorded it and did
not patch it.

Patch it. Compare versions as versions, not as strings. Show the test failing against a
deliberately planted stray before the fix, then remove the stray.

If this changes what the guard considers current and forces a rebuild, stop and tell me
before rebuilding.

## 4 — org_map is empty in the dev database

Zero rows, so Environment B's events carried null business group and division, and
collector-side org resolution went unverified this round.

Seed it and re-verify the resolution path: a mapped ACF2 ID resolving without the caller
passing anything, an unmapped one landing in the unknown bucket, and the precedence rule
holding when caller and map disagree. This was verified in the acceptance run and has not
been checked since the SDK changed underneath it.

## 5 — `unknown` in the Notify draft

Acceptance finding 4. The unmapped bucket's internal name leaks into a draft subject
line, which reads as a bug to anyone who sees it.

Fix it where it renders. Then check whether that bucket name reaches any other
user-facing string — a tab label, a CSV header, a chart legend — since the same mistake
made once is usually made twice.

## 6 — Clipped chart labels

Acceptance finding 5. Axis labels truncate to "Retai" and "unkn", and one metric renders
cut off.

Fix the rendering rather than shortening the underlying data. A judge reads these tabs on
a projector; the numbers being right does not help if the label is unreadable.

## Verification

Full suite with the count updated in README if it moves. The dashboard tabs loaded and
the two cosmetic fixes confirmed visually — tell me what you actually looked at.

## Report

What went into the two 9.7 records and what you deliberately left out. The version-sort
test failing against the planted stray. The org resolution results. What else carried the
unknown bucket name. Anything you found that is not on this list.

Then stop. Next is the author rewrite and the final fresh-clone run.
