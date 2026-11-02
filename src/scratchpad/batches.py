import os,json
os.chdir('/home/claude/villa')
files=['img/'+f for f in sorted(os.listdir('img'))]+['data/'+f for f in sorted(os.listdir('data'))]
B=[];cur=[];sz=0
for f in files:
    s=os.path.getsize(f)
    if cur and (sz+s>58*1048576 or len(cur)>=240): B.append(cur);cur=[];sz=0
    cur.append(f);sz+=s
if cur:B.append(cur)
for i,b in enumerate(B):
    json.dump([{"path":p} for p in b],open(f'/tmp/claude-0/-home-claude/9b11369b-255f-547e-a148-3cb5bc61c84e/scratchpad/batch{i}.json','w'))
    print(i,len(b),round(sum(os.path.getsize(p) for p in b)/1048576,1),'MB')
print('total files',len(files),round(sum(os.path.getsize(p) for p in files)/1048576,1),'MB')
