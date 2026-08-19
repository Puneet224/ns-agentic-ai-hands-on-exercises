mode - agent

# Version bump and rebuild

Run this after Phase 9 is committed, and before the documentation sweep.

Commit nothing. Stop where told.

---

Phase 9 changed SDK source, so the documented rule applies: bump before
rebuilding, and ship the new artifact as built.

## 1 — Confirm the change first

Do not take my word for it:

```
git log <last-release-point>..HEAD -- sdk/aiops sdk/pyproject.toml
```

Paste the output. If it is empty, **stop and tell me** — the bump would then be
advertising a change that never happened, and the next real change would be
invisible. This exact assumption was wrong once before.

## 2 — Recommend the version, then stop

`0.1.0 -> 0.2.0` if the SDK's surface or behaviour changed for a caller.
`0.1.1` if it did not.

Say which and why, naming the change that decides it. **Wait for my answer
before editing anything.**

### STOP HERE.

---

## 3 — After I confirm

- Edit `sdk/pyproject.toml`.
- Delete `sdk/dist/*` rather than overwriting — a failed build must not leave
  the old wheel sitting there pretending to be new.
- Rebuild with `SOURCE_DATE_EPOCH` set so the wheel is reproducible. Note in the
  output that the sdist will still differ; that limitation is already documented
  and is not a new finding.

## 4 — Update the filename everywhere

The wheel filename appears in the README in at least two places, and the
packaging test fails until they match — that is the point of that test.

Search the whole tree. Do not rely on the two places I named.

## 5 — Record it

In `RELEASE-VERIFICATION.md`: new filenames, sizes and hashes. This is the
record that the final acceptance run will check against, so it must be exact.

## 6 — Prove it

```
python -m pytest -q
python -m pytest -q -k wheel
```

Report both counts.

---

# Report back

1. the `git log` output
2. your version recommendation with the reasoning — then stop
3. after my confirmation: every file changed, the new artifact details, and both
   test counts

Nothing committed. Show me the diffs.
