# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Repository bootstrap: integration skeleton (single-instance config flow), CI
  (ruff, mypy, pytest), validation (hassfest, HACS), security (CodeQL,
  pip-audit, gitleaks), release pipeline (release-please), Renovate config, and
  dev container.
- Runtime injection of the community Koenkk/zigbee-OTA provider into ZHA's
  zigpy application, plus a `zha_firmware.check_updates` service to re-run it.
