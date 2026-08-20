# 06b — Addendum, to be read last

This goes at the end of the acceptance prompt. Where it and anything above disagree, this
block wins.

## Write the record as you go, not at the end

This is a long run — two environments, every dashboard tab, the spool test, a
from-scratch agent. If the session ends early, everything not yet written down is lost
and has to be run again. So the record is built incrementally:

- After **Environment A completes**, before starting B: append the A results to
  `RELEASE-VERIFICATION.md` — the command / documented / actual table, the regression
  count, and every discrepancy found so far. Then continue.
- After **Environment B completes**: append the B results the same way.
- Keep the running list of findings in the chat as you go too, so a discrepancy found at
  A.4 is visible to me without waiting for the end.

If a step fails badly enough that you have to stop, write what you have to
RELEASE-VERIFICATION first, then stop. A partial record of a run that happened is worth
more than a complete plan for one that did not.

The final summary at the end is still expected — this is in addition to it, not instead
of it.

## Cleanup — do not run it yet

`A.7` and `B.5` delete the test clone and the wheel-only venv. **Do not run either one
until I have read your report and told you to.** If something failed, that environment is
the evidence, and deleting it means re-running the whole thing to look at one detail.

When I do give the word, before each `Remove-Item`:

- Echo the full resolved path and wait for my confirmation. `aiOps` and `aiOps-accept`
  differ by one suffix and the flags are `-Recurse -Force`. Getting this wrong deletes
  the project.
- Confirm nothing is still running out of the directory you are about to remove — stop
  the collector and the dashboard first, so ports 8000 and 8501 are free and no process
  holds a handle to the database.

If I never give the word, leave both directories in place and say so in your final
summary, so it is a known loose end rather than a surprise next week.

## One last time

Follow the documentation literally. An omission is a finding. Build nothing new. Commit
nothing until I have read the report.
