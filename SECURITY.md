# Security policy

## Reporting a vulnerability

Use this repository's **private vulnerability reporting**: the Security tab →
*Report a vulnerability*. It opens a thread only the maintainers can see.

Do not open a public issue for a security problem, and do not paste a working
exploit there.

## What to expect

- **Acknowledgement** within three days.
- **An assessment** — whether it is a vulnerability, its severity, and whether
  we can reproduce it — within ten days.
- If it is a vulnerability: a fix in the default branch, and a note in the
  release that carries it. You are credited unless you ask not to be.
- If it is not: an explanation of why not, in the same thread.

This is a self-hosted project without a paid security team, so these are
intentions rather than a contract, but silence is not an answer — if you have
heard nothing in ten days, say so in the thread.

## What is in scope

- The credential boundary: anything that lets the create credential answer a
  decision, or lets an answer be recorded without the owner identity.
- The store: reading or writing outside the configured data location, or a
  relocation that strands cards.
- The HTTP surface: authentication bypass, request smuggling, denial of
  service from an unauthenticated caller.
- The tap path: a callback that claims a card without the owner identity, or a
  stale callback that is accepted after the card changed.

## What is not

- Running Paraphe without configuring credentials, or otherwise beyond what the
  README documents.
- Anything that requires an attacker to already hold the owner's answer
  credential.
