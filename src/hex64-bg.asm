; HEX64BG helper at $C800 - SYS 51200
; Copies the loader background (screen $C000, colour $C400) to the screen,
; then restores the 21 background piles ($C900 -> characters 74-115 at $3A50).
        * = $c800
        ldx #0
-       lda $c000,x
        sta $0400,x
        lda $c100,x
        sta $0500,x
        lda $c200,x
        sta $0600,x
        lda $c300,x
        sta $0700,x
        lda $c400,x
        sta $d800,x
        lda $c500,x
        sta $d900,x
        lda $c600,x
        sta $da00,x
        lda $c700,x
        sta $db00,x
        lda $c900,x
        sta $3a50,x
        inx
        bne -
        ldx #79
-       lda $ca00,x
        sta $3b50,x
        dex
        bpl -
        rts
