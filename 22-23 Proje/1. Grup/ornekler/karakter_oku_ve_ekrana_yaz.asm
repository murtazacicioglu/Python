;
;       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
;       RISC-Mini               2023
;       karakter_oku_ve_ekrana_yaz.asm

.global
    mvi x9, Ah          ; yeni satır karakterini x9 yazmacında tut
    mvi x1, 2h          ;  2 numaralı sistem çağrısını hazırla
    mvi x2, [str0]      ; "Bir karakter giriniz: " stringinin bellek adresini sakla
    cll                 ; çağrı: ekrana string yaz

    mvi x1, 3h          ; 3 numaralı sistem çağrısı
    mvi x2, [FFh]       ; okunan karakterin bellekte saklanacağı adresi ver
    cll                 ; çağrı: klavyeden karakter oku

    mvi x1, 2h
    mvi x2, [str1]
    cll

    mvi x1, 2h
    mvi x2, [FFh]       ; okunan karakterin bellek adresini sakla
    cll                 ; okunan karakteri ekrana yaz

    mvi x1, 1h          ; 1 numaralı sistem çağrısını hazırla
    mov x2, x9          ; x9'daki yeni satır karakterini sakla
    mvi x3, 3h          ; ekrana yazma modunu utf8 olarak ayarla
    cll                 ; çağrı: yazmaç değerini ekrana yaz

    mov x1, x0          ; çağrı: halt
    mov x2, x0		; durum kodu 0
    cll

.store
    dbs str0, "Bir karakter giriniz: "
    dbs str1, "Okunan karakter: "
