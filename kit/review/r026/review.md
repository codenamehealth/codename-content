Build review: r026 (10s)
✅ Keep doing
• Motion from frame one: the gummy is already arcing off Rayleigh's staff orb at 0.0s, and the title explains the game straight away.
• Moonlit scene, Rayleigh and a purple bottle all match the sleep theme with no clutter.
• Never shows the gummy landing. At the end the orb fades back to the bare staff (last 0.5s), which matches the opening frames, so the loop reads as a restart.
• Short at 10s, which suits a pause challenge.

❌ Fix
• 0.0 to 10.0s: the gummy is about 45px wide at full res and the bottle neck is narrow, so it's hard to track on a phone. → Make the gummy 2x larger and add a short glowing trail so the eye can follow it.
• 1.5s, 3.0s, 8.5s: the closest passes go near the bottle mouth but never clearly over it, so a viewer may decide it can't be done and swipe. → Route at least 3 passes directly over the neck opening at speed, so the window is real but tight. Still no landing.
• 0.0 to 10.0s: "PAUSE WHEN IT DROPS IN" is about 27px tall at full res. → It's the actual instruction, so make it at least 40px or merge it into the title: "PAUSE WHEN THE GUMMY DROPS IN".
• 8.5 to 10.0s: "Did you get it?" arrives late, is thin lowercase, and doesn't ask for a comment. → Show it from 0s as a bold one-liner: "COMMENT IF YOU GOT IT".
• 0.0 to 10.0s: Rayleigh and the bottle fill only the middle third, and the bottom third is empty floor. → Scale the play area up about 1.3x and center it slightly lower (staying above the bottom 420px).
• No escalation across 10s. → Speed up the gummy's arc slightly from 6s on so the last passes feel harder.

🎯 Priority order
1. Clear, fast passes directly over the bottle mouth
2. Bigger gummy with a trail
3. Comment prompt from 0s
4. Larger instruction line
5. Bigger play area, speed ramp

Target length: 10s, payoff at 9s (fastest pass over the mouth just before the loop)
