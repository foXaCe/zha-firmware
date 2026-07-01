# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0](https://github.com/foXaCe/zha-firmware/compare/v1.2.0...v1.3.0) (2026-07-01)


### Added

* bundle brand icons (Brands Proxy API) ([5cd72db](https://github.com/foXaCe/zha-firmware/commit/5cd72dbfb6581e9926370a1c59d017575b5f7c6e))

## [1.2.0](https://github.com/foXaCe/zha-firmware/compare/v1.1.0...v1.2.0) (2026-07-01)


### Added

* add OTA status sensor and diagnostics ([65471c8](https://github.com/foXaCe/zha-firmware/commit/65471c872b0cf509e83476175f96f949a3ccc6b3))
* add repair issue, options validation, and per-source index stats ([8e47b89](https://github.com/foXaCe/zha-firmware/commit/8e47b8952de805f2be78535c2c0e2d5e875d6075))

## [1.1.0](https://github.com/foXaCe/zha-firmware/compare/v1.0.0...v1.1.0) (2026-07-01)


### Added

* add official zigpy-ota source; fix ZHA gateway access ([dd49d6d](https://github.com/foXaCe/zha-firmware/commit/dd49d6d0de0b7f66fc258d09dbb555c610b48b15))

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
