# SPEC DSFjv2viBWJ ("Built in Ball Chaos for iOS" maze, 58.96s, 1080x1920 60fps, no audio track)
Measured from 10fps frames, 60fps around the start, plus per-cell probes for the flood, the bricks and the pistons.

## Layout (u = 69.57px, origin x0=53, y0=333; 14 cols x 18 rows; tan walls/background, light grey floor, black outlines)
- Start chambers (one box each, bottom-left corner, all moving up-right at t=0.1): cols 0-1, 3-4, 6-7, 9-10, rows 12-17. Boxes: yellow, green, blue, red.
- Gates (3 bricks tall, rows 12-14): col 2 green, col 5 yellow, col 8 blue, col 11 red. Rows 15-17 of those columns are wall.
- Right room: cols 12-13, rows 9-14. Corridor rows 9-10, cols 0-13. Row 11 is wall (cols 0-11). Left column col 0, rows 0-10. Top corridor rows 0-1. Right column col 13, rows 0-7.
- Inner block (rows 2-8 framed by wall): checkered exit cols 2-3 rows 3-4, with a dark exit brick at cols 2-3 row 5. Room row 6-7, cols 2-5 | dark brick col 6 | cols 7-9 | dark brick col 10 | cols 11-13 (open to the right column).
- Two L-rooms: col 6 rows 3-4 + col 7 rows 3-5 (purple pickup at row 3 col 7), and col 10 rows 3-4 + col 11 rows 3-5 (purple pickup at row 3 col 11). Each opens down into the room row.
- Text: "Built in Ball Chaos for iOS" (watermark, y ~1700). No title, no roster.

## Boxes
- 53px squares (46px fill plus outline) with two eyes. Constant ~340 px/s (about 4.9u/s), always on 45-degree diagonals. They reflect off walls, bricks, pistons and each other. No steering.

## Pistons (dark slabs, solid, triangle-wave motion, 2 cells wide, stroke = the full 2-row corridor height of 136-139px)
- P1: cols 6-7, rises from the inner wall top (y=472) up into the top corridor. Period 5.4s, starts at 0 extension at t=0, full at 2.7s, back to 0 at 5.4s.
- P2: cols 1-2, drops from the row-8 wall (y=959) down into corridor rows 9-10. Period 12.6s, 0 at t=0, full at 6.3s.
- P3: cols 10-11, drops into corridor rows 9-10. Period 12.6s, 0 at 6.3s, full at 12.6s.
- At full stroke a piston closes its corridor completely.

## Flood (purple, solid, flat fronts; per half-cell arrival times measured and stored in wk_m02/flood_m02.json)
| Region | Movement | Time (s) |
|---|---|---|
| Chambers, rows 15-17 | rises | 0-5 |
| Hall rows 12-14 | sweeps left to right | 8-15 |
| Right room | rises | 16-20 |
| Corridor rows 9-10 | right to left | 20-37 |
| Left column | up | 33-42 |
| Top corridor | left to right | 42-50 |
| Right column | down | 50-53 |
| Room row 6-7 | right to left | 54-58 |
- It never reaches the L-rooms or the exit.

## KILL RULE (measured)
- 1 death: yellow at ~30.9s. It was pushed left by the flood front (corridor rows 9-10, about col 3) into the side of piston P2, which was near full stroke. It was crushed between the flood and the piston and got an X.
- Pistons and the flood are both solid movers. A box dies only when one pins it against something solid. Nobody died from touching.

## Bricks (break times, from cell probes)
- Gates: col 2 ~1.4s, col 8 ~1.0-1.7s, col 11 ~1.0-1.7s, col 5 ~3.9-5.6s.
- Dark bricks: (6,10) 23.5s, (7,10) ~40s, (7,6) ~41s, (6,6) ~53s, exit (5,2-3) ~58s (blue).

## Pickup (purple square)
- On touch, the box grows to about 2x size and keeps it.
- Red took the right one at ~24.5s and is then too big to leave the L-room. Green took the left one at ~57.4s and got stuck the same way.

## Ending
- Blue breaks the exit brick and enters the checker at 58.4s. The video ends 0.55s later (58.96s). No card, no text.

## Our recreation (m02)
- Same grid, placement, pistons, flood (replayed per half-cell), bricks and rules.
- Our 4 guides as 52px face boxes (24px face crop at 2x).
- The pickup is a STRENGTH gummy that makes the guide grow 2x (stamp "NAME: STRENGTH!").
- Roster cards sit in the two wall blocks inside the inner area (cols 4-5 and 8-9, rows 3-5). They are on the board, out of the caption zone and the right 12%.
- Job hook in the soft top fade. Brand winner card for 2.5s after the win.
