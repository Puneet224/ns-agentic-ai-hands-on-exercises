mode - agent

# Phase 9 — Identity and org resolution

This is the last build phase before freeze. Its purpose is to turn a claim into
a fact: that aiOps works for many ACF2 IDs, across single-agent and multi-agent
environments.

**Run this in two sessions.** Stop at the marked point and report. Do not carry
on into Session 2 in the same turn.

Commit nothing. Show diffs.

---

# SESSION 1 — Org resolution moves to the collector

## Why

Today the caller supplies ACF2 ID, Business Group and Division. In a real bank
the adopting team does not know or maintain BG and Division — those come from a
directory. Asking every agent developer to hardcode them means the data is wrong
the day someone changes team, and it means the README's headline snippet has to
carry three arguments instead of one.

Moving resolution to the collector makes the adopter's job one line. That is the
whole adoption argument for this challenge.

## 9.1 — The mapping store

- Add an `org_map` table: ACF2 ID -> business_group, division, plus a
  `source` and `loaded_at` column so a stale map is visible rather than silent.
- Add a CLI command to load it from CSV. Seed data already contains a usable
  mapping — derive the CSV from it rather than inventing new names, so the demo
  stays coherent.
- The CSV format goes in the docs. A judge asking "how does this get populated
  in production?" should get a straight answer: an AD or HR extract on a
  schedule, and here is the shape it must have.

## 9.2 — Resolution and precedence

Wire resolution into `_upsert_user` (`repository.py:128-157`).

**Precedence is a decision, not a detail.** My recommendation: the map is
authoritative, and a caller-supplied value is used only when the ACF2 ID is
absent from the map. Reason: centralising is pointless if a stale hardcoded
string in someone's agent can override the directory.

The existing merge rule at `repository.py:151-155` — a later `identify()` fills
nulls but a null never overwrites — was written for the caller-supplied world.
Say plainly how it must change under map-authoritative precedence, and what
happens when a user moves division after being enriched once.

Do not just implement my recommendation. If the code makes the other precedence
obviously better, argue for it and wait.

Unmapped IDs keep falling into the `unknown` bucket. That behaviour stays.

## 9.3 — Three identity modes, documented

The SDK supports more ways to establish identity than the docs admit. Write the
section that names all three and says when each applies:

- **Multi-user service** — per-request `identify()` from the auth context
  (SSO token, JWT claim, request header). The agent developer extracts it.
- **Single-user desktop agent** — `fallback_to_os_user`
  (`client.py:196-202`), which exists but is off by default and undocumented.
  Test whether the OS username actually resolves usefully here, and say so.
- **Environment variable** — check whether one already exists. If not, say
  whether adding `AIOPS_ACF2_ID` is worth it or is a third way to do the same
  thing badly.

Explicitly warn against the trap: putting a single ACF2 ID in static config for
a multi-user service, which silently attributes every event to one person.

## 9.4 — README and docs

With the collector resolving org attributes, the install snippet goes back to
one identifying argument. Update it, and update `USAGE-GUIDE.md` Case 1, which
currently teaches passing all three.

Prove the new snippet the same way as last time: copy it verbatim into a scratch
directory, run it against a running collector, and show the resulting user row
with BG and Division populated from the map — not from the call.

### STOP HERE. Report Session 1 before starting Session 2.

Report: the precedence decision and its consequences, the failing-then-passing
tests, the new snippet with its proof, and every doc you changed.

---

# SESSION 2 — Proving multi-user and multi-agent

## Why

Everything above assumes identity stays attached to the right request. That has
never been tested. Until it is, "works for multiple users" is a claim.

## 9.5 — Concurrency isolation

This is the most important work in Phase 9.

- Fire N concurrent async calls with different ACF2 IDs through the SDK, and
  assert every event landed against the right one. Make N large enough that
  interleaving actually happens.
- **Then test threads separately.** `ContextVar` does not propagate into a new
  thread the way it does into a task. An agent using `threading.Thread` or a
  thread pool may lose identity entirely, or inherit the wrong one. Nobody has
  checked this. If it breaks, that is the single most valuable finding in this
  phase — report it before fixing it, and tell me the blast radius.
- Cover the sync client path too if there is one, not only async.

Write these tests so they fail against the current code if the behaviour is
broken. Do not write a test that passes because it never exercised the race.

## 9.6 — Multi-agent rollup

One ACF2 ID, three agents. The data model already carries `agent_name` per
event, so this should be a query and a view, not a schema change. If it turns
out to need a schema change, stop and tell me before making one.

Show the per-user agent breakdown somewhere a judge can click to.

## 9.7 — Known limits

Add a "Known limits — production hardening" section to `ARCHITECTURE.md`:
SQLite concurrency ceiling, auth model, no retention policy, the org map being
a periodic extract rather than live directory reads.

Write them as understood trade-offs with the conditions that would force each
change. A stated limitation reads as engineering judgement; an unstated one
reads as an oversight when a judge finds it.

## Documents to update

Across both sessions: `README.md`, `sdk/docs/USAGE-GUIDE.md`,
`sdk/docs/ARCHITECTURE.md`, `sdk/docs/BUILD-JOURNEY.md`, and a `handoff.md`
entry per session. Update `RELEASE-VERIFICATION.md` if any command it lists
changes.

Do not touch the committed wheel in `sdk/dist/`. If SDK source changes in this
phase, say so and recommend the version bump — do not perform it.

## Report back for Session 2

1. concurrency results — async and threads, separately, with the failing output
   where behaviour was broken
2. what the thread finding means for a real integrating agent
3. the multi-agent view, and whether it needed anything beyond a query
4. docs changed
5. anything you found that I did not ask about

Nothing committed. Show me the diffs.
