---
title: paraphe async answer return path - Plan
type: docs
date: 2026-09-11
topic: paraphe-async-return-path
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: owner-directed session design, 2026-09-11
execution: code
---

# paraphe async answer return path - Plan

## Goal Capsule

- **Objective:** A decision raised by an agent returns to the exact agent that asked — on the runtimes in daily use, and on any Model Context Protocol client that can background a command or re-enter at a boundary — without per-runtime integration and without the owner announcing the answer in chat.
- **Means:** Make the reserved wait surface real; ship a waiter command and a shell-side ask; teach the async protocol through the tool text and one shipped skill; withdraw the gateway-wake machinery and describe the store-and-poll fallback honestly.
- **Product authority:** the repository owner (owner-directed design, 2026-09-11).
- **Open blockers:** none. The mechanism, the delivery vehicle, and the naming constraint are settled.
- **Execution profile:** code.
- **Stop conditions:** Stop if the suite is not green; if the private-term scan returns a match; if a step would require per-runtime integration code, a new third-party dependency, or a credential an agent holds being able to answer a card; if the deployed service would be left unable to start.
- **Tail ownership:** the repository owner. Live adoption and the end-to-end proof remain owner-gated.

---

## Product Contract

### Summary

This plan completes the product's founding loop — ask, answer, resume — by making the answer return through the ask itself. An asking call may wait; a background waiter command may hold for the card's lifetime; a tap is answered down the same wire the agent holds; and when no wire is open, the durable store and the poll path remain the ground truth. The earlier design that tried to wake a stopped session is withdrawn: the Model Context Protocol defines no server-initiated turn, no runtime in scope turns a server notification into a new turn, per-runtime integration was rejected as a requirement, and the product must work for any runtime out of the box.

**Product Contract preservation:** changed — the return path. The waited call and the waiter command become the mechanism; the gateway-wake records are superseded explicitly; poll remains the fallback; the credential boundary is untouched (the agent credential still creates and reads, and never answers).

### Problem Frame

An agent that must ask before it acts sends a card and then stops. The owner answers on a phone. What happens next is the whole product: nothing, unless the asking session keeps checking or the owner returns to the chat to say the answer arrived. The earlier attempt answered this with a wake delivered by a separate watcher wired for specific runtimes — it required per-runtime installation, it misfired when the runtime changed, and after a rename it silently matched nothing at all. That approach is withdrawn.

Three observations settle the shape of the correct one:

- The Model Context Protocol defines no server-initiated turn, and a runtime that is not in a call does not read one. There is no portable "wake" to build.
- All the runtimes in scope share one primitive: the tool call, which can wait. When the answer returns through the open call, the asking agent resumes with no integration at all.
- Holding a single call forever is fragile — runtimes expire calls. A waiting process outside the model loop has no such expiry: it can block until the card itself can no longer be answered.

The repository already reserved this surface: the waiting parameter exists on the asking and reading tools, validated and deliberately not slept on, awaiting the first client that needs the wait. This plan is that client.

### Key Decisions

- **The return path is the waited call, the waiter command, and poll.** A call may wait; a background waiter may hold for the card's lifetime; the durable store alone remains sufficient. Governs R1–R6, R10.
- **No per-runtime integration, anywhere.** The skill teaches the protocol as documentation; the tool text carries it to clients that do not read the skill; the waiter is a plain command any runner can background. Governs R7, R8, R13. (session-settled: user-directed — the three daily runtimes work out of the box; every client that can background a command gets the waiter path, and clients that cannot rely on the boundary sweep.)
- **The wait is bounded per call and unbounded per intent.** A single waited call stays under the runtime's own call timeout (the existing 0–60 second window); the waiter command loops internally so a decision can take hours. Governs R1, R4.
- **Silence is never approval; the store remains the source.** A missed wait, a dead waiter, an expired window — all fall back to the same durable read. Governs R2, R10, R11.
- **The previous name and the inherited inbox leave active surfaces.** Caller configuration, helper commands, service units, skills and tracked files carry the product's current name; the inherited third-party inbox is retired from active workflows. Governs R12. (session-settled: user-directed.)

## Requirements

**The waited call**

- R1. A waiting parameter on an asking or a reading call is honored: when the owner answers inside the window, the call returns the answered envelope; when the window ends, it returns the pending envelope. The window stays bounded as documented (0–60 seconds per call).
- R2. An answer wakes the waiting call promptly and cleanly: the notification follows the durable store write, so an answered card and a returned call agree; no waiter outlives its card; a disconnected client leaves no residue; the server serves other traffic while calls wait.
- R3. Waiting changes no other semantics: the card is created and notified whether or not anyone waits; the credential boundary is untouched; expiry and version rules are unchanged.

**The waiter command**

- R4. The distribution ships `paraphe wait <request_id>`: it blocks until the card is answered or can no longer be answered, then prints the answer; it exits with distinct codes for answered, expired or not answerable, and unknown; it loops internally so no single wire exceeds the per-call window. Standard library only.
- R5. The distribution ships a shell-side ask that prints the request id, so a runner without tool bindings completes the whole loop through the command line alone.
- R6. The waiter is backgroundable: any runner that can start a command and notice it exit can be returned by the answer; no runtime-specific code exists on either side.

**The agent protocol**

- R7. The served tool text carries the protocol without any skill installed: record the request id when you ask; drain answered requests that are yours when you next run; the ask result names the reading path.
- R8. One skill file ships in the repository: the async protocol, the per-runtime idiom table (background-and-notify where the runtime has it, boundary sweep everywhere), and the handoff rule. It is documentation only — the only agent-side artifact in the return path.
- R9. The specification, the vocabulary, the tool guide and the decision records describe the return path as it now is; the earlier gateway-wake records are superseded explicitly rather than silently contradicted.

**Fallback and honesty**

- R10. Poll remains sufficient alone: every answer is readable through the reading tools without any waiter; nothing is lost when a waiter is absent, dead, or expired.
- R11. A session ending with an open card records the request id and its continuation, so a later run can act; the protocol states this.

**Delivery**

- R12. No active surface carries the previous product name or the inherited inbox's name: caller configuration, helper commands, service units, skills and tracked files are current-name only, and retired transports are removed or repointed.
- R13. The return path arrives with the product install: a fresh install provides the waiting engine and the commands; the skill is one documented copy step; nothing else is wired per runtime.

## Key Flows

- F1. Gated ask, owner away
  - **Trigger:** an agent reaches a gate it may not pass alone and the owner is not at the machine.
  - **Actors:** the asking agent, the waiter command, the owner.
  - **Steps:** the agent asks and starts `paraphe wait` in the background; it stops work or continues elsewhere; hours later the owner taps; the command exits; the runtime returns the agent with the answer; the agent revalidates, executes once, reports, marks processed.
  - **Outcome:** the exact asking session continues, with no chat announcement.
  - **Covers:** R1, R2, R4, R6, R11.

- F2. Gated ask, owner at the desk
  - **Steps:** the agent asks with a short window; the owner answers within the minute; the answer returns inside the call.
  - **Covers:** R1, R3.

- F3. Runner without tool bindings
  - **Steps:** `paraphe ask` prints the id; `paraphe wait` blocks in the background; the tap exits it; the runner reads the answer.
  - **Covers:** R4, R5, R6.

- F4. Session gone before the tap
  - **Steps:** no waiter exists; the owner taps; the answer rests in the store; the next run drains it per the protocol.
  - **Covers:** R7, R10, R11.

## Acceptance Examples

- AE1. **Covers R1, R3.** Given a card with an open waiting call and a tap inside the window, when the call returns, then it carries the answered envelope, and the card's lifecycle fields equal the fields the same tap writes without any waiter.
- AE2. **Covers R2.** Given a waiting client that is killed mid-window, when the server is exercised afterward, then no waiter remains, later calls succeed, and the card is unchanged.
- AE3. **Covers R1, R4.** Given an answered card, an expired card and an unknown id, when the waiter command runs against each, then it exits with the three distinct codes and prints the answer only for the first.
- AE4. **Covers R7, R10.** Given a client that reads only the served tool text, when it asks, stops, and runs again after the answer, then it drains the answer and acts — with no skill installed and no waiter running.
- AE5. **Covers R10.** Given zero waiters anywhere, when the owner taps, then the full lifecycle still completes through the reading tools.
- AE6. **Covers R4, R13.** Given a fresh checkout and the documented install, when a runner asks through the command line and waits, then the tap returns the answer to that same shell process.

## Success Criteria

- SC1. The owner taps; the exact asking session continues; the owner is not required to announce the answer in chat.
- SC2. The flow is demonstrated from the three agent runtimes in daily use (Hermes, Claude Code, Codex), each through its own native background facility or the documented boundary sweep.
- SC3. A fresh install reaches the loop without modifying any runtime's code.
- SC4. The suite is green and no third-party dependency was added.

## Scope Boundaries

**Deferred for later**

- Waking a session whose process is gone. The protocol defines no server-initiated turn; per-runtime resume interfaces are deliberately not built. The store read and the handoff rule are the answer.
- Any push protocol or upstream runtime change. The call is the only portable seam.
- Additional waiter conveniences (watch-any, subscriptions). The single-request waiter and the boundary sweep cover the flows; add more only when a real flow demands it.

**Out of scope entirely**

- Changing the answer authority or the credential boundary.
- Auto-answer, auto-approve, or executing without the owner's tap.
- Any runtime-specific integration code. If a flow appears to require one, that is a design violation: stop and re-plan.

## Sequencing

1. The wait engine and the commands (R1–R6), proven by the suite.
2. The teaching: tool text, the shipped skill, the specification and decision-record updates (R7–R9, R11).
3. Live adoption and the end-to-end proof (R12–R13, SC1–SC3), together with the naming and legacy-retirement sweeps tracked as companion issues.
