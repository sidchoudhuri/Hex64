# Hex64

A calm hex-stacking puzzle for the Commodore 64, written in BASIC V2 with a small machine language music player.

https://m0nde.itch.io/hex64

## How to play

Drop stacks of colored chips onto a board of hexes. When a stack lands, neighboring hexes whose top color matches slide those chips onto it. Get 6 chips of one color on top and they clear and score. A hex holds up to 8 chips; a stack that is about to clear can pull every matching chip from around it and scores them all.

Reach the goal to finish a board. There are 5 boards: Flower, Ring, Gem, Wings and Full. The stacks you are dealt grow from 1 chip on the first board to 5 on the last. Finish all 5 and you can play them again in a hard run, where every stack has 5 chips and 8 of a color clear. A full board ends the game.

## Keys

| Key | Action |
|---|---|
| Cursor keys or W/A/S/D | Move between hexes |
| SPACE | Place your stack |
| V | Volume (one SID) |
| M / E | Music / sound effects volume (two SIDs) |
| Q | Back to the menu |

Menu: P play, I instructions, C credits, S SID setup, Q quit.

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
| `hex64.d64` | The disk: loader, game, music, character set, menu background |
| `src/hex64-loader.bas` | Loader and menu (BASIC V2) |
| `src/hex64-game.bas` | The game (BASIC V2) |
| `src/hex64-music.asm` | Music player and tunes at $9000 (ACME) |
| `src/hex64-bg.asm` | Menu background routine at $C800 (ACME) |
| `prg/` | Built music, character set and background files |
| `sid/` | "Hexed" .sid files |
| `devlog.md`, `roadmap.md` | What changed, and what's next |

BASIC listings are tokenized with petcat (part of VICE): `petcat -w2 -o game.prg -- hex64-game.bas`.

## Credits and license

Design, code, graphics and music by m0nde.

(C)2026 m0nde. Licensed under CC BY-NC-SA 4.0: see [LICENSE](LICENSE).
