import subprocess,os,sys
def tok(src,dst):
    low=open(src).read().lower()
    open('/tmp/_t.bas','w').write(low)
    subprocess.run(['petcat','-w2','-o',dst,'--','/tmp/_t.bas'],check=True)
    subprocess.run(['petcat','-2','-o','/tmp/_b.txt','--',dst],check=True)
    import re
    a=[re.sub(r'\s+','',l) for l in low.splitlines() if l.strip()]
    b=[re.sub(r'\s+','',l) for l in open('/tmp/_b.txt').read().splitlines() if l.strip()]
    assert a==b,(src,[(x,y) for x,y in zip(a,b) if x!=y][:3])
    return os.path.getsize(dst)
for s,d in (('hex64-loader.bas','loader.prg'),('hex64-game.bas','game.prg'),('hex64-demo.bas','demo.prg')):
    print(d,tok(s,d),'bytes')
subprocess.run(['cp','prg/hex64music.prg','music.prg'],check=True)
D='hex64.d64'
if os.path.exists(D): os.remove(D)
subprocess.run(['c1541','-format','hex64,05','d64',D,'-write','loader.prg','hex64','-write','game.prg','hex64game','-write','demo.prg','hex64demo',
                '-write','music.prg','hex64music','-write','hex64chars.prg','hex64chars','-write','hex64bg.prg','hex64bg'],check=True,capture_output=True)
img=bytearray(open(D,'rb').read())
SPT=[0]+[21]*17+[19]*7+[18]*6+[17]*5
def off(t,s): return (sum(SPT[1:t])+s)*256
# read existing entries
ents=[];t,s=18,1
while t:
    o=off(t,s)
    for i in range(8):
        e=img[o+i*32+2:o+i*32+32]
        if e[0]: ents.append(bytes(e))
    t,s=img[o],img[o+1]
name=lambda e:bytes(e[3:19]).rstrip(b'\xa0').decode('latin1')
byname={name(e):e for e in ents}
# directory art drawn by m0nde: hexagon with a stack of chips (7 wide, centred in 16)
art=[b'    \x20\xce\xb7\xb7\xb7\xcd\x20     ',
     b'    \xce\x20\xc0\xc0\xc0\x20\xcd     ',
     b'    \xa5\x20\xc0\xc0\xc0\x20\xa7     ',
     b'    \xa5\x20\xc0\xc0\xc0\x20\xa7     ',
     b'    \xcd\x20\xc0\xc0\xc0\x20\xce     ',
     b'    \x20\xcd\x20\x20\x20\xce\x20     ',
     b'    \x20\x20\xb7\xb7\xb7\x20\x20     ']
def delent(nm):
    e=bytearray(30); e[0]=0x80; e[3:19]=nm.ljust(16,b'\xa0'); return bytes(e)
order=[byname['HEX64']]+[delent(a) for a in art]+[byname['HEX64GAME'],byname['HEX64DEMO'],byname['HEX64MUSIC'],byname['HEX64CHARS'],byname['HEX64BG']]
# write entries into 18/1, 18/4, 18/7 ...
secs=[1,4,7,10]
need=(len(order)+7)//8
for k in range(need):
    o=off(18,secs[k]); img[o:o+256]=bytes(256)
    if k<need-1: img[o]=18; img[o+1]=secs[k+1]
    else: img[o]=0; img[o+1]=255
    for i,e in enumerate(order[k*8:k*8+8]): img[o+i*32+2:o+i*32+32]=e
# BAM: mark the directory sectors used on track 18
b=off(18,0)+4*18
used={0}|set(secs[:need])
bits=[0,0,0]
for sct in range(19):
    if sct not in used: bits[sct//8]|=1<<(sct%8)
img[b]=19-len(used); img[b+1:b+4]=bytes(bits)
open(D,'wb').write(img)
print(subprocess.run(['c1541',D,'-dir'],capture_output=True,text=True).stdout)
