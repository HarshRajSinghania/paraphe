# Issue tracker

Issues live in **this repository's own issue tracker**. Pull requests are
welcome but are not a request surface: an unlabelled pull request that changes
behaviour without an issue is a conversation, not a queue item.

## Labels

The five triage roles and their exact strings are in
[`triage-labels.md`](triage-labels.md): `needs-triage`, `needs-info`,
`ready-for-agent`, `ready-for-human`, `wontfix`.

## Workflow

1. **Open** an issue with what you expected, what happened, and how to
   reproduce it. A bug report that names the version and the exact command is
   worth ten that do not.
2. **Triage.** A maintainer applies exactly one triage label.
   - `needs-info` — waiting on you; the issue has no owner until you reply.
   - `ready-for-agent` — fully specified. Someone can act on it without asking.
   - `ready-for-human` — needs judgement or access a machine does not have.
   - `wontfix` — deliberately not actioned. The reason is in the thread.
3. **Work.** A change lands with the suite green and the behaviour it claims
   covered by a test. Reference the issue in the commit or the pull request.
4. **Close.** The issue closes when the change is merged. A closed issue whose
   fix is not in the default branch is a reopened issue.

## What an issue should carry

- The command you ran and what it printed.
- What you expected instead.
- Your Python version and operating system.
- For a behaviour change: which contract in `docs/tools.md` or
  `docs/adapters.md` it touches.

## Security

A vulnerability does not go in the tracker. See [`SECURITY.md`](../../SECURITY.md).
