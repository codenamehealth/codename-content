Build review: r027 (10s)
✅ Keep doing
• The before and after reads instantly. Top: Day 1, LV 1, small Hollow in the forest. Bottom: "1 YEAR LATER", Day 365, LV 99, big Hollow cheering in the golden hall.
• The gummy drops onto the Hollow at 0.0 to 0.5s, so there's motion in the first second.
• Seamless loop: the last 0.5s flows straight into the first.
• Title is one short, large line, well inside the safe zone.

❌ Fix
• 0.5 to 10.0s: nothing changes after the first second. The top repeats the same gummy drop and "+1 XP" every 2 to 3s, and the bottom idles. → Make the top progress: tick DAY up fast (1, 7, 30, 100, 365) and fill the LV bar to a LEVEL UP stamp at about 8s that matches the bottom, then loop.
• 0.0 to 10.0s: "+1 XP" is light blue on green and about 24px tall, so it vanishes on a phone. "DAY 1", "LV 1" and "1 YEAR LATER" are also about 24px. → Make "+1 XP" white or yellow with a dark outline at 48px or more, and bump the labels to at least 36px.
• 0.0 to 10.0s: the Day 1 Hollow is about 120px tall. → Scale him up 1.5x. The size gap still sells the growth.
• 0.0 to 10.0s: the red apple and pink berry around the LV 99 Hollow read as fruit, not gummies. → Give every pickup the gummy shape and sheen.
• 0.0 to 10.0s: there's no comment trigger. → Add one bold line in the empty floor strip under the bottom panel (above the bottom 420px): "WHAT DAY ARE YOU ON?"
• 0.0 to 10.0s: "DAY 1" and "LV 99" sit about 75 to 80px from the left edge. → Move them 30px inward.

🎯 Priority order
1. Day counter and XP bar that progress to a LEVEL UP at 8s
2. Larger, higher-contrast "+1 XP" and labels
3. "WHAT DAY ARE YOU ON?" prompt
4. Pickups that read as gummies
5. Bigger Day 1 Hollow, labels moved in

Target length: 9s, payoff at 8s
