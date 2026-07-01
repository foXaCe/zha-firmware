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
- Runtime injection of OTA sources into ZHA's zigpy application, plus a
  `zha_firmware.check_updates` service to re-run it on demand.
- Options flow to manage OTA sources: toggle the Koenkk/zigbee-OTA index, add
  extra remote index URLs, add a local firmware folder, and toggle the OTA
  broadcast.
- Config flow aborts when the ZHA integration is not set up.
- Periodic ensure loop that re-injects the sources after a ZHA reload.
