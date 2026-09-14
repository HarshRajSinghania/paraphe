Closes #

<!-- Base this pull request on `dev`. `main` only receives pull requests from `dev`. -->

## What changed

<!-- One paragraph. What behaviour is different after this? -->

## Verification

- [ ] `python3 -m unittest discover -s tests -p 'test_*.py'` is green, and I
      read the test count.
- [ ] The behaviour I changed is covered by a test that fails without this
      change.
- [ ] If this touches the create/answer credential boundary: a test proves the
      create credential is refused on the answer path, no claim is recorded,
      and the card is unchanged.
- [ ] `python3 tools/scan_private_terms.py` exits 0 over the tracked tree.
- [ ] `python3 tools/scan_private_terms.py --commits origin/dev..HEAD` exits 0
      over the commit messages in this branch.
- [ ] No secret, token or credential value appears in this diff.

## Notes for the reviewer

<!-- Anything you decided that the diff does not explain. -->
