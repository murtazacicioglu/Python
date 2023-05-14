;
;       Ferit Yiğit BALABAN,    <fybalaban@fybx.dev>
;       RISC-Mini               2023
;       çarp ve ekrana yaz.asm

.global
    mvi x1, 5h	 ; çarpılacak değer (1)
    mvi x2, 4h	 ; çarpılacak değer (2)
    stm x1, [0h]
    stm x2, [1h]
    lfm x1, [0h] ; 0x00 adresinden değer oku, x1'de sakla
    lfm x2, [1h] ; 0x01 adresinden değer oku, x2'de sakla
    jmp mul	 ; mul section'ına atla
    mvi x1, 1h	 ; x1'de 1 değerini sakla
    mvi x3, 1h	 ; x3'te 1 değerini sakla
    cll          ; sistem çağrısı (1,x2,1) [EKRANA YAZ]

    mov x1, x0	 ; x1'de 0 değerini sakla
    mov x2, x0	 ; durum kodu 0	
    cll          ; sistem çağrısı (0) [HALT]

.mul
    mov x4, x2
    mvi x2, 0h
    add x2, x2, x4
    mvi x3, 1h
    sub x1, x1, x3
    ble x1, x0, [global+6h]
    jmp [mul+2h]
