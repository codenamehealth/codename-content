import json, collections, sys
used=set(l.strip().lower() for l in open('/home/claude/hunter/used_domains_all.txt') if l.strip())
# also domains already present in earlier lead files but missing from used list
extra_used={'draftsim.com','esportsinsider.com','gamesindustry.biz','gamingonlinux.com','geeknative.com','pocketgamer.com','roadtovr.com','shutupandsitdown.com','whatsthebest.co.uk'}
ev={
'gearpatrol.com':'https://www.gearpatrol.com/gift-guides/best-holiday-christmas-gifts-2025/',
'hiconsumption.com':'https://hiconsumption.com/author/ian',
'coolmaterial.com':'https://coolmaterial.com/editorial-submissions',
'mensjournal.com':'https://www.mensjournal.com',
'manofmany.com':'https://manofmany.com/tag/christmas',
'dmarge.com':'https://dmarge.com/contact',
'thegadgetflow.com':'https://thegadgetflow.com/about-us',
'mindbodygreen.com':'https://lps.pagedeck.com/brand/mindbodygreen.com/articles-best-self-care-gifts-2025',
'hercampus.com':'https://spoonuniversity.com/lifestyle/new-lisa-says-gah-collection-is-the-perfect-clothing-gift-for-foodies',
'atlantamagazine.com':'https://atlantamagazine.com/contact-us/pitches',
'phoenixmag.com':'https://www.phoenixmag.com/tag/local-gifts/',
'bostonmagazine.com':'https://bostonmagazine.com/tag/holiday-gift-guides',
'mspmag.com':'https://mspmag.com/shop-and-style/swag/here-come-the-holiday-pop-ups',
'charlottemagazine.com':'https://www.charlottemagazine.com/?p=87816',
'orlandomagazine.com':'https://orlandomagazine.com/about-us/contact-us',
'saltlakemagazine.com':'https://saltlakemagazine.com/salt-lake-magazine-2025-holiday-gift-guide/',
'nashvillelifestyles.com':'https://nashvillelifestyles.com/contact',
'yankodesign.com':'https://www.yankodesign.com/tag/yd-handpicks/',
'ubergizmo.com':'https://www.ubergizmo.com',
'gadgetreview.com':'https://gadgetreview.com/contact-us',
'wellandgood.com':'https://wellandgood.com/pitching-guidelines',
'garagegymreviews.com':'https://garagegymreviews.com',
'sleepopolis.com':'https://sleepopolis.com/sleepopolis-holiday-gift-guide/',
'theskimm.com':'https://www.theskimm.com/shopping/founder-holiday-gifts-24',
'apetogentleman.com':'https://apetogentleman.com/ape-gentleman-selects-jack-spade',
'narcity.com':'https://narcity.com/vancouver/magical-small-towns-near-vancouver-transform-dreamy-winter-wonderland',
'thespinoff.co.nz':'https://thespinoff.co.nz/tags/kirihimete',
'brobible.com':'https://brobible.com/tag/gift-guides/',
'hypebeast.com':'https://hypebeast.com/tags/hypebeast-gift-guide-2025',
'primermagazine.com':'https://primermagazine.com',
'lamag.com':'https://lamag.com/style/los-angeles-magazine-2025-holiday-gift-guide-l/',
'kansascitymag.com':'https://kansascitymag.com/2020-kansas-city-magazine-holiday-gift-guide/',
'waltermagazine.com':'https://waltermagazine.com/about',
'westword.com':'https://westword.com/about/staff',
'lasvegasweekly.com':'https://lasvegasweekly.com',
'androidheadlines.com':'https://www.androidheadlines.com',
'image.ie':'https://image.ie/style/whats-in-the-image-teams-autumn-make-up-bags-831423',
'phillymag.com':'https://phillymag.com/contact/editorial-staff',
'miaminewtimes.com':'https://miaminewtimes.com/about/staff',
'texasmonthly.com':'https://www.texasmonthly.com/podcast/tm-out-loud-texas-gift-guide-2025/',
'phonearena.com':'https://phonearena.com/team',
'cincinnatimagazine.com':'https://www.cincinnatimagazine.com/article/a-best-of-the-city-gift-guide/',
'indianapolismonthly.com':'https://www.indianapolismonthly.com/lifestyle/shopping/our-outside-the-box-all-local-gift-guide/',
'stlmag.com':'https://www.stlmag.com/culture/Things-We-Love-Holiday-Gift-Guide',
}
over={'cass@brobible.com':'https://brobible.com/tag/gift-guides/'}
rows=[]
for l in open('picks1.tsv'):
    p=l.rstrip('\n').split('\t')
    assert len(p)==8, p
    e,f,la,pos,co,d,t,v=p
    rows.append(dict(email=e.lower(),first_name=f,last_name=la,position=pos,company=co,domain=d,type=t,verification=v,evidence_url=over.get(e,ev[d])))
for r in rows:
    assert r['domain'] not in used and r['domain'] not in extra_used, r
    assert r['verification'] in ('valid','accept_all'), r
    assert r['email'].split('@')[1]==r['domain'], r
    assert r['type'] in ('personal','generic')
    assert r['evidence_url'].startswith('https://')
emails=[r['email'] for r in rows]
assert len(emails)==len(set(emails)), [e for e,c in collections.Counter(emails).items() if c>1]
c=collections.Counter(r['domain'] for r in rows)
assert max(c.values())<=5, c
json.dump(rows,open('/home/claude/hunter/wk5_lifestyle.json','w'),indent=1,ensure_ascii=False)
print(len(rows),'emails',len(c),'domains')
print(collections.Counter(r['verification'] for r in rows), collections.Counter(r['type'] for r in rows))
