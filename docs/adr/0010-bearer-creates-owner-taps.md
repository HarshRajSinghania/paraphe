# ADR 0010 — Bearer creates; owner id taps

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing

## Context

v1 is a single-owner inbox, not multi-user SaaS. After cutover, the approved callers must create cards the same way they create
cards today: one MCP key. A tap is a Telegram `callback_query`. Forwarded
or spoofed buttons are a known risk; Telegram still delivers
`CallbackQuery.from`. ADR 0008 already stores the owner Telegram user id
in config.

## Decision

1. **Create:** any caller that presents the single shared Paraphe MCP
   bearer may create a card. That is the approved caller set
after the one-cut flip (ADR 0009). No second human create path. The Telegram
   bot does not mint cards for strangers who message it.
2. **Tap:** accept only when `CallbackQuery.from.id` equals the configured
   owner Telegram user id. Anyone else is ignored (`answerCallbackQuery`
   with a short refuse, no approve). No extra password. No extra chat-id
   allow-list in v1.
3. **Bearer:** one shared secret, in the 0600
   config file or env (ADR 0008). Not one key per caller. Not
   unix-socket-only with no bearer.

## Consequences

A leaked bearer can create cards; it cannot tap them. A leaked Telegram
account can tap; it cannot create via MCP. The spec must check `from.id`
on every callback, including `/config`.
