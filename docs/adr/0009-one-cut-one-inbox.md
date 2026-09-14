# ADR 0009 — One cut, one inbox, one proof card

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing
- **Refines:** ADR 0004 (who is in the cutover)

## Context

The approved callers already share one inbox. Running
Paraphe beside the previous inbox for the same caller would collect the same decision
twice. Unattended batch callers and crons stay on the previous inbox (ADR 0004). A
notify-only ping is not proof that a tap can resume the asking session
(ADR 0006).

## Decision

1. Those four callers flip in **one owner-approved cut**. After the cut,
   they talk only to Paraphe. They never send the same decision to both
   inboxes. There is no fallback to the previous inbox for a flipped caller.
2. The previous inbox stays live until **one real high-risk card** on Paraphe
   completes: tap → the same Hermes session acts → `report_execution` →
   `mark_processed`. Then the four flip together. A notify-only ping is
   not that card. Four per-caller proof cards are not required.
3. Unattended batch callers and crons keep using the previous inbox and may
   only send **different work** (their own batch/git class). They must not send
   a card for a decision the flipped callers would send.

## Consequences

The spec must name the single flip window and the proof-card checklist.
Per-harness order inside that window is ADR 0004: credential, endpoint,
behavior-block. Dual-write or “fall back to the previous inbox if Paraphe is down” is
forbidden for those four. A batch caller remaining on the previous inbox is
not a second yes if its `external_id` space stays in its own batch/git class
(its own `project` value today).
