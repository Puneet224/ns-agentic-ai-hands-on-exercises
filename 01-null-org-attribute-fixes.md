mode - agent

# Null org attributes — three bugs found by clicking through the dashboard

Show diffs, commit nothing.

I went through the running dashboard by hand. These are all the same family:
what happens to users and teams that have no Business Group or Division.

**Read section 1 before touching any code.** It changes how much you should
trust the rest of the suite.

---

## 1 — A test claims this is already handled. The UI says otherwise.

You previously told me that missing org attributes render as
`unassigned / unassigned` in the Notify view, pinned by
`test_missing_org_attributes_never_render_as_none`.

The running app does not do that. In Notify -> "Teams with no adoption of this
agent", the table shows `None / None`, and the generated draft message reads:

```
Subject: claims-bot is available to Group Functions, nan
Teams (2, 2 people): nan / nan; Group Functions / Finance Ops
```

That draft is what a human copies and sends.

So the test passes while the behaviour is broken. **Before fixing anything, work
out why**, and tell me:

- what exactly that test exercises — which function, called with what
- why the path it covers is not the path `notify.py` uses to build the table and
  the draft
- whether it ever could have caught this

Then the real question, and answer it honestly: **are there other tests in the
328 with the same shape** — passing against a helper the application does not
actually call on that path? Do not audit all 328. Check the ones covering
rendering and formatting, and tell me what you find. If the answer is "I found
more", that matters more to me than today's fixes.

## 2 — `nan` and `None` reaching the user

Fix the rendering so no null org attribute ever reaches a table cell or a draft
message as `None`, `nan`, or an empty string. One token, used everywhere.

Note that `None` and `nan` are appearing in the *same* view — the table shows
one, the draft shows the other, which suggests two separate conversions (likely
a pandas round-trip in one of them). Find both.

Then rewrite the failing test so it exercises the path the app really uses, and
show it failing against the current code before you fix it.

## 3 — The Division filter cannot reach the bucket the chart shows

`repository.py:860` `list_org_values()` filters nulls out, so the Division and
Business Group dropdowns never offer `unknown` — while `_org_chart` at
`app.py:287` renders that bar. Selecting any named division silently excludes
those users and the counts stop reconciling.

- Make both dropdowns offer `unknown` when null rows exist, and make selecting
  it filter to exactly those rows.
- Reuse the sentinel already at `repository.py:675` so the chart label and the
  filter value are the same token — and the same token as section 2. If they
  cannot all be one token, say why.

Test, failing first:

- seed one org-less user
- assert `unknown` is offered
- assert selecting it returns exactly that user
- assert the sum across all dropdown options equals the unfiltered total

## 4 — CRITICAL on 15 calls

The insight banner shows:

```
CRITICAL — meeting-notes is succeeding only 80% of the time. 3 failures in 15 calls.
```

next to `claims-bot` at 170 failures in 1510 calls. Both get the same CRITICAL
treatment. A success rate computed over 15 calls is noise, and a judge will say
so.

Add a minimum-volume threshold before an insight can be raised, or degrade the
severity below it. Recommend the number and the reasoning — do not pick one
silently. Say what the banner should show instead for a low-volume agent:
nothing, or a differently-worded note.

## 5 — Test data in the demo store

`AB12345` — the user created by the README snippet verification — is sitting in
the live store and now appears in Notify as a team with no adoption.

Tell me the cleanest way to get the demo store to a presentable state, and
whether the seed/reset path already covers it. Do not delete anything yet.

---

## Also check

Does the null/filter asymmetry exist in the Feedback and Reliability tabs too?
For each, say whether the filter and the chart agree, and name the file and line
you checked. If one tab already handles it correctly, say which pattern it uses
— that is the pattern the others should follow.

## Documents to update

Whatever these changes make stale — check `ARCHITECTURE.md` (query layer),
`USAGE-GUIDE.md` (dashboard filters), and add a `handoff.md` entry.

If a doc is already accurate, say so rather than editing it to look busy.

## Report back

1. **why the existing test passed while the UI was broken**, and whether other
   tests share that shape
2. the failing test output for each fix, then the passing one
3. every file and line changed
4. your threshold recommendation for section 4, with reasoning
5. the other-tabs answer
6. docs changed, docs deliberately left alone

Nothing committed. Show me the diffs.
