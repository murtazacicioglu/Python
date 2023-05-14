#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       memory.py
from data_types import Word


class Memory:
    def __init__(self):
        self.__lower_boundary = Word(0).from_binary("00000000000000000000000000000000")
        self.__upper_boundary = Word(0).from_binary("01111111111111111111111111111111")
        self.__memory = {}
        self.__code_memory = []

    def set_memory(self, address: Word, value: Word):
        if self.__lower_boundary.value > address.value or address.value > self.__upper_boundary.value:
            raise Exception("Erişilmek istenen adres izin verilen sınırların dışında")

        self.__memory[address.value] = value

    def read_memory(self, address: Word) -> Word:
        if self.__lower_boundary.value > address.value or address.value > self.__upper_boundary.value:
            raise Exception("Erişilmek istenen adres izin verilen sınırların dışında")

        if address.value not in self.__memory.keys():
            self.__memory[address.value] = Word(0)
            return Word(0)

        return self.__memory[address.value]

    def get_dump(self) -> str:
        lines = ["RAM Görüntüsü", "-" * 20]
        if not self.__memory.keys():
            lines.append("Bellek Boş!")
        else:
            for key, value in self.__memory.items():
                lines.append(f"{Word(key).as_hexadecimal()}h: {value.as_hexadecimal()}h")
        return "\n".join(lines)

    def store_code(self, line: str):
        self.__code_memory.append(line)

    def read_code(self, address: Word) -> str:
        if 0 > address.value or address.value >= len(self.__code_memory):
            raise Exception("Erişilmek istenen adres sınırların dışında")
        return self.__code_memory[address.value]
