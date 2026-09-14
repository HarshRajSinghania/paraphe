# Labels (draft)

Status: **draft. Nothing here is applied.** The new repository starts with zero
labels — the flip files these, once the repository is public. This file is the
plan and the exact commands, not the doing.

## Triage vocabulary

These are the five strings [`docs/agents/triage-labels.md`](../agents/triage-labels.md)
maps, and a maintainer applies exactly one of them to an open issue
([`docs/agents/issue-tracker.md`](../agents/issue-tracker.md), "Workflow").

```text
needs-triage
needs-info
ready-for-agent
ready-for-human
wontfix
```

The five lines above are the byte-match target. The gate, run from the
repository root:

```bash
diff <(awk -F'|' '/^\| `/ {gsub(/[ `]/,"",$3); print $3}' docs/agents/triage-labels.md) \
     <(sed -n '/^## Triage vocabulary$/,/^## /p' docs/launch/labels.md | grep -E '^[a-z][a-z-]+$')
```

Empty output is the pass; anything printed is a string that drifted.

## Contributor labels

Two more, for the funnel a first visitor walks into:

| Label | Meaning |
|---|---|
| `good first issue` | A bounded change with everything a newcomer needs: one or two files, a test to copy, an acceptance list. |
| `help wanted` | Open for someone else to take — the maintainer is not the bottleneck, the work is. |

## Descriptions and colours

Colours are the ones this project already uses, so a label means the same thing
before and after the reset.

| Label | Colour | Description |
|---|---|---|
| `needs-triage` | `C2E0C6` | Maintainer needs to evaluate this issue |
| `needs-info` | `FEF2C0` | Waiting on reporter for more information |
| `ready-for-agent` | `C5DEF5` | Fully specified, ready for an AFK agent |
| `ready-for-human` | `C5DEF5` | Requires human implementation |
| `wontfix` | `BFDADC` | Will not be actioned |
| `good first issue` | `7057ff` | Good for newcomers |
| `help wanted` | `008672` | Extra attention is needed |

## The commands

Run from the repository root: `gh` resolves the repository from the remote.
`--force` creates the label, or updates the description and colour if it is
already there, so the block is safe to re-run.

```bash
gh label create needs-triage --color C2E0C6 --description "Maintainer needs to evaluate this issue" --force
gh label create needs-info --color FEF2C0 --description "Waiting on reporter for more information" --force
gh label create ready-for-agent --color C5DEF5 --description "Fully specified, ready for an AFK agent" --force
gh label create ready-for-human --color C5DEF5 --description "Requires human implementation" --force
gh label create wontfix --color BFDADC --description "Will not be actioned" --force
gh label create "good first issue" --color 7057ff --description "Good for newcomers" --force
gh label create "help wanted" --color 008672 --description "Extra attention is needed" --force
```

## Notes for the flip

- A new repository is created with GitHub's defaults: `bug`, `documentation`,
  `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`,
  `question`, `wontfix`. Three of the seven above already exist there, with
  different text for `wontfix`; `--force` is what makes the result
  deterministic. The four triage labels do not exist by default.
- Nothing is deleted. The defaults that are not in the plan stay as they are.
- One label per issue from the triage five, plus any of the two contributor
  labels. Two triage labels on one issue means it was not triaged.
