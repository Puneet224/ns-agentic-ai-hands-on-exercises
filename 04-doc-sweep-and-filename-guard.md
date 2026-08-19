mode - agent

# Documentation consistency sweep

Run this after the version bump is committed, and before the final acceptance
run.

No code changes except the one guard test in section 6. Commit nothing. Report
the list before fixing anything.

---

## 1 — Find every document

List every `.md` file in the repo, with its path and last-modified date.

**Walk the tree.** Do not work from any list I have given you in earlier turns —
the point of this step is to find the documents nobody remembered.

If both `docs/` and `sdk/docs/` exist, tell me why, and whether any file is
duplicated across them or has diverged. Two copies of the same guide drifting
apart is worse than one incomplete guide.

## 2 — Current or stale

For each document, say whether it is current after Phase 9 and the 0.2.0 bump,
or stale. Name the specific stale lines — not "needs updating", but the line and
what is now wrong about it.

**Apply the distinction you drew during the bump:** a historical record that
describes what was true at the time is not stale, and rewriting it would turn
evidence into fiction. A live instruction, or a statement written in the present
tense about how the system behaves now, is a different thing. For anything you
call stale, say which of the two it is.

## 3 — Two you already found

You flagged these during the bump. They are in scope now:

- `BUILD-JOURNEY.md:545` still describes the identity leak in the present tense
  — `IdentityStore.set()` writes a process-wide default, recorded as a strict
  `xfail` rather than patched. It was closed in `d77e14c`.
- `BUILD-JOURNEY.md:588` labels that bug "(Phase 9, open)".

You said this needs a paragraph rather than a token swap, because the file has
no Session 3 section. Write that paragraph in the same voice as the surrounding
narrative — the leak was found, the three options, the one chosen, and why.

## 4 — Cross-check the docs against each other

Not just against the code. Docs contradicting each other is the failure mode a
judge actually hits, because they read two files and get two answers.

List every disagreement:

- the same command written two different ways
- the same concept named differently across files
- a version, file count or test count stated in one document and contradicted in
  another
- a workflow described in one document that another says is unnecessary

## 5 — BUILD-JOURNEY needs a Phase 9 chapter

This is the narrative document — it is what shows a judge how the project was
actually built and reasoned about, so it matters more than its file size
suggests.

Draft the Phase 9 chapter covering both sessions. Include the decisions that
were argued, not only the ones that shipped: the precedence choice, the
concurrency findings, and the two SDK bugs the pre-freeze audit turned up.

## 6 — Close the gap you named

You said it yourself after the bump: `test_the_committed_wheel_matches_the_declared_version`
keeps `dist/` and `pyproject.toml` in agreement, but **no test asserts the
README's wheel filename against the built one.** Those four edits were caught by
grep, not by the suite. Next time grep misses one.

Add that guard, in the same shape as
`test_every_pytest_command_in_the_docs_selects_something`: scan the docs for
wheel filenames and assert every one that is a live instruction matches what is
actually in `sdk/dist/`.

The hard part is the exclusion — historical records legitimately name old
filenames, and the test must not fail on those. Say how you distinguish them,
and if you cannot do it reliably, say so and propose something narrower rather
than shipping a test that will cry wolf.

Show it failing first: change one README filename by a character and paste the
failure.

This will move the test count, so update the README's count and any other doc
that states it.

---

# Report back

Report the full list from sections 1, 2 and 4 first. **I will tell you what to
fix.** Do not start editing after step 1 — except section 6, which you can build
straight away since it is a gap you already identified.

The one thing I want stated plainly: which document should a stranger read
first, and does that document actually work as an entry point today?
