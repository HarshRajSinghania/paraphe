# Seed: ship the owner-side setup path for the phone destination

Status: **draft. Nothing is filed.** The flip files this issue once the
repository is public. Drawn from `docs/roadmap.md`, "A shipped tap transport for
the phone destination".

| | |
|---|---|
| Title | Ship the owner-side setup path for the phone destination |
| Labels | `help wanted`, `ready-for-human` |
| Origin | `docs/roadmap.md`, "Next" |

## Body

```markdown
## What is missing

A reader can install Paraphe in three commands, but pointing it at a phone is
still work done outside the repository. The README's install section says to add
a Telegram bot token and your Telegram user id to `paraphe.toml`; the only
document that explains the wiring is `docs/adapters.md`, which is written for
someone implementing a destination rather than for an owner wiring their own
phone.

Between `pip install .` and the first card on a phone, the reader creates a bot
with Telegram's BotFather, finds their own numeric user id, pastes both into a
config file, and only discovers at the first real card whether the pair was
right. The transport itself is shipped and polls (`src/paraphe/inbox/runtime.py`);
the gap is the owner-side path to it.

## Where

- `README.md` — the install section, where the phone destination is one
  sentence.
- `docs/adapters.md` — the two-method contract, addressed to a contributor
  writing a destination.
- `config.example.toml` — the phone-destination keys.
- `src/paraphe/inbox/config.py` — the phone-destination validation
  (`bot_token`, `owner_telegram_id`) and the owner-only answer path.
- `src/paraphe/inbox/runtime.py` — the polling transport and its API client.

## Acceptance

Choosing the shape is the first deliverable: say in this thread whether this is
a documented walkthrough, a setup command, a check command, or a combination,
and why. Then:

- A reader with the repository and Python reaches a card on their own phone
  without reading `docs/adapters.md`.
- Taps are accepted only from the configured owner identity, and the create
  credential still cannot answer. A change that touches that boundary ships
  with a test that proves the boundary holds.
- No secret is printed, logged, or committed: the bot token stays in the
  owner's configuration file or environment.
- `paraphe --help` and the README name the path.
- The suite stays green: `python3 -m unittest discover -s tests -p 'test_*.py'`.
  A test covers what the change adds.
- Standard library only — no new dependency.

## Notes

The adapter is not the work: it exists and is documented for contributors. The
work is what stands between a reader and their first card on a phone.
```

## Why `ready-for-human`

`ready-for-agent` means fully specified, and this one is not: the shape is a
maintainer call before the code, and the answer path is the product's defining
line. Whoever picks it up owns that call.
