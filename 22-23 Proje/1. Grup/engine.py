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
from tkinter import Text


class Engine:
    def __init__(self, konsol: Text, env="tui"):
        self.__ram = memory.Memory()
        self.__cpu = Processor(self.__ram, self)
        self.__parser = parser.Parser()
        self.__delay = 1
        self.__status = True
        self.__print_decoding = False
        self.__print_registers = False
        self.result_code = 0
        self.__environment = env
        self.__console = konsol

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

    def set_debug(self, print_registers, print_decoding):
        """
        Çalışma zamanı motorunun debug seçeneklerini ayarlar.
        :param print_registers: Çalıştırılan her komuttan sonra 0'dan farklı bir değer tutan yazmaçların değerini ekrana onaltılı sistemde yazar
        :param print_decoding: İşlemci tarafından çözülecek ve çalıştırılacak olan komutu ekrana yazar.
        """
        self.__print_registers = print_registers
        self.__print_decoding = print_decoding

    def get_debug(self) -> (bool, bool):
        """
        Çalışma zamanı motorunun debug seçeneklerini demet olarak döndürür.
        :return: (print_registers, print_decoding)
        """
        return self.__print_registers, self.__print_decoding

    def step(self) -> int:
        if not self.__status:
            return -1
        
        c_point = self.__cpu.prog_counter
        c_instr = self.__ram.read_code(c_point)
        if self.__print_decoding:
            print(f"decode: {c_instr}")
        self.__cpu.decode(c_instr)
        if self.__print_registers:
            self.debug_print_registers()
        if c_instr[0:3] != "jmp":
            self.__cpu.prog_counter = data_types.Word(self.__cpu.prog_counter.value + 1)
        sleep(0.001 * self.__delay)
        return 0

    def run(self):
        self.__status = True
        while self.__status:
            self.step()

    def debug_get_registers(self, mode=0) -> str:
        """
        Sıfırdan farklı değer saklayan yazmaçların listesini metin olarak döndürür.
        :param mode: Döndürülecek bilginin sunum formatını belirler (0: konsol çıktısı, 1: grafik arayüz çıktısı)
        :return:
        """
        _x1 = self.__cpu.registers["x1"]
        _x2 = self.__cpu.registers["x2"]
        _x3 = self.__cpu.registers["x3"]
        if mode == 0:
            essential = "[x1: {}h, x2: {}h, x3: {}h]".format(
                _x1.as_hexadecimal(),
                _x2.as_hexadecimal(),
                _x3.as_hexadecimal()
            )
            additional = ""
            for i in range(1, 29):
                key = f"x{i + 3}"
                val = self.__cpu.registers[key]
                if val.value != 0:
                    additional += f" {key}: {val.as_hexadecimal()}h,"
            return essential + additional[:-1]
        elif mode == 1:
            lines = [f"x1: {_x1.as_hexadecimal()}h", f"x2: {_x2.as_hexadecimal()}h", f"x3: {_x3.as_hexadecimal()}h"]
            for i in range(1,29):
                key = f"x{i+3}"
                val = self.__cpu.registers[key]
                if val.value != 0:
                    lines.append(f"{key}: {val.as_hexadecimal()}h")
            return "\n".join(lines)

    def debug_print_registers(self):
        print(self.debug_get_registers())

    def debug_get_memory(self, mode=0) -> str:
        if mode == 0:
            print(self.__ram.get_dump())
        elif mode == 1:
            return self.__ram.get_dump()

    def signal_syscall(self, *args):
        if args:
            # halt
            if args[0].value == 0:
                self.__status = False
                self.result_code = args[1]
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
                    if self.__environment == "tui":
                        print(next_char.as_utf8(), end="")
                    elif self.__environment == "gui":
                        self.__console.insert("end", next_char.as_utf8())
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
                if self.__environment == "tui":
                    string = input("")
                elif self.__environment == "gui":
                    pass
                w: data_types.Word
                try:
                    if args[1].value == 0:
                        w = data_types.Word(0).from_binary(string)
                    elif args[1].value == 1:
                        w = data_types.Word(int(string))
                    elif args[1].value == 2:
                        w = data_types.Word(0).from_hex(string[:-1])
                    self.__cpu.registers["x3"] = w
                except Exception:
                    self.__cpu.registers["x4"] = data_types.Word(1)

