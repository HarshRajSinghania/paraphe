# PyPI runbook

The owner links the pending publisher once; from then on the release does the
rest. It is about two minutes, it can be done any time before the release, and
a pending publisher claims nothing until its first use — nothing is published
until a release is cut.

This is the link step the flip checklist runs as its own row; the workflow it
points at is
[`.github/workflows/publish.yml`](../../.github/workflows/publish.yml).

## Link the pending publisher

The PyPI account exists. Two-factor authentication must be enabled on it — PyPI
requires 2FA to publish.

1. Sign in at <https://pypi.org>.
2. Open <https://pypi.org/manage/account/publishing/> and choose **Add a new
   pending publisher**.
3. Fill the GitHub form exactly:

   | Field | Value |
   |---|---|
   | PyPI Project Name | `paraphe` |
   | Owner | `leonardsellem` |
   | Repository name | `paraphe` |
   | Workflow name | `publish.yml` |
   | Environment name | *leave empty* |

4. Submit. The page lists the pending publisher.

## After that

Nothing manual. Cutting the release — tag `v0.1.0` from `main` plus the
GitHub Release — triggers the publish workflow, which builds the wheel and the
sdist and uploads them with trusted publishing over OIDC: no API token, no
secret stored anywhere.

## Notes

- **The environment stays empty on both sides.** The workflow declares no
  GitHub `environment:`, so the PyPI form must leave the environment blank. A
  name on either side and the OIDC exchange is refused.
- **2FA**: enable it under Account settings → Two-factor authentication.
  Trusted publishing removes the token; it does not remove 2FA.
- **The name** `paraphe` was unclaimed when checked on 2026-09-14. A pending
  publisher does not reserve it; if the project exists by the time of the
  flip, stop and re-decide.
- **Read back after the flip**: <https://pypi.org/pypi/paraphe/0.1.0/json>
  serves 0.1.0, and a clean environment completes `pip install paraphe` and
  the console loop.
