---
title: Mo Glass 1.6 - Tinted Glass, Bugfixes
date: 2021-12-15T18:13:00+01:00
image: https://images.wurstclient.net/_media/update/mo-glass/mo_glass_1.6_540p.webp
mod: mo-glass
modversion: "1.6"
mcversions:
- "1.18.1"
- "1.18"
- "1.17.1"
fabric:
- "1.18.1"
- "1.18"
- "1.17.1"
---
## Changelog

- Added tinted glass slabs and stairs.

- Slightly modified the lighting engine to make tinted glass slabs and stairs possible.

- Added Italian (Italy) translations. (Thanks to <a href="https://github.com/XfedeX" target="_blank" rel="noopener noreferrer">XfedeX</a>!)

- Added French (France) translations. (Thanks to <a href="https://github.com/HanatakeYurii" target="_blank" rel="noopener noreferrer">HanatakeYurii</a>!)

- Added various common item tags that other mods can use in their crafting recipes to specify what kind of glass they want.

- Added a `mo_glass:glass_slabs` block tag containing all glass slabs and a `mo_glass:glass_stairs` block tag containing all glass stairs. This should be useful for vertical slabs mods.

- Added a `mo_glass:opaque_for_lighting` block tag for blocks that need my lighting engine modification to render properly. This should be useful for mods that change how lighting works.

- Reduced the file size of Mo Glass. (Thanks to <a href="https://github.com/RDKRACZ" target="_blank" rel="noopener noreferrer">RDKRACZ</a>!)

- Fixed glass stairs facing each other's front sides not being seamless. (<a href="https://user-images.githubusercontent.com/10100202/146294359-378351a4-9b1f-488d-9b4a-bba1309ac3fe.png" target="_blank" rel="noopener noreferrer">before</a>/<a href="https://user-images.githubusercontent.com/10100202/146294361-02af55ef-6998-46a3-a3c3-f5096caef95d.png" target="_blank" rel="noopener noreferrer">after</a>)

- Fixed glass stairs and glass slabs dripping when placed under a liquid (unlike vanilla glass blocks).

- Fixed glass stairs and glass slabs blocking the camera in 3rd person view (unlike vanilla glass blocks).

- Fixed glass slabs not being included in the `minecraft:slabs` tags.

- Fixed glass stairs not being included in the `minecraft:stairs` tags.

- Removed support for old Fabric Loader versions without the <a href="https://wurst.wiki/log4shell" target="_blank" rel="noopener noreferrer">Log4Shell</a> patch (older than v0.12.10).

## Features

- Glass Slabs
- Glass Stairs
- Stained Glass Slabs
- Stained Glass Stairs
- Tinted Glass Slabs
- Tinted Glass Stairs
- Working Transparency
- Working Translucency

## Crafting Recipes

<details>
  <summary>Glass Slab: (click to expand)</summary>
  
  ![glass slab crafting recipe](https://user-images.githubusercontent.com/10100202/69957444-5a2ddc80-150b-11ea-8c8c-e2afc5d72fb7.png)  
  ![glass slab stonecutter recipe](https://user-images.githubusercontent.com/10100202/70445670-2a974b00-1a9c-11ea-9a09-46c304cd167b.png)
</details>

<details>
  <summary>Glass Stairs: (click to expand)</summary>
  
  ![glass stairs crafting recipe](https://user-images.githubusercontent.com/10100202/69957446-5bf7a000-150b-11ea-8e61-d189de63333d.png)  
  ![glass stairs stonecutter recipe](https://user-images.githubusercontent.com/10100202/70445677-2c610e80-1a9c-11ea-8e1b-108863b47124.png)
</details>

## Translations

<details>
  <summary>Supported Languages: (click to expand)</summary>

  - Chinese (Simplified/Mainland)
  - Chinese (Traditional/Taiwan)
  - English (US)
  - French (France)
  - German (Germany)
  - Italian (Italy)
  - Oshiwambo (Oshindonga)
  - Oshiwambo (Oshikwanyama)
  - Russian (Russia)
  - Spanish (Argentina)
  - Spanish (Chile)
  - Spanish (Ecuador)
  - Spanish (Spain)
  - Spanish (Mexico)
  - Spanish (Uruguay)
  - Spanish (Venezuela)
</details>
