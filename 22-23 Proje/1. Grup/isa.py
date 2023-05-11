#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       isa.py
import processor
from data_types import Word


def isa_add(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    _rd = Word(0)

    _rd = Word(proc.registers[rs1].value + proc.registers[rs2].value)

    # carry bayrağı hesaplama, işaretsiz sayı desteği yok
    proc.flags["Z"] = Word(1 if _rd.value == 0 else 0)
    proc.flags["S"] = Word(0 if _rd.value >= 0 else 1)
    proc.flags["V"] = Word(1 if (_rs1 > 0 > _rd.value and _rs2 > 0) or (_rs1 < 0 < _rd.value and _rs2 < 0) else 0)
    proc.registers[rd] = _rd


def isa_inv(proc: processor.Processor, rd: str):
    _prev_rd = proc.registers[rd].value
    _rd = Word(-1 * proc.registers[rd].value)

    # carry bayrağı hesaplama, işaretsiz sayı desteği yok
    proc.flags["Z"] = Word(1 if _rd.value == 0 else 0)
    proc.flags["S"] = Word(0 if _rd.value >= 0 else 1)
    proc.flags["V"] = Word(1 if _prev_rd == _rd.value else 0)
    proc.registers[rd] = _rd


def isa_sub(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    _rd = Word(0)

    _rd = Word(_rs1 - _rs2)

    proc.flags["C"] = Word(0 if _rs2 >= _rs1 else 1)
    proc.flags["Z"] = Word(1 if _rd.value == 0 else 0)
    proc.flags["S"] = Word(0 if _rd.value >= 0 else 1)
    proc.flags["V"] = Word(1 if (_rs1 > 0 > _rs2 and _rd.value < 0) or (_rs1 < 0 < _rs2 and _rd.value > 0) else 0)
    proc.registers[rd] = _rd

def isa_nop(proc: processor.Processor):
    proc.registers["x0"] = Word(proc.registers["x0"].value)
    proc.flags["C"] = Word(0)
    proc.flags["Z"] = Word(0)
    proc.flags["S"] = Word(0)
    proc.flags["V"] = Word(0)
