# Contributing

Thanks for your interest in **ZHA Firmware OTA Manager**!

## Reporting a bug

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml).

## Requesting a feature

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml).

## Pull requests

1. Fork the repository.
2. Create a dedicated branch: `git checkout -b feat/my-feature`.
3. Set up the environment: `scripts/setup`.
4. Write code and add/update tests: `scripts/test`.
5. Check lint and typing: `scripts/lint`.
6. Use [Conventional Commits](https://www.conventionalcommits.org/): `feat: …`, `fix: …`.
7. Push and open a PR against `main`.

## Local setup

```bash
pipx install prek   # or: brew install j178/prek/prek
scripts/setup       # installs deps + the prek hook
```

`prek` is a Rust drop-in replacement for `pre-commit` (much faster) that reads
the same `.pre-commit-config.yaml`. If you prefer the Python version:
`pipx install pre-commit`.

> Note: `mypy` is intentionally **not** a pre-commit hook (its environment,
> which needs Home Assistant, is too large). It runs in CI and via
> `scripts/lint`.

## Dependency management

This repository uses **Renovate** (not Dependabot). Update PRs are opened by
`@renovate[bot]`; see the dependency dashboard in the issues.
