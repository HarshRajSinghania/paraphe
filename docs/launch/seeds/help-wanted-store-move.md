# Seed: move an existing store to a new location

Status: **draft. Nothing is filed.** The flip files this issue once the
repository is public. Drawn from `docs/roadmap.md`, "An upgrade path that moves
an existing store".

| | |
|---|---|
| Title | Move an existing store instead of only refusing |
| Labels | `help wanted`, `ready-for-agent` |
| Origin | `docs/roadmap.md`, "Next" |

## Body

```markdown
## What is missing

Paraphe can refuse a second store; it cannot move the first one. When the
default data location holds no store and a store exists at the location earlier
releases used (`/var/lib/paraphe/inbox.sqlite`), startup refuses and names the
two ways out: point `store_path` at the old location, or start from an empty
one. The refusal is deliberate and it is the right default — an upgrade must
never quietly open a second, empty inbox.

What is missing is the upgrade path itself. Today an existing deployment is
pinned to the location it was born in, because the only other option is a
manual copy that nothing checks.

## Where

- `src/paraphe/inbox/config.py` — `resolve_store_path`, the refusal and its
  message.
- `src/paraphe/inbox/store.py` — `LEGACY_STORE_PATH`, `default_store_path`,
  `Store.prepare`, and the `0700` directory / `0600` file modes a store must
  keep.
- `README.md` — the section on where your data lives, which documents the
  refusal and the `store_path` workaround today.
- `tests/inbox/test_setup.py` — the two behaviours to keep: relocation away
  from a store that still exists refuses, and an explicit location is honoured
  while a store exists elsewhere.

## Acceptance

- Given a store at the earlier location and no explicit `store_path`, WHEN the
  owner follows the documented move, THEN the store is at the new location, a
  card that existed before the move is readable after it, the file is `0600`
  inside a `0700` directory, and startup no longer refuses.
- The move refuses rather than overwrite when a store already exists at the
  target, and it never leaves a partial store behind: either the whole store
  arrives, or nothing anywhere changed.
- Relocating away from a store that still exists elsewhere still refuses.
- The suite stays green: `python3 -m unittest discover -s tests -p 'test_*.py'`.
  A test fails without the change.
- Standard library only — no new dependency.

## Notes

State in this thread whether the operation copies or moves, and which of the two
is the default; the safer one is the default and the other is the flag. Cards
are the only thing in the store, so nothing else needs migrating.
```

## Why this is a good issue to take

The refusal, its message, the modes, and the two tests to keep are all in the
repository; the change is the operation between them. Nothing about the card
lifecycle or the credential boundary moves.
