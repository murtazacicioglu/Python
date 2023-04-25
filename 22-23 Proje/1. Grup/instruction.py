#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       instruction.py
import data_types
import errors
from enum import Enum


class InstructionType(Enum):
    R, I, S, B, U, J = range(6)


class Instruction:
    type: InstructionType
    mnemonic: str
    width = 32
    instruction = data_types.Word(0)

    def __init__(self, inst_type: InstructionType, binary_rep: str, mnemonic: str):
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

    def get_rd(self):
        if self.type in {InstructionType.S, InstructionType.B}:
            raise errors.InstructionTypeError(f"{self.type.name} tipli komutta RD'ye ulaşılmaya çalışıldı.")
        return self.instruction.as_binary()[-12:-7]

    def get_rs1(self):
        if self.type in {InstructionType.U, InstructionType.J}:
            raise errors.InstructionTypeError(f"{self.type.name} tipli komutta RS1'e ulaşılmaya çalışıldı.")
        return self.instruction.as_binary()[-20:-15]

    def get_rs2(self):
        if self.type in {InstructionType.I, InstructionType.U, InstructionType.J}:
            raise errors.InstructionTypeError(f"{self.type.name} tipli komutta RS2'e ulaşılmaya çalışıldı.")
        return self.instruction.as_binary()[-25:-20]

    def get_funct3(self):
        if self.type in {InstructionType.U, InstructionType.J}:
            raise errors.InstructionTypeError(f"{self.type.name} tipli komutta FUNCT3'e ulaşılmaya çalışıldı.")
        return self.instruction.as_binary()[-15:-12]

    def get_funct7(self):
        if self.type != InstructionType.R:
            raise errors.InstructionTypeError(f"{self.type.name} tipli komutta FUNCT7'e ulaşılmaya çalışıldı.")
        return self.instruction.as_binary()[-32:-25]
