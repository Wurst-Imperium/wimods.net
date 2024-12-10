---
title: ChestESP 1.2 - Normal Chests Toggle, Easier Installation, Automated Testing
date: 2024-11-15T16:00:00+01:00
image: https://images.wurstclient.net/_media/update/chestesp/chestesp_1.2_540p.webp
mod: chestesp
modversion: "1.2"
mcversions:
- 1.21.4
- 1.21.3
- 1.21.2
- 1.21.1
- "1.21"
neoforge:
- 1.21.3
- "1.21"
---
## Changelog

- Added an "Include normal chests" option so you can turn off the ESP on normal chests while still keeping it enabled on other containers. ([#5](https://github.com/Wurst-Imperium/ChestESP/issues/5))

- ChestESP now includes ModMenu (v11.0.3 in Fabric 1.21 - 1.21.1, v12.0.0-beta.1 in Fabric 1.21.2 - 1.21.3) so you don't have to install it separately anymore.

- ChestESP now includes Cloth Config (v15.0.140 in Fabric/NeoForge 1.21 - 1.21.1, v16.0.141 in Fabric/NeoForge 1.21.2 - 1.21.3) so you don't have to install it separately anymore.

- If you already have a different version of ModMenu or Cloth Config installed (e.g. from a modpack), Fabric/NeoForge will prioritize your version over the one that comes with ChestESP, so you don't have to worry about version conflicts.

- Added automated testing (in both Fabric and NeoForge versions) to make sure ChestESP keeps working correctly. Every time ChestESP changes or is ported to a new Minecraft version, GitHub Actions will run the mod and take screenshots of chests with various settings. While I still do manual testing too, I can't possibly check every type of chest in every Minecraft version with every ChestESP setting, so this is a huge help.

- You can view the automated test results in the [Actions tab](https://github.com/Wurst-Imperium/ChestESP/actions) of ChestESP's GitHub repo (if you're logged into a GitHub account). You can also run this test on your own computer by adding `-Dchestesp.e2eTest` to your JVM arguments (the results will appear in your screenshots folder, not on GitHub).
