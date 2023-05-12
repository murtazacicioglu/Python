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

    # noinspection PyMethodMayBeStatic
    def __parse_code(self, source_code: str) -> [str]:
        """
        RISC-Mini Assembly dialektini orta formata çeviren parser algoritmasını gerçekler.
        :param source_code: RISC-Mini dialektinde Assembly kodu içeren string
        :return: Çevrilmiş satırları içeren dizi
        """
        sections = {}
        intermediate_code = []

        for line in source_code.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('.'):
                section_name = line.strip('.')
                sections[section_name] = len(intermediate_code)
            else:
                instruction = line.split(maxsplit=1)
                if len(instruction) == 2:
                    operands = instruction[1].replace(',', '').split()
                    intermediate_code.append(f'{instruction[0]} {" ".join(operands)}')
                elif len(instruction) == 1:
                    intermediate_code.append(instruction[0])

        for i, line in enumerate(intermediate_code):
            if line[0:3] in BRANCHING:
                parts = line.split()
                section = parts[-1]
                if section in sections.keys():
                    parts[-1] = data_types.Word(sections[section]).as_hexadecimal() + "h"
                elif section.startswith("[") and section.endswith("]"):
                    inner = section[1:-1]
                    if "+" in inner:
                        ip = inner.split("+")
                        parts[-1] = data_types.Word(
                            sections[ip[0]] + data_types.Word(0).from_hex(ip[1][:-1]).value
                        ).as_hexadecimal() + "h"
                    else:
                        parts[-1] = data_types.Word(0).from_hex(inner[:-1]).as_hexadecimal() + "h"
                intermediate_code[i] = " ".join(parts)
        return intermediate_code

    def parse_code(self, source_code: str) -> None:
        """
        Kaynak kodu parse ederek orta formata çevirir ve __intermediate özelliğinde saklar.
        :param source_code: Assembly kaynak kodu
        """
        self.__intermediate = self.__parse_code(source_code)

    def load_to_memory(self, mem: memory.Memory) -> None:
        """
        __intermediate özelliğinde tutulan orta formattaki kodu verilen belleğe yükler.
        :param mem: Kodun yükleneceği bellek nesnesi
        """
        for line in self.__intermediate:
            mem.store_code(line)
