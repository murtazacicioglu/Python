#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       isa.py
import processor
from data_types import Word


def isa_add(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    proc.registers[rd] = Word(proc.registers[rs1].value + proc.registers[rs2].value)


def isa_inv(proc: processor.Processor, rd: str):
    proc.registers[rd] = Word(-1 * proc.registers[rd].value)

