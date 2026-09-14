---
title: paraphe card context and reply - Plan
type: docs
date: 2026-09-11
topic: paraphe-card-context-and-reply
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: owner-directed session design, 2026-09-11 (four decisions settled with the owner)
execution: code
---

# paraphe card context and reply - Plan

## Goal Capsule

- **Objective:** Every card the owner reads on the phone says who is asking, from where, and about what; renders as an ordered rich-text decision instead of a prose blob; and accepts a long-press reply as the owner's own words — an answer or a question — with that text returning to the exact asking session through the shipped return path.
- **Means:** Render the card's structured fields as Telegram HTML sections in a fixed order with a deterministic budget; carry runtime/repo/worktree/ticket as optional taught fields; record an owner reply as the card's text answer on the existing claim → waiter wake → boundary read path; teach agents that a question is a question, not a decision.
- **Product authority:** the repository owner. Four decisions owner-answered 2026-09-11: the card shape was adopted; provenance is supplied and never guessed; a reply decides the card; the work files as one epic plus four children.
- **Open blockers:** none. The card contract is settled, and the return path it rides is shipped (decision record 0011).
- **Execution profile:** code.
- **Stop conditions:** stop if the suite is not green; if the private-term scan returns a match; if a change would let the agent credential answer a card; if the renderer could fail a send on oversized or hostile field text (it must escape and trim, never raise); if a new third-party dependency is required.
- **Tail ownership:** the repository owner. Live adoption and the end-to-end reply proof are the adoption child's boundary.

---

## Product Contract

### Summary

The card is the entire product surface the owner sees. Today the Telegram card is one plain-text blob: the choices exist only as tappable buttons, nothing says who asks or from where, and a reply typed into Telegram is silently dropped. This plan makes the card legible — ordered sections, rich text, the identity of the ask — and answerable in the owner's own words: a long-press reply becomes the card's text answer.

It builds directly on the shipped return path: the reply is recorded as an owner answer exactly like a tap, so a waiting call wakes and the boundary read returns it, with no new transport and no per-runtime code. The credential boundary is untouched: reply intake is an owner-side surface validated like a tap claim; the agent credential still creates and reads and can never answer.

**Product Contract preservation:** changed — the card surface (rendering, provenance, reply intake). The return path (waited call, waiter command, poll) is preserved and ridden, not modified. The answer authority is preserved: taps — and now owner replies, both owner-side — answer; nothing else can.

### Problem Frame

The owner decides on a phone, often away from a desk. A card that cannot be read at a glance and cannot take a nuanced answer forces him back to chat — the exact failure the return path removed. Observed state (verified 2026-09-11, tree at `aedd558`):

- `src/paraphe/adapters/telegram.py` `notify()` flattens a subset of the card fields into a plain string (title, message/details, "Recommended:", consequence); `choices` appear only as inline-keyboard buttons (`_markup`); no `parse_mode` is sent; there is no formatting hierarchy.
- The ask surface (`src/paraphe/inbox/__init__.py`, the tool schemas) has no runtime/repo/worktree/ticket fields; `agent_name`, `project`, `external_id` and `source_thread` exist but none of them render.
- `handle_update()` handles `callback_query` and owner private text (only `/config`); a message whose `reply_to_message` targets a card message is ignored entirely.
- The card model (`src/paraphe/inbox/card.py`) already carries `response_text` and `responded_via`; the owner-tap record path already stores text with `choice=None`; the Telegram claim intake does not accept text yet; waiters wake on any card that leaves `open` (`_notify_waiters`, the park loop).
- The return path shipped the same day: waiting parameters, the `paraphe wait` / `paraphe ask` commands, boundary reads. The reply feature needs no new transport.

Four observations settle the shape:

- Telegram messages support rich HTML formatting natively, and inline replies (`reply_to_message`) are a native client gesture that resolves to the card message — no new UI to build.
- The card fields are already structured; the renderer, not the asking agent, should own the layout — today agents hand-write option lists into prose, duplicating the buttons or replacing them.
- Provenance exists only on the asking side, and the surface is stateless, so the values must travel with the ask. Guessing them (client sniffing) was considered and rejected: wrong context is worse than absent context.
- A reply that decides the card reuses the entire shipped lifecycle — claim, durable write, waiter wake, boundary read. The reply is an owner answer, nothing more.

### Key Decisions

- **The renderer owns the layout; the card never flattens.** Fixed section order, bold labels, rich text, full escaping, deterministic trim with a visible marker. Governs R1–R6. (session-settled: owner adopted the shape, 2026-09-11.)
- **Provenance travels with the ask — taught, optional, never guessed.** Four bounded optional fields on the asking tools; the card renders what is present; the tool text and the shipped skill teach callers; adoption updates the three daily runtimes. Governs R2, R7–R9. (session-settled: owner chose supplied-and-taught over sniffing and over required.)
- **A reply is an owner answer, not a message.** The text is recorded verbatim as the card's answer (no choice index), the card leaves `open` exactly as a same-moment tap closes it, waiters wake, the boundary read returns it. A question-like reply is agent protocol, not a special case: do not execute; explain; re-ask. Reviving the same card was deferred. Governs R10–R13. (session-settled: owner chose reply-decides over reply-is-merged and reply-never-decides.)
- **No new authority, no new transport, no new dependency.** Reply intake is owner-side like the tap; delivery is the shipped return path; standard library only. Governs R13, R14.

## Requirements

**The rendered card**

- R1. The Telegram card renders from its structured fields in a fixed order: identity line → kind line (risk word shown when high or critical) → title → context → numbered options with notes → Recommended → If approved → Limits → links → reply hint → expiry. Title and section labels render bold; the hierarchy is visible at a glance.
- R2. The identity line carries the asking agent, runtime, repository, worktree, and ticket in that order; absent fields are omitted gracefully — the line shrinks, nothing is invented — and a canonical checkout renders without a worktree part.
- R3. Choices render as a numbered list in the message text, each with its one-line note when the caller provided one; the same choices remain the inline keyboard; the recommended option is marked in the text.
- R4. Rendering is total and safe: all interpolated text is HTML-escaped; a deterministic budget trims long content with a visible marker before the platform's hard limit; no field content can inject markup or fail the send.
- R5. Status messages (`notify_user`) get the identity line and rich rendering, carry no options, and a reply to a status message is not an answer.
- R6. Every decision card ends with the reply hint line: a long-press reply answers in the owner's own words or asks a question.

**The provenance fields**

- R7. The asking tools (`ask_question`, `request_approval`, `request_feedback`) and `update_request` accept four optional fields — `runtime` (≤40), `repo` (≤120), `worktree` (≤120), `ticket` (≤200) — stored on the card and rendered per R2. Older clients that omit them keep working.
- R8. The served tool text, the shipped skill, and the tool guide teach the fields; the adoption child updates the three daily runtimes' callers to pass them.
- R9. A `ticket` value that is a URL renders as a tappable link; the existing `links` field renders as a links line.

**The reply**

- R10. A private-chat message from the owner that replies to a card message is accepted as the owner's answer to that card: the text is recorded verbatim as the response text (no choice index; the response channel marks the reply), the card leaves `open` exactly as a same-moment tap would close it — identical lifecycle fields except the absent choice — the keyboard strips, parked waiters wake, and the reading path (`get_response`, `list_unprocessed`, the waiter command) returns it. Resolution by replied-to message id survives a process restart.
- R11. Reply validation follows the tap rules exactly (private chat, owner id, live card binding); an unknown or closed card records nothing, raises nothing, and wakes nothing. The reply text arrives bounded by the platform (within the message limit).
- R12. The answer envelope distinguishes the reply channel, and the protocol teaches interpretation: an owner answer that is a question or non-decision is not executed — the agent explains and re-asks with a fresh card.
- R13. No new authority: reply intake is an owner-side surface validated like a tap claim; the agent credential still cannot answer; no new transport; the return path is ridden unchanged.

**Delivery**

- R14. The specification, the tool guide, the adapters doc, and the served `how_to_use` text describe the card as it now is; the suite stays green; the private-term scan stays clean; standard library only.

## Key Flows

- F1. Owner at a glance. A card arrives; the identity line names agent, runtime, repository, worktree, ticket; the bold title and numbered options make the decision readable without opening anything else. Covers R1–R6.
- F2. Owner answers in his own words. Long-press → reply → "Push only the docs folder, not wip.txt". The card closes with that text; a parked waiter wakes holding it; the asking session revalidates and acts. Covers R10, R13.
- F3. Owner asks a question. Long-press → reply → "What does Park move exactly?" The asking session receives the text and, per protocol, does not execute: it explains and re-asks with a fresh card; the owner then answers. Covers R10, R12.
- F4. Status card. A notification renders with the identity line; a reply to it records nothing. Covers R5.
- F5. Stale reply. The owner replies to an old card; nothing is recorded; a stale tap keeps its existing refusal. Covers R11.

## Acceptance Examples

- AE1 (**R1, R3**). Given a card with all fields populated, when rendered, then the sections appear in the fixed order, title and labels bold, choices numbered with notes, the recommended option marked — and the renderer output equals the pinned fixture (deterministic).
- AE2 (**R2, R7**). Given cards with none / some / all provenance fields, when rendered, then the identity line equals the expected string for each subset and shrinks gracefully.
- AE3 (**R4**). Given a field containing markup metacharacters and a card whose text exceeds the budget, when rendered, then every metacharacter is escaped, the trim marker is visible, and the total is under the platform limit before the send.
- AE4 (**R10, R13**). Given a live card with a parked waiter and an owner reply carrying custom text, when the reply lands, then the card's lifecycle fields equal the fields a same-moment tap writes except the absent choice and the recorded text; the waiter wakes with the text; a boundary read returns it.
- AE5 (**R10**). Given a service restart between send and reply, when the owner replies, then the reply still resolves to the card.
- AE6 (**R11**). Given a non-owner / non-private / unknown-card / closed-card reply, when handled, then nothing is recorded and no exception escapes the adapter.
- AE7 (**R5**). Given a status message, when rendered, then it carries the identity line and no options; a reply to it records nothing.
- AE8 (**R8, R14**). Given the served tool text and the repository docs, when read after this change, then the four fields and the reply interpretation rule are stated; the suite is green; the scan is clean.

## Success Criteria

- SC1. On the phone, every card says who asks, from where, and about what, at a glance — proven across the three daily runtimes by the adoption child.
- SC2. The owner can answer in his own words or ask a question from the card, and the exact asking session receives it with no chat announcement — exact-case proof in the adoption child.
- SC3. The suite is green, standard library only, the private-term scan is clean, and the credential boundary is provably unchanged (create cannot answer).

## Scope Boundaries

**Deferred for later**

- Reviving the same card for a question reply (edit the message in place: explanation plus buttons back). Add when the fresh-card re-ask proves clunky in real use.
- A courtesy notice when the owner replies to a closed card; taps have a toast, replies have no equivalent channel yet.
- Auto-derived provenance (client sniffing). Rejected deliberately: the surface is stateless, and wrong context is worse than absent.

**Out of scope entirely**

- Per-runtime integration code; changing what a tap means; changing the answer authority or the credential boundary; auto-execute of any kind; new third-party dependencies; a per-card opt-out of replies (the freeform field stays schema-only).

## Sequencing

1. The renderer: sections, identity line, budget, escaping, reply hint (R1–R6) — child 1.
2. Provenance fields and their teaching (R7–R9, with R2) — child 2.
3. Reply intake and protocol teaching (R10–R13) — child 3.
4. Adoption on the three runtimes and the exact-case proof (R14 sweep, SC1–SC2) — child 4.
