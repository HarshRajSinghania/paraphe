# ADR 0011 — The answer returns through the ask

- **Status:** Accepted (2026-09-11)
- **Supersedes:** ADR 0003 (dual-path wake), ADR 0006 (same-session gateway wake)
- **Refines:** nothing

## Context

The product's founding loop is ask → answer → resume. ADR 0003 and ADR 0006
tried to close it with a wake: a gateway session-wake record written at create,
attempted at tap, delivered by machinery installed for specific runtimes. That
design required per-runtime integration, misfired when a runtime changed, and
after a rename silently matched nothing at all; asking sessions stopped being
woken and the owner had to announce answers in chat.

Three observations settle the replacement:

- The Model Context Protocol defines no server-initiated turn, and a runtime
  that is not in a call does not read one. There is no portable wake to build.
- Every runtime in scope shares one primitive that can wait: the tool call. An
  answer that returns through the open call resumes the asking agent with no
  integration at all.
- Holding one call forever is fragile — runtimes expire calls — but a process
  outside the model loop has no such expiry: it can block until the card itself
  can no longer be answered.

## Decision

1. The return path is the **waited call**, the **waiter command**, and the
   **poll read**. `wait_seconds` (0–60) parks an asking or reading call until
   the owner answers or the window ends; `paraphe wait <request_id>` repeats
   that bounded window until the card is answered or can no longer be answered
   (exit 0 answered, 3 expired or not answerable, 4 unknown); `get_response`
   and `list_unprocessed` read every answer with no waiter at all.
2. **No per-runtime integration exists anywhere.** The served tool text carries
   the protocol to clients that read nothing else; one shipped skill documents
   the per-runtime idioms; the waiter is a plain command any runner can
   background.
3. **Silence is never approval; the store remains the source.** A missed wait,
   a dead waiter, an expired window — all fall back to the same durable read.
   A session ending with an open card records the request id and its
   continuation so a later run can act; no fresh session executes a dead
   origin.
4. The **gateway-wake machinery is withdrawn**: no wake record is written, no
   wake is attempted, and `source_thread` is descriptive metadata only. The
   `WakePort` seam and its adapter are removed with this decision.

## Consequences

- The waiting engine ships with the product install; the skill is one
  documented copy step; nothing else is wired per runtime.
- The waiter must never outlive its card: its window is bounded per call and
  its loop re-reads the durable state.
- Clients that cannot background a command rely on the read at the next
  boundary; that is a first-class path, not a degraded one.
