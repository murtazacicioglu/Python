#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       errors.py
import instruction


class InstructionTypeError(Exception):
    def __init__(self, inst: instruction.Instruction):
        message = f"{inst.type.name} tipli komutta uyumsuz bir çağrı yürütüldü."
        super().__init__(message)
