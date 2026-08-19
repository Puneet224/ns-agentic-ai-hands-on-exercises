mode - agent

# Documentation consistency sweep

Run this after the version bump is committed, and before the final acceptance
run.

No code changes. Commit nothing. Report the list before fixing anything.

---

## 1 — Find every document

List every `.md` file in the repo, with its path and last-modified date.

**Walk the tree.** Do not work from any list I have given you in earlier turns —
the point of this step is to find the documents nobody remembered.

If both `docs/` and `sdk/docs/` exist, tell me why, and whether any file is
duplicated across them or has diverged. Two copies of the same guide drifting
apart is worse than one incomplete guide.

## 2 — Current or stale

For each document, say whether it is current after Phase 9 and the version bump,
or stale. Name the specific stale lines — not "needs updating", but the line and
what is now wrong about it.

## 3 — Cross-check the docs against each other

Not just against the code. Docs contradicting each other is the failure mode a
judge actually hits, because they read two files and get two answers.

List every disagreement:

- the same command written two different ways
- the same concept named differently across files
- a version, file count or test count stated in one document and contradicted in
  another
- a workflow described in one document that another says is unnecessary

## 4 — BUILD-JOURNEY needs a Phase 9 chapter

This is the narrative document — it is what shows a judge how the project was
actually built and reasoned about, so it matters more than its file size
suggests.

Draft the Phase 9 chapter in the same voice as the existing chapters. Include
the decisions that were argued, not only the ones that shipped: the precedence
choice, and the concurrency findings.

## 5 — Wheel filename

Confirm the filename in the README matches `sdk/dist/` in every place it
appears. Report each location and whether it matches.

---

# Report back

Report the full list first, with your assessment. **I will tell you what to
fix.** Do not start editing after step 1.

The one thing I want stated plainly: which document should a stranger read
first, and does that document actually work as an entry point today?
