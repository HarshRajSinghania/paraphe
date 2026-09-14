---
type: operations
title: Data location, permissions and backup
description: Where Paraphe keeps its cards, how one function resolves that location, why relocating refuses rather than starting empty, the modes on the directory and the file, the snapshot contract before a backup, and the container mount.
tags: [operations, persistence, permissions, backup]
verified:
  - by: openwiki/0.5.0
    at: 2026-09-10T10:36:31.915Z
sources:
  - id: openwiki-source-bb1ebe868e35e9e500714501
    resource: repo://Dockerfile
  - id: openwiki-source-15b9545d25b6d5dec781e086
    resource: repo://docs/adr/0005-sqlite-restic.md
  - id: openwiki-source-872ba00e35eb81073c2713f0
    resource: repo://src/paraphe/inbox/config.py
  - id: openwiki-source-d39aa17b1580d696b9e0586e
    resource: repo://src/paraphe/inbox/store.py
generated: { by: "hermes", at: "2026-09-10T10:36:31.915Z" }
---

# Data location, permissions and backup

## One resolver, used everywhere

`resolve_store_path` is the only place a data location is decided, and it is
called by the validator, the composition root and the tests. That is the point:
the path that is **checked** is the path that is **opened**, so a misconfigured
deployment fails at startup rather than at the first card.

| Input | Result |
|---|---|
| an explicit location (config key or `PARAPHE_STORE_PATH`) | honoured, always |
| nothing configured | the platform's per-user data directory |

The per-user default is `$XDG_DATA_HOME/paraphe`, falling back to
`~/.local/share/paraphe`, with the store file `inbox.sqlite` inside it.

## Why relocation refuses

Earlier releases kept the store at a fixed system path. If a run resolves the
**default** and that location holds no store while a store exists at the
retained location, Paraphe refuses with one line naming both paths, and creates
nothing:

```
no store at <default>; a store exists at <retained>. Set store_path to
<retained> to keep using it, or start from an empty location.
```

Two deliberate details:

- **An explicit location is honoured**, even while a store exists elsewhere.
  Naming a location is a decision; drifting to a default is not. This is what
  lets an existing deployment keep its data by configuring `store_path` to the
  retained path, which is what the README's upgrade note tells it to do.
- **An unreadable path counts as no store.** The check uses a helper that treats
  a permission error as "nothing to strand" rather than propagating it, because
  a process that cannot read a directory cannot have been keeping its cards
  there.

The consequence is a product guarantee, not just an error message: a change of
data location never silently begins a second, empty inbox while the real cards
sit somewhere else.

## Modes

`Store.prepare` creates the data directory if it does not exist, sets it to
`0700`, then touches the store file and sets it to `0600`. The chmod is explicit
rather than left to `mkdir`'s mode, because a umask would otherwise decide how
private the owner's data is.

A failure at that point — an unwritable directory, a read-only filesystem —
arrives as the product's single-line setup error, not as a later `OSError` from
somewhere inside a request handler.

## What is in the file

| Table | Contents |
|---|---|
| `cards` | one row per card, keyed by request id, the card serialised as JSON |
| `notifications` | the external ids already notified, so a retry does not notify twice |
| `durable_state` | small key/value state that must survive a restart, today the Telegram long-poll offset |

The inbox loads every card into memory on first use and fails closed if a stored
payload does not parse. Cards are small and few by nature — this is an inbox,
not a log — so the whole set in memory is the honest implementation rather than
a cache with a policy.

## Backup

The decision record fixes the contract: a SQLite file under a dedicated service
user, and a **consistent snapshot taken before the daily backup service reads
its include list**, rather than copying a live database.

The contract lives in this repository; the helper that performs it does not. The
snapshot script is part of the deployment's own host configuration, alongside
the unit and the include list, because it is about one host's backup system
rather than about the product. What matters to the product is the shape:
snapshot first, then back up the directory, and never back up a half-written
file.

Restoring is: install the service user and the unit, restore the data directory
(preferring the snapshot when the live file is dirty), and start.

## The container

The image keeps the data location outside itself: `/data` is declared as a
volume and `PARAPHE_STORE_PATH` points inside it. The container runs as an
unprivileged user, so the mounted directory has to be writable by that user —
which is why the README's container block starts by creating it with permissive
mode.

The container binds loopback inside itself. Reaching it from outside the
container means either configuring the phone destination and setting
`PARAPHE_MCP_HOST`, or putting a proxy in front — never both the answer path and
a world-reachable bind, because startup refuses that combination.
