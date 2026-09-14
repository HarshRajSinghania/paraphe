# Discussions (draft)

Status: **draft. Discussions is off and nothing here is created.** The flip
enables it and posts the welcome, once the repository is public.

## Categories

Enabling Discussions creates Announcements, General, Ideas, Polls, Q&A and Show
and tell. Keep the five below; Polls is the one category this project has no use
for, with no community to poll yet. Descriptions are what to paste.

| Category | Format | Who can post | Description |
|---|---|---|---|
| Announcements | Announcement | maintainers | Releases, roadmap notes, and the occasional post about how the project is going. |
| Q&A | Discussion | everyone | Installing, configuring, wiring a destination — ask here, and mark the answer when you get one. |
| Ideas | Discussion | everyone | Half-formed suggestions. When one turns into a task, it becomes an issue with a triage label. |
| Show and tell | Discussion | everyone | A deployment, a destination, an integration — anything you built on top. |
| General | Discussion | everyone | Everything that is none of the above. |

Two things do not belong in a category, and the welcome says so:

- A bug with a command and an output is a tracker issue, not a discussion
  ([`docs/agents/issue-tracker.md`](../agents/issue-tracker.md)).
- A vulnerability is neither: [`SECURITY.md`](../../SECURITY.md).

## Welcome post

Filed in **Announcements** as the first post, at the flip.

```markdown
# Paraphe is an owner-decision inbox

Paraphe holds one decision at a time. An agent raises a card, it lands on your
phone or on the console of the machine running it, you answer, and the agent
that asked picks the answer up and carries on. Self-hosted, standard library
only, and your data is a single SQLite file in your own data directory.

## The line it does not cross

**The credential an agent holds cannot answer its own card.** It creates and it
reads. Answering needs the owner's credential, on a path the agent's cannot
reach. An inbox an agent can approve on its behalf is not an owner-decision
inbox, so this is not a setting.

## Where to ask

- **A bug, or a concrete request:** the issue tracker. A report is worth ten
  times more with the version you are running, the command you ran, what it
  printed, and what you expected instead. `good first issue` and `help wanted`
  mark what is open to a newcomer; CONTRIBUTING covers the suite and what a
  mergeable change looks like.
- **A question, or an idea:** Q&A and Ideas, here.
- **What you built:** Show and tell.
- **A vulnerability:** neither place — `SECURITY.md`.

Pull requests are welcome, but they are not a request surface: an unlabelled
pull request that changes behaviour without an issue is a conversation, not a
queue item.
```

## Notes for the flip

- The welcome states what the project is, the rule it protects, and where to
  ask. If the README's first screen and this post disagree after the surface
  pass, the README wins — fix the post, not the README.
- The post carries no URL: every reference is a path or a code span, so nothing
  in it 404s at flip time.
