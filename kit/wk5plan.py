import json,collections
used=set(l.strip() for l in open('used_domains_all.txt') if l.strip())
def score(r):
    s=0
    if r.get('verification')=='valid': s+=4
    if r.get('type')=='personal': s+=2
    if (r.get('position') or '').strip(): s+=1
    if (r.get('first_name') or '').strip(): s+=1
    return s
merged={r['email']:r for r in json.load(open('wk4_merged.json'))}
carry=[]
for m in json.load(open('wk5_carryover.json')):
    r=dict(merged.get(m['email'],{})); r.update(email=m['email'],domain=m['domain'],company=m['company'],first_name=m['first_name'],last_name=m['last_name'],position=m['position'],lead_id=m['lead_id'],src='carry'); carry.append(r)
locdom={r['domain'] for r in json.load(open('wk5_local.json'))}
new=[]; seen={r['email'] for r in carry}
for f in ['wk5_gaming.json','wk5_geek.json','wk5_lifestyle.json']:
    for r in json.load(open(f)):
        e=r['email'].lower()
        if e in seen or r['domain'] in used or r['domain'] in locdom: continue
        seen.add(e); r['email']=e; r['src']='new'; new.append(r)
c=collections.Counter(r['domain'] for r in carry+new); print('over5',{d:n for d,n in c.items() if n>5})
new.sort(key=score,reverse=True)
need=186-len(carry); gift=carry+new[:need]; wk6=new[need:]
print('carry',len(carry),'new',len(new),'gift',len(gift),'wk6',len(wk6))
loc=[r for r in json.load(open('wk5_local.json')) if r['domain']!='floridapolitics.com']
for r in loc: r['email']=r['email'].lower(); r['src']='new'
assert not ({r['email'] for r in loc} & seen)
print('local',len(loc))
def spread(pool,seqmap,per):
    slots=list(seqmap); cap={s:per for s in slots}; out=[]
    bd=collections.defaultdict(list)
    for r in pool: bd[r['domain']].append(r)
    for d in sorted(bd,key=lambda d:-len(bd[d])):
        u=set()
        for r in bd[d]:
            cs=[s for s in slots if cap[s]>0 and s not in u] or [s for s in slots if cap[s]>0]
            s=max(cs,key=lambda s:cap[s]); cap[s]-=1; u.add(s)
            out.append(dict(seq=seqmap[s],slot=s,email=r['email'],first_name=r.get('first_name') or '',last_name=r.get('last_name') or '',position=r.get('position') or '',company=r.get('company') or '',domain=d,src=r['src'],lead_id=r.get('lead_id')))
    return out
g=spread(gift,{'partners|Mon':908176,'partners|Tue':908177,'partners|Wed':908178,'bennett|Mon':908179,'bennett|Tue':908180,'bennett|Wed':908181},31)
l=spread(loc,{'partners|Mon':908182,'partners|Tue':908183,'partners|Wed':908184,'bennett|Mon':908185,'bennett|Tue':908186,'bennett|Wed':908187},9)
allr=g+l
print(len(g),len(l),collections.Counter(a['seq'] for a in allr))
print('nocompany',[a['email'] for a in allr if not a['company']])
json.dump(allr,open('wk5_load.json','w'),indent=1); json.dump(wk6,open('wk6_carryover.json','w'),indent=1)
print(collections.Counter(r['verification'] for r in gift[51:]+loc), collections.Counter(r['domain'] for r in wk6).most_common(5))
