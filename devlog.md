# Hex64 devlog

## v4 - 2026-11-12

**Gameplay**
- A finishing stack pulls every matching chip. When a stack lands, its top run plus the matching top runs of all its neighbours are counted. If that reaches the clear count (6, or 8 in the hard run), it pulls all of them and clears the whole run. The 8-chip limit is lifted only at that moment; otherwise a hex still holds at most 8 chips.
- Every chip cleared scores (chips x level, x2 in the hard run), so a big finishing pull can score more than 8 at once.
- While a pile is briefly over 8, it shows its top 8 chips.
- The third board, ARCH, is now called GEM (it never looked like an arch).

**Memory**
- The game was running out of memory (`?OUT OF MEMORY` on board 2 in a long autoplay test): the program ended at $266E and BASIC's top was $3000, leaving about 2.4 KB for variables, arrays and strings.
- The character set moved from $3000 to $3800 (file `HEX64CHARS`), and the loader background and its draw routine moved to $C000 (file `HEX64BG`, `SYS 51200`). They replace `HEX64DATA`.
- All 10 game arrays are now integer arrays (`AD%`, `Q%`, `HO%`, `HX%`, `HY%`, `IQ%`, `RW%`, `RS%`, `RN%`, `PB%`): 2 bytes per element instead of 5, about 900 bytes saved.
- Result: the arrays end at $2B80, leaving about 3.2 KB for strings below $3800 (about 2.3 KB with the character set move alone).

**Other**
- Title, instructions, credits and disk ID are V4 / 04.

**Tested (VICE)**
- Scripted board: a stack of 2 dropped next to matching runs of 4, 3 and 3 pulled all 12, scored 12, and left the neighbour's other chip.
- 10 minutes of random autoplay: 10 games, 48 clears (4 of them over 8 chips), no errors.
- Booting the disk: menu, background, animation and music work at the new addresses.

## v3 - 2026-11-10

**Move to own repo**
- The game was moved from the C64-BASIC repo to its own repo

**Game rewrite**
- Each hex holds a stack of up to 8 chips in 3 colors. Stacks are dealt to you; you place them on empty hexes.
- Matching top colors slide onto the stack you placed, and chains continue through the neighbours. 6 of one color on top clear and score.
- 5 boards: FLOWER, RING, ARCH, WINGS, FULL. Dealt stacks grow from 1 chip on board 1 to 5 on board 5.
- After board 5 you can play all 5 again in a hard run: every board deals 5, and 8 of a color clear.
- Multicolour character set: piles drawn as stacked chips, hex outlines from custom characters, cursor highlight.
- Cursor keys or WASD to move, SPACE to place.

**Framework (same as C64 Circuits)**
- Loader with a calm, animated honeycomb menu: piles slowly gain and lose chips.
- SID detection (second SID at $D420), one or two SIDs, PAL/NTSC, settings page at $9F00, SID setup screen, volume keys (M/E with two SIDs, V with one).
- The game chains from and back to the loader (Q returns to the menu).

**Music and sound**
- Music player at $9000 with the Circuits entry points. Song "Hexed" (subtune 1, used in the game) and "Hexed Glide" (subtune 2, slower, with glissandos). Voices 1-2 only; the same tempo on PAL and NTSC.
- Soft sound effects on voice 3 (of the second SID when there are two): tap, plop, swish, chimes.

**Disk**
- `hex64.d64`: loader first, a hex drawn in DEL lines, then the game, music and data files.
