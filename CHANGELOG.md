# Changelog

All notable changes to **tray-ping-monitor** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2026-08-19

### Added
- **Dual-Mode Latency Engine**: Automatic ICMP echo with instant TCP socket fallback (port 443) for firewalled game servers (e.g. Valorant / Riot shards, AWS GameLift).
- **Roblox Live In-Game Auto-Detect**: Real-time sniffer for `%localappdata%\Roblox\logs` that extracts the exact server IP (`128.116.x.x`) upon joining any place.
- **Valve SDR Relays (CS2 / Steam)**: Added regional endpoints for Stockholm, Frankfurt, Warsaw, Vienna, Helsinki, London, and Virginia.
- **Categorized Submenus**: Grouped server list by game (Roblox, CS2 / Steam, Valorant / Riot, Discord, DNS).

### Fixed
- Fixed `AttributeError: type object 'MenuItem' has no attribute 'SEPARATOR'` crash in `pystray` menu builder.
- Fixed Valorant / Riot Games connection timeouts by routing through high-availability API endpoints.

### Changed
- **Visual Overhaul**: Redesigned tray icon badge using 4x supersampling (256x256 rendered with Lanczos downscaling) for ultra-sharp anti-aliased text and borders.
- **Clean UI**: Removed all emoji spam across the application menus, tooltip strings, and configuration files.

---

## [1.0.0] - 2026-08-19

### Added
- Initial project release with basic tray icon and rolling ping stats.
- Standalone portable `.exe` build with PyInstaller.
- Configurable polling intervals and thresholds via `config.json`.
