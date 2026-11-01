# Music credits audit, Metricool Oct 29 6:00pm to Nov 9 11:59pm ET

Read-only audit, run Oct 29 2026. Brand Code Name Main (blogId 7178389), America/New_York. Drafts skipped. Every batch_v3 slot has the same three non-draft posts (FB+IG, TikTok, YouTube) and the same caption credit on all three.

How the track was found: the latest batch_v3/log.txt line that ran mix.py names the wav; when the latest line says the audio was reused (mux/mux2), the track comes from the reel's batch_review/log.txt entry. Where the earlier (pre-restart) run of this audit had already fingerprinted a file (S/maudit/fp_*.log), the score is shown; every fingerprint agreed with the logs. No new fingerprinting of batch_v3 files was done.

## Summary

- **One caption needs a change: #047 Motivation vs discipline (Nov 6 8:00pm), all three posts (FB+IG, TikTok, YouTube). Remove the line "Music: Start the Day by Lee Rosevere, CC BY 4.0".** The current 047 file is mixed on the Adobe Stock track joypad_arcade (log lines 164 and 190), which needs no credit.
- No other batch_v3 reel in the window has a music line, and none needs one: every track used anywhere in the batch, batch_v2, batch_review, batch_final and batch_v3 logs is from S/music_adobe. No CC BY track (the FMA mp3s in /home/claude/tl/music) appears in any reel log.
- The noon "take 2" animation posts are not batch_v3 reels; their credits are checked separately below.

## batch_v3 reels

| slot (ET) | reel | networks | caption credit now | actual track in current file | license | needed caption change |
|---|---|---|---|---|---|---|
| Oct 29 6:00pm | 006_find_3_differences_in_10_seconds_or_youre_an_npc.mp4 | FB+IG, TikTok, YouTube | none | arcade_game_loop.wav (title not recorded) [audio reused (log 114); batch_review r6 arcade_game_loop; fp 0.96] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none |
| Oct 29 8:00pm | 007_day_1_vs_day_365.mp4 | FB+IG, TikTok, YouTube | none | Magical Action Adventure (loop version) (AdobeStock_1536842484) [mux2 reuse (log 125); batch_review r7; fp 0.74] | Adobe Stock (no credit needed) | none |
| Oct 30 10:00am | 014_watch_carefully.mp4 | FB+IG, TikTok, YouTube | none | Adventure Epic Game (AdobeStock_481021343) [mux reuse (log 87); batch_review r14 @4s; fp 0.91] | Adobe Stock (no credit needed) | none |
| Oct 30 6:00pm | 051_pick_your_marble_cleo_or_cyrus.mp4 | FB+IG, TikTok, YouTube | none | Arcade Loop (AdobeStock_1536841857) [log 191 mix.py arcade_loop2; fp 0.91] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Oct 30 8:00pm | 012_2_xp_zero_potions_left.mp4 | FB+IG, TikTok, YouTube | none | Orchestral Fantasy (AdobeStock_495722646) [mux reuse (log 21); batch_review r12 @18s; fp 0.83] | Adobe Stock (no credit needed) | none |
| Oct 31 10:00am | 016_iq_test.mp4 | FB+IG, TikTok, YouTube | none | Cheerful Lighthearted Pop Rock glockenspiel loop (AdobeStock_1536841906) [mux reuse (log 10); batch_review r16; fp 0.93] | Adobe Stock (no credit needed) | none |
| Oct 31 4:00pm | 018_think_you_can_nail_it_only_01_can.mp4 | FB+IG, TikTok, YouTube | none | adventure loop (AdobeStock_526744215) [mux reuse (log 1); fp 0.94 (no named track in logs)] | Adobe Stock (no credit needed) | none |
| Oct 31 6:00pm | 058_pick_your_marble.mp4 | FB+IG, TikTok, YouTube | none | energetic.wav (title not recorded) [log 173 mix.py energetic@12; fp 0.97] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none; Metricool has an older render (flag 1) |
| Oct 31 8:00pm | 017_play_along_with_the_beat.mp4 | FB+IG, TikTok, YouTube | none | Back To The 80s (Loop) (AdobeStock_526743454) [mux2 reuse (log 118); batch_review r17 @1.8s; fp 0.72] | Adobe Stock (no credit needed) | none |
| Nov 1 10:00am | 025_only_1_can_find_this_hollow.mp4 | FB+IG, TikTok, YouTube | none | digital_mushrooms.wav (title not recorded) [mux2 reuse (log 158); batch_review digital_mushrooms@20; fp 0.99] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none |
| Nov 1 4:00pm | 021_pause_and_match_all_4_to_reveal_your_guild.mp4 | FB+IG, TikTok, YouTube | none | Space Game Arcade Loop (AdobeStock_513023888) [mux reuse (log 7); batch_review r21; fp 1.00] | Adobe Stock (no credit needed) | none |
| Nov 1 6:00pm | 064_each_ball_has_only_4_seconds_to_escape.mp4 | FB+IG, TikTok, YouTube | none | digital_mushrooms.wav (title not recorded) [log 200 mix.py digital_mushrooms@0] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none; Metricool has an older render (flag 1) |
| Nov 1 8:00pm | 023_rank_the_guides.mp4 | FB+IG, TikTok, YouTube | none | Cheerful Lighthearted Pop Rock glockenspiel loop (AdobeStock_1536841906) [mux2 reuse (log 156); batch_review r23; fp 0.88] | Adobe Stock (no credit needed) | none |
| Nov 2 10:00am | 034_find_the_gummy.mp4 | FB+IG, TikTok, YouTube | none | 8-bit Arcade - World Made Of Platforms - Loop (AdobeStock_676139665) [mux reuse (log 32); batch_review r34 / batch_v2 remix] | Adobe Stock (no credit needed) | none |
| Nov 2 4:00pm | 026_put_the_gummy_in_the_bottle.mp4 | FB+IG, TikTok, YouTube | none | Magical Action Adventure (loop version) (AdobeStock_1536842484) [mux reuse (log 34); batch_review r26; fp 0.99] | Adobe Stock (no credit needed) | none |
| Nov 2 6:00pm | 077_musical_chairs.mp4 | FB+IG, TikTok, YouTube | none | adventure loop (AdobeStock_526744215) [mux2 reuse, gated music (log 75); batch_review r77 / batch_v2 remix] | Adobe Stock (no credit needed) | none |
| Nov 2 8:00pm | 027_1_xp_a_day.mp4 | FB+IG, TikTok, YouTube | none | Adventure Island Loop (AdobeStock_513024170) [log 171/180 remix adventure_island@0] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 3 10:00am | 038_which_gummy_fits_the_outline.mp4 | FB+IG, TikTok, YouTube | none | Classic Retro Video Game Play (AdobeStock_1925597393) [mux reuse (log 44); batch_review r38 switched fantasy_adventure -> retro_game_play] | Adobe Stock (no credit needed) | none |
| Nov 3 4:00pm | 030_screenshot_the_second_the_gummy_fits_perfectly.mp4 | FB+IG, TikTok, YouTube | none | Casual Sweat On The Joypad - Arcade, Upbeat - Loop (AdobeStock_676139692) [mux reuse (log 22); batch_review r30; fp 0.93] | Adobe Stock (no credit needed) | none |
| Nov 3 6:00pm | 081_outrun_the_shadow.mp4 | FB+IG, TikTok, YouTube | none | Space Game Arcade Loop (AdobeStock_513023888) [log 184 mix.py space_arcade] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 3 8:00pm | 040_still_need_a_pass.mp4 | FB+IG, TikTok, YouTube | none | Symphonic Uplifting Fantasy Adventure (Short Loop 6) (AdobeStock_513024727) [mux reuse (log 28); batch_review r40] | Adobe Stock (no credit needed) | none |
| Nov 4 10:00am | 044_lock_your_eyes_on_the_glowing_gummy.mp4 | FB+IG, TikTok, YouTube | none | Classic Retro Video Game Play (AdobeStock_1925597393) [mux reuse (log 40); batch_review r44 switched back_to_80s -> retro_game_play] | Adobe Stock (no credit needed) | none |
| Nov 4 4:00pm | 036_pause_the_video_on_99.mp4 | FB+IG, TikTok, YouTube | none | energetic.wav (title not recorded) [log 199 remix energetic @11.995 (correlation 0.999)] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none; Metricool has an older render (flag 1) |
| Nov 4 8:00pm | 043_finally_made_it_to_a_save_point.mp4 | FB+IG, TikTok, YouTube | none | Adventure Island Loop (AdobeStock_513024170) [log 140 mix.py adventure_island; log 182 remixed (adventure_island)] | Adobe Stock (no credit needed) | none |
| Nov 5 10:00am | 049_find_the_odd_gummy_in_5_seconds.mp4 | FB+IG, TikTok, YouTube | none | arcade_game_loop.wav (title not recorded) [log 166 mix.py arcade_game_loop; log 176 loudness-only] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none |
| Nov 5 4:00pm | 042_pause_when_both_fit_perfectly.mp4 | FB+IG, TikTok, YouTube | none | Arcade Loop (AdobeStock_1536841857) [mux reuse (log 35); batch_review r42 same track arcade_loop2] | Adobe Stock (no credit needed) | none |
| Nov 5 6:00pm | 082_can_the_hollow_escape.mp4 | FB+IG, TikTok, YouTube | none | Back To The 80s (Loop) (AdobeStock_526743454) [log 183 mix.py back_to_80s] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 5 8:00pm | 045_which_guild_are_you.mp4 | FB+IG, TikTok, YouTube | none | Symphonic Uplifting Fantasy Adventure (Short Loop 6) (AdobeStock_513024727) [log 187 mix.py fantasy_adventure] | Adobe Stock (no credit needed) | none |
| Nov 6 10:00am | 057_how_many_hollows_do_you_see.mp4 | FB+IG, TikTok, YouTube | none | Classic Retro Video Game Play (AdobeStock_1925597393) [mux2 reuse (log 153); batch_review r57 retro_game_play kept] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 6 4:00pm | 075_think_you_can_nail_it_only_01_can.mp4 | FB+IG, TikTok, YouTube | none | Adventure Island Loop (AdobeStock_513024170) [mux2 reuse (log 73); batch_review r75 adventure_island kept] | Adobe Stock (no credit needed) | none |
| Nov 6 6:00pm | 085_arena_war.mp4 | FB+IG, TikTok, YouTube | none | digital_mushrooms.wav (title not recorded) [log 189 mix.py digital_mushrooms] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none; Metricool has an older render (flag 1) |
| Nov 6 8:00pm | 047_motivation_vs_discipline.mp4 | FB+IG, TikTok, YouTube | Music: Start the Day by Lee Rosevere, CC BY 4.0 | Casual Sweat On The Joypad - Arcade, Upbeat - Loop (AdobeStock_676139692) [log 164 mix.py joypad_arcade; log 190 remixed (joypad_arcade)] | Adobe Stock (no credit needed) | remove line; Metricool has an older render (flag 1) |
| Nov 7 10:00am | 060_only_1_difference.mp4 | FB+IG, TikTok, YouTube | none | digital_mushrooms.wav (title not recorded) [audio muxed unchanged (log 67); batch_review r60 digital_mushrooms@20 kept] | Adobe Stock, inferred (no licence record found locally; see flag 2) | none |
| Nov 7 4:00pm | 083_pause_when_it_perfectly_mirrors.mp4 | FB+IG, TikTok, YouTube | none | Space Game Arcade Loop (AdobeStock_513023888) [audio reused (log 94); batch_review r83 space_arcade kept] | Adobe Stock (no credit needed) | none |
| Nov 7 6:00pm | 100_first_to_the_top_wins.mp4 | FB+IG, TikTok, YouTube | none | Adventure Island Loop (AdobeStock_513024170) [log 150 reuses previous file track; batch_review r100 adventure_island kept] | Adobe Stock (no credit needed) | none |
| Nov 7 8:00pm | 090_slimes_eat_all_the_glass.mp4 | FB+IG, TikTok, YouTube | none | Cheerful Lighthearted Pop Rock glockenspiel loop (AdobeStock_1536841906) [log 202 mix.py glockenspiel_pop] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 8 10:00am | 062_which_gummy_makes_it_fall.mp4 | FB+IG, TikTok, YouTube | none | Orchestral Fantasy (AdobeStock_495722646) [log 186 mix.py orchestral_fantasy@40] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 8 4:00pm | 087_pause_when_all_3_gummies_fit.mp4 | FB+IG, TikTok, YouTube | none | Back To The 80s (Loop) (AdobeStock_526743454) [audio reused (log 98); batch_review r87 back_to_80s kept] | Adobe Stock (no credit needed) | none |
| Nov 8 6:00pm | 089_last_one_in_the_ring_wins.mp4 | FB+IG, TikTok, YouTube | none | Back To The 80s (Loop) (AdobeStock_526743454) [log 193 mix.py back_to_80s] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 8 8:00pm | 095_build_joys_perfect_charm.mp4 | FB+IG, TikTok, YouTube | none | adventure loop (AdobeStock_526744215) [mux2 reuse (log 84); batch_review r95 adventure_loop kept] | Adobe Stock (no credit needed) | none |
| Nov 9 10:00am | 066_which_gummy_fits_the_outline.mp4 | FB+IG, TikTok, YouTube | none | Symphonic Uplifting Fantasy Adventure (Short Loop 6) (AdobeStock_513024727) [log 206 remix fantasy_adventure@0] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 9 4:00pm | 096_choose_your_digger.mp4 | FB+IG, TikTok, YouTube | none | Arcade Loop (AdobeStock_1536841857) [mux2 reuse (log 85); batch_review r96 arcade_loop2 kept] | Adobe Stock (no credit needed) | none |
| Nov 9 6:00pm | 093_whoever_gets_3_gummies_wins_powers_on.mp4 | FB+IG, TikTok, YouTube | none | Arcade Loop (AdobeStock_1536841857) [log 208 mix.py arcade_loop2@3] | Adobe Stock (no credit needed) | none; Metricool has an older render (flag 1) |
| Nov 9 8:00pm | 072_watch_carefully.mp4 | FB+IG, TikTok, YouTube | none | Space Game Arcade Loop (AdobeStock_513023888) [mux2 reuse (log 71); batch_review r72 switched fantasy_adventure -> space_arcade] | Adobe Stock (no credit needed) | none |

## Non-batch_v3 video posts in the window (noon "take 2" animations)

These carry music credits. Their files are the Metricool media copies saved in S/maudit/t2 by the earlier run; no log names their tracks, so these 11 short files were fingerprinted against the 13 tracks in /home/claude/tl/music (manifest.json gives title, artist, licence). All 11 match the credited track.

| slot (ET) | post | networks | caption credit now | actual track in posted file | license | needed caption change |
|---|---|---|---|---|---|---|
| Oct 30 12:00pm | Our logo, take 2 | TikTok, YouTube, FB+IG | Utopian Future by John Bartmann, CC0 | utopian_future.mp3 (fp median 1.00) | CC0 (credit optional, harmless) | none |
| Oct 31 12:00pm | Cleo's victory pose, take 2 | TikTok, YouTube, FB+IG | Forest road by TRG Banks, CC0 | forest_road.mp3 (fp median 0.99) | CC0 (credit optional, harmless) | none |
| Nov 1 12:00pm | Thornberry Forest, take 2 | TikTok, YouTube, FB+IG | Surreal Forest by Meydän, CC BY 4.0 | surreal_forest.mp3 (fp median 0.99) | CC BY (credit required) | none |
| Nov 2 12:00pm | Rayleigh, take 2 | TikTok, YouTube, FB+IG | Kodama by HoliznaCC0, CC0 | kodama.mp3 (fp median 0.99) | CC0 (credit optional, harmless) | none |
| Nov 3 12:00pm | Joy's trading card, take 2 | TikTok, YouTube, FB+IG | Running Waters by Jason Shaw, CC BY 3.0 | running_waters.mp3 (fp median 1.00) | CC BY (credit required) | none |
| Nov 4 12:00pm | The Side Quest dragon, take 2 | TikTok, YouTube, FB+IG | Daybreak in a new town by TRG Banks, CC0 | daybreak_in_a_new_town.mp3 (fp median 1.00) | CC0 (credit optional, harmless) | none |
| Nov 5 12:00pm | The Hollow from the side, take 2 | TikTok, YouTube, FB+IG | Into the Cloud by John Bartmann, CC0 | into_the_cloud.mp3 (fp median 1.00) | CC0 (credit optional, harmless) | none |
| Nov 6 12:00pm | The creatine label, take 2 | TikTok, YouTube, FB+IG | River Meditation by Jason Shaw, CC BY 3.0 | river_meditation.mp3 (fp median 1.00) | CC BY (credit required) | none |
| Nov 7 12:00pm | Joy and the Hollow, take 2 | TikTok, YouTube, FB+IG | Bright Tomorrow by John Bartmann, CC0 | bright_tomorrow.mp3 (fp median 1.00) | CC0 (credit optional, harmless) | none |
| Nov 8 12:00pm | The Royal Castle, take 2 | TikTok, YouTube, FB+IG | Elk by Meydän, CC BY 4.0 | elk.mp3 (fp median 1.00) | CC BY (credit required) | none |
| Nov 9 12:00pm | Cyrus's victory pose, take 2 | TikTok, YouTube, FB+IG | Spring In Sight by HoliznaCC0, CC0 | spring_in_sight.mp3 (fp median 0.99) | CC0 (credit optional, harmless) | none |

Also in the window, not audited for music: the 1:00pm image posts (TikTok has autoAddMusic on, so TikTok picks the sound; no caption credit, none needed) and the 10:00am timelapse and 4:00pm UGC posts, which are all drafts.

## Flags

1. **Metricool is still on older renders for 15 of these reels: 027, 036, 047, 051, 057, 058, 062, 064, 066, 081, 082, 085, 089, 090, 093.** Byte sizes of the Metricool media (checked by the earlier run, media ids unchanged today) differ from the current batch_v3 files. This does not change any credit (the older renders use Adobe Stock tracks too: fingerprints show 027 adventure_island, 036 energetic, 047 adventure_island, 064 back_to_80s, 066 magical_action), but it means the reels as scheduled are not the current cuts until they are swapped.
2. **Licence record missing for 3 tracks used here: arcade_game_loop (006, 049), digital_mushrooms (025, 060, 064, 085) and energetic (036, 058).** They sit in S/music_adobe (downloaded Oct 27, 11:51pm, an hour before the logged Adobe Stock batch) but are not in S/dl_music.txt, have no embedded tags, and no other licence or credits file names them. They are not on the CC (FMA) list, so I treated them as Adobe Stock, but that is inferred, not verified. If they came from somewhere else, the credit answer for those 8 reels could change.
3. #018 (Oct 31 4:00pm): no log line names its track; adventure_loop comes from the earlier run's fingerprint (0.94), not from a log.
4. The Oct 29 6:00pm "Guide battle" (029) and Nov 7 6:00pm "Don't blink" (088) posts are drafts, so they are not in the table; the live posts in those slots are 006 and 100.
