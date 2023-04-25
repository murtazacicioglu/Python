#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       instruction.py
import data_types


class Instruction:
    type: str
    width = 32
    instruction = data_types.Word(0)

    def __init__(self, inst_type: str):
        inst_type = inst_type.lower()
        if inst_type != "r" and inst_type != "i" and inst_type != "sb" and inst_type != "uj":
            raise AttributeError("Instruction tipi R, I, SB veya UJ olmalı!")
        self.type = inst_type

    def set_opcode(self, int_value: int):
        self.instruction.set_rrange(6, 0, bin(int_value)[2:])
