#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       processor.py
from data_types import Word


class Processor:
    def __init__(self):
        self.registers = {
            'x0': Word(0),
            'x1': Word(0),
            'x2': Word(0),
            'x3': Word(0),
            'x4': Word(0),
            'x5': Word(0),
            'x6': Word(0),
            'x7': Word(0),
            'x8': Word(0),
            'x9': Word(0),
            'x10': Word(0),
            'x11': Word(0),
            'x12': Word(0),
            'x13': Word(0),
            'x14': Word(0),
            'x15': Word(0),
            'x16': Word(0),
            'x17': Word(0),
            'x18': Word(0),
            'x19': Word(0),
            'x20': Word(0),
            'x21': Word(0),
            'x22': Word(0),
            'x23': Word(0),
            'x24': Word(0),
            'x25': Word(0),
            'x26': Word(0),
            'x27': Word(0),
            'x28': Word(0),
            'x29': Word(0),
            'x30': Word(0),
            'x31': Word(0)
        }
