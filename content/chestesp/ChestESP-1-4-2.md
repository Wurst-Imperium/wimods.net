---
title: ChestESP 1.4.2
layout: update
date: 2025-11-05T10:30:00+01:00
image: 
  https://images.wurstclient.net/_media/update/chestesp/chestesp_1.4.2_540p.webp
mod: chestesp
modversion: "1.4.2"
mcversions:
- 1.21.11
- 1.21.10
- 1.21.9
- 1.21.8
- 1.21.4
- 1.21.1
neoforge:
- 1.21.11
- 1.21.10
- 1.21.9
- 1.21.8
- 1.21.4
- 1.21.1
fabric:
- 1.21.11
---
## Changelog

- Fixed the NeoForge version of ChestESP no longer rendering anything, due to an undocumented change in NeoGradle 7.1 that disabled all mixins in production builds but kept them enabled during development and testing, effectively hiding the issue until a user reported it.

- This was originally a NeoForge-only release because the Fabric version of ChestESP was not affected by this issue. But this is also the version I used to update ChestESP to 1.21.11 so now there's a Fabric version of it too.
