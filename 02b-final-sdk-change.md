mode - agent

# The last change before the version bump

Four things. Show diffs, commit nothing.

**This is the final change to `sdk/aiops` before the wheel is rebuilt and the
version bumped, so section 4 matters as much as section 1.**

---

## 1 — Identity under concurrency

Read the "Identity under concurrency" section in `ARCHITECTURE.md` and the
`xfail` in `tests/test_concurrency.py` first — that is the bug this fixes.

Decision: **option (a).** The process-wide identity default becomes opt-in
instead of a side effect of `identify()`.

- `identify()` writes the ContextVar only. It must never write the process-wide
  default.
- `AIOPS_ACF2_ID` (and an explicit `init()` argument, if that path exists) keeps
  setting a process-wide default, because declaring one is the point of that
  variable.
- `get()` with no identity in context and no declared default drops the event
  with a one-time warning naming the likely cause.

Reason: today the SDK can attribute an event to the wrong person and nothing
warns. For an adoption tracker a wrong name is worse than no event. This makes
wrong attribution impossible — either the right ACF2 ID or none.

Turn the `xfail` into a passing test. Then add the case it does not cover: a
single-user agent that calls `identify()` at startup and does tracked work on a
worker thread. Under this change its events now drop. Show me that as a test
with the warning captured, and say plainly in the docs that such an agent must
set `AIOPS_ACF2_ID`.

**Also tell me whether any demo agent, test fixture or the README's example
falls into that newly-dropping case.** If one does, that is a regression I need
to know about before it reaches a judge.

## 2 — The seed now maps everyone, so the unknown bucket is empty

Session 2's seed reported `25/25 users mapped, 0 unknown`.

That means the demo store has no org-less users at all, and everything built in
the earlier round — the `unknown` bucket, its filter option, the reconciliation
test — has nothing to display. A judge who opens the Division filter will not
see `unknown` offered, because no row needs it.

Leave a small number of seeded users deliberately unmapped. A real directory
extract never covers everyone, so this is more realistic than full coverage, not
less. Pick the number, say what you picked and why, and confirm afterwards that
the `unknown` bucket appears in the chart, is offered in both dropdowns, and
that selecting it returns exactly those users.

## 3 — A mismatched map key style looks identical to an unmapped population

You flagged this and left it: nothing checks that the map's key style matches
what agents actually send. Loading a plaintext map for hashing agents — or the
reverse — produces `0/N mapped`, which is indistinguishable from a directory
extract that genuinely covers nobody.

This is the same failure family as everything else this project has had to fix:
a wrong state that renders as a plausible one. Make it say so. A warning on the
loader, on the status line, or both — your choice, but the operator must be able
to tell "the map does not match your agents" from "the map is empty".

Recommend the check before you build it if you think there is a cheaper signal
than the one I am describing.

## 4 — Confirm the SDK is finished

After this change the wheel gets rebuilt and the version bumped, and
`sdk/aiops` should not move again before the freeze.

So, plainly: **is there anything else you were about to change under
`sdk/aiops`, or anything you know is wrong there and have not raised?** Say it
now rather than after the rebuild. Include anything you deferred, worked around,
or left as a TODO in earlier phases.

Also: the loader's unsalted SHA-256 fallback is flagged by the security linter,
and this repo runs Checkmarx. Tell me whether that finding will block a
pipeline, and if it will, what the suppression should say — the parity argument
is correct and I do not want it silently changed to satisfy a scanner.

## Documents to update

`ARCHITECTURE.md` §9 and §10, `USAGE-GUIDE.md`, `README.md` if the identity
guidance moves, and a `handoff.md` entry.

## Report back

1. the `xfail` now passing, and the new dropping test with its warning
2. anything that fell into the newly-dropping case
3. the unmapped-user count you chose, and the `unknown` bucket confirmed live
4. the map key-style check, and what you recommend
5. **anything else pending under `sdk/aiops`** — the answer to section 4
6. the Checkmarx answer
7. files and lines changed, docs changed

Nothing committed. Show me the diffs.
