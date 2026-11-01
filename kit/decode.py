import json,base64,glob,os,sys
TR='/root/.claude/projects/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/tool-results/'
OUT='/home/claude/charlie/raw/'
man={l.split()[0]:(l.split()[1],int(l.split()[2])) for l in open(sys.argv[1]) if l.strip()}
done=set()
for f in sorted(glob.glob(TR+'mcp-Google_Drive-download_file_content-*.txt')):
    try: d=json.load(open(f))
    except Exception as e: print('bad json',f,e); continue
    t=d.get('title')
    if t not in man or man[t][0]!=d.get('id'): continue
    b=base64.b64decode(d['content'])
    p=OUT+t
    if not os.path.exists(p) or os.path.getsize(p)!=len(b):
        open(p,'wb').write(b)
    done.add(t)
missing=[t for t in sorted(man) if not os.path.exists(OUT+t)]
print('present',len(man)-len(missing),'missing',len(missing))
for t in missing: print(t,man[t][0])
