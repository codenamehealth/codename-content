Build review: r01_DerujF_BHAA (37.1s, reference 37.43s)

✅ Keep doing
• Course, order and camera match the reference within about 0.3s per section (pills, long pills, ropes, pads, domes and pillars, bars, breather, hill, downhill, finish at 33.85 vs 33.75).
• Sabotage block lands on the reference beats: slime on Rayleigh's head 4.75, knock-off 5.62 (ref 5.77), jumps to Cyrus 5.9, Rayleigh back from the left 8.7 (ref 8.6).
• Rope gag (13.45 to 15.3) is a clean 1:1 copy: slip, lands flat on lane 3, Rayleigh walks over her, springs back.
• Hook WHO MAKES IT ACROSS FIRST? is a real question with no pick-a-guide wording. Strip style is approved, text sits at y 266 to 388, inside the safe zone.
• Audio: -15.0 LUFS, -1.8 dBTP, opens on the drop (first 0.5s at -14.2 dB mean). SFX onsets line up with each gag (5.6, 13.6, 15.1, 22.8, 32.4, 34.1).

❌ Fix
• 5.9 to 7.5 and 29.2 to 32.7: Cyrus's "panic" pose (arms straight up, calm face) reads as cheering. On the hill crest it looks like he is winning. In the reference, the axolotl screaming is the joke both times. → Re-render a PixelLab panic pose from Syeda's Cyrus files (hands on head or flailing, wide eyes, no teeth) and add a 2 to 3px shake for the stuck time.
• 19.3 to 22.65: four guides hang in the same pose for about 3.3s with no event. That makes 15.3 to 22.65 a 7.3s gap with no gag (the reference has a gap of 5.8s, then the penguin puff gag at 21.6). → From 21.6 to 22.6, show Cleo losing her grip (one-hand hang, slipping) so her drop is set up.
• 23.0 to 23.35: Cleo climbs out of the water by herself. The reference rescue (the penguin hauls the octopus out at 23.2 to 23.5) is gone. → Have Rayleigh reach down from the pad and pull Cleo up by the hand. The gag stays, and it builds sympathy for the winner.
• Whole reel: the guides are about 190px tall and about 90px wide, while the reference runners are 180 to 290px tall and about 240px wide. Ours carry roughly a third of the visual mass and read small on a phone. → Scale the sprites up by the largest integer-clean step the 267px lanes allow. For sure, scale the 34.3 to 37.1 winner card (Rayleigh is about 200px in an empty dock) to 2x.
• 27.5 to 30.7: the reference has its runners crawl on the climbing holds and climb together. Ours walk up at normal run speed. → Use a slower climb cycle on the hill. Optional: Rayleigh and Cleo climb as a pair.

🎯 Priority order
1. Cyrus panic pose (both sabotage payoffs depend on it)
2. Bars dead stretch: Cleo grip-slip at 21.6
3. Rayleigh pulls Cleo out at 23.2
4. Sprite scale, winner card first
5. Hill climb speed

Target length: 37s, payoff at 33.9s. Keep these as they are, because they match the reference by design.

---

## Detail

### Beat table (reference vs r01)

| Beat | Reference | r01 | Status |
|---|---|---|---|
| Opening text | "choose your runner!" 0-2.33 | Strip WHO MAKES IT ACROSS FIRST? 0-25.6, fades by 26.0 | Changed. Helps: it asks a question and is not a pick-a-guide line. |
| Countdown 3/2/1/GO | 0.1 / 0.7 / 1.4 / 1.9 | 0.1 / 0.7 / 1.4 / 1.9 | Match |
| Camera starts | 2.4-2.5 | 2.4 | Match |
| Interferer travels in | duck flies lane 2, 2.6-4.6 | slime hops along lane 3, 3.0-4.5 | Match (hops; no flying, good) |
| Pecking on target | duck over penguin 4.7-5.75 | slime on Rayleigh's head 4.75-5.6 (two bounces) | Match |
| Target knocked into water | 5.77 | 5.62, splash 5.84, sinks/swims | Match |
| Second victim | duck grabs axolotl 6.2, wrestle, both drift off 8.6-8.9 | slime on Cyrus's head 5.9, Cyrus stands arms up, off-screen about 7.6 | Changed. Hurts: static pose reads as celebrating, and there is no struggle |
| Victim 1 returns | penguin from left 8.6, level by 9.0 | Rayleigh from left 8.7, level by 9.3 | Match |
| Victim 2 returns | axolotl 10.6 | Cyrus 10.6 (per build log; in front on ropes by 11) | Match |
| Long pills / pads / ropes | 9.0 / 10.0 / 10.6-14.4 | 9.0 / 10.0 / 10.6-14.4 | Match |
| Rope slip gag | axolotl slips 13.65, flat on lane 3, penguin walks over 14.4-14.6, springs up 15.3-15.8 | Joy slips 13.45, flat on lane 3 13.98, Rayleigh steps over about 14.5, springs back 15.3 | Match (gag moved to Joy, fine) |
| Domes + pillars | 16.3-19.3 | 16.3-19.3 | Match |
| Monkey bars gag 1 | penguin puffs up 21.6-22.6 | nothing, all hang still | Missing. Hurts (dead time) |
| Bar drop | octopus drops 22.6 | Cleo lets go 22.65, splash | Match |
| Rescue | penguin's legs pull octopus out 23.2-23.5 | Cleo climbs out alone onto pad 23.35 | Missing. Hurts |
| Breather | 23.6-26.3 | 23.6-26.3 | Match |
| Interferer returns | duck flies in 27.8, lands on axolotl's head 29.3 | slime hops in 27.75 (low hops on lane-1 pills), lands on Cyrus 29.3 | Match on timing; payoff weakened by the pose (see above) |
| Climb | crawling on holds, penguin hangs on octopus | normal run up a smooth hill | Changed. Slight hurt |
| Crest + tumble | 30.7, tumble 30.8-32 | 30.7, Rayleigh and Cleo tumble | Match |
| Splash-out | octopus rolls into water 32.06 | Cleo into water 32.2, swims (head above water) | Match |
| Winner crosses | 33.75-33.85 | 33.85 | Match |
| WINNER! + pose | 34.1, happy pose 34.4, hold to 37.43 (3.3s) | 34.1, victory pose 34.32, hold to 37.1 (3.0s) | Match (0.3s shorter hold; fine) |
| Length | 37.43 | 37.1 | Match |

Lead changes (from the build log, confirmed in frames): Rayleigh 2.6, Cyrus 3.2, Cleo 6.0, Cyrus 12.3, Rayleigh 22.8, Cleo 26.4, Rayleigh 32.5. That is about the same count as the reference, with an underdog winner who was the first sabotage victim, as in the reference.

### Brand checks
- Characters: Syeda guide sprites plus PixelLab jump and hang derivatives from her files (log: 9 gens). No AI-redrawn characters and no teeth seen in the zoomed frames. Hollow absent (fine).
- Physics: nobody stands on water. The slime only hops ballistically, landing on pills or heads. Swimmers sit on their waterline with the body masked. Rayleigh sinks rather than floating at 5.9. Cleo swims with her head up at 23.0 and 32.8, so she does not read as drowned. The 34.1 to 34.32 swap from lying to the victory pose is a snap, as in the reference.
- Winner: the WINNER! text is clear. The pose is a modest fist and staff raise and small (see fix 4).
- Safe zone: the hook strip runs y 252 to 408, text 266 to 388 (OK, 16px clear of the top line). Lane 4 action reaches about y 1500, right on the bottom 420px line. The layout is the same as the reference, so this is acceptable. At 29 to 32.7 the slime on Cyrus's head sits at y about 280 to 360, just inside the top line. WINNER! is at about x 45 to 615, y 515 to 600 (OK).
- Text: no hashtags, no em dashes. The hook is not CHOOSE A GUIDE.
- Audio: -15.0 LUFS integrated (target -15 ±0.3), true peak -1.8 dBTP (≤ -1.5), energy in the first 0.5s. Music per the build log is Epidemic "Slam Dunk" by FLYIN (track identity not verified by ear).

### Rubric scores
1. Hook: 7/10. The question is better than the reference. The first 2.4s is still a static dock with a countdown, the same as the reference. Optional minor tweak: let the slime peek in at the dock edge during the countdown, so viewers get a "watch the slime" job before GO.
2. Dead time: 15.3 to 22.65 (7.3s with no gag) is the only real gap. See fixes 2 and 3.
3. Payoff: 33.9 of 37.1s (91%), the same as the reference by design. Do not shorten.
4. Legibility: text is fine. Characters are on the small side.
5. Stamps: countdown and WINNER! only, as in the reference. The hook fade at 25.6 to 26.0 lands in the breather, so it does not cost momentum.
6. Ending: a 3.0s hold with sparkle only, as in the reference. Keep it (no cutting the end).
7. Comment trigger: the hook question works as one. Match the caption CTA to it.
8. Gummy powers: none in this reel (N/A).

Fidelity to the reference: 8/10. Every structural beat and the timing are there. The losses are two comedy beats (puff, rescue) and the scream readability.
Quality vs the reference: slightly below until fixes 1 to 3 are in, then roughly on par.

Client-reject risks: Cyrus looking like he is celebrating at the crest (people will read it as a weird pose or a wrong winner tease), and characters reading small on a phone (a stated rule).

Comparison images: _cmp/cmp_sheet_01..07.jpg (1fps, reference left, r01 right), dense tiles _cmp/o_sab, o_ret, o_rope, o_bars, o_hill, o_fin, o_slime1, o_slime2.jpg, zooms _cmp/o_zoom.png, _cmp/o_t295_top.png, _cmp/o_t355_end.png.
