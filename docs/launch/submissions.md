# Directory submissions — staged shortlist

Status: staged 2026-09-14. **Nothing has been submitted, sent, or opened.**
Every submission is owner-run after the flip; this file makes each one a paste,
not research. Rules were read live on 2026-09-14 and are quoted verbatim —
lists change, so re-read each rules page at submission time.

Suggested order after the flip: targets 1–3 any time; target 4 is date-gated.
All four also appear in `docs/launch/flip-checklist.md` (rows 12–15).

## Targets

### 1. awesome-mcp-servers (`punkpeye`) — eligible

- Rules read live on 2026-09-14 (CONTRIBUTING.md + README, `https://github.com/punkpeye/awesome-mcp-servers`).

> When adding a new server, make sure to include:
> * The server name, linked to its repository.
> * A brief description of the server's functionality.
> * Categorize the server appropriately under the relevant section. If a new category is needed, please create one and maintain alphabetical order.

> * **Alphabetical order:** Maintain alphabetical order within each category of servers.
> * **One server per line:** List each server on a separate line for better readability.

- Eligibility: yes — the entry is a repository link plus a description; no package or account requirement. The category list includes "Agreements & Coordination": "MCP servers for creating, coordinating, and executing agreements: commitments, escrow, and multi-party decision workflows across humans, agents, and organizations." Fallback if a maintainer prefers: "Other Tools and Integrations".
- Entry format: one line per server, language/scope/OS glyphs from the README legend (`🐍` Python, `🏠` local service, `🍎` macOS, `🐧` Linux), description ending in a period.
- Draft entry (paste as-is, alphabetically inside the category — after `humanforai/humanforai-mcp`; confirm against the live list at submission). Link text is the server name; the list's entries often show `owner/repo` — cosmetic either way:

```
- [paraphe](https://github.com/leonardsellem/paraphe) 🐍 🏠 🍎 🐧 - Self-hosted owner-decision inbox: an agent asks for approval over MCP, the owner answers from Telegram or the console, and the asking agent resumes. The credential an agent holds creates and reads cards but cannot answer one.
```

### 2. MCP Registry (`modelcontextprotocol/registry`) — eligible once `paraphe` 0.1.0 is on PyPI

- Rules read live on 2026-09-14 (quickstart + package-types + remote-servers docs, `https://github.com/modelcontextprotocol/registry`).

> If you are publishing a non-npm package (PyPI, NuGet, OCI, MCPB), the overall flow is identical, but the ownership-verification step in Step 1 is different per package type.

> The MCP Registry verifies ownership of PyPI packages by checking for the existence of an `mcp-name: $SERVER_NAME` string in the package README (which becomes the package description on PyPI).

> The MCP Registry is currently in preview. Breaking changes or data resets may occur before general availability.

- Eligibility: yes, by package — `paraphe` is a PyPI distribution. Not by remote: "A remote server MUST be publicly accessible at its specified URL", and a self-hosted instance is not. The name must start with `io.github.<github-username>/` under GitHub authentication.
- Entry format: a `server.json` file plus the `mcp-publisher` CLI (`init` → `login github` → `validate` → `publish`); the ownership marker must be inside the published package's description.
- Pre-release requirement (the registry reads the marker from the PUBLISHED PyPI artifacts, so a README edit after the release never reaches it): the repository README ships `<!-- mcp-name: io.github.leonardsellem/paraphe -->` before the `v0.1.0` release — the published 0.1.0 artifacts then carry it. Read back before submitting: `https://pypi.org/pypi/paraphe/0.1.0/json` → `info.description` contains the marker line.
- Fallback if the marker is absent at flip: do NOT submit. Cut a patch version with the marker in the README, republish, and bump `server.json`'s `version` fields (server and package) to match.
- Pre-flight for the owner: read back that the service runs and serves the MCP surface at the transport URL below — actually start it (`pip install paraphe`, write `paraphe.toml`, run `.venv/bin/paraphe --config paraphe.toml`) and probe `http://127.0.0.1:8787/mcp` (the shipped default port; `PARAPHE_MCP_PORT` overrides it) before trusting this draft's transport block.
- Draft `server.json`:

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.leonardsellem/paraphe",
  "title": "Paraphe",
  "description": "Self-hosted owner-decision inbox: an agent asks for approval over MCP, the owner answers from Telegram or the console, and the asking agent resumes.",
  "repository": { "url": "https://github.com/leonardsellem/paraphe", "source": "github" },
  "version": "0.1.0",
  "packages": [
    {
      "registryType": "pypi",
      "identifier": "paraphe",
      "version": "0.1.0",
      "runtimeHint": "uvx",
      "transport": { "type": "streamable-http", "url": "http://127.0.0.1:8787/mcp" }
    }
  ]
}
```

### 3. mcpservers.org (the `wong2` directory) — eligible

- Rules read live on 2026-09-14 (README of `https://github.com/wong2/awesome-mcp-servers` + the submit form).

> We do not accept PRs. Please submit your MCP on the website: https://mcpservers.org/submit

- Eligibility: yes — free website submission, no PR. "Listings on mcpservers.org are free"; a paid premium option exists and is not needed.
- Entry format: the submit form fields — Server Name; Short Description; Link (GitHub or docs); Category (dropdown); Contact Email (the owner supplies their own at submission time).
- Draft entry: name `Paraphe`; short description: `Self-hosted owner-decision inbox: an agent asks for approval over MCP, the owner answers from Telegram or the console, and the asking agent resumes.`; link `https://github.com/leonardsellem/paraphe`; category `Development`.

### 4. awesome-selfhosted — eligible, date-gated (four months after the first release)

- Rules read live on 2026-09-14 (CONTRIBUTING.md + addition template, `https://github.com/awesome-selfhosted/awesome-selfhosted-data`).

> Create a new `software/software-name.yml` file, based on the template in `.github/ISSUE_TEMPLATES/addition.md`. Please use kebab-case for file naming, for example, `my-awesome-software.yml`.

> Please avoid redundant terms in project descriptions, such as _open-source_, _free_, _self-hosted_... as their presence on awesome-selfhosted already implies this.

> - [ ] Any software project you are adding was first released more than 4 months ago.

- Eligibility: free software and self-hostable (`AGPL-3.0-or-later`, a tagged release, working install instructions) — but the release-age gate applies: the first release is `v0.1.0` at the flip, so the earliest submission is four months after flip day. Do not submit before that; the maintainers close it with the quoted rule.
- Entry format: a YAML file in the data repository's `software/` directory (kebab-case filename, `paraphe.yml`); fields from the addition template, description under 250 characters and in sentence case.
- Draft `software/paraphe.yml` (confirm the best tag against the live tag list at submission — no agent/MCP tag exists yet; `Miscellaneous` is the list's own fallback):

```yaml
name: "Paraphe"
website_url: "https://github.com/leonardsellem/paraphe"
source_code_url: "https://github.com/leonardsellem/paraphe"
description: "Owner-decision inbox for agents: an agent asks, you answer from your phone or terminal, the same agent resumes."
licenses:
  - AGPL-3.0
platforms:
  - Python
  - Docker
tags:
  - Miscellaneous
depends_3rdparty: false
```

## Checked, not targets — 2026-09-14

Recorded so nobody re-researches them:

- **`modelcontextprotocol/servers`** — retired third-party listings; the Registry (target 2) is its successor:

> The README no longer contains a list of third-party MCP servers — that list has been retired in favor of the [MCP Server Registry](https://github.com/modelcontextprotocol/registry). To make your server discoverable, follow the [quickstart guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx) to publish it there.

- **`vinta/awesome-python`** — a fixed-size shortlist, not a catalog; not a fit at launch:

> awesome-python is a shortlist, not a catalog.

> **Evidence**: admission is decided by maintainer editorial judgment, informed primarily by PyPI download counts rather than GitHub stars.

- **`e2b-dev/awesome-ai-agents`** — no published contribution rules: no CONTRIBUTING file at the root and no contribution section in the README (both checked 2026-09-14); without a documented format it cannot be staged safely.
