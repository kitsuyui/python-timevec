# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2] - 2026-05-03

### Changed
- Add workflow concurrency groups to CI

## [0.3.1] - 2025-02-01

### Changed
- Migrate package manager from Poetry to uv
- Set minimal permissions in CI publish workflow
- Add actionlint check to CI

### Fixed
- Fix decade range near datetime minimum

## [0.3.0] - 2024-10-16

### Added
- Add Python 3.13 support

## [0.2.0] - 2023-10-06

### Added
- Add Python 3.12 support

## [0.1.7] - 2023-07-17

### Changed
- Minor refactor: convert comments to docstrings

## [0.1.6] - 2023-02-18

### Added
- Add `py.typed` marker for PEP 561 compliance

## [0.1.5] - 2023-02-08

### Changed
- Rewrite vector ↔ time conversion logic
- Add additional tests for time/vector round-trips

## [0.1.4] - 2023-01-26

### Added
- Reverse conversion: create datetime from time vector
- Add tests for many dates

## [0.1.3] - 2023-01-24

### Added
- Add `numpy.datetime64` vector support
- Unify date conversion between `builtin_math` and `numpy` submodules

## [0.1.2] - 2023-01-23

### Fixed
- Fix boundary value bug in edge cases

## [0.1.1] - 2023-01-23

### Changed
- Abstract common logic across `year_vec`, `month_vec`, `day_vec`, `week_vec`
- Add figure to README illustrating vector representation

## [0.1.0] - 2023-01-21

### Added
- Initial release
- Time vector representation using cos/sin for periodicity
- `builtin_math` submodule (no NumPy dependency)
- `numpy` submodule (optional NumPy support)

[Unreleased]: https://github.com/kitsuyui/python-timevec/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/kitsuyui/python-timevec/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/kitsuyui/python-timevec/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/kitsuyui/python-timevec/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kitsuyui/python-timevec/compare/v0.1.7...v0.2.0
[0.1.7]: https://github.com/kitsuyui/python-timevec/compare/v0.1.6...v0.1.7
[0.1.6]: https://github.com/kitsuyui/python-timevec/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/kitsuyui/python-timevec/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/kitsuyui/python-timevec/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/kitsuyui/python-timevec/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/kitsuyui/python-timevec/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/kitsuyui/python-timevec/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/kitsuyui/python-timevec/releases/tag/v0.1.0
