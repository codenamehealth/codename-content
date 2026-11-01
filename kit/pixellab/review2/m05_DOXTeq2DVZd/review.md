Build review: m05_DOXTeq2DVZd (61.7s)

Verdict: FIX FIRST (three quick fixes, no re-layout). Fidelity 7/10.

✅ Keep doing
• Structure is a faithful copy: 4 lanes in lockstep from frame 0, own-colour floor bars plus Rayleigh's ceiling bar, corridor, single-file funnel, top-right subroom, 66 block counting 1 per hit, gummy in the exit room, pick up / KO next touch / drops at the hit spot, shadow never kills, game keeps running after the win.
• Hook has motion under it from frame 0 (trails visible by 0.13s). Gate breaks are colour-correct (4.93 green/blue/orange together, 14.83 purple by Rayleigh). Both KOs are real touches (53.33 Joy on Cleo, 56.43 Cyrus on Joy).
• Last 10s is open: four alive at 52.0, Joy 8px off the exit at 53.13, Rayleigh near the exit ~57.0, Cyrus wins 58.7. Not obvious.
• Audio: I -15.2 LUFS, TP -2.3 dBTP. Pass.

❌ Fix
• 53.97-54.10: Cyrus's carried gummy (~80px, drawn up-right of his box) overlaps Rayleigh's box and nothing happens. Reads as a hit that didn't count. → Draw the carried gummy ~28px, centered on top of the holder's box (inside his footprint).
• 0-58s: trails are box-wide smoothed S-ribbons ~250px long. In the lanes they read as boxes snaking, not bouncing (client complaint: bounce, not steered), and they swamp the column (8-14s) and room (51-58s). → Short tapered trail (~3 box lengths) with hard corners at each bounce, like the reference.
• 35-50s: block-hit SFX estimated ~20 dB under the music; the reference's loudest stretch is this countdown. → Raise block-hit SFX 8-10 dB or duck music 6 dB from 35.6 to 50.3.
• 58.7-61.7: hook stays up over "CYRUS WON", and the dim card hides Rayleigh still running (spec: pose at exit, game keeps running). → Hide the hook at 58.7; drop the dim, keep the big CYRUS WON and pose.
• 30-34s and 24-30s: funnel climb (x 905-975) and bottom corridor (y 1480-1540) sit under the IG right rail and caption zone. → Accept for fidelity, or shift roster right and funnel left ~60px.

🎯 Priority order
1. Shrink and center the carried gummy
2. Bounce trails with hard corners
3. Block-hit SFX up during the countdown
4. Hook off and no dim at the win
5. Funnel/bottom corridor vs IG UI (optional)

Target length: 61s, payoff at 58.7s (matches reference; keep).

Minor: 35.6-39.5 is the slowest stretch (66 to 60 in 4s, single file). First hit lands 8.5s earlier than the reference, so the countdown runs 14.7s vs 7.8s. Not dead (a hit every ~0.6s); acceptable since the run itself can differ. Joy's KO burst at 56.43 sits on the hook band's top fade.

## Appendix: beat table (reel vs reference)

| Beat | Reference | m05 | Status |
|---|---|---|---|
| Motion from frame 0, lockstep start | 0.0 | 0.0 | match |
| Hook | none | WHO BREAKS THROUGH FIRST? 0-61.7 | changed (intended) |
| Roster | none | right wall x 756-884, X on KO | changed (intended) |
| Own-colour floor bars break | 8.0 / 8.2 | 4.93 (all three) | match, earlier |
| Wait in column for bottom box's ceiling bar | 8-19.4 | 5-14.8 | match |
| Ceiling bar breaks | 19.4 | 14.83 (Rayleigh) | match |
| Corridor / right column / bottom corridor | 19-33 | 15-30 | match (continuous motion, no hits) |
| Funnel single file | 33-44 | 30-35.5 | match, shorter |
| Block first hit | 44.1 | 35.6 | changed (8.5s earlier) |
| Countdown length | 7.8s | 14.7s | changed (slower start) |
| Block breaks | 51.9 | 50.3 | match |
| Pickup 1 / KO 1 | 53.42 / 54.47 (1.05s carry) | 53.23 / 53.33 (0.1s carry) | match rule, much faster |
| Pickup 2 / KO 2 | 58.8 / 59.1 | 53.93 / 56.43 (2.5s carry) | match rule |
| Win | 59.15, small text, game runs | 58.7 small text, 59.2 dim card + big pose | changed |
| End | 60.87 mid-motion | 61.7 | match |

No dead stretch over 3s with zero state change: 15-35s has constant box motion and the shadow advancing; it has no discrete events (20.8s between Rayleigh's bar and the first block hit vs 24.7s in the reference).

Physics: no teleports, wall clipping or unprovoked direction changes seen at 2fps overall and 15fps around 0-1s, 4.3-5.7, 14.3-15.7, 49.8-51.1, 52.9-54.6, 56.0-57.0, 58.3-59.9. Near-misses: carried gummy over Rayleigh 53.97-54.10 (fix 1); Joy 8px from the exit strip at 53.13 while overlapping the opening's height (keep, it is tension, but a phone shows ~3px).

Legibility: board x 40-1040, y 250-1610; faces 50px read by border and trail colour on a phone, faces themselves are small. Hook on the wall band y ~700-830 covers no key action except the funnel passing behind it 31-34s. STRENGTH stamps sit under the hook at y ~830-880, clear of the action. Block number is the main readout during the 15s subroom stretch and reads well.

Audio: AAC mono 44.1k, I -15.2 LUFS (target -15 +-0.3), LRA 3.9, TP -2.3 dBTP. Bounce ticks ~10/s at roughly -30 dB RMS under the music: audible, not grating. Event SFX (block break 50.3, KOs, win) sit near music level. SFX levels are estimated by subtracting the HeartBIT stem (heartbit__m05.wav, 0.97 correlation).

Brand: guide faces only, gummy pickup, STRENGTH (not STRONG), no hashtags, no em dashes, hook is not a choose-a-guide line. Music HeartBIT as intended.

Comparison sheets: _cmp/sbs_1fps_01-07.jpg, dense_*.jpg, zoom_54.jpg, lip_strip.jpg, stamp_joy.jpg.
