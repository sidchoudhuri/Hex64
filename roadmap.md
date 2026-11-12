# Hex64 roadmap

| Status | Item |
|---|---|
| TO DO | Self-playing demo on the disk (menu key D), like the C64 Circuits demo |
| TO DO | C64 puzzle disk: Hex64, C64Doku and C64Sweeper on one disk, same loader framework |
| MAYBE | Use "Hexed Glide" (subtune 2) in the game: `POKE 36871,1` before `SYS 36864` |
| MAYBE | Tune the goal per board (`NC=4` clears' worth of points, game line 110) |
| IMPLEMENTED | v4: a finishing stack pulls every matching chip from its neighbours (no 8 limit while clearing) and scores them all; board ARCH renamed GEM; character set moved to $3800 and loader background to $C000 so the game no longer runs out of memory |
| IMPLEMENTED | v3: hex stacks with sliding and clearing, multicolour character set, 5 boards and a hard second run |
| IMPLEMENTED | v3: loader with animated honeycomb menu, SID detection, one or two SIDs, PAL/NTSC, music "Hexed" |
