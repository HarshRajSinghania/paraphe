# Launch post (draft)

Status: draft, refreshed 2026-09-14. **Not posted.** Posting is a separate
owner decision that follows the visibility flip; nothing in this file has been
sent anywhere.

One post per channel. The primary channel is **Show HN** — it carries the full
argument below; the other two are short and link to it. The claim check (every
claim mapped to its source) is at the end of this file.

---

## Primary post — Show HN (full argument)

**Title:** Show HN: Paraphe – a self-hosted owner-decision inbox for agents

**Text to post:**

An agent asked me a question, and I answered it from my phone.

I run agents that do real work — they ship changes, they spend money, they touch
production. The hard part was never the work. It was the moment one of them
needs a decision from me and I am not at a keyboard.

Every tool I looked at wanted to be a platform: a workflow engine, a task
tracker, a chat client with a bot framework bolted on. I wanted one thing: my
agent asks, I answer from wherever I am, and the same agent picks the answer up
and keeps going.

So I built the small version of it. **Paraphe** is a self-hosted owner-decision
inbox.

- **One decision at a time.** An agent raises a card. It lands on your phone
  (Telegram) or on the console of the machine running it. You answer. The agent
  that asked resumes.
- **The agent cannot answer its own card.** Its credential creates and reads.
  Answering needs the owner's credential, on a path the agent's cannot reach.
  That is the product, and it is not a setting.
- **Zero dependencies.** The runtime imports nothing outside the Python
  standard library. `pip install paraphe` fetches a wheel; there is nothing to
  compile, nothing to audit, and nothing to upgrade.
- **Your data is a SQLite file** in your own data directory, `0600`, and
  nothing is read or written outside it.
- **Add a destination in two methods.** `notify` and `edit_and_strip`. The
  console destination is 60 lines and is the worked example.

An inbox an agent can approve on its owner's behalf is not an owner-decision
inbox. Paraphe is deliberately bad at being that, and deliberately good at
being the other thing.

The repository is shaped the same way I want contributions to flow: every
change lands on `dev` through a pull request, `main` only takes promotions from
`dev`, and releases are tagged from `main`.

**Quick start**

```bash
python3 -m venv .venv
.venv/bin/pip install paraphe
cp config.example.toml paraphe.toml   # fill in two values you make up
.venv/bin/paraphe --config paraphe.toml
```

The file carries two values: `mcp_create_bearer`, which the agent holds, and
`owner_answer_token`, which only you hold.

AGPL-3.0-or-later. Self-host it, change it, run it for your team. If you serve
it to other people over a network, they get your modified source.

---

## Secondary posts (ready; each links the primary)

### r/selfhosted

**Title:** Paraphe – a self-hosted owner-decision inbox for agents (one small
Python service, SQLite, zero dependencies)

**Text to post:**

I built Paraphe for one moment: an agent I run needs a decision, and I am not
at a keyboard. The agent asks over MCP, the card lands on Telegram or on the
console, I answer, and the same run picks the answer up and resumes.

- One small Python service, nothing outside the standard library, data in one
  SQLite file.
- A container is in the repository, with the data location mounted.
- The credential the agent holds cannot answer a decision — that asymmetry is
  the product.

Full write-up: `<paste the primary post URL once it is live>`

Source: https://github.com/leonardsellem/paraphe

### r/LocalLLaMA

**Title:** Paraphe – an owner-decision inbox for agents: the agent asks, you
answer, the same run resumes

**Text to post:**

Every agent stack eventually hits the same moment: the agent needs a decision
and you are not at a keyboard. I built a small self-hosted service for exactly
that — an MCP surface where an agent raises a card, the card reaches you on
Telegram or the console, and the asking agent resumes with your answer.

There is a recorded console run of the whole loop, including the agent's own
credential being refused on the answer path, and the tool surface is documented
in the repository.

Full write-up: `<paste the primary post URL once it is live>`

Source: https://github.com/leonardsellem/paraphe

## Channel map

| Channel | Role | Why it fits | What to attach |
|---|---|---|---|
| Show HN | primary — full argument | the audience runs agents and self-hosts, and the "agent cannot answer its own card" line is a genuine argument | the recorded console-loop demo (README first screen) and the one-line install |
| r/selfhosted | links the primary | cares about zero dependencies, a SQLite file, one container | the Dockerfile and the mounted-data note |
| r/LocalLLaMA | links the primary | cares about the tool surface and the resume path | `docs/tools.md` and the recorded console loop |

---

## Claim check (review notes — not part of any post)

Every factual claim above maps to a source. No claim exceeds the launch surface
delivery (README hero, demo, badge, `publish.yml`, runbook) or the flip
delivery (rulesets, release, PyPI publish, seeds).

| Claim in the post | Source |
|---|---|
| "Paraphe is a self-hosted owner-decision inbox" | shipped `README.md` opening |
| card lands on Telegram or the console; the owner answers; the asking agent resumes | shipped `src/paraphe/adapters/console.py`, `src/paraphe/adapters/telegram.py`, `docs/tools.md` lifecycle, `docs/adr/0011-answer-returns-through-the-ask.md` |
| "The credential an agent holds cannot answer a decision" | `docs/adr/0010-bearer-creates-owner-taps.md`; boundary tests under `tests/inbox/` |
| "Zero dependencies. The runtime imports nothing outside the Python standard library." | shipped `pyproject.toml` (`dependencies = []`) and `src/paraphe/` |
| "`pip install paraphe` fetches a wheel" | plan R16; launch-surface delivery (the publish workflow builds wheel + sdist); flip delivery (PyPI publish row) |
| quick start (`venv`, `pip install paraphe`, two-value `paraphe.toml`, `--config`) | plan R16 (one-line path, venv and configuration steps stay); shipped `config.example.toml` and `pyproject.toml` entry point |
| config values `mcp_create_bearer` / `owner_answer_token` | shipped `config.example.toml` |
| "SQLite file in your own data directory, `0600`, nothing read or written outside it" | shipped `src/paraphe/inbox/store.py` (`STORE_MODE`, `DATA_DIR_MODE`, `default_data_dir`) |
| "Add a destination in two methods. `notify` and `edit_and_strip`." | shipped `docs/adapters.md`; `src/paraphe/adapters/console.py` |
| "The console destination is 60 lines and is the worked example." | shipped `src/paraphe/adapters/console.py` (`wc -l` = 60); `docs/adapters.md` ("the smallest complete implementation") |
| "every change lands on `dev` through a pull request, `main` only takes promotions from `dev`, releases tagged from `main`" | plan R5–R9; the source check (gates lane) and the rulesets armed by the flip lane |
| "AGPL-3.0-or-later … they get your modified source" | shipped `LICENSE`, `pyproject.toml` (`license = "AGPL-3.0-or-later"`) |
| attach: recorded console-loop demo | launch-surface delivery (demo asset); shipped `docs/demo/console-loop.md` |
| attach: Dockerfile and the mounted-data note | shipped `Dockerfile`, README container section |
| attach: `docs/tools.md` | shipped `docs/tools.md` |
| first-person narrative (what the author runs, why the tool exists) | narrative only — no surface assertion |
