# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.9] - 2024-05-22
### Added
- OMPE-7960: Added functions `purge_all_notifications()` and `get_all_notifications()`
-  destroy_all_notifications() will destroy all notifications. Active or pending.
-  get_all_notifications() will return a list of notifications. Active or pending.

## [1.0.8] - 2024-04-02
### Added
- Add docs.

## [1.0.7] - 2023-08-02
### Changed
- Fix tests.

## [1.0.5] - 2022-12-13
### Changed
- Fix dismissed state check for notification.

## [1.0.4] - 2022-03-11
### Changed
- Fix issue when notifications are posted through non-main threads.

## [1.0.3] - 2022-02-16
### Changed
- Add unittests.

## [1.0.2] - 2022-02-08
### Changed
- Fix issue that non-auto-hide notifications will re-appear after resizing viewport.

## [1.0.1] - 2022-01-14
### Added
- Improve notification manager to support stacking notifications.

## [1.0.0] - 2021-02-21
### Added
- Initial version.
