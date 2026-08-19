mode - agent

Four fixes from the release-verification review. Do them in order, then stop.
Do NOT commit anything. Show me the diffs and I will decide.

---

## FIX 1 — The README's headline example is broken

In the README section "Installing the SDK in your own agent", the snippet
calls `identify(acf2_id=user.acf2)` but never defines `user`. Anyone copying
it verbatim gets a NameError. This is the first code a stranger runs.

- Find every occurrence of that snippet across `README.md`, `sdk/docs/USAGE-GUIDE.md`,
  `sdk/docs/ARCHITECTURE.md` and `sdk/docs/BUILD-JOURNEY.md`.
- Rewrite it so it runs as-is on a clean machine — a literal ACF2 ID with a
  comment saying to replace it, not an undefined object.
- Then prove it: copy the snippet into a scratch file in `C:\Temp`, run it against
  a running collector, and paste the output. If it does not run, it is not fixed.

## FIX 2 — A test selector that proves nothing

The release script used: `python -m pytest tests/test_sdk.py -q -k packaging`

That reports "62 deselected" and passes with zero tests executed. The real
tests are named `test_the_wheel_*`, so the selector is `-k wheel` (3 passed).

- Search the repo — `handoff.md`, `RELEASE-VERIFICATION.md`, `sdk/docs/*`, `README` —
  for every `-k packaging` occurrence and correct it.
- Then audit the other pytest selectors used anywhere in the docs the same way:
  for each one, report the collected count. Any selector that collects zero
  tests is a silent lie and must be fixed or deleted.

## FIX 3 — Write the versioning rule down

Decision: version stays `0.1.0`. Do not bump.

But the rebuild produced different bytes with identical source
(whl `5af9e30` -> `4732728`, tar.gz 29,984 -> 29,996 bytes). That is build
non-determinism, and it matters because the wheel is committed and will be
handed to people via SharePoint.

Add a short "Versioning and release" section to `sdk/docs/RELEASE-VERIFICATION.md`
stating:

- bump the version only when something under `sdk/aiops/` or `sdk/pyproject.toml`
  changes; the verification command is
  `git log <last-release-tag>..HEAD -- sdk/aiops sdk/pyproject.toml`
- the committed wheel is built once and shipped as-is; never rebuild an
  already-distributed version, because the bytes will differ under the same
  filename
- if a rebuild is unavoidable, bump first

Then tell me whether setting `SOURCE_DATE_EPOCH` before `python -m build` makes the
output byte-identical across two consecutive builds on this machine. Test it,
do not guess. If it works, add the command to the doc.

## FIX 4 — Commit policy

During the last run you committed pending work locally (`f3fe910`) without being
asked. The reasoning was sound, but I need to know before it happens.

Add to `handoff.md`, in the working-agreement section: the agent stages and shows
diffs but does not run `git commit` unless explicitly told to in that message.

---

## Report back

1. the corrected snippet and the actual output of running it
2. every file and line you changed for the selector fix, plus the collected
   count for each selector you audited
3. the `SOURCE_DATE_EPOCH` result — byte-identical or not
4. anything you found while doing the above that I did not ask about

Nothing committed. Show me the diffs.
