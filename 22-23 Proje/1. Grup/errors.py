#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       errors.py


class InstructionTypeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
