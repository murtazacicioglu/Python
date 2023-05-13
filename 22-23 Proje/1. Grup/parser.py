#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       parser.py
import copy

import data_types
import memory
import preprocessor


BRANCHING = ["jmp", "beq", "bne", "bge", "ble"]
MEMACCESS = ["lfm", "stm", "mvi"]


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
        stores = {}
        intermediate_code = []
        current_section = ""
        section_offset = 0

        for line in source_code.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('.'):
                section_name = line.strip('.')
                sections[section_name] = len(intermediate_code)
                current_section = section_name
            elif current_section == "store" and line[0:3] == "dbs":
                parts = line.split(maxsplit=2)
                stores[parts[1].removesuffix(",")] = [len(parts[2]) - 1, parts[2], 0]
            else:
                instruction = line.split(maxsplit=1)
                if len(instruction) == 2:
                    operands = instruction[1].replace(',', '').split()
                    intermediate_code.append(f'{instruction[0]} {" ".join(operands)}')
                elif len(instruction) == 1:
                    intermediate_code.append(instruction[0])

        if stores.keys():
            temp = copy.deepcopy(intermediate_code)
            intermediate_code = []
            mem_offset = 0
            for key in stores.keys():
                stores[key][2] = mem_offset
                string = stores[key][1][1:-1]
                for char in string:
                    intermediate_code.append(f"mvi x1 {data_types.Word(0).from_utf8(char).as_hexadecimal()}h")
                    intermediate_code.append(f"stm x1 {data_types.Word(mem_offset).as_hexadecimal()}h")
                    mem_offset += 1
                intermediate_code.append(f"mov x1 x0")
                intermediate_code.append(f"stm x1 {data_types.Word(mem_offset).as_hexadecimal()}h")
                mem_offset += 1

            section_offset = len(intermediate_code)
            intermediate_code = intermediate_code + temp

        for i, line in enumerate(intermediate_code):
            if line[0:3] in BRANCHING or line[0:3] in MEMACCESS:
                parts = line.split()
                section = parts[-1]
                if section in sections.keys():
                    parts[-1] = data_types.Word(sections[section] + section_offset).as_hexadecimal() + "h"
                elif section.startswith("[") and section.endswith("]"):
                    inner = section[1:-1]
                    if inner in stores.keys():
                        parts[-1] = data_types.Word(stores[inner][2]).as_hexadecimal() + "h"
                    elif "+" in inner:
                        ip = inner.split("+")
                        parts[-1] = data_types.Word(
                            sections[ip[0]] + data_types.Word(0).from_hex(ip[1][:-1]).value + section_offset
                        ).as_hexadecimal() + "h"
                    else:
                        parts[-1] = data_types.Word(
                            data_types.Word(0).from_hex(inner[:-1]).value + section_offset
                        ).as_hexadecimal() + "h"
                intermediate_code[i] = " ".join(parts)

        return intermediate_code

    def parse_code(self, source_code: str) -> None:
        """
        Kaynak kodu parse ederek orta formata çevirir ve __intermediate özelliğinde saklar.
        :param source_code: Assembly kaynak kodu
        """
        pp = preprocessor.Preprocessor(trim_spaces=False, clear_newline=False)
        clean_code = pp.format(source_code)
        self.__intermediate = self.__parse_code(clean_code)

    def load_to_memory(self, mem: memory.Memory) -> None:
        """
        __intermediate özelliğinde tutulan orta formattaki kodu verilen belleğe yükler.
        :param mem: Kodun yükleneceği bellek nesnesi
        """
        for line in self.__intermediate:
            mem.store_code(line)
