; HEX64DATA helper at $4000 - SYS 16384
; Copies the loader background (screen $3800, colour $3C00) to the screen,
; then restores the 21 background piles ($4100 -> characters 74-115 at $3250).
        * = $4000
        ldx #0
-       lda $3800,x
        sta $0400,x
        lda $3900,x
        sta $0500,x
        lda $3a00,x
        sta $0600,x
        lda $3b00,x
        sta $0700,x
        lda $3c00,x
        sta $d800,x
        lda $3d00,x
        sta $d900,x
        lda $3e00,x
        sta $da00,x
        lda $3f00,x
        sta $db00,x
        lda $4100,x
        sta $3250,x
        inx
        bne -
        ldx #79
-       lda $4200,x
        sta $3350,x
        dex
        bpl -
        rts
