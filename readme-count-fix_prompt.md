---
mode: agent
description: Fix the stale test count in the README and sweep the repo for other figures that have drifted
---

The README's tech stack line says "pytest — 299 tests". That number is
stale — it was in the prompt I gave you and you carried it over.

Do not trust my number or yours. Run `python -m pytest -q` and use the
count it actually reports.

Then grep the whole repo for other stale test counts — `README.md`,
`docs/BUILD-JOURNEY.md`, `docs/ARCHITECTURE.md`, `docs/USAGE-GUIDE.md`,
`handoff.md`. Any figure that claims a test total must match what pytest
just reported.

While you're in there, check the same way for anything else that has
drifted since it was written: phase numbers, tab counts (the dashboard
has four tabs now, including Notify), file paths, and command forms.

Tell me every number you changed and what it was before. If a count
appears somewhere I didn't list, say where.
