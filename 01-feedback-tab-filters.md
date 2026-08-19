mode - agent

# The Feedback tab ignores the sidebar filters

Show diffs, commit nothing.

---

## Why this matters more than it looks

You found this while doing the null-attribute work and correctly left it alone as
out of scope. It is now in scope.

`get_feedback_summary`, `get_checkup_stats` and `get_feedback_responses` take
only `agent_name`. Neither the org filters nor the date range reach that tab.
Only "Sentiment against usage" (`app.py:370` -> `get_sentiment_vs_usage`)
filters by org.

So every number on the Feedback tab — average sentiment, response rate,
self-reported time saved, checkups raised, the distribution, the funnel, the
barriers table — is all-time and all-org, no matter what the sidebar says.

The demo failure is specific: someone sets Division to Retail Bank, opens
Feedback, and reads a number that is not about Retail Bank. Nothing on screen
says so. "What does this division think of this agent" is the question this
whole challenge exists to answer, so a filter that silently does nothing there
is worse than a filter that is missing.

## The pattern already exists

Adoption's approach, which you established in the last round: label nulls with
the shared sentinel at the repository boundary, and have `_org_clause`
translate it back to `IS NULL`. Half of this already exists inside
`get_sentiment_vs_usage`.

Follow that pattern rather than inventing a second one. If any query genuinely
cannot follow it, say which and why before working around it.

## Steps

- Thread the org filters and the date range through all three functions.
- Check the whole tab, not only the three named: list every query backing a
  Feedback panel and say, for each, which filters it now honours. If any panel
  cannot be filtered meaningfully, say so and label it in the UI rather than
  leaving it silently unfiltered.
- Keep the `unknown` bucket reachable here too, exactly as in Adoption.

## Date range — one judgement call

Checkups have more than one timestamp: when raised, when answered. Decide which
one the date range should filter on, state your choice and your reasoning, and
say what a user would expect. Do not pick silently.

## Tests — failing first

Run them against the unfixed code and paste the failures before you fix
anything.

- filtering to one division changes each headline metric, and matches a directly
  computed expected value
- narrowing the date range reduces the counts
- the sums across all filter options reconcile to the unfiltered total
- selecting `unknown` returns exactly the org-less respondents
- a filter combination that should return nothing renders empty rather than
  falling back to unfiltered data — this is the failure mode that looks like
  success

## Also check

The Notify tab: do its three audiences honour the sidebar filters, or does it
have the same gap? You checked Reliability and Feedback last time; Notify was
not checked. Report either way.

## Documents to update

Whatever this makes stale — `ARCHITECTURE.md` (query layer, the filter
contract) and `USAGE-GUIDE.md` (what the filters apply to). Add a `handoff.md`
entry. If `USAGE-GUIDE.md` currently implies the filters apply everywhere, that
line was wrong before this fix and should be called out.

## Report back

1. the failing test output, then the passing one
2. every Feedback panel with the filters it now honours
3. your date-range decision and reasoning
4. the Notify answer
5. files and lines changed, docs changed, docs deliberately left alone
6. anything you found that I did not ask about

Nothing committed. Show me the diffs.
