# ADR 0005 — SQLite under /var/lib/paraphe, restic after a consistent snapshot

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing

## Context

The durable store is the source of the tap (ADR 0003). A closed, third-party inbox is the risk this product exists to escape. The
deployment host already has a live daily restic backup to a network target at
03:00 Europe/Paris, and a weekly check. A second database engine or a second copy
job would add a restore path nobody already practices.

A git repository is the wrong store: card state changes on every tap, and
repository writers must not become the inbox.

## Decision

1. Paraphe v1 keeps cards in a SQLite file on the deployment host.
2. Dedicated service user is **`paraphe`**. Live file is
   `/var/lib/paraphe/inbox.sqlite`, mode 0600, owned `paraphe:paraphe`.
3. Before the daily backup service runs, take a consistent snapshot with
   SQLite online backup / `.backup` to `/var/lib/paraphe/inbox.sqlite.bak`, and
   include `/var/lib/paraphe` in the backup service's include list. That path is
   **not** in the list on an existing deployment; adding it is a required
   cutover prerequisite, not optional. Existing restic excludes stay
   (`--exclude-caches`, `*/node_modules/*`, `*/.cache/*`, `*.log`, `*.tmp`).
   Do not exclude `/var/lib/paraphe`. Do not add a second encrypted destination.
4. The repository stays code only. It does not hold live cards, and no git
   writer reads this directory.

## Consequences

Restore is: install the `paraphe` user and unit, restore `/var/lib/paraphe`
from the backup set (prefer `inbox.sqlite.bak` if the live file is dirty),
start.
A vendor disappearing cannot take the history if the backup snapshot
is intact. A deployment must add the include-list line before the proof card.
