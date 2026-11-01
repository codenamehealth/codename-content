import json,re,sys
D=json.load(open('drafts.json'))
md=open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone/captions_v2_drafts.md').read()
errs=[]
def e(m): errs.append(m)
# whole-file checks
for bad,name in [('#','hashtag'),('—','em dash'),('–','en dash'),('REALM','REALM')]:
    body=re.sub(r'^#+ .*$','',md,flags=re.M)  # markdown headings excluded for '#'
    if bad in (body if bad=='#' else md): e(f'file contains {name}')
if re.search(r'link in bio',md,re.I): e('link in bio in file')
if re.search(r'https?://|www\.|\.com\b',md): e('URL in file')
if re.search(r'free cards',md,re.I): e('free cards')
if re.search(r'\bjars?\b|supplement',re.sub(r'^Old caption first line:.*$','',md,flags=re.M),re.I): e('jar/supplement mention')
for d in D:
    tag=d['slot']+' '+d['reel']
    for k in ('fb_cap','fb_pin','tt_cap','tt_pin','tt_title','yt_cap','yt_pin'):
        t=d[k]
        if re.search(r'quest',re.sub(r'Side [Qq]uests?','',t),re.I) and 'QUEST' not in t: e(f'{tag} {k}: lowercase quest keyword')
        for w in re.findall(r'\b[Qq][Uu][Ee][Ss][Tt]\w*\b',re.sub(r'Side [Qq]uests?','',t)):
            if w!='QUEST': e(f'{tag} {k}: keyword variant {w}')
    for k,cta in (('fb_cap','Comment QUEST'),('tt_cap','DM us QUEST')):
        L=d[k].split('\n')
        if cta not in L[-1]: e(f'{tag} {k}: CTA not last line')
        if sum(cta in x for x in L)!=1: e(f'{tag} {k}: CTA count')
        if k=='fb_cap' and not re.search(r"DM",L[-1]): e(f'{tag} fb CTA lacks DM promise')
        g=L[-2]
        if 'Switch 2' not in g: e(f'{tag} {k}: giveaway line (before CTA) lacks Switch 2')
        else:
            # Switch 2 is the first prize/thing named in the giveaway line
            pre=g.split('Switch 2')[0]
            if re.search(r'marble|founder|free',pre,re.I): e(f'{tag} {k}: something before Switch 2 in giveaway line: {pre}')
        if 'Feb 1' not in g: e(f'{tag} {k}: no Feb 1 in giveaway line')
        if not re.search(r'free|no purchase',g,re.I): e(f'{tag} {k}: giveaway line lacks free/no purchase')
        if 'Switch 2' in '\n'.join(L[:-2]): e(f'{tag} {k}: Switch 2 above giveaway line')
    for k,cta in (('fb_pin','Comment QUEST'),('tt_pin','DM us QUEST')):
        L=d[k].split('\n')
        if cta not in L[-1] or len(L)>2: e(f'{tag} {k}: pin shape')
        if 'Switch 2' not in L[0]: e(f'{tag} {k}: pin lacks Switch 2')
    if d['fb_pin'].split('\n')[-1]!=d['fb_cap'].split('\n')[-1]: e(f'{tag}: fb pin CTA differs from caption CTA')
    if d['tt_pin'].split('\n')[-1]!=d['tt_cap'].split('\n')[-1]: e(f'{tag}: tt pin CTA differs from caption CTA')
    if 'Comment QUEST' in d['tt_cap']+d['tt_pin']: e(f'{tag}: Comment QUEST on TikTok')
    for k in ('yt_cap','yt_pin'):
        if re.search(r'QUEST|Switch|giveaway|Feb 1|DM',d[k]): e(f'{tag} {k}: giveaway/QUEST on YouTube')
    if d.get('yt') is not None or 'Oct 31' in d['slot']:
        pass
    n=len(d['lines'])
    if not 1<=n<=2: e(f'{tag}: {n} video lines')
# variety
from collections import Counter
c=Counter(d['fb_cap'].split('\n')[-2]+'|'+d['fb_cap'].split('\n')[-1] for d in D)
print('distinct FB giveaway+CTA combos',len(c),'of',len(D),'max repeat',max(c.values()))
print('ERRORS' if errs else 'ALL CHECKS PASS', len(errs))
for x in errs: print(' -',x)
