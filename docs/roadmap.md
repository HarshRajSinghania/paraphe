# Roadmap

What Paraphe is building next, and what it is deliberately not building. An
item leaves this file when it ships or when it is decided against; the
reasoning for a decision against lives in the issue that closed it.

## Next

- **A recorded demo of the phone loop.** The console loop is recorded in
  [`demo/console-loop.md`](demo/console-loop.md); the phone path needs a
  recording made on a device, which no machine in this repository can produce.
- **A shipped tap transport for the phone destination.** Today the repository
  ships the adapter behind its contract and the deployment supplies the bot
  configuration; a first run needs neither. Shipping one would let a reader
  point Paraphe at a phone without reading `docs/adapters.md`.
- **Portability to Windows.** The suite binds a loopback address, relies on
  file modes and assumes a data location that does not exist there. The
  platform needs that work before a Windows job in integration would be
  honest.
- **An upgrade path that moves an existing store.** Paraphe refuses to start
  against an empty location while a store exists elsewhere; it does not move
  that store. A move is a smaller change than it sounds, once someone needs it.
- **Coverage gates and static type checking.** Neither is earned at this
  version; the suite is the witness, and it is read.
- **PyPI releases.** The distribution publishes from the release workflow
  ([`../.github/workflows/publish.yml`](../.github/workflows/publish.yml)) when
  a release is cut — wheel and sdist, trusted publishing, no stored token.
  `pip install paraphe` is the one-line install; the owner's link step is
  [`launch/pypi-runbook.md`](launch/pypi-runbook.md).

## Not planned

- **An agent answering its own decision.** On any surface, at any
  configuration. This is the product.
- **A general workflow engine, task tracker or chat client.** Paraphe holds one
  decision at a time, from one agent to one owner.
- **A destination leaderboard.** More destinations is not the point; two
  methods and a contract is.
