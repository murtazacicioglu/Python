#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       instruction.py
import data_types


class Instruction:
    type: str
    mnemonic: str
    width = 32
    instruction = data_types.Word(0)

    def __init__(self, inst_type: str, binary_rep: str, mnemonic: str):
        inst_type = inst_type.lower()
        if inst_type != "r" and inst_type != "i" and inst_type != "sb" and inst_type != "uj":
            raise AttributeError("Instruction tipi R, I, SB veya UJ olmalı!")
        self.type = inst_type
        self.mnemonic = mnemonic
        self.instruction.from_binary(binary_rep)

    def set_opcode(self, int_value: int) -> None:
        """
        Verilen ondalık sayıyı opcode (6-0) olarak ayarlar.
        :param int_value: Ayarlanacak sayı
        """
        self.instruction.set_rrange(6, 0, bin(int_value)[2:])

    def set_rd(self, int_value: int) -> None:
        """
        Verilen ondalık sayıyı rd (11-7) olarak ayarlar.
        :param int_value: Ayarlanacak sayı
        """
        self.instruction.set_rrange(11, 7, bin(int_value)[2:])

    def set_rs1(self, int_value: int) -> None:
        """
        Verilen ondalık sayıyı rs1 (19-15) olarak ayarlar.
        :param int_value: Ayarlanacak sayı
        """
        self.instruction.set_rrange(19, 15, bin(int_value)[2:])

    def set_rs2(self, int_value: int) -> None:
        """
        Verilen ondalık sayıyı rs2 (24-20) olarak ayarlar.
        :param int_value: Ayarlanacak sayı
        """
        self.instruction.set_rrange(24, 20, bin(int_value)[2:])

    def set_funct3(self, int_value: int) -> None:
        """
        Verilen ondalık sayıyı funct3 (14-12) olarak ayarlar.
        :param int_value: Ayarlanacak sayı
        """
        self.instruction.set_rrange(14, 12, bin(int_value)[2:])

    def set_funct7(self, int_value: int) -> None:
        """
        Verilen ondalık sayıyı funct7 (31-25) olarak ayarlar.
        :param int_value: Ayarlanacak sayı
        """
        self.instruction.set_rrange(31, 25, bin(int_value)[2:])

    def get_opcode(self):
        return self.instruction.as_binary()[-7:]
