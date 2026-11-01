Build review: n02_race (20.8s)
Verdict: FIX FIRST (the attack section needs a rework)

✅ Keep doing
• 0.6 to 0.8s: Cyrus clearly steps off the line on "1" before GO!. It's findable on a rewatch.
• 4.5 to 5.4s: the growing shadow telegraphs King Slime, the knockouts read, and JOY OUT! / CLEO OUT! come one at a time.
• 13.8 to 15.7s: the referee whistle, FALSE START, and the crown going to Rayleigh land the job's answer. The King Slime heart break (17.2s) and DID YOU SEE IT? (2.5s hold) work. It loops to the countdown.
• No backward jumps at any attack start or end (checked at 30fps).

❌ Fix
• 2.03 to 4.40s and 8.3 to 9.6s: strikes don't land on the victim. Each guide attacks the same slime twice. The first attack (Cyrus 2.03s, Rayleigh 2.40s, Joy 2.92s, Cleo 3.10s) gets no reaction. Slimes pop about 0.2s after the second attack, and the first pop (2.80s, Rayleigh's lane) is timed to Cyrus's punch. Cyrus's fist also sinks into the slime at 2.10 to 2.22s. → One attack per guide. The victim reacts on the strike frame, with no fist overlap.
• 2.0 to 4.4s: all four guides fight at once, and Cyrus attacks again during JOY OUT! (6.3s). → Stagger the attacks one at a time, or cut this section down to a single slime.
• Same window: the small pickup each slime drops is never collected and has no effect. → Remove it, or make it a named gummy power.
• 5.50 to 5.87s and 17.33 to 17.50s: the screen shake exposes black bars 8 to 24px wide at the frame edges. → Overscan the background by 30px before shaking.
• 15.0 to 15.6s: the crown glides sideways at a fixed height. It floats. → Toss it in a gravity arc onto Rayleigh.
• 14.1 to 15.0s: the FALSE START! banner and the CYRUS: FOUL! stamp show at the same time. → Keep one.

🎯 Priority order
1. Strike sync and one attack per guide
2. One attacker at a time
3. Black bars on the shake
4. Crown arc
5. One foul label
Target length: 18.5s (trim the 9.6 to 11.4s run), payoff at 12s
