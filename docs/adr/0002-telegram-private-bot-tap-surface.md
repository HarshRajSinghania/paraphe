# ADR 0002 — Telegram private bot is the tap surface

- **Status:** Accepted (2026-08-25)
- **Supersedes:** the earlier sketch of a Telegram channel as the inbox

## Context

The value is one tap on a phone, not an app of its own. The owner already
lives in Telegram. A channel or group topic with inline buttons was the
first convenience idea; stale Telegram approval buttons are a known
failure in practice. A dedicated private bot chat keeps the tap on one
surface without a public channel or a second app.

## Decision

The tap surface for Paraphe v1 is a dedicated Telegram bot in a private
chat with the owner. That chat collects the decision. It is not a pager
that sends the owner to a web console, the previous inbox, or another app for
the same yes.

## Consequences

Card writing stays ELI15 and short enough for a phone. Button lifetime,
edit-in-place, and cancel/expiry behaviour must be proven before the spec
freezes the Telegram shape. Chat topics stay alerts, not the inbox.
