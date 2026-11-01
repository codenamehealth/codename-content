# SPEC DaG5nn5v8AP ("Choose a Square", 54.27s, 1080x1920 60fps, no audio track)
Measured from 10fps frames + 30/60fps around every break, pickup, kill and the win.

## Layout (grid unit u = 51.26px, origin x0=53, y0=396; 19 cols x 22 rows; bg/walls tan, floor light grey, 4px black outlines)
- Start chambers (4): cols 4-5, 7-8, 10-11, 13-14, rows 0-6. Boxes start top-right of each chamber: yellow, cyan, green, red.
- Gaps between chambers: cols 6, 9, 12 and 15. Rows 0-3 are wall; rows 4-6 are brick gates: green (6), cyan (9), red (12), yellow (15, opens to the right room).
  Each gate is 3 bricks tall. Boxes chip them brick by brick; the chambers merge into one hall (rows 4-6) as the gates go.
- Right room: cols 16-18, rows 4-10. Dark brick D1 at col 15, rows 8-10, opens to corridor A.
- Corridor A: rows 8-10, cols 0-14 (westward). Left column: cols 0-2, rows 8-14. Dark brick D2 at col 3, rows 12-14.
- Corridor B: rows 12-14, cols 4-18 (eastward). Right column: cols 16-18, rows 12-18.
- Corridor C: rows 16-18, cols 4-18 (westward). Dark brick D3 at col 3, rows 16-18.
- Left room: cols 0-2, rows 16-21. The sword sits here at (col 1.5, row 17.5).
- Corridor D: rows 20-21, cols 0-15 (eastward). Dark exit brick D4 at col 16, rows 20-21. Checkered exit: cols 17-18, rows 20-21.
- Text: "Choose a Square" (white, about 70px) at y 1550-1610 and a 4-colour bar at y 1630-1705, static the whole video.

## Boxes
- 26px squares (about 0.5u), black outline, flat colour, comet trail about 4-5 box lengths.
- Constant speed of about 330 px/s (about 6.4u/s), ALWAYS on 45-degree diagonals (measured angles of +-45 and +-135 throughout).
- Reflect off walls and bricks (flip one component). Box-box contact is a bounce (flip on the contact axis). No steering.
- At t=0.2s all four start moving down-left in sync. They desync only through gate hits and box contacts.

## Bricks
- Coloured gates and dark bricks both break by being hit. Each brick cell crumbles in chunks (measured: D2 lost material on 3 consecutive hits, 22.4 to 23.3s).
- Break times: red gate about 2.5s, cyan about 4.5s, green about 10.5s, yellow 15-16s; D1 about 17.5s; D2 23.3s; D3 about 33s; D4 about 48.5s.
- An intact brick blocks both boxes and the flood (no case observed where the flood reached an intact brick).

## Flood (purple, solid, flat front perpendicular to the corridor, continuous, follows the path)
Measured front times (s):
| Segment | Fill direction | Start | End |
|---|---|---|---|
| Chamber tops, rows 0-3 | down | 0.3 | 10.4 (about 20px/s) |
| Hall, rows 4-6, cols 4-15 | left to right | 10.4 | 23.7 (about 46px/s) |
| Right room | down | 24.1 | 27.0 (about 122px/s) |
| A | right to left | 26.4 | 32.7 (about 150px/s) |
| Left column | down | 33 | 35.0 |
| B | left to right | 35.3 | 40.7 |
| Right column | down | 41.5 | 43.0 |
| C | right to left | 42.4 | 47.9 |
| Left room | down | 48.1 | 50.9 |
| D | left to right | 50.5 | to the end, about 130px/s |
The flood is slow while the boxes are still penned in, then roughly 4x faster in the corridors.

## KILL RULES (every death measured)
- This reel has 2 deaths, both from the SWORD: green at 36.9s and cyan at 37.7s. The sword-holder (yellow) touched them; the victim instantly freezes, gets a black X and stays as a static obstacle until the flood covers it.
- The flood never killed anyone here. The boxes stayed ahead of it.
- The CRUSH rule, measured in DZqJLrcvXpQ at 29.0-30.2s: the flood is a solid moving wall that PUSHES a box. The box rides on the front, and it dies (X) only when the front pins it against a wall and there is no room left (red, at 30.15s, X'd exactly when squeezed flush against the top wall). Touching the flood alone does not kill.

## Sword (pickup)
- Yellow touched it at 34.2s. The sword icon then rides on the box for the rest of the video.
- Holder: a box it touches is killed (X), and it appears to break D4 in one hit.

## Exit and ending
- D4 broken about 48.5s. Red (no sword) entered the checker at 53.27s and won; yellow (sword) was right behind.
- Everything freezes the moment the winner enters the checker. Hold of about 1.0s, then the video ends at 54.27. No winner text, no card.
- Audio: none in the downloaded file.

## Our recreation (m01)
- Same grid and rules. Our guides in roster order Joy, Cleo, Cyrus, Rayleigh. The gummy (STRENGTH, kills on touch, breaks a brick in 1 hit) replaces the sword.
- Hook: job hook in the soft top fade ("WHO ESCAPES THE SHADOW?"). Our roster replaces the colour bar. Shadow flood. Sand floor, slate walls. New Epidemic track.
- Brand tweaks: the payoff holds about 2.5s with the winner's victory pose; the STRENGTH stamp names the guide.
