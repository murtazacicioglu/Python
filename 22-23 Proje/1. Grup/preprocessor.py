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
            
 
""" 
03.04.2023
İlgili işlemin tanımını içeren lambda fonksiyonlarını tutan dict oluşturup sonrasında for döngüsünde 
her bir değere anahtar üzerinden .items() metodunu kullanarak ulaşmak
"""
   
import re as regex

class Preprocessor:
    def __init__(self, _trimSpaces=True, _clearComments=True, _clearNewline=True):
        self.filters = {}
        if _trimSpaces:
            self.filters["trimSpaces"] = lambda b: regex.sub('[\t ]+', ' ', b).strip()
        if _clearComments:
            self.filters["clearComments"] = lambda b: regex.sub('\s*;.+', '', b)
        if _clearNewline:
            self.filters["clearNewline"] = lambda b: regex.sub('^(?:[\t ]*(?:\r?\n|\r))+', '', b)

    def format(self, buffer: str):
        """
        buffer'a girilen metni, nesnenin temizlik kurallarına göre işler ve işlenmiş string'i döndürür.
        """
        for filter_name, filter_func in self.filters.items():
            buffer = filter_func(buffer)
            print(buffer)
        return buffer
