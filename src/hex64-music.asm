; HEX64 MUSIC - "HEXED" BY M0NDE - HTTPS://M0NDE.ITCH.IO
; Player at $9000 with the same entry points as the C64 Circuits player:
;   $9000 start (init + hook IRQ)   $9003 stop (unhook, silence voices 1-2)
;   $9006 two-SID flag (unused here) $9009 init   $900C play   $900F volume 0-15
; Music uses SID 1 voices 1 and 2 only. Voice 3 is left free for sound effects.
; Tempo comes from the KERNAL 60 Hz IRQ, so it is the same on PAL and NTSC;
; init picks the PAL or NTSC pitch table from $02A6.
; $9007 picks the song before start: 0 = Hexed, 1 = Hexed Glide, 2 = Hexed Calm
; (only the long tones: each group of four plucks becomes one held note).
; Tune data: note (C1=1 ... B6=72, +128 = glide into it, 0 = rest),
;            duration in ticks, gate ticks (255 = hold); 255 as a note = loop.
        * = $9000
        jmp start
        jmp stop
s2      !byte 0
song    !byte 2                 ; $9007: 0 = Hexed, 1 = Hexed Glide, 2 = Hexed Calm
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
        cmp #3
        bcc +
        lda #2
+       tax
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

; ---- voice 1: SID register offset 0 ----
v1tick
        lda gc1               ; glide in progress?
        beq ++
        clc
        lda cl1
        adc sl1
        sta cl1
        lda ch1
        adc sh1
        sta ch1
        dec gc1
        bne +
        lda tl1               ; glide finished: land exactly on the note
        sta cl1
        lda th1
        sta ch1
+       lda cl1
        sta $d400+0
        lda ch1
        sta $d401+0
++      dec cnt1
        lda cnt1
        cmp off1
        bne +
        lda #16
        sta $d404+0           ; gate off: the release fades out
+       lda cnt1
        beq v1next
        rts
v1next
        jsr v1get
        cmp #$ff
        bne +
        lda st1l              ; end of data: loop to the song's start
        sta v1g+1
        lda st1h
        sta v1g+2
        jmp v1next
+       sta note
        jsr v1get
        sta cnt1
        jsr v1get             ; gate length; 255 = hold to the end
        sta tmp
        lda cnt1
        sec
        sbc tmp
        beq +
        bcc +
        sta off1
        jmp ++
+       lda #$fe
        sta off1
++      lda note
        and #$7f
        tax
        bne +
        lda #$fe                ; rest
        sta off1
        rts
+       lda flo-1,x
        sta tl1
        lda fhi-1,x
        sta th1
        lda note
        bmi v1gl
        lda tl1               ; plain note: jump to pitch and re-attack
        sta cl1
        sta $d400+0
        lda th1
        sta ch1
        sta $d401+0
        lda #0
        sta gc1
        lda #16
        sta $d404+0
        lda #16+1
        sta $d404+0
        rts
v1gl  sec                     ; glide: step = (target - current) / 32
        lda tl1
        sbc cl1
        sta sl1
        lda th1
        sbc ch1
        sta sh1
        ldx #5
-       lda sh1
        cmp #$80                ; carry = sign, for an arithmetic shift
        ror sh1
        ror sl1
        dex
        bne -
        lda #32
        sta gc1
        lda #16+1              ; keep the gate on (legato)
        sta $d404+0
        rts
v1get
v1g   lda $ffff
        inc v1g+1
        bne +
        inc v1g+2
+       rts


; ---- voice 2: SID register offset 7 ----
v2tick
        lda gc2               ; glide in progress?
        beq ++
        clc
        lda cl2
        adc sl2
        sta cl2
        lda ch2
        adc sh2
        sta ch2
        dec gc2
        bne +
        lda tl2               ; glide finished: land exactly on the note
        sta cl2
        lda th2
        sta ch2
+       lda cl2
        sta $d400+7
        lda ch2
        sta $d401+7
++      dec cnt2
        lda cnt2
        cmp off2
        bne +
        lda #16
        sta $d404+7           ; gate off: the release fades out
+       lda cnt2
        beq v2next
        rts
v2next
        jsr v2get
        cmp #$ff
        bne +
        lda st2l              ; end of data: loop to the song's start
        sta v2g+1
        lda st2h
        sta v2g+2
        jmp v2next
+       sta note
        jsr v2get
        sta cnt2
        jsr v2get             ; gate length; 255 = hold to the end
        sta tmp
        lda cnt2
        sec
        sbc tmp
        beq +
        bcc +
        sta off2
        jmp ++
+       lda #$fe
        sta off2
++      lda note
        and #$7f
        tax
        bne +
        lda #$fe                ; rest
        sta off2
        rts
+       lda flo-1,x
        sta tl2
        lda fhi-1,x
        sta th2
        lda note
        bmi v2gl
        lda tl2               ; plain note: jump to pitch and re-attack
        sta cl2
        sta $d400+7
        lda th2
        sta ch2
        sta $d401+7
        lda #0
        sta gc2
        lda #16
        sta $d404+7
        lda #16+1
        sta $d404+7
        rts
v2gl  sec                     ; glide: step = (target - current) / 32
        lda tl2
        sbc cl2
        sta sl2
        lda th2
        sbc ch2
        sta sh2
        ldx #5
-       lda sh2
        cmp #$80                ; carry = sign, for an arithmetic shift
        ror sh2
        ror sl2
        dex
        bne -
        lda #32
        sta gc2
        lda #16+1              ; keep the gate on (legato)
        sta $d404+7
        rts
v2get
v2g   lda $ffff
        inc v2g+1
        bne +
        inc v2g+2
+       rts

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
t1l     !byte <s1v1,<s2v1,<s3v1 ; per-song start of voice 1 data
t1h     !byte >s1v1,>s2v1,>s3v1
t2l     !byte <s1v2,<s2v2,<s1v2 ; per-song start of voice 2 data (Calm uses the Hexed bass)
t2h     !byte >s1v2,>s2v2,>s1v2
ad1     !byte $19,$19,$5a       ; voice 1 attack/decay per song (Calm swells in)
sr1     !byte $0a,$5a,$6b       ; voice 1 sustain/release: songs 2 and 3 hold notes
flo     !fill 72,0
fhi     !fill 72,0
pallo !byte 45,78,113,150,190,231,20,66,116,169,224,27,90,156,226,45,123,207,39,133,232,81,193,55
      !byte 180,56,196,89,247,157,78,10,208,162,129,109,103,112,137,178,237,59,156,19,160,69,2,218
      !byte 206,224,17,100,218,118,57,38,64,137,4,180,156,192,35,200,180,235,114,76,128,18,8,104
palhi !byte 2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,5,5,5,6,6,6,7,7,8
      !byte 8,9,9,10,10,11,12,13,13,14,15,16,17,18,19,20,21,23,24,26,27,29,31,32
      !byte 34,36,39,41,43,46,49,52,55,58,62,65,69,73,78,82,87,92,98,104,110,117,124,131
ntsclo !byte 24,56,90,126,164,204,247,36,84,134,188,245,49,113,180,252,72,152,237,72,167,12,120,233
       !byte 98,226,105,248,144,48,219,143,78,25,240,211,196,195,209,240,31,97,182,30,157,50,223,166
       !byte 136,134,163,224,63,194,107,61,58,100,190,76,15,12,70,191,125,132,214,122,115,200,125,151
ntschi !byte 2,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,5,5,5,6,6,7,7,7
       !byte 8,8,9,9,10,11,11,12,13,14,14,15,16,17,18,19,21,22,23,25,26,28,29,31
       !byte 33,35,37,39,42,44,47,50,53,56,59,63,67,71,75,79,84,89,94,100,106,112,119,126
s1v1 !byte 37,26,5,44,26,5,51,26,5,53,26,5,56,26,5,53,26,5,51,26,5,44,26,5
     !byte 34,26,5,41,26,5,46,26,5,49,26,5,53,26,5,49,26,5,46,26,5,41,26,5
     !byte 30,26,5,37,26,5,46,26,5,49,26,5,56,26,5,49,26,5,46,26,5,37,26,5
     !byte 32,26,5,39,26,5,44,26,5,46,26,5,51,26,5,46,26,5,44,26,5,39,26,5
     !byte 53,26,5,0,26,5,56,26,5,0,26,5,51,26,5,0,26,5,49,26,5,0,26,5
     !byte 49,26,5,0,26,5,53,26,5,0,26,5,46,26,5,0,26,5,44,26,5,0,26,5
     !byte 46,26,5,0,26,5,49,26,5,0,26,5,56,26,5,0,26,5,53,26,5,0,26,5
     !byte 51,26,5,0,26,5,44,26,5,0,26,5,46,26,5,0,26,5,51,26,5,0,26,5
     !byte 37,26,5,44,26,5,51,26,5,53,26,5,56,26,5,53,26,5,51,26,5,44,26,5
     !byte 34,26,5,41,26,5,46,26,5,49,26,5,53,26,5,49,26,5,46,26,5,41,26,5
     !byte 30,26,5,37,26,5,46,26,5,49,26,5,56,26,5,49,26,5,46,26,5,37,26,5
     !byte 32,26,5,39,26,5,44,26,5,46,26,5,51,26,5,46,26,5,44,26,5,39,26,5
     !byte 53,26,5,0,26,5,56,26,5,0,26,5,51,26,5,0,26,5,49,26,5,0,26,5
     !byte 49,26,5,0,26,5,53,26,5,0,26,5,46,26,5,0,26,5,44,26,5,0,26,5
     !byte 46,26,5,0,26,5,49,26,5,0,26,5,56,26,5,0,26,5,53,26,5,0,26,5
     !byte 51,26,5,0,26,5,44,26,5,0,26,5,46,26,5,0,26,5,51,26,5,0,26,5
     !byte 255
s1v2 !byte 25,208,196,22,208,196,18,208,196,20,208,196,25,208,196,22,208,196,18,208,196,20,208,196
     !byte 25,208,196,22,208,196,18,208,196,20,208,196,25,208,196,22,208,196,18,208,196,20,208,196
     !byte 255
s2v1 !byte 37,68,60,44,34,5,51,34,5,53,34,5,56,102,255,181,68,60,49,34,5,46,34,5
     !byte 41,34,5,46,102,255,177,68,60,46,34,5,49,34,5,56,34,5,53,102,255,179,68,60
     !byte 44,34,5,46,34,5,51,34,5,46,102,255,181,136,255,184,136,126,53,136,255,177,136,126
     !byte 46,136,255,177,136,255,179,136,255,174,136,255,165,68,60,44,34,5,51,34,5,53,34,5
     !byte 56,102,255,181,68,60,49,34,5,46,34,5,41,34,5,46,102,255,177,68,60,46,34,5
     !byte 49,34,5,56,34,5,53,102,255,179,68,60,44,34,5,46,34,5,51,34,5,46,102,255
     !byte 181,136,255,184,136,126,53,136,255,177,136,126,46,136,255,177,136,255,179,136,255,174,136,255
     !byte 255
s2v2 !byte 25,136,255,153,136,124,22,136,255,150,136,124,18,136,255,146,136,124,20,136,255,148,136,255
     !byte 153,136,255,153,136,124,22,136,255,150,136,124,18,136,255,146,136,124,20,136,255,148,136,255
     !byte 153,136,255,153,136,124,22,136,255,150,136,124,18,136,255,146,136,124,20,136,255,148,136,255
     !byte 153,136,255,153,136,124,22,136,255,150,136,124,18,136,255,146,136,124,20,136,255,148,136,255
     !byte 255

s3v1 !byte 37,104,88,56,104,88,34,104,88,53,104,88,30,104,88,56,104,88,32,104,88,51,104,88
     !byte 53,104,88,51,104,88,49,104,88,46,104,88,46,104,88,56,104,88,51,104,88,46,104,88
     !byte 37,104,88,56,104,88,34,104,88,53,104,88,30,104,88,56,104,88,32,104,88,51,104,88
     !byte 53,104,88,51,104,88,49,104,88,46,104,88,46,104,88,56,104,88,51,104,88,46,104,88
     !byte 255

; entry points used only by the .sid files (set PAL/NTSC, then init)
sidpal  sta song
        lda #1
        sta $02a6
        jmp init
sidntsc sta song
        lda #0
        sta $02a6
        jmp init
