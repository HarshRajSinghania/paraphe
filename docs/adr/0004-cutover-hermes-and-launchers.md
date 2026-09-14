# ADR 0004 — Cutover covers one always-on agent plus three launchers

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing

## Context

the previous inbox is wired into the always-on agent and into three launcher
harnesses. Unattended batch callers and crons also call it, but they are a
different caller class with their own origin-guard failures.

## Decision

The v1 spec includes a cutover plan for the always-on agent plus the three
launcher harnesses. Unattended batch and cron callers are out of v1. The
previous inbox stays live until one real Paraphe card
completes detected → delivered → executed → reported → marked processed.
One decision is never collected on both inboxes.

## Consequences

The spec must sequence, for **each** approved caller:
(1) add Paraphe bearer + endpoint next to the previous inbox without sending cards,
(2) prove `tools/list` on Paraphe, (3) after the single proof card,
switch that harness's endpoint and behaviour-block so it cannot call
the previous inbox. The switches happen in one owner-approved window (ADR
0009), not as four independent production cuts. Unattended batch callers keep using the previous inbox until a later map.
