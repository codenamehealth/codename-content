import json, sys
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
import re
t2 = {}
for lf in sys.argv[1:]:
    for line in open(lf):
        m = re.match(r'(\S+\.mp4) (\S+) med=([\d.]+) max=([\d.]+) off=([\d.]+)', line)
        if m:
            t2[m.group(1)] = [[m.group(2), (float(m.group(3)), float(m.group(4)), float(m.group(5)))]]

AD = {  # Adobe Stock titles from S/dl_music.txt (AdobeStock_<id> filenames)
 'joypad_arcade': 'Casual Sweat On The Joypad - Arcade, Upbeat - Loop (AdobeStock_676139692)',
 'arcade_loop2': 'Arcade Loop (AdobeStock_1536841857)',
 'space_arcade': 'Space Game Arcade Loop (AdobeStock_513023888)',
 'platforms_8bit': '8-bit Arcade - World Made Of Platforms - Loop (AdobeStock_676139665)',
 'retro_game_play': 'Classic Retro Video Game Play (AdobeStock_1925597393)',
 'magical_action': 'Magical Action Adventure (loop version) (AdobeStock_1536842484)',
 'adventure_epic_game': 'Adventure Epic Game (AdobeStock_481021343)',
 'adventure_island': 'Adventure Island Loop (AdobeStock_513024170)',
 'adventure_loop': 'adventure loop (AdobeStock_526744215)',
 'fantasy_adventure': 'Symphonic Uplifting Fantasy Adventure (Short Loop 6) (AdobeStock_513024727)',
 'arcade_edm_rock': 'Arcade Upbeat EDM Rock - Loop (AdobeStock_676139718)',
 'back_to_80s': 'Back To The 80s (Loop) (AdobeStock_526743454)',
 'glockenspiel_pop': 'Cheerful Lighthearted Pop Rock glockenspiel loop (AdobeStock_1536841906)',
 'orchestral_fantasy': 'Orchestral Fantasy (AdobeStock_495722646)',
}
UNREC = {'arcade_game_loop', 'digital_mushrooms', 'energetic', 'eight_bit', 'chiptune_gameboy'}

# reel -> (track file stem, evidence)
R = {
 '006': ('arcade_game_loop', 'audio reused (log 114); batch_review r6 arcade_game_loop; fp 0.96'),
 '007': ('magical_action', 'mux2 reuse (log 125); batch_review r7; fp 0.74'),
 '014': ('adventure_epic_game', 'mux reuse (log 87); batch_review r14 @4s; fp 0.91'),
 '051': ('arcade_loop2', 'log 191 mix.py arcade_loop2; fp 0.91'),
 '012': ('orchestral_fantasy', 'mux reuse (log 21); batch_review r12 @18s; fp 0.83'),
 '016': ('glockenspiel_pop', 'mux reuse (log 10); batch_review r16; fp 0.93'),
 '018': ('adventure_loop', 'mux reuse (log 1); fp 0.94 (no named track in logs)'),
 '058': ('energetic', 'log 173 mix.py energetic@12; fp 0.97'),
 '017': ('back_to_80s', 'mux2 reuse (log 118); batch_review r17 @1.8s; fp 0.72'),
 '025': ('digital_mushrooms', 'mux2 reuse (log 158); batch_review digital_mushrooms@20; fp 0.99'),
 '021': ('space_arcade', 'mux reuse (log 7); batch_review r21; fp 1.00'),
 '064': ('digital_mushrooms', 'log 200 mix.py digital_mushrooms@0'),
 '023': ('glockenspiel_pop', 'mux2 reuse (log 156); batch_review r23; fp 0.88'),
 '034': ('platforms_8bit', 'mux reuse (log 32); batch_review r34 / batch_v2 remix'),
 '026': ('magical_action', 'mux reuse (log 34); batch_review r26; fp 0.99'),
 '077': ('adventure_loop', 'mux2 reuse, gated music (log 75); batch_review r77 / batch_v2 remix'),
 '027': ('adventure_island', 'log 171/180 remix adventure_island@0'),
 '038': ('retro_game_play', 'mux reuse (log 44); batch_review r38 switched fantasy_adventure -> retro_game_play'),
 '030': ('joypad_arcade', 'mux reuse (log 22); batch_review r30; fp 0.93'),
 '081': ('space_arcade', 'log 184 mix.py space_arcade'),
 '040': ('fantasy_adventure', 'mux reuse (log 28); batch_review r40'),
 '044': ('retro_game_play', 'mux reuse (log 40); batch_review r44 switched back_to_80s -> retro_game_play'),
 '036': ('energetic', 'log 199 remix energetic @11.995 (correlation 0.999)'),
 '043': ('adventure_island', 'log 140 mix.py adventure_island; log 182 remixed (adventure_island)'),
 '049': ('arcade_game_loop', 'log 166 mix.py arcade_game_loop; log 176 loudness-only'),
 '042': ('arcade_loop2', 'mux reuse (log 35); batch_review r42 same track arcade_loop2'),
 '082': ('back_to_80s', 'log 183 mix.py back_to_80s'),
 '045': ('fantasy_adventure', 'log 187 mix.py fantasy_adventure'),
 '057': ('retro_game_play', 'mux2 reuse (log 153); batch_review r57 retro_game_play kept'),
 '075': ('adventure_island', 'mux2 reuse (log 73); batch_review r75 adventure_island kept'),
 '085': ('digital_mushrooms', 'log 189 mix.py digital_mushrooms'),
 '047': ('joypad_arcade', 'log 164 mix.py joypad_arcade; log 190 remixed (joypad_arcade)'),
 '060': ('digital_mushrooms', 'audio muxed unchanged (log 67); batch_review r60 digital_mushrooms@20 kept'),
 '083': ('space_arcade', 'audio reused (log 94); batch_review r83 space_arcade kept'),
 '100': ('adventure_island', 'log 150 reuses previous file track; batch_review r100 adventure_island kept'),
 '090': ('glockenspiel_pop', 'log 202 mix.py glockenspiel_pop'),
 '062': ('orchestral_fantasy', 'log 186 mix.py orchestral_fantasy@40'),
 '087': ('back_to_80s', 'audio reused (log 98); batch_review r87 back_to_80s kept'),
 '089': ('back_to_80s', 'log 193 mix.py back_to_80s'),
 '095': ('adventure_loop', 'mux2 reuse (log 84); batch_review r95 adventure_loop kept'),
 '066': ('fantasy_adventure', 'log 206 remix fantasy_adventure@0'),
 '096': ('arcade_loop2', 'mux2 reuse (log 85); batch_review r96 arcade_loop2 kept'),
 '093': ('arcade_loop2', 'log 208 mix.py arcade_loop2@3'),
 '072': ('space_arcade', 'mux2 reuse (log 71); batch_review r72 switched fantasy_adventure -> space_arcade'),
}
FILES = {}
import glob, os
for p in glob.glob(S + '/pixellab/batch_v3/[0-9][0-9][0-9]_*.mp4'):
    FILES.setdefault(os.path.basename(p)[:3], os.path.basename(p))

STALE = {'051', '058', '064', '027', '081', '036', '082', '057', '085', '047', '090', '062', '089', '066', '093'}

# (date time, reel, networks, caption credit)
rows = [
 ('Oct 29 6:00pm', '006', 'none'), ('Oct 29 8:00pm', '007', 'none'),
 ('Oct 30 10:00am', '014', 'none'), ('Oct 30 6:00pm', '051', 'none'), ('Oct 30 8:00pm', '012', 'none'),
 ('Oct 31 10:00am', '016', 'none'), ('Oct 31 4:00pm', '018', 'none'), ('Oct 31 6:00pm', '058', 'none'), ('Oct 31 8:00pm', '017', 'none'),
 ('Nov 1 10:00am', '025', 'none'), ('Nov 1 4:00pm', '021', 'none'), ('Nov 1 6:00pm', '064', 'none'), ('Nov 1 8:00pm', '023', 'none'),
 ('Nov 2 10:00am', '034', 'none'), ('Nov 2 4:00pm', '026', 'none'), ('Nov 2 6:00pm', '077', 'none'), ('Nov 2 8:00pm', '027', 'none'),
 ('Nov 3 10:00am', '038', 'none'), ('Nov 3 4:00pm', '030', 'none'), ('Nov 3 6:00pm', '081', 'none'), ('Nov 3 8:00pm', '040', 'none'),
 ('Nov 4 10:00am', '044', 'none'), ('Nov 4 4:00pm', '036', 'none'), ('Nov 4 8:00pm', '043', 'none'),
 ('Nov 5 10:00am', '049', 'none'), ('Nov 5 4:00pm', '042', 'none'), ('Nov 5 6:00pm', '082', 'none'), ('Nov 5 8:00pm', '045', 'none'),
 ('Nov 6 10:00am', '057', 'none'), ('Nov 6 4:00pm', '075', 'none'), ('Nov 6 6:00pm', '085', 'none'),
 ('Nov 6 8:00pm', '047', 'Music: Start the Day by Lee Rosevere, CC BY 4.0'),
 ('Nov 7 10:00am', '060', 'none'), ('Nov 7 4:00pm', '083', 'none'), ('Nov 7 6:00pm', '100', 'none'), ('Nov 7 8:00pm', '090', 'none'),
 ('Nov 8 10:00am', '062', 'none'), ('Nov 8 4:00pm', '087', 'none'), ('Nov 8 6:00pm', '089', 'none'), ('Nov 8 8:00pm', '095', 'none'),
 ('Nov 9 10:00am', '066', 'none'), ('Nov 9 4:00pm', '096', 'none'), ('Nov 9 6:00pm', '093', 'none'), ('Nov 9 8:00pm', '072', 'none'),
]

# non-batch_v3 noon videos: (slot, name, caption credit, licence, t2 file)
noon = [
 ('Oct 30 12:00pm', 'Our logo, take 2', 'Utopian Future by John Bartmann, CC0', 't2_logo.mp4', 'utopian_future.mp3'),
 ('Oct 31 12:00pm', "Cleo's victory pose, take 2", 'Forest road by TRG Banks, CC0', 't2_cleo_pose.mp4', 'forest_road.mp3'),
 ('Nov 1 12:00pm', 'Thornberry Forest, take 2', 'Surreal Forest by Meydän, CC BY 4.0', 't2_thornberry.mp4', 'surreal_forest.mp3'),
 ('Nov 2 12:00pm', 'Rayleigh, take 2', 'Kodama by HoliznaCC0, CC0', 't2_rayleigh.mp4', 'kodama.mp3'),
 ('Nov 3 12:00pm', "Joy's trading card, take 2", 'Running Waters by Jason Shaw, CC BY 3.0', 't2_joy_card.mp4', 'running_waters.mp3'),
 ('Nov 4 12:00pm', 'The Side Quest dragon, take 2', 'Daybreak in a new town by TRG Banks, CC0', 't2_dragon.mp4', 'daybreak_in_a_new_town.mp3'),
 ('Nov 5 12:00pm', 'The Hollow from the side, take 2', 'Into the Cloud by John Bartmann, CC0', 't2_hollow_side.mp4', 'into_the_cloud.mp3'),
 ('Nov 6 12:00pm', 'The creatine label, take 2', 'River Meditation by Jason Shaw, CC BY 3.0', 't2_creatine_label.mp4', 'river_meditation.mp3'),
 ('Nov 7 12:00pm', 'Joy and the Hollow, take 2', 'Bright Tomorrow by John Bartmann, CC0', 't2_joy_hollow.mp4', 'bright_tomorrow.mp3'),
 ('Nov 8 12:00pm', 'The Royal Castle, take 2', 'Elk by Meydän, CC BY 4.0', 't2_castle.mp4', 'elk.mp3'),
 ('Nov 9 12:00pm', "Cyrus's victory pose, take 2", 'Spring In Sight by HoliznaCC0, CC0', 't2_cyrus_pose.mp4', 'spring_in_sight.mp3'),
]

def lic(stem):
    if stem in AD: return 'Adobe Stock (no credit needed)'
    return 'Adobe Stock, inferred (no licence record found locally; see flag 2)'

def title(stem):
    return AD.get(stem, f'{stem}.wav (title not recorded)')

out = []
out.append('# Music credits audit, Metricool Oct 29 6:00pm to Nov 9 11:59pm ET\n')
out.append('Read-only audit, run Oct 29 2026. Brand Code Name Main (blogId 7178389), America/New_York. Drafts skipped. Every batch_v3 slot has the same three non-draft posts (FB+IG, TikTok, YouTube) and the same caption credit on all three.\n')
out.append('How the track was found: the latest batch_v3/log.txt line that ran mix.py names the wav; when the latest line says the audio was reused (mux/mux2), the track comes from the reel\'s batch_review/log.txt entry. Where the earlier (pre-restart) run of this audit had already fingerprinted a file (S/maudit/fp_*.log), the score is shown; every fingerprint agreed with the logs. No new fingerprinting of batch_v3 files was done.\n')
out.append('## Summary\n')
out.append('- **One caption needs a change: #047 Motivation vs discipline (Nov 6 8:00pm), all three posts (FB+IG, TikTok, YouTube). Remove the line "Music: Start the Day by Lee Rosevere, CC BY 4.0".** The current 047 file is mixed on the Adobe Stock track joypad_arcade (log lines 164 and 190), which needs no credit.')
out.append('- No other batch_v3 reel in the window has a music line, and none needs one: every track used anywhere in the batch, batch_v2, batch_review, batch_final and batch_v3 logs is from S/music_adobe. No CC BY track (the FMA mp3s in /home/claude/tl/music) appears in any reel log.')
out.append('- The noon "take 2" animation posts are not batch_v3 reels; their credits are checked separately below.\n')
out.append('## batch_v3 reels\n')
out.append('| slot (ET) | reel | networks | caption credit now | actual track in current file | license | needed caption change |')
out.append('|---|---|---|---|---|---|---|')
for slot, rid, cred in rows:
    stem, ev = R[rid]
    f = FILES.get(rid, rid)
    change = 'remove line' if cred != 'none' else 'none'
    note = '; Metricool has an older render (flag 1)' if rid in STALE else ''
    out.append(f'| {slot} | {f} | FB+IG, TikTok, YouTube | {cred} | {title(stem)} [{ev}] | {lic(stem)} | {change}{note} |')
out.append('')
out.append('## Non-batch_v3 video posts in the window (noon "take 2" animations)\n')
out.append('These carry music credits. Their files are the Metricool media copies saved in S/maudit/t2 by the earlier run; no log names their tracks, so these 11 short files were fingerprinted against the 13 tracks in /home/claude/tl/music (manifest.json gives title, artist, licence). All 11 match the credited track.\n')
out.append('| slot (ET) | post | networks | caption credit now | actual track in posted file | license | needed caption change |')
out.append('|---|---|---|---|---|---|---|')
for slot, name, cred, f, want in noon:
    r = t2.get(f)
    if r:
        best, (med, mx, off) = r[0][0], r[0][1]
        ok = best == want and med >= 0.5
        act = f'{best} (fp median {med:.2f})' if med >= 0.5 else f'no confident match (best {best}, median {med:.2f})'
        change = 'none' if ok else 'CHECK: fingerprint does not confirm the credited track'
    else:
        act, change = 'not checked', 'not checked'
    licence = 'CC BY (credit required)' if 'CC BY' in cred else 'CC0 (credit optional, harmless)'
    out.append(f'| {slot} | {name} | TikTok, YouTube, FB+IG | {cred} | {act} | {licence} | {change} |')
out.append('')
out.append('Also in the window, not audited for music: the 1:00pm image posts (TikTok has autoAddMusic on, so TikTok picks the sound; no caption credit, none needed) and the 10:00am timelapse and 4:00pm UGC posts, which are all drafts.\n')
out.append('## Flags\n')
out.append('1. **Metricool is still on older renders for 15 of these reels: 027, 036, 047, 051, 057, 058, 062, 064, 066, 081, 082, 085, 089, 090, 093.** Byte sizes of the Metricool media (checked by the earlier run, media ids unchanged today) differ from the current batch_v3 files. This does not change any credit (the older renders use Adobe Stock tracks too: fingerprints show 027 adventure_island, 036 energetic, 047 adventure_island, 064 back_to_80s, 066 magical_action), but it means the reels as scheduled are not the current cuts until they are swapped.')
out.append('2. **Licence record missing for 3 tracks used here: arcade_game_loop (006, 049), digital_mushrooms (025, 060, 064, 085) and energetic (036, 058).** They sit in S/music_adobe (downloaded Oct 27, 11:51pm, an hour before the logged Adobe Stock batch) but are not in S/dl_music.txt, have no embedded tags, and no other licence or credits file names them. They are not on the CC (FMA) list, so I treated them as Adobe Stock, but that is inferred, not verified. If they came from somewhere else, the credit answer for those 8 reels could change.')
out.append('3. #018 (Oct 31 4:00pm): no log line names its track; adventure_loop comes from the earlier run\'s fingerprint (0.94), not from a log.')
out.append('4. The Oct 29 6:00pm "Guide battle" (029) and Nov 7 6:00pm "Don\'t blink" (088) posts are drafts, so they are not in the table; the live posts in those slots are 006 and 100.')
open(S + '/pixellab/safezone/MUSIC_CREDITS_AUDIT.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
