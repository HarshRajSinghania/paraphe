# Repository metadata (drafts)

Status: **drafts only. Nothing here is applied.** Applying repository metadata
while the repository is private leaks it anyway — topic names are public even on
a private repository — so this is the flip-day checklist, not a change.

Refreshed 2026-09-14: the description and the release path below are the values
to apply at the flip.

## Description (one line, 350 char ceiling)

```
The owner-decision inbox for agents. An agent asks, you answer from your phone or the console, and the same agent resumes. Zero dependencies, self-hosted, SQLite, MCP.
```

## Homepage

Leave empty until there is a documentation page. A repository URL pointing at
itself reads as an accident.

## Topics

Fifteen is the ceiling and more than four reads as noise. Proposed, in order:

```
agents
human-in-the-loop
approvals
mcp
self-hosted
telegram
python
sqlite
```

## Social preview image

1200×630. Two panels, one idea:

- **Left:** `ask_question(...)` → a phone showing a card with two buttons →
  `responded_via: telegram`. Caption: *the agent asked*.
- **Right, behind a struck-through arrow:** a credential labelled
  `create bearer` pointing at the answer endpoint, with
  `401 · cannot answer`. Caption: *the credential it holds cannot answer*.

Wordmark: `paraphe`, lower case, in the repository's own font. No screenshots of
someone else's product, no stock photography, no gradients.

Owner: Clara builds the image from this spec (launch decision D4). It is
applied at the flip if ready, and deferred without blocking otherwise.

## Release

Tag `v0.1.0` from `main` at the flip, with the README's quick start as the
body. The release event triggers
[`publish.yml`](../../.github/workflows/publish.yml), which builds the wheel
and the sdist and publishes them to PyPI with trusted publishing — OIDC, no
token, no GitHub environment declared. The pending publisher is linked first;
its steps are in [`pypi-runbook.md`](pypi-runbook.md). `pip install paraphe`
is the documented one-line path; the venv route stays for checkouts.

## Order at the flip

1. Visibility.
2. Description, topics, social preview.
3. Tag and release.
4. Post — primary channel first, then the two that link to it.

Each step is its own owner decision. This file records the plan, not the doing.
