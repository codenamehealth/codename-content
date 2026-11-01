#!/usr/bin/env python3
"""Build caption v2 drafts (CAPTIONS_QUEST_v2.md) for scheduled Metricool posts Oct 30 19:00 - Nov 9."""
import json, os

OUT_MD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone/captions_v2_drafts.md'
OUT_JSON = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/capv2/drafts.json'

S = "Characters hand drawn by Syeda Humna 🎨"
SL = "Characters hand drawn by Syeda Humna, the Realm painted by Liza 🎨"
L = "The Realm painted by Liza 🎨"

# slot, reel, credit, video lines, old first line, (fbig id, uuid), (tt id, uuid), (yt id, uuid) or None, kind, music (CC BY only)
P = []
def add(slot, reel, credit, lines, fbig, tt, yt, kind='reel', music=None, tt_title_mode='caption'):
    P.append(dict(slot=slot, reel=reel, credit=credit, lines=lines, fbig=fbig, tt=tt, yt=yt,
                  kind=kind, music=music, tt_title_mode=tt_title_mode))

add('2026-10-30 19:00','n02 race',SL,["Watch the start one more time 🏁"],(410756032,'5520268982795979162'),(410756064,'1741902407531972431'),(410756086,'-1093402785605465206'))
add('2026-10-30 22:00','#12 +2 XP',SL,["+2 XP. Zero potions left ⚔️"],(410684558,'6106776738648310571'),(410684601,'6431989399489888674'),(410684627,'3797566569377710120'))
add('2026-10-31 12:00','Cleo victory pose take 2 (art)',S,["Cleo's victory pose, take 2 🛡️","The Vitality guide, sword up. Take 1 was all arms."],(409328046,'2540990533283824756'),(409327944,'9209667095019668972'),(409327997,'6324574899250413978'),kind='art')
add('2026-10-31 13:00','Halloween still (AI image, no art credit)',None,["Happy Halloween from everyone still in the lobby 🎃"],(409347217,'7055940563347524907'),(409347177,'3893130791073959366'),None,kind='still',tt_title_mode='first')
add('2026-11-01 10:00','#25 find this Hollow (Sunday, redo at swap)',SL,["Only 1% can find this Hollow 👀"],(410597336,'-1944658012569319335'),(410597354,'3470467703558194435'),(410597464,'-5018025237339946355'))
add('2026-11-01 12:00','Thornberry Forest take 2 (art)',L,["Thornberry Forest, take 2 🌲","Take 1 was three lollipops and a door."],(409328666,'2705527194864471363'),(409328558,'-2785602800094658060'),(409328601,'-7384546340333335000'),kind='art',music="🎵 Surreal Forest by Meydän, CC BY 4.0")
add('2026-11-01 13:00','card pack still',S,["Who'd you pull? 🃏"],(409347344,'-3096937469150477831'),(409347283,'8225136420306964021'),None,kind='still',tt_title_mode='first')
add('2026-11-01 16:00','#21 match all 4 (Sunday, redo at swap)',SL,["Pause and match all 4 to reveal your guild 🧪"],(410584672,'1044777846732964845'),(410584747,'5915602327956835424'),(410584765,'8480257410822784165'))
add('2026-11-01 19:00','#11 guess the guide (Sunday, redo at swap)',SL,["Guess the guide from the silhouette 🔍"],(410684969,'2511962048508412534'),(410685019,'1556468952809951105'),(410685057,'-6719652054135387668'))
add('2026-11-01 22:00','#23 rank the guides (Sunday, redo at swap)',SL,["Rank the guides 🏆"],(410685093,'5066140752340402810'),(410685128,'5371251837746957321'),(410685158,'-5278142475389155176'))
add('2026-11-02 10:00','#34 find the gummy',SL,["Find the gummy 👀"],(410597496,'-8888055009249506595'),(410597569,'-309192829646582712'),(410597616,'8686013892787390039'))
add('2026-11-02 12:00','Rayleigh take 2 (art)',S,["Rayleigh, take 2 🌙","The Recovery guide, robe, hat and staff. Take 1 had none of those."],(409329201,'5341269815569238779'),(409329096,'178494995058607376'),(409329157,'1829939251412616436'),kind='art')
add('2026-11-02 13:00','extra life still',S,["Still waiting on the extra life 🍄"],(409347491,'7156879603827231272'),(409347439,'2397769531115785924'),None,kind='still',tt_title_mode='first')
add('2026-11-02 16:00','#26 gummy in the bottle',SL,["Put the gummy in the bottle 🌙","Pause when it drops in."],(410585139,'-9160926125426192436'),(410585197,'6453445702669189790'),(410585240,'-3320675575384423286'))
add('2026-11-02 19:00','#35 outruns the dark',SL,["Who outruns the dark? 🌑","Pick a guide before the dark catches up."],(410685263,'-4470537398867112903'),(410685305,'5597509786806995516'),(410685343,'6519026837465678175'))
add('2026-11-02 22:00','#27 +1 XP a day',SL,["+1 XP a day 📈"],(410685517,'-7637199920589485598'),(410685551,'929375747629402942'),(410685591,'4096468882230693599'))
add('2026-11-03 10:00','#38 gummy fits the outline',S,["Which gummy fits the outline? 🧩"],(410590009,'-8273041079796807053'),(410590065,'-4730698616007080987'),(410590114,'-4183701852652941883'))
add('2026-11-03 12:00',"Joy's trading card take 2 (art)",S,["Joy's trading card, take 2 🃏","The Foundation card from our intro pack."],(409329849,'36001204994917712'),(409329727,'7278962990417005347'),(409329779,'1614552896100123576'),kind='art',music="🎵 Running Waters by Jason Shaw, CC BY 3.0")
add('2026-11-03 13:00','Vitality Guild carousel',S,["First member of the Vitality Guild 🛡️"],(409347633,'2767722843641236356'),(409347559,'-3071802142122360809'),None,kind='still',tt_title_mode='first')
add('2026-11-03 16:00','#30 screenshot the fit',SL,["Screenshot the second the gummy fits perfectly 📸"],(410590181,'-1733379654550272796'),(410590231,'-4373138547466481873'),(410590296,'656691282945132011'))
add('2026-11-03 19:00','#13 jackpot',SL,["Only 1% can stop it on the jackpot 🎰","Pause when all 3 match."],(410685801,'3393374402934949656'),(410685847,'4617121966184285533'),(410685884,'387947675814283719'))
add('2026-11-03 22:00','#40 NPCs blocking',SL,["NPCs blocking the only path 🛡️"],(410686062,'701545873954130516'),(410686107,'-2184200079581560087'),(410686184,'4319904885249820268'))
add('2026-11-04 10:00','#44 glowing gummy',SL,["Lock your eyes on the glowing gummy 👀"],(410590585,'-3310459806068028263'),(410590665,'-7775538890005265717'),(410590717,'6932549734447661614'))
add('2026-11-04 12:00','Side Quest dragon take 2 (art)',S,["The Side Quest dragon, take 2 🐉"],(409330205,'-5537714003631718204'),(409329928,'-2926121914980414886'),(409350577,'2367546411571234330'),kind='art')
add('2026-11-04 13:00','one dungeon still',S,["it was supposed to be one dungeon"],(409347759,'7834342740923993156'),(409347713,'-4101330567569521919'),None,kind='still',tt_title_mode='first')
add('2026-11-04 16:00','#36 pause on 99',SL,["Pause the video on 99 ⏸️"],(410597675,'3018972214036808900'),(410597733,'3652536971168728522'),(410597790,'3394283695592918597'))
add('2026-11-04 19:00','#32 Hollow eats the glass',SL,["The Hollow eats all the glass 🪞","Guess what's behind it before it's gone."],(410686357,'-4660382989924809576'),(410686391,'5085651568741927021'),(410686416,'-5434695878919633175'))
add('2026-11-04 22:00','#43 save point',SL,["Finally made it to a save point 💾","You're doing better than you think."],(410686523,'4487291682382823875'),(410686550,'7231203008004833877'),(410686577,'1851498649050366465'))
add('2026-11-05 10:00','#49 odd gummy',SL,["Find the odd gummy in 5 seconds ⏱️"],(410598013,'106711878710084345'),(410598074,'-6026485148707567091'),(410598127,'-5971828652637664524'))
add('2026-11-05 12:00','Hollow from the side take 2 (art)',S,["The Hollow from the side, take 2 🌑","Still no face. That part was on purpose."],(409330849,'6897589261911608242'),(409330744,'-2071679756826292891'),(409330777,'3828664284631550428'),kind='art')
add('2026-11-05 13:00','last game still',S,['The friend who says "last game" 🎮'],(409347869,'1716999453810377929'),(409347816,'-6398768404616491413'),None,kind='still',tt_title_mode='first')
add('2026-11-05 16:00','#42 both fit',SL,["Pause when both fit perfectly ⏸️","Noob, Pro, Hacker or God."],(410598168,'-7578991614787434160'),(410598214,'7499483337266905672'),(410598258,'-971767604599500962'))
add('2026-11-05 19:00','#82 Hollow escape',SL,["Can the Hollow escape? 🧱","Every bounce adds a brick."],(410686699,'-8085980699959934480'),(410686734,'-8150698600551528896'),(410686767,'-6518493386876367604'))
add('2026-11-05 22:00','#45 which guild',SL,["Which guild are you? 🛡️","Pick one each round and count your colors."],(410686816,'899908999691454047'),(410686859,'-7124578912112129109'),(410686896,'-5172556106960057370'))
add('2026-11-06 10:00','#57 how many Hollows',SL,["How many Hollows do you see? 👀"],(410611058,'-5123437207201758341'),(410611084,'4053864206726482469'),(410611145,'-7467225618325748013'))
add('2026-11-06 12:00','label take 2 (art)',S,["Label art, take 2 🫐"],(409331091,'1892104864351275412'),(409330958,'4390473052366326468'),(409331022,'-2777841507169057764'),kind='art',music="🎵 River Meditation by Jason Shaw, CC BY 3.0")
add('2026-11-06 13:00','gains still',S,["gains are gains 💀"],(409347992,'-7517600508263840116'),(409347933,'2626141621903970083'),None,kind='still',tt_title_mode='first')
add('2026-11-06 16:00','#75 nail it, shield',SL,["Think you can nail it? Only 0.1% can 🎯","Pause when the gummy fits the shield."],(410611197,'-5128651624726312865'),(410611240,'-4349650838467492648'),(410611289,'-7196876331486002155'))
add('2026-11-06 19:00','#51 pick your marble',SL,["Pick your marble: Cleo or Cyrus 🔵🟠"],(410755929,'-3517147925650389359'),(410755960,'6618200257437452482'),(410755994,'8934328923612725910'))
add('2026-11-06 22:00','#47 motivation vs discipline',SL,["Motivation vs discipline 🔥"],(410687012,'-5233507156924022222'),(410687052,'-7402576938537565419'),(410687079,'222200760679679551'))
add('2026-11-07 10:00','#60 only 1 difference',SL,["Only 1 difference 🛡️"],(410611529,'1600309899301046323'),(410611569,'-5691332725087320665'),(410611854,'-8956085240180358581'))
add('2026-11-07 12:00','Joy and the Hollow take 2 (art)',S,["Joy and the Hollow, take 2 🌿","The Foundation guide shares a gummy."],(409331271,'8564357741251413559'),(409331169,'-4520557662751866713'),(409331212,'-8392233101589723077'),kind='art')
add('2026-11-07 13:00','side quests or main story still',S,["Side quests or main story? Wrong answers only"],(409348087,'-6466153305697467421'),(409348054,'-2591941231425928952'),None,kind='still',tt_title_mode='first')
add('2026-11-07 16:00','#83 mirrors',SL,["Pause when it perfectly mirrors ⏸️"],(410612164,'4141610263427433503'),(410612221,'-3817291134180965439'),(410612274,'2475957203923583464'))
add('2026-11-07 19:00','#100 first to the top',SL,["First to the top wins ☁️","Pick your climber."],(410687258,'6980890155538008212'),(410687287,'5766170802850710322'),(410687316,'-1969870174742492247'))
add('2026-11-07 22:00','#90 slimes',SL,["Slimes eat all the glass 🟢"],(410687445,'4516983477474772743'),(410687496,'8984543860404994127'),(410687528,'5695377895361562337'))
add('2026-11-08 12:00','Royal Castle take 2 (art)',L,["The Royal Castle, take 2 🏰","Take 1 was mostly a rectangle."],(409332232,'6861039834409026200'),(409332150,'4486069457587357400'),(409332195,'4829139350625537588'),kind='art',music="🎵 Elk by Meydän, CC BY 4.0")
add('2026-11-08 13:00','open or sealed still',S,["Open it or keep it sealed? 🃏"],(409348261,'-1842586289645334704'),(409348202,'1171213493849180808'),None,kind='still',tt_title_mode='first')
add('2026-11-08 16:00','#87 all 3 fit',SL,["Pause when all 3 gummies fit ⏸️","99% fail."],(410613034,'-1259610357128280092'),(410613077,'3740019658535620019'),(410613127,'-5364892003193238071'))
add('2026-11-08 22:00',"#95 Joy's charm",SL,["Build Joy's perfect charm 🌿"],(410687665,'-6213177193154461559'),(410687699,'-5785903962576500491'),(410687733,'-8885998527826278982'))
add('2026-11-09 12:00','Cyrus victory pose take 2 (art)',S,["Cyrus's victory pose, take 2 ☀️","The Energy guide, fist up."],(409332468,'7141178493040871242'),(409332364,'1954661235138839348'),(409332411,'-3078046264533235018'),kind='art')
add('2026-11-09 13:00','merchant still',S,["The one item you'd never sell to the merchant 🪙"],(409348371,'3374083545755568562'),(409348317,'1816390821018617177'),None,kind='still',tt_title_mode='first')
add('2026-11-09 16:00','#96 digger',SL,["Choose your digger ⛏️"],(410687837,'-7433231415171004530'),(410687900,'-3221360688201774498'),(410687923,'-7414889214370361369'))
add('2026-11-09 19:00','#93 3 gummies, powers on',SL,["Whoever gets 3 gummies wins, powers on ⚡"],(410687950,'-109483205016533647'),(410687982,'-7084830465344843791'),(410688030,'-8091916547753882187'))
add('2026-11-09 22:00','#72 watch carefully',SL,["Watch carefully 👀","One Cleo has the gummy. A, B or C?"],(410688060,'5081543152392097249'),(410688094,'6328059159889857373'),(410688123,'308975357557031028'))

# Oct 31 recreations, labeled by reel (slot assigned later). No ids yet.
REC = [
 dict(reel='r01 race (obstacle race over water)', credit=S, lines=["Who makes it across first? 🌊","Floating pads, ropes, monkey bars and one slime causing problems."]),
 dict(reel='m01 box maze', credit=S, lines=["Who escapes the shadow? 🌑","Four guides, one brick maze, and the shadow is flooding in."]),
 dict(reel='m05 number wall', credit=S, lines=["Who breaks through first? 🧱","66 hits to bring the wall down, and one STRENGTH gummy up for grabs."]),
 dict(reel='m06 stairs', credit=S, lines=["Who outruns the water? 🌊","Up the stairs, don't touch the pencil tips, first to the top wins."]),
]

GIVE = [
 "We're giving away a Nintendo Switch 2 on Feb 1, free to enter.",
 "Nintendo Switch 2 giveaway on Feb 1. No purchase needed.",
 "A Nintendo Switch 2 goes to one of you on Feb 1, and entry is free.",
 "Switch 2 on the line Feb 1. One free entry puts your marble in every monthly race.",
 "Nintendo Switch 2 giveaway, Feb 1. Free to enter, US only, 18+.",
 "One Nintendo Switch 2, up for grabs Feb 1. Entry is free.",
 "Nintendo Switch 2, Feb 1. Free to enter, and your marble races every month.",
 "Win a Nintendo Switch 2 on Feb 1. It's free to get in.",
]
CTA_FB = [
 "Comment QUEST and we'll DM you the link 🎁",
 "Comment QUEST and the link lands in your DMs.",
 "Comment QUEST and we'll send the link to your DMs 🎁",
 "Comment QUEST below and we'll DM you the entry link.",
 "Comment QUEST for the link, we'll DM it to you 🎁",
]
CTA_TT = [
 "DM us QUEST for the link 🎁",
 "DM us QUEST and we'll send you the link.",
 "DM us QUEST for the entry link 🎁",
]
PIN = [  # restates giveaway for a no-context reader; CTA appended
 "Nintendo Switch 2 giveaway, Feb 1. Free to enter.",
 "We're giving away a Nintendo Switch 2 on Feb 1. Free, no purchase, US only, 18+.",
 "Switch 2 giveaway on Feb 1. One free entry puts a marble with your name in every monthly race.",
 "Nintendo Switch 2 up for grabs Feb 1, free to enter. Five heat winners each month also get a founder box.",
 "Our first grand prize is a Nintendo Switch 2 on Feb 1. Entry is free, no purchase needed.",
 "Nintendo Switch 2 on Feb 1. It's free to enter, US only, 18+.",
]

def build(i, item, has_ids=True):
    vlines = list(item['lines'])
    pre = []
    if item.get('credit'): pre.append(item['credit'])
    if item.get('music'): pre.append(item['music'])
    g = GIVE[i % len(GIVE)]
    cf = CTA_FB[(i * 3 + 1) % len(CTA_FB)]
    ct = CTA_TT[i % len(CTA_TT)]
    k = (i * 5 + 2) % len(PIN)
    # keep the pinned comment from echoing the caption's giveaway line
    while PIN[k].split()[:3] == g.split()[:3] or PIN[k].split(',')[0] == g.split(',')[0]:
        k = (k + 1) % len(PIN)
    pin = PIN[k]
    fb_cap = "\n".join(vlines + pre + [g, cf])
    fb_pin = pin + "\n" + cf
    tt_cap = "\n".join(vlines + pre + [g, ct])
    tt_pin = pin + "\n" + ct
    yt_cap = "\n".join(vlines + pre)
    yt_pin = item['credit'] or ""
    if item.get('tt_title_mode') == 'first':
        tt_title = vlines[0]
    else:
        tt_title = tt_cap
    return dict(fb_cap=fb_cap, fb_pin=fb_pin, tt_cap=tt_cap, tt_pin=tt_pin, tt_title=tt_title, yt_cap=yt_cap, yt_pin=yt_pin)

OLD = json.load(open(os.path.join(os.path.dirname(__file__), 'old_first.json'))) if os.path.exists(os.path.join(os.path.dirname(__file__), 'old_first.json')) else {}

out = []
md = ["# Caption v2 drafts (CAPTIONS_QUEST_v2.md), built Oct 30 2026",
      "",
      "Scope: every non-draft scheduled post Oct 30 7:00pm ET through Nov 9 (draft=true posts left out). Oct 31 10:00, 16:00, 19:00 and 22:00 reel slots are replaced by the recreation reels below (labeled by reel, no slot). Sunday Nov 1 reel slots are drafted as normal and will be redone at swap time.",
      "Lines are separated by real line breaks. Nothing has been pushed to Metricool.",
      ""]
for i, it in enumerate(P):
    c = build(i, it)
    rec = dict(it); rec.update(c); out.append(rec)
    md.append(f"## {it['slot']} | {it['reel']}")
    md.append(f"Art credit: {it['credit'] or 'none'}" + (f" | CC BY music kept: {it['music']}" if it['music'] else ""))
    md.append("")
    md.append(f"### FB+IG (id {it['fbig'][0]}, uuid {it['fbig'][1]})")
    md.append(f"Old caption first line: {OLD.get(str(it['fbig'][0]), it['lines'][0])}")
    md.append("Caption:\n```\n" + c['fb_cap'] + "\n```")
    md.append("Pinned comment:\n```\n" + c['fb_pin'] + "\n```")
    md.append(f"### TikTok (id {it['tt'][0]}, uuid {it['tt'][1]})")
    md.append("Caption:\n```\n" + c['tt_cap'] + "\n```")
    md.append("Pinned comment:\n```\n" + c['tt_pin'] + "\n```")
    md.append("TikTok title: " + ("same as caption" if c['tt_title'] == c['tt_cap'] else f"`{c['tt_title']}`"))
    if it['yt']:
        md.append(f"### YouTube (id {it['yt'][0]}, uuid {it['yt'][1]}); youtubeData title unchanged")
        md.append("Caption:\n```\n" + c['yt_cap'] + "\n```")
        md.append("First comment:\n```\n" + c['yt_pin'] + "\n```")
    md.append("")

md.append("# Oct 31 recreation reels (slot assigned at review; new posts or edits at swap time)")
md.append("")
for j, it in enumerate(REC):
    c = build(len(P) + j, it)
    rec = dict(it); rec.update(c); rec['slot'] = 'Oct 31 (TBD)'; out.append(rec)
    md.append(f"## {it['reel']}")
    md.append(f"Art credit: {it['credit']} (Syeda only by default; add Liza only if Bennett confirms her art is in it)")
    md.append("### FB+IG\nCaption:\n```\n" + c['fb_cap'] + "\n```")
    md.append("Pinned comment:\n```\n" + c['fb_pin'] + "\n```")
    md.append("### TikTok\nCaption (and title):\n```\n" + c['tt_cap'] + "\n```")
    md.append("Pinned comment:\n```\n" + c['tt_pin'] + "\n```")
    md.append("### YouTube\nCaption:\n```\n" + c['yt_cap'] + "\n```")
    md.append("First comment:\n```\n" + c['yt_pin'] + "\n```")
    md.append("")

json.dump(out, open(OUT_JSON, 'w'), ensure_ascii=False, indent=1)
open(OUT_MD, 'w').write("\n".join(md) + "\n")
n_posts = sum(2 + (1 if it['yt'] else 0) for it in P)
print('slots', len(P), 'existing posts', n_posts, 'recreation reels', len(REC))
