import json, collections
P,G="personal","generic"
rows=[
# email, first, last, position, company, domain, type, verification, evidence
("erodriguez@tampabay.com","Evan","Rodriguez","Food & dining writer (Hunter label: Partner)","Tampa Bay Times","tampabay.com",P,"valid","https://tbt-tbt-prod.web.arc-cdn.net/author/evan-rodriguez"),
("rroa@cltampa.com","Ray","Roa","Editor-in-Chief","Creative Loafing Tampa Bay","cltampa.com",P,"valid","https://muckrack.com/ray-roa"),
("selene@cltampa.com","Selene","Felice","Managing Editor","Creative Loafing Tampa Bay","cltampa.com",P,"valid","https://www.linkedin.com/in/selenesanfelice"),
("kyla@cltampa.com","Kyla","Fetch","Food & drink writer (Hunter label: Bartender)","Creative Loafing Tampa Bay","cltampa.com",P,"valid","https://cltampa.com/food-drink/the-painfully-delicious-i-like-it-hot-festival-returns-to-largo-18478250"),
("josh@cltampa.com","Josh","Bradley","Unknown (no title in Hunter)","Creative Loafing Tampa Bay","cltampa.com",P,"valid","https://andy-harrislegalfirm.com/index-56.html"),
("bill@stpetecatalyst.com","Bill","DeYoung","Senior Writer and Editor","St Pete Catalyst","stpetecatalyst.com",P,"valid","https://stpetecatalyst.com/weekend-spotlight-new-plays-buffetts-boys-and-sellouts"),
("michael@stpetecatalyst.com","Michael","Connor","Business reporter (inferred from bylines; no title in Hunter)","St Pete Catalyst","stpetecatalyst.com",P,"valid","https://stpetecatalyst.com/bayfirst-names-al-rogers-as-new-ceo"),
("spark@stpetecatalyst.com","","","Contributor / content submissions inbox","St Pete Catalyst","stpetecatalyst.com",G,"valid","https://stpetecatalyst.com/contribute/independents"),
("editor@83degreesmedia.com","","","Editor inbox (listed on tips page)","83 Degrees Media","83degreesmedia.com",G,"valid","https://83degreesmedia.com/about/tips.aspx"),
("feedback@83degreesmedia.com","","","Feedback / story ideas inbox","83 Degrees Media","83degreesmedia.com",G,"valid","https://tamiamiangels.com/press/3-things-tampa-bay-needs-to-help-startups-thrive/archives"),
("info@ilovetheburg.com","","","General / editorial inbox","I Love the Burg","ilovetheburg.com",G,"valid","https://ilovetheburg.com/about"),
("kaylen@ilovetheburg.com","Kaylen","Ross","Social Media Content Creator","I Love the Burg","ilovetheburg.com",P,"valid","https://www.linkedin.com/in/kaylenross"),
("info@thatssotampa.com","","","General / editorial inbox","That's So Tampa","thatssotampa.com",G,"valid","https://thatssotampa.com/a-tiny-home-village-is-open-in-tampa"),
("cmerlis@tbbwmag.com","Chuck","Merlis","Managing Editor","Tampa Bay Business and Wealth","tbbwmag.com",P,"accept_all","https://tbbwmag.com/meet-the-team"),
("mmikuliza@tbbwmag.com","","","Feature writer (inferred from byline; no name/title in Hunter)","Tampa Bay Business and Wealth","tbbwmag.com",P,"accept_all","https://tbbwmag.com/2021/04/08/a-slice-of-sicily-in-the-heart-of-ybor-city"),
("bbello@tbbwmag.com","Bridgette","Bello","Founder / Publisher (inferred; no name/title in Hunter)","Tampa Bay Business and Wealth","tbbwmag.com",P,"valid","https://spinutech.com/resources/podcasts/bridgette-bello"),
("jbaker@tbbwmag.com","Jason","Baker","President / Associate Publisher","Tampa Bay Business and Wealth","tbbwmag.com",P,"valid","https://tbbwmag.com/2025/09/03/ceo-connect-recap-bob-stahl-talks-about-legacy-and-company-culture"),
("editor@tampabaymagazine.com","","","Editor inbox","Tampa Bay Magazine","tampabaymagazine.com",G,"valid","https://tampabaymagazine.com"),
("bcallahan@wfla.com","Brian","Callahan","Director of News and Digital Content","WFLA News Channel 8","wfla.com",P,"valid","https://www.linkedin.com/in/briancallahan3"),
("dciliberti@wfla.com","David","Ciliberti","News Director","WFLA News Channel 8","wfla.com",P,"valid","https://www.linkedin.com/in/davidciliberti"),
("cseitz@wfla.com","Colleen","Seitz","Digital Director","WFLA News Channel 8","wfla.com",P,"valid","https://www.linkedin.com/in/colleenseitz"),
("jleigh@wfla.com","Jen","Leigh","Reporter / Anchor","WFLA News Channel 8","wfla.com",P,"valid","https://www.linkedin.com/in/jen-leigh-52816a10"),
("desk@wtsp.com","","","Newsroom assignment desk","WTSP 10 Tampa Bay","wtsp.com",G,"valid","https://threadreaderapp.com/user/10tampabay"),
("tips@wtsp.com","","","News tips inbox","WTSP 10 Tampa Bay","wtsp.com",G,"valid","https://fentanyl.pro/fentanyl/1-dead-14-hospitalized-after-mass-overdose-california-police-say"),
("mrancourt@wtsp.com","","","Lifestyle segment contact (inferred from Great Day Live 'Fitness Friday'/gadget segment credits; no name/title in Hunter)","WTSP 10 Tampa Bay","wtsp.com",P,"valid","https://grandmashealthykidsclub.com/fitness-friday-sexy-arms-wtsp-com"),
("cjadick@abcactionnews.com","Chris","Jadick","News Director","ABC Action News (WFTS)","abcactionnews.com",P,"accept_all","https://www.linkedin.com/in/chris-jadick-743069b"),
("joey.west@baynews9.com","Joey","West","Planning Editor","Spectrum Bay News 9","baynews9.com",P,"accept_all","https://www.linkedin.com/in/joey-west-6708a31a"),
("eric.eraso@baynews9.com","Eric","Eraso","Reporter / author (Hunter label: Author)","Spectrum Bay News 9","baynews9.com",P,"accept_all","https://med.ucf.edu/news/bay-news-9-new-ucf-clinic-aims-to-serve-pilots-near-orlando-international-airport"),
("akeller@floridatrend.com","Amy","Keller","Executive Editor","Florida Trend","floridatrend.com",P,"valid","https://floridatrend.com/people/amy-keller"),
("mbrassfield@floridatrend.com","Mike","Brassfield","Managing Editor","Florida Trend","floridatrend.com",P,"valid","https://floridatrend.com/people/mike-brassfield"),
("news@floridatrend.com","","","News inbox (contact page)","Florida Trend","floridatrend.com",G,"valid","https://floridatrend.com/contact"),
("mfechter@floridatrend.com","Michael","Fechter","Associate Editor","Florida Trend","floridatrend.com",P,"valid","https://floridatrend.com/people/michael-fechter"),
("bhartz@floridatrend.com","Brian","Hartz","Associate Editor","Florida Trend","floridatrend.com",P,"valid","https://floridatrend.com/people/brian-hartz"),
("anthony@stpeterising.com","Anthony","Close","Founder & Co-owner","St Pete Rising","stpeterising.com",P,"valid","https://stpeterising.com/team"),
("veronica@stpeterising.com","Veronica","Brezina","Reporter","St Pete Rising","stpeterising.com",P,"valid","https://stpeterising.com"),
("press@stpeterising.com","","","Press inbox (contact page)","St Pete Rising","stpeterising.com",G,"valid","https://stpeterising.squarespace.com/contact"),
("brian@stpeterising.com","Brian","Zucker","Team member, likely co-owner (Hunter label: Consulting Actuary)","St Pete Rising","stpeterising.com",P,"valid","https://stpeterising.com/team"),
("laura@tampabayparenting.com","Laura","Byrne","Managing Editor, Owner","Tampa Bay Parenting Magazine","tampabayparenting.com",P,"valid","https://www.linkedin.com/in/laura-byrne-23895a9"),
("brie@tampabayparenting.com","Brie","Gorecki","Associate Editor","Tampa Bay Parenting Magazine","tampabayparenting.com",P,"valid","https://www.helpareporter.com/journalist/brie-gorecki"),
("editorial@tbnweekly.com","","","Editorial / news tips inbox","Tampa Bay Newspapers (Tampa Bay Beacons)","tbnweekly.com",G,"valid","https://tampabaybeacons.com/newstips"),
("clane@tbnweekly.com","","","Reporter, Manatee coverage (inferred from bylines; no name in Hunter)","Tampa Bay Newspapers (Tampa Bay Beacons)","tbnweekly.com",P,"valid","https://tampabaybeacons.com/2026/06/22/house-concerts-take-the-backyard-stage-in-parrish"),
("bputnam@tbnweekly.com","","","Reporter, Hernando retail/business (inferred from byline; no name in Hunter)","Tampa Bay Newspapers (Tampa Bay Beacons)","tbnweekly.com",P,"valid","https://tampabaybeacons.com/2026/04/14/new-publix-opens-on-mariner-boulevard-in-spring-hill"),
("mbaker@tbnweekly.com","","","Unknown (listed on contact page; no name/title in Hunter)","Tampa Bay Newspapers (Tampa Bay Beacons)","tbnweekly.com",P,"valid","https://tampabaybeacons.com/contact"),
("jbennett@ospreyobserver.com","Jenny","Bennett","Business Editor","Osprey Observer","ospreyobserver.com",P,"valid","https://ospreyobserver.com/about-us/our-team"),
("twells@ospreyobserver.com","Taylor","Wells","News Reporter","Osprey Observer","ospreyobserver.com",P,"valid","https://ospreyobserver.com/about-us/our-team/meet-taylor-wells"),
("kcollins@ospreyobserver.com","Kathy","Collins","Founder","Osprey Observer","ospreyobserver.com",P,"valid","https://ospreyobserver.com/about-us"),
("jowen@ospreyobserver.com","Jane","Owen","Freelance Writer","Osprey Observer","ospreyobserver.com",P,"valid","https://ospreyobserver.com/about-us/our-team"),
("libby@ospreyobserver.com","Libby","Hopkins","Freelance Writer","Osprey Observer","ospreyobserver.com",P,"valid","https://ospreyobserver.com/2012/11/crazy-for-pumpkin-during-the-holidays"),
("julioochoa@wusf.org","Julio","Ochoa","Editorial Director","WUSF Public Media","wusf.org",P,"accept_all","https://wusf.org/contactus"),
("shedden@wusf.org","Mary","Shedden","News Director","WUSF Public Media","wusf.org",P,"accept_all","https://wusf.org/people/mary-shedden"),
("mpeddie@wusf.org","Matt","Peddie","Host, Florida Matters","WUSF Public Media","wusf.org",P,"accept_all","https://wusf.org/podcast/florida-matters/2026-08-06/breaking-down-whats-new-for-the-school-year-improv-takes-center-stage-ybor"),
]
keys=["email","first_name","last_name","position","company","domain","type","verification","evidence_url"]
out=[dict(zip(keys,r)) for r in rows]
used=set(open('/home/claude/hunter/used_domains_all.txt').read().split())
assert not any(o['domain'] in used for o in out)
assert len({o['email'] for o in out})==len(out)
c=collections.Counter(o['domain'] for o in out); assert max(c.values())<=5
json.dump(out,open('/home/claude/hunter/wk4_local.json','w'),indent=2)
print(len(out)); print(dict(c)); print(collections.Counter(o['verification'] for o in out)); print(collections.Counter(o['type'] for o in out))
