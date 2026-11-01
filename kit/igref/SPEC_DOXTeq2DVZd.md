# SPEC DOXTeq2DVZd (60.87s, 1080x1920, 60fps)

Measured from frames (10fps overall, 30fps at every bar hit, HP hit, pickup, death and the win), pixel runs on frame 0, flood-area timeline at 5fps (fl_dox.txt), square tracking with spd.py. Coordinates are reference px.

## Layout
- Green-checker background, board = flat green (0,152,0) wall mass with black outline, x 45-1035, y 270-1640. Floor (open cells) = cream (253,246,214).
- Four horizontal start lanes, x 80-603, each 96 tall: y 974-1071, 1140-1235, 1305-1401, 1470-1565 (dividers 66 tall). Square colours top to bottom: green, yellow, red, blue, each starting at the lane's left end.
- The right part of the lanes (x 478-603) is a vertical column split by thin coloured breakable bars (126 wide, 62 tall, 3 stripe bands):
  - green bar = floor of lane 1, yellow bar = floor of lane 2, red bar = floor of lane 3 (lane 4 floor is solid),
  - blue bar = ceiling of the column at y 908-970 (between the column and the corridor above). Everyone needs blue to reach the top.
- Corridor: top corridor y 844-905 from x 476 to 735, right column x 674-735 down to y 1565, bottom corridor y 1504-1565 from x 674 to 986.
- Funnel shaft going up at the right: x 886-972 (1.8 squares wide) y 1380-1504, x 899-960 (1.27) y 1126-1380, x 912-946 (0.7) y 844-1126, then a thin drawn line (8px) y 442-844 into the top-right subroom. Squares travel it single file (it is drawn narrower than a square; motion inside is purely vertical).
- Top-right subroom x 804-999, y 315-442. Big grey bevelled HP block (number 66) x ~420-800, y ~355-780, between the subroom and the left part of the top room.
- Top room left part x 226-407, y 315-706; the sword lies horizontally at x ~240-400, y ~500 pointing right at the block.
- Exit: bright green block x 80-192, y 466-558 with a checkered strip on its right edge, set into the left wall of the top room at mid height.
- After the block breaks the top room is one L-shaped room x 226-999, y 315-706 (right-bottom corner x 804-999 below y 442 stays wall).

## Squares
- 4 squares, flat colour with black outline, ~48px (46 + outline). Short tapered trail in own colour. No faces in this one.
- Speed constant ~300 px/s (measured vx 210, vy 220: launches at ~45 deg). All four start with the identical velocity in identical lanes, so they move in lockstep until the bars make them differ.
- Bounce: straight lines, reflect on contact with walls, bars, the block, the flood and each other. Squares collide with each other (stacking and bouncing seen in the column and the shaft).

## Flood (orange 248,104,0)
- Starts at t~0.1 at the left ends of all four lanes; vertical fronts advance right in all lanes together at ~33 px/s (x 80 -> 442 by 11s, reach the column ~11.5-12s).
- Then the column fills from the bottom up (lanes 1-3 stop at the column edge; only the bottom lane feeds the column) at ~67 px/s; top reached ~21s.
- Top corridor and right column ~140 px/s (21-31s), bottom corridor 31-33s, funnel and line ~66 px/s (33-47s), short hold at the top of the line (44-48s) while the squares hit the block, subroom 49-56s, then the main room after the block breaks at ~80 px/s right-to-left as a full-height vertical front (56s on).
- Continuous fronts (not cell by cell). Solid for squares: they bounce off its front. The flood never kills anyone in this reel; squares get packed tight above it in the column (16-19s) and the shaft but always had room.

## Kills (measured on both deaths)
- Neither death is the flood. Both are the sword:
  - 53.42 green touches the lying sword: it is picked up and carried (drawn diagonally above green, moving with it) for ~1.05s.
  - 54.47 blue collides with green (the holder): blue vanishes in a burst of small orange-brown squares (~0.4s). The sword drops and lies horizontally at the hit spot (top-left of the room).
  - 58.8 green touches it again, picks it up; 59.1 it collides with yellow: yellow bursts, the sword drops again.
- Rule: touching the lying sword = pick it up; the holder's next contact with another square kills that square; the sword then lies at that spot and can be picked up again. No crush deaths.

## Breakable bars (colour gates)
- 3 HP each (3 stripe bands, each hit removes one band, ~19-20px).
- Only the matching colour damages its bar; others bounce off it (blue bar untouched 9-19s while green/yellow/red were packed against it; first chip at 19.0 when blue arrived).
- Times: first hits 2.2s (green, red, yellow simultaneously, lockstep), green and red bars gone ~8.0s, yellow ~8.2s, blue chipped 19.0, broken ~19.4 -> squares escape into the corridor.

## HP block (66)
- Counts down by exactly 1 per contact (66->65 at 44.10, 65->64 44.53, 64->63 45.06, 63->62 45.63, then faster as the four rattle in the small subroom: 55 at 47, 47 at 48, 37 at 49, 30 at 50, 16 at 51). Any colour damages it.
- At 0 (~51.9s) the block disappears and the room opens.

## Exit
- 59.15 red touches the exit: red sits inside the green exit block, text "RED WON" (red, black outline, ~26px tall) appears just above-left of the exit (x ~50-215, y ~430). The game keeps running (green keeps bouncing, the flood keeps coming) until the end.

## On-screen text
- None at the start (no hook, no countdown; squares move from frame 0). Only "RED WON" at 59.2 to the end.

## Ending, audio, length
- Ends at 60.87s, 1.7s after the win, mid-motion.
- Audio: no music bed detected; per-contact blips through the run, louder dense hits during the block countdown (45-52s, peaks -7 dBFS), silence fading at the end.

## Recreation notes (Code Name)
- Guides: lanes top to bottom in roster order Joy, Cleo, Cyrus, Rayleigh; the bottom guide (Rayleigh) owns the ceiling bar, the others own their lane floors.
- Flood = the shadow (dark purple). Sword -> creatine gummy (STRENGTH!), same pick-up / knock-out-on-next-contact / drops-at-spot rule.
- Funnel tapers to exactly one box wide (honest single file instead of the drawn-thinner line). Vertical proportions compressed to fit the board between the hook and the roster (y ~466-1394).
- Hook (coordinator): soft dark fade, job hook WHO BREAKS / THROUGH FIRST?. Win: the box becomes Syeda's victory pose at the exit, "NAME WON" text as in the reference, game keeps running, hold ~2.5s.
