#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       processor.py
import register


class Processor:
    _ISA = "RV32I"
    _integer_registers = dict[register.IntegerRegister]

    def __init__(self):
        self.__load_registers()

    def __load_registers(self):
        self._integer_registers = {}
        for i in range(32):
            address = f'x{i}'
            self._integer_registers[address] = register.IntegerRegister(address, 0)

    @property
    def isa(self):
        return self._ISA
