.global
    lfm x1, [0x00] ; 0x00 adresinden değer oku, x1'de sakla
    lfm x2, [0x01] ; 0x01 adresinden değer oku, x2'de sakla
    jmp mul        ; mul section'ına atla
    mvi x1, 1h     ; x1'de 1 değerini sakla
    mvi x3, 1h     ; x3'te 1 değerini sakla
    cll            ; sistem çağrısı (1,x2,1) [EKRANA YAZ]
    mov x1, x0     ; x1'de 0 değerini sakla (x0 daima 0 tutuyor)
    cll            ; sistem çağrısı (0) [HALT]


.mul
    add x2, x2, x2
    mvi x3, 1h
    sub x1, x1, x3
    add x30, x30, x3
    ble x1, x0, [global+101h]
    jmp mul
