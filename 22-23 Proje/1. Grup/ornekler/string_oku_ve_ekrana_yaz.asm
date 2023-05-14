;
;       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
;       RISC-Mini               2023
;       string_oku_ve_ekrana_yaz.asm

.global
    mvi x9, 10h     ; yeni satır karakterini x9'da sakla

    mvi x1, 2h
    mvi x2, [str0]
    cll

    mvi x1, 4h
    mvi x2, [FFh]
    cll

    mvi x1, 2h
    mvi x2, [str1]
    cll
    mvi x2, [FFh]
    cll
    mvi x2, [str2]
    cll
    mvi x1, 1h
    mov x2, x9
    mvi x3, 4h
    cll

    mov x1, x0
    mov x2, x0
    cll

.store
    dbs str0, "Adınızı girin: "
    dbs str1, "Merhaba, "
    dbs str2, "!"
