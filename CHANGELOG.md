# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0 (2026-07-01)


### Added

* add options flow, ZHA guard, and re-injection loop ([440f38a](https://github.com/foXaCe/zha-firmware/commit/440f38a8b50912c50ceabf96cf21d319fdd85dd7))
* bootstrap ZHA Firmware OTA Manager integration ([1b22036](https://github.com/foXaCe/zha-firmware/commit/1b22036ae0a08e0657b237239c311788b7ab80d8))
* inject Koenkk OTA provider into ZHA; make repo content English ([83006f5](https://github.com/foXaCe/zha-firmware/commit/83006f57bcd976c57affc2d2768ff6a381b77c95))

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
