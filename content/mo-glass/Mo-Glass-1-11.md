---
title: Mo Glass 1.11 - More Tests and Fixes
description: Update 1.11 makes the Mo Glass mod more reliable by adding many 
  automated tests and fixing bugs that these tests uncovered.
date: 2025-03-08T13:16:00+01:00
image: 
  https://images.wurstclient.net/_media/update/mo-glass/mo_glass_1.11_540p.webp
mod: mo-glass
modversion: "1.11"
mcversions:
- 1.21.8
- 1.21.7
- 1.21.6
- 1.21.5
- 1.21.4
snapshots:
- 25w33a
- 25w32a
- 25w31a
- 1.21.8-rc1
- 1.21.7-rc2
- 1.21.7-rc1
- 1.21.6-rc1
- 1.21.6-pre4
- 1.21.6-pre3
- 1.21.6-pre2
- 1.21.6-pre1
- 25w21a
- 25w20a
- 25w19a
- 25w18a
- 25w17a
- 25w16a
- 25w15a
- 25w14craftmine
- 1.21.5-rc2
- 1.21.5-rc1
- 1.21.5-pre3
- 1.21.5-pre2
- 1.21.5-pre1
- 25w10a
fabric:
- 1.21.8
- 1.21.7
- 1.21.6
- 1.21.5
- 1.21.4
---
## Changelog

- Added a test that checks if the names of Mo Glass's items show up correctly. (An unreleased build of Mo Glass for 24w45a had a bug where you would see the raw translation keys instead.)

- Added a test that checks if all of Mo Glass's crafting and stonecutting recipes work. (Mo Glass 1.8 had a bug where all recipes stopped working in Minecraft 1.20.5/6.)

- Added a test that checks thousands of different combinations of glass blocks, stairs, and slabs to make sure they all connect properly to each other.

- Added a test that checks if the tinted glass slabs and stairs correctly block light depending on their orientation. (An unreleased build of Mo Glass for 24w33a had a bug where they stopped blocking light.)

- Added a test that checks if all of the glass slabs and stairs drop the correct items when mined with and without silk touch.

- Fixed a bug where non-tinted glass slabs would not connect to inner curved stairs of the same type, if those stairs were 90° rotated relative to the slab and either the slab was a double slab or the stairs were upside down relative to the slab. Confusing, I know, but just check the example screenshots and it will make sense: [example 1](https://github.com/user-attachments/assets/7224a67c-e178-46c2-aa66-b0914428e388), [example 2](https://github.com/user-attachments/assets/3591e4d7-db4a-48a3-a2f1-d0bf857d2db2), [example 3](https://github.com/user-attachments/assets/f4725620-3280-4532-8a68-f40feecc3284)

- Fixed a bug where there would be a hole in the side of inner curved glass stairs when placed next to another glass stair in certain orientations. ([example 1](https://github.com/user-attachments/assets/12228a4e-f6aa-48bd-966d-2a95d9b08f64), [example 2](https://github.com/user-attachments/assets/c9e7ebae-1c20-4758-a8f9-f252b98eae4f))

- Fixed a bug where inner curved glass stairs would have a hole in their front side if you used a debug stick to make them curve towards something that they normally couldn't. ([example 1](https://github.com/user-attachments/assets/da85770d-92e1-44b7-985b-ffb575136c98), [example 2](https://github.com/user-attachments/assets/0439eee6-e8ad-4138-ba88-a007e5de62ad), [example 3](https://github.com/user-attachments/assets/22b313e0-6384-42de-8f97-089505b66779))

- Fixed various scenarios in which outer curved glass stairs would not connect to other glass stairs correctly. ([example 1](https://github.com/user-attachments/assets/3166d9ee-d2ea-4177-8bee-e8d5c08a4a8e), [example 2](https://github.com/user-attachments/assets/7d07332b-7273-4351-bc42-bcd6ab5c9602), [example 3](https://github.com/user-attachments/assets/245a2f3a-905d-4cc7-a3bb-f749acc606da), [example 4](https://github.com/user-attachments/assets/65a69f49-f59e-4e3d-b2bd-0524c5639cc7), [example 5](https://github.com/user-attachments/assets/2022f192-433b-48e5-ab08-172303e6bf5a), [example 6](https://github.com/user-attachments/assets/2bb50e8f-7a04-4f7a-beac-317ba6d92d81))

- Fixed a bug in the loot tables causing non-tinted glass slabs and stairs to drop as items when being mined without silk touch. (Only tinted glass is supposed to do this.)

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
  - Japanese (Japan)
  - Oshiwambo (Oshindonga)
  - Oshiwambo (Oshikwanyama)
  - Portuguese (Brazil)
  - Russian (Russia)
  - Spanish (Argentina)
  - Spanish (Chile)
  - Spanish (Ecuador)
  - Spanish (Spain)
  - Spanish (Mexico)
  - Spanish (Uruguay)
  - Spanish (Venezuela)
</details>
