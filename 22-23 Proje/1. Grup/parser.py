#!/usr/bin/env python
#
#       Ferit Yiğit BALABAN, <fybalaban@fybx.dev>
#
#       parser.py
import data_types

BRANCHING = ["jmp", "beq", "bne", "bge", "ble"]


def parse_code(source_code: str) -> str:
    sections = {}
    current_section = None
    intermediate_code = []

    for line in source_code.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('.'):
            section_name = line.strip('.')
            sections[section_name] = len(intermediate_code)
            current_section = section_name
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
    return '\n'.join(intermediate_code)


def main():
    sc = """.global
    mov x0, x0
    nop
    nop
    nop
    jmp mul
    lfm x0, [00000000h]
    stm x0, [01010000h]
    jmp global





.mul
    beq x1, x2, [10100000h]
    bne x1, x2, [global+11h]
    ble x1, x2, [mul+101h]







.nop
    nop
    nop
    nop
    nop
    nop
    jmp mul
"""

    print(parse_code(sc))


if __name__ == "__main__":
    main()
