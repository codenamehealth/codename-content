# Epidemic Sound music pass (Oct 29)

Bennett: "we need viral tracks. i know social media rewards viral audio" ... "you have the upgraded account now. do your magic".
Goal: replace the Adobe Stock beds on the scheduled Code Name reels with popular, high-energy Epidemic Sound tracks that fit each reel, cut to the reel, keeping each reel's own SFX. Then swap them into Metricool.

S = /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
Read first: S/pixellab/safezone/FIX_COMMON.md (agent rules: prev/ backups, log lines, mux2, disk) and S/pixellab/safezone/METRICOOL_RULES.md + S/pixellab/safezone/metricool_v3_swap.md (swap flow and ids).

## Epidemic API
- Client: S/epidemic/es.py (`sid=es.session()`, `es.call(name,args,sid)`). The key is in S/epidemic/.key. Never print, log or copy the key anywhere.
- SearchRecordings: `{'query':{'term':...},'sort':{'by':'POPULARITY','order':'DESCENDING'},'first':N}`; results in data.recordings.nodes[].recording (id, title, bpm, audioFile.lqmp3Url, credits, stems). Check the tool schema (tools/list) for more filters (mood, genre, bpm, vocals).
- DownloadRecording `{'id':ID,'options':{'fileType':'WAV' or 'MP3','stemType':'FULL'}}` returns data.recordingDownload.assetUrl (works now, verified). Prefer WAV.
- EditRecording (targetDurationMs, loopable) + PollEditRecordingJob + DownloadRecordingEdit: Epidemic's own musical re-edit to an exact length. Use it with targetDurationMs = reel length and loopable=true, since the reels loop: the seam at the loop point should be musical. If the edit tool fails or sounds wrong, fall back to a trim from a strong section with a short fade.
- SearchSimilarToRecording / SearchExternalReferences: find Epidemic tracks that sound like a currently trending TikTok/Reels song. Worth trying for the "viral" sound: look up what is trending now (WebSearch, or the Higgsfield tiktok_music_trending tool if you can load it) and find Epidemic sound-alikes. Instrumental only (no vocals) unless a vocal track clearly fits; no lyrics that clash with the brand.
- Save downloads under S/epidemic/tracks/ with a JSON manifest (id, title, artist, bpm, file, which reels use it).

## What makes a track right here
- Starts hot: energy and a clear beat inside the first 0.5s (the hook frame). Pick the start point by measuring RMS/onsets (librosa or numpy), not by guessing. No slow intros.
- Fits the reel: races, battles and chases get high-energy (phonk, hype trap, EDM, chiptune-hybrid, sports rock); find-it puzzles and "pause when" reels get tense, ticking, sneaky or bouncy tracks that do not drown the SFX; cozy and comedy reels get playful/quirky. Pixel-art fits chiptune flavors, but popular modern tracks beat generic 8-bit.
- Varied (Bennett's standing rule): no track on more than 2 reels in the Oct 29 to Nov 9 schedule, never the same track twice on one day or on back-to-back slots.
- Popularity: sort by POPULARITY and favor the top results that fit. Record the rank you picked from.

## Mixing
- Keep every reel's own SFX. The SFX come from the reel's events JSON through S/pixellab/mix.py (music + events -> -14 LUFS). Find the events file and music settings from the reel's latest mix line in S/pixellab/batch_v3/log.txt (follow it back to earlier lines or batch_review/log.txt when it says the audio was reused). Run mix.py with the new track (offset = your chosen start, music vol around 0.45 to 0.55 so SFX still read), then mux2.sh onto the CURRENT batch_v3 video (video stream untouched, every frame kept). Target -14 LUFS, true peak under -1 dBTP (S/fork_rc2/loudfix.sh).
- Reels with special music: 077 musical chairs uses a gated bed (music silent on each STOP!); rebuild the gate on the new track with the same mute windows (fork_rc8/v77 and fork_n19/v077 show how). 017 "play along with the beat" is synced to its music: leave 017 alone. Any reel whose visuals are timed to the music: leave it and list it.
- If a reel has no events file you can trust, do NOT try to strip the old music out of the mixed audio (that degrades quality). List it and move on.
- Back up to batch_v3/prev/<name>_preepidemic.mp4 first, log one line per reel in batch_v3/log.txt (track title, artist, Epidemic id, offset/edit, LUFS, peak).
- Listen-check in numbers: after mixing, confirm the SFX peaks are still visible over the bed at their event times and the first 0.5s RMS is high.

## Which reels, in what order
- Schedule: S/pixellab/safezone/schedule_plan.json ([slot ET, reel, type]) and the audit S/pixellab/safezone/MUSIC_CREDITS_AUDIT.md (track now in each scheduled reel).
- Do the scheduled reels in posting order starting Oct 30 10:00am (014). Skip the two Oct 29 posts (006 at 6pm, 007 at 8pm): too close to posting time.
- SKIP anything listed in S/pixellab/safezone/INFLIGHT.txt (another agent is editing it). Re-read INFLIGHT.txt before every reel. When you've done all free reels, re-read it and do any reels that have been freed since; repeat until only in-flight reels are left, then stop and report which are still waiting.
- #051 (Oct 30 6pm) is free and urgent: Metricool still has an older cut of it, so remix the current file and swap it first after 014.

## Metricool swap (after each remix)
- Use the established flow in metricool_v3_swap.md: Higgsfield media_upload, curl PUT (Content-Type video/mp4, If-None-Match: *), media_confirm, updateScheduledPost on all 3 posts in the slot (FB+IG REEL, TikTok, YouTube Short), then verify the static.metricool.com content-length equals the local file size (S/mc_v3/indep_check.py). Captions unchanged. Leave out twitterData; leave out instagramData on TikTok-only and YouTube-only posts. autoPublish stays true. Record new post ids in metricool_v3_swap.md (the post id changes on update, the uuid stays).
- Do not swap anything inside 45 minutes of its post time.
- Epidemic needs no caption credit line. Do not add one.

## Report back
Table: reel, slot, track (title / artist / popularity rank), start or edit, LUFS, swapped yes/no + new ids, and anything skipped with the reason. Plus the full list of Epidemic tracks downloaded.

## Level change (Oct 29 5:25pm, Bennett: "maybe a little loud")
- Epidemic mixes: music bed ~3 dB lower vs SFX than first pass; integrated -15.0 LUFS (+-0.3), true peak <= -1.5 dBTP. Applies to every reel from now, including fix-agent re-mixes.
