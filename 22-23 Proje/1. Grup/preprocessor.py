#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#       Sabir SÜLEYMANLI <suleymanlisabir3@gmail.com>
#
#       preprocessor.py
import re as regex
import expressions


class Preprocessor:
    def __init__(self, trim_spaces=True, clear_comments=True, clear_newline=True):
        self.filters = {}
        if trim_spaces:
            self.filters["trim_spaces"] = lambda b: regex.sub(expressions.exp_preproc_space, ' ', b).strip()
        if clear_comments:
            self.filters["clear_comments"] = lambda b: regex.sub(expressions.exp_preproc_comment, '', b)
        if clear_newline:
            self.filters["clear_newline"] = lambda b: regex.sub(expressions.exp_preproc_newline, '', b)

    def format(self, buffer: str) -> str:
        """
        buffer'a girilen metni, nesnenin temizlik kurallarına göre işler ve işlenmiş string'i döndürür.
        """
        for filter_name, filter_func in self.filters.items():
            buffer = filter_func(buffer)
        return buffer
