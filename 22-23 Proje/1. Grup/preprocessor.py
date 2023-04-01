#!/usr/bin/env python3
#
#         Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#         Sabir SÜLEYMANLI <suleymanlisabir3@gmail.com>
#
import re as regex


class Preprocessor:
    def __init__(self, _trimSpaces=True, _clearComments=True, _clearNewline=True):
        self.trimSpaces = _trimSpaces
        self.clearComments = _clearComments
        self.clearNewline = _clearNewline


    def format(self, buffer: str):
        """
        buffer'a girilen metni, nesnenin temizlik kurallarına göre işler ve işlenmiş string'i döndürür.
        """
        if self.trimSpaces:
            buffer = regex.sub('[\t ]+', ' ', buffer).strip()
            print(buffer)
        if self.clearComments:
            buffer = regex.sub('\s*;.+', '', buffer)
            print(buffer)
        if self.clearNewline:
            buffer = regex.sub('^(?:[\t ]*(?:\r?\n|\r))+', '', buffer)
            print(buffer)
        return buffer
            
