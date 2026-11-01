Build review: r01_DerujF_BHAA pass 2 (37.1s, reference 37.43s)

✅ Keep doing
• Course, camera and beat timing still match the reference within about 0.3s. Finish at 33.9, WINNER! at 34.0, pose at 34.3, held to 37.1.
• Scale-up landed. Guides are about 250px in 258px lanes, the reference runners are 180 to 220px, and nothing goes into the bottom 20% (the band ends at y 1480) or past x 950, apart from one staff sparkle at 34.5. The winner card is 2x: Rayleigh is about 507px tall, and WINNER! (x 64 to 699, y 513 to 639) reads at thumbnail size.
• The Cyrus panic now reads as distress, not cheering. It is front facing with hands on head and a closed frowning mouth, with no teeth (6.0, 7.0, 29.5 to 30.5). Facing the camera is correct here, because the reference axolotl turns to camera to scream.
• The Cleo grip-slip works. She hangs one-handed from 21.6 to 22.6, with an SFX at 21.75, and the bars no longer feel dead.
• Audio: -15.2 LUFS, -1.8 dBTP. SFX are clearly above the bed on the slip (+25 dB high band), the drop (22.7), the slime landing (29.55) and the win (34.25).

❌ Fix
• 5.9 to 7.6: the bigger sprites push the slime on Cyrus's head (y 300 to 400) behind the hook strip (y 250 to 408). The second sabotage payoff is a dark blob under "ACROSS". The bar tops and Cyrus's hands also touch the strip from 19.3 to 23. → Fade the strip out between 5.4 and 5.7. The reference drops its text at 2.33, and the hook has been read by 5.5.
• 22.87 to 23.6, rescue: Rayleigh kneels and reaches from 23.0 to 23.27, which works. But at 23.33 Cleo snaps from prone to standing, upright on open water left of the pad with ripples at her feet, until 23.47. From 23.47 to 23.6 her sprite slides through Rayleigh's, fully overlapped. It reads as "she pops up and passes through him", not as a pull. → Re-render a PixelLab "pulled up by the hand" frame pair. Keep their hands joined, mask her below the waterline until she clears it, and land her on the pad about 120px left of him, with no overlap. Add a small lift SFX at about 23.35 (none is audible there now).
• 22.73 to 22.93: Cleo drops in a standing pose, touches the water upright for one frame, then snaps prone. → Use a fall pose and splash on entry.
• 22.93 to 23.27 and 32.4 to 33.4: Cleo's prone swim shows her whole body lying on the surface. → Mask below the waterline, as pass 1 had.
• Minor: WINNER! fill starts at x 64 (safe line 70). Nudge it right by 10px.

🎯 Priority order
1. Hook strip fade before 5.8 (slime gag hidden)
2. Rescue re-render (standing on water, sprite overlap, snap)
3. Fall entry pose plus swim mask
4. WINNER! nudge

Target length: 37s, payoff at 33.9s (unchanged, matches the reference).

---

## Pass-1 fixes
1. Cyrus panic: landed (yes). The 2 to 3px shake could not be checked in stills, because the camera is scrolling.
2. Bars dead stretch: landed (yes).
3. Rayleigh pulls Cleo out: partial (no). The kneel and reach landed, but the pull-out is a snap plus an overlap.
4. Scale-up and 2x winner card: landed (yes).
5. Slower climb: mostly (yes). The cadence is slower and the crest is at about 30.5 (reference 30.7), but it is still a walk, not a crawl on holds. Occasional hop frames lift the feet 20 to 40px off the slope (around 30.0). This is minor.

## New checks
- Timing: no new dead time. The gap from the rope gag to the slip is 15.3 to 21.6 (6.3s, reference 5.8s).
- Lead changes: still readable. Rayleigh leaves the lead to rescue at 22.8 and the camera stays on Joy and Cyrus.
- Rayleigh leaves the bar at 22.8, before Cleo's splash at 22.9. That is fine, but a 0.1 to 0.2s later start would read as a reaction.
- Brand: Syeda and PixelLab-derived sprites only. No teeth or open mouth on Cyrus. On-screen text is only the hook and WINNER!, with no hashtags and no em dashes.

Fidelity: 8/10. It was 8 at pass 1: the scale, Cyrus and slip gains are offset by the hidden slime beat and the rescue physics.

Sheets: s1fps_01..04.jpg (1fps, reference left, ours right), d05_10_01.jpg, d19_24_01.jpg, d27_35_01.jpg (dense), safezone_sheet.jpg (red = IG safe lines, cyan = 80% height / 88% width), rescue_zoom.jpg, rescue_dense.jpg (15fps, 22.6 to 23.73), cyrus_zoom.jpg, hill_zoom.jpg, climb_dense.jpg.
