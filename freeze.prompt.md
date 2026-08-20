---
mode: agent
---

# The freeze — commit the run record, close findings 15-20, destroy the pre-rewrite history

The final fresh-clone run returned **go, with one condition**. Its record is written but not
committed. This round makes the repository final. Several steps here are irreversible and the
order below is the whole point of the round — do not reorder it and do not run ahead.

Nothing in this round is exploratory. If something does not match what is described here, stop
and tell me rather than adapting.

**Do not push, and do not add a remote.** Pushing is a separate round and I will run it myself.

## F.0 — Read your own record before committing it

`git status` should show exactly two modified files, `handoff.md` and
`sdk/docs/RELEASE-VERIFICATION.md`, +133/-0. Confirm that, then read the +133 lines back.

One specific thing to check: the leftover collector was identified in two different ways during
the run — once as `C:\Python314\python.exe` in the question you put to me, and later as the
dev-tree venv interpreter (`C:\GitRepo\aiOps\venv\...\python.exe`) in your reasoning after you
verified it with `Get-CimInstance`. Only one of those is what the process actually was. If both
readings reached the written record, the record contradicts itself about the central finding of
the run. Correct it to the verified one and say what you changed.

While you are in there, confirm the record does not claim anything you did not measure, and that
findings 15-20 are numbered consistently with 1-14.

## F.1 — Close findings 15-18

These are documentation wording, not behaviour, and this is the last round in which the
documentation can be made true. Fix all four. Do not touch dated records — the same rules as the
truth pass apply, and the acceptance and fresh-clone records stay as written.

- **15** — the `curl` examples. The Quickstart is Windows-aware everywhere else and then hands a
  PowerShell 5.1 reader a command that cannot run. Give the working form beside the bash one
  rather than replacing it; the reader may be on either shell.
- **16** — the `/v1/events` sentence. The behaviour is correct and only the prose is wrong: bare
  object and bare array are both accepted, the wrapper is what 422s. Rewrite the sentence to
  match what you measured, and make sure the worked example three lines below still agrees with it.
- **17** — `accepted` counts duplicates. Document what a resend actually returns and that no new
  row is stored. This is a contract a teammate will hit the first time they retry by hand.
- **18** — the README never states the flush contract. USAGE-GUIDE's short-lived-agent section is
  correct and complete, so do not restate it — say what `flush()` returning True and False mean,
  in one or two sentences, and link to the section that has the detail.

**19 and 20 are not in this list.** 19 is procedure and is handled in its own round. 20 is closed
in F.3.

Re-run the full suite after these edits — the docs-reading guards read exactly these files, and a
wording fix that trips the count guard or the filename guard must be caught here rather than after
the history is destroyed.

## F.2 — Commit

Stage explicitly, not with `-A`. Show me the diff before committing. Two commits or one, your
call, but the run record and the finding fixes should be distinguishable in the log.

Report the new HEAD.

## F.3 — Tag, and close finding 20

`843053a` is both the commit that built the 0.2.1 wheel and the last commit to touch `dist/`.
Annotate it:

```
git tag -a v0.2.1 843053a -m "<message naming the artifact and its hash>"
```

Tags clone — this is the point. After the freeze, a stranger with a clone can answer "which commit
built this wheel" without asking anyone. Confirm `git tag -l` and `git describe` behave, and note
in the record that finding 20 is now closed and how.

## F.4 — Destroy the pre-rewrite history

This is the irreversible step. Everything above must be committed and verified first.

You established that `refs/original/` never clones — it exists only in this repository, so once it
is gone there is no second copy anywhere. Same for the backup branch after deletion. Before you
run any of this, state in one line what will become unreachable and confirm the tree is clean.

Then, in this order:

```
git branch -D backup/pre-author-rewrite
git for-each-ref --format="%(refname)" refs/original | ForEach-Object { git update-ref -d $_ }
git reflog expire --expire=now --all
git gc --prune-now
```

The reflog expiry is not optional — without it the reflog keeps the old commits reachable and the
gc prunes nothing, which would leave the old identity in the repository while every visible check
says it is gone.

Verify afterwards and show me the output:

- `git log --all --oneline | wc -l` — count, and compare against master's commit count
- `git shortlog -s -n --all` — must show one name only
- `git cat-file -e 5849739` — must fail
- a grep of the whole corpus for the old identity, as in 9.9

## F.5 — Cleanup

The clone's collectors on :8000 and :8010 and its dashboard on :8501 are still running, and
`aiOps-freshclone` still holds a venv, a seeded database and spool directories. Stop the servers
and remove the clone. Report anything still listening afterwards.

Do not delete the acceptance clone or any other directory without telling me first.

## Report

1. What the +133 lines said wrong, if anything, and what you corrected.
2. Each of findings 15-18: the old text and the new text.
3. The suite count after the doc edits, and each docs-reading guard by name.
4. The commits, the tag, and the new HEAD.
5. The full F.4 verification output.
6. What is still running and what is still on disk.

Commit the doc work. Do not push, do not add a remote, do not touch the acceptance clone. If any
verification in F.4 comes back other than expected, stop immediately and tell me — that is the one
place in this project where guessing is expensive.
