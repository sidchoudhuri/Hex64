# Hex64 devlog

## v6 - 2026-11-13

**Fruit**
- Every board has fruit on fixed hexes: Flower 1, Ring 2, Gem 3, Wings 4, Honeycomb 5 (apple, strawberry, banana). A fruit hex can't be played on.
- Every clear next to a fruit takes a bite: a cartoon chomp (teeth snapping shut twice) plays on the hex, then the fruit's next bitten stage appears. Apple 3 bites, strawberry 3, banana 4; in the harder runs strawberry 4 and banana 5. An eaten fruit leaves an empty hex.
- A board is finished when all its fruit is eaten and the goal is reached.
- A mini fruit bar under the board name shows each fruit left, at its bitten stage.
- Ring now has every hex except the centre, with its fruit on 9 and 11.
- Board 5, Full, is renamed Honeycomb.

**Scoring and difficulty**
- Clear target is 5 (was 6). Extra chips in a clear score double. Eating a fruit scores 2 x its bites x board x run; finishing a board scores 20 x board x run.
- Dealt stacks hold from 1 chip up to the board number. After each run you can play again, harder, as many times as you like: the smallest stack grows (2, 2, 2, 3, 3, 4, 4, then 5) and the clear target goes 6, 7, then 8.
- The difficulty (Normal, Hard, Hard 2...), the clear target and the deal size show between STACK and NEXT.
- The stack under the cursor is shown big on the right: thick bars with gaps between chips, so the colors are easy to tell apart. It updates when the cursor rests.

**Retry**
- When a board fills up ("FULL! R RETRY N NEW Q MENU"), R plays the same board again with the score you had when it started. N starts a new game from board 1, Q goes to the menu.

**Sound**
- Softer, fuller sound effects: each one fades in, holds at a gentle level and fades out slowly, so they can be heard at normal volume. New sound when a fruit is eaten.
- Starting volumes: music 2/5 and sound effects 5/5 with two SIDs, 3/5 with one SID.

**Test tool**
- `HEX64TEST` on the disk, not in the menu (`LOAD"HEX64TEST",8` and `RUN`): start the game or the demo at any board (1-5) and run (Normal, Hard, Hard 2...), play every sound effect, play subtune 1 or 2, and view the fruit, chomp, icons and the whole character set. Q in the game or demo goes back to the test tool.

**Text and font**
- New Hex64 font, drawn for the game: capitals, digits and symbols, plus 26 lowercase letters. All the text is in mixed case.
- Lowercase letters live in characters 129-154 and are printed with reverse on, so the board graphics keep their characters. Reverse space is now blank; the volume notches use character 157.
- Control codes are typed inline in the strings instead of CHR$ where the text was rewritten.
- The instructions are rewritten for v6, with a chip stack and the three fruit drawn next to their names.

**Memory**
- Loader arrays `PH%` and `PA%` are integer now.
- The game and demo now load at $4001 with the top of memory at $9000 (about 20 KB), instead of $0801 to $3800. The loader sets this before loading them.

**Tested (VICE)**
- Menu, instructions, credits, SID setup and the game screen.
- The demo gets past Flower and plays Ring, eating fruit.


## v5 - 2026-11-12

**Demo mode**
- New program `HEX64DEMO`, started with D from the menu: the game plays itself.
- The demo player picks the empty hex with the most matching chips around it, walks the cursor there one step at a time, and places the stack.
- Same game every time (fixed seed 64), so it can be recorded. With that seed it clears all 5 boards, then shows the result for 3 seconds and starts again. If the board ever fills, it does the same.
- `+` and `-` change the speed (1 to 5, starting at 3). The volume keys work as in the game. Q returns to the menu at any time, including during the pauses.
- The demo plays the same music as the game ("Hexed"); when the game starts switching tunes, the demo will follow.

**Game and demo screen**
- The score line, the board name/message line and the key line are centered across all 40 columns.
- "BOARD COMPLETE" is now "COMPLETE", and it shows on the board you just finished while the chime plays; the next board starts with the message cleared.

**Other**
- Loader menu: new line `D - DEMO`; S and Q moved down one row.
- Title, instructions, credits and disk ID are V5 / 05.
- `HEXED.SID` (PAL, both subtunes: "Hexed" and "Hexed Glide") is on the disk.
- Volume is shown as 5 notches, like PETSCII Pit: a block for each notch that is on, a checkerboard for each one that is off (game, demo and SID setup). The checkerboard is a new character, 124, in the character set.
- Instructions screen: keywords highlighted in white over the green text.
- Thicker hex outlines: 2-pixel diagonals; sides are 1 pixel where two hexes touch (2 together) and 2 pixels on outer edges (new characters 125 and 126), so every edge looks even.
- Demo: after all 5 boards it shows the same "ALL 5 BOARDS COMPLETE!" screen as the game, with the score, for 3 seconds, then starts again.

**Tested (VICE)**
- Seed 64 clears all 5 boards (fast mode, about 75 seconds).
- Menu, D, the demo running on board 2, `-` changing the speed, and Q back to the menu.
- "COMPLETE" shows on the finished Flower board and is gone when Ring starts.

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
