---
mode: agent
---

# F.4 continuation — option 2: run F.4, and delete aiOps-accept along with it

Your premise check was right and the prompt was wrong: `refs/original/` has no second copy, but
the commits do. Thank you for stopping.

## Before deleting anything — prove aiOps-accept holds nothing unique

```powershell
git -C C:\GitRepo\aiOps-accept status --short
git -C C:\GitRepo\aiOps-accept log --oneline
git -C C:\GitRepo\aiOps-accept rev-list HEAD | ForEach-Object { git -C C:\GitRepo\aiOps cat-file -e $_ 2>$null; if ($LASTEXITCODE -ne 0) { "MISSING: $_" } }
```

Show me that output. Every one of its 16 commits should already exist in `aiOps`, and the working
tree should be clean.

If anything comes back `MISSING:` or dirty, **stop and tell me — do not delete.**

Note what this check does and does not prove: it runs before F.4, while the backup branch still
holds those commits reachable, so it proves the acceptance clone contains nothing unique — not
that anything survives F.4. After F.4 those 16 commits are gone from both places, which is the
intent.

## If it is clean

1. Run **F.4** exactly as written in the freeze prompt — branch delete, `refs/original/` delete,
   reflog expire, `gc --prune-now`, then the four verifications.

2. Then **F.5, widened**: stop the servers on 8000, 8010 and 8501, and remove `aiOps-freshclone`,
   `aiOps-accept`, `accept-agent` and `accept-agent-021`.

3. Then re-run the corpus grep for the old identity **across every remaining directory on disk**,
   not only inside the repository. That is what the F.4 verification was always meant to prove,
   and this round showed the repository-scoped version of it would have passed while a full second
   copy sat in a sibling directory. Report the command you used and its scope.

## Record

Write into the freeze section that the acceptance clone was deleted, that its evidence survives in
the committed acceptance record from `5de9f1a`, and why deleting a stale scratch clone is not
deleting a record.

Still no push and no remote.
