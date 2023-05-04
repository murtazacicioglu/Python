#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       isa_rv32i.py
from instruction import Instruction, InstructionType


class ISA_RV32I:
    inst: dict[Instruction]

    def __init__(self):
        pass

    def __populate_dict(self):
        self.instruction_dict = {
            "ADD":   Instruction(InstructionType.R, "00000000000000000000000000110011", "add"),
            "SUB":   Instruction(InstructionType.R, "01000000000000000000000000110011", "sub"),
            "SLT":   Instruction(InstructionType.R, "00000000000000000010000000110011", "slt"),
            "SLTU":  Instruction(InstructionType.R, "00000000000000000011000000110011", "sltu"),
            "LUI":   Instruction(InstructionType.U, "00000000000000000000000000110111", "lui"),
            "AUIPC": Instruction(InstructionType.U, "00000000000000000000000000010111", "auipc"),
            "ADDI":  Instruction(InstructionType.I, "00000000000000000000000000010011", "addi"),
            "SLTI":  Instruction(InstructionType.I, "00000000000000000010000000010011", "slti"),
            "SLTIU": Instruction(InstructionType.I, "00000000000000000011000000010011", "sltiu")
        }
