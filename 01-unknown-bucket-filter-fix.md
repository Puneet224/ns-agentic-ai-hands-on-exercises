mode - agent

One change. Show diffs, commit nothing.

---

## The Division filter cannot reach the bucket the chart shows

`repository.py:860` `list_org_values()` filters nulls out, so the Division and
Business Group dropdowns never offer `unknown` — while `_org_chart` at
`app.py:287` renders that bar. Selecting any named division silently excludes
those users, and the counts stop reconciling. A judge who clicks a filter will
see numbers that do not add up.

This is independent of any future org-enrichment work: unmapped ACF2 IDs will
always land in that bucket, so the bucket must be reachable.

## Steps

- Make the Division and Business Group dropdowns offer `unknown` whenever null
  rows exist, and make selecting it filter to exactly those rows.
- Do not invent a new sentinel string in the query layer if one already exists
  at `repository.py:675` — reuse it, so the chart label and the filter value are
  the same token. If they cannot be the same, say why.

## Test — must fail on current behaviour first

Write it, run it against the unfixed code, and paste the failure. Then fix and
paste the pass. A test that only ever passed proves nothing.

- seed one org-less user
- assert `unknown` is offered in the dropdown
- assert selecting it returns exactly that user
- assert the sum across all dropdown options equals the unfiltered total

## Also check

Does the same asymmetry exist anywhere else — Feedback tab, Reliability tab,
Notify audiences? For each, say whether the filter and the chart agree, and
name the file and line you checked. If one of them is already correct, say
which pattern it uses; that is the pattern the others should follow.

## Documents to update

Update whatever the change makes stale — at minimum check `ARCHITECTURE.md`
(the query-layer section) and `USAGE-GUIDE.md` (any dashboard-filter
description). Add a `handoff.md` entry for this turn.

If a doc is already accurate, say so rather than editing it to look busy.

## Report back

1. the failing test output, then the passing one
2. every file and line changed
3. the answer on the other three tabs
4. which docs you updated and which you deliberately left alone

Nothing committed. Show me the diffs.
