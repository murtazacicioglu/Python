#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       processor.py
import data_types


class Processor:
    def __init__(self):
        self.registers = {f'x{i}': data_types.Word(0) for i in range(32)}


