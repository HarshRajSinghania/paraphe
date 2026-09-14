# ADR 0008 — File config plus owner-only /config

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing

## Context

The throwaway prototype read the bot token and owner id from 0600 files
under `/var/tmp` and hardcoded a 45-second TTL. That expired while the
owner opened the notification. Setup must be changeable without editing code:
owner Telegram id, bot token, default card life, and floor life. A Telegram
`/config` command keeps later tweaks out of a shell.

Putting the token in a Telegram message would copy a secret into chat
history. `/config` cannot be the only setup path, and it cannot echo
secrets.

## Decision

1. v1 reads setup from a **config file** (`config.yml` or equivalent)
   plus **environment variables**. Env wins over the file for the same
   key. Required at start: bot token, owner Telegram user id, default
   TTL, floor TTL. Missing required values fail closed; do not start.
2. Defaults in the file match ADR 0007: default life 4 hours, floor 15
   minutes. A value below the floor is rejected.
3. Secrets (bot token) live in the file with mode 0600, or in the
   environment. They are never committed, never written to Linear or
   git, never printed in logs, and never shown back in Telegram.
4. After first start, the owner may use an **owner-only** Telegram
   `/config` command to read and change non-secret settings (default
   TTL, floor TTL, and later similar knobs). `/config` that is not from
   the configured owner id is ignored.
5. `/config` may rotate the token only by accepting a new value; it
   never displays the current token. First-run still needs the file or
   env, because the bot cannot receive `/config` before it has a token.

## Consequences

The spec must list the exact keys and the env-over-file rule. Setup is
edit the file (or env), start the service, then optional `/config`.
The owner-identity check still decides who may tap; this ADR only decides how
settings are loaded and who may change them in Telegram.
