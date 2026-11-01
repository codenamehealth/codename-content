import json
P=[]
def h2(t): P.append(('HEADING_2',t)); P.append(('N',''))
def h3(t):
    if P and P[-1][0]=='B': P.append(('N',''))
    P.append(('HEADING_3',t)); P.append(('N',''))
def b(t): P.append(('B',t))

h2("Oct 17, 2026: TikTok affiliate count, Klaviyo seed update, Hunter week 4 (gift guides plus local Tampa Bay) loaded and started (added by the Oct 16 night chat)")
h3("TikTok Shop affiliates (read from Affiliate Center, Oct 17 afternoon)")
b("92 creators accepted out of 4,000 invited. By batch: D1 0 of 150, D2 28 of 900, D3 5 of 650, D4 22 of 1,300, D5 37 of 1,000. 78 sample requests waiting, 1 creator message, 6 flagged \"Samples not enabled\", 0 creators promoted.")
b("Bennett: about 100 affiliates in under 3 days is a great start. Next test is 40 to 50 orders in the next 3 weeks; he expects the low end because creators need time to receive product and post. Inventory holds if the program pauses.")
b("Claude's estimates (given once, not to be moved): about 25 TikTok Shop orders in 3 weeks, about 45 in a month; about 1 in 7 odds that one of the first ~40 videos clears 500K views.")
h3("Facts and decisions from Bennett (Oct 17)")
b("Lead times: Vitalabs 2 weeks; cards 3 weeks; stickers 3 weeks; labels 3 to 4 weeks (4 on a first order).")
b("The blackberry melatonin label needs to go to the printer now, rushed, aiming for about 3 weeks back. Melatonin is the product most creators are ordering. He orders the 500 blackberry jars Tue Oct 20.")
b("New shops are capped at 50 orders a day. Samples do not count against that cap. 200 shipped orders is the last probation tier before the shop is uncapped.")
b("Ideal path: 50 to 100 orders over the next month, then about 1,000 of each unit ordered in November, then Euka and 500+ more creators.")
b("After probation TikTok allows dropping to 4 products. If subscriptions turn on, Bennett may go to 4 products and give trading cards to subscribers, made clear on the listing. Current lean: keep the 8 listings (4 jars, 4 card bundles) and drop the 2 two-jar bundles.")
h3("Klaviyo seed list updated from Updated_Seedlist_1.csv (Warmy changes)")
b("List \"Warmup - Seed list (do not use)\" (Y5PzcM). Added 4 new profiles, never subscribed like the rest: hiralaljia@gmail.com, choudharyfajru81@gmail.com, hs5987577@gmail.com, tekrajmagarmaya@gmail.com. Removed from the list: areamabdelgadir466@gmail.com, guilhermeldv405@gmail.com, dapham54@gmail.com, bardadsin@gmail.com. Count checked after: 500.")
h3("Hunter week 4 (week of Nov 2): 294 leads, 40 first emails per inbox Mon to Wed, follow-ups Thu to Sat")
b("Bennett: \"go ahead and schedule week 4. the full 40 emails per day\", \"80 emails total 40 per inbox\", and later \"make sure some of these are local like tampa bay times\" (local can spill to week 5; volume over quality; use Sam's press pitch angle, \"29 year old tampa native\").")
b("All 12 sequences started Oct 17 (status planned), 9am to 5pm, 7 days, no tracking, no unsubscribe link, one follow-up 3 days later, subject \"We built supplements into an RPG\". Leads list 31316046 \"Gift guides wk4 bulk (Nov 2)\".")
b("Gift-guide copy (same as weeks 2 and 3), 31 recipients each: partners Mon 11/2 908160, Tue 11/3 908161, Wed 11/4 908162; bennett Mon 908163, Tue 908164, Wed 908165. Outlets: gaming, PC hardware, VR, retro, mobile, geek culture, comics, board games, city and lifestyle magazines (US, UK, Canada, Australia).")
b("Local Tampa Bay copy, 9 recipients each: partners Mon 908169, Tue 908170, Wed 908171; bennett Mon 908172, Tue 908173, Wed 908174. Opener: \"I'm a 29-year-old Tampa native, and I think the company I just launched here would make a fun local story for {{company}}.\" Close: \"I'd love to send you a jar to try, no strings attached. Happy to send character art or get on a call too.\" Middle paragraph and follow-up unchanged.")
b("Local outlets (54 contacts): Creative Loafing, St. Pete Catalyst, 83 Degrees, I Love the Burg, That's So Tampa, Tampa Bay Business and Wealth, Tampa Bay Magazine, Tampa Magazines, WFLA, WTSP, ABC Action News, Bay News 9, Florida Trend, St Pete Rising, Tampa Bay Parenting, Tampa Bay Beacons (tbnweekly.com), Osprey Observer, WUSF. Tampa Bay Times only has its food writer (Evan Rodriguez); the rest of the Times takes pitches through projects.tampabay.com/projects/tips. Fox 13 had nothing in Hunter. No morning-show producers found.")
b("Per inbox per day: Mon 11/2 40, Tue 40, Wed 40, Thu 40, Fri 40, Sat 40 (follow-ups only), Sun 0. Week 3's last sends are Sun Nov 1, so nothing overlaps. Same unverified assumption as before: the 3-day wait counts calendar days.")
b("Week 5 carryover: 51 verified gift-guide leads pulled from week 4 to make room for the locals, saved at /home/claude/hunter/wk5_carryover.json (they are already in Hunter as leads, in list 31316046, but in no sequence).")
b("All week-4 domains are logged against /home/claude/hunter/used_domains_all.txt plus the week-4 files (wk4_load.json, wk4_local_load.json). Lead id maps: wk4_lead_ids.json, wk4_local_ids.json. Lead fixes made: Locus inbox name cleared (was \"Fran Locus\"), three Tampa Bay Newspapers leads set to company \"Tampa Bay Beacons\" (had a stray apostrophe), Kyla Fetch position set to Food writer.")
b("Process note: the Hunter remove tool takes emails, not lead ids. Create-Lead-If-Missing never fixes leads an earlier Email Verifier run created; those need Update-Lead.")
h3("Open threads (Bennett decides what goes on his list)")
for t in ["Main-account timelapses run out after Oct 23. Whether that is this chat's job is not answered.",
 "78 sample requests in Affiliate Center, after Euka is in.",
 "Blackberry label to the printer, rushed. The print PDF is in the Oct 14 to 16 chat; Claude offered to check it and draft the rush request if it is attached here.",
 "Vito: TikTok Shipping (Upgraded) decision.",
 "Week 5 Hunter: 51 carryover leads ready; more needed to fill 40 per inbox."]: b(t)

txt="\n".join(t for _,t in P)
assert '—' not in txt and '–' not in txt
START=301187
u=lambda s: len(s.encode('utf-16-le'))//2
reqs=[{"insertText":{"location":{"index":START,"tabId":"t.0"},"text":"\n"+txt}}]
pos=START+1; rng=[]
for st,t in P:
    rng.append((st,pos,pos+u(t)+1)); pos+=u(t)+1
end=pos-1
reqs.append({"deleteParagraphBullets":{"range":{"startIndex":START+1,"endIndex":end,"tabId":"t.0"}}})
reqs.append({"updateParagraphStyle":{"range":{"startIndex":START+1,"endIndex":end,"tabId":"t.0"},"paragraphStyle":{"namedStyleType":"NORMAL_TEXT"},"fields":"namedStyleType"}})
for st,a,z in rng:
    if st.startswith('HEADING'):
        reqs.append({"updateParagraphStyle":{"range":{"startIndex":a,"endIndex":z,"tabId":"t.0"},"paragraphStyle":{"namedStyleType":st},"fields":"namedStyleType"}})
i=0
while i<len(rng):
    if rng[i][0]=='B':
        j=i
        while j+1<len(rng) and rng[j+1][0]=='B': j+=1
        reqs.append({"createParagraphBullets":{"range":{"startIndex":rng[i][1],"endIndex":rng[j][2]-1,"tabId":"t.0"},"bulletPreset":"BULLET_DISC_CIRCLE_SQUARE"}})
        i=j+1
    else: i+=1
json.dump(reqs,open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/req17.json','w'))
print(len(P),len(reqs),end)
