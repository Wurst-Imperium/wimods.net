---
title: WI Freecam 1.1
layout: update
date: 2026-03-22T17:00:00+01:00
image: https://images.wurstclient.net/wi-freecam/2026/1.1/960x540.webp
mod: wi-freecam
modversion: "1.1"
mcversions:
- 26.1.1
- '26.1'
- 1.21.11
fabric:
- 26.1.1
- '26.1'
- 1.21.11
snapshots:
- 26.2-snapshot-1
- 26w14a
- 26.1.1-rc-1
- 26.1-rc-3
- 26.1-rc-2
---
## Changelog

- Added an "Interact from" setting. When changed to "Camera", this allows you to interact with blocks and entities from the camera like Freecam did in older versions of Wurst. ([#1300 (Wurst)](https://github.com/Wurst-Imperium/Wurst7/pull/1300), [/d/1491](https://wurstforum.net/d/1491), [/d/1505](https://wurstforum.net/d/1505))

- Added a "Reload chunks" checkbox to Freecam. Turning this off improves performance but can cause visual holes in the world. ([#6](https://github.com/Wurst-Imperium/WI-Freecam/issues/6))

- Fixed Freecam affecting vehicles in Camera input mode. ([#4](https://github.com/Wurst-Imperium/WI-Freecam/issues/4))

- Fixed some chunks being invisible while using Freecam with Sodium installed. ([/d/1502](https://wurstforum.net/d/1502))

- Changed `SectionOcclusionGraphMixin` to use `@WrapOperation` instead of `@Redirect` for better compatibility with other mods. No specific compatibility issues found, just making sure WI Freecam follows best practices.

- Further improved the automated test system.
