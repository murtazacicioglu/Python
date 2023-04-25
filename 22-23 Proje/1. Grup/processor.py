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
        self._integer_registers = {"x0": register.IntegerRegister("x0", 0, "zero", "Hard-wired zero"),
                                   "x1": register.IntegerRegister("x1", 0, "ra", "Return address"),
                                   "x2": register.IntegerRegister("x2", 0, "sp", "Stack pointer"),
                                   "x3": register.IntegerRegister("x3", 0, "gp", "Global pointer"),
                                   "x4": register.IntegerRegister("x4", 0, "tp", "Thread pointer"),
                                   "x5": register.IntegerRegister("x5", 0, "t0", "Temporary/alternate link register"),
                                   "x6": register.IntegerRegister("x6", 0, "t1", "Temporaries"),
                                   "x7": register.IntegerRegister("x7", 0, "t2", "Temporaries"),
                                   "x8": register.IntegerRegister("x8", 0, "s0/fp", "Saved register/frame pointer"),
                                   "x9": register.IntegerRegister("x9", 0, "s1", "Saved register"),
                                   "x10": register.IntegerRegister("x10", 0, "a0", "Function arguments/return values"),
                                   "x11": register.IntegerRegister("x11", 0, "a1", "Function arguments/return values"),
                                   "x12": register.IntegerRegister("x12", 0, "a2", "Function arguments"),
                                   "x13": register.IntegerRegister("x13", 0, "a3", "Function arguments"),
                                   "x14": register.IntegerRegister("x14", 0, "a4", "Function arguments"),
                                   "x15": register.IntegerRegister("x15", 0, "a5", "Function arguments"),
                                   "x16": register.IntegerRegister("x16", 0, "a6", "Function arguments"),
                                   "x17": register.IntegerRegister("x17", 0, "a7", "Function arguments"),
                                   "x18": register.IntegerRegister("x18", 0, "s2", "Saved registers"),
                                   "x19": register.IntegerRegister("x19", 0, "s3", "Saved registers"),
                                   "x20": register.IntegerRegister("x20", 0, "s4", "Saved registers"),
                                   "x21": register.IntegerRegister("x21", 0, "s5", "Saved registers"),
                                   "x22": register.IntegerRegister("x22", 0, "s6", "Saved registers"),
                                   "x23": register.IntegerRegister("x23", 0, "s7", "Saved registers"),
                                   "x24": register.IntegerRegister("x24", 0, "s8", "Saved registers"),
                                   "x25": register.IntegerRegister("x25", 0, "s9", "Saved registers"),
                                   "x26": register.IntegerRegister("x26", 0, "s10", "Saved registers"),
                                   "x27": register.IntegerRegister("x27", 0, "s11", "Saved registers"),
                                   "x28": register.IntegerRegister("x28", 0, "t3", "Temporaries"),
                                   "x29": register.IntegerRegister("x29", 0, "t4", "Temporaries"),
                                   "x30": register.IntegerRegister("x30", 0, "t5", "Temporaries"),
                                   "x31": register.IntegerRegister("x31", 0, "t6", "Temporaries")}

    @property
    def isa(self):
        return self._ISA
