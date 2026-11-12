# Hex64 roadmap

Status: **DONE**, **TO DO**, **TO DO LATER**, **MAYBE**.

## Hex64

| Status | Item |
|---|---|
| DONE | v3: stacks of 3 colors, slide and clear, 5 boards, dealt stacks growing from 1 to 5 chips, hard second run (deal 5, clear 8) |
| DONE | v3: multicolour character set, hex outlines, piles, cursor highlight; CRSR/WASD and SPACE |
| DONE | v3: loader with animated honeycomb menu, SID detection, one or two SIDs, PAL/NTSC, SID setup, volume keys |
| DONE | v3: music "Hexed" (in game) and "Hexed Glide" as 2 subtunes; soft sound effects on voice 3 |
| DONE | v3: `hex64.d64` with directory art; .sid files for PAL and NTSC |
| DONE | v4: a finishing stack pulls every matching chip from its neighbours (8-chip limit lifted only while clearing) and scores every chip |
| DONE | v4: board ARCH renamed GEM |
| DONE | v4: memory: character set at $3800, loader background at $C000, all game arrays integer (`%`) |
| TO DO | Self-playing demo on the disk (menu key D), like the C64 Circuits demo |
| TO DO | Show you a mockup of the directory art (built without one in v3) |
| TO DO | Test on real hardware, including two SIDs and NTSC (only tested in VICE so far, one SID, PAL) |
| TO DO | Make the build scripts in `tools/` portable (they still use paths from the build machine) |
| TO DO LATER | Thicker edges on the hex tiles |
| TO DO LATER | When the cursor is on a hex, show what is in it somewhere, or in big graphics, since piles are sometimes hard to read |
| TO DO LATER | High-contrast version for accessibility |
| TO DO LATER | Music changes from "Hexed" to "Hexed Glide" on game events |
| TO DO LATER | Better sound effects: go through every game event, decide where a sound is needed, and make every effect very calming (ASMR) |
| MAYBE | Tune the goal per board (`NC=4` clears' worth of points, game line 110) |
| MAYBE | Integer arrays in the loader too (`PH`, `PA`; small saving) |

## C64 puzzle disk (Hex64, C64Doku, C64Sweeper)

| Status | Item |
|---|---|
| TO DO | One disk with all three games, using the same loader framework (SID detection, settings, music) |
| TO DO | Disk name and directory art for the puzzle disk |
| TO DO | C64Doku: remove the stray ```` ```basic ```` line at the top of `c64doku.bas` on GitHub; split line 1020 (over 80 characters) |
| TO DO | C64Doku and C64Sweeper: Q returns to the menu instead of ending the program; volume keys like Hex64 |
| TO DO | C64Sweeper: WASD as well as cursor keys; play again or menu after a win or loss |
| MAYBE | C64Doku: solver check so every puzzle has exactly one solution (generation would be slower) |
| MAYBE | Calm music for C64Doku and C64Sweeper, or one tune across the disk |
