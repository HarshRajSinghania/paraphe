# Seed: print the version from the distribution metadata

Status: **draft. Nothing is filed.** The flip files this issue once the
repository is public. The body is preserved from the pre-flip first-time issue;
its references are paths, and they are current at the reset.

| | |
|---|---|
| Title | Print the version from the distribution metadata |
| Labels | `good first issue`, `ready-for-agent` |
| Origin | the pre-flip first-time issue, content preserved |

## Body

```markdown
## What is missing

`paraphe --version` should print the version of the installed distribution, and
`python3 -m paraphe --version` should print the same thing.

Today `--help` is the only flag the entry point answers: `ask` and `wait` are
the only subcommands, `--config` takes a path, and anything else is read as
configuration. A reader filing a bug report has no way to ask the tool which
version they are running.

## Where

`src/paraphe/__main__.py` — add `--version` beside the existing help handling in
`main`, and read the value from `importlib.metadata.version("paraphe")` rather
than a second literal that will drift from `pyproject.toml`.

## Acceptance

- `paraphe --version` exits 0 and prints the version declared in
  `pyproject.toml`.
- `python3 -m paraphe --version` prints the same string.
- Both answer without configuration: no `paraphe.toml` and no `PARAPHE_*`
  variable is required, exactly as `--help` behaves today.
- The suite stays green: `python3 -m unittest discover -s tests -p 'test_*.py'`.
- One test covers it, in `tests/inbox/test_setup.py` beside the console-command
  tests.

## Notes

Nothing outside the standard library. `importlib.metadata` is stdlib; no
dependency is needed.
```

## Why this is a good first issue

One file, one flag, one test, and an acceptance list that is already written.
Nothing in it can change a card's lifecycle or the credential boundary.
