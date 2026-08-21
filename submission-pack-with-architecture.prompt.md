---
mode: agent
---

# P.2 — the submission pack: slide content and a demo recording script

Two deliverables for the challenge submission. Both are distillations of what is already
committed — ARCHITECTURE, BUILD-JOURNEY, USAGE-GUIDE, RELEASE-VERIFICATION, handoff and the
README. Nothing invented, nothing contradicting them.

**Derive from the repository.** Every number re-derived this session. Every command run before it
is written down. Every commit hash checked with `cat-file -e` — pre-rewrite hashes exist in old
notes and look plausible.

**The seed is not being changed.** Do not propose it. The Feedback tab is sparse at the
dashboard's default range because checkups are raised 14 days after a user's first event and
seeded users first appear 60-90 days back. That is correct behaviour, and the script handles it by
setting the range — see C.

Two files in `docs/`: `SUBMISSION.md` (A, B, D) and `DEMO-SCRIPT.md` (C).

---

## A — Context, problem, solution

**A.1 Context.** The business and technical situation this sits in. Who has the problem, what they
do today, why it matters now. Two paragraphs.

**A.2 The problem statement, non-technically.** A reader with no engineering background must
finish this and be able to restate the problem in their own words. No jargon, no acronyms without
expansion. If you cannot say it plainly, you have not finished understanding it.

Include one paragraph on the problem **as you found it** versus as it was stated, if they differ.
That paragraph is evidence of understanding in a way a restatement is not.

**A.3 The solution, twice.** Once for a non-technical reader — what it does, in terms of outcomes.
Once for a technical reader — SDK, collector, store, checkup engine, org map, dashboard, what
crosses each boundary. Keep them separate and labelled; do not blend them into one paragraph that
serves neither.

**A.3.1 The architecture diagram.** One diagram carrying both states: what runs today, and the
AWS deployment it is built to become. Mermaid, so it lives in the repository and stays editable.

The two states must be visually distinguishable — solid for what exists and runs today, dashed or
otherwise clearly marked for what is proposed. A viewer must never be able to mistake a planned
box for a built one, and if the distinction is not obvious at a glance the diagram is doing harm
rather than good.

For the AWS side, propose the mapping and argue it in a short paragraph beneath the diagram, one
line per service, grounded in the recorded limits rather than in what is conventional. The store's
single-writer ceiling is the reason the database changes, not a general preference for managed
services. Say what would carry the collector, the store, the dashboard, secrets, and identity, and
say which of today's components move unchanged and which are replaced.

Keep it to one diagram. If it needs a second to stay readable, split by layer rather than by
state — the point is that a reader sees the path from here to there in one picture.

## B — Pre/post, benefits, innovation

**B.1 Pre and post.** A table or a flow — whichever is clearer for this material. What the
before actually was, what the after actually is. Do not caricature the before to flatter the
after; a reader who lives in the before will notice.

**B.2 Quantifiable benefits.** This is the section most likely to be fabricated, so it is the one
to be most careful in.

Separate cleanly:

- **Measured** — things this project actually produced numbers for. Cite what produced each.
- **Estimated** — efforts saved, manual touch-points removed, quality improvement. For each, show
  the assumption and the arithmetic in one line so a reader can disagree with the assumption
  rather than the conclusion.

Label every estimate as an estimate. A defensible small number beats an impressive one that
collapses on the first question.

**B.3 Innovation.** What was actually unusual here, not what sounds impressive. Candidates worth
considering — judge them, do not just list them:

- tests that read the documentation and fail when the docs drift from the code
- the salt being unavailable to the collector, so re-identification is not possible where the data
  lands
- telemetry that makes its own failures visible rather than swallowing them — drops counted,
  the spool that says events are on disk instead of claiming delivery
- the acceptance method itself: a clean machine, the README followed literally, findings recorded
  before fixes

Pick the ones with a real argument. Two well-argued beats five listed.

## D — From POC to production

**D.1 Technical capabilities needed.** Be concrete and grounded in the recorded limits —
ARCHITECTURE §10 and the seven open SDK findings. The store's single-writer ceiling, the shared
bearer token with a self-asserted identity field, no retention or erasure path, the org map being
a periodic extract. What each would need to become production-grade, and roughly what that costs.

**The AWS deployment belongs here**, as the largest single item, and it should read as the same
plan the A.3.1 diagram shows — not a second, differently-shaped proposal. Cover what has to be
true before it can happen: the identity source becoming a real integration rather than a periodic
extract, secrets management once the salt is no longer a local environment variable, network
placement given that the SDK runs inside other teams' processes, and what the retention and
erasure path would have to look like once the data is somewhere it can be subpoenaed.

Sequence it. What is the first deployable slice, what does it prove, and what comes after — a
production plan that arrives all at once is not a plan.

**D.2 Stakeholder participation.** Who has to be involved for this to be real — whoever owns the
identity source, whoever owns platform hosting, whoever owns data retention and privacy sign-off,
the teams whose agents would instrument. What you need from each, specifically.

**D.3 Other support.** Access, environments, approvals, anything else. Name it plainly.

---

## C — The demo recording script

`DEMO-SCRIPT.md`. This is a script to perform, not a document to read out. Assume the reader is
nervous, recording in one take, and will not improvise.

### Before recording

A checklist for the state the machine must be in:

- what must be running and on which ports, with the exact start commands
- **the reseed, as the last command before recording** — `python seed.py --reset --users 80`.
  State plainly that the acceptance probe and the outage demo must not run after it, and what
  appears on three tabs if they do
- the Feedback tab's date range, set before recording starts, and why
- terminal and browser setup: font size, window layout, which tabs open, anything that will be
  unreadable in a recording if left at defaults

### The run

Number every step. For each step give four things, distinctly:

1. **Do** — the exact click, or the exact command, copy-pasteable
2. **Say** — what to say while it happens, written as speech, not as prose to be paraphrased
3. **Why** — the point that step is making, so the presenter can recover if a question interrupts
4. **Wait** — where to pause and for how long, where the screen needs a beat before moving on

Choose the order yourself and argue for it in a short paragraph at the top. Judgement to apply:
lead with what a viewer can immediately understand, and put the strongest evidence where attention
is highest rather than at the end. The reliability sequence — collector down, the honest message,
events on disk, collector back, nothing lost and nothing duplicated — is likely the strongest
material here, because it shows the system behaving well when things go wrong. Decide where it
belongs and say why.

Mark each step **essential** or **cut if short**. A ten-minute recording and a four-minute one
should both be runnable from the same script.

### Recovery

What to do when something does not work on camera. For each likely failure — a port already held,
an empty tab, a slow first Streamlit load — one line on how to recover without stopping the
recording, and one line on what to say while recovering.

### Closing

The repository link, the tag, and one sentence on what a viewer can verify themselves.

---

## Verify

- Every command in DEMO-SCRIPT run in a fresh shell, in the written order, and the result
  reported. A command that does not run as written is a defect in the script.
- The click path walked in the actual dashboard — do not write clicks you have not made.
- Every number traced to what produced it.
- Every hash checked.
- Full suite afterwards if you touch the README.
- A consistency pass against the existing documents; report contradictions rather than resolving
  them silently.

## Report

1. The problem-as-stated versus problem-as-found paragraph, called out separately.
2. Both documents.
3. The command and click check, with results.
4. The B.2 split — what is measured, what is estimated, and the assumption behind each estimate.
5. Any contradiction found.
6. Anything you were asked for that the repository does not support, stated plainly rather than
   filled in.

Stage explicitly. Show me the diff. Commit nothing until I have read it. No push, no remote.
