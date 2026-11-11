import sys  # usage: python3 mk-hex64data.py chargen-901225-01.bin  (writes the HEX64DATA parts; assemble src/hex64-data.asm into $4000)
# Builds HEX64DATA, loaded at $3000:
#   $3000 character set (0-63 from the C64 character ROM, 64-73 hex outline/dot, 74-115 piles, 116-123 panel frame)
#   $3800 loader background screen codes   $3C00 its colour RAM
#   $4000 machine code: SYS 16384 copies the background to the screen and resets the 21 piles
#   $4100 the 21 starting pile bitmaps (42 chars, 336 bytes)
import random
ROM=open(sys.argv[1],'rb').read()
mem=bytearray(0x1250)
def put(addr,data): mem[addr-0x3000:addr-0x3000+len(data)]=bytes(data)
put(0x3000,ROM[:512])
def slant(up):
    rows=[[0]*24 for _ in range(8)]
    for x in range(24):
        y=round(x*7/23); y=7-y if up else y; rows[y][x]=1
    return [sum(128>>k for k in range(8) if rows[r][c*8+k]) for c in range(3) for r in range(8)]
custom=slant(True)+slant(False)+[128]*8+[1]*8+[1,1,0,0,0,0,0,0]+[128,128,0,0,0,0,0,0]
put(0x3200,custom)
# panel frame chars 116-123: TL,T,TR,L,R,BL,B,BR (thin line, 2 pixels in from the panel edge)
def ch(f): return [sum(128>>x for x in range(8) if f(x,y)) for y in range(8)]
frame=[ch(lambda x,y:(y==2 and x>=2) or (x==2 and y>=2)), ch(lambda x,y:y==2),
       ch(lambda x,y:(y==2 and x<=5) or (x==5 and y>=2)), ch(lambda x,y:x==2), ch(lambda x,y:x==5),
       ch(lambda x,y:(y==5 and x>=2) or (x==2 and y<=5)), ch(lambda x,y:y==5),
       ch(lambda x,y:(y==5 and x<=5) or (x==5 and y<=5))]
put(0x3000+116*8,[b for c in frame for b in c])
put(0x3000+160*8,[255]*8)        # reverse space, for the SID setup volume bar
# background
scr=[32]*1000; col=[0]*1000
PX0,PX1,PY0,PY1=7,32,6,18           # panel columns/rows (inclusive)
def inpanel(x,y): return PX0<=x<=PX1 and PY0<=y<=PY1
def setc(x,y,c,cc):
    if 0<=x<40 and 0<=y<25 and not inpanel(x,y): scr[y*40+x]=c; col[y*40+x]=cc
hexes=[]
for r in range(-1,9):
    for c in range(-1,8):
        hexes.append((c*6+(3 if r%2 else 0)-1, r*3-1))
for (x,y) in hexes:
    for j in range(3):
        setc(x+j,y,64+j,6); setc(x+j+3,y,67+j,6); setc(x+j,y+3,67+j,6); setc(x+j+3,y+3,64+j,6)
    for dy in (1,2):
        setc(x,y+dy,70,6); setc(x+5,y+dy,71,6); setc(x+1,y+dy,32,6); setc(x+4,y+dy,32,6)
# piles: hexes whose 4 pile cells are fully on screen and outside the panel
cand=[(x,y) for (x,y) in hexes if all(0<=x+2+i<40 and 0<=y+1+j<25 and not inpanel(x+2+i,y+1+j) for i in (0,1) for j in (0,1))]
random.seed(64)
piles=random.sample(cand,21) if len(cand)>=21 else cand
print('pile candidates',len(cand))
heights=[]; pile_pos=[]
pilebytes=bytearray(336)
PB={1:0x55,2:0xAA,3:0xFF}
for p,(x,y) in enumerate(piles):
    chc=74+2*p
    h=random.randint(1,6); heights.append(h); pile_pos.append((x,y))
    for i in range(1,h+1): pilebytes[p*16+17-2*i]=PB[random.randint(1,3)]
    setc(x+2,y+1,chc,15); setc(x+3,y+1,chc,15); setc(x+2,y+2,chc+1,15); setc(x+3,y+2,chc+1,15)
for (x,y) in cand:
    if (x,y) not in piles:
        setc(x+2,y+1,32,6); setc(x+3,y+1,32,6); setc(x+2,y+2,72,6); setc(x+3,y+2,73,6)
# panel: black inside, frame on its edge
for y in range(PY0,PY1+1):
    for x in range(PX0,PX1+1):
        c=32
        if y==PY0: c=117
        if y==PY1: c=122
        if x==PX0: c={PY0:116,PY1:121}.get(y,119)
        if x==PX1: c={PY0:118,PY1:123}.get(y,120)
        scr[y*40+x]=c; col[y*40+x]=6
put(0x3800,scr); put(0x3C00,col)
put(0x3000+74*8,pilebytes); put(0x4100,pilebytes)
open('heights.txt','w').write(','.join(map(str,heights)))
