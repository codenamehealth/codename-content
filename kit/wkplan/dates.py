import json,sys,datetime
A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
def dt(sc):
    n=0
    for c in sc[:11]: n=n*64+A.index(c)
    ms=(n>>23)+1314220021721
    return datetime.datetime.utcfromtimestamp(ms/1000).strftime('%m-%d')
d=json.load(open(sys.argv[1]))
for i,r in enumerate(d):
    sc=r[2].rstrip('/').split('/')[-1]
    print(i,sc,r[1],round(r[0],2),r[3],dt(sc))
for sc in sys.argv[2:]: print('IMG',sc,dt(sc))
