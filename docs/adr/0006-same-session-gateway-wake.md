# ADR 0006 — Same-session gateway wake, honest miss

- **Status:** Superseded by [ADR 0011](0011-answer-returns-through-the-ask.md) (2026-09-11)
- **Supersedes:** nothing
- **Refines:** ADR 0003 (dual-path wake)

## Context

ADR 0003 already said the store is source of the tap, wake is best-effort,
and poll is the fallback. The pain of the inbox this replaces is that a tap
does not resume the session that asked; Desktop MCP is often blocked, clean-process cards have
no origin, and `deliver=origin` with `origin=null` cannot inject into
the web console. A chat surface must not be treated as a web-console wake.

The owner wants the *same* session to resume and act, without announcing the
tap in chat. Inventing a replacement agent session would execute a tap in the
wrong conversation. Three surfaces (desktop, web console and chat) all hang off
the same gateway.

## Decision

1. A successful wake means the **exact session that sent the card** resumes
   and acts. The owner does not announce the tap in chat.
2. The **mechanism** is one class of gateway session-wake record. The **origin records** are not the
   same. Persist one of:
   - Desktop / WebUI: `source_thread=hermes:session:api_server:<session_id>`
     and destination platform `api_server`. WebUI is a surface, never
     `platform=webui`.
   - Chat (the agent chatting in the chat surface, not the Paraphe tap bot):
     `source_thread=hermes:session:telegram:<session_id>`. Chat topics are not a
     wake.
   - Explicit `origin=none`: poll-only. Valid card. No wake attempted.
3. If that exact session is gone, the wake **fails honestly**. The tap
   stays in SQLite. Agents recover with `get_response` /
   `list_unprocessed`. Do not start a fresh agent session. Do not invent a
   replacement executor unless a later ticket recorded one at send time.
4. A wake file or poll row is not delivery. Delivery is the origin
   session actually continuing. Launcher harnesses after
   cutover use store + poll only; this ADR does not invent a non-gateway
   resume.

## Consequences

Every create must persist a real session id (or explicitly `origin=none`).
`source_thread` stays on the card. Launcher harnesses in the cutover plan
consume the same store + poll path; this ADR does not invent a non-gateway
resume. The spec must not call a Telegram chat topic a wake.
