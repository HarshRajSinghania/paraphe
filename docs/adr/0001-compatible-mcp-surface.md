# ADR 0001 — Compatible MCP surface

- **Status:** Accepted (2026-08-25)
- **Supersedes:** nothing

## Context

Hermes, Codex, Claude, and Grok already talk to the inherited inbox through a known MCP
tool set (`request_approval`, `ask_question`, `get_response`,
`list_unprocessed`, `mark_processed`, `report_execution`, and kin). Skills
and souls are written against those names and reliability fields
(`external_id`, `version`, expiry, honest risk). A clean-break API would
force a rewrite of that contract before Paraphe had proven the return path.

## Decision

Paraphe v1 exposes the same tool names and reliability fields that surface already
uses. iOS-only extras (bulk approve, lock-screen chrome, "Always allow"
`rule_key`) are dropped unless a later ticket proves they are required for the
cutover.

## Consequences

The spec must enumerate every live tool, required argument, and
response field with keep or drop. The keep/drop inventory lives in
`docs/research/mcp-surface-keep-or-drop.md` and is the normative source. Clients can be pointed at Paraphe without renaming tools.
Anything that exists only to serve a mobile app that is not paraphe's stays out of v1.
