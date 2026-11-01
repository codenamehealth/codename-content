import json
H="/home/claude/hunter/"
used={l.strip().lower() for l in open(H+"used_domains_all.txt") if l.strip()}
wk4={r["email"].lower() for r in json.load(open(H+"wk4_local_load.json"))}
P,G="personal","generic"
R=[
# email, first, last, position, company, domain, type, verification, evidence
("meganm@sarasotamagazine.com","Megan","McDonald","Managing Editor","Sarasota Magazine","sarasotamagazine.com",P,"valid","https://sarasotamagazine.com/pages/about"),
("kim@sarasotamagazine.com","Kim","Doleatto","Writer","Sarasota Magazine","sarasotamagazine.com",P,"valid","https://sarasotamagazine.com"),
("info@sarasotamagazine.com","","","General inbox","Sarasota Magazine","sarasotamagazine.com",G,"valid","https://bookmarketingbestsellers.com/regional-and-local-magazines"),
("rballogg@bradenton.com","Ryan","Ballogg","Associate Editor","Bradenton Herald","bradenton.com",P,"valid","https://bradenton.com/customer-service/contact-us"),
("rcallihan@bradenton.com","Ryan","Callihan","Senior Editor","Bradenton Herald","bradenton.com",P,"valid","https://bradenton.com/customer-service/contact-us"),
("metro@bradenton.com","","","Metro news desk","Bradenton Herald","bradenton.com",G,"valid","https://bradenton.com/latest-news/article113244248.html"),
("kwingert@yourobserver.com","Kat","Wingert","Executive Editor & COO","Observer Media Group (Sarasota/East County Observer)","yourobserver.com",P,"valid","https://observermediagroupinc.com/leadership"),
("khughes@businessobserverfl.com","Kat","Hughes","Executive Editor","Business Observer","businessobserverfl.com",P,"valid","https://talkingbiznews.com/biz-news-help-wanted/tampa-biz-newspaper-seeks-real-estate-reporter"),
("mgordon@businessobserverfl.com","Mark","Gordon","Managing Editor","Business Observer","businessobserverfl.com",P,"valid","https://observermediagroupinc.com/publication/business-observer"),
("lllovio@businessobserverfl.com","Louis","Llovio","Deputy Managing Editor","Business Observer","businessobserverfl.com",P,"valid","https://lqcre.com/tampa-bay-investor-pays-43-million-for-fort-myers-apartment"),
("adawson@businessobserverfl.com","Anastasia","Dawson","Reporter","Business Observer","businessobserverfl.com",P,"valid","https://www.linkedin.com/in/anastasia-dawson-34b13636"),
("eking@businessobserverfl.com","Elizabeth","King","Reporter","Business Observer","businessobserverfl.com",P,"valid","https://www.linkedin.com/in/elizabeth-king-1a1449389"),
("carrie.seidman@heraldtribune.com","Carrie","Seidman","Arts writer / columnist","Sarasota Herald-Tribune","heraldtribune.com",P,"accept_all","https://www.linkedin.com/in/carrie-seidman-44037b28"),
("chris.anderson@heraldtribune.com","Chris","Anderson","Reporter / columnist","Sarasota Herald-Tribune","heraldtribune.com",P,"accept_all","https://marklipinski.blogspot.com/2016/07/sarasota-herald-tribune.html"),
("tom.lyons@heraldtribune.com","Tom","Lyons","News columnist","Sarasota Herald-Tribune","heraldtribune.com",P,"accept_all","https://www.linkedin.com/in/tom-lyons-5249265"),
("andy.kuppers@theledger.com","Andy","Kuppers","Assistant Managing Editor","The Ledger (Lakeland)","theledger.com",P,"accept_all","https://www.linkedin.com/in/andy-kuppers-1a7084b3"),
("lynne.maddox@theledger.com","Lynne","Maddox","Assistant Managing Editor (Polk business news listings)","The Ledger (Lakeland)","theledger.com",P,"accept_all","https://theledger.com/news/20090727/new-businesses"),
("gary.white@theledger.com","Gary","White","Reporter","The Ledger (Lakeland)","theledger.com",P,"accept_all","https://mystorycontinues.com/press/young-lakeland-womans-heart-beats-for-another-after-her-tragic-death"),
("robin.adams@theledger.com","Robin","Adams","Senior Reporter (health)","The Ledger (Lakeland)","theledger.com",P,"accept_all","https://www.linkedin.com/in/robin-adams-56369428"),
("barry@lkldnow.com","Barry","Friedman","Editor at Large","LkldNow","lkldnow.com",P,"valid","https://lakelandvision.org/barry-friedman-of-lkldnow-awarded-lakeland-visions-cygnet-award"),
("anna@lkldnow.com","Anna","Toms","Journalist and Newsroom Lead","LkldNow","lkldnow.com",P,"valid","https://www.linkedin.com/in/annatoms"),
("cindy@lkldnow.com","Cindy","Glover","Reporter","LkldNow","lkldnow.com",P,"valid","https://www.lkldnow.com/author/cindy-glover/"),
("newstips@lkldnow.com","","","News tips inbox","LkldNow","lkldnow.com",G,"valid","https://lkldnow.com/lkldnow-selected-for-newsmatch-initiative"),
("jyoung@orlandoweekly.com","Jessica","Young","Editor-in-Chief","Orlando Weekly","orlandoweekly.com",P,"valid","https://feaweb.org/issues/write-a-letter-to-the-editor"),
("feedback@orlandoweekly.com","","","Editorial feedback inbox","Orlando Weekly","orlandoweekly.com",G,"valid","https://orlandoweekly.com/orlando/faqs/page"),
("michele.walker@orlandomagazine.com","Michele","Walker","Editor","Orlando Magazine","orlandomagazine.com",P,"accept_all","https://orlandomagazine.com/editor-letter-burgers-goblins-and-the-50-most-powerful"),
("jennifer.mckee@orlandomagazine.com","Jennifer","McKee","Editorial staff (title not listed; on editor-letter and contact pages)","Orlando Magazine","orlandomagazine.com",P,"accept_all","https://orlandomagazine.com/editor-letter-for-june-all-hail-the-independents"),
("mike.boslet@orlandomagazine.com","Mike","Boslet","Writer/editor (title not listed; business feature bylines)","Orlando Magazine","orlandomagazine.com",P,"accept_all","https://orlandomagazine.com/if-they-build-it-2"),
("lkinsler@growthspotter.com","Laura","Kinsler","Editor","GrowthSpotter","growthspotter.com",P,"valid","https://maurycarter.com/narcoossee-investor-looking-to-expand-commercial-site-at-cyrils-growthspotter"),
("newsroom@growthspotter.com","","","Newsroom inbox","GrowthSpotter","growthspotter.com",G,"valid","https://growthspotter.com/contact-us"),
("peter@floridapolitics.com","Peter","Schorsch","Publisher","Florida Politics","floridapolitics.com",P,"valid","https://thecapitolist.com/mediaguide"),
("drew@floridapolitics.com","Drew","Wilson","Vice President","Florida Politics","floridapolitics.com",P,"valid","https://floridapolitics.com/archives/465440-personnel-note-andrew-kalel-joins-sunrise-consulting-group"),
("celia.almeida@miaminewtimes.com","Celia","Almeida","Culture Editor","Miami New Times","miaminewtimes.com",P,"valid","https://miaminewtimes.com/about/staff"),
("tom.finkel@miaminewtimes.com","Tom","Finkel","Editor in Chief","Miami New Times","miaminewtimes.com",P,"valid","https://miaminewtimes.com/author/tom-finkel"),
("sean@wmnf.org","Seán","Kinane","Director, News & Public Affairs","WMNF 88.5 FM","wmnf.org",P,"valid","https://wmnf.org/hosts/sean-kinane-2"),
("randy@wmnf.org","Randy","Wynne","Program Director / Morning Show host","WMNF 88.5 FM","wmnf.org",P,"valid","https://wmnf.org/hosts/randy-wynne"),
("cbennett@lakerlutznews.com","Carolyn","Bennett","Staff Writer","The Laker/Lutz News","lakerlutznews.com",P,"valid","https://saintpaulsepiscopalchurch.org/wp-content/uploads/TheLakerNews_STPRibbonCutting_February16_2021.pdf"),
("news@lakerlutznews.com","","","News inbox","The Laker/Lutz News","lakerlutznews.com",G,"valid","https://saintpaulsepiscopalchurch.org/wp-content/uploads/TheLakerNews_STPRibbonCutting_February16_2021.pdf"),
("summer@hernandosun.com","Summer","Hampton","Assistant Editor / Community Reporter","Hernando Sun","hernandosun.com",P,"valid","https://hernandosun.com/2021/01/25/sports-news-bites"),
("mhussey@hernandosun.com","Megan","Hussey","Community Reporter","Hernando Sun","hernandosun.com",P,"valid","https://hernandosun.com/2020/10/24/show-us-your-sunshine-food-drive-competition-honor-friend"),
("noelle@hernandosun.com","Noelle","Pappas","Staff Writer","Hernando Sun","hernandosun.com",P,"valid","https://www.linkedin.com/in/noelle-pappas-591158257"),
("hanna@hernandosun.com","Hanna","Maglio","Staff Writer and Photographer","Hernando Sun","hernandosun.com",P,"valid","https://www.linkedin.com/in/hannamaglio"),
("tim@embarccollective.com","Tim","Holcomb","CEO","Embarc Collective","embarccollective.com",P,"valid","https://tampabay.tech/2024/09/09/tim-holcombs-experience-vision-set-to-guide-embarc-collective-forward"),
("evan@embarccollective.com","Evan","Erickson","Senior Director of Partnerships and Events","Embarc Collective","embarccollective.com",P,"valid","https://embarccollective.com/young-professionals-board"),
("hello@embarccollective.com","","","General inbox","Embarc Collective","embarccollective.com",G,"valid","https://embarccollective.com/resources/first-phase-of-launch"),
("cameron@thegabber.com","Cameron","Healy","Editor-in-Chief","The Gabber Newspaper (Gulfport/St. Pete)","thegabber.com",P,"valid","https://www.linkedin.com/in/cameronhealy1"),
("cathy@thegabber.com","Cathy","Salustri","Owner / Publisher","The Gabber Newspaper (Gulfport/St. Pete)","thegabber.com",P,"valid","https://thegabber.com/contact-the-gabber-newspaper/meet-team-gabber"),
("news@thegabber.com","","","News inbox","The Gabber Newspaper (Gulfport/St. Pete)","thegabber.com",G,"valid","https://business.tampabaybeaches.com/list/member/the-gabber-newspaper-9884"),
("editor@theweeklychallenger.com","","","Editor inbox","The Weekly Challenger (St. Pete)","theweeklychallenger.com",G,"valid","https://theweeklychallenger.com/media-kit-press"),
("newsdesk@theweeklychallenger.com","","","News desk","The Weekly Challenger (St. Pete)","theweeklychallenger.com",G,"valid","https://theweeklychallenger.com/contact"),
("dmccree@theweeklychallenger.com","Dexter","McCree","Writer","The Weekly Challenger (St. Pete)","theweeklychallenger.com",P,"valid","https://theweeklychallenger.com/leading-with-a-smile"),
("jgriffin@tampabay.com","Justine","Griffin","Economy and Health Editor","Tampa Bay Times","tampabay.com",P,"valid","https://tampabay.com/author/justine-griffin/"),
("nseenarine@tampabay.com","Neha","Seenarine","Trending Producer, News and Entertainment","Tampa Bay Times","tampabay.com",P,"valid","https://www.tampabay.com/author/neha-seenarine"),
("cspata@tampabay.com","Christopher","Spata","Features / Life & Culture writer (title inferred from bylines)","Tampa Bay Times","tampabay.com",P,"valid","https://tampabay.com/life-culture/2025/09/03/andrew-huse-tampa-author-cuban-sandwich-book-usf-food-history"),
("gcalise@tampabay.com","Gabrielle","Calise","Life & Culture / Bay magazine writer (title inferred from bylines)","Tampa Bay Times","tampabay.com",P,"valid","https://tbt-tbt-prod.web.arc-cdn.net/life-culture/bay-magazine/2025/08/08/tampa-bay-spa-treatments-resort-services"),
("bberdychowski@tampabay.com","Bernadette","Berdychowski","Local Business Reporter (Business by the Bay newsletter)","Tampa Bay Times","tampabay.com",P,"accept_all","https://www.tampabay.com/author/bernadette-berdychowski"),
]
K=["email","first_name","last_name","position","company","domain","type","verification","evidence_url"]
rows=[dict(zip(K,r)) for r in R]
from collections import Counter
emails=[r["email"].lower() for r in rows]
assert len(emails)==len(set(emails)),"dup emails"
for r in rows:
    d=r["domain"]; e=r["email"].lower()
    assert e.split("@")[1]==d, e
    assert d=="tampabay.com" or d not in used, d
    assert e not in wk4, e
    assert r["verification"] in ("valid","accept_all"), e
    assert r["type"] in ("personal","generic")
c=Counter(r["domain"] for r in rows)
assert all(v<=5 for v in c.values()), c
assert c["tampabay.com"]<=5
json.dump(rows,open(H+"wk5_local.json","w"),indent=1,ensure_ascii=False)
new=[d for d in c if d!="tampabay.com"]
print("rows",len(rows),"new domains",len(new),"new-domain emails",sum(c[d] for d in new),"times",c["tampabay.com"])
print("valid",sum(r["verification"]=="valid" for r in rows),"accept_all",sum(r["verification"]=="accept_all" for r in rows))
print("generic",sum(r["type"]=="generic" for r in rows))
print(dict(c))
