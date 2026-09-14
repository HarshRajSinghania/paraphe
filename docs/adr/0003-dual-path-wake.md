# ADR 0003 — Dual-path wake

- **Status:** Superseded by [ADR 0011](0011-answer-returns-through-the-ask.md) (2026-09-11)
- **Supersedes:** nothing

## Context

The worst pain of the inbox this replaces is that a tap does not wake the
session that asked.
Official recovery is poll (`get_response` / `list_unprocessed`). A desktop
MCP client is often blocked, so real sends go through a clean-process helper.
Wake-only would lose answers when the origin session is gone. Store-only
would keep the "the owner tapped and nothing happened" failure.

## Decision

The durable store is the source of the tap. Paraphe also attempts a
best-effort wake of the asking session or job. Agents still recover by
polling. Silence is never approval.

A card stores the **normalized** origin, and stores none when the caller sent
none (`origin=none`) or when no wake port is configured at all. Two null wake
implementations once disagreed here — one kept the caller's raw string — and
the disagreement was visible in stored data. The normalized value is the
intended behaviour: the stored origin exists so it can be woken, and a
deployment with no gateway has nothing to wake. `tests/inbox/test_surface_contract.py`
pins it.

## Consequences

Every send must record enough origin to attempt a wake and to close out
(`report_execution`, `mark_processed`) even if the wake fails. The spec
must define desktop, web console and chat origins separately.
