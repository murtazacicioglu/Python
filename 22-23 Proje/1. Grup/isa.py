#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       isa.py
import processor
import memory
from data_types import Word


def isa_add(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    _rd = Word(0)

    _rd = Word(_rs1 + _rs2)

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


def isa_slt(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    proc.registers[rd] = Word(_rs1 if _rs1 < _rs2 else _rs2)


def isa_nop(proc: processor.Processor):
    proc.registers["x0"] = Word(proc.registers["x0"].value)
    proc.flags["C"] = Word(0)
    proc.flags["Z"] = Word(0)
    proc.flags["S"] = Word(0)
    proc.flags["V"] = Word(0)


def isa_lfm(proc: processor.Processor, mem: memory.Memory, rd: str, hex_value: str):
    _rd = mem.read_memory(Word(0).from_hex(hex_value[:-1]))
    proc.registers[rd] = _rd


def isa_stm(proc: processor.Processor, mem: memory.Memory, rd: str, hex_value: str):
    _rd = proc.registers[rd]
    mem.set_memory(Word(0).from_hex(hex_value[:-1]), _rd)


def isa_mov(proc: processor.Processor, rd: str, rs1: str):
    _rs1 = proc.registers[rs1]
    proc.registers[rd] = _rs1


def isa_mvi(proc: processor.Processor, rd: str, hex_value: str):
    _rd = Word(0).from_hex(hex_value[:-1])
    proc.registers[rd] = _rd


def isa_and(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    _rd = Word(_rs1 & _rs2)

    proc.registers[rd] = _rd


def isa_or(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    _rd = Word(_rs1 | _rs2)

    proc.registers[rd] = _rd


def isa_xor(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    _rd = Word(_rs1 ^ _rs2)

    proc.registers[rd] = _rd


def isa_shl(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rep = proc.registers[rs1].as_binary()
    _rs2 = proc.registers[rs2].value

    for i in range(0, _rs2):
        _rep = _rep[1:]
        _rep += "0"

    proc.registers[rd] = Word(0).from_binary(_rep)


def isa_shr(proc: processor.Processor, rd: str, rs1: str, rs2: str):
    _rep = proc.registers[rs1].as_binary()
    _rs2 = proc.registers[rs2].value

    for i in range(0, _rs2):
        _rep = _rep[:-1]
        _rep = "0" + _rep

    proc.registers[rd] = Word(0).from_binary(_rep)


def isa_jmp(proc: processor.Processor, section: str):
    proc.registers["x30"] = proc.prog_counter
    proc.prog_counter = Word(0).from_hex(section[:-1])


def isa_ble(proc: processor.Processor, rs1: str, rs2: str, section: str):
    _rs1 = proc.registers[rs1].value
    _rs2 = proc.registers[rs2].value
    if _rs1 <= _rs2:
        isa_jmp(proc, section)


def isa_cll(proc: processor.Processor):
    proc.parent.signal_syscall(proc.registers["x1"], proc.registers["x2"], proc.registers["x3"])
