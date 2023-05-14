;
;       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
;       RISC-Mini               2023
;       fonksiyon_testi.asm

.global
    mvi x9, Ah      ; x9 yazmacında yeni satır karakterini tut

    jmp fonksiyon1

    mvi x2, [str3]
    cll

    jmp fonksiyon2

    mov x1, x0
    mov x2, x0
    cll

.fonksiyon1
    mvi x1, 1h
    mvi x2, [str1]
    cll
    jmp [global+2h]

.fonksiyon2
    mvi x1, 1h
    mvi x2, [str2]
    cll
    jmp [global+5h]

.store
    dbs str1, "Fonksiyon 1: selam!"
    dbs str2, "Fonksiyon 2: selam!"
    dbs str3, "Global: yine buradayız!"
