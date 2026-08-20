# 06a — Amendments to the final acceptance prompt

Run the acceptance prompt below, with these amendments. The prompt was written before
Phase 9 closed, so where it and this block disagree, this block wins.

## Before you start

Dump the environment and record which `AIOPS_*` variables are already set in this shell.
Unset them for Environment B. Everything runs on one machine, so a value inherited from
the dev shell would make an identity test pass for the wrong reason and neither of us
would see it.

## A.1

Also confirm `setup.ps1` is absent from the fresh clone. It was deleted this week. If it
is there, the clone is not what you think it is and you should stop.

## A.3

Five guards now, not four. Add the wheel-filename guard (`..._dist_filename_...`) and the
count guard (`test_documented_full_run_totals_match_the_collected_suite`). The docs record
437.

## B.3

The prompt says write the agent from the README section. Write it from USAGE-GUIDE as
well, separately, and tell me which of the two is self-sufficient on its own. The copyable
sample in USAGE-GUIDE changed this week and this is the first time anyone reads it cold.

## B.4

Identity is settled, so stop treating it as open. The modes are: explicit single-argument
`identify(acf2_id=...)`, `AIOPS_ACF2_ID`, and OS-user fallback. There is no process-wide
default any more.

Add a fourth case that is not in the list and matters more than the three: no
`identify()`, no env var — the event must be dropped with the one-time warning, never
misattributed.

## Everything else

Everything else in the prompt stands as written, including: follow the documentation
literally, an omission is a finding, build nothing new, and commit nothing until I have
read the report.
