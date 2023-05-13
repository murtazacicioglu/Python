#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       processor.py
import memory
from data_types import Word


class Processor:
    def __init__(self, mem: memory.Memory, parent):
        self.prog_counter = Word(0)
        self.registers = {
            'x0': Word(0),
            'x1': Word(0),
            'x2': Word(0),
            'x3': Word(0),
            'x4': Word(0),
            'x5': Word(0),
            'x6': Word(0),
            'x7': Word(0),
            'x8': Word(0),
            'x9': Word(0),
            'x10': Word(0),
            'x11': Word(0),
            'x12': Word(0),
            'x13': Word(0),
            'x14': Word(0),
            'x15': Word(0),
            'x16': Word(0),
            'x17': Word(0),
            'x18': Word(0),
            'x19': Word(0),
            'x20': Word(0),
            'x21': Word(0),
            'x22': Word(0),
            'x23': Word(0),
            'x24': Word(0),
            'x25': Word(0),
            'x26': Word(0),
            'x27': Word(0),
            'x28': Word(0),
            'x29': Word(0),
            'x30': Word(0),
            'x31': Word(0)
        }
        self.flags = {
            "C": Word(0),
            "Z": Word(0),
            "N": Word(0),
            "V": Word(0),
            "XLEN": Word(32)
        }
        self.memory = mem
        self.parent = parent

    # noinspection PyUnboundLocalVariable,PyMethodMayBeStatic
    def decode(self, code: str) -> None:
        import isa

        if " " in code:
            opcode, operands = code.split(maxsplit=1)
            operands = [operand.strip() for operand in operands.split(" ")]
        else:
            opcode = code.strip()

        if opcode == "add":
            isa.isa_add(self, operands[0], operands[1], operands[2])
        elif opcode == "inv":
            isa.isa_inv(self, operands[0])
        elif opcode == "sub":
            isa.isa_sub(self, operands[0], operands[1], operands[2])
        elif opcode == "slt":
            isa.isa_slt(self, operands[0], operands[1], operands[2])
        elif opcode == "nop":
            isa.isa_nop(self)
        elif opcode == "lfm":
            isa.isa_lfm(self, self.memory, operands[0], operands[1])
        elif opcode == "stm":
            isa.isa_stm(self, self.memory, operands[0], operands[1])
        elif opcode == "mov":
            isa.isa_mov(self, operands[0], operands[1])
        elif opcode == "mvi":
            isa.isa_mvi(self, operands[0], operands[1])
        elif opcode == "and":
            isa.isa_and(self, operands[0], operands[1], operands[2])
        elif opcode == "or":
            isa.isa_or(self, operands[0], operands[1], operands[2])
        elif opcode == "xor":
            isa.isa_xor(self, operands[0], operands[1], operands[2])
        elif opcode == "shl":
            isa.isa_shl(self, operands[0], operands[1], operands[2])
        elif opcode == "shr":
            isa.isa_shr(self, operands[0], operands[1], operands[2])
        elif opcode == "jmp":
            isa.isa_jmp(self, operands[0])
        # elif opcode == "beq":
        #     isa.isa_beq(self, operands[0], operands[1], operands[2])
        # elif opcode == "bne":
        #     isa.isa_bne(self, operands[0], operands[1], operands[2])
        # elif opcode == "bge":
        #     isa.isa_bge(self, operands[0], operands[1], operands[2])
        elif opcode == "ble":
            isa.isa_ble(self, operands[0], operands[1], operands[2])
        elif opcode == "cll":
            isa.isa_cll(self)
        else:
            raise ValueError(f"Invalid opcode: {opcode}")
