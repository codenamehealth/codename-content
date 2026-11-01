Build review: r077 (20.9s)
✅ Keep doing
• Clear premise with an instant comment job: "PICK A PLAYER!" at 0.0s.
• Three-round structure (3, 2, 1 chairs) with a STOP, a SLAP and an elimination each round gives a state change every 2 to 3s from 1.5s to 17.5s.
• "CYRUS WINS! Did you pick right?" closes the loop on the opening prompt. Cutting from the win back to "PICK A PLAYER!" works as a replay invite.
❌ Fix
• 0.0 to 1.5s: guides stand still under the prompt (edges.jpg shows no movement in the first 0.5s) → start the march around the chairs at frame 1 with the prompt over the moving guides.
• 0.0 to 1.5s: guides are about 90px tall and unlabeled, so a stranger can't tell who to pick → add a short name tag over each guide during the prompt, or scale the guides up about 1.5x for the whole reel.
• 17.5 to 20.9s: win screen holds 3.4s with only confetti, and the win lands at 84% of runtime → cut the hold to 1.5s.
• 16.0 to 17.5s: Rayleigh walks off while Cyrus sits alone, about 1.5s of nothing → go straight from the final SLAP to "CYRUS WINS!".
• 4.5s, 10.0s, 15.0s: "STOP!" and "X IS OUT!" appear only as small text in the status bar → stamp both large and centered on the carpet for about 0.6s, then let the bar keep the record.
• 5.0s, 10.5s, 15.5s: "SLAP!" is small and sits right on the characters → make it bigger with a white flash or shake on the hit so the slap actually lands.
• Status bar text ("ROUND 1 - 3 CHAIRS") is small at phone size → enlarge or drop it. The chair count is visible on the carpet anyway.
🎯 Priority order
1. Motion and name tags in the first second.
2. Big centered STOP / OUT stamps.
3. Cut the empty stretch at 16.0 to 17.5s and the long win hold.
4. Bigger SLAP hit.
Target length: 17s, payoff at 15s

Series note: rotate the winner across posts so Cyrus doesn't become the default pick.
