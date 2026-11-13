# Hex64

A calm hex-stacking puzzle for the Commodore 64, written in BASIC V2 with a small machine language music player.

https://m0nde.itch.io/hex64

## How to play

Drop stacks of colored chips onto a board of hexes. When a stack lands, neighboring hexes whose top color matches slide those chips onto it. Get 5 chips of one color on top and they clear and score; extra chips in a clear score double. A hex holds up to 8 chips; a stack that is about to clear can pull every matching chip from around it and scores them all.

Fruit sits on some hexes and blocks them. Every clear next to a fruit takes a bite out of it: an apple takes 3 bites, a strawberry 3 and a banana 4. To finish a board, eat all the fruit and reach the goal. There are 5 boards: Flower, Ring, Gem, Wings and Full. The stacks you are dealt hold from 1 chip up to the board number. Finish all 5 and you can play them again, harder: bigger stacks, more chips to clear (6, then 7, then 8), and tougher strawberries and bananas, run after run. A full board ends the game.

## Keys

| Key | Action |
|---|---|
| Cursor keys or W/A/S/D | Move between hexes |
| SPACE | Place your stack |
| V | Volume (one SID) |
| M / E | Music / sound effects volume (two SIDs) |
| Q | Back to the menu |

Menu: P play, I instructions, C credits, D demo, S SID setup, Q quit.

In the demo the game plays itself: `+` and `-` change the speed, Q returns to the menu.

## Running it

Load `hex64.d64` on a real C64, an Ultimate 64 or VICE:

```
LOAD"*",8
RUN
```

The loader detects one or two SIDs (the second at $D420) and PAL or NTSC. With two SIDs, the music plays on the first and the sound effects on the second.

## Music

"Hexed" by m0nde plays in the menu and the game. `sid/` has it as .sid files for PAL and NTSC, with "Hexed Glide", a slower version with glissandos, as subtune 2.

## Files

| Path | What it is |
|---|---|
| `hex64.d64` | The disk: loader, game, demo, music, character set, menu background, and `HEXED.SID` (both subtunes) |
| `src/hex64-loader.bas` | Loader and menu (BASIC V2) |
| `src/hex64-game.bas` | The game (BASIC V2) |
| `src/hex64-demo.bas` | The self-playing demo (BASIC V2) |
| `src/hex64-test.bas` | Test tool, not in the menu: `LOAD"HEX64TEST",8` and `RUN`. Start the game or demo at any board and run, play every sound effect, play the music subtunes, and view the fruit, chomp, icons and the whole character set |
| `src/hex64-music.asm` | Music player and tunes at $9000 (ACME) |
| `src/hex64-bg.asm` | Menu background routine at $C800 (ACME) |
| `font/hex64-font.bin` | The Hex64 font: 64 characters (capitals, digits, symbols) followed by 26 lowercase letters, 8 bytes each; `hex64-font.png` shows it |
| `prg/` | Built music, character set and background files |
| `sid/` | "Hexed" .sid files |
| `devlog.md`, `roadmap.md` | What changed, and what's next |

BASIC listings are tokenized with petcat (part of VICE): `petcat -w2 -o game.prg -- hex64-game.bas`.

## Credits and license

Design, code, graphics, font and music by m0nde.

(C)2026 m0nde. Licensed under CC BY-NC-SA 4.0: see [LICENSE](LICENSE). This covers everything in the repo, including the Hex64 font.
