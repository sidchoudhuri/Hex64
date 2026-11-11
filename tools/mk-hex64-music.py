# hex64-music.asm v2: "Hexed", slower, with glissandos (portamento) tying phrases together
NAMES={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def n(s): return int(s[1])*12+NAMES[s[0]]-11          # C1=1 ... B6=72
E=34                                                  # eighth = 34 ticks at 60 Hz, about 53 BPM
HOLD=255
GL=128                                                # +128 on the note = glide into it from the last note
v1=[];v2=[]
def ev(lst,note,dur,gate,glide=False): lst.append(((n(note)|(GL if glide else 0)) if note else 0,dur,gate))
# --- melody (voice 1) ---
def secA():
    # bar: [first 2E][3 plucks][held 3E that glides into the next bar]
    bars=[("C4",False,"G4 D5 E5","G5"),("E5",True,"C5 A4 E4","A4"),
          ("C5",True,"A4 C5 G5","E5"),("D5",True,"G4 A4 D5","A4")]
    for first,gl,pl,held in bars:
        ev(v1,first,2*E,2*E-8 if not gl else 2*E-8,gl)
        for p in pl.split(): ev(v1,p,E,5)
        ev(v1,held,3*E,HOLD)                      # held: gate stays on, next note glides from it
def secB():
    # long notes; most glide into the next
    seq=[("E5",True,HOLD),("G5",True,4*E-10),
         ("E5",False,HOLD),("C5",True,4*E-10),
         ("A4",False,HOLD),("C5",True,HOLD),
         ("D5",True,HOLD),("A4",True,HOLD)]
    for note,gl,gate in seq: ev(v1,note,4*E,gate,gl)
secA()
v1[0]=(n("C4"),2*E,2*E-8)
secB()
# second time through: section A starts by gliding down from B's last note
start=len(v1); secA(); v1[start]=(n("C4")|GL,2*E,2*E-8)
secB()
# loop: first note of the tune is plain C4 (no glide), the jump back is a soft re-attack
# --- pad (voice 2): half-bar events so durations fit in a byte ---
roots=["C3","A2","F2","G2"]
for sec in range(4):
    for i,r in enumerate(roots):
        last = (i==3)
        first = (i==0 and sec>0)
        ev(v2,r,4*E,HOLD,first)            # first half: glide in at the start of each phrase
        ev(v2,r,4*E,HOLD if last else 4*E-12,True)   # second half: same note, legato; last bar holds into the slide
v2[0]=(n("C3"),4*E,HOLD)
# --- song 1: the original "Hexed" (about 69 BPM, plucks and a bar-long pad, no glides)
E1=26
a1=[];b1=[]
arpA=["C4 G4 D5 E5 G5 E5 D5 G4","A3 E4 A4 C5 E5 C5 A4 E4","F3 C4 A4 C5 G5 C5 A4 C4","G3 D4 G4 A4 D5 A4 G4 D4"]
arpB=["E5 - G5 - D5 - C5 -","C5 - E5 - A4 - G4 -","A4 - C5 - G5 - E5 -","D5 - G4 - A4 - D5 -"]
for sec in (arpA,arpB,arpA,arpB):
    for bar in sec:
        for t in bar.split(): a1.append((0 if t=='-' else n(t),E1,5))
for _ in range(4):
    for p in ["C3","A2","F2","G2"]: b1.append((n(p),8*E1,8*E1-12))
def tbl(clock):
    lo=[];hi=[]
    for k in range(1,73):
        f=440*2**((k+23-69)/12); r=round(f*16777216/clock); lo.append(r&255); hi.append(r>>8)
    return lo,hi
pl,ph=tbl(985248); nl,nh=tbl(1022727)
def bl(name,v):
    return '\n'.join((name if i==0 else ' '*len(name))+' !byte '+','.join(map(str,v[i:i+24])) for i in range(0,len(v),24))
def dat(name,evs):
    vals=[x for e in evs for x in e]+[255]
    return bl(name,vals)
VOICE='''
; ---- voice {N}: SID register offset {R} ----
v{N}tick
        lda gc{N}               ; glide in progress?
        beq ++
        clc
        lda cl{N}
        adc sl{N}
        sta cl{N}
        lda ch{N}
        adc sh{N}
        sta ch{N}
        dec gc{N}
        bne +
        lda tl{N}               ; glide finished: land exactly on the note
        sta cl{N}
        lda th{N}
        sta ch{N}
+       lda cl{N}
        sta $d400+{R}
        lda ch{N}
        sta $d401+{R}
++      dec cnt{N}
        lda cnt{N}
        cmp off{N}
        bne +
        lda #{W}
        sta $d404+{R}           ; gate off: the release fades out
+       lda cnt{N}
        beq v{N}next
        rts
v{N}next
        jsr v{N}get
        cmp #$ff
        bne +
        lda st{N}l              ; end of data: loop to the song's start
        sta v{N}g+1
        lda st{N}h
        sta v{N}g+2
        jmp v{N}next
+       sta note
        jsr v{N}get
        sta cnt{N}
        jsr v{N}get             ; gate length; 255 = hold to the end
        sta tmp
        lda cnt{N}
        sec
        sbc tmp
        beq +
        bcc +
        sta off{N}
        jmp ++
+       lda #$fe
        sta off{N}
++      lda note
        and #$7f
        tax
        bne +
        lda #$fe                ; rest
        sta off{N}
        rts
+       lda flo-1,x
        sta tl{N}
        lda fhi-1,x
        sta th{N}
        lda note
        bmi v{N}gl
        lda tl{N}               ; plain note: jump to pitch and re-attack
        sta cl{N}
        sta $d400+{R}
        lda th{N}
        sta ch{N}
        sta $d401+{R}
        lda #0
        sta gc{N}
        lda #{W}
        sta $d404+{R}
        lda #{W}+1
        sta $d404+{R}
        rts
v{N}gl  sec                     ; glide: step = (target - current) / 32
        lda tl{N}
        sbc cl{N}
        sta sl{N}
        lda th{N}
        sbc ch{N}
        sta sh{N}
        ldx #5
-       lda sh{N}
        cmp #$80                ; carry = sign, for an arithmetic shift
        ror sh{N}
        ror sl{N}
        dex
        bne -
        lda #32
        sta gc{N}
        lda #{W}+1              ; keep the gate on (legato)
        sta $d404+{R}
        rts
v{N}get
v{N}g   lda $ffff
        inc v{N}g+1
        bne +
        inc v{N}g+2
+       rts
'''
asm=f'''; HEX64 MUSIC - "HEXED" BY M0NDE - HTTPS://M0NDE.ITCH.IO
; Player at $9000 with the same entry points as the C64 Circuits player:
;   $9000 start (init + hook IRQ)   $9003 stop (unhook, silence voices 1-2)
;   $9006 two-SID flag (unused here) $9009 init   $900C play   $900F volume 0-15
; Music uses SID 1 voices 1 and 2 only. Voice 3 is left free for sound effects.
; Tempo comes from the KERNAL 60 Hz IRQ, so it is the same on PAL and NTSC;
; init picks the PAL or NTSC pitch table from $02A6.
; $9007 picks the song before start: 0 = Hexed, 1 = Hexed with glides.
; Tune data: note (C1=1 ... B6=72, +128 = glide into it, 0 = rest),
;            duration in ticks, gate ticks (255 = hold); 255 as a note = loop.
        * = $9000
        jmp start
        jmp stop
s2      !byte 0
song    !byte 0                 ; $9007: 0 = song 1 (Hexed), 1 = song 2 (Hexed with glides)
        !byte 0
        jmp init
        jmp play
vol     !byte 12

start   sei
        jsr init
        lda $0315
        cmp #>irq
        beq +
        lda $0314
        sta old
        lda $0315
        sta old+1
        lda #<irq
        sta $0314
        lda #>irq
        sta $0315
+       cli
        rts

stop    sei
        lda $0315
        cmp #>irq
        bne +
        lda old
        sta $0314
        lda old+1
        sta $0315
+       lda #0
        sta $d404
        sta $d40b
        cli
        rts

irq     jsr play
        jmp (old)
old     !word $ea31

init    ldx #71                 ; copy the PAL or NTSC pitch table
-       lda $02a6
        beq +
        lda pallo,x
        sta flo,x
        lda palhi,x
        sta fhi,x
        jmp ++
+       lda ntsclo,x
        sta flo,x
        lda ntschi,x
        sta fhi,x
++      dex
        bpl -
        lda song
        and #1
        tax
        lda t1l,x
        sta st1l
        sta v1g+1
        lda t1h,x
        sta st1h
        sta v1g+2
        lda t2l,x
        sta st2l
        sta v2g+1
        lda t2h,x
        sta st2h
        sta v2g+2
        lda ad1,x
        sta $d405
        lda sr1,x
        sta $d406
        lda #1
        sta cnt1
        sta cnt2
        lda #0
        sta gc1
        sta gc2
        lda #$fe
        sta off1
        sta off2
        lda #$a8                ; voice 2 pad: slow attack 10, decay 8
        sta $d40c
        lda #$8b                ; sustain 8, long release 11
        sta $d40d
        lda #0
        sta $d404
        sta $d40b
        rts

play    lda vol
        and #15
        sta $d418
        jsr v1tick
        jmp v2tick
{VOICE.format(N=1,R=0,W=16)}
{VOICE.format(N=2,R=7,W=16)}
cnt1    !byte 0
cnt2    !byte 0
off1    !byte 0
off2    !byte 0
gc1     !byte 0
gc2     !byte 0
cl1     !byte 0
ch1     !byte 0
cl2     !byte 0
ch2     !byte 0
tl1     !byte 0
th1     !byte 0
tl2     !byte 0
th2     !byte 0
sl1     !byte 0
sh1     !byte 0
sl2     !byte 0
sh2     !byte 0
note    !byte 0
tmp     !byte 0
st1l    !byte 0
st1h    !byte 0
st2l    !byte 0
st2h    !byte 0
t1l     !byte <s1v1,<s2v1       ; per-song start of voice 1 data
t1h     !byte >s1v1,>s2v1
t2l     !byte <s1v2,<s2v2       ; per-song start of voice 2 data
t2h     !byte >s1v2,>s2v2
ad1     !byte $19,$19           ; voice 1 attack/decay per song
sr1     !byte $0a,$5a           ; voice 1 sustain/release: song 2 holds notes for glides
flo     !fill 72,0
fhi     !fill 72,0
{bl("pallo",pl)}
{bl("palhi",ph)}
{bl("ntsclo",nl)}
{bl("ntschi",nh)}
{dat("s1v1",a1)}
{dat("s1v2",b1)}
{dat("s2v1",v1)}
{dat("s2v2",v2)}

; entry points used only by the .sid files (set PAL/NTSC, then init)
sidpal  sta song
        lda #1
        sta $02a6
        jmp init
sidntsc sta song
        lda #0
        sta $02a6
        jmp init
'''
open('hex64-music.asm','w').write(asm)
print('v1 loop s',sum(e[1] for e in v1)/60,' v2 loop s',sum(e[1] for e in v2)/60, 'events',len(v1),len(v2))
