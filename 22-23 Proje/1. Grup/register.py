#!/usr/bin/env python3
#
#         Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
import re
import expressions
import data_types


class IntegerRegister:
    _type = "integer_rv32I"
    stored_value: data_types.Word
    address: str
    abi_name: str
    desc: str

    def __init__(self, address: str, value: int, abi_name="", desc=""):
        if re.match(expressions.exp_regaddr_rv32i, address):
            self.address = address
        else:
            raise AttributeError("IntegerRegister adresi RV32I ISA'e uygun değil. Kabul edilen aralık: x0 - x31!")
        self.stored_value = data_types.Word(value)
        self.abi_name = abi_name
        self.desc = desc

    @property
    def type(self):
        return self._type
