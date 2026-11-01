import re,collections
L=open('../pixellab/batch_v3/log.txt').read().splitlines()
d=collections.OrderedDict()
for i,l in enumerate(L):
    m=re.match(r'\s*([0-9]{3}|race_v\d|steal|plat)\b',l)
    if m: d.setdefault(m.group(1),[]).append(i)
skip=set("010 019 020 022 023 025 027 028 029 031 033 036 037 039 043 045 047 048 049 050 051 052 053 054 055 056 057 058 059 062 063 064 066 067 079 080 081 082 085 089 090 098 104 108 race_v4 steal 088 103".split())
for k in sorted(d):
    if k in skip: continue
    l=L[d[k][-1]]
    scr=re.findall(r'[\w/.\-]*fork[\w/.\-]*\.py',l)
    print(k,len(d[k]),'|',scr[:3])
