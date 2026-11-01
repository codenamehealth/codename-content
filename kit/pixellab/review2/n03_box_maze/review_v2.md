Build review: n03_box_maze (22.53s)
Verdict: FIX FIRST

✅ Keep doing
• Countdown, GO, passive bouncing and the colored wall breaks (2.0 to 3.8s) match the reference and read cleanly.
• Gummy pickup is synced: Cyrus touches it at 5.07s, "CYRUS: STRENGTH!" lands at 5.13s.
• Physics are mostly clean: no wall clipping at the breaks, box contacts at 10.67s are edge-to-edge, no teleports or jitter at 15fps.
• Winner pose replaces the box (19.93s), only one Cyrus on screen. Card holds 2.6s.

❌ Fix
• 18.45 to 19.93s: Cyrus is through the exit at 18.5s but the win fires 1.4s later. Meanwhile his box sits on top of the coin pile, and Ray also gets through (18.9s) and rubs into the dragon (19.1 to 19.3s). "First through" doesn't read, and boxes overlap the scenery. → Fire the win the frame Cyrus crosses the exit line, freeze everyone else, and make the dragon and hoard solid.
• 7.53s: Joy's OUT is a phantom catch. The shadow is a 4px strip at the top edge with a visible gap above her box. → Only call OUT once the shadow visibly overlaps the box.
• Whole reel: this isn't a maze. The reference is a winding corridor maze where the shadow chases boxes down the path. This is an open room with two shelves, so the shadow turns into a flat diagonal wedge (16 to 19.5s). → Rebuild with winding corridors that fill the frame.
• Whole reel: the exit, dragon and finish (y 1455 to 1710) sit in the bottom 420px caption zone, so the exit break and the win play under the caption. → Move the exit up to mid-maze on the right like the reference, above y 1450.
• Whole reel: the dragon sits on a pile of gold coins and gems. It reads as a gold hoard. → Swap it for a gummy pile.
• Whole reel: the grey and white checker floor looks like a transparent-PNG placeholder, and with the black and white finish the whole frame is checkerboard. Not clearly better than the reference's sand tiles. → Use a real low-contrast floor tile.
• 7.53 to 8.2s and 12.13 to 12.6s: two stamps per elimination (a banner plus an OUT tag). The reference uses the OUT tag only. At 12.13s the OUT tag runs off the right edge. → One stamp per catch, kept inside the maze.

🎯 Priority order
1. Win timing and exit overlap (18.45 to 19.93s)
2. Phantom catch (7.53s)
3. Real corridor maze
4. Exit out of the caption zone
5. Coin hoard to gummies
6. Floor tile
7. One stamp per catch
Minor: lane order (Cleo, Ray, Joy, Cyrus) doesn't match the HUD (Joy, Cleo, Cyrus, Ray), where the reference matched. HUD says RAY, the reference says RAYLEIGH. The thin amber maze border reads as gold framing. STRENGTH is only a red glow, so add an impact flash when Cyrus smashes the exit. Soft lull from 8.3 to 12.0s.
Target length: 21.5s, payoff at 18.6s, hold 3s
