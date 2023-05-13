#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       engine.py
import data_types
import memory
import parser
from processor import Processor
from time import sleep


class Engine:
    def __init__(self):
        self.__ram = memory.Memory()
        self.__cpu = Processor(self.__ram, self)
        self.__parser = parser.Parser()
        self.__delay = 1
        self.__status = False
        self.__print_decoding = True 
        self.__print_registers = True

    def load_source_code(self, source_code: str):
        self.__parser.parse_code(source_code)
        self.__parser.load_to_memory(self.__ram)

    def set_frequency(self, frequency: float):
        """
        Çalıştırma motorunun her işlem arasına getirdiği gecikmeyi milisaniye cinsinden ayarlar.
        Gecikme (ms) = 1000 / frequency
        :param frequency: Saniye başına satır çalıştırma hızı
        """
        self.__delay = 1000 / frequency

    def get_frequency(self) -> float:
        """
        Motorun çalışma frekansını döndürür.
        :return: Çalışma frekansı olan tam sayı
        """
        return 1000 / self.__delay

    def step(self):
        c_point = self.__cpu.prog_counter
        c_instr = self.__ram.read_code(c_point)
        if self.__print_decoding:
            print(f"decode: {c_instr}")
        self.__cpu.decode(c_instr)
        if self.__print_registers:
            print(f"x0: {self.__cpu.registers['x0'].as_hexadecimal()} "
                  f"x1: {self.__cpu.registers['x1'].as_hexadecimal()} "
                  f"x2: {self.__cpu.registers['x2'].as_hexadecimal()}")
        if c_instr[0:3] != "jmp":
            self.__cpu.prog_counter = data_types.Word(self.__cpu.prog_counter.value + 1)
        sleep(0.001 * self.__delay)

    def run(self):
        self.__status = True
        while self.__status:
            self.step()

    def signal_syscall(self, *args):
        if args:
            # halt
            if args[0].value == 0:
                self.__status = False
            # print value stored in register
            if args[0].value == 1:
                w = args[1]
                nf = args[2].value
                if nf == 0:
                    print(w.as_binary())
                elif nf == 1:
                    print(w.value)
                elif nf == 2:
                    print(w.as_hexadecimal())
                elif nf == 3:
                    print(w.as_utf8(), end="")
            # print string
            if args[0].value == 2:
                _iter = args[1]
                next_char = self.__ram.read_memory(_iter)
                while next_char.value != 0:
                    print(next_char.as_utf8(), end="")
                    _iter = data_types.Word(_iter.value + 1)
                    next_char = self.__ram.read_memory(_iter)
            # read char to memory
            if args[0].value == 3:
                char = input("")
                if char:
                    self.__ram.set_memory(args[1], data_types.Word(0).from_utf8(char[0]))
                else:
                    self.__ram.set_memory(args[1], data_types.Word(0))
            # read string to memory
            if args[0].value == 4:
                string = input("")
                mem = args[1]
                for char in string:
                    self.__ram.set_memory(mem, data_types.Word(0).from_utf8(char))
                    mem = data_types.Word(mem.value + 1)
            # read number to register
            if args[0].value == 5:
                string = input("")
                w: Word
                try:
                    if args[1] == 0:
                        w = data_types.Word(0).as_binary(string)
                    elif args[1] == 1:
                        w = data_types.Word(int(string))
                    elif args[1] == 2:
                        w = data_types.Word(0).as_hexadecimal(string[:-1])
                except Exception:
                    self.__cpu.registers["x3"] = data_types.Word(1)

