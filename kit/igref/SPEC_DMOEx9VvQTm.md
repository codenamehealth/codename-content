# SPEC DMOEx9VvQTm (72.1s, 1080x1920, 30fps)

Measured from frames (1fps overall, 5fps phases, 30fps at both deaths and the final 0.3s), pixel runs on frame 0, water-area timeline (fl_dmoe.txt).

## Layout
- Red checker background, board x 40-1043, y ~230-1500: solid red wall mass, pale cyan floor. Watermark @simulando2d and the creator logo under the board (not copied).
- A staircase corridor climbing from bottom-left to top-right, narrowing as it climbs:
  - left (upper) wall steps: x 44 (y 1424-1500), 182 (1232-1400), 322 (1040-1208), 462 (848-1016), 602 (680-824), 742 (488-656), 882 (296-464). ~140 px across, ~176-192 up per step.
  - right (lower) step blocks: x 488 (y 1328-1460), 579 (1160-1304), 671 (992-1136), 763 (800-968), 854 (632-776), 946 (464-608), board edge 1035 (296-440). ~92 across per step.
  - corridor width ~400 at the bottom down to 153 at the top room.
- Top room x 882-1035, y 296-464 (~4 squares wide). Exit: a one-square slot in the top-right corner of its ceiling (x ~995-1043, y 262-296, checkered) leading to a green exit block x 982-1041, y 200-261.
- Pencils (hazards, not pickups): one under each right step block, lying in a slot on the step below, tip pointing left at the step's inner corner, eraser cap at the right wall. Body 14px tall, lengths 466, 374, 282, 190, 98 px (each 92 shorter going up). Eraser caps cycle colours (decoration only).
- No pickups exist in this reel. The crossed X boxes that appear on the steps are death markers.

## Squares
- 4 squares, 36px, flat colour (red, blue, yellow, green), black outline, trail. Start in a row at the bottom-left (red, blue, yellow, green touching), launch ~0.1s up-right; red, blue and yellow share a velocity and move as a cluster for the first seconds, green apart.
- Speed constant ~277 px/s (7.6 squares/s). Bounce off walls, steps, pencil bodies, the water surface and each other. They wander up and down the stairs (blue reaches the top at 19s, comes back down 21-23s).

## Water (dark blue 0,64,140)
- Starts ~0.3s at the floor, flat surface rising at a nearly constant ~16 px/s (area rate falls as the corridor narrows): lowest pencil covered by ~2s, top room entered ~60s, surface just under the exit corner at the end. Continuous, not cell by cell.
- Drawn over pencils (they vanish under it); death markers stay drawn on top. Solid for squares (they bounce off the surface). It kills no one in the reference.

## Kills (measured)
- Yellow 9.17s: touches the tip of the step-3 pencil -> freezes in place as an X-crossed box (stays as a marker).
- Green 13.15s: touches the tip of the step-2 pencil -> X marker.
- Rule: touching a pencil tip kills (body is a surface). Water never kills here (would only by crushing in the top room, which never happens on screen).

## Exit and ending
- Red and blue reach the top room by ~33s and bounce there for ~39s; the water enters the room ~60s and shrinks it. Blue enters the exit slot at ~71.9-72.0 and the video cuts at 72.1 with no win text (cliffhanger cut).
- On-screen text: none (watermark only).
- Audio: no music bed; hit blips, louder events at deaths.

## Recreation notes (Code Name)
- Water stays water (blue), squares -> guide face boxes, pencils kept as the hazards (no weapon pickup to swap; nothing invented). Board compressed vertically to y ~466-1394, boxes ~40px.
- Coordinator's ending: winner enters the slot, Syeda victory pose replaces the box, hold ~2.5s (adds ~2.5s to the 72s).
- Hook (coordinator): WHO OUTRUNS / THE WATER?
