import json,os,random,sys,urllib.request
V=(0,100,320,330,500,900,0)
KN=(31,33,14,18,-14,-18,-31,-33)
KG=(1,-1,16,-16,15,17,-15,-17)
BD=(15,17,-15,-17)
RD=(1,-1,16,-16)
CK=[15]*128
for s,v in((4,12),(7,14),(0,13),(116,3),(119,11),(112,7)):CK[s]=v
RM={6:(7,5),2:(0,3),118:(119,117),114:(112,115)}
R=random.Random(20261120)
Z=[R.getrandbits(64) for _ in range(1705)]
ZS=Z[1664];ZC=Z[1665:1681];ZE=Z[1681:]
P=[[0]*64 for _ in range(7)]
E=[0]*64
for r in range(8):
 for f in range(8):
  i=r*8+f;c=min(f,7-f)+min(r,7-r)
  P[1][i]=(0,0,4,8,14,24,40,0)[r]+((0,0,0,10,15,10,5,0)[r] if f in(3,4) else 0)
  P[2][i]=6*c-20;P[3][i]=4*c-8
  P[4][i]=15 if r==6 else(5 if r==0 and f in(3,4) else 0)
  P[5][i]=2*c-6
  P[6][i]=(20,25,10,0,0,10,25,20)[f] if r==0 else max(-50,-15*r)
  E[i]=8*c-24
b=[0]*128;sd=0;cs=0;ep=-1;h=0;K=[0,0];NP=[0,0]
C={};Y=set()
TT={};KL=[[0,0] for _ in range(128)]
nodes=0;NL=150000
class Ab(Exception):pass
def at(s,w):
 for d in(-15,-17)if w else(15,17):
  x=s+d
  if 0<=x<128 and not x&136 and b[x]==(1 if w else -1):return 1
 for d in KN+KG:
  x=s+d
  if 0<=x<128 and not x&136 and b[x]==((2 if w else -2)if d in KN else(6 if w else -6)):return 1
 for d in BD+RD:
  x=s+d
  while 0<=x<128 and not x&136:
   q=b[x]
   if q:
    if(q>0)==w and(abs(q)==5 or abs(q)==(3 if d in BD else 4)):return 1
    break
   x+=d
 return 0
def gen(cp):
 m=[];w=sd==0
 for s in range(128):
  if s&136:continue
  p=b[s]
  if not p or(p>0)!=w:continue
  t=abs(p)
  if t==1:
   d=16 if w else -16;lr=7 if w else 0;to=s+d
   if b[to]==0:
    if(to>>4)==lr:m.append(s|(to<<7)|(5<<14))
    elif not cp:
     m.append(s|(to<<7))
     if(s>>4)==(1 if w else 6):
      t2=s+2*d
      if b[t2]==0:m.append(s|(t2<<7))
   for to in(s+d-1,s+d+1):
    if to&136:continue
    q=b[to]
    if q and(q>0)!=w:
     if(to>>4)==lr:m.append(s|(to<<7)|(5<<14))
     else:m.append(s|(to<<7))
    elif to==ep:m.append(s|(to<<7))
  elif t==2 or t==6:
   for d in(KN if t==2 else KG):
    to=s+d
    if to<0 or to>=128 or to&136:continue
    q=b[to]
    if q==0:
     if not cp:m.append(s|(to<<7))
    elif(q>0)!=w:m.append(s|(to<<7))
  else:
   for d in(BD if t==3 else RD if t==4 else BD+RD):
    to=s+d
    while 0<=to<128 and not to&136:
     q=b[to]
     if q==0:
      if not cp:m.append(s|(to<<7))
     else:
      if(q>0)!=w:m.append(s|(to<<7))
      break
     to+=d
 if not cp:
  for k,f,t in((1,4,6),(2,4,2),(4,116,118),(8,116,114)):
   if cs&k and(k<4)==w and b[(f+t)//2]==0 and b[t]==0 and(t>f or not b[t-1])and not any(at(x,f>100)for x in(f,(f+t)//2,t)):m.append(f|(t<<7))
 return m
def mk(m):
 global sd,cs,ep,h
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7;p=b[f];q=b[t]
 cq=t;cap=q
 if abs(p)==1 and t==ep and q==0:
  cq=t-16 if sd==0 else t+16;cap=b[cq]
 u=(m,cq,cap,cs,ep,h)
 h^=Z[(p+6)*128+f]
 if cap:h^=Z[(cap+6)*128+cq]
 if pr:
  np_=pr if sd==0 else -pr
  h^=Z[(np_+6)*128+t]
 else:h^=Z[(p+6)*128+t]
 nc=cs&CK[f]&CK[t]
 if nc!=cs:h^=ZC[cs]^ZC[nc];cs=nc
 if ep>=0:h^=ZE[ep&7]
 ep=-1
 if abs(p)==1 and abs(t-f)==32:
  ep=(f+t)//2;h^=ZE[ep&7]
 b[t]=(pr if sd==0 else -pr)if pr else p;b[f]=0
 if cq!=t:b[cq]=0
 if abs(p)==6 and abs(t-f)==2:
  a,b2=RM[t];r=4 if sd==0 else -4;b[b2]=r;b[a]=0;h^=Z[(r+6)*128+a]^Z[(r+6)*128+b2]
 if abs(p)==6:K[sd]=t
 if cap and abs(cap)!=1:NP[1-sd]-=V[abs(cap)]
 if pr:NP[sd]+=V[pr]-100
 sd^=1;h^=ZS;C[h]=C.get(h,0)+1
 return u
def un(u):
 global sd,cs,ep,h
 C[h]=C.get(h,0)-1
 m,cq,cap,ocs,oep,oh=u
 sd^=1;f=m&127;t=(m>>7)&127;pr=(m>>14)&7;p=b[t]
 if abs(p)==6:K[sd]=f
 b[f]=(1 if sd==0 else -1)if pr else p;b[t]=0
 if cap:b[cq]=cap
 if abs(p)==6 and abs(t-f)==2:
  a,b2=RM[t];b[a]=b[b2];b[b2]=0
 if cap and abs(cap)!=1:NP[1-sd]+=V[abs(cap)]
 if pr:NP[sd]-=V[pr]-100
 cs,ep,h=ocs,oep,oh
def mkn():
 global sd,ep,h
 u=(ep,h)
 if ep>=0:h^=ZE[ep&7]
 ep=-1;sd^=1;h^=ZS
 return u
def unn(u):
 global sd,ep,h
 ep,h=u;sd^=1
def ev():
 s=0;bp=[0,0];ka=[0,0]
 for sq in range(128):
  if sq&136:continue
  p=b[sq]
  if not p:continue
  t=abs(p);w=p>0
  rl=(sq>>4)*8+(sq&7) if w else(7-(sq>>4))*8+(sq&7)
  if t==6:ka[0 if w else 1]=rl;continue
  v=V[t]+P[t][rl];s+=v if w else -v
  if t==3:bp[0 if w else 1]+=1
 ph=min(NP[0]+NP[1],6400)
 s+=(P[6][ka[0]]*ph+E[ka[0]]*(6400-ph))//6400-(P[6][ka[1]]*ph+E[ka[1]]*(6400-ph))//6400
 if bp[0]>1:s+=30
 if bp[1]>1:s-=30
 return s if sd==0 else -s
def qs(a,be,pl):
 global nodes
 nodes+=1
 if nodes>NL:raise Ab
 if at(K[sd],sd==1):
  ms=gen(0);best=-100000;nl=0
  for m in ms:
   u=mk(m)
   if at(K[sd^1],sd==0):un(u);continue
   nl+=1;sc=-qs(-be,-a,pl+1);un(u)
   if sc>best:best=sc
   if sc>a:a=sc
   if a>=be:return a
  return best if nl else -100000+pl
 st=ev()
 if st>=be:return be
 if st>a:a=st
 ms=gen(1)
 ms.sort(key=lambda m:(V[abs(b[(m>>7)&127])]if b[(m>>7)&127] else 100)*16-V[abs(b[m&127])],reverse=True)
 for m in ms:
  u=mk(m)
  if at(K[sd^1],sd==0):un(u);continue
  sc=-qs(-be,-a,pl+1);un(u)
  if sc>=be:return be
  if sc>a:a=sc
 return a
def sr(d,a,be,pl):
 global nodes
 nodes+=1
 if nodes>NL:raise Ab
 if C.get(h,0)>1 or h in Y:return 0
 inck=at(K[sd],sd==1)
 if inck:d+=1
 if d<=0:return qs(a,be,pl)
 e=TT.get(h)
 if e and e[0]>=d:
  sc=e[1]-pl if e[1]>90000 else e[1]+pl if e[1]<-90000 else e[1]
  if e[2]==0:return sc
  if e[2]==1 and sc>=be:return sc
  if e[2]==2 and sc<=a:return sc
 if d>=3 and not inck and NP[sd]>500:
  u=mkn()
  sc=-sr(d-3,-be,-be+1,pl+1);unn(u)
  if sc>=be:return be
 ms=gen(0)
 def ok(m):
  if e and m==e[3]:return 1<<20
  q=b[(m>>7)&127]
  if q:return 10000+V[abs(q)]*16-V[abs(b[m&127])]
  if m==KL[pl][0] or m==KL[pl][1]:return 9000
  return 0
 ms.sort(key=ok,reverse=True)
 best=-100000;bm=0;fl=2;a0=a;nl=0
 for i,m in enumerate(ms):
  u=mk(m)
  if at(K[sd^1],sd==0):un(u);continue
  nl+=1
  if d>=3 and i>=4 and not u[2] and not at(K[sd],sd==1):
   sc=-sr(d-2,-a-1,-a,pl+1)
   if sc>a:sc=-sr(d-1,-be,-a,pl+1)
  else:sc=-sr(d-1,-be,-a,pl+1)
  un(u)
  if sc>best:best=sc;bm=m
  if sc>a:a=sc
  if a>=be:
   if not b[(m>>7)&127]:
    KL[pl][1]=KL[pl][0];KL[pl][0]=m
   break
 if not nl:return -100000+pl if inck else 0
 if best>=be:fl=1
 elif best<=a0:fl=2
 else:fl=0
 s2=best+pl if best>90000 else best-pl if best<-90000 else best
 TT[h]=(d,s2,fl,bm)
 return best
def G():
 global nodes
 if len(TT)>400000:TT.clear()
 ms=gen(0);lg=[]
 for m in ms:
  u=mk(m)
  if at(K[sd^1],sd==0):un(u);continue
  lg.append(m);un(u)
 if len(lg)==1:return lg[0]
 nodes=0;best=lg[0];scs={m:0 for m in lg}
 C.clear();C[h]=1
 for d in range(1,12):
  n0=nodes
  try:
   lg.sort(key=lambda m:scs[m],reverse=True)
   a=-100000;bb=lg[0]
   for m in lg:
    u=mk(m);sc=-sr(d-1,-100000,-a,1);un(u)
    scs[m]=sc
    if sc>a:a=sc;bb=m
   best=bb
   if nodes+(nodes-n0)*4>NL:break
  except Ab:break
 return best
def J(ms):
 F("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
 Y.clear();Y.add(h)
 for s in ms:
  f="abcdefgh".index(s[0])+(int(s[1])-1)*16;t="abcdefgh".index(s[2])+(int(s[3])-1)*16
  mk(f|(t<<7)|(({"q":5,"r":4,"b":3,"n":2}[s[4]]<<14)if len(s)==5 else 0));Y.add(h)
def F(f):
 global b,sd,cs,ep,h
 b=[0]*128;w=f.split();rws=w[0].split("/")
 for r,row in enumerate(rws):
  rr=7-r;fl=0
  for c in row:
   if c.isdigit():fl+=int(c)
   else:
    p="PNBRQK".index(c.upper())+1
    if c.islower():p=-p
    b[rr*16+fl]=p;fl+=1
 sd=0 if w[1]=="w" else 1;cs=0
 if w[2]!="-":
  for c in w[2]:cs|={"K":1,"Q":2,"k":4,"q":8}[c]
 ep=-1
 if w[3]!="-":ep="abcdefgh".index(w[3][0])+(int(w[3][1])-1)*16
 NP[0]=0;NP[1]=0;h=0
 for sq in range(128):
  if sq&136:continue
  p=b[sq]
  if not p:continue
  if abs(p)==6:K[0 if p>0 else 1]=sq
  elif abs(p)!=1:NP[0 if p>0 else 1]+=V[abs(p)]
  h^=Z[(p+6)*128+sq]
 if sd:h^=ZS
 h^=ZC[cs]
 if ep>=0:h^=ZE[ep&7]

def O(p,o):
 r=urllib.request.Request(os.environ["MAKEFUN_ENV_URL"]+p,data=json.dumps(o).encode(),headers={"Content-Type":"application/json"})
 with urllib.request.urlopen(r) as x:return json.load(x)
if __name__=="__main__":
 while True:
  g=O("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   J(g["moves"]);F(g["fen"]);m=G();g=O("/move",{"game":g["game"],"move":"abcdefgh"[m&7]+str(((m&127)>>4)+1)+"abcdefgh"[(m>>7)&7]+str((((m>>7)&127)>>4)+1)+("q" if(m>>14)&7 else"")})
  print("game",g["game"],g["outcome"],g["reason"],file=sys.stderr)
 print("done",g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
