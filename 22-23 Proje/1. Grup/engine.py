#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       engine.py
import memory
import parser
import processor


class Engine:
    def __init__(self):
        self.__cpu = processor.Processor()
        self.__ram = memory.Memory()
        self.__parser = parser.Parser()
        self.__delay = 1

