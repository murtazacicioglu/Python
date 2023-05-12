#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       parser.py
import data_types
import memory


BRANCHING = ["jmp", "beq", "bne", "bge", "ble"]


class Parser:
    def __init__(self):
        self.__intermediate = ""

