# ADR 0007 — Edit buttons off; default card life is hours

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing
- **Proven by:** a throwaway prototype on a scratch branch, with live taps on
  2026-08-25.

## Context

Telegram does not expire inline buttons (ADR 0002 research). A
45-second demo card expired while the owner was still opening the
notification; the late tap was correctly refused, but that TTL is too
short for real use. Owners read notifications late. After an on-time tap,
the prototype edited the message and stripped the keyboard, so there was
no leftover button to press. That rewrite felt right.

## Decision

1. Paraphe owns card liveness. A Telegram callback is a claim, not a
   decision. Late, cancelled, expired, or already-tapped claims refuse
   with `answerCallbackQuery` and do not approve. `callback_data` is
   opaque and ≤64 bytes. It MUST bind `card_id` **and** the current
   card `version` (or an equivalent revision nonce). After
   `update_request` bumps `version`, a leftover button carrying the old
   version is stale and must refuse even if the action string matches.
   Card id + action alone is not enough.
2. On tap, cancel, or expiry, edit the bot message in place and **remove
   the inline keyboard**. Visual cleanup is UX, not the safety gate. If
   a stale client still sends a callback, refuse it.
3. Default `expires_in_seconds` is **4 hours** (14400). The floor for any
   card is **15 minutes**. Agents may set a longer expiry (up to the
   recorded maximum). A 45-second demo TTL is not a
   product default.
4. Do not keep dead buttons visible so a second press can show a toast.
   Strip them.

## Consequences

The spec freezes this Telegram card shape. The throwaway bot is not
production. The demo bot can be deleted in BotFather after the demo. Callers
must send an expiry ≥ 15 minutes.
