import sys,json; sys.path.insert(0,'.'); import esx
term=sys.argv[1]; filt=json.loads(sys.argv[2]) if len(sys.argv)>2 else None; n=int(sys.argv[3]) if len(sys.argv)>3 else 15
for i,r in enumerate(esx.search(term,n,filt=filt)): print(esx.fmt(i,r))
