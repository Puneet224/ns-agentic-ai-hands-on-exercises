# 05 — Documentation truth pass

You produced the consistency sweep in the previous session and built the wheel-filename
guard (`test_every_installable_dist_filename_in_the_docs_is_the_one_that_is_built`,
test_sdk.py:1030). Suite is at 436 passed. README.md and test_sdk.py are modified and
uncommitted. This prompt is the fix pass for what you reported and did not fix.

## Working agreement

- Stage and show diffs. Do not run `git commit` unless I say so in a later message.
- Every new test is written failing first, and you show me the failure before the fix.
- Work the sections in order. Report at the end of each section, then continue.
- If a fix is wrong or the reasoning behind it does not survive contact with the code,
  stop and say so rather than making the document agree with the prompt.

## Ground rule for the whole pass

A line is a **live instruction** if a reader acts on it — types it, copies it, or
believes it about the code as it stands today. A line is a **historical record** if it
states what happened on a dated run. Fix the first. Never rewrite the second: the
RELEASE-VERIFICATION result tables, handoff.md (immutable per handoff.md:15), and the
Phase 6.1 narrative in BUILD-JOURNEY are evidence, and editing evidence to agree with
the present turns it into fiction.

---

## 1 — README.md and USAGE-GUIDE.md, live instructions

| Where | Fix |
|---|---|
| README.md:108 | Expected output of `version('aiops')` is `0.2.0`, not `0.1.0`. |
| README.md:230 | `# 360 passed` → the real number after this session's suite. Must agree with README.md:31. |
| README.md:45 | "all five tables" → six. `org_map` landed in Phase 9. |
| README.md:445 | "six packages and nothing else" → seven, and check the named list is complete: aiops, httpx, anyio, certifi, h11, httpcore, idna. |
| README.md:143 | Do **not** change the value. `"version":"0.1.0"` is `API_VERSION` at health.py:14 and is correct. Label it — make it unambiguous that this is the collector API version, not the SDK version, because it currently sits ~35 lines after a `pip install aiops-0.2.0` line and reads as a failed install. |
| USAGE-GUIDE.md:180 | "six packages in total" → seven. Same list as above. |
| USAGE-GUIDE.md:595 | The three-argument `identify(acf2_id=..., business_group=..., division=...)` in "A synchronous agent" → the one-argument form. This is the highest-value fix in the pass: it is the only error that teaches a reader to do the wrong thing, and the same file argues against it at :128 and :249. Check the whole file for any other copyable sample still in the three-argument shape. |
| .github/README.md:8 | Lists 7 phase prompts; the folder holds 9 (`phase-0-bootstrap` absent from the list, `fix-drift` present). |
| .github/README.md:79 | Lists `/phase-7-cost` as a phase to run. It was deliberately never built — BUILD-JOURNEY's "What was deliberately not built" says so. Say so here too rather than deleting the line silently. |

After these, re-run the two existing doc guards and confirm they still pass.

## 2 — setup.ps1

The one item on the list that can damage a stranger's clone rather than merely misinform
them. It sits at the repo root next to README.md, is named in no document a reader will
open, and overwrites `.gitignore`, `.env.example` and `requirements.txt`
unconditionally. The only warning is handoff.md:85, inside a 2,913-line log.

Pick one and tell me which, with the reason:

- **(a)** Delete it, and note the removal where a reader of RELEASE-VERIFICATION's clone
  listing would otherwise expect to see it.
- **(b)** Keep it and name it in README's repo-layout section with one line: what it was
  for, and that it must not be run against an existing clone.

Do not do both. Do not leave it unnamed.

## 3 — ARCHITECTURE.md, present tense against deleted code

- :64 — `identity.py  ACF2 context (ContextVar + process fallback)`. The process fallback
  was deleted in d77e14c and §9 of this same file says so explicitly.
- :401 — end-to-end trace step 3, "resolve identity (ContextVar, then process fallback)".
  Same defect.
- :77 — "the five SQLAlchemy tables" → six. §3 four lines later already says six.
- :81 — "the default six-question Checkup". questions.py defines five top-level questions
  plus three conditional follow-ups; README states it correctly. Match README's wording.
- :562 — `/health` "also reports the store URL". It returns `status`, `database`, `auth`,
  `version` and never has reported a store URL. Fix against the code, not against README.

## 4 — BUILD-JOURNEY.md

This is the largest gap and it needs prose, not token swaps.

- :545 — describes `IdentityStore.set()` writing a process-wide default, recorded as a
  strict xfail. Both halves are false since d77e14c. It is written as a standing
  description of the SDK and it is the last word this file has on the subject. Rewrite
  the paragraph so the Session 2 finding stays readable as a finding, and the resolution
  follows it. The test is now
  `test_identity_set_in_one_thread_does_not_follow_work_into_a_pool`, 12 passed / 0 xfailed.
- :588 — bug table row "Identity leaks across users into a thread pool (Phase 9, open)".
  Closed in d77e14c. Close the row and cite the commit.
- :391 — "`python -m build sdk/` produces `sdk/dist/aiops-0.1.0-py3-none-any.whl`". The
  chapter around it is legitimately Phase 6.1 history; the verb is not. Put the sentence
  in the past tense so it stays true, rather than updating the version.
- **Session 3 is missing entirely.** Phase 9.6 — the identity fix, the 12% unmapped seed
  population, the key-style mismatch check, the two SDK bugs from the pre-freeze audit,
  and the 0.2.0 bump — has no narrative anywhere in this file. Write it in the voice of
  the existing chapters.

The Phase 9 chapter already covers Sessions 1 and 2, including the precedence choice, the
hashing argument, the rejected provenance column and the concurrency findings. Do not
rewrite it. Append.

## 5 — A third guard: the stated test count

The reason README:31 and README:230 disagreed is that no test asserts either of them.
Add a guard in the documentation block of test_sdk.py, same shape as the two beside it:
iterate, accumulate `problems`, one assert naming every failure.

Design constraint you must solve before writing it: the count is only meaningful for a
full run. Under `-k`, `-x`, or any deselection the live number is not the documented one,
and a guard that fails under `pytest -k wheel` is worse than no guard. Decide how to
handle that — subprocess collection, skipping when deselection is active, or asserting
against collected rather than passed — and tell me which you chose and what it costs.

Same naming discipline as last time: choose a name that does not get swept into any
`-k` selection documented in the docs. Confirm `-k wheel` still reports 3 passed after
you add it, and re-check the count in README once the suite total moves.

## 6 — The wheel-staleness contradiction

handoff.md:2910 and RELEASE-VERIFICATION.md:110 say the committed wheel is stale.
RELEASE-VERIFICATION.md:152, "Release 0.2.0 — executed", says it is not. handoff is
immutable, so it is RELEASE-VERIFICATION that has to resolve its own two answers — :110
was true when written and is now superseded by :152. Make the supersession explicit at
:110 rather than deleting it.

## Explicitly out of scope

- The 40-line sidebar-filter table duplicated across USAGE-GUIDE.md:445 and
  ARCHITECTURE.md:637. They currently agree. Leave the duplication and add nothing.
- handoff.md — immutable, including its three historical `pip install aiops-0.1.0` lines.
- RELEASE-VERIFICATION's dated run records (`435 passed`, `327 passed`) and its six tables
  of superseded hashes.
- copilot-instructions.md and the phase prompts — process input, not a description of the
  result.

## Report

At the end: files touched, tests added and the failure each showed first, the final suite
count, the two decisions I asked you for (setup.ps1, and the count-guard trade-off), and
anything you found while working that is wrong and is not on this list.
